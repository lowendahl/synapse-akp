---
type: Metric
title: Committed Pipeline
id: mcem.metric.committed-pipeline
description: The volume of customer-committed milestones in execution (Stages 3–5).
tags: [mcem, metric, pipeline, committed, execution]
relationships:
  - predicate: measures
    object: mcem.stage.stage-3-empower-achieve
  - predicate: measures
    object: mcem.stage.stage-4-realize-value
  - predicate: measures
    object: mcem.stage.stage-5-manage-optimize
  - predicate: references
    object: csu.pipeline.azure-consumption-pipeline
  - predicate: references
    object: csu.pipeline.azure-consumption-milestone
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

Committed Pipeline represents milestones where customers have confirmed commitment and CSU has accepted execution accountability. This is the numerator for the [Commit-to-Complete Rate](/mcem/metrics/commit-to-complete-rate.md).

# Commitment Criteria

A milestone enters committed pipeline when:
- Customer has confirmed intent and resources
- Deployment plan is agreed
- CSU has accepted execution ownership via [STU-to-CSU handoff](/csu/processes/stu-to-csu-handoff.md)
- Milestone is categorized and dated in MSX

# Relationship to MCEM

Committed pipeline is the bridge between Stage 2 (commitment) and Stage 3 (execution). It represents the execution backlog that CSU is accountable for driving to completion.

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` | `[Committed Pipeline]`, `[Committed Pipeline (excl. blocked)]` |
| MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | `[Committed Pipeline]` per territory |

**Recipe:** `pipeline-coverage` — shows committed vs qualified vs uncommitted pipeline per TPID. See [MACC Evidence](/csu/evidence/macc-evidence.md).