---
type: KPI
title: "In-Quarter Create (IQC)"
id: csu.metric.in-quarter-create-iqc
description: CSU pipeline origination velocity — milestones created by CSU within the current quarter, regardless of expected completion date.
tags: [csu, kpi, iqc, pipeline, origination, velocity, leading]
relationships:
  - predicate: measures
    object: csu.process.new-deals-motion-motion-1
  - predicate: measures
    object: mcem.metric.intent-creation-usage-pipeline
  - predicate: evidenced_by
    object: csu.evidence.msx-insights-msxi-analytics-measurement
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: azure-consumption-program
    resource: "Azure Consumption Program"
    title: CSU In-Quarter Create Reporting
    last_modified: 2026-04-28
---
# Definition

**In-Quarter Create (IQC)** measures CSU-originated milestones created in the current quarter, regardless of when they are estimated to complete. It is the creation-velocity signal feeding [Job 2](/csu/metrics/job2-completed-created.md) in future quarters.

**Classification: LEADING** — today's origination velocity predicts future Job 2 completion and NNR.

# Formula

```
IQC = Count (or $) of milestones created in-quarter with originator = CSU
```

# Relationship to Job 2

| IQC (This) | Job 2 |
|------------|-------|
| Anchor: creation date | Anchor: completion date |
| Tells you: "How much NEW CSU pipeline did we originate this quarter?" | Tells you: "How much completed pipeline was CSU-originated?" |

A healthy IQC feeds future Job 2. Weak IQC with strong Job 2 = burning down back-book.

# Causal Chain

```
Upstream: CSA origination activity, Customer engagement depth, CSAM pipeline collaboration
    → In-Quarter Create (THIS)
        → Downstream: Job 2 (future quarters), NNR, Territory pipeline sufficiency
```

# Source Systems

- **MSX Dataverse** — opportunity/milestone creation dates, originator attribution

# Evidence Path

| Source | Artifact ID | Key Tables |
|--------|------------|-----------|
| MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | `factazureconsumptionpipeline` — filter by creation date in current quarter |

**Investigation:** Milestones where `creation_date` is within the current quarter AND `originator` = CSU. These are the in-quarter pipeline additions that feed Job 2.

**Measurement paradigm:** Real-time (counts all qualifying creations within the quarter window). See [Snapshot vs Real-Time](/csu/evidence/snapshot-vs-realtime.md).