---
type: KPI
title: "Committed Close Rate (Usage Pipeline)"
id: mcem.metric.committed-close-rate-usage-pipeline
description: Percentage of committed usage intents that achieve their adoption outcome within the target timeframe. Target ≥95%.
tags: [mcem, kpi, committed-close-rate, usage, pipeline, lagging]
relationships:
  - predicate: measures
    object: mcem.stage.stage-4-realize-value
  - predicate: measures
    object: mcem.stage.stage-5-manage-optimize
  - predicate: measures
    object: csu.process.existing-deals-renewals-motion-motion-2
classification: lagging
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

**Committed Close Rate** is the usage pipeline equivalent of [C2C](/csu/metrics/job1-commit-to-complete.md) — it measures the percentage of committed usage intents that achieve their adoption outcome within the target timeframe.

**Classification: LAGGING** — measures execution fidelity on committed adoption plans.

**Target: ≥ 95% Quarterly Close Rate**

# Relationship to Azure C2C

| Azure Pipeline | Usage Pipeline |
|---------------|---------------|
| Committed Milestones → Completed | Committed Intents → Achieved |
| C2C % (Job 1) | Committed Close Rate |
| Revenue impact: ACR | Impact: MAU/PAU/PRU → Revenue protection |

# Causal Chain

```
Upstream: Intent Creation, CSP milestone quality, Delivery execution
    → Committed Close Rate (THIS)
        → Downstream: MAU/PAU/PRU outcomes, Usage Revenue at Risk reduction, Renewal protection
```

# Source Systems

- **eSXP API** — intent status tracking, close dates

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | `[Completed Pipeline_MTD]` / `[Committed Pipeline]` |
| MSX Insights — Usage Close Rate | `usage-close-rate model` | Usage-side close rate |

**Distinction:** Azure consumption C2C uses `msxi-completed-pipeline`; M365 usage close rate uses `msxi-usage-close-rate`.