---
type: ADR
title: "ADR-012 — V2 Compiler Scope: Retrieval Projections and Enrichment"
id: adr.012
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, compiler, v2, bm25, embeddings, enrichment, domain-events]
---

# ADR-012 — V2 Compiler Scope: Retrieval Projections and Enrichment

## Status

**Accepted** — 2026-07-25

## Context

V1 produced a working Knowledge Pack with canonical objects, graph, semantic units, aliases, and a manifest. However, the consumer CLI relied on SQL LIKE for lexical search and had no dense vector retrieval. This limits recall and precision for natural-language queries.

V2 completes the retrieval pipeline described in ADR-009 by adding the missing compilation stages:

1. **Domain event bus** — observability across pipeline stages
2. **NLP enrichment** — deterministic alias/acronym/entity expansion
3. **BM25 lexical index** — proper term-frequency retrieval via bm25s
4. **Dense embeddings** — contextualized vectors via fastembed + usearch ANN index
5. **Cross-pack validation** — CSU validates against MCEM manifest
6. **Result fusion** — Reciprocal Rank Fusion (RRF) in the consumer

## Decision

### V2 Pipeline (additions highlighted)

```
OKF Markdown + YAML frontmatter
        |
  [Parse]           (V1 — unchanged)
        |
  [Validate]        (V1 — unchanged)
        |
  [Enrich] *NEW*    spaCy + rapidfuzz: aliases, acronyms, entities, fuzzy dedup
        |
  [Graph]           (V1 — unchanged)
        |
  [Semantic Units]  (V1 — unchanged)
        |
  [BM25 Index] *NEW*   bm25s over semantic units -> DuckDB token table
        |
  [Embed] *NEW*        fastembed -> usearch ANN sidecar file
        |
  [Cross-Pack] *NEW*   Validate qualified IDs against dependency manifest
        |
  [Write Pack]      (V1 — extended with new tables)
```

### V2 New Components

| Component | What | Library | Output |
|-----------|------|---------|--------|
| EventBus | Pipeline observability | stdlib (dataclass events) | Logged events per stage |
| Enricher | Deterministic NLP | spaCy (en_core_web_sm) + rapidfuzz | Expanded aliases, entities, acronyms |
| BM25 Indexer | Term-frequency retrieval | bm25s | Token frequencies in DuckDB |
| Embedder | Dense vectors | fastembed (BAAI/bge-small-en-v1.5) | .usearch sidecar file |
| CrossPackValidator | Dependency enforcement | manifest lookup | Diagnostics for broken refs |
| RRF Fusion | Result merging | arithmetic | Fused ranking in consumer |

### V2 Embedding Strategy

- **Model:** `BAAI/bge-small-en-v1.5` via fastembed (384 dims, ~33M params, CPU-friendly)
- **Input:** Contextualized semantic units (context + content)
- **Index:** USearch HNSW (cosine metric, single .usearch file)
- **Provenance:** Every vector row carries model_name, model_version, input_hash

### V2 BM25 Strategy

- **Library:** bm25s (Scipy-backed, no Java dependency)
- **Corpus:** Semantic unit content + aliases + headings
- **Storage:** Tokenized corpus stored in DuckDB `bm25_tokens` table
- **Query:** bm25s loads from DuckDB at consumer startup

### V2 Consumer Fusion (RRF)

```
query -> [alias exact]    score=1.0 for exact matches
      -> [BM25 lexical]   bm25s.retrieve(query, k=20)
      -> [dense vector]   usearch.search(embed(query), k=20)
      -> [object match]   SQL LIKE fallback
      -> RRF fusion (k=60) -> ranked results
```

### V2 New DuckDB Tables

V2 extends the pack schema with three new tables:
- **BM25 token storage** — serialized token arrays per semantic unit for lexical retrieval
- **Vector metadata** — model name, version, dimensions, and input hash per embedded unit (vectors stored in a sidecar index file)
- **Cross-pack references** — source-to-target qualified ID mappings with resolution status

### V2 Domain Events

```python
@dataclass(frozen=True)
class ObjectParsed:
    object_id: str
    source_file: str
    timestamp: datetime

@dataclass(frozen=True)
class ValidationComplete:
    error_count: int
    warning_count: int

@dataclass(frozen=True)
class EnrichmentComplete:
    aliases_added: int
    entities_found: int
    acronyms_resolved: int

@dataclass(frozen=True)
class GraphBuilt:
    node_count: int
    edge_count: int
    orphan_count: int

@dataclass(frozen=True)
class EmbeddingComplete:
    unit_count: int
    model_name: str
    dimensions: int
    duration_seconds: float

@dataclass(frozen=True)
class PackWritten:
    pack_id: str
    path: str
    content_hash: str
```

## What V2 Does NOT Include

| Capability | Reason | Target |
|------------|--------|--------|
| SPLADE learned sparse | Needs PyTorch; benchmark first | V3 |
| Cross-encoder reranking | Runtime concern | V3 runtime |
| PyG / Node2Vec | Needs PyTorch; benchmark proof | V3 research |
| LLM-based enrichment | Needs governance policy | V3 |
| Evaluation harness | Needs 50 curated test queries | Post-V2 |

## Consequences

- V2 pack enables all 6 compilation-time retrieval stages from ADR-009
- Consumer CLI gains BM25 + vector search + RRF fusion
- No new heavy dependencies — fastembed and bm25s are both CPU-only, small
- spaCy model `en_core_web_sm` adds ~12MB but enables deterministic NLP
- .usearch sidecar file adds ~200KB per pack (384 dims * ~500 units * 4 bytes)
- Domain events provide build observability without coupling stages
