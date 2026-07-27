# COM007: Define the Synapse Canonical Document Model

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer needs a stable intermediate representation between document extraction and semantic interpretation. Without such a boundary, parser-specific structures leak into knowledge composition, provenance becomes inconsistent, and switching extraction providers becomes a breaking architectural change.

## Decision

Establish the Synapse canonical document model as the only accepted input to semantic composition. The model must preserve document structure before interpretation through document metadata, source version, content tree, blocks, assets, links, annotations, extraction diagnostics and provenance anchors; supported block types include headings, paragraphs, lists, tables, figures, images, code blocks, slides, notes, diagrams, charts, formulas, headers, footers, page breaks and unknown regions. Every block must carry stable IDs, ordering, source text, normalized text, page or slide anchors, bounding boxes where available, parser identity and version, extraction confidence, source hash, hierarchy metadata, asset references and security metadata.

## Consequences

The canonical model becomes the airlock between document world and knowledge world. All extractors must map into it, later AI stages can reason over a stable contract, and provenance and validation can attach consistently before any concepts, claims or policies are proposed.
