---
type: Operating Model
title: Pipeline Ownership Model
id: csu.pipeline.pipeline-ownership-model
description: Defines which organization owns pipeline at each MCEM stage and the accountability transitions.
tags: [csu, pipeline, azure, ownership, accountability]
relationships:
  - predicate: operationalizes
    object: mcem.organization.account-technology-unit-atu
  - predicate: operationalizes
    object: mcem.organization.specialist-technology-unit-stu
  - predicate: operationalizes
    object: mcem.organization.customer-success-unit-csu
  - predicate: references
    object: mcem.metric.handoff-sla
  - predicate: governs
    object: csu.pipeline.azure-consumption-pipeline
  - predicate: gates
    object: csu.process.atu-to-stu-handoff
  - predicate: gates
    object: csu.process.stu-to-csu-handoff
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The Pipeline Ownership Model defines which organization owns and is accountable for pipeline at each MCEM stage, ensuring clear accountability and preventing "gap between chairs" scenarios.

# Ownership Matrix

| Stage | Owner | Pipeline Type | Key Accountability |
|-------|-------|---------------|-------------------|
| 1 | [ATU](/mcem/organization/atu.md) | Unqualified | Pipeline creation, qualification |
| 2 | [STU](/mcem/organization/stu.md) | Qualified | Solution validation, commitment |
| 3–5 | [CSU](/mcem/organization/csu.md) | Committed | Execution, completion, value |

# Transition Points

- **Stage 1 → 2:** [ATU-to-STU Handoff](/csu/processes/atu-to-stu-handoff.md) upon qualification
- **Stage 2 → 3:** [STU-to-CSU Handoff](/csu/processes/stu-to-csu-handoff.md) upon commitment

# Anti-Pattern

Pipeline without a clear owner creates accountability gaps. Every opportunity and milestone must have an assigned owner matching the stage ownership model.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — owner assignments on opportunities and milestones across sellers, CSAMs, and CSAs.
