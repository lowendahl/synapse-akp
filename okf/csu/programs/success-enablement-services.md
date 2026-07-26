---
type: Program
title: Success Enablement Services (ESA)
id: csu.program.success-enablement-services-esa
aliases: [ESA, SES, Success Enablement Services, Success Enablement Advisory]
description: Advisory service hours within Unified contracts providing strategic enablement, architecture guidance, and transformation planning. Distinct from reactive support and proactive EDE/STA delivery.
tags: [csu, programs, esa, ses, enablement, advisory, unified, delivery]
relationships:
  - predicate: extends
    object: mcem.planning.customer-success-planning
  - predicate: extends
    object: mcem.planning.account-planning
  - predicate: operationalizes
    object: mcem.stage.stage-2-inspire-design
  - predicate: delivered_by
    object: csu.delivery.udc-unified-delivery-coverage
  - predicate: tracks_metric
    object: csu.metric.booked-hours
  - predicate: drives
    object: csu.outcome.cloud-adoption-outcomes
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
sources:
  - id: ces-delivery-insights
    resource: "CES Delivery Insights semantic model"
    title: CES Delivery Insights
    last_modified: 2026-07-01
---
# Definition

**Success Enablement Services (ESA)** — also referred to as SES (Success Enablement Services) — are advisory service hours within [Unified](/mcem/unified/unified-support.md) contracts that provide strategic enablement, architecture guidance, and transformation planning to customers.

# Key Distinction

| Service Type | Nature | Delivered By |
|-------------|--------|--------------|
| **Reactive Support** | Break-fix, incident response | Support Engineers |
| **Proactive EDE/STA** | Scheduled technical delivery | CSAs (delivery engine) |
| **ESA** | Strategic advisory, transformation planning | Senior CSAs / Architects |

# Purpose

- Bridge the gap between reactive support and proactive delivery
- Provide architecture guidance for [Cloud Adoption](/csu/outcomes/cloud-adoption.md) and [AI Transformation](/csu/outcomes/ai-transformation.md)
- Enable customer self-sufficiency over time
- Drive adoption and usage metrics ([MAU](/csu/metrics/mau.md), [PAU](/csu/metrics/pau.md))

# Contract Mechanics

| Attribute | Detail |
|-----------|--------|
| **Allocation** | Hours per agreement year (varies by contract band) |
| **Tracking** | CES Delivery Insights `customer-unified-hours` recipe |
| **Cycle** | Agreement Start Date anchor (365-day rolling window) |
| **Unused hours** | Do not roll over between cycles |

# Evidence

| Source | Recipe/Measure | What It Shows |
|--------|---------------|---------------|
| CES Delivery Insights | `customer-unified-hours` | ESA hours (all-time), ESA hours in trailing 365-day cycle |
| CES Delivery Insights | `customer-unified` | Agreement band (determines ESA entitlement) |

# Relationship to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Unified Support](/mcem/unified/unified-support.md) | ESA is a service component within Unified |
| [EDE/STA](/mcem/unified/enhanced-solutions.md) | Complementary — EDE/STA is scheduled delivery; ESA is advisory |
| [UDC](/csu/delivery/udc.md) | ESA hours are tracked separately from UDC package hours |
| [UCR](/mcem/unified/consumed-revenue.md) | ESA utilization contributes to UCR |
| [CSDR](/mcem/planning/csdr.md) | ESA delivery progress reviewed in CSDR |
| [CSP Hierarchy](/csu/doctrine/csp-hierarchy.md) | ESA engagements should align to CSP priorities |
