"""Knowledge Pack Consumer CLI — find knowledge in a compiled pack.

Usage:
    kp-find "UDC"
    kp-find "What is the relationship between a milestone and Job1"
    kp-find --exact "C2C"
    kp-find --graph "csu.metric.job1-c2c" --hops 2
    kp-find --semantic "cloud adoption risk factors"

V2: Implements stages 1-6 of the retrieval pipeline with BM25 + vector + RRF.
"""

from __future__ import annotations

import sys
from pathlib import Path


def search_aliases(con, query: str) -> list[dict]:
    """Stage 1: Exact identity + alias lookup."""
    results = con.execute(
        """
        SELECT a.canonical_id, a.alias, a.alias_type, o.title, o.type, o.description
        FROM aliases a
        JOIN objects o ON a.canonical_id = o.id
        WHERE LOWER(a.alias) = LOWER(?)
           OR LOWER(a.alias) LIKE LOWER(?)
        LIMIT 10
        """,
        [query, f"%{query}%"],
    ).fetchall()
    return [
        {"id": r[0], "alias": r[1], "alias_type": r[2], "title": r[3], "type": r[4], "description": r[5]}
        for r in results
    ]


def search_bm25(con, query: str, top_k: int = 10) -> list[dict]:
    """Stage 2: BM25 lexical retrieval over semantic units."""
    try:
        import bm25s

        # Load semantic unit texts from DuckDB for BM25
        rows = con.execute(
            "SELECT su.id, su.heading_path, su.content, su.context, o.title, o.type "
            "FROM semantic_units su "
            "JOIN objects o ON su.source_object_id = o.id"
        ).fetchall()
        if not rows:
            return []

        unit_ids = [r[0] for r in rows]
        corpus_texts = [
            f"{r[1]} {r[2]}" for r in rows  # heading + content only (no context/aliases)
        ]

        # Build BM25 index from text
        corpus_tokens = bm25s.tokenize(corpus_texts, stopwords="en")
        retriever = bm25s.BM25()
        retriever.index(corpus_tokens)

        # Search
        query_tokens = bm25s.tokenize([query], stopwords="en")
        k = min(top_k, len(unit_ids))
        scores, indices = retriever.retrieve(query_tokens, k=k)

        hits = []
        for i in range(scores.shape[1]):
            idx = int(indices[0, i])
            score = float(scores[0, i])
            if score > 0 and idx < len(rows):
                r = rows[idx]
                hits.append({
                    "unit_id": r[0], "score": score, "heading": r[1],
                    "snippet": r[2][:200], "title": r[4], "type": r[5],
                })
        return hits
    except Exception:
        return []


def search_semantic(pack_path: Path, con, query: str, top_k: int = 10) -> list[dict]:
    """Stage 4: Dense vector retrieval via fastembed + usearch."""
    try:
        usearch_path = pack_path.with_suffix(".usearch")
        if not usearch_path.exists():
            return []

        from fastembed import TextEmbedding
        from usearch.index import Index

        # Get unit_ids ordering from vector_metadata
        rows = con.execute(
            "SELECT unit_id FROM vector_metadata ORDER BY rowid"
        ).fetchall()
        if not rows:
            return []
        unit_ids = [r[0] for r in rows]

        # Embed query
        model_row = con.execute(
            "SELECT model_name FROM vector_metadata LIMIT 1"
        ).fetchone()
        model_name = model_row[0] if model_row else "BAAI/bge-small-en-v1.5"
        model = TextEmbedding(model_name=model_name)
        query_vec = list(model.query_embed([query]))[0]

        # Search index
        import numpy as np
        index = Index.restore(str(usearch_path))
        results = index.search(np.array(query_vec, dtype=np.float32), min(top_k, len(unit_ids)))

        hits = []
        for i in range(len(results.keys)):
            idx = int(results.keys[i])
            dist = float(results.distances[i])
            if idx < len(unit_ids):
                uid = unit_ids[idx]
                row = con.execute(
                    "SELECT su.heading_path, su.content, o.title, o.type "
                    "FROM semantic_units su JOIN objects o ON su.source_object_id = o.id "
                    "WHERE su.id = ?",
                    [uid],
                ).fetchone()
                if row:
                    hits.append({
                        "unit_id": uid, "distance": dist, "heading": row[0],
                        "snippet": row[1][:200], "title": row[2], "type": row[3],
                    })
        return hits
    except Exception:
        return []


def search_objects(con, query: str) -> list[dict]:
    """Search objects by title, description, or content."""
    results = con.execute(
        """
        SELECT id, type, title, description, domain
        FROM objects
        WHERE LOWER(title) LIKE LOWER(?)
           OR LOWER(description) LIKE LOWER(?)
        ORDER BY
            CASE WHEN LOWER(title) LIKE LOWER(?) THEN 0 ELSE 1 END,
            LENGTH(title)
        LIMIT 10
        """,
        [f"%{query}%", f"%{query}%", f"%{query}%"],
    ).fetchall()
    return [
        {"id": r[0], "type": r[1], "title": r[2], "description": r[3], "domain": r[4]}
        for r in results
    ]


def expand_graph(con, object_id: str, hops: int = 2) -> list[dict]:
    """Stage 5: Graph expansion -- follow edges N hops from a node."""
    edges = con.execute(
        """
        SELECT e.subject_id, e.predicate, e.object_id, o.title, o.type
        FROM edges e
        LEFT JOIN objects o ON (
            CASE WHEN e.subject_id = ? THEN e.object_id ELSE e.subject_id END
        ) = o.id
        WHERE e.subject_id = ? OR e.object_id = ?
        LIMIT 30
        """,
        [object_id, object_id, object_id],
    ).fetchall()
    return [
        {"subject": r[0], "predicate": r[1], "object": r[2], "neighbor_title": r[3], "neighbor_type": r[4]}
        for r in edges
    ]


def rrf_fuse(
    *result_lists: list[dict],
    id_key: str = "unit_id",
    k: int = 60,
    top_n: int = 10,
) -> list[dict]:
    """Reciprocal Rank Fusion across multiple result lists."""
    scores: dict[str, float] = {}
    items: dict[str, dict] = {}

    for results in result_lists:
        for rank, item in enumerate(results):
            item_id = item.get(id_key, item.get("id", str(rank)))
            rrf_score = 1.0 / (k + rank + 1)
            scores[item_id] = scores.get(item_id, 0.0) + rrf_score
            if item_id not in items:
                items[item_id] = item

    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [items[i] for i in sorted_ids[:top_n] if i in items]


def main() -> None:
    """Entry point for kp-find command."""
    import argparse
    import io

    import duckdb

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        prog="kp-find",
        description="Search a compiled Knowledge Pack for concepts, relationships, and evidence",
    )
    parser.add_argument("query", help="Search query (text or concept ID)")
    parser.add_argument("--pack", type=Path, default=Path("dist/kp-csu.duckdb"), help="Path to Knowledge Pack")
    parser.add_argument("--exact", action="store_true", help="Exact alias match only")
    parser.add_argument("--graph", action="store_true", help="Expand graph neighborhood for the first result")
    parser.add_argument("--semantic", action="store_true", help="Include dense vector semantic search")
    parser.add_argument("--hops", type=int, default=2, help="Graph expansion depth")

    args = parser.parse_args()

    if not args.pack.exists():
        print(f"Error: pack '{args.pack}' does not exist. Run kp-compile first.")
        sys.exit(1)

    con = duckdb.connect(str(args.pack), read_only=True)

    print(f">> Searching for: \"{args.query}\"\n")

    # ── Stage 1: Exact alias lookup ─────────────────────────────────────────
    alias_hits = search_aliases(con, args.query)
    if alias_hits:
        print(f"=== Exact Matches ({len(alias_hits)}) ===")
        for hit in alias_hits:
            print(f"  [{hit['type']}] {hit['title']}")
            print(f"    ID: {hit['id']}")
            print(f"    Matched alias: \"{hit['alias']}\" ({hit['alias_type']})")
            if hit['description']:
                print(f"    {hit['description'][:150]}")
            print()

    if args.exact:
        con.close()
        return

    # -- Stage 2: BM25 Lexical Search (V2) ----------------------------------
    bm25_hits = search_bm25(con, args.query, top_k=10)
    # Deduplicate BM25 by source object — keep highest scoring unit per object
    seen_titles: dict[str, dict] = {}
    for hit in bm25_hits:
        key = hit["title"]
        if key not in seen_titles or hit["score"] > seen_titles[key]["score"]:
            seen_titles[key] = hit
    bm25_hits = sorted(seen_titles.values(), key=lambda h: h["score"], reverse=True)

    if bm25_hits:
        print(f"=== BM25 Lexical ({len(bm25_hits)}) ===")
        for hit in bm25_hits[:5]:
            print(f"  [{hit['type']}] {hit['title']} > {hit['heading']}  (score={hit['score']:.3f})")
            print(f"    {hit['snippet'][:120]}...")
            print()

    # ── Stage 4: Dense Semantic Search (V2) ─────────────────────────────────
    semantic_hits: list[dict] = []
    if args.semantic:
        semantic_hits = search_semantic(args.pack, con, args.query, top_k=10)
        if semantic_hits:
            print(f"=== Semantic ({len(semantic_hits)}) ===")
            for hit in semantic_hits[:5]:
                print(f"  [{hit['type']}] {hit['title']} > {hit['heading']}  (dist={hit['distance']:.4f})")
                print(f"    {hit['snippet'][:120]}...")
                print()

    # ── Stage 3: Object search (fallback) ───────────────────────────────────
    obj_hits = search_objects(con, args.query)
    if obj_hits:
        print(f"=== Object Matches ({len(obj_hits)}) ===")
        for hit in obj_hits:
            print(f"  [{hit['type']}] {hit['title']} ({hit['domain']})")
            print(f"    ID: {hit['id']}")
            if hit['description']:
                print(f"    {hit['description'][:150]}")
            print()

    # ── Stage 5: Graph expansion ────────────────────────────────────────────
    if args.graph or alias_hits:
        target_id = ""
        if alias_hits:
            target_id = alias_hits[0]["id"]
        elif obj_hits:
            target_id = obj_hits[0]["id"]

        if target_id:
            graph_hits = expand_graph(con, target_id, args.hops)
            if graph_hits:
                print(f"=== Graph Neighborhood ({target_id}) ===")
                for edge in graph_hits:
                    direction = "->" if edge["subject"] == target_id else "<-"
                    other = edge["object"] if edge["subject"] == target_id else edge["subject"]
                    print(f"  {direction} [{edge['predicate']}] {other}")
                    if edge["neighbor_title"]:
                        print(f"    ({edge['neighbor_type']}: {edge['neighbor_title']})")
                print()

    # ── RRF Fusion Summary (V2) ─────────────────────────────────────────────
    if bm25_hits and (semantic_hits or obj_hits):
        fused = rrf_fuse(bm25_hits, semantic_hits, id_key="unit_id")
        if fused:
            print(f"=== Fused Top Results (RRF) ===")
            for i, hit in enumerate(fused[:5], 1):
                title = hit.get("title", "")
                heading = hit.get("heading", "")
                print(f"  {i}. [{hit.get('type', '')}] {title} > {heading}")
            print()

    # ── Summary ─────────────────────────────────────────────────────────────
    total = len(alias_hits) + len(bm25_hits) + len(semantic_hits) + len(obj_hits)
    if total == 0:
        print("No results found.")
    else:
        channels = []
        if alias_hits:
            channels.append(f"{len(alias_hits)} alias")
        if bm25_hits:
            channels.append(f"{len(bm25_hits)} BM25")
        if semantic_hits:
            channels.append(f"{len(semantic_hits)} semantic")
        if obj_hits:
            channels.append(f"{len(obj_hits)} object")
        print(f"-- Found {total} total results: {', '.join(channels)}")

    con.close()


if __name__ == "__main__":
    main()
