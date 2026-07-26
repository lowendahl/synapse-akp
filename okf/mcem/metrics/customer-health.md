---
type: Metric
title: Customer Health
id: mcem.metric.customer-health
description: Composite signal reflecting overall customer relationship health across engagement, consumption, satisfaction, and risk dimensions.
tags: [mcem, metric, composite, health, customer]
relationships:
  - predicate: measures
    object: mcem.stage.stage-4-realize-value
  - predicate: measures
    object: mcem.stage.stage-5-manage-optimize
  - predicate: references
    object: csu.metric.customer-health-revenue-at-risk
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Customer Health is the composite signal reflecting overall customer relationship health. It combines engagement signals, consumption/usage metrics, satisfaction indicators, and risk dimensions into a unified view used for prioritization and intervention.

# Dimensions

- **Engagement:** Executive sponsor interactions, CSDR cadence, QBR delivery
- **Consumption:** ACR trajectory, MACC utilization, workload adoption
- **Satisfaction:** OSAT/DSAT signals, support experience
- **Risk:** Renewal risk, adoption risk, slippage indicators

# Governance

Customer Health is a CSU CSAM priority in FY27 and is reviewed in [Customer Success Delivery Reviews](/csu/planning/integrated-customer-planning.md). It is a primary input to account prioritization and resource allocation decisions.

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSXi Customer Health — Revenue at Risk | `57664612-66df-4081-9e99-4edeebefc65e` | `[Reactivity Health Status]`, `[FRATTM]`, `[Annualized FRA]` |

**Recipe:** `customer-aggregate` — per-TPID health signals. See [Customer Health Evidence](/csu/evidence/customer-health-evidence.md).