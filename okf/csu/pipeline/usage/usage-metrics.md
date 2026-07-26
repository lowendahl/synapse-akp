---
type: Metric Collection
title: Usage Metrics
id: csu.pipeline.usage-metrics
description: Core usage health indicators — MAU, PAU, PRU — measuring depth of workload adoption.
tags: [csu, pipeline, usage, metrics, mau, pau, pru]
relationships:
  - predicate: informs
    object: csu.metric.mau-monthly-active-users
  - predicate: informs
    object: csu.metric.pau-productive-active-users
  - predicate: informs
    object: csu.metric.pru-productive-recurring-user
  - predicate: informs
    object: mcem.metric.customer-health
generated: { by: human:plwendahl, at: 2026-07-25T01:00:00Z }
status: stable
sources:
  - id: mcem-usage-pipeline-okf
    resource: "MCEM Usage Pipeline OKF corpus"
    title: MCEM Usage Pipeline OKF Corpus
    last_modified: 2026-07-19
---
# Core Metrics

| Metric | Full Name | Definition |
|--------|-----------|------------|
| MAU | Monthly Active Users | Unique users actively using a workload in a calendar month |
| PAU | Paid Active Users | MAU subset on paid/licensed SKUs |
| PRU | Paid Retained Users | PAU retained month-over-month (retention signal) |

# Measurement Scope

These metrics apply across all measured workloads:
- Microsoft 365 Copilot
- Azure AI services
- Security workloads
- Core productivity (Teams, SharePoint, etc.)

# Health Interpretation

| Signal | Interpretation |
|--------|----------------|
| MAU growing, PAU flat | Trial adoption without conversion |
| PAU growing, PRU declining | Churn — users adopting but not retaining |
| All three growing | Healthy adoption trajectory |
| All three declining | Critical — immediate intervention via [Motion 2](/csu/processes/existing-deals-motion.md) |

# Governance

Usage metrics feed into [Customer Health](/mcem/metrics/customer-health.md) and are a primary CSAM priority in FY27.

# Source Systems

- **[MSX Dataverse](/csu/evidence/msx-dataverse.md)** — milestone and opportunity data used to measure usage-oriented pipeline execution.
- **[MSX Insights (MSXi)](/csu/evidence/msxi.md)** — KPI measurement, snapshot metrics, and actual outcome tracking (ACR, labour hours, close rates).
