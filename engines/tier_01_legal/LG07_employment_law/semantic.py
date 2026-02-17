"""
LG07 Employment Law Engine - Semantic Normalization Module
============================================================
Normalizes employment law terminology, maps colloquial terms to legal
canonical forms, handles statute references, agency acronyms, and
claim type variations across all major federal employment statutes.

Components:
    - SEMANTIC_MAP: Core term normalization dictionary
    - normalize_query(): Main entry point for query normalization
    - Employment Statute Classifier
    - Colloquial-to-Legal Term Mapper
    - Agency Acronym Resolver
    - Claim Type Normalizer
    - Texas Labor Code Mapper

Version: 1.0.0
Engine: LG07 Employment Law
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# SEMANTIC MAP - EMPLOYMENT LAW TERMINOLOGY NORMALIZATION
# ============================================================================

SEMANTIC_MAP: Dict[str, Dict[str, Any]] = {
    # ---- TITLE VII / DISCRIMINATION ----
    "discrimination": {
        "canonical": "employment_discrimination",
        "synonyms": ["bias", "prejudice", "unfair treatment", "treated differently",
                     "singled out", "picked on", "targeted"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "race_discrimination": {
        "canonical": "racial_discrimination_title_vii",
        "synonyms": ["racial bias", "color discrimination", "racism at work",
                     "treated differently because of race", "racial profiling at work"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "sex_discrimination": {
        "canonical": "sex_discrimination_title_vii",
        "synonyms": ["gender discrimination", "gender bias", "sexism",
                     "treated differently because of sex", "glass ceiling",
                     "gender pay gap", "sex stereotyping"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "religious_discrimination": {
        "canonical": "religious_discrimination_title_vii",
        "synonyms": ["religious bias", "faith discrimination", "cant wear hijab",
                     "forced to work on sabbath", "religious accommodation denied"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "national_origin_discrimination": {
        "canonical": "national_origin_discrimination_title_vii",
        "synonyms": ["national origin bias", "ethnicity discrimination", "accent discrimination",
                     "english only rule", "immigrant discrimination", "citizenship discrimination"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "pregnancy_discrimination": {
        "canonical": "pregnancy_discrimination_pda",
        "synonyms": ["pregnant fired", "maternity discrimination", "pregnancy leave denied",
                     "fired for being pregnant", "pregnancy accommodation", "PDA violation"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "disparate_treatment": {
        "canonical": "disparate_treatment_claim",
        "synonyms": ["intentional discrimination", "treated differently", "direct discrimination",
                     "individual discrimination", "differential treatment"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "disparate_impact": {
        "canonical": "disparate_impact_claim",
        "synonyms": ["unintentional discrimination", "neutral policy discrimination",
                     "adverse impact", "four fifths rule", "80 percent rule",
                     "facially neutral policy"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "bfoq": {
        "canonical": "bona_fide_occupational_qualification",
        "synonyms": ["bfoq defense", "job qualification defense", "bona fide qualification",
                     "legitimate job requirement"],
        "category": "title_vii",
        "weight": 0.9,
    },
    "hostile_work_environment": {
        "canonical": "hostile_work_environment_harassment",
        "synonyms": ["hostile workplace", "toxic work environment", "abusive workplace",
                     "harassment environment", "pervasive harassment",
                     "severe or pervasive conduct"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "quid_pro_quo": {
        "canonical": "quid_pro_quo_harassment",
        "synonyms": ["sexual favors for job", "this for that harassment",
                     "sleep with boss", "sex for promotion", "tangible employment action"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "sexual_harassment": {
        "canonical": "sexual_harassment_title_vii",
        "synonyms": ["sexual misconduct", "inappropriate touching at work",
                     "unwanted sexual advances", "sexual comments at work",
                     "me too", "metoo", "#metoo"],
        "category": "title_vii",
        "weight": 1.0,
    },
    "retaliation": {
        "canonical": "employment_retaliation",
        "synonyms": ["retaliated against", "punished for complaining", "got back at me",
                     "fired for reporting", "demoted for filing complaint",
                     "reprisal", "adverse action for protected activity"],
        "category": "title_vii",
        "weight": 1.0,
    },

    # ---- ADA / DISABILITY ----
    "disability_discrimination": {
        "canonical": "disability_discrimination_ada",
        "synonyms": ["ada violation", "disabled worker", "handicap discrimination",
                     "disability bias", "treated differently for disability",
                     "impairment discrimination"],
        "category": "ada",
        "weight": 1.0,
    },
    "reasonable_accommodation": {
        "canonical": "reasonable_accommodation_ada",
        "synonyms": ["accommodation request", "need accommodation", "workplace adjustment",
                     "modified duties", "modified schedule", "assistive technology",
                     "telework as accommodation", "work from home accommodation"],
        "category": "ada",
        "weight": 1.0,
    },
    "interactive_process": {
        "canonical": "interactive_process_ada",
        "synonyms": ["accommodation discussion", "interactive dialogue",
                     "good faith interactive process", "failed to engage in interactive process"],
        "category": "ada",
        "weight": 0.9,
    },
    "undue_hardship": {
        "canonical": "undue_hardship_defense_ada",
        "synonyms": ["too expensive accommodation", "cant afford accommodation",
                     "accommodation too difficult", "significant difficulty or expense"],
        "category": "ada",
        "weight": 0.9,
    },
    "essential_functions": {
        "canonical": "essential_job_functions_ada",
        "synonyms": ["core job duties", "fundamental job functions", "primary job duties",
                     "cant perform essential functions", "unable to do the job"],
        "category": "ada",
        "weight": 0.9,
    },
    "regarded_as_disabled": {
        "canonical": "regarded_as_disabled_ada",
        "synonyms": ["perceived disability", "thought I was disabled",
                     "treated as disabled", "perceived as having impairment"],
        "category": "ada",
        "weight": 0.9,
    },

    # ---- ADEA / AGE ----
    "age_discrimination": {
        "canonical": "age_discrimination_adea",
        "synonyms": ["adea violation", "too old", "age bias", "forced out because of age",
                     "age 40 and over", "older worker", "replaced by younger",
                     "overqualified", "not a cultural fit age"],
        "category": "adea",
        "weight": 1.0,
    },
    "age_harassment": {
        "canonical": "age_based_harassment",
        "synonyms": ["old jokes at work", "age comments", "dinosaur comments",
                     "over the hill jokes", "too old to learn"],
        "category": "adea",
        "weight": 0.9,
    },
    "rif_age": {
        "canonical": "reduction_in_force_age_impact",
        "synonyms": ["layoff targeting older workers", "restructuring age bias",
                     "downsizing older employees", "age based layoff"],
        "category": "adea",
        "weight": 1.0,
    },

    # ---- FMLA / LEAVE ----
    "fmla_leave": {
        "canonical": "fmla_protected_leave",
        "synonyms": ["family leave", "medical leave", "fmla", "family medical leave",
                     "12 weeks leave", "unpaid medical leave", "fmla request"],
        "category": "fmla",
        "weight": 1.0,
    },
    "fmla_interference": {
        "canonical": "fmla_interference_claim",
        "synonyms": ["denied fmla", "cant take fmla", "leave denied",
                     "fmla request denied", "not allowed to take leave",
                     "discouraged from taking leave"],
        "category": "fmla",
        "weight": 1.0,
    },
    "fmla_retaliation": {
        "canonical": "fmla_retaliation_claim",
        "synonyms": ["fired after fmla", "terminated after medical leave",
                     "punished for taking leave", "demoted after fmla",
                     "negative review after leave"],
        "category": "fmla",
        "weight": 1.0,
    },
    "intermittent_leave": {
        "canonical": "fmla_intermittent_leave",
        "synonyms": ["sporadic leave", "occasional medical absence",
                     "periodic fmla", "reduced schedule fmla"],
        "category": "fmla",
        "weight": 0.9,
    },
    "serious_health_condition": {
        "canonical": "serious_health_condition_fmla",
        "synonyms": ["qualifying condition", "fmla qualifying illness",
                     "chronic condition", "inpatient care", "continuing treatment"],
        "category": "fmla",
        "weight": 0.9,
    },

    # ---- FLSA / WAGE & HOUR ----
    "overtime_pay": {
        "canonical": "flsa_overtime_compensation",
        "synonyms": ["overtime", "ot pay", "time and a half", "overtime violation",
                     "not paid overtime", "unpaid overtime", "over 40 hours",
                     "working off the clock overtime"],
        "category": "flsa",
        "weight": 1.0,
    },
    "minimum_wage": {
        "canonical": "flsa_minimum_wage",
        "synonyms": ["min wage", "minimum pay", "below minimum wage",
                     "subminimum wage", "federal minimum", "not paid minimum"],
        "category": "flsa",
        "weight": 1.0,
    },
    "exempt_employee": {
        "canonical": "flsa_exempt_classification",
        "synonyms": ["exempt status", "salary exempt", "not eligible for overtime",
                     "exempt from overtime", "white collar exemption",
                     "executive exemption", "administrative exemption",
                     "professional exemption", "computer exemption",
                     "outside sales exemption"],
        "category": "flsa",
        "weight": 1.0,
    },
    "nonexempt_employee": {
        "canonical": "flsa_nonexempt_classification",
        "synonyms": ["non-exempt", "hourly worker", "eligible for overtime",
                     "overtime eligible", "hourly employee"],
        "category": "flsa",
        "weight": 1.0,
    },
    "misclassification": {
        "canonical": "worker_misclassification",
        "synonyms": ["classified wrong", "should be employee", "misclassified",
                     "independent contractor misclassification", "1099 but really employee",
                     "employee vs contractor", "abc test", "economic reality test"],
        "category": "flsa",
        "weight": 1.0,
    },
    "off_the_clock": {
        "canonical": "off_the_clock_work_flsa",
        "synonyms": ["working off the clock", "unpaid work", "working without pay",
                     "donning and doffing", "pre-shift work", "post-shift work",
                     "checking email at home unpaid"],
        "category": "flsa",
        "weight": 1.0,
    },
    "tip_credit": {
        "canonical": "flsa_tip_credit",
        "synonyms": ["tip credit violation", "tipped employee", "tip pooling",
                     "tip sharing", "server wages", "tipped minimum wage"],
        "category": "flsa",
        "weight": 0.9,
    },
    "comp_time": {
        "canonical": "compensatory_time_flsa",
        "synonyms": ["comp time", "time off instead of overtime",
                     "compensatory time off", "comp time private sector"],
        "category": "flsa",
        "weight": 0.9,
    },

    # ---- OSHA / SAFETY ----
    "workplace_safety": {
        "canonical": "osha_workplace_safety",
        "synonyms": ["osha violation", "unsafe working conditions", "safety hazard",
                     "dangerous workplace", "osha complaint", "safety violation",
                     "general duty clause"],
        "category": "osha",
        "weight": 1.0,
    },
    "osha_retaliation": {
        "canonical": "osha_whistleblower_retaliation",
        "synonyms": ["fired for safety complaint", "punished for osha report",
                     "retaliation for safety concern", "section 11c violation"],
        "category": "osha",
        "weight": 1.0,
    },
    "osha_citation": {
        "canonical": "osha_citation_enforcement",
        "synonyms": ["osha fine", "osha penalty", "serious violation",
                     "willful violation", "repeat violation", "other than serious"],
        "category": "osha",
        "weight": 0.9,
    },

    # ---- ERISA / BENEFITS ----
    "erisa_benefits": {
        "canonical": "erisa_employee_benefits",
        "synonyms": ["benefits denial", "pension denied", "401k issue",
                     "retirement benefits", "health plan denial", "benefit plan violation",
                     "erisa violation", "fiduciary duty benefits"],
        "category": "erisa",
        "weight": 1.0,
    },
    "erisa_interference": {
        "canonical": "erisa_interference_claim",
        "synonyms": ["fired before vesting", "terminated to avoid pension",
                     "fired before retirement", "benefits interference",
                     "section 510 violation"],
        "category": "erisa",
        "weight": 1.0,
    },

    # ---- NLRA / LABOR RELATIONS ----
    "union_activity": {
        "canonical": "nlra_protected_concerted_activity",
        "synonyms": ["union organizing", "collective bargaining", "union rights",
                     "section 7 rights", "concerted activity", "protected activity nlra",
                     "right to organize", "joining a union"],
        "category": "nlra",
        "weight": 1.0,
    },
    "unfair_labor_practice": {
        "canonical": "unfair_labor_practice_nlra",
        "synonyms": ["ulp", "employer unfair labor practice", "union busting",
                     "interfering with union", "nlrb charge", "section 8 violation"],
        "category": "nlra",
        "weight": 1.0,
    },

    # ---- TERMINATION ----
    "fired": {
        "canonical": "employment_termination",
        "synonyms": ["terminated", "let go", "dismissed", "discharged", "sacked",
                     "canned", "axed", "pink slipped", "given walking papers",
                     "shown the door", "laid off", "riffed"],
        "category": "termination",
        "weight": 1.0,
    },
    "wrongful_termination": {
        "canonical": "wrongful_termination_claim",
        "synonyms": ["wrongful discharge", "wrongful firing", "illegal termination",
                     "unfair termination", "unjust dismissal", "fired illegally",
                     "fired without cause"],
        "category": "termination",
        "weight": 1.0,
    },
    "constructive_discharge": {
        "canonical": "constructive_discharge_claim",
        "synonyms": ["forced to quit", "made to resign", "quit because of conditions",
                     "intolerable working conditions", "forced resignation",
                     "no choice but to quit"],
        "category": "termination",
        "weight": 1.0,
    },
    "at_will_employment": {
        "canonical": "at_will_employment_doctrine",
        "synonyms": ["at will", "employment at will", "fire for any reason",
                     "no employment contract", "terminable at will"],
        "category": "termination",
        "weight": 1.0,
    },
    "public_policy_exception": {
        "canonical": "public_policy_exception_at_will",
        "synonyms": ["fired for reporting crime", "fired for jury duty",
                     "fired for refusing illegal act", "public policy wrongful discharge"],
        "category": "termination",
        "weight": 0.9,
    },

    # ---- NON-COMPETE / RESTRICTIVE COVENANTS ----
    "non_compete": {
        "canonical": "non_compete_agreement",
        "synonyms": ["non-compete", "noncompete", "covenant not to compete",
                     "non compete clause", "restrictive covenant", "competition ban",
                     "cant work for competitor"],
        "category": "non_compete",
        "weight": 1.0,
    },
    "non_solicitation": {
        "canonical": "non_solicitation_agreement",
        "synonyms": ["non-solicitation", "nonsolicitation", "cant contact clients",
                     "client non-solicit", "employee non-solicit"],
        "category": "non_compete",
        "weight": 0.9,
    },
    "trade_secret_employment": {
        "canonical": "trade_secret_protection_employment",
        "synonyms": ["trade secrets", "confidential information", "proprietary info",
                     "nda employment", "confidentiality agreement", "dtsa"],
        "category": "non_compete",
        "weight": 0.9,
    },

    # ---- WORKERS COMP ----
    "workers_compensation": {
        "canonical": "workers_compensation_claim",
        "synonyms": ["workers comp", "work comp", "on the job injury",
                     "workplace injury", "injured at work", "work related injury",
                     "occupational injury", "comp claim"],
        "category": "workers_comp",
        "weight": 1.0,
    },
    "workers_comp_retaliation": {
        "canonical": "workers_comp_retaliation_claim",
        "synonyms": ["fired for filing workers comp", "retaliation comp claim",
                     "punished for work injury", "terminated after workers comp"],
        "category": "workers_comp",
        "weight": 1.0,
    },

    # ---- WARN ACT ----
    "warn_act": {
        "canonical": "warn_act_mass_layoff",
        "synonyms": ["mass layoff", "plant closing", "plant shutdown",
                     "60 day notice", "warn notice", "mass termination",
                     "warn act violation", "no layoff notice"],
        "category": "warn_act",
        "weight": 1.0,
    },

    # ---- WHISTLEBLOWER ----
    "whistleblower": {
        "canonical": "whistleblower_protection",
        "synonyms": ["blowing the whistle", "reported violations", "reported fraud",
                     "sarbanes oxley whistleblower", "dodd frank whistleblower",
                     "qui tam", "false claims act"],
        "category": "whistleblower",
        "weight": 1.0,
    },

    # ---- TEXAS LABOR CODE ----
    "texas_payday_law": {
        "canonical": "texas_payday_law_ch61",
        "synonyms": ["texas final paycheck", "texas last paycheck", "texas wage claim",
                     "twc wage claim", "texas workforce commission complaint",
                     "chapter 61 labor code"],
        "category": "texas_labor",
        "weight": 1.0,
    },
    "texas_anti_retaliation": {
        "canonical": "texas_anti_retaliation_ch451",
        "synonyms": ["texas workers comp retaliation", "chapter 451",
                     "texas retaliation workers comp"],
        "category": "texas_labor",
        "weight": 1.0,
    },
    "texas_whistleblower_act": {
        "canonical": "texas_whistleblower_act_ch554",
        "synonyms": ["texas whistleblower", "chapter 554 government code",
                     "texas government employee whistleblower"],
        "category": "texas_labor",
        "weight": 1.0,
    },
    "texas_non_compete": {
        "canonical": "texas_non_compete_covenant",
        "synonyms": ["texas noncompete", "texas covenant not to compete",
                     "texas business commerce code 15.50", "texas non compete enforceability"],
        "category": "texas_labor",
        "weight": 1.0,
    },

    # ---- GENERAL EMPLOYMENT ----
    "severance": {
        "canonical": "severance_agreement_negotiation",
        "synonyms": ["severance package", "separation agreement", "severance pay",
                     "termination agreement", "golden parachute", "exit package"],
        "category": "general_employment",
        "weight": 0.9,
    },
    "employment_contract": {
        "canonical": "employment_contract_analysis",
        "synonyms": ["employment agreement", "offer letter", "employment terms",
                     "job contract", "at will clause", "employment arrangement"],
        "category": "general_employment",
        "weight": 0.9,
    },
    "workplace_privacy": {
        "canonical": "employee_privacy_rights",
        "synonyms": ["employee monitoring", "email monitoring", "drug testing",
                     "social media policy", "background check", "surveillance at work"],
        "category": "general_employment",
        "weight": 0.8,
    },
}


# ============================================================================
# AGENCY ACRONYM MAP
# ============================================================================

AGENCY_ACRONYM_MAP: Dict[str, Dict[str, str]] = {
    "EEOC": {"full_name": "Equal Employment Opportunity Commission", "statute": "Title VII, ADA, ADEA, EPA, GINA"},
    "DOL": {"full_name": "Department of Labor", "statute": "FLSA, FMLA, WARN Act"},
    "WHD": {"full_name": "Wage and Hour Division (DOL)", "statute": "FLSA, FMLA"},
    "OSHA": {"full_name": "Occupational Safety and Health Administration", "statute": "OSH Act"},
    "NLRB": {"full_name": "National Labor Relations Board", "statute": "NLRA"},
    "OFCCP": {"full_name": "Office of Federal Contract Compliance Programs", "statute": "Executive Order 11246"},
    "EBSA": {"full_name": "Employee Benefits Security Administration", "statute": "ERISA"},
    "TWC": {"full_name": "Texas Workforce Commission", "statute": "Texas Labor Code"},
    "SEC": {"full_name": "Securities and Exchange Commission", "statute": "SOX Whistleblower"},
    "CFTC": {"full_name": "Commodity Futures Trading Commission", "statute": "Dodd-Frank Whistleblower"},
    "MSHA": {"full_name": "Mine Safety and Health Administration", "statute": "Federal Mine Safety Act"},
    "PBGC": {"full_name": "Pension Benefit Guaranty Corporation", "statute": "ERISA Title IV"},
}


# ============================================================================
# STATUTE REFERENCE PATTERNS
# ============================================================================

STATUTE_PATTERNS: Dict[str, str] = {
    r"42\s*U\.?S\.?C\.?\s*\xA72000e": "Title VII of the Civil Rights Act of 1964",
    r"42\s*U\.?S\.?C\.?\s*\xA712101": "Americans with Disabilities Act (ADA)",
    r"29\s*U\.?S\.?C\.?\s*\xA7621": "Age Discrimination in Employment Act (ADEA)",
    r"29\s*U\.?S\.?C\.?\s*\xA72601": "Family and Medical Leave Act (FMLA)",
    r"29\s*U\.?S\.?C\.?\s*\xA7201": "Fair Labor Standards Act (FLSA)",
    r"29\s*U\.?S\.?C\.?\s*\xA7651": "Occupational Safety and Health Act",
    r"29\s*U\.?S\.?C\.?\s*\xA71001": "Employee Retirement Income Security Act (ERISA)",
    r"29\s*U\.?S\.?C\.?\s*\xA7151": "National Labor Relations Act (NLRA)",
    r"29\s*U\.?S\.?C\.?\s*\xA72101": "Worker Adjustment and Retraining Notification Act (WARN)",
    r"title\s*vii": "Title VII of the Civil Rights Act of 1964",
    r"\bada\b": "Americans with Disabilities Act",
    r"\badea\b": "Age Discrimination in Employment Act",
    r"\bfmla\b": "Family and Medical Leave Act",
    r"\bflsa\b": "Fair Labor Standards Act",
    r"\bosha\b": "Occupational Safety and Health Act",
    r"\berisa\b": "Employee Retirement Income Security Act",
    r"\bnlra\b": "National Labor Relations Act",
    r"\bwarn\s*act\b": "WARN Act",
    r"\bsox\b": "Sarbanes-Oxley Act",
    r"\bgina\b": "Genetic Information Nondiscrimination Act",
    r"\buserra\b": "Uniformed Services Employment and Reemployment Rights Act",
    r"\bepa\b": "Equal Pay Act",
    r"\birca\b": "Immigration Reform and Control Act",
    r"tex\.?\s*lab\.?\s*code": "Texas Labor Code",
}


# ============================================================================
# CITATION PATTERNS
# ============================================================================

CITATION_PATTERNS: Dict[str, str] = {
    r"\d+\s*U\.?S\.?\s+\d+": "us_reporter",
    r"\d+\s*F\.\d[a-z]*\s+\d+": "federal_reporter",
    r"\d+\s*F\.?\s*Supp\.?\s*\d*[a-z]*\s+\d+": "federal_supplement",
    r"\d+\s*S\.?\s*Ct\.?\s+\d+": "supreme_court_reporter",
    r"\d+\s*L\.?\s*Ed\.?\s*\d*[a-z]*\s+\d+": "lawyers_edition",
    r"\d+\s*S\.?W\.?\s*\d*[a-z]*\s+\d+": "south_western_reporter",
    r"29\s*C\.?F\.?R\.?\s*\xA7?\s*\d+": "cfr_labor",
    r"42\s*C\.?F\.?R\.?\s*\xA7?\s*\d+": "cfr_public_health",
    r"EEOC\s+v\.\s+\w+": "eeoc_case",
    r"NLRB\s+v\.\s+\w+": "nlrb_case",
}


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization of a query."""
    original_query: str
    normalized_query: str
    canonical_terms: List[str]
    matched_synonyms: Dict[str, str]
    detected_categories: List[str]
    detected_statutes: List[str]
    detected_agencies: List[str]
    detected_citations: List[Dict[str, str]]
    confidence: float
    normalization_hash: str
    processing_time_ms: float
    term_count: int
    category_weights: Dict[str, float]
    jurisdiction: str = "federal"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "canonical_terms": self.canonical_terms,
            "matched_synonyms": self.matched_synonyms,
            "detected_categories": self.detected_categories,
            "detected_statutes": self.detected_statutes,
            "detected_agencies": self.detected_agencies,
            "detected_citations": self.detected_citations,
            "confidence": round(self.confidence, 4),
            "normalization_hash": self.normalization_hash,
            "processing_time_ms": round(self.processing_time_ms, 3),
            "term_count": self.term_count,
            "category_weights": {k: round(v, 4) for k, v in self.category_weights.items()},
            "jurisdiction": self.jurisdiction,
        }


# ============================================================================
# SEMANTIC NORMALIZER
# ============================================================================

class SemanticNormalizer:
    """Core employment law semantic normalization engine."""

    def __init__(self) -> None:
        """Initialize with computed lookup structures."""
        self._synonym_index: Dict[str, str] = {}
        self._category_terms: Dict[str, List[str]] = {}
        self._build_indexes()
        self._map_version = "1.0.0"
        self._map_hash = self._compute_map_hash()
        logger.info("SemanticNormalizer initialized with {} terms, {} synonyms",
                     len(SEMANTIC_MAP), len(self._synonym_index))

    def _build_indexes(self) -> None:
        """Build reverse lookup indexes from the semantic map."""
        for term_key, term_data in SEMANTIC_MAP.items():
            canonical = term_data["canonical"]
            category = term_data["category"]
            for synonym in term_data.get("synonyms", []):
                self._synonym_index[synonym.lower()] = canonical
            self._synonym_index[term_key.lower()] = canonical
            self._synonym_index[canonical.lower()] = canonical
            if category not in self._category_terms:
                self._category_terms[category] = []
            self._category_terms[category].append(canonical)

    def _compute_map_hash(self) -> str:
        """Compute SHA-256 hash of the semantic map for integrity checking."""
        map_json = json.dumps(SEMANTIC_MAP, sort_keys=True)
        return hashlib.sha256(map_json.encode("utf-8")).hexdigest()[:16]

    def normalize(self, query: str) -> NormalizationResult:
        """Normalize a query through the employment law semantic pipeline."""
        start = time.monotonic()
        query_lower = query.lower().strip()

        canonical_terms: List[str] = []
        matched_synonyms: Dict[str, str] = {}
        detected_categories: Set[str] = set()
        category_weights: Dict[str, float] = {}

        # Phase 1: Direct synonym matching
        for synonym, canonical in self._synonym_index.items():
            if synonym in query_lower:
                if canonical not in canonical_terms:
                    canonical_terms.append(canonical)
                    matched_synonyms[synonym] = canonical

        # Phase 2: Category detection from matched terms
        for term_key, term_data in SEMANTIC_MAP.items():
            canonical = term_data["canonical"]
            if canonical in canonical_terms:
                cat = term_data["category"]
                detected_categories.add(cat)
                weight = term_data.get("weight", 1.0)
                category_weights[cat] = max(category_weights.get(cat, 0.0), weight)

        # Phase 3: Statute detection
        detected_statutes: List[str] = []
        for pattern, statute_name in STATUTE_PATTERNS.items():
            if re.search(pattern, query_lower):
                if statute_name not in detected_statutes:
                    detected_statutes.append(statute_name)

        # Phase 4: Agency detection
        detected_agencies: List[str] = []
        for acronym, info in AGENCY_ACRONYM_MAP.items():
            if acronym.lower() in query_lower:
                detected_agencies.append(info["full_name"])

        # Phase 5: Citation extraction
        detected_citations: List[Dict[str, str]] = []
        for pattern, citation_type in CITATION_PATTERNS.items():
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                detected_citations.append({"citation": match, "type": citation_type})

        # Phase 6: Jurisdiction detection
        jurisdiction = "federal"
        texas_patterns = [r"\btexas\b", r"\btx\b", r"tex\.\s*lab", r"\btwc\b"]
        for pat in texas_patterns:
            if re.search(pat, query_lower):
                jurisdiction = "texas"
                break

        # Phase 7: Build normalized query
        normalized_parts = [query]
        for synonym, canonical in matched_synonyms.items():
            normalized_parts.append(canonical.replace("_", " "))
        normalized_query = " | ".join(normalized_parts)

        # Phase 8: Confidence scoring
        confidence = 0.0
        if canonical_terms:
            confidence = min(0.95, 0.3 + 0.15 * len(canonical_terms))
        if detected_statutes:
            confidence = min(0.98, confidence + 0.1 * len(detected_statutes))
        if detected_citations:
            confidence = min(0.99, confidence + 0.05 * len(detected_citations))

        # Compute determinism hash
        hash_input = f"{query_lower}:{sorted(canonical_terms)}:{sorted(detected_categories)}"
        norm_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:16]

        elapsed = (time.monotonic() - start) * 1000.0

        return NormalizationResult(
            original_query=query,
            normalized_query=normalized_query,
            canonical_terms=canonical_terms,
            matched_synonyms=matched_synonyms,
            detected_categories=sorted(detected_categories),
            detected_statutes=detected_statutes,
            detected_agencies=detected_agencies,
            detected_citations=detected_citations,
            confidence=confidence,
            normalization_hash=norm_hash,
            processing_time_ms=elapsed,
            term_count=len(canonical_terms),
            category_weights=category_weights,
            jurisdiction=jurisdiction,
        )

    def get_terms_for_category(self, category: str) -> List[str]:
        """Get all canonical terms for a category."""
        return self._category_terms.get(category, [])

    def get_all_categories(self) -> List[str]:
        """Get all available categories."""
        return sorted(self._category_terms.keys())

    def resolve_agency(self, acronym: str) -> Optional[Dict[str, str]]:
        """Resolve an agency acronym to full details."""
        return AGENCY_ACRONYM_MAP.get(acronym.upper())

    def get_map_stats(self) -> Dict[str, Any]:
        """Get statistics about the semantic map."""
        total_synonyms = sum(len(v.get("synonyms", [])) for v in SEMANTIC_MAP.values())
        return {
            "total_terms": len(SEMANTIC_MAP),
            "total_synonyms": total_synonyms,
            "total_index_entries": len(self._synonym_index),
            "categories": len(self._category_terms),
            "category_term_counts": {k: len(v) for k, v in self._category_terms.items()},
            "agencies": len(AGENCY_ACRONYM_MAP),
            "statute_patterns": len(STATUTE_PATTERNS),
            "citation_patterns": len(CITATION_PATTERNS),
            "map_version": self._map_version,
            "map_hash": self._map_hash,
        }


# ============================================================================
# GOVERNANCE METADATA
# ============================================================================

class SemanticGovernanceMetadata:
    """Governance information about the semantic dictionary."""

    def __init__(self) -> None:
        """Initialize governance metadata."""
        self.version = "1.0.0"
        self.engine_id = "LG07"
        self.last_reviewed = "2026-02-10"
        self.reviewer = "ECHO OMEGA PRIME"
        self.term_count = len(SEMANTIC_MAP)
        self.hash = hashlib.sha256(
            json.dumps(SEMANTIC_MAP, sort_keys=True).encode()
        ).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "version": self.version,
            "engine_id": self.engine_id,
            "last_reviewed": self.last_reviewed,
            "reviewer": self.reviewer,
            "term_count": self.term_count,
            "integrity_hash": self.hash,
        }


# ============================================================================
# SINGLETON AND MODULE-LEVEL FUNCTIONS
# ============================================================================

_normalizer: Optional[SemanticNormalizer] = None
_governance: Optional[SemanticGovernanceMetadata] = None


def _get_normalizer() -> SemanticNormalizer:
    """Get or create the singleton normalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = SemanticNormalizer()
    return _normalizer


def normalize_query(query: str) -> NormalizationResult:
    """Normalize a query using the global normalizer."""
    return _get_normalizer().normalize(query)


def get_semantic_map() -> Dict[str, Dict[str, Any]]:
    """Get the raw semantic map."""
    return SEMANTIC_MAP


def get_governance_metadata() -> Dict[str, Any]:
    """Get governance metadata for the semantic dictionary."""
    global _governance
    if _governance is None:
        _governance = SemanticGovernanceMetadata()
    return _governance.to_dict()


def get_semantic_map_version() -> str:
    """Get the semantic map version."""
    return _get_normalizer()._map_version


def get_semantic_map_hash() -> str:
    """Get the semantic map integrity hash."""
    return _get_normalizer()._map_hash


def verify_dictionary_integrity() -> Dict[str, Any]:
    """Verify the semantic dictionary has not been tampered with."""
    normalizer = _get_normalizer()
    current_hash = normalizer._compute_map_hash()
    stored_hash = normalizer._map_hash
    return {
        "valid": current_hash == stored_hash,
        "current_hash": current_hash,
        "stored_hash": stored_hash,
        "term_count": len(SEMANTIC_MAP),
        "synonym_count": len(normalizer._synonym_index),
    }


def get_citation_patterns() -> Dict[str, str]:
    """Get the citation pattern registry."""
    return CITATION_PATTERNS


def get_agency_map() -> Dict[str, Dict[str, str]]:
    """Get the agency acronym map."""
    return AGENCY_ACRONYM_MAP


def get_statute_patterns() -> Dict[str, str]:
    """Get the statute reference patterns."""
    return STATUTE_PATTERNS
