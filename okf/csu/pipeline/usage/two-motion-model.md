---
type: Operating Model
title: Two-Motion Model
id: csu.pipeline.two-motion-model
description: Defines how usage pipeline is executed through two complementary motions — new deals and existing deals/renewals.
tags: [csu, pipeline, usage, two-motion, operating-model]
relationships:
  - predicate: operationalizes
    object: csu.process.new-deals-motion-motion-1
  - predicate: operationalizes
    object: csu.process.existing-deals-renewals-motion-motion-2
  - predicate: operationalizes
    object: mcem.planning.consumption-planning
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The Two-Motion Model defines how usage pipeline is executed through two complementary motions that address different customer contexts.

# Motion 1 — New Deals

Capture usage intent during the sales process and transition execution to CSU.

```
ATU → STU/DES → Intent Milestone → Intent Secured → CSU Handoff → CSU Execution → Usage Realization
```

See [New Deals Motion](/csu/processes/new-deals-motion.md) for process detail.

# Motion 2 — Existing Deals & Renewals

Improve unhealthy usage and protect renewals through structured intervention.

```
Usage Risk Identified → Intent Workshop → Intent Validation → Milestone Creation → Deployment → Usage Improvement
```

See [Existing Deals Motion](/csu/processes/existing-deals-motion.md) for process detail.

# Relationship to Azure Pipeline

The Usage Pipeline operates in parallel with the [Azure Consumption Pipeline](/csu/pipeline/azure/consumption-pipeline.md). Usage pipeline focuses on adoption depth (MAU, PAU, PRU) while Azure pipeline focuses on consumption breadth (ACR, milestones).

# MCEM Alignment

Usage pipeline stages align to MCEM:
- Motion 1 spans Stages 1–3 (intent through execution)
- Motion 2 operates within Stages 4–5 (optimization and renewal protection)

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the new-deal and existing-deal opportunities and milestones that separate the two pipeline motions.
