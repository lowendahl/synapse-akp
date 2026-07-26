---
type: Metric
title: Qualified Pipeline
id: mcem.metric.qualified-pipeline
description: The volume and value of opportunities that have satisfied Stage 1 exit criteria and entered Stage 2.
tags: [mcem, metric, pipeline, qualification]
relationships:
  - predicate: measures
    object: mcem.stage.stage-1-listen-consult
  - predicate: measures
    object: mcem.stage.stage-2-inspire-design
  - predicate: informs
    object: mcem.stage.stage-3-empower-achieve
  - predicate: references
    object: csu.pipeline.azure-consumption-opportunity
  - predicate: informs
    object: csu.process.new-deals-motion-motion-1
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Qualified Pipeline represents opportunities that have satisfied [Stage 1](/mcem/stages/1-listen-and-consult.md) exit criteria and entered [Stage 2](/mcem/stages/2-inspire-and-design.md). These opportunities have validated outcomes, identified decision makers, and confirmed budget and timing.

# Measurement

- **Source System:** MSX Dataverse
- **Indicator Class:** Leading
- **Qualification Gate:** Discovery Questions completed, exit criteria satisfied

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` | `[Qualified Pipeline]`, `[FY QP Coverage to NNR]` |

**Recipe:** `pipeline-coverage` — shows qualified pipeline and coverage ratio to NNR target.