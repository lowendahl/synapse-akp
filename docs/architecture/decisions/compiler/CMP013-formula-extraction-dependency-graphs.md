# ADR-034: Formula Extraction and Dependency Graphs

| Field | Value |
|-------|-------|
| **ID** | `ADR-034` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-018 (unified pipeline), ADR-020 (assertion confidence), ADR-021 (promotion chain) |

## Context

Business corpora contain formula definitions in varied formats:

- Prose: "Delivery Coverage is booked hours divided by required hours"
- Semi-formal: "ACR = Consumed / Committed × 100"
- Tabular: a row in a metrics table with "Formula" column
- Implicit: "calculated as the ratio of X to Y"

Formulas are **assertions about measures** (ADR-020), not intrinsic properties. The compiler may confidently know a measure exists while being uncertain about its exact formula.

### Challenges

1. **Ambiguous formulas** — "Revenue Growth" could be absolute or percentage; period-over-period or cumulative.
2. **Conflicting formulas** — two documents define the same measure differently.
3. **Circular dependencies** — Measure A depends on B which depends on A.
4. **Unit inconsistency** — a formula divides dollars by headcount but claims a percentage result.
5. **Descriptive vs. executable** — "weighted average of customer scores" is meaningful but not directly computable without knowing the weight function.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Store formulas as plain text** | Simple | No validation, no dependency tracking |
| **B. Regex-based extraction into structured fields** | Deterministic | Brittle; misses prose formulas |
| **C. SymPy-backed extraction with dependency graph (chosen)** | Parseable, validatable, cycle-detectable | Requires SymPy dependency; LLM assist for prose formulas |

## Decision

Formula extraction uses a **three-layer approach**:

### Layer 1: Surface Extraction

- Regex patterns detect explicit formula syntax (`X = Y / Z`).
- `quantulum3` extracts numeric quantities and units.
- `textacy` extracts semi-structured triples.
- LLM adapter extracts formulas from prose descriptions.

### Layer 2: Symbolic Normalization (SymPy)

- Extracted formulas are parsed into SymPy expressions.
- Variables are resolved to measure IDs where possible.
- Unresolved symbols are flagged as diagnostic SEM008.
- Aggregation type is inferred (sum, ratio, average, weighted_average, count, etc.).

### Layer 3: Dependency Graph (NetworkX)

- Each formula creates edges: `derived_measure → input_measure`.
- Cycle detection runs after all formulas are extracted (SEM009).
- Grain consistency is validated: formulas mixing different granularities produce SEM010.
- Unit consistency: `Pint` validates dimensional analysis (SEM018).

### Formula as Assertion

A formula is stored as a `SemanticAssertion` with:
- `predicate: "has_formula"`
- `literal_value`: the canonical SymPy expression string
- Independent confidence score
- Evidence span from the source text

This means:
- A measure can have 0 formulas (existence known, formula unknown).
- A measure can have >1 formula assertions (conflicting definitions — surfaces SEM002).
- A reviewed formula overrides a generated one.

### Dependency Schema

```python
class FormulaDefinition(BaseModel):
    source_text: str                    # Original text
    canonical_expression: str | None    # SymPy-normalized form
    aggregation: str | None             # sum, ratio, average, etc.
    input_measure_ids: list[str]        # Dependency edges
    confidence: float
```

### Diagnostics

| Code | Condition |
|------|-----------|
| SEM007 | Formula text cannot be parsed into SymPy expression |
| SEM008 | Formula contains symbols that don't resolve to known measures |
| SEM009 | Measure dependency cycle detected |
| SEM010 | Formula grain inconsistency (mixing daily/monthly inputs) |
| SEM011 | Formula aggregation is ambiguous |
| SEM018 | Unit dimensionally inconsistent with formula |
| SEM024 | Formula is descriptive but not executable |

## Consequences

- `sympy>=1.13` is added as an optional dependency under `[formula]` extras.
- `pint>=0.24` and `quantulum3>=0.9` are added for unit/quantity extraction.
- `networkx>=3.3` (already a dependency) handles the dependency graph.
- Formulas that cannot be parsed are still stored as text assertions with lower confidence.
- The runtime can return both the human-readable and symbolic forms of a formula.
- Cycle detection prevents infinite loops in downstream measure computation.
