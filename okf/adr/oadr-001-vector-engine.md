---
type: ADR
title: "OADR-001 — Vector Engine Selection"
id: oadr.001
status: open
date: 2026-07-25
tags: [adr, open, vector, embedding, search]
---

# OADR-001 — Vector Engine Selection

## Status

**Open** — awaiting benchmark results

## Question

Which embedded vector index engine should store and search the vector projection?

## Candidates

| Engine | Notes |
|--------|-------|
| **FAISS** | Facebook; mature; CPU/GPU; large community; C++ with Python bindings |
| **USearch** | Unum; Rust/C++; single-file index; good Windows support; newer |
| **hnswlib** | Header-only C++; minimal; proven HNSW; no metadata storage |
| **sqlite-vec** | SQLite extension; single-file with metadata; young; limited ANN |
| **LanceDB** | Embedded columnar vector DB; Rust; growing; disk-native |

## Evaluation Criteria

- In-process operation (no server)
- CPU performance on ~5,000–20,000 vectors (our corpus scale)
- Windows packaging (native DLL or pure-Python fallback)
- Metadata linkage to DuckDB canonical IDs
- Index portability (single-file preferred)
- Incremental update support
- Licensing (permissive)
- Integration with Python ecosystem

## Dependencies

- ADR-003 (DuckDB stores metadata; vector engine stores only embeddings + ID references)
- OADR-002 (embedding model selection determines dimensionality)

## Resolution Criteria

Benchmark on the actual compiled CSU corpus using the selected embedding model. Measure:
- Recall@10 on a curated test set of 50 queries
- Index build time
- Query latency (p50, p95)
- File size
- Windows build complexity
