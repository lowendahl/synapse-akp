---
type: Metric
title: Commit-to-Complete Rate
id: mcem.metric.commit-to-complete-rate
description: The percentage of committed milestones that reach completion within their committed timeframe.
tags: [mcem, metric, lagging, execution, completion]
relationships:
  - predicate: measures
    object: mcem.stage.stage-3-empower-achieve
  - predicate: measures
    object: mcem.stage.stage-4-realize-value
  - predicate: measures
    object: csu.process.commit-to-complete
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

Commit-to-Complete (C2C) Rate measures the percentage of committed milestones that CSU drives to completion. It is the primary execution effectiveness metric for CSU's MCEM accountability.

# Target

| Metric | Target | Type |
|--------|--------|------|
| C2C Rate | 95% | Lagging |

# Calculation

```
C2C Rate = (Completed Committed Milestones / Total Committed Milestones) × 100
```

# Scope

Applies to both:
- [Azure Consumption Pipeline](/csu/pipeline/azure/consumption-pipeline.md) — committed production milestones
- [Usage Pipeline](/csu/pipeline/usage/two-motion-model.md) — committed usage intent milestones

# Governance

C2C is the defining accountability metric for CSU in MCEM. It is reviewed weekly in operating rhythms and is a primary input to [Customer Health](/mcem/metrics/customer-health.md).

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | `[Completed Pipeline_MTD]` / committed milestones |

**Distinction from CSU Job 1 C2C:** This MCEM metric measures the general pipeline velocity (committed → completed conversion rate) across all opportunities. CSU's [Job 1 C2C](/csu/metrics/job1-commit-to-complete.md) specifically uses the quarterly snapshot-locked denominator.