# Implementation Plan: Explain Operation

| Field | Value |
|-------|-------|
| **PBI/Epic** | ADR-038 Explain Operation |
| **ADR** | ADR-038 |
| **Components** | Explain Concept |
| **Date** | 2026-07-27 |

## Summary

This plan implements the Explain Concept operation by creating a new operation
module, a `SemanticReasoningClient` protocol extension, domain models for
the explain output, and wiring into the MCP server. The work is sequenced so
each phase turns a specific subset of the 21 RED tests GREEN.

## Prerequisites

- ADR-038 accepted ✓
- Component spec (`docs/components/explain.md`) reviewed ✓
- 21 RED tests committed ✓
- Runtime installs cleanly (`pip install -e ".[dev]"`) ✓
- Existing 214 tests pass ✓

## Implementation Phases

### Phase 1 — Domain Models and Contracts

**Goal:** Define the output data model and protocol extension so subsequent
phases have types to work against.

**Files to create:**
- `runtime/src/akp_runtime/domain/explain_models.py` — frozen dataclasses:
  `ExplainResult` (concept_title, explanation, cited_unit_ids,
  synthesis_method, fallback_reason, detail_level, neighbor_titles) and
  `SynthesisResult` (prose, cited_unit_ids, confidence)

**Files to modify:**
- `runtime/src/akp_runtime/contracts/protocols.py` — add
  `SemanticReasoningClient` protocol with `synthesize_explanation()` method
- `runtime/src/akp_runtime/domain/models.py` — add re-exports for
  `ExplainResult` and `SynthesisResult`

**Key decisions:**
- `ExplainResult` is a frozen dataclass (matches existing patterns in
  `search_results.py`)
- `SemanticReasoningClient` is `@runtime_checkable` with a single method
- `reasoning_client` parameter is typed `SemanticReasoningClient | None`

**Tests turned GREEN:**
- `test_inv_exp_002_constructor_accepts_protocol_types` (partially — needs
  Phase 2 for full pass, but types will exist)

### Phase 2 — Core Operation Logic

**Goal:** Implement `ExplainConceptOperation` with concept resolution,
unit filtering by detail level, and structured fallback assembly.

**Files to create:**
- `runtime/src/akp_runtime/operations/explain_concept.py` — the operation
  class with `__init__(pack, reasoning_client)` and
  `explain(query, detail_level) -> ExplainResult | None`

**Key decisions:**
- Concept resolution: try `pack.lookup_concept(query)` first, then
  `pack.exact_matches(query, limit=1)` as alias fallback (same pattern as
  `ConceptLookupOperation`)
- Detail level filtering logic:
  - `brief`: include units where heading_path contains "Definition" or
    "Summary" (case-insensitive)
  - `standard`: brief + "Formula", "Threshold", "Relationship", "Context"
  - `detailed`: all units (no filtering)
- Structured fallback: Markdown document with `# {title}` heading, then
  `## {heading_path}` + content for each included unit, then
  `## Related Concepts` with neighbor titles
- `cited_unit_ids` = list of unit_ids for all included units
- `neighbor_titles` extracted from `graph_neighbors()` results

**Tests turned GREEN:**
- `test_p_exp_001_returns_explanation_with_title`
- `test_p_exp_001_returns_at_least_one_cited_unit`
- `test_p_exp_002_produces_markdown_without_reasoning_client`
- `test_p_exp_002_fallback_includes_semantic_unit_content`
- `test_p_exp_004_no_client_includes_reason`
- `test_p_exp_005_brief_includes_definition_only`
- `test_p_exp_005_standard_includes_formula_and_thresholds`
- `test_p_exp_005_detailed_includes_all_units`
- `test_p_exp_006_fallback_reports_structured_fallback`
- `test_p_exp_007_returns_none_for_unknown_concept`
- `test_p_exp_008_explanation_includes_neighbor_titles`
- `test_p_exp_008_raw_object_ids_not_in_explanation`
- `test_inv_exp_001_no_mutating_calls_on_pack`
- `test_inv_exp_002_constructor_accepts_protocol_types`
- `test_inv_exp_003_cited_ids_match_pack_units`
- `test_inv_exp_004_fallback_with_all_units`
- `test_inv_exp_004_fallback_with_empty_units`

### Phase 3 — LLM Synthesis Path

**Goal:** Add the LLM delegation branch that tries `reasoning_client`
before falling back, with diagnostic reasons on failure.

**Files to modify:**
- `runtime/src/akp_runtime/operations/explain_concept.py` — add
  `_attempt_synthesis()` private method that calls
  `reasoning_client.synthesize_explanation()`, catches
  `NotImplementedError` and general `Exception`, returns
  `(SynthesisResult | None, fallback_reason | None)`

**Key decisions:**
- `NotImplementedError` → fallback_reason = "reasoning client declined: {msg}"
- `RuntimeError` / other exceptions → fallback_reason =
  "reasoning client error: {msg}"
- `None` reasoning_client → fallback_reason =
  "no reasoning client configured"
- On successful synthesis, `cited_unit_ids` from the LLM are validated
  against pack units (INV-EXP-003); invalid IDs are dropped

**Tests turned GREEN:**
- `test_p_exp_003_uses_llm_when_client_succeeds`
- `test_p_exp_004_falls_back_on_runtime_error`
- `test_p_exp_004_falls_back_on_not_implemented`
- `test_p_exp_006_llm_reports_llm`

### Phase 4 — MCP Integration (Optional, post-gate)

**Goal:** Wire `ExplainConceptOperation` into the MCP server as the
`explain_concept` tool.

**Files to modify:**
- `runtime/src/akp_runtime/consumer/mcp_server.py` — add `explain_concept`
  tool handler
- `runtime/src/akp_runtime/contracts/` — add `ExplainConceptToolInput` and
  `ExplainConceptToolOutput` MCP models

**Key decisions:**
- Input model: `query` (str, required), `detail_level` (enum:
  brief/standard/detailed, default: standard)
- Output model maps 1:1 from `ExplainResult` fields
- This phase is outside the current RED test scope (no MCP integration
  tests yet) — it can land as a follow-up PBI

## Contract Mapping

| Component Promise | Test | Implementation Location |
|-------------------|------|------------------------|
| P-EXP-001 | test_p_exp_001_* (2) | explain_concept.py: `explain()` |
| P-EXP-002 | test_p_exp_002_* (2) | explain_concept.py: `_build_fallback()` |
| P-EXP-003 | test_p_exp_003_* (1) | explain_concept.py: `_attempt_synthesis()` |
| P-EXP-004 | test_p_exp_004_* (3) | explain_concept.py: `_attempt_synthesis()` |
| P-EXP-005 | test_p_exp_005_* (3) | explain_concept.py: `_filter_units()` |
| P-EXP-006 | test_p_exp_006_* (2) | explain_concept.py: `explain()` |
| P-EXP-007 | test_p_exp_007_* (1) | explain_concept.py: `_resolve_concept()` |
| P-EXP-008 | test_p_exp_008_* (2) | explain_concept.py: `_build_fallback()` |
| INV-EXP-001 | test_inv_exp_001 | explain_concept.py (all methods) |
| INV-EXP-002 | test_inv_exp_002 | explain_concept.py: `__init__()` |
| INV-EXP-003 | test_inv_exp_003 | explain_concept.py: `explain()` |
| INV-EXP-004 | test_inv_exp_004_* (2) | explain_concept.py: `_build_fallback()` |

## Code Standards Compliance

- [x] All new files <200 LoC (explain_concept.py estimated ~120, explain_models.py ~30)
- [x] All new modules define at least one class
- [x] No SQL in operation files (SQL stays in persistence/)
- [x] SemanticReasoningClient implements a protocol
- [x] No abbreviations in public identifiers
- [x] Type annotations on all public functions
- [x] Ruff lint and format pass

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Detail level filtering too coarse (heading_path matching) | Some units miscategorized | Use case-insensitive substring match; add "Description" to brief; document the mapping |
| LLM returns cited_unit_ids that don't exist in pack | INV-EXP-003 violated | Validate LLM citations against actual pack units; drop invalid IDs |
| Structured fallback Markdown is ugly for concepts with many units | Poor UX for detailed level | Limit to first 10 units in fallback; add "..." truncation note |
| explain_concept.py exceeds 200 LoC | Design gate violation | Extract `_build_fallback()` into separate module if needed |

## Verification

After implementation, verify:
- [ ] All 21 RED tests turn GREEN
- [ ] No existing 214 tests break
- [ ] Ruff lint passes (`ruff check src/ tests/`)
- [ ] Ruff format passes (`ruff format --check src/ tests/`)
- [ ] Architecture gate tests pass (`pytest tests/test_architecture.py`)
- [ ] Design gate tests pass (`pytest tests/test_design_gates.py`)
