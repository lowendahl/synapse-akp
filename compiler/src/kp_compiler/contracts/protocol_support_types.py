"""Support types shared by compiler protocols."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Diagnostic:
    """A structured build diagnostic."""

    severity: Severity
    source_file: str
    message: str
    stage: str
    object_id: str = ""
    line: int | None = None


@dataclass(frozen=True)
class GraphNode:
    """A node in the compiled knowledge graph."""

    id: str
    type: str
    title: str
    domain: str
    source_path: str
    pagerank: float = 0.0
    in_degree: int = 0
    out_degree: int = 0


@dataclass(frozen=True)
class GraphEdge:
    """An edge in the compiled knowledge graph."""

    subject_id: str
    object_id: str
    predicate: str = "references"
    origin: str = "authored"
    confidence: float | None = None


@dataclass
class GraphResult:
    """Output of the graph builder stage."""

    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    metrics: dict[str, int] = field(default_factory=dict)
