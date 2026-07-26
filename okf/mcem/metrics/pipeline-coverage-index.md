---
type: Metric
title: Pipeline Coverage Index (PCI)
id: mcem.metric.pipeline-coverage-index-pci
description: Leading indicator measuring pipeline coverage as a multiple of the FY ACR target.
tags: [mcem, metric, leading, pipeline, coverage]
relationships:
  - predicate: measures
    object: mcem.planning.consumption-planning
  - predicate: measures
    object: mcem.planning.macc-consumption-planning
  - predicate: informs
    object: mcem.planning.quarterly-business-review-qbr
  - predicate: references
    object: csu.pipeline.azure-consumption-pipeline
  - predicate: measures
    object: csu.metric.nnr-net-new-revenue-ecif-yield
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Pipeline Coverage Index (PCI) measures the ratio of total qualified pipeline value to the rolling 12-month (R12M) ACR target. It is the primary leading indicator for MCEM pipeline health.

# Target

| Metric | Target | Governance Level |
|--------|--------|-----------------|
| PCI | 300% (3× FY ACR target) | G-03 |

# Indicator Classification

- **Class:** Leading
- **Frequency:** Weekly
- **Source Systems:** MSX Dataverse

# Interpretation

- PCI < 200%: Critical pipeline gap — immediate pipeline generation action required
- PCI 200–300%: Attention — pipeline may not cover expected close rates
- PCI ≥ 300%: Healthy — sufficient coverage to absorb normal pipeline attrition

# Relationship to MCEM

PCI is driven by Stage 1 (pipeline creation) and Stage 2 (qualification) effectiveness. Low PCI indicates insufficient [Stage 1](/mcem/stages/1-listen-and-consult.md) activity or poor qualification rates.

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` | `[FY QP Coverage to NNR]`, `[MSX Consumption Plan Attach %]` |

**Recipe:** `pipeline-coverage` — per-TPID qualified/committed/uncommitted pipeline vs NNR requirement.