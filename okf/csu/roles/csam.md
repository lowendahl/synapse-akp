---
type: Role
title: Customer Success Account Manager (CSAM)
id: csu.role.customer-success-account-manager-csam
description: The primary customer relationship owner in CSU, responsible for executive partnership, health, cloud adoption, and Frontier Transformation.
tags: [csu, role, csam, relationship, customer-success]
relationships:
  - predicate: belongs_to
    object: mcem.organization.customer-success-unit-csu
  - predicate: belongs_to
    object: csu.delivery.csu-delivery-process
  - predicate: depends_on
    object: csu.planning.customer-success-plan-csp
  - predicate: informs
    object: csu.metric.customer-health-revenue-at-risk
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck"
    title: FY27 CE&S Manager Deck (slides 41–42)
    author: team:ces-leadership
    last_modified: 2026-07-01
---
# Definition

The Customer Success Account Manager (CSAM) is the primary customer relationship owner in CSU. The CSAM is responsible for executive partnership, customer health, cloud adoption, and [Frontier Transformation](/mcem/frontier-transformation.md).

# FY27 Priorities

1. **Customer Health** — stakeholder alignment, CSP, CSDR, value realization
2. **Consumption & Usage** — drive adoption, accelerate utilization
3. **Delivery Excellence** — orchestrate delivery, drive milestone completion

# Key Focus Areas

- Earn Customer Trust through stakeholder alignment, CSP, CSDR, and value realization
- Strengthen [Customer Health](/mcem/metrics/customer-health.md)
- Accelerate Cloud Adoption
- Advance AI Transformation via [Frontier Transformation](/mcem/frontier-transformation.md)

# Variants

| Variant | Segment | Focus |
|---------|---------|-------|
| Standard CSAM | Enterprise, SME&C | Full customer success model |
| Partner CSAM | Partners | Practice-building outcomes via [Unified for Partners](/csu/programs/unified-for-partners.md) |

# Accountability Model

- Owns [Customer Success Plan](/csu/planning/customer-success-plan.md)
- Drives [QBR](/csu/planning/integrated-customer-planning.md) cadence
- Accountable for [Commit-to-Complete](/csu/processes/commit-to-complete.md) milestone execution
- Orchestrates [CSA](/csu/roles/csa.md) and delivery resources

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — CSAM ownership of account plans, opportunities, and milestone execution accountability.
- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — scoping, package, and booking context the CSAM coordinates to get delivery resources engaged.
- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — the success plans, priorities, and RAID governance the CSAM owns with the customer.
