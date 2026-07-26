# ADR-033: Measure → Indicator → KPI Promotion Chain

| Field | Value |
|-------|-------|
| **ID** | `ADR-033` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-018 (unified pipeline), ADR-020 (assertion confidence) |

## Context

Business corpora frequently conflate "metric", "measure", "indicator", and "KPI". A sentence like "Track ACR as our key metric" is ambiguous — does "key metric" mean it is a governed KPI with a target, or simply an important measure?

The compiler must distinguish these concepts rigorously because they have **different governance requirements**:

- A **Measure** exists if it is quantifiable and referenced (low bar).
- An **Indicator** exists if a measure is used to indicate, evaluate, or predict something (requires interpretive context).
- A **KPI** exists only if an indicator has governance evidence: target, owner, cadence, and accountability (high bar).

Conflating these creates false authority: labelling every mentioned metric as a "KPI" implies governance that may not exist.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Flat classification (measure or KPI)** | Simple | Loses indicator semantics; over-promotes measures |
| **B. Type hierarchy with implicit promotion** | Less storage | Hides governance gaps |
| **C. Explicit promotion chain with evidence gates (chosen)** | Precise; auditable; surfaces governance gaps | More stages; more review items |

## Decision

Implement a three-tier entity promotion chain:

```
Measure ──[interpretive evidence]──> Indicator ──[governance evidence]──> KPI
```

Each promotion is an **independent assertion** (ADR-020) with its own confidence and evidence.

### Tier Definitions

| Tier | Minimum Evidence | Examples |
|------|-----------------|----------|
| **Measure** | Named quantifiable property mentioned in corpus | "Delivery Coverage", "Revenue Growth Rate" |
| **Indicator** | Measure + "indicates X", "predicts Y", "evaluates Z" | "Delivery Coverage indicates readiness" |
| **KPI** | Indicator + target AND (owner OR cadence OR accountability) | "Delivery Coverage target ≥85%, owned by Delivery Lead, reviewed monthly" |

### Classification Rules

1. **A measure stays a measure** unless there is explicit interpretive context promoting it.
2. **Leading vs. lagging** is context-sensitive, not intrinsic — the same measure can be leading for one objective and lagging for another.
3. **KPI status requires governance evidence** — a target alone is insufficient; the compiler looks for ownership, cadence, or accountability language.
4. **Demotion is possible** — if reviewed evidence contradicts KPI status, the entity reverts to Indicator or Measure.
5. **Ambiguous promotions enter the review queue** — confidence below threshold produces a review item, not a false promotion.

### Separate Entities, Not Properties

Measures, Indicators, and KPIs are **distinct entities** in the data model, not properties of one entity:

```
measure.delivery-coverage          → BaseMeasure
indicator.delivery-coverage-readiness → LeadingIndicator (references measure)
kpi.delivery-coverage-gov          → KPI (references indicator, has target + owner)
```

This allows:
- A measure to have multiple indicator interpretations.
- An indicator to be governed as a KPI in one context but not another.
- Each tier to have independent confidence and review status.

## Consequences

- The DuckDB schema has separate `measure`, `indicator`, and `kpi` tables (ADR-025).
- Diagnostic SEM012 fires when an indicator lacks an indicated state.
- Diagnostic SEM013 fires when a KPI lacks an objective.
- Diagnostic SEM014 fires when a KPI lacks a target or threshold.
- Diagnostic SEM022 fires when a measure may be incorrectly classified as a KPI.
- The runtime exposes distinct queries: `find_measures()`, `find_indicators()`, `find_kpis()`.
- Review items clearly show what evidence is missing for promotion (actionable for corpus authors).
