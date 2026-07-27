# ADR-025: Pack Format Specification (Schema 2.0.0)

## Status

Accepted

## Context

The compiler emits Knowledge Packs as DuckDB database files with an adjacent USearch vector sidecar. Until now, the schema was implicitly defined by the compiler's `duckdb_writer.py` implementation. As we build the runtime as a separate package that reads these packs, we need a formal contract between compiler output and runtime input.

Without a specification:
- Runtime authors must reverse-engineer the compiler code
- Schema drift between compiler and runtime causes silent failures
- No clear versioning strategy for pack format evolution
- No validation criteria for third-party pack producers

## Decision

We SHALL maintain a formal AKP Pack Format Specification (`docs/specifications/akp-pack-format.md`) as the authoritative contract between compiler and runtime.

Key decisions within the spec:

1. **Schema version `2.0.0`** — runtime MUST accept `2.x.y` packs and reject other majors
2. **Manifest table** — key-value store with 19 required keys for identity, provenance, and build metrics
3. **5 required tables** — `objects`, `semantic_units`, `aliases`, `edges`, `manifest`
4. **4 optional tables** — `nodes`, `bm25_tokens`, `vector_metadata`, `cross_pack_refs`
5. **Vector sidecar** — `.usearch` file with rowid ordering matching `vector_metadata` table
6. **Pack identity** — `publisher.domain.package` naming convention with semver versioning
7. **Immutability** — packs are never mutated after compilation; `content_hash` provides integrity
8. **RFC 2119 language** — MUST/SHOULD/MAY for clear conformance levels

## Consequences

### Positive
- Runtime can validate packs without compiler knowledge
- Clear versioning enables forward-compatible evolution
- Third-party tooling can produce compliant packs
- Breaking changes are signaled by schema major bump

### Negative
- Spec maintenance overhead alongside compiler changes
- Must coordinate spec updates when adding tables/columns

### Mitigations
- Architecture tests in both compiler and runtime validate spec compliance
- CI checks that compiler output matches spec-declared schema
