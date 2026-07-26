---
type: Pipeline Field
title: Forecast Recommendation (FRA)
id: mcem.metric.forecast-recommendation-fra
description: The opportunity-level field tracking customer commitment level and forecast classification — drives pipeline categorization and forecasting.
tags: [mcem, pipeline, forecast, fra, commitment, opportunity, stages]
relationships:
  - predicate: informs
    object: mcem.metric.committed-pipeline
  - predicate: informs
    object: mcem.metric.committed-close-rate-usage-pipeline
  - predicate: informs
    object: mcem.planning.customer-relationship-governance
  - predicate: references
    object: csu.metric.nnr-net-new-revenue-ecif-yield
  - predicate: informs
    object: csu.process.commit-to-complete
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

**Forecast Recommendation (FRA)** is the opportunity-level field in MSX D365 used to track customer commitment and forecast billed revenue. It classifies pipeline confidence and drives forecast accuracy.

# Levels

| Level | Stage | Close Probability | Definition |
|-------|-------|-------------------|-----------|
| **Committed** | Stage 3 | >95% | Customer has indicated intent/agreed to buy; deal expected to close on time |
| **Committed At Risk** | Stage 3 | >75% | Intent indicated but identifiable risk to date/scope/tender |
| **Upside** | Stage 2–3 | >50% | No intent yet but solution/business case agreed; plausible acceleration |
| **Uncommitted** | Stage 1–2 | Low | Default value; no agreement on solution/business case |

# Business Rules

- Identifiable risk MUST be explained in Comments when using "Committed At Risk"
- Uncommitted deals should be disengaged before Empower and Achieve periods to manage cost of sales
- FRA drives forecast roll-up at territory, Area, and Corp level
- Movement from Uncommitted → Committed requires [commitment criteria](/mcem/metrics/pipeline-stages.md) validation

# Relationship to Pipeline Categories

```
Uncommitted = Unqualified/Qualified Pipeline
Upside = Qualified Pipeline (not yet committed)
Committed At Risk = Committed Pipeline (with risk)
Committed = Committed Pipeline (clean)
```

# Source Systems

- **MSX Dataverse** — opportunity-level FRA field

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSXi Customer Health — Revenue at Risk | `57664612-66df-4081-9e99-4edeebefc65e` | `[FRATTM]`, `[Annualized FRA]` |

**Definition:** FRA (Forecast Recommendation Algorithm) generates a TTM (trailing twelve months) value representing predicted future revenue based on consumption patterns. Used as an input to Customer Health classification.