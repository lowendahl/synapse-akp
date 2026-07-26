---
type: KPI
title: "Cloud (ACR) Revenue at Risk"
id: csu.metric.cloud-acr-revenue-at-risk
description: Azure Consumed Revenue at risk from declining or at-risk consumption patterns on managed accounts.
tags: [csu, kpi, acr, azure, risk, consumption, leading]
relationships:
  - predicate: measures
    object: csu.outcome.cloud-adoption-outcomes
  - predicate: references
    object: mcem.metric.customer-health
  - predicate: informs
    object: mcem.risk.recapture
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: azure-consumption-program
    resource: "Azure Consumption Program"
    title: ACR At-Risk Tracking
    last_modified: 2026-07-01
---
# Definition

**Cloud (ACR) Revenue at Risk** measures Azure Consumed Revenue exposed to decline based on consumption trend signals — accounts showing declining month-over-month usage, approaching MACC shortfall, or flagged by consumption health models.

**Classification: LEADING** — declining consumption trends today predict revenue loss in future periods.

# Formula

```
ACR Revenue at Risk = Σ ACR (Accounts with declining/at-risk consumption signals) / Σ ACR (All managed accounts)
```

# Risk Signal Sources

| Signal | Trigger |
|--------|---------|
| MoM decline | ≥2 consecutive months of ACR decline |
| MACC pacing gap | Projected shortfall vs annual commitment |
| Workload churn | Key workload(s) deprovisioned or migrating away |
| Health model flag | PCI/health model identifies consumption risk |

# Causal Chain

```
Upstream: Consumption patterns, Workload health, MACC pacing, Optimization activity
    → Cloud ACR Revenue at Risk (THIS)
        → Downstream: MACC shortfall, Renewal risk, Territory attainment gap
```

# Relationship to Other Metrics

- **[MACC](/mcem/planning/macc.md)** — ACR at risk directly threatens MACC consumption targets
- **[Customer Health RaR](customer-health-rar.md)** — overlapping but ACR-specific (Azure only vs all-up health)
- **[Usage Revenue at Risk](usage-revenue-at-risk.md)** — sibling metric for M365 (vs Azure)

# Source Systems

- **Azure Consumption Program** — ACR trending, pacing models
- **PCI** — health model consumption signals
- **MSX** — MACC commitment data

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| WWBI Azure Date Grain | `7b01b356-d289-4478-8293-916b6b16663c` | `[$ ACR]`, `[$ Projected ACR]`, `[% Avg Daily MoM Growth]` |
| MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` | `[Shortfall Risk CQ]`, `[Shortfall Risk R12M]`, `[Remaining MACC]` |

**Investigation:** For per-account ACR trending, use `wwbi-azure-date-grain` recipes (`landing`, `workload`). For MACC shortfall risk, use `macc-acr-acceleration` recipes (`commitment-shortfall`).

See also: [MACC Evidence](/csu/evidence/macc-evidence.md)

**Measurement paradigm:** Real-time (daily ACR refresh).