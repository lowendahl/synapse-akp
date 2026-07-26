---
type: Metric
title: Days in Stage
id: mcem.metric.days-in-stage
description: Velocity indicator measuring the average elapsed time opportunities spend in each MCEM stage.
tags: [mcem, metric, leading, velocity, lifecycle]
relationships:
  - predicate: measures
    object: mcem.stage.stage-1-listen-consult
  - predicate: measures
    object: mcem.stage.stage-2-inspire-design
  - predicate: measures
    object: mcem.stage.stage-3-empower-achieve
  - predicate: measures
    object: mcem.stage.stage-4-realize-value
  - predicate: measures
    object: mcem.stage.stage-5-manage-optimize
  - predicate: measures
    object: csu.process.commit-to-complete
  - predicate: informs
    object: csu.pipeline.pipeline-hygiene
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Days in Stage measures the average elapsed calendar days that opportunities remain in each MCEM stage before transitioning to the next. It is a leading velocity indicator — extended days suggest friction in exit criteria satisfaction or handoff execution.

# Indicator Classification

- **Class:** Leading
- **Frequency:** Weekly
- **Source System:** MSX Dataverse

# Interpretation

Extended days in stage indicates:
- Stage 1: Qualification friction or insufficient discovery
- Stage 2: Technical complexity or commitment delays
- Stage 3: Delivery bottlenecks or resource constraints
- Stage 4/5: Customer engagement gaps or health issues

# Evidence Path

| Source | System | What It Shows |
|--------|--------|---------------|
| MSX Dataverse | `msdyn_opportunities` | Stage transition timestamps per opportunity |
| MSX Insights — Total Completed Pipeline | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | `az_bz_opportunity` table contains stage-date columns |

**Investigation:** Calculate days-in-stage by computing the delta between stage entry and exit timestamps on MSX opportunities. High dwell time in Qualified or Committed indicates pipeline stall.