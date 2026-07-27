# ADR-029: LLM Integration — Protocol Pattern with GitHub Copilot SDK Provider

| Field | Value |
|-------|-------|
| **ID** | `ADR-029` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |

## Context

The acronym discovery pipeline (ADR-015) requires LLM capabilities for two tasks:

1. **Disambiguation** — when a surface form (e.g., "CSP") has multiple known expansions, select the correct one based on surrounding context.
2. **Expansion inference** — when no explicit definition exists in the corpus, propose a plausible expansion based on usage patterns.

These are Phase 3 capabilities (not needed for deterministic detection in Phase 1), but the architecture must accommodate them from the start.

### Constraints

- **No vendor lock-in** — the framework must not depend on a specific LLM provider
- **Structured output** — LLM responses must conform to Pydantic schemas
- **Reproducibility** — same input + same model + same temperature → same output
- **Testability** — all LLM-dependent code must be unit-testable with mocks
- **LLM as judge, never as source** — output is confidence-gated and human-reviewed

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| Direct OpenAI SDK | Familiar, well-documented | Vendor lock-in, no Copilot integration |
| LangChain | Multi-provider | Heavy dependency, abstraction overhead |
| Protocol + concrete providers | Clean, testable, composable | More files to maintain |
| GitHub Copilot SDK | First-party, org-authorized, token-managed | SDK not yet GA for Python |

## Decision

### Architecture: Protocol + Provider Pattern

```
AcronymReasoningClient (Protocol)      ← abstract contract in contracts/
        ↑
CopilotReasoningProvider               ← default provider using GH Copilot SDK
MockReasoningProvider                   ← test double for unit tests
```

### Protocol Definition

```python
class AcronymReasoningClient(Protocol):
    def disambiguate(self, request: DisambiguationRequest) -> DisambiguationResponse: ...
    def infer_expansion(self, request: ExpansionInferenceRequest) -> ExpansionInferenceResponse: ...
```

All request/response types are frozen Pydantic models with strict validation.

### Default Provider: GitHub Copilot SDK

The default concrete implementation uses the GitHub Copilot chat completions API because:

1. **Org-authorized** — uses existing GitHub token, no separate API key management
2. **Model access** — routes to GPT-4o (or configured model) via Copilot proxy
3. **Structured output** — JSON mode with schema enforcement
4. **Audit trail** — requests are logged through GitHub's infrastructure
5. **Cost attribution** — usage is attributed to the org's Copilot seat

### Configuration

```yaml
# In pack-rules.yaml or compiler config
llm:
  provider: copilot        # or "openai", "ollama", "mock"
  model: gpt-4o
  temperature: 0.1
  max_tokens: 512
```

### Constraints on LLM Usage

1. **Temperature ≤ 0.1** — minimize randomness for reproducible builds
2. **Structured output only** — all responses must parse to Pydantic models
3. **Confidence self-reporting** — model must include confidence in response
4. **No trust escalation** — LLM output never exceeds "inferred" status (0.80-0.95 confidence ceiling)
5. **Fallback to "unresolved"** — if LLM fails or returns low confidence, occurrence goes to review queue
6. **No training data leakage** — prompts contain only corpus text, never proprietary config

### Provider Contract

Any provider implementing `AcronymReasoningClient` must:
- Accept structured requests (Pydantic models)
- Return structured responses (Pydantic models)
- Handle rate limiting internally (retry with backoff)
- Raise typed exceptions on failure (not silent fallback)
- Be injectable via constructor parameter (DI pattern)

## Consequences

### Positive
- Zero vendor lock-in — swap providers by changing one config line
- Fully testable — mock provider for unit tests, real provider for integration
- Clean separation — pipeline logic knows nothing about HTTP, tokens, or models
- Future-proof — when Copilot SDK ships GA, just implement `_call_completions`

### Negative
- Copilot SDK not yet GA — provider stub raises `NotImplementedError` until package ships
- Extra abstraction layer vs. direct SDK call
- Must maintain protocol compatibility across provider versions

### Implementation Status

Refer to the implementation planning documents for current status and file-level tracking.
