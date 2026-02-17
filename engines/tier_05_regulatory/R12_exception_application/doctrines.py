"""R12 - Exception Application Doctrine Blocks"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SPECULATIVE = "speculative"


class IssueCategory(str, Enum):
    EXCEPTION_ANALYSIS = "exception_analysis"
    GOOD_CAUSE = "good_cause"
    HEARING_PROCEDURE = "hearing_procedure"


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
        topic="rule_37_exception",
        category=IssueCategory.EXCEPTION_ANALYSIS,
        keywords=["rule 37", "spacing exception", "location exception", "drilling permit"],
        conclusion_template=["Rule 37 exceptions require proof of necessity and no undue injury."],
        reasoning_framework="16 TAC §3.37 allows exceptions to spacing rules upon showing good cause. Applicant must prove exception prevents waste or protects correlative rights without causing undue injury.",
        key_factors=["Field rules", "Offset operator consent", "Engineering justification", "No-injury proof"],
        primary_authority=["16 TAC §3.37"],
        confidence=ConfidenceLevel.MEDIUM,
        confidence_stratification="aggressive"
    ),

    DoctrineBlock(
        topic="rule_38_density_exception",
        category=IssueCategory.EXCEPTION_ANALYSIS,
        keywords=["rule 38", "density", "additional wells", "field density"],
        conclusion_template=["Density exceptions require geological proof of additional recoverable reserves."],
        reasoning_framework="16 TAC §3.38 density exceptions demand showing additional wells will recover reserves not otherwise producible. Requires reservoir engineering analysis and proof of no drainage from offsetting tracts.",
        key_factors=["Reservoir characterization", "Drainage analysis", "EUR calculations", "Offset well performance"],
        primary_authority=["16 TAC §3.38"],
        confidence=ConfidenceLevel.MEDIUM,
        confidence_stratification="aggressive"
    ),

    DoctrineBlock(
        topic="good_cause_standard",
        category=IssueCategory.GOOD_CAUSE,
        keywords=["good cause", "burden of proof", "applicant burden"],
        conclusion_template=["Good cause requires clear and convincing evidence."],
        reasoning_framework="RRC requires applicant demonstrate good cause by clear and convincing evidence. Standard is higher than preponderance but lower than beyond reasonable doubt. Applicant bears burden throughout proceeding.",
        key_factors=["Quality of evidence", "Expert witness credibility", "Technical data completeness"],
        primary_authority=["Texas Administrative Procedure Act", "RRC precedent"],
        confidence=ConfidenceLevel.HIGH,
        confidence_stratification="defensible"
    ),
]
