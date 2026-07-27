# ADR-039: Concept-Centric Resolution and Multi-Faceted Explanation

| Field | Value |
|-------|-------|
| **ID** | `ADR-039` |
| **Status** | Proposed |
| **Date** | 2026-07-27 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-038 (Explain Operation), ADR-021 (Hybrid Retrieval), ADR-013 (Ontology Discovery) |

## Context

When a user queries "Job1", they expect the system to resolve to the *concept* — what Job 1 is, how it's measured, and how to observe it. In the knowledge pack, this concept spans multiple objects:

- A **Process** ("Commit-to-Complete") — what it IS
- A **KPI** ("Job 1 — Commit to Complete (C2C)") — how it's MEASURED
- An **Evidence Map** ("Job 1 C2C Evidence") — how to LOOK AT it

These objects are connected by typed predicates (`measures`, `evidenced_by`, `references`) that encode their structural roles. The ontology already defines these roles through predicate constraints (e.g., `measures` can only flow from KPI/Metric → Process/Outcome; `evidenced_by` can only point → Evidence_Source/Evidence_Map).

Today, when an alias matches multiple objects, the runtime returns them in arbitrary database order and the explain operation picks the first one. This produces two failures:

1. **Wrong resolution** — an Evidence Map is returned when the user means the KPI or Process
2. **Incomplete explanation** — only one object's semantic units are shown, missing the other facets of the same concept

The principle issue: the runtime treats all objects as equally important peers, ignoring the structural roles encoded in the ontology's type system and predicate constraints.

### Constraints

- **Ontology-first** (ADR-013) — the ontology SHALL remain the single source of truth for type semantics
- **Read-only** (ADR-019) — resolution logic SHALL NOT mutate pack data
- **Evidence-grounded** (ADR-038) — explanation SHALL trace to cited semantic units
- **Model-neutral** — resolution strategy SHALL NOT depend on LLM availability

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Hard-coded type priority list** | Simple, fast | Brittle, not ontology-driven, breaks on new types |
| **B. Ontology-declared type roles** | Declarative, extensible | Requires ontology schema change |
| **C. Structural inference from predicates (chosen)** | Zero ontology changes, uses existing relationship semantics | Slightly more complex resolution logic |
| **D. Cluster-based resolution** | Most complete | Over-engineered for current scale |

## Decision

### 1. The ontology's predicate constraints SHALL define structural type roles

Object types are classified into structural roles based on how predicates reference them:

- **Primary types** — types that appear as `subject_types` in directional predicates like `measures`, `operationalizes`, `depends_on`. These are *actors* that do things.
- **Supporting types** — types that appear only as `object_types` in predicates like `evidenced_by` (i.e., Evidence_Map, Evidence_Source). These *serve* primary types.

This classification is derived, not declared — the runtime SHALL infer it from the ontology's predicate constraint definitions at pack load time.

### 2. Alias resolution SHALL prefer primary types over supporting types

When an alias matches multiple objects, the runtime SHALL rank results so that primary-role objects appear before supporting-role objects. Within the same role tier, ordering SHALL prefer:
1. Objects where the alias appears in the title (exact title match)
2. Objects with more inbound relationship edges (higher graph centrality)

### 3. The explain operation SHALL compose across concept facets

When explaining a concept, the operation SHALL follow first-hop relationships to gather context from structurally related objects:

- If the resolved object has `evidenced_by` edges → include evidence context
- If the resolved object has `measures`/`operationalizes` edges → include the target concept's definition
- If the resolved object is measured by other objects → include their metrics

The explanation SHALL clearly attribute each section to its source object, maintaining provenance.

### 4. Facet composition SHALL be bounded and deterministic

The operation SHALL follow at most one hop for facet composition. It SHALL NOT recursively expand the graph. The predicates followed for composition SHALL be limited to structural predicates: `measures`/`measured_by`, `evidenced_by`/`provides_evidence_for`, `operationalizes`/`operationalized_by`.

### 5. The ontology MAY declare explicit type roles in a future version

If structural inference proves insufficient, the ontology schema MAY be extended with an explicit `role: primary | supporting | meta` field on object type definitions. This ADR does not require that change — inference from predicates is sufficient for the current type system.

## Consequences

### Positive
- "Job1" resolves to the KPI (primary type) instead of the Evidence Map (supporting type)
- Explanations are multi-faceted: what it is + how it's measured + how to look at it
- No ontology schema changes required — uses existing predicate constraints
- Works for all concepts that follow the same structural pattern (UDC, Job2, etc.)
- Deterministic — same query always resolves the same way

### Negative
- Resolution logic is more complex (mitigated: bounded to one-hop traversal)
- Type role inference adds startup cost at pack load (mitigated: cached once)
- If ontology predicates lack constraints, role inference degrades to alphabetical (mitigated: ontology already has good constraint coverage)
