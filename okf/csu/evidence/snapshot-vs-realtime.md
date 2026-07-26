---
type: Measurement Concept
title: Snapshot vs Real-Time Measurement
id: csu.evidence.snapshot-vs-real-time-measurement
aliases: [snapshot measurement, C2C snapshot, 5th-of-month-1 snapshot]
description: The two measurement paradigms in CSU — snapshot-locked denominators (C2C, Slippage, Pull-Forward) vs real-time running totals (NNR, Job 2, ACR).
tags: [csu, evidence, measurement, snapshot, real-time, methodology]
relationships:
  - predicate: references
    object: csu.metric.job-1-commit-to-complete-c2c
  - predicate: references
    object: csu.metric.nnr-net-new-revenue-ecif-yield
  - predicate: references
    object: csu.evidence.slippage
  - predicate: references
    object: csu.evidence.pull-forward
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
---
# Definition

CSU uses two fundamentally different measurement paradigms. Confusing them causes misinterpretation of metrics and incorrect root-cause analysis.

# Paradigm 1: Snapshot-Locked

A denominator is **frozen at a point in time** (the snapshot). Everything measured against that snapshot population. Post-snapshot changes are invisible to the metric.

| Attribute | Detail |
|-----------|--------|
| **Snapshot date** | 5th of the first month of the quarter |
| **What's frozen** | The set of committed milestones at that moment |
| **Metrics using this** | [Job 1 C2C](/csu/metrics/job1-commit-to-complete.md), [Slippage](/csu/evidence/slippage.md), [Pull-Forward](/csu/evidence/pull-forward.md) |
| **Post-snapshot changes** | Invisible to these metrics; flow to NNR/Job 2 instead |

**Critical implication:** A milestone committed on the 6th of month-1 will NEVER appear in C2C, Slippage, or Pull-Forward for that quarter — even if it closes beautifully.

# Paradigm 2: Real-Time Running Total

A metric counts **everything that qualifies within the window**, regardless of when it was committed or created.

| Attribute | Detail |
|-----------|--------|
| **Window** | Current quarter (or rolling period) |
| **What's counted** | All qualifying events within the window |
| **Metrics using this** | [NNR](/csu/metrics/nnr.md), [Job 2](/csu/metrics/job2-completed-created.md), ACR, [In-Quarter Create](/csu/metrics/in-quarter-create.md) |
| **Post-snapshot additions** | Fully visible and counted |

# Why This Matters

A quarter can show:

| Scenario | C2C (Snapshot) | NNR (Real-time) | Explanation |
|----------|---------------|-----------------|-------------|
| Strong execution, no new | 97% ✅ | Low ❌ | Delivered what we promised, but didn't originate new |
| Weak execution, strong new | 82% ❌ | High ✅ | Post-snapshot net-new compensated for snapshot misses |
| Both strong | 96% ✅ | High ✅ | Ideal: delivered committed AND originated new |

# Investigation Pattern

When investigating a KPI, always ask: **"Is this a snapshot metric or a real-time metric?"**

- If snapshot → the denominator was locked on the 5th; look at what was in the snapshot
- If real-time → the denominator is all qualifying events; look at flow rate

# Semantic Model Access

| Paradigm | System | Key Table |
|----------|--------|-----------|
| Snapshot | MSX Insights — Total Completed Pipeline | `factazureconsumptionpipelinec2csnapshots` |
| Real-time | MSX Insights — Total Completed Pipeline | `factazureconsumptionpipeline` |
| Monthly snapshots | MSX Insights — Total Completed Pipeline | `factazureconsumptionpipelinemonthlyc2csnapshots` |
