# Retrieved baseline indicators: Italy (ITA)

- Retrieval date: 2026-05-16T15:07:59+00:00
- Downstream focus: immunization
- Registry: skills/country-profiling/sourcing_scripts/indicator_registry.json

These indicators provide a small baseline context layer. They do not prove country-profile completeness and must be combined with reviewed country documents, source inventories, and evidence gaps.

## World Bank indicators

| Indicator | Code | Value | Unit | Year | Status | Source URL |
|---|---|---|---|---|---|---|
| Population, total | SP.POP.TOTL | 58952704 | people | 2024 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SP.POP.TOTL?format=json&per_page=100 |
| Life expectancy at birth, total | SP.DYN.LE00.IN | 83.9512195121951 | years | 2024 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SP.DYN.LE00.IN?format=json&per_page=100 |
| Current health expenditure per capita | SH.XPD.CHEX.PC.CD | 3397.68798828 | current US$ | 2024 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SH.XPD.CHEX.PC.CD?format=json&per_page=100 |
| Out-of-pocket expenditure as percentage of current health expenditure | SH.XPD.OOPC.CH.ZS | 22.30979538 | percent | 2024 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SH.XPD.OOPC.CH.ZS?format=json&per_page=100 |
| Physicians per 1,000 people | SH.MED.PHYS.ZS | 4.191 | per 1,000 people | 2022 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SH.MED.PHYS.ZS?format=json&per_page=100 |
| Hospital beds per 1,000 people | SH.MED.BEDS.ZS | 3.06 | per 1,000 people | 2022 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SH.MED.BEDS.ZS?format=json&per_page=100 |
| People using at least basic sanitation services | SH.STA.BASS.ZS | 99.8849043408577 | percent of population | 2024 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SH.STA.BASS.ZS?format=json&per_page=100 |
| People using at least basic drinking water services | SH.H2O.BASW.ZS | 99.9170340740928 | percent of population | 2024 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SH.H2O.BASW.ZS?format=json&per_page=100 |
| Immunization, measles | SH.IMM.MEAS | 95 | percent of children ages 12-23 months | 2024 | retrieved | https://api.worldbank.org/v2/country/ITA/indicator/SH.IMM.MEAS?format=json&per_page=100 |

## WHO GHO indicators

| Indicator | Code | Value | Unit | Year | Status | Source URL |
|---|---|---|---|---|---|---|
| DTP3 immunization coverage among 1-year-olds | WHS4_100 | 94.0 | percent | 2024 | retrieved | https://ghoapi.azureedge.net/api/WHS4_100 |
| MCV1 immunization coverage among 1-year-olds | WHS8_110 | 95.0 | percent | 2024 | retrieved | https://ghoapi.azureedge.net/api/WHS8_110 |
| MCV2 immunization coverage by nationally recommended age | MCV2 | 84.0 | percent | 2024 | retrieved | https://ghoapi.azureedge.net/api/MCV2 |
| PCV3 immunization coverage among 1-year-olds | PCV3 | 90.0 | percent | 2024 | retrieved | https://ghoapi.azureedge.net/api/PCV3 |

## Retrieval caveats

- Use precise indicator source, code, year, and retrieval date in profile claims.
- `missing_value` means the configured indicator did not return a non-empty country value.
- `failed` means retrieval failed and should be recorded as an evidence gap.
- WHO GHO retrieval is intentionally limited to configured indicator codes; it is not a full GHO data platform.
