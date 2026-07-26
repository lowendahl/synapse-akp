---
type: Process
title: EDE/STA Scoping
id: mcem.unified.ede-sta-scoping
description: The process of translating sold Enhanced Solutions packages into actionable delivery plans through structured CSA scoping engagements.
tags: [unified, scoping, ede, sta, csa, delivery-planning, t-90]
relationships:
  - predicate: operationalizes
    object: mcem.unified.enhanced-solutions-ede-sta
  - predicate: depends_on
    object: mcem.unified.service-requests-bookings
  - predicate: operationalizes
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

EDE/STA Scoping is the process of capturing a customer's engagement focus, outcomes, pain points, technology footprint, value statement, delivery needs, and staffing requirements so [Enhanced Solutions](/mcem/unified/enhanced-solutions.md) delivery can align to customer-defined outcomes before delivery begins.

# Scoping Request Lifecycle

| Step | Actor | Activity |
|------|-------|----------|
| 1. Initiation | [CSAM](/csu/roles/csam.md) | Creates scoping request in Support Delivery, linking MSX opportunity, package, offering, skill |
| 2. Validation | Services Seller | Validates against sold package (hours, offering, service name), deal context |
| 3. Assignment | Scoping Lead / RM | Routes to CSA with matching product skill and solution-area fit |
| 4. Execution | [CSA](/csu/roles/csa.md) | Performs scoping: defines workload scope, hours, deliverables |
| 5. Outcome | CSA | Scope Completed recorded; delivery requests created |

# T-90 Rule

**Mandatory gate:** Enhanced Solutions packages must be scoped no later than 90 days before the contract effective date.

```
T-90 Gate: lead_days = effective_date − scoping_received_date ≥ 90
```

When this gate fails, the package is "late-scoped" — delivery plan may be incomplete at contract start, risking poor outcomes and delayed value.

# Segment-Specific Timing

| Segment | Scoping Begins | Manager Checkpoint |
|---------|---------------|-------------------|
| Enterprise | T-9 months (CSAM initiated) | SSM reviews at T-6 |
| DES Majors Growth | T-6 (CSAM initiates at T-5) | DES-M reviews at T-6 |
| SME&C | Within CSDR cadence | As part of key CSDRs |

# Quality Gates

- Support Need linked; Opportunity linked
- Required fields completed (DSE/STA selection, Package Name, Offering, Product Component, Price in Hours, date range, scoping hours ≤ 4, Request Information, Value Statement)
- Request submitted and SCOP ID generated
- Routed for staffing (ROSS/CES Staffing Insights request created)
- Scope Completed flag/date populated
- Delivery requests created

# Status Classification (Per-Package)

| Status | Definition |
|--------|-----------|
| **Unscoped** | No aligned scoping request found within temporal window |
| **Covered** | Scoping request matched + T-90 gate passes |
| **Uncovered** | Scoping request exists but no matching delivery outcome |
| **Stale Scoping** | Scoping from prior contract cycle only |
| **No EDE Outcome** | Contract plan has no DSE Delivery items |

# Business Impact

15–20% higher sales attach when experienced scoping leads join pre-sales calls. Better-scoped engagements correlate with higher CSAT, faster staffing turnaround, higher contract consumption, higher renewal likelihood, and higher product/licensing usage.

# Source Systems

- **CES Staffing Insights** — authoritative system of record for scoping requests
- **CES Delivery Insights** — package details and consumption status
- **MDM Enhanced Solutions** — contract metadata and effective dates
