---
type: Pipeline Object
title: Usage Intent
id: csu.pipeline.usage-intent
description: A customer's qualified commitment to adopt or deepen usage of a specific workload or capability.
tags: [csu, pipeline, usage, intent, workload, adoption]
relationships:
  - predicate: informs
    object: mcem.metric.intent-creation-usage-pipeline
  - predicate: depends_on
    object: csu.process.new-deals-motion-motion-1
  - predicate: depends_on
    object: csu.process.existing-deals-renewals-motion-motion-2
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

A Usage Intent represents a customer's qualified commitment to adopt or deepen usage of a specific workload or capability. It is the primary pipeline object in the [Usage Pipeline](/csu/pipeline/usage/two-motion-model.md).

# Intent Milestones

Intent milestones are the executable units within usage pipeline:
- **Intent Created** — usage opportunity identified
- **Intent Secured** — customer commitment confirmed
- **Intent Executing** — adoption actions underway
- **Intent Realized** — measurable usage growth confirmed

# Relationship to Workloads

Each intent is tied to a specific workload taxonomy entry (e.g., Azure AI, Microsoft 365 Copilot, Security). The workload determines which [usage metrics](/csu/pipeline/usage/usage-metrics.md) are measured.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — Azure opportunities and milestones that operationalize qualified customer intent into pipeline.
