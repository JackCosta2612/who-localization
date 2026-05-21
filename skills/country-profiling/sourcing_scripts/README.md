# Country Profiling sourcing scripts

This directory contains the maintained sourcing and validation tooling for the
Country Profiling skill. Retrieval is used to collect selected baseline
indicators and source metadata. It is not a complete country evidence base, a
full data platform, or proof that a country profile is complete.

The preferred minimal-input path is:

1. environment preflight in the target Agent/runtime;
2. target country;
3. optional ISO3 code;
4. optional downstream focus;
5. deterministic retrieval of configured baseline indicators and stable WHO
   artifacts;
6. optional source-manifest resolution for Agent-discovered country-specific
   official URLs or local files;
7. profile drafting with explicit evidence gaps and human review.

If Python scripts are unavailable, the skill may fall back to
semi-deterministic web-assisted retrieval using the protocol in
`../context/web-assisted-retrieval.md`.

All retrieved or reviewed values must preserve:

- source;
- indicator code where applicable;
- label;
- value;
- unit when available;
- year;
- retrieval date;
- URL;
- status.

## Environment preflight

Run before live retrieval in a new local, CI, Codex, Claude, or other Agent
runtime:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network
```

Use `--skip-network` for document-only/offline runs. Use `--require-network`
when the workflow should fail if World Bank or WHO GHO endpoints are blocked.
Add `--require-pdf` for planned PDF parsing, including immunization runs that
will use the bundled WHO DAK and manifest workflows that may retrieve PDFs.

When preflight or retrieval reports missing `pypdf` while PDF parsing is
required or attempted, stop before profile drafting and ask the user to approve
the install command. If installation is approved, rerun the PDF-capable
retrieval step. Do not install packages silently, and do not silently continue
past the warning. If approval is not granted, run with the available
capabilities and preserve the limitation in the retrieval artifacts or profile
evidence gaps. The retrieval helper exits before PDF-capable retrieval when
`pypdf` is missing; use `--allow-missing-pypdf` only after the user declines
installation.

Invoke these scripts from the repository or installed skill path and pass
`--output-dir` directly to the profile run output folder. Do not copy this
`sourcing_scripts/` folder or the broader skill tree into an output folder.
JSON/Markdown artifacts are written at the output-folder root, and downloaded
or parsed PDFs are written under `Parsed sources/`. PDF filenames are
deterministic, and existing copies are reused by content or parsed-text
fingerprint instead of creating duplicate `-2`, `-3`, or similar files.
Do not run `git status` from the output folder or include a non-repository
warning in validation summaries; run git checks only from the source repository
root or installed skill target when repository state is actually relevant.

## Implemented and optional sources

| Source | Current support | Notes |
|---|---|---|
| World Bank Data API | Implemented | Fetches the latest available non-empty value for configured baseline indicators. |
| WHO GHO OData API | Implemented for configured immunization indicators | Retrieves DTP3, MCV1, MCV2, and PCV3 when the focus is immunization. |
| Manifest-supplied institutional web/PDF sources | Implemented | Resolves Agent- or user-supplied country-specific URLs/local files, downloads PDFs, parses text when `pypdf` is available, and records checksums and statuses. |
| OECD SDMX | Not active | Re-evaluate only if a narrow dataset-specific need is proven; OECD/EU context may enter through reviewed institutional profiles. |

Deterministic retrieval should be small and controlled. Add indicators only when
their public codes and interpretation are stable enough for repeated use.
Do not add national ministry, institute, policy, or programme URLs as
country-specific code branches; discover them per run and pass them through a
source manifest.

## Maintained files

| File | Purpose |
|---|---|
| `retrieve_country_profile_data.py` | Orchestrates World Bank, WHO GHO, reviewed web/PDF artifacts, and short source-gap creation. |
| `check_environment.py` | Agent-agnostic runtime preflight for Python, writable output, optional PDF parsing, live HTTPS, and Codex sandbox network settings. |
| `indicator_registry.json` | Small controlled indicator list. |
| `world_bank.py` | World Bank API helper. |
| `who_gho.py` | Configured WHO GHO OData helper. |
| `web_sources.py` | Institutional HTML/PDF resolver and PDF parser wrapper. |
| `source_registry.py` | Country-agnostic source classes, stable WHO artifacts, source manifest loading, and short unresolved source gaps. |
| `validate_profile.py` | Structural validator for Country Profiling outputs. |
| `requirements.txt` | Optional runtime dependency list for PDF parsing. |
