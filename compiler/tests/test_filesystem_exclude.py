"""FilesystemReader.discover honors pack.yaml `exclude` globs.

A single OKF source tree can serve several projections (e.g. a website snapshot and this
pack), so the compiler must be able to skip subtrees it should not compile (assets, graph
yaml, disclosure sidecars) without maintaining a separate source copy.
"""

from __future__ import annotations

from pathlib import Path

from kp_compiler.infrastructure.filesystem import FilesystemReader


def _tree(root: Path) -> None:
    for rel in (
        "concepts/a.md",
        "concepts/b.md",
        "frontier-firm/c.md",
        "assets/keep-out.md",
        "assets/market-research/deep.md",
        "graph/notes.md",
        "disclosure/sidecars/x.md",
        "drafts/scratch.draft.md",
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# doc\n", encoding="utf-8")


def _rels(root: Path, paths: list[Path]) -> set[str]:
    return {p.relative_to(root).as_posix() for p in paths}


def test_discover_without_exclude_returns_everything(tmp_path: Path) -> None:
    _tree(tmp_path)
    found = _rels(tmp_path, FilesystemReader().discover(tmp_path))
    assert "assets/keep-out.md" in found
    assert "graph/notes.md" in found
    assert len(found) == 8


def test_subtree_globs_exclude_whole_directories(tmp_path: Path) -> None:
    _tree(tmp_path)
    found = _rels(
        tmp_path,
        FilesystemReader().discover(tmp_path, ["assets/**", "graph/**", "disclosure/**"]),
    )
    assert found == {
        "concepts/a.md",
        "concepts/b.md",
        "frontier-firm/c.md",
        "drafts/scratch.draft.md",
    }


def test_fnmatch_pattern_excludes_matching_files(tmp_path: Path) -> None:
    _tree(tmp_path)
    found = _rels(tmp_path, FilesystemReader().discover(tmp_path, ["**/*.draft.md"]))
    assert "drafts/scratch.draft.md" not in found
    assert "concepts/a.md" in found


def test_blank_patterns_are_ignored(tmp_path: Path) -> None:
    _tree(tmp_path)
    found = _rels(tmp_path, FilesystemReader().discover(tmp_path, ["", "  ", "assets/**"]))
    assert "assets/keep-out.md" not in found
    assert "assets/market-research/deep.md" not in found
    assert "concepts/a.md" in found
