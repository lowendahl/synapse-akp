---
type: KPI
title: "Remaining Hours"
id: csu.metric.remaining-hours
description: Undelivered Enhanced Solutions hours within the current contract lifecycle — measures delivery pacing risk.
tags: [csu, kpi, remaining-hours, delivery, pacing, ede, leading]
relationships:
  - predicate: measures
    object: csu.delivery.csu-delivery-process
  - predicate: measures
    object: mcem.unified.enhanced-solutions-ede-sta
  - predicate: evidenced_by
    object: csu.evidence.delivery-evidence-udc-ucr-hours
classification: leading
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-delivery-insights
    resource: "CES Delivery Insights"
    title: Remaining Hours Tracking
    last_modified: 2026-07-01
---
# Definition

**Remaining Hours** measures the undelivered [Enhanced Solutions](/mcem/unified/enhanced-solutions.md) hours within the current contract lifecycle. It is the gap between sold hours and consumed hours, indicating delivery pacing risk.

**Classification: LEADING** — high remaining hours late in contract = UDC failure and renewal risk ahead.

# Formula

```
Remaining Hours = Sold Hours − Consumed Hours
Remaining % = Remaining Hours / Sold Hours
```

# Risk Signal

| Contract Position | Remaining % | Signal |
|-------------------|-------------|--------|
| < 50% through contract | > 50% remaining | Normal — on pace |
| > 50% through contract | > 60% remaining | Warning — delivery acceleration needed |
| > 75% through contract | > 40% remaining | Critical — UDC target at risk |

# Relationship to UDC

Remaining Hours is the inverse input to [UDC](/csu/delivery/udc.md):
```
UDC = (Sold − Remaining + Pre-billed) / Prorated Sold
```

High remaining hours directly threatens UDC achievement.

# Causal Chain

```
Upstream: Scoping quality, CSA assignment speed, Delivery cadence
    → Remaining Hours (THIS)
        → Downstream: UDC, UCR, Renewal pacing, Customer outcome delivery
```

# Source Systems

- **CES Delivery Insights** — sold hours, consumed hours, contract position

# Evidence Path

| Source | Artifact ID | Key Measures |
|--------|------------|-------------|
| CES Delivery Insights | `56064262-fdfa-4c3d-968f-dffd3ebf759a` | `[Sold Hours]` − `[Consumed Hours]` = Remaining |

**Key recipe:** `package-detail` — per-package sold/consumed/remaining/prorated hours.

**Risk recipe:** `package-risk` — packages with high remaining hours AND approaching expiry.

See also: [Delivery Evidence](/csu/evidence/delivery-evidence.md)