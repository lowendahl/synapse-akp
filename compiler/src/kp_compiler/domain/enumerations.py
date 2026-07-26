"""Domain enumerations — typed vocabularies for the compiler IR."""

from __future__ import annotations

from enum import Enum


class ObjectType(str, Enum):
    """Allowed object types per ontology.yaml."""

    FRAMEWORK = "Framework"
    STAGE = "Stage"
    METHODOLOGY = "Methodology"
    STRATEGY = "Strategy"
    ORGANIZATION = "Organization"
    ROLE = "Role"
    PROCESS = "Process"
    METRIC = "Metric"
    KPI = "KPI"
    DOCTRINE = "Doctrine"
    PROGRAM = "Program"
    OUTCOME = "Outcome"
    EVIDENCE_SOURCE = "Evidence Source"
    EVIDENCE_MAP = "Evidence Map"
    RISK = "Risk"
    PRIORITY = "Priority"
    PLANNING = "Planning"
    TAXONOMY = "Taxonomy"
    PIPELINE = "Pipeline"
    GOVERNANCE = "Governance"
    GTM = "GTM"
    CONTRACT = "Contract"
    DELIVERY = "Delivery"
    MEASUREMENT = "Measurement"
    ADR = "ADR"
    INDEX = "Index"
    LOG = "Log"


class Origin(str, Enum):
    """How a relationship or object was created."""

    AUTHORED = "authored"
    DERIVED = "derived"
    INFERRED = "inferred"
    GENERATED = "generated"


class MeasurementParadigm(str, Enum):
    """How a metric is measured."""

    SNAPSHOT = "snapshot"
    REALTIME = "realtime"


class Classification(str, Enum):
    """KPI classification."""

    LEADING = "leading"
    LAGGING = "lagging"
    DIAGNOSTIC = "diagnostic"
