"""Models and constants for enrichment."""

from __future__ import annotations

from dataclasses import dataclass, field

from kp_compiler.contracts.protocols import Diagnostic
from kp_compiler.domain.models import KnowledgeObject


@dataclass
class EnrichmentResult:
    objects: list[KnowledgeObject] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    aliases_added: int = 0
    entities_found: int = 0
    acronyms_resolved: int = 0


class KnownAcronymCatalog:
    """Known acronym expansions used during enrichment."""

    VALUES: dict[str, str] = {
        "C2C": "Commit to Complete",
        "UDC": "Unified Delivery Coverage",
        "UCR": "Unified Consumed Revenue",
        "NNR": "Net New Revenue",
        "IQC": "In-Quarter Create",
        "ECIF": "Enterprise Customer Investment Fund",
        "CSP": "Customer Success Plan",
        "CSA": "Customer Success Architect",
        "CSAM": "Customer Success Account Manager",
        "MCEM": "Microsoft Customer Engagement Methodology",
        "MACC": "Microsoft Azure Consumption Commitment",
        "ACR": "Azure Consumed Revenue",
        "ATU": "Account Technology Unit",
        "STU": "Specialist Technology Unit",
        "CSU": "Customer Success Unit",
        "DSAT": "Customer Dissatisfaction",
        "MAU": "Monthly Active Users",
        "PAU": "Productive Active Users",
        "PRU": "Productive Recurring User",
        "PCI": "Pipeline Coverage Index",
        "FRA": "Forecast Recommendation",
        "AIRF": "AI Revenue Forecast",
        "QBR": "Quarterly Business Review",
        "CSDR": "Customer Success Delivery Review",
        "ICP": "Integrated Customer Planning",
        "TMM": "Technical Maturity Model",
        "MDM": "Master Data Management",
        "GRM": "Global Resource Management",
        "MSXi": "MSX Insights",
        "CMF": "Cloud Migration Factory",
        "MIRP": "Microsoft Internal Revenue Plan",
        "ESA": "Enterprise Skills Assessment",
        "SES": "Success Enablement Services",
        "UFP": "Unified for Partners",
        "EDE": "Enhanced Delivery Engagements",
        "STA": "Strategic Technical Assessments",
        "OKF": "Open Knowledge Format",
    }
