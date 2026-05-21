# Skills Index

This repository contains Agent Skills for WHO SMART Guidelines and Digital
Adaptation Kit localization workflows. Each skill lives in its own folder under
`skills/`.

## Country Profiling

- Status: Active.
- Location: `skills/country-profiling/`.
- Purpose: Builds a source-backed healthcare country profile from minimal
  country input, supplied documents, deterministic baseline retrieval, or
  controlled web-assisted retrieval.
- Output: A markdown country profile, retrieval artifacts, reviewed-source
  artifacts, parsed PDFs under `Parsed sources/`, evidence gaps, and
  expert-review needs.
- Boundary: Does not compare WHO guidance with national policy and does not
  replace expert review.

## Policy Comparison

- Status: Scaffold only.
- Location: `skills/policy-comparison/`.
- Purpose: Describes a future workflow for comparing WHO SMART Guidelines or
  DAK artifacts with reviewed country-specific policy material.
- Inputs: Intended to use Country Profiling outputs as context, alongside
  reviewed WHO and national policy sources.
- Boundary: Not implemented; should not be used for comparison findings yet.

## Possible Future Extensions

- Terminology mapping for codes, value sets, schedules, formularies, or
  data elements.
- SMART/FHIR artifact inspection through approved read-only tooling.
- Structured handoff between country context, policy comparison, and
  localization planning.

All skills are review aids. They do not make clinical decisions, provide
patient advice, draft final national policy, or replace WHO, ministry, legal,
clinical, programme, terminology, epidemiological, WASH, environmental health,
or country expert review.
