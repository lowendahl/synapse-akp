---
type: Governance Rhythm
title: Customer Success Delivery Review (CSDR)
id: mcem.planning.customer-success-delivery-review-csdr
description: Monthly customer success and delivery governance rhythm reviewing execution progress, health, and value realization.
tags: [mcem, icp, csdr, governance, monthly, execution]
relationships:
  - predicate: belongs_to
    object: mcem.planning.customer-relationship-governance
  - predicate: informs
    object: mcem.planning.customer-success-planning
  - predicate: informs
    object: mcem.stage.stage-4-realize-value
  - predicate: informs
    object: mcem.stage.stage-5-manage-optimize
  - predicate: references
    object: csu.delivery.csu-delivery-process
  - predicate: measures
    object: csu.metric.on-strategy-delivery
  - predicate: measures
    object: csu.metric.booked-hours
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: customer-integrated-planning-okf
    resource: "Customer Integrated Planning OKF corpus"
    title: Customer Integrated Planning OKF Corpus
    author: team:mcaps-strategy
    last_modified: 2026-07-19
---
# Definition

The Customer Success Delivery Review (CSDR) is the monthly customer success and delivery governance rhythm. It reviews delivery progress, value realization, cloud optimization, health, support insights, adoption, and operational governance.

# Owner

[CSU](/mcem/organization/csu.md) — [CSAM](/csu/roles/csam.md) leads.

# Standard Topics

1. Executive and Customer Success Portfolio summary
2. Cloud optimization and health
3. End of support insights
4. Reactive support insights and case trending
5. Major incident guidance
6. Unified contract value realization
7. M365 adoption heatmap
8. MACC consumption reporting
9. Azure platform investments
10. Events and workshops
11. Microsoft team overview
12. Delivery project details

# Purpose

- Keep [CSPs](/csu/planning/customer-success-plan.md) current
- Validate progress on committed milestones
- Monitor [Customer Health](/mcem/metrics/customer-health.md)
- Feed outcomes into the next [QBR](/mcem/planning/qbr.md)

# Cadence

Monthly or more frequent, depending on account complexity and delivery intensity.

# Evidence

The CSDR pulls from multiple semantic models to build its agenda:

| Data Point | Source | Recipe/Measure |
|-----------|--------|----------------|
| Delivery progress (UDC) | [CES Delivery Insights](/csu/evidence/delivery-evidence.md) | `udc`, `package-detail` |
| Customer health | [Customer Health](/csu/evidence/customer-health-evidence.md) | Health checklist items |
| MACC consumption pacing | [MACC ACR Acceleration](/csu/evidence/macc-evidence.md) | `customer-summary` |
| Reactive support trends | MSXi CX Pulse OSAT | Reactive incident trending |
| MIRP/CSDR flags | CES Delivery Insights | `customer-unified` |
| CSP status | CES Delivery Insights | `csp-status` |
| Success Program completions | CES Delivery Insights | `sp-customer-metrics` |

# CSDR Flag in Data

The CSDR flag on an account in `customer-unified` indicates the account is enrolled in the CSDR governance rhythm — it surfaces in the `sp-eligibility` recipe alongside [MIRP](/csu/programs/mirp.md) and CSDM flags.
