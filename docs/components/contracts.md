# Component: Contracts

## Purpose
The contracts component defines the typed seams between AKP layers. It captures compiler and runtime protocols, error hierarchies, runtime event contracts, and MCP request/response models so orchestration, infrastructure, and consumer code depend on explicit shapes rather than implicit conventions.

## Modules Covered
- `kp_compiler.contracts.__init__` — contracts package marker
- `kp_compiler.contracts.protocols` — compiler protocols, diagnostics, and graph result contracts
- `kp_compiler.contracts.infrastructure_protocols` — compiler infrastructure adapter and query protocols
- `kp_compiler.contracts.protocol_support_types` — shared compiler diagnostics and graph support types
- `kp_compiler.contracts.stage_protocols` — compiler stage boundary protocols
- `kp_compiler.contracts.errors` — typed compiler exception hierarchy
- `akp_runtime.contracts.__init__` — contracts package marker
- `akp_runtime.contracts.protocols` — runtime protocols for loaders, operations, embedders, and vector indexes
- `akp_runtime.contracts.errors` — typed runtime exception hierarchy
- `akp_runtime.contracts.events` — immutable runtime event contracts
- `akp_runtime.contracts.mcp_config` — runtime configuration models
- `akp_runtime.contracts.mcp_search` — MCP search request and response models
- `akp_runtime.contracts.mcp_lookup` — MCP concept lookup request and response models
- `akp_runtime.contracts.mcp_graph` — MCP graph expansion request and response models
- `akp_runtime.contracts.mcp_provenance` — MCP provenance request and response models
- `akp_runtime.contracts.mcp_models` — facade re-export of public MCP models

## Responsibilities
- Define protocol-based dependencies for compiler stages and runtime adapters
- Define typed diagnostics and exceptions with actionable context
- Define the public MCP schemas used by the runtime consumer surface
- Define immutable event types used for runtime observability
- Provide stable import locations for callers that should not know canonical module splits

## Out of Scope
- Filesystem IO
- DuckDB queries
- Search scoring
- Runtime bootstrap or server hosting

## Promises
- **P-CONTRACT-001**: Runtime MCP models reject undeclared fields via `extra="forbid"`.
- **P-CONTRACT-002**: `GetProvenanceToolInput` accepts exactly one provenance target kind.
- **P-CONTRACT-003**: Compiler and runtime protocols remain `runtime_checkable` for adapter verification.
- **P-CONTRACT-004**: Compiler and runtime exceptions carry structured context in their fields and string rendering.
- **P-CONTRACT-005**: Field constraints on limits, hops, and score payloads are enforced by Pydantic validation.

## Invariants
- **INV-CONTRACT-001**: Contract modules do not perform infrastructure IO.
- **INV-CONTRACT-002**: Consumer, operation, and infrastructure layers depend on contracts; contracts do not depend on those layers.
- **INV-CONTRACT-003**: Public transport schemas are explicit Python models rather than anonymous dictionaries.

## Dependencies
- `pydantic`
- Standard library typing and dataclasses
- Runtime domain models for protocol return types

## Dependents
- All compiler stages and adapters
- All runtime infrastructure adapters and operations
- MCP consumer surfaces
