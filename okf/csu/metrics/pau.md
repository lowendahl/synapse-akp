---
type: KPI
title: "PAU — Productive Active Users"
id: csu.metric.pau-productive-active-users
description: Subset of MAU performing productive (not just trivial) actions — measures adoption quality beyond mere logins.
tags: [csu, kpi, pau, adoption, usage, leading]
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
    title: PAU Reporting
    last_modified: 2026-04-28
---
# Definition

**PAU (Productive Active Users)** counts users performing productive actions (not just logins or trivial clicks) on Microsoft cloud workloads. It measures adoption quality — are users doing real work in the product?

**Classification: LEADING** — productive usage today predicts stickiness, value realization, and renewal tomorrow.

# Relationship Hierarchy

```
MAU (any activity) → PAU (productive activity — THIS) → PRU (habitual ≥30 actions)
```

PAU sits between breadth (MAU) and depth (PRU). An account with high MAU but low PAU has surface adoption without productivity gains.

# Business Rules

- **Inclusion:** Paid license holders performing qualified productive actions
- **Exclusion:** Trivial actions (login-only, passive receipt), service accounts
- **Aggregation:** By account, workload, segment, Area

# Causal Chain

```
Upstream: MAU, Feature adoption, Training, Success Programs
    → PAU (THIS)
        → Downstream: PRU, Usage Revenue at Risk (inverse), Expansion readiness
```

# Source Systems

- **Viva Insights** — productivity signal classification
- **MSXAI** — cross-workload productive action telemetry

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSX Insights — M365 Usage Excellence | `db74d200-6b93-4a91-a629-6ca10ef65b49` | `[Copilot PAU]`, usage intensity tiers |

**Key table:** `ActualUsageAccounts` — per-account MAU/PAU classification.

**Measurement paradigm:** Real-time (rolling 28-day productive action window).