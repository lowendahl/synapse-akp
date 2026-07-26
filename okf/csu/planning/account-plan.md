---
type: Planning Artifact
title: Account Plan
id: csu.planning.account-plan
description: Strategic account-level plan covering the full Microsoft relationship, customer objectives, and engagement strategy.
tags: [csu, planning, account-plan, strategy, relationship]
relationships:
  - predicate: operationalizes
    object: mcem.planning.account-planning
  - predicate: informs
    object: csu.planning.customer-success-plan-csp
  - predicate: references
    object: csu.doctrine.csp-hierarchy
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

The Account Plan is the strategic planning artifact that covers the full Microsoft relationship with a customer. It sets the strategic context within which [Customer Success Plans](/csu/planning/customer-success-plan.md) and [Consumption Plans](/csu/planning/consumption-planning.md) operate.

# Scope

- Annual planning cycle with quarterly refresh
- Spans all Microsoft engagement (not just CSU)
- Cross-org coordination between ATU, STU, CSU
- Connects customer business priorities to Microsoft solutions

# Key Components

| Component | Purpose |
|-----------|---------|
| Customer context | Industry, business priorities, competitive landscape |
| Relationship map | Stakeholders, sponsors, influencers |
| Opportunity landscape | Growth and expansion potential |
| Risk assessment | Competitive, renewal, satisfaction risks |
| Engagement strategy | How to align Microsoft to customer priorities |

# Quality Review

Account plan quality is assessed through structured reviews. Plans must demonstrate alignment between customer business outcomes and Microsoft solution strategy.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — the authoritative account plan, customer objective, and account-plan priority records.
- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — the customer priorities and linked success plans that connect account strategy to execution.
