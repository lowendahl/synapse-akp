---
type: Delivery Offering
title: Enhanced Solutions (EDE/STA)
id: mcem.unified.enhanced-solutions-ede-sta
description: Premium Unified Support add-on assigning named engineering resources for proactive, outcome-aligned technical delivery within a solution area.
tags: [unified, ede, sta, enhanced-solutions, delivery, csa, designated-engineering]
relationships:
  - predicate: belongs_to
    object: mcem.unified.unified-support
  - predicate: depends_on
    object: mcem.unified.ede-sta-scoping
  - predicate: depends_on
    object: mcem.unified.service-requests-bookings
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: references
    object: csu.delivery.delivery-engine-routing
  - predicate: references
    object: csu.program.success-enablement-services-esa
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ede-sta-scoping-okf
    resource: "EDE/STA Scoping OKF corpus"
    title: EDE/STA Scoping Process Documentation
    last_modified: 2026-07-20
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck"
    title: FY27 CE&S Manager Deck
    author: team:ces-leadership
    last_modified: 2026-07-01
---
# Definition

Enhanced Designated Engineering (EDE) and Support Technical Advisor (STA) are premium [Unified Support](/mcem/unified/unified-support.md) add-on packages that assign a named engineering resource (a [CSA](/csu/roles/csa.md)) to a customer for proactive, outcome-aligned technical delivery within a solution area.

# EDE vs STA

| Offering | Resource | Focus |
|----------|----------|-------|
| EDE (Enhanced Designated Engineering) | Named CSA | Hands-on technical delivery, architecture, implementation |
| STA (Support Technical Advisor) | Technical Advisor | Planning, delivery oversight, advisory guidance |

Both are sold as package/contract line items within Unified Support and require [scoping](/mcem/unified/scoping.md) before delivery execution begins.

# Package Taxonomy

Enhanced Solutions are categorized by solution area:
- **Security** — identity, compliance, threat protection
- **Cloud & AI** — Azure infrastructure, data, AI/ML
- **AI Business Solutions** — Copilot, business applications
- **Modern Work** — M365, Teams, collaboration

# Commercial Structure

| Dimension | Detail |
|-----------|--------|
| Sold as | Hour-based packages within Unified contract |
| Contract link | Package line item in MDM (braavosAgreementNumber) |
| Pricing unit | Support Assist Hours |
| Consumption tracking | Sold hours vs consumed hours in CES Delivery Insights |
| Revenue model | [UCR](/mcem/unified/consumed-revenue.md) — delivery drives revenue recognition |

# Lifecycle

```
Package Sold → Scoping Initiated → CSA Assigned → Delivery Executed → Hours Consumed → Renewal Scoping
```

1. Package sold as part of Unified contract negotiation
2. [Scoping](/mcem/unified/scoping.md) initiated by CSAM (T-90 rule applies)
3. CSA assigned via [ROSS staffing request](/mcem/unified/service-requests-bookings.md)
4. Delivery executed against scoped outcomes
5. Hours consumed and tracked in CES Delivery Insights
6. Renewal scoping begins per [T-minus motion](/csu/processes/t-minus-renewal.md)

# MACC Alignment

Enhanced Solutions are a mandatory component of MACC quality ([Gate 5](/mcem/planning/macc.md)): Purple Empowerment minimum requires ≥1% of annualized MACC value invested in Enhanced Solutions.

# Source Systems

- **MDM** — contract metadata, package taxonomy, effective dates
- **CES Delivery Insights** — active packages, sold/consumed hours, package risk
- **CES Staffing Insights** — scoping requests, delivery requests, staffing state
