---
type: Evidence Map
title: MACC Evidence
id: csu.evidence.macc-evidence
description: Complete evidence path from MACC concept to semantic models, measures, and investigation patterns for shortfall risk and acceleration.
tags: [csu, evidence, macc, acr, acceleration, shortfall, semantic-model]
relationships:
  - predicate: references
    object: csu.evidence.msx-insights-msxi-analytics-measurement
  - predicate: references
    object: mcem.planning.macc-consumption-planning
  - predicate: references
    object: csu.program.cloud-migration-factory-cmf
  - predicate: references
    object: csu.program.ecif-enterprise-customer-investment-fund
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
---
# Concept

**[MACC](/mcem/planning/macc.md)**: Microsoft Azure Consumption Commitment — customer's contractual commitment to consume Azure over a term.

# Evidence Sources

## Primary: MACC ACR Acceleration

| Attribute | Value |
|-----------|-------|
| **PBI Artifact ID** | `0c0296b9-b521-4991-8a9a-f99285c89bb3` |
| **Workspace** | `FD129F38-B725-4397-B112-B45ED91A518B` (BICOE_Prod_BICore_Azure02) |
| **MSXi Report** | [MACC to ACR Acceleration](https://msxinsights.microsoft.com/User/Home/report/283b99b1-c9a7-4094-8950-7060d24943ba/2733) |
| **Grain** | TPID × MACCID (commitment); TPID × FiscalMonth × StrategicPillar (ACR) |

### Key Tables

| Table | Purpose |
|-------|---------|
| `factmacccommitment` | MACC signed value, remaining, LTD ACR, attainment |
| `dimmaccaccounts` | Account attributes, geography, TPID |
| `factmacc_acr` | Monthly ACR by workload pillar |
| `factmacc_target` | FY targets by strategic pillar |
| `factmacc_consumptionpipeline` | Pipeline coverage (Qualified, Committed, Uncommitted, Non-Qualified) |
| `factmacc_billedpipeline` | Billed pipeline data |
| `macchealthscoredetails` | Execution health scoring (Pipeline Mgmt, Consumption Planning, Support) |

### Key Measures

| Measure | What It Answers |
|---------|----------------|
| `[MACC $ Signed]` | Total MACC commitment value |
| `[LTD MACC ACR]` | Lifetime-to-date actual consumption |
| `[LTD MACC Attainment]` | % consumed of total commitment |
| `[Remaining MACC]` | Remaining commitment to consume |
| `[Shortfall Risk CQ]` | Current-quarter shortfall risk ($) |
| `[Shortfall Risk R12M]` | Rolling-12-month shortfall risk ($) |
| `[Qualified Pipeline]` | Qualified pipeline against this MACC |
| `[Committed Pipeline]` | Committed pipeline against this MACC |
| `[Average Execution Score]` | MACC health execution score |

### DAX Recipes (in catalog/recipes/)

| Recipe | Purpose |
|--------|---------|
| `customer-summary` | MACC commitment, consumed, remaining, shortfall risk per TPID |
| `acceleration-by-workload` | Workload-level ACR vs target gap analysis |
| `expiring-soon` | MACCs expiring within N months with remaining commitment |
| `pipeline-coverage` | Qualified/Committed/Uncommitted pipeline per TPID |
| `execution-score-by-account` | Health score breakdown (Pipeline Mgmt, Consumption Planning, Support) |
| `commitment-shortfall` | Shortfall risk by customer |

# Investigation Patterns

## "Which accounts are at MACC shortfall risk?"

→ Recipe: `commitment-shortfall` — sorted by `[Shortfall Risk R12M]` DESC

## "What workloads need acceleration for a specific customer?"

→ Recipe: `acceleration-by-workload` with TPID filter — shows gap by StrategicPillar

## "Do we have enough pipeline to hit the MACC target?"

→ Recipe: `pipeline-coverage` — compare Qualified Pipeline to NNR gap

## "What's the MACC execution health?"

→ Recipe: `execution-score-by-account` — sub-scores: Pipeline Mgmt, Consumption Planning, Support

## "Which MACCs expire soon with big remaining?"

→ Recipe: `expiring-soon` with months=6 — surfaces urgent acceleration needs

# Related Evidence

- [Job 1 Evidence](/csu/evidence/job1-evidence.md) — milestone C2C drives MACC consumption
- [Delivery Evidence](/csu/evidence/delivery-evidence.md) — CSA delivery accelerates consumption
