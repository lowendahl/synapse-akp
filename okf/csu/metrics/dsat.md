---
type: KPI
title: "DSAT — Customer Dissatisfaction"
id: csu.metric.dsat-customer-dissatisfaction
description: Percentage of customers responding bottom-2-box (Somewhat/Very Dissatisfied) on CX Pulse Overall Satisfaction survey.
tags: [csu, kpi, dsat, csat, cx, satisfaction, lagging]
relationships:
  - predicate: measures
    object: mcem.metric.customer-health
  - predicate: informs
    object: csu.priority.earn-customer-trust
  - predicate: evidenced_by
    object: csu.evidence.msx-insights-msxi-analytics-measurement
classification: lagging
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: cx-pulse-program
    resource: "CX Pulse / OSAT Program"
    title: "FY26 CSU Leader Priority KPIs (#1)"
    last_modified: 2026-04-27
---
# Definition

**DSAT (Customer Dissatisfaction)** measures the percentage of customers who responded "Somewhat Dissatisfied" or "Very Dissatisfied" to the Overall Satisfaction (OSAT) question on the CX Pulse Survey.

**Classification: LAGGING** — reflects past experience, not future trajectory.

# Formula

```
DSAT % = Bottom-2-box OSAT responses / Total OSAT responses
```

# Thresholds

| Zone | Meaning |
|------|---------|
| < 10% | On target |
| 10–15% | Watch |
| > 15% | Off-track — CX intervention required |

# Business Rules

- **Inclusion:** Responses to OSAT question on CX Pulse
- **Exclusion:** Non-responses; surveys outside reporting window
- **Qualification:** Bottom-2-box (Somewhat/Very Dissatisfied) = DSAT
- **Aggregation:** By CSU, Area, segment

# Causal Chain

```
Upstream: Delivery quality, Support outcomes, UDC, On-Strategy Delivery
    → DSAT (THIS)
        → Downstream: Renewal Risk, Advocacy, Customer Health Revenue at Risk
```

# Semantic Interpretation

| Tells You | Does NOT Tell You |
|-----------|-------------------|
| Concentration of dissatisfaction among respondents | Why customers are dissatisfied (use verbatims) |
| Where CX intervention is needed | Sentiment of non-respondents |

# Source Systems

- **CX Pulse** — survey responses, OSAT scores

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSX Insights — CX Pulse OSAT | `e91c9a87-84e9-4481-a140-271b68c1e1f5` | `[Surveyed TPIDs/Cx Accounts]`, `[Account Response Count]` |
| CSU Performance Master | `9dda8040-d9bc-4cfd-8d62-c991b611de33` | `[DSAT]` (aggregated scorecard) |

**Key table:** `Fact CXPulse Customer Solution Area Survey` — response-level OSAT/VSAT/DSAT classification.

**Measurement paradigm:** Real-time (rolling survey window). See [Snapshot vs Real-Time](/csu/evidence/snapshot-vs-realtime.md).