---
type: KPI
title: "Job 2 — Total Completed Created (CSU-Originated)"
id: csu.metric.job-2-total-completed-created-csu-originated
description: Quarterly completed pipeline originated by CSU as % of Net New $ Required. Target ≥20%. Anchored on completion date.
tags: [csu, kpi, job2, pipeline, origination, consumption, lagging]
relationships:
  - predicate: measures
    object: csu.process.new-deals-motion-motion-1
  - predicate: measures
    object: mcem.planning.macc-consumption-planning
  - predicate: evidenced_by
    object: csu.evidence.msx-insights-msxi-analytics-measurement
classification: lagging
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: azure-consumption-program
    resource: "Azure Consumption Program"
    title: "FY26 CSU Leader Priority KPIs (#4)"
    last_modified: 2026-04-28
---
# Definition

**Job 2 — Total Completed Created** measures quarterly completed pipeline created by CSU as a percentage of Net New $ Required to reach Budget or Forecast at start of quarter.

**Classification: LAGGING** — measures what completed, not what was originated.

# Formula

```
Job 2 % = CSU-Originated Milestones Completed This Quarter ($) / Net New $ Required at Quarter Start
```

**Target: ≥ 20%**

# Critical Distinction: Completed vs Created

| Perspective | Anchor | What It Counts |
|-------------|--------|---------------|
| **Job 2 (this metric)** | Quarter in which milestone COMPLETES | CSU-originated milestones closed-won in-quarter (regardless of creation date) |
| **In-Quarter Create (IQC)** | Quarter in which milestone is CREATED | CSU-originated milestones created in-quarter (regardless of completion date) |

A quarter can show:
- Healthy Job 2 + Weak IQC = burning down prior origination (back-book depleting)
- Weak Job 2 + Healthy IQC = originating well, but completion lag lands in future quarters

# Business Rules

- **Inclusion (numerator):** CSU-originated pipeline whose Closed-Won date falls in current quarter
- **Exclusion:** Pipeline originated by STU/other roles; CSU-originated not yet completed; cancelled
- **Creation date is IRRELEVANT for inclusion** — a milestone created 2 quarters ago completing now counts
- **Post-snapshot net-new:** Milestones created after C2C snapshot DO count toward Job 2 if they complete in-quarter and CSU originated them (they are invisible to C2C)
- **Denominator:** Net New $ Required at quarter start, frozen

# Causal Chain

```
Upstream: In-Quarter Create velocity, Pipeline Hygiene, CSA origination activity
    → Job 2 Completed Created (THIS)
        → Downstream: NNR, ACR Growth, Azure Revenue Attainment
```

# Source Systems

- **MSX Dataverse** — opportunities, milestones, originator attribution, close dates

# Evidence Path

| Source | Artifact ID | Key Tables |
|--------|------------|-----------|
| MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | `factazureconsumptionpipeline` (real-time completions), `fact_nnr_data` |
| CSU Performance Master | `9dda8040-d9bc-4cfd-8d62-c991b611de33` | `[Consumption Job 2 VTT]` (scorecard) |

**Investigation:** Job 2 uses the **real-time** table (`factazureconsumptionpipeline`), NOT the C2C snapshot table. Post-snapshot milestones that close in-quarter flow here.

**Measurement paradigm:** Real-time (all qualifying completions in the window). See [Snapshot vs Real-Time](/csu/evidence/snapshot-vs-realtime.md).