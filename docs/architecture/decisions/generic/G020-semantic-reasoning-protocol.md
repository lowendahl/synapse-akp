# ADR-036: SemanticReasoningClient Protocol

| Field | Value |
|-------|-------|
| **ID** | `ADR-036` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-017 (LLM protocol), ADR-018 (unified pipeline), ADR-038 (explain operation) |
| **Supersedes** | Widens ADR-017's `AcronymReasoningClient` into a broader protocol |

## Context

ADR-017 established the LLM integration pattern: a Python `Protocol` with provider adapters (GitHub Copilot SDK as the default). That protocol defined two methods for acronym-specific tasks (`disambiguate`, `expand`).

The unified semantic pipeline (ADR-018) requires LLM capabilities across multiple stages:

- **Classification** — given a candidate term and context, determine its entity type(s).
- **Definition extraction** — given a concept mention, extract or synthesize its definition.
- **Measure extraction** — given a sentence about a metric, extract measure semantics (formula, unit, aggregation).
- **Equivalence resolution** — given two candidate terms, determine if they refer to the same entity.
- **Indicator classification** — given a measure in context, determine if it is used as an indicator and what it indicates.

Each method must return **structured Pydantic output** with confidence scores, not free-form text.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Extend AcronymReasoningClient with new methods** | Backwards compatible | Naming is misleading; acronym-specific |
| **B. Create separate protocols per domain** | Clean separation | Provider must implement N protocols |
| **C. Single SemanticReasoningClient protocol (chosen)** | One adapter covers all LLM needs; coherent interface | Larger protocol surface |

## Decision

Define a single `SemanticReasoningClient` protocol that replaces `AcronymReasoningClient`:

```python
class SemanticReasoningClient(Protocol):
    async def classify_candidate(
        self, context: CandidateContext
    ) -> ClassificationResult: ...

    async def extract_definition(
        self, context: CandidateContext
    ) -> DefinitionResult: ...

    async def extract_measure(
        self, context: CandidateContext
    ) -> MeasureExtractionResult: ...

    async def resolve_equivalence(
        self, context: EquivalenceContext
    ) -> EquivalenceResult: ...

    async def classify_indicator(
        self, context: IndicatorContext
    ) -> IndicatorResult: ...

    async def disambiguate_acronym(
        self, context: AcronymContext
    ) -> AcronymDisambiguationResult: ...

    async def infer_expansion(
        self, context: AcronymContext
    ) -> AcronymExpansionResult: ...
```

### Design Principles

1. **All methods are optional** — a provider that only handles classification is valid; unimplemented methods raise `NotImplementedError` and the pipeline falls back to heuristics.
2. **Structured output only** — every method returns a Pydantic model with confidence scores.
3. **Context objects are rich** — include surrounding text, document metadata, existing classifications, and taxonomy labels.
4. **Idempotent** — same input + same model + same temperature = same output.
5. **Batch-capable** — providers may implement `classify_batch()` for throughput optimization.

### Provider Implementation

The existing `CopilotReasoningProvider` (from ADR-017) is widened to implement this protocol:

- Each method constructs a domain-specific system prompt with taxonomy context.
- JSON mode / structured output is used where the LLM supports it.
- Response parsing uses Pydantic `model_validate_json()` with fallback to regex extraction.
- The 3-tier fallback (SDK → API key → `gh models`) is preserved from ADR-017.

### Prompt Construction

Prompts are **built dynamically** from:
- The taxonomy (ADR-019) — injected as classification labels.
- The context window — surrounding sentences, document metadata.
- The existing entity state — what is already known about this candidate.
- The question — specific to each method (classify, define, extract measure, etc.).

No prompts are hardcoded in the framework — they are assembled from templates and corpus-derived context.

## Consequences

- `AcronymReasoningClient` is deprecated; existing acronym methods move into `SemanticReasoningClient`.
- The `CopilotReasoningProvider` gains new methods but retains its existing auth/fallback logic.
- New providers (Azure OpenAI, Ollama, Foundry) implement the same protocol.
- Testing uses a `MockReasoningProvider` that returns fixture responses.
- The protocol is versioned — adding methods is backwards-compatible (they default to `NotImplementedError`).
- ADR-038 adds `synthesize_explanation()` to this protocol for human-readable concept explanations.
