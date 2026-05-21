#!/usr/bin/env python3
"""Validate the structure of a Country Profiling markdown output.

This validator checks format and controlled values only. It does not assess
epidemiological, policy, country, legal, WASH, or WHO interpretation correctness.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "# Country healthcare profile:",
    "## Profile metadata",
    "## Executive summary",
    "## Source inventory",
    "## Country context snapshot",
    "## Population health overview",
    "## Main health issues and burden",
    "## Health system organization and capacity",
    "## Healthcare access and coverage",
    "## Sanitary conditions and environmental health",
    "## Health financing and affordability",
    "## Health workforce, infrastructure, and supply availability",
    "## Digital health and health information systems",
    "## Equity, vulnerable groups, and regional variation",
    "## Current concerns, risks, and watchpoints",
    "## Policy-analysis readiness",
    "## Evidence gaps and expert input needed",
    "## Sources",
]

SOURCE_COLUMNS = [
    "Source",
    "Source type",
    "Publisher",
    "Date",
    "URL or file path",
    "Relevance",
    "Status",
]

GAP_COLUMNS = [
    "Gap or uncertainty",
    "Why it matters",
    "Suggested next source or action",
    "Review owner",
]

HANDOFF_COLUMNS = [
    "Downstream need",
    "Why it matters",
    "Available evidence",
    "Missing source or uncertainty",
    "Suggested next action",
]

ALLOWED_SOURCE_STATUS = {
    "Reviewed",
    "Candidate source",
    "Needs retrieval",
    "Needs expert validation",
    "Not available in supplied material",
}

ALLOWED_RETRIEVAL_MODE = {
    "document-only",
    "deterministic script-assisted",
    "semi-deterministic web-assisted",
    "mixed",
}

ALLOWED_PROFILE_EVIDENCE_LEVEL = {
    "full profile",
    "limited profile",
    "skeleton/gap-analysis profile",
}

REQUIRED_METADATA_LABELS = [
    "Country",
    "Optional downstream health-area focus, region, or population group",
    "Profile date",
    "Profile author or agent",
    "Intended downstream use",
    "Retrieval mode",
    "Profile evidence level",
    "Retrieval date",
    "Retrieved indicator bundle path, if available",
    "Source lead bundle path, if available",
    "Web-reviewed source inventory path or note, if available",
    "Source manifest path or note, if available",
    "Known input limitations",
]


def parse_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def find_table(lines: list[str], columns: list[str]) -> int | None:
    for index, line in enumerate(lines):
        if parse_markdown_row(line) == columns:
            return index
    return None


def separator_is_valid(line: str, expected_columns: int) -> bool:
    cells = parse_markdown_row(line)
    return len(cells) == expected_columns and all(
        cell and set(cell) <= {"-", ":"} for cell in cells
    )


def table_rows(lines: list[str], header_index: int) -> list[tuple[int, list[str]]]:
    rows: list[tuple[int, list[str]]] = []
    for line_number, line in enumerate(lines[header_index + 2 :], start=header_index + 3):
        if not line.strip():
            break
        row = parse_markdown_row(line)
        if not row:
            break
        rows.append((line_number, row))
    return rows


def validate_table(
    lines: list[str],
    columns: list[str],
    table_name: str,
    *,
    require_rows: bool = False,
) -> tuple[list[str], list[tuple[int, list[str]]]]:
    errors: list[str] = []
    header_index = find_table(lines, columns)
    if header_index is None:
        return [f"{table_name} table header was not found."], []

    if header_index + 1 >= len(lines) or not separator_is_valid(
        lines[header_index + 1], len(columns)
    ):
        errors.append(f"{table_name} table separator row is missing or malformed.")
        return errors, []

    rows = table_rows(lines, header_index)
    if require_rows and not rows:
        errors.append(f"{table_name} table has no data rows.")
    return errors, rows


def section_exists(content: str, heading: str) -> bool:
    return heading in content


def metadata_value(lines: list[str], label: str) -> str | None:
    prefix = f"- {label}:"
    for line in lines:
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return None


def validate_profile_metadata(lines: list[str]) -> list[str]:
    errors: list[str] = []
    for label in REQUIRED_METADATA_LABELS:
        value = metadata_value(lines, label)
        if value is None:
            errors.append(f"Profile metadata is missing: {label}.")
        elif not value:
            errors.append(f"Profile metadata field is empty: {label}.")

    retrieval_mode = metadata_value(lines, "Retrieval mode")
    if retrieval_mode and retrieval_mode not in ALLOWED_RETRIEVAL_MODE:
        allowed = ", ".join(sorted(ALLOWED_RETRIEVAL_MODE))
        errors.append(
            "Retrieval mode must be one of "
            f"{allowed}; found '{retrieval_mode}'."
        )

    evidence_level = metadata_value(lines, "Profile evidence level")
    if evidence_level and evidence_level not in ALLOWED_PROFILE_EVIDENCE_LEVEL:
        allowed = ", ".join(sorted(ALLOWED_PROFILE_EVIDENCE_LEVEL))
        errors.append(
            "Profile evidence level must be one of "
            f"{allowed}; found '{evidence_level}'."
        )
    return errors


def repo_root_for(path: Path) -> Path:
    starts = [path.resolve().parent, Path.cwd().resolve()]
    for start in starts:
        for candidate in [start, *start.parents]:
            if (candidate / ".git").exists():
                return candidate
    for start in starts:
        for candidate in [start, *start.parents]:
            if (candidate / "skills" / "country-profiling").exists():
                return candidate
    return path.resolve().parent


def skill_root_for(path: Path) -> Path:
    repo_root = repo_root_for(path)
    skill_root = repo_root / "skills" / "country-profiling"
    if skill_root.exists():
        return skill_root
    for candidate in [path.resolve().parent, *path.resolve().parents]:
        if candidate.name == "country-profiling":
            return candidate
    return repo_root


def is_url(value: str) -> bool:
    return value.startswith(("http://", "https://"))


def normalize_candidate_path(value: str) -> str:
    return value.strip().strip(".,;:)").strip()


def looks_like_local_path(value: str) -> bool:
    if not value or is_url(value):
        return False
    return (
        "/" in value
        or value.endswith((".md", ".json", ".pdf", ".txt", ".csv", ".xlsx"))
    )


def path_candidates(cell: str) -> list[str]:
    candidates: list[str] = []
    for value in re.findall(r"`([^`]+)`", cell):
        candidate = normalize_candidate_path(value)
        if looks_like_local_path(candidate):
            candidates.append(candidate)

    for value in re.findall(r"\[[^\]]+\]\(([^)]+)\)", cell):
        candidate = normalize_candidate_path(value)
        if looks_like_local_path(candidate):
            candidates.append(candidate)

    plain_cell = re.sub(r"`([^`]+)`", " ", cell)
    plain_cell = re.sub(r"\[[^\]]+\]\(([^)]+)\)", " ", plain_cell)
    for value in re.split(r"[\s,;]+", plain_cell):
        candidate = normalize_candidate_path(value)
        if looks_like_local_path(candidate):
            candidates.append(candidate)

    deduped = []
    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        deduped.append(candidate)
    return deduped


def resolve_local_path(candidate: str, target: Path) -> Path | None:
    path = Path(candidate)
    if path.is_absolute():
        return path if path.exists() else None

    repo_root = repo_root_for(target)
    skill_root = skill_root_for(target)
    search_roots = [
        target.resolve().parent,
        repo_root,
        skill_root,
    ]
    for root in search_roots:
        resolved = root / path
        if resolved.exists():
            return resolved
    return None


def reviewed_source_warnings_and_errors(
    target: Path,
    source_rows: list[tuple[int, list[str]]],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for line_number, row in source_rows:
        if len(row) != len(SOURCE_COLUMNS):
            continue
        source_type = row[1]
        locator = row[4]
        status = row[6]
        if status == "Reviewed" and not locator.strip():
            errors.append(
                f"Line {line_number}: Reviewed source has no URL or file path."
            )
        if status == "Reviewed" and source_type == "Landing page":
            errors.append(
                f"Line {line_number}: Landing page cannot be marked Reviewed "
                "unless the evidence-bearing material was reviewed."
            )
        for candidate in path_candidates(locator):
            path = resolve_local_path(candidate, target)
            if path is None:
                warnings.append(
                    f"Line {line_number}: referenced local path does not "
                    f"exist: {candidate}"
                )
            elif path.name == "web-reviewed-sources.md":
                text = path.read_text(encoding="utf-8", errors="replace")
                if "_No web/PDF source targets were supplied" in text:
                    warnings.append(
                        f"Line {line_number}: referenced web-reviewed source "
                        "artifact has no supplied or configured targets."
                    )
                if "_A source manifest was supplied, but no entries matched" in text:
                    warnings.append(
                        f"Line {line_number}: referenced web-reviewed source "
                        "artifact has no matching manifest entries."
                    )
    return warnings, errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the markdown structure and limited source-artifact "
            "semantics of a Country Profiling output. This does not validate "
            "epidemiological, policy, country, legal, WASH, or WHO correctness."
        )
    )
    parser.add_argument(
        "markdown_file",
        help="Country profile markdown file to validate.",
    )
    args = parser.parse_args(argv[1:])

    target = Path(args.markdown_file)
    if not target.is_file():
        print(f"Error: file not found: {target}")
        print(
            "Note: this validator checks structure and limited source-artifact "
            "semantics only, not epidemiological, policy, country, legal, "
            "WASH, or WHO correctness."
        )
        return 1

    content = target.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors: list[str] = []
    warnings: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"Required section missing: {section}")

    errors.extend(validate_profile_metadata(lines))

    source_errors, source_rows = validate_table(
        lines,
        SOURCE_COLUMNS,
        "Source inventory",
    )
    errors.extend(source_errors)
    for line_number, row in source_rows:
        if len(row) != len(SOURCE_COLUMNS):
            errors.append(f"Line {line_number}: source row has {len(row)} columns.")
            continue
        if row[6] not in ALLOWED_SOURCE_STATUS:
            errors.append(f"Line {line_number}: invalid source Status '{row[6]}'.")
    source_warnings, source_semantic_errors = reviewed_source_warnings_and_errors(
        target,
        source_rows,
    )
    warnings.extend(source_warnings)
    errors.extend(source_semantic_errors)

    gap_errors, _gap_rows = validate_table(
        lines,
        GAP_COLUMNS,
        "Evidence gaps and expert input needed",
        require_rows=True,
    )
    errors.extend(gap_errors)

    failure_tokens = ("network_failed", "retrieval_failed", "downloaded_parse_failed")
    if any(token in content for token in failure_tokens):
        evidence_gap_section = content.split(
            "## Evidence gaps and expert input needed",
            1,
        )[-1]
        gap_tokens = (
            "network_failed",
            "retrieval_failed",
            "downloaded_parse_failed",
            "failed retrieval",
        )
        if not any(token in evidence_gap_section for token in gap_tokens):
            warnings.append(
                "Retrieval failure text appears outside the evidence-gap "
                "section; confirm failed retrievals are carried into evidence "
                "gaps."
            )

    if section_exists(content, "## Policy-comparison handoff"):
        handoff_errors, _handoff_rows = validate_table(
            lines, HANDOFF_COLUMNS, "Policy-comparison handoff"
        )
        errors.extend(handoff_errors)

    if errors:
        print("Structural validation failed:")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("Semantic validation warnings:")
            for warning in warnings:
                print(f"- {warning}")
        print(
            "Note: this validator checks structure and limited source-artifact "
            "semantics only, not epidemiological, policy, country, legal, "
            "WASH, or WHO correctness."
        )
        return 1

    print(f"Structural validation passed for {target}.")
    if warnings:
        print("Semantic validation warnings:")
        for warning in warnings:
            print(f"- {warning}")
    print(
        "Note: this validator checks structure and limited source-artifact "
        "semantics only, not epidemiological, policy, country, legal, WASH, "
        "or WHO correctness."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
