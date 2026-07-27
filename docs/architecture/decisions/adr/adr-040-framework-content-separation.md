# ADR-040: Framework / Content Separation

| Field     | Value                                          |
|-----------|------------------------------------------------|
| Status    | Accepted                                       |
| Date      | 2025-07-27                                     |
| Deciders  | Patrik Löwendahl                               |
| Relates   | ADR-003 (DuckDB), ADR-002 (Shared Ontology)    |

## Context

The `synapse-akp` monorepo currently contains both the **framework** (compiler +
runtime) and the **content** (OKF knowledge sources for CSU-IQ-V2). These have
different audiences, release cadences, and access requirements:

| Concern       | Framework              | Content                      |
|---------------|------------------------|------------------------------|
| Audience      | Platform engineers     | Domain authors + all consumers |
| Release       | Semver, on demand      | Per-sprint or on-demand      |
| Sensitivity   | Open-source eligible   | Internal domain knowledge    |
| Size          | ~5 MB code             | ~50 MB compiled packs        |
| Install need  | pip install            | Download .duckdb             |

Keeping them together means:
- Everyone who wants to query knowledge must clone compilation tooling
- Content authors must navigate framework code
- Pack consumers pull NLP/embedding dependencies they'll never use

## Decision

### 1. Two Repositories

| Repository                    | Contains                                        |
|-------------------------------|-------------------------------------------------|
| `lowendahl/synapse-akp`       | Compiler package, Runtime package, framework docs |
| `lowendahl/csu-iq-v2-knowledge` | OKF sources, ontology, pack-rules, compiled packs (releases) |

### 2. Two Installable Packages (from framework repo)

```
pip install akp-compiler    # Authors: compile sources → .duckdb
pip install akp-runtime     # Consumers: MCP server + query tools
```

The compiler has heavy dependencies (spacy, fastembed, networkx). The runtime is
lightweight (duckdb, mcp, bm25s).

### 3. Pack Distribution via GitHub Releases

The content repo CI compiles packs and attaches `.duckdb` files as release assets.
The runtime can fetch packs from:

1. **Local path** (simplest fallback) — just point to a `.duckdb` file on disk
2. **GitHub Release URL** — runtime downloads, verifies checksum, caches locally
3. **Auto-update** — runtime checks for newer releases on startup (optional)

Resolution chain in `config.yaml`:

```yaml
packs:
  - name: mcem
    source: github://lowendahl/csu-iq-v2-knowledge/releases/latest/mcem.duckdb
    local_cache: ~/.akp/packs/mcem.duckdb
    fallback: ./dist/mcem.duckdb
  - name: csu
    source: github://lowendahl/csu-iq-v2-knowledge/releases/latest/csu.duckdb
    local_cache: ~/.akp/packs/csu.duckdb
    fallback: ./dist/csu.duckdb
```

### 4. Simplest Fallback

For users who cannot access GitHub releases (air-gapped, offline):

```yaml
packs:
  - name: mcem
    source: file:///path/to/mcem.duckdb
```

No network calls. The runtime reads whatever is at the configured path.

## Consequences

### Positive
- Consumers install only what they need (`akp-runtime` + download packs)
- Content authors work in a focused repo without framework noise
- Independent versioning — framework v2.0 doesn't force content re-release
- Compiled packs are immutable release artifacts with checksums
- Supports air-gapped deployments via local file fallback

### Negative
- Two repos to maintain (mitigated: content repo is simpler)
- CI in content repo needs the compiler installed (mitigated: pip install)
- Breaking compiler changes require coordinated release

### Risks
- Pack format versioning: runtime must reject incompatible pack versions
  → Mitigation: pack metadata includes `compiler_version` + `pack_format_version`
- GitHub release size limits (2 GB per asset) — unlikely to hit with text-based packs
