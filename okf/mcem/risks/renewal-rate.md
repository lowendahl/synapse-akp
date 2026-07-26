---
type: Risk Indicator
title: Renewal Rate
id: mcem.risk.renewal-rate
description: Lagging indicator measuring the percentage of expiring contracts that successfully renew.
tags: [mcem, risk, lagging, renewal, churn]
relationships:
  - predicate: measures
    object: mcem.stage.stage-5-manage-optimize
  - predicate: depends_on
    object: mcem.risk.on-time-renewal
  - predicate: depends_on
    object: mcem.metric.customer-health
  - predicate: measures
    object: csu.process.t-minus-renewal-motion
  - predicate: references
    object: csu.metric.customer-health-revenue-at-risk
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: csu-context-engineering
    resource: "CSU-Context-Engineering corpus"
    title: CSU Context Engineering Corpus
    last_modified: 2026-04-28
---
# Definition

Renewal Rate measures the percentage of expiring contracts (MACC, EA, MCA) that successfully renew. It is the ultimate lagging indicator of MCEM lifecycle health — a low renewal rate indicates systemic failure in value realization (Stages 4–5).

# Indicator Classification

- **Class:** Lagging
- **Frequency:** Monthly / Quarterly
- **Source Systems:** MSX Contracts, UnifiedSalesOffer (Power BI)

# Risk Signal

Declining renewal rate signals:
- Insufficient value demonstration in Stage 4
- Poor optimization and governance in Stage 5
- Competitive displacement or budget reallocation
- Customer health degradation unaddressed

# Mitigation

Proactive mitigation via [T-minus Renewal Motion](/csu/processes/t-minus-renewal.md) which initiates structured intervention 12+ months before expiration.
