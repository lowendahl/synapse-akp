---
type: Metric
title: Exit Conformance
id: mcem.metric.exit-conformance
description: Percentage of MCEM stage transitions that satisfy all defined exit criteria before advancing.
tags: [mcem, metric, governance, quality]
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
    object: csu.delivery.csu-delivery-process
  - predicate: informs
    object: csu.metric.on-strategy-delivery
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Exit Conformance measures the percentage of stage transitions where all defined exit criteria were satisfied before the opportunity advanced. Non-conformant transitions represent pipeline quality risk.

# Governance

Exit Conformance is a quality gate metric. Low conformance indicates:
- Opportunities advancing without proper qualification
- Handoffs occurring without complete information
- Pipeline hygiene degradation

# Evidence Path

Exit conformance is a governance metric assessed against [MCEM stage exit criteria](/mcem/stages/). It does not have a single dedicated semantic model but is derived from:

| Signal | Source |
|--------|--------|
| Milestone status/quality | MSX Dataverse (opportunity fields) |
| Pipeline hygiene score | MACC ACR Acceleration `[Average Execution Score]` |
| Stage transition completeness | MSX opportunity audit trail |