"""Typed exception hierarchy for the AKP Runtime.

Every exception carries structured context so that diagnostics are
always actionable. No bare Exception or string-only errors allowed.
"""

from dataclasses import dataclass, field
from pathlib import Path


class RuntimeErrorBase(Exception):
    """Base for all AKP runtime failures."""


@dataclass
class ConfigurationError(RuntimeErrorBase):
    source: str
    violation: str

    def __str__(self) -> str:
        return f"[{self.source}] {self.violation}"


@dataclass
class PackOpenError(RuntimeErrorBase):
    pack_path: Path
    detail: str

    def __str__(self) -> str:
        return f"Cannot open pack '{self.pack_path}': {self.detail}"


@dataclass
class UnsupportedSchemaVersion(RuntimeErrorBase):
    pack_path: Path
    found: str
    supported_major: str = "2"

    def __str__(self) -> str:
        return f"[{self.pack_path}] schema_version={self.found}; expected major {self.supported_major}.x"


@dataclass
class MissingPackTable(RuntimeErrorBase):
    pack_path: Path
    table_name: str

    def __str__(self) -> str:
        return f"[{self.pack_path}] missing required table '{self.table_name}'"


@dataclass
class MissingManifestKey(RuntimeErrorBase):
    pack_path: Path
    key: str

    def __str__(self) -> str:
        return f"[{self.pack_path}] manifest missing key '{self.key}'"


@dataclass
class DuplicatePackId(RuntimeErrorBase):
    pack_id: str
    paths: list[Path] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Duplicate pack_id '{self.pack_id}': {', '.join(str(p) for p in self.paths)}"


@dataclass
class PackNotLoaded(RuntimeErrorBase):
    pack_id: str
    loaded_pack_ids: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Pack '{self.pack_id}' not loaded. Available: {', '.join(self.loaded_pack_ids)}"


@dataclass
class VectorIndexMissing(RuntimeErrorBase):
    pack_id: str
    expected_path: Path

    def __str__(self) -> str:
        return f"Pack '{self.pack_id}' is missing vector sidecar '{self.expected_path.name}'"


@dataclass
class ObjectNotFound(RuntimeErrorBase):
    identifier: str
    searched_packs: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Object '{self.identifier}' not found in packs: {', '.join(self.searched_packs)}"


@dataclass
class ProvenanceNotFound(RuntimeErrorBase):
    target_type: str
    target_id: str

    def __str__(self) -> str:
        return f"No provenance found for {self.target_type} '{self.target_id}'"
