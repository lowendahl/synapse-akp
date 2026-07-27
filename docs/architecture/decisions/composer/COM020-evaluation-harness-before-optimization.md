# COM020: Build an Evaluation Harness Before Optimizing Models

**Status:** Draft  
**Capability:** Composer  
**Date:** 2026-07-27

## Context

Composer quality should be measured against representative sources rather than optimized around vendor reputation or anecdotal performance. Parser choice, OCR strategy and model prompting all need a stable benchmark surface before the platform starts tuning for speed or accuracy.

## Decision

Create and version a golden corpus that covers simple and complex PDFs, scanned PDFs, policy documents, DOCX with tables and tracked changes, PowerPoint with notes, diagram-heavy presentations, Markdown wikis, static and JavaScript-rendered web pages, contradictory sources and updated versions of existing sources. Measure extraction quality through block recall, reading order, heading hierarchy, table correctness, image association and citation-anchor accuracy; measure interpretation through knowledge-type precision, evidence-link precision, unsupported inference rate, concept-resolution accuracy and contradiction detection; and measure composition through human acceptance rate, correction rate, time to publish, unnecessary review count, knowledge duplication and AKP retrieval quality. Use those results to choose parsers and models rather than fixed vendor preference.

## Consequences

Optimization work becomes evidence driven and repeatable. Regression testing can compare extraction providers and model versions over time, and the evaluation harness becomes the governing input to parser routing, model selection and scaling decisions.
