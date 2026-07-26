---
type: Metric
title: "UDC — Unified Delivery Coverage"
id: csu.delivery.udc-unified-delivery-coverage
description: Percentage of prorated Proactive Add-on and Enhanced Solution services delivered or booked with pre-billing at a given point in the contract lifecycle.
tags: [csu, kpi, delivery, coverage, unified, ede, consumption, proactive]
relationships:
  - predicate: measures
    object: csu.delivery.csu-delivery-process
  - predicate: measures
    object: mcem.unified.enhanced-solutions-ede-sta
  - predicate: evidenced_by
    object: csu.evidence.delivery-evidence-udc-ucr-hours
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-delivery-insights
    resource: "https://aka.ms/CES-DeliveryInsights"
    title: CES Delivery Insights
    last_modified: 2026-07-01
  - id: csu-fy26-leader-kpis
    resource: "FY26 CSU Leader KPI Pack"
    title: "FY26 CSU Leader Priority KPIs (#10)"
    last_modified: 2026-04-27
---
# Definition

**Unified Delivery Coverage (UDC)** measures the percentage of prorated Proactive Add-on and [Enhanced Solutions](/mcem/unified/enhanced-solutions.md) services that have been either delivered or booked with pre-billing at a specific point in the contract lifecycle.

**Plain language:** Of the proactive services a customer purchased, how much have we actually delivered (or locked in via pre-billing) by now?

# Formula

```
UDC % = (Delivered Hours + Pre-billed Booked Hours) / Prorated Entitled Hours
```

## Logical Steps

1. Identify in-scope Proactive Add-on / Enhanced Solution entitlements within an active [Unified contract](/mcem/unified/unified-support.md)
2. Prorate entitlement to the current point in the contract lifecycle
3. Sum delivered + pre-billed booked hours
4. Divide by prorated entitlement

# Thresholds

| Zone | Meaning |
|------|---------|
| ≥ 95% | On target — delivery pacing healthy |
| 85–94% | Watch — pacing risk, intervention needed |
| < 85% | Off-track — outcome and renewal risk |

# Business Rules

- **Inclusion:** Proactive Add-on and Enhanced Solution services within an active Unified contract
- **Exclusion:** Reactive support hours; non-Unified contracts
- **Qualification:** Service is prorated against contract lifecycle position
- **Aggregation:** By CSU, Area, Sub, contract

# Semantic Interpretation

| Tells You | Does NOT Tell You |
|-----------|-------------------|
| Whether delivery is keeping pace with what was sold | Whether delivery produced the intended customer outcome |
| Where to accelerate delivery or pre-billing | Whether content was right-fit for the customer |

# Leading / Lagging Context

- **Type:** Lagging
- **Upstream signals:** Delivery scheduling, CSA capacity, On-Strategy Delivery mix
- **Downstream outcomes:** Customer outcomes, renewal posture, [Customer Health Revenue at Risk](/mcem/risks/)

# Known Limitations

- Pre-billed bookings can mask actual delivery gaps
- Proration sensitivity at contract start/end
- High UDC ≠ proof of customer value realized (coverage ≠ outcome)

# Relationship to CSU Operating Model

UDC is the coverage accountability metric that answers "are we delivering what we sold?" It connects:
- [Scoping](/mcem/unified/scoping.md) → delivery plans feed the hours pipeline
- [Service Requests](/mcem/unified/service-requests-bookings.md) → CSA booking drives delivered hours
- [UCR](/mcem/unified/consumed-revenue.md) → consumed hours drive revenue recognition
- [Renewal Rate](/mcem/risks/renewal-rate.md) → healthy UDC correlates with higher renewal

# Source Systems

- **CES Delivery Insights** — authoritative system-of-record
- **MDM** — contract entitlements and proration

# Evidence Path

For full semantic model access and DAX recipes see: **[Delivery Evidence](/csu/evidence/delivery-evidence.md)**

| Source | Artifact ID | Key Recipe |
|--------|------------|-----------|
| CES Delivery Insights | `56064262-fdfa-4c3d-968f-dffd3ebf759a` | `udc` (package × agreement × customer hours) |

**Additional recipes:** `package-detail`, `package-risk`, `ede-packages`
