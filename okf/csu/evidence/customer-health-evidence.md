---
type: Evidence Map
title: Customer Health Evidence
id: csu.evidence.customer-health-evidence
description: Evidence path from Customer Health Revenue at Risk to its semantic model and investigation patterns.
tags: [csu, evidence, customer-health, risk, semantic-model]
relationships:
  - predicate: references
    object: csu.evidence.msx-insights-msxi-analytics-measurement
  - predicate: references
    object: csu.metric.customer-health-revenue-at-risk
  - predicate: references
    object: mcem.metric.customer-health
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
---
# Concept

**[Customer Health Revenue at Risk](/csu/metrics/customer-health-rar.md)**: % of revenue on customers failing health checklist activities.

# Evidence Sources

## Primary: Customer Health Revenue at Risk

| Attribute | Value |
|-----------|-------|
| **PBI Artifact ID** | `57664612-66df-4081-9e99-4edeebefc65e` |
| **Domain** | Customer Health Program |
| **Grain** | Customer (TPID) × health checklist items |

# Investigation Patterns

## "How much revenue is at risk from health failures?"

→ Sum revenue on customers failing health bar / total in-scope revenue

## "Which customers have the most health debt?"

→ Filter to customers failing ≥3 checklist items, sorted by revenue DESC

## "What specific health items are failing most?"

→ Aggregate by checklist item across all at-risk customers → surfaces systemic gaps

# Related Evidence

- [Delivery Evidence](/csu/evidence/delivery-evidence.md) — UDC health feeds customer health
- [MACC Evidence](/csu/evidence/macc-evidence.md) — MACC execution score includes health sub-score
