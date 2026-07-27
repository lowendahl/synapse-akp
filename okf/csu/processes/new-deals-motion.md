---
type: Process
title: New Deals Motion (Motion 1)
id: csu.process.new-deals-motion-motion-1
description: Capturing usage intent during the sales process and transitioning execution to CSU.
aliases: [Job2, Job 2, Motion 1, New Deals]
tags: [csu, process, usage, new-deals, motion-1]
relationships:
  - predicate: operationalizes
    object: mcem.planning.consumption-planning
  - predicate: operationalizes
    object: mcem.stage.stage-2-inspire-design
  - predicate: informs
    object: csu.metric.in-quarter-create-iqc
  - predicate: depends_on
    object: csu.planning.customer-success-plan-csp
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The New Deals Motion (Motion 1) of the [Two-Motion Model](/csu/pipeline/usage/two-motion-model.md) captures usage intent during the sales process and transitions execution to CSU.

# Flow

```
ATU → STU/DES → Intent Milestone → Intent Secured → CSU Handoff → CSU Execution → Usage Realization
```

# Key Activities

1. **ATU:** Identify usage intent during [Stage 1](/mcem/stages/1-listen-and-consult.md) discovery
2. **STU/DES:** Validate intent and create intent milestone
3. **Intent Secured:** Customer confirms usage commitment
4. **CSU Handoff:** Execution transitions to CSU
5. **CSU Execution:** Drive adoption per [Adoption Plan](/csu/pipeline/usage/adoption-plan.md)
6. **Usage Realization:** Measure and confirm usage growth

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — new opportunities, associated milestones, and stage progression for net-new pipeline creation.
