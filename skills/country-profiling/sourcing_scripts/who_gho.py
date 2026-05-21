"""WHO GHO OData retrieval for configured Country Profiling indicators."""

from __future__ import annotations

import datetime as dt
import json
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

import network_errors

BASE_GHO_URL = "https://ghoapi.azureedge.net/api"
USER_AGENT = "who-smart-localization/0.1"

IMMUNIZATION_INDICATORS: list[dict[str, str]] = [
    {
        "indicator_code": "WHS4_100",
        "label": "DTP3 immunization coverage among 1-year-olds",
        "unit": "percent",
        "profile_section": "Healthcare access and coverage",
        "notes": "WHO/UNICEF Estimates of National Immunization Coverage (WUENIC).",
    },
    {
        "indicator_code": "WHS8_110",
        "label": "MCV1 immunization coverage among 1-year-olds",
        "unit": "percent",
        "profile_section": "Healthcare access and coverage",
        "notes": "WHO/UNICEF Estimates of National Immunization Coverage (WUENIC).",
    },
    {
        "indicator_code": "MCV2",
        "label": "MCV2 immunization coverage by nationally recommended age",
        "unit": "percent",
        "profile_section": "Healthcare access and coverage",
        "notes": "WHO/UNICEF Estimates of National Immunization Coverage (WUENIC).",
    },
    {
        "indicator_code": "PCV3",
        "label": "PCV3 immunization coverage among 1-year-olds",
        "unit": "percent",
        "profile_section": "Healthcare access and coverage",
        "notes": (
            "Optional immunization context indicator; may be missing for some "
            "countries or years."
        ),
    },
]


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def configured_indicators_for_focus(focus: str | None = None) -> list[dict[str, str]]:
    """Return configured WHO GHO indicators for a downstream focus."""

    if focus and "immun" in focus.casefold():
        return IMMUNIZATION_INDICATORS
    return []


def _json_get(url: str, timeout: int) -> Any:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _year_from_row(row: dict[str, Any]) -> int:
    for key in ("TimeDim", "TimeDimensionValue"):
        value = row.get(key)
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return -1


def latest_country_row(payload: dict[str, Any], iso3: str) -> dict[str, Any] | None:
    """Return the latest non-empty GHO row for an ISO3 country.

    This is intentionally small and testable. It expects the standard GHO OData
    JSON shape where country rows are in the top-level ``value`` array.
    """

    rows = payload.get("value")
    if not isinstance(rows, list):
        return None

    country_rows = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("SpatialDim", "")).upper() != iso3.upper():
            continue
        if row.get("NumericValue") is None and row.get("Value") in (None, ""):
            continue
        country_rows.append(row)

    if not country_rows:
        return None
    country_rows.sort(key=_year_from_row, reverse=True)
    return country_rows[0]


def fetch_latest_indicator(
    iso3: str,
    indicator: dict[str, Any],
    *,
    timeout: int = 30,
    retrieval_date: str | None = None,
) -> dict[str, Any]:
    retrieval_date = retrieval_date or now_utc()
    code = str(indicator.get("indicator_code", "")).strip()
    label = str(indicator.get("label", code)).strip()
    unit = str(indicator.get("unit", "percent")).strip()
    url = f"{BASE_GHO_URL}/{quote(code, safe='')}" if code else BASE_GHO_URL

    if not code:
        return {
            "source": "WHO Global Health Observatory",
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": url,
            "retrieval_date": retrieval_date,
            "iso3": iso3.upper(),
            "status": "not_configured",
            "error": "Indicator code is missing.",
        }

    try:
        payload = _json_get(url, timeout)
    except Exception as exc:
        return {
            "source": "WHO Global Health Observatory",
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": url,
            "retrieval_date": retrieval_date,
            "iso3": iso3.upper(),
            "status": network_errors.status_for_exception(exc),
            "failure_type": network_errors.classify_exception(exc),
            "error": str(exc),
        }

    if not isinstance(payload, dict) or not isinstance(payload.get("value"), list):
        return {
            "source": "WHO Global Health Observatory",
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": url,
            "retrieval_date": retrieval_date,
            "iso3": iso3.upper(),
            "status": "failed",
            "error": "Unexpected WHO GHO API response shape.",
        }

    row = latest_country_row(payload, iso3)
    if row is None:
        return {
            "source": "WHO Global Health Observatory",
            "indicator_code": code,
            "label": label,
            "unit": unit,
            "year": None,
            "value": None,
            "url": url,
            "retrieval_date": retrieval_date,
            "iso3": iso3.upper(),
            "status": "missing_value",
            "error": "No non-empty country value returned.",
        }

    return {
        "source": "WHO Global Health Observatory",
        "indicator_code": code,
        "label": label,
        "unit": unit,
        "year": row.get("TimeDim") or row.get("TimeDimensionValue"),
        "value": (
            row.get("NumericValue")
            if row.get("NumericValue") is not None
            else row.get("Value")
        ),
        "display_value": row.get("Value"),
        "url": url,
        "retrieval_date": retrieval_date,
        "iso3": iso3.upper(),
        "status": "retrieved",
        "profile_section": indicator.get("profile_section", ""),
        "notes": indicator.get("notes", ""),
        "who_region": row.get("ParentLocation"),
        "data_updated": row.get("Date"),
    }


def fetch_configured_indicators(
    country: str,
    iso3: str,
    focus: str | None = None,
    *,
    timeout: int = 30,
    retrieval_date: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch configured WHO GHO indicators for the supplied focus."""

    del country
    retrieval_date = retrieval_date or now_utc()
    return [
        fetch_latest_indicator(
            iso3,
            indicator,
            timeout=timeout,
            retrieval_date=retrieval_date,
        )
        for indicator in configured_indicators_for_focus(focus)
    ]
