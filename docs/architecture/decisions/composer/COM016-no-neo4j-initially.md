# COM016: Do Not Introduce Neo4j Initially

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer needs graph semantics for relationships, provenance and analysis, but that does not automatically require a graph database. Starting with a dedicated graph store would add operational complexity before graph-specific scale or interaction patterns are proven.

## Decision

Represent graph state initially through relational structures such as `knowledge_nodes`, `knowledge_edges`, `aliases`, `source_links` and `provenance_edges`, persisted in DuckDB or PostgreSQL and analyzed in-process with NetworkX. Treat OKF relations as the canonical graph representation, and defer Neo4j until measurable needs such as large cross-AKP traversal, high concurrency, deep path querying, graph-native APIs, interactive exploration or enterprise graph governance justify a separate projection.

## Consequences

Composer gets graph capabilities immediately without another operational dependency. If a graph database is later introduced, it must remain a projection derived from canonical OKF and relational state rather than becoming the new source of truth.
