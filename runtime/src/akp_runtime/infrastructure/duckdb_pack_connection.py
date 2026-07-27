"""Connection and metadata helpers for loaded packs."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from akp_runtime.contracts.errors import MissingManifestKey, MissingPackTable
from akp_runtime.contracts.protocols import SchemaValidator
from akp_runtime.domain.models import PackMetadata, ProvenanceStep
from akp_runtime.infrastructure.persistence.manifest_parser import (
    REQUIRED_MANIFEST_KEYS,
    REQUIRED_TABLES,
    ManifestParser,
)
from akp_runtime.infrastructure.persistence.queries.base import QueryExecutor
from akp_runtime.infrastructure.persistence.queries.schema_validation import (
    ListTablesQuery,
    LoadManifestQuery,
)


class ConnectionProtocol(Protocol):
    """Minimal connection interface for schema validation helpers."""

    def close(self) -> None: ...


class DuckDBPackConnection(SchemaValidator):
    """Validates schema and exposes metadata for a loaded pack. Implements SchemaValidator protocol."""

    def __init__(
        self,
        path: Path,
        connection: ConnectionProtocol,
        executor: QueryExecutor,
    ) -> None:
        self._path = path
        self._connection = connection
        self._executor = executor

    def build_metadata(self) -> PackMetadata:
        self._validate_schema()
        manifest = self._load_manifest()
        return ManifestParser().build_metadata(manifest, self._path)

    def pack_provenance_step(self, metadata: PackMetadata) -> ProvenanceStep:
        return ProvenanceStep(
            layer="pack",
            identifier=metadata.pack_id,
            origin="authored",
            pack_id=metadata.pack_id,
            pack_version=metadata.pack_version,
        )

    def _validate_schema(self) -> None:
        existing = self._executor.execute(ListTablesQuery())
        for table in REQUIRED_TABLES:
            if table not in existing:
                self._connection.close()
                raise MissingPackTable(pack_path=self._path, table_name=table)

    def _load_manifest(self) -> dict[str, str]:
        manifest = self._executor.execute(LoadManifestQuery())
        missing = REQUIRED_MANIFEST_KEYS - manifest.keys()
        if missing:
            self._connection.close()
            raise MissingManifestKey(pack_path=self._path, key=sorted(missing)[0])
        return manifest
