---
type: ADR
title: "ADR-009 — V1 Compiler Scope and Dependency Stack"
id: adr.009
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, compiler, v1, scope, dependencies, retrieval]
---

# ADR-009 — V1 Compiler Scope and Dependency Stack

## Status

**Accepted** — 2026-07-25

## Context

The Knowledge Pack SDD defines what a compiled pack must contain (§22 — Minimum Definition of Done). The prior conversation established a 10-stage retrieval architecture as the target for precision context assembly. The question is: what does the **V1 compiler** produce, and what is deferred?

The design principle is: **the pack contains everything needed for stages 1–6 of the retrieval pipeline**. Stages 7–10 (fusion, reranking, diversity, evidence-pack assembly) are runtime logic that consumes the pack.

## Decision

### V1 Compiler Pipeline

```
OKF Markdown + YAML frontmatter
        ↓
  markdown-it-py + ruamel-yaml        [Parse]
        ↓
  Pydantic v2 domain objects          [Type, validate, assign stable IDs]
        ↓
  spaCy + rapidfuzz                   [Deterministic enrichment: aliases, acronyms, entities]
        ↓
  NetworkX DiGraph                    [Graph build + validation + scoring]
        ↓
  ┌─────────────────────────────────────────────────┐
  │  Compiled Projections (DuckDB + USearch):       │
  │                                                  │
  │  1. Canonical objects   (typed metadata, provenance)  │
  │  2. Graph projection    (nodes, edges, PageRank)      │
  │  3. Alias registry      (exact + fuzzy match index)   │
  │  4. Lexical projection  (BM25 via bm25s)             │
  │  5. Semantic units      (meaning-aligned chunks)      │
  │  6. Dense vectors       (fastembed, contextualized)   │
  │  7. Manifest            (hashes, versions, inventory) │
  └─────────────────────────────────────────────────┘
        ↓
  Immutable Knowledge Pack (kp-mcem.duckdb + .usearch | kp-csu.duckdb + .usearch)
```

### V1 Produces These Retrieval Layers

| Retrieval Stage | Pack Content | Library |
|-----------------|-------------|---------|
| 1. Exact identity + aliases | Alias registry table | rapidfuzz |
| 2. Lexical retrieval | BM25 index (terms, aliases, headings) | bm25s |
| 3. *(deferred)* | — | — |
| 4. Dense semantic retrieval | Contextualized vectors + ANN index | fastembed + usearch |
| 5. Graph expansion | Node/edge tables + pre-computed metrics | networkx → duckdb |
| 6. Metadata filtering | Canonical object table (domain, type, status, authority) | duckdb |

### V1 Deterministic Enrichment (spaCy + rapidfuzz)

| Enrichment | What It Produces |
|------------|-----------------|
| Alias expansion | "C2C" → "Commit to Complete" → "Job 1 C2C" |
| Acronym registry | All acronym↔expansion pairs from corpus |
| Entity extraction | Organization names, system names, metric names |
| Fuzzy dedup detection | Flag near-duplicate concepts (build warning) |
| Term normalization | Canonical forms for matching |

### V1 Embedding Strategy

- **Model:** FastEmbed default (likely BGE-small-en-v1.5 or similar — benchmarked in V2)
- **Encoding:** Asymmetric (separate query/passage modes)
- **Contextualization:** Each semantic unit embedded with prepended context:
  ```
  Domain: {domain}
  Type: {object_type}
  Document: {title}
  Section: {heading_path}
  Concepts: {related_concepts}

  {source_text}
  ```
- **Index:** USearch (single-file ANN, cosine distance)
- **Lineage:** Every vector carries model ID, version, input hash, context policy

### V1 Graph Validation (Compiler Diagnostics)

| Check | Severity | NetworkX Method |
|-------|----------|-----------------|
| Orphan nodes (no edges) | Warning | `nx.isolates(G)` |
| Cycles in acyclic predicates | Error | `nx.simple_cycles(G)` |
| Disconnected components | Warning | `nx.connected_components(G.to_undirected())` |
| Dangling cross-pack refs | Error | ID lookup against manifest |
| Missing required predicates | Error | Custom validator |
| Duplicate IDs | Error | Set collision check |

### V1 Dependencies

```toml
[project]
name = "kp-compiler"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "markdown-it-py>=3.0",
    "ruamel.yaml>=0.18",
    "spacy>=3.7",
    "rapidfuzz>=3.0",
    "networkx>=3.0",
    "fastembed>=0.3",
    "bm25s>=0.2",
    "usearch>=2.0",
    "duckdb>=1.0",
    "orjson>=3.9",
    "numpy>=1.26",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "hypothesis>=6.0"]
```

**Constraints:**
- No PyTorch (saves ~2GB; CPU-only runtime)
- No CUDA dependency
- Windows-native (all deps have wheels)
- ~12 direct dependencies

## What V1 Does NOT Include

| Capability | Reason for Deferral | Target |
|------------|--------------------|---------| 
| Learned sparse retrieval (SPLADE) | Needs benchmark vs BM25 uplift | V2 |
| Cross-encoder reranking | Runtime concern, not pack content | V2 runtime |
| ColBERT/late interaction | Advanced; evaluate after baseline | V2+ |
| LLM-based enrichment | Needs governance policy (KP-07) | V2 |
| PyG / Node2Vec | PyTorch dep; needs benchmark proof | V2 research |
| Clustering / taxonomy analysis | Analytical tool, not pack content | V2 tooling |
| Duplicate/contradiction detection | Corpus is human-curated; low risk | V2 |
| Evaluation harness | Needs 50 curated test queries | Post-V1 |
| Result fusion / RRF | Runtime logic, not compilation | Runtime |
| Evidence-pack assembly | Runtime planner concern | Runtime |

## Consequences

- V1 pack enables stages 1, 2, 4, 5, 6 of the 10-stage retrieval pipeline.
- Stage 3 (learned sparse) is the most impactful V2 addition — SPLADE handles CSU acronym density.
- Stages 7–10 are runtime decisions — the pack is neutral on how consumers fuse/rank/assemble.
- No PyTorch means fast CI, small Docker images, and easy Windows development.
- The evaluation harness (post-V1) drives all V2 decisions with data, not guesswork.

## V2 Research Track (Requires Benchmark First)

```
V2 retrieval additions:
  + sentence-transformers (SPLADE sparse + cross-encoder reranking)
  + tantivy (high-perf lexical if bm25s bottlenecks)

V2 graph-learning additions:
  + torch + torch-geometric (Node2Vec, TransE, link prediction)

V2 analysis tooling:
  + datasketch (MinHash dedup at scale)
  + umap-learn + hdbscan (corpus clustering)
  + ranx + ir-measures (evaluation harness)
```

All V2 decisions gated on benchmark results from the live V1 pack.
