# AKP Pack Format Specification

## 1. Status and Scope

This document defines the AKP Knowledge Pack file format emitted by the compiler and consumed by the runtime. The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119.

This specification defines **Schema 2.0.0**.

## 2. Artifact Set

An AKP Knowledge Pack is a packaged retrieval corpus consisting of:

- a primary database file named `<pack-id>.duckdb`
- an OPTIONAL vector sidecar file named `<pack-id>.usearch`

The `.duckdb` file MUST be the canonical pack artifact. The runtime MUST treat the `.duckdb` file as authoritative for metadata, graph data, semantic units, aliases, and lexical retrieval content.

The `.duckdb` file MUST be SQLite-compatible via DuckDB usage patterns supported by the AKP toolchain.

## 3. Pack Identity

### 3.1 Naming Convention

A `pack_id` MUST use the naming convention:

`publisher.domain.package`

Examples:

- `microsoft.finance.ledger`
- `contoso.hr.policies`

A `pack_id` MUST be globally stable for a logical package line. A new package lineage MUST use a different `pack_id`.

### 3.2 File Naming

The compiler MUST emit the primary file as `<pack-id>.duckdb`.
If a vector sidecar is emitted, it MUST be named `<pack-id>.usearch`.
The runtime MUST associate a sidecar only when the basename exactly matches the pack database basename.

## 4. Versioning and Compatibility

### 4.1 Pack Version

`pack_version` MUST follow Semantic Versioning (semver).
Publishers SHOULD increment:

- MAJOR for incompatible content contracts or identifier migrations
- MINOR for backward-compatible content additions
- PATCH for corrections that preserve existing contracts

### 4.2 Schema Version

`schema_version` MUST be `2.0.0` for packs conforming to this specification.
The schema MAJOR version determines runtime compatibility.
A runtime that supports schema major `2` MUST accept `2.x.y` packs and MUST reject packs with any other major version unless explicitly upgraded to support them.

### 4.3 Ontology and Compiler Versions

`ontology_version` and `compiler_version` MUST be recorded in the manifest.
The runtime MAY expose these values in diagnostics and provenance.

## 5. Physical Storage Rules

1. The primary artifact MUST be a DuckDB database file.
2. All required tables defined by this specification MUST exist.
3. Optional tables MAY be omitted when the corresponding feature is not produced.
4. Column names and declared logical meanings MUST match this specification exactly.
5. Additional tables MAY be present for forward-compatible extensions, but consumers MUST ignore unknown tables unless explicitly configured otherwise.
6. Additional columns SHOULD NOT be added to required tables in schema `2.0.0`; if required, such change SHOULD be introduced in a later schema version.

## 6. Manifest Table

The pack MUST contain a manifest table with the following schema:

```sql
CREATE TABLE manifest (
  key VARCHAR PRIMARY KEY,
  value VARCHAR
);
```

The manifest table is a key-value store. Each required key MUST appear exactly once.

### 6.1 Required Manifest Keys

The following keys are REQUIRED:

- `pack_id`
- `pack_version`
- `schema_version`
- `ontology_version`
- `compiler_version`
- `build_timestamp`
- `source_file_count`
- `object_count`
- `node_count`
- `edge_count`
- `semantic_unit_count`
- `alias_count`
- `bm25_vocab_size`
- `embedding_model`
- `embedding_dimensions`
- `cross_pack_refs`
- `content_hash`
- `error_count`
- `warning_count`

### 6.2 Manifest Semantics

- `pack_id` MUST equal the logical package identity and SHOULD match the emitted filename stem.
- `pack_version` MUST be semver.
- `schema_version` MUST be `2.0.0` for this specification.
- `build_timestamp` SHOULD be an RFC 3339 / ISO 8601 UTC timestamp.
- Count fields MUST represent the final persisted object counts after compilation.
- `embedding_model` SHOULD identify the embedding model used to produce vectors; it MAY be empty when embeddings are not emitted.
- `embedding_dimensions` MUST reflect the vector dimensionality when embeddings are emitted; otherwise it MAY be `0` or an empty string by compiler convention.
- `cross_pack_refs` MUST summarize whether cross-pack references were emitted or the number of such references, according to compiler policy, but the value MUST be stable and machine-readable within a deployment.
- `content_hash` MUST represent the integrity hash of the persisted pack contents.
- `error_count` and `warning_count` MUST reflect compiler diagnostics captured for the build.

## 7. Required Tables

The following tables are REQUIRED for schema `2.0.0`.

### 7.1 `objects`

```sql
CREATE TABLE objects (
  id VARCHAR PRIMARY KEY,
  type VARCHAR NOT NULL,
  title VARCHAR,
  description VARCHAR,
  domain VARCHAR,
  status VARCHAR,
  aliases JSON,
  tags JSON,
  source_path VARCHAR,
  properties JSON
);
```

Semantics:

- Each row represents a canonical object addressable by `id`.
- `id` MUST be unique within the pack.
- `type` MUST be populated.
- `aliases`, `tags`, and `properties` MUST contain JSON values when present.
- `source_path` SHOULD reference the originating source artifact path relative to the compiler input root when available.

### 7.2 `semantic_units`

```sql
CREATE TABLE semantic_units (
  id VARCHAR PRIMARY KEY,
  source_object_id VARCHAR NOT NULL,
  heading_path VARCHAR,
  content VARCHAR,
  context VARCHAR,
  object_type VARCHAR,
  domain VARCHAR
);
```

Semantics:

- Each row represents a retrieval unit derived from or attached to a source object.
- `source_object_id` MUST reference `objects.id` for the logical parent object.
- `content` SHOULD contain the retrievable textual payload.
- `heading_path` MAY encode hierarchical section context.
- `context` MAY include compiler-expanded neighborhood or summary text.

### 7.3 `aliases`

```sql
CREATE TABLE aliases (
  alias VARCHAR NOT NULL,
  canonical_id VARCHAR NOT NULL,
  alias_type VARCHAR DEFAULT 'exact'
);
```

Semantics:

- Multiple rows MAY point to the same canonical object.
- `canonical_id` SHOULD reference `objects.id`.
- `alias_type` MUST default to `exact` when not explicitly set.

### 7.4 `edges`

```sql
CREATE TABLE edges (
  subject_id VARCHAR NOT NULL,
  predicate VARCHAR NOT NULL,
  object_id VARCHAR NOT NULL,
  origin VARCHAR NOT NULL,
  confidence FLOAT
);
```

Semantics:

- Each row represents a directed graph edge.
- `subject_id` and `object_id` SHOULD reference canonical object identifiers.
- `origin` MUST describe the production origin of the edge, such as authored, derived, or inferred.
- `confidence` MAY be null when confidence is not applicable.

### 7.5 `manifest`

```sql
CREATE TABLE manifest (
  key VARCHAR PRIMARY KEY,
  value VARCHAR
);
```

The manifest table definition is normative and REQUIRED.

## 8. Optional Tables (V2 Extensions)

The following tables are OPTIONAL V2 extensions. If present, they MUST conform exactly to the schemas below.

### 8.1 `nodes`

```sql
CREATE TABLE nodes (
  id VARCHAR PRIMARY KEY,
  type VARCHAR NOT NULL,
  title VARCHAR,
  domain VARCHAR,
  source_path VARCHAR,
  pagerank FLOAT,
  in_degree INTEGER,
  out_degree INTEGER
);
```

`nodes` MAY duplicate or denormalize object information for graph-optimized workloads.

### 8.2 `bm25_tokens`

```sql
CREATE TABLE bm25_tokens (
  unit_id VARCHAR NOT NULL,
  tokens JSON NOT NULL
);
```

If present, `tokens` MUST be serialized JSON suitable for reconstructing lexical retrieval state for the semantic unit referenced by `unit_id`.

### 8.3 `vector_metadata`

```sql
CREATE TABLE vector_metadata (
  unit_id VARCHAR PRIMARY KEY,
  model_name VARCHAR NOT NULL,
  model_version VARCHAR NOT NULL,
  dimensions INTEGER NOT NULL,
  input_hash VARCHAR NOT NULL
);
```

If vectors are emitted, `vector_metadata` SHOULD be present. `unit_id` SHOULD reference `semantic_units.id`.

### 8.4 `cross_pack_refs`

```sql
CREATE TABLE cross_pack_refs (
  source_id VARCHAR NOT NULL,
  target_qualified_id VARCHAR NOT NULL,
  target_pack VARCHAR NOT NULL,
  predicate VARCHAR NOT NULL DEFAULT 'references',
  resolved BOOLEAN DEFAULT FALSE
);
```

This table MAY be present when the compiler emits references crossing pack boundaries.

## 9. Relational and Content Invariants

The following invariants apply:

1. A pack MUST be immutable after write. Any content change MUST produce a new build artifact rather than in-place mutation.
2. The `content_hash` manifest value MUST allow integrity verification of the persisted pack content.
3. `object_count`, `node_count`, `edge_count`, `semantic_unit_count`, and `alias_count` SHOULD match the actual persisted row counts of their corresponding tables when those tables exist.
4. Every `semantic_units.source_object_id` SHOULD resolve to an `objects.id` value.
5. Every `aliases.canonical_id` SHOULD resolve to an `objects.id` value.
6. Every `edges.subject_id` and `edges.object_id` SHOULD resolve to canonical identifiers, except when a deployment explicitly permits unresolved references.
7. JSON columns MUST contain valid JSON text when non-null.
8. The runtime MUST treat the primary database as read-only pack content.

## 10. Sidecar Contract (`.usearch`)

The `.usearch` sidecar is OPTIONAL.

If a pack includes vector retrieval, the compiler SHOULD emit a `.usearch` sidecar and SHOULD emit `vector_metadata`.
If the sidecar exists, the runtime MUST treat it as bound to the corresponding `.duckdb` file with the same basename.

### 10.1 Ordering Contract

The `.usearch` file MUST contain semantic unit vectors in **rowid order matching the `vector_metadata` table rowid order**.

Therefore:

- row `n` in the sidecar MUST correspond to rowid `n` in `vector_metadata` according to the compiler/runtime contract
- `vector_metadata.unit_id` MUST identify the semantic unit represented by that vector row
- `vector_metadata.dimensions` MUST match the dimensionality of vectors stored in the sidecar

If this ordering contract cannot be satisfied, the runtime MUST reject semantic search for that pack.

### 10.2 Optionality

If the sidecar is absent:

- the pack MUST remain valid as a lexical/graph/object lookup pack
- the runtime MAY disable semantic retrieval for that pack
- the runtime SHOULD surface a diagnostic when semantic retrieval is requested but no sidecar is available

## 11. Runtime Validation Requirements

A conforming runtime implementation for schema major `2`:

1. MUST verify the presence of all required tables.
2. MUST verify the presence of all required manifest keys.
3. MUST verify `schema_version` compatibility by major version.
4. MUST reject a pack whose `pack_id` conflicts with another loaded pack identity in the same runtime instance.
5. SHOULD validate the sidecar contract before enabling vector retrieval.
6. MAY ignore optional tables it does not use.

## 12. Forward Compatibility

Unknown optional tables MAY be ignored.
Unknown manifest keys MAY be preserved or surfaced diagnostically.
Breaking schema changes MUST use a new schema MAJOR version.

## 13. Summary of Normative Schemas

```sql
CREATE TABLE objects (
  id VARCHAR PRIMARY KEY,
  type VARCHAR NOT NULL,
  title VARCHAR,
  description VARCHAR,
  domain VARCHAR,
  status VARCHAR,
  aliases JSON,
  tags JSON,
  source_path VARCHAR,
  properties JSON
);

CREATE TABLE semantic_units (
  id VARCHAR PRIMARY KEY,
  source_object_id VARCHAR NOT NULL,
  heading_path VARCHAR,
  content VARCHAR,
  context VARCHAR,
  object_type VARCHAR,
  domain VARCHAR
);

CREATE TABLE aliases (
  alias VARCHAR NOT NULL,
  canonical_id VARCHAR NOT NULL,
  alias_type VARCHAR DEFAULT 'exact'
);

CREATE TABLE edges (
  subject_id VARCHAR NOT NULL,
  predicate VARCHAR NOT NULL,
  object_id VARCHAR NOT NULL,
  origin VARCHAR NOT NULL,
  confidence FLOAT
);

CREATE TABLE manifest (
  key VARCHAR PRIMARY KEY,
  value VARCHAR
);

CREATE TABLE nodes (
  id VARCHAR PRIMARY KEY,
  type VARCHAR NOT NULL,
  title VARCHAR,
  domain VARCHAR,
  source_path VARCHAR,
  pagerank FLOAT,
  in_degree INTEGER,
  out_degree INTEGER
);

CREATE TABLE bm25_tokens (
  unit_id VARCHAR NOT NULL,
  tokens JSON NOT NULL
);

CREATE TABLE vector_metadata (
  unit_id VARCHAR PRIMARY KEY,
  model_name VARCHAR NOT NULL,
  model_version VARCHAR NOT NULL,
  dimensions INTEGER NOT NULL,
  input_hash VARCHAR NOT NULL
);

CREATE TABLE cross_pack_refs (
  source_id VARCHAR NOT NULL,
  target_qualified_id VARCHAR NOT NULL,
  target_pack VARCHAR NOT NULL,
  predicate VARCHAR NOT NULL DEFAULT 'references',
  resolved BOOLEAN DEFAULT FALSE
);
```
