# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in Synapse AKP, please report it
responsibly:

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Email: plwendahl@microsoft.com with subject "AKP Security Report"
3. Include: description, reproduction steps, potential impact
4. Response target: within 48 hours

## Threat Model

### Trust Boundaries

```
┌─────────────────────────────────────────────────┐
│  Trusted Zone (Compile-Time)                    │
│  - OKF Markdown sources (human-reviewed)         │
│  - ontology.yaml (schema)                        │
│  - pack-rules.yaml (validation)                  │
│  Compiler produces immutable DuckDB artifacts    │
└──────────────────────┬──────────────────────────┘
                       │ Compiled .duckdb packs (read-only)
┌──────────────────────▼──────────────────────────┐
│  Runtime Zone (Query-Time)                       │
│  - MCP server (stdio/SSE transport)              │
│  - DuckDB opened READ-ONLY                       │
│  - No pack mutation (ADR-019)                    │
│  - Input validated at tool boundary              │
└──────────────────────┬──────────────────────────┘
                       │ MCP protocol (typed JSON)
┌──────────────────────▼──────────────────────────┐
│  Consumer Zone (Untrusted)                       │
│  - AI agent clients                              │
│  - User queries (arbitrary strings)              │
│  - Potential for injection, DoS                  │
└─────────────────────────────────────────────────┘
```

### Attack Surface

| Vector | Mitigation |
|--------|-----------|
| Query injection (SQL) | DuckDB parameterized queries only; no string interpolation |
| Query injection (prompt) | Runtime returns pack content verbatim; no LLM re-interpretation in core path |
| Denial of service (large queries) | Query length limits (500 chars), result limits (50 results), hop limits (3) |
| Pack tampering | Packs opened read-only; content_hash in metadata for integrity verification |
| Path traversal | Config paths resolved and validated; pack_path must be absolute or relative to config |
| PII leakage | See PII Policy below; compile-time rules reject PII in sources |
| Supply chain | Minimal dependencies; all pinned in pyproject.toml |

### Security Invariants

1. **Read-only database access** — DuckDB connections opened with `read_only=True`
2. **Parameterized queries** — all SQL uses `?` placeholders, never f-strings
3. **Input validation at boundary** — all MCP tool inputs validated via Pydantic
4. **No shell execution** — runtime never spawns subprocesses from user input
5. **No network egress** — stdio transport has no outbound connections
6. **Process isolation** — runtime runs as subprocess of the consuming agent

## PII Policy

### Compile-Time (Source Authoring)

Knowledge pack sources **MUST NOT** contain:
- Customer names, account names, or tenant identifiers
- Email addresses or phone numbers
- Employee names (use role references: "the CSA", "the AE")
- Internal tool URLs with embedded auth tokens
- Financial figures tied to specific customers

Pack-rules.yaml enforces pattern-based PII detection at compile time.
Compilation fails if PII patterns are detected in source Markdown.

### Runtime (Query-Time)

- User queries are never logged at INFO level (only DEBUG, disabled by default)
- Query content is never written to disk
- Error messages never echo back full query content (truncated to 50 chars)
- No telemetry or analytics collection in the open-source runtime

### Enforcement

Add to `okf/pack-rules.yaml`:
```yaml
pii_rules:
  - pattern: '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    description: "Email address detected"
    severity: error
  - pattern: '\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    description: "Phone number detected"
    severity: error
  - pattern: '\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b'
    description: "UUID/tenant ID detected"
    severity: warning
```

## Dependency Security

- Runtime dependencies are intentionally minimal
- No native code dependencies beyond DuckDB (which is vendored)
- `mcp` SDK is the only network-capable dependency (stdio mode uses no network)
- Regular `pip audit` recommended in CI pipeline

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.x     | ✅ (current development) |

## Secure Deployment Recommendations

1. Run the MCP server as a **non-privileged user**
2. Mount pack directories as **read-only filesystem** in containers
3. Use process-level resource limits (memory, CPU, file descriptors)
4. In SSE mode (future), bind to localhost only unless behind a reverse proxy
5. Rotate and version packs — never patch compiled artifacts in place
