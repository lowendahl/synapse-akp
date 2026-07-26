---
type: Evidence Map
title: Job 1 C2C Evidence
id: csu.evidence.job-1-c2c-evidence
description: Complete evidence path from Job 1 C2C concept to its semantic models, measures, and investigation patterns.
tags: [csu, evidence, job1, c2c, semantic-model, pipeline, investigation]
relationships:
  - predicate: references
    object: csu.evidence.msx-insights-msxi-analytics-measurement
  - predicate: references
    object: csu.metric.job-1-commit-to-complete-c2c
  - predicate: references
    object: csu.process.commit-to-complete
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
---
# Concept

**[Job 1 — Commit to Complete](/csu/metrics/job1-commit-to-complete.md)**: % of snapshot-committed milestones closed on time. Target ≥95%.

# Evidence Sources

## Primary: MSX Insights — Total Completed Pipeline_OneAMP

| Attribute | Value |
|-----------|-------|
| **PBI Artifact ID** | `ba0a24fe-f7e8-4210-850c-f9d961140fea` |
| **Workspace** | `fd129f38-b725-4397-b112-b45ed91a518b` |
| **MSXi Report** | [MSX Insights Total Completed Pipeline](https://msxinsights.microsoft.com/User/Home/report/c388649f-47db-49ca-af2b-1f7b22c690da/2892) |
| **Grain** | Engagement milestone × account × opportunity × fiscal month |

### Key Tables

| Table | Purpose |
|-------|---------|
| `factazureconsumptionpipelinec2csnapshots` | **THE C2C snapshot** — locked denominator |
| `factazureconsumptionpipeline` | Real-time milestone status (for Job 2/NNR) |
| `factazureconsumptionpipelinemonthlyc2csnapshots` | Monthly trending of snapshot population |
| `az_bz_opportunity` | Opportunity-level rollup |
| `fact_csu_target` | CSU completion targets by territory |
| `fact_nnr_data` | Net New Revenue attribution |

### Key Measures

| Measure | Purpose |
|---------|---------|
| `[Completed Pipeline_MTD]` | Month-to-date completed value |
| `[Committed Pipeline]` | Committed pipeline value |
| `[Consumption Total Completed]` | All completed consumption |

## Secondary: MSX Dataverse (Real-Time)

| Attribute | Value |
|-----------|-------|
| **Entity** | `msdyn_opportunities` / engagement milestones |
| **Access** | MSX API / msx_mcp_server |
| **Use** | Real-time milestone status, due dates, ownership, blocked reasons |

# Investigation Patterns

## "What is our current C2C rate?"

→ Query `factazureconsumptionpipelinec2csnapshots`: count milestones closed on time / total snapshot milestones

## "Which milestones are slipping?"

→ Filter snapshot milestones where status ≠ Completed AND due date < today
→ See [Slippage](/csu/evidence/slippage.md)

## "What's being pulled forward?"

→ Filter snapshot milestones where actual close date < due date OR actual value > committed value
→ See [Pull-Forward](/csu/evidence/pull-forward.md)

## "Is the pipeline sufficient for next quarter?"

→ Query `factazureconsumptionpipeline` for milestones with estimated dates in next quarter
→ Cross-reference with [Pipeline Coverage Index](/mcem/metrics/pipeline-coverage-index.md)

## "What post-snapshot net-new closed this quarter?"

→ Milestones in `factazureconsumptionpipeline` with close date in-quarter BUT not in `factazureconsumptionpipelinec2csnapshots`
→ These flow to [Job 2](/csu/metrics/job2-completed-created.md) and NNR but NOT C2C

# Related Evidence

- [MACC Evidence](/csu/evidence/macc-evidence.md) — MACC shortfall drives C2C urgency
- [MSX Dataverse](/csu/evidence/msx-dataverse.md) — Real-time individual milestone status, ownership, change history (authoritative source)

# Causal Risk Signals

These are **not direct evidence** for C2C measurement, but their absence correlates with [Slippage](/csu/evidence/slippage.md):

| Signal | System | Why It Matters |
|--------|--------|---------------|
| No CSP linked to milestone | [eSXP CSP](/csu/evidence/esxp-csp.md) | No one is actively project-managing the milestone → drift → slippage |
| No CSA booked against the workload | [GRM](/csu/evidence/mdm-grm.md) | No delivery resource assigned → milestone won't close on time |
| Milestone owner has no capacity | [GRM](/csu/evidence/mdm-grm.md) | Owner is overbooked → execution will stall |

**Pattern:** When investigating slippage root causes, check these causal systems. When measuring C2C itself, use the PBI snapshot model + MSX Dataverse.
