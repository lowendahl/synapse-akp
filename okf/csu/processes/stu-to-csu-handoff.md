---
type: Process
title: STU-to-CSU Handoff
id: csu.process.stu-to-csu-handoff
description: The commitment transition from Stage 2 (STU) to Stage 3 (CSU) when customer commitment is secured.
tags: [csu, process, handoff, stu, csu, commitment]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-2-inspire-design
  - predicate: gates
    object: mcem.stage.stage-3-empower-achieve
  - predicate: references
    object: mcem.metric.handoff-sla
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The STU-to-CSU Handoff is the formal transition of execution accountability from [STU](/mcem/organization/stu.md) to [CSU](/mcem/organization/csu.md) when customer commitment is secured in [Stage 2](/mcem/stages/2-inspire-and-design.md).

# Prerequisites

Before handoff, STU must have:
- Secured explicit customer commitment
- Validated solution architecture
- Defined deployment plan
- Identified resource requirements
- Agreed success criteria with customer

# Handoff Artifacts

| Artifact | From | To | Purpose |
|----------|------|-----|---------|
| Committed milestone(s) in MSX | STU | CSU | Execution backlog |
| Solution design | STU | CSU | Technical blueprint |
| Deployment plan | STU | CSU | Execution timeline |
| Success criteria | STU | CSU/Customer | Outcome measurement |

# CSU Acceptance

Upon handoff acceptance, CSU enters [Commit-to-Complete](/csu/processes/commit-to-complete.md) mode and integrates milestones into the [Customer Success Plan](/csu/planning/customer-success-plan.md).

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the opportunity, milestone, and owner context handed from STU into CSU execution.
