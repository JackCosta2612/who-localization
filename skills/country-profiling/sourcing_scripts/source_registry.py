"""Country-agnostic source classes and source-manifest loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


UNIVERSAL_SOURCE_CLASSES: list[dict[str, str]] = [
    {
        "source_class": "WHO country or regional source",
        "why_needed": (
            "Needed for WHO-country collaboration, regional context, "
            "country-specific health priorities, or institutional profile leads."
        ),
        "suggested_action": (
            "Use controlled web-assisted retrieval to resolve a country-specific "
            "WHO, WHO regional, or WHO-hosted profile source and pass the "
            "material endpoint through a source manifest."
        ),
        "status": "Needs retrieval",
    },
    {
        "source_class": "National Ministry of Health or equivalent",
        "why_needed": (
            "Needed for national health-system ownership, strategies, official "
            "policy source classes, and implementation context."
        ),
        "suggested_action": (
            "Identify the official ministry site or document for the target "
            "country and pass reviewed URLs or candidate URLs through a source "
            "manifest."
        ),
        "status": "Needs retrieval",
    },
    {
        "source_class": "National public health institute or equivalent",
        "why_needed": (
            "Needed for surveillance, programme monitoring, outbreak context, "
            "health-system implementation, and technical guidance ownership."
        ),
        "suggested_action": (
            "Resolve official public-health institute, disease-control, or "
            "surveillance sources through controlled web-assisted retrieval."
        ),
        "status": "Needs retrieval",
    },
    {
        "source_class": "National statistics office or official data portal",
        "why_needed": (
            "Needed to supplement global indicators with country-specific "
            "demographic, geographic, survey, or administrative context."
        ),
        "suggested_action": (
            "Retrieve official country-filtered tables, reports, or data "
            "portals when profile sections require national denominators or "
            "subnational context."
        ),
        "status": "Needs retrieval",
    },
    {
        "source_class": (
            "Health financing, workforce, infrastructure, or "
            "service-delivery source"
        ),
        "why_needed": (
            "Needed when global baseline indicators are insufficient for "
            "implementation feasibility and health-system capacity interpretation."
        ),
        "suggested_action": (
            "Prefer official national reports, WHO/regional observatory "
            "profiles, World Bank country documents, or other institutional "
            "country-specific material."
        ),
        "status": "Needs retrieval",
    },
    {
        "source_class": "Digital health, HIS, registry, or data-flow source",
        "why_needed": (
            "Needed for SMART/DAK localization readiness, reporting feasibility, "
            "interoperability, and data quality interpretation."
        ),
        "suggested_action": (
            "Resolve official digital health strategy, health information "
            "system, registry, interoperability, or surveillance-data-flow "
            "material when available."
        ),
        "status": "Needs retrieval",
    },
]


FOCUS_SOURCE_CLASSES: dict[str, list[dict[str, str]]] = {
    "immun": [
        {
            "source_class": (
                "National immunization schedule, guideline, circular, or "
                "recommendation source"
            ),
            "why_needed": (
                "Needed to identify current national vaccine target groups, "
                "timing, ownership, and implementation policy source classes "
                "for later comparison."
            ),
            "suggested_action": (
                "Retrieve the official schedule or recommendation material "
                "endpoint; do not infer policy from global coverage indicators."
            ),
            "status": "Needs retrieval",
        },
        {
            "source_class": "National immunization coverage or programme monitoring dataset",
            "why_needed": (
                "Needed to distinguish policy text from uptake, timeliness, "
                "equity, and subnational implementation performance."
            ),
            "suggested_action": (
                "Resolve official coverage reports, dashboards, datasets, or "
                "exports with vaccine, age, geography, and year definitions "
                "where available."
            ),
            "status": "Needs retrieval",
        },
        {
            "source_class": "Medicines agency, vaccine authority, or pharmacovigilance source",
            "why_needed": (
                "Relevant for vaccine safety monitoring, adverse event "
                "reporting, product governance, and public-trust context."
            ),
            "suggested_action": (
                "Retrieve official vaccine safety or pharmacovigilance material "
                "when safety or implementation workflow context is in scope."
            ),
            "status": "Needs retrieval",
        },
        {
            "source_class": (
                "Immunization registry, reminder, reporting, or "
                "interoperability source"
            ),
            "why_needed": (
                "Needed to assess SMART-compatible data readiness, patient-level "
                "status verification, reminder/recall, and reporting workflows."
            ),
            "suggested_action": (
                "Resolve official immunization registry, e-health, coding, "
                "reporting, or interoperability specifications if available."
            ),
            "status": "Needs retrieval",
        },
    ],
    "hiv": [
        {
            "source_class": (
                "National HIV strategy, guideline, surveillance, or programme "
                "report"
            ),
            "why_needed": (
                "Needed for country-specific HIV service delivery, cascade, "
                "surveillance, and policy source readiness."
            ),
            "suggested_action": (
                "Retrieve current official HIV programme and surveillance "
                "material through a source manifest."
            ),
            "status": "Needs retrieval",
        }
    ],
    "tuberculosis": [
        {
            "source_class": (
                "National tuberculosis strategy, guideline, surveillance, or "
                "programme report"
            ),
            "why_needed": (
                "Needed for TB burden, service delivery, reporting, and later "
                "policy-comparison readiness."
            ),
            "suggested_action": (
                "Retrieve current official TB programme and surveillance "
                "material through a source manifest."
            ),
            "status": "Needs retrieval",
        }
    ],
    "maternal": [
        {
            "source_class": (
                "National maternal, newborn, or reproductive health strategy "
                "and service-delivery source"
            ),
            "why_needed": (
                "Needed for maternal-health service organization, coverage, "
                "quality, and readiness interpretation."
            ),
            "suggested_action": (
                "Retrieve current official maternal/reproductive health "
                "programme material through a source manifest."
            ),
            "status": "Needs retrieval",
        }
    ],
    "wash": [
        {
            "source_class": "National WASH, environmental health, or climate-health source",
            "why_needed": (
                "Needed for sanitary, water, hygiene, environmental, and "
                "climate-risk context beyond global baseline indicators."
            ),
            "suggested_action": (
                "Retrieve country-specific official or institutional "
                "WASH/environmental health material through a source manifest."
            ),
            "status": "Needs retrieval",
        }
    ],
}


def stable_source_targets(
    country: str,
    iso3: str,
    focus: str | None = None,
) -> list[dict[str, Any]]:
    """Return stable non-country-institution targets.

    This intentionally avoids national ministry, institute, or policy URLs.
    Country-specific official sources should be discovered by the Agent and
    passed in with ``--source-manifest``.
    """

    del country, iso3
    focus_text = focus or ""
    targets: list[dict[str, Any]] = []
    if "immun" in focus_text.casefold():
        targets.append(
            {
                "target_type": "local_pdf",
                "title": "WHO SMART Guidelines Digital Adaptation Kit for Immunization",
                "publisher": "World Health Organization",
                "source_type": "WHO SMART / DAK artifact",
                "path": "assets/who-immunizations-dak.pdf",
                "date": "Bundled local source",
                "source_class": "WHO SMART / DAK artifact",
                "evidence_role": (
                    "Downstream handoff artifact; not evidence about the target "
                    "country's health system."
                ),
                "intent": "candidate",
                "retrieval_priority": "stable",
            }
        )
    return targets


def _focus_classes(focus: str | None = None) -> list[dict[str, str]]:
    focus_text = (focus or "").casefold()
    classes: list[dict[str, str]] = []
    for token, entries in FOCUS_SOURCE_CLASSES.items():
        if token in focus_text:
            classes.extend(entries)
    return classes


def reviewed_source_classes(web_records: list[dict[str, Any]] | None = None) -> set[str]:
    reviewed = set()
    for record in web_records or []:
        if record.get("review_status") != "reviewed":
            continue
        source_class = str(record.get("source_class") or "").strip()
        if source_class:
            reviewed.add(source_class.casefold())
    return reviewed


def unresolved_source_gaps(
    country: str,
    iso3: str,
    focus: str | None = None,
    *,
    web_records: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return country-agnostic actionable gaps not satisfied by reviewed records."""

    del country, iso3
    reviewed = reviewed_source_classes(web_records)
    gaps = []
    for gap in UNIVERSAL_SOURCE_CLASSES + _focus_classes(focus):
        if gap["source_class"].casefold() in reviewed:
            continue
        gaps.append(dict(gap))
    return gaps


def _manifest_sources(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        sources = payload.get("sources", [])
        if not isinstance(sources, list):
            raise ValueError("source manifest field 'sources' must be a list.")
        return sources
    if isinstance(payload, list):
        return payload
    raise ValueError(
        "source manifest must be a JSON object with 'sources' or a JSON list."
    )


def _source_matches_context(
    source: dict[str, Any],
    *,
    country: str,
    iso3: str,
    focus: str | None,
) -> bool:
    source_country = str(source.get("country", "")).strip()
    source_iso3 = str(source.get("iso3", "")).strip()
    source_focus = str(source.get("focus", "")).strip()
    if source_country and source_country.casefold() != country.casefold():
        return False
    if source_iso3 and source_iso3.upper() != iso3.upper():
        return False
    if source_focus and focus and source_focus.casefold() not in focus.casefold():
        return False
    if source_focus and not focus:
        return False
    return True


def _target_from_manifest_source(
    source: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    title = str(source.get("title") or "").strip()
    publisher = str(source.get("publisher") or "").strip()
    source_type = str(source.get("source_type") or "").strip()
    url = str(source.get("url") or "").strip()
    path = str(source.get("path") or "").strip()
    if not title:
        raise ValueError(f"source manifest entry {index} is missing 'title'.")
    if not publisher:
        raise ValueError(f"source manifest entry {index} is missing 'publisher'.")
    if not source_type:
        raise ValueError(f"source manifest entry {index} is missing 'source_type'.")
    if bool(url) == bool(path):
        raise ValueError(
            f"source manifest entry {index} must provide exactly one of "
            "'url' or 'path'."
        )

    target: dict[str, Any] = {
        "title": title,
        "publisher": publisher,
        "source_type": source_type,
        "date": source.get("date", ""),
        "source_class": source.get("source_class", source_type),
        "evidence_role": source.get("evidence_role", ""),
        "retrieval_priority": source.get("retrieval_priority", ""),
        "intent": source.get("intent", "reviewed"),
        "reviewed_intent": source.get(
            "reviewed_intent",
            source.get("intent", "reviewed"),
        ),
        "excerpt_keywords": source.get("excerpt_keywords", []),
        "max_summary_chars": int(source.get("max_summary_chars", 2000)),
    }
    if path:
        target["target_type"] = source.get("target_type", "local_pdf")
        target["path"] = path
    else:
        target["target_type"] = source.get("target_type", "html")
        target["url"] = url
        target["download_pdfs"] = bool(source.get("download_pdfs", False))
        target["max_downloads"] = int(source.get("max_downloads", 0))
    return target


def load_source_manifest(
    path: str | Path,
    *,
    country: str,
    iso3: str,
    focus: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load Agent-discovered source targets from a JSON manifest."""

    manifest_path = Path(path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    sources = _manifest_sources(payload)
    targets: list[dict[str, Any]] = []
    skipped = 0
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            raise ValueError(f"source manifest entry {index} must be an object.")
        if not _source_matches_context(
            source,
            country=country,
            iso3=iso3,
            focus=focus,
        ):
            skipped += 1
            continue
        targets.append(_target_from_manifest_source(source, index))

    return targets, {
        "path": str(manifest_path),
        "source_count": len(sources),
        "target_count": len(targets),
        "skipped_count": skipped,
    }
