---
type: Evidence Source
title: MSX Dataverse (CRM)
id: csu.evidence.msx-dataverse-crm
aliases: [MSX, MSX Dataverse, MSX CRM, Dataverse, Microsoft Sales Experience]
description: Authoritative transactional system for accounts, account plans, opportunities, milestones, and pipeline. The system of record for all deal and milestone lifecycle data.
tags: [csu, evidence, msx, dataverse, crm, accounts, opportunities, milestones, pipeline]
relationships:
  - predicate: references
    object: csu.planning.account-plan
  - predicate: references
    object: csu.planning.customer-success-plan-csp
  - predicate: references
    object: csu.process.commit-to-complete
  - predicate: references
    object: mcem.planning.account-planning
generated: { by: human:plwendahl, at: 2026-07-25T02:45:00Z }
status: stable
sources:
  - id: msx-dataverse
    resource: "MSX Dataverse (CRM)"
    title: MSX Dataverse OData API
    last_modified: 2026-07-01
---
# What MSX Is

**MSX Dataverse** is the **Dynamics 365** CRM system (Microsoft Sales Experience). It is the **authoritative system of record** for:

- Customer accounts (TPID, hierarchy, geography)
- Account Plans (objectives, priorities)
- Opportunities (deals, pipeline)
- Engagement Milestones (committed, at risk, completed)
- Pipeline status and ownership

# Access Method

| Attribute | Value |
|-----------|-------|
| **Platform** | Dynamics 365 / Dataverse |
| **Protocol** | OData REST API (Dataverse Web API) |
| **Auth** | Azure AD bearer token (delegated or app) |
| **Base URL** | `https://msx.crm.dynamics.com/api/data/v9.2/` |
| **Format** | JSON with OData annotations |

# Key Entities

| Entity | Entity Set | Purpose |
|--------|-----------|---------|
| `account` | `accounts` | Customer accounts (TPID, name, geography) |
| `opportunity` | `opportunities` | Sales opportunities (pipeline, stage, value) |
| `msp_engagementmilestone` | `msp_engagementmilestones` | CSU engagement milestones (the atomic unit of C2C) |
| `msp_accountplan` | `msp_accountplans` | Account plans |
| `msp_accountplanpriority` | `msp_accountplanpriorities` | Account plan priorities |
| `msp_customerobjective` | `msp_customerobjectives` | Customer objectives within account plans |
| `systemuser` | `systemusers` | Users (CSAMs, CSAs, sellers) |
| `msp_audittrail` | `msp_audittrails` | Change history (who changed what when) |

# Milestone Fields (Critical for Pipeline KPIs)

| Field | Type | Purpose |
|-------|------|---------|
| `msp_milestonestatus` | OptionSet | Status: Committed, At Risk, Blocked, Completed, Cancelled |
| `msp_milestonedate` | Date | Target completion date |
| `msp_committedon` | Date | When committed (→ determines if in C2C snapshot) |
| `msp_completedon` | Date | Actual completion date |
| `msp_monthlyuse` | Decimal | Monthly ACR value (× 12 for annual if recurring) |
| `msp_commitmentrecommendation` | OptionSet | Uncommitted / Ready to Commit / Committed |
| `msp_helpneeded` | OptionSet | Help-needed flag |
| `_ownerid_value` | GUID | Milestone owner (CSA/CSAM) |
| `_msp_opportunityid_value` | GUID | Parent opportunity |

# What You Can Investigate

| Question | How to Query |
|----------|-------------|
| "What milestones are committed for this account?" | Filter `msp_engagementmilestones` by `_msp_parentaccount_value` + `msp_commitmentrecommendation` = Committed |
| "Who owns this milestone?" | Expand `_ownerid_value` → `systemusers` |
| "What changed on this milestone?" | Query `msp_audittrails` for the milestone GUID |
| "What's in the account plan?" | Query `msp_accountplans` → expand priorities → objectives |
| "What's the pipeline for this account?" | Filter `opportunities` by account + stage |

# Relationship to PBI Semantic Models

MSX Dataverse is the **upstream source** for most PBI pipeline models:

| PBI Model | What It Gets from MSX |
|-----------|----------------------|
| [MSX Insights — Total Completed Pipeline](/csu/evidence/job1-evidence.md) | Milestone snapshots + completions |
| [MACC ACR Acceleration](/csu/evidence/macc-evidence.md) | Opportunity + MACC commitment data |
| [CES Delivery Insights](/csu/evidence/delivery-evidence.md) | CSP linkage, milestone insights |

**Key distinction:** PBI models provide **aggregated analytics** (trends, rates, rankings). MSX Dataverse provides **real-time individual record** access (single milestone status, single opportunity detail, change history).

# When to Use MSX vs PBI

| Use Case | Use MSX Dataverse | Use PBI Semantic Model |
|----------|------------------|----------------------|
| Check one milestone's status | ✅ | ❌ |
| See who committed what when | ✅ | ❌ |
| Calculate C2C rate across territory | ❌ | ✅ |
| Compare pipeline this quarter vs last | ❌ | ✅ |
| Update a milestone | ✅ | ❌ |
| Audit change history | ✅ | ❌ |
