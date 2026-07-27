"""Preparation helpers for compiler orchestration."""

from __future__ import annotations

from pathlib import Path

from kp_compiler.contracts.errors import OntologyViolation
from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.domain.models import KnowledgeObject
from kp_compiler.domain.ontology import Ontology
from kp_compiler.events.bus import DiscoveryComplete, EventBus, LoggingObserver, ParseComplete
from kp_compiler.infrastructure.filesystem import FilesystemReader
from kp_compiler.stages.discover_ontology import discover_ontology, generate_ontology_yaml
from kp_compiler.stages.parse import parse_source


class CompilationPreparation:
    """Handles source discovery, ontology loading, and parsing."""

    def __init__(self) -> None:
        self._reader = FilesystemReader()

    def create_bus(self) -> EventBus:
        bus = EventBus()
        LoggingObserver(bus)
        return bus

    def ensure_utf8_stdout(self) -> None:
        import sys

        if (
            hasattr(sys.stdout, "buffer")
            and getattr(sys.stdout, "encoding", "")
            and sys.stdout.encoding.lower() not in {"utf-8", "utf8"}
        ):
            import io

            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    def discover_sources(self, source_root: Path, bus: EventBus) -> list[Path]:
        source_files = self._reader.discover(source_root)
        print(f"[discover] Found {len(source_files)} source files")
        bus.emit(DiscoveryComplete(file_count=len(source_files)))
        return source_files

    def maybe_discover_ontology(
        self,
        enabled: bool,
        source_files: list[Path],
        source_root: Path,
        ontology_path: Path,
    ) -> None:
        if not enabled:
            return
        result = discover_ontology(source_files, source_root)
        print(
            f"[ontology-discover] {len(result.types)} types, "
            f"{len(result.predicates)} predicates, domains={sorted(result.domains)}"
        )
        existing_data = None
        if ontology_path.exists():
            from ruamel.yaml import YAML

            existing_data = YAML(typ="safe").load(ontology_path.read_text(encoding="utf-8"))
            print(f"[ontology-discover] Merging with existing {ontology_path}")
        ontology_path.parent.mkdir(parents=True, exist_ok=True)
        ontology_path.write_text(generate_ontology_yaml(result, existing_data), encoding="utf-8")
        print(f"[ontology-discover] Wrote {ontology_path}")

    def load_ontology(self, ontology_path: Path, source_files: list[Path], source_root: Path) -> Ontology:
        from ruamel.yaml import YAML

        ontology = Ontology.from_dict(YAML(typ="safe").load(ontology_path.read_text(encoding="utf-8")))
        print(f"[ontology] Loaded v{ontology.version}")
        result = discover_ontology(source_files, source_root)
        added = ontology.merge_discovered_predicates(result.predicates)
        if added:
            print(f"[ontology] Merged {added} corpus-discovered predicates")
        return ontology

    def parse_sources(
        self,
        source_files: list[Path],
        source_root: Path,
        bus: EventBus,
    ) -> tuple[list[KnowledgeObject], list[Diagnostic]]:
        objects: list[KnowledgeObject] = []
        diagnostics: list[Diagnostic] = []
        parse_errors = 0
        for file_path in source_files:
            content = self._reader.read(file_path)
            relative_path = str(file_path.relative_to(source_root.parent)).replace("\\", "/")
            try:
                objects.append(parse_source(content, relative_path))
            except (OntologyViolation, ValueError, KeyError, TypeError) as error:
                parse_errors += 1
                diagnostics.append(Diagnostic(Severity.ERROR, relative_path, f"Parse error: {error}", "parse"))
        print(f"[parse] Parsed {len(objects)} objects")
        bus.emit(ParseComplete(object_count=len(objects), error_count=parse_errors))
        return objects, diagnostics
