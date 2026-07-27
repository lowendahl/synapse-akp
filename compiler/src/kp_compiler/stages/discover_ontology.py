"""Ontology discovery stage facade."""

from __future__ import annotations

from pathlib import Path

from kp_compiler.stages.ontology_discovery_models import DiscoveredPredicate, DiscoveredType, OntologyDiscoveryResult
from kp_compiler.stages.ontology_document_renderer import OntologyDocumentRenderer
from kp_compiler.stages.ontology_scanner import OntologyScanner


class OntologyDiscoveryStage:
    """Coordinates ontology scanning and rendering."""

    def __init__(self) -> None:
        self._scanner = OntologyScanner()
        self._renderer = OntologyDocumentRenderer()

    def discover(self, source_files: list[Path], source_root: Path) -> OntologyDiscoveryResult:
        return self._scanner.discover(source_files, source_root)

    def render(self, result: OntologyDiscoveryResult, existing_ontology: dict | None = None) -> str:
        return self._renderer.render(result, existing_ontology)


_stage = OntologyDiscoveryStage()
discover_ontology = _stage.discover
generate_ontology_yaml = _stage.render
__all__ = [
    "DiscoveredPredicate",
    "DiscoveredType",
    "OntologyDiscoveryResult",
    "OntologyDiscoveryStage",
    "discover_ontology",
    "generate_ontology_yaml",
]
