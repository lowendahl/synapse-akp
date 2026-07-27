# Component: Infrastructure

## Purpose
The infrastructure component contains the concrete adapters that talk to filesystems, DuckDB artifacts, rules files, embedding libraries, vector sidecars, and persistence query engines. It keeps IO and external-library dependencies out of domain, contracts, and operation code.

## Modules Covered
- `kp_compiler.infrastructure.__init__` — compiler infrastructure package marker
- `kp_compiler.infrastructure.filesystem` — UTF-8 source discovery and file reads
- `kp_compiler.infrastructure.duckdb_writer` — compiler-side DuckDB schema creation and projection persistence
- `kp_compiler.infrastructure.duckdb_projection_writer` — projection-level DuckDB write helper
- `kp_compiler.infrastructure.duckdb_schema_builder` — compiled-pack schema creation helper
- `kp_compiler.infrastructure.rules_loader` — YAML rules loading into typed pack rules
- `kp_compiler.infrastructure.queries.__init__` — compiler query package facade
- `kp_compiler.infrastructure.queries.pack_queries` — dependency-pack query objects
- `kp_compiler.infrastructure.queries.outcome_queries` — outcome-validation query objects
- `akp_runtime.infrastructure.__init__` — runtime infrastructure package marker
- `akp_runtime.infrastructure.config_loader` — runtime configuration adapter (specialized in `config-loader.md`)
- `akp_runtime.infrastructure.duckdb_loader` — runtime pack adapter (specialized in `pack-loader.md`)
- `akp_runtime.infrastructure.fastembed_adapter` — reserved query-embedding adapter boundary
- `akp_runtime.infrastructure.provenance_factory` — provenance-step factory for loaded pack artifacts
- `akp_runtime.infrastructure.usearch_reader` — reserved vector-sidecar adapter boundary
- `akp_runtime.infrastructure.persistence.__init__` — persistence package marker
- `akp_runtime.infrastructure.persistence.manifest_parser` — manifest parsing adapter
- `akp_runtime.infrastructure.persistence.result_mapper` — row mapping adapter
- `akp_runtime.infrastructure.persistence.queries.__init__` — queries package marker
- `akp_runtime.infrastructure.persistence.queries.base` — query object base and executor
- `akp_runtime.infrastructure.persistence.queries.schema_validation` — schema validation queries
- `akp_runtime.infrastructure.persistence.queries.search_queries` — search queries
- `akp_runtime.infrastructure.persistence.queries.graph_queries` — graph queries
- `akp_runtime.infrastructure.persistence.queries.provenance_queries` — provenance queries

## Responsibilities
- Perform filesystem reads and rules-file deserialization for the compiler
- Persist compiled projections into DuckDB tables and sidecar metadata
- Open and query compiled packs through query objects and mappers
- Isolate optional embedding and vector-index library dependencies behind dedicated adapter modules
- Constrain SQL to persistence query objects

## Out of Scope
- Domain modeling
- Search fusion logic
- MCP response shaping
- CLI or server argument handling

## Promises
- **P-INFRA-001**: `FilesystemReader.discover(...)` returns `.md` files in sorted order and excludes ADR content.
- **P-INFRA-002**: `RulesLoader` returns `PackRules.default()` when the rules file is absent or empty.
- **P-INFRA-003**: `DuckDBPackWriter` creates all required compiler pack tables before writing projections.
- **P-INFRA-004**: Alias values written by `DuckDBPackWriter` are normalized to lowercase.
- **P-INFRA-005**: Runtime SQL remains confined to `akp_runtime.infrastructure.persistence.queries.*`.
- **P-INFRA-006**: Manifest parsing converts numeric manifest fields to Python integers for runtime consumers.
- **P-INFRA-007**: FastEmbed and USearch dependencies are isolated to their dedicated adapter modules.

## Invariants
- **INV-INFRA-001**: Compiler DuckDB writes occur only in `kp_compiler.infrastructure.duckdb_writer`.
- **INV-INFRA-002**: Runtime DuckDB reads occur only through the pack-loader and query-object boundary.
- **INV-INFRA-003**: Infrastructure modules may depend on domain and contracts, but domain and contracts do not depend on infrastructure.

## Dependencies
- Filesystem and path APIs
- DuckDB
- YAML parsers
- Optional embedding/vector libraries

## Dependents
- Compiler pipeline
- Runtime pipeline
- Runtime operations
