---
type: Governance
title: Pipeline Hygiene
id: csu.pipeline.pipeline-hygiene
description: Data quality standards and governance checks ensuring pipeline accuracy and trustworthiness.
tags: [csu, pipeline, azure, hygiene, governance, data-quality]
relationships:
  - predicate: operationalizes
    object: mcem.risk.pipeline-hygiene
  - predicate: informs
    object: mcem.metric.qualified-pipeline
  - predicate: informs
    object: mcem.metric.exit-conformance
  - predicate: governs
    object: csu.pipeline.azure-consumption-pipeline
  - predicate: references
    object: csu.pipeline.pipeline-ownership-model
  - predicate: uses_evidence
    object: csu.evidence.msx-dataverse-crm
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

Pipeline Hygiene encompasses the data quality standards and governance checks that ensure pipeline data accurately reflects customer reality. Poor hygiene degrades forecasting, obscures risk, and undermines the [Pipeline Ownership Model](/csu/pipeline/azure/pipeline-ownership-model.md).

# Hygiene Checks

| Dimension | Check | Frequency |
|-----------|-------|-----------|
| Stage accuracy | Opportunity stage matches actual customer status | Weekly |
| Date currency | Milestone dates are current and realistic | Weekly |
| Owner assignment | Owner matches stage ownership model | Weekly |
| Categorization | Milestones properly categorized | On creation |
| Completion marking | Completed milestones marked within 7 days | Weekly |
| Stale pipeline | No opportunity unchanged > 30 days | Monthly |

# Governance

Pipeline hygiene is a shared accountability across ATU, STU, and CSU for their respective stages. See [Pipeline Hygiene Risk](/mcem/risks/hygiene.md) for the risk signal interpretation.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the pipeline fields whose completeness and accuracy define hygiene, including status, dates, ownership, and help-needed flags.
