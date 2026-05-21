# Runtime requirements

The Country Profiling retrieval helpers are designed to run in changing Agent
environments with minimal setup.

Start new installs, exported skill packages, and deterministic retrieval runs
in fresh runtimes with `environment-setup.md` and the bundled preflight:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network
```

Add `--require-pdf` when the planned run will parse PDFs. If preflight or
retrieval reports missing `pypdf` while PDF parsing is required or attempted,
stop and prompt the user for permission before installing it. Include the exact
command, usually:

```bash
python3 -m pip install -r skills/country-profiling/sourcing_scripts/requirements.txt
```

If the user approves installation, rerun the PDF-capable retrieval step. If the
user declines, continue only with modes supported by the current runtime and
record missing PDF parsing support as a runtime limitation.

## Required for deterministic script-assisted retrieval

- Python 3.10 or newer.
- Python standard library only.
- Write access to the output directory. Always pass an explicit `--output-dir`
  for the profile run. Output folders are not expected to be git repositories;
  do not run `git status` there or report non-repository notes as validation
  findings. Keep the final profile and JSON/Markdown artifacts at the
  output-folder root, and keep downloaded or parsed PDFs under
  `Parsed sources/`.

## Optional

- Outbound HTTPS access for live World Bank retrieval.
- Outbound HTTPS access for live WHO GHO and manifest-supplied institutional web/PDF retrieval.
- `pypdf>=6.0` for PDF text extraction. Without it, PDFs can still be
  downloaded and checksummed, but their status is `downloaded_parse_failed`.
- MCP tooling is optional and documented separately in `mcp-integration-plan.md`.

For Codex workspace-write sandboxes that need live retrieval, the active
`config.toml` should include:

```toml
approval_policy = "on-failure"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

Restart the Codex session after changing sandbox configuration.

## Deterministic baseline retrieval command

Run from the repository root:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream focus>" \
  --source-manifest "<optional Agent-discovered source manifest>" \
  --output-dir "/path/to/country-profile-output"
```

This writes `retrieved-indicators.json`, `retrieved-indicators.md`,
`web-reviewed-sources.json`, `web-reviewed-sources.md`, and `source-leads.md`.
Treat these as source artifacts and gap-mapping support, not as proof of
country-profile completeness.

Use `--strict` when a workflow should fail fast if all configured
network-backed indicator retrieval fails. Source manifests follow
`context/source-manifest-schema.md` and are the preferred way to pass
country-specific official URLs to the resolver.

## Structural validation command

```bash
python3 skills/country-profiling/sourcing_scripts/validate_profile.py \
  skills/country-profiling/examples/example_1/reference-output.md
```
