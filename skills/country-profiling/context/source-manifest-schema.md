# Source manifest schema

Country-specific institutional URLs are not hardcoded in the Country Profiling
skill. The Agent should discover official sources through controlled
web-assisted retrieval, then pass the selected URLs or local files to the
retrieval script with `--source-manifest`.

The manifest is a JSON object with a `sources` array. A JSON array of source
objects is also accepted.

```json
{
  "country": "Exampleland",
  "iso3": "XPL",
  "focus": "immunization",
  "sources": [
    {
      "country": "Exampleland",
      "iso3": "XPL",
      "focus": "immunization",
      "title": "Exampleland Ministry of Health vaccination page",
      "publisher": "Exampleland Ministry of Health",
      "source_type": "National ministry",
      "source_class": "National Ministry of Health or equivalent",
      "url": "https://health.example/vaccination",
      "date": "Latest available",
      "evidence_role": "Official immunization ownership and implementation context",
      "retrieval_priority": "high",
      "intent": "reviewed",
      "download_pdfs": true,
      "max_downloads": 2,
      "excerpt_keywords": ["vaccination", "immunization", "schedule"]
    }
  ]
}
```

## Required fields per source

- `title`
- `publisher`
- `source_type`
- exactly one of `url` or `path`

## Optional fields per source

- `country`, `iso3`, and `focus` filter entries to the requested run.
- `source_class` maps reviewed records to unresolved source gaps.
- `date` records the source publication or page date when known.
- `evidence_role` explains why the source is being reviewed.
- `retrieval_priority` records source priority for human review.
- `intent` records whether the source is intended as reviewed evidence or a
  candidate lead.
- `download_pdfs` and `max_downloads` tell the resolver to follow likely PDF
  links from an HTML page.
- `excerpt_keywords` and `max_summary_chars` guide HTML/PDF text summaries.
- `target_type` can be `html` or `local_pdf`; it is inferred from `url` or
  `path` when omitted.

## Source-class guidance

Use country-agnostic classes so the gap registry can recognize reviewed
material across countries:

- `WHO country or regional source`
- `National Ministry of Health or equivalent`
- `National public health institute or equivalent`
- `National statistics office or official data portal`
- `Health financing, workforce, infrastructure, or service-delivery source`
- `Digital health, HIS, registry, or data-flow source`
- `National immunization schedule, guideline, circular, or recommendation source`
- `National immunization coverage or programme monitoring dataset`
- `Medicines agency, vaccine authority, or pharmacovigilance source`
- `Immunization registry, reminder, reporting, or interoperability source`

The manifest records what the Agent discovered; it does not by itself make a
source `Reviewed`. A source becomes reviewed only after the resolver opens a
usable material endpoint and extracts evidence-bearing HTML or parsed PDF text.
