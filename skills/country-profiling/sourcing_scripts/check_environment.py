#!/usr/bin/env python3
"""Check Country Profiling runtime setup in an agent-agnostic way."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import network_errors


MIN_VERSION = (3, 10)
DEFAULT_OUTPUT_DIR = Path("skills/country-profiling/retrieval-output")
REQUIREMENTS_PATH = Path("skills/country-profiling/sourcing_scripts/requirements.txt")
NETWORK_TESTS = [
    (
        "World Bank API",
        "https://api.worldbank.org/v2/country/ITA/indicator/SP.POP.TOTL?format=json&per_page=1",
    ),
    ("WHO GHO API", "https://ghoapi.azureedge.net/api/WHS4_100?$top=1"),
]


def result(ok: bool, level: str, name: str, detail: str) -> dict[str, Any]:
    return {"ok": ok, "level": level, "name": name, "detail": detail}


def check_python() -> dict[str, Any]:
    current = sys.version_info[:3]
    version = f"{current[0]}.{current[1]}.{current[2]}"
    if current >= MIN_VERSION:
        return result(True, "ok", "python", f"Python version OK: {version}")
    return result(
        False,
        "error",
        "python",
        f"Python version too old: {version}; requires {MIN_VERSION[0]}.{MIN_VERSION[1]}+",
    )


def check_output_dir(path: Path) -> dict[str, Any]:
    try:
        if path.exists():
            if not path.is_dir():
                return result(False, "error", "output_dir", f"Output path is not a directory: {path}")
            probe_dir = path
            detail = f"Output directory writable: {path}"
        else:
            probe_dir = path.parent
            while not probe_dir.exists() and probe_dir != probe_dir.parent:
                probe_dir = probe_dir.parent
            if not probe_dir.is_dir():
                return result(
                    False,
                    "error",
                    "output_dir",
                    f"No existing parent directory found for output path: {path}",
                )
            detail = f"Output parent writable: {probe_dir}; target can be created later: {path}"

        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=probe_dir,
            prefix=".write-probe-",
            delete=True,
        ) as probe:
            probe.write("ok")
    except OSError as exc:
        return result(False, "error", "output_dir", f"Output directory not writable: {path} ({exc})")
    return result(True, "ok", "output_dir", detail)


def check_pypdf(require_pdf: bool) -> dict[str, Any]:
    try:
        import pypdf  # type: ignore
    except Exception as exc:
        level = "error" if require_pdf else "warn"
        install_command = (
            f"{sys.executable} -m pip install -r {REQUIREMENTS_PATH}"
        )
        return result(
            not require_pdf,
            level,
            "pypdf",
            (
                f"pypdf unavailable: {exc}. Stop and ask the user for approval "
                "before PDF-capable retrieval or profile drafting. Install "
                f"PDF parsing dependencies with: {install_command}"
            ),
        )
    return result(True, "ok", "pypdf", f"pypdf available: {getattr(pypdf, '__version__', 'unknown')}")


def check_url(label: str, url: str, timeout: int, require_network: bool) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "who-smart-localization/0.1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return result(True, "ok", label, f"Reachable: HTTP {response.status} ({url})")
    except Exception as exc:
        category = network_errors.classify_exception(exc)
        level = "error" if require_network else "warn"
        return result(
            not require_network,
            level,
            label,
            f"Not reachable: {category}: {exc} ({url})",
        )


def check_codex_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return result(
            True,
            "warn",
            "codex_config",
            f"Codex config not found at {path}; skip if this is not a Codex runtime.",
        )

    text = path.read_text(encoding="utf-8")
    approval_on_failure = False
    has_workspace = False
    network_enabled = False
    in_workspace_section = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_workspace_section = line == "[sandbox_workspace_write]"
            continue
        if line.startswith("approval_policy") and "on-failure" in line:
            approval_on_failure = True
        if line.startswith("sandbox_mode") and "workspace-write" in line:
            has_workspace = True
        if in_workspace_section and line.startswith("network_access"):
            network_enabled = line.split("=", 1)[-1].strip().casefold() == "true"

    if approval_on_failure and has_workspace and network_enabled:
        return result(True, "ok", "codex_config", f"Codex workspace-write network access enabled: {path}")

    return result(
        True,
        "warn",
        "codex_config",
        (
            "Codex workspace-write network access not fully detected. If live retrieval is blocked, "
            "add: approval_policy = \"on-failure\", sandbox_mode = \"workspace-write\", "
            "and [sandbox_workspace_write] network_access = true."
        ),
    )


def print_results(results: list[dict[str, Any]]) -> None:
    for item in results:
        print(f"{item['level'].upper()}: {item['detail']}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check environment setup for the Country Profiling skill."
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=(
            "Directory retrieval scripts should be able to write to. "
            "This preflight checks writability without creating the directory."
        ),
    )
    parser.add_argument("--timeout", type=int, default=10, help="Network timeout in seconds.")
    parser.add_argument("--skip-network", action="store_true", help="Skip live HTTPS checks.")
    parser.add_argument(
        "--require-network",
        action="store_true",
        help="Exit nonzero if live HTTPS checks fail.",
    )
    parser.add_argument(
        "--require-pdf",
        action="store_true",
        help="Exit nonzero if pypdf is unavailable.",
    )
    parser.add_argument(
        "--codex-config",
        default=str(Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "config.toml"),
        help="Optional Codex config path to inspect for workspace-write network access.",
    )
    parser.add_argument(
        "--skip-codex-config",
        action="store_true",
        help="Skip Codex config inspection.",
    )
    args = parser.parse_args(argv[1:])

    results = [
        check_python(),
        check_output_dir(Path(args.output_dir)),
        check_pypdf(args.require_pdf),
    ]
    if args.skip_network:
        results.append(result(True, "warn", "network", "Network checks skipped."))
    else:
        results.extend(
            check_url(label, url, args.timeout, args.require_network)
            for label, url in NETWORK_TESTS
        )
    if not args.skip_codex_config:
        results.append(check_codex_config(Path(args.codex_config).expanduser()))

    print_results(results)
    if any(not item["ok"] for item in results):
        print("Environment check failed.")
        return 1

    print("Environment check completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
