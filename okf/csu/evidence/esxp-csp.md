---
type: Evidence Source
title: eSXP CSP — Customer Success Plan System
id: csu.evidence.esxp-csp-customer-success-plan-system
aliases: [CSP API, eSXP CSP, Customer Success Plan API, ESXP]
description: Operational system for Customer Success Plans — priorities, milestones insights, RAID logs, and opportunity linkage. System of record for the CSP lifecycle (planning → delivery → review).
tags: [csu, evidence, csp, esxp, success-plans, priorities, raid, milestones]
relationships:
  - predicate: references
    object: csu.planning.customer-success-plan-csp
  - predicate: references
    object: csu.doctrine.csp-hierarchy
  - predicate: references
    object: csu.process.commit-to-complete
generated: { by: human:plwendahl, at: 2026-07-25T02:45:00Z }
status: stable
sources:
  - id: esxp-csp
    resource: "eSXP Customer Success Plans (CSP API)"
    title: eSXP CSP API
    last_modified: 2026-07-01
---
# What eSXP CSP Is

**eSXP CSP** is the operational system managing [Customer Success Plans](/csu/doctrine/csp-hierarchy.md), accessed via **eSXP API calls**. It stores the full lifecycle of customer engagement plans — from discovery through planning, delivery, and review.

# Key Entities

| Entity | API Path | Purpose |
|--------|----------|---------|
| **Success Plans** | `/successplans/accounts/{guid}` | CSP documents (name, state, owner, dates) |
| **Priorities** | `/accounts/{guid}/priorities` | Customer priorities within a plan |
| **RAID Logs** | `/accounts/{guid}/raidLogs` | Risks, Assumptions, Issues, Dependencies |
| **Milestones Insights** | `/accounts/{guid}/milestones/insights` | Milestone rollup with CSP linkage |
| **Opportunities Insights** | `/accounts/{guid}/opportunities/insights` | Pipeline linked to success plans |

# CSP States

| State | Meaning |
|-------|---------|
| `Planning` | Plan is being developed |
| `Approved` | Plan approved by customer and Microsoft |
| `InDelivery` | Active execution phase |
| `InDeliveryAtRisk` | Delivery at risk (escalated) |
| `Completed` | Plan lifecycle complete |
| `Cancelled` | Plan abandoned |

# Access

| Attribute | Value |
|-----------|-------|
| **Platform** | eSXP (API module) |
| **Protocol** | eSXP REST API |
| **Auth** | eSXP CSP bearer token (PRT-SSO) |
| **Account resolution** | TPID → account GUID via saved portfolio |

# Available Recipes

| Recipe | Purpose |
|--------|---------|
| `csps-by-tpid` | All CSPs for a customer (plan name, state, owner, sponsors, dates) |
| `success-plans` | List plans by account GUID, TPID, or name fragment |
| `priorities` | Customer priorities (objectives + unparented priorities) |
| `raids` | RAID log entries (delivery blockers, risks, dependencies) |
| `milestones-insights` | Milestone status with CSP linkage |
| `opportunities-insights` | Pipeline grouped by success plan |

# Investigation Patterns

| Question | How |
|----------|-----|
| "Does this customer have an active CSP?" | Recipe: `csps-by-tpid` → check state = InDelivery/Approved |
| "What are the customer's priorities?" | Recipe: `priorities` → returns objectives + priority items |
| "What risks/blockers exist?" | Recipe: `raids` → RAID log for the account |
| "How are milestones linked to the plan?" | Recipe: `milestones-insights` → shows which CSP owns which milestones |
| "What pipeline backs this CSP?" | Recipe: `opportunities-insights` → pipeline by plan |

# Relationship to the CSP Hierarchy

eSXP CSP is the **operational system** backing the [CSP Hierarchy doctrine](/csu/doctrine/csp-hierarchy.md):

```
Account Plan (MSX) → Customer Objective (MSX)
    → Priority (eSXP CSP) → CSP (eSXP CSP) → Milestone (MSX Dataverse)
```

The CSP system bridges MSX account plans (strategy) with MSX milestones (execution), adding the priorities and RAID governance layer in between.

# Relationship to PBI Models

| PBI Model | What CSP Feeds It |
|-----------|-------------------|
| CES Delivery Insights | `csp-status` recipe shows CSP state + days-in-state |
| CES Delivery Insights | `csp-coverage` recipe shows pipeline coverage by CSP |
| MSX Insights | Milestones linked to CSPs flow into C2C/NNR reporting |

# Relationship to Other Evidence Sources

| System | Linkage |
|--------|---------|
| [MSX Dataverse](/csu/evidence/msx-dataverse.md) | Account plans + milestones (CSP references them) |
| [MDM/GRM](/csu/evidence/mdm-grm.md) | Contract packages (delivery scheduled against CSP priorities) |
| [CES Delivery Insights](/csu/evidence/delivery-evidence.md) | CSP coverage and status analytics |
