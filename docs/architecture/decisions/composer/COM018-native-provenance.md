# COM018: Provenance Must Be Native, Not Added Afterward

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer exists to create evidence-grounded knowledge, so provenance cannot be inferred after composition has already happened. Every candidate and published object must preserve lineage across extraction, interpretation and human review boundaries.

## Decision

Capture provenance at the moment each candidate is created and at every later transformation boundary. Every candidate must reference source ID, source version, extraction run, block IDs, page or slide anchors, character or spatial span, interpretation run, prompt version, model version and human decisions. The model may align conceptually with W3C PROV, but Synapse must use its own provenance schema optimized for composition workflows.

## Consequences

Evidence lineage becomes mandatory for all publishable knowledge objects. Validation, review and later compiler steps can reason over native provenance instead of retrofitted metadata, and any knowledge without traceable evidence or authorship can be rejected systematically.
