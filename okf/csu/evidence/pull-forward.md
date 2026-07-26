---
type: Risk Signal
title: Pull-Forward
id: csu.evidence.pull-forward
aliases: [pull-forward, PF, negative slippage, pull forward]
description: Revenue-positive acceleration on snapshot milestones — value closing earlier or larger than committed, boosting NNR above baseline.
tags: [csu, risk, pull-forward, pipeline, c2c, snapshot, diagnostic]
relationships:
  - predicate: causal_signal
    object: csu.metric.job-1-commit-to-complete-c2c
  - predicate: causal_signal
    object: csu.metric.nnr-net-new-revenue-ecif-yield
  - predicate: references
    object: csu.evidence.snapshot-vs-real-time-measurement
classification: diagnostic
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
sources:
  - id: msxi-completed-pipeline
    resource: "MSX Insights — Total Completed Pipeline_OneAMP"
    title: MSX Insights Total Completed Pipeline
    last_modified: 2026-07-01
---
# Definition

**Pull-Forward** is the revenue-positive acceleration on [snapshot](/csu/evidence/snapshot-vs-realtime.md) milestones — committed value that closes earlier than due date, or at a higher value than committed, or with an earlier estimated date, boosting NNR above the baseline.

**Classification: DIAGNOSTIC** — positive execution signal but can mask underlying pipeline health issues if over-relied upon.

# Mechanics

```
Pull-Forward = Σ (Actual Closed Value − Committed Value at Snapshot) for early/upside milestones
```

Like [Slippage](/csu/evidence/slippage.md), Pull-Forward only applies to the **C2C snapshot population**.

# Types of Pull-Forward

| Type | What Happened |
|------|--------------|
| **Date pull** | Milestone closes before its due date |
| **Value pull** | Milestone closes at higher ACR than committed |
| **Scope expansion** | Milestone scope increased after snapshot (still in population) |

# Impact

- Lifts [C2C](/csu/metrics/job1-commit-to-complete.md) numerator (early close counts as on-time)
- Boosts NNR from Path 2 (scope ↑ / earlier closure)
- **Caution:** Sustained pull-forward without matching [IQC](/csu/metrics/in-quarter-create.md) signals back-book depletion

# Evidence Sources

| Source | What It Shows | Access |
|--------|--------------|--------|
| **MSX Insights — Total Completed Pipeline** | Early closures and value upside vs snapshot baseline | PBI artifact `ba0a24fe-f7e8-4210-850c-f9d961140fea` |
| **Key table** | `factazureconsumptionpipelinec2csnapshots` | Compare snapshot committed value to actual closed value |
| **MSX Dataverse** | Milestone actual close date vs due date | MSX API |
