"""Search services for compiled knowledge packs."""

from __future__ import annotations

from pathlib import Path

import duckdb

from kp_compiler.consumer.queries import (
    AliasSearchQuery,
    GraphExpansionQuery,
    ObjectSearchQuery,
    SemanticUnitByIdentifierQuery,
    SemanticUnitCorpusQuery,
    VectorModelNameQuery,
    VectorUnitIdentifiersQuery,
)


class KnowledgePackSearchService:
    """Runs retrieval operations against a compiled pack."""

    def search_aliases(self, connection: duckdb.DuckDBPyConnection, query: str) -> list[dict]:
        rows = AliasSearchQuery(query).execute(connection)
        return [
            {
                "id": row[0],
                "alias": row[1],
                "alias_type": row[2],
                "title": row[3],
                "type": row[4],
                "description": row[5],
            }
            for row in rows
        ]

    def search_bm25(self, connection: duckdb.DuckDBPyConnection, query: str, top_k: int = 10) -> list[dict]:
        try:
            import bm25s
        except Exception:
            return []
        try:
            rows = SemanticUnitCorpusQuery().execute(connection)
            if not rows:
                return []
            corpus_tokens = bm25s.tokenize([f"{row[1]} {row[2]}" for row in rows], stopwords="en")
            retriever = bm25s.BM25()
            retriever.index(corpus_tokens)
            scores, indices = retriever.retrieve(bm25s.tokenize([query], stopwords="en"), k=min(top_k, len(rows)))
            hits = []
            for index in range(scores.shape[1]):
                row_index = int(indices[0, index])
                score = float(scores[0, index])
                if score > 0 and row_index < len(rows):
                    row = rows[row_index]
                    hits.append(
                        {
                            "unit_id": row[0],
                            "score": score,
                            "heading": row[1],
                            "snippet": row[2][:200],
                            "title": row[4],
                            "type": row[5],
                        }
                    )
            return hits
        except Exception:
            return []

    def search_semantic(
        self,
        pack_path: Path,
        connection: duckdb.DuckDBPyConnection,
        query: str,
        top_k: int = 10,
    ) -> list[dict]:
        try:
            usearch_path = pack_path.with_suffix(".usearch")
            if not usearch_path.exists():
                return []
            import numpy as np
            from fastembed import TextEmbedding
            from usearch.index import Index

            unit_rows = VectorUnitIdentifiersQuery().execute(connection)
            if not unit_rows:
                return []
            model_name = VectorModelNameQuery().execute(connection)
            embedder = TextEmbedding(model_name=model_name[0] if model_name else "BAAI/bge-small-en-v1.5")
            query_vector = list(embedder.query_embed([query]))[0]
            results = Index.restore(str(usearch_path)).search(
                np.array(query_vector, dtype=np.float32),
                min(top_k, len(unit_rows)),
            )
            unit_ids = [row[0] for row in unit_rows]
            hits = []
            for index in range(len(results.keys)):
                row_index = int(results.keys[index])
                if row_index < len(unit_ids):
                    unit_id = unit_ids[row_index]
                    row = SemanticUnitByIdentifierQuery(unit_id).execute(connection)
                    if row:
                        hits.append(
                            {
                                "unit_id": unit_id,
                                "distance": float(results.distances[index]),
                                "heading": row[0],
                                "snippet": row[1][:200],
                                "title": row[2],
                                "type": row[3],
                            }
                        )
            return hits
        except Exception:
            return []

    def search_objects(self, connection: duckdb.DuckDBPyConnection, query: str) -> list[dict]:
        rows = ObjectSearchQuery(query).execute(connection)
        return [
            {"id": row[0], "type": row[1], "title": row[2], "description": row[3], "domain": row[4]} for row in rows
        ]

    def expand_graph(self, connection: duckdb.DuckDBPyConnection, object_id: str, hops: int = 2) -> list[dict]:
        _ = hops
        rows = GraphExpansionQuery(object_id).execute(connection)
        return [
            {
                "subject": row[0],
                "predicate": row[1],
                "object": row[2],
                "neighbor_title": row[3],
                "neighbor_type": row[4],
            }
            for row in rows
        ]

    def rrf_fuse(
        self,
        *result_lists: list[dict],
        id_key: str = "unit_id",
        k: int = 60,
        top_n: int = 10,
    ) -> list[dict]:
        scores: dict[str, float] = {}
        items: dict[str, dict] = {}
        for results in result_lists:
            for rank, item in enumerate(results):
                item_id = item.get(id_key, item.get("id", str(rank)))
                scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (k + rank + 1)
                items.setdefault(item_id, item)
        return [items[item_id] for item_id in sorted(scores, key=scores.get, reverse=True)[:top_n] if item_id in items]
