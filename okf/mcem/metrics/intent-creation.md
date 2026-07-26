---
type: KPI
title: "Intent Creation (Usage Pipeline)"
id: mcem.metric.intent-creation-usage-pipeline
description: Rate at which new usage intents are created — the origination velocity metric for the M365/Copilot usage pipeline.
tags: [mcem, kpi, intent-creation, usage, pipeline, leading]
relationships:
  - predicate: measures
    object: mcem.stage.stage-1-listen-consult
  - predicate: references
    object: csu.process.new-deals-motion-motion-1
  - predicate: informs
    object: mcem.planning.consumption-planning
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

**Intent Creation** measures the rate at which new usage intents (adoption commitments) are created in the usage pipeline. It is the origination velocity metric — equivalent to [In-Quarter Create](/csu/metrics/in-quarter-create.md) but for the M365/Copilot usage domain.

**Classification: LEADING** — today's intent creation feeds tomorrow's adoption outcomes and usage revenue protection.

# Causal Chain

```
Upstream: Customer engagement, Success Programs, CSP milestone planning
    → Intent Creation (THIS)
        → Downstream: Committed Close Rate, MAU/PAU/PRU growth, Usage Revenue at Risk reduction
```

# Source Systems

- **eSXP API** — usage intent tracking
- **MSX CSP module** — intent-linked milestones

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| MSX Insights — M365 Usage Excellence | `db74d200-6b93-4a91-a629-6ca10ef65b49` | `[Usage Intent Created]` |
| MSX Insights — Total Completed Pipeline | `ba0a24fe-f7e8-4210-850c-f9d961140fea` | Milestone creation dates (consumption intent) |

**Grain:** Intent creation is tracked per-account; maps to milestone creation in MSX.