---
type: Taxonomy
title: ICP Planning Taxonomy
id: mcem.planning.icp-planning-taxonomy
description: Authoritative definitions of all Integrated Customer Planning terms, from Customer Objective to Delivery Project.
tags: [mcem, icp, taxonomy, definitions, planning]
relationships:
  - predicate: belongs_to
    object: mcem.planning.integrated-customer-planning-icp
  - predicate: references
    object: mcem.planning.account-planning
  - predicate: references
    object: mcem.planning.customer-success-planning
  - predicate: references
    object: mcem.planning.consumption-planning
  - predicate: references
    object: mcem.planning.customer-relationship-governance
  - predicate: references
    object: csu.planning.customer-success-plan-csp
  - predicate: informs
    object: csu.pipeline.adoption-plan
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: customer-integrated-planning-okf
    resource: "Customer Integrated Planning OKF corpus"
    title: Customer Integrated Planning OKF Corpus
    author: team:mcaps-strategy
    last_modified: 2026-07-19
---
# Planning Taxonomy

Authoritative definitions of all terms within [Integrated Customer Planning](/mcem/planning/integrated-customer-planning.md).

## Orchestration & Planning

| Term | Definition |
|------|-----------|
| **Orchestration** | Coordinating work across people and roles to achieve customer outcomes |
| **Customer Planning** | Account Plan + CSP portfolio + Consumption Plan — kept complete and reviewed |
| **Account Planning** | Ongoing process for understanding customer context and articulating Microsoft value |
| **Account Plan** | Account-level plan for delivering value and revenue; the strategic container |

## Customer Strategy Objects

| Term | Definition |
|------|-----------|
| **Customer Objective** | Long-term strategic goal the customer is pursuing (business outcome level) |
| **Customer Priority** | A specific initiative aligned to one or more objectives (execution level) |
| **Customer Success Criteria** | Customer-agreed KPIs that define success for a priority |

## Success Planning

| Term | Definition |
|------|-----------|
| **Customer Success Planning** | The discipline of accelerating value realization through structured plans |
| **Customer Success Plan (CSP)** | Program container of activities, projects, and milestones aligned to a Customer Priority |
| **Customer Success Portfolio** | The collection of all CSPs for one customer |
| **Delivery Project** | Execution activities within a CSP (the tactical doing) |

## Consumption Planning

| Term | Definition |
|------|-----------|
| **Consumption Planning** | Pipeline sufficiency check + execution ROB against consumption targets |
| **Consumption Plan** | MSX reporting view of expected vs target consumption; must exist for all MACCs |

# Hierarchy

```
Customer Objective
  └── Customer Priority
       └── Customer Success Plan (CSP)
            └── Delivery Project(s)
                 └── Milestone(s)
```

# Key Rule

A CSP cannot be created without a parent Customer Priority in the Account Plan. Plans flow from strategy (objectives) through priorities to execution (CSPs), never the reverse.
