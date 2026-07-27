# AKP Runtime — Human Instruction Manual

## What is AKP Runtime?

AKP Runtime is an MCP (Model Context Protocol) server that gives you
structured access to compiled knowledge packs. Think of it as a search engine
for your organization's curated knowledge — every answer traces back to a
specific source document.

## Installation

```bash
cd runtime
pip install -e ".[dev]"
```

## Configuration

Create a `config.yaml` (or use the provided one in `runtime/config.yaml`):

```yaml
server_name: akp-runtime
embeddings_enabled: false

packs:
  - pack_id: mcem
    path: ../dist/mcem.duckdb
    required: true
  - pack_id: csu
    path: ../dist/csu.duckdb
    required: true
```

Paths are relative to the config file location.

## Running the Server

```bash
# From the runtime/ directory
python -m akp_runtime --config config.yaml

# Or with debug logging
python -m akp_runtime --config config.yaml --log-level DEBUG
```

The server communicates over **stdio** (stdin/stdout). It's designed to be
launched as a subprocess by an MCP-compatible client (GitHub Copilot, Claude
Desktop, CSU-IQ, etc.).

## Compiling Knowledge Packs First

Before the runtime can serve queries, you need compiled packs:

```bash
cd compiler
pip install -e .

# Delete old packs for a clean build
rm -f ../dist/mcem.duckdb ../dist/csu.duckdb

# Compile MCEM (no dependencies)
python -m kp_compiler.cli ../okf/mcem --skip-embeddings --output ../dist/mcem.duckdb

# Compile CSU (depends on MCEM for cross-pack references)
python -m kp_compiler.cli ../okf/csu --skip-embeddings --output ../dist/csu.duckdb --dependency ../dist/mcem.duckdb
```

## Available Tools

Once the MCP server is running, these tools are exposed to any connected client:

### `akp_search`

Search across all loaded packs with a natural-language query.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | string | required | What to search for |
| limit | int | 10 | Max results (1-50) |
| pack_ids | list[str] | [] | Filter to specific packs |
| object_types | list[str] | [] | Filter to types (Process, KPI, etc.) |

### `akp_lookup_concept`

Look up a specific concept by its ID or alias.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| identifier | string | required | Object ID or alias (e.g., "Job1", "csu.process.commit-to-complete") |
| include_units | bool | true | Include semantic units (content chunks) |
| include_neighbors | bool | true | Include graph relationships |
| neighbor_limit | int | 10 | Max neighbors to return (1-50) |

### `akp_explain_concept`

Get a human-readable explanation of a concept, structured like a professional
report.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | string | required | Concept name or alias |
| detail_level | string | "standard" | "brief", "standard", or "detailed" |

Detail levels:
- **brief** — Definition and summary only
- **standard** — Adds formulas, thresholds, key relationships
- **detailed** — Everything available

### `akp_expand_graph`

Traverse the knowledge graph from a starting point.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| object_id | string | required | Starting node ID |
| hops | int | 1 | How far to traverse (1-3) |
| predicates | list[str] | [] | Filter edge types (e.g., "measures", "informs") |
| limit | int | 20 | Max edges to return (1-100) |

### `akp_get_provenance`

Trace any piece of knowledge back to its source. Exactly one target must be provided:

| Parameter | Type | Description |
|-----------|------|-------------|
| object_id | string | Trace an object |
| unit_id | string | Trace a semantic unit |
| edge_subject_id + edge_predicate + edge_object_id | strings | Trace a graph edge |

## Concept Resolution

When you search for an alias like "Job1", the runtime resolves it using this
priority system:

1. **Resolution role** — concepts (Process, Framework, Stage) rank above
   measurements (KPI, Metric), which rank above evidence (Evidence Map)
2. **Alias source** — author-declared aliases (from frontmatter) beat
   enrichment-derived aliases
3. **Title proximity** — exact title matches rank highest
4. **Alphabetical** — final tie-breaker

This means asking about "Job1" gives you the Commit-to-Complete process (the
concept), not the KPI that measures it.

## MCP Client Configuration

### GitHub Copilot (`.github/copilot-instructions.md`)

```markdown
When the user asks about CSU processes, metrics, or methodology, use the
akp-runtime MCP server to retrieve grounded answers with citations.
```

### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "akp-runtime": {
      "command": "python",
      "args": ["-m", "akp_runtime", "--config", "/path/to/config.yaml"]
    }
  }
}
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "No packs loaded" | Pack files missing or wrong path | Check config.yaml paths, recompile if needed |
| "Required pack not found" | .duckdb file doesn't exist | Run the compiler first |
| Stale results after source edits | Old .duckdb file | Delete and recompile |
| "Query too long" | Input exceeds 500 chars | Shorten your query |

## Security Notes

- Packs are opened **read-only** — queries cannot modify knowledge
- All queries use parameterized SQL — no injection possible
- No query content is logged at INFO level
- See `SECURITY.md` for the full threat model
