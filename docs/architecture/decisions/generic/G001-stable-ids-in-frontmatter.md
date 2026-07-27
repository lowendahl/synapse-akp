---
type: ADR
title: "ADR-001 — Stable IDs in OKF Frontmatter"
id: adr.001
status: accepted
date: 2026-07-25
decision_makers: [plwendahl]
tags: [adr, identity, compilation, frontmatter]
---

# ADR-001 — Stable IDs in OKF Frontmatter

## Status

**Accepted** — 2026-07-25

## Context

The Knowledge Pack SDD (§14, ADR-KP-010) requires that every canonical object have a stable identity that survives renames, path moves, and projection rebuilds. Without explicit IDs, the compiler would need to derive identity from file paths or headings — both of which are fragile and violate ADR-KP-010.

Our OKF corpus currently uses `type` and `title` in frontmatter but has no formal `id` field. Cross-links use bundle-relative paths (e.g., `/csu/metrics/job1-commit-to-complete.md`) which couple identity to filesystem layout.

## Decision

Every OKF markdown file SHALL include a stable `id` field in its YAML frontmatter.

IDs follow the convention:

```
{domain}.{category}.{slug}
```

Examples:

```yaml
id: csu.metric.job1-commit-to-complete
id: mcem.stage.inspire-design
id: csu.evidence.msxi
id: mcem.planning.macc
```

Rules:

1. IDs are lowercase kebab-case segments separated by dots.
2. The first segment is the domain namespace (`csu` or `mcem`).
3. The second segment is the object category (maps to `type` in singular lowercase).
4. The third segment is a human-readable slug unique within its category.
5. IDs are immutable once assigned. Renaming a file or title does NOT change the ID.
6. Removing or replacing an ID requires a deprecation entry in `log.md`.
7. Duplicate IDs fail the build (KP-12, KP-16).

## Consequences

- All ~130 OKF files require a one-time `id` addition to frontmatter.
- Cross-pack references use qualified IDs (e.g., `mcem.stage.inspire-design`) not file paths.
- The compiler resolves `id` → physical file for provenance; file paths become a discovery mechanism, not an identity mechanism.
- ID conflicts are caught at validation (build fails visibly).
- Future file reorganization does not break compiled graph edges.

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Derive ID from file path | Fragile — moves break identity |
| Use title as ID | Titles change; not unique across domains |
| Auto-generate UUIDs | Not human-inspectable; violates SDD §14 preference |
| Leave ID-less, resolve at compile time | Non-deterministic; violates KP-09 |
