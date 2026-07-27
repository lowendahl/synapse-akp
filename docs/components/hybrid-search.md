# Component: Hybrid Search

## Purpose
Hybrid Search fuses exact, lexical, semantic, and graph-adjacent evidence into a deterministic ranked result set. It separates pure fusion mathematics from runtime orchestration so retrieval quality can evolve without leaking infrastructure concerns into scoring logic.

## Modules Covered
- `akp_runtime.domain.scoring` — Reciprocal Rank Fusion, graph proximity boosting, and deterministic sorting
- `akp_runtime.operations.search` — search-channel orchestration and MCP output mapping

## Responsibilities
- Fuse ranked channels with Reciprocal Rank Fusion
- Deduplicate hits by `(pack_id, object_id, unit_id)`
- Optionally apply one-hop graph proximity boosting from top-ranked seeds
- Fall back to object-title lookup when richer channels return nothing
- Emit runtime search results with provenance and channel metadata

## Out of Scope
- Building BM25 indexes
- Generating embeddings
- Loading packs or vector sidecars
- MCP transport registration

## Promises
- **P-SEARCH-001**: RRF uses `Σ 1 / (k + rank)` with 1-based rank positions.
- **P-SEARCH-002**: Duplicate hits across channels appear once in output with summed RRF contributions.
- **P-SEARCH-003**: Graph boost seeds come only from the pre-boost top-N results and are not recursively expanded.
- **P-SEARCH-004**: Empty ranked channels produce an empty `SearchToolOutput` rather than an exception.
- **P-SEARCH-005**: Stable ordering breaks score ties by `pack_id`, `object_id`, and `unit_id`.
- **P-SEARCH-006**: Object fallback executes only when no exact, lexical, or semantic channel produced candidates.

## Invariants
- **INV-SEARCH-001**: `akp_runtime.domain.scoring` is side-effect free and does not mutate input hits.
- **INV-SEARCH-002**: Search orchestration depends on pack and embedding protocols, not concrete adapters.
- **INV-SEARCH-003**: Score fusion remains deterministic for identical channel inputs.

## Dependencies
- `akp_runtime.domain.search_results`
- `akp_runtime.contracts.protocols`
- `akp_runtime.contracts.mcp_search`

## Dependents
- MCP `akp_search` tool surface
- Runtime consumers that require ranked retrieval
