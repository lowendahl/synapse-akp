"""Graph Stage — NetworkX graph construction, validation, and scoring.

What: Builds a directed property graph from KnowledgeObjects and runs graph algorithms.
Why: Enables structural validation (orphans, cycles) and pre-computed metrics (PageRank).
Contracts: Receives list[KnowledgeObject]. Produces GraphResult (nodes, edges, diagnostics, metrics).
Boundaries: Must NOT perform IO or write to DuckDB. NetworkX is a domain library here.
Test strategy: Unit tests with small object lists; verify graph properties.
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


def build_graph(objects: list[KnowledgeObject]) -> GraphResult:
    """Build NetworkX DiGraph from objects and run validation + scoring."""
    G = nx.DiGraph()
    diagnostics: list[Diagnostic] = []

    # Add nodes
    for obj in objects:
        if not obj.id:
            continue
        G.add_node(
            obj.id,
            type=obj.type.value,
            title=obj.title,
            domain=obj.domain,
            source_path=obj.source_path,
        )

    # Add edges from relationships
    for obj in objects:
        if not obj.id:
            continue
        for rel in obj.relationships:
            if rel.object_id and rel.object_id.startswith("/"):
                # Skip path-based refs for now (will be resolved to IDs later)
                continue
            if rel.object_id and rel.object_id in G.nodes:
                G.add_edge(
                    rel.subject_id,
                    rel.object_id,
                    predicate=rel.predicate,
                    origin=rel.origin.value,
                    confidence=rel.confidence,
                )

    # ── Validation ──────────────────────────────────────────────────────────

    # Orphan detection
    orphans = list(nx.isolates(G))
    for orphan_id in orphans:
        node_data = G.nodes[orphan_id]
        # Index and Log types are expected to be orphans
        if node_data.get("type") not in ("Index", "Log"):
            diagnostics.append(Diagnostic(
                severity=Severity.WARNING,
                source_file=node_data.get("source_path", ""),
                message=f"Orphan node — no incoming or outgoing edges",
                stage="graph",
                object_id=orphan_id,
            ))

    # Cycle detection (on depends_on edges only)
    depends_subgraph = nx.DiGraph()
    for u, v, data in G.edges(data=True):
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

    # Connected components
    undirected = G.to_undirected()
    components = list(nx.connected_components(undirected))
    if len(components) > 2:  # Expect at most 2 (mcem + csu domains)
        diagnostics.append(Diagnostic(
            severity=Severity.INFO,
            source_file="",
            message=f"Graph has {len(components)} disconnected components",
            stage="graph",
        ))

    # ── Scoring ─────────────────────────────────────────────────────────────

    pagerank = nx.pagerank(G) if len(G.nodes) > 0 else {}
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())

    # ── Export ──────────────────────────────────────────────────────────────

    nodes: list[GraphNode] = []
    for node_id, data in G.nodes(data=True):
        nodes.append(GraphNode(
            id=node_id,
            type=data.get("type", ""),
            title=data.get("title", ""),
            domain=data.get("domain", ""),
            source_path=data.get("source_path", ""),
            pagerank=pagerank.get(node_id, 0.0),
            in_degree=in_degree.get(node_id, 0),
            out_degree=out_degree.get(node_id, 0),
        ))

    edges: list[GraphEdge] = []
    for u, v, data in G.edges(data=True):
        edges.append(GraphEdge(
            subject_id=u,
            object_id=v,
            predicate=data.get("predicate", "references"),
            origin=data.get("origin", "authored"),
            confidence=data.get("confidence"),
        ))

    metrics = {
        "node_count": len(G.nodes),
        "edge_count": len(G.edges),
        "orphan_count": len(orphans),
        "cycle_count": len(cycles),
        "component_count": len(components),
    }

    return GraphResult(
        nodes=nodes,
        edges=edges,
        diagnostics=diagnostics,
        metrics=metrics,
    )
