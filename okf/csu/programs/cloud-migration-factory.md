---
type: Program
title: Cloud Migration Factory (CMF)
id: csu.program.cloud-migration-factory-cmf
aliases: [CMF, Cloud Migration Factory, Migration Factory]
description: Scaled migration delivery engine that accelerates Azure workload migration through repeatable patterns, partner delivery, and ECIF-funded engagements. Drives Job 1 milestone completion and MACC consumption.
tags: [csu, programs, cmf, migration, azure, scaled, delivery]
relationships:
  - predicate: extends
    object: mcem.planning.macc-consumption-planning
  - predicate: operationalizes
    object: csu.outcome.cloud-adoption-outcomes
  - predicate: operationalizes
    object: csu.process.commit-to-complete
generated: { by: human:plwendahl, at: 2026-07-25T02:30:00Z }
status: stable
---
# Definition

**Cloud Migration Factory (CMF)** is CSU's scaled migration delivery engine. It accelerates Azure workload migration from on-premises or other clouds to Azure through standardized, repeatable delivery patterns executed by partners and CSAs.

# Purpose

- Convert on-premises workloads to Azure consumption at scale
- Directly accelerate [MACC](/mcem/planning/macc.md) consumption pacing
- Generate [Job 1 milestones](/csu/metrics/job1-commit-to-complete.md) through migration completions
- Drive [Technical Maturity Model](/csu/doctrine/technical-maturity-model.md) progression from On-Prem → Growth

# Operating Model

```
Identify → Assess → Plan → Migrate → Optimize → Hand-off
```

| Phase | Activity | Outcome |
|-------|----------|---------|
| **Identify** | MIRP accounts with large on-prem estate | Migration candidate pipeline |
| **Assess** | Azure Migrate / discovery | Workload inventory + readiness |
| **Plan** | Migration wave planning | Sequenced migration plan with milestones |
| **Migrate** | Partner-led execution (ECIF-funded) | Workloads running on Azure |
| **Optimize** | Right-sizing, reserved instances | Optimized consumption |
| **Hand-off** | Operational ownership to customer | Sustained ACR |

# Funding Model

CMF engagements are typically funded via [ECIF](/csu/programs/ecif.md):

```
ECIF Request → CMF Workscope → Partner Assignment → Migration Delivery → NNR Attribution
```

# Delivery Patterns

| Pattern | Scope | Typical Duration |
|---------|-------|-----------------|
| **Infra migration** | VMs, storage, networking | 3–6 months |
| **Data migration** | SQL → Azure SQL/Synapse | 2–4 months |
| **App modernization** | .NET/Java to AKS/App Service | 4–8 months |
| **SAP migration** | SAP ECC/S4 to Azure | 6–12 months |

# Evidence Path

| Concept | How CMF Drives It |
|---------|-------------------|
| [MACC ACR](/csu/evidence/macc-evidence.md) | Every migrated workload adds sustained monthly ACR |
| [Job 1 C2C](/csu/evidence/job1-evidence.md) | Each migration wave maps to committed milestones |
| [ECIF Yield](/csu/evidence/ecif-evidence.md) | Migration NNR / ECIF $ invested |

# Relationship to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [ECIF](/csu/programs/ecif.md) | CMF funded by ECIF grants |
| [MACC](/mcem/planning/macc.md) | CMF accelerates MACC consumption |
| [TMM](/csu/doctrine/technical-maturity-model.md) | Moves customers from On-Prem → Growth |
| [Partners](/mcem/organization/partners.md) | Delivery executed by migration partners |
| [FastStart](/csu/programs/faststart.md) | FastStart may precede CMF for small initial workloads |
