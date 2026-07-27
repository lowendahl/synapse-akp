# ADR-030: Unified Semantic Compilation Pipeline

| Field | Value |
|-------|-------|
| **ID** | `ADR-030` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Supersedes** | Partially supersedes ADR-015 (acronyms become one extraction method within this pipeline) |

## Context

The compiler currently treats different extraction tasks as isolated subpackages (e.g., `acronym/` for acronym discovery, ontology discovery as a separate step). As scope expands to include domain concepts, measures, indicators, KPIs, formulas, objectives, targets, and dimensions, this isolated-extractor pattern creates:

1. **Redundant parsing** — each extractor re-parses the same source documents.
2. **Inconsistent provenance** — each extractor tracks source locations differently.
3. **No cross-entity reasoning** — a measure cannot reference a concept discovered by a separate extractor.
4. **Duplicate normalization** — fuzzy matching and entity resolution logic is reimplemented per extractor.
5. **Combinatorial integration cost** — N extractors require N² coordination paths.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Keep isolated extractors** | Simple to add one-off features | Exponential integration cost; no shared context |
| **B. Plugin architecture with shared bus** | Extensible | Over-engineered for compile-time; runtime coupling |
| **C. Unified sequential pipeline (chosen)** | Single parse, shared context, explicit stage boundaries | Larger initial design surface |

## Decision

Implement a **single unified semantic compilation pipeline** with the following stage sequence:

```
Parse → Candidate Extraction → Context Assembly → Classification →
Definition Extraction → Measure/Formula Extraction → Indicator Classification →
Relationship Extraction → Entity Resolution → Confidence Gating → Generation → Review
```

### Key principles:

1. **One parse, many extractions** — source documents are parsed exactly once into a shared AST/token stream.
2. **Shared candidate pool** — all extraction methods (acronyms, terminology, patterns, LLM) contribute to a single candidate set.
3. **Progressive enrichment** — each stage adds information; no stage removes or overwrites prior evidence.
4. **Stage contracts** — Pydantic models define the exact input/output boundary of each stage.
5. **Pluggable extraction methods** — new detection heuristics are added as methods within existing stages, not new pipelines.

### Where acronyms fit:

- Acronym pattern matching becomes one detection method within the Candidate Extraction stage.
- Acronym resolution becomes one resolution strategy within the Entity Resolution stage.
- The `AcronymReasoningClient` protocol is widened into `SemanticReasoningClient` (ADR-024).
- Existing acronym contracts (`AcronymCandidate`, `AcronymConcept`) map into the broader `SemanticCandidate` and `DomainConcept` models.

## Consequences

- The `compiler/acronym/` subpackage will be refactored into `compiler/semantic/` with acronym logic as extraction methods.
- All future extraction features (measures, KPIs, relationships) plug into this single pipeline.
- A single DuckDB schema holds all semantic artifacts (ADR-025).
- Testing becomes integration-first: test the full pipeline with fixture corpora, not just individual extractors.

## Implementation

Subpackage: `compiler/src/kp_compiler/semantic/`

```
semantic/
├── __init__.py
├── pipeline.py            # Orchestrator
├── stages/
│   ├── parse.py           # Source document parsing
│   ├── candidate.py       # Candidate extraction (includes acronym patterns)
│   ├── context.py         # Context window assembly
│   ├── classify.py        # Entity type classification
│   ├── define.py          # Definition extraction
│   ├── measure.py         # Measure and formula extraction
│   ├── indicator.py       # Indicator/KPI classification
│   ├── relationship.py    # Relationship extraction
│   ├── resolve.py         # Entity resolution and merge
│   ├── confidence.py      # Confidence gating
│   ├── generate.py        # Artifact generation
│   └── review.py          # Review queue generation
├── contracts/             # Pydantic stage boundary models
├── adapters/              # LLM and embedding adapters
├── config/                # Taxonomy, rules, registries
└── queries/               # DuckDB writers
```
