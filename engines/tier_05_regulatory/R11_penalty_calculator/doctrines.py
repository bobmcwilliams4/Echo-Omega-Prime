"""R11 - Penalty Calculator Doctrine Blocks"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SPECULATIVE = "speculative"


class IssueCategory(str, Enum):
    PENALTY_CALCULATION = "penalty_calculation"
    MITIGATION = "mitigation"
    ENFORCEMENT = "enforcement"


@dataclass
class DoctrineBlock:
    topic: str
    category: IssueCategory
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: Optional[str] = None


DOCTRINE_BLOCKS = [
    DoctrineBlock(
        topic="rrc_penalty_guidelines",
        category=IssueCategory.PENALTY_CALCULATION,
        keywords=["penalty", "administrative penalty", "violation", "enforcement"],
        conclusion_template=["RRC may assess up to $10,000 per day per violation."],
        reasoning_framework="16 TAC §3.107 establishes penalty framework with base amounts adjusted for gravity, history, cooperation.",
        key_factors=["Violation type", "Duration", "Prior violations", "Environmental harm"],
        primary_authority=["16 TAC §3.107", "Texas Natural Resources Code §85.321"],
        confidence=ConfidenceLevel.HIGH,
        confidence_stratification="defensible"
    ),
]
