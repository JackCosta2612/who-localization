# Execution modes

Country Profiling creates a country context layer for WHO / SMART / DAK
localization work. It is not only for countries missing from WHO databases. A
country may have strong WHO, World Bank, OECD, EU, or national data coverage and
still require localization because implementation depends on health-system
structure, governance, regional variation, digital infrastructure, service
delivery, policy ownership, and source gaps.

The skill supports three execution modes.

## 0. Environment setup for new runtimes

When distributing or running deterministic retrieval in a new Agent runtime,
first follow `environment-setup.md` and run:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network
```

This confirms Python version, output-directory writability, live HTTPS
reachability, and Codex sandbox network settings when applicable. Add
`--require-pdf` when the planned run will parse PDFs. If setup checks fail,
choose document-only mode or record the failure as an evidence gap instead of
drafting unsupported country facts.

When setup or retrieval finds missing `pypdf` while PDF parsing is required or
attempted, stop and ask the user before installing packages or changing the
environment. If the user approves installation, rerun the PDF-capable retrieval
step before drafting from those sources. If the user declines, continue only
with the retrieval and parsing capabilities already available and record PDF
parsing as a runtime limitation.

## 1. Document-only mode

Use document-only mode when the user provides source documents, excerpts,
attachments, local files, or conversation context that are sufficient to draft
from supplied material.

In this mode, the Agent should:

- identify the target country and optional downstream health-area focus;
- normalize supplied material into the source inventory from
  `profile-schema.md`;
- draft only from supplied material;
- mark missing source classes and missing facts as evidence gaps;
- avoid using web search or deterministic scripts unless the user asks for mixed
  retrieval support.

Supplied URLs are not automatically reviewed evidence. A catalog page,
publication landing page, search result, or download page remains a candidate
until the PDF, dataset, official attachment, official full-text HTML, or local
file has been opened and reviewed.

## 2. Deterministic script-assisted retrieval mode

Use deterministic script-assisted retrieval when Python scripts are available
and the user provides only a country and optional downstream focus. This is the
preferred assistance path for minimal-input profiling.

Run the repository or installed skill script and pass an explicit
`--output-dir` for the profile run. Do not copy the skill package into the
output directory, and do not create nested `skills/country-profiling`,
`manifests`, `profiles`, or `retrieval-output` folders there. The retrieval
helper keeps JSON/Markdown artifacts at the output-directory root and writes
downloaded or parsed PDFs under `Parsed sources/`.

When writing the final country profile into an output directory, use the
deterministic filename `<Country_name>_profile.md`, where whitespace and
punctuation in the normalized input country name are replaced with single
underscores.

Output directories are not expected to contain `.git`. Do not run `git status`
from those folders or report a "not inside a git repository" note as part of
validation. If repository state is needed, check it from the source repository
root or the installed skill target.

The baseline retrieval command is:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream health-area focus>" \
  --source-manifest "<optional Agent-discovered source manifest>" \
  --output-dir "/path/to/country-profile-output"
```

The script writes:

- `retrieved-indicators.json`;
- `retrieved-indicators.md`;
- `web-reviewed-sources.json`;
- `web-reviewed-sources.md`;
- `source-leads.md`.

The deterministic layer is intentionally small. It retrieves selected World Bank
baseline indicators, configured WHO GHO indicators, stable local WHO/DAK
artifacts where relevant, optional source-manifest web/PDF sources, and short
unresolved source gaps. OECD SDMX retrieval is not active in this mode; OECD/EU
context should come from reviewed institutional profiles unless a future narrow
dataset-specific retriever is added.

Country-specific institutional discovery is not hardcoded in scripts. When the
Agent identifies official ministry, public-health, statistics, policy, digital
health, programme, or registry sources, it should record them in the manifest
format from `source-manifest-schema.md` and rerun the helper with
`--source-manifest <file>`.

Use deterministic outputs as source artifacts. Precise data claims must include
indicator source, code, year, source URL, and retrieval date. Successful
retrieval does not prove completeness; it only provides a baseline context
bundle.

## 3. Semi-deterministic web-assisted retrieval mode

Use semi-deterministic web-assisted retrieval when Python scripts are
unavailable but web access is available. Follow
`web-assisted-retrieval.md`.

This mode is structured source discovery and review, not open-ended browsing.
The Agent should:

- follow the predefined source priority list;
- search only for specific approved source classes;
- prefer official and institutional sources;
- record publisher, title, URL, date, retrieval date, source type, and status;
- separate reviewed evidence from candidate source leads;
- treat landing pages as landing pages unless the evidence-bearing material is
  retrieved and reviewed;
- mark inaccessible PDFs, missing datasets, and unresolved national/regional
  sources as evidence gaps.

## Mixed mode

Use mixed mode when supplied documents are combined with deterministic retrieval
or controlled web-assisted retrieval. This is common when the user supplies a
few national documents but still needs baseline indicators, reviewed source
artifacts, or gap mapping.

## What counts as enough evidence

- Full profile: the country is known and several major sections are supported by
  reviewed documents, retrieved indicators, or reviewed web sources.
- Limited profile: some relevant evidence is available, but important sections
  rely on missing, stale, landing-page-only, inaccessible, or unreviewed source
  classes.
- Skeleton/gap-analysis profile: the country is known but there is too little
  reviewed evidence. The useful output is a source plan, evidence-gap map, and
  policy-comparison readiness assessment.
- Pause and ask for sources: no country is specified, or neither scripts, web
  access, nor sufficient supplied documents are available and the user did not
  request a skeleton/gap analysis.

Baseline indicators alone are not enough for a full profile. A full profile also
needs health-system context, source inventory, evidence gaps, and implementation
context. Official or institutional documents are usually required for system
organization, policy ownership, digital health, regional implementation, and
downstream policy-comparison readiness.

## When scripts are unavailable

If scripts are unavailable but web access exists, switch to semi-deterministic
web-assisted retrieval. Do not ask the user to construct a source package before
attempting controlled retrieval unless the task is high risk, the country is
ambiguous, or web access is blocked.

If scripts fail but supplied source material is adequate, proceed in
document-only or mixed mode and record the script failure as a retrieval gap
only if it affects the profile.

## When neither scripts nor enough documents are available

If there is no web access, no usable script path, and insufficient source
material, do not draft unsupported country facts. Ask for source material or
produce only a skeleton/gap-analysis profile if that is useful.

## Evidence gaps

Missing content should become evidence gaps, not assumptions. Include gaps from:

- missing data;
- unavailable indicator values;
- failed retrieval;
- empty or non-matching source manifests;
- landing-page-only sources;
- inaccessible PDFs or datasets;
- national, regional, or programme sources not reviewed;
- digital health or registry source classes not reviewed;
- policy sources needed later for comparison but not yet retrieved.

## Downstream policy-comparison decision

A profile can feed the future Policy Comparison skill only if it identifies
enough country context and at least suggests which national policy source
classes are needed. It does not need to include policy documents unless the user
is preparing an immediate comparison.

If the profile cannot support downstream comparison, write `Not ready for
policy comparison` in the `Policy-analysis readiness` section and explain why.
Common reasons include missing national policy sources, no country-specific
health system evidence, unresolved source conflicts, stale documents, or
insufficient context for interpreting policy text.
