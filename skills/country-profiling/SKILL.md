---
name: country-profiling
description: >-
  Build a source-backed healthcare country profile for a target country and
  optional downstream health-area focus, including health situation, health
  system context, implementation environment, evidence gaps, and readiness for
  later WHO SMART Guidelines localization or policy comparison.
license: MIT
metadata:
  compatibility: >-
    Model-neutral Agent Skill. Supports document-only, deterministic
    script-assisted, and semi-deterministic web-assisted retrieval modes.
  version: "1.0"
---

# WHO SMART Country Profiling Skill

## Purpose

Create a concise, source-backed healthcare country profile for a target country.

The profile explains the country's health situation and health system context
before detailed policy comparison, DAK localization, or SMART Guidelines
adaptation. It should cover the main health issues, health system organization,
implementation environment, access and coverage, sanitary and environmental
health conditions, financing and affordability, workforce and infrastructure,
digital health and data systems, equity concerns, and current risks or
uncertainties.

The output is designed as an input to the future Policy Comparison skill. It
should identify which downstream health areas may need later comparison, which
national policy source classes are still needed, and what country context
constrains interpretation of national policy. It should not compare policies,
assess alignment with WHO guidance, or draft localization recommendations.

Country Profiling is not only for countries missing from WHO databases. It is
for any target country where WHO / SMART / DAK content needs country-specific
contextualization before policy comparison or localization. A country can have
WHO, World Bank, OECD, EU, or national data coverage and still require
localization because implementation depends on health-system structure,
governance, regional variation, digital health infrastructure, policy ownership,
service delivery, and source gaps. WHO database coverage is not enough by
itself.

## When to use

Use this skill for:

- healthcare country overviews;
- regional or national health context summaries;
- identifying main health issues, health system constraints, coverage gaps, or
  sanitary conditions;
- preparing background context before policy comparison, DAK localization, or
  SMART Guidelines adaptation;
- determining what documents or expert input are needed before policy-specific analysis.

## When not to use

Do not use this skill for:

- clinical decision-making or patient advice;
- final national policy drafting;
- direct WHO-versus-country policy comparison;
- unsourced country, health system, sanitary, policy, clinical, or WHO claims;
- replacing WHO, national, legal, policy, clinical, epidemiological, WASH,
  environmental health, or country expert review.

## Expected inputs

Minimum expected input:

1. Target country.

Helpful inputs:

- optional downstream health-area focus, region, population group, or use case;
- source documents pasted into the prompt, attached as files, or already
  present in the conversation;
- national health strategies, country health profiles, programme reports,
  census or survey outputs, health financing reports, health workforce
  documents, WASH or environmental health sources, digital health strategies,
  and health information system documents;
- WHO SMART Guidelines or DAK scope if known, as downstream context rather than
  a required profiling input;
- WHO, World Bank, UNICEF, UNAIDS, GBD, OECD, regional observatory, or other
  reputable public-health sources;
- source URLs, local file paths, publication dates, retrieval dates, and
  language notes when available.

Inputs may be unstructured. Normalize the prompt, attached files, conversation
context, deterministic retrieval outputs, web-reviewed sources, parsed PDFs,
and short unresolved source gaps into a source inventory before writing the
profile.

Source URLs must resolve to usable source material before they are marked `Reviewed`.
A publication page, catalog page, search result, or "Download PDF" page can be
listed as a candidate, but the Agent should follow it to the PDF, dataset,
official attachment, official full-text HTML, or local file and review that
material before citing substantive findings. If only the landing page is
reachable, keep the source as `Candidate source` or `Needs retrieval` and record
the unresolved material endpoint as an evidence gap.

The optional downstream health-area focus can name an area such as
immunization, HIV, tuberculosis, or maternal health when the profile is being
prepared for later policy comparison. It should guide source discovery and
readiness notes, but the country profile should still describe the country's
healthcare system and context overall.

When the downstream focus is immunization, include the bundled WHO immunization
DAK at `assets/who-immunizations-dak.pdf` as an available downstream
comparison source if the file exists. Country Profiling should identify this
source for handoff only; it should not compare the DAK with national policy.

## Execution modes

Use one of three execution modes:

1. Document-only mode. Use when the user provides source documents, excerpts, or
   attachments. Profile only from supplied material and record missing source
   classes as evidence gaps.
2. Deterministic script-assisted retrieval mode. Use when Python scripts are
   available, especially when the human provides only a target country and
   optional downstream focus. This retrieves stable global indicators and
   resolves Agent- or user-supplied country source manifests; it does not
   hardcode country-specific ministry, institute, or policy URLs.
3. Semi-deterministic web-assisted retrieval mode. Use when scripts are
   unavailable but web access is available. Follow the controlled source
   priority and provenance protocol in `context/web-assisted-retrieval.md`.

Use mixed mode when supplied documents are combined with deterministic retrieval
or controlled web-assisted retrieval.

If neither scripts, web access, nor enough documents are available, ask for
source material or produce only a skeleton/gap-analysis profile. Do not draft
unsupported country facts.

See `context/execution-modes.md` for the decision rules.

## Environment setup

When installing, distributing, or running deterministic retrieval in a new
Agent runtime, start with `context/environment-setup.md`. Run the bundled
preflight before live retrieval when scripts are available:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py \
  --require-network
```

Add `--require-pdf` only when the planned run is PDF-capable, such as an
immunization run that will use the bundled WHO DAK or a source-manifest run
that may retrieve official PDF material.

If outbound network access is unavailable, use document-only mode or
semi-deterministic web-assisted retrieval only when the runtime provides
approved web access. Record network failures as evidence gaps.

If the preflight reports missing dependencies, stop before deterministic
retrieval or profile drafting and prompt the user for permission before
installing anything in the execution environment. Name the dependency, why it
is needed, the exact install command, and the fallback if the user declines. Do
not run `pip`, package managers, or environment-editing commands without user
approval.

Treat missing `pypdf` as an approval checkpoint when PDF parsing is actually
needed or attempted. If the preflight with `--require-pdf` fails, or if
retrieval artifacts report `pypdf` missing or `downloaded_parse_failed` for a
PDF source, stop and ask the user whether to install
`skills/country-profiling/sourcing_scripts/requirements.txt`, then rerun the
PDF-capable retrieval step after installation. Continue without installation
only if the user declines or confirms that PDF parsing is not needed, and then
record PDF parsing as a runtime limitation. The retrieval helper exits before
PDF-capable retrieval when `pypdf` is missing; use `--allow-missing-pypdf` only
after the user declines installation.

Use a dedicated output directory for each country profile run. Do not copy or
recreate the skill package inside that output directory. Keep the final country
profile, JSON artifacts, retrieved indicator summaries, source inventories, and
source leads at the output-directory root. Put downloaded or parsed PDF
material under `Parsed sources/`. Keep scratch memory outside the output
directory.

Treat output directories as run artifacts, not repository checkouts. Do not run
or report `git status` from inside an output directory. If repository state is
relevant, run git commands from the source repository root or the installed
skill target only; otherwise omit git-status notes from profile or validation
summaries.

## Workflow

1. Before deterministic script-assisted retrieval in any new installation,
   distribution package, or fresh runtime, run environment setup from
   `context/environment-setup.md`.
2. If setup or retrieval reports missing `pypdf` while PDF parsing is required
   or attempted, ask the user to approve dependency installation before drafting
   the profile. If installation is approved, rerun the PDF-capable retrieval
   step. Do not silently skip PDF parsing unless the user declines installation
   or confirms that PDF parsing is not needed.
3. Identify the target country and any optional downstream health-area focus,
   region, population group, or intended downstream use.
4. If the user supplies documents, use document-only or mixed mode.
5. If the user provides only country and optional focus, use deterministic
   script-assisted retrieval if scripts are available.
6. If scripts are unavailable but web access is available, use
   semi-deterministic web-assisted retrieval.
7. If neither scripts nor web access are available, ask for source material or
   produce only a skeleton/gap-analysis profile.
8. When country-specific official URLs are needed, discover them through
   controlled web-assisted retrieval and pass them to the retrieval helper with
   `--source-manifest` so scripts can resolve, parse, checksum, and record them.
9. Build a source inventory from supplied material, retrieved data, reviewed web
   sources, parsed PDFs, manifest-resolved sources, and short unresolved source
   gaps.
10. Resolve source locations to source material where possible.
11. Classify source types as datasets, official documents, institutional
   profiles, landing pages, reviewed web sources, parsed PDFs, candidate source
   leads, or missing source classes.
12. Decide whether a full profile, limited profile, or skeleton/gap-analysis
   profile is appropriate.
13. Draft the textual profile using `context/profile-schema.md`.
14. Mark unavailable data, failed retrieval, empty source manifests,
   landing-page-only sources, and unreviewed national/regional sources as
   evidence gaps.
15. Separate facts, uncertainties, assumptions, and expert-review needs.
16. Include a `Policy-analysis readiness` section and, when useful, a
   `Policy-comparison handoff` table.
17. State how the output can feed the future Policy Comparison skill.
18. Ask for human review, not manual source-hunting, unless key source classes
   remain missing after controlled retrieval.
19. Do not fabricate missing country context.

When available, consult `examples/` for reference input-output patterns before
drafting. Treat examples as behavior references, not as final policy evidence.

## Output requirements

Always follow `context/profile-schema.md`.

When writing the final profile to a local output folder, use a deterministic
filename derived from the input country name: `<Country_name>_profile.md`.
Replace whitespace and punctuation with single underscores, trim leading or
trailing underscores, and keep the country capitalization from the normalized
input. Examples: `Germany_profile.md`, `United_States_profile.md`,
`Cote_d_Ivoire_profile.md`.

The output is primarily narrative. Tables are used for source inventory,
evidence gaps, and policy-comparison handoff when appropriate.

Every substantive country, health system, health burden, coverage, sanitary
condition, access, financing, workforce, infrastructure, digital health, or data
claim should include:

- source name;
- source type;
- source URL, local file path, or dataset identifier;
- publication or retrieval date when available;
- confidence level or uncertainty note;
- review need when the claim affects later policy analysis.

Precise indicator claims must include indicator source, code, year, value, URL,
and retrieval date when relevant.

## Sourcing script usage

Maintained retrieval and validation tooling lives in
`skills/country-profiling/sourcing_scripts/`.

Check a new environment:

```bash
python3 skills/country-profiling/sourcing_scripts/check_environment.py
```

For a profile run, provide an explicit output directory:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --output-dir "/path/to/country-profile-output"
```

This keeps `retrieved-indicators.json`, `web-reviewed-sources.json`,
`source-leads.md`, and related Markdown artifacts at the output-folder root.
Downloaded or parsed PDFs are written under `Parsed sources/`.

The deterministic baseline retrieval helper is preferred when the human gives
only a country and optional focus:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream health-area focus>" \
  --source-manifest "<optional Agent-discovered source manifest>" \
  --output-dir "/path/to/country-profile-output"
```

Validate a completed profile:

```bash
python3 skills/country-profiling/sourcing_scripts/validate_profile.py <profile.md>
```

Script outputs are support artifacts. A failed retrieval run does not
automatically prevent profile drafting if supplied sources are adequate. A
successful retrieval does not prove that all country-specific evidence exists;
baseline indicators, reviewed web/PDF artifacts, and short unresolved gaps must
not be treated as complete country evidence.

Country-specific institutional discovery is intentionally Agent-led rather than
hardcoded. Use `context/source-manifest-schema.md` when preparing a manifest of
official ministry, public-health, statistics, policy, digital health, programme,
or registry sources for the retrieval helper.

## Safety and uncertainty

- Preserve traceability from claims to sources.
- Use explicit source references wherever possible.
- Label missing, stale, conflicting, or uncertain content.
- Keep global or regional evidence separate from country-specific evidence.
- Do not infer national policy, service availability, sanitary conditions, or
  coverage from missing documents.
- Recommend human expert review where evidence is incomplete, ambiguous,
  conflicting, stale, locally sensitive, or likely to affect later policy
  comparison.
- Do not claim completeness from retrieved indicators or web search alone.
