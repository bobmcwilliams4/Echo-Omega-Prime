"""
LG05 LITIGATION RISK ENGINE - Semantic Normalization Dictionary
Deterministic preprocessing layer for litigation terminology normalization.

VERSION: 1.0.0
GOVERNANCE: FROZEN at runtime. No auto-learning. No probabilistic inference.

    RAW LITIGATION TEXT / QUERY
        |
        v
    SEMANTIC NORMALIZATION (this layer - deterministic)
        |
        v
    HASH COMPUTATION
        |
        v
    DOCTRINE MATCH / RISK SCORING

Engine: LG05 | Tier: 1 (LEGAL) | Mode: DET | Port: 8395 | Authority: 5.0
"""

from typing import Any, Dict, Tuple, List, FrozenSet, Optional
from dataclasses import dataclass
import re
import hashlib


# ============================================================================
# GOVERNANCE METADATA
# ============================================================================

SEMANTIC_VERSION = "1.0.0"
SEMANTIC_RELEASE_DATE = "2026-02-10"
TOTAL_MAPPINGS = 0  # computed at module load


@dataclass(frozen=True)
class NormalizationResult:
    """Result of semantic normalization."""
    original: str
    normalized: str
    mappings_applied: int
    text_hash: str
    version: str


# ============================================================================
# SEMANTIC MAPPING TABLES
# ============================================================================

# Civil Procedure Terms
_CIVIL_PROCEDURE_MAP: Dict[str, str] = {
    "standing to sue": "article_iii_standing",
    "standing requirement": "article_iii_standing",
    "case or controversy": "article_iii_standing",
    "injury in fact": "injury_in_fact",
    "concrete injury": "injury_in_fact",
    "particularized injury": "injury_in_fact",
    "personal jurisdiction": "personal_jurisdiction",
    "in personam jurisdiction": "personal_jurisdiction",
    "long arm jurisdiction": "personal_jurisdiction",
    "long-arm statute": "long_arm_statute",
    "minimum contacts": "minimum_contacts",
    "purposeful availment": "purposeful_availment",
    "general jurisdiction": "general_jurisdiction",
    "specific jurisdiction": "specific_jurisdiction",
    "subject matter jurisdiction": "subject_matter_jurisdiction",
    "federal question": "federal_question_jurisdiction",
    "diversity jurisdiction": "diversity_jurisdiction",
    "diversity of citizenship": "diversity_jurisdiction",
    "amount in controversy": "amount_in_controversy",
    "supplemental jurisdiction": "supplemental_jurisdiction",
    "pendent jurisdiction": "supplemental_jurisdiction",
    "ancillary jurisdiction": "supplemental_jurisdiction",
    "removal to federal court": "removal_jurisdiction",
    "remand to state court": "removal_remand",
    "venue": "venue_analysis",
    "proper venue": "venue_analysis",
    "forum non conveniens": "forum_non_conveniens",
    "forum selection clause": "forum_selection_clause",
    "transfer of venue": "venue_transfer",
    "change of venue": "venue_transfer",
    "joinder of parties": "party_joinder",
    "compulsory joinder": "compulsory_joinder",
    "permissive joinder": "permissive_joinder",
    "indispensable party": "indispensable_party",
    "necessary party": "indispensable_party",
    "intervention": "intervention",
    "interpleader": "interpleader",
    "impleader": "impleader",
    "third party claim": "impleader",
    "class action": "class_action",
    "class certification": "class_certification",
    "class representative": "named_plaintiff",
    "lead plaintiff": "named_plaintiff",
    "opt out": "class_opt_out",
    "opt in": "collective_action_opt_in",
    "statute of limitations": "statute_of_limitations",
    "limitations period": "statute_of_limitations",
    "statute of repose": "statute_of_repose",
    "discovery rule": "sol_discovery_rule",
    "tolling": "sol_tolling",
    "equitable tolling": "equitable_tolling",
    "laches": "laches_defense",
    "summary judgment": "summary_judgment",
    "motion to dismiss": "motion_to_dismiss",
    "12b6 motion": "motion_to_dismiss_failure_to_state",
    "failure to state a claim": "motion_to_dismiss_failure_to_state",
    "motion for judgment on the pleadings": "judgment_on_pleadings",
    "directed verdict": "judgment_as_matter_of_law",
    "judgment as a matter of law": "judgment_as_matter_of_law",
    "jnov": "judgment_as_matter_of_law",
    "new trial": "motion_for_new_trial",
    "remittitur": "remittitur",
    "additur": "additur",
    "appeal": "appellate_review",
    "appellate review": "appellate_review",
    "interlocutory appeal": "interlocutory_appeal",
    "mandamus": "mandamus",
    "writ of certiorari": "certiorari",
    "cert petition": "certiorari",
}

# Tort Liability Terms
_TORT_MAP: Dict[str, str] = {
    "negligence": "negligence",
    "duty of care": "duty_of_care",
    "reasonable care": "reasonable_care_standard",
    "reasonable person standard": "reasonable_care_standard",
    "breach of duty": "breach_of_duty",
    "standard of care": "standard_of_care",
    "proximate cause": "proximate_causation",
    "proximate causation": "proximate_causation",
    "but for causation": "but_for_causation",
    "cause in fact": "but_for_causation",
    "actual cause": "but_for_causation",
    "foreseeability": "foreseeability",
    "foreseeable harm": "foreseeability",
    "zone of danger": "zone_of_danger",
    "strict liability": "strict_liability",
    "abnormally dangerous activity": "abnormally_dangerous_activity",
    "ultrahazardous activity": "abnormally_dangerous_activity",
    "intentional tort": "intentional_tort",
    "assault": "assault_tort",
    "battery": "battery_tort",
    "false imprisonment": "false_imprisonment",
    "intentional infliction of emotional distress": "iied",
    "iied": "iied",
    "outrageous conduct": "iied",
    "negligent infliction of emotional distress": "nied",
    "nied": "nied",
    "trespass to land": "trespass_land",
    "trespass to chattels": "trespass_chattels",
    "conversion": "conversion_tort",
    "defamation": "defamation",
    "libel": "libel",
    "slander": "slander",
    "invasion of privacy": "invasion_of_privacy",
    "false light": "false_light",
    "public disclosure of private facts": "public_disclosure_private_facts",
    "intrusion upon seclusion": "intrusion_upon_seclusion",
    "appropriation of likeness": "appropriation_likeness",
    "fraud": "common_law_fraud",
    "fraudulent misrepresentation": "common_law_fraud",
    "negligent misrepresentation": "negligent_misrepresentation",
    "scienter": "scienter",
    "reliance": "reliance",
    "justifiable reliance": "justifiable_reliance",
    "detrimental reliance": "detrimental_reliance",
    "comparative negligence": "comparative_negligence",
    "comparative fault": "comparative_fault",
    "contributory negligence": "contributory_negligence",
    "assumption of risk": "assumption_of_risk",
    "joint and several liability": "joint_several_liability",
    "vicarious liability": "vicarious_liability",
    "respondeat superior": "respondeat_superior",
    "punitive damages": "punitive_damages",
    "exemplary damages": "punitive_damages",
    "compensatory damages": "compensatory_damages",
    "general damages": "general_damages",
    "special damages": "special_damages",
    "nominal damages": "nominal_damages",
    "loss of consortium": "loss_of_consortium",
    "wrongful death": "wrongful_death",
    "survival action": "survival_action",
}

# Contract Dispute Terms
_CONTRACT_MAP: Dict[str, str] = {
    "breach of contract": "breach_of_contract",
    "material breach": "material_breach",
    "minor breach": "minor_breach",
    "partial breach": "minor_breach",
    "total breach": "total_breach",
    "substantial performance": "substantial_performance",
    "anticipatory breach": "anticipatory_repudiation",
    "anticipatory repudiation": "anticipatory_repudiation",
    "specific performance": "specific_performance",
    "rescission": "rescission_remedy",
    "reformation": "reformation_remedy",
    "restitution": "restitution_remedy",
    "unjust enrichment": "unjust_enrichment",
    "quantum meruit": "quantum_meruit",
    "promissory estoppel": "promissory_estoppel",
    "expectation damages": "expectation_damages",
    "reliance damages": "reliance_damages",
    "consequential damages": "consequential_damages",
    "incidental damages": "incidental_damages",
    "liquidated damages": "liquidated_damages",
    "penalty clause": "penalty_clause",
    "mitigation of damages": "duty_to_mitigate",
    "duty to mitigate": "duty_to_mitigate",
    "cover damages": "cover_damages",
    "ucc": "uniform_commercial_code",
    "uniform commercial code": "uniform_commercial_code",
    "statute of frauds": "statute_of_frauds",
    "parol evidence rule": "parol_evidence_rule",
    "implied warranty": "implied_warranty",
    "express warranty": "express_warranty",
    "warranty of merchantability": "implied_warranty_merchantability",
    "warranty of fitness": "implied_warranty_fitness",
    "unconscionability": "unconscionability",
    "adhesion contract": "adhesion_contract",
    "good faith": "duty_good_faith",
    "implied covenant": "implied_covenant_good_faith",
}

# Employment Litigation Terms
_EMPLOYMENT_MAP: Dict[str, str] = {
    "wrongful termination": "wrongful_termination",
    "wrongful discharge": "wrongful_termination",
    "at will employment": "at_will_employment",
    "employment at will": "at_will_employment",
    "title vii": "title_vii",
    "title 7": "title_vii",
    "disparate treatment": "disparate_treatment",
    "disparate impact": "disparate_impact",
    "hostile work environment": "hostile_work_environment",
    "sexual harassment": "sexual_harassment",
    "quid pro quo harassment": "quid_pro_quo",
    "retaliation": "retaliation_claim",
    "whistleblower retaliation": "whistleblower_retaliation",
    "age discrimination": "adea_claim",
    "adea": "adea_claim",
    "disability discrimination": "ada_claim",
    "ada": "ada_claim",
    "reasonable accommodation": "reasonable_accommodation",
    "fmla": "fmla_claim",
    "family medical leave": "fmla_claim",
    "flsa": "flsa_claim",
    "fair labor standards act": "flsa_claim",
    "overtime": "overtime_claim",
    "minimum wage": "minimum_wage_claim",
    "exempt employee": "exempt_classification",
    "non exempt": "nonexempt_classification",
    "misclassification": "worker_misclassification",
    "independent contractor": "independent_contractor",
    "eeoc charge": "eeoc_charge",
    "right to sue letter": "eeoc_right_to_sue",
    "collective action": "flsa_collective_action",
    "non compete": "noncompete_agreement",
    "non solicitation": "nonsolicitation_agreement",
    "severance agreement": "severance_agreement",
    "garden leave": "garden_leave",
}

# Securities Litigation Terms
_SECURITIES_MAP: Dict[str, str] = {
    "securities fraud": "securities_fraud",
    "10b5": "rule_10b5",
    "10b-5": "rule_10b5",
    "rule 10b-5": "rule_10b5",
    "section 10b": "section_10b",
    "material misstatement": "material_misstatement",
    "material omission": "material_omission",
    "loss causation": "loss_causation",
    "fraud on the market": "fraud_on_the_market",
    "efficient market hypothesis": "efficient_market",
    "pslra": "pslra",
    "private securities litigation reform act": "pslra",
    "slusa": "slusa",
    "securities litigation uniform standards act": "slusa",
    "safe harbor": "forward_looking_safe_harbor",
    "forward looking statement": "forward_looking_statement",
    "insider trading": "insider_trading",
    "section 16": "section_16",
    "regulation fd": "regulation_fd",
    "d and o insurance": "d_and_o_insurance",
    "directors and officers": "d_and_o_insurance",
    "derivative action": "derivative_action",
    "shareholder derivative": "derivative_action",
    "demand futility": "demand_futility",
    "business judgment rule": "business_judgment_rule",
    "fiduciary duty": "fiduciary_duty",
    "duty of loyalty": "duty_of_loyalty",
    "duty of care": "duty_of_care_corporate",
    "entire fairness": "entire_fairness",
    "sec enforcement": "sec_enforcement",
    "disgorgement": "disgorgement_remedy",
}

# Antitrust Terms
_ANTITRUST_MAP: Dict[str, str] = {
    "antitrust": "antitrust",
    "sherman act": "sherman_act",
    "section 1 sherman": "sherman_section_1",
    "section 2 sherman": "sherman_section_2",
    "clayton act": "clayton_act",
    "ftc act": "ftc_act",
    "price fixing": "price_fixing",
    "bid rigging": "bid_rigging",
    "market allocation": "market_allocation",
    "group boycott": "group_boycott",
    "tying arrangement": "tying_arrangement",
    "exclusive dealing": "exclusive_dealing",
    "monopolization": "monopolization",
    "attempted monopolization": "attempted_monopolization",
    "market power": "market_power",
    "relevant market": "relevant_market",
    "per se illegal": "per_se_violation",
    "rule of reason": "rule_of_reason",
    "quick look": "quick_look_analysis",
    "treble damages": "treble_damages",
    "merger challenge": "merger_antitrust",
    "hhi": "herfindahl_index",
}

# IP Litigation Terms
_IP_MAP: Dict[str, str] = {
    "patent infringement": "patent_infringement",
    "literal infringement": "literal_infringement",
    "doctrine of equivalents": "doctrine_of_equivalents",
    "claim construction": "claim_construction",
    "markman hearing": "markman_hearing",
    "prior art": "prior_art",
    "obviousness": "obviousness_103",
    "novelty": "novelty_102",
    "patent eligibility": "patent_eligibility_101",
    "inter partes review": "ipr",
    "ipr": "ipr",
    "ptab": "ptab",
    "reasonable royalty": "reasonable_royalty",
    "lost profits": "lost_profits_damages",
    "willful infringement": "willful_infringement",
    "enhanced damages": "enhanced_damages",
    "injunctive relief": "injunctive_relief",
    "preliminary injunction": "preliminary_injunction",
    "permanent injunction": "permanent_injunction",
    "trade secret": "trade_secret",
    "misappropriation": "trade_secret_misappropriation",
    "dtsa": "defend_trade_secrets_act",
    "defend trade secrets act": "defend_trade_secrets_act",
    "inevitable disclosure": "inevitable_disclosure",
    "trademark infringement": "trademark_infringement",
    "likelihood of confusion": "likelihood_of_confusion",
    "trademark dilution": "trademark_dilution",
    "trade dress": "trade_dress",
    "lanham act": "lanham_act",
    "copyright infringement": "copyright_infringement",
    "fair use": "fair_use_defense",
    "dmca": "dmca",
}

# Environmental Litigation Terms
_ENVIRONMENTAL_MAP: Dict[str, str] = {
    "cercla": "cercla",
    "superfund": "cercla",
    "prp": "potentially_responsible_party",
    "potentially responsible party": "potentially_responsible_party",
    "hazardous substance": "hazardous_substance",
    "clean water act": "clean_water_act",
    "cwa": "clean_water_act",
    "clean air act": "clean_air_act",
    "npdes": "npdes_permit",
    "rcra": "rcra",
    "resource conservation": "rcra",
    "toxic tort": "toxic_tort",
    "environmental contamination": "environmental_contamination",
    "remediation": "environmental_remediation",
    "consent decree": "consent_decree",
    "supplemental environmental project": "sep",
    "innocent landowner": "innocent_landowner_defense",
    "bona fide prospective purchaser": "bfpp_defense",
}

# Products Liability Terms
_PRODUCTS_MAP: Dict[str, str] = {
    "products liability": "products_liability",
    "product liability": "products_liability",
    "design defect": "design_defect",
    "manufacturing defect": "manufacturing_defect",
    "failure to warn": "failure_to_warn",
    "inadequate warning": "failure_to_warn",
    "consumer expectations test": "consumer_expectations_test",
    "risk utility test": "risk_utility_test",
    "reasonable alternative design": "reasonable_alternative_design",
    "crashworthiness": "crashworthiness",
    "learned intermediary": "learned_intermediary_doctrine",
    "product recall": "product_recall",
    "mdl": "multidistrict_litigation",
    "mass tort": "mass_tort",
    "bellwether trial": "bellwether_trial",
}

# Insurance Terms
_INSURANCE_MAP: Dict[str, str] = {
    "duty to defend": "duty_to_defend",
    "duty to indemnify": "duty_to_indemnify",
    "insurance coverage": "insurance_coverage",
    "coverage dispute": "insurance_coverage_dispute",
    "bad faith": "insurance_bad_faith",
    "reservation of rights": "reservation_of_rights",
    "eight corners rule": "eight_corners_rule",
    "four corners rule": "eight_corners_rule",
    "cgl": "commercial_general_liability",
    "commercial general liability": "commercial_general_liability",
    "occurrence": "occurrence_coverage",
    "claims made": "claims_made_coverage",
    "subrogation": "subrogation",
    "equitable subrogation": "equitable_subrogation",
    "additional insured": "additional_insured",
    "excess insurance": "excess_insurance",
    "umbrella policy": "umbrella_policy",
    "self insured retention": "self_insured_retention",
    "deductible": "insurance_deductible",
    "exclusion": "policy_exclusion",
    "intentional act exclusion": "intentional_act_exclusion",
    "pollution exclusion": "pollution_exclusion",
    "professional liability": "professional_liability_insurance",
    "errors and omissions": "errors_omissions_insurance",
}

# Discovery and Litigation Cost Terms
_DISCOVERY_MAP: Dict[str, str] = {
    "discovery": "discovery_process",
    "e discovery": "e_discovery",
    "ediscovery": "e_discovery",
    "electronically stored information": "esi",
    "esi": "esi",
    "document production": "document_production",
    "interrogatories": "interrogatories",
    "requests for admission": "requests_for_admission",
    "deposition": "deposition",
    "subpoena": "subpoena",
    "subpoena duces tecum": "subpoena_duces_tecum",
    "protective order": "protective_order",
    "privilege log": "privilege_log",
    "attorney client privilege": "attorney_client_privilege",
    "work product doctrine": "work_product_doctrine",
    "proportionality": "discovery_proportionality",
    "spoliation": "spoliation",
    "litigation hold": "litigation_hold",
    "preservation obligation": "preservation_obligation",
    "sanctions": "discovery_sanctions",
    "adverse inference": "adverse_inference_instruction",
    "expert witness": "expert_witness",
    "daubert motion": "daubert_challenge",
    "daubert challenge": "daubert_challenge",
    "frye standard": "frye_standard",
}


# ============================================================================
# UNIFIED MAPPING TABLE
# ============================================================================

SEMANTIC_MAP: Dict[str, str] = {}
for _map in [
    _CIVIL_PROCEDURE_MAP, _TORT_MAP, _CONTRACT_MAP, _EMPLOYMENT_MAP,
    _SECURITIES_MAP, _ANTITRUST_MAP, _IP_MAP, _ENVIRONMENTAL_MAP,
    _PRODUCTS_MAP, _INSURANCE_MAP, _DISCOVERY_MAP,
]:
    SEMANTIC_MAP.update(_map)

TOTAL_MAPPINGS = len(SEMANTIC_MAP)

# Compile regex patterns (word boundary matching)
_COMPILED_PATTERNS: List[Tuple[re.Pattern, str]] = []
for raw_term, canonical in sorted(SEMANTIC_MAP.items(), key=lambda x: -len(x[0])):
    pattern = re.compile(r"\b" + re.escape(raw_term) + r"\b", re.IGNORECASE)
    _COMPILED_PATTERNS.append((pattern, canonical))

# Frozen set of all canonical terms
CANONICAL_TERMS: FrozenSet[str] = frozenset(SEMANTIC_MAP.values())


# ============================================================================
# NORMALIZATION FUNCTIONS
# ============================================================================

def normalize_semantics(text: str) -> NormalizationResult:
    """Apply deterministic semantic normalization to litigation text.

    Args:
        text: Raw input text to normalize.

    Returns:
        NormalizationResult with normalized text and metadata.
    """
    if not text or not text.strip():
        empty_hash = hashlib.sha256(b"").hexdigest()[:16]
        return NormalizationResult(
            original=text,
            normalized="",
            mappings_applied=0,
            text_hash=empty_hash,
            version=SEMANTIC_VERSION,
        )

    original = text
    normalized = text.lower().strip()
    normalized = re.sub(r"\s+", " ", normalized)
    mappings_applied = 0

    for pattern, canonical in _COMPILED_PATTERNS:
        match = pattern.search(normalized)
        if match:
            already_normalized = canonical in normalized
            if not already_normalized:
                normalized = pattern.sub(canonical, normalized)
                mappings_applied += 1

    text_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]

    return NormalizationResult(
        original=original,
        normalized=normalized,
        mappings_applied=mappings_applied,
        text_hash=text_hash,
        version=SEMANTIC_VERSION,
    )


def compute_text_hash(text: str) -> str:
    """Compute SHA-256 hash of text for determinism verification."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_map_metadata() -> Dict[str, Any]:
    """Return metadata about the semantic mapping table."""
    category_counts = {
        "civil_procedure": len(_CIVIL_PROCEDURE_MAP),
        "tort_liability": len(_TORT_MAP),
        "contract_dispute": len(_CONTRACT_MAP),
        "employment": len(_EMPLOYMENT_MAP),
        "securities": len(_SECURITIES_MAP),
        "antitrust": len(_ANTITRUST_MAP),
        "ip_litigation": len(_IP_MAP),
        "environmental": len(_ENVIRONMENTAL_MAP),
        "products_liability": len(_PRODUCTS_MAP),
        "insurance": len(_INSURANCE_MAP),
        "discovery": len(_DISCOVERY_MAP),
    }
    return {
        "version": SEMANTIC_VERSION,
        "total_mappings": TOTAL_MAPPINGS,
        "unique_canonical_terms": len(CANONICAL_TERMS),
        "categories": category_counts,
        "release_date": SEMANTIC_RELEASE_DATE,
    }


def lock_governance() -> Dict[str, str]:
    """Return governance lock state for integrity verification."""
    full_map_str = json.dumps(SEMANTIC_MAP, sort_keys=True)
    integrity_hash = hashlib.sha256(full_map_str.encode("utf-8")).hexdigest()
    return {
        "version": SEMANTIC_VERSION,
        "total_mappings": str(TOTAL_MAPPINGS),
        "integrity_hash": integrity_hash,
        "frozen": "true",
        "auto_learning": "disabled",
    }


def verify_integrity(expected_hash: Optional[str] = None) -> bool:
    """Verify the integrity of the semantic map has not been modified."""
    import json as _json
    full_map_str = _json.dumps(SEMANTIC_MAP, sort_keys=True)
    current_hash = hashlib.sha256(full_map_str.encode("utf-8")).hexdigest()
    if expected_hash is None:
        return True
    return current_hash == expected_hash


def get_canonical_for_term(term: str) -> Optional[str]:
    """Look up the canonical form for a raw litigation term."""
    lower = term.lower().strip()
    return SEMANTIC_MAP.get(lower)


def get_all_terms_for_canonical(canonical: str) -> List[str]:
    """Find all raw terms that map to a given canonical form."""
    return [k for k, v in SEMANTIC_MAP.items() if v == canonical]


# Required for lock_governance
import json
