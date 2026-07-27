# COM017: Use Vectors Only for Candidate Generation

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Embeddings are useful for finding likely matches and review candidates, but similarity search does not determine authority, truth or commit-worthy relationships. Composer therefore needs a bounded role for vector infrastructure.

## Decision

Use embeddings and vector indexes only for candidate-generation tasks such as duplicate detection, similar-concept discovery, candidate-to-existing-object matching, related-source detection, review prioritization and clustering. Do not let vectors decide identity, source authority, supersession, truth or committed relations. Use a replaceable local adapter such as LanceDB or another lightweight local index, and use pgvector or Qdrant for enterprise deployments as scale warrants.

## Consequences

Vector infrastructure stays rebuildable and disposable, which keeps semantic truth in the canonical knowledge and validation layers. Candidate recall can improve without granting the vector store authoritative status in the composition workflow.
