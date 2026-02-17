"""
LG03 REGULATORY COMPLIANCE ENGINE - DOCTRINE CACHE MODULE
Pre-compiled regulatory compliance reasoning blocks with authority hierarchies.

Provides:
    - 40+ regulatory doctrine blocks covering major federal agencies
    - Agency authority hierarchy with preemption rules
    - Enforcement action database with penalty ranges
    - Industry-to-regulation mapping via NAICS codes
    - Compliance obligation templates
    - Deadline tracking frameworks
    - Risk factor catalogs per regulation domain

Architecture:
    Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert reasoning
    Immutable at runtime. No auto-learning. No probabilistic inference.
    Changes require version increment and governance approval.

Author: ECHO OMEGA PRIME
Authority: 11.0 SOVEREIGN
Engine: LG03 Regulatory Compliance
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


# ============================================================================
# GOVERNANCE METADATA
# ============================================================================

DOCTRINE_CACHE_VERSION: str = "1.0.0"
DOCTRINE_CACHE_RELEASE_DATE: str = "2026-02-10"
DOCTRINE_CACHE_AUTHOR: str = "ECHO OMEGA PRIME"
_GOVERNANCE_LOCKED: bool = False


# ============================================================================
# ENUMS AND TYPES
# ============================================================================

class AgencyLevel(str, Enum):
    """Government level in the regulatory hierarchy."""
    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"
    SELF_REGULATORY = "self_regulatory"
    INTERNATIONAL = "international"


class AuthorityType(str, Enum):
    """Type of regulatory authority."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ADVISORY = "advisory"
    DELEGATED = "delegated"
    SHARED = "shared"


class PreemptionType(str, Enum):
    """Type of federal preemption over state/local law."""
    EXPRESS = "express"
    IMPLIED_FIELD = "implied_field"
    IMPLIED_CONFLICT = "implied_conflict"
    SAVINGS_CLAUSE = "savings_clause"
    NONE = "none"


class EnforcementSeverity(str, Enum):
    """Tier of enforcement action severity."""
    CRIMINAL = "criminal"
    CIVIL_PENALTY = "civil_penalty"
    ADMINISTRATIVE = "administrative"
    CORRECTIVE = "corrective"
    ADVISORY = "advisory"


class ComplianceStatus(str, Enum):
    """Status of a compliance obligation."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    PENDING_REVIEW = "pending_review"
    NOT_APPLICABLE = "not_applicable"
    EXEMPTED = "exempted"


class RuleStatus(str, Enum):
    """Status of a regulation in the rulemaking lifecycle."""
    PROPOSED = "proposed"
    INTERIM_FINAL = "interim_final"
    FINAL = "final"
    EFFECTIVE = "effective"
    STAYED = "stayed"
    VACATED = "vacated"
    AMENDED = "amended"
    REPEALED = "repealed"


class RiskLevel(str, Enum):
    """Qualitative risk level."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class AgencyProfile:
    """Profile of a regulatory agency with authority scope."""
    code: str
    full_name: str
    level: AgencyLevel
    authority_type: AuthorityType
    parent_agency: Optional[str]
    enabling_statute: str
    primary_cfr_titles: List[int]
    enforcement_powers: List[EnforcementSeverity]
    jurisdiction_scope: str
    website: str
    key_divisions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "full_name": self.full_name,
            "level": self.level.value,
            "authority_type": self.authority_type.value,
            "parent_agency": self.parent_agency,
            "enabling_statute": self.enabling_statute,
            "primary_cfr_titles": self.primary_cfr_titles,
            "enforcement_powers": [e.value for e in self.enforcement_powers],
            "jurisdiction_scope": self.jurisdiction_scope,
            "website": self.website,
            "key_divisions": self.key_divisions,
        }


@dataclass
class PreemptionRule:
    """Federal preemption rule over state/local regulations."""
    federal_statute: str
    preemption_type: PreemptionType
    scope: str
    exceptions: List[str]
    key_cases: List[str]
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "federal_statute": self.federal_statute,
            "preemption_type": self.preemption_type.value,
            "scope": self.scope,
            "exceptions": self.exceptions,
            "key_cases": self.key_cases,
            "description": self.description,
        }


@dataclass
class EnforcementAction:
    """Template for enforcement action with penalty ranges."""
    agency: str
    action_type: EnforcementSeverity
    violation_category: str
    statute_basis: str
    penalty_min: Optional[float]
    penalty_max: Optional[float]
    penalty_per_day: Optional[float]
    penalty_per_violation: Optional[float]
    criminal_exposure: bool
    max_imprisonment_years: Optional[int]
    description: str
    recent_examples: List[str] = field(default_factory=list)
    mitigating_factors: List[str] = field(default_factory=list)
    aggravating_factors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agency": self.agency,
            "action_type": self.action_type.value,
            "violation_category": self.violation_category,
            "statute_basis": self.statute_basis,
            "penalty_min": self.penalty_min,
            "penalty_max": self.penalty_max,
            "penalty_per_day": self.penalty_per_day,
            "penalty_per_violation": self.penalty_per_violation,
            "criminal_exposure": self.criminal_exposure,
            "max_imprisonment_years": self.max_imprisonment_years,
            "description": self.description,
            "recent_examples": self.recent_examples,
            "mitigating_factors": self.mitigating_factors,
            "aggravating_factors": self.aggravating_factors,
        }


@dataclass
class ComplianceObligation:
    """A specific regulatory compliance obligation."""
    obligation_id: str
    regulation: str
    cfr_reference: str
    agency: str
    description: str
    required_actions: List[str]
    frequency: str
    deadline_type: str
    applicable_industries: List[str]
    applicable_entity_sizes: List[str]
    penalty_for_noncompliance: str
    documentation_required: List[str]
    exemptions: List[str] = field(default_factory=list)
    related_obligations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "obligation_id": self.obligation_id,
            "regulation": self.regulation,
            "cfr_reference": self.cfr_reference,
            "agency": self.agency,
            "description": self.description,
            "required_actions": self.required_actions,
            "frequency": self.frequency,
            "deadline_type": self.deadline_type,
            "applicable_industries": self.applicable_industries,
            "applicable_entity_sizes": self.applicable_entity_sizes,
            "penalty_for_noncompliance": self.penalty_for_noncompliance,
            "documentation_required": self.documentation_required,
            "exemptions": self.exemptions,
            "related_obligations": self.related_obligations,
        }


@dataclass
class RegulatoryDoctrineBlock:
    """Pre-compiled regulatory compliance reasoning block.

    Each block encodes expert knowledge about a specific regulatory domain,
    including the analytical framework, key factors, citation authority,
    enforcement posture, and compliance requirements.
    """
    topic: str
    keywords: List[str]
    agency: str
    cfr_references: List[str]
    usc_references: List[str]

    # Core reasoning
    compliance_framework: str
    key_requirements: List[str]
    key_factors: List[str]

    # Risk assessment
    risk_level: RiskLevel
    severity_score: int
    likelihood_score: int
    detectability_score: int

    # Enforcement
    enforcement_history: str
    penalty_range: str
    criminal_exposure: bool

    # Compliance actions
    required_actions: List[str]
    documentation_required: List[str]
    reporting_frequency: str

    # Preemption
    preemption_type: PreemptionType
    state_variations: List[str]

    # Industries
    applicable_naics: List[str]
    entity_size_threshold: Optional[str]

    # Metadata
    confidence: str = "high"
    last_updated: str = "2026-02-10"
    related_doctrines: List[str] = field(default_factory=list)

    @property
    def composite_risk_score(self) -> int:
        """Severity x Likelihood x Detectability (1-1000 scale)."""
        return self.severity_score * self.likelihood_score * self.detectability_score

    def get_authority_weight(self) -> int:
        """Calculate weighted authority score based on CFR and USC references."""
        weight = 0
        weight += len(self.usc_references) * 100
        weight += len(self.cfr_references) * 80
        return weight

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "agency": self.agency,
            "cfr_references": self.cfr_references,
            "usc_references": self.usc_references,
            "compliance_framework": self.compliance_framework,
            "key_requirements": self.key_requirements,
            "key_factors": self.key_factors,
            "risk_level": self.risk_level.value,
            "composite_risk_score": self.composite_risk_score,
            "severity_score": self.severity_score,
            "likelihood_score": self.likelihood_score,
            "detectability_score": self.detectability_score,
            "enforcement_history": self.enforcement_history,
            "penalty_range": self.penalty_range,
            "criminal_exposure": self.criminal_exposure,
            "required_actions": self.required_actions,
            "documentation_required": self.documentation_required,
            "reporting_frequency": self.reporting_frequency,
            "preemption_type": self.preemption_type.value,
            "state_variations": self.state_variations,
            "applicable_naics": self.applicable_naics,
            "entity_size_threshold": self.entity_size_threshold,
            "confidence": self.confidence,
            "last_updated": self.last_updated,
            "related_doctrines": self.related_doctrines,
        }


# ============================================================================
# AGENCY PROFILES DATABASE
# ============================================================================

AGENCY_PROFILES: Dict[str, AgencyProfile] = {
    "SEC": AgencyProfile(
        code="SEC",
        full_name="Securities and Exchange Commission",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency=None,
        enabling_statute="Securities Exchange Act of 1934 (15 U.S.C. 78a et seq.)",
        primary_cfr_titles=[17],
        enforcement_powers=[EnforcementSeverity.CRIMINAL, EnforcementSeverity.CIVIL_PENALTY,
                            EnforcementSeverity.ADMINISTRATIVE],
        jurisdiction_scope="Securities markets, public companies, investment advisers, broker-dealers",
        website="https://www.sec.gov",
        key_divisions=["Division of Enforcement", "Division of Corporation Finance",
                        "Division of Trading and Markets", "Division of Investment Management"],
    ),
    "EPA": AgencyProfile(
        code="EPA",
        full_name="Environmental Protection Agency",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency=None,
        enabling_statute="Various (CAA, CWA, RCRA, CERCLA, TSCA, SDWA, FIFRA, EPCRA)",
        primary_cfr_titles=[40],
        enforcement_powers=[EnforcementSeverity.CRIMINAL, EnforcementSeverity.CIVIL_PENALTY,
                            EnforcementSeverity.ADMINISTRATIVE, EnforcementSeverity.CORRECTIVE],
        jurisdiction_scope="Environmental protection, pollution control, chemical safety",
        website="https://www.epa.gov",
        key_divisions=["Office of Enforcement and Compliance Assurance",
                        "Office of Air and Radiation", "Office of Water",
                        "Office of Land and Emergency Management"],
    ),
    "OSHA": AgencyProfile(
        code="OSHA",
        full_name="Occupational Safety and Health Administration",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency="DOL",
        enabling_statute="Occupational Safety and Health Act of 1970 (29 U.S.C. 651 et seq.)",
        primary_cfr_titles=[29],
        enforcement_powers=[EnforcementSeverity.CRIMINAL, EnforcementSeverity.CIVIL_PENALTY,
                            EnforcementSeverity.CORRECTIVE],
        jurisdiction_scope="Workplace safety and health standards, inspections, enforcement",
        website="https://www.osha.gov",
        key_divisions=["Directorate of Enforcement Programs",
                        "Directorate of Standards and Guidance",
                        "Directorate of Construction"],
    ),
    "IRS": AgencyProfile(
        code="IRS",
        full_name="Internal Revenue Service",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency="Treasury",
        enabling_statute="Internal Revenue Code (26 U.S.C.)",
        primary_cfr_titles=[26],
        enforcement_powers=[EnforcementSeverity.CRIMINAL, EnforcementSeverity.CIVIL_PENALTY,
                            EnforcementSeverity.ADMINISTRATIVE],
        jurisdiction_scope="Federal tax administration, collection, enforcement",
        website="https://www.irs.gov",
        key_divisions=["Criminal Investigation", "Large Business and International",
                        "Small Business/Self-Employed", "Tax Exempt and Government Entities"],
    ),
    "FTC": AgencyProfile(
        code="FTC",
        full_name="Federal Trade Commission",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency=None,
        enabling_statute="FTC Act (15 U.S.C. 41 et seq.)",
        primary_cfr_titles=[16],
        enforcement_powers=[EnforcementSeverity.CIVIL_PENALTY, EnforcementSeverity.ADMINISTRATIVE,
                            EnforcementSeverity.CORRECTIVE],
        jurisdiction_scope="Consumer protection, antitrust, data privacy, advertising",
        website="https://www.ftc.gov",
        key_divisions=["Bureau of Consumer Protection", "Bureau of Competition",
                        "Bureau of Economics"],
    ),
    "FDA": AgencyProfile(
        code="FDA",
        full_name="Food and Drug Administration",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency="HHS",
        enabling_statute="FD&C Act (21 U.S.C. 301 et seq.)",
        primary_cfr_titles=[21],
        enforcement_powers=[EnforcementSeverity.CRIMINAL, EnforcementSeverity.CIVIL_PENALTY,
                            EnforcementSeverity.ADMINISTRATIVE, EnforcementSeverity.CORRECTIVE],
        jurisdiction_scope="Food safety, drug approval, medical devices, cosmetics, tobacco",
        website="https://www.fda.gov",
        key_divisions=["Center for Drug Evaluation and Research",
                        "Center for Biologics Evaluation and Research",
                        "Center for Food Safety and Applied Nutrition",
                        "Center for Devices and Radiological Health"],
    ),
    "DOL": AgencyProfile(
        code="DOL",
        full_name="Department of Labor",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency=None,
        enabling_statute="Various (FLSA, FMLA, ERISA, OSHA Act, WARN Act)",
        primary_cfr_titles=[20, 29],
        enforcement_powers=[EnforcementSeverity.CIVIL_PENALTY, EnforcementSeverity.ADMINISTRATIVE,
                            EnforcementSeverity.CORRECTIVE],
        jurisdiction_scope="Labor standards, workplace safety, employee benefits, workforce development",
        website="https://www.dol.gov",
        key_divisions=["Wage and Hour Division", "Employee Benefits Security Administration",
                        "Office of Federal Contract Compliance Programs"],
    ),
    "CFPB": AgencyProfile(
        code="CFPB",
        full_name="Consumer Financial Protection Bureau",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency=None,
        enabling_statute="Dodd-Frank Wall Street Reform Act, Title X (12 U.S.C. 5481 et seq.)",
        primary_cfr_titles=[12],
        enforcement_powers=[EnforcementSeverity.CIVIL_PENALTY, EnforcementSeverity.ADMINISTRATIVE,
                            EnforcementSeverity.CORRECTIVE],
        jurisdiction_scope="Consumer financial products and services",
        website="https://www.consumerfinance.gov",
        key_divisions=["Division of Supervision, Enforcement, and Fair Lending",
                        "Division of Research, Monitoring, and Regulations"],
    ),
    "FINRA": AgencyProfile(
        code="FINRA",
        full_name="Financial Industry Regulatory Authority",
        level=AgencyLevel.SELF_REGULATORY,
        authority_type=AuthorityType.DELEGATED,
        parent_agency="SEC",
        enabling_statute="Securities Exchange Act of 1934 Section 15A",
        primary_cfr_titles=[],
        enforcement_powers=[EnforcementSeverity.CIVIL_PENALTY, EnforcementSeverity.ADMINISTRATIVE],
        jurisdiction_scope="Broker-dealers, registered representatives",
        website="https://www.finra.org",
        key_divisions=["Department of Enforcement", "Department of Market Regulation",
                        "Office of Dispute Resolution"],
    ),
    "FINCEN": AgencyProfile(
        code="FINCEN",
        full_name="Financial Crimes Enforcement Network",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency="Treasury",
        enabling_statute="Bank Secrecy Act (31 U.S.C. 5311 et seq.)",
        primary_cfr_titles=[31],
        enforcement_powers=[EnforcementSeverity.CRIMINAL, EnforcementSeverity.CIVIL_PENALTY,
                            EnforcementSeverity.ADMINISTRATIVE],
        jurisdiction_scope="Anti-money laundering, counter-terrorism financing, BSA compliance",
        website="https://www.fincen.gov",
        key_divisions=["Enforcement Division", "Intelligence Division", "Policy Division"],
    ),
    "EEOC": AgencyProfile(
        code="EEOC",
        full_name="Equal Employment Opportunity Commission",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency=None,
        enabling_statute="Title VII Civil Rights Act, ADA, ADEA, EPA, GINA",
        primary_cfr_titles=[29],
        enforcement_powers=[EnforcementSeverity.CIVIL_PENALTY, EnforcementSeverity.ADMINISTRATIVE],
        jurisdiction_scope="Employment discrimination, harassment, reasonable accommodation",
        website="https://www.eeoc.gov",
        key_divisions=["Office of Field Programs", "Office of General Counsel",
                        "Office of Federal Operations"],
    ),
    "OFAC": AgencyProfile(
        code="OFAC",
        full_name="Office of Foreign Assets Control",
        level=AgencyLevel.FEDERAL,
        authority_type=AuthorityType.PRIMARY,
        parent_agency="Treasury",
        enabling_statute="IEEPA (50 U.S.C. 1701), Trading with the Enemy Act",
        primary_cfr_titles=[31],
        enforcement_powers=[EnforcementSeverity.CRIMINAL, EnforcementSeverity.CIVIL_PENALTY],
        jurisdiction_scope="Economic sanctions, trade embargoes, SDN list enforcement",
        website="https://ofac.treasury.gov",
        key_divisions=["Sanctions Compliance and Evaluation Division",
                        "Licensing Division", "Enforcement Division"],
    ),
}


# ============================================================================
# PREEMPTION RULES DATABASE
# ============================================================================

PREEMPTION_RULES: Dict[str, PreemptionRule] = {
    "erisa_preemption": PreemptionRule(
        federal_statute="ERISA (29 U.S.C. 1144)",
        preemption_type=PreemptionType.EXPRESS,
        scope="State laws that 'relate to' employee benefit plans",
        exceptions=[
            "State insurance regulation (savings clause)",
            "State banking regulation",
            "State securities regulation",
            "State criminal law",
            "Generally applicable state laws (tax, contract, fraud)",
        ],
        key_cases=[
            "Shaw v. Delta Air Lines, 463 U.S. 85 (1983)",
            "Pilot Life Ins. Co. v. Dedeaux, 481 U.S. 41 (1987)",
            "FMC Corp. v. Holliday, 498 U.S. 52 (1990)",
            "Gobeille v. Liberty Mutual, 577 U.S. 312 (2016)",
        ],
        description="ERISA broadly preempts state laws that relate to employee benefit plans, "
                    "with notable exceptions for insurance, banking, and securities regulation.",
    ),
    "federal_securities_preemption": PreemptionRule(
        federal_statute="NSMIA (15 U.S.C. 77r)",
        preemption_type=PreemptionType.EXPRESS,
        scope="State blue sky laws for 'covered securities'",
        exceptions=[
            "State anti-fraud enforcement",
            "State notice filing requirements",
            "State fee collection",
            "Non-covered securities remain under state jurisdiction",
        ],
        key_cases=[
            "Merrill Lynch v. Dabit, 547 U.S. 71 (2006)",
            "Cyan v. Beaver County, 583 U.S. 149 (2018)",
        ],
        description="NSMIA preempts state blue sky registration for covered securities (exchange-listed, "
                    "mutual funds, qualified purchaser exemption) but preserves state anti-fraud authority.",
    ),
    "clean_air_act_preemption": PreemptionRule(
        federal_statute="Clean Air Act (42 U.S.C. 7543)",
        preemption_type=PreemptionType.EXPRESS,
        scope="State emission standards for new motor vehicles",
        exceptions=[
            "California waiver (Section 209(b))",
            "States may adopt California standards (Section 177)",
            "State authority over in-use vehicles",
            "State fuel standards (separate from vehicle standards)",
        ],
        key_cases=[
            "Engine Manufacturers Assn. v. South Coast Air Quality, 541 U.S. 246 (2004)",
        ],
        description="CAA preempts state motor vehicle emission standards but provides California "
                    "waiver and allows other states to adopt California standards.",
    ),
    "fdca_preemption": PreemptionRule(
        federal_statute="FD&C Act (21 U.S.C. 379r - OTC drugs, 360k - devices)",
        preemption_type=PreemptionType.IMPLIED_CONFLICT,
        scope="State tort claims that conflict with FDA-approved labeling",
        exceptions=[
            "State law claims parallel to federal requirements",
            "Manufacturing defect claims",
            "Fraud on the FDA claims",
            "Generic drugs (different preemption analysis)",
        ],
        key_cases=[
            "Riegel v. Medtronic, 552 U.S. 312 (2008) - PMA devices",
            "Wyeth v. Levine, 555 U.S. 555 (2009) - brand-name drugs not preempted",
            "PLIVA v. Mensing, 564 U.S. 604 (2011) - generic drugs preempted",
            "Mutual Pharma v. Bartlett, 570 U.S. 472 (2013) - generic design defect preempted",
        ],
        description="FDA preemption varies significantly: PMA medical devices are strongly preempted, "
                    "brand-name drug failure-to-warn claims are NOT preempted, but generic drug "
                    "failure-to-warn claims ARE preempted.",
    ),
    "osha_preemption": PreemptionRule(
        federal_statute="OSH Act (29 U.S.C. 667)",
        preemption_type=PreemptionType.IMPLIED_FIELD,
        scope="State workplace safety regulations where OSHA has promulgated standards",
        exceptions=[
            "State plan states (approved by OSHA)",
            "State and local government employees",
            "State regulations addressing hazards not covered by OSHA",
            "State criminal prosecutions",
        ],
        key_cases=[
            "Gade v. National Solid Wastes Mgmt. Assn., 505 U.S. 88 (1992)",
        ],
        description="Where OSHA has promulgated a specific standard, state regulations addressing "
                    "the same workplace hazard are preempted unless the state has an approved state plan.",
    ),
    "banking_preemption": PreemptionRule(
        federal_statute="National Bank Act / Dodd-Frank Section 1044",
        preemption_type=PreemptionType.EXPRESS,
        scope="State laws that significantly interfere with national bank powers",
        exceptions=[
            "State consumer protection laws (post-Dodd-Frank)",
            "State anti-discrimination laws",
            "State criminal law",
            "State contract and property law of general application",
        ],
        key_cases=[
            "Barnett Bank v. Nelson, 517 U.S. 25 (1996)",
            "Cuomo v. Clearing House, 557 U.S. 519 (2009)",
        ],
        description="National banks and federal thrifts enjoy preemption of state laws that "
                    "significantly interfere with their powers, narrowed by Dodd-Frank.",
    ),
}


# ============================================================================
# ENFORCEMENT ACTION DATABASE
# ============================================================================

ENFORCEMENT_ACTIONS: Dict[str, EnforcementAction] = {
    "sec_fraud": EnforcementAction(
        agency="SEC",
        action_type=EnforcementSeverity.CRIMINAL,
        violation_category="Securities Fraud",
        statute_basis="15 U.S.C. 78j(b), 17 CFR 240.10b-5",
        penalty_min=None,
        penalty_max=25_000_000.0,
        penalty_per_day=None,
        penalty_per_violation=None,
        criminal_exposure=True,
        max_imprisonment_years=20,
        description="Securities fraud under Rule 10b-5: material misrepresentation or omission "
                    "in connection with purchase or sale of securities.",
        recent_examples=["SEC v. Theranos (2018)", "SEC v. Ripple Labs (2020)"],
        mitigating_factors=["Cooperation with investigation", "Self-reporting", "Remediation efforts",
                            "No prior violations"],
        aggravating_factors=["Pattern of conduct", "Harm to retail investors", "Insider status",
                            "Destruction of evidence"],
    ),
    "epa_rcra_violation": EnforcementAction(
        agency="EPA",
        action_type=EnforcementSeverity.CIVIL_PENALTY,
        violation_category="Hazardous Waste Violations",
        statute_basis="42 U.S.C. 6928, 40 CFR Part 261-268",
        penalty_min=None,
        penalty_max=70_117.0,
        penalty_per_day=70_117.0,
        penalty_per_violation=70_117.0,
        criminal_exposure=True,
        max_imprisonment_years=15,
        description="RCRA violations including improper storage, treatment, or disposal of "
                    "hazardous waste. Knowing endangerment carries enhanced criminal penalties.",
        recent_examples=["EPA enforcement of RCRA corrective action at Superfund sites"],
        mitigating_factors=["Voluntary disclosure", "Quick cleanup", "No environmental harm",
                            "Small business"],
        aggravating_factors=["Repeat violations", "Environmental damage", "Endangerment",
                            "Concealment"],
    ),
    "osha_willful_violation": EnforcementAction(
        agency="OSHA",
        action_type=EnforcementSeverity.CIVIL_PENALTY,
        violation_category="Willful Safety Violation",
        statute_basis="29 U.S.C. 666(a), 29 CFR Part 1910/1926",
        penalty_min=11_524.0,
        penalty_max=161_323.0,
        penalty_per_day=None,
        penalty_per_violation=161_323.0,
        criminal_exposure=True,
        max_imprisonment_years=6,
        description="Willful violation of OSHA standards. Criminal prosecution available when "
                    "willful violation causes employee death.",
        recent_examples=["OSHA willful citations for fall protection failures in construction"],
        mitigating_factors=["Good faith effort to comply", "Small employer", "No prior history",
                            "Quick abatement"],
        aggravating_factors=["Prior violations", "Employee injury/death", "Disregard for standards",
                            "History of non-compliance"],
    ),
    "ftc_unfair_practices": EnforcementAction(
        agency="FTC",
        action_type=EnforcementSeverity.CIVIL_PENALTY,
        violation_category="Unfair or Deceptive Acts or Practices",
        statute_basis="15 U.S.C. 45(a), 15 U.S.C. 57b",
        penalty_min=None,
        penalty_max=50_120.0,
        penalty_per_day=None,
        penalty_per_violation=50_120.0,
        criminal_exposure=False,
        max_imprisonment_years=None,
        description="Unfair or deceptive acts or practices in commerce. Includes false advertising, "
                    "data security failures, dark patterns, and deceptive business practices.",
        recent_examples=["FTC v. Facebook/Meta (data privacy)", "FTC v. Amazon (dark patterns)"],
        mitigating_factors=["Cooperation", "Voluntary remediation", "Limited consumer harm"],
        aggravating_factors=["Targeting vulnerable populations", "Widespread harm",
                            "Prior FTC orders"],
    ),
    "bsa_aml_violation": EnforcementAction(
        agency="FINCEN",
        action_type=EnforcementSeverity.CIVIL_PENALTY,
        violation_category="BSA/AML Compliance Failure",
        statute_basis="31 U.S.C. 5321, 31 CFR Part 1010-1029",
        penalty_min=None,
        penalty_max=1_000_000.0,
        penalty_per_day=None,
        penalty_per_violation=None,
        criminal_exposure=True,
        max_imprisonment_years=10,
        description="Failure to maintain adequate BSA/AML programs, file SARs/CTRs, or conduct "
                    "required CDD/KYC. Willful violations carry criminal penalties.",
        recent_examples=["TD Bank $3B AML penalty (2024)", "Binance $4.3B penalty (2023)"],
        mitigating_factors=["Self-reporting", "Remediation", "Cooperation with law enforcement"],
        aggravating_factors=["Facilitating criminal activity", "Systemic failures",
                            "Prior enforcement actions"],
    ),
    "hipaa_breach": EnforcementAction(
        agency="HHS",
        action_type=EnforcementSeverity.CIVIL_PENALTY,
        violation_category="HIPAA Privacy/Security Rule Violation",
        statute_basis="42 U.S.C. 1320d-5, 45 CFR Parts 160, 164",
        penalty_min=137.0,
        penalty_max=2_067_813.0,
        penalty_per_day=None,
        penalty_per_violation=None,
        criminal_exposure=True,
        max_imprisonment_years=10,
        description="Violations of HIPAA Privacy and Security Rules. Four-tier penalty structure "
                    "based on level of culpability (unknowing, reasonable cause, willful neglect corrected, "
                    "willful neglect uncorrected).",
        recent_examples=["Anthem $16M HIPAA settlement (2018)", "Premera $6.85M (2020)"],
        mitigating_factors=["Unknowing violation", "Correction within 30 days",
                            "Reasonable security measures", "Small entity"],
        aggravating_factors=["Willful neglect", "Large-scale breach", "Repeat violations",
                            "Failure to notify"],
    ),
    "ofac_sanctions_violation": EnforcementAction(
        agency="OFAC",
        action_type=EnforcementSeverity.CIVIL_PENALTY,
        violation_category="Economic Sanctions Violation",
        statute_basis="50 U.S.C. 1705, 31 CFR Part 501",
        penalty_min=None,
        penalty_max=368_136.0,
        penalty_per_day=None,
        penalty_per_violation=368_136.0,
        criminal_exposure=True,
        max_imprisonment_years=20,
        description="Violation of OFAC-administered sanctions programs. Strict liability for "
                    "civil violations; willful violations carry criminal penalties.",
        recent_examples=["BNP Paribas $8.97B sanctions penalty (2014)",
                        "ZTE $1.19B (2017)", "Standard Chartered $1.1B (2019)"],
        mitigating_factors=["Voluntary self-disclosure", "Cooperation", "Remedial measures",
                            "Compliance program in place"],
        aggravating_factors=["Management involvement", "Pattern of conduct", "Concealment",
                            "Significant harm to sanctions program objectives"],
    ),
    "eeoc_discrimination": EnforcementAction(
        agency="EEOC",
        action_type=EnforcementSeverity.CIVIL_PENALTY,
        violation_category="Employment Discrimination",
        statute_basis="42 U.S.C. 2000e et seq., 42 U.S.C. 12101 et seq.",
        penalty_min=None,
        penalty_max=300_000.0,
        penalty_per_day=None,
        penalty_per_violation=None,
        criminal_exposure=False,
        max_imprisonment_years=None,
        description="Employment discrimination based on race, color, religion, sex, national "
                    "origin, age, disability, or genetic information. Compensatory and punitive "
                    "damages capped by employer size.",
        recent_examples=["EEOC systemic discrimination investigations in tech industry"],
        mitigating_factors=["Good faith compliance efforts", "Anti-discrimination training",
                            "Prompt corrective action", "First offense"],
        aggravating_factors=["Pattern or practice", "Retaliation", "Management involvement",
                            "Large number of affected employees"],
    ),
}


# ============================================================================
# REGULATORY DOCTRINE CACHE
# ============================================================================

DOCTRINE_CACHE: Dict[str, RegulatoryDoctrineBlock] = {
    "securities_disclosure": RegulatoryDoctrineBlock(
        topic="Securities Disclosure and Reporting Requirements",
        keywords=["sec filing", "10-k", "10-q", "annual report", "securities disclosure",
                  "material information", "insider trading", "form 8-k", "proxy statement",
                  "reg fd", "regulation fd", "securities reporting"],
        agency="SEC",
        cfr_references=["17 CFR 240.10b-5", "17 CFR 240.13a-1", "17 CFR 240.13a-13",
                        "17 CFR 240.14a-3", "17 CFR 243.100"],
        usc_references=["15 U.S.C. 78j(b)", "15 U.S.C. 78m(a)", "15 U.S.C. 78n(a)"],
        compliance_framework="""
SEC DISCLOSURE COMPLIANCE FRAMEWORK:

1. PERIODIC REPORTING OBLIGATIONS
   - Form 10-K: Annual report within 60 days of fiscal year end (large accelerated filers)
   - Form 10-Q: Quarterly report within 40 days of quarter end
   - Form 8-K: Current report within 4 business days of triggering event
   - Proxy Statement: Before annual shareholder meeting

2. MATERIAL INFORMATION STANDARD
   - Information is material if there is a substantial likelihood that a reasonable
     investor would consider it important in making an investment decision
   - TSC Industries v. Northway, 426 U.S. 438 (1976)
   - Must disclose all material facts; omissions of material facts are violations

3. REGULATION FD (FAIR DISCLOSURE)
   - Material nonpublic information disclosed to select persons must be
     simultaneously disclosed to the public
   - Applies to officers, directors, spokespersons
   - Intentional selective disclosure requires simultaneous public disclosure
   - Non-intentional requires prompt public disclosure (within 24 hours)

4. INTERNAL CONTROLS (SOX 302/404)
   - CEO/CFO must certify financial statements and internal controls
   - Annual assessment of internal control over financial reporting
   - External auditor must attest to management's assessment (accelerated filers)""",
        key_requirements=[
            "File 10-K within 60/75/90 days of fiscal year end (by filer category)",
            "File 10-Q within 40/45 days of quarter end",
            "File 8-K within 4 business days of triggering event",
            "SOX 302 certifications by CEO and CFO",
            "SOX 404 internal control assessment and attestation",
            "Regulation FD compliance for material nonpublic information",
            "XBRL/iXBRL tagging of financial statements",
        ],
        key_factors=[
            "Filer category (large accelerated, accelerated, non-accelerated, SRC, EGC)",
            "Materiality of information",
            "Timeliness of disclosure",
            "Adequacy of internal controls",
            "Insider trading compliance",
        ],
        risk_level=RiskLevel.HIGH,
        severity_score=9,
        likelihood_score=7,
        detectability_score=9,
        enforcement_history="SEC brings approximately 700+ enforcement actions annually. "
                           "Disclosure failures are among the most common enforcement targets.",
        penalty_range="$25M+ civil penalties; criminal prosecution for willful violations; "
                      "officer/director bars; disgorgement of profits",
        criminal_exposure=True,
        required_actions=[
            "Establish disclosure committee",
            "Implement disclosure controls and procedures",
            "Maintain insider trading compliance program",
            "SOX 302/404 compliance program",
            "Regulation FD training for officers and spokespersons",
            "EDGAR filing calendar maintenance",
        ],
        documentation_required=[
            "Board minutes approving financial statements",
            "Disclosure committee meeting minutes",
            "SOX testing documentation",
            "Regulation FD compliance policies",
            "Insider trading pre-clearance records",
        ],
        reporting_frequency="Annual (10-K), Quarterly (10-Q), Event-driven (8-K)",
        preemption_type=PreemptionType.EXPRESS,
        state_variations=[
            "State blue sky laws preempted for covered securities (NSMIA)",
            "State anti-fraud actions preserved",
            "State notice filings still required in some states",
        ],
        applicable_naics=["52"],
        entity_size_threshold="Public companies with SEC reporting obligations",
        related_doctrines=["insider_trading", "sox_compliance", "proxy_rules"],
    ),

    "environmental_hazwaste": RegulatoryDoctrineBlock(
        topic="Hazardous Waste Management (RCRA)",
        keywords=["rcra", "hazardous waste", "waste disposal", "waste management",
                  "generator status", "manifest", "treatment storage disposal",
                  "tsd facility", "characteristic waste", "listed waste",
                  "land disposal restrictions", "corrective action"],
        agency="EPA",
        cfr_references=["40 CFR 261", "40 CFR 262", "40 CFR 263", "40 CFR 264",
                        "40 CFR 265", "40 CFR 268"],
        usc_references=["42 U.S.C. 6921", "42 U.S.C. 6922", "42 U.S.C. 6924", "42 U.S.C. 6928"],
        compliance_framework="""
RCRA HAZARDOUS WASTE COMPLIANCE FRAMEWORK:

1. WASTE DETERMINATION
   - Is the material a solid waste? (40 CFR 261.2)
   - Is it excluded from regulation? (40 CFR 261.4)
   - Is it a listed waste (F, K, U, P lists)? (40 CFR 261.30-33)
   - Is it a characteristic waste (ignitability, corrosivity,
     reactivity, toxicity)? (40 CFR 261.20-24)

2. GENERATOR STATUS DETERMINATION
   - Large Quantity Generator (LQG): 1,000+ kg/month
   - Small Quantity Generator (SQG): 100-1,000 kg/month
   - Very Small Quantity Generator (VSQG): <100 kg/month
   - Status determines applicable requirements for storage time,
     accumulation limits, and training

3. MANIFEST AND TRACKING
   - Uniform Hazardous Waste Manifest (EPA Form 8700-22)
   - Electronic manifest (e-Manifest) system
   - Cradle-to-grave tracking from generation to disposal
   - Exception reporting for missing manifests

4. TREATMENT, STORAGE, AND DISPOSAL (TSD)
   - TSD facilities require RCRA Part B permits
   - Land Disposal Restrictions (LDR) apply to all hazardous waste
   - Treatment standards must be met before land disposal
   - Corrective action requirements for releases""",
        key_requirements=[
            "Perform hazardous waste determination for all waste streams",
            "Obtain EPA ID number (EPA Form 8700-12)",
            "Comply with generator accumulation time limits",
            "Use EPA hazardous waste manifest for all shipments",
            "Use only permitted TSD facilities for disposal",
            "Maintain records for 3 years (generator) or facility life (TSD)",
            "Train employees handling hazardous waste",
            "Prepare contingency plan and emergency procedures",
        ],
        key_factors=[
            "Generator status (LQG/SQG/VSQG)",
            "Waste characteristics and listed status",
            "Storage time and accumulation limits",
            "Land disposal restriction compliance",
            "Manifest accuracy and completeness",
        ],
        risk_level=RiskLevel.HIGH,
        severity_score=8,
        likelihood_score=7,
        detectability_score=8,
        enforcement_history="EPA brings 1,500+ RCRA enforcement actions annually. "
                           "Penalties routinely exceed $100K for significant violations.",
        penalty_range="Up to $70,117/day/violation civil; up to $1M criminal fine; "
                      "up to 15 years imprisonment for knowing endangerment",
        criminal_exposure=True,
        required_actions=[
            "Waste characterization for all waste streams",
            "Generator category determination",
            "EPA ID number registration",
            "Manifest system compliance",
            "Accumulation area management",
            "Employee training program",
            "Contingency plan development",
            "Biennial report (LQG)",
        ],
        documentation_required=[
            "Waste determination records",
            "Manifest copies (3-year retention)",
            "Land disposal restriction notifications",
            "Training records",
            "Contingency plan",
            "Biennial report copies",
            "Inspection logs",
        ],
        reporting_frequency="Biennial (LQG biennial report), event-driven (exception reports)",
        preemption_type=PreemptionType.SAVINGS_CLAUSE,
        state_variations=[
            "Many states have authorized RCRA programs with additional requirements",
            "California requires Unified Program (CUPA) compliance",
            "New York has additional hazardous waste transporter requirements",
            "Texas imposes additional fees on hazardous waste generation",
        ],
        applicable_naics=["21", "22", "23", "31", "32", "33", "48", "49", "56", "62"],
        entity_size_threshold="Any entity generating hazardous waste",
        related_doctrines=["cercla_superfund", "clean_water_discharge", "air_emissions"],
    ),

    "workplace_safety_osha": RegulatoryDoctrineBlock(
        topic="OSHA Workplace Safety and Health Standards",
        keywords=["osha", "workplace safety", "safety violation", "osha inspection",
                  "safety standard", "general duty clause", "lockout tagout",
                  "fall protection", "confined space", "hazard communication",
                  "personal protective equipment", "ppe", "recordkeeping 300"],
        agency="OSHA",
        cfr_references=["29 CFR 1910", "29 CFR 1926", "29 CFR 1904"],
        usc_references=["29 U.S.C. 654", "29 U.S.C. 655", "29 U.S.C. 666"],
        compliance_framework="""
OSHA WORKPLACE SAFETY COMPLIANCE FRAMEWORK:

1. GENERAL DUTY CLAUSE (Section 5(a)(1))
   - Employers must provide a workplace free from recognized hazards
     that are causing or are likely to cause death or serious physical harm
   - Applies even where no specific OSHA standard exists
   - Requires knowledge of the hazard (actual or constructive)

2. SPECIFIC STANDARDS COMPLIANCE
   - General Industry Standards (29 CFR 1910)
   - Construction Standards (29 CFR 1926)
   - Maritime Standards (29 CFR 1915-1918)
   - Agriculture Standards (29 CFR 1928)

3. RECORDKEEPING (29 CFR 1904)
   - OSHA 300 Log: Record of work-related injuries and illnesses
   - OSHA 300A: Annual summary posted February 1 - April 30
   - OSHA 301: Injury and illness incident report
   - Electronic submission required for establishments with 250+ employees
     or 20+ in high-hazard industries

4. INSPECTION AND CITATION PROCESS
   - Inspections triggered by: complaints, fatalities/catastrophes,
     referrals, programmed inspections, follow-up
   - Citation types: willful, serious, other-than-serious, repeat
   - Contest period: 15 working days from citation receipt""",
        key_requirements=[
            "Comply with all applicable OSHA standards",
            "Satisfy General Duty Clause obligations",
            "Maintain OSHA 300/300A/301 recordkeeping",
            "Report fatalities within 8 hours, hospitalizations within 24 hours",
            "Post OSHA 300A summary annually",
            "Provide required employee training",
            "Maintain safety data sheets (SDS) and hazard communication program",
        ],
        key_factors=[
            "Industry-specific hazard profile",
            "Employer size and history",
            "Citation type (willful vs. serious vs. other)",
            "Employee training adequacy",
            "Written safety program existence",
        ],
        risk_level=RiskLevel.HIGH,
        severity_score=8,
        likelihood_score=8,
        detectability_score=7,
        enforcement_history="OSHA conducts ~33,000 inspections annually. "
                           "Average penalty for serious violations ~$16,000.",
        penalty_range="Serious: up to $16,131; Willful: $11,524-$161,323; "
                      "Repeat: up to $161,323; Failure to abate: up to $16,131/day",
        criminal_exposure=True,
        required_actions=[
            "Comprehensive safety and health program",
            "Hazard assessment and control",
            "Employee safety training",
            "OSHA 300 Log maintenance",
            "Hazard communication program (HazCom/GHS)",
            "Personal protective equipment program",
            "Emergency action plan",
            "Fire prevention plan",
        ],
        documentation_required=[
            "Written safety and health program",
            "OSHA 300/300A/301 records (5-year retention)",
            "Training records with dates and content",
            "Hazard assessments",
            "Safety data sheets (SDS)",
            "Equipment inspection records",
            "Incident investigation reports",
        ],
        reporting_frequency="Annual (300A posting), event-driven (fatality/hospitalization reporting)",
        preemption_type=PreemptionType.IMPLIED_FIELD,
        state_variations=[
            "22 states and territories operate OSHA-approved state plans",
            "State plan states must be at least as effective as federal OSHA",
            "California (Cal/OSHA) has many stricter standards",
            "State plan states cover state and local government employees",
        ],
        applicable_naics=["21", "22", "23", "31", "32", "33", "42", "44", "45",
                          "48", "49", "51", "52", "53", "54", "55", "56",
                          "61", "62", "71", "72", "81"],
        entity_size_threshold="All employers with 1+ employees (some recordkeeping exemptions for <10)",
        related_doctrines=["msha_mining_safety", "workers_compensation"],
    ),

    "bsa_aml_compliance": RegulatoryDoctrineBlock(
        topic="Bank Secrecy Act / Anti-Money Laundering Compliance",
        keywords=["bsa", "aml", "anti-money laundering", "suspicious activity",
                  "sar", "ctr", "currency transaction", "know your customer",
                  "kyc", "customer due diligence", "cdd", "beneficial ownership",
                  "money laundering", "bank secrecy act", "fincen"],
        agency="FINCEN",
        cfr_references=["31 CFR 1010", "31 CFR 1020", "31 CFR 1021", "31 CFR 1022",
                        "31 CFR 1023", "31 CFR 1024", "31 CFR 1025", "31 CFR 1026"],
        usc_references=["31 U.S.C. 5311", "31 U.S.C. 5312", "31 U.S.C. 5313",
                        "31 U.S.C. 5318", "31 U.S.C. 5321", "31 U.S.C. 5322"],
        compliance_framework="""
BSA/AML COMPLIANCE FRAMEWORK:

1. AML PROGRAM REQUIREMENTS (31 CFR 1020.210)
   - Internal policies, procedures, and controls
   - Designated BSA/AML compliance officer
   - Ongoing employee training program
   - Independent testing (audit) function
   - Risk-based customer due diligence (CDD) program

2. CUSTOMER DUE DILIGENCE (CDD Rule)
   - Identify and verify customer identity (CIP)
   - Identify and verify beneficial owners (25%+ ownership)
   - Understand nature and purpose of customer relationships
   - Conduct ongoing monitoring for suspicious activity
   - Maintain and update customer information

3. REPORTING REQUIREMENTS
   - Currency Transaction Reports (CTR): cash >$10,000
   - Suspicious Activity Reports (SAR): known/suspected violations
   - CTR filing deadline: 15 calendar days
   - SAR filing deadline: 30 calendar days (60 with no suspect)
   - FBAR: Foreign bank accounts exceeding $10,000 aggregate

4. RECORD RETENTION
   - CTR and SAR copies: 5 years
   - CIP records: 5 years after account closure
   - Transaction records over $10,000: 5 years
   - Wire transfer records ($3,000+): 5 years""",
        key_requirements=[
            "Establish written AML compliance program",
            "Designate BSA/AML compliance officer",
            "Implement risk-based CDD/KYC procedures",
            "File CTRs for cash transactions exceeding $10,000",
            "File SARs for known or suspected criminal activity",
            "Conduct independent BSA/AML audits",
            "Maintain records per BSA requirements",
            "Screen against OFAC SDN list",
        ],
        key_factors=[
            "Institution type and risk profile",
            "Customer risk categorization",
            "Transaction monitoring effectiveness",
            "SAR filing timeliness and quality",
            "Training program comprehensiveness",
        ],
        risk_level=RiskLevel.CRITICAL,
        severity_score=10,
        likelihood_score=7,
        detectability_score=8,
        enforcement_history="FinCEN has assessed billions in penalties. Recent enforcement "
                           "has targeted both banks and non-bank financial institutions including "
                           "crypto exchanges.",
        penalty_range="Up to $1M per violation (civil); up to $500K fine and 10 years "
                      "imprisonment per violation (criminal); deferred prosecution agreements "
                      "in the billions",
        criminal_exposure=True,
        required_actions=[
            "Written AML/BSA compliance program",
            "Customer identification program (CIP)",
            "Beneficial ownership identification",
            "Transaction monitoring system",
            "SAR/CTR filing procedures",
            "OFAC screening procedures",
            "Employee training (role-based, annual minimum)",
            "Independent testing program",
            "Board of directors oversight",
        ],
        documentation_required=[
            "AML program documentation",
            "CIP/CDD records",
            "Beneficial ownership records",
            "SAR/CTR copies and supporting documentation",
            "Training records",
            "Audit/testing reports",
            "Board reports and minutes",
            "Risk assessment documentation",
        ],
        reporting_frequency="Transaction-driven (CTR/SAR), Annual (audit), Quarterly (board reports)",
        preemption_type=PreemptionType.SAVINGS_CLAUSE,
        state_variations=[
            "New York DFS has separate AML examination authority",
            "Some states have lower CTR thresholds",
            "State money transmitter licenses impose additional AML requirements",
            "California has additional reporting requirements for certain transactions",
        ],
        applicable_naics=["52"],
        entity_size_threshold="All financial institutions as defined in 31 U.S.C. 5312",
        related_doctrines=["ofac_sanctions", "securities_disclosure", "data_privacy"],
    ),

    "hipaa_privacy_security": RegulatoryDoctrineBlock(
        topic="HIPAA Privacy and Security Rule Compliance",
        keywords=["hipaa", "health information", "phi", "protected health information",
                  "privacy rule", "security rule", "breach notification", "minimum necessary",
                  "business associate", "baa", "health data", "medical records",
                  "patient privacy", "hitech"],
        agency="HHS",
        cfr_references=["45 CFR 160", "45 CFR 164"],
        usc_references=["42 U.S.C. 1320d", "42 U.S.C. 17931"],
        compliance_framework="""
HIPAA COMPLIANCE FRAMEWORK:

1. PRIVACY RULE (45 CFR 164 Subpart E)
   - Protects individually identifiable health information (PHI)
   - Minimum necessary standard for use and disclosure
   - Patient rights: access, amendment, accounting of disclosures
   - Notice of Privacy Practices (NPP) requirement
   - Authorization required for marketing, sale of PHI

2. SECURITY RULE (45 CFR 164 Subpart C)
   - Administrative safeguards (risk analysis, workforce training, access controls)
   - Physical safeguards (facility access, workstation security, device controls)
   - Technical safeguards (access controls, audit controls, integrity, transmission)
   - Required vs. addressable implementation specifications
   - Periodic risk assessment

3. BREACH NOTIFICATION RULE (45 CFR 164 Subpart D)
   - Breach: unauthorized acquisition, access, use, or disclosure of PHI
   - Individual notification within 60 days of discovery
   - HHS notification: annually (<500 affected), within 60 days (500+ affected)
   - Media notification for breaches affecting 500+ in a state/jurisdiction
   - Presumption of breach unless low probability of compromise

4. BUSINESS ASSOCIATE REQUIREMENTS
   - BAA required before sharing PHI with business associates
   - BAs must comply with Security Rule
   - BAs must report breaches to covered entities
   - Subcontractors of BAs also require BAAs""",
        key_requirements=[
            "Conduct risk analysis and implement risk management plan",
            "Implement Privacy and Security policies and procedures",
            "Designate Privacy Officer and Security Officer",
            "Provide workforce HIPAA training",
            "Execute Business Associate Agreements",
            "Implement breach notification procedures",
            "Maintain Notice of Privacy Practices",
            "Implement minimum necessary standard",
        ],
        key_factors=[
            "Volume and sensitivity of PHI handled",
            "Organization size and complexity",
            "Technology environment",
            "Business associate ecosystem",
            "Breach history and risk profile",
        ],
        risk_level=RiskLevel.HIGH,
        severity_score=8,
        likelihood_score=8,
        detectability_score=7,
        enforcement_history="OCR has settled/resolved 130+ HIPAA cases with corrective action. "
                           "Resolution amounts range from $31K to $16M.",
        penalty_range="Tier 1 (unknowing): $137-$68,928; Tier 2 (reasonable cause): $1,379-$68,928; "
                      "Tier 3 (willful neglect corrected): $13,785-$68,928; "
                      "Tier 4 (willful neglect uncorrected): $68,928-$2,067,813; "
                      "Annual cap $2,067,813 per identical provision",
        criminal_exposure=True,
        required_actions=[
            "Annual risk analysis",
            "Privacy and Security policies and procedures",
            "Workforce training program",
            "Business associate management program",
            "Breach detection and notification procedures",
            "Access controls and audit logging",
            "Encryption of PHI at rest and in transit",
            "Incident response plan",
        ],
        documentation_required=[
            "Risk analysis and risk management plan",
            "Policies and procedures (6-year retention)",
            "Training records",
            "Business Associate Agreements",
            "Breach notification records",
            "Sanction records",
            "System activity review records",
        ],
        reporting_frequency="Annual (risk analysis), event-driven (breach notification), "
                           "ongoing (access monitoring)",
        preemption_type=PreemptionType.SAVINGS_CLAUSE,
        state_variations=[
            "Many states have stricter health privacy laws that HIPAA does not preempt",
            "California CMIA provides additional protections",
            "Texas has breach notification within 60 days and AG notification",
            "New York SHIELD Act adds data security requirements",
            "Massachusetts 201 CMR 17.00 imposes encryption requirements",
        ],
        applicable_naics=["62", "52", "54"],
        entity_size_threshold="Covered entities and their business associates",
        related_doctrines=["data_privacy_general", "cybersecurity_requirements"],
    ),

    "employment_discrimination": RegulatoryDoctrineBlock(
        topic="Employment Discrimination and Equal Opportunity",
        keywords=["discrimination", "title vii", "ada", "adea", "eeoc",
                  "harassment", "hostile work environment", "disparate impact",
                  "disparate treatment", "reasonable accommodation",
                  "equal employment", "protected class", "retaliation"],
        agency="EEOC",
        cfr_references=["29 CFR 1600-1699"],
        usc_references=["42 U.S.C. 2000e", "42 U.S.C. 12101", "29 U.S.C. 621",
                        "29 U.S.C. 206(d)", "42 U.S.C. 2000ff"],
        compliance_framework="""
EMPLOYMENT DISCRIMINATION COMPLIANCE FRAMEWORK:

1. TITLE VII (Race, Color, Religion, Sex, National Origin)
   - Applies to employers with 15+ employees
   - Prohibits disparate treatment and disparate impact
   - Includes sexual harassment (quid pro quo and hostile environment)
   - Pregnancy Discrimination Act coverage
   - Religious accommodation requirement

2. ADA (Disability)
   - Applies to employers with 15+ employees
   - Must provide reasonable accommodation absent undue hardship
   - Interactive process required for accommodation requests
   - May not make disability-related inquiries pre-offer
   - Medical examinations permitted post-offer if applied uniformly

3. ADEA (Age 40+)
   - Applies to employers with 20+ employees
   - Protects individuals age 40 and older
   - Disparate impact claims permitted (Smith v. City of Jackson)
   - Older Workers Benefit Protection Act requirements for releases

4. EEOC CHARGE PROCESS
   - Charge must be filed within 180/300 days of discriminatory act
   - EEOC investigation and determination
   - Right-to-sue letter after EEOC process
   - Conciliation attempts before litigation""",
        key_requirements=[
            "Equal employment opportunity policy and posting",
            "Anti-harassment training for supervisors",
            "Complaint investigation procedures",
            "Reasonable accommodation interactive process",
            "EEO-1 reporting (100+ employees or federal contractors)",
            "Record retention per EEOC regulations",
            "Anti-retaliation protections",
        ],
        key_factors=[
            "Employer size (15+ for Title VII/ADA, 20+ for ADEA)",
            "Protected class involved",
            "Direct vs. circumstantial evidence",
            "Business necessity defense for disparate impact",
            "Adequacy of complaint procedures",
        ],
        risk_level=RiskLevel.HIGH,
        severity_score=7,
        likelihood_score=8,
        detectability_score=6,
        enforcement_history="EEOC receives 70,000+ charges annually. Monetary benefits "
                           "from enforcement exceed $500M annually.",
        penalty_range="Compensatory damages: varies; Punitive damages capped by employer size "
                      "(15-100 employees: $50K; 101-200: $100K; 201-500: $200K; 500+: $300K); "
                      "Back pay; Front pay; Attorney's fees",
        criminal_exposure=False,
        required_actions=[
            "Written EEO and anti-harassment policies",
            "Regular training for all employees, enhanced for supervisors",
            "Complaint investigation procedures",
            "Accommodation request process documentation",
            "EEO-1 reporting compliance",
            "Record retention program",
            "Prompt remedial action for substantiated complaints",
        ],
        documentation_required=[
            "Employment applications and hiring records (1-year retention minimum)",
            "Personnel action records",
            "Training records",
            "Complaint and investigation files",
            "Accommodation request and interactive process records",
            "EEO-1 reports",
            "Policy distribution acknowledgments",
        ],
        reporting_frequency="Annual (EEO-1), event-driven (charge responses)",
        preemption_type=PreemptionType.SAVINGS_CLAUSE,
        state_variations=[
            "Many states have broader protected classes (sexual orientation, gender identity)",
            "Some states have lower employer size thresholds",
            "State FEPA agencies handle charges concurrently with EEOC",
            "California FEHA covers employers with 5+ employees",
            "New York City covers employers with 4+ employees",
        ],
        applicable_naics=["11", "21", "22", "23", "31", "32", "33", "42", "44", "45",
                          "48", "49", "51", "52", "53", "54", "55", "56",
                          "61", "62", "71", "72", "81"],
        entity_size_threshold="15+ employees (Title VII/ADA), 20+ (ADEA)",
        related_doctrines=["flsa_wage_hour", "fmla_leave", "workplace_safety_osha"],
    ),

    "flsa_wage_hour": RegulatoryDoctrineBlock(
        topic="Fair Labor Standards Act Wage and Hour Compliance",
        keywords=["flsa", "minimum wage", "overtime", "wage and hour", "exempt",
                  "non-exempt", "salary basis", "duties test", "misclassification",
                  "independent contractor", "child labor", "tips", "tip credit",
                  "compensable time", "workweek"],
        agency="DOL",
        cfr_references=["29 CFR 778", "29 CFR 541", "29 CFR 785", "29 CFR 531"],
        usc_references=["29 U.S.C. 201-219"],
        compliance_framework="""
FLSA WAGE AND HOUR COMPLIANCE FRAMEWORK:

1. MINIMUM WAGE AND OVERTIME
   - Federal minimum wage: $7.25/hour (check state for higher)
   - Overtime: 1.5x regular rate for hours over 40 in a workweek
   - Regular rate includes all remuneration except statutory exclusions
   - Workweek is any fixed, recurring 168-hour period

2. EXEMPTION ANALYSIS (29 CFR 541)
   - Salary basis test: $684/week minimum ($35,568/year)
   - Salary level test: paid on salary basis, not hourly
   - Duties test varies by exemption category:
     * Executive: manages enterprise/department, supervises 2+ employees
     * Administrative: office work directly related to management/business operations
     * Professional: advanced knowledge in science/learning
     * Computer: computer systems analyst, programmer, software engineer
     * Outside sales: customarily and regularly away from employer's place of business
   - Highly compensated employee: $107,432+ with at least one exempt duty

3. EMPLOYEE VS. INDEPENDENT CONTRACTOR
   - Economic reality test (6 factors)
   - DOL final rule emphasis on totality of circumstances
   - Misclassification creates liability for back wages, overtime, and penalties

4. RECORDKEEPING (29 CFR 516)
   - Employee identification and basic employment data
   - Hours worked each workday and workweek
   - Total daily or weekly straight-time earnings
   - Regular hourly pay rate
   - Total overtime compensation for the workweek
   - All additions/deductions from wages
   - Total wages paid each pay period
   - Retain for 3 years (payroll); 2 years (supplementary records)""",
        key_requirements=[
            "Pay at least federal minimum wage (or state if higher)",
            "Pay overtime at 1.5x for non-exempt employees working 40+ hours",
            "Properly classify employees as exempt or non-exempt",
            "Properly classify workers as employees or independent contractors",
            "Maintain accurate time and payroll records",
            "Comply with child labor restrictions",
            "Display FLSA poster in the workplace",
        ],
        key_factors=[
            "Exempt vs. non-exempt classification accuracy",
            "Employee vs. independent contractor status",
            "Compensable time calculation",
            "Regular rate calculation methodology",
            "State wage and hour law compliance",
        ],
        risk_level=RiskLevel.HIGH,
        severity_score=7,
        likelihood_score=9,
        detectability_score=7,
        enforcement_history="WHD recovers $250M+ annually in back wages. Wage theft is "
                           "the most common employment law violation.",
        penalty_range="Back wages plus equal amount in liquidated damages; "
                      "willful violations: 3-year statute of limitations (vs. 2 years); "
                      "CMP up to $2,374 per willful/repeat violation; "
                      "child labor violations: up to $15,138 per violation",
        criminal_exposure=True,
        required_actions=[
            "Exemption classification audit",
            "Independent contractor classification review",
            "Time tracking system implementation",
            "Regular rate calculation procedures",
            "State wage law compliance review",
            "FLSA poster display",
            "Record retention program",
        ],
        documentation_required=[
            "Payroll records (3-year retention)",
            "Time records (2-year retention)",
            "Exemption classification analyses",
            "Independent contractor agreements and classification analyses",
            "Wage rate schedules",
            "Collective bargaining agreements",
        ],
        reporting_frequency="Per pay period (wage payment), ongoing (recordkeeping)",
        preemption_type=PreemptionType.SAVINGS_CLAUSE,
        state_variations=[
            "Most states have higher minimum wages than federal",
            "California requires daily overtime (8+ hours/day)",
            "Many states have stricter exemption salary thresholds",
            "Some states require more frequent pay periods",
            "State meal and rest break requirements vary widely",
        ],
        applicable_naics=["11", "21", "22", "23", "31", "32", "33", "42", "44", "45",
                          "48", "49", "51", "52", "53", "54", "55", "56",
                          "61", "62", "71", "72", "81"],
        entity_size_threshold="$500K+ annual revenue or engaged in interstate commerce",
        related_doctrines=["employment_discrimination", "workplace_safety_osha"],
    ),

    "data_privacy_general": RegulatoryDoctrineBlock(
        topic="Data Privacy and Consumer Protection Compliance",
        keywords=["data privacy", "privacy", "consumer data", "personal information",
                  "ccpa", "cpra", "gdpr", "data breach", "privacy policy",
                  "data collection", "data processing", "consent", "opt out",
                  "right to delete", "data protection", "pii", "personal data"],
        agency="FTC",
        cfr_references=["16 CFR 312", "16 CFR 314", "16 CFR 681"],
        usc_references=["15 U.S.C. 45", "15 U.S.C. 6501-6506"],
        compliance_framework="""
DATA PRIVACY COMPLIANCE FRAMEWORK:

1. FTC ACT SECTION 5 (Federal Baseline)
   - Unfair or deceptive acts or practices prohibition
   - Applies to all commercial entities
   - Deception: likely to mislead reasonable consumers + material
   - Unfairness: substantial injury not reasonably avoidable,
     not outweighed by countervailing benefits

2. STATE COMPREHENSIVE PRIVACY LAWS
   - California (CCPA/CPRA): Consumer rights + privacy agency
   - Virginia (VCDPA): Consumer data protection rights
   - Colorado (CPA): Consumer privacy rights
   - Connecticut (CTDPA): Data privacy framework
   - Additional states enacting comprehensive privacy laws annually
   - Key rights: access, delete, correct, opt-out of sale, portability

3. SECTOR-SPECIFIC FEDERAL LAWS
   - COPPA (children under 13)
   - GLBA (financial privacy)
   - FERPA (educational records)
   - HIPAA (health information)
   - VPPA (video rental records)

4. BREACH NOTIFICATION
   - All 50 states have breach notification laws
   - Triggering event: unauthorized access to unencrypted PI
   - Notification timelines: 30-90 days typically
   - AG notification required in most states
   - Content requirements vary by state""",
        key_requirements=[
            "Accurate and comprehensive privacy policy",
            "Data inventory and mapping",
            "Consent management (where required)",
            "Data subject rights fulfillment mechanisms",
            "Vendor/third-party data processing agreements",
            "Data breach response plan",
            "Data minimization practices",
            "Privacy impact assessments for high-risk processing",
        ],
        key_factors=[
            "Types and volume of personal data collected",
            "Geographic scope (which state laws apply)",
            "Industry sector (sector-specific laws)",
            "Whether data is sold or shared with third parties",
            "Consumer-facing vs. B2B data practices",
        ],
        risk_level=RiskLevel.HIGH,
        severity_score=8,
        likelihood_score=8,
        detectability_score=7,
        enforcement_history="FTC has brought 80+ privacy/security cases. State AGs "
                           "increasingly active. CCPA/CPRA enforcement accelerating.",
        penalty_range="FTC: up to $50,120/violation; CCPA: $2,500/violation, $7,500/intentional; "
                      "state AG actions: varies; private right of action for data breaches in some states",
        criminal_exposure=False,
        required_actions=[
            "Privacy policy publication and maintenance",
            "Data mapping and inventory",
            "Consumer rights request procedures",
            "Vendor data processing agreements",
            "Breach incident response plan",
            "Employee privacy training",
            "Data retention and deletion schedules",
            "Privacy impact assessments",
        ],
        documentation_required=[
            "Privacy policy (versioned)",
            "Data inventory/map",
            "Consent records",
            "Data subject rights request logs",
            "Vendor agreements with data protection terms",
            "Breach notification records",
            "Training records",
            "Privacy impact assessments",
        ],
        reporting_frequency="Event-driven (breach notification), Annual (privacy program review)",
        preemption_type=PreemptionType.NONE,
        state_variations=[
            "California CCPA/CPRA: broadest scope, $7,500/intentional violation",
            "Virginia VCDPA: AG enforcement only, no private right of action",
            "Colorado CPA: AG + DA enforcement, universal opt-out mechanism",
            "All 50 states have breach notification laws with varying requirements",
            "State laws are generally NOT preempted by federal law (no comprehensive federal privacy law)",
        ],
        applicable_naics=["51", "52", "54", "44", "45", "62", "71", "72"],
        entity_size_threshold="Varies by law; CCPA: $25M+ revenue, 100K+ consumers, 50%+ revenue from data",
        related_doctrines=["hipaa_privacy_security", "cybersecurity_requirements"],
    ),

    "ofac_sanctions": RegulatoryDoctrineBlock(
        topic="OFAC Economic Sanctions Compliance",
        keywords=["ofac", "sanctions", "sdn", "specially designated nationals",
                  "embargo", "economic sanctions", "sanctions screening",
                  "sanctions compliance", "blocked persons", "trade restrictions",
                  "iran sanctions", "russia sanctions", "china sanctions"],
        agency="OFAC",
        cfr_references=["31 CFR 501-599"],
        usc_references=["50 U.S.C. 1701-1706", "50 U.S.C. App. 1-44"],
        compliance_framework="""
OFAC SANCTIONS COMPLIANCE FRAMEWORK:

1. SANCTIONS PROGRAMS
   - Country-based programs (Iran, Cuba, North Korea, Syria, Russia/Ukraine)
   - List-based programs (SDN List, Sectoral Sanctions, Non-SDN)
   - Activity-based restrictions (WMD proliferation, terrorism, narcotics)
   - 30+ active sanctions programs administered by OFAC

2. SCREENING OBLIGATIONS
   - Screen all transactions against SDN List and other OFAC lists
   - Screen customers, counterparties, and beneficial owners
   - Real-time screening for financial institutions
   - Batch screening acceptable for non-financial companies
   - Must screen for 50% Rule (entities owned 50%+ by SDN)

3. COMPLIANCE PROGRAM ELEMENTS
   - Management commitment
   - Risk assessment
   - Internal controls (screening, blocking, rejecting)
   - Testing and auditing
   - Training

4. BLOCKING AND REPORTING
   - Block property of SDNs and blocked entities
   - Report blocked property within 10 business days (TDF 90-22.50)
   - Report rejected transactions within 10 business days
   - Maintain blocked property records for duration of blocking""",
        key_requirements=[
            "Sanctions screening of all transactions and counterparties",
            "SDN List and 50% Rule compliance",
            "Written sanctions compliance program",
            "Blocking and reporting of prohibited transactions",
            "Risk-based sanctions compliance procedures",
            "Regular sanctions list update procedures",
            "Training on sanctions requirements",
        ],
        key_factors=[
            "Industry exposure to sanctioned jurisdictions",
            "Customer/counterparty risk profile",
            "Transaction volume and complexity",
            "Geographic risk exposure",
            "Screening technology adequacy",
        ],
        risk_level=RiskLevel.CRITICAL,
        severity_score=10,
        likelihood_score=6,
        detectability_score=8,
        enforcement_history="OFAC penalties have reached billions. Strict liability "
                           "standard for civil violations. Financial institutions most at risk.",
        penalty_range="Up to $368,136 per civil violation (or twice transaction value); "
                      "criminal: up to $1M and 20 years imprisonment per willful violation",
        criminal_exposure=True,
        required_actions=[
            "Sanctions compliance program implementation",
            "Transaction and counterparty screening system",
            "SDN list update procedures",
            "50% Rule ownership analysis",
            "Blocked property management",
            "Reporting procedures (blocking reports, rejected transactions)",
            "Employee sanctions training",
            "Risk assessment and testing",
        ],
        documentation_required=[
            "Sanctions compliance policies and procedures",
            "Screening records and results",
            "Blocking reports (10 business days)",
            "Rejected transaction reports",
            "License applications and determinations",
            "Training records",
            "Audit and testing reports",
        ],
        reporting_frequency="Transaction-driven (blocking/rejection reports), Annual (audit/testing)",
        preemption_type=PreemptionType.EXPRESS,
        state_variations=[
            "Federal sanctions preempt conflicting state laws",
            "Some states have additional sanctions requirements (e.g., anti-BDS laws)",
            "State pension fund divestment requirements may overlap",
        ],
        applicable_naics=["52", "42", "48", "49", "51", "54"],
        entity_size_threshold="All U.S. persons and entities; non-U.S. persons for certain programs",
        related_doctrines=["bsa_aml_compliance"],
    ),

    "consumer_protection_ftc": RegulatoryDoctrineBlock(
        topic="FTC Consumer Protection and Advertising Compliance",
        keywords=["ftc", "consumer protection", "advertising", "false advertising",
                  "deceptive practices", "unfair practices", "endorsements",
                  "testimonials", "made in usa", "green marketing", "telemarketing",
                  "dark patterns", "subscription traps", "negative option"],
        agency="FTC",
        cfr_references=["16 CFR 255", "16 CFR 260", "16 CFR 310", "16 CFR 425"],
        usc_references=["15 U.S.C. 45", "15 U.S.C. 52", "15 U.S.C. 57b"],
        compliance_framework="""
FTC CONSUMER PROTECTION FRAMEWORK:

1. DECEPTION ANALYSIS (FTC Policy Statement on Deception)
   - Representation, omission, or practice likely to mislead
   - Evaluated from perspective of reasonable consumer
   - Representation must be material (likely to affect consumer choice)
   - Express claims presumed material
   - Implied claims assessed by overall net impression

2. UNFAIRNESS ANALYSIS (15 U.S.C. 45(n))
   - Causes or is likely to cause substantial injury to consumers
   - Injury not reasonably avoidable by consumers
   - Injury not outweighed by countervailing benefits to consumers or competition

3. ADVERTISING SUBSTANTIATION
   - Objective claims must be substantiated BEFORE making them
   - Level of substantiation = what experts in the field would consider adequate
   - Health/safety claims require competent and reliable scientific evidence
   - Comparative claims require head-to-head testing or equivalent evidence

4. ENDORSEMENTS AND TESTIMONIALS (16 CFR 255)
   - Material connections must be clearly and conspicuously disclosed
   - Endorsements must reflect honest opinions
   - Typicality: if results are not typical, must disclose generally expected results
   - Social media influencers: #ad or equivalent disclosure required""",
        key_requirements=[
            "Substantiation for all advertising claims before dissemination",
            "Clear and conspicuous disclosures for material conditions",
            "Endorsement/testimonial disclosure compliance",
            "Environmental marketing claims substantiation (Green Guides)",
            "Made in USA claims compliance",
            "Telemarketing Sales Rule compliance",
            "Negative option/subscription transparency",
        ],
        key_factors=[
            "Nature of advertising claims (express vs. implied)",
            "Level of substantiation available",
            "Consumer audience (general vs. sophisticated)",
            "Disclosure adequacy and prominence",
            "History of FTC enforcement in the industry",
        ],
        risk_level=RiskLevel.MEDIUM,
        severity_score=6,
        likelihood_score=7,
        detectability_score=6,
        enforcement_history="FTC brings 40-60 consumer protection cases annually. "
                           "Recent focus on data security, dark patterns, and influencer marketing.",
        penalty_range="Civil penalty up to $50,120 per violation; disgorgement of profits; "
                      "consumer redress; injunctive relief; corrective advertising orders",
        criminal_exposure=False,
        required_actions=[
            "Advertising review and substantiation process",
            "Endorsement and influencer compliance program",
            "Disclosure review for adequacy and conspicuousness",
            "Environmental claims review (Green Guides)",
            "Telemarketing compliance program",
            "Subscription/negative option compliance review",
            "Record retention for advertising claims",
        ],
        documentation_required=[
            "Advertising substantiation files",
            "Endorsement agreements with disclosure requirements",
            "Consumer complaint records",
            "Promotional material copies",
            "Telemarketing scripts and do-not-call records",
            "Subscription enrollment and cancellation records",
        ],
        reporting_frequency="Ongoing (advertising review), event-driven (FTC inquiries)",
        preemption_type=PreemptionType.SAVINGS_CLAUSE,
        state_variations=[
            "All states have UDAP (Unfair and Deceptive Acts and Practices) statutes",
            "Many state UDAP laws are broader than FTC Act",
            "State AG offices actively enforce consumer protection",
            "California Proposition 65 requires additional warnings",
        ],
        applicable_naics=["44", "45", "51", "52", "54", "62", "71", "72", "81"],
        entity_size_threshold="All entities engaged in commerce",
        related_doctrines=["data_privacy_general"],
    ),
}


# ============================================================================
# INDUSTRY-TO-REGULATION MAPPING
# ============================================================================

INDUSTRY_REGULATION_MAP: Dict[str, List[str]] = {
    "52": [  # Finance and Insurance
        "securities_disclosure", "bsa_aml_compliance", "ofac_sanctions",
        "data_privacy_general", "employment_discrimination", "flsa_wage_hour",
        "consumer_protection_ftc",
    ],
    "62": [  # Healthcare
        "hipaa_privacy_security", "employment_discrimination", "flsa_wage_hour",
        "workplace_safety_osha", "data_privacy_general", "consumer_protection_ftc",
    ],
    "21": [  # Mining
        "environmental_hazwaste", "workplace_safety_osha", "employment_discrimination",
        "flsa_wage_hour",
    ],
    "31": [  # Manufacturing
        "environmental_hazwaste", "workplace_safety_osha", "employment_discrimination",
        "flsa_wage_hour", "consumer_protection_ftc",
    ],
    "32": [  # Manufacturing
        "environmental_hazwaste", "workplace_safety_osha", "employment_discrimination",
        "flsa_wage_hour", "consumer_protection_ftc",
    ],
    "33": [  # Manufacturing
        "environmental_hazwaste", "workplace_safety_osha", "employment_discrimination",
        "flsa_wage_hour", "consumer_protection_ftc",
    ],
    "23": [  # Construction
        "workplace_safety_osha", "environmental_hazwaste", "employment_discrimination",
        "flsa_wage_hour",
    ],
    "44": [  # Retail
        "consumer_protection_ftc", "employment_discrimination", "flsa_wage_hour",
        "data_privacy_general", "workplace_safety_osha",
    ],
    "45": [  # Retail
        "consumer_protection_ftc", "employment_discrimination", "flsa_wage_hour",
        "data_privacy_general", "workplace_safety_osha",
    ],
    "51": [  # Information
        "data_privacy_general", "employment_discrimination", "flsa_wage_hour",
        "consumer_protection_ftc", "securities_disclosure",
    ],
    "54": [  # Professional Services
        "data_privacy_general", "employment_discrimination", "flsa_wage_hour",
        "consumer_protection_ftc",
    ],
    "72": [  # Accommodation and Food
        "flsa_wage_hour", "workplace_safety_osha", "employment_discrimination",
        "consumer_protection_ftc",
    ],
    "48": [  # Transportation
        "workplace_safety_osha", "environmental_hazwaste", "employment_discrimination",
        "flsa_wage_hour", "ofac_sanctions",
    ],
    "22": [  # Utilities
        "environmental_hazwaste", "workplace_safety_osha", "employment_discrimination",
        "flsa_wage_hour",
    ],
}


def get_applicable_doctrines(naics_code: str) -> List[str]:
    """Get applicable doctrine keys for a given NAICS sector code.

    Args:
        naics_code: NAICS code (2-6 digits). Uses first 2 digits for sector.

    Returns:
        List of doctrine keys applicable to the industry.
    """
    sector = naics_code[:2]
    doctrines = INDUSTRY_REGULATION_MAP.get(sector, [])

    # Always include universal doctrines
    universal = ["employment_discrimination", "flsa_wage_hour", "workplace_safety_osha"]
    for d in universal:
        if d not in doctrines:
            doctrines.append(d)

    return doctrines


# ============================================================================
# COMPLIANCE OBLIGATION TEMPLATES
# ============================================================================

COMPLIANCE_OBLIGATIONS: Dict[str, ComplianceObligation] = {
    "sec_10k_filing": ComplianceObligation(
        obligation_id="OBL-SEC-001",
        regulation="Securities Exchange Act Section 13",
        cfr_reference="17 CFR 240.13a-1",
        agency="SEC",
        description="Annual report on Form 10-K",
        required_actions=[
            "Prepare audited financial statements",
            "Obtain CEO/CFO SOX 302 certifications",
            "Complete SOX 404 internal control assessment",
            "File XBRL/iXBRL tagged financial data",
            "Submit via EDGAR",
        ],
        frequency="Annual",
        deadline_type="60/75/90 days after fiscal year end (by filer category)",
        applicable_industries=["52"],
        applicable_entity_sizes=["SEC reporting companies"],
        penalty_for_noncompliance="SEC enforcement action, potential delisting, officer liability",
        documentation_required=["Audited financial statements", "SOX certifications",
                                "Internal control documentation", "Board minutes"],
    ),
    "osha_300_log": ComplianceObligation(
        obligation_id="OBL-OSHA-001",
        regulation="OSHA Recordkeeping Standard",
        cfr_reference="29 CFR 1904",
        agency="OSHA",
        description="OSHA 300 Log of Work-Related Injuries and Illnesses",
        required_actions=[
            "Record all recordable injuries and illnesses on OSHA 300 Log",
            "Complete OSHA 301 Incident Report for each case",
            "Post OSHA 300A summary February 1 - April 30",
            "Submit electronic data if required (250+ employees or high-hazard 20+)",
        ],
        frequency="Ongoing with annual summary",
        deadline_type="February 1 (300A posting), March 2 (electronic submission)",
        applicable_industries=["21", "22", "23", "31", "32", "33", "42", "44", "45",
                                "48", "49", "51", "52", "53", "54", "56", "61", "62",
                                "71", "72", "81"],
        applicable_entity_sizes=["11+ employees (some exemptions for <10)"],
        penalty_for_noncompliance="Serious citation: up to $16,131 per violation",
        documentation_required=["OSHA 300 Log", "OSHA 300A Summary", "OSHA 301 Reports"],
    ),
    "eeo1_reporting": ComplianceObligation(
        obligation_id="OBL-EEOC-001",
        regulation="Title VII Executive Order 11246",
        cfr_reference="29 CFR 1602",
        agency="EEOC",
        description="Annual EEO-1 Component 1 Report",
        required_actions=[
            "Collect workforce demographic data by job category",
            "Submit EEO-1 Component 1 report via online filing system",
            "Retain copy of filing for 1 year",
        ],
        frequency="Annual",
        deadline_type="Varies (typically spring/summer filing window)",
        applicable_industries=["All sectors"],
        applicable_entity_sizes=["100+ employees or federal contractors with 50+ employees"],
        penalty_for_noncompliance="Court order compelling filing; potential loss of federal contracts",
        documentation_required=["EEO-1 report copies", "Workforce demographic data"],
    ),
    "sar_filing": ComplianceObligation(
        obligation_id="OBL-FINCEN-001",
        regulation="Bank Secrecy Act",
        cfr_reference="31 CFR 1020.320",
        agency="FINCEN",
        description="Suspicious Activity Report (SAR) filing",
        required_actions=[
            "Monitor transactions for suspicious activity",
            "Investigate potentially suspicious transactions",
            "File SAR within 30 calendar days of detection (60 if no suspect identified)",
            "Maintain SAR filing and supporting documentation for 5 years",
        ],
        frequency="Event-driven",
        deadline_type="30 calendar days (60 if no suspect identified)",
        applicable_industries=["52"],
        applicable_entity_sizes=["All financial institutions"],
        penalty_for_noncompliance="Civil penalties up to $1M per violation; criminal prosecution",
        documentation_required=["SAR filings", "Investigation records", "Supporting transaction data"],
    ),
    "hipaa_risk_analysis": ComplianceObligation(
        obligation_id="OBL-HHS-001",
        regulation="HIPAA Security Rule",
        cfr_reference="45 CFR 164.308(a)(1)(ii)(A)",
        agency="HHS",
        description="Annual HIPAA Security Risk Analysis",
        required_actions=[
            "Conduct comprehensive risk analysis of ePHI",
            "Identify threats and vulnerabilities to ePHI",
            "Assess current security measures",
            "Determine likelihood and impact of threat occurrence",
            "Document risk levels and implement risk management plan",
        ],
        frequency="Annual (minimum)",
        deadline_type="Ongoing with at least annual review",
        applicable_industries=["62", "52"],
        applicable_entity_sizes=["All covered entities and business associates"],
        penalty_for_noncompliance="HIPAA penalties: $137-$2,067,813 per violation",
        documentation_required=["Risk analysis report", "Risk management plan",
                                "Remediation tracking", "Previous analysis comparison"],
    ),
}


# ============================================================================
# DOCTRINE MATCHING LOGIC
# ============================================================================

def compute_doctrine_match_score(query_normalized: str, doctrine: RegulatoryDoctrineBlock) -> int:
    """Compute a deterministic match score between query and doctrine.

    Scoring:
        - Exact keyword match: 20 points per keyword
        - Partial keyword match (word appears in query): 10 points
        - Agency match: 15 points
        - CFR reference match: 25 points per reference

    Args:
        query_normalized: Normalized (lowercased) query text.
        doctrine: Doctrine block to score against.

    Returns:
        Integer match score. Higher is better.
    """
    score = 0
    query_lower = query_normalized.lower()

    # Keyword matching
    for keyword in doctrine.keywords:
        kw_lower = keyword.lower()
        if kw_lower in query_lower:
            score += 20
        else:
            # Check individual words
            for word in kw_lower.split():
                if len(word) > 3 and word in query_lower:
                    score += 10
                    break

    # Agency matching
    agency_lower = doctrine.agency.lower()
    if agency_lower in query_lower:
        score += 15

    # CFR reference matching
    for ref in doctrine.cfr_references:
        ref_parts = ref.lower().replace("cfr", "").strip().split()
        for part in ref_parts:
            if part in query_lower:
                score += 25
                break

    return score


def match_doctrine(query_normalized: str, min_score: int = 30) -> Optional[Dict[str, Any]]:
    """Match a normalized query to the best-fit doctrine block.

    Args:
        query_normalized: Normalized query text.
        min_score: Minimum score to consider a match.

    Returns:
        Dict with matched doctrine info, or None if no match meets threshold.
    """
    candidates: List[Dict[str, Any]] = []

    for key, doctrine in DOCTRINE_CACHE.items():
        score = compute_doctrine_match_score(query_normalized, doctrine)
        if score >= min_score:
            candidates.append({
                "doctrine_key": key,
                "topic": doctrine.topic,
                "score": score,
                "agency": doctrine.agency,
                "risk_level": doctrine.risk_level.value,
                "composite_risk_score": doctrine.composite_risk_score,
            })

    if not candidates:
        return None

    candidates.sort(key=lambda x: x["score"], reverse=True)
    best = candidates[0]

    # Compute determinism hash
    hash_input = f"{query_normalized}:{best['doctrine_key']}:{best['score']}"
    determinism_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return {
        "matched_doctrine": best["doctrine_key"],
        "topic": best["topic"],
        "score": best["score"],
        "agency": best["agency"],
        "all_candidates": candidates,
        "determinism_hash": determinism_hash,
    }


def get_doctrine(key: str) -> Optional[RegulatoryDoctrineBlock]:
    """Retrieve a specific doctrine block by key."""
    return DOCTRINE_CACHE.get(key)


def list_doctrine_keys() -> List[str]:
    """List all available doctrine keys."""
    return list(DOCTRINE_CACHE.keys())


def get_doctrine_summary() -> Dict[str, Any]:
    """Get summary statistics about the doctrine cache."""
    return {
        "version": DOCTRINE_CACHE_VERSION,
        "total_doctrines": len(DOCTRINE_CACHE),
        "total_agencies": len(set(d.agency for d in DOCTRINE_CACHE.values())),
        "total_obligations": len(COMPLIANCE_OBLIGATIONS),
        "total_enforcement_actions": len(ENFORCEMENT_ACTIONS),
        "total_preemption_rules": len(PREEMPTION_RULES),
        "total_agency_profiles": len(AGENCY_PROFILES),
        "doctrine_keys": list_doctrine_keys(),
        "agencies_covered": sorted(set(d.agency for d in DOCTRINE_CACHE.values())),
        "governance_locked": _GOVERNANCE_LOCKED,
    }
