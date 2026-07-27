# COM009: Use Typed Model Calls, Not Free-Form Agent Responses

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer relies on model output to create candidate claims and change proposals, so free-form prose responses are too unstable for reliable orchestration. The source document calls for Pydantic v2 contracts and a provider-neutral gateway that can validate structured outputs consistently across model providers.

## Decision

Require all model interactions to use versioned, typed Pydantic contracts through a provider-neutral model gateway. The gateway must own structured output generation, model selection, retries, token budgets, redaction, logging, prompt versions, model versions and evaluation traces, and every response must pass provider-side structured output where supported, Pydantic validation, semantic validation, evidence-anchor validation, and retry or rejection when checks fail.

## Consequences

Composer gains deterministic interfaces for interpretation and resolution and avoids coupling to any one agent framework. Frameworks such as LangChain or LlamaIndex may exist inside adapters, but Synapse must own the contracts, validation semantics and orchestration surface.
