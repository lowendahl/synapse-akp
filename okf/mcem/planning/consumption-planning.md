---
type: Process
title: Consumption Planning
id: mcem.planning.consumption-planning
description: The ICP discipline checking pipeline sufficiency and managing execution against consumption targets, quota targets, and MACC commitments.
tags: [mcem, icp, consumption, pipeline, macc, execution]
relationships:
  - predicate: belongs_to
    object: mcem.planning.integrated-customer-planning-icp
  - predicate: depends_on
    object: mcem.planning.account-planning
  - predicate: operationalizes
    object: mcem.stage.stage-2-inspire-design
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
  - predicate: references
    object: csu.pipeline.azure-consumption-pipeline
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
# Definition

Consumption Planning is the [ICP](/mcem/planning/integrated-customer-planning.md) discipline that checks pipeline sufficiency and manages execution against consumption targets, quota targets, and [MACC](/mcem/planning/macc.md) commitments. It combines two activity sets operated by different organizations.

# Owner

Shared: [ATU](/mcem/organization/atu.md) (pipeline sufficiency) + [CSU](/mcem/organization/csu.md) (execution).

# Two Activity Sets

## 1. Pipeline Sufficiency (ATU/STU)

The Account Plan drives enough qualified pipeline to achieve quota and MACC targets:
- Pipeline aligned to account strategy
- Mapped to Customer Priorities
- [Pipeline Coverage Index](/mcem/metrics/pipeline-coverage-index.md) ≥ 300%

## 2. Consumption Execution (CSU/GPS/ISD)

CSPs aligned to priorities show customer value through execution:
- Drive [Commit-to-Complete](/csu/processes/commit-to-complete.md)
- Maintain or accelerate baseline growth
- Execution plans connected to pipeline

# Mandatory Requirement

**All MACCs must have a Consumption Plan in MSX.** See [MACC Consumption Planning](/mcem/planning/macc.md) for the full lifecycle and quality gates.

# Relationship to Consumption Plan Artifact

The Consumption Plan is the MSX reporting view of expected vs target consumption. It captures:
- Customer strategic goals (from Account Plan)
- Execution plans (from CSPs)
- Rolling 12-month qualified pipeline

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — Azure opportunities and milestones that operationalize the consumption plan into pipeline actions.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
