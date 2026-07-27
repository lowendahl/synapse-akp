"""Console formatting for compiled pack search results."""

from __future__ import annotations


class SearchResultPrinter:
    """Prints search channel output to stdout."""

    def print_alias_hits(self, hits: list[dict]) -> None:
        if hits:
            print(f"=== Exact Matches ({len(hits)}) ===")
            for hit in hits:
                print(f"  [{hit['type']}] {hit['title']}")
                print(f"    ID: {hit['id']}")
                print(f'    Matched alias: "{hit["alias"]}" ({hit["alias_type"]})')
                if hit["description"]:
                    print(f"    {hit['description'][:150]}")
                print()

    def print_ranked_hits(self, title: str, hits: list[dict], score_label: str) -> None:
        if hits:
            print(f"=== {title} ({len(hits)}) ===")
            for hit in hits[:5]:
                print(f"  [{hit['type']}] {hit['title']} > {hit['heading']}  ({score_label}={hit[score_label]:.4f})")
                print(f"    {hit['snippet'][:120]}...")
                print()

    def print_object_hits(self, hits: list[dict]) -> None:
        if hits:
            print(f"=== Object Matches ({len(hits)}) ===")
            for hit in hits:
                print(f"  [{hit['type']}] {hit['title']} ({hit['domain']})")
                print(f"    ID: {hit['id']}")
                if hit["description"]:
                    print(f"    {hit['description'][:150]}")
                print()

    def print_graph_hits(self, target_id: str, hits: list[dict]) -> None:
        if hits:
            print(f"=== Graph Neighborhood ({target_id}) ===")
            for edge in hits:
                direction = "->" if edge["subject"] == target_id else "<-"
                other = edge["object"] if edge["subject"] == target_id else edge["subject"]
                print(f"  {direction} [{edge['predicate']}] {other}")
                if edge["neighbor_title"]:
                    print(f"    ({edge['neighbor_type']}: {edge['neighbor_title']})")
            print()

    def print_fused_hits(self, hits: list[dict]) -> None:
        if hits:
            print("=== Fused Top Results (RRF) ===")
            for index, hit in enumerate(hits[:5], start=1):
                print(f"  {index}. [{hit.get('type', '')}] {hit.get('title', '')} > {hit.get('heading', '')}")
            print()

    def print_summary(
        self,
        alias_hits: list[dict],
        bm25_hits: list[dict],
        semantic_hits: list[dict],
        object_hits: list[dict],
    ) -> None:
        total = len(alias_hits) + len(bm25_hits) + len(semantic_hits) + len(object_hits)
        if total == 0:
            print("No results found.")
            return
        channels = []
        for label, hits in (
            ("alias", alias_hits),
            ("BM25", bm25_hits),
            ("semantic", semantic_hits),
            ("object", object_hits),
        ):
            if hits:
                channels.append(f"{len(hits)} {label}")
        print(f"-- Found {total} total results: {', '.join(channels)}")
