# Country healthcare profile output schema

The Country Profiling skill should produce a markdown document with the sections below.

The profile may be produced from user-provided documents, deterministic
script-assisted retrieval outputs, semi-deterministic web-assisted retrieval, or
a combination of these. If a source class is missing, record it as an evidence
gap rather than filling it from assumption.

When writing the profile to a local output folder, use the deterministic
filename `<Country_name>_profile.md`: replace whitespace and punctuation in the
normalized input country name with single underscores and trim leading or
trailing underscores.

## Required sections

```md
# Country healthcare profile: <Country> — <optional downstream health-area focus>

## Profile metadata

## Executive summary

## Source inventory

## Country context snapshot

## Population health overview

## Main health issues and burden

## Health system organization and capacity

## Healthcare access and coverage

## Sanitary conditions and environmental health

## Health financing and affordability

## Health workforce, infrastructure, and supply availability

## Digital health and health information systems

## Equity, vulnerable groups, and regional variation

## Current concerns, risks, and watchpoints

## Policy-analysis readiness

## Evidence gaps and expert input needed

## Sources
```

Add `## Policy-comparison handoff` after `## Policy-analysis readiness` when it
helps structure downstream work.

If there is no specific focus, use `# Country healthcare profile: <Country>`.

## Profile metadata

Include:

- country;
- optional downstream health-area focus, region, or population group;
- profile date;
- profile author or agent;
- intended downstream use, if known;
- retrieval mode: `document-only`, `deterministic script-assisted`,
  `semi-deterministic web-assisted`, or `mixed`;
- profile evidence level: `full profile`, `limited profile`, or
  `skeleton/gap-analysis profile`;
- retrieval date;
- retrieved indicator bundle path, if available;
- source lead bundle path, if available;
- web-reviewed source inventory path or note, if available;
- source manifest path or note, if available;
- known input limitations.

## Source inventory

Use this table:

```md
| Source | Source type | Publisher | Date | URL or file path | Relevance | Status |
|---|---|---|---|---|---|---|
```

Supported source types include:

- `Dataset`
- `Official document`
- `Institutional profile`
- `Landing page`
- `Candidate source lead`
- `Web-reviewed source`
- `Parsed PDF`
- `National ministry`
- `National public health institute`
- `National medicines agency`
- `National statistics office`
- `WHO source class`
- `Regional implementation source`

Allowed `Status` values:

- `Reviewed`
- `Candidate source`
- `Needs retrieval`
- `Needs expert validation`
- `Not available in supplied material`

Use `Reviewed` only when the profile actually uses the source as evidence. Use
`Candidate source` for sources identified but not fully reviewed.

`Reviewed` also requires a usable material endpoint. The Agent must have opened
and reviewed the PDF, dataset, official attachment, official full-text HTML, or
local file that contains the evidence. A publication landing page or download
page can identify a source, but it should remain `Candidate source` or `Needs
retrieval` until the material endpoint is resolved and reviewed.

## Narrative sections

The main body should be textual, with short paragraphs and source-backed
statements. Use bullets only where they improve scanability.

Precise data claims must include the indicator source, indicator code when
applicable, year, and retrieval date if the value comes from a retrieved
dataset. For example, use the source artifact wording rather than a bare number:
`World Bank indicator SP.DYN.LE00.IN, 2024 value, retrieved 2026-05-16`.

Do not treat baseline indicators as complete country context. Combine them with
reviewed documents, source inventories, implementation context, and evidence
gaps.

### Country context snapshot

Summarize the basic demographic, geographic, administrative, economic, or
regional context needed to understand health conditions. Avoid general
encyclopedia content unless it directly affects healthcare context.

### Population health overview

Summarize life expectancy, mortality patterns, population structure, maternal
and child health context, and broad health outcomes when supported by sources.

### Main health issues and burden

Discuss major communicable diseases, noncommunicable diseases, injuries, mental
health concerns, maternal and child health issues, outbreaks, or other burdens
relevant to the country. Note whether evidence is national, regional, modelled,
reported, or survey-based.

### Health system organization and capacity

Describe governance, public/private roles, primary care, referral care,
hospital capacity, decentralization, emergency preparedness, service delivery
constraints, and implementation environment when sourced.

### Healthcare access and coverage

Discuss universal health coverage, insurance or entitlement models, benefit
coverage, service availability, affordability, geographic access, waiting times,
and continuity of care when sourced.

### Sanitary conditions and environmental health

Discuss drinking water, sanitation, hygiene, waste management, air pollution,
housing, climate and environmental risks, vector conditions, food safety, or
occupational/environmental exposures when sourced.

### Health financing and affordability

Discuss total health expenditure, public spending, out-of-pocket payments,
external financing, financial hardship, or programme funding vulnerabilities
when sourced.

### Health workforce, infrastructure, and supply availability

Discuss workforce density and distribution, training capacity, facility
availability, laboratories, supply chains, essential medicines, vaccines,
diagnostics, and equipment when sourced.

### Digital health and health information systems

Discuss civil registration and vital statistics, routine health information
systems, registries, surveillance, data quality, interoperability, digital
health strategy, and patient-level system readiness when sourced.

### Equity, vulnerable groups, and regional variation

Discuss disparities by income, region, urban/rural status, sex, age,
disability, migration status, ethnicity, conflict exposure, or other locally
relevant dimensions when sourced.

### Current concerns, risks, and watchpoints

Summarize active or recent health system pressures, outbreaks, humanitarian
conditions, climate risks, workforce strain, medicine shortages, financing
risks, trust or misinformation concerns, and other watchpoints when supported
by evidence.

## Policy-analysis readiness

Explain whether the available profile is sufficient to proceed to later policy
comparison. This section should not perform policy comparison.

Address:

- which downstream health areas appear most relevant for later policy comparison;
- which national policy source classes are needed;
- which systems are in place that will affect policy interpretation;
- which source gaps prevent safe comparison;
- whether country-specific policy sources appear current and authoritative;
- what expert review is needed before policy comparison;
- whether the profile is sufficient for a first policy-comparison pass;
- any limits that should constrain downstream DAK or SMART Guidelines localization work.

If the evidence base is too thin, explicitly state
`Not ready for policy comparison` and explain why.

## Policy-comparison handoff

Add this section when it helps structure downstream work. This section should
prepare the future Policy Comparison skill; it should not compare WHO and
national policy.

Use this table:

```md
| Downstream need | Why it matters | Available evidence | Missing source or uncertainty | Suggested next action |
|---|---|---|---|---|
```

Common downstream needs include:

- national health strategy;
- domain-specific guideline;
- service delivery model;
- financing or coverage rules;
- data or reporting system;
- terminology or coding system;
- implementation constraints;
- expert validation.

## Evidence gaps and expert input needed

Use this table:

```md
| Gap or uncertainty | Why it matters | Suggested next source or action | Review owner |
|---|---|---|---|
```

Include missing source classes, conflicting evidence, stale documents, unclear
applicability, unsupported country or downstream-focus facts, and claims that
could affect later policy analysis.

Include gaps from:

- missing data;
- unavailable indicator values;
- failed retrieval;
- empty or non-matching source manifests;
- landing-page-only sources;
- inaccessible PDFs or datasets;
- national or regional source classes not reviewed;
- policy source not yet retrieved for later comparison;
- digital health, registry, reporting, or interoperability sources not yet
  reviewed.

## Sources

List every source used. Include URLs, local file paths, dataset identifiers,
publication dates, and retrieval dates for web sources when available.

## Validation expectations

The structural validator checks for:

- all required sections;
- a source inventory table;
- an evidence gaps and expert input table;
- the optional policy-comparison handoff table when the section is present;
- controlled values for source status.

The validator also performs limited source-artifact semantic checks, such as
flagging `Reviewed` landing-page rows, missing locators for reviewed sources,
missing local paths, and empty web-reviewed artifacts when they can be read.
It does not check whether the country profile is factually, epidemiologically,
clinically, legally, operationally, policy, source-interpretation, or
WHO-interpretation correct.
