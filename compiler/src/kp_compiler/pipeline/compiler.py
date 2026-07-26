"""Knowledge Pack Compiler — main pipeline orchestrator.

What: Wires stages and adapters together, runs the compilation DAG.
Why: Single entry point that coordinates all stages (CP-02).
Contracts: Composes stages via dependency injection.
Boundaries: This is the ONLY place concrete adapters are instantiated.
Test strategy: Integration tests with minimal corpus fixtures.
"""

from __future__ import annotations

import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

from kp_compiler import __version__
from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.contracts.errors import OntologyViolation
from kp_compiler.domain.models import KnowledgeObject, SemanticUnit
from kp_compiler.domain.ontology import Ontology
from kp_compiler.domain.rules import PackRules
from kp_compiler.events.bus import (
    BM25IndexBuilt,
    CrossPackValidationComplete,
    DiscoveryComplete,
    EmbeddingComplete,
    EnrichmentComplete,
    EventBus,
    GraphBuilt,
    LoggingObserver,
    PackWritten,
    ParseComplete,
    ValidationComplete,
)
from kp_compiler.infrastructure.duckdb_writer import DuckDBPackWriter
from kp_compiler.infrastructure.filesystem import FilesystemReader
from kp_compiler.stages.bm25 import build_bm25_index
from kp_compiler.stages.cross_pack import validate_cross_pack_refs
from kp_compiler.stages.embed import build_embeddings, save_usearch_index
from kp_compiler.stages.enrich import enrich_corpus
from kp_compiler.stages.graph import build_graph
from kp_compiler.stages.outcome_validator import validate_outcomes
from kp_compiler.stages.parse import parse_source
from kp_compiler.stages.validate import validate_corpus


def build_semantic_units(objects: list[KnowledgeObject]) -> list[SemanticUnit]:
    """Create semantic units from object sections (meaning-aligned chunks)."""
    units: list[SemanticUnit] = []
    for obj in objects:
        if not obj.id:
            continue

        for i, section in enumerate(obj.sections):
            if not section.content.strip():
                continue
            context = (
                f"Domain: {obj.domain}\n"
                f"Type: {obj.type.value}\n"
                f"Document: {obj.title}\n"
                f"Section: {section.heading}\n"
            )
            if obj.aliases:
                context += f"Aliases: {', '.join(obj.aliases)}\n"

            unit_id = f"su:{obj.id}:{i}"
            units.append(SemanticUnit(
                id=unit_id,
                source_object_id=obj.id,
                heading_path=section.heading,
                content=section.content,
                context=context,
                object_type=obj.type.value,
                domain=obj.domain,
            ))

        if obj.description:
            context = (
                f"Domain: {obj.domain}\n"
                f"Type: {obj.type.value}\n"
                f"Document: {obj.title}\n"
                f"Section: Definition\n"
            )
            if obj.aliases:
                context += f"Aliases: {', '.join(obj.aliases)}\n"

            units.append(SemanticUnit(
                id=f"su:{obj.id}:def",
                source_object_id=obj.id,
                heading_path="Definition",
                content=f"{obj.title}: {obj.description}",
                context=context,
                object_type=obj.type.value,
                domain=obj.domain,
            ))

    return units


def build_alias_registry(
    objects: list[KnowledgeObject],
    pack_id: str = "",
) -> list[tuple[str, str, str]]:
    """Build alias registry from all objects.

    Tags matching the pack's domain prefix are excluded — the domain is
    implicit context, not a useful search discriminator (ADR-014).
    """
    # Derive implicit domain tags from pack_id (e.g. "kp-csu" → "csu")
    domain_tag = pack_id.removeprefix("kp-").lower() if pack_id else ""

    aliases: list[tuple[str, str, str]] = []
    for obj in objects:
        if not obj.id:
            continue
        aliases.append((obj.title, obj.id, "title"))
        for alias in obj.aliases:
            aliases.append((alias, obj.id, "explicit"))
        for tag in obj.tags:
            if tag.lower() == domain_tag:
                continue  # domain tag is implicit
            aliases.append((tag, obj.id, "tag"))
    return aliases


def compile_pack(
    source_root: Path,
    ontology_path: Path,
    output_path: Path,
    pack_id: str = "kp-csu",
    dependency_pack: Path | None = None,
    skip_embeddings: bool = False,
    discover_ontology: bool = False,
    rules: PackRules | None = None,
) -> tuple[bool, list[Diagnostic]]:
    """Run the full V2 compilation pipeline.

    Returns (success, diagnostics).
    """
    if rules is None:
        rules = PackRules.default()

    # Ensure UTF-8 output on Windows (only when running in a real terminal)
    import sys
    if (
        hasattr(sys.stdout, "buffer")
        and hasattr(sys.stdout, "encoding")
        and sys.stdout.encoding
        and sys.stdout.encoding.lower() not in ("utf-8", "utf8")
    ):
        import io
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )

    start_time = time.time()
    all_diagnostics: list[Diagnostic] = []

    # -- Event Bus -----------------------------------------------------------
    bus = EventBus()
    LoggingObserver(bus)

    # -- Stage 1: Discover ---------------------------------------------------
    reader = FilesystemReader()
    source_files = reader.discover(source_root)
    print(f"[discover] Found {len(source_files)} source files")
    bus.emit(DiscoveryComplete(file_count=len(source_files)))

    # -- Stage 1b: Ontology Discovery (ADR-013) ------------------------------
    if discover_ontology:
        from kp_compiler.stages.discover_ontology import (
            discover_ontology as run_discovery,
            generate_ontology_yaml,
        )
        discovery_result = run_discovery(source_files, source_root)
        print(
            f"[ontology-discover] {len(discovery_result.types)} types, "
            f"{len(discovery_result.predicates)} predicates, "
            f"domains={sorted(discovery_result.domains)}"
        )

        # Load existing ontology for merge if it exists
        existing_data = None
        if ontology_path.exists():
            from ruamel.yaml import YAML
            yaml_loader = YAML(typ="safe")
            with open(ontology_path, encoding="utf-8") as f:
                existing_data = yaml_loader.load(f)
            print(f"[ontology-discover] Merging with existing {ontology_path}")

        yaml_content = generate_ontology_yaml(discovery_result, existing_data)
        ontology_path.parent.mkdir(parents=True, exist_ok=True)
        ontology_path.write_text(yaml_content, encoding="utf-8")
        print(f"[ontology-discover] Wrote {ontology_path}")

    # -- Stage 2: Load Ontology ----------------------------------------------
    from ruamel.yaml import YAML
    yaml = YAML(typ="safe")
    with open(ontology_path, encoding="utf-8") as f:
        ontology_data = yaml.load(f)
    ontology = Ontology.from_dict(ontology_data)
    print(f"[ontology] Loaded v{ontology.version}")

    # ── Stage 3: Parse ──────────────────────────────────────────────────────
    objects: list[KnowledgeObject] = []
    parse_errors = 0
    for file_path in source_files:
        content = reader.read(file_path)
        rel_path = str(file_path.relative_to(source_root.parent)).replace("\\", "/")
        try:
            obj = parse_source(content, rel_path)
            objects.append(obj)
        except (OntologyViolation, ValueError, KeyError, TypeError) as e:
            parse_errors += 1
            all_diagnostics.append(Diagnostic(
                severity=Severity.ERROR,
                source_file=rel_path,
                message=f"Parse error: {e}",
                stage="parse",
            ))
    print(f"[parse] Parsed {len(objects)} objects")
    bus.emit(ParseComplete(object_count=len(objects), error_count=parse_errors))

    # ── Stage 4: Validate ───────────────────────────────────────────────────
    validation_diagnostics = validate_corpus(objects, ontology)
    all_diagnostics.extend(validation_diagnostics)
    errors = [d for d in validation_diagnostics if d.severity == Severity.ERROR]
    warnings = [d for d in validation_diagnostics if d.severity == Severity.WARNING]
    print(f"[validate] {len(errors)} errors, {len(warnings)} warnings")
    bus.emit(ValidationComplete(error_count=len(errors), warning_count=len(warnings)))

    # ── Stage 5: Enrich (V2) ───────────────────────────────────────────────
    enrich_result = enrich_corpus(objects, rules)
    objects = enrich_result.objects
    all_diagnostics.extend(enrich_result.diagnostics)
    print(f"[enrich] +{enrich_result.aliases_added} aliases, {enrich_result.acronyms_resolved} acronyms")
    bus.emit(EnrichmentComplete(
        aliases_added=enrich_result.aliases_added,
        acronyms_resolved=enrich_result.acronyms_resolved,
    ))

    # ── Stage 6: Build Graph ────────────────────────────────────────────────
    graph_result = build_graph(objects)
    all_diagnostics.extend(graph_result.diagnostics)
    print(f"[graph] {graph_result.metrics['node_count']} nodes, {graph_result.metrics['edge_count']} edges")
    bus.emit(GraphBuilt(
        node_count=graph_result.metrics["node_count"],
        edge_count=graph_result.metrics["edge_count"],
        orphan_count=graph_result.metrics["orphan_count"],
        cycle_count=graph_result.metrics["cycle_count"],
    ))

    # ── Stage 7: Build Semantic Units ───────────────────────────────────────
    semantic_units = build_semantic_units(objects)
    print(f"[semantic] {len(semantic_units)} semantic units")

    # ── Stage 8: Build Alias Registry ───────────────────────────────────────
    alias_registry = build_alias_registry(objects, pack_id=pack_id)
    print(f"[aliases] {len(alias_registry)} alias entries")

    # ── Stage 9: BM25 Index (V2) ───────────────────────────────────────────
    bm25_result = build_bm25_index(semantic_units)
    print(f"[bm25] Indexed {len(bm25_result.unit_ids)} units, vocab={bm25_result.vocab_size}")
    bus.emit(BM25IndexBuilt(unit_count=len(bm25_result.unit_ids), vocab_size=bm25_result.vocab_size))

    # ── Stage 10: Dense Embeddings (V2) ────────────────────────────────────
    embed_result = None
    if not skip_embeddings:
        embed_start = time.time()
        try:
            embed_result = build_embeddings(semantic_units)
            embed_duration = time.time() - embed_start
            print(f"[embed] {len(embed_result.unit_ids)} vectors, {embed_result.dimensions}d, {embed_duration:.1f}s")
            bus.emit(EmbeddingComplete(
                unit_count=len(embed_result.unit_ids),
                model_name=embed_result.model_name,
                dimensions=embed_result.dimensions,
                duration_seconds=embed_duration,
            ))
        except Exception as e:
            print(f"[embed] SKIPPED — {type(e).__name__}: {e}")
            all_diagnostics.append(Diagnostic(
                severity=Severity.WARNING,
                source_file="",
                message=f"Embedding stage skipped: {e}",
                stage="embed",
            ))
    else:
        print("[embed] SKIPPED (--skip-embeddings)")

    # ── Stage 11: Cross-Pack Validation (V2) ───────────────────────────────
    dep_ids: set[str] = set()
    dep_domain = ""
    if dependency_pack and dependency_pack.exists():
        from kp_compiler.stages.cross_pack import (
            _detect_dependency_domain,
            load_dependency_manifest,
        )

        dep_ids = load_dependency_manifest(dependency_pack)
        dep_domain = _detect_dependency_domain(dependency_pack) or ""

    cross_pack_result = validate_cross_pack_refs(
        objects,
        dependency_ids=dep_ids,
        dependency_domain=dep_domain,
        pack_id=pack_id,
    )
    all_diagnostics.extend(cross_pack_result.diagnostics)
    if cross_pack_result.refs_checked > 0:
        print(f"[cross-pack] {cross_pack_result.refs_checked} refs, "
              f"{cross_pack_result.refs_resolved} resolved, "
              f"{cross_pack_result.refs_broken} broken")
    bus.emit(CrossPackValidationComplete(
        refs_checked=cross_pack_result.refs_checked,
        refs_resolved=cross_pack_result.refs_resolved,
        refs_broken=cross_pack_result.refs_broken,
    ))

    # ── Gate: fail before writing if errors exist ───────────────────────
    current_errors = [d for d in all_diagnostics if d.severity == Severity.ERROR]
    if current_errors:
        duration = time.time() - start_time
        print(f"\n[FAIL] BUILD FAILED before write — {len(current_errors)} error(s):")
        for d in current_errors[:20]:
            print(f"  {d.severity.value}: [{d.source_file}] {d.message}")
        return False, all_diagnostics

    # ── Stage 12: Write Pack ───────────────────────────────────────────────
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = DuckDBPackWriter(output_path)
    writer.write_objects(objects)
    writer.write_graph(graph_result)
    writer.write_semantic_units(semantic_units)
    writer.write_aliases(alias_registry)

    # V2: Write BM25 tokens
    if bm25_result.unit_ids:
        writer.write_bm25_tokens(bm25_result.unit_ids, bm25_result.corpus_tokens)

    # V2: Write vector metadata + usearch index
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

    # V2: Write cross-pack refs
    if cross_pack_result.cross_refs:
        writer.write_cross_pack_refs(cross_pack_result.cross_refs, dep_ids)

    # Manifest
    content_hash = hashlib.sha256(
        "".join(obj.id for obj in objects if obj.id).encode()
    ).hexdigest()[:16]

    manifest = {
        "pack_id": pack_id,
        "pack_version": __version__,
        "schema_version": "2.0.0",
        "ontology_version": ontology.version,
        "compiler_version": __version__,
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
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
    writer.write_manifest(manifest)
    writer.close()

    duration = time.time() - start_time
    print(f"[done] Pack written to {output_path} in {duration:.1f}s")
    bus.emit(PackWritten(
        pack_id=pack_id,
        path=str(output_path),
        content_hash=content_hash,
        duration_seconds=duration,
    ))

    # Report
    all_errors = [d for d in all_diagnostics if d.severity == Severity.ERROR]
    all_warnings = [d for d in all_diagnostics if d.severity == Severity.WARNING]

    # ── Stage 13: Outcome Validation (ADR-014) ─────────────────────────────
    outcome_report = validate_outcomes(output_path, rules)
    if outcome_report.results:
        passed_count = sum(1 for r in outcome_report.results if r.passed)
        total_count = len(outcome_report.results)
        print(f"[outcome] {passed_count}/{total_count} assertions passed "
              f"(rate={outcome_report.pass_rate:.0%})")
        for r in outcome_report.results:
            status = "PASS" if r.passed else "FAIL"
            print(f"  [{status}] {r.name}: {r.detail}")
            for f in r.failures[:3]:
                print(f"         ↳ {f}")
        if not outcome_report.passed and rules.quality_thresholds.fail_on_error:
            all_errors.append(Diagnostic(
                severity=Severity.ERROR,
                source_file="",
                message=(
                    f"Outcome validation failed: {outcome_report.pass_rate:.0%} pass rate "
                    f"< {rules.quality_thresholds.min_assertion_pass_rate:.0%} threshold"
                ),
                stage="outcome",
            ))
            all_diagnostics.append(all_errors[-1])

    success = len(all_errors) == 0
    if not success:
        print(f"\n[FAIL] BUILD FAILED -- {len(all_errors)} error(s):")
        for d in all_errors[:20]:
            print(f"  {d.severity.value}: [{d.source_file}] {d.message}")
    else:
        print(f"\n[OK] BUILD SUCCEEDED -- {len(all_warnings)} warning(s)")

    return success, all_diagnostics
