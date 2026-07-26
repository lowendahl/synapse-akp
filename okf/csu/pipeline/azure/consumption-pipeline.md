---
type: Operating Model
title: Azure Consumption Pipeline
id: csu.pipeline.azure-consumption-pipeline
description: The MCEM operating model for creating, qualifying, committing, executing, and measuring Azure consumption opportunities and milestones.
tags: [csu, pipeline, azure, consumption, mcem, operating-model]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-1-listen-consult
  - predicate: operationalizes
    object: mcem.stage.stage-2-inspire-design
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
  - predicate: operationalizes
    object: mcem.planning.consumption-planning
  - predicate: contains
    object: csu.pipeline.azure-consumption-opportunity
  - predicate: contains
    object: csu.pipeline.azure-consumption-milestone
  - predicate: measured_by
    object: csu.pipeline.azure-pipeline-metrics
  - predicate: governed_by
    object: csu.pipeline.pipeline-hygiene
  - predicate: references
    object: csu.pipeline.two-motion-model
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The Azure Consumption Pipeline is the MCEM operating model that defines how Azure consumption opportunities and milestones are created, qualified, committed, executed, completed, and measured across the full lifecycle.

# Concept Chain

```
Customer Priority → Opportunity → Milestone(s) → Customer Commitment → Committed Pipeline → PBO → Forecast / ACR Execution
```

# Ownership Transitions

| MCEM Stage | Accountable Org | Pipeline Status |
|------------|-----------------|-----------------|
| Stage 1 | ATU | Unqualified / Non-qualified production |
| Stage 2 | STU/DES | Qualified |
| Stage 3–5 | CSU | Committed → Executing → Completed |

# Key Governance

- How opportunities move through [MCEM stages](/mcem/stages/)
- How milestones are categorized and committed
- How MACC execution and consumption planning are governed
- How forecasting and escalation are managed
- How accountability transitions via [handoffs](/csu/processes/)

# Related Concepts

- [Usage Pipeline](/csu/pipeline/usage/two-motion-model.md) — the parallel model for usage/adoption
- [Consumption Planning](/csu/planning/consumption-planning.md) — planning framework for MACC execution
- [Pipeline Metrics](/csu/pipeline/azure/pipeline-metrics.md) — measurement and governance

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — opportunity and milestone pipeline records, status, value, and ownership for Azure consumption work.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
