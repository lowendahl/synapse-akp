# COM001: Recommended Reference Stack

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer needs a replaceable reference architecture so ingestion, interpretation, storage and release concerns are chosen intentionally rather than around a single parser, agent framework or database. The source document identifies a default stack and explicit escalation paths across acquisition, extraction, orchestration, persistence, search, provenance and evaluation.

## Decision

Adopt the recommended reference stack as Composer's default architecture: Python 3.12+, Pydantic v2 contracts, FastAPI with Typer CLI, Docling as the default parser, format-native enrichers for DOCX/PPTX/PDF, Azure AI Document Intelligence for difficult OCR cases, MarkItDown for convenience conversion, Unstructured for fallback and benchmarking, HTTPX plus Trafilatura for web ingestion with Playwright escalation, a multimodal model gateway for visual interpretation, an explicit state machine that can later move to Temporal, DuckDB locally, PostgreSQL for shared service state, Git-backed OKF as the canonical knowledge store, relational edge tables plus NetworkX for graph work, vector search only as a candidate aid, OpenTelemetry for observability, and a golden-corpus evaluation harness.

## Consequences

This stack becomes the canonical starting point for Composer decisions, but each tool remains replaceable behind Synapse-owned contracts. Teams must justify deviations, keep secondary paths policy controlled, and preserve the architecture's core rule that the canonical document model and OKF model define the system rather than any vendor tool.
