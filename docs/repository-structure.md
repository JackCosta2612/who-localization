# Repository structure

This repository is organized as a collection of localization skills rather than
a single skill package.

## Root files

| Path | Purpose |
|---|---|
| `README.md` | Repository overview, setup guidance, and skill usage commands. |
| `SKILLS.md` | Index of available skills. |
| `docs/` | Cross-skill design notes. |
| `shared/` | Shared assets or materials that apply to more than one skill. |
| `skills/` | Individual Agent Skill packages. |

## Skill package convention

Each skill should follow this structure:

```text
skills/<skill-name>/
├── SKILL.md
├── README.md
├── context/
├── examples/
└── scripts/ or sourcing_scripts/
```

Keep run outputs outside shippable skill packages. Country Profiling writes
retrieval artifacts to the requested output directory and downloaded or parsed
PDFs under `Parsed sources/`.

## Current skills

| Skill | Status |
|---|---|
| `skills/country-profiling/` | Implemented skill for source-backed textual healthcare country profiles. |
| `skills/policy-comparison/` | Scaffold for a later policy-comparison skill. |

## Adding a new skill

When adding another skill:

1. Create `skills/<new-skill-name>/`.
2. Add a valid `SKILL.md` with frontmatter.
3. Keep long definitions in `context/`.
4. Put structural examples in `examples/`.
5. Put lightweight validation or helper code in `scripts/`, or in
   `sourcing_scripts/` when the skill has source retrieval and source registry
   helpers.
6. Keep output artifacts outside the shippable skill package unless they are
   required bundled resources.
7. Update the root `README.md` and `SKILLS.md`.
