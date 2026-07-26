---
type: Process
title: ATU-to-STU Handoff
id: csu.process.atu-to-stu-handoff
description: The qualification transition from Stage 1 (ATU) to Stage 2 (STU) when exit criteria are satisfied.
tags: [csu, process, handoff, atu, stu, qualification]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-1-listen-consult
  - predicate: gates
    object: mcem.stage.stage-2-inspire-design
  - predicate: references
    object: mcem.metric.handoff-sla
  - predicate: defined_by
    object: csu.pipeline.pipeline-ownership-model
  - predicate: followed_by
    object: csu.process.stu-to-csu-handoff
  - predicate: uses_evidence
    object: csu.evidence.msx-dataverse-crm
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The ATU-to-STU Handoff is the formal transition of opportunity ownership from [ATU](/mcem/organization/atu.md) to [STU](/mcem/organization/stu.md) when [Stage 1](/mcem/stages/1-listen-and-consult.md) exit criteria are satisfied.

# Prerequisites

Before handoff, ATU must have satisfied all Stage 1 exit criteria:
- Customer outcomes identified via [Discovery Questions](/mcem/discovery-questions.md)
- Decision makers identified
- Technical blockers understood
- Approval process understood
- Budget validated
- Timing confirmed

# Handoff Artifacts

| Artifact | Owner | Purpose |
|----------|-------|---------|
| Qualified opportunity in MSX | ATU | Formal pipeline record |
| Discovery findings | ATU | Customer context for STU |
| Identified stakeholders | ATU | Relationship map |

# SLA

Governed by [Handoff SLA](/mcem/metrics/handoff-sla.md) — minimize gap between qualification and STU acceptance to prevent customer experience degradation.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the account, opportunity, milestone, and ownership records transferred as work moves from ATU to STU.
