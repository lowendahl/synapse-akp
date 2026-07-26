"""Provenance domain models.

What: Frozen dataclasses for provenance chain steps and metadata handling.
Why: Every result must trace to its knowledge source for explainability.
Boundaries: No IO, no infrastructure imports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Literal

SourceKind = Literal["authored", "derived", "inferred", "generated"]

MetadataValue = str | int | float | bool | tuple[str, ...]
MetadataMap = MappingProxyType[str, MetadataValue]

_EMPTY_METADATA: MetadataMap = MappingProxyType({})


class MetadataFreezer:
    """Converts mutable metadata dicts to deeply-immutable MappingProxyType."""

    @staticmethod
    def freeze(
        raw: dict[str, str | int | float | bool | list[str] | tuple[str, ...]] | None,
    ) -> MetadataMap:
        """Convert a mutable metadata dict to a deeply-immutable MappingProxyType."""
        if not raw:
            return _EMPTY_METADATA
        frozen: dict[str, MetadataValue] = {}
        for k, v in raw.items():
            frozen[k] = tuple(v) if isinstance(v, list) else v
        return MappingProxyType(frozen)


@dataclass(frozen=True)
class ProvenanceStep:
    """A single step in a provenance chain recording origin and lineage."""

    layer: str
    identifier: str
    origin: SourceKind
    source_path: str | None = None
    source_revision: str | None = None
    pack_id: str | None = None
    pack_version: str | None = None
    _metadata: MetadataMap = field(default=_EMPTY_METADATA, repr=False)

    def __init__(
        self,
        layer: str,
        identifier: str,
        origin: SourceKind,
        source_path: str | None = None,
        source_revision: str | None = None,
        pack_id: str | None = None,
        pack_version: str | None = None,
        metadata: dict[str, str | int | float | bool | list[str] | tuple[str, ...]] | None = None,
    ) -> None:
        object.__setattr__(self, "layer", layer)
        object.__setattr__(self, "identifier", identifier)
        object.__setattr__(self, "origin", origin)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "source_revision", source_revision)
        object.__setattr__(self, "pack_id", pack_id)
        object.__setattr__(self, "pack_version", pack_version)
        object.__setattr__(self, "_metadata", MetadataFreezer.freeze(metadata))

    @property
    def metadata(self) -> MetadataMap:
        """Deeply-immutable metadata mapping."""
        return self._metadata
