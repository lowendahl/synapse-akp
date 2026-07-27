# Component: Pack Loader

## Purpose
The pack loader is the sole runtime gateway between AKP domain logic and compiled DuckDB artifacts. It opens packs read-only, validates required schema contracts, executes query objects, and maps raw rows into typed runtime models with provenance-aware metadata.

## Modules Covered
- `akp_runtime.infrastructure.duckdb_loader` — read-only pack adapter and multi-pack loader
- `akp_runtime.infrastructure.duckdb_pack_connection` — schema validation and manifest-to-metadata loading
- `akp_runtime.infrastructure.duckdb_graph_service` — graph traversal and provenance assembly
- `akp_runtime.infrastructure.persistence.__init__` — persistence package marker
- `akp_runtime.infrastructure.persistence.manifest_parser` — manifest validation and `PackMetadata` construction
- `akp_runtime.infrastructure.persistence.result_mapper` — row-to-domain mapping
- `akp_runtime.infrastructure.persistence.queries.__init__` — query package marker
- `akp_runtime.infrastructure.persistence.queries.base` — query object base class and executor
- `akp_runtime.infrastructure.persistence.queries.schema_validation` — initialization queries
- `akp_runtime.infrastructure.persistence.queries.search_queries` — alias, lexical, lookup, and unit retrieval queries
- `akp_runtime.infrastructure.persistence.queries.graph_queries` — edge traversal and edge provenance queries
- `akp_runtime.infrastructure.persistence.queries.provenance_queries` — object and semantic-unit provenance queries

## Responsibilities
- Open `.duckdb` packs in read-only mode
- Validate required tables and required manifest keys before serving queries
- Enforce schema-major compatibility for compiled packs
- Expose typed retrieval methods through the `LoadedPack` protocol
- Execute SQL through query objects rather than inline orchestration SQL
- Map raw DuckDB rows into runtime domain models and provenance steps
- Manage idempotent close semantics for single-pack and multi-pack loaders

## Out of Scope
- Query embedding generation
- USearch sidecar access
- MCP transport
- Runtime operation orchestration
- Compiler-side DuckDB writing

## Promises
- **P-PACK-001**: Every pack connection is opened with `read_only=True`.
- **P-PACK-002**: Missing required tables or manifest keys fail before a `LoadedPack` is returned.
- **P-PACK-003**: Only schema major version `2` is accepted.
- **P-PACK-004**: Query failures are translated into typed runtime errors with pack context.
- **P-PACK-005**: `close()` is idempotent and marks the query executor closed.
- **P-PACK-006**: SQL statements remain confined to `infrastructure.persistence.queries.*`.

## Invariants
- **INV-PACK-001**: `akp_runtime.infrastructure.duckdb_loader` is the only runtime module that imports `duckdb` directly; helper modules remain dependency-free.
- **INV-PACK-002**: Loader APIs do not perform DDL or DML against loaded packs.
- **INV-PACK-003**: Query execution always flows through `PackQuery` objects and `QueryExecutor`.
- **INV-PACK-004**: Returned runtime models are detached from raw row tuples.

## Dependencies
- `akp_runtime.contracts.protocols`
- `akp_runtime.contracts.errors`
- `akp_runtime.domain.models`
- DuckDB

## Dependents
- `akp_runtime.operations.search`
- `akp_runtime.operations.lookup_concept`
- `akp_runtime.operations.expand_graph`
- `akp_runtime.operations.get_provenance`
- `akp_runtime.pipeline.bootstrap`
