---
type: Evidence Source
title: MDM & GRM — Contract and Resource Systems
id: csu.evidence.mdm-grm-contract-and-resource-systems
aliases: [MDM, GRM, Master Data Management, Global Resource Management, ROSS]
description: Operational systems accessed via eSXP APIs for Unified contract management (MDM) and CSA resource booking/scheduling (GRM). System of record for what was sold (MDM) and who is booked where (GRM).
tags: [csu, evidence, mdm, grm, contracts, bookings, staffing, unified, resources]
relationships:
  - predicate: references
    object: csu.evidence.delivery-evidence-udc-ucr-hours
  - predicate: references
    object: mcem.unified.service-requests-bookings
  - predicate: references
    object: csu.metric.booked-hours
  - predicate: references
    object: csu.metric.remaining-hours
generated: { by: human:plwendahl, at: 2026-07-25T02:45:00Z }
status: stable
sources:
  - id: mdm-enhanced-solutions
    resource: "MDM Enhanced Solutions (Contract Packages)"
    title: MDM Contract API
    last_modified: 2026-07-20
  - id: grm
    resource: "GRM (Global Resource Management)"
    title: GRM Calendar API
    last_modified: 2026-07-01
---
# MDM — Master Data Management (Contracts)

## What MDM Is

MDM is the **contract system of record** for Unified Support deals, accessed via **eSXP API calls**. It stores the complete contract hierarchy: agreements, packages, offerings, and pricing. MDM is the authoritative source for "what did we sell this customer?"

## Key Data

| Entity | Purpose |
|--------|---------|
| **Contract** | Top-level agreement (contractId, TPID, opportunityId, dates) |
| **Package** | Line-item within contract (catalogName, pricing, dates) |
| **Enhanced Solutions** | EDE/STA packages identified by `categoryName = "2.6 Unified Enhanced Solutions"` |

## Critical Fields

| Field | What It Tells You |
|-------|-------------------|
| `catalogName` | Package type (e.g., "Enhanced Designated Engineering \| Azure IaaS") |
| `businessScenarioName` | Compact workload ID (e.g., "EDE Azure IaaS") |
| `customerPrice` | Package price in contract currency |
| `startDate` / `endDate` | Package coverage period |
| `categoryName` | Distinguishes Enhanced Solutions from base/reactive packages |

## Access

| Attribute | Value |
|-----------|-------|
| **Platform** | eSXP (API module) |
| **Connector** | eSXP CPQ API (MDM endpoints) |
| **Auth** | eSXP SPA bearer token (PRT-SSO) |

## Investigation Patterns

| Question | How |
|----------|-----|
| "What Enhanced Solutions does this customer have?" | Filter packages by `categoryName` containing "Enhanced Solutions" |
| "What's the workload breakdown?" | Parse `catalogName` after pipe (`\|`) for workload |
| "Which EDE packages need scoping?" | Cross-reference with [CES Staffing Insights](/csu/evidence/delivery-evidence.md) by contractId |
| "What's the total SBR pipeline for Security EDE?" | Join MDM packages (opportunityId) to billed pipeline model |

---

# GRM — Global Resource Management (Bookings)

## What GRM Is

GRM is the **CSA booking and scheduling system**, accessed via **eSXP API calls**. It is the authoritative source for WHO is booked WHERE and WHEN — the system of record for utilisation calculations and booking-conversion analysis.

## Key Data

| Entity | Purpose |
|--------|---------|
| **Calendar Item** | A single booking on a CSA's schedule (dates, customer, type) |
| **Staffing Request** | A demand request (ROSS) waiting to be assigned/booked |

## Critical Fields — Calendar Items

| Field | What It Tells You |
|-------|-------------------|
| `EventType` | 17 = Holiday; booking types for work |
| `BookingType` | 1 = booked work (DSE/Custom/MIP/Scoping) |
| `StartDate` / `EndDate` | Booking dates |
| `CustomerName` | Who the CSA is booked to |
| `DemandSourcePrefix` | ROSS = delivery request, RMOT = resource manager, SCOP = scoping |
| `RequestDomain` | Solution area / workload |
| `DeliveryType` | Type of delivery engagement |

## Critical Fields — Staffing Requests

| Field | What It Tells You |
|-------|-------------------|
| `ResourceRequestStatusEnum` | Active / Assigned / Booked / Completed / Cancelled |
| `RequestType` | Custom / MIP / DSEStaffing / Scoping |
| `Role` | CSA role requested |
| `RequestedSkills` | Required skills |
| `DeliveryCountryName` | Where delivery happens |

## Access

| Attribute | Value |
|-----------|-------|
| **Platform** | eSXP (API module) |
| **API** | eSXP Azure Front Door (`esxp-prod.azurefd.net/grm`) |
| **Auth** | PRT-SSO bearer token |
| **Calendar endpoint** | `POST /rm/api/v1/Calendar/GetCalendar` |
| **Search endpoint** | `POST /read/api/Search` |

## Investigation Patterns

| Question | How |
|----------|-----|
| "What is this CSA booked on?" | `GetCalendar` with alias + date window |
| "What demand is unassigned?" | Staffing request search with status = Active (not Assigned/Booked) |
| "How much free capacity does the team have?" | Fan-out calendar across all team aliases → compute free days |
| "What scoping requests are pending?" | Search with RequestType = Scoping, status = Active |
| "What's the booking-to-delivery conversion?" | Compare GRM booked hours vs CES Delivery Insights logged hours |

## ⚠️ Critical Rule

**Booked hours must be span-derived** from StartDate/EndDate (09:00-17:00 weekday, holiday-aware). **Never** use TotalDuration/DurationUnit — those are calendar-day approximations.

---

# Relationship to KPIs

| KPI | MDM Answers | GRM Answers |
|-----|-------------|-------------|
| [UDC](/csu/delivery/udc.md) | What was sold (package entitlements) | — |
| [Booked Hours](/csu/metrics/booked-hours.md) | — | What's scheduled (calendar bookings) |
| [Requested Not Booked](/csu/metrics/requested-not-booked.md) | — | Unfilled demand (staffing requests) |
| [Remaining Hours](/csu/metrics/remaining-hours.md) | Package sold hours (denominator) | — |
| [On-Strategy Delivery](/csu/metrics/on-strategy-delivery.md) | — | Booking strategy classification |
| [Scoping](/mcem/unified/scoping.md) | Which packages need scoping | Whether scoping requests exist |

# Relationship to PBI Models

| PBI Model | What MDM/GRM Feed It |
|-----------|---------------------|
| CES Delivery Insights | MDM agreement/package data → UDC calculation |
| CES Staffing Insights | GRM staffing requests → demand funnel |
| MS Billed Pipeline SBR | MDM contracts → billed pipeline values |
