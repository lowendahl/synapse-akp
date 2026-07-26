# AKP Runtime

## Purpose

Load compiled Knowledge Packs and serve hybrid retrieval via MCP (Model Context Protocol) over stdio transport. The runtime is the bridge between compiled knowledge and consuming applications (CSU-IQ, Forecast, BOJO).

## Responsibilities

- **Pack loading** — Open `.duckdb` packs read-only, validate schema 2.0.0, warm caches
- **Vector sidecar loading** — Restore `.usearch` indexes and map to unit IDs
- **Hybrid retrieval** — Exact alias → BM25 lexical → vector semantic → RRF fusion → graph boost
- **Concept lookup** — ID/alias/title resolution with unit preview and neighbor hydration
- **Graph expansion** — N-hop BFS over preloaded adjacency maps
- **Provenance assembly** — Full lineage chain (package → object → unit → edge → embedding → retrieval)
- **MCP tool exposure** — `akp_search`, `akp_lookup_concept`, `akp_expand_graph`, `akp_get_provenance`
- **Configuration** — Env vars → YAML → defaults precedence
- **Multi-pack federation** — Query multiple packs independently, merge with deterministic ordering
- **Graceful degradation** — Missing vector sidecar disables semantic channel without crashing
- **Runtime observability** — Domain events (ServerStarting, PackLoaded, ToolInvoked, etc.)

## Out of Scope

- Planning and execution (AIR owns this)
- Business domain logic (applications own this)
- Knowledge authoring or mutation (compiler owns authoring)
- Pack compilation or enrichment
- User authentication (consumer application responsibility)
- Governance policy enforcement beyond read-only access (future Phase 3)

## Package Structure

```
runtime/src/akp_runtime/
├── contracts/       # Pydantic models, protocols, typed errors
├── domain/          # Frozen dataclasses, scoring, provenance
├── events/          # Runtime event bus
├── infrastructure/  # DuckDB loader, USearch reader, FastEmbed, config
├── operations/      # Search, lookup, graph, provenance operations
├── pipeline/        # Composition root / bootstrap
└── consumer/        # MCP server (stdio transport)
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `akp_search` | Hybrid retrieval with RRF fusion and graph boost |
| `akp_lookup_concept` | Exact concept resolution with units and neighbors |
| `akp_expand_graph` | N-hop neighborhood traversal |
| `akp_get_provenance` | Full lineage chain for any artifact |

## Promises

- **Deterministic results** — Same inputs, same pack order, same result order
- **Provenance on every response** — Every result includes full lineage chain
- **Stable MCP contract** — Tool input/output schemas are the public API
- **No compiler dependency** — Runtime reads only the emitted pack schema, never imports compiler code
- **Graceful degradation** — Missing optional assets degrade features, never crash

## Invariants

- Runtime MUST NOT mutate loaded packs (read-only DuckDB connections)
- Runtime MUST NOT import from `kp_compiler` package
- Only `infrastructure/duckdb_loader.py` MAY import `duckdb`
- Only `infrastructure/usearch_reader.py` MAY import `usearch`
- Only `infrastructure/fastembed_adapter.py` MAY import `fastembed`
- Provenance MUST be attached to every returned result
- RRF formula: `score = Σ 1/(k + rank_i)` with k=60 default
- Sort key: `(-score, pack_id, object_id, unit_id or "")`

## Dependencies

- `duckdb>=1.0` — Pack database engine
- `bm25s>=0.2` — Lexical retrieval
- `fastembed>=0.3` — Query embedding
- `usearch>=2.0` — Vector ANN search
- `mcp>=1.0` — MCP server SDK (stdio transport)
- `pydantic>=2.0` — Contract validation
- `ruamel.yaml>=0.18` — Config file parsing

## Related ADRs

- ADR-003: DuckDB as physical engine
- ADR-015: Runtime neutrality
- ADR-021: Hybrid retrieval mandatory
- ADR-025: Pack format specification (Schema 2.0.0)
- ADR-026: MCP stdio transport for runtime
