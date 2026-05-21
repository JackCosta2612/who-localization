# WHO SMART Localization Skills

This repository contains Agent Skills that support WHO SMART Guidelines and
Digital Adaptation Kit localization workflows.

The active skill is Country Profiling. It creates a source-backed healthcare
country profile from a target country, optional health-area focus, supplied
documents, stable global indicators, and reviewed official or institutional
sources. The profile is intended to help WHO staff understand country context,
source readiness, evidence gaps, and constraints before policy comparison or
localization work begins.

The skills are review aids. They do not make clinical decisions, provide
patient advice, draft final national policy, or replace WHO, ministry, legal,
clinical, programme, WASH, environmental health, epidemiological, or country
expert review.

## Repository Structure

```text
.
├── README.md
├── SKILLS.md
├── docs/
├── shared/
└── skills/
    ├── country-profiling/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── assets/
    │   ├── context/
    │   ├── examples/
    │   └── sourcing_scripts/
    └── policy-comparison/
        └── SKILL.md
```

## Country Profiling

Path: `skills/country-profiling/`

Country Profiling produces a markdown country profile covering:

- country context and population health;
- major health issues and burden;
- health system organization, access, coverage, financing, workforce,
  infrastructure, and supplies;
- sanitary and environmental health context;
- digital health and health information systems;
- equity, vulnerable groups, regional variation, risks, and watchpoints;
- policy-analysis readiness, evidence gaps, expert-review needs, and sources.

The minimal input is a country name. An optional downstream health-area focus,
such as immunization, helps prioritize source discovery and handoff notes. The
profile should still describe the broader health system context, not only the
focus area.

## Setup for Codex or Similar Agent Runtimes

Use Python 3.10 or newer. For deterministic retrieval, the runtime needs write
access to the selected output directory and outbound HTTPS access to stable
global APIs and manifest-supplied source URLs.

In Codex workspace-write environments, configure the active Codex TOML file,
usually `~/.codex/config.toml`, with:

```toml
approval_policy = "on-failure"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

Restart the Codex session after changing the configuration. Network access must
also be enabled in the host or Agent execution environment; the TOML setting
allows the Codex sandbox to use outbound HTTPS, but it cannot override an
external firewall, proxy, VPN, or platform-level network block.

Install optional PDF parsing support only after user approval:

```bash
python3 -m pip install -r skills/country-profiling/sourcing_scripts/requirements.txt
```

The only required optional dependency currently listed is `pypdf>=6.0`. If PDF
sources are part of the run and `pypdf` is unavailable, the Agent should stop
and ask whether to install it before retrieval or drafting continues. If the
user declines, the run can continue only with PDF parsing explicitly recorded
as a limitation.

## Preflight

Run from the repository root:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network
```

Add `--require-pdf` when the run will use PDFs, such as source manifests with
PDFs or immunization runs that use the bundled WHO immunization DAK:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network \
  --require-pdf
```

Use `--skip-network` only for document-only or offline workflows.

## Running Retrieval

Run deterministic retrieval when the user gives only a country and optional
focus, or when reviewed source artifacts should be written consistently:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional health-area focus>" \
  --source-manifest "<optional source manifest>" \
  --output-dir "<output directory>"
```

The output directory will contain:

- `retrieved-indicators.json`
- `retrieved-indicators.md`
- `web-reviewed-sources.json`
- `web-reviewed-sources.md`
- `source-leads.md`
- `Parsed sources/` for downloaded or parsed PDFs

The final profile should be written at the output-directory root with a
deterministic filename, for example `Germany_profile.md` or
`United_States_profile.md`.

Country-specific official URLs are intentionally not hardcoded. The Agent
should discover national ministry, public-health institute, statistics,
medicine/vaccine authority, digital health, programme, or registry sources
during controlled source review and pass them through the manifest schema in
`skills/country-profiling/context/source-manifest-schema.md`.

## Writing the Profile

Use `skills/country-profiling/SKILL.md` as the primary Agent instruction and
`skills/country-profiling/context/profile-schema.md` as the output schema.

The profile must distinguish:

- reviewed evidence;
- candidate source leads;
- landing pages that still need material endpoints;
- failed retrievals;
- unavailable indicator values;
- evidence gaps and expert-review needs.

Do not treat successful retrieval as proof that the country evidence base is
complete. Do not treat failed retrieval as evidence that a fact is false.

## Validation

Validate a completed profile structurally:

```bash
python3 skills/country-profiling/sourcing_scripts/validate_profile.py \
  <path-to-profile.md>
```

The validator checks headings, required tables, controlled source statuses,
selected metadata fields, and limited source-artifact semantics. It does not
validate factual correctness, epidemiology, legal interpretation, clinical
content, policy interpretation, source interpretation, WASH interpretation, or
WHO correctness.

## Policy Comparison

Path: `skills/policy-comparison/`

Policy Comparison is currently a scaffold. It describes the intended future
workflow for comparing WHO SMART Guidelines or DAK artifacts with reviewed
country-specific policy material. It does not include runnable comparison
logic.
