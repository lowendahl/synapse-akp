# COM019: Validation Is Layered

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer must reject malformed or semantically unsafe changes without turning every heuristic quality concern into a hard stop. The source document therefore separates validation into layers with different responsibilities and blocking behavior.

## Decision

Apply four validation layers: contract validation with Pydantic and JSON Schema; repository validation through a custom OKF linter for IDs, references, namespaces, file layout, front matter, links and source anchors; semantic validation for domain rules such as evidence requirements, temporal metadata on supersession, metric units, policy scope and alias sanity; and quality evaluation for duplicate concepts, conflicting definitions, missing context, weak source authority, unsupported synthesis and overly broad pages. Only the first three layers are deterministic publication blockers.

## Consequences

Composer gets a clear separation between hard correctness gates and softer quality signals. Structural and semantic integrity stay enforceable in automation, while quality checks can guide review and prioritization without making the system brittle.
