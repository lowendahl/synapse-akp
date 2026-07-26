---
type: Evidence Source
title: MSX Insights (MSXi) — Analytics & Measurement
id: csu.evidence.msx-insights-msxi-analytics-measurement
aliases: [MSXi, MSX Insights, MSXI, PBI Analytics, Semantic Models]
description: The analytics and measurement layer — PBI semantic models providing KPI calculations, snapshot-based metrics, actual outcomes (ACR, labour, pipeline rates), and scorecard aggregations. This is where you go to MEASURE performance, not to manage individual records.
tags: [csu, evidence, msxi, analytics, measurement, pbi, kpi, outcomes, snapshots]
relationships:
  - predicate: references
    object: csu.metric.job-1-commit-to-complete-c2c
  - predicate: references
    object: csu.metric.customer-health-revenue-at-risk
  - predicate: references
    object: csu.evidence.ecif-evidence
  - predicate: references
    object: csu.evidence.delivery-evidence-udc-ucr-hours
generated: { by: human:plwendahl, at: 2026-07-25T02:55:00Z }
status: stable
---
# What MSXi Is

**MSX Insights (MSXi)** is the **Power BI** analytics and measurement layer — a collection of semantic models that calculate KPIs, track outcomes against snapshots, and aggregate actuals (ACR, labour hours, pipeline rates, close rates). This is where you go to **MEASURE** performance.

# Key Distinction

| System | Platform | Purpose | Use When |
|--------|----------|---------|----------|
| [MSX Dataverse](/csu/evidence/msx-dataverse.md) | Dynamics 365 | Manage individual records | "What's the status of milestone MS-123456?" |
| **MSX Insights (MSXi)** | Power BI | Measure aggregate outcomes | "What's our C2C rate? How much ACR slipped?" |
| [MDM & GRM](/csu/evidence/mdm-grm.md) | eSXP APIs | Manage contracts & bookings | "What packages does this customer have?" |
| [eSXP CSP](/csu/evidence/esxp-csp.md) | eSXP APIs | Manage success plans | "What priorities are in the CSP?" |

# What MSXi Provides

| Category | What It Measures | Example Models |
|----------|-----------------|----------------|
| **Pipeline KPIs** | C2C rate, close rates, pipeline velocity | Total Completed Pipeline, Usage Close Rate |
| **Consumption outcomes** | ACR, MACC attainment, shortfall risk | MACC ACR Acceleration, Azure Date Grain |
| **Delivery outcomes** | UDC, labour hours, package consumption | CES Delivery Insights |
| **Usage outcomes** | MAU, PAU, PRU, Revenue at Risk | M365 Usage Excellence, Copilot PRU |
| **Customer health** | FRA, reactivity, CritSit, DSAT | Customer Health RaR, CX Pulse OSAT |
| **Investment yield** | ECIF ROI, NNR attribution | ECIF Yield |
| **Scorecard rollup** | All 10 CSU KPIs in one model | CSU Performance Master |

# Primary Semantic Models

| Model | Artifact ID | Measures |
|-------|------------|----------|
| MSX Insights — Total Completed Pipeline | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | C2C snapshot, completed pipeline, NNR, slippage |
| MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` | MACC attainment, shortfall risk, pipeline coverage, execution scores |
| CES Delivery Insights | `56064262-fdfa-4c3d-968f-dffd3ebf759a` | UDC, labour hours, package consumption, CSP coverage |
| MSX Insights — M365 Usage Excellence | `db74d200-6b93-4a91-a629-6ca10ef65b49` | MAU, PAU, usage milestones, revenue at risk |
| Copilot PRU | `29c43c92-a41b-4ce3-86d3-0ddb03ab629d` | PRU daily/monthly, VTT, pipeline excellence |
| WWBI Azure Date Grain | `7b01b356-d289-4478-8293-916b6b16663c` | Daily/monthly ACR, projected ACR, MoM growth |
| Customer Health — Revenue at Risk | `57664612-66df-4081-9e99-4edeebefc65e` | FRA TTM, reactivity, CritSit, annualized FRA |
| CX Pulse OSAT | `e91c9a87-84e9-4481-a140-271b68c1e1f5` | OSAT, VSAT, DSAT, satisfaction drivers |
| ECIF Yield | `d45f99eb-decb-4b32-a71b-94139d9948e6` | ECIF yield, PBO ROI, utilization |
| CSU Performance Master | `9dda8040-d9bc-4cfd-8d62-c991b611de33` | All 10 CSU KPIs aggregated by subsidiary |
| CES Staffing Insights | `3d1501b1-c8d4-4c4e-b724-116dc7c6e9ce` | Staffing demand funnel, requested/booked/assigned |

# Access Pattern

**Primary:** Fabric ExecuteQuery (DAX):

```
POST https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{artifact_id}/executeQueries
Body: { "queries": [{ "query": "EVALUATE SUMMARIZECOLUMNS(...)" }] }
```

- Hard cap: **1000 rows per call** (chunk with filters)
- Auth: Azure AD bearer token with Power BI scope
- Format: JSON tabular result

**Fallback:** REST API when Dataverse endpoints are saturated:

```
GET https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{artifact_id}/...
```

- Use REST fallback when: Dataverse OData endpoints return 429/503 or are overwhelmed under load
- Same auth (Azure AD bearer token with Power BI scope)
- Provides alternative path to the same underlying data through the PBI service layer

# Measurement Paradigms

MSXi models use two paradigms (see [Snapshot vs Real-Time](/csu/evidence/snapshot-vs-realtime.md)):

| Paradigm | Models Using It | What Gets Frozen |
|----------|----------------|-----------------|
| **Snapshot-locked** | Total Completed Pipeline (C2C tables) | Milestone population on 5th of month-1 |
| **Real-time** | Azure Date Grain, Usage Excellence, MACC, CES Delivery | Running totals, no frozen denominator |

# When to Use MSXi vs MSX Dataverse

| Question Type | Use MSXi | Use MSX Dataverse |
|---------------|----------|-------------------|
| "What is our C2C rate?" | ✅ | ❌ |
| "How much ACR did we complete this month?" | ✅ | ❌ |
| "What's the status of milestone MS-123?" | ❌ | ✅ |
| "Who owns this opportunity?" | ❌ | ✅ |
| "What's the MACC shortfall risk across my territory?" | ✅ | ❌ |
| "Why did this milestone slip?" | ❌ | ✅ (audit trail) |
| "How many labour hours did we deliver last month?" | ✅ | ❌ |
| "Is this CSA booked next week?" | ❌ | [GRM](/csu/evidence/mdm-grm.md) |

# Relationship to Evidence Maps

Each concept's evidence map file provides the specific semantic model, tables, measures, and DAX recipes for that concept:

- [Job 1 C2C Evidence](/csu/evidence/job1-evidence.md)
- [MACC Evidence](/csu/evidence/macc-evidence.md)
- [Delivery Evidence](/csu/evidence/delivery-evidence.md)
- [Customer Health Evidence](/csu/evidence/customer-health-evidence.md)
- [ECIF Evidence](/csu/evidence/ecif-evidence.md)
