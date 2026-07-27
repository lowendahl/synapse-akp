# ADR-014: Pack Rules Engine & Outcome Validator

| Field | Value |
|-------|-------|
| **ID** | `adr-014` |
| **Status** | Accepted |
| **Date** | 2026-07-25 |
| **Decision Makers** | Patrik Lowendahl |

## Context

The V2 compiler produces high-quality Knowledge Packs, but two classes of quality issues slip through:

1. **Alias pollution** — The enrichment stage generates aliases from acronym expansion and body text extraction. Short, generic tokens like `"this"`, `"csu"`, `"risk"` become aliases on dozens of objects, degrading BM25 precision. A query for `"C2C"` returns irrelevant delivery engine documents because alias context bleeds into the lexical index.

2. **No outcome verification** — The compiler validates *structure* (ontology conformance, required fields) but never validates *retrieval quality*. A structurally valid pack can still produce terrible search results. There is no way to catch this without manually testing queries.

Both problems share a root cause: **the compiler has no declarative rules system**. Quality constraints are hardcoded in Python, requiring code changes to add new rules. Pack authors cannot configure precision thresholds without modifying the compiler.

### Design Constraints

- **No LLM dependency** — All rules must be deterministic and reproducible. No inference calls, no API keys, no model downloads for rule evaluation.
- **Pack-author accessible** — Non-technical users must be able to add and modify rules via YAML, not Python.
- **CI-compatible** — Rules must produce machine-readable pass/fail results for automated pipelines.

## Decision

### 1. Pack Rules File (`pack-rules.yaml`)

A declarative YAML file that ships alongside `ontology.yaml`. The compiler loads it at startup and applies rules at two points: **enrichment time** (preventive) and **post-compilation** (outcome validation).

```yaml
version: "1.0"

alias_rules:
  stopwords: [this, the, a, an, it, is, are, was, that, with, for, from, into, also]
  min_length: 2
  max_tag_fanout: 15
  max_explicit_fanout: 8
  blocked_patterns: ["^\\d+$", "^[a-z]$"]

outcome_assertions:
  - name: explicit-alias-precision
    rule: alias_owner_in_top_k
    params: { k: 3, sample: 20 }

  - name: tag-fanout-limit
    rule: max_tag_coverage
    params: { threshold: 0.3 }

  - name: bm25-self-retrieval
    rule: title_self_retrieval
    params: { k: 5, sample: 30 }

quality_thresholds:
  min_assertion_pass_rate: 0.8
  fail_on_error: true
```

### 2. Alias Quality Gate (Compile-Time)

Injected into the enrichment stage. Before any alias is emitted, the gate checks:

| Check | Behavior |
|-------|----------|
| Alias in stopwords list | **Reject** alias, emit WARNING diagnostic |
| Alias length < `min_length` | **Reject** alias |
| Alias matches `blocked_patterns` | **Reject** alias |
| Tag alias already on >`max_tag_fanout` objects | **Reject** alias, emit WARNING |
| Explicit alias on >`max_explicit_fanout` objects | Emit WARNING (may indicate legitimate shared concept) |

### 3. Outcome Validator (Post-Compilation Stage 13)

After the pack is written but before the build reports success, the validator:

1. Opens the compiled DuckDB pack (read-only)
2. Runs each outcome assertion from `pack-rules.yaml`
3. Emits a pass/fail report per assertion
4. If `fail_on_error: true` and pass rate < threshold, the build FAILS

#### Built-in Assertion Functions

| Function | What it checks |
|----------|---------------|
| `alias_owner_in_top_k` | For N sampled explicit aliases, searching the alias returns its owning object in the top-K results |
| `max_tag_coverage` | No single tag alias covers more than X% of all objects |
| `title_self_retrieval` | Searching an object's title via BM25 returns that object in top-K |

New assertion functions can be registered by adding a Python function with a standard signature — but the *rules themselves* are always YAML.

### 4. Pipeline Integration

```
Discover → [Ontology Discovery] → Load Ontology → Load Rules
→ Parse → Validate → Enrich (with alias gate) → Graph
→ Semantic Units → Aliases → BM25 → Embed → Cross-Pack
→ Write Pack → Outcome Validate → Report
```

Rules are loaded once in the orchestrator and passed as a dependency to:
- `enrich_corpus(objects, rules)` — alias quality gate
- `validate_outcomes(pack_path, rules)` — post-compilation assertions

## Consequences

### Positive
- Pack authors can tune quality thresholds without code changes
- The `"this"` alias bug and similar issues are prevented structurally
- Outcome assertions catch retrieval regressions before deployment
- CI pipelines get deterministic pass/fail signals
- New rule types (e.g., coverage minimums) can be added via one Python function + YAML config

### Negative
- Outcome validation adds ~2-5 seconds to compile time (BM25 rebuilds for assertion checks)
- Rules file is another artifact to maintain alongside ontology.yaml
- Assertion sampling means some edge cases may not be caught on every build

### Mitigations
- Outcome validation is always-on but `fail_on_error` is configurable
- Default `pack-rules.yaml` ships with sensible defaults; pack authors only override what they need
- Sampling size is configurable per assertion
