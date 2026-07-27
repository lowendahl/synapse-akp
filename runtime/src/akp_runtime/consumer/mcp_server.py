"""MCP server entry point — stdio transport for Knowledge Pack retrieval.

What: Exposes 5 MCP tools over stdio for knowledge pack retrieval.
Why: Agents need structured, typed access to compiled knowledge packs.
Boundaries: Consumer layer only — delegates to operations + infrastructure.
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP

from akp_runtime.consumer.tool_handlers import ToolHandlerRegistry
from akp_runtime.contracts.protocols import QueryEmbedder, VectorIndex
from akp_runtime.infrastructure.config_loader import YamlConfigLoader
from akp_runtime.infrastructure.duckdb_loader import DuckDBLoadedPack, DuckDBPackLoader

logger = logging.getLogger(__name__)

_MAX_QUERY_LENGTH = 500
_MAX_IDENTIFIER_LENGTH = 200


class PackContext:
    """Lifespan state holding loaded packs, vector indexes, and operations."""

    def __init__(
        self,
        packs: dict[str, DuckDBLoadedPack],
        vector_indexes: dict[str, VectorIndex] | None = None,
        embedder: QueryEmbedder | None = None,
    ) -> None:
        self.packs = packs
        self.vector_indexes = vector_indexes or {}
        self.embedder = embedder
        self.handlers = ToolHandlerRegistry(packs, vector_indexes=self.vector_indexes, embedder=embedder)


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[PackContext]:
    """Load packs at startup, close on shutdown."""
    config_path = getattr(server, "_akp_config_path", None)
    loader = YamlConfigLoader()
    config = loader.load(config_path)

    from akp_runtime.infrastructure.pack_source_resolver import PackResolutionError, PackSourceResolver

    resolver = PackSourceResolver(default_cache_directory=config.pack_cache_directory)
    pack_loader = DuckDBPackLoader()
    packs: dict[str, DuckDBLoadedPack] = {}

    for binding in config.packs:
        try:
            resolved_path = resolver.resolve(binding)
        except PackResolutionError as error:
            if binding.required:
                logger.error("Required pack '%s' not resolvable: %s", binding.pack_id, error)
                raise SystemExit(1) from error
            logger.warning("Optional pack '%s' not resolvable, skipping", binding.pack_id)
            continue
        pack = pack_loader.load(resolved_path)
        packs[pack.metadata.pack_id] = pack
        logger.info("Loaded pack: %s (%d objects)", pack.metadata.pack_id, pack.metadata.object_count)

    if not packs:
        logger.error("No packs loaded — check config.yaml packs section")
        raise SystemExit(1)

    # Load vector indexes for packs that have embeddings
    from akp_runtime.infrastructure.usearch_reader import USearchVectorIndex

    vector_indexes: dict[str, USearchVectorIndex] = {}
    embedder = None

    for pack_id, pack in packs.items():
        # Find .usearch sidecar alongside the pack's .duckdb
        pack_path = pack.metadata.path
        usearch_path = pack_path.with_suffix(".usearch")

        # Also check in extracted .akp directory
        if not usearch_path.exists():
            usearch_path = pack_path.parent / "pack.usearch"

        if not usearch_path.exists():
            logger.debug("No vector index for pack '%s'", pack_id)
            continue

        # Load vector labels (unit_ids in order) from DuckDB
        try:
            labels = pack.vector_unit_labels()
            dimensions = pack.metadata.embedding_dimensions
            if dimensions > 0 and labels:
                vector_indexes[pack_id] = USearchVectorIndex(usearch_path, dimensions, labels)
                logger.info("Loaded vector index for '%s': %d vectors, %dd", pack_id, len(labels), dimensions)
        except Exception:
            logger.exception("Failed to load vector index for '%s'", pack_id)

    # Initialize embedder if any vectors loaded
    if vector_indexes and config.embeddings_enabled:
        try:
            from akp_runtime.infrastructure.fastembed_adapter import FastEmbedQueryEmbedder

            embedder = FastEmbedQueryEmbedder()
            logger.info("Query embedder initialized")
        except Exception:
            logger.warning("Failed to initialize embedder — vector search disabled")

    logger.info("AKP Runtime ready: %d pack(s), %d vector index(es)", len(packs), len(vector_indexes))
    try:
        yield PackContext(packs=packs, vector_indexes=vector_indexes, embedder=embedder)
    finally:
        for pack in packs.values():
            pack.close()
        logger.info("All packs closed")


def _create_server(config_path: Path | None = None) -> FastMCP:
    """Create and configure the MCP server with all tools registered."""
    mcp = FastMCP(
        name="akp-runtime",
        instructions=(
            "AKP Runtime provides structured access to compiled knowledge packs. "
            "Use akp_search for broad queries, akp_lookup_concept for known IDs, "
            "akp_explain_concept for human-readable explanations, "
            "akp_expand_graph for relationship traversal, and "
            "akp_get_provenance for source tracing."
        ),
        lifespan=server_lifespan,
    )
    mcp._akp_config_path = config_path  # noqa: SLF001

    @mcp.tool()
    def akp_search(
        query: str,
        limit: int = 10,
        pack_ids: list[str] | None = None,
        object_types: list[str] | None = None,
        ctx: Context = None,
    ) -> dict:
        """Search knowledge packs for concepts matching a natural-language query.

        Returns ranked results with provenance and scoring breakdown.
        """
        if len(query) > _MAX_QUERY_LENGTH:
            return {"error": f"Query too long (max {_MAX_QUERY_LENGTH} chars)"}
        pack_context: PackContext = ctx.request_context.lifespan_context
        return pack_context.handlers.handle_search(
            query=query,
            limit=min(limit, 50),
            pack_ids=pack_ids or [],
            object_types=object_types or [],
        )

    @mcp.tool()
    def akp_lookup_concept(
        identifier: str,
        include_units: bool = True,
        include_neighbors: bool = True,
        neighbor_limit: int = 10,
        ctx: Context = None,
    ) -> dict:
        """Look up a specific concept by ID or alias and return its full details.

        Returns semantic units, graph neighbors, and provenance.
        """
        if len(identifier) > _MAX_IDENTIFIER_LENGTH:
            return {"error": f"Identifier too long (max {_MAX_IDENTIFIER_LENGTH} chars)"}
        pack_context: PackContext = ctx.request_context.lifespan_context
        return pack_context.handlers.handle_lookup(
            identifier=identifier,
            include_units=include_units,
            include_neighbors=include_neighbors,
            neighbor_limit=min(neighbor_limit, 50),
        )

    @mcp.tool()
    def akp_explain_concept(
        query: str,
        detail_level: str = "standard",
        ctx: Context = None,
    ) -> dict:
        """Produce a human-readable explanation for a concept.

        Detail levels: 'brief' (definition only), 'standard' (includes formulas/thresholds),
        'detailed' (all available content). Returns structured Markdown with citations.
        """
        if len(query) > _MAX_QUERY_LENGTH:
            return {"error": f"Query too long (max {_MAX_QUERY_LENGTH} chars)"}
        if detail_level not in ("brief", "standard", "detailed"):
            return {"error": "detail_level must be 'brief', 'standard', or 'detailed'"}
        pack_context: PackContext = ctx.request_context.lifespan_context
        return pack_context.handlers.handle_explain(
            query=query,
            detail_level=detail_level,
        )

    @mcp.tool()
    def akp_expand_graph(
        object_id: str,
        hops: int = 1,
        predicates: list[str] | None = None,
        limit: int = 20,
        ctx: Context = None,
    ) -> dict:
        """Traverse the knowledge graph from a seed object.

        Returns edges (subject → predicate → object) up to N hops away.
        """
        if len(object_id) > _MAX_IDENTIFIER_LENGTH:
            return {"error": f"Object ID too long (max {_MAX_IDENTIFIER_LENGTH} chars)"}
        pack_context: PackContext = ctx.request_context.lifespan_context
        return pack_context.handlers.handle_expand_graph(
            object_id=object_id,
            hops=min(hops, 3),
            predicates=tuple(predicates or ()),
            limit=min(limit, 100),
        )

    @mcp.tool()
    def akp_get_provenance(
        object_id: str | None = None,
        unit_id: str | None = None,
        edge_subject_id: str | None = None,
        edge_predicate: str | None = None,
        edge_object_id: str | None = None,
        ctx: Context = None,
    ) -> dict:
        """Trace the provenance chain for any pack artifact (object, unit, or edge).

        Exactly one target must be specified.
        """
        pack_context: PackContext = ctx.request_context.lifespan_context
        return pack_context.handlers.handle_provenance(
            object_id=object_id,
            unit_id=unit_id,
            edge_subject_id=edge_subject_id,
            edge_predicate=edge_predicate,
            edge_object_id=edge_object_id,
        )

    return mcp


class McpServerApplication:
    """Runtime consumer entry-point wrapper."""

    def run(self) -> None:
        """Parse --config, bootstrap runtime, run MCP stdio server."""
        parser = argparse.ArgumentParser(description="AKP Runtime MCP Server")
        parser.add_argument("--config", type=Path, default=None, help="Path to config.yaml")
        parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
        args = parser.parse_args()

        logging.basicConfig(
            level=getattr(logging, args.log_level),
            format='{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
            stream=sys.stderr,
        )

        server = _create_server(config_path=args.config)
        server.run(transport="stdio")


def main() -> None:
    """Run the MCP server application."""
    McpServerApplication().run()
