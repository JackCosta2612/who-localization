# MCP integration assessment and plan

## Recommendation

MCP integration is optional and should not be required for the core
country-profiling workflow.

The Country Profiling skill can produce useful healthcare profiles from plain
documents, public web sources, and open WHO data APIs. MCP becomes valuable
later if a workflow needs structured access to SMART/FHIR artifacts or
terminology services after the country profile has established the broader
context.

## Why MCP may be useful later

Country profiling itself is primarily public-health and health-system synthesis. Later policy comparison or localization may need to connect that context to SMART Implementation Guides, FHIR packages, terminology services, ValueSet expansion, CodeSystem lookup, or ImplementationGuide context.

Potential MCP-supported downstream tasks:

- inspect ImplementationGuide metadata;
- list available PlanDefinition, ActivityDefinition, ValueSet, CodeSystem, Questionnaire, and StructureMap resources;
- expand ValueSets relevant to a later policy-comparison task;
- look up code meanings;
- identify terminology bindings that may need country adaptation;
- flag unresolved terminology or workflow dependencies for human review.

## Proposed implementation phases

### Phase 1: No MCP dependency

- Keep the profile skill model-neutral.
- Use provided documents, WHO pages, and the GHO OData helper script.
- Store MCP requirements as documentation only.

### Phase 2: MCP discovery spike

- Evaluate candidate SMART/FHIR MCP tooling in a disposable environment.
- List available tools and resources.
- Test read-only operations against one public SMART Implementation Guide.
- Document required configuration, authentication, and data inputs.

### Phase 3: Downstream integration

- Add MCP usage notes to policy comparison or terminology mapping skills, not to the core country profile path.
- Keep all outputs traceable to artifact IDs and versions.
- Keep MCP-derived facts separate from human-authored country policy documents and public-health country profile evidence.

## Safety rules

- Use MCP read-only at first.
- Do not treat FHIR terminology matches as policy decisions.
- Record artifact version, package URL, retrieval date, and tool output.
- Keep MCP-derived facts separate from country healthcare conditions and national policy claims.
