---
type: Operating Model
title: MACC Consumption Planning
id: mcem.planning.macc-consumption-planning
description: End-to-end MACC lifecycle management — planning, quality gates, execution loop, milestone checkpoints, and shortfall governance.
tags: [mcem, macc, consumption, commitment, pipeline, azure, planning]
relationships:
  - predicate: belongs_to
    object: mcem.planning.integrated-customer-planning-icp
  - predicate: depends_on
    object: mcem.planning.consumption-planning
  - predicate: informs
    object: mcem.stage.stage-3-empower-achieve
  - predicate: informs
    object: mcem.stage.stage-4-realize-value
  - predicate: references
    object: csu.evidence.macc-evidence
  - predicate: references
    object: csu.pipeline.azure-consumption-pipeline
  - predicate: measures
    object: csu.metric.cloud-acr-revenue-at-risk
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: macc-consumption-planning-okf
    resource: "MACC Consumption Planning OKF corpus"
    title: MACC Consumption Planning OKF Corpus
    author: team:mcaps-strategy
    last_modified: 2026-07-20
---
# Definition

MACC (Microsoft Azure Consumption Commitment) Consumption Planning is the discipline of planning, monitoring, and executing a customer's Azure/Marketplace spend commitment — commonly a 3-year term — through account strategy, pipeline sufficiency, milestone progression, and consumption execution.

# Concept Chain

```
Account Plan → Consumption Plan → Qualified Pipeline → Committed Pipeline → ACR Execution → MACC Burn
```

# MACC Lifecycle Stages

| Stage | Activities |
|-------|-----------|
| 0. Account Plan Created | Account Plan established in MSX with customer priorities |
| 1. Consumption Plan Created | RTM qualified pipeline, aspirational pipeline, Azure region selection |
| 2. Account Team Review | Formal acknowledgment, Unified alignment, concessions, Year 1 ACR growth |
| 3. CE/Deal Desk Review | ROI determination, concession approval |
| 4. MACC Deal Signed | Consumption Plan completed, signature amounts aligned |
| 5. Tracking Performance | Continuous review, execution loop, acceleration |

# Milestone MACC Model

The FY26+ model introduces annual cumulative commitment checkpoints inside the MACC term:

| Checkpoint | Timing | Purpose |
|-----------|--------|---------|
| Milestone 1 | 12 months | Year 1 consumption checkpoint |
| Milestone 2 | 24 months | Year 2 cumulative checkpoint |
| Milestone 3 | 36 months | Full term completion |

**Shortfall consequence:** If a milestone or overall commitment is missed, commerce systems automatically issue a shortfall invoice, converted to Azure Prepayment credit valid for 12 months.

# Six Quality Gates (MACC QF)

A green MACC requires **ALL six gates simultaneously** (composite pass) — not an average. Reading any single gate as overall health is a known anti-pattern.

| Gate | Requirement |
|------|-------------|
| 1. ACR Growth | Year 1 target: 10% (>$250M MACC) or 20% (<$250M MACC), Pure ACR Growth |
| 2. Rolling 12-Month Pipeline | RTM qualified pipeline in Consumption Plan; best practice: R12M PCI ≥ 300% |
| 3. Aspirational Pipeline | Horizon 2/3 projects with identified owners |
| 4. Capacity Planning | Azure Region selected for all milestones |
| 5. Unified Alignment | Unified contract in place; Purple Empowerment minimum ≥1% annualized MACC value in Enhanced Solutions |
| 6. Consumption Plan Acknowledgement | Signoff: AE, Azure Specialist, Azure GTM Lead, Azure Sales Excellence, CSAM/CSA |

# Pipeline States

| State | Definition | Managed By |
|-------|-----------|-----------|
| Uncommitted Pipeline | Customer agreement not yet obtained | ATU/STU |
| Committed Pipeline | Customer agreement obtained, implementation underway | CSU/Programs/Delivery |
| Production | Consumption from deployed workloads and baseline growth | CSU (monitor) |

# Consumption Execution Loop

The repeatable operating cycle on a signed MACC:

1. **Create/maintain** Account Plan and Consumption Plan aligned to account strategy
2. **Analyze** actuals versus targets (Consumption Gap = Total Targets − Total Sources)
3. **Document actions** and follow up on gaps and acceleration opportunities
4. **Review** per governance rhythm

# Consumption Gap Formula

```
Consumption Gap = Total Targets − (Actuals/Projected Baseline + Committed Pipeline + Uncommitted Pipeline)
```

# Role Accountability

| Role | MACC Accountability |
|------|---------------------|
| [ATU](/mcem/organization/atu.md) | Customer objectives/priorities, Account Plan, Consumption Plan creation/ownership, pipeline sufficiency |
| [STU](/mcem/organization/stu.md) | Progress opportunities from uncommitted to committed, business/technical validation |
| [CSU](/mcem/organization/csu.md) | Execute toward outcomes, architecture/implementation, Customer Success Plans, committed milestones |
| GPS/Partners | Partner delivery contributing to customer objectives |
| ISD/Services | Consulting delivery to priorities and consumption objectives |
| Commercial (CE/Deal Desk) | ROI review, concession validation, contracting, ECIF |

# Review Rhythms

| Rhythm | Cadence | Focus |
|--------|---------|-------|
| [QBR](/mcem/planning/qbr.md) | Quarterly | 3-horizon roadmap, priorities, MACC updates, exec sponsorship |
| [CSDR](/mcem/planning/csdr.md) | Monthly | CSP portfolio, cloud optimization, health, value realization |
| Pipeline Management | Weekly/biweekly | Progress, qualification, commit progression, slippage, escalations |
| Commercial Management | As-needed | Contracting, agreements, ECIF, commercial execution |

# Key Metrics

| Metric | Source |
|--------|--------|
| FY TPID PBO VTT | MACC ACR Acceleration report |
| MACC Performance / Decrement | factmacccommitment |
| Consumption Pipeline (committed/uncommitted/non-qualified) | factmacc_consumptionpipeline |
| Shortfall Risk (CQ/RTM) | factmacccommitment |
| Pipeline Coverage Index | [PCI](/mcem/metrics/pipeline-coverage-index.md) |
| Marketplace & Unified contribution | factmacc_billedpipeline |

# Source Systems

- **MSX Dataverse** — Consumption Plan, opportunities, milestones
- **MACC ACR Acceleration Report** (Power BI) — execution health dashboard

# Anti-Patterns

- Treating a single quality gate as overall MACC health (must be composite)
- Creating Consumption Plans without RTM qualified pipeline
- Missing Purple Empowerment minimum without exception documentation
- Not updating Consumption Plans after MACC signature
- Ignoring Horizon 2/3 aspirational pipeline

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — MACC opportunity records, commitment milestone data.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — MACC ACR Acceleration model: attainment, shortfall risk, pipeline coverage, execution scores.
