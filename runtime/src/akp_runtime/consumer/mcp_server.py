"""MCP server entry point — stdio transport for Knowledge Pack retrieval.

This is the consumer-facing surface. It delegates to operations via the
composition root established in pipeline/bootstrap.py.
"""

from __future__ import annotations


class McpServerApplication:
    """Runtime consumer entry-point wrapper."""

    def run(self) -> None:
        """Parse --config, bootstrap runtime, run MCP stdio server."""
        raise NotImplementedError("PBI #11")


def main() -> None:
    """Run the MCP server application."""
    McpServerApplication().run()
