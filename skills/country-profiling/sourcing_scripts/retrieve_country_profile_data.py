#!/usr/bin/env python3
"""Retrieve controlled baseline data and reviewed source artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import source_registry  # noqa: E402
import web_sources  # noqa: E402
import who_gho  # noqa: E402
import world_bank  # noqa: E402

DEFAULT_OUTPUT_DIR = SKILL_DIR / "retrieval-output" / "country-profile-data"
REGISTRY_PATH = SCRIPT_DIR / "indicator_registry.json"
REQUIREMENTS_PATH = SCRIPT_DIR / "requirements.txt"


class MissingPdfDependencyError(RuntimeError):
    """Raised when configured PDF parsing needs pypdf but it is unavailable."""


def web_artifact_output_dir(output_dir: Path) -> Path:
    return output_dir / "Parsed sources"


def pypdf_available() -> bool:
    return importlib.util.find_spec("pypdf") is not None


def target_requires_pdf_parsing(target: dict[str, Any]) -> bool:
    target_type = str(target.get("target_type", "html")).casefold()
    if target_type == "local_pdf":
        return True
    url = str(target.get("url", "")).casefold()
    return (
        bool(target.get("download_pdfs"))
        or url.endswith(".pdf")
        or ".pdf?" in url
        or "/bitstreams/" in url
    )


def pdf_dependency_error_message(source_targets: list[dict[str, Any]]) -> str:
    pdf_titles = [
        str(target.get("title") or "untitled PDF source")
        for target in source_targets
        if target_requires_pdf_parsing(target)
    ][:5]
    title_text = "; ".join(pdf_titles) if pdf_titles else "configured PDF sources"
    return (
        "PDF parsing dependency missing: pypdf is not installed, but this run "
        f"includes PDF-capable source targets ({title_text}). Stop and ask the "
        "user whether to install the dependency before retrieval continues.\n"
        f"Install command: {sys.executable} -m pip install -r {REQUIREMENTS_PATH}\n"
        "If the user declines installation, rerun this command with "
        "--allow-missing-pypdf and record PDF parsing as a runtime limitation."
    )


def require_pdf_dependency(
    source_targets: list[dict[str, Any]],
    *,
    allow_missing_pypdf: bool,
) -> None:
    if allow_missing_pypdf:
        return
    if not any(target_requires_pdf_parsing(target) for target in source_targets):
        return
    if not pypdf_available():
        raise MissingPdfDependencyError(pdf_dependency_error_message(source_targets))


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def markdown_table_row(values: list[Any]) -> str:
    cells = []
    for value in values:
        text = "" if value is None else str(value)
        cells.append(text.replace("|", "\\|").replace("\n", " "))
    return "| " + " | ".join(cells) + " |"


def write_indicators_markdown(bundle: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Retrieved baseline indicators: {bundle['country']} ({bundle['iso3']})",
        "",
        f"- Retrieval date: {bundle['retrieval_date']}",
        f"- Downstream focus: {bundle['focus'] or 'not specified'}",
        f"- Registry: {bundle['registry_path']}",
        "",
        (
            "These indicators provide a small baseline context layer. They do "
            "not prove country-profile completeness and must be combined with "
            "reviewed country documents, source inventories, and evidence gaps."
        ),
        "",
        "## World Bank indicators",
        "",
        "| Indicator | Code | Value | Unit | Year | Status | Failure type | Error | Source URL |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for item in bundle["world_bank_indicators"]:
        lines.append(
            markdown_table_row(
                [
                    item.get("label"),
                    item.get("indicator_code"),
                    item.get("value"),
                    item.get("unit"),
                    item.get("year"),
                    item.get("status"),
                    item.get("failure_type", ""),
                    item.get("error", ""),
                    item.get("url"),
                ]
            )
        )

    lines.extend(
        [
            "",
            "## WHO GHO indicators",
            "",
        ]
    )
    if bundle["who_gho_indicators"]:
        lines.extend(
            [
                (
                    "| Indicator | Code | Value | Unit | Year | Status | "
                    "Failure type | Error | Source URL |"
                ),
                "|---|---|---|---|---|---|---|---|---|",
            ]
        )
        for item in bundle["who_gho_indicators"]:
            lines.append(
                markdown_table_row(
                    [
                        item.get("label"),
                        item.get("indicator_code"),
                        item.get("value"),
                        item.get("unit"),
                        item.get("year"),
                        item.get("status"),
                        item.get("failure_type", ""),
                        item.get("error", ""),
                        item.get("url"),
                    ]
                )
            )
    else:
        lines.append("No WHO GHO indicators are configured for this focus.")

    lines.extend(
        [
            "",
            "## Retrieval caveats",
            "",
            "- Use precise indicator source, code, year, and retrieval date in profile claims.",
            (
                "- `missing_value` means the configured indicator did not "
                "return a non-empty country value."
            ),
            (
                "- `network_failed` means DNS, timeout, or outbound-network "
                "retrieval failed and should be recorded as an evidence gap."
            ),
            (
                "- `failed` means non-network retrieval failed and should be "
                "recorded as an evidence gap."
            ),
            (
                "- WHO GHO retrieval is intentionally limited to configured "
                "indicator codes; it is not a full GHO data platform."
            ),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_web_reviewed_markdown(bundle: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Web-reviewed sources: {bundle['country']} ({bundle['iso3']})",
        "",
        f"- Retrieval date: {bundle['retrieval_date']}",
        f"- Downstream focus: {bundle['focus'] or 'not specified'}",
        f"- Source manifest: {bundle['source_manifest'].get('path') or 'not supplied'}",
        f"- Stable source targets: {bundle['stable_source_target_count']}",
        f"- Manifest source targets: {bundle['source_manifest'].get('target_count', 0)}",
        "",
        (
            "This artifact records sources that the script actually opened, "
            "downloaded, or parsed. A landing page remains a landing page "
            "unless its evidence-bearing text or linked PDF was retrieved."
        ),
        "",
        (
            "| Title | Publisher | Source class | Source type | Date | Status | "
            "Failure type | URL or file path | Material endpoint | Parse status |"
        ),
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    if not bundle["web_reviewed_sources"]:
        if (
            not bundle["source_manifest"].get("path")
            and not bundle["stable_source_target_count"]
        ):
            lines.extend(
                [
                    "",
                    (
                        "_No web/PDF source targets were supplied or configured. "
                        "Use controlled web-assisted retrieval to discover "
                        "country-specific official sources, then pass them with "
                        "`--source-manifest`._"
                    ),
                ]
            )
        elif (
            bundle["source_manifest"].get("path")
            and not bundle["source_manifest"].get("target_count")
        ):
            lines.extend(
                [
                    "",
                    (
                        "_A source manifest was supplied, but no entries "
                        "matched the requested country/ISO3/focus._"
                    ),
                ]
            )
    for item in bundle["web_reviewed_sources"]:
        path_or_url = item.get("local_file_path") or item.get("url")
        lines.append(
            markdown_table_row(
                [
                    item.get("title"),
                    item.get("publisher"),
                    item.get("source_class"),
                    item.get("source_type"),
                    item.get("date"),
                    item.get("status"),
                    item.get("failure_type", ""),
                    path_or_url,
                    item.get("material_endpoint", ""),
                    item.get("parse_status"),
                ]
            )
        )

    lines.extend(["", "## Extracted text summaries", ""])
    for item in bundle["web_reviewed_sources"]:
        lines.extend(
            [
                f"### {item.get('title', 'Untitled source')}",
                "",
                f"- URL: {item.get('url', '')}",
                f"- Local file path: {item.get('local_file_path') or 'not applicable'}",
                f"- SHA-256: {item.get('sha256') or 'not applicable'}",
                f"- Status: {item.get('status')}",
                "",
                item.get("text_summary") or "_No extracted text summary available._",
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_source_leads_markdown(bundle: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Unresolved source gaps: {bundle['country']} ({bundle['iso3']})",
        "",
        f"- Retrieval date: {bundle['retrieval_date']}",
        f"- Downstream focus: {bundle['focus'] or 'not specified'}",
        "",
        (
            "This file is intentionally short. It lists only unresolved source "
            "classes that remain useful after deterministic dataset retrieval "
            "and configured web/PDF source resolution."
        ),
        "",
        "| Source class | Why needed | Suggested action | Status |",
        "|---|---|---|---|",
    ]
    gaps = bundle["source_gaps"][: bundle["max_source_gaps"]]
    if gaps:
        for gap in gaps:
            lines.append(
                markdown_table_row(
                    [
                        gap.get("source_class"),
                        gap.get("why_needed"),
                        gap.get("suggested_action"),
                        gap.get("status"),
                    ]
                )
            )
    else:
        lines.append(
            "| None recorded | Configured retrieval did not leave additional "
            "generic source gaps. | Continue with human review of retrieved "
            "artifacts. | Reviewed |"
        )

    lines.extend(
        [
            "",
            "## Web-assisted fallback note",
            "",
            (
                "If scripts or configured resolvers are unavailable, use "
                "`context/web-assisted-retrieval.md`: follow the approved "
                "source priority list, record provenance and status, separate "
                "reviewed evidence from candidate leads, and keep inaccessible "
                "PDFs or landing-page-only sources as evidence gaps."
            ),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    retrieval_date = now_utc()
    stable_targets = source_registry.stable_source_targets(
        args.country,
        args.iso3,
        args.focus,
    )
    manifest_targets: list[dict[str, Any]] = []
    manifest_summary: dict[str, Any] = {
        "path": "",
        "source_count": 0,
        "target_count": 0,
        "skipped_count": 0,
    }
    if args.source_manifest:
        manifest_targets, manifest_summary = source_registry.load_source_manifest(
            args.source_manifest,
            country=args.country,
            iso3=args.iso3,
            focus=args.focus,
        )
    source_targets = stable_targets + manifest_targets
    require_pdf_dependency(
        source_targets,
        allow_missing_pypdf=args.allow_missing_pypdf,
    )

    registry = world_bank.load_registry(REGISTRY_PATH)
    world_bank_results = world_bank.fetch_registry_indicators(
        args.iso3,
        registry,
        timeout=args.timeout,
        retrieval_date=retrieval_date,
    )
    who_results = who_gho.fetch_configured_indicators(
        args.country,
        args.iso3,
        args.focus,
        timeout=args.timeout,
        retrieval_date=retrieval_date,
    )

    flat_output = True
    web_output_dir = web_artifact_output_dir(Path(args.output_dir))
    web_records = web_sources.resolve_sources(
        source_targets,
        output_dir=web_output_dir,
        flat_output=flat_output,
        timeout=args.timeout,
        retrieval_date=retrieval_date,
        repo_root=REPO_ROOT,
    )
    gaps = source_registry.unresolved_source_gaps(
        args.country,
        args.iso3,
        args.focus,
        web_records=web_records,
    )

    return {
        "country": args.country,
        "iso3": args.iso3.upper(),
        "focus": args.focus,
        "retrieval_date": retrieval_date,
        "registry_path": display_path(REGISTRY_PATH),
        "world_bank_indicators": world_bank_results,
        "who_gho_indicators": who_results,
        "web_reviewed_sources": web_records,
        "source_gaps": gaps,
        "max_source_gaps": args.max_source_gaps,
        "source_manifest": manifest_summary,
        "stable_source_target_count": len(stable_targets),
        "manifest_source_target_count": len(manifest_targets),
    }


def indicator_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "country": bundle["country"],
        "iso3": bundle["iso3"],
        "focus": bundle["focus"],
        "retrieval_date": bundle["retrieval_date"],
        "registry_path": bundle["registry_path"],
        "world_bank_indicators": bundle["world_bank_indicators"],
        "who_gho_indicators": bundle["who_gho_indicators"],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve a controlled Country Profiling baseline bundle: World "
            "Bank indicators, configured WHO GHO indicators, reviewed web/PDF "
            "source artifacts, and short unresolved source gaps."
        )
    )
    parser.add_argument("--country", required=True, help="Country name.")
    parser.add_argument("--iso3", required=True, help="ISO3 country code.")
    parser.add_argument(
        "--focus",
        default="",
        help="Optional downstream focus, e.g. immunization.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=(
            "Directory for retrieved-indicators, web-reviewed-sources, and "
            "source-leads artifacts."
        ),
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--source-manifest",
        default="",
        help=(
            "Optional JSON manifest of Agent-discovered country-specific sources to resolve. "
            "Use this for national ministry, public-health, statistics, "
            "policy, digital health, and programme sources."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero if all configured network-backed indicator retrieval fails.",
    )
    parser.add_argument(
        "--max-source-gaps",
        type=int,
        default=12,
        help="Maximum unresolved source gaps to write to source-leads.md.",
    )
    parser.add_argument(
        "--flat-output",
        action="store_true",
        help=(
            "Deprecated compatibility flag. Retrieval artifacts are now always "
            "written to --output-dir, with downloaded/parsed PDFs under "
            "'Parsed sources'."
        ),
    )
    parser.add_argument(
        "--allow-missing-pypdf",
        action="store_true",
        help=(
            "Continue without pypdf when configured PDF sources are present. "
            "Use only after the user declines dependency installation; PDFs "
            "will be marked as not parsed."
        ),
    )
    args = parser.parse_args(argv[1:])

    output_dir = Path(args.output_dir)

    try:
        bundle = build_bundle(args)
    except MissingPdfDependencyError as exc:
        print(f"ERROR: {exc}")
        return 3

    output_dir.mkdir(parents=True, exist_ok=True)
    indicators_json = output_dir / "retrieved-indicators.json"
    indicators_md = output_dir / "retrieved-indicators.md"
    web_json = output_dir / "web-reviewed-sources.json"
    web_md = output_dir / "web-reviewed-sources.md"
    source_leads_md = output_dir / "source-leads.md"

    indicators_json.write_text(
        json.dumps(indicator_bundle(bundle), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_indicators_markdown(bundle, indicators_md)
    web_json.write_text(
        json.dumps(bundle["web_reviewed_sources"], indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_web_reviewed_markdown(bundle, web_md)
    write_source_leads_markdown(bundle, source_leads_md)

    wb_retrieved = sum(
        1
        for item in bundle["world_bank_indicators"]
        if item.get("status") == "retrieved"
    )
    wb_total = len(bundle["world_bank_indicators"])
    gho_retrieved = sum(
        1
        for item in bundle["who_gho_indicators"]
        if item.get("status") == "retrieved"
    )
    gho_total = len(bundle["who_gho_indicators"])
    web_reviewed = sum(
        1
        for item in bundle["web_reviewed_sources"]
        if item.get("status") in {"reviewed_html", "parsed"}
    )
    print(f"Wrote {display_path(indicators_json)}")
    print(f"Wrote {display_path(indicators_md)}")
    print(f"Wrote {display_path(web_json)}")
    print(f"Wrote {display_path(web_md)}")
    print(f"Wrote {display_path(source_leads_md)}")
    print(f"World Bank indicators retrieved: {wb_retrieved}/{wb_total}")
    print(f"WHO GHO indicators retrieved: {gho_retrieved}/{gho_total}")
    print(
        "Web/PDF sources reviewed or parsed: "
        f"{web_reviewed}/{len(bundle['web_reviewed_sources'])}"
    )
    if wb_retrieved < wb_total or gho_retrieved < gho_total:
        print("Some indicators were missing or failed; carry them into evidence gaps.")
    if (
        args.strict
        and (wb_total + gho_total)
        and (wb_retrieved + gho_retrieved == 0)
    ):
        print("Strict mode failed: no configured network-backed indicators were retrieved.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
