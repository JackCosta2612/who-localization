# Environment setup

Environment setup is the first step when distributing, installing, or running
deterministic retrieval with the Country Profiling skill in a new Agent
environment. The skill can run in document-only mode without live network
access, but deterministic script-assisted retrieval needs Python, writable
output storage, outbound HTTPS, and PDF parsing support whenever PDF sources
may be reviewed.

## Quick preflight

Run from the repository root:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network
```

Use `--skip-network` when validating a document-only or offline environment.
Use `--codex-config <path>` to check a Codex config file that is not at
`~/.codex/config.toml`.
The preflight checks output-path writability without creating an output or
`preflight` directory.

Add `--require-pdf` when the planned run is PDF-capable, including immunization
runs using the bundled WHO DAK and manifest or official source workflows that
may retrieve PDFs. If `--require-pdf` fails because `pypdf` is unavailable, stop
and ask the user whether to install the dependency before PDF-capable retrieval
or profile drafting continues.

## Dependency installation approval

The Agent must not install packages, edit the execution environment silently, or
continue past a PDF parsing failure without user acknowledgement. If preflight
or retrieval reports missing `pypdf` while PDF parsing is required or attempted,
ask the user for permission before running the install command. If installation
is approved, rerun the PDF-capable retrieval step before drafting from those
sources.

The prompt should include:

- the missing dependency;
- why it is needed for this run;
- the exact command to run;
- what will happen if the user declines.

Example prompt:

```text
PDF parsing requires pypdf, which is not installed in this Python environment.
May I run `python -m pip install -r skills/country-profiling/sourcing_scripts/requirements.txt`?
If not, retrieval can still continue, but PDFs will be checksummed and marked
downloaded_parse_failed instead of parsed.
```

If approval is declined or unavailable, continue with document-only or limited
retrieval where possible and record the missing dependency as an evidence or
runtime limitation.

## Python setup

Use Python 3.10 or newer. Create an isolated environment if the host does not
already provides the required packages and the user approves installation:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r skills/country-profiling/sourcing_scripts/requirements.txt
```

The only optional package currently listed is `pypdf>=6.0`. Without `pypdf`,
the retrieval helper can still download and checksum PDFs, but PDF text
extraction is recorded as `downloaded_parse_failed`.

## Network access

Live deterministic retrieval uses outbound HTTPS to:

- World Bank Data API;
- WHO Global Health Observatory API;
- manifest-supplied official or institutional web/PDF URLs.

If network access is disabled, the retrieval helper should still write
artifacts with `network_failed` statuses so the profile can record explicit
evidence gaps.

## Codex sandbox configuration

In Codex environments that use a workspace-write sandbox, enable outbound
network access for the sandbox before running live retrieval. Edit
`~/.codex/config.toml` or the active Codex config file:

```toml
approval_policy = "on-failure"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

Approval policy is environment-specific. Keeping approvals enabled is usually
appropriate for shared or unfamiliar repositories. The `on-failure` setting
allows normal sandboxed commands to run while still escalating operations that
need permissions outside the workspace.

Before editing `~/.codex/config.toml`, the Agent should ask the user to approve
the change and show the TOML snippet that will be added or verified.

After editing the config, restart the Codex session or launch a new one so the
sandbox policy is refreshed. Then rerun:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network
```

## Local skill installation

For Codex use, expose the repository skill folder through the Codex skills
directory. A symlink keeps the local skill synchronized with the working tree:

```bash
ln -sfn /path/to/who-smart-localization/skills/country-profiling \
  "${CODEX_HOME:-$HOME/.codex}/skills/country-profiling"
```

Other Agent runtimes can copy or package the `skills/country-profiling/`
folder directly. Keep `SKILL.md`, `context/`, `sourcing_scripts/`, `assets/`,
and relevant `examples/` together so the skill remains self-contained.

Do not copy the skill package into execution output folders. Output folders are
run artifacts, not skill roots. Invoke the repository or installed skill and
write outputs with `--output-dir`. The final profile and JSON/Markdown
retrieval artifacts should stay at the output-folder root; downloaded or parsed
PDFs should be written under `Parsed sources/`.

Do not treat output folders as git repositories. If a git check is needed, run
it from the source repository root or the installed skill symlink target. Do
not include "not inside a git repository" notes in profile or validation
summaries when the non-repository folder is only an output directory.

## Retrieval check

After setup, run a minimal live retrieval into a disposable output directory:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country Italy \
  --iso3 ITA \
  --focus immunization \
  --output-dir /tmp/country-profiling-run \
  --strict
```

Expected live result with network access is nonzero retrieved counts for World
Bank and WHO GHO indicators. If all configured network-backed indicators fail,
inspect `retrieved-indicators.md` for `failure_type` values such as
`dns_error`, `timeout`, `network_error`, or `request_error`.
