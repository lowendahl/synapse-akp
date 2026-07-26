# ADR-021: Hybrid Retrieval SHALL Be Supported

**Status:** Accepted
**Date:** 2026-07-26
**Context:** No single retrieval mode is sufficient for all knowledge tasks. Identifier lookup, lexical matching, semantic similarity, graph traversal, and metadata filtering each solve different retrieval problems.
**Decision:** The AKP Runtime SHALL support hybrid retrieval. The retrieval contract SHALL allow exact lookup, lexical retrieval, semantic retrieval, graph expansion, metadata filtering, and structured retrieval to operate independently or in combination.
**Consequences:** Runtime implementations must compose multiple retrieval strategies, package formats must preserve the structures needed for each mode, and consumers gain a stable contract without depending on one retrieval technique.
**References:** AKP Product Definition §27, §28
