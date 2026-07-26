---
type: KPI
title: "Requested Not Booked Hours"
id: csu.metric.requested-not-booked-hours
description: Staffing requests without CSA assignment — measures demand-supply gap and staffing bottleneck severity.
tags: [csu, kpi, requested-not-booked, staffing, capacity, gap, leading]
relationships:
  - predicate: measures
    object: csu.delivery.csu-delivery-process
  - predicate: measures
    object: mcem.unified.service-requests-bookings
  - predicate: evidenced_by
    object: csu.evidence.delivery-evidence-udc-ucr-hours
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-staffing-insights
    resource: "CES Staffing Insights"
    title: Unstaffed Demand Tracking
    last_modified: 2026-07-01
---
# Definition

**Requested Not Booked Hours** measures staffing demand (delivery requests and scoping requests) that have NOT yet been matched with a CSA assignment. It is the demand-supply gap in the delivery workforce.

**Classification: LEADING** — high unstaffed demand predicts future delivery delays, UDC shortfall, and customer outcome risk.

# Formula

```
Requested Not Booked = Σ Hours (Active staffing requests without CSA assignment)
```

# Risk Signal

| Volume | Signal |
|--------|--------|
| < 10% of total demand | Healthy — staffing keeping pace |
| 10–25% | Watch — capacity pressure building |
| > 25% | Critical — delivery delays certain; UDC at risk |

# Causal Chain

```
Upstream: Scoping volume, Renewal pipeline (T-90), CSA headcount, Skill availability
    → Requested Not Booked (THIS)
        → Downstream: Delivery delays, Remaining hours growth, UDC decline, Customer dissatisfaction
```

# Management Actions

When Requested Not Booked hours are elevated:
1. Prioritize by contract value and renewal proximity
2. Cross-skill CSAs or bring partner delivery
3. Escalate capacity constraints to SSM/leadership
4. Defer lower-priority scoping to next cycle

# Source Systems

- **CES Staffing Insights** — staffing request status, unfilled demand
- **ROSS** — resource availability, skills matching gaps

# Evidence Path

| Source | Artifact ID | Purpose |
|--------|------------|---------|
| CES Staffing Insights | `3d1501b1-c8d4-4c4e-b724-116dc7c6e9ce` | Staffing demand funnel: requests without booking/assignment |

**Domain model:** A staffing request with status = "Requested" (not yet "Assigned"/"Booked") IS the demand gap signal. Filter by Role=CSA and Engagement Type to scope.

**Grain:** Project Request (ROSS demand) × resource assignment status.