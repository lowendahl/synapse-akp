---
type: KPI
title: "NNR — Net New Revenue (ECIF Yield)"
id: csu.metric.nnr-net-new-revenue-ecif-yield
description: Net New Revenue consumption plan attainment relative to ECIF utilization. Measures ROI of ECIF investment decisions.
tags: [csu, kpi, nnr, ecif, revenue, consumption, lagging]
relationships:
  - predicate: measures
    object: csu.program.ecif-enterprise-customer-investment-fund
  - predicate: measures
    object: mcem.planning.macc-consumption-planning
  - predicate: evidenced_by
    object: csu.evidence.ecif-evidence
classification: lagging
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ecif-program
    resource: "Consumption / ECIF Program"
    title: "FY26 CSU Leader Priority KPIs (#5)"
    last_modified: 2026-04-27
---
# Definition

**NNR (Net New Revenue / ECIF Yield)** measures Net New Revenue consumption plan attainment relative to ECIF utilization rate. It answers: for every dollar of ECIF spent, how much net-new Azure consumption did we generate vs what we promised?

**Classification: LAGGING** — measures realized return after investment and delivery complete.

# Formula

```
ECIF Yield = NNR Attained / NNR Plan (filtered to ECIF utilization)
```

# Three NNR Contribution Paths

| Path | Source | C2C Visibility |
|------|--------|---------------|
| 1. Snapshot milestones closing at baseline value | C2C-aligned execution | Visible in C2C |
| 2. Pull-forward on snapshot milestones | Earlier closure or scope increase | Visible in C2C (boosts numerator) |
| 3. Post-snapshot net-new closing in-quarter | CSU origination after snapshot | Invisible to C2C; flows to Job 2 if CSU-originated |

# Business Rules

- **Inclusion:** Approved ECIF engagements with NNR commitments
- **Exclusion:** Non-ECIF funded work; pre-existing baseline consumption
- **Qualification:** NNR measured against plan baseline at ECIF approval
- **Aggregation:** By CSU, Area, engagement

# Critical Note

C2C (Job 1) and NNR have **different denominators** and can move independently. A quarter can hit 95% C2C but miss NNR (if baselines were set wrong) or miss C2C but hit NNR (via post-snapshot net-new closing big).

# Causal Chain

```
Upstream: ECIF approvals, Milestone close rate (Job 1), Job 2 origination
    → NNR / ECIF Yield (THIS)
        → Downstream: ACR, Azure Revenue Attainment, Customer Expansion
```

# Source Systems

- **ECIF Program** — investment approvals, NNR plans
- **MSX Dataverse** — milestone close values

# Evidence Path

For full semantic model access and DAX recipes see: **[ECIF Evidence](/csu/evidence/ecif-evidence.md)**

| Source | Artifact ID | Key Recipe |
|--------|------------|-----------|
| ECIF Yield | `d45f99eb-decb-4b32-a71b-94139d9948e6` | `yield-by-subregion`, `yield-by-tpid` |

**Measurement paradigm:** Real-time (not snapshot-locked). See [Snapshot vs Real-Time](/csu/evidence/snapshot-vs-realtime.md).
