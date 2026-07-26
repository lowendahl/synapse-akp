# ADR-016: AKP SHALL Remain Model-Neutral

**Status:** Accepted
**Date:** 2026-07-26
**Context:** Synapse packages must survive changes in LLM providers, embedding models, and retrieval strategies. Tying package meaning or usability to one model would reduce portability and complicate upgrades.
**Decision:** AKP SHALL remain model-neutral. Packages MAY include model-derived artifacts such as embeddings, but the package contract SHALL NOT require a specific LLM, embedding provider, or model version in order to interpret the package's canonical knowledge.
**Consequences:** Deployments can choose or replace models independently, packages can travel between runtimes, and any model-specific artifacts must be declared as optional or replaceable package capabilities.
**References:** AKP Product Definition §5.7, §15.4, §35
