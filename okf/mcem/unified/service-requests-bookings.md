---
type: Process
title: Service Requests & Bookings
id: mcem.unified.service-requests-bookings
description: The ROSS staffing request and booking lifecycle governing how delivery resources are requested, assigned, and scheduled.
tags: [unified, service-requests, bookings, staffing, ross, delivery]
relationships:
  - predicate: operationalizes
    object: mcem.unified.enhanced-solutions-ede-sta
  - predicate: depends_on
    object: mcem.unified.unified-support
  - predicate: depends_on
    object: csu.delivery.csu-delivery-process
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ede-sta-scoping-okf
    resource: "EDE/STA Scoping OKF corpus"
    title: EDE/STA Scoping Process Documentation
    last_modified: 2026-07-20
---
# Definition

Service Requests and Bookings are the operational mechanisms through which delivery resources are requested, matched, assigned, and scheduled for [Enhanced Solutions](/mcem/unified/enhanced-solutions.md) execution. The staffing request in CES Staffing Insights is the system-of-record evidence that scoping and delivery have been initiated.

# Request Types

| Type | Purpose | Typical Actor |
|------|---------|--------------|
| Scoping Request | Initiate EDE/STA scoping engagement | CSAM |
| Delivery Request | Request ongoing technical delivery | Scoping Lead / CSA |
| Staffing Request | ROSS request for CSA assignment | Resource Manager |

# Staffing Request Lifecycle

```
CSAM Creates Request → Validation → Routing → CSA Matching → Assignment → Booking → Delivery
```

| Phase | System | Key Fields |
|-------|--------|-----------|
| Request Creation | CES Staffing Insights | Role (CSA), Offering Name, Engagement Type, Contract ID |
| Routing | ROSS | Skills match, geography, availability |
| Assignment | ROSS | CSA assigned (incumbent-first preference) |
| Booking | GRM/ROSS | Start/end dates, hours allocated |
| Delivery | CES Delivery Insights | Hours consumed, outcomes tracked |

# Key Fields on Staffing Request

| Field | Purpose |
|-------|---------|
| Role | Must contain "CSA" for EDE/STA delivery |
| Offering Name | References the EDE workload |
| Engagement Type | Scoping / Advisory / Delivery |
| Contract ID | Links to MDM contract (braavosAgreementNumber) |
| Requested Start Date | Drives T-90 gate calculation |

# Auto-Create Signal

RMEx can auto-create a support need approximately 180 days before renewal (T-180 auto-create), feeding the staffing demand pipeline materially earlier than CSAM-initiated scoping.

# Booking Governance

- Incumbent-first staffing: existing CSA assigned to customer retains priority
- Skills matching: product skill and solution-area alignment required
- Capacity management: tracked in CES Staffing Insights by geography and resource skill
- Unstaffed monitoring: requests without assignment trigger escalation

# Source Systems

- **CES Staffing Insights** — demand, staffing state, capacity, contract consumption (4-hour refresh)
- **ROSS** — resource orchestration and scheduling
- **GRM** — project and booking management
- **Support Delivery** — request creation and validation
