# WHO documentation and data retrieval guidance

This note records source classes that can support healthcare country profiling.
Retrieval is optional assistance for source discovery and evidence collection;
it is not a substitute for source review.

For minimal-input profiling, prefer
`sourcing_scripts/retrieve_country_profile_data.py` when Python scripts are available.
That script retrieves selected World Bank baseline indicators, configured WHO
GHO indicators, stable WHO/DAK artifacts where relevant, and
manifest-supplied institutional web/PDF sources with provenance.
Generic WHO pages must not be treated as country-specific evidence unless a
country-specific document or country-filtered dataset is actually retrieved and
reviewed.

Country profiling comes first. Later policy comparison may use the profile to decide which national policies, guidelines, reporting artifacts, or terminology sources to retrieve next.

## Recommended WHO source classes

### WHO country and regional sources

Use WHO country pages, country cooperation strategies, regional observatory profiles, and country health overviews to identify national priorities, broad health system context, and WHO-country collaboration priorities.

### WHO Global Health Observatory OData API

The Global Health Observatory exposes WHO health data through an OData API. Useful endpoints include:

```text
https://ghoapi.azureedge.net/api/Dimension
https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues
https://ghoapi.azureedge.net/api/Indicator
https://ghoapi.azureedge.net/api/<INDICATOR_CODE>
```

Use this for structured country indicators only when stable indicator codes and
country filters are configured. The maintained immunization focus currently
retrieves DTP3 (`WHS4_100`), MCV1 (`WHS8_110`), MCV2 (`MCV2`), and PCV3
(`PCV3`). If indicator codes are uncertain, do not invent values.

### WHO SCORE documents

SCORE country summaries describe health information system strengths and weaknesses. This is useful for profiling data system readiness, CRVS, reporting, surveillance, and data-use risks.

### Global Health Expenditure Database

The Global Health Expenditure Database provides comparable health expenditure data. Use this when the profile needs financing, public spending, out-of-pocket spending, or financial protection context.

### National Health Workforce Accounts

Use National Health Workforce Accounts or related workforce sources when workforce distribution, capacity, or service delivery feasibility matters.

### WHO/UNICEF WASH and environmental health sources

Use WASH, sanitation, drinking water, hygiene, air pollution, climate, and environmental health sources when sanitary conditions or environmental risks are relevant to country health context.

## Optional downstream-focus sources

When the user provides a downstream health-area focus, add topic-specific WHO sources and indicator searches. Examples:

| Focus | Search terms |
|---|---|
| Immunization | immunization, vaccination, vaccine |
| Tuberculosis | tuberculosis, TB |
| HIV | HIV |
| Maternal health | maternal, antenatal, birth |
| Child health | child mortality, neonatal, under-five |
| WASH | water, sanitation, hygiene |
| NCDs | cardiovascular, diabetes, cancer, noncommunicable |

## Suggested retrieval workflow

When deterministic baseline retrieval is useful, run:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream health-area focus>" \
  --source-manifest "<optional Agent-discovered source manifest>" \
  --output-dir "/path/to/country-profile-output"
```

If WHO-specific source discovery is needed beyond configured retrieval, use the
semi-deterministic web-assisted retrieval protocol in
`web-assisted-retrieval.md` and record reviewed sources separately from
candidate source leads or unresolved gaps.

## Country-specific documentation note

For final profile use, country-specific documents should be supplied as inputs or retrieved through an explicit retrieval step with source verification. Generic WHO pages are not enough to support claims about country health conditions, sanitary coverage, service availability, or policy readiness.
