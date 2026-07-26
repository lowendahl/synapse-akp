# ADR-032: Assertion-Level Confidence and Governance

| Field | Value |
|-------|-------|
| **ID** | `ADR-032` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-018 (unified pipeline), ADR-023 (source layers) |

## Context

Traditional NER and concept extraction systems assign a single confidence score to each entity. This conflates distinct claims:

- "ACR exists as a concept" (high confidence — mentioned 47 times)
- "ACR is a KPI" (medium confidence — called a "metric" in one document)
- "ACR target is 85%" (low confidence — mentioned once in a draft)
- "ACR formula = X/Y" (medium confidence — two conflicting definitions exist)

Collapsing these into one score forces binary decisions: either the entity is "confident enough" and all its properties are treated as true, or it is rejected entirely. This produces:

1. **Over-commitment** — a well-evidenced concept gets a formula assertion promoted without evidence.
2. **Under-commitment** — a concept with one uncertain property is suppressed entirely.
3. **Ungovernable review** — reviewers see entity-level "approve/reject" but cannot correct individual claims.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Entity-level confidence** | Simple; familiar from NER | Conflates distinct claims; unactionable review |
| **B. Property-level confidence** | More granular | Still collapses sources; no independent governance |
| **C. Assertion-level confidence (chosen)** | Each claim independently scored, sourced, governed | More complex data model; more review items |

## Decision

Every fact the compiler extracts is modelled as an **independent assertion** with its own:

- **Confidence score** (0.0–1.0)
- **Status** (`authored` | `reviewed` | `inferred` | `unresolved` | `rejected`)
- **Source location** (document, section, line range)
- **Evidence span** (the text that supports the claim)
- **Method** (how it was extracted: pattern, LLM, rule, embedding, human)

### Assertion Model

```python
class SemanticAssertion(BaseModel):
    assertion_id: str
    subject_id: str          # The entity this assertion is about
    predicate: str           # What is being claimed (e.g., "has_formula", "is_kpi", "has_target")
    object_id: str | None    # Another entity (for relationships)
    literal_value: ...       # A scalar value (for properties)
    confidence: float        # Independent confidence for THIS claim
    status: Literal["authored", "reviewed", "inferred", "unresolved", "rejected"]
    source: SourceLocation
    evidence_span: str
    method: str
```

### Confidence Gating Rules

| Confidence | Action |
|------------|--------|
| ≥ 0.85 | Auto-accept into compiled output |
| 0.50–0.84 | Accept but flag for review |
| < 0.50 | Route to review queue; do not include in compiled output |

Thresholds are configurable per predicate type in `semantic-config.yaml`.

### Governance Model

- **Reviewed assertions override inferred assertions** — a human correction always wins.
- **Conflicting assertions co-exist** — both are stored with their respective confidence; the review queue surfaces the conflict.
- **Rejected assertions are preserved** — they remain in the database with `status: rejected` to prevent re-inference.
- **Each assertion is independently reviewable** — a reviewer can approve "ACR exists" while rejecting "ACR target is 85%".

## Consequences

- The DuckDB schema has a `semantic_assertion` table as a first-class citizen (ADR-025).
- The review queue operates at assertion granularity, not entity granularity.
- Diagnostics reference specific assertions (e.g., "SEM019: generated assertion conflicts with reviewed assertion").
- Runtime queries can filter by confidence threshold, letting consumers choose their own precision/recall tradeoff.
- Storage is larger (many assertions per entity), but DuckDB handles this efficiently with columnar compression.
