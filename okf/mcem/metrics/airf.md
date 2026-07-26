---
type: KPI
title: "AIRF — AI Revenue Forecast"
id: mcem.metric.airf-ai-revenue-forecast
description: Leading indicator tracking AI workload revenue pipeline and forecast commitment across Azure OpenAI, Copilot, and AI platform services.
tags: [mcem, kpi, airf, ai, revenue, forecast, leading]
relationships:
  - predicate: informs
    object: mcem.planning.consumption-planning
  - predicate: informs
    object: csu.priority.lead-ai-transformation
  - predicate: informs
    object: mcem.planning.quarterly-business-review-qbr
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU Context Engineering corpus"
    title: MCEM AIRF Definition
    last_modified: 2026-04-28
---
# Definition

**AIRF (AI Revenue Forecast)** is a leading indicator tracking AI workload revenue pipeline and forecast commitment across Azure OpenAI, Copilot, and AI platform services. It measures the forward-looking AI consumption and licensing revenue pipeline.

**Classification: LEADING** — predicts future AI revenue realization based on current pipeline quality and commitment level.

# Scope

AIRF encompasses:
- Azure OpenAI Service consumption pipeline
- M365 Copilot licensing pipeline
- GitHub Copilot licensing
- Security Copilot deployment
- Azure ML/AI platform consumption
- Custom AI workload pipeline (RAG, fine-tuning, agents)

# Relationship to Other Metrics

```
AIRF (AI pipeline health)
    → AI Transformation Outcomes (delivery)
        → AI ACR + AI Licensing Revenue (actual)
```

# Source Systems

- **MSX Dataverse** — AI-tagged opportunities and milestones
- **MSXAI** — AI workload identification and classification

# Evidence Path

AIRF signals are consumed by the pipeline stage classification system. Current stage assignment surfaces in:

| Source | Artifact ID | How AIRF Manifests |
|--------|------------|-------------------|
| MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` | `[Average Execution Score]` — composite of pipeline mgmt, consumption planning, support sub-scores |
| MSX Insights — Total Completed Pipeline | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | Milestone readiness flags (At Risk, Blocked, Help Needed) |