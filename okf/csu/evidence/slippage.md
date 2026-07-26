---
type: Risk Signal
title: Slippage
id: csu.evidence.slippage
aliases: [slippage, slip, slipped, slippage column]
description: Revenue-negative deviation on snapshot milestones — committed value that fails to close on time, reducing NNR from the expected baseline.
tags: [csu, risk, slippage, pipeline, c2c, snapshot, lagging]
relationships:
  - predicate: causal_signal
    object: csu.metric.job-1-commit-to-complete-c2c
  - predicate: causal_signal
    object: csu.metric.nnr-net-new-revenue-ecif-yield
  - predicate: references
    object: csu.evidence.snapshot-vs-real-time-measurement
classification: lagging
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
sources:
  - id: msxi-completed-pipeline
    resource: "MSX Insights — Total Completed Pipeline_OneAMP"
    title: MSX Insights Total Completed Pipeline
    last_modified: 2026-07-01
---
# Definition

**Slippage** is the revenue-negative deviation on [snapshot](/csu/evidence/snapshot-vs-realtime.md) milestones — committed value that fails to close within its due date, slips to a future quarter, or closes at a lower value than committed.

**Classification: LAGGING** — measures execution failure after the commitment window.

# Mechanics

```
Slippage = Σ (Committed Value at Snapshot − Actual Closed Value) for missed/delayed milestones
```

Slippage only applies to the **C2C snapshot population** (milestones committed on or before the 5th of month-1). Post-snapshot milestones cannot slip because they were never in the denominator.

# Types of Slippage

| Type | What Happened |
|------|--------------|
| **Date slip** | Milestone misses its due date; closes in a future quarter |
| **Value slip** | Milestone closes on time but at lower ACR than committed |
| **Cancellation** | Milestone from snapshot is cancelled entirely |

# Impact

- Reduces [C2C](/csu/metrics/job1-commit-to-complete.md) numerator directly
- Reduces NNR from Path 1 (snapshot milestones at baseline value)
- May be compensated by [Pull-Forward](/csu/evidence/pull-forward.md) or post-snapshot net-new (Paths 2–3)
- Persistent slippage signals systemic execution failure

# Investigation Path

1. **Identify:** Which milestones from the snapshot have slipped? → `factazureconsumptionpipelinec2csnapshots` filtered to non-closed
2. **Root cause:** Why? → Check milestone status (At Risk / Blocked), status reason, help needed fields
3. **Pattern:** Is slippage concentrated in specific accounts, solution areas, or CSAs?
4. **Intervention:** What can be recovered before quarter-end?

# Evidence Sources

| Source | What It Shows | Access |
|--------|--------------|--------|
| **MSX Insights — Total Completed Pipeline** | Snapshot vs actual close status per milestone | PBI artifact `ba0a24fe-f7e8-4210-850c-f9d961140fea` |
| **Key table** | `factazureconsumptionpipelinec2csnapshots` | Snapshot population with committed values |
| **Key measures** | `[Completed Pipeline_MTD]`, slippage derived from snapshot delta | DAX against the semantic model |
| **MSX Dataverse** | Real-time milestone status, due dates, close reasons | MSX API / msx_mcp_server |
