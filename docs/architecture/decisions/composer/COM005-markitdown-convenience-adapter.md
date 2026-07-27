# COM005: MarkItDown Is a Convenience Adapter

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer benefits from a lightweight way to quickly convert many file types into readable Markdown for preview, diagnostics and low-fidelity import. However, Markdown discards structural and provenance detail needed for reliable knowledge composition.

## Decision

Support Microsoft MarkItDown as a convenience adapter for rapid import, simple documents, previews, unsupported formats and human-readable diagnostics. Do not allow MarkItDown output to serve as the canonical normalized representation, provenance foundation, authoritative table extractor, sole PowerPoint interpreter or graph relationship source.

## Consequences

Developers get a fast conversion tool without redefining the architecture around lossy Markdown. Rich sources must continue through structured extraction and canonical normalization, and any Markdown-only path is explicitly non-authoritative and suitable only as a fallback or convenience view.
