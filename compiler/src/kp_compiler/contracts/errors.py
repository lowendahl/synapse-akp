"""Typed exception hierarchy for the Knowledge Pack Compiler.

Every exception carries structured context so that diagnostics are
always actionable. No bare Exception or string-only errors allowed (ES-04).
"""

from dataclasses import dataclass, field


class CompilerError(Exception):
    """Base for all compiler errors."""


# ─── Ontology & Validation ─────────────────────────────────────────────────


@dataclass
class OntologyViolation(CompilerError):
    """Raised when a source file uses an unknown type or predicate."""

    source_file: str
    object_id: str
    violation: str
    line: int | None = None

    def __str__(self) -> str:
        loc = f":{self.line}" if self.line else ""
        return f"[{self.source_file}{loc}] {self.object_id}: {self.violation}"


@dataclass
class SchemaViolation(CompilerError):
    """Raised when required frontmatter fields are missing."""

    source_file: str
    object_type: str
    missing_fields: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"[{self.source_file}] type={self.object_type} missing: {', '.join(self.missing_fields)}"


@dataclass
class DuplicateId(CompilerError):
    """Raised when two objects share the same stable ID."""

    id: str
    first_file: str
    second_file: str

    def __str__(self) -> str:
        return f"Duplicate ID '{self.id}': {self.first_file} and {self.second_file}"


@dataclass
class DanglingReference(CompilerError):
    """Raised when a reference points to a non-existent ID."""

    source_file: str
    reference_id: str
    context: str = ""

    def __str__(self) -> str:
        ctx = f" ({self.context})" if self.context else ""
        return f"[{self.source_file}] dangling reference: '{self.reference_id}'{ctx}"


@dataclass
class InvalidIdFormat(CompilerError):
    """Raised when a stable ID doesn't match the required format."""

    source_file: str
    id_value: str
    expected_pattern: str

    def __str__(self) -> str:
        return f"[{self.source_file}] invalid ID '{self.id_value}': expected {self.expected_pattern}"


# ─── Graph ──────────────────────────────────────────────────────────────────


@dataclass
class CycleDetected(CompilerError):
    """Raised when a cycle is found in an acyclic predicate."""

    predicate: str
    cycle_path: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Cycle in '{self.predicate}': {' → '.join(self.cycle_path)}"


@dataclass
class OrphanNode(CompilerError):
    """Raised when a node has zero edges (warning-level)."""

    object_id: str
    source_file: str

    def __str__(self) -> str:
        return f"Orphan node '{self.object_id}' in {self.source_file}"


# ─── Build ──────────────────────────────────────────────────────────────────


@dataclass
class BuildFailure(CompilerError):
    """Raised when the build cannot produce a valid pack."""

    error_count: int
    diagnostics: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Build failed with {self.error_count} error(s)"


@dataclass
class ProvenanceMissing(CompilerError):
    """Raised when an object is missing provenance metadata."""

    object_id: str
    stage: str

    def __str__(self) -> str:
        return f"Missing provenance for '{self.object_id}' after stage '{self.stage}'"
