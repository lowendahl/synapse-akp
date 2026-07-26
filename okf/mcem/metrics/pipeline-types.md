---
type: Pipeline Taxonomy
title: Pipeline Types
id: mcem.metric.pipeline-types
description: The distinct pipeline types flowing through MCEM — Azure consumption, billed (EA/M365/Unified/MACC), and usage pipeline.
tags: [mcem, pipeline, types, azure, billed, usage, macc, unified, ea]
relationships:
  - predicate: references
    object: mcem.metric.qualified-pipeline
  - predicate: references
    object: mcem.metric.committed-pipeline
  - predicate: references
    object: mcem.metric.intent-creation-usage-pipeline
  - predicate: references
    object: mcem.planning.consumption-planning
  - predicate: references
    object: csu.pipeline.two-motion-model
  - predicate: references
    object: csu.pipeline.azure-consumption-pipeline
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: mcem-azure-pipeline-okf
    resource: "MCEM Azure Pipeline OKF corpus"
    title: MCEM Azure Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Definition

Microsoft's pipeline ecosystem consists of distinct pipeline types, each with different mechanics, ownership, and revenue recognition models. All flow through the [pipeline state machine](/mcem/metrics/pipeline-stages.md) but have different characteristics.

# Azure Consumption Pipeline (ACR)

| Attribute | Detail |
|-----------|--------|
| **Unit** | Milestones (incremental ACR) |
| **Revenue type** | Consumption (pay-as-you-go against MACC or direct) |
| **Owner** | CSU (committed), STU (uncommitted) |
| **Tracking** | MSX milestones with estimated dates and ACR values |
| **Key metrics** | [C2C](/csu/metrics/job1-commit-to-complete.md), [Job 2](/csu/metrics/job2-completed-created.md), [NNR](/csu/metrics/nnr.md) |

### Milestone Categories

| Category | Impact | Typical Owner |
|----------|--------|--------------|
| Production | Recurring consumption (positive) | CSU |
| POC/Pilot | Technical-win activity in stages 2–3 | STU |
| Optimization | Consumption reduction (negative) | CSU |
| Credit Offer | Consumption decrease from Azure credits | Finance |
| Other Adjustments | Organic growth/erosion | Auto |
| Deal Registration | Compensation-credit event | Partners |
| PRACR | Marketplace SaaS compensation | Partners |
| ISV/Marketplace | Marketplace consumption credit | Partners |
| Dual Credit | Partner co-sell compensation | Partners |

### Milestone Status Model

| Open Statuses | Closed Statuses |
|---------------|----------------|
| On Track | Completed |
| At Risk | Cancelled |
| Blocked | Lost to Competitor |
| | Hygiene/Duplicate |

# Billed Pipeline

Revenue from contractual billing events (not consumption-based).

## EA/EAS Renewal Pipeline

| Attribute | Detail |
|-----------|--------|
| **Unit** | Opportunities (annualized revenue) |
| **Revenue type** | Billed (annualized at end of term) |
| **Owner** | ATU (AE owns opportunity) |
| **Creation** | Auto-created: 100% recapture assumed, aligned to expiring enrollment |
| **Default FRA** | Committed At Risk |

## EAS Recurring Annual Order

| Attribute | Detail |
|-----------|--------|
| **Unit** | Opportunities (estimated future billed revenue) |
| **Revenue type** | Billed (recurring) |
| **Owner** | ATU (AE) |
| **Creation** | Auto-created: zero growth default |
| **Default FRA** | Committed At Risk |

## EA True-Up Pipeline

| Attribute | Detail |
|-----------|--------|
| **Unit** | Opportunities (% of scheduled future billed from BRE files) |
| **Revenue type** | Billed (true-up) |
| **Owner** | ATU (AE reviews/updates) |
| **Default FRA** | Upside |

## M365 / Modern Work Pipeline

| Attribute | Detail |
|-----------|--------|
| **Unit** | Opportunities (seat-based licensing) |
| **Revenue type** | Billed (per-user-per-month or annual) |
| **Owner** | ATU/STU |

## Unified Support Pipeline

| Attribute | Detail |
|-----------|--------|
| **Unit** | Opportunities (contract value) |
| **Revenue type** | Billed (annual contract) |
| **Owner** | Services Seller / CSAM |
| **Includes** | Reactive + Proactive + Enhanced Solutions packages |

## MACC Renewal Pipeline

| Attribute | Detail |
|-----------|--------|
| **Unit** | Opportunities (commitment value) |
| **Revenue type** | Commitment (consumed against over term) |
| **Owner** | ATU (commercial), CSU (consumption planning) |
| **Key link** | [MACC](/mcem/planning/macc.md) quality gates |

# Usage Pipeline

| Attribute | Detail |
|-----------|--------|
| **Unit** | Usage Intents / Adoption Milestones |
| **Revenue type** | Indirect (usage drives renewal/expansion) |
| **Owner** | CSU |
| **Tracking** | eSXP / MSX CSP milestones |
| **Key metrics** | [MAU](/csu/metrics/mau.md), [PAU](/csu/metrics/pau.md), [PRU](/csu/metrics/pru.md), Usage RaR |

# Closing Billed Opportunities

Required fields when closing:
- Billed Revenue Close Reason
- Actual Billed Close Date
- Billed Actual Revenue
- Competitor
- Billed Closing Comments (competitive win/loss details, value proposition, pricing, market conditions)

Close reasons: WON (Competitive Win, MS Sales Validated, Non-Compete, OEM Automated, Partial Win) | LOST (Canceled/Delayed, Competitive Loss, Hygiene/Duplicate, Kept Existing Solution, Consolidated)

# Evidence Path

| Pipeline Type | Primary Source | Artifact ID |
|--------------|---------------|-------------|
| Azure (Consumption) | MSX Insights — Total Completed Pipeline_OneAMP | `ba0a24fe-f7e8-4210-850c-f9d961140fea` |
| Billed (EA/M365/Unified) | MS Billed Pipeline SBR | `msbilled-pipeline-sbr` |
| MACC Renewal | MACC ACR Acceleration | `0c0296b9-b521-4991-8a9a-f99285c89bb3` |
| Usage (M365) | MSX Insights — M365 Usage Excellence | `db74d200-6b93-4a91-a629-6ca10ef65b49` |