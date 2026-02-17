"""
R10 - Bond Requirements Doctrine Blocks
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SPECULATIVE = "speculative"


class IssueCategory(str, Enum):
    BOND_CALCULATION = "bond_calculation"
    BOND_TYPES = "bond_types"
    ALTERNATIVE_SECURITY = "alternative_security"
    OPERATOR_REQUIREMENTS = "operator_requirements"
    BOND_RELEASE = "bond_release"
    BOND_FORFEITURE = "bond_forfeiture"


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
        topic="individual_well_bond_calculation",
        category=IssueCategory.BOND_CALCULATION,
        keywords=["individual bond", "single well", "depth-based", "per well"],
        conclusion_template=[
            "Individual well bonds range from $2,000 to $25,000 based on depth.",
            "Wells 0-2,000 feet require $2,000 bond.",
            "Wells over 10,000 feet require $25,000 bond."
        ],
        reasoning_framework="""
        16 TAC §3.78(a) establishes individual well bond amounts by depth:
        - 0 to 2,000 feet: $2,000
        - 2,001 to 4,000 feet: $4,000
        - 4,001 to 6,000 feet: $6,000
        - 6,001 to 10,000 feet: $10,000
        - Over 10,000 feet: $25,000

        Enhanced bonds required for special circumstances:
        - Bay/estuary wells: 2x base amount
        - H2S wells: 1.5x base amount
        - Injection wells: 2x base amount
        """,
        key_factors=["Well depth", "Well type", "Special designations", "Location"],
        primary_authority=["16 TAC §3.78(a)", "16 TAC §3.78(b)"],
        confidence=ConfidenceLevel.HIGH,
        confidence_stratification="defensible"
    ),

    DoctrineBlock(
        topic="blanket_bond_tiers",
        category=IssueCategory.BOND_CALCULATION,
        keywords=["blanket bond", "multiple wells", "operator bond", "aggregate"],
        conclusion_template=[
            "Blanket bonds cover multiple wells with tiered amounts.",
            "1-10 wells: $25,000 blanket bond minimum.",
            "Over 250 wells: $250,000 plus $2,500 per well over 250."
        ],
        reasoning_framework="""
        16 TAC §3.78(c) blanket bond schedule:
        - 1 to 10 wells: $25,000
        - 11 to 25 wells: $50,000
        - 26 to 100 wells: $125,000
        - 101 to 250 wells: $250,000
        - Over 250 wells: $250,000 + ($2,500 × wells over 250)

        Special wells require additional bond amount.
        Blanket typically more economical for 3+ wells.
        """,
        key_factors=["Total well count", "Special well count", "Cost comparison to individual"],
        primary_authority=["16 TAC §3.78(c)"],
        confidence=ConfidenceLevel.HIGH,
        confidence_stratification="defensible"
    ),

    DoctrineBlock(
        topic="letter_of_credit_alternative",
        category=IssueCategory.ALTERNATIVE_SECURITY,
        keywords=["letter of credit", "LOC", "bank guarantee", "alternative security"],
        conclusion_template=[
            "Letter of credit acceptable alternative to surety bond.",
            "Must be from Texas-licensed or federally-insured institution.",
            "Same amount as equivalent surety bond."
        ],
        reasoning_framework="""
        16 TAC §3.78(f) allows letters of credit as alternative financial security.
        Requirements:
        - Issued by Texas-licensed bank or federally-insured institution
        - Irrevocable letter of credit
        - Payable to Railroad Commission
        - Amount equal to required bond
        - Annual renewal required

        Advantages: No premium payments, better for large operators
        Disadvantages: Ties up credit capacity, annual renewal burden
        """,
        key_factors=["Issuing bank qualifications", "Amount adequacy", "Renewal provisions"],
        primary_authority=["16 TAC §3.78(f)"],
        confidence=ConfidenceLevel.HIGH,
        confidence_stratification="defensible"
    ),

    # Additional doctrine blocks for bonds...
]
