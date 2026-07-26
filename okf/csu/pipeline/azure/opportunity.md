---
type: Pipeline Object
title: Azure Consumption Opportunity
id: csu.pipeline.azure-consumption-opportunity
description: A qualified customer intent to consume Azure services, tracked through MCEM stages in MSX.
tags: [csu, pipeline, azure, opportunity, msx]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-1-listen-consult
  - predicate: operationalizes
    object: mcem.stage.stage-2-inspire-design
  - predicate: depends_on
    object: csu.planning.account-plan
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

An Azure Consumption Opportunity represents a qualified customer intent to consume Azure services. It is the primary pipeline object tracked through [MCEM stages](/mcem/stages/) in MSX Dataverse.

# Lifecycle

1. **Created** in Stage 1 by ATU as unqualified opportunity
2. **Qualified** upon Stage 1 exit criteria satisfaction
3. **Committed** when customer confirms in Stage 2
4. **Executed** through Stages 3–5 by CSU
5. **Closed** upon milestone completion or loss

# Relationship to Milestones

One opportunity contains one or more [milestones](/csu/pipeline/azure/milestone.md). Milestones are the executable units; the opportunity is the container that connects them to a customer priority.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — opportunity records that hold Azure pipeline stage, account linkage, and the milestone container for the deal.
