---
type: Contract Model
title: Unified Support
id: mcem.unified.unified-support
description: Microsoft's premier support offering combining reactive support, proactive services, Enhanced Solutions, and designated engineering into a single contract.
tags: [unified, support, contract, proactive, reactive, ede]
relationships:
  - predicate: references
    object: mcem.unified.enhanced-solutions-ede-sta
  - predicate: references
    object: mcem.unified.service-requests-bookings
  - predicate: references
    object: mcem.unified.unified-consumed-revenue-ucr
  - predicate: references
    object: csu.delivery.csu-delivery-process
  - predicate: references
    object: csu.delivery.udc-unified-delivery-coverage
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: macc-consumption-planning-okf
    resource: "MACC Consumption Planning OKF corpus"
    title: MACC Consumption Planning OKF Corpus
    last_modified: 2026-07-20
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck"
    title: FY27 CE&S Manager Deck
    author: team:ces-leadership
    last_modified: 2026-07-01
---
# Definition

Unified Support is Microsoft's premier support offering that combines reactive break-fix support, proactive services, [Enhanced Solutions](/mcem/unified/enhanced-solutions.md) (EDE/STA packages), and designated engineering into a single contract. It is the delivery vehicle through which CSU provides proactive customer value.

# Contract Components

| Component | Type | Purpose |
|-----------|------|---------|
| Reactive Support | Break-fix | Incident resolution, case management |
| Proactive Services | Preventative | Assessments, workshops, health checks |
| Enhanced Solutions (EDE) | Designated | Named CSA engineering aligned to outcomes |
| Support Technical Advisor (STA) | Advisory | Technical planning and delivery oversight |
| Success Programs | Programmatic | Scalable multi-touch engagement programs |

# MACC Quality Gate Alignment

Unified alignment is **Gate 5** of the [six MACC quality gates](/mcem/planning/macc.md):
- Unified contract must be in place
- Purple Empowerment minimum: ≥1% of annualized MACC value in Enhanced Solutions
- Sub-1% requires a Purple Empowerment exception

# Commercial Model

- Sold as annual contracts (typically aligned to MACC/EA terms)
- Enhanced Solutions sold as hour-based packages within the Unified contract
- Revenue recognized through [Unified Consumed Revenue (UCR)](/mcem/unified/consumed-revenue.md)
- Contract value covers both reactive and proactive components

# Delivery Execution

Unified contract delivery is executed through:
1. [CSAM](/csu/roles/csam.md) — owns the customer relationship and orchestrates delivery
2. [CSA](/csu/roles/csa.md) — executes EDE/STA technical delivery
3. [Scoping](/mcem/unified/scoping.md) — translates sold packages into delivery plans
4. [Service Requests](/mcem/unified/service-requests-bookings.md) — governs staffing and booking lifecycle

# Relationship to MCEM

Unified Support underpins [Stages 3–5](/mcem/stages/) of MCEM by providing the delivery resources and commercial framework through which CSU drives value realization, optimization, and renewal.

# Source Systems

- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — MDM contract and package hierarchy is the operational source for Unified Support coverage and entitlements.
