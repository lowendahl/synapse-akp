# ADR-023: Released Package Versions SHOULD Be Immutable

**Status:** Accepted
**Date:** 2026-07-26
**Context:** Distribution, caching, signatures, audit, rollback, and trust all depend on released package versions remaining stable after publication. Mutable releases would undermine verification and provenance.
**Decision:** Released package versions SHOULD be immutable. Once a package version is signed or published, it SHOULD NOT be overwritten; corrections SHOULD be shipped as a new version, and revocation or deprecation SHOULD be used when a release must be withdrawn.
**Consequences:** Registry implementations need explicit promotion, deprecation, and revocation flows; consumers can cache and verify packages safely; and operational fixes require versioned releases instead of in-place replacement.
**References:** AKP Product Definition §33, §34
