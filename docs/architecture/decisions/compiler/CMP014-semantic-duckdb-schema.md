# ADR-037: Semantic DuckDB Runtime Schema

| Field | Value |
|-------|-------|
| **ID** | `ADR-037` |
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Decision Makers** | Patrik Lowendahl |
| **Related** | ADR-003 (DuckDB as physical engine), ADR-018 (unified pipeline), ADR-020 (assertions), ADR-021 (promotion chain) |

## Context

ADR-003 established DuckDB as the physical metadata engine. The acronym subpackage (ADR-015) defined 3 tables (`acronym_concept`, `acronym_occurrence`, `acronym_index`). The unified semantic pipeline requires a much broader schema that accommodates:

- All entity types from the taxonomy (ADR-019).
- Assertion-level confidence (ADR-020).
- The measure → indicator → KPI promotion chain (ADR-021).
- Formula definitions and dependencies (ADR-022).
- Source layer provenance (ADR-023).
- Occurrence-level tracking (which document mentions which entity, where).
- Relationship graph edges.
- Review queue state.
- Diagnostics.

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| **A. Single denormalized entity table** | Simple queries | Massive columns; type-specific fields are sparse |
| **B. EAV (entity-attribute-value)** | Flexible | Poor query performance; no type safety |
| **C. Typed tables with shared assertion table (chosen)** | Type-safe per tier; assertion model is uniform | More tables; requires joins |

## Decision

The compiled AKP DuckDB database contains the following tables:

### Core Entity Tables

```sql
-- All semantic entities (concepts, processes, roles, states, events, etc.)
CREATE TABLE semantic_entity (
    entity_id VARCHAR PRIMARY KEY,
    entity_type VARCHAR NOT NULL,      -- From taxonomy
    name VARCHAR NOT NULL,
    description VARCHAR,
    status VARCHAR NOT NULL,           -- authored | reviewed | inferred | unresolved | rejected
    confidence DOUBLE,
    source_layer VARCHAR NOT NULL,     -- authored | reviewed | generated
    generated BOOLEAN NOT NULL
);

-- Aliases and alternative surface forms
CREATE TABLE semantic_alias (
    alias_id VARCHAR PRIMARY KEY,
    entity_id VARCHAR NOT NULL REFERENCES semantic_entity(entity_id),
    surface_form VARCHAR NOT NULL,
    normalized_form VARCHAR NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE
);

-- Where entities are mentioned in the corpus
CREATE TABLE semantic_occurrence (
    occurrence_id VARCHAR PRIMARY KEY,
    entity_id VARCHAR NOT NULL REFERENCES semantic_entity(entity_id),
    document VARCHAR NOT NULL,
    section VARCHAR,
    line_start INTEGER,
    line_end INTEGER,
    context_snippet VARCHAR,
    detection_method VARCHAR NOT NULL
);
```

### Assertion Table (ADR-020)

```sql
CREATE TABLE semantic_assertion (
    assertion_id VARCHAR PRIMARY KEY,
    subject_id VARCHAR NOT NULL,
    predicate VARCHAR NOT NULL,
    object_id VARCHAR,
    literal_value VARCHAR,
    confidence DOUBLE NOT NULL,
    status VARCHAR NOT NULL,           -- authored | reviewed | inferred | unresolved | rejected
    source_document VARCHAR NOT NULL,
    source_section VARCHAR,
    source_line_start INTEGER,
    source_line_end INTEGER,
    evidence_span VARCHAR,
    method VARCHAR NOT NULL            -- pattern | llm | rule | embedding | human
);
```

### Measure/Formula Tables (ADR-021, ADR-022)

```sql
CREATE TABLE measure (
    measure_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    measure_type VARCHAR NOT NULL,     -- BaseMeasure | DerivedMeasure | CalculatedMeasure
    value_type VARCHAR,
    unit_id VARCHAR,
    aggregation VARCHAR,
    confidence DOUBLE
);

CREATE TABLE measure_formula (
    formula_id VARCHAR PRIMARY KEY,
    measure_id VARCHAR NOT NULL REFERENCES measure(measure_id),
    source_text VARCHAR NOT NULL,
    canonical_expression VARCHAR,      -- SymPy-normalized
    aggregation VARCHAR,
    confidence DOUBLE
);

CREATE TABLE measure_dependency (
    measure_id VARCHAR NOT NULL REFERENCES measure(measure_id),
    input_measure_id VARCHAR NOT NULL REFERENCES measure(measure_id),
    formula_id VARCHAR REFERENCES measure_formula(formula_id),
    PRIMARY KEY (measure_id, input_measure_id)
);

CREATE TABLE measure_dimension (
    measure_id VARCHAR NOT NULL REFERENCES measure(measure_id),
    dimension_id VARCHAR NOT NULL,
    PRIMARY KEY (measure_id, dimension_id)
);
```

### Indicator/KPI Tables (ADR-021)

```sql
CREATE TABLE indicator (
    indicator_id VARCHAR PRIMARY KEY,
    measure_id VARCHAR NOT NULL REFERENCES measure(measure_id),
    indicator_type VARCHAR NOT NULL,   -- LeadingIndicator | LaggingIndicator | DiagnosticIndicator
    confidence DOUBLE
);

CREATE TABLE kpi (
    kpi_id VARCHAR PRIMARY KEY,
    indicator_id VARCHAR NOT NULL REFERENCES indicator(indicator_id),
    objective_id VARCHAR,
    owner_id VARCHAR,
    cadence VARCHAR,
    confidence DOUBLE
);

CREATE TABLE objective (
    objective_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    confidence DOUBLE
);

CREATE TABLE target (
    target_id VARCHAR PRIMARY KEY,
    kpi_id VARCHAR NOT NULL REFERENCES kpi(kpi_id),
    operator VARCHAR NOT NULL,         -- >=, <=, ==, >, <
    value DOUBLE,
    unit VARCHAR,
    time_horizon VARCHAR,
    confidence DOUBLE
);

CREATE TABLE threshold (
    threshold_id VARCHAR PRIMARY KEY,
    kpi_id VARCHAR NOT NULL REFERENCES kpi(kpi_id),
    level VARCHAR NOT NULL,            -- green | amber | red
    operator VARCHAR NOT NULL,
    value DOUBLE,
    confidence DOUBLE
);
```

### Supporting Tables

```sql
CREATE TABLE dimension (
    dimension_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    values_known TEXT[]                 -- Known categorical values
);

CREATE TABLE unit (
    unit_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    symbol VARCHAR,
    dimension VARCHAR                   -- length, time, currency, ratio, etc.
);

CREATE TABLE semantic_relationship (
    relationship_id VARCHAR PRIMARY KEY,
    source_id VARCHAR NOT NULL,
    target_id VARCHAR NOT NULL,
    relationship_type VARCHAR NOT NULL, -- IS_A, PART_OF, MEASURES, DERIVED_FROM, etc.
    confidence DOUBLE,
    assertion_id VARCHAR REFERENCES semantic_assertion(assertion_id)
);
```

### Governance Tables

```sql
CREATE TABLE semantic_review (
    review_id VARCHAR PRIMARY KEY,
    assertion_id VARCHAR NOT NULL REFERENCES semantic_assertion(assertion_id),
    status VARCHAR NOT NULL,           -- pending | approved | corrected | rejected
    reviewer VARCHAR,
    reviewed_at TIMESTAMP,
    reason VARCHAR
);

CREATE TABLE semantic_diagnostic (
    diagnostic_id VARCHAR PRIMARY KEY,
    code VARCHAR NOT NULL,             -- SEM001..SEM024
    severity VARCHAR NOT NULL,         -- info | warning | review-required | error
    entity_id VARCHAR,
    assertion_id VARCHAR,
    message VARCHAR NOT NULL,
    source_document VARCHAR,
    source_line INTEGER
);
```

### Migration from Acronym Tables

The existing `acronym_concept`, `acronym_occurrence`, and `acronym_index` tables are subsumed:

| Old Table | New Table | Mapping |
|-----------|-----------|---------|
| `acronym_concept` | `semantic_entity` + `semantic_alias` | entity_type = "Acronym" |
| `acronym_occurrence` | `semantic_occurrence` | detection_method = "acronym_pattern" |
| `acronym_index` | `semantic_entity` (queried with type filter) | — |

## Consequences

- A single schema serves all semantic extraction features.
- The runtime query layer (ADR-018 §43) operates over these tables.
- New entity types from taxonomy extensions automatically fit into `semantic_entity`.
- Foreign keys enforce referential integrity at compile time.
- DuckDB's columnar format handles the assertion table efficiently even with millions of rows.
- The schema is versioned — a `schema_version` metadata table tracks migrations.
