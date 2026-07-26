---
type: KPI
title: "Booked Hours"
id: csu.metric.booked-hours
description: CSA hours scheduled (booked) against active delivery engagements — measures staffing coverage and forward delivery capacity.
tags: [csu, kpi, booked-hours, staffing, capacity, delivery, diagnostic]
relationships:
  - predicate: measures
    object: csu.delivery.csu-delivery-process
  - predicate: measures
    object: mcem.unified.service-requests-bookings
  - predicate: evidenced_by
    object: csu.evidence.delivery-evidence-udc-ucr-hours
classification: diagnostic
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-staffing-insights
    resource: "CES Staffing Insights"
    title: Booking Status Tracking
    last_modified: 2026-07-01
---
# Definition

**Booked Hours** measures CSA hours that are scheduled (booked) against active delivery engagements. It indicates forward delivery capacity allocation and staffing coverage health.

**Classification: DIAGNOSTIC** — tells you staffing utilization health, combining elements of both leading (capacity) and lagging (commitment).

# Relationship to Other Hour Metrics

```
Sold Hours = Consumed Hours + Remaining Hours
Remaining Hours = Booked Hours (future) + Unbooked Hours (gap)
```

| Metric | What It Measures |
|--------|-----------------|
| Sold Hours | Total contract entitlement |
| Consumed Hours | Already delivered |
| Booked Hours (this) | Scheduled for future delivery |
| Remaining Hours | Total undelivered |
| Requested Not Booked | Demand without assignment |

# Causal Chain

```
Upstream: Scoping completion, CSA assignment, ROSS staffing
    → Booked Hours (THIS)
        → Downstream: Delivery execution cadence, UDC trajectory, Consumed hours velocity
```

# Source Systems

- **CES Staffing Insights** — booking status, CSA schedules
- **ROSS / GRM** — project scheduling, resource allocation

# Evidence Path

| Source | Artifact ID | Purpose |
|--------|------------|---------|
| CES Staffing Insights | `3d1501b1-c8d4-4c4e-b724-116dc7c6e9ce` | Staffing requests: assigned + booked status |
| CES Delivery Insights | `56064262-fdfa-4c3d-968f-dffd3ebf759a` | `package-detail` recipe: booked-undelivered hours per package |

**Investigation:** CES Staffing Insights shows the staffing funnel (requested → assigned → booked). CES Delivery Insights shows per-package booking status via the `package-detail` recipe.

See also: [Delivery Evidence](/csu/evidence/delivery-evidence.md)