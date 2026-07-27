# Component: AKP Runtime

## Purpose
The runtime component is the package-level boundary for serving compiled Knowledge Packs. It provides the stable package identity and the module entry path that hands control to the consumer-facing MCP runtime without importing compiler code or opening infrastructure resources at import time.

## Modules Covered
- `akp_runtime.__init__` — runtime package identity and version contract
- `akp_runtime.__main__` — `python -m akp_runtime` entry point

## Responsibilities
- Publish the runtime package version
- Expose the canonical module entry point for MCP hosting
- Preserve the package boundary between compiled-pack serving and compile-time concerns
- Delegate runtime startup to the consumer/bootstrap layers

## Out of Scope
- Pack loading implementation
- Search, lookup, graph, or provenance operations
- MCP tool registration logic
- Compiler stage execution

## Promises
- **P-RUN-001**: `python -m akp_runtime` delegates to the MCP server entry surface every time.
- **P-RUN-002**: Importing `akp_runtime` is side-effect free with respect to pack loading and network/server startup.
- **P-RUN-003**: The package root remains the stable location for runtime versioning.

## Invariants
- **INV-RUN-001**: Root runtime modules do not import `kp_compiler`.
- **INV-RUN-002**: Runtime package initialization does not open DuckDB connections or vector indexes.
- **INV-RUN-003**: Entry-surface modules stay thin and delegate behavior to subcomponents.
- **INV-RUN-004**: Only `akp_runtime.infrastructure.duckdb_loader` imports `duckdb`; helper modules stay dependency-free.

## Dependencies
- `akp_runtime.consumer.mcp_server`
- Standard library import machinery only

## Dependents
- MCP hosts launching the runtime
- Bootstrap and consumer layers
- Downstream applications consuming AKP retrieval tools
