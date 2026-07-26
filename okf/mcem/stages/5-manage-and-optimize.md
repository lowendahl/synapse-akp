---
type: MCEM Stage
title: "Stage 5 — Manage & Optimize"
id: mcem.stage.stage-5-manage-optimize
description: CSU-led stage focused on continuous optimization, renewal protection, and lifecycle governance.
tags: [mcem, stage-5, csu, optimization, renewal]
relationships:
  - predicate: depends_on
    object: mcem.planning.customer-relationship-governance
  - predicate: depends_on
    object: mcem.risk.on-time-renewal
  - predicate: references
    object: mcem.organization.customer-success-unit-csu
  - predicate: operationalizes
    object: csu.process.t-minus-renewal-motion
  - predicate: measures
    object: csu.metric.customer-health-revenue-at-risk
  - predicate: measures
    object: csu.metric.cloud-acr-revenue-at-risk
  - predicate: informs
    object: csu.process.existing-deals-renewals-motion-motion-2
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-fy27-changes
    resource: "FY27 Strategy and Landing — MCEM Summary of Changes"
    title: FY27 MCEM Summary of Changes
    author: team:mcaps-strategy
    last_modified: 2026-07-01
---
# Definition

Stage 5 — Manage & Optimize is the fifth and final stage of [MCEM](/mcem/methodology.md). [CSU](/mcem/organization/csu.md) drives continuous optimization, protects renewals, and governs the customer lifecycle to prevent churn and maximize long-term value.

# Accountability

| Dimension | Value |
|-----------|-------|
| Accountable Org | CSU |
| Stage Status | Operational / Renewing |
| Focus | Optimization, renewal, health |

# Stage Goal

Ensure continuous optimization of deployed solutions, protect renewal outcomes, and maintain healthy customer relationships through governance.

# Exit Criteria

- Continuous optimization cadence established
- Renewal secured (T-minus motions executed)
- Customer health maintained or improved
- Cost optimization recommendations delivered
- Next-cycle planning initiated

# Key Activities

1. Execute [T-minus Renewal Motion](/csu/processes/t-minus-renewal.md)
2. Monitor and improve [Customer Health](/mcem/metrics/customer-health.md)
3. Drive cost optimization and workload efficiency
4. Maintain [CSDR cadence](/csu/planning/integrated-customer-planning.md)
5. Feed insights back into account planning for next cycle
6. Protect against [renewal risk](/mcem/risks/renewal-rate.md)

# Lifecycle Loop

Stage 5 is not terminal. Expansion opportunities loop back to [Stage 1](/mcem/stages/1-listen-and-consult.md) for new motions, creating the continuous engagement flywheel.

# Source Systems

- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — MDM contract dates and coverage define the renewal and optimization window.
- **[eSXP CSP](/csu/evidence/esxp-csp.md)** — success plan status, priorities, and RAID governance support ongoing optimization and renewal management.
