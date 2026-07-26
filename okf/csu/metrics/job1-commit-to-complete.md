---
type: KPI
title: "Job 1 — Commit to Complete (C2C)"
id: csu.metric.job-1-commit-to-complete-c2c
description: Percentage of quarterly committed milestones (frozen at 5th of month-1 snapshot) closed within due date by CSU. Target ≥95%.
tags: [csu, kpi, c2c, job1, consumption, milestones, lagging]
relationships:
  - predicate: measures
    object: csu.process.commit-to-complete
  - predicate: measures
    object: mcem.metric.commit-to-complete-rate
  - predicate: evidenced_by
    object: csu.evidence.job-1-c2c-evidence
classification: lagging
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: azure-consumption-program
    resource: "Azure Consumption Program"
    title: "FY26 CSU Leader Priority KPIs (#3)"
    last_modified: 2026-04-27
---
# Definition

**Commit to Complete (C2C)** is the percentage of quarterly committed milestones — as captured in the baseline snapshot taken on the **5th of the first month of the quarter** — that are Closed within their due date by CSU.

**Classification: LAGGING** — measures execution fidelity after the commitment window closes.

# Formula

```
C2C % = Snapshot Milestones Closed On Time / Snapshot Committed Milestones
```

**Target: ≥ 95%**

# Critical Rule: The Snapshot

- **Snapshot date:** 5th of the first month of the quarter (e.g., Q1 → 5 Jul, Q2 → 5 Oct)
- **Denominator is FROZEN** at snapshot — milestones committed after the snapshot are NOT added
- Late-added milestones still count toward NNR and revenue all-up but are invisible to C2C

# Thresholds

| Zone | Meaning |
|------|---------|
| ≥ 95% | On target — execution discipline strong |
| 85–94% | Watch — delivery risk emerging |
| < 85% | Off-track — systemic execution failure |

# Business Rules

- **Inclusion (denominator):** CSU-owned milestones with status = Committed at or before snapshot date, due in current quarter
- **Exclusion:** Milestones committed after snapshot; non-committed; non-CSU-owned; transferred out after snapshot
- **Numerator:** Of the snapshot population, those Closed (Completed) within due date
- **Aggregation:** By CSU, Area, Sub — snapshot population locked at every level

# Relationship to Other Metrics

| Metric | Relationship |
|--------|-------------|
| Job 2 (Completed Created) | Post-snapshot milestones flow to Job 2, not C2C |
| NNR | All closed milestones (including post-snapshot) contribute to NNR |
| Slippage | Only applies to snapshot population |
| Pull-Forward | Only applies to snapshot population |

# Causal Chain

```
Upstream: Pipeline Hygiene, Milestone Quality, CSA Capacity, On-Strategy Delivery
    → Job 1 C2C (THIS)
        → Downstream: NNR, ACR Growth, Customer Outcomes
```

# Source Systems

- **MSX Dataverse** — milestone status, committed dates, ownership
- **Azure Consumption Program** — snapshot governance, C2C reporting

# Evidence Path

For full semantic model access, DAX recipes, and investigation patterns see: **[Job 1 C2C Evidence](/csu/evidence/job1-evidence.md)**

| Source | Artifact ID | Key Table |
|--------|------------|-----------|
| MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | `factazureconsumptionpipelinec2csnapshots` |

**Investigation shortcuts:**
- [Slippage detection](/csu/evidence/slippage.md) — milestones from snapshot that haven't closed
- [Pull-Forward detection](/csu/evidence/pull-forward.md) — milestones closing early or above committed value
- [Snapshot vs Real-Time](/csu/evidence/snapshot-vs-realtime.md) — why C2C is snapshot-locked
