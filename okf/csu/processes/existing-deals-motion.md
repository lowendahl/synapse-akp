---
type: Process
title: Existing Deals & Renewals Motion (Motion 2)
id: csu.process.existing-deals-renewals-motion-motion-2
description: Improving unhealthy usage and protecting renewals through structured intervention.
tags: [csu, process, usage, existing-deals, renewals, motion-2]
relationships:
  - predicate: operationalizes
    object: mcem.planning.consumption-planning
  - predicate: depends_on
    object: csu.metric.customer-health-revenue-at-risk
  - predicate: informs
    object: csu.process.t-minus-renewal-motion
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

The Existing Deals & Renewals Motion (Motion 2) of the [Two-Motion Model](/csu/pipeline/usage/two-motion-model.md) improves unhealthy usage and protects renewals through structured intervention.

# Flow

```
Usage Risk Identified → Intent Workshop → Intent Validation → Milestone Creation → Deployment → Usage Improvement
```

# Key Activities

1. **Risk Identification:** Monitor usage health signals, identify declining or underperforming workloads
2. **Intent Workshop:** Structured session with customer to define intervention
3. **Intent Validation:** Confirm customer commitment to address usage gap
4. **Milestone Creation:** Create usage intent milestones in pipeline
5. **Deployment:** Execute technical intervention (optimization, adoption)
6. **Usage Improvement:** Measure and confirm usage trajectory improvement

# Triggers

- Declining MAU/PAU metrics
- [ACO Percentage](/mcem/risks/aco-pct.md) below threshold
- Customer health degradation
- Approaching renewal with low utilization

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — expansion or acceleration opportunities and milestones created against existing customer accounts.
