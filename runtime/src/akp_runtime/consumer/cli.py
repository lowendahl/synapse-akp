"""AKP CLI — user-facing commands for managing knowledge packs.

Commands:
  akp install <source>   Download and register a knowledge pack
  akp list               Show installed packs
  akp refresh [pack_id]  Refresh packs to latest version
  akp remove <pack_id>   Uninstall a pack
  akp serve              Start the MCP server
  akp info <pack_id>     Show pack manifest details
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from akp_runtime.consumer.pack_manager import PackManager


class AkpCommandLineInterface:
    """Entry point for the `akp` CLI tool."""

    def __init__(self) -> None:
        self._parser = self._build_parser()

    def run(self) -> None:
        """Parse arguments and dispatch to the appropriate command."""
        args = self._parser.parse_args()

        if args.command is None:
            self._parser.print_help()
            sys.exit(0)

        manager = PackManager()

        if args.command == "install":
            manager.install(args.source)
        elif args.command == "list":
            manager.list_packs()
        elif args.command == "refresh":
            manager.update(args.pack_id)
        elif args.command == "remove":
            manager.remove(args.pack_id)
        elif args.command == "serve":
            self._serve(args)
        elif args.command == "info":
            manager.info(args.pack_id)

    def _build_parser(self) -> argparse.ArgumentParser:
        """Build the argument parser with all subcommands."""
        parser = argparse.ArgumentParser(
            prog="akp",
            description="Agentic Knowledge Pack runtime — install, manage, and serve knowledge packs",
        )
        subparsers = parser.add_subparsers(dest="command")

        install_parser = subparsers.add_parser("install", help="Install a knowledge pack")
        install_parser.add_argument("source", help="Pack source: org/repo/pack_id or path to .akp file")

        subparsers.add_parser("list", help="List installed knowledge packs")

        refresh_parser = subparsers.add_parser("refresh", help="Refresh packs to latest version")
        refresh_parser.add_argument("pack_id", nargs="?", help="Specific pack to refresh (default: all)")

        remove_parser = subparsers.add_parser("remove", help="Remove an installed pack")
        remove_parser.add_argument("pack_id", help="Pack ID to remove")

        serve_parser = subparsers.add_parser("serve", help="Start the MCP server")
        serve_parser.add_argument("--config", type=Path, help="Path to config.yaml")
        serve_parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])

        info_parser = subparsers.add_parser("info", help="Show pack details")
        info_parser.add_argument("pack_id", help="Pack ID to inspect")

        return parser

    def _serve(self, args: argparse.Namespace) -> None:
        """Start the MCP server."""
        import logging

        from akp_runtime.consumer.mcp_server import _create_server

        logging.basicConfig(
            level=getattr(logging, args.log_level),
            format='{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
            stream=sys.stderr,
        )
        server = _create_server(config_path=args.config)
        server.run(transport="stdio")


def main() -> None:
    """Run the AKP CLI."""
    AkpCommandLineInterface().run()
