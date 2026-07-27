# COM013: Visual Interpretation Is Separate from Text Extraction

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

For PDFs and PowerPoint especially, meaning may depend on arrows, spatial layout, colour, swim lanes, quadrants, maturity curves, architecture layers, topology or chart trends. A text parser alone cannot reliably reconstruct those semantics.

## Decision

Treat visual interpretation as a separate enrichment stage after structural extraction and rendering. The pipeline must combine structural extraction with page or slide rendering, run a visual relevance classifier, send relevant assets through multimodal interpretation, produce typed visual propositions such as diagram or layered-architecture objects, retain the original source asset, and require human review when the visual claim is material.

## Consequences

Composer avoids flattening diagrams into lossy prose and can preserve image-backed meaning explicitly. Visual semantics become first-class, inspectable artifacts linked to source imagery instead of being hidden inside generic text extraction.
