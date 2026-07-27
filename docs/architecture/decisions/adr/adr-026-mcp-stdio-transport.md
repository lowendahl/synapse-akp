# ADR-026: MCP stdio Transport for Runtime

## Status

Accepted

## Context

The AKP Runtime must expose retrieval capabilities to consuming applications (CSU-IQ, Forecast, BOJO). These applications use AI agents that need structured access to knowledge. We need a protocol that:

1. Allows any MCP-compatible client to discover and call runtime tools
2. Works locally without network infrastructure (MVP requirement)
3. Supports typed schemas for tool inputs and outputs
4. Is language-agnostic on the client side
5. Aligns with the Synapse platform direction (agent-native)

Options considered:
- **REST API** — requires HTTP server, port management, deployment complexity
- **gRPC** — binary protocol, complex setup, overkill for local single-process
- **MCP over stdio** — subprocess communication, no network, schema-native
- **MCP over SSE** — network-based MCP, suitable for multi-client but adds infra
- **Direct Python import** — no process isolation, couples consumer to runtime internals

## Decision

We SHALL use **MCP (Model Context Protocol) over stdio transport** for the Phase 1 runtime server.

Implementation details:
- Use the Python `mcp` SDK's `FastMCP` surface for tool registration
- Server launched as subprocess: `python -m akp_runtime --config path/to/config.yaml`
- Client (CSU-IQ context assembler) connects via MCP client SDK over stdin/stdout
- Four tools exposed initially: `akp_search`, `akp_lookup_concept`, `akp_expand_graph`, `akp_get_provenance`
- Fifth tool planned: `akp_explain_concept` (ADR-038) — human-readable prose synthesis
- Each tool accepts typed JSON input and returns typed JSON output
- Errors map to MCP error codes (-32602 for validation, -32000 for domain, -32603 for internal)

## Consequences

### Positive
- Zero network infrastructure for local development
- Process isolation between consumer and runtime
- Schema discovery built into MCP protocol (clients auto-discover tools)
- Aligns with GitHub Copilot / AI agent ecosystem (MCP is the emerging standard)
- Easy migration path to SSE transport for multi-client scenarios (Phase 3)

### Negative
- Subprocess startup cost on first invocation (~1-3s for pack loading)
- Single client per stdio session (acceptable for MVP)
- No built-in connection pooling

### Mitigations
- Pack warm-up at server start (caches survive across tool calls within session)
- SSE transport planned for Phase 3 multi-client support
- Long-lived server process (stays running until client disconnects)

## Future Evolution

- Phase 3: Add SSE transport option alongside stdio
- Phase 4: Registry-based discovery (runtime advertises capabilities)
- Phase 5: Multi-runtime federation (query across distributed runtimes)
