# COM006: Keep Unstructured as a Benchmark and Fallback Provider

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer needs resilience across unusual formats and a way to compare parser quality over time. Unstructured offers broad partitioning coverage, useful email support such as `.eml` and `.msg`, and a second opinion on element boundaries, but making two extraction frameworks equally central would increase coupling.

## Decision

Maintain Unstructured as a benchmark and fallback extraction provider under the same `DocumentExtractor` contract used by Docling. Parser selection must be policy driven, with Unstructured reserved for unsupported formats, comparison, regression testing and fallback extraction rather than as Composer's primary domain dependency.

## Consequences

Composer can compare providers and recover from parser gaps without exposing provider specifics beyond the extraction boundary. The platform must own adapter contracts and routing policy, and downstream stages must remain indifferent to whether a result came from Docling, Unstructured or another future provider.
