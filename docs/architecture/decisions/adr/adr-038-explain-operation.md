# ADR-038: Explain Operation — Human-Readable Concept Explanation via LLM Synthesis

| Field | Value |
|-------|-------|
| **ID** | `ADR-038` |
| **Status** | Proposed |
| **Date** | 2026-07-27 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-016 (model-neutral), ADR-018 (provenance survives compilation), ADR-019 (no runtime mutation), ADR-021 (hybrid retrieval), ADR-026 (MCP stdio transport), ADR-029 (LLM protocol), ADR-036 (SemanticReasoningClient) |

## Context

Knowledge packs store structured, machine-optimized data: semantic units, graph edges, aliases, provenance chains. Agentic consumers can navigate this structure programmatically. Human consumers cannot — they need coherent prose that synthesizes a concept's definition, thresholds, formulas, and relationships into a narrative that reads like an expert wrote it.

A human asking "what is UDC?" expects an answer that:
- Weaves definition, formula, thresholds, and business rules into a single narrative
- References related concepts naturally, not as raw object IDs
- Cites evidence sources without exposing pack internals
- Adapts depth to the audience's need (brief overview vs. detailed analysis)

This creates a need for an **explain** capability — a read-only operation that retrieves pack content and synthesizes it into human-readable prose.

### Constraints

- **Model-neutral** (ADR-016) — synthesis SHALL work through a protocol, not a hardcoded LLM provider
- **Evidence-grounded** — every claim in the explanation SHALL trace to a semantic unit in the pack
- **Read-only** (ADR-019) — the explain operation SHALL NOT mutate the pack
- **Graceful degradation** — the operation SHALL produce useful output even when no LLM is available
- **Relaxed determinism** — unlike compilation (which must be deterministic), explanation is inherently generative; identical inputs MAY produce varying prose

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Client-side synthesis** — return units, let the calling agent synthesize | No runtime LLM dependency | Inconsistent quality across callers; no provenance control; hallucination risk |
| **B. Runtime LLM synthesis** — dedicated operation delegates to `SemanticReasoningClient` | Consistent quality; provenance-grounded; cacheable | Requires LLM availability; adds latency |
| **C. Compile-time explanation** — generate prose during compilation, store in pack | Fast at query time; no LLM needed | Combinatorial explosion of possible queries; stale on corpus change |
| **D. Hybrid (chosen)** — runtime synthesis with structured fallback | Best of B + graceful degradation of A | Slightly more complex operation |

## Decision

### 1. The runtime SHALL expose an `explain_concept` operation

This operation accepts a natural-language query or concept identifier and returns a human-readable prose explanation grounded in pack content.

The operation SHALL resolve a query to a concept, retrieve its semantic units and graph neighbors, synthesize a human-readable explanation, and return it with cited unit IDs and provenance.

### 2. Synthesis SHALL use the `SemanticReasoningClient` protocol

The `SemanticReasoningClient` (ADR-036) SHALL be extended with a method for explanation synthesis. The method SHALL accept concept metadata, semantic units, and neighbor context, and return prose with cited unit IDs and a confidence score.

Any provider implementing `SemanticReasoningClient` MAY implement this method. Providers that do not SHALL raise `NotImplementedError`, triggering the structured fallback.

### 3. The operation SHALL degrade gracefully without an LLM

When no `SemanticReasoningClient` is available (or when it raises `NotImplementedError`), the operation SHALL produce a **structured fallback** — a Markdown document assembled directly from the pack's semantic units, organized by heading with related concepts appended. This fallback is readable, evidence-complete, and requires no external service.

### 4. The output contract SHALL distinguish synthesis method

The output SHALL include a field indicating whether the explanation was LLM-synthesized or assembled from raw units, enabling downstream quality decisions. The input SHALL accept a query, optional pack filter, and a detail level.

### 5. Detail levels control depth, not accuracy

| Level | Guidance |
|-------|----------|
| `brief` | 2–3 sentence summary: what it is, why it matters |
| `standard` | Full explanation covering definition, formula/logic, thresholds, and key relationships |
| `detailed` | Standard + business rules, limitations, source systems, leading/lagging context |

All levels cite the same evidence; detail level controls which semantic units are included, not whether claims are grounded.

## Consequences

### Positive
- Human consumers get coherent, evidence-grounded explanations without needing to understand pack structure
- Model-neutral — any LLM provider works through the existing protocol pattern
- Graceful degradation — useful output is always available, LLM just improves polish
- Cacheable — same concept + same detail level produces stable output

### Negative
- LLM path adds latency (mitigated by fallback and potential caching)
- Explanation quality varies with LLM quality (mitigated by structured, evidence-rich input)
- New method on `SemanticReasoningClient` — existing providers must add an implementation or accept fallback
