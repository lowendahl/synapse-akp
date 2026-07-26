"""Tests for the AKP runtime exception hierarchy."""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from akp_runtime.contracts.errors import (
    ConfigurationError,
    DuplicatePackId,
    MissingManifestKey,
    MissingPackTable,
    ObjectNotFound,
    PackNotLoaded,
    PackOpenError,
    ProvenanceNotFound,
    RuntimeBaseError,
    UnsupportedSchemaVersion,
    VectorIndexMissing,
)

SAFE_TEXT = st.text(alphabet=st.characters(blacklist_characters="\x00"), max_size=30)


def _to_path(value: str) -> Path:
    return Path(value or "pack.duckdb")


SAFE_PATH = SAFE_TEXT.map(_to_path)


# Invariant: every concrete runtime exception must derive from RuntimeBaseError.
@pytest.mark.parametrize(
    "error_type",
    (
        ConfigurationError,
        PackOpenError,
        UnsupportedSchemaVersion,
        MissingPackTable,
        MissingManifestKey,
        DuplicatePackId,
        PackNotLoaded,
        VectorIndexMissing,
        ObjectNotFound,
        ProvenanceNotFound,
    ),
)
def test_concrete_errors_subclass_runtime_base_error(error_type: type[RuntimeBaseError]) -> None:
    assert issubclass(error_type, RuntimeBaseError)


# Invariant: error strings are deterministic and preserve structured context.
@pytest.mark.parametrize(
    ("error", "expected"),
    (
        (ConfigurationError(source="env", violation="missing value"), "[env] missing value"),
        (
            PackOpenError(pack_path=Path("pack.duckdb"), detail="permission denied"),
            "Cannot open pack 'pack.duckdb': permission denied",
        ),
        (
            UnsupportedSchemaVersion(pack_path=Path("pack.duckdb"), found="3.0.0"),
            "[pack.duckdb] schema_version=3.0.0; expected major 2.x",
        ),
        (
            MissingPackTable(pack_path=Path("pack.duckdb"), table_name="objects"),
            "[pack.duckdb] missing required table 'objects'",
        ),
        (
            MissingManifestKey(pack_path=Path("pack.duckdb"), key="pack_id"),
            "[pack.duckdb] manifest missing key 'pack_id'",
        ),
        (
            DuplicatePackId(pack_id="dup.pack", paths=[Path("a.duckdb"), Path("b.duckdb")]),
            "Duplicate pack_id 'dup.pack': a.duckdb, b.duckdb",
        ),
        (
            PackNotLoaded(pack_id="missing.pack", loaded_pack_ids=["a", "b"]),
            "Pack 'missing.pack' not loaded. Available: a, b",
        ),
        (
            VectorIndexMissing(pack_id="pack", expected_path=Path("pack.usearch")),
            "Pack 'pack' is missing vector sidecar 'pack.usearch'",
        ),
        (
            ObjectNotFound(identifier="csu.metric.c2c", searched_packs=["pack-a", "pack-b"]),
            "Object 'csu.metric.c2c' not found in packs: pack-a, pack-b",
        ),
        (
            ProvenanceNotFound(target_type="object", target_id="csu.metric.c2c"),
            "No provenance found for object 'csu.metric.c2c'",
        ),
    ),
)
def test_error_stringification_is_deterministic(error: RuntimeBaseError, expected: str) -> None:
    assert str(error) == expected
    assert str(error) == expected


# Invariant: mutable default fields must not be shared between exception instances.
def test_error_default_lists_are_isolated_between_instances() -> None:
    duplicate_a = DuplicatePackId(pack_id="dup")
    duplicate_b = DuplicatePackId(pack_id="dup")
    duplicate_a.paths.append(Path("a.duckdb"))

    pack_a = PackNotLoaded(pack_id="missing")
    pack_b = PackNotLoaded(pack_id="missing")
    pack_a.loaded_pack_ids.append("pack-a")

    object_a = ObjectNotFound(identifier="obj")
    object_b = ObjectNotFound(identifier="obj")
    object_a.searched_packs.append("pack-a")

    assert duplicate_b.paths == []
    assert pack_b.loaded_pack_ids == []
    assert object_b.searched_packs == []


# Invariant: callers can catch any runtime failure via RuntimeBaseError.
def test_runtime_errors_are_catchable_via_base_type() -> None:
    with pytest.raises(RuntimeBaseError):
        raise PackOpenError(pack_path=Path("pack.duckdb"), detail="boom")


# Invariant: empty, unicode, and special-character fields must still stringify safely.
@pytest.mark.parametrize(
    "text_value",
    ("", "Δelta", "quote'\"<>\nline-two", "emoji-✅"),
)
def test_error_strings_handle_edge_case_text_values(text_value: str) -> None:
    error = ConfigurationError(source=text_value, violation=text_value)
    rendered = str(error)

    assert rendered.startswith("[")
    assert "]" in rendered
    assert isinstance(rendered, str)


# Invariant: arbitrary field values must never crash __str__ across the full hierarchy.
@given(text=SAFE_TEXT, other=SAFE_TEXT, path=SAFE_PATH, items=st.lists(SAFE_TEXT, max_size=4))
def test_error_stringification_never_crashes(
    text: str,
    other: str,
    path: Path,
    items: list[str],
) -> None:
    errors: tuple[RuntimeBaseError, ...] = (
        ConfigurationError(source=text, violation=other),
        PackOpenError(pack_path=path, detail=other),
        UnsupportedSchemaVersion(pack_path=path, found=text or "0.0.0"),
        MissingPackTable(pack_path=path, table_name=text),
        MissingManifestKey(pack_path=path, key=text),
        DuplicatePackId(pack_id=text, paths=[_to_path(item) for item in items]),
        PackNotLoaded(pack_id=text, loaded_pack_ids=items),
        VectorIndexMissing(pack_id=text, expected_path=path),
        ObjectNotFound(identifier=text, searched_packs=items),
        ProvenanceNotFound(target_type=text, target_id=other),
    )

    for error in errors:
        rendered = str(error)
        assert isinstance(rendered, str)
