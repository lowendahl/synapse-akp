---
type: Doctrine
title: CSP Hierarchy
id: csu.doctrine.csp-hierarchy
description: The complete hierarchy from Account Plan → Customer Objective → Customer Priority → Customer Success Plan → Milestone that governs CSU execution.
tags: [csu, csp, hierarchy, doctrine, account-plan, objective, priority, milestone, execution]
relationships:
  - predicate: informs
    object: csu.planning.account-plan
  - predicate: informs
    object: csu.planning.customer-success-plan-csp
  - predicate: operationalizes
    object: mcem.planning.customer-success-planning
  - predicate: informs
    object: csu.process.commit-to-complete
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: customer-integrated-planning-okf
    resource: "Customer Integrated Planning OKF corpus"
    title: Customer Integrated Planning OKF Corpus
    last_modified: 2026-07-20
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-20
---
# Definition

The CSP Hierarchy is the governing structural chain through which CSU connects strategic customer intent to measurable execution. Every CSU action must trace through this hierarchy to maintain alignment between what the customer declared important and what Microsoft delivers.

# The Hierarchy

```
Account Plan
  └── Customer Objective (CxO-owned strategic goal)
        └── Customer Priority (initiative aligned to objective)
              └── Customer Success Plan / CSP (delivery container)
                    └── Milestone (measurable delivery checkpoint)
```

# Level Definitions

## 1. Account Plan

The integrated planning container for the customer relationship, maintained in MSX Dataverse. The Account Plan aggregates all of Microsoft's engagement with a customer across ATU, STU, and CSU.

**Owner:** Account Team Lead (ATU)  
**System:** MSX Account Plan  
**Content:** Customer profile, objectives, priorities, competitive landscape, partner ecosystem, consumption plans

## 2. Customer Objective

A CxO-level strategic business goal expressed in the customer's language. Objectives are the "why" — the business outcomes the customer is pursuing.

**Owner:** Customer (validated by ATU)  
**System:** MSX Account Plan > Objectives  
**Rules:**
- Must be articulated by a named customer executive sponsor
- Must have measurable KPIs (Customer Success Criteria)
- Typically 3–5 per top account

**Examples:**
- "Reduce infrastructure costs by 30% in 18 months"
- "Accelerate time-to-market for AI products by 50%"
- "Achieve SOC2 compliance for all cloud workloads"

## 3. Customer Priority

An initiative directly aligned to a Customer Objective, focused on what success looks like and how it will be measured. Priorities are the "what" — the specific programs of work.

**Owner:** ATU (validated with customer)  
**System:** MSX Account Plan > Priorities  
**Rules:**
- Written in the customer's language, confirmed with customer
- Each priority has an owner and timeline
- Linked to opportunities, partners, competitors
- ≥80% must be current with future timeframes
- Top priorities have 3-horizon attributes (differentiated value, strategic importance, disruption potential)
- Include measurable Success Criteria
- Default 1:1 mapping to CSP (one priority → one CSP)

## 4. Customer Success Plan (CSP)

The customer-facing container for linked activities, projects, and outcomes committed to achieving the success criteria of a Customer Priority.

**Owner:** CSAM (CSU)  
**System:** eSXP API / MSX CSP Module  
**Rules:**
- **No CSP without a parent Priority** — every CSP MUST link to exactly one Customer Priority
- **No CSP without an outcome** — every CSP must define at least one measurable outcome (milestone)
- Must include a named customer sponsor
- Monthly review minimum cadence
- Can span multiple delivery vehicles (EDE, Success Programs, FastTrack, partner)

**Contents (a CSP can include):**
- Pursuit activities and business case work
- Opportunities and milestone data
- Support projects
- ISD or consulting projects
- FastTrack projects
- Partner projects
- Customer activities
- CSA/CSM activities
- Delivery projects

## 5. Milestone

A measurable delivery checkpoint within a CSP that represents tangible progress toward the priority's success criteria.

**Owner:** CSAM (with CSA for technical milestones)  
**System:** eSXP API / MSX CSP Milestones  
**Rules:**
- Each milestone has a target date and completion criteria
- Milestones linked to consumption pipeline where applicable
- Completion drives [C2C accountability](/csu/processes/commit-to-complete.md)
- Milestones can map to [Azure pipeline milestones](/csu/pipeline/azure/milestone.md) for consumption tracking

# Governance Rules

| Rule | Enforcement |
|------|------------|
| No orphan CSPs | Every CSP must link to a Priority; orphans flagged in PCI hygiene |
| No phantom milestones | Milestones without target dates are invalid |
| Monthly CSP review | CSAM reviews all active CSPs with customer monthly minimum |
| CxO sponsor required | Each Objective and top Priority must have named customer executive |
| Success Criteria mandatory | Top Priorities must have measurable, customer-agreed success criteria |
| Staleness limit | CSP not updated in >30 days flagged as stale |

# Connecting CSP to Delivery

The CSP is the single orchestration layer connecting:

```
Customer Intent (Objective/Priority)
        ↓
    CSP (Container)
        ↓
┌───────┼───────────────────┐
│       │                   │
EDE/STA    Success Programs    Partner
Delivery   Engagement          Projects
│       │                   │
└───────┼───────────────────┘
        ↓
    Milestones → Outcomes
        ↓
    C2C Accountability
```

# Connecting CSP to Cloud Adoption & AI Transformation

CSPs are the execution vehicle for [CSU Outcomes](/csu/outcomes/):
- **Cloud Adoption** CSPs drive workload migration, modernization, and consumption milestones
- **AI Transformation** CSPs drive Copilot deployment, AI workload onboarding, and AI-powered business outcomes
- Each CSP naturally maps to either the Cloud Adoption or AI Transformation outcome framework

# Relationship to MCEM Stages

| MCEM Stage | CSP Hierarchy Activity |
|------------|----------------------|
| Stage 1 (Qualify) | Objectives and Priorities identified |
| Stage 2 (Solution) | CSPs drafted with success criteria |
| Stage 3 (Commit) | CSPs finalized, milestones agreed |
| Stage 4 (Realize) | Delivery executed, milestones completed |
| Stage 5 (Expand) | New CSPs for next-horizon priorities |

# Source Systems

- **MSX Dataverse** — Account Plan, Objectives, Priorities
- **eSXP API** — CSP module, milestones, activities
- **CES Delivery Insights** — Delivery project linkage
- **PCI** — CSP hygiene scoring
