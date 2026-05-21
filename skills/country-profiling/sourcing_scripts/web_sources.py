"""Institutional web and PDF source resolution for Country Profiling."""

from __future__ import annotations

import datetime as dt
import hashlib
import html
import re
from io import BytesIO
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

import network_errors

USER_AGENT = "who-smart-localization/0.1"
SKILL_DIR = Path(__file__).resolve().parent.parent
SOURCE_METADATA_KEYS = (
    "source_class",
    "evidence_role",
    "retrieval_priority",
    "intent",
    "reviewed_intent",
)
PDF_TEXT_FINGERPRINT_MIN_CHARS = 500
PDF_TEXT_FINGERPRINT_MAX_CHARS = 100_000


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def slugify(value: str, fallback: str = "source") -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:80] or fallback


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


class HTMLTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.links: list[dict[str, str]] = []
        self._current_link: dict[str, str] | None = None
        self._in_title = False
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return
        if tag == "title":
            self._in_title = True
        if tag == "a":
            self._current_link = {"href": attr_map.get("href", ""), "text": ""}

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = clean_text(data)
        if not text:
            return
        if self._in_title:
            self.title_parts.append(text)
        if self._current_link is not None:
            self._current_link["text"] += f" {text}"
        self.text_parts.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if tag == "title":
            self._in_title = False
        if tag == "a" and self._current_link is not None:
            self._current_link["text"] = clean_text(self._current_link["text"])
            self.links.append(self._current_link)
            self._current_link = None


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def fetch_bytes(url: str, timeout: int) -> tuple[bytes, str, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()
        return response.read(), content_type, final_url


def source_metadata(target: dict[str, Any]) -> dict[str, Any]:
    return {
        key: target.get(key, "")
        for key in SOURCE_METADATA_KEYS
        if target.get(key) is not None
    }


def parse_html(content: bytes, base_url: str) -> dict[str, Any]:
    text = content.decode("utf-8", "replace")
    parser = HTMLTextParser()
    parser.feed(text)
    links = []
    for link in parser.links:
        href = link.get("href", "")
        if not href:
            continue
        links.append({"text": link.get("text", ""), "url": urljoin(base_url, href)})
    return {
        "title": clean_text(" ".join(parser.title_parts)),
        "text": clean_text(" ".join(parser.text_parts)),
        "links": links,
    }


def excerpt_from_text(
    text: str,
    keywords: list[str] | None = None,
    *,
    max_chars: int = 2000,
) -> str:
    if not text:
        return ""
    lowered = text.casefold()
    for keyword in keywords or []:
        index = lowered.find(keyword.casefold())
        if index >= 0:
            return text[index : index + max_chars].strip()
    return text[:max_chars].strip()


def parse_pdf(path: Path, *, max_pages: int = 8, max_chars: int = 5000) -> tuple[str, str]:
    try:
        from pypdf import PdfReader
    except Exception as exc:
        return (
            "",
            "pypdf is not installed; the Agent should stop and ask the user "
            "whether to install skills/country-profiling/sourcing_scripts/"
            f"requirements.txt before PDF-capable retrieval continues: {exc}",
        )

    try:
        reader = PdfReader(str(path))
        parts = []
        for page in reader.pages[:max_pages]:
            parts.append(page.extract_text() or "")
            if sum(len(part) for part in parts) >= max_chars:
                break
        return clean_text(" ".join(parts))[:max_chars], ""
    except Exception as exc:
        return "", str(exc)


def pdf_text_fingerprint_from_reader(reader: Any) -> str:
    parts = []
    total_chars = 0
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
        total_chars += len(text)
        if total_chars >= PDF_TEXT_FINGERPRINT_MAX_CHARS:
            break
    normalized = clean_text(" ".join(parts)).casefold()
    if len(normalized) < PDF_TEXT_FINGERPRINT_MIN_CHARS:
        return ""
    normalized = normalized[:PDF_TEXT_FINGERPRINT_MAX_CHARS]
    return sha256_bytes(normalized.encode("utf-8"))


def pdf_text_fingerprint_from_path(path: Path) -> str:
    try:
        from pypdf import PdfReader

        return pdf_text_fingerprint_from_reader(PdfReader(str(path)))
    except Exception:
        return ""


def pdf_text_fingerprint_from_bytes(content: bytes) -> str:
    try:
        from pypdf import PdfReader

        return pdf_text_fingerprint_from_reader(PdfReader(BytesIO(content)))
    except Exception:
        return ""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def write_pdf_once(
    *,
    title: str,
    url: str,
    content: bytes,
    output_dir: Path,
) -> tuple[Path, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    digest = sha256_bytes(content)
    for existing_path in sorted(output_dir.glob("*.pdf")):
        if sha256_file(existing_path) == digest:
            return existing_path, digest

    text_fingerprint = pdf_text_fingerprint_from_bytes(content)
    if text_fingerprint:
        for existing_path in sorted(output_dir.glob("*.pdf")):
            if pdf_text_fingerprint_from_path(existing_path) == text_fingerprint:
                return existing_path, sha256_file(existing_path)

    base_slug = slugify(title)
    primary = output_dir / f"{base_slug}.pdf"
    path = primary
    if primary.exists() and sha256_file(primary) != digest:
        url_digest = sha256_bytes(url.encode("utf-8"))[:10] if url else digest[:10]
        path = output_dir / f"{base_slug}-{url_digest}.pdf"
        if path.exists() and sha256_file(path) != digest:
            path = output_dir / f"{base_slug}-{digest[:10]}.pdf"
    if path.exists() and sha256_file(path) != digest:
        raise FileExistsError(f"PDF output path already exists with different content: {path}")
    if not path.exists():
        path.write_bytes(content)
    return path, digest


def looks_like_pdf(url: str, content: bytes, content_type: str) -> bool:
    parsed = urlparse(url)
    return (
        "pdf" in content_type.casefold()
        or parsed.path.casefold().endswith(".pdf")
        or content.startswith(b"%PDF")
    )


def selected_pdf_links(links: list[dict[str, str]], max_downloads: int) -> list[dict[str, str]]:
    selected = []
    seen = set()
    previous_title = ""
    for link in links:
        label = link.get("text", "")
        url = link.get("url", "")
        haystack = f"{label} {url}".casefold()
        if not url or url in seen:
            continue
        if "download" in haystack or ".pdf" in haystack or "/bitstreams/" in haystack:
            if label.casefold() == "download" and previous_title:
                link = dict(link)
                link["text"] = previous_title
            selected.append(link)
            seen.add(url)
        if len(selected) >= max_downloads:
            break
        if label and label.casefold() not in {"download", "read more", "view", "sign up"}:
            previous_title = label
    return selected


def pdf_record_from_bytes(
    *,
    title: str,
    publisher: str,
    source_type: str,
    url: str,
    content: bytes,
    output_dir: Path,
    retrieval_date: str,
    repo_root: Path,
    date: str = "",
    source_url: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path, digest = write_pdf_once(
        title=title,
        url=url,
        content=content,
        output_dir=output_dir,
    )
    extracted_text, parse_error = parse_pdf(path)
    status = "parsed" if extracted_text else "downloaded_parse_failed"
    record = {
        "title": title,
        "publisher": publisher,
        "source_type": source_type,
        "url": url,
        "source_page_url": source_url,
        "material_endpoint": url,
        "material_endpoint_type": "pdf",
        "date": date,
        "retrieval_date": retrieval_date,
        "status": status,
        "local_file_path": display_path(path, repo_root),
        "parse_status": "parsed" if extracted_text else "failed",
        "parse_error": parse_error,
        "text_summary": extracted_text[:2000],
        "review_status": "reviewed" if extracted_text else "downloaded_not_parsed",
        "sha256": digest,
    }
    record.update(metadata or {})
    return record


def local_pdf_record(
    target: dict[str, Any],
    *,
    output_dir: Path,
    retrieval_date: str,
    repo_root: Path,
) -> dict[str, Any]:
    target_path = Path(target["path"])
    candidates = (
        [target_path]
        if target_path.is_absolute()
        else [repo_root / target_path, SKILL_DIR / target_path]
    )
    path = next((candidate for candidate in candidates if candidate.is_file()), candidates[0])
    if not path.is_file():
        record = {
            "title": target["title"],
            "publisher": target["publisher"],
            "source_type": target["source_type"],
            "url": target["path"],
            "material_endpoint": target["path"],
            "material_endpoint_type": "local_pdf",
            "date": target.get("date", ""),
            "retrieval_date": retrieval_date,
            "status": "retrieval_failed",
            "local_file_path": target["path"],
            "sha256": "",
            "parse_status": "not_parsed",
            "parse_error": "Local file was not found.",
            "text_summary": "",
            "review_status": "missing",
        }
        record.update(source_metadata(target))
        return record
    output_path, digest = write_pdf_once(
        title=target["title"],
        url=target["path"],
        content=path.read_bytes(),
        output_dir=output_dir,
    )
    extracted_text, parse_error = parse_pdf(output_path)
    record = {
        "title": target["title"],
        "publisher": target["publisher"],
        "source_type": target["source_type"],
        "url": target["path"],
        "material_endpoint": display_path(path, repo_root),
        "material_endpoint_type": "local_pdf",
        "date": target.get("date", ""),
        "retrieval_date": retrieval_date,
        "status": "parsed" if extracted_text else "downloaded_parse_failed",
        "local_file_path": display_path(output_path, repo_root),
        "sha256": digest,
        "parse_status": "parsed" if extracted_text else "failed",
        "parse_error": parse_error,
        "text_summary": extracted_text[:2000],
        "review_status": "reviewed" if extracted_text else "available_not_parsed",
    }
    record.update(source_metadata(target))
    return record


def resolve_html_target(
    target: dict[str, Any],
    *,
    output_dir: Path,
    flat_output: bool = False,
    timeout: int,
    retrieval_date: str,
    repo_root: Path,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        content, content_type, final_url = fetch_bytes(target["url"], timeout)
    except Exception as exc:
        record = {
            "title": target["title"],
            "publisher": target["publisher"],
            "source_type": target["source_type"],
            "url": target["url"],
            "material_endpoint": target["url"],
            "material_endpoint_type": "unresolved",
            "date": target.get("date", ""),
            "retrieval_date": retrieval_date,
            "status": network_errors.status_for_exception(exc),
            "local_file_path": "",
            "sha256": "",
            "parse_status": "not_parsed",
            "failure_type": network_errors.classify_exception(exc),
            "parse_error": str(exc),
            "text_summary": "",
            "review_status": "failed",
        }
        record.update(source_metadata(target))
        return [record]

    if looks_like_pdf(final_url, content, content_type):
        return [
            pdf_record_from_bytes(
                title=target["title"],
                publisher=target["publisher"],
                source_type=target["source_type"],
                url=final_url,
                content=content,
                output_dir=output_dir,
                retrieval_date=retrieval_date,
                repo_root=repo_root,
                date=target.get("date", ""),
                metadata=source_metadata(target),
            )
        ]

    parsed = parse_html(content, final_url)
    text_summary = excerpt_from_text(
        parsed["text"],
        target.get("excerpt_keywords", []),
        max_chars=target.get("max_summary_chars", 2000),
    )
    html_record = {
        "title": target["title"],
        "page_title": parsed["title"],
        "publisher": target["publisher"],
        "source_type": target["source_type"],
        "url": final_url,
        "material_endpoint": final_url,
        "material_endpoint_type": "full_text_html",
        "date": target.get("date", ""),
        "retrieval_date": retrieval_date,
        "status": "reviewed_html" if text_summary else "retrieved_empty",
        "local_file_path": "",
        "sha256": hashlib.sha256(content).hexdigest(),
        "parse_status": "html_extracted" if text_summary else "empty",
        "parse_error": "",
        "text_summary": text_summary,
        "review_status": "reviewed" if text_summary else "empty",
        "discovered_links": selected_pdf_links(
            parsed["links"],
            int(target.get("max_downloads", 0)),
        ),
    }
    html_record.update(source_metadata(target))
    records.append(html_record)

    if target.get("download_pdfs"):
        pdf_dir = output_dir if flat_output else output_dir / "downloads"
        for index, link in enumerate(
            selected_pdf_links(parsed["links"], int(target.get("max_downloads", 3))),
            start=1,
        ):
            try:
                pdf_content, pdf_content_type, final_pdf_url = fetch_bytes(link["url"], timeout)
            except Exception as exc:
                record = {
                    "title": link.get("text") or f"{target['title']} PDF {index}",
                    "publisher": target["publisher"],
                    "source_type": "Official or institutional PDF",
                    "url": link["url"],
                    "source_page_url": final_url,
                    "material_endpoint": link["url"],
                    "material_endpoint_type": "unresolved_pdf",
                    "date": target.get("date", ""),
                    "retrieval_date": retrieval_date,
                    "status": network_errors.status_for_exception(exc),
                    "local_file_path": "",
                    "sha256": "",
                    "parse_status": "not_parsed",
                    "failure_type": network_errors.classify_exception(exc),
                    "parse_error": str(exc),
                    "text_summary": "",
                    "review_status": "failed",
                }
                record.update(source_metadata(target))
                records.append(record)
                continue
            if not looks_like_pdf(final_pdf_url, pdf_content, pdf_content_type):
                continue
            records.append(
                pdf_record_from_bytes(
                    title=link.get("text") or f"{target['title']} PDF {index}",
                    publisher=target["publisher"],
                    source_type="Official or institutional PDF",
                    url=final_pdf_url,
                    content=pdf_content,
                    output_dir=pdf_dir,
                    retrieval_date=retrieval_date,
                    repo_root=repo_root,
                    date=target.get("date", ""),
                    source_url=final_url,
                    metadata=source_metadata(target),
                )
            )
    return records


def resolve_sources(
    targets: list[dict[str, Any]],
    *,
    output_dir: Path,
    flat_output: bool = False,
    timeout: int = 30,
    retrieval_date: str | None = None,
    repo_root: Path,
) -> list[dict[str, Any]]:
    retrieval_date = retrieval_date or now_utc()
    records: list[dict[str, Any]] = []
    for target in targets:
        target_type = target.get("target_type", "html")
        if target_type == "local_pdf":
            records.append(
                local_pdf_record(
                    target,
                    output_dir=output_dir,
                    retrieval_date=retrieval_date,
                    repo_root=repo_root,
                )
            )
        else:
            records.extend(
                resolve_html_target(
                    target,
                    output_dir=output_dir,
                    flat_output=flat_output,
                    timeout=timeout,
                    retrieval_date=retrieval_date,
                    repo_root=repo_root,
                )
            )
    return records
