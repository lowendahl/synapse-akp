---
type: Risk Indicator
title: On-Time Renewal
id: mcem.risk.on-time-renewal
description: Percentage of contract renewals that complete within the defined T-minus governance window.
tags: [mcem, risk, renewal, t-minus, governance]
relationships:
  - predicate: measures
    object: mcem.stage.stage-5-manage-optimize
  - predicate: informs
    object: mcem.planning.customer-relationship-governance
  - predicate: references
    object: mcem.risk.renewal-rate
  - predicate: measures
    object: csu.process.t-minus-renewal-motion
  - predicate: references
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

On-Time Renewal measures the percentage of contract renewals that are executed before or on their expiration date, within the [T-minus governance window](/csu/processes/t-minus-renewal.md). Late renewals create revenue gap risk and indicate process failure.

# Relationship to MCEM

On-time renewal is a Stage 5 outcome metric. It reflects the effectiveness of proactive renewal motions and customer health management in [Manage & Optimize](/mcem/stages/5-manage-and-optimize.md).
