# AKP Runtime — Agent Instruction Manual

## Purpose

You are connecting to the AKP (Agentic Knowledge Pack) Runtime MCP server.
It provides structured, evidence-grounded access to compiled knowledge packs.
Every answer you retrieve traces to a specific authored source — use this for
factual claims about organizational processes, metrics, and methodology.

## Connection

The runtime is an MCP server over stdio. Launch it as a subprocess:

```json
{
  "command": "python",
  "args": ["-m", "akp_runtime", "--config", "runtime/config.yaml"]
}
```

## Tools Available

### `akp_search` — Broad Discovery

Use when: the user asks a general question and you need to find relevant concepts.

```json
{"query": "delivery cost metrics", "limit": 5}
```

Returns: ranked list of objects with `object_id`, `title`, `object_type`, `snippet`.

### `akp_lookup_concept` — Specific Retrieval

Use when: you already know the concept ID or an exact alias.

```json
{"identifier": "csu.process.commit-to-complete", "include_units": true}
```

Returns: full object with semantic units (content chunks) and graph neighbors.

### `akp_explain_concept` — Human-Readable Explanation

Use when: the user needs a narrative explanation to present to stakeholders.

```json
{"query": "Job1", "detail_level": "standard"}
```

Returns: structured Markdown explanation with `cited_unit_ids` for traceability.

**Detail levels:**
- `brief` — one paragraph, definition only
- `standard` — includes formulas, thresholds, relationships (default)
- `detailed` — all available content, suitable for deep-dive reports

### `akp_expand_graph` — Relationship Traversal

Use when: you need to understand what connects to a concept.

```json
{"object_id": "csu.process.commit-to-complete", "hops": 1, "limit": 10}
```

Returns: list of edges with `predicate`, `neighbor_title`, `neighbor_type`.

### `akp_get_provenance` — Source Tracing

Use when: the user asks "where does this come from?" or you need to cite sources.

```json
{"object_id": "csu.process.commit-to-complete"}
```

Returns: provenance chain with `source_path`, `origin` (authored/derived/inferred).

## Resolution Behavior

The runtime resolves ambiguous queries using ontology-declared priority:

1. **Concepts first** (Process, Framework, Stage, Methodology, Planning, Program)
2. **Measurements second** (KPI, Metric)
3. **Evidence third** (Evidence Map, Evidence Source)

This means "Job1" resolves to the Commit-to-Complete **process** (the concept),
not the KPI that measures it. If the user explicitly asks for the KPI or
evidence, use `akp_search` with `object_types: ["KPI"]` to filter.

## Best Practices for Agents

### Always cite sources

Every `explain` result includes `cited_unit_ids`. Reference these when making
claims. Every `lookup` result includes semantic units with `heading_path` that
tells you what section the content came from.

### Use the right tool for the job

| User intent | Tool to use |
|-------------|------------|
| "What is X?" | `akp_explain_concept` with `detail_level: "standard"` |
| "Tell me everything about X" | `akp_explain_concept` with `detail_level: "detailed"` |
| "What's related to X?" | `akp_expand_graph` |
| "Find things about topic Y" | `akp_search` |
| "Where does this come from?" | `akp_get_provenance` |
| "Show me the KPI for X" | `akp_search` with `object_types: ["KPI"]` |

### Compose multi-faceted answers

For complex questions, chain tools:
1. `akp_explain_concept` → get the concept explanation
2. `akp_expand_graph` → find measurements and evidence connected to it
3. `akp_lookup_concept` on neighbors → get detail on related items

### Handle "not found" gracefully

If a tool returns `{"error": "No concept found for: X"}`:
- Try alternative aliases (acronyms, full names)
- Use `akp_search` for broader matching
- Tell the user the knowledge pack doesn't contain information on that topic

### Respect limits

- Query length: max 500 characters
- Results: max 50 per search
- Graph hops: max 3
- Don't loop — if you don't find it in 2-3 calls, it's not in the pack

## Object Types in the Knowledge Graph

| Type | Resolution Role | Description |
|------|----------------|-------------|
| Process | concept | Operational workflows and motions |
| Framework | concept | Structural/governance frameworks |
| Stage | concept | Lifecycle stages (MCEM stages) |
| Methodology | concept | Named methodologies |
| Planning | concept | Planning artifacts and documents |
| Program | concept | Organizational programs |
| KPI | measurement | Key performance indicators |
| Metric | measurement | Quantitative measures |
| Evidence Map | evidence | Data source mapping |
| Evidence Source | evidence | Raw data sources |
| Doctrine | concept | Organizational principles |
| Strategy | concept | Strategic directions |

## Common Predicates (Edge Types)

| Predicate | Meaning |
|-----------|---------|
| `measures` | KPI measures an outcome/process |
| `informs` | Object provides input to another |
| `enables` | Object is prerequisite for another |
| `contains` | Parent-child containment |
| `precedes` | Temporal ordering |
| `references` | Cites or mentions another object |

## Error Codes

| Error | Meaning | Action |
|-------|---------|--------|
| "Query too long" | Input exceeded 500 chars | Shorten the query |
| "No concept found" | Alias/ID doesn't resolve | Try alternative names or search broadly |
| "Provide exactly one target" | Provenance needs one target type | Pass only object_id OR unit_id OR edge fields |

## Security Constraints

- The runtime is **read-only** — you cannot modify knowledge packs
- No PII should appear in results (enforced at compile time)
- Query content is not logged — user privacy is preserved
- All results are grounded in authored sources — never hallucinate from pack data
