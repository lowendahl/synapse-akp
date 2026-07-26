---
type: KPI
title: "PRU — Productive Recurring User"
id: csu.metric.pru-productive-recurring-user
description: Users with ≥30 intentional actions in a rolling 28-day window on Microsoft cloud workloads. Measures adoption depth and habitual productive use.
tags: [csu, kpi, pru, adoption, usage, copilot, agents, lagging]
relationships:
  - predicate: measures
    object: csu.outcome.ai-transformation-outcomes
  - predicate: measures
    object: csu.outcome.cloud-adoption-outcomes
  - predicate: informs
    object: mcem.metric.customer-health
classification: lagging
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: viva-insights
    resource: "Viva Insights / MSXAI"
    title: PRU Telemetry
    last_modified: 2026-04-28
---
# Definition

**PRU (Productive / Premium Recurring User)** is a paid license holder performing ≥30 intentional actions in a rolling 28-day window on Microsoft cloud workloads. It distinguishes habitual productive use from occasional activity.

**Classification: LAGGING** — confirms adoption depth after users have formed habits.

# Variants

| Variant | Scope | Source |
|---------|-------|--------|
| M365 PRU | M365 workloads (Teams, Outlook, etc.) | Viva Insights |
| Copilot PRU | M365 Copilot usage | MSXAI |
| Agent PRU | Copilot Agent usage | MSXAI |

# Formula

```
PRU = Count of paid license holders with ≥30 intentional actions in 28-day rolling window
PRU Rate = PRU / Total Paid License Holders
```

# Relationship to MAU/PAU

```
MAU (broadest) → PAU (productive subset) → PRU (habitual productive subset)
```

PRU is the deepest signal — if a user reaches PRU threshold, they have formed a genuine product habit.

# Causal Chain

```
Upstream: Onboarding, Success Programs, Feature Activation, Copilot Deployment
    → PRU (THIS)
        → Downstream: Usage Revenue at Risk (inverse), Renewal Likelihood, Expansion
```

# Source Systems

- **Viva Insights** — M365 usage telemetry
- **MSXAI** — Copilot and Agent usage telemetry

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| Copilot PRU — Chat — Agent Usage Pipeline Excellence | `29c43c92-a41b-4ce3-86d3-0ddb03ab629d` | `[M365 Copilot PRU Daily]`, `[PRU Q4 Goal]`, `[Copilot PRU VTT %]` |

**Key tables:** `FactM365CopilotPremiumMAUDaily`, `DimMAL` (customer dimension), `FactCopilotChatMAUDaily`

**DAX grain:** TPID (customer-level) or WW Region (summary-level).

**Measurement paradigm:** Real-time (rolling 28-day, ≥30 intentional actions threshold).