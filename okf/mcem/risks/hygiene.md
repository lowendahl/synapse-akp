---
type: Risk Indicator
title: Pipeline Hygiene
id: mcem.risk.pipeline-hygiene
description: Data quality and governance health of the MCEM pipeline across all stages.
tags: [mcem, risk, hygiene, data-quality, governance]
relationships:
  - predicate: measures
    object: mcem.metric.pipeline-stages-states
  - predicate: informs
    object: mcem.planning.consumption-planning
  - predicate: informs
    object: mcem.metric.qualified-pipeline
  - predicate: references
    object: csu.pipeline.pipeline-hygiene
  - predicate: informs
    object: csu.pipeline.pipeline-ownership-model
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

Pipeline Hygiene measures the data quality and governance health of opportunities and milestones across all MCEM stages. Poor hygiene degrades forecasting accuracy, obscures risk signals, and undermines execution accountability.

# Hygiene Dimensions

- **Stage accuracy:** Opportunity stage reflects actual customer status
- **Date currency:** Milestone dates are current and realistic
- **Owner assignment:** Clear accountable owner per stage model
- **Categorization:** Milestones properly categorized per taxonomy
- **Completion marking:** Completed milestones marked promptly

# Governance

Pipeline hygiene is reviewed weekly in CSU operating rhythms. See [Pipeline Hygiene](/csu/pipeline/azure/pipeline-hygiene.md) for specific checks.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the opportunity and milestone field completeness, status, dates, and ownership signals that drive pipeline hygiene risk.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
