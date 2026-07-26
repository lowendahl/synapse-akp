---
type: Outcome Framework
title: Cloud Adoption Outcomes
id: csu.outcome.cloud-adoption-outcomes
description: CSU's outcome framework governing workload migration, modernization, optimization, and consumption growth to accelerate customer cloud value realization.
tags: [csu, outcomes, cloud-adoption, azure, migration, modernization, consumption]
relationships:
  - predicate: depends_on
    object: csu.priority.realize-value-faster
  - predicate: operationalizes
    object: mcem.stage.stage-3-empower-achieve
  - predicate: operationalizes
    object: mcem.stage.stage-4-realize-value
  - predicate: depends_on
    object: csu.program.cloud-migration-factory-cmf
generated: { by: human:plwendahl, at: 2026-07-25T02:00:00Z }
status: stable
sources:
  - id: ces-fy27-manager-deck
    resource: "FY27 CE&S Manager Deck"
    title: FY27 CE&S Manager Deck
    author: team:ces-leadership
    last_modified: 2026-07-01
  - id: csu-fy27-priorities-okf
    resource: "CSU FY27 Priorities OKF corpus"
    title: CSU FY27 Priorities
    last_modified: 2026-07-20
---
# Definition

Cloud Adoption Outcomes is CSU's framework for driving and measuring the customer's journey from on-premises or underutilized cloud estate to fully adopted, optimized, and growing Azure consumption. It provides the outcome lens through which [CSPs](/csu/doctrine/csp-hierarchy.md) focused on infrastructure and platform workloads are structured and measured.

# The Cloud Adoption Maturity Model

| Stage | Outcome Focus | CSU Activity |
|-------|--------------|-------------|
| **Assess** | Understand current estate; define cloud business case | Discovery assessments, TCO analysis, migration readiness |
| **Migrate** | Move workloads to Azure with minimal disruption | Migration execution, FastTrack, Well-Architected reviews |
| **Modernize** | Refactor for cloud-native value; PaaS/containers | Architecture modernization, AKS adoption, data platform upgrades |
| **Optimize** | Right-size, govern cost, maximize performance | FinOps, Reserved Instances, Azure Advisor remediation |
| **Scale** | Expand footprint; net-new workloads | New workload onboarding, consumption pipeline growth |

# Key Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| ACR Growth | Azure Consumed Revenue period-over-period | Per account/territory target |
| MACC Consumption | Actual consumption against MACC commitment | ≥100% of annual commitment |
| Workload Count | Distinct workloads running on Azure | Increasing quarter-over-quarter |
| Migration Completion | % of identified migration candidates moved | Per account plan |
| Optimization Savings | Cost reduction from optimization activities | Reinvested into new workloads |

# CSP Alignment

Cloud Adoption CSPs should:
- Link to a Customer Objective focused on infrastructure modernization, cost reduction, or agility
- Define milestones per maturity stage (assess → migrate → optimize)
- Track consumption pipeline impact (new [Azure opportunities](/csu/pipeline/azure/opportunity.md))
- Connect to [MACC](/mcem/planning/macc.md) commitment and quality gates

# Delivery Vehicles

| Vehicle | Role in Cloud Adoption |
|---------|----------------------|
| [EDE/STA](/mcem/unified/enhanced-solutions.md) | Named CSA driving migration/modernization execution |
| [Success Programs](/csu/programs/success-programs.md) | Scaled multi-touch programs (Azure Well-Architected, Security Baseline) |
| FastTrack | Microsoft-funded migration support |
| Partner | ISV/SI migration and management services |

# Connection to FY27 Priorities

Cloud Adoption directly supports:
- [Realize Value Faster](/csu/priorities/realize-value-faster.md) — accelerating time to production workloads
- [Grow Azure Committed & Consumed](/csu/priorities/) — driving MACC utilization and ACR growth

# Outcome Evidence

A Cloud Adoption outcome is evidenced when:
1. Workload(s) are running in production on Azure
2. Consumption is stable or growing (not spike-and-drop)
3. Customer reports measurable business value (cost savings, agility, performance)
4. CSP milestones are marked complete
5. [C2C](/csu/processes/commit-to-complete.md) accountability recorded
