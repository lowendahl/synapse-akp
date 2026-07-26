# Component: Pack Loader

## Module

`akp_runtime.infrastructure.duckdb_loader`

## Purpose

Open, validate, and provide query access to compiled AKP Knowledge Pack `.duckdb`
files. This is the sole gateway between the runtime domain logic and the physical
storage layer.

## Responsibilities

1. **Open packs read-only** — open a `.duckdb` file in read-only mode.
2. **Validate schema compatibility** — reject packs whose `schema_version` major
   does not equal `2`.
3. **Validate required tables** — confirm all 5 required tables exist:
   `objects`, `semantic_units`, `aliases`, `edges`, `manifest`.
4. **Validate required manifest keys** — confirm all 19 keys are present.
5. **Expose PackMetadata** — parse the manifest into a `PackMetadata` domain model.
6. **Provide query methods** — implement the `LoadedPack` protocol with:
   - Exact alias matches
   - Object ID fallback
   - BM25 lexical search
   - Semantic (vector) search delegation
   - Concept lookup by qualified ID
   - Semantic unit retrieval for an object
   - Graph neighbor traversal (BFS, max hops)
   - Provenance assembly for objects, units, and edges
7. **Manage multi-pack loading** — load multiple packs by path, keyed by `pack_id`.
8. **Resource cleanup** — close DuckDB connections deterministically.

## Out of Scope

- **Vector index management** — delegated to `usearch_reader.py`.
- **Embedding generation** — delegated to `fastembed_adapter.py`.
- **Configuration parsing** — delegated to `config_loader.py`.
- **Scoring and fusion** — handled by `domain/scoring.py`.
- **MCP transport** — handled by `consumer/mcp_server.py`.
- **Graph boost logic** — handled by operations layer.
- **Pack compilation** — belongs to the compiler package.
- **Schema migration** — out of scope for schema 2.0.0.

## Promises

1. **P-READONLY**: The loader MUST never write to a pack file. All connections
   use DuckDB `read_only=True`.
2. **P-VALIDATE**: A pack that fails schema or table validation MUST raise
   `PackValidationError` before returning a `LoadedPack`.
3. **P-METADATA**: `PackMetadata` MUST contain all 19 manifest values parsed
   to their correct Python types.
4. **P-PROTOCOL**: Every `DuckDBLoadedPack` instance MUST satisfy the
   `LoadedPack` protocol at runtime (`isinstance` check passes).
5. **P-DETERMINISTIC**: Given the same pack file and same query parameters,
   results MUST be identical across invocations.
6. **P-CLOSE-SAFE**: Calling `close()` multiple times MUST NOT raise.
   Calling query methods after `close()` MUST raise `RuntimeStateError`.
7. **P-ERROR-TYPED**: All failures map to the typed error hierarchy:
   - File not found → `PackOpenError`
   - Schema major ≠ 2 → `UnsupportedSchemaVersion`
   - Missing tables → `MissingPackTable`
   - Missing manifest keys → `MissingManifestKey`
   - Query on closed pack → `RuntimeStateError`
   - SQL errors during queries → `PackQueryError`
8. **P-ISOLATION**: Each `LoadedPack` is independent. Closing one pack
   MUST NOT affect another.
9. **P-SCHEMA-MAJOR**: Only schema major version `2` is accepted. Any other
   major version MUST be rejected with `PackValidationError`.

## Invariants

1. **INV-CONNECTION**: A `DuckDBLoadedPack` holds exactly one DuckDB connection
   for its lifetime. No connection pooling, no sharing.
2. **INV-NO-MUTATION**: No method on `LoadedPack` may execute DDL or DML
   (INSERT, UPDATE, DELETE, ALTER, DROP).
3. **INV-LAYER-BOUNDARY**: This module imports ONLY from `contracts/` and
   `domain/`. It MUST NOT import from `operations/`, `pipeline/`, or `consumer/`.
4. **INV-SINGLE-IMPORT**: Only this module (`duckdb_loader.py`) may import the
   `duckdb` library within the runtime package.
5. **INV-PROVENANCE-COMPLETE**: Provenance results always include at minimum
   one step: the `pack` layer step with pack_id and pack_version.
6. **INV-BFS-BOUNDED**: Graph traversal MUST respect the `hops` and `limit`
   parameters. It MUST NOT traverse beyond the requested depth.

## Dependencies

- `duckdb` — physical storage engine (read-only access)
- `akp_runtime.contracts.protocols` — `LoadedPack`, `PackLoader` protocols
- `akp_runtime.contracts.errors` — typed exception hierarchy
- `akp_runtime.domain.models` — `PackMetadata`, `SearchHit`, `GraphEdgeHit`, etc.
- `akp_runtime.domain.provenance` — provenance assembly helpers

## Testing Strategy

- **Unit tests**: Mock DuckDB with in-memory databases populated to spec.
- **Validation tests**: Verify every error path with malformed packs.
- **Protocol compliance**: `isinstance(loader.load(path), LoadedPack)`.
- **Isolation tests**: Close one pack, verify others still work.
- **Determinism tests**: Same query twice → same results.
- **BFS tests**: Verify traversal respects depth and limit bounds.
