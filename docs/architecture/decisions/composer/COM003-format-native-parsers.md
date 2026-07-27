# COM003: Use Format-Native Parsers for Fidelity

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Docling provides broad coverage, but some source semantics are only recoverable through format-native tooling. DOCX documents may encode meaning in styles, comments, tracked changes or content controls; PPTX files may depend on slide shapes, notes and layout; PDFs often require page coordinates, annotations or forensic inspection.

## Decision

Keep Docling as the main path, but add format-native enrichment adapters where fidelity matters. Use `python-docx` plus direct OOXML inspection for DOCX depth, `python-pptx` plus OOXML inspection and rendering for PPTX, PyMuPDF for PDF rendering, coordinates, annotations and image extraction, and reserve LibreOffice conversion or `pypdf` for compatibility and lightweight cases only.

## Consequences

Composer must support dual extraction modes: broad default conversion and targeted fidelity enrichment. Normalization logic must merge native parser output into the canonical document model, and PowerPoint processing must treat slides as visual arguments that may require later multimodal interpretation instead of text-only flattening.
