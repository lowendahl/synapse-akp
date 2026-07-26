# Component: Hybrid Search (Scoring & Fusion)

## Modules

- `akp_runtime.domain.scoring` — Pure scoring functions (RRF, graph boost, stable sort)
- `akp_runtime.operations.search` — HybridSearchOperation orchestrator

## Purpose

Fuse multiple ranked retrieval channels (exact, lexical, semantic) into a single
deterministic result set using Reciprocal Rank Fusion (RRF) with optional
graph-proximity boosting.

## Responsibilities

### `domain/scoring.py` (Pure Functions)

1. **RRF Fusion** — merge N ranked lists using `score = Σ 1/(k + rank)` per hit.
2. **Deduplication** — hits appearing in multiple channels are merged (scores summed).
3. **Graph Boost** — increase scores of hits whose objects are 1-hop graph neighbors
   of the top-N results.
4. **Stable Sort** — deterministic sort by (-score, pack_id, object_id, unit_id).

### `operations/search.py` (Orchestrator)

1. **Channel dispatch** — call exact, lexical, and semantic retrieval on loaded packs.
2. **Channel assembly** — collect results from each retrieval channel.
3. **Fusion** — pass channels through RRF.
4. **Boost** — optionally apply graph boost.
5. **Limit** — truncate to requested limit.
6. **Provenance** — ensure all results carry provenance from their source pack.

## Out of Scope

- **BM25 index construction** — that's the compiler's job.
- **Vector embedding** — delegated to `fastembed_adapter.py`.
- **Vector search** — delegated to `usearch_reader.py`.
- **Pack loading** — handled by `duckdb_loader.py`.
- **MCP transport** — handled by `consumer/mcp_server.py`.

## Promises

1. **P-FORMULA**: RRF score for a hit = `Σ 1/(rrf_k + rank_in_channel)` across
   all channels where it appears. Rank is 1-based.
2. **P-DEDUP**: A hit appearing in multiple channels appears ONCE in output with
   summed RRF contributions. Dedup key is `(pack_id, object_id, unit_id)`.
3. **P-BOOST**: Graph boost adds `boost_value` to hits whose `object_id` is a
   1-hop neighbor of any top-N result's `object_id`. Boost is additive.
4. **P-BOOST-SCOPE**: Only the top-N results (by pre-boost score) seed the
   neighbor set. Boosted hits are NOT recursively used as seeds.
5. **P-CHANNEL-INVARIANT**: RRF output is invariant to the ordering of input
   channels (i.e., `rrf_fuse([A, B]) == rrf_fuse([B, A])` after stable sort).
6. **P-MONOTONIC**: Adding a retrieval channel can only increase or preserve a
   hit's score — never decrease it.
7. **P-DETERMINISTIC**: Same inputs → same outputs. No randomness.
8. **P-EMPTY-SAFE**: Empty input channels produce empty output. No errors.

## Invariants

1. **INV-PURE**: `scoring.py` has ZERO side effects — no IO, no mutation of inputs,
   no logging that affects behavior.
2. **INV-IMMUTABLE-INPUT**: Input lists and hits are never mutated. New hits are
   created with updated scores.
3. **INV-LAYER-BOUNDARY**: `scoring.py` imports only from `domain/models.py`.
   `operations/search.py` may import from `domain/` and `contracts/` only.
4. **INV-STABLE-TIEBREAK**: When scores are equal, sort is deterministic by
   (pack_id, object_id, unit_id).

## Testing Strategy

- **Formula tests**: Verify exact RRF math for single/multi-channel scenarios.
- **Dedup tests**: Same hit in 2+ channels → single output, summed score.
- **Graph boost tests**: Verify only neighbors of top-N get boosted.
- **Property tests** (hypothesis): Channel-order invariance, monotonicity.
- **Empty/edge cases**: Empty lists, single hit, all duplicates.
