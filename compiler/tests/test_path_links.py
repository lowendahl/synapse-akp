"""Authored path links become graph edges with the right subject and target."""

from kp_compiler.domain.models import KnowledgeObject
from kp_compiler.stages.graph import build_graph
from kp_compiler.stages.parse import parse_source


def _objects(files: dict[str, str]) -> list[KnowledgeObject]:
    return [parse_source(content, path) for path, content in files.items()]


def _edges(files: dict[str, str]) -> set[tuple[str, str, str]]:
    return {(e.subject_id, e.predicate, e.object_id) for e in build_graph(_objects(files)).edges}


def test_record_without_id_gets_its_own_id_as_subject() -> None:
    obj = parse_source("---\ntitle: A\n---\nSee [b](/knowledge/b.md).\n", "lib/a.md")
    assert obj.id == "lib-a"
    assert {r.subject_id for r in obj.relationships} == {"lib-a"}


def test_knowledge_path_link_resolves_to_path_derived_id() -> None:
    edges = _edges(
        {
            "lib/concepts/a.md": "---\ntitle: A\n---\nSee [b](/knowledge/syntheses/b.md).\n",
            "lib/syntheses/b.md": "---\ntitle: B\n---\nBody.\n",
        }
    )
    assert ("lib-concepts-a", "references", "lib-syntheses-b") in edges


def test_relative_link_resolves_against_the_source_directory() -> None:
    edges = _edges(
        {
            "lib/concepts/a.md": "---\ntitle: A\n---\nSee [b](../syntheses/b.md#part).\n",
            "lib/syntheses/b.md": "---\ntitle: B\n---\nBody.\n",
        }
    )
    assert ("lib-concepts-a", "references", "lib-syntheses-b") in edges


def test_frontmatter_source_resource_becomes_a_reference() -> None:
    a = (
        "---\ntitle: A\nsources:\n  - id: s\n    resource: /knowledge/sources/s.md\n"
        "  - /knowledge/sources/t.md\n---\nBody.\n"
    )
    edges = _edges(
        {
            "lib/concepts/a.md": a,
            "lib/sources/s.md": "---\ntitle: S\n---\nx\n",
            "lib/sources/t.md": "---\ntitle: T\n---\nx\n",
        }
    )
    assert ("lib-concepts-a", "references", "lib-sources-s") in edges
    assert ("lib-concepts-a", "references", "lib-sources-t") in edges


def test_explicit_id_is_the_target_of_a_path_link() -> None:
    edges = _edges(
        {
            "lib/a.md": "---\ntitle: A\n---\nSee [b](/knowledge/b.md).\n",
            "lib/b.md": "---\nid: custom.b\ntitle: B\n---\nBody.\n",
        }
    )
    assert ("lib-a", "references", "custom.b") in edges


def test_unresolvable_and_external_links_are_dropped() -> None:
    edges = _edges({"lib/a.md": "---\ntitle: A\n---\n[x](/knowledge/missing.md) [y](https://e.com/p.md)\n"})
    assert edges == set()
