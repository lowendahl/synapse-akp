---
type: KPI
title: "Customer Health — Revenue at Risk"
id: csu.metric.customer-health-revenue-at-risk
description: Composite metric expressing the percentage of revenue exposed to customers failing health checklist activities.
tags: [csu, kpi, health, risk, revenue, leading]
relationships:
  - predicate: measures
    object: mcem.metric.customer-health
  - predicate: evidenced_by
    object: csu.evidence.customer-health-evidence
  - predicate: informs
    object: csu.process.t-minus-renewal-motion
  - predicate: informs
    object: csu.priority.earn-customer-trust
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: customer-health-program
    resource: "Customer Health Program"
    title: "FY26 CSU Leader Priority KPIs (#2)"
    last_modified: 2026-04-27
---
# Definition

**Customer Health Revenue at Risk** measures the percentage of revenue sitting on customers who are NOT meeting the health bar (defined checklist activities incomplete).

**Classification: LEADING** — health debt today predicts renewal risk, DSAT, and churn tomorrow.

# Formula

```
% Revenue at Risk = Σ Revenue (Customers failing health checklist) / Σ Revenue (All in-scope customers)
```

# Thresholds

| Zone | Meaning |
|------|---------|
| < 10% | On target |
| 10–20% | Watch — health debt accumulating |
| > 20% | Off-track — renewal risk material |

# Business Rules

- **Inclusion:** Active CSU-managed customers with revenue
- **Exclusion:** Out-of-scope segments
- **Qualification:** "Healthy" requires completion of defined checklist activities
- **Aggregation:** By CSU, Area, Sub
- **Cadence:** Monthly snapshot

# Causal Chain

```
Upstream: UDC, On-Strategy Delivery, Checklist Completion
    → Customer Health Revenue at Risk (THIS)
        → Downstream: Renewal Risk, DSAT, NNR
```

# Semantic Interpretation

| Tells You | Does NOT Tell You |
|-----------|-------------------|
| Health debt exposure across the book | Imminent churn (health is leading, not forecast) |
| Where remediation investment is needed | Root cause of specific health failures |

# Source Systems

- **Customer Health Program** — checklist scoring, health classification
- **PBI: Customer Health Revenue at Risk** (artifact 57664612-66df-4081-9e99-4edeebefc65e)

# Evidence Path

For full investigation patterns see: **[Customer Health Evidence](/csu/evidence/customer-health-evidence.md)**

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSXi Customer Health — Revenue at Risk | `57664612-66df-4081-9e99-4edeebefc65e` | `[Created SR]`, `[CritSit Count]`, `[Reactivity]`, `[Reactivity Health Status]`, `[FRATTM]`, `[Annualized FRA]` |
| CSU Performance Master | `9dda8040-d9bc-4cfd-8d62-c991b611de33` | `[Customer Health RaR]` (aggregated scorecard) |

**Key recipe:** `customer-aggregate` — per-TPID FRA, reactivity, CritSit, SR count.

**Measurement paradigm:** Real-time. See [Snapshot vs Real-Time](/csu/evidence/snapshot-vs-realtime.md).