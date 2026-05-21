# Example format

Use this file as the format for a future example. Do not treat it as a completed example.

Placeholder only. Add real WHO and country-specific sources before using this as an evaluation example.

## Example input format

```md
# Country profile request

## Country

<Country>

## Optional downstream focus

<None/general overview, or a downstream health area such as immunization when preparing later policy comparison>

## Intended downstream use

<Policy comparison, SMART Guidelines localization, DAK preparation, or general context only>

## Supplied source material

| Source | Source type | Publisher | Date | URL or file path | Notes |
|---|---|---|---|---|---|
| <source title> | <source class> | <publisher> | <date> | <direct PDF, dataset, official full-text/attachment URL, or local file path> | <why it matters; note if only a landing page is available> |

## Retrieval note

<If no documents are supplied, use deterministic script-assisted retrieval where
available. If scripts are unavailable but web access exists, use controlled
web-assisted retrieval.>

## Known limitations

- <missing source class, stale document, language limitation, or scope limitation>
```

## Example output format

```md
# Country healthcare profile: <Country> — <optional downstream health-area focus>

## Profile metadata

- Country:
- Optional downstream health-area focus, region, or population group:
- Profile date:
- Profile author or agent:
- Intended downstream use:
- Retrieval mode: <document-only | deterministic script-assisted | semi-deterministic web-assisted | mixed>
- Profile evidence level: <full profile | limited profile | skeleton/gap-analysis profile>
- Retrieval date:
- Retrieved indicator bundle path, if available:
- Source lead bundle path, if available:
- Web-reviewed source inventory path or note, if available:
- Source manifest path or note, if available:
- Known input limitations:

## Executive summary

<Short textual summary of the country's healthcare context, main issues, system constraints, and readiness for later policy analysis.>

## Source inventory

| Source | Source type | Publisher | Date | URL or file path | Relevance | Status |
|---|---|---|---|---|---|---|
| <source title> | <source class> | <publisher> | <date> | <url-or-path> | <relevance> | Candidate source |

## Country context snapshot

<Text with source-backed context.>

## Population health overview

<Text with source-backed context.>

## Main health issues and burden

<Text with source-backed context.>

## Health system organization and capacity

<Text with source-backed context.>

## Healthcare access and coverage

<Text with source-backed context.>

## Sanitary conditions and environmental health

<Text with source-backed context.>

## Health financing and affordability

<Text with source-backed context.>

## Health workforce, infrastructure, and supply availability

<Text with source-backed context.>

## Digital health and health information systems

<Text with source-backed context.>

## Equity, vulnerable groups, and regional variation

<Text with source-backed context.>

## Current concerns, risks, and watchpoints

<Text with source-backed context.>

## Policy-analysis readiness

<State whether later policy comparison is ready, partially ready, or blocked. Do not perform policy comparison here.>

## Policy-comparison handoff

<Optional. Include when useful for the future Policy Comparison skill.>

| Downstream need | Why it matters | Available evidence | Missing source or uncertainty | Suggested next action |
|---|---|---|---|---|
| <need> | <reason> | <source-backed evidence or none> | <gap/uncertainty> | <next action> |

## Evidence gaps and expert input needed

| Gap or uncertainty | Why it matters | Suggested next source or action | Review owner |
|---|---|---|---|
| <gap> | <impact> | <next source/action> | <owner> |

## Sources

- <source title>, <publisher>, <date>, <URL/path>, retrieved <date if applicable>.
```
