---
type: Evidence Map
title: ECIF Evidence
id: csu.evidence.ecif-evidence
description: Evidence path from ECIF/NNR yield to the ECIF Yield semantic model and investigation patterns.
tags: [csu, evidence, ecif, nnr, yield, investment, semantic-model]
relationships:
  - predicate: references
    object: csu.evidence.msx-insights-msxi-analytics-measurement
  - predicate: references
    object: csu.metric.nnr-net-new-revenue-ecif-yield
  - predicate: references
    object: csu.program.ecif-enterprise-customer-investment-fund
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
---
# Concept

**[NNR — ECIF Yield](/csu/metrics/nnr.md)**: Net New Revenue attainment relative to ECIF investment utilization.

# Evidence Sources

## Primary: ECIF Yield

| Attribute | Value |
|-----------|-------|
| **PBI Artifact ID** | `d45f99eb-decb-4b32-a71b-94139d9948e6` |
| **Friendly name** | ECIF Yield |
| **Grain** | TPID × fiscal-year |

### Key Tables

| Table | Purpose |
|-------|---------|
| `TPID Dimension` | Account attributes |
| `ECIF Grants` | Approved ECIF investments |

### Key Measures

| Measure | What It Answers |
|---------|----------------|
| `[ECIF Yield]` | NNR attained vs NNR planned |
| `[PBO ROI]` | Pipeline Based Outlook return on investment |
| `[FY26 ECIF Granted]` | Total ECIF granted for fiscal year |
| `[YTD ECIF Spent]` | Year-to-date ECIF spent |
| `[YTD ECIF Utilization]` | % of granted ECIF utilized |
| `[Prorated Burn Rate %]` | Prorated spend pace |

### DAX Recipes

| Recipe | Purpose |
|--------|---------|
| `yield-by-subregion` | ECIF yield, ROI, granted/spent/utilization by sub-region |
| `yield-by-tpid` | Per-TPID ECIF metrics |

# Investigation Patterns

## "Are our ECIF investments returning NNR?"

→ Recipe: `yield-by-subregion` — shows yield and ROI across the territory

## "Which specific ECIF accounts are underperforming?"

→ Recipe: `yield-by-tpid` — per-account granted, spent, yield, utilization

## "Are we spending our ECIF allocation?"

→ `[YTD ECIF Utilization]` — low utilization = ECIF dollars being wasted (not invested)

# Related Evidence

- [Job 1 Evidence](/csu/evidence/job1-evidence.md) — ECIF-funded milestones feed C2C
- [MACC Evidence](/csu/evidence/macc-evidence.md) — ECIF often targets MACC acceleration
