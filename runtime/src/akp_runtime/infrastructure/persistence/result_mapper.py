"""Result mapping from raw query rows to domain objects.

What: Maps DuckDB row tuples into typed domain models.
Why: Isolates mapping logic from query execution and connection management.
"""

from __future__ import annotations

from akp_runtime.contracts.protocols import ResultMapper
from akp_runtime.domain.models import ProvenanceStep, SearchHit, SemanticUnitRecord


class SearchHitMapper(ResultMapper):
    """Maps raw query rows to domain SearchHit objects."""

    def __init__(self, pack_id: str, pack_version: str, provenance_step: ProvenanceStep) -> None:
        self._pack_id = pack_id
        self._pack_version = pack_version
        self._provenance_step = provenance_step

    def from_object_row(self, row: tuple) -> SearchHit:
        """Convert (id, type, title, desc, domain, source_path) to SearchHit."""
        return SearchHit(
            pack_id=self._pack_id,
            pack_version=self._pack_version,
            object_id=row[0],
            unit_id=None,
            title=row[2] or "",
            object_type=row[1] or "",
            domain=row[4] or "",
            heading_path=None,
            snippet=row[3] or "",
            score=1.0,
            source_kind="authored",
            channels=(),
            provenance=(self._provenance_step,),
        )


class SemanticUnitMapper:
    """Maps raw query rows to SemanticUnitRecord domain objects."""

    @staticmethod
    def from_row(row: tuple) -> SemanticUnitRecord:
        """Convert (id, source_object_id, heading_path, content, context, type, domain, title, desc, path)."""
        return SemanticUnitRecord(
            unit_id=row[0],
            source_object_id=row[1],
            heading_path=row[2] or "",
            content=row[3] or "",
            context=row[4] or "",
            object_type=row[5] or "",
            domain=row[6] or "",
            title=row[7] or "",
            description=row[8] or "",
            source_path=row[9] or "",
            source_kind="authored",
        )
