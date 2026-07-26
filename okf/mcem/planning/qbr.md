---
type: Governance Rhythm
title: Quarterly Business Review (QBR)
id: mcem.planning.quarterly-business-review-qbr
description: The primary customer relationship governance mechanism for confirming progress, reviewing outcomes, and validating plan changes.
tags: [mcem, icp, qbr, governance, quarterly, customer]
relationships:
  - predicate: belongs_to
    object: mcem.planning.customer-relationship-governance
  - predicate: informs
    object: mcem.planning.account-planning
  - predicate: informs
    object: mcem.planning.customer-success-planning
  - predicate: informs
    object: mcem.stage.stage-4-realize-value
  - predicate: references
    object: csu.metric.customer-health-revenue-at-risk
  - predicate: references
    object: csu.metric.nnr-net-new-revenue-ecif-yield
  - predicate: informs
    object: csu.process.t-minus-renewal-motion
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

The Quarterly Business Review (QBR) is the primary relationship governance mechanism for confirming progress against customer priorities, reviewing outcomes, and validating changes to plans and targets with the customer.

# Owner

[ATU](/mcem/organization/atu.md) — with CSU contributing execution content.

# Typical Agenda

1. Account team updates and priority topics
2. Industry and business review
3. Stakeholder changes
4. Strategy alignment and 3-horizon roadmap review
5. Outcomes and value delivered (CSU contributes)
6. Customer Success Portfolio review
7. Cloud optimization and health review
8. Consumption/deployment plan review ([MACC](/mcem/planning/macc.md) status)
9. Executive sponsor discussions

# Cadence

Quarterly by default; can be adjusted based on account complexity and customer preference.

# Relationship to CSDR

QBR is strategic (quarterly); [CSDR](/mcem/planning/csdr.md) is operational (monthly). CSDR findings feed into QBR content. Together they form the governance backbone of [Customer Relationship Governance](/mcem/planning/customer-relationship-governance.md).

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — pipeline, milestone progress, and account-plan context reviewed in the quarterly business review.
- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — customer success plan status, priorities, and RAID items reviewed in the QBR.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI outcomes and scorecard data reviewed in this governance rhythm.
