---
type: Process
title: Commit-to-Complete
id: csu.process.commit-to-complete
description: The CSU execution model where CSU becomes accountable for driving committed milestones to completion at 95%+ rate.
tags: [csu, process, c2c, execution, milestones]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
  - predicate: operationalizes
    object: mcem.stage.stage-5-manage-optimize
  - predicate: depends_on
    object: csu.planning.customer-success-plan-csp
  - predicate: depends_on
    object: csu.process.stu-to-csu-handoff
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

Commit-to-Complete (C2C) is the execution model where CSU becomes accountable for driving committed milestones to completion. It is the defining operational model for CSU's MCEM accountability in Stages 3–5.

# Target

**95% committed milestone completion rate.**

# Scope

C2C applies to both pipeline types:
- [Azure Consumption Pipeline](/csu/pipeline/azure/consumption-pipeline.md) — committed production milestones
- [Usage Pipeline](/csu/pipeline/usage/two-motion-model.md) — committed usage intent milestones

# CSU Accountability

| Responsibility | Description |
|----------------|-------------|
| Drive completion | Actively manage milestones to completion |
| Orchestrate delivery | Coordinate ISD, partners, CSA resources |
| Coordinate partners | Align partner execution with customer outcomes |
| Drive value realization | Ensure deployed solutions deliver measurable value |
| Identify expansion | Surface growth opportunities back to ATU |

# Operationalization

C2C is operationalized through:
- [Customer Success Plans](/csu/planning/customer-success-plan.md) — defines the milestone portfolio per customer
- [Adoption Plans](/csu/pipeline/usage/adoption-plan.md) — defines usage growth trajectory
- Weekly operating rhythms — milestone review and exception management

# Metric

[Commit-to-Complete Rate](/mcem/metrics/commit-to-complete-rate.md) = Completed / Total Committed × 100

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — committed milestone records, status changes, target dates, and ownership for C2C execution.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
