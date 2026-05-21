---
name: policy-comparison
description: >-
  Scaffold for a future source-backed policy comparison skill that will compare
  WHO SMART Guidelines or DAK artifacts with country-specific policy material,
  using country profiles and retrieved source inventories as context.
license: MIT
metadata:
  compatibility: Model-neutral Agent Skill scaffold.
  version: "0.1"
---

# Policy Comparison Skill Scaffold

## Purpose

This is a placeholder for a future policy comparison skill. The intended skill
will compare a selected WHO SMART Guidelines or Digital Adaptation Kit artifact
with country-specific policy, programme, operational, terminology, reporting,
or implementation material.

The skill is not implemented yet. It should not be used to produce alignment
findings, divergence assessments, localization recommendations, or policy
decisions.

## Intended Inputs

A future comparison run should use:

- a target country;
- a health area or implementation domain;
- the relevant WHO SMART Guidelines, DAK, or other WHO normative artifact;
- country-specific policy material, such as national guidelines, laws,
  strategies, schedules, circulars, operational manuals, registers, reporting
  forms, data dictionaries, terminology lists, product lists, or financing and
  eligibility rules;
- country context artifacts from the Country Profiling skill, including the
  profile markdown, source inventory, evidence gaps, reviewed-source artifacts,
  parsed PDFs under `Parsed sources/`, and any source manifest used during
  retrieval.

## Intended Workflow

The future skill should:

1. Confirm the comparison scope and the exact WHO artifact version.
2. Confirm that country-specific source material is available and reviewed.
3. Use the Country Profiling output only as context, not as a substitute for
   policy source review.
4. Build a source inventory with reviewed WHO and country material.
5. Compare only claims that are supported by reviewed sources.
6. Separate alignment, divergence, ambiguity, missing evidence, and expert
   review needs.
7. Preserve source traceability for every substantive comparison finding.
8. Stop before final policy drafting or localization decisions.

## Safety Boundaries

The future skill should not:

- make clinical decisions or provide patient advice;
- draft final national policy;
- infer country policy from global WHO material alone;
- use a country profile as evidence for the contents of national policy;
- replace WHO, ministry, legal, clinical, programme, terminology, or country
  expert review.
