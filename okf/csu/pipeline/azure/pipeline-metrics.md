---
type: Metric Collection
title: Azure Pipeline Metrics
id: csu.pipeline.azure-pipeline-metrics
description: Key health and execution metrics governing the Azure Consumption Pipeline.
tags: [csu, pipeline, azure, metrics, governance]
relationships:
  - predicate: informs
    object: mcem.metric.qualified-pipeline
  - predicate: informs
    object: mcem.metric.committed-pipeline
  - predicate: informs
    object: mcem.metric.days-in-stage
  - predicate: informs
    object: mcem.metric.exit-conformance
  - predicate: measures
    object: csu.pipeline.azure-consumption-pipeline
  - predicate: uses_evidence
    object: csu.evidence.msx-dataverse-crm
  - predicate: uses_evidence
    object: csu.evidence.msx-insights-msxi-analytics-measurement
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| [Pipeline Coverage Index](/mcem/metrics/pipeline-coverage-index.md) | Leading | 3× ACR target coverage |
| [Commit-to-Complete Rate](/mcem/metrics/commit-to-complete-rate.md) | Lagging | % committed milestones completed |
| ACR (Azure Consumed Revenue) | Lagging | Actual consumption revenue |
| In-Quarter Create | Leading | Pipeline created within current quarter |
| NNR (Net New Revenue) | Lagging | Net new Azure consumption |

# Governance Rhythm

Pipeline metrics are reviewed:
- **Weekly:** Milestone execution status, at-risk identification
- **Monthly:** Pipeline coverage, ACR trajectory, C2C rates
- **Quarterly:** Strategic pipeline health, forecast accuracy

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the underlying opportunity and milestone statuses, dates, and values used to compute pipeline KPIs.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
