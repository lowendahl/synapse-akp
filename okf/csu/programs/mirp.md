---
type: Program
title: MIRP — Microsoft Internal Revenue Plan
id: csu.program.mirp-microsoft-internal-revenue-plan
aliases: [MIRP, Microsoft Internal Revenue Plan]
description: Flag on Unified accounts indicating they have been identified for proactive CSA planning and investment. Drives prioritized delivery engagement, ECIF eligibility, and success program enrollment.
tags: [csu, programs, mirp, proactive, unified, delivery, prioritization]
relationships:
  - predicate: informs
    object: csu.program.ecif-enterprise-customer-investment-fund
  - predicate: informs
    object: csu.program.success-programs
  - predicate: references
    object: csu.planning.customer-success-plan-csp
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
sources:
  - id: ces-delivery-insights
    resource: "CES Delivery Insights semantic model"
    title: CES Delivery Insights
    last_modified: 2026-07-01
---
# Definition

**MIRP (Microsoft Internal Revenue Plan)** is an internal flag on Unified/Premier customers indicating they have been selected for proactive success management planning. MIRP accounts receive heightened CSA engagement, priority scoping, and are first in line for ECIF investment.

# Purpose

- Prioritizes CSA proactive delivery to high-value accounts
- Gates eligibility for [ECIF](/csu/programs/ecif.md) investment
- Drives [Success Program](/csu/programs/success-programs.md) enrollment
- Informs [CSP](/csu/doctrine/csp-hierarchy.md) intensity and milestone planning

# Eligibility Criteria

| Factor | Requirement |
|--------|-------------|
| Active Unified contract | Mandatory |
| Revenue threshold | Typically top-quartile by ACR or MACC |
| Strategic importance | S500, high-growth, or strategic partnership |
| Refresh cadence | Semi-annual (MIRP refresh) |

# MIRP Signals in Data

The `customer-unified` recipe in [CES Delivery Insights](/csu/evidence/delivery-evidence.md) surfaces the MIRP flag:

```
Has MIRP = TRUE → account is MIRP-designated
MIRP Refresh Due = TRUE → MIRP designation expiring, needs renewal
```

# Relationship to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [ECIF](/csu/programs/ecif.md) | MIRP is often a prerequisite for ECIF approval |
| [CSP Hierarchy](/csu/doctrine/csp-hierarchy.md) | MIRP accounts get more intensive CSP planning |
| [Scoping](/mcem/unified/scoping.md) | MIRP accounts get priority EDE/STA scoping |
| [CSDR](/mcem/planning/csdr.md) | MIRP accounts are always on the CSDR agenda |
| [Success Programs](/csu/programs/success-programs.md) | MIRP gates program eligibility |

# Evidence

| Source | Table/Measure | What It Shows |
|--------|--------------|---------------|
| CES Delivery Insights | `customer-unified` recipe | MIRP flag per TPID |
| CES Delivery Insights | `sp-eligibility` recipe | MIRP + MIRP Refresh Due flags |
| MACC ACR Acceleration | `macchealthscoredetails` | MIRP accounts overlap heavily with MACC health |
