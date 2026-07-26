---
type: Framework
title: Integrated Customer Planning (ICP)
id: mcem.planning.integrated-customer-planning-icp
description: Cross-org orchestration and governance framework integrating Account Planning, Consumption Planning, Customer Success Planning, and Relationship Governance.
tags: [mcem, icp, planning, orchestration, governance, cross-org]
relationships:
  - predicate: references
    object: mcem.planning.account-planning
  - predicate: references
    object: mcem.planning.customer-success-planning
  - predicate: references
    object: mcem.planning.consumption-planning
  - predicate: references
    object: mcem.planning.customer-relationship-governance
  - predicate: references
    object: mcem.planning.icp-planning-taxonomy
  - predicate: references
    object: csu.planning.customer-success-plan-csp
  - predicate: references
    object: csu.planning.account-plan
  - predicate: informs
    object: csu.pipeline.two-motion-model
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

Integrated Customer Planning (ICP) is the cross-org orchestration and governance framework that connects all Microsoft team members supporting a customer's full lifecycle. ICP integrates existing planning assets rather than creating a separate standalone process.

# The ICP Formula

```
Customer Plan = Account Plan + Consumption Plan + Customer Success Plan(s) + Governance Rhythm
```

# Four Disciplines

| Discipline | Owner | Purpose |
|------------|-------|---------|
| [Account Planning](/mcem/planning/account-planning.md) | ATU | Understand customer, articulate Microsoft value |
| [Consumption Planning](/mcem/planning/consumption-planning.md) | ATU/CSU | Pipeline sufficiency, MACC execution |
| [Customer Success Planning](/mcem/planning/customer-success-planning.md) | CSU | Accelerate value realization |
| [Customer Relationship Governance](/mcem/planning/customer-relationship-governance.md) | ATU/CSU | Validate progress, align stakeholders |

# Operating Principles

1. **Integration, not separation** — ICP connects existing planning assets; it is not a separate process
2. **Customer-anchored** — plans start from customer objectives, not Microsoft quota
3. **Quarterly validation** — anchored on quarterly reviews with the customer
4. **Continuous alignment** — not annual planning; always-on planning rhythms
5. **Cross-org coordination** — facilitates pipeline and resource allocation alignment across ATU, STU, CSU, GPS, ISD

# Relationship to MCEM

ICP provides the planning backbone for [MCEM](/mcem/methodology.md) execution. Without ICP, MCEM stage progression lacks the coordinated planning that ensures handoffs carry context and milestones connect to customer priorities.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — account plans, customer objectives, opportunities, and milestones provide the strategic and pipeline backbone.
- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — priorities, success plans, and RAID governance provide the execution planning layer.
