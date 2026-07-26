---
type: Taxonomy
title: Pipeline Stages & States
id: mcem.metric.pipeline-stages-states
description: The end-to-end pipeline state machine from Unqualified through Completed, governing both Azure consumption and billed pipeline.
tags: [mcem, pipeline, stages, states, unqualified, qualified, committed, completed, taxonomy]
relationships:
  - predicate: references
    object: mcem.stage.stage-1-listen-consult
  - predicate: references
    object: mcem.stage.stage-2-inspire-design
  - predicate: references
    object: mcem.stage.stage-3-empower-achieve
  - predicate: references
    object: mcem.stage.stage-4-realize-value
  - predicate: references
    object: mcem.stage.stage-5-manage-optimize
  - predicate: references
    object: csu.pipeline.pipeline-ownership-model
  - predicate: references
    object: csu.pipeline.two-motion-model
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The Pipeline Stages & States model defines the lifecycle every pipeline item (opportunity or milestone) moves through from initial identification to revenue realization.

# The Pipeline State Machine

```
Unqualified → Qualified → Committed → Completed
     │              │            │           │
     └─ Disengaged  └─ Lost      └─ Slipped  └─ (Revenue realized)
```

# Stage Definitions

## Unqualified Pipeline

| Attribute | Detail |
|-----------|--------|
| **Definition** | Pipeline where customer has NOT yet agreed to outcome, value, date, resources, or budget |
| **Probability** | Low; default state for all new milestones |
| **Owner** | STU/DES (moves toward qualification) |
| **Forecast level** | Uncommitted |
| **Classification** | Leading signal — raw demand; much will never convert |

## Qualified Pipeline

| Attribute | Detail |
|-----------|--------|
| **Definition** | Customer has validated the opportunity/solution; business case agreed; plausible path to close |
| **Probability** | >50% (Upside) or higher |
| **Owner** | STU (consumption), ATU (billed) |
| **Forecast level** | Upside or Committed At Risk |
| **Classification** | Leading signal — vetted demand feeding execution pipeline |
| **MCEM Stage** | Stage 2 (Inspire & Design) exit |

## Committed Pipeline

| Attribute | Detail |
|-----------|--------|
| **Definition** | Customer has indicated intent/agreed to buy; execution plan confirmed (outcome, value, timing, resources, budget, next steps all agreed) |
| **Probability** | >75% (Committed At Risk) to >95% (Committed) |
| **Owner** | CSU (consumption milestones), ATU/STU (billed opportunities) |
| **Forecast level** | Committed or Committed At Risk |
| **Classification** | Lagging relative to qualification; leading relative to revenue |
| **MCEM Stage** | Stage 3 (Commit) exit |
| **C2C Rule** | Committed milestones at 5th-of-month-1 snapshot form the [C2C denominator](/csu/metrics/job1-commit-to-complete.md) |

## Completed Pipeline

| Attribute | Detail |
|-----------|--------|
| **Definition** | Milestone/opportunity has been closed-won; revenue recognized or consumption materialized |
| **Probability** | 100% (closed) |
| **Owner** | CSU (delivery), Finance (revenue recognition) |
| **Forecast level** | N/A (actual) |
| **Classification** | Lagging — confirmed outcome |
| **MCEM Stage** | Stage 4 (Realize Value) |

# Conversion Metrics

| Transition | Metric | Target |
|------------|--------|--------|
| Unqualified → Qualified | Qualification Rate | Varies by segment |
| Qualified → Committed | [Q-to-C Rate](/mcem/metrics/qualified-pipeline.md) | Per territory |
| Committed → Completed | [C2C Rate](/mcem/metrics/commit-to-complete-rate.md) | ≥95% |
| Overall velocity | [Days in Stage](/mcem/metrics/days-in-stage.md) | Decreasing |

# Pipeline Types That Flow Through This Model

| Pipeline Type | Description |
|---------------|-------------|
| **Azure Consumption (ACR) Pipeline** | Milestones representing incremental Azure consumption |
| **Billed Pipeline** | EA/EAS renewals, recurring orders, true-ups |
| **Usage Pipeline** | M365/Copilot usage intents and adoption milestones |
| **MACC Renewal Pipeline** | MACC commitment renewals and upsells |
| **Unified Pipeline** | Unified Support contract renewals/expansions |

# Evidence Path

| Source | Artifact ID | Purpose |
|--------|------------|---------|
| MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | Azure consumption pipeline state transitions |
| MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` | `[Qualified Pipeline]`, `[Committed Pipeline]`, `[Uncommitted Pipeline]`, `[Non Qualified Pipeline]` |

**Recipes:** Use `pipeline-coverage` from MACC ACR Acceleration to see the current distribution across pipeline stages per TPID.