---
type: Operating Model
title: Delivery Engine Routing
id: csu.delivery.delivery-engine-routing
description: The 5 delivery engines through which CSU routes customer delivery based on segment, TMM level, and customer complexity.
tags: [csu, delivery, engines, routing, segment, tmm, scaled]
relationships:
  - predicate: operationalizes
    object: csu.delivery.csu-delivery-process
  - predicate: depends_on
    object: csu.doctrine.technical-maturity-model-tmm
  - predicate: informs
    object: csu.metric.on-strategy-delivery
  - predicate: informs
    object: csu.metric.repeatable-delivery
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: csu-delivery-engine-routing-okf
    resource: "CSU Delivery Engine Routing OKF corpus"
    title: CSU Delivery Engine Routing Documentation
    last_modified: 2026-07-20
---
# Definition

CSU routes delivery through 5 engines, differentiated by customer segment, [TMM (Technical Maturity Model)](/csu/doctrine/technical-maturity-model.md) classification, and engagement complexity. The routing model ensures the right delivery motion applies to the right customers at the right scale.

# The 5 Delivery Engines

| # | Engine | Segment | TMM Threshold | Delivery Model |
|---|--------|---------|---------------|----------------|
| 1 | **Designated Managed** | Enterprise | High TMM | Named CSAM + named CSA; deep, ongoing engagement |
| 2 | **Pooled Managed** | Enterprise / DES-M | Medium TMM | Named CSAM; CSA pooled across multiple accounts |
| 3 | **Programmatic** | SME&C / Lower Enterprise | Lower TMM | Success Programs + digital delivery; no named CSA |
| 4 | **Reactive Only** | Lower | Minimal TMM | Break-fix only; no proactive coverage |
| 5 | **Partner-Led** | All | Varies | Partner CSA/CSAM delivers under Microsoft standards |

# Routing Logic

```
IF TMM ≥ Designated Threshold AND segment = Enterprise → Engine 1 (Designated Managed)
ELIF TMM ≥ Pooled Threshold → Engine 2 (Pooled Managed)
ELIF has_unified_contract AND packages_sold → Engine 3 (Programmatic + Pooled CSA)
ELIF has_unified_contract → Engine 3 (Programmatic only)
ELSE → Engine 4 (Reactive) or Engine 5 (Partner-Led)
```

# Characteristics by Engine

## Engine 1: Designated Managed
- Named CSAM + named CSA with continuous engagement
- Full [CSP hierarchy](/csu/doctrine/csp-hierarchy.md) active
- Monthly [CSDR](/mcem/planning/csdr.md) cadence
- Target: highest-value accounts with complex multi-workload environments

## Engine 2: Pooled Managed
- Named CSAM; CSA assignments per engagement/project
- CSP created for top priorities only
- CSDR may be bi-monthly or triggered
- Target: high-growth accounts with moderate complexity

## Engine 3: Programmatic
- Engagement through [Success Programs](/csu/programs/success-programs.md) and digital motions
- CSA involved only for program delivery (multi-touch sequences)
- Scaled coverage; limited 1:1 engagement
- Target: broad base of Unified customers needing adoption acceleration

## Engine 4: Reactive Only
- Break-fix support only; no proactive delivery
- No CSAM assignment; handled by reactive support engineers
- Target: customers without Unified contracts or proactive investment

## Engine 5: Partner-Led
- Partner delivers proactive services under Microsoft co-management standards
- CSAM may coordinate but partner CSA executes delivery
- Target: partner-originated or partner-preference customers

# Implications for Resource Planning

The routing model directly drives:
- CSA demand forecasting (headcount per engine)
- Scoping demand (Engines 1–2 dominate scoping volume)
- Success Programs scale (Engine 3 is the scalability lever)
- [MACC](/mcem/planning/macc.md) quality coverage (only Engines 1–3 count as proactively managed)

# Source Systems

- **[MDM & GRM](/csu/evidence/mdm-grm.md)** — MDM package attributes and GRM routing and booking data determine how delivery demand is assigned.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
