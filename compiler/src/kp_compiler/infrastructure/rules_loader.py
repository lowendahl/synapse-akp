"""Rules Loader — reads pack-rules.yaml and returns a typed PackRules instance.

What: YAML → Pydantic deserialization for the rules engine.
Why: Single IO boundary for rules loading (DIP / ADR-014).
Contracts: Returns PackRules (domain model). Raises on invalid YAML.
Boundaries: Infrastructure — performs filesystem IO, imports domain models.
Test strategy: Unit tests with valid/invalid YAML fixtures.
"""

from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML

from kp_compiler.domain.rules import PackRules


def load_pack_rules(path: Path) -> PackRules:
    """Load and validate pack-rules.yaml.

    Returns PackRules with defaults for any omitted field.
    If the file does not exist, returns PackRules.default().
    """
    if not path.exists():
        return PackRules.default()

    yaml = YAML(typ="safe")
    with open(path, encoding="utf-8") as f:
        data = yaml.load(f)

    if data is None:
        return PackRules.default()

    return PackRules.model_validate(data)
