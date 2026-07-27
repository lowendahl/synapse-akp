"""Shared fixtures for gold standard integration tests.

These tests run against REAL compiled packs in dist/.
They validate end-to-end resolution, explain output, and data quality.
Skip gracefully if packs are not compiled.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from akp_runtime.infrastructure.duckdb_loader import DuckDBLoadedPack
from akp_runtime.operations.explain_concept import ExplainConceptOperation

DIST_DIR = Path(__file__).resolve().parents[4] / "dist"
CSU_PACK_PATH = DIST_DIR / "csu.duckdb"
MCEM_PACK_PATH = DIST_DIR / "mcem.duckdb"


@pytest.fixture(scope="module")
def csu_pack() -> DuckDBLoadedPack:
    """Real CSU pack — skips if not compiled."""
    if not CSU_PACK_PATH.exists():
        pytest.skip("CSU pack not compiled (run compiler first)")
    pack = DuckDBLoadedPack(CSU_PACK_PATH)
    yield pack
    pack.close()


@pytest.fixture(scope="module")
def mcem_pack() -> DuckDBLoadedPack:
    """Real MCEM pack — skips if not compiled."""
    if not MCEM_PACK_PATH.exists():
        pytest.skip("MCEM pack not compiled (run compiler first)")
    pack = DuckDBLoadedPack(MCEM_PACK_PATH)
    yield pack
    pack.close()


@pytest.fixture(scope="module")
def csu_explain(csu_pack: DuckDBLoadedPack) -> ExplainConceptOperation:
    """Explain operation against real CSU pack (no LLM)."""
    return ExplainConceptOperation(pack=csu_pack, reasoning_client=None)


@pytest.fixture(scope="module")
def mcem_explain(mcem_pack: DuckDBLoadedPack) -> ExplainConceptOperation:
    """Explain operation against real MCEM pack (no LLM)."""
    return ExplainConceptOperation(pack=mcem_pack, reasoning_client=None)
