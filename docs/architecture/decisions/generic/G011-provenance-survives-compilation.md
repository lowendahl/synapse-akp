# ADR-018: Provenance SHALL Survive Compilation

**Status:** Accepted
**Date:** 2026-07-26
**Context:** Retrieved knowledge must remain explainable after parsing, normalization, enrichment, chunking, graph compilation, and packaging. Without durable provenance, users cannot audit or trust the result.
**Decision:** Every material knowledge object and derived retrieval unit SHALL retain provenance linking it to source identity, source location, source revision, transformation history, compiler build, and package version. Compilation SHALL preserve this lineage rather than replace it.
**Consequences:** Build outputs grow richer, runtime responses can return evidence trails, and every transformation stage must record lineage rather than emitting anonymous derived data.
**References:** AKP Product Definition §16, §20.11, §27
