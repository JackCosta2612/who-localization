# Semi-deterministic web-assisted retrieval

Use this protocol when Country Profiling scripts are unavailable but web access
is available. The goal is controlled source retrieval for a draft profile that
requires human review, not extensive manual source construction.

Web-assisted retrieval should remain structured and source-prioritized. It is
not open-ended browsing.

## Source priority

Search source classes in this order:

1. WHO country / regional pages and WHO data sources.
2. European Observatory / OECD / EU country profiles where relevant.
3. World Bank Data / World Bank country indicators.
4. National Ministry of Health.
5. National public health institute.
6. National medicines agency / vaccine authority, where relevant.
7. National statistics office.
8. Peer-reviewed or institutional publications only if official sources are
   unavailable or insufficient.

Prefer official and institutional sources. Use peer-reviewed or secondary
institutional literature to fill context gaps only when official sources are
missing, stale, inaccessible, or insufficient.

## Retrieval record

For every reviewed source or candidate source lead, record:

- source title;
- publisher;
- URL;
- publication or dataset date;
- retrieval date;
- source type;
- status;
- whether the source was actually reviewed or only identified.

Allowed statuses should map to the profile schema:

- `Reviewed`;
- `Candidate source`;
- `Needs retrieval`;
- `Needs expert validation`;
- `Not available in supplied material`.

## Landing page rule

Do not use a landing page as if it were the PDF, dataset, official attachment,
or full-text source.

If a landing page links to a PDF, record the landing page as a landing page
unless the actual PDF URL is retrieved and reviewed. If the PDF or dataset is
missing or inaccessible, mark it as an evidence gap.

Generic dashboards, topic pages, institutional home pages, publication catalogs,
search pages, and download pages are source leads. They can support source
discovery but cannot support precise country claims unless their contents were
actually reviewed and are specific enough for the claim.

## Reviewed evidence versus candidate leads

Separate:

- reviewed evidence used in the profile;
- datasets retrieved or reviewed;
- web-reviewed sources;
- candidate source leads identified but not reviewed;
- landing pages requiring PDF, dataset, or attachment retrieval;
- inaccessible sources and missing documents.

This distinction should appear in the source inventory, source notes, and
evidence gaps.

## Country-specific source leads

For any target country, translate the source-priority list into country-specific
queries and reviewed source records. Prefer sources that can be resolved to
country pages, country-filtered datasets, full-text HTML, PDFs, or official
attachments. Do not copy source leads from a reference example into another
country profile unless they are actually relevant to that country.

Useful query patterns include:

- WHO country page or WHO regional country profile for the target country;
- regional observatory or institutional country overview where one exists;
- country health profile from OECD, EU, PAHO, WHO regional offices, World Bank,
  or another institutional publisher where relevant;
- World Bank country-filtered data for baseline indicators;
- WHO GHO configured indicators when the focus has stable configured codes;
- national Ministry of Health or equivalent;
- national public health institute, disease-control center, or equivalent;
- medicines agency, vaccine authority, or regulatory authority where relevant;
- national statistics office or official open-data portal;
- current official policy, strategy, plan, calendar, circular, or attachment
  for the downstream focus.

For immunization-focused downstream work, also look for national coverage
datasets, official circulars, national vaccine calendar attachments, regional or
subnational implementation documents, pharmacovigilance material,
registry/reporting specifications, and digital health data-flow sources. Country
Profiling should identify these as source classes and gaps; it should not
compare national policy with WHO guidance.

When scripts are available, record reviewed or candidate country-specific
source URLs in a source manifest using `source-manifest-schema.md`, then pass
that manifest to `retrieve_country_profile_data.py --source-manifest`. This
keeps country-specific official source discovery Agent-led while preserving
scripted parsing, checksums, material-endpoint status, and provenance.

If the bundled local DAK exists at `assets/who-immunizations-dak.pdf`,
include it as an available WHO SMART / DAK artifact for later Policy Comparison.
Do not treat it as evidence about the target country's health system or
implementation context.

## Drafting rules

- Prefer latest sources, but do not discard authoritative older health-system
  reviews if still relevant for structure, governance, or implementation
  context.
- Do not claim completeness from web retrieval alone.
- Do not make precise statistics unless a reviewed source or retrieved dataset
  supports the value, year, and definition.
- Keep WHO/global guidance separate from country-specific evidence.
- Mark missing or inaccessible documents as evidence gaps.
- Ask for human review of the draft and source inventory, not for manual source
  construction unless key source classes remain missing after controlled
  retrieval.
