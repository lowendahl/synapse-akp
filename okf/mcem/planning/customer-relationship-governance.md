---
type: Process
title: Customer Relationship Governance
id: mcem.planning.customer-relationship-governance
description: The customer-facing governance rhythms across all account teams, defining how progress is validated and alignment maintained.
tags: [mcem, icp, governance, rhythms, qbr, csdr]
relationships:
  - predicate: belongs_to
    object: mcem.planning.integrated-customer-planning-icp
  - predicate: evidenced_by
    object: mcem.planning.quarterly-business-review-qbr
  - predicate: evidenced_by
    object: mcem.planning.customer-success-delivery-review-csdr
  - predicate: informs
    object: mcem.stage.stage-5-manage-optimize
  - predicate: references
    object: csu.role.customer-success-account-manager-csam
  - predicate: informs
    object: csu.priority.earn-customer-trust
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: customer-integrated-planning-okf
    resource: "Customer Integrated Planning OKF corpus"
    title: Customer Integrated Planning OKF Corpus
    author: team:mcaps-strategy
    last_modified: 2026-07-19
---
# Definition

Customer Relationship Governance defines the customer-facing governance rhythms across all teams involved in the account, including partners. It is one of the four [ICP](/mcem/planning/integrated-customer-planning.md) disciplines and is not separate from planning — governance IS planning in action.

# Owner

[ATU](/mcem/organization/atu.md) (QBR) + [CSU](/mcem/organization/csu.md) (CSDR).

# Purpose

Validate priorities, roadmap progress, outcomes, value realization, customer health, support performance, resource alignment, stakeholder engagement, and delivery execution.

# Primary Rhythms

| Rhythm | Cadence | Owner | Purpose |
|--------|---------|-------|---------|
| [CSDR](/mcem/planning/csdr.md) | Monthly+ | CSU/CSAM | Execution governance |
| [QBR](/mcem/planning/qbr.md) | Quarterly | ATU | Strategic relationship governance |
| Executive Sponsor Engagement | Ongoing | ATU/CSU | C-level alignment |

# Governance Principles

1. Internal Microsoft rhythms align to monthly and quarterly customer reviews
2. Strategic accounts include executive sponsor participation in ≥2 QBRs annually
3. Governance is not separate from planning — it validates and adjusts plans
4. All teams contribute: ATU, STU, CSU, GPS, ISD, Partners

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — account-plan, opportunity, and milestone status reviewed in governance cadences.
- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — plan status, priorities, and RAID items governed through the customer relationship rhythm.
