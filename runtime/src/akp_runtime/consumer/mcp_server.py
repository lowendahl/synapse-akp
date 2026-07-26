"""MCP server entry point — stdio transport for Knowledge Pack retrieval.

This is the consumer-facing surface. It delegates to operations via the
composition root established in pipeline/bootstrap.py.
"""

from __future__ import annotations


def main() -> None:
    """Parse --config, bootstrap runtime, run MCP stdio server."""
    raise NotImplementedError("PBI #11")
