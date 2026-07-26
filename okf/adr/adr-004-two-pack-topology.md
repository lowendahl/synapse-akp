---
type: ADR
title: "ADR-004 — Two-Pack Topology (MCEM + CSU)"
id: adr.004
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, topology, modularity, packs]
---

# ADR-004 — Two-Pack Topology (MCEM + CSU)

## Status

**Accepted** — 2026-07-25

## Context

The canonical knowledge corpus contains two distinct domains:

1. **MCEM** (Microsoft Customer Engagement Methodology) — the cross-organizational methodology framework. Owned by MCAPS. Defines what engagement stages exist, what roles participate, and what principles apply.

2. **CSU** (Customer Success Unit) — the execution layer. Owned by CSU leadership. Defines how MCEM is operationalized: KPIs, delivery processes, programs, evidence paths, source systems.

These domains have different governance, different change cadence, and different audiences. CSU references MCEM extensively but MCEM knows nothing about CSU-specific execution details.

The SDD's OADR-KP-009 explicitly asks whether packs can depend on, extend, or compose with one another.

## Decision

The system SHALL produce **two independent Knowledge Packs**:

| Pack | Domain | Namespace | Content |
|------|--------|-----------|---------|
| `kp-mcem` | Methodology | `mcem.*` | Frameworks, stages, methodology, organization, roles, pipeline taxonomy, planning concepts |
| `kp-csu` | Execution | `csu.*` | Metrics, processes, programs, delivery, doctrine, evidence paths, source systems, outcomes |

Rules:

1. `kp-mcem` compiles independently with zero external dependencies.
2. `kp-csu` declares `kp-mcem` as a build dependency.
3. Cross-pack references in CSU source (e.g., `mcem.stage.inspire-design`) are validated against MCEM's published manifest at CSU compile time.
4. Both packs share the same ontology (ADR-002).
5. At runtime, a consumer may load one or both packs. Loading CSU without MCEM leaves cross-pack refs unresolved (graceful degradation, not failure).

## Consequences

- MCEM can be updated and published without recompiling CSU (if no breaking ID changes).
- CSU build fails if it references an MCEM ID that no longer exists (visible breakage per KP-12).
- Runtime planners merge both packs' graph/lexical/vector projections using the shared namespace.
- Future domain packs (e.g., `kp-ase`, `kp-country-XX`) follow the same pattern.
- Pack version pinning prevents accidental breaking changes from propagating.

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Single monolithic pack | Violates separation of concerns; different governance/cadence |
| Many micro-packs (one per subfolder) | Over-fragmented; cross-references become unmanageable |
| Flat namespace, single pack with domain tags | Doesn't model the dependency direction; MCEM→CSU coupling risk |
