---
type: Organization
title: Customer Success Unit (CSU)
id: mcem.organization.customer-success-unit-csu
description: The Microsoft field organization accountable for post-commitment execution, value realization, and renewal across MCEM Stages 3–5.
tags: [csu, organization, customer-success, execution]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
  - predicate: operationalizes
    object: mcem.stage.stage-5-manage-optimize
  - predicate: depends_on
    object: mcem.planning.customer-success-planning
  - predicate: references
    object: csu.priority.csu-fy27-priorities
  - predicate: references
    object: csu.role.customer-success-account-manager-csam
  - predicate: references
    object: csu.role.customer-success-architect-csa
  - predicate: references
    object: csu.delivery.delivery-engine-routing
  - predicate: references
    object: csu.metric.job-1-commit-to-complete-c2c
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-fy27-changes
    resource: "FY27 Strategy and Landing — MCEM Summary of Changes"
    title: FY27 MCEM Summary of Changes
    author: team:mcaps-strategy
    last_modified: 2026-07-01
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck"
    title: FY27 Customer Experience & Success Manager Deck
    author: team:ces-leadership
    last_modified: 2026-07-01
---
# Definition

The Customer Success Unit (CSU) is the Microsoft field organization accountable for driving customer value after commitment is secured. CSU owns Stages 3–5 of [MCEM](/mcem/methodology.md) and operates through the [Commit-to-Complete](/csu/processes/commit-to-complete.md) execution model.

# MCEM Accountability

| Stage | Role |
|-------|------|
| Stage 3 | **Accountable** — deployment and initial value |
| Stage 4 | **Accountable** — outcomes and expansion |
| Stage 5 | **Accountable** — optimization and renewal |

# Key Responsibilities

- Drive committed milestones to completion (target: 95% completion rate)
- Orchestrate delivery resources (ISD, partners, CSA)
- Own customer health and satisfaction
- Drive cloud adoption and consumption
- Protect renewals via T-minus motions
- Advance AI/Frontier Transformation in active engagements

# Execution Model

CSU operates through two primary pipeline motions:
1. [Azure Consumption Pipeline](/csu/pipeline/azure/consumption-pipeline.md) — committed production milestones
2. [Usage Pipeline](/csu/pipeline/usage/two-motion-model.md) — usage intent milestones

# Key Roles

- [CSAM](/csu/roles/csam.md) — Customer Success Account Manager (relationship owner)
- [CSA](/csu/roles/csa.md) — Customer Success Architect (technical delivery lead)

# FY27 Priorities

See [CSU FY27 Priorities](/csu/priorities/fy27.md) for the five strategic pillars.
