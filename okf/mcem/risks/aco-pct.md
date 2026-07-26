---
type: Risk Indicator
title: ACO Percentage
id: mcem.risk.aco-percentage
description: Azure Consumed Outcome percentage measuring actual consumption against commitment levels.
tags: [mcem, risk, aco, consumption, macc]
relationships:
  - predicate: measures
    object: mcem.planning.macc-consumption-planning
  - predicate: informs
    object: mcem.stage.stage-4-realize-value
  - predicate: informs
    object: mcem.stage.stage-5-manage-optimize
  - predicate: measures
    object: csu.metric.cloud-acr-revenue-at-risk
  - predicate: informs
    object: csu.pipeline.azure-consumption-pipeline
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

ACO Percentage (Azure Consumed Outcome %) measures actual Azure consumption against the customer's committed consumption level (MACC). Low ACO% indicates the customer is under-consuming relative to their commitment — a leading indicator of renewal risk and value realization failure.

# Risk Signal

- ACO% < 50% at contract midpoint: High risk — immediate intervention required
- ACO% 50–80%: Moderate risk — acceleration plan needed
- ACO% > 80%: Healthy — on track for commitment burn

# Mitigation

Addressed through [Consumption Planning](/csu/planning/consumption-planning.md) and [Azure Pipeline](/csu/pipeline/azure/consumption-pipeline.md) acceleration.
