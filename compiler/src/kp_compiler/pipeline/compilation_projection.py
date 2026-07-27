"""Projection and validation helpers for compiler orchestration."""

from __future__ import annotations

import time
from pathlib import Path

from kp_compiler.contracts.protocols import Diagnostic, GraphResult, Severity
from kp_compiler.domain.models import KnowledgeObject, SemanticUnit
from kp_compiler.domain.ontology import Ontology
from kp_compiler.domain.rules import PackRules
from kp_compiler.events.bus import (
    BM25IndexBuilt,
    CrossPackValidationComplete,
    EmbeddingComplete,
    EnrichmentComplete,
    EventBus,
    GraphBuilt,
    ValidationComplete,
)
from kp_compiler.pipeline.alias_registry_builder import build_alias_registry
from kp_compiler.pipeline.semantic_unit_builder import build_semantic_units
from kp_compiler.stages.bm25 import BM25Result, build_bm25_index
from kp_compiler.stages.cross_pack import CrossPackResult, validate_cross_pack_refs
from kp_compiler.stages.embed import EmbeddingResult, build_embeddings
from kp_compiler.stages.enrich import enrich_corpus
from kp_compiler.stages.graph import build_graph
from kp_compiler.stages.validate import validate_corpus


class CompilationProjection:
    """Builds validated retrieval projections for pack writing."""

    def validate(
        self,
        objects: list[KnowledgeObject],
        ontology: Ontology,
        bus: EventBus,
    ) -> tuple[list[Diagnostic], list[Diagnostic], list[Diagnostic]]:
        diagnostics = validate_corpus(objects, ontology)
        errors = [diag for diag in diagnostics if diag.severity == Severity.ERROR]
        warnings = [diag for diag in diagnostics if diag.severity == Severity.WARNING]
        print(f"[validate] {len(errors)} errors, {len(warnings)} warnings")
        bus.emit(ValidationComplete(error_count=len(errors), warning_count=len(warnings)))
        return diagnostics, errors, warnings

    def enrich(
        self,
        objects: list[KnowledgeObject],
        rules: PackRules,
        bus: EventBus,
    ) -> tuple[list[KnowledgeObject], list[Diagnostic]]:
        result = enrich_corpus(objects, rules)
        print(f"[enrich] +{result.aliases_added} aliases, {result.acronyms_resolved} acronyms")
        bus.emit(
            EnrichmentComplete(
                aliases_added=result.aliases_added,
                acronyms_resolved=result.acronyms_resolved,
            )
        )
        return result.objects, result.diagnostics

    def graph(self, objects: list[KnowledgeObject], bus: EventBus) -> GraphResult:
        result = build_graph(objects)
        print(f"[graph] {result.metrics['node_count']} nodes, {result.metrics['edge_count']} edges")
        bus.emit(
            GraphBuilt(
                node_count=result.metrics["node_count"],
                edge_count=result.metrics["edge_count"],
                orphan_count=result.metrics["orphan_count"],
                cycle_count=result.metrics["cycle_count"],
            )
        )
        return result

    def retrieval_artifacts(
        self,
        objects: list[KnowledgeObject],
        pack_id: str,
        bus: EventBus,
        skip_embeddings: bool,
    ) -> tuple[
        list[SemanticUnit],
        list[tuple[str, str, str]],
        BM25Result,
        EmbeddingResult | None,
        list[Diagnostic],
    ]:
        semantic_units: list[SemanticUnit] = build_semantic_units(objects)
        alias_registry = build_alias_registry(objects, pack_id=pack_id)
        bm25_result = build_bm25_index(semantic_units)
        print(f"[semantic] {len(semantic_units)} semantic units")
        print(f"[aliases] {len(alias_registry)} alias entries")
        print(f"[bm25] Indexed {len(bm25_result.unit_ids)} units, vocab={bm25_result.vocab_size}")
        bus.emit(
            BM25IndexBuilt(
                unit_count=len(bm25_result.unit_ids),
                vocab_size=bm25_result.vocab_size,
            )
        )
        embed_result, embed_diagnostics = self._embed(semantic_units, bus, skip_embeddings)
        return semantic_units, alias_registry, bm25_result, embed_result, embed_diagnostics

    def _embed(
        self,
        semantic_units: list[SemanticUnit],
        bus: EventBus,
        skip_embeddings: bool,
    ) -> tuple[EmbeddingResult | None, list[Diagnostic]]:
        if skip_embeddings:
            print("[embed] SKIPPED (--skip-embeddings)")
            return None, []
        embed_start = time.time()
        try:
            result = build_embeddings(semantic_units)
            duration = time.time() - embed_start
            print(f"[embed] {len(result.unit_ids)} vectors, {result.dimensions}d, {duration:.1f}s")
            bus.emit(
                EmbeddingComplete(
                    unit_count=len(result.unit_ids),
                    model_name=result.model_name,
                    dimensions=result.dimensions,
                    duration_seconds=duration,
                )
            )
            return result, []
        except Exception as error:
            print(f"[embed] SKIPPED — {type(error).__name__}: {error}")
            return (
                None,
                [Diagnostic(Severity.WARNING, "", f"Embedding stage skipped: {error}", "embed")],
            )

    def cross_pack(
        self,
        objects: list[KnowledgeObject],
        dependency_pack: Path | None,
        pack_id: str,
        bus: EventBus,
    ) -> tuple[CrossPackResult, set[str]]:
        dependency_ids: set[str] = set()
        dependency_domain = ""
        if dependency_pack and dependency_pack.exists():
            from kp_compiler.stages.cross_pack import (
                _detect_dependency_domain,
                load_dependency_manifest,
            )

            dependency_ids = load_dependency_manifest(dependency_pack)
            dependency_domain = _detect_dependency_domain(dependency_pack) or ""
        result = validate_cross_pack_refs(
            objects,
            dependency_ids=dependency_ids,
            dependency_domain=dependency_domain,
            pack_id=pack_id,
        )
        if result.refs_checked > 0:
            print(
                f"[cross-pack] {result.refs_checked} refs, {result.refs_resolved} resolved, {result.refs_broken} broken"
            )
        bus.emit(
            CrossPackValidationComplete(
                refs_checked=result.refs_checked,
                refs_resolved=result.refs_resolved,
                refs_broken=result.refs_broken,
            )
        )
        return result, dependency_ids
