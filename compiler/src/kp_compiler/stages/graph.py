"""Graph Stage — NetworkX graph construction, validation, and scoring.

What: Builds a directed property graph from KnowledgeObjects and runs graph algorithms.
Why: Enables structural validation (orphans, cycles) and pre-computed metrics (PageRank).
Contracts: Receives list[KnowledgeObject]. Produces GraphResult (nodes, edges, diagnostics, metrics).
Boundaries: Must NOT perform IO or write to DuckDB. NetworkX is a domain library here.
"""

from __future__ import annotations

import networkx as nx

from kp_compiler.contracts.protocols import (
    Diagnostic,
    GraphEdge,
    GraphNode,
    GraphResult,
    Severity,
)
from kp_compiler.domain.models import KnowledgeObject


class GraphBuilder:
    """Builds and analyzes the knowledge graph from parsed objects."""

    def build(self, objects: list[KnowledgeObject]) -> GraphResult:
        """Build NetworkX DiGraph from objects and run validation + scoring."""
        graph = self._construct_graph(objects)
        diagnostics = self._validate(graph)
        metrics = self._compute_metrics(graph)
        nodes = self._export_nodes(graph, metrics)
        edges = self._export_edges(graph)

        return GraphResult(
            nodes=nodes,
            edges=edges,
            diagnostics=diagnostics,
            metrics={
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges),
                "orphan_count": metrics["orphan_count"],
                "cycle_count": metrics["cycle_count"],
                "component_count": metrics["component_count"],
            },
        )

    def _construct_graph(self, objects: list[KnowledgeObject]) -> nx.DiGraph:
        graph = nx.DiGraph()

        for obj in objects:
            if not obj.id:
                continue
            graph.add_node(
                obj.id,
                type=obj.type.value,
                title=obj.title,
                domain=obj.domain,
                source_path=obj.source_path,
            )

        for obj in objects:
            if not obj.id:
                continue
            for rel in obj.relationships:
                if rel.object_id and rel.object_id.startswith("/"):
                    continue
                if rel.object_id and rel.object_id in graph.nodes:
                    graph.add_edge(
                        rel.subject_id,
                        rel.object_id,
                        predicate=rel.predicate,
                        origin=rel.origin.value,
                        confidence=rel.confidence,
                    )

        return graph

    def _validate(self, graph: nx.DiGraph) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []

        orphans = list(nx.isolates(graph))
        for orphan_id in orphans:
            node_data = graph.nodes[orphan_id]
            if node_data.get("type") not in ("Index", "Log"):
                diagnostics.append(Diagnostic(
                    severity=Severity.WARNING,
                    source_file=node_data.get("source_path", ""),
                    message="Orphan node — no incoming or outgoing edges",
                    stage="graph",
                    object_id=orphan_id,
                ))

        depends_subgraph = nx.DiGraph()
        for u, v, data in graph.edges(data=True):
            if data.get("predicate") == "depends_on":
                depends_subgraph.add_edge(u, v)

        cycles = list(nx.simple_cycles(depends_subgraph))
        for cycle in cycles:
            diagnostics.append(Diagnostic(
                severity=Severity.ERROR,
                source_file="",
                message=f"Cycle in 'depends_on': {' → '.join(cycle)}",
                stage="graph",
            ))

        undirected = graph.to_undirected()
        components = list(nx.connected_components(undirected))
        if len(components) > 2:
            diagnostics.append(Diagnostic(
                severity=Severity.INFO,
                source_file="",
                message=f"Graph has {len(components)} disconnected components",
                stage="graph",
            ))

        return diagnostics

    def _compute_metrics(self, graph: nx.DiGraph) -> dict:
        pagerank = nx.pagerank(graph) if len(graph.nodes) > 0 else {}
        orphans = list(nx.isolates(graph))

        depends_subgraph = nx.DiGraph()
        for u, v, data in graph.edges(data=True):
            if data.get("predicate") == "depends_on":
                depends_subgraph.add_edge(u, v)
        cycles = list(nx.simple_cycles(depends_subgraph))

        undirected = graph.to_undirected()
        components = list(nx.connected_components(undirected))

        return {
            "pagerank": pagerank,
            "in_degree": dict(graph.in_degree()),
            "out_degree": dict(graph.out_degree()),
            "orphan_count": len(orphans),
            "cycle_count": len(cycles),
            "component_count": len(components),
        }

    def _export_nodes(self, graph: nx.DiGraph, metrics: dict) -> list[GraphNode]:
        nodes: list[GraphNode] = []
        for node_id, data in graph.nodes(data=True):
            nodes.append(GraphNode(
                id=node_id,
                type=data.get("type", ""),
                title=data.get("title", ""),
                domain=data.get("domain", ""),
                source_path=data.get("source_path", ""),
                pagerank=metrics["pagerank"].get(node_id, 0.0),
                in_degree=metrics["in_degree"].get(node_id, 0),
                out_degree=metrics["out_degree"].get(node_id, 0),
            ))
        return nodes

    def _export_edges(self, graph: nx.DiGraph) -> list[GraphEdge]:
        edges: list[GraphEdge] = []
        for u, v, data in graph.edges(data=True):
            edges.append(GraphEdge(
                subject_id=u,
                object_id=v,
                predicate=data.get("predicate", "references"),
                origin=data.get("origin", "authored"),
                confidence=data.get("confidence"),
            ))
        return edges


def build_graph(objects: list[KnowledgeObject]) -> GraphResult:
    """Module-level function for backward compatibility."""
    return GraphBuilder().build(objects)
