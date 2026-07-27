# Component: Explain Concept

## Purpose

The Explain Concept component synthesizes human-readable prose explanations
from structured pack content. It bridges the gap between machine-optimized
knowledge packs and human understanding by retrieving a concept's semantic
units and relationships, then composing them into a coherent narrative —
either through LLM synthesis or structured fallback assembly.

## Responsibilities

- Resolve a natural-language query or concept identifier to a pack concept,
  preferring concept-role types over measurement or evidence types (ADR-039)
- When the resolved concept has related measurement and evidence objects,
  compose across them to build a multi-faceted explanation
- Structure the explanation like a professional report: lead with the concept
  (what it IS), then measurements (how it's tracked), then evidence (how to
  observe it)
- Retrieve the concept's semantic units and graph neighbors for context
- Delegate prose synthesis to a reasoning client when available
- Assemble a structured Markdown fallback when no reasoning client is present
  or when the client declines
- Filter semantic units by detail level to control explanation depth
- Return explanation output that distinguishes synthesis method and cites
  source unit identifiers

## Out of Scope

- Providing the LLM or reasoning client implementation (that is a separate
  infrastructure adapter behind a protocol)
- Caching explanations (a cross-cutting concern for a future component)
- Defining MCP transport schemas (that is the MCP server component's concern)
- Mutating pack state in any way
- Performing search ranking or scoring (the Search component owns that)
- Embedding or vector similarity (the retrieval pipeline owns that)

## Promises

- **P-EXP-001**: Given a valid concept identifier, the operation returns an
  explanation containing the concept's title and at least one cited semantic
  unit identifier.
- **P-EXP-002**: When no reasoning client is available, the operation produces
  a structured Markdown fallback organized by semantic unit headings.
- **P-EXP-003**: When a reasoning client is available and succeeds, the
  operation returns LLM-synthesized prose and reports the synthesis method
  as such.
- **P-EXP-004**: When a reasoning client raises an error or declines, the
  operation falls back to structured assembly and includes a diagnostic
  reason in the output indicating why synthesis was unavailable (e.g.
  "no reasoning client configured", "reasoning client declined",
  "reasoning client error: [message]").
- **P-EXP-005**: The `brief` detail level includes only definition and
  summary units. The `standard` level adds formulas, thresholds, and key
  relationships. The `detailed` level includes all available units.
- **P-EXP-006**: The output always includes a `synthesis_method` field
  indicating whether the explanation was produced by LLM synthesis or
  structured fallback.
- **P-EXP-007**: When the query does not resolve to any concept, the
  operation returns `None` rather than an empty or fabricated explanation.
- **P-EXP-008**: Related concepts from graph neighbors are included as
  context in the explanation, referenced by title rather than raw object
  identifiers.
- **P-EXP-009**: When an alias matches multiple objects, the operation
  resolves to the one with the highest-priority resolution role as declared
  in the ontology (concept > measurement > evidence > neutral).
- **P-EXP-010**: When the resolved concept has `measured_by` or
  `evidenced_by` relationships, the explanation includes their semantic
  units as additional facets, clearly attributed and ordered: concept first,
  then measurements, then evidence.
- **P-EXP-011**: The multi-faceted composition follows at most one hop from
  the resolved concept. It does not recursively expand the graph.

## Invariants

- **INV-EXP-001**: The operation never mutates pack state — all pack
  interactions are read-only queries.
- **INV-EXP-002**: The operation depends on protocols (LoadedPack,
  SemanticReasoningClient), never on concrete infrastructure classes.
- **INV-EXP-003**: Every claim in the explanation traces to a cited semantic
  unit identifier — no unsourced assertions.
- **INV-EXP-004**: The structured fallback produces valid Markdown regardless
  of which semantic units are present or absent.

## Collaborators

- **LoadedPack** (depends on) — provides concept lookup, semantic unit
  retrieval, and graph neighbor traversal
- **SemanticReasoningClient** (depends on, optional) — provides LLM-backed
  prose synthesis when available
- **Operations** (peer within) — follows the same patterns as concept lookup,
  search, and graph expansion operations
- **MCP Server** (depended on by) — exposes this operation as the
  `explain_concept` tool to MCP clients
- **Contracts** (depends on) — uses protocol definitions and shared
  request/response models

## Architectural Constraints

- **ADR-038**: Defines the explain operation, detail levels, fallback
  strategy, and output contract
- **ADR-039**: Defines concept-centric resolution (ontology-declared roles)
  and multi-faceted composition (concept → measurement → evidence order)
- **ADR-036**: SemanticReasoningClient protocol — synthesis delegates through
  this protocol
- **ADR-029**: LLM integration is protocol-based, provider-neutral
- **ADR-019**: Runtime never mutates packs — explain is strictly read-only
- **ADR-016**: Model-neutral design — no hardcoded LLM provider references
- **ADR-021**: Retrieval follows the hybrid pattern for concept resolution
