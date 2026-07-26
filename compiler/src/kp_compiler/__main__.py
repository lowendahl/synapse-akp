"""Unified CLI entry point for Knowledge Pack tools.

Usage:
    kp compile okf/csu --ontology okf/ontology.yaml --output dist/kp-csu.duckdb --pack-id kp-csu
    kp find "UDC" --pack dist/kp-csu.duckdb
    kp find "milestone and Job1" --pack dist/kp-csu.duckdb --semantic
"""

from __future__ import annotations

import sys


def main() -> None:
    """Dispatch to compile or find subcommand."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Knowledge Pack CLI")
        print()
        print("Usage:")
        print("  kp compile <source> [options]   Compile OKF sources into a Knowledge Pack")
        print("  kp find <query> [options]        Search a compiled Knowledge Pack")
        print()
        print("Run 'kp compile --help' or 'kp find --help' for subcommand options.")
        sys.exit(0)

    subcommand = sys.argv[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]  # strip subcommand from argv

    if subcommand == "compile":
        from kp_compiler.cli import main as compile_main
        compile_main()
    elif subcommand == "find":
        from kp_compiler.consumer.cli import main as find_main
        find_main()
    else:
        print(f"Unknown subcommand: '{subcommand}'. Use 'compile' or 'find'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
