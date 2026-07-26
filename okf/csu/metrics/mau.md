---
type: KPI
title: "MAU — Monthly Active Users"
id: csu.metric.mau-monthly-active-users
description: Count of unique users who performed at least one action on a Microsoft cloud workload in the trailing 28-day window.
tags: [csu, kpi, mau, adoption, usage, leading]
relationships:
  - predicate: measures
    object: csu.outcome.ai-transformation-outcomes
  - predicate: measures
    object: csu.outcome.cloud-adoption-outcomes
  - predicate: informs
    object: mcem.metric.customer-health
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: m365-usage-program
    resource: "M365 Usage Excellence"
    title: MAU Reporting
    last_modified: 2026-04-28
---
# Definition

**MAU (Monthly Active Users)** counts unique users who performed at least one action on a Microsoft cloud workload in the trailing 28-day window. It measures usage breadth — how many people are touching the product.

**Classification: LEADING** — rising/falling MAU predicts future renewal health and revenue trajectory.

# Relationship Hierarchy

```
MAU (any activity) → PAU (productive activity) → PRU (habitual ≥30 actions)
```

MAU is the broadest adoption signal. An account with high MAU but low PAU/PRU has surface-level adoption without depth.

# Business Rules

- **Inclusion:** Paid license holders with ≥1 action in 28 days
- **Exclusion:** Trial users, service accounts, automated actions
- **Aggregation:** By account, workload, segment, Area

# Causal Chain

```
Upstream: License deployment, Onboarding, Feature awareness
    → MAU (THIS)
        → Downstream: PAU, PRU, Usage Revenue at Risk (inverse), Renewal
```

# Source Systems

- **Viva Insights / M365 Admin** — user activity telemetry
- **MSXAI** — cross-workload activity aggregation

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSX Insights — M365 Usage Excellence | `db74d200-6b93-4a91-a629-6ca10ef65b49` | `[Copilot MAU]`, `[Usage Intent Created]`, `[Revenue At Risk]` |
| Copilot PRU — Chat — Agent Usage Pipeline Excellence | `29c43c92-a41b-4ce3-86d3-0ddb03ab629d` | `[Copilot Chat MAU Daily]`, `[TAM (Usage pipeline Excellence)]` |

**Key tables:** `ActualUsageAccounts`, `FactUsageMilestones`, `FactM365CopilotPremiumMAUDaily`

**Measurement paradigm:** Real-time (rolling 28-day active window).