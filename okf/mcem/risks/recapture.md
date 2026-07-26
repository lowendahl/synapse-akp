---
type: Risk Indicator
title: Recapture
id: mcem.risk.recapture
description: Recovery of at-risk or churned consumption and commitments through proactive intervention.
tags: [mcem, risk, recapture, churn, recovery]
relationships:
  - predicate: depends_on
    object: mcem.metric.customer-health
  - predicate: depends_on
    object: mcem.planning.macc-consumption-planning
  - predicate: informs
    object: mcem.stage.stage-5-manage-optimize
  - predicate: measures
    object: csu.metric.cloud-acr-revenue-at-risk
  - predicate: informs
    object: csu.process.existing-deals-renewals-motion-motion-2
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Recapture measures the successful recovery of consumption or commitments that were at risk of loss or had already churned. It reflects the effectiveness of reactive intervention when proactive measures (T-minus motions, health monitoring) were insufficient.

# Indicator Classification

- **Class:** Lagging / Recovery
- **Source Systems:** MSX, Power BI dashboards
