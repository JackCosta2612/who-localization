# Country Profiling Skill

The Country Profiling skill creates a source-backed healthcare overview for a
target country. It summarizes the health situation, health system structure,
implementation environment, data and digital health context, equity issues,
risks, and readiness for later policy comparison or SMART Guidelines
localization.

Country Profiling is not only for countries missing from WHO databases. It is
for any target country where WHO / SMART / DAK content needs country-specific
contextualization before policy comparison or localization. A country can have
WHO, World Bank, OECD, EU, or national data coverage and still require
localization because implementation depends on health-system structure,
governance, regional variation, digital health infrastructure, policy ownership,
service delivery, and source gaps.

## Why this comes first

Policy comparison depends on context. A national policy excerpt is hard to
interpret without knowing the country's service delivery model, coverage rules,
financing constraints, workforce and infrastructure limits, WASH conditions,
data systems, and regional inequalities. This skill makes that context explicit
before the future Policy Comparison skill compares WHO/SMART content with
national policy material.

## Output

The skill produces a narrative markdown profile using `context/profile-schema.md`. It includes:

- healthcare country context and major health issues;
- health system organization, access, coverage, financing, workforce, infrastructure, and supplies;
- sanitary and environmental health context;
- digital health and health information system context;
- equity, vulnerable groups, regional variation, current risks, and watchpoints;
- policy-analysis readiness and optional policy-comparison handoff notes;
- source inventory, evidence gaps, expert-review needs, and sources.

## Sources

Minimum input is a country name. An optional downstream focus such as
immunization can guide source prioritization and policy-comparison readiness
notes, but the profile should still describe the country's healthcare context
overall.

The skill should reduce human source-gathering. With minimal input, use
deterministic retrieval where available to collect selected baseline indicators
from stable global endpoints. Country-specific institutional URLs are not
hardcoded; the Agent discovers official sources through controlled
web-assisted retrieval and passes them to the script with a source manifest. If
scripts are unavailable but web access exists, use semi-deterministic
web-assisted retrieval from approved source classes with strict provenance.
Human input should mainly be review and optional source supplementation.

Better profiles use country-specific sources such as country health profiles,
national health strategies, health sector plans, financing or UHC reports,
workforce and infrastructure sources, WASH/environmental health sources, digital
health or HIS documents, surveillance outputs, and survey or burden-of-disease
sources.

Domain-specific policy documents are useful only when the next step is policy
comparison. They are not required to create the country profile.

## Execution modes

### Environment setup first

For a new local install, exported skill package, or Agent runtime, start
with `context/environment-setup.md`. It covers Python setup, optional PDF
parsing dependencies, live HTTPS requirements, Codex sandbox network
configuration, local skill symlinking, and a retrieval check.

Run the bundled preflight from the repository root:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network \
  --require-pdf
```

Use `--skip-network` for document-only/offline environments. If network checks
fail, deterministic retrieval can still produce explicit `network_failed`
artifacts, but live World Bank, WHO GHO, and manifest URL retrieval will not
succeed until outbound HTTPS is available.

If the preflight reports missing dependencies, the Agent should ask the user
before installing them. The request should name the dependency, explain why it
is needed, show the exact command, and describe the fallback if installation is
not approved.

### Document-only mode

Use this by default when the user provides enough source material in the prompt,
attached files, local files, or conversation context. Draft only from supplied
material and turn missing source classes into explicit evidence gaps.

A supplied URL is not automatically supplied evidence. Treat catalog pages,
publication landing pages, search results, and download pages as source
discovery unless the actual PDF, dataset, official attachment, official
full-text HTML, or local file is opened and reviewed. For example, an OECD
Country Health Profile publication page should be resolved to the `content/dam`
PDF before the profile cites the profile's contents as `Reviewed` evidence.

### Deterministic script-assisted retrieval mode

Use this when Python scripts are available, especially when the user gives only
a country and optional downstream focus. This is the preferred minimal-input
assistance path.

The baseline retrieval script collects selected World Bank indicators,
configured WHO GHO indicators, stable local WHO/DAK artifacts where relevant,
manifest-supplied web/PDF artifacts, and a short unresolved-gap list. These
artifacts support drafting and gap mapping; they do not prove completeness.

### Semi-deterministic web-assisted retrieval mode

Use this when scripts are unavailable but web access exists. Follow
`context/web-assisted-retrieval.md`: use the approved source priority list,
record publisher/title/date/URL/retrieval date/source type/status, separate
reviewed sources from candidate leads, and keep landing-page-only or inaccessible
materials as evidence gaps.

## Sourcing scripts

The maintained Country Profiling tooling is consolidated under
`sourcing_scripts/`. Older preflight and broad WHO-discovery scripts were
removed because the current workflow uses controlled baseline retrieval,
manifest-driven institutional source resolution, short unresolved source gaps, and
documented web-assisted fallback rules.

Check environment setup:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py
```

Retrieve controlled baseline indicators and reviewed source artifacts:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream health-area focus>" \
  --source-manifest "<optional Agent-discovered source manifest>" \
  --output-dir "<output-directory>"
```

For country-specific source classes, use the controlled web-assisted retrieval
protocol in `context/web-assisted-retrieval.md`, record discovered official
sources in the schema from `context/source-manifest-schema.md`, and rerun the
retrieval helper with `--source-manifest`.

PDF parsing uses `pypdf>=6.0` when available. Install
`skills/country-profiling/sourcing_scripts/requirements.txt` in environments
that should parse downloaded PDFs instead of recording them as downloaded but
not parsed.

For each profile run, keep `retrieved-indicators.json`,
`web-reviewed-sources.json`, source-lead artifacts, and the final
`<Country_name>_profile.md` file at the output-directory root. Downloaded or
parsed PDF material belongs under `Parsed sources/`. The retrieval helper uses
that layout for all output directories and suppresses duplicate PDFs by content
or parsed-text fingerprint.

## Validation

Validate a completed profile:

```bash
python3 skills/country-profiling/sourcing_scripts/validate_profile.py <profile.md>
```

The validator checks headings, table headers, optional handoff structure, and
controlled source-status values. It does not validate factual correctness,
epidemiology, policy interpretation, clinical correctness, source
interpretation, WASH interpretation, or WHO interpretation.

## What this skill does not do

- It does not make clinical decisions or provide patient advice.
- It does not draft final national policy.
- It does not compare WHO guidance with national policy.
- It does not produce final DAK localization decisions.
- It does not invent missing country facts.
- It does not replace WHO, national, legal, clinical, policy, WASH,
  epidemiological, environmental health, or country expert review.

## Policy Comparison handoff

The profile should identify which downstream health areas matter for later
comparison, which national policy source classes are needed, which systems
affect policy interpretation, what gaps block safe comparison, and what expert
inputs are required. If the evidence base is too thin, the profile should state
`Not ready for policy comparison`.

## Folder structure

```text
country-profiling/
├── SKILL.md
├── README.md
├── assets/
│   └── who-immunizations-dak.pdf
├── context/
│   ├── execution-modes.md
│   ├── environment-setup.md
│   ├── input-documentation.md
│   ├── mcp-integration-plan.md
│   ├── profile-schema.md
│   ├── retrieval-limitations.md
│   ├── runtime-requirements.md
│   ├── source-manifest-schema.md
│   ├── web-assisted-retrieval.md
│   └── who-data-retrieval.md
├── sourcing_scripts/
│   ├── README.md
│   ├── check_environment.py
│   ├── indicator_registry.json
│   ├── requirements.txt
│   ├── retrieve_country_profile_data.py
│   ├── source_registry.py
│   ├── validate_profile.py
│   ├── web_sources.py
│   ├── who_gho.py
│   └── world_bank.py
├── examples/
│   ├── README.md
│   ├── example-format.md
│   └── example_1/
```

## Reference examples

The `examples/example_1/` folder contains a behavior-shaping reference
example, not final country evidence. It shows the preferred minimal-input
pattern:
country plus optional downstream focus, deterministic baseline retrieval where
available, controlled web-assisted fallback when scripts are unavailable,
configured web/PDF source resolution, short evidence gaps, and downstream
Policy Comparison handoff without performing comparison.
