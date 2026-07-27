---
type: ADR
title: "ADR-007 — Graph: DuckDB Storage, NetworkX as Compiler Tool"
id: adr.007
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, graph, networkx, duckdb, compiler, validation]
---

# ADR-007 — Graph: DuckDB Storage, NetworkX as Compiler Tool

## Status

**Accepted** — 2026-07-25

## Context

The SDD (§8.4, OADR-KP-003) requires a graph projection representing knowledge relationships. The graph must support validation, structural analysis, and relationship inference during compilation.

Key insight: graph algorithms are needed **at compile time** (validation, orphan detection, cycle detection, centrality scoring, relationship inference). The **published pack** needs only a portable, inspectable, queryable representation — not a graph engine.

## Decision

### NetworkX is a compiler-internal tool

NetworkX is used **inside the Knowledge Compiler** as an intermediate processing engine:

```
Markdown sources
      ↓
   Parser
      ↓
   NetworkX DiGraph  ← compiler-internal representation
      ↓
   ┌──────────────────────────────┐
   │  Validation                   │
   │  • orphan detection           │
   │  • cycle detection            │
   │  • connected components       │
   │  • dangling reference check   │
   │                               │
   │  Ontology enforcement         │
   │  • predicate validation       │
   │  • cardinality checks         │
   │  • type constraints           │
   │                               │
   │  Graph algorithms             │
   │  • PageRank (importance)      │
   │  • centrality (hub concepts)  │
   │  • shortest path (distances)  │
   │                               │
   │  Relationship inference       │
   │  • transitive closure         │
   │  • implied relationships      │
   │  • community detection        │
   └──────────────────────────────┘
      ↓
   Export to DuckDB
      ↓
   Knowledge Pack (.duckdb)
```

NetworkX is **NOT shipped with the pack**. It is a compiler dependency only.

### DuckDB is the published graph format

The compiled Knowledge Pack stores the graph as relational tables:

```sql
CREATE TABLE nodes (
    id VARCHAR PRIMARY KEY,       -- stable canonical ID (e.g., csu.metric.job1-c2c)
    type VARCHAR NOT NULL,        -- ontology object type
    title VARCHAR,
    domain VARCHAR,               -- mcem | csu
    pack_id VARCHAR,              -- which pack owns this node
    properties JSON,              -- type-specific metadata
    pagerank FLOAT,               -- compiler-computed importance
    in_degree INTEGER,            -- compiler-computed
    out_degree INTEGER            -- compiler-computed
);

CREATE TABLE edges (
    id VARCHAR PRIMARY KEY,       -- deterministic edge ID
    subject_id VARCHAR NOT NULL,  -- source node ID
    predicate VARCHAR NOT NULL,   -- ontology predicate
    object_id VARCHAR NOT NULL,   -- target node ID
    origin VARCHAR NOT NULL,      -- authored | derived | inferred
    confidence FLOAT,             -- NULL for authored/derived; 0-1 for inferred
    provenance JSON,              -- source document, revision, compiler stage
    FOREIGN KEY (subject_id) REFERENCES nodes(id),
    FOREIGN KEY (object_id) REFERENCES nodes(id)
);

CREATE TABLE graph_metadata (
    key VARCHAR PRIMARY KEY,
    value JSON
);
-- e.g., node_count, edge_count, connected_components, orphan_count, build diagnostics
```

### What the compiler does with NetworkX

| Compiler Stage | NetworkX Usage |
|----------------|----------------|
| **Validation** | `nx.isolates(G)` → orphan detection (nodes with no edges) |
| **Validation** | `nx.simple_cycles(G)` → circular dependency detection |
| **Validation** | `nx.number_connected_components(G.to_undirected())` → fragmentation check |
| **Ontology** | Filter edges by predicate, validate against allowed predicates |
| **Scoring** | `nx.pagerank(G)` → importance ranking per node |
| **Scoring** | `nx.betweenness_centrality(G)` → hub concept identification |
| **Inference** | `nx.ancestors(G, node)` / `nx.descendants(G, node)` → transitive closure |
| **Diagnostics** | `nx.shortest_path_length(G)` → graph diameter, reachability |
| **Export** | Serialize to DuckDB node/edge tables |
| **Visualization** | Optional GraphML/GEXF export for Gephi/yEd |

### What the runtime does NOT require

The runtime consumer of the Knowledge Pack:

- Reads DuckDB tables directly (SQL queries, joins, filters)
- May choose to load into NetworkX, rustworkx, igraph, or any graph library — that's their decision
- May use DuckDB recursive CTEs for simple traversal
- May export to Neo4j, TigerGraph, or a visualization tool

The pack makes **no assumptions** about the runtime graph engine. It exports a clean, portable relational representation.

## Consequences

- **Compiler gets full graph power** — validation, scoring, inference, cycle detection during build.
- **Pack remains engine-neutral** — just DuckDB tables; runtime picks its own tools.
- **NetworkX is NOT a runtime dependency** — consumers don't need it installed.
- **Pre-computed metrics** (PageRank, centrality, degree) are baked into node records — runtime doesn't need to recalculate.
- **Build diagnostics use graph analysis** — orphans, cycles, disconnected components surface as build warnings/errors.
- **Inferred relationships are proposed** — compiler uses graph algorithms to suggest edges; stored with `origin: inferred` and `confidence` score.

## Alternatives Considered

| Alternative | Why Not Selected |
|-------------|-----------------|
| NetworkX as runtime requirement | Couples consumers to a specific library; violates KP-14 |
| No graph processing at compile time | Loses validation power and computed metrics |
| KùzuDB at compile time | Heavier than needed; NetworkX is pure Python, zero-config |
| Skip graph entirely, just store edges | Loses orphan/cycle detection; no computed importance |
| Ship graph as separate file format | Breaks single-pack-file principle |
