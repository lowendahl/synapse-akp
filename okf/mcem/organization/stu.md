---
type: Organization
title: Specialist Technology Unit (STU)
id: mcem.organization.specialist-technology-unit-stu
description: The Microsoft field organization accountable for solution validation, technical proof, and commitment in MCEM Stage 2.
tags: [stu, organization, solution-design, specialists]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-2-inspire-design
  - predicate: depends_on
    object: mcem.planning.consumption-planning
  - predicate: informs
    object: mcem.planning.integrated-customer-planning-icp
  - predicate: references
    object: csu.process.stu-to-csu-handoff
  - predicate: informs
    object: csu.delivery.delivery-engine-routing
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-fy27-changes
    resource: "FY27 Strategy and Landing — MCEM Summary of Changes"
    title: FY27 MCEM Summary of Changes
    author: team:mcaps-strategy
    last_modified: 2026-07-01
---
# Definition

The Specialist Technology Unit (STU) is the Microsoft field organization responsible for deep technical solution design, proof of concept, and securing customer commitment. In MCEM, STU (alongside DES) is accountable for [Stage 2 — Inspire & Design](/mcem/stages/2-inspire-and-design.md).

# MCEM Accountability

| Stage | Role |
|-------|------|
| Stage 2 | **Accountable** — leads solution validation and commitment |
| Stage 1 | Supports ATU with technical depth as needed |

# Key Responsibilities

- Validate solution architecture against customer requirements
- Conduct technical proof of concept
- Secure customer commitment to proceed
- Define deployment plan and resource requirements
- Execute [STU-to-CSU handoff](/csu/processes/stu-to-csu-handoff.md) upon commitment

# Pipeline Ownership

STU owns qualified pipeline in Stage 2. Upon commitment, pipeline transitions to CSU for execution via [Commit-to-Complete](/csu/processes/commit-to-complete.md).
