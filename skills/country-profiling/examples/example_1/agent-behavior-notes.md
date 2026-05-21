# Agent behavior notes

This example demonstrates the preferred minimal-input Country Profiling pattern:
country plus optional downstream focus, not a human-built source packet.

## Expected behavior

- Use deterministic retrieval to produce a baseline indicator bundle when
  scripts are available, including configured World Bank and WHO GHO indicators.
- Resolve manifest-supplied institutional web sources and parsed PDFs before
  producing a long list of candidate leads.
- Use semi-deterministic web-assisted retrieval when scripts are unavailable,
  following the source priority and provenance rules in
  `context/web-assisted-retrieval.md`.
- Treat unresolved source gaps carefully. A source gap is not reviewed evidence;
  it is an instruction for targeted follow-up only when needed by the downstream
  comparison scope.
- Use retrieved indicators as context, not as proof of completeness.
- Ask for human review of the draft and source inventory, not for manual source
  construction, unless key source classes remain missing.
- Feed the Policy Comparison skill by identifying context, likely source
  classes, the bundled immunization DAK, and gaps without performing comparison.

## Boundary to enforce

Country Profiling may identify the target country's health-system structure,
baseline indicators, configured WHO GHO estimates, reviewed institutional
sources, official source anchors, remaining source gaps, and the bundled WHO
immunization DAK at `assets/who-immunizations-dak.pdf` when the focus is
immunization. It should not compare national policy with the DAK or WHO
guidance, recommend schedule changes, make clinical judgments, or claim policy
readiness without source support.

## Reliability pattern

When scripts are available, the agent should preserve indicator source, code,
value, year, URL, retrieval date, and status. Web/PDF artifacts should preserve
publisher, title, source type, URL, retrieval date, local path when downloaded,
checksum, parse status, and a bounded text summary.

When scripts are unavailable, the agent should use the approved source priority
list, record publisher/title/date/URL/retrieval date/source type/status, and
separate reviewed evidence from candidate leads. Landing pages and inaccessible
PDFs become evidence gaps, not hidden assumptions. Avoid emitting broad source
inventories when targeted retrieval has already produced enough usable context.
