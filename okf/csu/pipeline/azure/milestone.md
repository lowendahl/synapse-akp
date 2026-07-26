---
type: Pipeline Object
title: Azure Consumption Milestone
id: csu.pipeline.azure-consumption-milestone
description: The executable unit within an opportunity — a specific deployment, migration, or consumption event with a committed date.
tags: [csu, pipeline, azure, milestone, execution, commitment]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: informs
    object: csu.metric.job-1-commit-to-complete-c2c
  - predicate: informs
    object: mcem.metric.commit-to-complete-rate
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

An Azure Consumption Milestone is the executable unit within an [opportunity](/csu/pipeline/azure/opportunity.md). It represents a specific deployment, migration, or consumption event with a committed date and categorization.

# Milestone Categories

Milestones are categorized to enable proper governance and measurement:
- **Production milestones** — workload deployment to production
- **Non-production milestones** — POCs, pilots, dev/test
- **Consumption milestones** — ACR growth events

# Status Model

| Status | Meaning |
|--------|---------|
| Draft | Created, not yet committed |
| Committed | Customer confirmed, CSU accepted |
| In Progress | Active execution |
| Completed | Deployment/consumption confirmed |
| At Risk | Execution concerns identified |
| Slipped | Missed committed date |

# Commitment Criteria

A milestone becomes "committed" when:
- Customer confirms intent and resources
- Deployment plan and date are agreed
- CSU accepts execution accountability
- Milestone is properly categorized in MSX

# Measurement

Milestone completion drives the [Commit-to-Complete Rate](/mcem/metrics/commit-to-complete-rate.md) — the primary CSU execution metric.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — milestone records, commitment status, target dates, owners, and completion state.
