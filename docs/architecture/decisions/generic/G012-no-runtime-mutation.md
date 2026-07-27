# ADR-019: Runtime Learning SHALL NOT Directly Mutate Packages

**Status:** Accepted
**Date:** 2026-07-26
**Context:** Runtime memory, observations, and learning are valuable, but allowing deployed packages to self-mutate would break release accountability, reproducibility, and governance review.
**Decision:** Runtime learning SHALL NOT directly mutate a published AKP. Learned knowledge MAY be captured in runtime memory or candidate stores, but promotion into a package SHALL occur through governed review, OKF source updates, recompilation, and new package version release.
**Consequences:** Published packages remain stable and auditable, learning workflows require explicit promotion paths, and runtimes must separate transient memory from governed distributable knowledge.
**References:** AKP Product Definition §31, §32
