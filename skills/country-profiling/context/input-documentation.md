# Input documentation guidance

The skill can start from only a country name. Country Profiling is not only for
countries missing from WHO databases; it is for any target country where WHO /
SMART / DAK content needs country-specific contextualization before later policy
comparison or localization.

The profile should combine deterministic public-health data where available,
semi-deterministic web-assisted retrieval when scripts are unavailable, official
or institutional documents, source inventories, evidence gaps, and
implementation context. WHO database coverage alone is not enough for
localization because service delivery, governance, digital systems, regional
variation, and policy ownership still need country context.

## Minimum input request

Ask for:

- country name.

Helpful but not required:

- downstream health-area focus or downstream use;
- region or population group;
- WHO SMART Guidelines or DAK scope, if known;
- any country-specific health documents already available.

When deterministic script-assisted retrieval is useful, these values can be
passed into the baseline retrieval command:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream health-area focus>" \
  --output-dir "/path/to/country-profile-output"
```

The output files can be treated as source artifacts, not as a complete evidence
base.

If country documents are available, record each one in this format when building
the source inventory:

```text
title|document type|path-or-url|date
```

The path or URL should point as close as possible to the actual source
material. Prefer a direct PDF, dataset export, official attachment page,
official full-text page, or local file over a catalog or publication landing
page. If only a landing page is available, record it, but keep the source as
candidate material until the evidence-bearing document is opened.

Domain-specific policy documents are not mandatory for Country Profiling. They
become important when the profile is used to prepare the future Policy
Comparison skill.

If Python scripts are unavailable but web access exists, use
`web-assisted-retrieval.md` to retrieve or identify the same source classes in a
controlled way. Record reviewed sources separately from candidate source leads.

## Recommended source classes by profile section

### General country and health overview

- WHO country profile, country cooperation strategy, regional observatory profile, or equivalent country health overview.
- National health strategy or health sector strategic plan.

### Population health and burden

- Recent burden-of-disease, mortality, surveillance, health statistics, census, DHS/MICS, or household survey source.

### Health system organization

- Health sector plan, health system review, service delivery assessment, emergency preparedness review, or ministry of health annual report.

### Access and coverage

- UHC monitoring source, insurance or entitlement documentation, benefit package summary, service availability assessment, or access/quality survey.

### Financing

- Health financing, UHC, insurance, expenditure, or financial protection source.

### Workforce and infrastructure

- Health workforce and facility-capacity source.

### WASH and environmental health

- WASH, sanitary conditions, environmental health, pollution, climate, or vector-risk source.

### Digital health and health information systems

- Digital health strategy, health information system strategy, CRVS source, surveillance-system source, or data-quality report.

### Equity and vulnerable groups

- Equity analysis, poverty or social determinants source, migrant/refugee source, disability source, subnational health source, or humanitarian assessment.

### Current risks

- Recent outbreak reports, emergency updates, climate risk assessments, medicine shortage notices, workforce-strain reports, or financing-risk reports.

### Policy-comparison source classes

Collect these only if the profile is preparing a later comparison:

- national health strategy;
- domain-specific national guideline;
- service delivery model or operational manual;
- financing, eligibility, or coverage rules;
- reporting forms, registers, indicators, or data dictionaries;
- terminology, coding, formulary, schedule, or product-list source;
- implementation guidance or programme monitoring document.

For immunization-focused profiles, also list the bundled WHO immunization DAK at
`assets/who-immunizations-dak.pdf` as an available downstream comparison
source when present. It should be carried into the Policy Comparison handoff,
not used to perform comparison inside Country Profiling.

## Input quality checklist

Before profiling, record:

- whether each source is official, draft, archived, secondary, modelled, or survey-based;
- publication year;
- retrieval date;
- language;
- country ministry, agency, or organization responsible;
- whether the source covers the country nationally or only a region/population group;
- whether the source covers the optional downstream health-area focus directly;
- whether the URL is direct source material or only a landing/download page;
- whether the material endpoint was opened and reviewed before use;
- whether a newer version may exist.

## Handling missing inputs

If a country source is missing:

- mark it as `Needs retrieval`;
- do not infer national health conditions from global guidance alone;
- propose likely source owners, such as ministry of health, national statistics office, public health institute, WHO country office, UNICEF, World Bank, regional observatory, or relevant programme authority;
- flag the gap for human follow-up.

If neither scripts nor enough documents are available, ask for source material
or produce only a skeleton/gap-analysis profile. Do not draft unsupported
country facts.
