---
type: ADR
title: "ADR-003 — DuckDB as Physical Metadata Engine"
id: adr.003
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, duckdb, storage, physical-engine]
---

# ADR-003 — DuckDB as Physical Metadata Engine

## Status

**Accepted** — 2026-07-25

## Context

The SDD (OADR-KP-002) identifies the need for an embedded engine to store normalized objects, metadata, provenance, graph projections, and lexical indexes. The engine must:

- Run embedded (no server process)
- Support Windows
- Handle analytical queries over projections efficiently
- Support schema evolution
- Provide full-text capabilities or pair with a lexical engine

Candidates: DuckDB, SQLite, or another embedded relational engine.

## Decision

**DuckDB** SHALL be the physical engine for the Knowledge Pack's structured projections:

- Canonical object store (normalized metadata, provenance)
- Graph projection (node/edge tables with typed predicates)
- Lexical projection (terms, aliases, acronyms, inverted index)
- Relationship projection (subject → predicate → object with provenance)
- Manifest and diagnostics

The vector projection SHALL use a **separate dedicated engine** (decision deferred to OADR-001).

## Rationale

| Criterion | DuckDB | SQLite |
|-----------|--------|--------|
| Analytical batch queries | ✓ Columnar, vectorized | ✗ Row-oriented |
| JSON/struct native handling | ✓ Native STRUCT, LIST, MAP | ~ JSON1 extension |
| Full-text search | ~ DuckDB FTS extension | ✓ FTS5 mature |
| Windows support | ✓ | ✓ |
| File portability | ✓ Single `.duckdb` file | ✓ Single `.db` file |
| Parquet/Arrow interop | ✓ Native | ✗ Requires tooling |
| Runtime footprint | ~40MB | ~5MB |
| Concurrency (single-writer) | ✓ Acceptable for build | ✓ |
| Schema evolution | ✓ ALTER TABLE, views | ✓ |

DuckDB wins on analytical query patterns (the primary access pattern for a compiled pack) and native structured data handling. Its FTS extension covers lexical needs. The larger footprint is acceptable for a developer/server-side artifact.

## Consequences

- Each Knowledge Pack is a single `.duckdb` file (plus a separate vector index file).
- The compiler writes DuckDB; consumers read DuckDB.
- Graph traversal uses recursive CTEs (no native graph syntax — acceptable for knowledge-graph scale).
- FTS uses DuckDB's full-text extension for lexical matching.
- Vector search is decoupled — the vector engine reads from DuckDB metadata but stores embeddings separately.
- Pack integrity checks validate DuckDB content hashes against the manifest.

## Alternatives Considered

| Alternative | Why Not Selected |
|-------------|-----------------|
| SQLite | Weaker analytical queries; Knowledge Pack access pattern is batch/analytical |
| SQLite + sqlite-vec | Would unify vector + metadata but sqlite-vec is immature; analytical queries still row-scan |
| PostgreSQL/remote DB | Violates embedded/portable requirement |
| Flat files (JSON/Parquet) | No query capability; no FTS; manual index management |
