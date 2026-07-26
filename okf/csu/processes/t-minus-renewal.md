---
type: Process
title: T-Minus Renewal Motion
id: csu.process.t-minus-renewal-motion
description: Structured intervention beginning 12+ months before contract expiration to protect renewal outcomes.
tags: [csu, process, renewal, t-minus, governance]
relationships:
  - predicate: operationalizes
    object: mcem.risk.on-time-renewal
  - predicate: depends_on
    object: csu.process.existing-deals-renewals-motion-motion-2
  - predicate: informs
    object: csu.priority.earn-customer-trust
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

The T-Minus Renewal Motion is a structured intervention process that begins 12+ months before contract expiration (MACC, EA, MCA). It ensures proactive engagement to protect [Renewal Rate](/mcem/risks/renewal-rate.md) and [On-Time Renewal](/mcem/risks/on-time-renewal.md) outcomes.

# Timeline

| T-Minus | Activity |
|---------|----------|
| T-12 months | Scoping gate — assess renewal readiness, identify risks |
| T-9 months | Value narrative preparation, consumption acceleration |
| T-6 months | Renewal strategy alignment with customer |
| T-3 months | Proposal and negotiation |
| T-0 | Renewal execution |

# Scoping Gate

The T-minus scoping gate assesses:
- Current [ACO%](/mcem/risks/aco-pct.md) and consumption trajectory
- Customer satisfaction and health signals
- Competitive threats and budget pressures
- Expansion vs. flat vs. contraction scenarios

# Accountability

CSAM owns the T-minus renewal motion. Escalation paths activate when risk indicators exceed thresholds defined in governance.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — renewal-related opportunities, milestones, and pipeline progression managed during the motion.
- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — MDM contract start and end dates establish the renewal timeline and coverage window.
