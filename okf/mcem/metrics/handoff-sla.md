---
type: Metric
title: Handoff SLA
id: mcem.metric.handoff-sla
description: Elapsed time from stage exit to completion of the formal handoff between accountable organizations.
tags: [mcem, metric, leading, handoff, velocity]
relationships:
  - predicate: measures
    object: csu.process.atu-to-stu-handoff
  - predicate: measures
    object: csu.process.stu-to-csu-handoff
  - predicate: measures
    object: mcem.stage.stage-1-listen-consult
  - predicate: measures
    object: mcem.stage.stage-2-inspire-design
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Handoff SLA measures the elapsed time from when exit criteria are satisfied to when the receiving organization formally accepts accountability. It applies to both [ATU-to-STU](/csu/processes/atu-to-stu-handoff.md) and [STU-to-CSU](/csu/processes/stu-to-csu-handoff.md) transitions.

# SLA Thresholds

Handoff SLA targets vary by transition type and are governed at the area/region level.

# Risk Signal

Extended handoff times create customer experience gaps where no organization has clear accountability — the "gap between chairs" anti-pattern.

# Evidence Path

| Source | System | What It Shows |
|--------|--------|---------------|
| MSX Dataverse | Opportunity ownership transfer timestamps | Time from handoff trigger to new owner acceptance |

**Note:** Handoff SLA is primarily an operational governance metric tracked via CSU process compliance reviews, not a dedicated PBI semantic model.