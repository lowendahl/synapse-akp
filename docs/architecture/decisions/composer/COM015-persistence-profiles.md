# COM015: DuckDB Locally, PostgreSQL for Shared Composer State

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer must support both a local workbench and a collaborative enterprise service. Those modes have different concurrency and storage needs, so one persistence choice should not be forced across both.

## Decision

Use DuckDB as the local composition workbench for source manifests, normalized block metadata, candidates, relations, evaluation results, search analytics and local composition state, with SQLite used only where simple transactional workflow semantics or library constraints make it preferable. For shared enterprise operation, use PostgreSQL for concurrent workspaces, reviews, job state, identity and authorization, composition proposals, audit records and workspace metadata, and use object storage for source files, rendered pages, normalized JSON or Parquet, model artifacts and release packages.

## Consequences

Local Composer stays lightweight and analytics friendly, while collaborative deployments gain robust concurrent service storage. Persistence design must keep working data and binary artifacts separate, and enterprise search extensions such as pgvector remain optional rather than foundational.
