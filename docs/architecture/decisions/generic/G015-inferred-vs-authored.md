# ADR-024: Inferred Knowledge SHALL Be Distinguishable from Authored Knowledge

**Status:** Accepted
**Date:** 2026-07-26
**Context:** The compiler may generate aliases, retrieval questions, summaries, inferred relationships, and other enrichments. These additions are useful, but they must not be confused with directly authored domain knowledge.
**Decision:** Inferred or generated knowledge SHALL be explicitly distinguishable from authored knowledge. Derived objects SHALL retain metadata describing their source objects, generation method, model or algorithm where applicable, confidence, and timestamp.
**Consequences:** Consumers can apply different trust policies to authored versus inferred content, explainability improves, and the compiler must persist provenance and derivation metadata for all generated artifacts.
**References:** AKP Product Definition §16, §20.6, §21.3, §21.4
