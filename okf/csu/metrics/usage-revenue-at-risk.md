---
type: KPI
title: "Usage Revenue at Risk (M365)"
id: csu.metric.usage-revenue-at-risk-m365
description: Percentage of M365 revenue on accounts classified at-risk due to low/declining usage signals. Target <5%.
tags: [csu, kpi, usage-rar, m365, risk, adoption, leading]
relationships:
  - predicate: measures
    object: csu.outcome.ai-transformation-outcomes
  - predicate: measures
    object: mcem.metric.customer-health
  - predicate: informs
    object: mcem.risk.recapture
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: m365-usage-excellence
    resource: "M365 Usage Excellence"
    title: "FY26 CSU Leader Priority KPIs (#6)"
    last_modified: 2026-04-27
---
# Definition

**Usage Revenue at Risk** measures the percentage of active M365 account revenue classified "at risk" based on usage signals (low/declining MAU vs entitled seats).

**Classification: LEADING** — under-adoption today predicts renewal failure and revenue loss at next renewal event.

# Formula

```
% Revenue at Risk = Σ Revenue (At-Risk M365 Accounts) / Σ Revenue (All Active M365 Accounts)
```

**Target: < 5%**

# Thresholds

| Zone | Meaning |
|------|---------|
| < 5% | On target |
| 5–10% | Watch — adoption motions required |
| > 10% | Off-track — significant M365 revenue exposed |

# Business Rules

- **Inclusion:** Active M365 paid accounts
- **Exclusion:** Trial/non-paid/churned accounts
- **Qualification:** "At risk" per M365 Usage Excellence thresholds (MAU/entitlement ratio)
- **Aggregation:** By CSU, Area, Sub, Account
- **Cadence:** Monthly snapshot

# Causal Chain

```
Upstream: MAU, PAU, License assignments, Onboarding status
    → Usage Revenue at Risk (THIS)
        → Downstream: Renewal Risk, Customer Health Revenue at Risk, NNR
```

# Semantic Interpretation

| Tells You | Does NOT Tell You |
|-----------|-------------------|
| How much M365 footprint is under-adopted and exposed at renewal | Why adoption is low |
| Where adoption intervention is needed | Whether the customer would actually churn |

# Source Systems

- **M365 Usage Excellence** — MAU/entitlement classification
- **MSX** — revenue attribution

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSX Insights — M365 Usage Excellence | `db74d200-6b93-4a91-a629-6ca10ef65b49` | `[Revenue At Risk]`, `[Projected Revenue At Risk %]` |
| CSU Performance Master | `9dda8040-d9bc-4cfd-8d62-c991b611de33` | `[Usage RaR]` (scorecard) |

**Key table:** `ActualUsageAccounts` — per-account MAU/entitlement ratio classification driving at-risk status.

**Measurement paradigm:** Monthly snapshot (MAU/entitlement ratio at month-end).