---
type: ADR
title: "ADR-006 — MCEM Pack Compiles Independently"
id: adr.006
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, mcem, independence, compilation, dependency-direction]
---

# ADR-006 — MCEM Pack Compiles Independently

## Status

**Accepted** — 2026-07-25

## Context

The two-pack topology (ADR-004) establishes MCEM and CSU as separate compiled artifacts. A critical design choice is the **dependency direction**: which pack can reference the other?

MCEM is the methodology framework — it defines engagement stages, organizational structure, and strategic planning concepts. It is maintained by MCAPS and applies across all customer-facing units (CSU, ASE, Support, etc.).

CSU is one operational instantiation of MCEM — specific KPIs, delivery processes, programs, and measurement systems.

If MCEM were allowed to reference CSU concepts, it would:
- create a circular dependency;
- couple methodology to one unit's execution;
- break independence for other units that also implement MCEM.

## Decision

1. `kp-mcem` SHALL compile with **zero external pack dependencies**.
2. `kp-mcem` SHALL NOT contain any `csu.*` references.
3. `kp-csu` MAY reference any `mcem.*` ID (validated against MCEM manifest per ADR-005).
4. The dependency graph is strictly **acyclic**: `kp-csu` → `kp-mcem` (one direction only).

```
kp-mcem  ←──depends──  kp-csu
(independent)           (dependent)
```

5. MCEM compilation requires only:
   - the canonical MCEM source files (`okf/mcem/`)
   - the shared ontology (`okf/ontology.yaml`)
   - the compiler

6. CSU compilation requires:
   - the canonical CSU source files (`okf/csu/`)
   - the shared ontology (`okf/ontology.yaml`)
   - the published MCEM manifest (for cross-pack reference validation)
   - the compiler

## Consequences

- MCEM can be versioned, published, and distributed without waiting for CSU.
- Other units (hypothetical `kp-ase`, `kp-support`) can independently depend on `kp-mcem`.
- CSU authors see immediate build failures if they reference deprecated MCEM IDs.
- MCEM authors can rename/restructure freely as long as exported IDs remain stable.
- Build order is deterministic: compile MCEM first, then CSU.

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Bidirectional references | Circular dependency; violates clean layering |
| No dependency — both fully independent | CSU genuinely references MCEM concepts; ignoring this loses semantic richness |
| MCEM embedded inside CSU | MCEM serves multiple units; embedding couples it to one |
