---
type: Framework
title: Technical Maturity Model (TMM)
id: csu.doctrine.technical-maturity-model-tmm
aliases: [TMM, Tech Maturity Model, technology maturity model]
description: The lifecycle classification framework that routes delivery to the right engine by classifying every workload/skill as Innovation, Growth, Mature, or On-Prem.
tags: [csu, doctrine, tmm, maturity, delivery, routing, lifecycle, framework]
relationships:
  - predicate: informs
    object: csu.delivery.delivery-engine-routing
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: informs
    object: csu.metric.on-strategy-delivery
  - predicate: informs
    object: csu.priority.right-people-in-the-right-moments-with-the-right-s
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck (slide 10, 17)"
    title: FY27 CE&S Manager Deck
    author: team:ces-leadership
    last_modified: 2026-07-01
  - id: fy26-delivery-strategy
    resource: "FY26 Customer Success Delivery Strategy"
    title: "FY26 Delivery Strategy Deck (slide 3)"
    author: hennie-loubser
    last_modified: 2026-06-09
---
# Definition

The **Technical Maturity Model (TMM)** classifies every technical skill/workload by its lifecycle stage. It is the primary axis CSU Delivery Strategy uses to decide **which [delivery engine](/csu/delivery/delivery-engine-routing.md) delivers which work**. Combined with customer segment, TMM determines routing.

# Why TMM Exists

The point is **capacity allocation**: emerging technologies need scarce, high-cost skills and close proximity; mature technologies need scale, repeatability, and lower-cost delivery. Classifying work by lifecycle stage lets CSU route each skill to the engine whose cost and proximity profile fits, freeing senior regional talent for the newest, highest-growth technologies.

# Classification Inputs

The TMM stage for a skill is determined by three inputs:

1. **Engineering team investment / strategy** — where the product group is spending
2. **ACR and MW/BA usage trends** — consumption and volume signals
3. **Unified delivery hours** — how much delivery demand the skill generates

# The Four Stages

| Stage | Definition | Delivery Posture | Demand Curve |
|-------|-----------|-----------------|-------------|
| **Innovation** | Emerging/niche technologies in early development. May or may not gain traction. Exploratory, long-term cloud growth. | Make the market via niche, scarce skillsets | Low (just starting) |
| **Growth** | Technologies that have gained traction; core of the cloud growth strategy. Direct alignment to Solution Plays and GTM. | Drive Solution Play growth with local resource affinity tied to segment GTM | Increasing |
| **Mature** | Market saturation reached. Consumption/volume may stay high but not a big driver of engineering investment. Stable releases. | Scale and commoditisation with lower-cost, repeatable delivery | High (entrenched) |
| **On-Prem** | On-prem technologies and select aging cloud technologies, some with end-of-life/deprecation path. | Drive transformation from on-prem to cloud; efficient, scaled delivery | Waning |

# Stage → Engine Routing

| TMM Stage | Primary Delivery Engine | Rationale |
|-----------|------------------------|-----------|
| **Innovation** | Global Solution Areas (specialised, scarce skills) | Segment-agnostic; needs niche expertise |
| **Growth** | Regional / Area CSAs (iCSU for Enterprise & Downstream) | Drives C2C on Solution Plays; local affinity |
| **Mature** | CSA Global Delivery (scaled, repeatable) | Lower-cost, high-volume; frees regional talent |
| **On-Prem** | CSA Global Delivery + SME&C / SfMC | Efficient transformation and modernisation |

# Classification Examples (Illustrative)

| Cloud | Innovation | Growth | Mature | On-Prem |
|-------|-----------|--------|--------|---------|
| **Azure** | Azure Cloud (new services) | Azure Bot Services | Azure Databricks | Entra ID / Active Directory |
| **M365** | M365 Cloud (new) | Copilot in Teams Phone | M365 Copilot | Exchange Online / Server |
| **D365** | D365 Cloud (new) | Copilot for Finance | D365 Customer Service | D365 Finance / Dynamics CRM |

> **Skills move stages as they mature.** Copilot/AI transitioned from Innovation to Growth as adoption rose. The model is continuously re-evaluated.

# Governance Cadence

| Rhythm | Scope | Outcome |
|--------|-------|---------|
| **Quarterly** | Skills taxonomy per Solution Area | Additions, changes, deletions to skills inventory → routing rules updated |
| **Six-monthly** | TMM stage classifications | Stage re-assignments → can drive annual delivery strategy changes |

Owned in partnership with Solution Area teams.

# Relationship to CSU KPIs

| TMM Concept | Connects To |
|-------------|-------------|
| Stage-driven routing | [Delivery Engine Routing](/csu/delivery/delivery-engine-routing.md) — TMM stage is input; engine is output |
| Growth-stage C2C | [Job 1 C2C](/csu/metrics/job1-commit-to-complete.md) — Growth-stage Solution Play delivery is where C2C commitments are realised |
| Innovation-stage origination | [Job 2](/csu/metrics/job2-completed-created.md) — Innovation skills seed expansion vectors |
| Mature/On-Prem scaling | [Repeatable Delivery](/csu/metrics/repeatable-delivery.md) — scaled engines drive repeatable % |
| Capacity freed | [On-Strategy Delivery](/csu/metrics/on-strategy-delivery.md) — TMM ensures CSAs spend hours on strategy-aligned work |

# Anti-Patterns

| ID | Anti-Pattern | Why It's Wrong |
|----|-------------|---------------|
| TMM-AP-1 | Treating TMM as fixed | Stage assignments change on six-month review; always read current classification |
| TMM-AP-2 | Routing by skill name instead of stage | The routing axis is the **stage**, not the product brand; a product can have services in different stages |
| TMM-AP-3 | Senior regional talent on Mature/On-Prem repeatable delivery | This is the capacity leak TMM exists to prevent — scaled engines own Mature/On-Prem |

# FY27 Updates

Delivery strategy remains aligned to TMM with stronger rigor on:
- Usage outcomes
- Milestone quality
- Pipeline coverage
- Renewal predictability
