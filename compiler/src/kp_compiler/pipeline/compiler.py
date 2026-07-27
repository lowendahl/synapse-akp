"""Knowledge Pack compiler orchestration entry point."""

from __future__ import annotations

import time
from pathlib import Path

from kp_compiler.contracts.protocols import Diagnostic
from kp_compiler.domain.rules import PackRules
from kp_compiler.pipeline.alias_registry_builder import build_alias_registry
from kp_compiler.pipeline.compilation_persistence import CompilationPersistence
from kp_compiler.pipeline.compilation_preparation import CompilationPreparation
from kp_compiler.pipeline.compilation_projection import CompilationProjection
from kp_compiler.pipeline.semantic_unit_builder import build_semantic_units


class PackCompiler:
    """Coordinates the full compilation pipeline."""

    def __init__(self) -> None:
        self._preparation = CompilationPreparation()
        self._projection = CompilationProjection()
        self._persistence = CompilationPersistence()

    def compile_pack(
        self,
        source_root: Path,
        ontology_path: Path,
        output_path: Path,
        pack_id: str = "kp-csu",
        dependency_pack: Path | None = None,
        skip_embeddings: bool = False,
        discover_ontology: bool = False,
        rules: PackRules | None = None,
    ) -> tuple[bool, list[Diagnostic]]:
        active_rules = rules or PackRules.default()
        self._preparation.ensure_utf8_stdout()
        start_time = time.time()
        bus = self._preparation.create_bus()
        source_files = self._preparation.discover_sources(source_root, bus)
        self._preparation.maybe_discover_ontology(discover_ontology, source_files, source_root, ontology_path)
        ontology = self._preparation.load_ontology(ontology_path)
        objects, diagnostics = self._preparation.parse_sources(source_files, source_root, bus)
        validation_diagnostics, errors, warnings = self._projection.validate(objects, ontology, bus)
        diagnostics.extend(validation_diagnostics)
        objects, enrich_diagnostics = self._projection.enrich(objects, active_rules, bus)
        diagnostics.extend(enrich_diagnostics)
        graph_result = self._projection.graph(objects, bus)
        diagnostics.extend(graph_result.diagnostics)
        semantic_units, alias_registry, bm25_result, embed_result, embed_diagnostics = (
            self._projection.retrieval_artifacts(objects, pack_id, bus, skip_embeddings)
        )
        diagnostics.extend(embed_diagnostics)
        cross_pack_result, dependency_ids = self._projection.cross_pack(objects, dependency_pack, pack_id, bus)
        diagnostics.extend(cross_pack_result.diagnostics)
        if self._persistence.fail_before_write(diagnostics):
            return False, diagnostics
        content_hash = self._persistence.write_pack(
            output_path,
            objects,
            graph_result,
            semantic_units,
            alias_registry,
            bm25_result,
            embed_result,
            cross_pack_result,
            dependency_ids,
            pack_id,
            source_files,
            ontology.version,
            errors,
            warnings,
        )
        print(f"[done] Pack written to {output_path} in {time.time() - start_time:.1f}s")
        print(f"[done] Content hash: {content_hash}")
        return self._persistence.report(output_path, active_rules, diagnostics, warnings)


_compiler = PackCompiler()
compile_pack = _compiler.compile_pack
CompilationPipeline = PackCompiler  # Backwards compatibility alias
__all__ = ["PackCompiler", "CompilationPipeline", "build_alias_registry", "build_semantic_units", "compile_pack"]
