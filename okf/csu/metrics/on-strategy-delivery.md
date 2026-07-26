---
type: KPI
title: "On-Strategy Delivery"
id: csu.metric.on-strategy-delivery
description: Percentage of Area CSA delivered hours aligned to the fiscal year delivery strategy, technology maturity model, and customer segmentation.
tags: [csu, kpi, on-strategy, delivery, csa, diagnostic]
relationships:
  - predicate: measures
    object: csu.delivery.delivery-engine-routing
  - predicate: measures
    object: csu.doctrine.technical-maturity-model-tmm
  - predicate: evidenced_by
    object: csu.evidence.delivery-evidence-udc-ucr-hours
classification: diagnostic
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-delivery-insights
    resource: "CES Delivery Insights"
    title: "FY26 CSU Leader Priority KPIs (#9)"
    last_modified: 2026-04-27
---
# Definition

**On-Strategy Delivery** measures the percentage of actual Delivered Hours by Area CSAs that align with the fiscal year delivery strategy, [Technical Maturity Model (TMM)](/csu/doctrine/technical-maturity-model.md), and customer segmentation.

**Classification: DIAGNOSTIC** — tells you whether capacity is being deployed to the right work (neither purely leading nor lagging).

# Formula

```
On-Strategy % = On-Strategy Delivered Hours / Total Delivered Hours (Area CSA)
```

# Business Rules

- **Inclusion:** Area CSA delivered hours
- **Exclusion:** Non-Area CSAs; non-strategy-tagged hours
- **Qualification:** Hours classified "on-strategy" per FY delivery framework
- **Aggregation:** By CSU, Area, CSA team
- **Cadence:** Rolling FY

# Semantic Interpretation

| Tells You | Does NOT Tell You |
|-----------|-------------------|
| Whether CSA capacity is funding strategic outcomes | Customer outcome quality of those hours |
| Where capacity is being misallocated | Why off-strategy work is being accepted |

# Causal Chain

```
Upstream: Delivery planning, Customer prioritization, Scoping quality
    → On-Strategy Delivery (THIS)
        → Downstream: Job 1 C2C, Job 2 Origination, UDC, NNR
```

# Source Systems

- **CES Delivery Insights** — delivery hours, strategy tagging

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| CES Delivery Insights | `56064262-fdfa-4c3d-968f-dffd3ebf759a` | `[Delivered Hours]`, `[Logged Hours]` with strategy classification |
| CSU Performance Master | `9dda8040-d9bc-4cfd-8d62-c991b611de33` | `[On Strategy %]` (scorecard) |

**Investigation:** Use `labor-month` or `labor-month-by-manager` recipes filtered by engagement strategy tag to determine on/off-strategy split.

See also: [Delivery Evidence](/csu/evidence/delivery-evidence.md)