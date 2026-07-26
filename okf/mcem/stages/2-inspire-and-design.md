---
type: MCEM Stage
title: "Stage 2 — Inspire & Design"
id: mcem.stage.stage-2-inspire-design
description: STU/DES-led stage where solutions are validated and customer commitment is secured.
tags: [mcem, stage-2, stu, des, solution-design, commitment]
relationships:
  - predicate: gates
    object: mcem.stage.stage-3-empower-achieve
  - predicate: depends_on
    object: mcem.planning.consumption-planning
  - predicate: references
    object: mcem.organization.specialist-technology-unit-stu
  - predicate: operationalizes
    object: csu.planning.customer-success-plan-csp
  - predicate: informs
    object: csu.pipeline.adoption-plan
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

Stage 2 — Inspire & Design is the second stage of [MCEM](/mcem/methodology.md). [STU](/mcem/organization/stu.md) and Delivery & Engineering Services (DES) lead solution validation, technical proof, and securing customer commitment to proceed.

# Accountability

| Dimension | Value |
|-----------|-------|
| Accountable Org | STU / DES |
| Stage Status | Qualified |
| Pipeline Type | Qualified pipeline → Committed pipeline |

# Stage Goal

Validate solution fit, prove technical feasibility, and secure customer commitment to move forward with deployment.

# Exit Criteria

- Solution architecture validated
- Technical proof of concept completed (where required)
- Customer commitment secured
- Deployment plan agreed
- Resource requirements identified
- Success criteria defined with customer

# Handoff

Upon commitment, opportunity transitions to [Stage 3 — Empower & Achieve](/mcem/stages/3-empower-and-achieve.md) via the [STU-to-CSU handoff](/csu/processes/stu-to-csu-handoff.md).

# Pipeline Ownership

STU owns qualified pipeline in this stage. Upon commitment, ownership transitions to CSU for execution. See [Pipeline Ownership Model](/csu/pipeline/azure/pipeline-ownership-model.md).

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — opportunity creation and early milestone progression as customer intent becomes qualified pipeline.
- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — the plan and priority context that shapes solution design and commitment readiness.
