"""Cross-Pack Validation Stage — validates references across pack boundaries.

What: Checks that qualified IDs referencing another pack resolve against its manifest.
Why: Enforces acyclic dependency model (ADR-005, ADR-006).
Contracts: Receives objects + dependency manifest. Produces diagnostics.
Boundaries: Must NOT modify objects. Read-only validation.
Test strategy: Unit tests with mock manifests; verify broken ref detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from kp_compiler.contracts.protocols import Diagnostic, Severity
from kp_compiler.domain.models import KnowledgeObject


@dataclass
class CrossPackResult:
    """Output of cross-pack validation."""

    diagnostics: list[Diagnostic] = field(default_factory=list)
    refs_checked: int = 0
    refs_resolved: int = 0
    refs_broken: int = 0
    cross_refs: list[tuple[str, str, str, str]] = field(default_factory=list)


def load_dependency_manifest(pack_path: Path) -> set[str]:
    """Load the set of object IDs from a dependency pack's manifest."""
    import duckdb

    if not pack_path.exists():
        return set()

    con = duckdb.connect(str(pack_path), read_only=True)
    try:
        rows = con.execute("SELECT id FROM objects").fetchall()
        return {row[0] for row in rows}
    finally:
        con.close()


def _detect_dependency_domain(dependency_pack: Path) -> str | None:
    """Infer the domain prefix from a dependency pack's object IDs."""
    import duckdb

    con = duckdb.connect(str(dependency_pack), read_only=True)
    try:
        row = con.execute("SELECT id FROM objects LIMIT 1").fetchone()
        if row and "." in row[0]:
            return row[0].split(".")[0]
        return None
    finally:
        con.close()


def validate_cross_pack_refs(
    objects: list[KnowledgeObject],
    dependency_ids: set[str] | None = None,
    dependency_domain: str = "",
    pack_id: str = "",
) -> CrossPackResult:
    """Validate that cross-pack references resolve against the dependency manifest.

    Cross-pack refs are relationships whose target domain differs from this
    pack's own domain.  The own-domain is derived from pack_id (e.g. 'kp-csu'
    → 'csu').  Intra-pack refs are skipped — they're validated by the graph
    stage instead.
    """
    result = CrossPackResult()

    # Derive own domain from pack_id (strip 'kp-' prefix)
    own_domain = pack_id.removeprefix("kp-") if pack_id else ""

    dep_ids = dependency_ids or set()
    dep_domain = dependency_domain

    for obj in objects:
        if not obj.id:
            continue

        for rel in obj.relationships:
            target = rel.object_id

            # Skip file-path refs (e.g. /mcem/stages/1-listen.md) —
            # these are markdown links, not qualified OKF IDs
            if target.startswith("/") or target.endswith(".md"):
                continue

            # Determine the domain of the target
            target_domain = target.split(".")[0] if "." in target else ""

            # Skip intra-pack refs (same domain) — validated by graph stage
            if own_domain and target_domain == own_domain:
                continue

            # This is a cross-pack ref
            result.refs_checked += 1
            result.cross_refs.append((obj.id, target, target_domain, rel.predicate))

            if dep_ids:
                if target in dep_ids:
                    result.refs_resolved += 1
                else:
                    result.refs_broken += 1
                    result.diagnostics.append(Diagnostic(
                        severity=Severity.ERROR,
                        source_file=obj.source_path,
                        message=(
                            f"Broken cross-pack ref: '{target}' not found "
                            f"in dependency pack ({dep_domain or 'unknown'})"
                        ),
                        stage="cross_pack",
                        object_id=obj.id,
                    ))

    return result
