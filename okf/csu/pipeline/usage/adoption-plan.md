---
type: Planning Artifact
title: Adoption Plan
id: csu.pipeline.adoption-plan
description: Structured plan for driving workload adoption growth for a specific customer, tied to usage intent milestones.
tags: [csu, pipeline, usage, adoption, planning]
relationships:
  - predicate: operationalizes
    object: mcem.planning.customer-success-planning
  - predicate: depends_on
    object: csu.planning.customer-success-plan-csp
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

An Adoption Plan is a structured plan for driving workload adoption growth for a specific customer. It operationalizes usage intent milestones into executable activities with measurable outcomes.

# Components

| Component | Purpose |
|-----------|---------|
| Workload scope | Which workloads are targeted for adoption growth |
| Baseline metrics | Current MAU/PAU/PRU state |
| Target metrics | Desired end-state usage levels |
| Activity plan | Specific enablement, training, and deployment actions |
| Timeline | Milestone dates aligned to intent milestones |
| Success criteria | How "adoption success" is measured |

# Relationship to CSP

Adoption Plans are a component of the broader [Customer Success Plan](/csu/planning/customer-success-plan.md). They focus specifically on usage growth while the CSP encompasses all aspects of customer success.

# Execution

CSA leads technical execution of Adoption Plans. CSAM governs progress through operating rhythms and customer engagement.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — adoption-oriented opportunities and milestones used to track planned usage acceleration work.
