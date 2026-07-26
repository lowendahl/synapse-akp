---
type: Process
title: Account Planning
id: mcem.planning.account-planning
description: The always-on process where account teams develop understanding of the customer and articulate how Microsoft helps achieve their goals.
tags: [mcem, icp, account-planning, strategy, atu]
relationships:
  - predicate: belongs_to
    object: mcem.planning.integrated-customer-planning-icp
  - predicate: informs
    object: mcem.planning.customer-success-planning
  - predicate: informs
    object: mcem.planning.consumption-planning
  - predicate: informs
    object: mcem.planning.customer-relationship-governance
  - predicate: operationalizes
    object: csu.planning.account-plan
  - predicate: informs
    object: csu.planning.customer-success-plan-csp
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

Account Planning is the always-on process where account teams develop a real understanding of the customer organization and priorities, then articulate how Microsoft can help the customer achieve strategic and business goals. It is one of the four [ICP](/mcem/planning/integrated-customer-planning.md) disciplines.

# Owner

[ATU](/mcem/organization/atu.md) — with cross-team collaboration (One Microsoft).

# High-Quality Account Planning Includes

1. **One Microsoft cross-team collaboration** — ATU, STU, CSU, GPS, ISD aligned
2. **Continuous planning** — not annual; always-on rhythms
3. **Customer and industry insights** — external context driving strategy
4. **Customer Priorities and 3-horizon roadmap** — strategic direction mapped
5. **Customer relationships** — stakeholder map and Rooms of the House
6. **Partners and competitors** — mapped to priorities
7. **Services and Unified Support strategy** — aligned to account
8. **Pipeline and CSPs aligned** — execution connected to strategy

# Output

The [Account Plan](/csu/planning/account-plan.md) artifact in MSX — the strategic container from which all other planning flows.

# Key Rule

The Account Plan is the source of Customer Objectives and Customer Priorities. No [CSP](/csu/planning/customer-success-plan.md) or [Consumption Plan](/mcem/planning/consumption-planning.md) can exist without connection to the Account Plan.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the authoritative account plan, customer objective, and account-plan priority records used in MCEM planning.
