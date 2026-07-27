"""Pack persistence helpers for compiler orchestration."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from pathlib import Path

from kp_compiler import __version__
from kp_compiler.contracts.protocols import Diagnostic, GraphResult, Severity
from kp_compiler.domain.models import KnowledgeObject, SemanticUnit
from kp_compiler.domain.rules import PackRules
from kp_compiler.infrastructure.duckdb_writer import DuckDBPackWriter
from kp_compiler.stages.bm25 import BM25Result
from kp_compiler.stages.cross_pack import CrossPackResult
from kp_compiler.stages.embed import EmbeddingResult, save_usearch_index
from kp_compiler.stages.outcome_validation_models import OutcomeReport
from kp_compiler.stages.outcome_validator import validate_outcomes


class CompilationPersistence:
    """Writes compiled artifacts and evaluates outcomes."""

    def fail_before_write(self, diagnostics: list[Diagnostic]) -> bool:
        errors = [diagnostic for diagnostic in diagnostics if diagnostic.severity == Severity.ERROR]
        if not errors:
            return False
        print(f"\n[FAIL] BUILD FAILED before write — {len(errors)} error(s):")
        for diagnostic in errors[:20]:
            print(f"  {diagnostic.severity.value}: [{diagnostic.source_file}] {diagnostic.message}")
        return True

    def write_pack(
        self,
        output_path: Path,
        objects: list[KnowledgeObject],
        graph_result: GraphResult,
        semantic_units: list[SemanticUnit],
        alias_registry: list[tuple[str, str, str]],
        bm25_result: BM25Result,
        embed_result: EmbeddingResult | None,
        cross_pack_result: CrossPackResult,
        dependency_ids: set[str],
        pack_id: str,
        source_files: list[Path],
        ontology_version: str,
        errors: list[Diagnostic],
        warnings: list[Diagnostic],
    ) -> str:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        writer = DuckDBPackWriter(output_path)
        writer.write_objects(objects)
        writer.write_graph(graph_result)
        writer.write_semantic_units(semantic_units)
        writer.write_aliases(alias_registry)
        if bm25_result.unit_ids:
            writer.write_bm25_tokens(bm25_result.unit_ids, bm25_result.corpus_tokens)
        if embed_result and embed_result.vectors is not None:
            writer.write_vector_metadata(
                embed_result.unit_ids,
                embed_result.model_name,
                embed_result.dimensions,
                embed_result.input_hashes,
            )
            usearch_path = output_path.with_suffix(".usearch")
            save_usearch_index(embed_result, usearch_path)
            print(f"[vectors] Saved .usearch index to {usearch_path}")
        if cross_pack_result.cross_refs:
            writer.write_cross_pack_refs(cross_pack_result.cross_refs, dependency_ids)
        content_hash = hashlib.sha256("".join(obj.id for obj in objects if obj.id).encode()).hexdigest()[:16]
        writer.write_manifest(
            self._manifest(
                pack_id,
                source_files,
                objects,
                graph_result,
                semantic_units,
                alias_registry,
                bm25_result,
                embed_result,
                cross_pack_result,
                ontology_version,
                content_hash,
                errors,
                warnings,
            )
        )
        writer.close()

        # Bundle into .akp package (ZIP with manifest + all artifacts)
        akp_path = self._write_akp_package(output_path, pack_id, content_hash, embed_result)
        print(f"[package] {akp_path} ({akp_path.stat().st_size / 1024:.0f} KB)")

        return content_hash

    def _write_akp_package(
        self,
        output_path: Path,
        pack_id: str,
        content_hash: str,
        embed_result: EmbeddingResult | None,
    ) -> Path:
        """Bundle .duckdb + .usearch + manifest.yaml into a single .akp ZIP file."""
        import zipfile

        import yaml

        duckdb_checksum = hashlib.sha256(output_path.read_bytes()).hexdigest()

        artifacts: list[dict[str, str | int]] = [
            {
                "file": "pack.duckdb",
                "type": "duckdb",
                "size_bytes": output_path.stat().st_size,
                "sha256": duckdb_checksum,
            }
        ]

        usearch_path = output_path.with_suffix(".usearch")
        has_vectors = usearch_path.exists()
        if has_vectors:
            artifacts.append(
                {
                    "file": "pack.usearch",
                    "type": "usearch_index",
                    "size_bytes": usearch_path.stat().st_size,
                    "sha256": hashlib.sha256(usearch_path.read_bytes()).hexdigest(),
                }
            )

        manifest = {
            "pack_id": pack_id,
            "pack_format_version": 1,
            "compiler_version": __version__,
            "schema_version": "2.0.0",
            "content_hash": content_hash,
            "build_timestamp": datetime.now(UTC).isoformat(),
            "embeddings_included": has_vectors,
            "embedding_model": embed_result.model_name if embed_result and embed_result.vectors is not None else None,
            "embedding_dimensions": embed_result.dimensions if embed_result and embed_result.vectors is not None else 0,
            "artifacts": artifacts,
            "runtime_minimum_version": "0.1.0",
        }

        akp_path = output_path.with_suffix(".akp")
        with zipfile.ZipFile(akp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            # Write manifest.yaml first
            manifest_yaml = yaml.dump(manifest, default_flow_style=False, sort_keys=False)
            archive.writestr("manifest.yaml", manifest_yaml)

            # Write DuckDB
            archive.write(output_path, "pack.duckdb")

            # Write vector index if present
            if has_vectors:
                archive.write(usearch_path, "pack.usearch")

        return akp_path

    def report(
        self,
        output_path: Path,
        rules: PackRules,
        diagnostics: list[Diagnostic],
        warnings: list[Diagnostic],
    ) -> tuple[bool, list[Diagnostic]]:
        errors = [diagnostic for diagnostic in diagnostics if diagnostic.severity == Severity.ERROR]
        outcome_report = validate_outcomes(output_path, rules)
        if outcome_report.results:
            self._print_outcomes(outcome_report)
            if not outcome_report.passed and rules.quality_thresholds.fail_on_error:
                diagnostics.append(
                    Diagnostic(
                        Severity.ERROR,
                        "",
                        "Outcome validation failed: "
                        f"{outcome_report.pass_rate:.0%} pass rate < "
                        f"{rules.quality_thresholds.min_assertion_pass_rate:.0%} threshold",
                        "outcome",
                    )
                )
                errors.append(diagnostics[-1])
        success = len(errors) == 0
        if success:
            print(f"\n[OK] BUILD SUCCEEDED -- {len(warnings)} warning(s)")
        else:
            print(f"\n[FAIL] BUILD FAILED -- {len(errors)} error(s):")
            for diagnostic in errors[:20]:
                print(f"  {diagnostic.severity.value}: [{diagnostic.source_file}] {diagnostic.message}")
        return success, diagnostics

    def _manifest(
        self,
        pack_id: str,
        source_files: list[Path],
        objects: list[KnowledgeObject],
        graph_result: GraphResult,
        semantic_units: list[SemanticUnit],
        alias_registry: list[tuple[str, str, str]],
        bm25_result: BM25Result,
        embed_result: EmbeddingResult | None,
        cross_pack_result: CrossPackResult,
        ontology_version: str,
        content_hash: str,
        errors: list[Diagnostic],
        warnings: list[Diagnostic],
    ) -> dict[str, str]:
        return {
            "pack_id": pack_id,
            "pack_version": __version__,
            "pack_format_version": "1",
            "schema_version": "2.0.0",
            "ontology_version": ontology_version,
            "compiler_version": __version__,
            "build_timestamp": datetime.now(UTC).isoformat(),
            "source_file_count": str(len(source_files)),
            "object_count": str(len(objects)),
            "node_count": str(graph_result.metrics["node_count"]),
            "edge_count": str(graph_result.metrics["edge_count"]),
            "semantic_unit_count": str(len(semantic_units)),
            "alias_count": str(len(alias_registry)),
            "bm25_vocab_size": str(bm25_result.vocab_size),
            "embedding_model": embed_result.model_name if embed_result else "none",
            "embedding_dimensions": str(embed_result.dimensions if embed_result else 0),
            "cross_pack_refs": str(cross_pack_result.refs_checked),
            "content_hash": content_hash,
            "error_count": str(len(errors)),
            "warning_count": str(len(warnings)),
        }

    def _print_outcomes(self, outcome_report: OutcomeReport) -> None:
        passed_count = sum(1 for result in outcome_report.results if result.passed)
        print(
            f"[outcome] {passed_count}/{len(outcome_report.results)} assertions passed "
            f"(rate={outcome_report.pass_rate:.0%})"
        )
        for result in outcome_report.results:
            print(f"  [{'PASS' if result.passed else 'FAIL'}] {result.name}: {result.detail}")
            for failure in result.failures[:3]:
                print(f"         ↳ {failure}")
