# ADR-017: Governance SHALL Be Object-Level

**Status:** Accepted
**Date:** 2026-07-26
**Context:** Package-level labels alone are insufficient because retrieval operates on derived objects such as chunks, graph edges, summaries, embeddings, and procedures. Governance must survive transformation and composition.
**Decision:** Governance SHALL attach to material knowledge objects and SHALL propagate to derived representations. Compilation, indexing, retrieval, composition, and summarization SHALL NOT weaken the effective protection applied to an object.
**Consequences:** The compiler and runtime must carry governance metadata through all representations, retrieval results can be filtered and explained correctly, and composition logic must apply the most restrictive applicable policy.
**References:** AKP Product Definition §17, §20.9, §22
