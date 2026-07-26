---
type: KPI
title: "Repeatable Delivery"
id: csu.metric.repeatable-delivery
description: Percentage of delivery hours using repeatable/scalable IP vs bespoke engagements — measures delivery efficiency and scalability.
tags: [csu, kpi, repeatable, delivery, scalability, ip, diagnostic]
relationships:
  - predicate: measures
    object: csu.program.success-programs
  - predicate: measures
    object: csu.delivery.delivery-engine-routing
  - predicate: informs
    object: csu.priority.execute-with-excellence
classification: diagnostic
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-delivery-insights
    resource: "CES Delivery Insights"
    title: Repeatable Delivery Tracking
    last_modified: 2026-07-01
---
# Definition

**Repeatable Delivery** measures the percentage of delivery hours spent on repeatable, scalable IP-based engagements (standardized workshops, assessments, frameworks) vs fully bespoke/custom delivery.

**Classification: DIAGNOSTIC** — tells you whether delivery operations are building leverage or staying artisanal.

# Formula

```
Repeatable % = Hours on Repeatable Engagements / Total Delivered Hours
```

# Why It Matters

| High Repeatable % | Low Repeatable % |
|-------------------|-----------------|
| Scalable, efficient delivery | Every engagement reinvents |
| Faster onboarding of new CSAs | Knowledge loss when CSAs leave |
| Consistent customer outcomes | Variable quality |
| Lower cost-to-serve | Higher cost-to-serve |
| Supports Engine 3 (Programmatic) growth | Stuck in Engine 1/2 only |

# Relationship to Delivery Engines

- **Engine 1 (Designated)** — mix of bespoke + repeatable
- **Engine 2 (Pooled)** — higher repeatable ratio expected
- **Engine 3 (Programmatic)** — should be ~100% repeatable (Success Programs)

# Causal Chain

```
Upstream: IP development investment, Success Program maturity, CSA enablement
    → Repeatable Delivery (THIS)
        → Downstream: Cost-to-serve, Scalability, On-Strategy Delivery
```

# Source Systems

- **CES Delivery Insights** — engagement classification (repeatable vs bespoke)

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| CES Delivery Insights | `56064262-fdfa-4c3d-968f-dffd3ebf759a` | Engagement classification (repeatable vs bespoke) via delivery tagging |

**Investigation:** Filter `labor-month` results by engagement classification tag. Repeatable engagements are tagged with Success Program or IP-based delivery patterns.

See also: [Delivery Evidence](/csu/evidence/delivery-evidence.md)