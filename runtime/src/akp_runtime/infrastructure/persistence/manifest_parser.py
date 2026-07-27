"""Manifest parsing and metadata construction.

What: Parses DuckDB manifest key-value pairs into PackMetadata.
Why: Separates validation logic from connection management.
"""

from __future__ import annotations

from pathlib import Path

from akp_runtime.contracts.errors import UnsupportedSchemaVersion
from akp_runtime.contracts.protocols import ManifestParserProtocol
from akp_runtime.domain.models import PackMetadata

REQUIRED_TABLES = ("objects", "semantic_units", "aliases", "edges", "manifest")

REQUIRED_MANIFEST_KEYS = frozenset(
    {
        "pack_id",
        "pack_version",
        "schema_version",
        "ontology_version",
        "compiler_version",
        "build_timestamp",
        "source_file_count",
        "object_count",
        "node_count",
        "edge_count",
        "semantic_unit_count",
        "alias_count",
        "bm25_vocab_size",
        "embedding_model",
        "embedding_dimensions",
        "cross_pack_refs",
        "content_hash",
        "error_count",
        "warning_count",
    }
)

_INT_MANIFEST_KEYS = frozenset(
    {
        "source_file_count",
        "object_count",
        "node_count",
        "edge_count",
        "semantic_unit_count",
        "alias_count",
        "bm25_vocab_size",
        "embedding_dimensions",
        "cross_pack_refs",
        "error_count",
        "warning_count",
    }
)


class ManifestParser(ManifestParserProtocol):
    """Parses and validates manifest key-value pairs into PackMetadata."""

    @staticmethod
    def parse_value(key: str, value: str) -> str | int:
        """Parse manifest string values to appropriate Python types."""
        if key in _INT_MANIFEST_KEYS:
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0
        return value

    def build_metadata(self, manifest: dict[str, str], path: Path) -> PackMetadata:
        """Construct PackMetadata from validated manifest dict."""
        schema_version = manifest["schema_version"]
        major = schema_version.split(".")[0]
        if major != "2":
            raise UnsupportedSchemaVersion(pack_path=path, found=schema_version)

        parsed = {k: self.parse_value(k, v) for k, v in manifest.items()}
        return PackMetadata(
            pack_id=parsed["pack_id"],
            pack_version=parsed["pack_version"],
            schema_version=parsed["schema_version"],
            compiler_version=parsed["compiler_version"],
            path=path,
            content_hash=parsed["content_hash"],
            ontology_version=parsed["ontology_version"],
            build_timestamp=parsed["build_timestamp"],
            source_file_count=parsed["source_file_count"],
            object_count=parsed["object_count"],
            node_count=parsed["node_count"],
            edge_count=parsed["edge_count"],
            semantic_unit_count=parsed["semantic_unit_count"],
            alias_count=parsed["alias_count"],
            bm25_vocab_size=parsed["bm25_vocab_size"],
            embedding_model=parsed["embedding_model"],
            embedding_dimensions=parsed["embedding_dimensions"],
            cross_pack_refs=parsed["cross_pack_refs"],
            error_count=parsed["error_count"],
            warning_count=parsed["warning_count"],
        )
