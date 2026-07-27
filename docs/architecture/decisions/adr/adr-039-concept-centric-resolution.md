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
| **A. Hard-coded type priority list** | Simple, fast | Brittle, not ontology-driven, breaks on new domains |
| **B. Infer roles from predicate constraints** | No ontology change | Inference may be wrong for new domains; not corpus-author intent |
| **C. Ontology-declared resolution roles (chosen)** | Explicit, corpus-agnostic, author declares intent | Requires one field added to ontology type definitions |
| **D. Cluster-based resolution** | Most complete | Over-engineered for current scale |

## Decision

### 1. The ontology SHALL declare resolution roles for object types

Each object type definition in the ontology SHALL include a `resolution_role` field that classifies it for disambiguation:

- **`concept`** — the primary thing being discussed. This is what a user means when they use a shared alias without qualification. In CSU: Process, Outcome. In a competitive analysis corpus: Claim. In a sovereign playbook: Regulation.
- **`measurement`** — things that quantify or track concepts. In CSU: KPI, Metric.
- **`evidence`** — things that observe or provide data about concepts. In CSU: Evidence_Map, Evidence_Source.
- **`neutral`** (default) — no special resolution priority.

Resolution priority order: concept > measurement > evidence > neutral.

This is corpus-declarative: each ontology decides which types are its "concepts" based on its domain semantics. The runtime applies the same resolution algorithm regardless of domain.

### 2. Alias resolution SHALL prefer concept-role types

When an alias matches multiple objects, the runtime SHALL rank results by their type's resolution_role. Within the same role tier, ordering SHALL prefer:
1. Objects where the alias matches the title most closely
2. Objects with more inbound relationship edges (higher graph centrality)

### 3. The explain operation SHALL compose across concept facets

When explaining a concept, the operation SHALL follow first-hop relationships to gather context from structurally related objects:

- If the resolved object has `evidenced_by` edges → include evidence context
- If the resolved object has `measures`/`operationalizes` edges → include the target concept's definition
- If the resolved object is measured by other objects → include their metrics

The explanation SHALL clearly attribute each section to its source object, maintaining provenance.

### 4. Facet composition SHALL be bounded and deterministic

The operation SHALL follow at most one hop for facet composition. It SHALL NOT recursively expand the graph. The predicates followed for composition SHALL be limited to structural predicates: `measures`/`measured_by`, `evidenced_by`/`provides_evidence_for`, `operationalizes`/`operationalized_by`.

### 5. Types without an explicit resolution_role SHALL default to neutral

When an ontology does not declare `resolution_role` for a type, the runtime SHALL treat it as `neutral`. This ensures backward compatibility — existing ontologies work without modification, they just lack disambiguation until roles are declared.

## Consequences

### Positive
- "Job1" resolves to the Process (what it IS), not the Evidence Map or KPI
- Explanations are multi-faceted: what it is + how it's measured + how to look at it
- Corpus-agnostic — each ontology declares its own concept types (Claim, Regulation, Process — whatever fits the domain)
- Works for all concepts that follow the same structural pattern (UDC, Job2, etc.)
- Deterministic — same query always resolves the same way
- Backward compatible — missing roles default to neutral

### Negative
- Requires one field added to ontology type definitions (mitigated: small, one-time change per ontology)
- Resolution logic is more complex (mitigated: bounded to one-hop traversal)
- Type role metadata adds a small cost at pack load (mitigated: cached once, tiny compared to BM25 indexing)
