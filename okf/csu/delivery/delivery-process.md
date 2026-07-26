---
type: Process
title: CSU Delivery Process
id: csu.delivery.csu-delivery-process
description: The end-to-end proactive delivery lifecycle within CSU, spanning 6 phases and governed by CSAM/CSA swimlanes.
tags: [csu, delivery, process, lifecycle, csam, csa, outcomes]
relationships:
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
  - predicate: operationalizes
    object: mcem.stage.stage-5-manage-optimize
  - predicate: depends_on
    object: csu.process.stu-to-csu-handoff
  - predicate: depends_on
    object: csu.delivery.delivery-engine-routing
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: csu-delivery-process-okf
    resource: "CSU Delivery Process OKF corpus"
    title: CSU Delivery Process Documentation
    last_modified: 2026-07-20
---
# Definition

The CSU Delivery Process is the end-to-end lifecycle through which CSU transforms [Enhanced Solutions](/mcem/unified/enhanced-solutions.md) commitments into measurable customer outcomes. It spans 6 phases and is governed by two swimlanes: the CSAM relationship/orchestration track and the CSA technical execution track.

# Six Lifecycle Phases

| # | Phase | Purpose | Owner |
|---|-------|---------|-------|
| 1 | **Scoping** | Define engagement scope, outcomes, staffing needs | CSAM |
| 2 | **Planning** | Build delivery plan, timeline, resource schedule | CSA + CSAM |
| 3 | **Onboarding** | Customer kick-off, stakeholder alignment, environment access | CSA |
| 4 | **Execution** | Technical delivery against scoped outcomes | CSA |
| 5 | **Measurement** | Track and validate outcomes against success criteria | CSAM + CSA |
| 6 | **Renewal Prep** | Document value delivered, scope next cycle | CSAM |

# CSAM Swimlane (9 Boxes)

The CSAM orchestration track includes:
1. Customer relationship ownership
2. Priority and success criteria alignment
3. CSP creation and milestone management
4. Delivery cadence governance (bi-weekly/monthly)
5. Escalation management
6. Value storytelling to economic buyers
7. Cross-team coordination (ATU/STU for new workloads)
8. Consumption monitoring and health management
9. Renewal commercial negotiation

# CSA Swimlane (4 Boxes)

The CSA technical execution track includes:
1. Technical discovery and architecture review
2. Implementation/migration/optimization execution
3. Knowledge transfer and enablement
4. Outcome documentation and handoff

# Phase Transitions

| From → To | Gate |
|-----------|------|
| Scoping → Planning | Scope completed; delivery request created |
| Planning → Onboarding | CSA assigned; delivery plan approved by customer |
| Onboarding → Execution | Environment access confirmed; kick-off complete |
| Execution → Measurement | Delivery milestones completed |
| Measurement → Renewal Prep | Outcomes documented; value case captured |

# Cadence

- **Weekly**: CSA delivery progress check-in
- **Bi-weekly**: CSAM-customer delivery status
- **Monthly**: Formal delivery review at [CSDR](/mcem/planning/csdr.md) or QBR
- **Quarterly**: Value realization review with CxO sponsor

# Metrics

- Hours consumed / hours sold (consumption ratio)
- Milestones completed on time
- CSAT per engagement
- Outcome success criteria achievement rate
- Renewal rate for accounts with active EDE/STA

# Source Systems

- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — MDM provides sold package and entitlement context, while GRM provides the staffing requests and bookings that execute delivery.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
