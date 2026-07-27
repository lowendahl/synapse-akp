"""Knowledge Pack consumer CLI."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import duckdb

from kp_compiler.consumer.knowledge_pack_search_service import KnowledgePackSearchService
from kp_compiler.consumer.search_result_printer import SearchResultPrinter


class PackSearcher(KnowledgePackSearchService):
    """Backward-compatible alias for compiled-pack search helpers."""


class KnowledgePackFindCommand:
    """Command entry point for kp-find."""

    def __init__(self) -> None:
        self._search_service = KnowledgePackSearchService()
        self._printer = SearchResultPrinter()

    def main(self) -> None:
        import argparse
        import io

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        parser = argparse.ArgumentParser(prog="kp-find", description="Search a compiled Knowledge Pack")
        parser.add_argument("query")
        parser.add_argument("--pack", type=Path, default=Path("dist/kp-csu.duckdb"))
        parser.add_argument("--exact", action="store_true")
        parser.add_argument("--graph", action="store_true")
        parser.add_argument("--semantic", action="store_true")
        parser.add_argument("--hops", type=int, default=2)
        args = parser.parse_args()
        if not args.pack.exists():
            print(f"Error: pack '{args.pack}' does not exist. Run kp-compile first.")
            raise SystemExit(1)
        connection = duckdb.connect(str(args.pack), read_only=True)
        try:
            self._run(args.pack, connection, args)
        finally:
            connection.close()

    def _run(
        self,
        pack_path: Path,
        connection: duckdb.DuckDBPyConnection,
        args: SimpleNamespace,
    ) -> None:
        print(f'>> Searching for: "{args.query}"\n')
        alias_hits = self._search_service.search_aliases(connection, args.query)
        self._printer.print_alias_hits(alias_hits)
        if args.exact:
            return
        bm25_hits = self._deduplicate_bm25(self._search_service.search_bm25(connection, args.query, top_k=10))
        self._printer.print_ranked_hits("BM25 Lexical", bm25_hits, "score")
        semantic_hits = (
            self._search_service.search_semantic(pack_path, connection, args.query, top_k=10) if args.semantic else []
        )
        self._printer.print_ranked_hits("Semantic", semantic_hits, "distance")
        object_hits = self._search_service.search_objects(connection, args.query)
        self._printer.print_object_hits(object_hits)
        target_id = alias_hits[0]["id"] if alias_hits else object_hits[0]["id"] if object_hits else ""
        if (args.graph or alias_hits) and target_id:
            graph_hits = self._search_service.expand_graph(connection, target_id, args.hops)
            self._printer.print_graph_hits(target_id, graph_hits)
        if bm25_hits and (semantic_hits or object_hits):
            fused_hits = self._search_service.rrf_fuse(bm25_hits, semantic_hits, id_key="unit_id")
            self._printer.print_fused_hits(fused_hits)
        self._printer.print_summary(alias_hits, bm25_hits, semantic_hits, object_hits)

    def _deduplicate_bm25(self, hits: list[dict]) -> list[dict]:
        best_by_title: dict[str, dict] = {}
        for hit in hits:
            if hit["title"] not in best_by_title or hit["score"] > best_by_title[hit["title"]]["score"]:
                best_by_title[hit["title"]] = hit
        return sorted(best_by_title.values(), key=lambda item: item["score"], reverse=True)


_command = KnowledgePackFindCommand()
_searcher = PackSearcher()
search_aliases = _searcher.search_aliases
search_bm25 = _searcher.search_bm25
search_semantic = _searcher.search_semantic
search_objects = _searcher.search_objects
expand_graph = _searcher.expand_graph
rrf_fuse = _searcher.rrf_fuse
main = _command.main


if __name__ == "__main__":
    main()
