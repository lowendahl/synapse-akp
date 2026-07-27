"""Stage protocol contracts for compiler flow."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from kp_compiler.contracts.protocol_support_types import Diagnostic, GraphResult
from kp_compiler.domain.models import KnowledgeObject


@runtime_checkable
class SourceReader(Protocol):
    def discover(self, root: Path) -> list[Path]: ...
    def read(self, path: Path) -> str: ...


@runtime_checkable
class Parser(Protocol):
    def parse(self, content: str, source_path: str) -> KnowledgeObject: ...


@runtime_checkable
class Validator(Protocol):
    def validate(self, obj: KnowledgeObject) -> list[Diagnostic]: ...


@runtime_checkable
class Enricher(Protocol):
    def enrich(self, obj: KnowledgeObject) -> KnowledgeObject: ...


@runtime_checkable
class GraphBuilder(Protocol):
    def build(self, objects: list[KnowledgeObject]) -> GraphResult: ...
