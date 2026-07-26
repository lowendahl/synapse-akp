---
type: Evidence Map
title: Delivery Evidence (UDC/UCR/Hours)
id: csu.evidence.delivery-evidence-udc-ucr-hours
description: Complete evidence path from delivery concepts (UDC, hours, packages) to their semantic models and investigation patterns.
tags: [csu, evidence, delivery, udc, hours, packages, semantic-model]
relationships:
  - predicate: references
    object: csu.evidence.mdm-grm-contract-and-resource-systems
  - predicate: references
    object: csu.evidence.msx-insights-msxi-analytics-measurement
  - predicate: references
    object: csu.metric.booked-hours
  - predicate: references
    object: csu.metric.remaining-hours
  - predicate: references
    object: csu.metric.requested-not-booked-hours
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
---
# Concepts

- **[UDC — Unified Delivery Coverage](/csu/delivery/udc.md)**: % of sold proactive services delivered/booked
- **[Remaining Hours](/csu/metrics/remaining-hours.md)**: Undelivered hours in contract
- **[Booked Hours](/csu/metrics/booked-hours.md)**: CSA hours scheduled
- **[Requested Not Booked](/csu/metrics/requested-not-booked.md)**: Unfilled demand

# Evidence Sources

## Primary: CES Delivery Insights

| Attribute | Value |
|-----------|-------|
| **PBI Artifact ID** | `56064262-fdfa-4c3d-968f-dffd3ebf759a` |
| **Friendly name** | CES Delivery Insights |
| **Grain** | Package × agreement × customer (UDC); Talent × customer × fiscal-month (Labor) |

### Key Tables

| Table | Purpose |
|-------|---------|
| `Package Details` | Active packages, offering names, EDE/STA classification |
| `Package Metrics` | Sold/consumed/prorated/remaining hours per package |
| `Agreement Details` | Unified contract metadata, dates, band |
| `Customer Details` | TPID, name, geography |
| `Delivery Metrics` | Delivered hours, logged hours, above-expectations |
| `Talent Hierarchy` | CSA/CSAM assignment, manager chain |
| `CSAM Hierarchy` | CSAM organizational roll-up |

### Key Measures

| Measure | What It Answers |
|---------|----------------|
| `[Sold Hours]` | Total package entitlement |
| `[Consumed Hours]` | Hours already delivered |
| `[Prorated Sold Hours]` | Expected delivery at this point in contract lifecycle |
| `[Delivered Hours]` | CSA technical delivery hours |
| `[Logged Hours]` | All logged time (including admin) |

### DAX Recipes

| Recipe | Purpose |
|--------|---------|
| `udc` | UDC per package × agreement × customer |
| `package-detail` | Full consumption metrics per active package |
| `package-risk` | Packages expiring soon OR low consumption |
| `ede-packages` | EDE-specific packages (for T-90 scoping analysis) |
| `labor-month` | CSA hours per talent × customer × month |
| `labor-month-by-manager` | CSA hours by manager's team |
| `customer-unified` | Unified contract flags: MIRP, CSDR, MACC, band |
| `customer-unified-hours` | Proactive UCR hours, ESA hours per TPID |
| `sp-eligibility` | Success Program eligibility flags per account |

# Investigation Patterns

## "What's our UDC — are we delivering what was sold?"

→ Recipe: `udc` — shows sold vs consumed vs prorated per package

## "Which packages are at risk of expiring undelivered?"

→ Recipe: `package-risk` with `expiry_days=90` — surfaces critical packages

## "How much demand is unstaffed?"

→ CES Staffing Insights (separate system — 4-hour refresh): requested not booked hours

## "What are our CSAs actually delivering?"

→ Recipe: `labor-month` or `labor-month-by-manager` — hours by talent/customer/month

## "Does this customer have MIRP? CSDR? Active MACC?"

→ Recipe: `customer-unified` — flags for MIRP, CSDR, CSDM, MACC, Priority, S500

# Related Evidence

- [Job 1 Evidence](/csu/evidence/job1-evidence.md) — CSA delivery drives milestone closure
- [MACC Evidence](/csu/evidence/macc-evidence.md) — EDE delivery drives MACC consumption
