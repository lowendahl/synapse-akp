---
type: Role
title: Customer Success Architect (CSA)
id: csu.role.customer-success-architect-csa
description: The technical delivery and architecture lead within CSU, responsible for driving technical outcomes and deepening customer adoption.
tags: [csu, role, csa, technical, architecture, delivery]
relationships:
  - predicate: belongs_to
    object: mcem.organization.customer-success-unit-csu
  - predicate: belongs_to
    object: csu.delivery.csu-delivery-process
  - predicate: depends_on
    object: csu.planning.customer-success-plan-csp
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck"
    title: FY27 CE&S Manager Deck
    author: team:ces-leadership
    last_modified: 2026-07-01
---
# Definition

The Customer Success Architect (CSA) is the technical delivery and architecture lead within CSU. CSAs drive technical outcomes, deepen customer adoption, and provide architectural guidance across Azure, M365, Security, and AI workloads.

# FY27 Priorities

1. **Customer Centricity** — deep understanding of customer technical landscape
2. **Business Impact** — drive measurable technical outcomes tied to business value
3. **Technical Leadership** — architectural guidance, security posture, AI readiness

# Key Responsibilities

- Drive technical delivery of committed milestones
- Provide architectural guidance and Well-Architected reviews
- Support [Adoption Plans](/csu/pipeline/usage/adoption-plan.md) with technical enablement
- Assess and advance customer [Technical Maturity](/csu/doctrine/technical-maturity-model.md)
- Lead Security and AI readiness conversations

# Assignment Model

CSAs are assigned based on workload alignment and customer complexity. The assignment model balances coverage across the CSAM portfolio.

# Source Systems

- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — MDM shows the sold delivery packages and GRM shows the CSA bookings and staffing assignments.
