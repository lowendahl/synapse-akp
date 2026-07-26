---
type: Planning Artifact
title: Customer Success Plan (CSP)
id: csu.planning.customer-success-plan-csp
description: The primary execution artifact aligning committed milestones, adoption targets, and delivery activities to customer business outcomes.
tags: [csu, planning, csp, execution, milestones, outcomes]
relationships:
  - predicate: operationalizes
    object: mcem.planning.customer-success-planning
  - predicate: depends_on
    object: csu.planning.account-plan
  - predicate: references
    object: csu.evidence.esxp-csp-customer-success-plan-system
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

The Customer Success Plan (CSP) is the primary execution artifact that aligns committed milestones, adoption targets, and delivery activities to customer business outcomes. It is owned by the [CSAM](/csu/roles/csam.md) and serves as the single source of truth for what CSU is executing for a customer.

# Components

| Component | Content |
|-----------|---------|
| Customer objectives | Business outcomes the customer is pursuing |
| Success criteria | How success will be measured |
| Milestone portfolio | Committed milestones from both [Azure](/csu/pipeline/azure/) and [Usage](/csu/pipeline/usage/) pipelines |
| Delivery activities | Planned execution actions and resources |
| Risk register | Identified risks and mitigations |
| Governance plan | Review cadence and escalation paths |

# Lifecycle

- Created during [STU-to-CSU Handoff](/csu/processes/stu-to-csu-handoff.md)
- Updated quarterly through ICP rhythms
- Reviewed in CSDR cadence
- Presented to customer in QBR format

# Relationship to MCEM

The CSP operationalizes Stages 3–5 of [MCEM](/mcem/methodology.md) at the individual customer level.

# Source Systems

- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — the authoritative success plan, priority, RAID, milestone-insight, and opportunity-insight records.
