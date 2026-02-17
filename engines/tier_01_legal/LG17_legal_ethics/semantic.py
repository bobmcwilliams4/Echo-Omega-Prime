"""
LG17 Legal Ethics Engine - Semantic Normalization Module
=========================================================
Deterministic semantic normalization for legal ethics queries.

Maps natural language ethics terms to canonical identifiers.
Handles Model Rule references, disciplinary terms, privilege terminology,
conflict-of-interest concepts, fee terminology, and practice area mapping.

Includes:
    - NormalizationResult: Full provenance of normalization
    - SemanticNormalizer: Rule-based term normalization engine
    - ConflictChecker: Deterministic conflict-of-interest screening
    - PrivilegeAnalyzer: Attorney-client privilege / work product analysis
    - FeeReasonablenessCalculator: Rule 1.5(a) factor-based fee analysis

Rules:
    - Purely deterministic (no ML, no vectors, no embeddings)
    - Case-insensitive matching
    - Longest-match-first for multi-word terms
    - Returns NormalizationResult with full provenance
    - No side effects, no state mutation

Port: 8407
Engine: LG17 Legal Ethics
Version: 2.0.0
"""

from __future__ import annotations

import hashlib
import re
import time
from dataclasses import dataclass, field as dc_field
from enum import Enum
from typing import Any, ClassVar, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization on a query."""
    original_query: str
    normalized_query: str
    mappings_applied: List[Dict[str, str]] = dc_field(default_factory=list)
    rules_detected: List[str] = dc_field(default_factory=list)
    ethics_domains: List[str] = dc_field(default_factory=list)
    privilege_indicators: List[str] = dc_field(default_factory=list)
    conflict_indicators: List[str] = dc_field(default_factory=list)
    discipline_indicators: List[str] = dc_field(default_factory=list)
    jurisdiction_detected: str = ""
    confidence_boost: float = 0.0
    normalization_hash: str = ""
    duration_ms: float = 0.0

    def __post_init__(self) -> None:
        if not self.normalization_hash:
            content = f"{self.original_query}|{self.normalized_query}|{len(self.mappings_applied)}"
            self.normalization_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


# ============================================================================
# RULE NORMALIZATION MAP
# ============================================================================

RULE_SYNONYMS: Dict[str, str] = {
    # Competence / Diligence / Communication
    "competence": "RULE_1_1",
    "rule 1.1": "RULE_1_1",
    "model rule 1.1": "RULE_1_1",
    "legal competence": "RULE_1_1",
    "technology competence": "RULE_1_1_TECH",
    "scope of representation": "RULE_1_2",
    "rule 1.2": "RULE_1_2",
    "limited scope representation": "RULE_1_2_C",
    "unbundled legal services": "RULE_1_2_C",
    "diligence": "RULE_1_3",
    "rule 1.3": "RULE_1_3",
    "neglect": "RULE_1_3",
    "client neglect": "RULE_1_3",
    "promptness": "RULE_1_3",
    "communication": "RULE_1_4",
    "rule 1.4": "RULE_1_4",
    "inform client": "RULE_1_4",
    "keep client informed": "RULE_1_4",
    "informed consent": "RULE_1_4",
    # Fees
    "fees": "RULE_1_5",
    "rule 1.5": "RULE_1_5",
    "fee agreement": "RULE_1_5",
    "reasonable fee": "RULE_1_5_A",
    "unreasonable fee": "RULE_1_5_A",
    "excessive fee": "RULE_1_5_A",
    "contingency fee": "RULE_1_5_C",
    "contingent fee": "RULE_1_5_C",
    "fee splitting": "RULE_1_5_E",
    "fee division": "RULE_1_5_E",
    "referral fee": "RULE_1_5_E",
    "hourly rate": "RULE_1_5",
    "flat fee": "RULE_1_5",
    "retainer": "RULE_1_5",
    "advance fee deposit": "RULE_1_5",
    # Confidentiality
    "confidentiality": "RULE_1_6",
    "rule 1.6": "RULE_1_6",
    "client confidences": "RULE_1_6",
    "client secrets": "RULE_1_6",
    "information relating to representation": "RULE_1_6",
    "disclosure exception": "RULE_1_6_B",
    "prevent death or bodily harm": "RULE_1_6_B_1",
    "prevent financial injury": "RULE_1_6_B_2",
    # Conflicts
    "conflict of interest": "RULE_1_7",
    "conflicts of interest": "RULE_1_7",
    "rule 1.7": "RULE_1_7",
    "concurrent conflict": "RULE_1_7",
    "direct adversity": "RULE_1_7_A_1",
    "material limitation": "RULE_1_7_A_2",
    "conflict waiver": "RULE_1_7_B",
    "nonconsentable conflict": "RULE_1_7",
    "hot potato doctrine": "RULE_1_7",
    "rule 1.8": "RULE_1_8",
    "business transaction with client": "RULE_1_8_A",
    "literary rights": "RULE_1_8_D",
    "financial assistance to client": "RULE_1_8_E",
    "aggregate settlement": "RULE_1_8_G",
    "prospective malpractice waiver": "RULE_1_8_H",
    "sexual relations with client": "RULE_1_8_J",
    "former client": "RULE_1_9",
    "rule 1.9": "RULE_1_9",
    "successive conflict": "RULE_1_9",
    "substantially related": "RULE_1_9",
    "imputed conflict": "RULE_1_10",
    "imputation": "RULE_1_10",
    "rule 1.10": "RULE_1_10",
    "ethical wall": "RULE_1_10",
    "chinese wall": "RULE_1_10",
    "screening": "RULE_1_10",
    "lateral hire": "RULE_1_10",
    "government officers": "RULE_1_11",
    "rule 1.11": "RULE_1_11",
    "revolving door": "RULE_1_11",
    "former government lawyer": "RULE_1_11",
    # Organization / Diminished Capacity
    "organization as client": "RULE_1_13",
    "rule 1.13": "RULE_1_13",
    "corporate counsel": "RULE_1_13",
    "up the ladder": "RULE_1_13",
    "reporting out": "RULE_1_13_C",
    "upjohn warning": "RULE_1_13",
    "corporate miranda": "RULE_1_13",
    "diminished capacity": "RULE_1_14",
    "rule 1.14": "RULE_1_14",
    "incapacitated client": "RULE_1_14",
    "protective action": "RULE_1_14",
    # Trust Accounts
    "trust account": "RULE_1_15",
    "rule 1.15": "RULE_1_15",
    "iolta": "RULE_1_15",
    "client funds": "RULE_1_15",
    "commingling": "RULE_1_15",
    "conversion of client funds": "RULE_1_15",
    "safekeeping": "RULE_1_15",
    "escrow": "RULE_1_15",
    # Withdrawal
    "withdrawal": "RULE_1_16",
    "rule 1.16": "RULE_1_16",
    "declining representation": "RULE_1_16",
    "mandatory withdrawal": "RULE_1_16_A",
    "permissive withdrawal": "RULE_1_16_B",
    "retaining lien": "RULE_1_16",
    "charging lien": "RULE_1_16",
    # Privilege
    "attorney-client privilege": "PRIVILEGE_AC",
    "attorney client privilege": "PRIVILEGE_AC",
    "privilege": "PRIVILEGE_AC",
    "privileged communication": "PRIVILEGE_AC",
    "upjohn": "PRIVILEGE_UPJOHN",
    "crime-fraud exception": "PRIVILEGE_CRIME_FRAUD",
    "crime fraud exception": "PRIVILEGE_CRIME_FRAUD",
    "work product": "WORK_PRODUCT",
    "work product doctrine": "WORK_PRODUCT",
    "hickman": "WORK_PRODUCT_HICKMAN",
    "hickman v taylor": "WORK_PRODUCT_HICKMAN",
    "opinion work product": "WORK_PRODUCT_OPINION",
    "fact work product": "WORK_PRODUCT_FACT",
    "anticipation of litigation": "WORK_PRODUCT",
    # Advocate
    "candor toward tribunal": "RULE_3_3",
    "rule 3.3": "RULE_3_3",
    "false statement to court": "RULE_3_3",
    "adverse authority": "RULE_3_3_A_2",
    "false evidence": "RULE_3_3_A_3",
    "perjury": "RULE_3_3",
    "fairness to opposing party": "RULE_3_4",
    "rule 3.4": "RULE_3_4",
    "trial publicity": "RULE_3_6",
    "rule 3.6": "RULE_3_6",
    "lawyer as witness": "RULE_3_7",
    "rule 3.7": "RULE_3_7",
    "advocate-witness": "RULE_3_7",
    "prosecutorial ethics": "RULE_3_8",
    "rule 3.8": "RULE_3_8",
    "prosecutor duties": "RULE_3_8",
    "exculpatory evidence": "BRADY",
    "brady": "BRADY",
    "brady v maryland": "BRADY",
    "brady violation": "BRADY",
    "giglio": "BRADY_GIGLIO",
    "impeachment evidence": "BRADY_GIGLIO",
    # Transactions with Others
    "truthfulness": "RULE_4_1",
    "rule 4.1": "RULE_4_1",
    "false statement to third person": "RULE_4_1",
    "no-contact rule": "RULE_4_2",
    "no contact rule": "RULE_4_2",
    "rule 4.2": "RULE_4_2",
    "communicating with represented person": "RULE_4_2",
    "unrepresented person": "RULE_4_3",
    "rule 4.3": "RULE_4_3",
    # Supervision
    "supervision": "RULE_5_1",
    "rule 5.1": "RULE_5_1",
    "supervisory responsibility": "RULE_5_1",
    "nonlawyer assistant": "RULE_5_3",
    "rule 5.3": "RULE_5_3",
    "professional independence": "RULE_5_4",
    "rule 5.4": "RULE_5_4",
    "fee sharing with non-lawyer": "RULE_5_4_A",
    "unauthorized practice of law": "RULE_5_5",
    "upl": "RULE_5_5",
    "rule 5.5": "RULE_5_5",
    "multijurisdictional practice": "RULE_5_5",
    "mjp": "RULE_5_5",
    "pro hac vice": "RULE_5_5",
    # Advertising / Solicitation
    "advertising": "RULE_7_1",
    "rule 7.1": "RULE_7_1",
    "lawyer advertising": "RULE_7_1",
    "false or misleading": "RULE_7_1",
    "solicitation": "RULE_7_3",
    "rule 7.3": "RULE_7_3",
    "ambulance chasing": "RULE_7_3",
    "barratry": "BARRATRY",
    # Discipline
    "reporting misconduct": "RULE_8_3",
    "rule 8.3": "RULE_8_3",
    "himmel": "RULE_8_3",
    "duty to report": "RULE_8_3",
    "misconduct": "RULE_8_4",
    "rule 8.4": "RULE_8_4",
    "dishonesty": "RULE_8_4_C",
    "fraud": "RULE_8_4_C",
    "deceit": "RULE_8_4_C",
    "conduct prejudicial": "RULE_8_4_D",
    "discipline": "DISCIPLINE",
    "disbarment": "DISCIPLINE_DISBARMENT",
    "suspension": "DISCIPLINE_SUSPENSION",
    "reprimand": "DISCIPLINE_REPRIMAND",
    "censure": "DISCIPLINE_REPRIMAND",
    "admonition": "DISCIPLINE_ADMONITION",
    "grievance": "DISCIPLINE",
    "sanctions": "DISCIPLINE",
    # Malpractice
    "malpractice": "MALPRACTICE",
    "legal malpractice": "MALPRACTICE",
    "standard of care": "MALPRACTICE",
    "case within a case": "MALPRACTICE",
    "suit within a suit": "MALPRACTICE",
    "breach of fiduciary duty": "FIDUCIARY",
    "fiduciary duty": "FIDUCIARY",
    "fee forfeiture": "FIDUCIARY",
    "disgorgement": "FIDUCIARY",
    # Judicial / ADR
    "judicial ethics": "CJC",
    "code of judicial conduct": "CJC",
    "recusal": "CJC_DISQUALIFICATION",
    "disqualification": "CJC_DISQUALIFICATION",
    "ex parte communication": "CJC_EX_PARTE",
    "mediator ethics": "MEDIATOR",
    "mediation ethics": "MEDIATOR",
    "arbitrator disclosure": "ARBITRATOR",
    "evident partiality": "ARBITRATOR",
    # SOX / Regulatory
    "sarbanes-oxley": "SOX_205",
    "sarbanes oxley": "SOX_205",
    "sox": "SOX_205",
    "sec part 205": "SOX_205",
    "section 307": "SOX_205",
    # Legal Tech / AI
    "ai ethics": "LEGAL_TECH_AI",
    "artificial intelligence": "LEGAL_TECH_AI",
    "chatgpt": "LEGAL_TECH_AI",
    "legal technology": "LEGAL_TECH_AI",
    "ghost-writing": "GHOST_WRITING",
    "ghostwriting": "GHOST_WRITING",
    "metadata": "METADATA_ETHICS",
    "tracked changes": "METADATA_ETHICS",
    "social media": "SOCIAL_MEDIA",
    "linkedin": "SOCIAL_MEDIA",
    # Texas
    "texas disciplinary rules": "TX_DRPC",
    "tdrpc": "TX_DRPC",
    "texas bar": "TX_DRPC",
    "texas grievance": "TX_DRPC",
}

# Domains detected from normalized tokens
DOMAIN_MAP: Dict[str, str] = {
    "RULE_1_1": "competence",
    "RULE_1_1_TECH": "competence",
    "RULE_1_2": "scope_of_representation",
    "RULE_1_2_C": "limited_scope",
    "RULE_1_3": "diligence",
    "RULE_1_4": "communication",
    "RULE_1_5": "fees",
    "RULE_1_5_A": "fees",
    "RULE_1_5_C": "contingency_fees",
    "RULE_1_5_E": "fee_splitting",
    "RULE_1_6": "confidentiality",
    "RULE_1_6_B": "confidentiality_exceptions",
    "RULE_1_6_B_1": "confidentiality_exceptions",
    "RULE_1_6_B_2": "confidentiality_exceptions",
    "RULE_1_7": "conflicts",
    "RULE_1_7_A_1": "conflicts",
    "RULE_1_7_A_2": "conflicts",
    "RULE_1_7_B": "conflicts",
    "RULE_1_8": "conflicts_current_client",
    "RULE_1_8_A": "conflicts_current_client",
    "RULE_1_8_D": "conflicts_current_client",
    "RULE_1_8_E": "conflicts_current_client",
    "RULE_1_8_G": "conflicts_current_client",
    "RULE_1_8_H": "conflicts_current_client",
    "RULE_1_8_J": "conflicts_current_client",
    "RULE_1_9": "former_client_conflicts",
    "RULE_1_10": "imputed_conflicts",
    "RULE_1_11": "government_conflicts",
    "RULE_1_13": "organization_as_client",
    "RULE_1_13_C": "reporting_out",
    "RULE_1_14": "diminished_capacity",
    "RULE_1_15": "trust_accounts",
    "RULE_1_16": "withdrawal",
    "RULE_1_16_A": "mandatory_withdrawal",
    "RULE_1_16_B": "permissive_withdrawal",
    "PRIVILEGE_AC": "attorney_client_privilege",
    "PRIVILEGE_UPJOHN": "corporate_privilege",
    "PRIVILEGE_CRIME_FRAUD": "crime_fraud_exception",
    "WORK_PRODUCT": "work_product",
    "WORK_PRODUCT_HICKMAN": "work_product",
    "WORK_PRODUCT_OPINION": "work_product",
    "WORK_PRODUCT_FACT": "work_product",
    "RULE_3_3": "candor_toward_tribunal",
    "RULE_3_3_A_2": "adverse_authority",
    "RULE_3_3_A_3": "false_evidence",
    "RULE_3_4": "fairness_opposing",
    "RULE_3_6": "trial_publicity",
    "RULE_3_7": "lawyer_as_witness",
    "RULE_3_8": "prosecutorial_ethics",
    "BRADY": "brady_obligations",
    "BRADY_GIGLIO": "brady_obligations",
    "RULE_4_1": "truthfulness",
    "RULE_4_2": "no_contact_rule",
    "RULE_4_3": "unrepresented_persons",
    "RULE_5_1": "supervision",
    "RULE_5_3": "nonlawyer_supervision",
    "RULE_5_4": "professional_independence",
    "RULE_5_4_A": "fee_sharing_nonlawyer",
    "RULE_5_5": "unauthorized_practice",
    "RULE_7_1": "advertising",
    "RULE_7_3": "solicitation",
    "BARRATRY": "barratry",
    "RULE_8_3": "reporting_misconduct",
    "RULE_8_4": "lawyer_misconduct",
    "RULE_8_4_C": "dishonesty",
    "RULE_8_4_D": "prejudicial_conduct",
    "DISCIPLINE": "discipline",
    "DISCIPLINE_DISBARMENT": "disbarment",
    "DISCIPLINE_SUSPENSION": "suspension",
    "DISCIPLINE_REPRIMAND": "reprimand",
    "DISCIPLINE_ADMONITION": "admonition",
    "MALPRACTICE": "malpractice",
    "FIDUCIARY": "fiduciary_duty",
    "CJC": "judicial_ethics",
    "CJC_DISQUALIFICATION": "judicial_disqualification",
    "CJC_EX_PARTE": "ex_parte",
    "MEDIATOR": "mediator_ethics",
    "ARBITRATOR": "arbitrator_ethics",
    "SOX_205": "sarbanes_oxley",
    "LEGAL_TECH_AI": "legal_tech",
    "GHOST_WRITING": "ghost_writing",
    "METADATA_ETHICS": "metadata_ethics",
    "SOCIAL_MEDIA": "social_media_ethics",
    "TX_DRPC": "texas_disciplinary",
}

# Jurisdiction detection patterns
JURISDICTION_PATTERNS: Dict[str, str] = {
    "texas": "TX",
    "new york": "NY",
    "california": "CA",
    "florida": "FL",
    "illinois": "IL",
    "pennsylvania": "PA",
    "ohio": "OH",
    "georgia": "GA",
    "north carolina": "NC",
    "michigan": "MI",
    "new jersey": "NJ",
    "virginia": "VA",
    "washington": "WA",
    "arizona": "AZ",
    "massachusetts": "MA",
    "federal": "FEDERAL",
    "aba model": "ABA_MODEL",
    "aba": "ABA_MODEL",
    "district of columbia": "DC",
    "d.c.": "DC",
}


# ============================================================================
# SEMANTIC NORMALIZER
# ============================================================================

class SemanticNormalizer:
    """Rule-based semantic normalizer for legal ethics queries."""

    def __init__(self) -> None:
        self._sorted_keys = sorted(RULE_SYNONYMS.keys(), key=len, reverse=True)
        self._jurisdiction_keys = sorted(
            JURISDICTION_PATTERNS.keys(), key=len, reverse=True
        )
        logger.info(
            f"SemanticNormalizer initialized: {len(self._sorted_keys)} rules, "
            f"{len(self._jurisdiction_keys)} jurisdictions"
        )

    def normalize(self, query: str) -> NormalizationResult:
        """Normalize a query, returning full provenance."""
        start = time.time()
        result = NormalizationResult(
            original_query=query,
            normalized_query=query,
        )
        lower = query.lower()

        # Detect jurisdiction
        for pattern in self._jurisdiction_keys:
            if pattern in lower:
                result.jurisdiction_detected = JURISDICTION_PATTERNS[pattern]
                result.confidence_boost += 0.05
                break

        # Normalize terms (longest match first)
        normalized = lower
        for key in self._sorted_keys:
            if key in normalized:
                canonical = RULE_SYNONYMS[key]
                result.mappings_applied.append({"from": key, "to": canonical})
                result.rules_detected.append(canonical)

                domain = DOMAIN_MAP.get(canonical, "")
                if domain and domain not in result.ethics_domains:
                    result.ethics_domains.append(domain)

                # Classify indicators
                if canonical.startswith("PRIVILEGE_") or canonical.startswith("WORK_PRODUCT"):
                    if canonical not in result.privilege_indicators:
                        result.privilege_indicators.append(canonical)
                elif canonical.startswith("RULE_1_7") or canonical.startswith("RULE_1_9") or canonical.startswith("RULE_1_10") or canonical.startswith("RULE_1_11"):
                    if canonical not in result.conflict_indicators:
                        result.conflict_indicators.append(canonical)
                elif canonical.startswith("DISCIPLINE") or canonical.startswith("RULE_8_"):
                    if canonical not in result.discipline_indicators:
                        result.discipline_indicators.append(canonical)

                normalized = normalized.replace(key, canonical, 1)
                result.confidence_boost += 0.03

        result.normalized_query = normalized
        result.confidence_boost = min(result.confidence_boost, 0.25)
        result.duration_ms = (time.time() - start) * 1000

        # Recompute hash
        content = f"{result.original_query}|{result.normalized_query}|{len(result.mappings_applied)}"
        result.normalization_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

        return result


# ============================================================================
# CONFLICT CHECKER
# ============================================================================

class ConflictType(str, Enum):
    """Types of conflicts of interest."""
    CONCURRENT_DIRECT = "concurrent_direct_adversity"
    CONCURRENT_LIMITATION = "concurrent_material_limitation"
    SUCCESSIVE = "successive_substantially_related"
    IMPUTED = "imputed_firm_wide"
    GOVERNMENT = "government_revolving_door"
    PERSONAL_INTEREST = "personal_interest"
    BUSINESS_TRANSACTION = "business_transaction_with_client"


@dataclass
class ConflictCheckResult:
    """Result of a conflict-of-interest screening."""
    conflict_found: bool
    conflict_type: Optional[ConflictType] = None
    parties_involved: List[str] = dc_field(default_factory=list)
    rule_applicable: str = ""
    consentable: bool = True
    consent_requirements: List[str] = dc_field(default_factory=list)
    screening_available: bool = False
    risk_level: str = "low"
    analysis: str = ""
    recommendations: List[str] = dc_field(default_factory=list)


class ConflictChecker:
    """Deterministic conflict-of-interest screening engine."""

    RISK_KEYWORDS_HIGH: FrozenSet[str] = frozenset([
        "opposing party", "adverse party", "same matter", "same transaction",
        "same litigation", "directly adverse", "co-defendant", "cross-claim",
    ])
    RISK_KEYWORDS_MEDIUM: FrozenSet[str] = frozenset([
        "former client", "substantially related", "lateral hire", "prior firm",
        "related matter", "similar industry", "competing interests",
    ])
    RISK_KEYWORDS_LOW: FrozenSet[str] = frozenset([
        "different matter", "unrelated", "different jurisdiction",
        "different practice area", "no overlap",
    ])

    def check(
        self,
        current_client: str,
        prospective_client: str,
        matter_description: str,
        prior_representations: Optional[List[str]] = None,
    ) -> ConflictCheckResult:
        """Run a deterministic conflict screen."""
        lower_matter = matter_description.lower()
        prior = [p.lower() for p in (prior_representations or [])]

        # Check for direct adversity (Rule 1.7(a)(1))
        if current_client.lower() in lower_matter and prospective_client.lower() in lower_matter:
            return ConflictCheckResult(
                conflict_found=True,
                conflict_type=ConflictType.CONCURRENT_DIRECT,
                parties_involved=[current_client, prospective_client],
                rule_applicable="Model Rule 1.7(a)(1)",
                consentable=self._is_consentable_concurrent(lower_matter),
                consent_requirements=[
                    "Informed consent confirmed in writing from each affected client",
                    "Lawyer must reasonably believe competent and diligent representation of each client is possible",
                    "Representation must not be prohibited by law",
                    "Must not involve assertion of claim by one client against another in same proceeding",
                ],
                risk_level="high",
                analysis=(
                    f"Direct adversity detected between current client '{current_client}' "
                    f"and prospective client '{prospective_client}' in the same matter."
                ),
                recommendations=[
                    "Conduct full conflicts analysis under Rule 1.7",
                    "Determine if the conflict is consentable",
                    "If consentable, obtain informed consent confirmed in writing from all affected clients",
                    "Consider whether competent representation is possible despite the conflict",
                    "Document the conflicts analysis and all waivers obtained",
                ],
            )

        # Check for successive conflict (Rule 1.9)
        prospective_lower = prospective_client.lower()
        for rep in prior:
            if prospective_lower in rep or any(
                kw in lower_matter for kw in self.RISK_KEYWORDS_MEDIUM
            ):
                return ConflictCheckResult(
                    conflict_found=True,
                    conflict_type=ConflictType.SUCCESSIVE,
                    parties_involved=[prospective_client],
                    rule_applicable="Model Rule 1.9(a)",
                    consentable=True,
                    consent_requirements=[
                        "Informed consent confirmed in writing from the former client",
                    ],
                    screening_available=True,
                    risk_level="medium",
                    analysis=(
                        f"Potential successive conflict: prospective client '{prospective_client}' "
                        f"may be adverse to a former client in a substantially related matter."
                    ),
                    recommendations=[
                        "Apply the 'substantially related' test (Analytica v. NPD Research)",
                        "Determine whether confidential information from the prior representation is relevant",
                        "If conflict exists, seek informed consent from the former client or implement screening",
                    ],
                )

        # Risk keyword analysis
        risk = "low"
        for kw in self.RISK_KEYWORDS_HIGH:
            if kw in lower_matter:
                risk = "high"
                break
        if risk == "low":
            for kw in self.RISK_KEYWORDS_MEDIUM:
                if kw in lower_matter:
                    risk = "medium"
                    break

        return ConflictCheckResult(
            conflict_found=False,
            risk_level=risk,
            analysis=(
                f"No conflict detected between '{current_client}' and '{prospective_client}'. "
                f"Risk level: {risk}."
            ),
            recommendations=[
                "Document the conflict check and its results",
                "Re-screen if new parties or facts emerge",
                "Update the conflict database with the new engagement",
            ],
        )

    def _is_consentable_concurrent(self, matter_text: str) -> bool:
        """Determine if a concurrent conflict is consentable."""
        nonconsentable_indicators = [
            "same litigation", "same proceeding", "assert claim against",
            "opposing parties in same case",
        ]
        for indicator in nonconsentable_indicators:
            if indicator in matter_text:
                return False
        return True


# ============================================================================
# PRIVILEGE ANALYZER
# ============================================================================

class PrivilegeType(str, Enum):
    """Types of privilege."""
    ATTORNEY_CLIENT = "attorney_client_privilege"
    WORK_PRODUCT_FACT = "work_product_fact"
    WORK_PRODUCT_OPINION = "work_product_opinion"
    JOINT_DEFENSE = "joint_defense_privilege"
    COMMON_INTEREST = "common_interest_doctrine"


@dataclass
class PrivilegeAnalysisResult:
    """Result of a privilege analysis."""
    privilege_likely: bool
    privilege_type: Optional[PrivilegeType] = None
    elements_met: List[str] = dc_field(default_factory=list)
    elements_missing: List[str] = dc_field(default_factory=list)
    exceptions_applicable: List[str] = dc_field(default_factory=list)
    waiver_risk: str = "low"
    analysis: str = ""
    recommendations: List[str] = dc_field(default_factory=list)


class PrivilegeAnalyzer:
    """Deterministic attorney-client privilege / work product analyzer."""

    AC_ELEMENTS: List[str] = [
        "communication",
        "between_privileged_persons",
        "in_confidence",
        "for_legal_advice",
    ]

    WP_ELEMENTS: List[str] = [
        "document_or_tangible_thing",
        "prepared_by_party_or_representative",
        "in_anticipation_of_litigation",
    ]

    def analyze_privilege(
        self,
        description: str,
        communication_type: str = "",
        parties_involved: Optional[List[str]] = None,
        purpose: str = "",
    ) -> PrivilegeAnalysisResult:
        """Analyze whether a communication is likely privileged."""
        lower = description.lower()
        elements_met: List[str] = []
        elements_missing: List[str] = []
        exceptions: List[str] = []

        # Check AC privilege elements
        if any(w in lower for w in ["communicated", "told", "asked", "discussed", "consulted", "email", "letter", "conversation"]):
            elements_met.append("communication")
        else:
            elements_missing.append("communication")

        if any(w in lower for w in ["attorney", "lawyer", "counsel", "law firm"]):
            elements_met.append("between_privileged_persons")
        else:
            elements_missing.append("between_privileged_persons")

        if any(w in lower for w in ["confidential", "private", "secret", "in confidence"]):
            elements_met.append("in_confidence")
        elif any(w in lower for w in ["public", "third party", "cc'd others", "shared with"]):
            elements_missing.append("in_confidence")
        else:
            elements_met.append("in_confidence")  # Presumed unless rebutted

        if any(w in lower for w in ["legal advice", "legal opinion", "legal question", "legal matter", "litigation", "lawsuit", "claim"]):
            elements_met.append("for_legal_advice")
        elif any(w in lower for w in ["business advice", "business decision", "financial advice", "tax advice"]):
            elements_missing.append("for_legal_advice")
        else:
            elements_missing.append("for_legal_advice")

        # Check exceptions
        if any(w in lower for w in ["crime", "fraud", "ongoing crime", "future crime", "illegal scheme"]):
            exceptions.append("crime_fraud_exception")
        if any(w in lower for w in ["waived", "disclosed", "shared publicly", "forwarded to third party"]):
            exceptions.append("waiver")
        if any(w in lower for w in ["fee dispute", "malpractice claim", "controversy between lawyer and client"]):
            exceptions.append("self_defense_exception")

        all_met = len(elements_missing) == 0
        privilege_likely = all_met and len(exceptions) == 0

        waiver_risk = "low"
        if any(w in lower for w in ["forwarded", "shared", "disclosed to third party"]):
            waiver_risk = "high"
        elif any(w in lower for w in ["cc", "copied", "multiple recipients"]):
            waiver_risk = "medium"

        return PrivilegeAnalysisResult(
            privilege_likely=privilege_likely,
            privilege_type=PrivilegeType.ATTORNEY_CLIENT if all_met else None,
            elements_met=elements_met,
            elements_missing=elements_missing,
            exceptions_applicable=exceptions,
            waiver_risk=waiver_risk,
            analysis=(
                f"{'Privilege likely applies' if privilege_likely else 'Privilege may not apply'}. "
                f"Elements met: {len(elements_met)}/{len(self.AC_ELEMENTS)}. "
                f"Exceptions: {', '.join(exceptions) if exceptions else 'none'}."
            ),
            recommendations=self._build_recommendations(elements_missing, exceptions, waiver_risk),
        )

    def _build_recommendations(
        self,
        missing: List[str],
        exceptions: List[str],
        waiver_risk: str,
    ) -> List[str]:
        """Build practice recommendations based on analysis."""
        recs: List[str] = []
        if "for_legal_advice" in missing:
            recs.append(
                "Clarify whether the communication was made for the purpose of obtaining "
                "or providing legal (not business) advice"
            )
        if "in_confidence" in missing:
            recs.append(
                "Determine whether the communication was made in confidence and not disclosed "
                "to third parties outside the privilege"
            )
        if "crime_fraud_exception" in exceptions:
            recs.append(
                "The crime-fraud exception may apply. Conduct an in camera review analysis "
                "under United States v. Zolin"
            )
        if waiver_risk == "high":
            recs.append(
                "There is a significant risk of waiver. Review FRE 502(b) for inadvertent "
                "disclosure protections and assess whether a claw-back agreement is in place"
            )
        if not recs:
            recs.append("Privilege analysis appears straightforward; document and preserve the analysis")
        return recs


# ============================================================================
# FEE REASONABLENESS CALCULATOR
# ============================================================================

@dataclass
class FeeReasonablenessResult:
    """Result of a fee reasonableness analysis under Rule 1.5(a)."""
    reasonable: bool
    score: float  # 0.0-1.0
    factors: Dict[str, Dict[str, Any]] = dc_field(default_factory=dict)
    analysis: str = ""
    recommendations: List[str] = dc_field(default_factory=list)


class FeeReasonablenessCalculator:
    """Rule 1.5(a) eight-factor fee reasonableness analysis."""

    FACTORS: List[str] = [
        "time_and_labor",
        "preclusion_of_other_employment",
        "customary_fee",
        "amount_involved_results",
        "time_limitations",
        "professional_relationship",
        "experience_reputation",
        "fixed_or_contingent",
    ]

    def analyze(
        self,
        fee_amount: float,
        hours_worked: float = 0.0,
        hourly_rate: float = 0.0,
        matter_type: str = "",
        matter_complexity: str = "moderate",
        jurisdiction: str = "TX",
        results_obtained: str = "",
        lawyer_experience_years: int = 10,
        is_contingent: bool = False,
        contingent_percentage: float = 0.0,
    ) -> FeeReasonablenessResult:
        """Analyze fee reasonableness under the eight Rule 1.5(a) factors."""
        factors: Dict[str, Dict[str, Any]] = {}
        total_score = 0.0

        # Factor 1: Time and labor
        if hours_worked > 0 and hourly_rate > 0:
            implied_rate = fee_amount / hours_worked if hours_worked > 0 else 0
            rate_ratio = implied_rate / hourly_rate if hourly_rate > 0 else 1.0
            f1_score = max(0, min(1.0, 2.0 - rate_ratio))
        else:
            f1_score = 0.5
        factors["time_and_labor"] = {
            "score": round(f1_score, 2),
            "description": "Time and labor required, novelty and difficulty, skill requisite",
        }
        total_score += f1_score

        # Factor 2: Preclusion
        f2_score = 0.7 if matter_complexity in ("high", "complex") else 0.5
        factors["preclusion_of_other_employment"] = {
            "score": round(f2_score, 2),
            "description": "Likelihood the acceptance precludes other employment",
        }
        total_score += f2_score

        # Factor 3: Customary fee
        f3_score = 0.6  # Neutral without market data
        factors["customary_fee"] = {
            "score": round(f3_score, 2),
            "description": f"Customary fee in {jurisdiction} for similar services",
        }
        total_score += f3_score

        # Factor 4: Amount involved and results
        if results_obtained:
            f4_score = 0.8 if "favorable" in results_obtained.lower() else 0.5
        else:
            f4_score = 0.5
        factors["amount_involved_results"] = {
            "score": round(f4_score, 2),
            "description": "Amount involved and results obtained",
        }
        total_score += f4_score

        # Factor 5: Time limitations
        f5_score = 0.6
        factors["time_limitations"] = {
            "score": round(f5_score, 2),
            "description": "Time limitations imposed by client or circumstances",
        }
        total_score += f5_score

        # Factor 6: Professional relationship
        f6_score = 0.6
        factors["professional_relationship"] = {
            "score": round(f6_score, 2),
            "description": "Nature and length of professional relationship with client",
        }
        total_score += f6_score

        # Factor 7: Experience
        if lawyer_experience_years >= 20:
            f7_score = 0.9
        elif lawyer_experience_years >= 10:
            f7_score = 0.7
        elif lawyer_experience_years >= 5:
            f7_score = 0.5
        else:
            f7_score = 0.3
        factors["experience_reputation"] = {
            "score": round(f7_score, 2),
            "description": f"Experience ({lawyer_experience_years} years), reputation, and ability",
        }
        total_score += f7_score

        # Factor 8: Fixed or contingent
        if is_contingent:
            f8_score = 0.7 if contingent_percentage <= 40 else 0.4
        else:
            f8_score = 0.6
        factors["fixed_or_contingent"] = {
            "score": round(f8_score, 2),
            "description": "Whether the fee is fixed or contingent",
        }
        total_score += f8_score

        avg_score = total_score / 8.0
        reasonable = avg_score >= 0.45

        return FeeReasonablenessResult(
            reasonable=reasonable,
            score=round(avg_score, 3),
            factors=factors,
            analysis=(
                f"Fee of ${fee_amount:,.2f} scores {avg_score:.3f}/1.000 on the "
                f"Rule 1.5(a) eight-factor analysis. "
                f"{'Fee appears reasonable.' if reasonable else 'Fee may be unreasonable — further review recommended.'}"
            ),
            recommendations=self._build_fee_recommendations(avg_score, factors, is_contingent),
        )

    def _build_fee_recommendations(
        self,
        score: float,
        factors: Dict[str, Dict[str, Any]],
        is_contingent: bool,
    ) -> List[str]:
        """Build fee recommendations."""
        recs: List[str] = []
        if score < 0.45:
            recs.append("The fee may be unreasonable under Rule 1.5(a). Consider reducing the fee or providing additional justification.")
        if is_contingent:
            recs.append("Ensure the contingency fee agreement is in writing, signed by the client, and states the method of calculation (Rule 1.5(c)).")
        recs.append("Maintain contemporaneous time records even for flat-fee and contingency matters.")
        recs.append("Communicate the basis of the fee to the client preferably in writing before or within a reasonable time after commencing representation (Rule 1.5(b)).")
        return recs


# ============================================================================
# MODULE-LEVEL SINGLETON
# ============================================================================

_normalizer: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get or create the global normalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = SemanticNormalizer()
    return _normalizer


def normalize_semantics(query: str) -> NormalizationResult:
    """Convenience: normalize a query."""
    return get_normalizer().normalize(query)
