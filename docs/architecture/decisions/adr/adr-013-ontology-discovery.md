# ADR-013: Ontology Discovery Mode

| Field | Value |
|-------|-------|
| **ID** | `adr-013` |
| **Status** | Accepted |
| **Date** | 2026-07-25 |
| **Decision Makers** | Patrik Lowendahl |

## Context

The current compiler requires a hand-maintained `ontology.yaml` that defines all allowed object types, predicates, and constraints. This creates two problems:

1. **Drift risk** — the corpus evolves faster than the ontology; new types appear in frontmatter but are absent from ontology.yaml, causing spurious validation warnings.
2. **Bootstrap friction** — when starting a new knowledge domain, you must author the ontology *before* you can compile, even though the corpus already contains the structural truth.

The OKF markdown corpus is the canonical source of truth. Every `type:` field, every `relationships[].predicate`, and every domain prefix already exists in the frontmatter. The ontology should be *derived* from this data, then *frozen* as a governance gate.

## Decision

The compiler operates in two modes:

### Mode 1: Discover (`--discover-ontology`)

When no `ontology.yaml` exists or `--discover-ontology` is passed:

1. **Scan** — walk all source files, extract `type:` from frontmatter
2. **Collect predicates** — walk all `relationships[].predicate` values
3. **Infer domain constraints** — which types appear in which domain prefixes
4. **Infer predicate constraints** — which subject/object types co-occur with each predicate
5. **Emit** — write a draft `ontology.yaml` with `auto_generated: true` marker
6. **Continue** — use the discovered ontology for the current compilation

The generated ontology includes:
- All observed object types with `required_fields: [id, title, description]` defaults
- All observed predicates with inferred `subject_types` / `object_types` constraints
- All observed domain bindings
- `id_format` pattern inferred from observed ID prefixes
- `auto_generated: true` + `generated_at` timestamp

### Mode 2: Validate (default)

When `ontology.yaml` exists and `--discover-ontology` is NOT passed:
- Current behavior — load and validate against it
- Unknown types/predicates found in corpus emit warnings

### Lifecycle

```
New corpus → kp compile --discover-ontology → ontology.yaml (draft)
                          ↓
                   Human review + remove auto_generated flag
                          ↓
Corpus evolves → kp compile → validates against frozen ontology
                          ↓
           Need new types? → kp compile --discover-ontology → regenerate
```

### Merge strategy for rediscovery

When `--discover-ontology` is passed but `ontology.yaml` already exists:
- Merge: keep existing descriptions, constraints, and hand-written metadata
- Add: new types/predicates found in corpus but missing from ontology
- Flag: types in ontology but absent from corpus (orphaned)
- Never delete: human-authored constraints are preserved

## Consequences

- **Positive**: Zero-friction bootstrap for new domains; ontology stays in sync with corpus
- **Positive**: Merge strategy preserves hand-written governance metadata
- **Positive**: `auto_generated` flag makes governance audit trail explicit
- **Negative**: Discovered constraints are heuristic (based on co-occurrence), not authoritative
- **Mitigation**: Human review step before removing `auto_generated` flag
