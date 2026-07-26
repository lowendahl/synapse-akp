---
type: Metric
title: Unified Consumed Revenue (UCR)
id: mcem.unified.unified-consumed-revenue-ucr
description: The revenue recognition metric measuring how Enhanced Solutions delivery drives Unified contract value realization.
tags: [unified, ucr, revenue, consumption, delivery, ede]
relationships:
  - predicate: measures
    object: mcem.unified.enhanced-solutions-ede-sta
  - predicate: measures
    object: mcem.stage.stage-4-realize-value
  - predicate: measures
    object: csu.delivery.csu-delivery-process
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck"
    title: FY27 CE&S Manager Deck (slides 6, 15, 38)
    author: team:ces-leadership
    last_modified: 2026-07-01
---
# Definition

Unified Consumed Revenue (UCR) measures how delivery execution against [Enhanced Solutions](/mcem/unified/enhanced-solutions.md) packages drives revenue recognition within Unified Support contracts. In FY27, [Success Programs](/csu/programs/success-programs.md) shift to drive revenue through UCR.

# Mechanism

Revenue is recognized when Enhanced Solutions hours are consumed (delivered to the customer). The formula connects delivery execution to commercial outcomes:

```
UCR = Hours Consumed × Hourly Rate (per package terms)
```

# Importance

- UCR is the bridge between delivery quality and commercial sustainability
- Higher delivery consumption → higher UCR → stronger renewal proposition
- Low consumption signals scoping/delivery failures → renewal risk

# Governance

UCR is tracked in CES Delivery Insights at the package level. CSAMs monitor consumption rates as part of [CSDR](/mcem/planning/csdr.md) reviews to ensure packages are being fully utilized before renewal.

# Relationship to MCEM

UCR connects the [Unified Support](/mcem/unified/unified-support.md) commercial model to MCEM execution — it proves that proactive delivery is creating value, which supports [renewal rate](/mcem/risks/renewal-rate.md) and customer health.

# Source Systems

- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — MDM contract packages and sold hours define the commercial basis for consumed revenue.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
