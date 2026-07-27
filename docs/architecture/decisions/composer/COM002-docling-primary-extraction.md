# COM002: Use Docling as the Primary Extraction Framework

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer needs one default multi-format extractor for PDF, DOCX, PPTX, HTML, images and Markdown so most documents follow a common ingestion path. The source document positions Docling as the broadest structured conversion engine because it combines layout analysis, reading order, OCR, table extraction and batch conversion.

## Decision

Adopt Docling as the default multi-format extraction provider behind the Synapse document extractor contract. Docling may produce a `DoclingDocument` inside the adapter boundary, but Composer must always translate that output into the Synapse canonical document model before any later stage consumes it.

## Consequences

Most documents can use one primary extraction path, improving consistency and operations. Composer stays decoupled from Docling internals, so Docling upgrades do not become domain migrations, provenance anchors remain stable, and alternative parsers can be introduced without rewriting downstream semantic composition.
