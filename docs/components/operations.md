# Component: Operations

## Purpose
The operations component is the runtime's application-service layer. It turns loaded-pack capabilities into retrieval use cases—search, concept lookup, graph expansion, and provenance retrieval—while translating domain values into the MCP transport models exposed to clients.

## Modules Covered
- `akp_runtime.operations.__init__` — operations package marker
- `akp_runtime.operations.search` — hybrid retrieval orchestration and result shaping
- `akp_runtime.operations.lookup_concept` — identifier and alias resolution into full concept responses
- `akp_runtime.operations.expand_graph` — bounded graph expansion from a seed object
- `akp_runtime.operations.get_provenance` — object, unit, and edge provenance retrieval

## Responsibilities
- Orchestrate retrieval use cases against `LoadedPack` protocol implementations
- Apply request flags for units, neighbors, limits, and provenance targets
- Translate runtime domain values into MCP output models
- Keep runtime use-case flow free of direct SQL and file IO

## Out of Scope
- Opening or validating packs
- Defining public MCP schemas
- Implementing RRF scoring primitives
- Hosting the MCP transport loop

## Promises
- **P-OPS-001**: Search returns an empty `SearchToolOutput` when no retrieval channel yields candidates.
- **P-OPS-002**: Concept lookup falls back from exact ID lookup to exact alias lookup before returning `None`.
- **P-OPS-003**: Graph expansion forwards hop, predicate, and limit constraints to the pack graph API.
- **P-OPS-004**: Provenance retrieval accepts exactly one target kind because its request model enforces that contract.
- **P-OPS-005**: Operation outputs are shaped as typed MCP models rather than raw dictionaries.

## Invariants
- **INV-OPS-001**: Operations depend on `LoadedPack` and related protocols, not concrete infrastructure classes.
- **INV-OPS-002**: Operations do not open database connections or parse config files.
- **INV-OPS-003**: Response shaping stays in the operations layer rather than leaking into domain objects.

## Dependencies
- `akp_runtime.contracts.protocols`
- MCP request and response contracts
- Runtime domain scoring and provenance helpers

## Dependents
- `akp_runtime.consumer.mcp_server`
- `akp_runtime.pipeline.bootstrap`
