"""Resolves path-style relationship targets to object ids.

OKF records link to each other by path (`/knowledge/concepts/a.md`, `../b.md`, front-matter
`sources`), and a record's id is its explicit front-matter `id` or else a slug of its path.
The resolver maps a path target to the id of the object whose source file it names, so the
graph stage can draw the edge. A target that names no object resolves to None and is dropped.
"""

from __future__ import annotations

import posixpath
from collections.abc import Iterable

from kp_compiler.domain.models import KnowledgeObject

# The authoring tree is published under this URL prefix; it is not part of the source tree.
_URL_PREFIXES = ("knowledge/",)


class PathResolver:
    def __init__(self, objects: Iterable[KnowledgeObject]) -> None:
        self._by_path: dict[str, str] = {}
        self._by_rooted_path: dict[str, str] = {}
        for obj in objects:
            if not obj.id or not obj.source_path:
                continue
            path = obj.source_path.replace("\\", "/")
            self._by_path[path] = obj.id
            _, _, rooted = path.partition("/")  # drop the corpus root directory
            if rooted:
                self._by_rooted_path.setdefault(rooted, obj.id)

    @staticmethod
    def is_path(target: str) -> bool:
        return target.startswith("/") or target.startswith(".") or target.endswith(".md")

    def resolve(self, target: str, from_source_path: str) -> str | None:
        path = target.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")
        if not path.endswith(".md") or "://" in path:
            return None
        if path.startswith("/"):
            return self._absolute(path.lstrip("/"))
        here = posixpath.dirname(from_source_path.replace("\\", "/"))
        return self._by_path.get(posixpath.normpath(posixpath.join(here, path)))

    def _absolute(self, path: str) -> str | None:
        for prefix in _URL_PREFIXES:
            if path.startswith(prefix):
                return self._by_rooted_path.get(path.removeprefix(prefix))
        return self._by_path.get(path) or self._by_rooted_path.get(path)
