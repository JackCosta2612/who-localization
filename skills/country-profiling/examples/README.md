# Country Profiling reference examples

These folders contain reference examples for the Country Profiling skill. They
are behavior-shaping examples, not final country evidence or clinical/policy
validation.

Use them to see how a country profile request should be normalized, how the
profile schema should be filled, how sources and gaps should be represented, and
where the profile should stop before WHO-versus-country policy comparison.

The structural validator may be run on `reference-output.md` files as a
document consistency check, but the main purpose of these examples is to reduce
variance in agent behavior during real skill use.

## Example 1

`example_1/` is a retrieval-assisted minimal-input profile with an
immunization-readiness handoff.

It demonstrates a country profile that starts from country plus optional focus,
uses deterministic baseline retrieval artifacts, demonstrates controlled
web-assisted fallback discipline, keeps policy comparison out of scope, and
combines readable narrative, source discipline, and conservative handoff/gap
framing.

The example contains:

- `input.md`: a realistic user request that should activate the skill;
- `reference-output.md`: a concise source-backed output pattern following
  `context/profile-schema.md`;
- `data/retrieved-indicators.json`: deterministic baseline indicator bundle;
- `data/retrieved-indicators.md`: human-readable retrieved indicator artifact;
- `data/web-reviewed-sources.json`: reviewed HTML, direct PDF URLs, parsed text
  summaries, checksums, URLs, and parse statuses;
- `data/web-reviewed-sources.md`: human-readable reviewed web/PDF artifact;
- `data/source-leads.md`: short unresolved source gaps and fallback guidance;
- `../assets/who-immunizations-dak.pdf`: bundled immunization DAK
  source for later Policy Comparison when the downstream focus is immunization;
- `source-notes.md`: source rationale, reviewed-versus-candidate distinctions,
  and proposed follow-up source work;
- `agent-behavior-notes.md`: what behavior the draft is meant to enforce,
  including where it stops before policy comparison.

If scripts are unavailable, the same example should be interpreted through
semi-deterministic web-assisted retrieval: use approved source classes, prefer
official and institutional sources, record strict provenance, and keep
landing-page-only or inaccessible material as evidence gaps.

## Use guidance

Before drafting a new country profile, consult the closest example for the
requested use case. Imitate the structure, source discipline, uncertainty
handling, and handoff framing. Do not copy country facts into a different
country, and do not treat these drafts as final WHO or national policy evidence.
Retrieved data artifacts are included as reference material only and require
human review before reuse in real policy work.
