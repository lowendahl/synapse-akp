"""Corpus scanner for ontology discovery."""

from __future__ import annotations

import re
from pathlib import Path

from kp_compiler.stages.ontology_discovery_models import DiscoveredPredicate, DiscoveredType, OntologyDiscoveryResult


class OntologyScanner:
    """Scans corpus frontmatter to discover ontology structure."""

    _CANONICAL_TYPE: dict[str, str] = {
        "Framework": "Framework",
        "MCEM Stage": "Stage",
        "Stage": "Stage",
        "Methodology": "Methodology",
        "Strategy": "Strategy",
        "Organization": "Organization",
        "Operating Model": "Organization",
        "Role": "Role",
        "Process": "Process",
        "Metric": "Metric",
        "Metric Collection": "Metric",
        "KPI": "KPI",
        "Doctrine": "Doctrine",
        "Program": "Program",
        "Outcome Framework": "Outcome",
        "Outcome": "Outcome",
        "Evidence Source": "Evidence_Source",
        "Evidence Map": "Evidence_Map",
        "Risk Indicator": "Risk",
        "Risk Signal": "Risk",
        "Risk": "Risk",
        "Priority": "Priority",
        "Planning Artifact": "Planning",
        "Planning": "Planning",
        "Taxonomy": "Taxonomy",
        "Pipeline Object": "Pipeline",
        "Pipeline": "Pipeline",
        "Governance": "Governance",
        "GTM": "GTM",
        "Contract": "Contract",
        "Delivery": "Delivery",
        "Measurement": "Measurement",
        "Measurement Concept": "Measurement",
        "ADR": "ADR",
        "Index": "Index",
        "Log": "Log",
    }

    def discover(self, source_files: list[Path], source_root: Path) -> OntologyDiscoveryResult:
        result = OntologyDiscoveryResult(source_count=len(source_files))
        for file_path in source_files:
            frontmatter = self._read_frontmatter(file_path)
            if not frontmatter:
                continue
            relative_path = str(file_path.relative_to(source_root.parent)).replace("\\", "/")
            domain = self._infer_domain(relative_path)
            result.domains.add(domain)
            object_type = self._record_type(frontmatter, domain, result)
            self._record_id_prefix(frontmatter, result)
            self._record_predicates(frontmatter, object_type, result)
        return result

    def _read_frontmatter(self, file_path: Path) -> dict:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return {}
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return {}
        try:
            from ruamel.yaml import YAML

            return YAML(typ="safe").load(match.group(1)) or {}
        except Exception:
            return {}

    def _infer_domain(self, file_path: str) -> str:
        normalized = file_path.replace("\\", "/")
        if "/mcem/" in normalized or normalized.startswith("mcem/"):
            return "mcem"
        if "/csu/" in normalized or normalized.startswith("csu/"):
            return "csu"
        return "unknown"

    def _record_type(self, frontmatter: dict, domain: str, result: OntologyDiscoveryResult) -> str:
        raw_type = frontmatter.get("type", "")
        if not raw_type:
            return ""
        object_type = self._CANONICAL_TYPE.get(raw_type, raw_type)
        discovered = result.types.setdefault(object_type, DiscoveredType(name=object_type))
        discovered.observed_count += 1
        discovered.domains.add(domain)
        discovered.observed_fields.update(frontmatter.keys())
        return object_type

    def _record_id_prefix(self, frontmatter: dict, result: OntologyDiscoveryResult) -> None:
        object_id = frontmatter.get("id", "")
        if object_id and "." in object_id:
            result.id_prefixes.add(object_id.rsplit(".", 1)[0].split(".")[0])

    def _record_predicates(self, frontmatter: dict, object_type: str, result: OntologyDiscoveryResult) -> None:
        relationships = frontmatter.get("relationships", [])
        if not isinstance(relationships, list):
            return
        for relationship in relationships:
            if not isinstance(relationship, dict):
                continue
            predicate = relationship.get("predicate", "")
            if not predicate:
                continue
            discovered = result.predicates.setdefault(predicate, DiscoveredPredicate(name=predicate))
            discovered.observed_count += 1
            if object_type:
                discovered.subject_types.add(object_type)
            target_id = relationship.get("object_id", "")
            if target_id and "." in target_id:
                parts = target_id.split(".")
                if len(parts) >= 2:
                    discovered.object_types.add(parts[1].replace("_", " ").title())
