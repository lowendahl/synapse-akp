---
type: Program
title: ECIF — Enterprise Customer Investment Fund
id: csu.program.ecif-enterprise-customer-investment-fund
aliases: [ECIF, Enterprise Customer Investment Fund]
description: Ring-fenced investment fund to accelerate customer cloud adoption through funded engineering engagements, partner delivery, and migration workloads. Measured by ECIF Yield (NNR returned per $ invested).
tags: [csu, programs, ecif, investment, nnr, yield, acceleration]
relationships:
  - predicate: funds
    object: csu.program.cloud-migration-factory-cmf
  - predicate: funds
    object: csu.outcome.cloud-adoption-outcomes
  - predicate: extends
    object: mcem.planning.macc-consumption-planning
  - predicate: evidenced_by
    object: csu.evidence.ecif-evidence
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
sources:
  - id: ecif-yield
    resource: "ECIF Yield semantic model"
    title: ECIF Yield
    last_modified: 2026-07-01
---
# Definition

**ECIF (Enterprise Customer Investment Fund)** is Microsoft's ring-fenced investment fund to accelerate customer cloud adoption. ECIF grants fund partner delivery, engineering engagements, migration factories, and proof-of-concept work that directly drives Azure consumption (NNR).

# Purpose

- Remove adoption blockers by funding customer-specific delivery
- Accelerate [MACC](/mcem/planning/macc.md) consumption towards commitment targets
- Drive [NNR](/csu/metrics/nnr.md) through funded milestone completion
- Fund [Cloud Migration Factory](/csu/programs/cloud-migration-factory.md) engagements
- Enable partners to deliver at scale

# Operational System

| Aspect | Detail |
|--------|--------|
| **Request system** | ECIF Central (web application) |
| **Approval authority** | CSAM → Manager → ECIF panel (varies by amount) |
| **Workscope model** | Request → Approve → Assign Partner → Deliver → Close |
| **Fiscal cadence** | Allocated per fiscal year; unspent funds do not roll over |

# KPI: ECIF Yield

```
ECIF Yield = NNR attributed to ECIF-funded milestones / ECIF $ Invested
```

Target: varies by area (typically 3–5× return on investment).

See [ECIF Evidence](/csu/evidence/ecif-evidence.md) for full semantic model access.

# Key Measures

| Measure | Source | Purpose |
|---------|--------|---------|
| `[FY26 ECIF Granted]` | ECIF Yield model | Total granted in fiscal year |
| `[YTD ECIF Spent]` | ECIF Yield model | Year-to-date utilization |
| `[YTD ECIF Utilization]` | ECIF Yield model | % of grant utilized |
| `[ECIF Yield]` | ECIF Yield model | NNR return on investment |
| `[PBO ROI]` | ECIF Yield model | Pipeline-Based Outlook ROI |
| `[Prorated Burn Rate %]` | ECIF Yield model | Pace of spend vs expectation |

# Anti-Patterns

| Anti-Pattern | Why It's Bad |
|-------------|-------------|
| ECIF requested but not deployed | Funds expire; no NNR generated |
| ECIF deployed without milestone | No NNR attribution possible |
| ECIF used on non-consumption work | Doesn't drive measured outcomes |

# Relationship to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [MIRP](/csu/programs/mirp.md) | MIRP accounts are prioritized for ECIF |
| [MACC](/mcem/planning/macc.md) | ECIF often targets MACC shortfall acceleration |
| [NNR](/csu/metrics/nnr.md) | ECIF yield IS NNR / $ invested |
| [Cloud Migration Factory](/csu/programs/cloud-migration-factory.md) | CMF is funded via ECIF grants |
| [Partners](/mcem/organization/partners.md) | Partners deliver ECIF-funded work |
