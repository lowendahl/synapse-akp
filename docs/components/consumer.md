# Component: Consumer

## Purpose
The consumer component contains the user-facing and tool-facing entry surfaces that let humans, scripts, and MCP clients interact with compiled packs. It is the boundary where AKP retrieval capabilities are packaged as CLIs, Explorer generation, and runtime server hosting.

## Modules Covered
- `kp_compiler.consumer.__init__` — compiler consumer package marker
- `kp_compiler.consumer.cli` — `kp-find` read-only retrieval CLI over compiled packs
- `kp_compiler.consumer.explorer` — Explorer artifact generator over compiled packs
- `kp_compiler.consumer.knowledge_pack_search_service` — compiled-pack retrieval service for consumer surfaces
- `kp_compiler.consumer.search_result_printer` — console formatter for retrieval channel output
- `kp_compiler.consumer.queries.__init__` — consumer query package facade
- `kp_compiler.consumer.queries.search_queries` — read-only query objects for CLI retrieval workflows
- `kp_compiler.consumer.queries.explorer_queries` — read-only query objects for Explorer extraction workflows
- `akp_runtime.consumer.__init__` — runtime consumer package marker
- `akp_runtime.consumer.mcp_server` — MCP stdio server entry surface

## Responsibilities
- Expose read-only human-facing retrieval commands over compiled packs
- Generate consumable visualization artifacts for compiled knowledge graphs
- Provide the runtime's MCP hosting entry point
- Keep transport and UX concerns separate from pack loading and domain models

## Out of Scope
- Compiler stage implementation
- Pack schema persistence
- Retrieval scoring mathematics
- Authoring source knowledge

## Promises
- **P-CONSUME-001**: Consumer surfaces treat compiled packs as read-only artifacts.
- **P-CONSUME-002**: `kp-find` can compose exact, lexical, semantic, and graph-oriented retrieval paths from a compiled pack.
- **P-CONSUME-003**: Explorer generation delegates graph assembly to pack extraction rather than re-parsing OKF sources.
- **P-CONSUME-004**: Runtime server startup is funneled through a single `mcp_server.main()` entry point.

## Invariants
- **INV-CONSUME-001**: Consumer modules do not own canonical pack schema or domain definitions.
- **INV-CONSUME-002**: Transport and presentation logic remain downstream of operations and infrastructure.
- **INV-CONSUME-003**: Consumer entry surfaces do not mutate authored OKF sources.

## Dependencies
- Compiler and runtime pipelines
- Pack loader and optional vector infrastructure
- MCP model contracts

## Dependents
- Human operators using `kp-find`
- Visual reviewers using Explorer
- MCP clients consuming runtime tools
