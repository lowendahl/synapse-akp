---
type: Process
title: Customer Success Planning
id: mcem.planning.customer-success-planning
description: The ICP discipline of accelerating value realization by creating and executing Customer Success Plans tied to Customer Priorities.
tags: [mcem, icp, csp, success-planning, csu]
relationships:
  - predicate: belongs_to
    object: mcem.planning.integrated-customer-planning-icp
  - predicate: depends_on
    object: mcem.planning.account-planning
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
  - predicate: informs
    object: mcem.planning.customer-success-delivery-review-csdr
  - predicate: operationalizes
    object: csu.planning.customer-success-plan-csp
  - predicate: references
    object: csu.role.customer-success-account-manager-csam
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

Customer Success Planning is the [ICP](/mcem/planning/integrated-customer-planning.md) discipline where a specific customer initiative (documented as a Customer Priority) is selected to track pursuit and delivery work that leads to the customer realizing the priority's success criteria. The output is a [Customer Success Plan (CSP)](/csu/planning/customer-success-plan.md).

# Owner

[CSU](/mcem/organization/csu.md) — [CSAM](/csu/roles/csam.md) is accountable.

# Core Rules

1. **No CSP without a Customer Priority** — a CSP cannot be created without a parent Customer Priority in the Account Plan
2. **Done with the customer** — CSP planning is done in partnership with the customer, not internally
3. **CSAM accountable** — CSAM owns CSP creation, execution, and governance
4. **Monthly review minimum** — plans reviewed at least monthly with customer-facing team and delivery partners

# CSP Facilitates

- Agreement on intended outcomes
- Alignment between Microsoft and customer on activities
- Commitment to the projects needed to achieve desired outcomes

# Relationship to Other Disciplines

- **Account Planning** provides the Customer Priority that spawns a CSP
- **Consumption Planning** provides the pipeline context for MACC-aligned CSPs
- **Governance Rhythms** ([CSDR](/mcem/planning/csdr.md), [QBR](/mcem/planning/qbr.md)) review CSP progress

# Source Systems

- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — the authoritative success plans, priorities, RAID logs, and linked pipeline insights used for customer success planning.
