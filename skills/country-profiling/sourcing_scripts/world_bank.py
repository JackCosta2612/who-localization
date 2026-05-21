"""World Bank baseline indicator retrieval for Country Profiling.

The functions here deliberately retrieve only configured baseline indicators.
They preserve provenance and failure states so the profile can carry missing
values into evidence gaps instead of filling them with assumptions.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

import network_errors

BASE_URL = "https://api.worldbank.org/v2"
USER_AGENT = "who-smart-localization/0.1"


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def load_registry(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_get(url: str, timeout: int) -> Any:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _latest_non_empty_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    sortable = []
    for row in rows:
        value = row.get("value")
        year_raw = row.get("date")
        if value is None:
            continue
        try:
            year = int(year_raw)
        except (TypeError, ValueError):
            year = -1
        sortable.append((year, row))
    if not sortable:
        return None
    sortable.sort(key=lambda item: item[0], reverse=True)
    return sortable[0][1]


def fetch_latest_indicator(
    iso3: str,
    indicator: dict[str, Any],
    *,
    timeout: int = 30,
    retrieval_date: str | None = None,
) -> dict[str, Any]:
    """Fetch the latest available non-empty value for one indicator."""

    retrieval_date = retrieval_date or now_utc()
    code = str(indicator.get("indicator_code", "")).strip()
    label = str(indicator.get("label", code)).strip()
    source = str(indicator.get("source", "World Bank")).strip()
    unit = str(indicator.get("unit", "")).strip()
    if not code:
        return {
            "source": source,
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": "",
            "retrieval_date": retrieval_date,
            "status": "not_configured",
            "error": "Indicator code is missing.",
        }

    country = quote(iso3.upper(), safe="")
    indicator_code = quote(code, safe="")
    url = (
        f"{BASE_URL}/country/{country}/indicator/{indicator_code}"
        "?format=json&per_page=100"
    )

    try:
        payload = _json_get(url, timeout)
    except Exception as exc:
        return {
            "source": source,
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": url,
            "retrieval_date": retrieval_date,
            "status": network_errors.status_for_exception(exc),
            "failure_type": network_errors.classify_exception(exc),
            "error": str(exc),
        }

    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        return {
            "source": source,
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": url,
            "retrieval_date": retrieval_date,
            "status": "failed",
            "error": "Unexpected World Bank API response shape.",
        }

    row = _latest_non_empty_row(payload[1])
    if row is None:
        return {
            "source": source,
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": url,
            "retrieval_date": retrieval_date,
            "status": "missing_value",
            "error": "No non-empty country value returned.",
        }

    return {
        "source": source,
        "indicator_code": code,
        "label": label,
        "unit": unit,
        "year": row.get("date"),
        "value": row.get("value"),
        "url": url,
        "retrieval_date": retrieval_date,
        "status": "retrieved",
        "profile_section": indicator.get("profile_section", ""),
        "notes": indicator.get("notes", ""),
    }


def fetch_registry_indicators(
    iso3: str,
    registry: dict[str, Any],
    *,
    timeout: int = 30,
    retrieval_date: str | None = None,
) -> list[dict[str, Any]]:
    retrieval_date = retrieval_date or now_utc()
    results = []
    for indicator in registry.get("indicators", []):
        if str(indicator.get("source", "")).casefold() != "world bank":
            continue
        results.append(
            fetch_latest_indicator(
                iso3,
                indicator,
                timeout=timeout,
                retrieval_date=retrieval_date,
            )
        )
    return results
