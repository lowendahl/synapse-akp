"""Consumer package — CLI tool for querying a compiled Knowledge Pack."""

from kp_compiler.consumer.cli import (
    KnowledgePackFindCommand,
    main,
    search_aliases,
    search_bm25,
    search_objects,
    search_semantic,
)
from kp_compiler.consumer.explorer import KnowledgePackExplorer, build_graph_json, extract_pack_data, get_html_template

__all__ = [
    "KnowledgePackFindCommand",
    "KnowledgePackExplorer",
    "build_graph_json",
    "extract_pack_data",
    "get_html_template",
    "main",
    "search_aliases",
    "search_bm25",
    "search_objects",
    "search_semantic",
]
