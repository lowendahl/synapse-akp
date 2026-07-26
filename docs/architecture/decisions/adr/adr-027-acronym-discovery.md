# ADR-027: Compile-Time Acronym Discovery, Resolution, and Registry

| Field | Value |
|-------|-------|
| **ID** | `ADR-027` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |

## Context

Enterprise knowledge corpora are dense with acronyms. A single surface form (e.g., "CSP") can mean:
- Customer Success Plan (customer-success domain)
- Cloud Solution Provider (partner/licensing domain)
- Content Security Policy (engineering domain)

The compiler must:
1. **Discover** acronyms from the corpus without hardcoded dictionaries
2. **Resolve** each occurrence to a specific meaning using context
3. **Model ambiguity** — one surface form can have multiple meanings
4. **Govern** via human review — LLM/statistical output is never authoritative alone

### Why Not a Single Library?

Evaluated:
- `abbreviation-extractor` (Schwartz-Hearst, Rust bindings) — biomedical-tuned, noisy on enterprise markdown
- `scispaCy AbbreviationDetector` — heavy, biomedical-focused
- `acronym-expander` — requires pre-built dictionary (chicken-and-egg)

None handle: markdown structure, YAML frontmatter, ambiguity modeling, context-aware disambiguation, or governance workflows.

### Design Constraints

- **No hardcoded domain knowledge** — the framework is generic; all domain acronyms come from the corpus
- **Humans govern meaning** — the compiler discovers usage and proposes knowledge
- **High recall during discovery, high precision during promotion**
- **Reproducible** — same corpus + config + models = same output

## Decision

### Architecture: Multi-Stage Enrichment Pipeline

The acronym feature is a **compiler enrichment capability**, not a glossary generator. It operates as a pipeline within the compilation DAG:

```text
Parse OKF documents
        ↓
Detect acronym candidates (spaCy + patterns)
        ↓
Extract explicit definitions (same-sentence → same-doc → corpus)
        ↓
Normalize terms and expansions (RapidFuzz)
        ↓
Retrieve existing meanings (reviewed > authored > generated)
        ↓
Cluster unknown occurrences (sentence-transformers)
        ↓
Infer candidate meanings (LLM as constrained judge)
        ↓
Resolve occurrence meanings (scoring model)
        ↓
Calculate confidence + detect ambiguity
        ↓
Generate concepts and indexes
        ↓
Emit review queue and diagnostics
```

### Acronyms as First-Class Concepts

Each distinct acronym meaning is an individual concept with its own ID:

```yaml
type: Acronym
id: acronym.csp.customer-success-plan
term: CSP
expanded_form: Customer Success Plan
status: inferred
confidence: 0.98
domains: [customer-success]
```

The compiler must NOT collapse ambiguity into one overloaded concept.

### Confidence Gating

| Confidence | Behaviour |
|-----------:|-----------|
| 0.95–1.00 | Generate and auto-approve |
| 0.80–0.95 | Generate as inferred |
| 0.60–0.80 | Add to review queue |
| Below 0.60 | Log as unresolved |

### Precedence

```text
reviewed > authored > generated > inferred external suggestion
```

### Dependencies

**Required (already in project):**
- spaCy — tokenization, sentence segmentation, rule-based span detection
- RapidFuzz — expansion normalization, fuzzy matching
- Pydantic — strict contracts
- DuckDB — compiled storage and runtime lookup
- NumPy — vector calculations

**Recommended (optional extras):**
- sentence-transformers — contextual embedding for clustering and resolution
- scikit-learn — confidence calibration, clustering

**Abstracted:**
- LLM adapter (Protocol) — constrained disambiguation, unknown expansion inference

### Output Artifacts

1. **Acronym concepts** (markdown+frontmatter) — governed knowledge
2. **Acronym index** (JSON) — surface-form-to-meaning lookup
3. **Occurrence records** (JSONL) — per-occurrence resolution
4. **Review queue** (JSONL) — uncertain decisions for humans
5. **Diagnostics** (JSONL) — structured compiler warnings/errors
6. **DuckDB tables** — compiled runtime representation

### DuckDB Schema (compiled pack)

```sql
CREATE TABLE acronym_concept (
    concept_id VARCHAR PRIMARY KEY,
    term VARCHAR NOT NULL,
    expanded_form VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    confidence DOUBLE,
    source_layer VARCHAR NOT NULL,
    generated BOOLEAN NOT NULL
);

CREATE TABLE acronym_occurrence (
    occurrence_id VARCHAR PRIMARY KEY,
    document_id VARCHAR NOT NULL,
    section VARCHAR,
    line_number INTEGER,
    surface_form VARCHAR NOT NULL,
    context_text VARCHAR,
    resolved_concept_id VARCHAR,
    confidence DOUBLE,
    resolution_method VARCHAR
);
```

### Runtime API

The AKP runtime exposes:
- `lookup(term)` → list of meanings
- `resolve(term, context)` → best meaning for context
- `expand(term)` → preferred expansion
- `find_occurrences(term)` → corpus locations
- `list_ambiguous()` → terms with multiple meanings

## Consequences

### Positive
- Zero hardcoded domain knowledge in framework code
- Ambiguity is explicitly modeled, not collapsed
- Human governance loop prevents LLM hallucination from becoming "truth"
- Reproducible builds via versioned config + models
- Incremental learning from reviewed decisions

### Negative
- Significant implementation effort (12+ modules)
- Optional ML dependencies (sentence-transformers) for full resolution quality
- LLM adapter needed for unknown acronym inference
- Review workflow requires tooling for human reviewers

### Implementation Phases

1. **Phase 1**: Deterministic detection + explicit extraction + spaCy patterns
2. **Phase 2**: Embedding-based clustering and similarity resolution
3. **Phase 3**: LLM-assisted constrained disambiguation
4. **Phase 4**: Learned classifier from reviewed decisions

## References

- Feature specification: `docs/features/acronym-discovery-spec.md`
- ADR-002: Formal Ontology (acronyms are concepts in the ontology)
- ADR-013: Ontology Discovery (acronym discovery parallels type discovery)
- ADR-014: Pack Rules Engine (confidence thresholds are configurable rules)
