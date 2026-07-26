# ADR-028: Domain-Agnostic Framework — Zero Hardcoded Domain Knowledge

| Field | Value |
|-------|-------|
| **ID** | `ADR-028` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |

## Context

During code review, we discovered that the compiler and runtime contained significant amounts of hardcoded domain knowledge:

- **37 CSU/MCEM acronyms** embedded in `enrich.py` as a `KNOWN_ACRONYMS` dictionary
- **35 type mappings** in `discover_ontology.py` as a `_CANONICAL_TYPE` dictionary (e.g., "MCEM Stage" → Stage)
- **Hardcoded strings** referencing "mcem", "csu" in parser, CLI, pipeline, and ontology discovery
- **Default pack IDs** like "kp-csu" baked into CLI and pipeline defaults
- **Domain-specific path inference** checking for "mcem" or "csu" directory names

This violates a fundamental principle: **the compiler is a generic framework that can compile ANY knowledge pack**. If we build a third knowledge pack (e.g., "partner-success"), none of this hardcoded knowledge would apply.

### Root Cause

During rapid prototyping, domain knowledge was embedded directly in code for convenience. Without explicit architectural gates, this drifted from "temporary hack" to "production code that looks authoritative."

## Decision

### Principle: The framework contains ZERO domain-specific knowledge

All domain knowledge — types, acronyms, terminology, domain names, pack identifiers — belongs exclusively in **pack-owned configuration files** that the framework reads at compile time.

### Configuration Sources (pack-author owned)

| Knowledge Type | Config Location | Example |
|---------------|----------------|---------|
| Type aliases | `ontology.yaml` → `type_aliases:` | `"MCEM Stage": "Stage"` |
| Acronyms | `pack-rules.yaml` → `acronyms:` | `"UDC": "Unified Delivery Coverage"` |
| Pack identity | CLI argument or directory name | `--pack-id kp-csu` |
| Domain names | Discovered from corpus path structure | `csu/metrics/` → domain "metrics" |
| Predicates | `ontology.yaml` → `predicates:` | `measures`, `evidenced_by` |

### Framework Behaviour (generic)

1. **Parser** — resolves types via `ontology.type_aliases` dict; falls back to `ObjectType` enum. Unknown types raise `OntologyViolation`.
2. **Enrichment** — expands acronyms from `rules.acronyms` dict. If dict is empty, no expansion occurs.
3. **Ontology discovery** — reports types, predicates, and domains as-is from the corpus. No canonicalization, no inference.
4. **CLI** — derives pack-id from source directory name; no default domain strings.
5. **Pipeline** — passes configuration objects (Ontology, PackRules) to each stage. Stages never import domain constants.

### Test Implication

Tests that exercise domain-specific behaviour (e.g., "MCEM Stage" resolution) must **supply the domain configuration explicitly**:

```python
# Correct: test supplies ontology with alias
ontology = Ontology(version="1.0", type_aliases={"MCEM Stage": "Stage"})
parser = SourceParser(ontology=ontology)

# Wrong: relies on hardcoded mapping inside framework
obj = parse_source(content, "mcem/stages/x.md")  # would fail without config
```

### Quality Gate

The design gates test suite (`test_design_gates.py`) SHALL enforce:
- No string literals matching known domain terms in `src/` (excluding test fixtures)
- No dictionaries with 5+ entries that map to `ObjectType` enum values
- No `dict[str, str]` constants with uppercase keys in stage modules

## Consequences

### Positive
- Framework works for ANY knowledge domain without code changes
- Pack authors own their terminology — no PRs needed to add types
- Tests are self-documenting (configuration is visible in each test)
- Clear boundary: code = generic logic, config = domain knowledge

### Negative
- Tests are slightly more verbose (must supply config)
- New packs require initial `ontology.yaml` with type_aliases (onboarding cost)
- Existing acronym expansion requires explicit pack-rules.yaml population
- Discovery step needed to bootstrap initial ontology from corpus

### Migration

Completed in commit `718e5ea`:
- Removed `KNOWN_ACRONYMS` (37 entries) from `enrich.py`
- Removed `_CANONICAL_TYPE` (35 entries) from `discover_ontology.py`
- Removed hardcoded "csu"/"mcem" strings from parser, CLI, pipeline
- Added `type_aliases` to Ontology dataclass
- Added `acronyms` to PackRules model
- Updated all tests to supply configuration explicitly (87 passing)
