---
type: ADR
title: "ADR-005 — Shared Ontology and Cross-Pack References"
id: adr.005
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, ontology, cross-pack, namespace, linking]
---

# ADR-005 — Shared Ontology and Cross-Pack References

## Status

**Accepted** — 2026-07-25

## Context

With two packs (ADR-004), the system needs a mechanism for CSU objects to reference MCEM objects without coupling the build systems or creating circular dependencies. The SDD requires that graphs, lexical indexes, and semantic projections remain coherent across loaded packs.

Key requirements:

- CSU must reference MCEM concepts (e.g., a CSU metric "operationalizes" an MCEM stage).
- References must be validated at compile time.
- The type system must be consistent across both packs.
- Runtime graph merging must be possible without schema conflicts.

## Decision

### Shared Ontology

Both packs SHALL compile against the **same** `ontology.yaml` (ADR-002). The ontology lives in a shared location (`okf/ontology.yaml`) and is versioned independently.

### Namespace Convention

All stable IDs use a dot-separated namespace:

```
{pack-domain}.{category}.{slug}
```

- `mcem.*` IDs belong exclusively to `kp-mcem`
- `csu.*` IDs belong exclusively to `kp-csu`

No pack may define IDs in another pack's namespace.

### Cross-Pack Reference Resolution

1. When `kp-mcem` is compiled, it produces a **manifest** listing all exported object IDs.
2. When `kp-csu` is compiled, it loads the MCEM manifest as an **external ID registry**.
3. Any `mcem.*` reference in CSU source is validated against the MCEM manifest.
4. Unresolved cross-pack references fail the CSU build.

### Manifest Contract

The MCEM manifest exports (at minimum):

```yaml
pack_id: kp-mcem
pack_version: "1.0.0"
ontology_version: "1.0.0"
exported_ids:
  - mcem.framework.mcem
  - mcem.stage.inspire-design
  - mcem.stage.define-design
  - mcem.stage.deliver-realize
  - mcem.stage.expand-renew
  - mcem.role.csam
  # ... all public IDs
```

### Relationship Predicates Across Packs

Cross-pack relationships use the same ontology predicates. The relationship record stores both subject and object IDs with full namespace qualification:

```yaml
subject: csu.metric.job1-commit-to-complete
predicate: operationalizes
object: mcem.stage.deliver-realize
origin: authored
```

## Consequences

- Type safety across packs — both use the same types and predicates.
- Build-time validation of cross-pack references — no dangling refs in published packs.
- Runtime graph merge is trivial (union of nodes + edges; IDs are globally unique).
- Ontology changes require coordinated release (both packs must pass validation).
- MCEM manifest becomes a versioned contract — breaking changes (ID removal) require deprecation.

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Separate ontologies per pack | Type conflicts; graph merge ambiguity |
| Runtime-only reference resolution | Violates KP-12 (silent failures); broken refs ship |
| Embed MCEM objects inside CSU pack | Duplication; violates single-source principle |
| URL-based references | Not stable; couples to hosting; not inspectable |
