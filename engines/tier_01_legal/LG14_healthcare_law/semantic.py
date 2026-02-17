"""
LG14 Healthcare Law Engine - Semantic Normalization Module
=============================================================
Normalizes healthcare-specific terminology, maps synonyms, handles
HIPAA terms, fraud/abuse vocabulary, clinical trial language, FDA
regulatory terms, malpractice concepts, and telemedicine terminology.

Components:
    - SemanticMap: Core term normalization dictionary
    - normalize_query(): Main entry point for query normalization
    - Citation Patterns: Healthcare statute/case citation extraction
    - HIPAAAnalyzer: HIPAA-specific semantic analysis
    - StarkLawAnalyzer: Stark Law financial relationship analysis
    - extract_medical_entities(): Medical entity extraction
    - classify_healthcare_issue(): Issue classification

Version: 2.0.0
Engine: LG14 Healthcare Law
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
# SEMANTIC MAP - HEALTHCARE TERMINOLOGY NORMALIZATION
# ============================================================================

SEMANTIC_MAP: Dict[str, Dict[str, Any]] = {
    # ---- HIPAA ----
    "phi": {
        "canonical": "protected_health_information",
        "synonyms": ["PHI", "protected health information", "patient data", "health data",
                      "individually identifiable health information", "IIHI", "patient information"],
        "category": "hipaa",
        "weight": 1.0,
    },
    "ephi": {
        "canonical": "electronic_protected_health_information",
        "synonyms": ["ePHI", "electronic PHI", "digital health data", "electronic health data",
                      "electronic patient information"],
        "category": "hipaa",
        "weight": 1.0,
    },
    "covered_entity": {
        "canonical": "covered_entity",
        "synonyms": ["covered entity", "CE", "HIPAA covered entity", "health plan",
                      "healthcare clearinghouse", "covered provider"],
        "category": "hipaa",
        "weight": 1.0,
    },
    "business_associate": {
        "canonical": "business_associate",
        "synonyms": ["BA", "business associate", "HIPAA business associate", "BA agreement",
                      "BAA", "business associate agreement"],
        "category": "hipaa",
        "weight": 1.0,
    },
    "breach": {
        "canonical": "hipaa_breach",
        "synonyms": ["data breach", "HIPAA breach", "breach notification", "security breach",
                      "breach of PHI", "unauthorized access", "data incident"],
        "category": "hipaa",
        "weight": 1.0,
    },
    "minimum_necessary": {
        "canonical": "minimum_necessary_standard",
        "synonyms": ["minimum necessary", "minimum necessary standard", "need to know",
                      "limited disclosure", "minimum necessary rule"],
        "category": "hipaa",
        "weight": 0.9,
    },
    "npp": {
        "canonical": "notice_of_privacy_practices",
        "synonyms": ["NPP", "notice of privacy practices", "privacy notice", "HIPAA notice",
                      "privacy policy notice"],
        "category": "hipaa",
        "weight": 0.9,
    },
    "deidentification": {
        "canonical": "deidentification",
        "synonyms": ["de-identification", "deidentified data", "anonymization", "safe harbor method",
                      "expert determination", "de-identified"],
        "category": "hipaa",
        "weight": 0.9,
    },
    # ---- FRAUD AND ABUSE ----
    "fca": {
        "canonical": "false_claims_act",
        "synonyms": ["FCA", "False Claims Act", "false claims", "qui tam",
                      "whistleblower", "31 USC 3729", "Lincoln Law"],
        "category": "fraud_abuse",
        "weight": 1.0,
    },
    "aks": {
        "canonical": "anti_kickback_statute",
        "synonyms": ["AKS", "anti-kickback", "Anti-Kickback Statute", "kickback",
                      "42 USC 1320a-7b", "anti kickback", "kickback statute"],
        "category": "fraud_abuse",
        "weight": 1.0,
    },
    "stark": {
        "canonical": "stark_law",
        "synonyms": ["Stark Law", "Stark", "physician self-referral", "self-referral law",
                      "42 USC 1395nn", "Stark Act", "self referral"],
        "category": "fraud_abuse",
        "weight": 1.0,
    },
    "dhs": {
        "canonical": "designated_health_services",
        "synonyms": ["DHS", "designated health services", "Stark DHS",
                      "designated health service"],
        "category": "fraud_abuse",
        "weight": 0.9,
    },
    "safe_harbor": {
        "canonical": "safe_harbor",
        "synonyms": ["safe harbor", "safe harbour", "AKS safe harbor",
                      "42 CFR 1001.952", "regulatory safe harbor"],
        "category": "fraud_abuse",
        "weight": 1.0,
    },
    "fmv": {
        "canonical": "fair_market_value",
        "synonyms": ["FMV", "fair market value", "market value", "commercial reasonableness",
                      "commercially reasonable"],
        "category": "fraud_abuse",
        "weight": 0.9,
    },
    "oig": {
        "canonical": "office_of_inspector_general",
        "synonyms": ["OIG", "Office of Inspector General", "HHS OIG", "Inspector General",
                      "OIG advisory opinion", "OIG Work Plan"],
        "category": "fraud_abuse",
        "weight": 0.9,
    },
    "exclusion": {
        "canonical": "federal_exclusion",
        "synonyms": ["exclusion", "OIG exclusion", "LEIE", "excluded individual",
                      "debarment", "42 USC 1320a-7", "exclusion list"],
        "category": "fraud_abuse",
        "weight": 0.9,
    },
    "cia": {
        "canonical": "corporate_integrity_agreement",
        "synonyms": ["CIA", "corporate integrity agreement", "integrity agreement",
                      "compliance agreement", "OIG CIA"],
        "category": "fraud_abuse",
        "weight": 0.8,
    },
    # ---- MALPRACTICE ----
    "malpractice": {
        "canonical": "medical_malpractice",
        "synonyms": ["medical malpractice", "malpractice", "medical negligence",
                      "professional negligence", "med mal", "physician negligence"],
        "category": "malpractice",
        "weight": 1.0,
    },
    "standard_of_care": {
        "canonical": "standard_of_care",
        "synonyms": ["standard of care", "duty of care", "professional standard",
                      "medical standard", "community standard"],
        "category": "malpractice",
        "weight": 1.0,
    },
    "informed_consent": {
        "canonical": "informed_consent",
        "synonyms": ["informed consent", "patient consent", "consent to treatment",
                      "disclosure requirement", "consent form"],
        "category": "malpractice",
        "weight": 1.0,
    },
    "damages_cap": {
        "canonical": "damages_cap",
        "synonyms": ["damages cap", "damage cap", "tort reform", "noneconomic damages",
                      "cap on damages", "damages limitation"],
        "category": "malpractice",
        "weight": 0.8,
    },
    # ---- FDA ----
    "fda": {
        "canonical": "fda_regulation",
        "synonyms": ["FDA", "Food and Drug Administration", "FDA regulation",
                      "FDA approval", "drug regulation", "device regulation"],
        "category": "fda",
        "weight": 1.0,
    },
    "nda": {
        "canonical": "new_drug_application",
        "synonyms": ["NDA", "new drug application", "drug approval",
                      "drug application", "505(b)(1)", "505(b)(2)"],
        "category": "fda",
        "weight": 0.9,
    },
    "pma": {
        "canonical": "premarket_approval",
        "synonyms": ["PMA", "premarket approval", "premarket approval application",
                      "Class III device approval"],
        "category": "fda",
        "weight": 0.9,
    },
    "510k": {
        "canonical": "premarket_notification_510k",
        "synonyms": ["510(k)", "510k", "premarket notification", "substantial equivalence",
                      "predicate device", "510k clearance"],
        "category": "fda",
        "weight": 0.9,
    },
    "eua": {
        "canonical": "emergency_use_authorization",
        "synonyms": ["EUA", "emergency use authorization", "emergency authorization",
                      "emergency use"],
        "category": "fda",
        "weight": 0.8,
    },
    "cgmp": {
        "canonical": "current_good_manufacturing_practices",
        "synonyms": ["cGMP", "good manufacturing practices", "GMP", "manufacturing standards",
                      "21 CFR 211", "quality manufacturing"],
        "category": "fda",
        "weight": 0.8,
    },
    # ---- EMTALA ----
    "emtala": {
        "canonical": "emtala",
        "synonyms": ["EMTALA", "emergency medical treatment", "patient dumping",
                      "emergency treatment act", "42 USC 1395dd", "anti-dumping law"],
        "category": "emtala",
        "weight": 1.0,
    },
    "mse": {
        "canonical": "medical_screening_examination",
        "synonyms": ["MSE", "medical screening examination", "medical screening",
                      "screening exam", "emergency screening"],
        "category": "emtala",
        "weight": 0.9,
    },
    "emc": {
        "canonical": "emergency_medical_condition",
        "synonyms": ["EMC", "emergency medical condition", "emergency condition",
                      "medical emergency"],
        "category": "emtala",
        "weight": 0.9,
    },
    # ---- ACA / INSURANCE ----
    "aca": {
        "canonical": "affordable_care_act",
        "synonyms": ["ACA", "Affordable Care Act", "Obamacare", "PPACA",
                      "Patient Protection and Affordable Care Act", "healthcare reform"],
        "category": "aca",
        "weight": 1.0,
    },
    "ale": {
        "canonical": "applicable_large_employer",
        "synonyms": ["ALE", "applicable large employer", "large employer",
                      "employer mandate", "employer shared responsibility"],
        "category": "aca",
        "weight": 0.9,
    },
    "ehb": {
        "canonical": "essential_health_benefits",
        "synonyms": ["EHB", "essential health benefits", "required benefits",
                      "mandated benefits", "essential benefits"],
        "category": "aca",
        "weight": 0.8,
    },
    # ---- TELEMEDICINE ----
    "telemedicine": {
        "canonical": "telemedicine_regulation",
        "synonyms": ["telemedicine", "telehealth", "virtual care", "remote medicine",
                      "teleconsultation", "video visit", "tele health"],
        "category": "telemedicine",
        "weight": 1.0,
    },
    "ryan_haight": {
        "canonical": "ryan_haight_act",
        "synonyms": ["Ryan Haight", "Ryan Haight Act", "online prescribing",
                      "telemedicine prescribing", "21 USC 829"],
        "category": "telemedicine",
        "weight": 0.9,
    },
    # ---- CLINICAL TRIALS ----
    "irb": {
        "canonical": "institutional_review_board",
        "synonyms": ["IRB", "institutional review board", "ethics committee",
                      "research ethics board", "human subjects committee"],
        "category": "clinical_trials",
        "weight": 1.0,
    },
    "common_rule": {
        "canonical": "common_rule",
        "synonyms": ["Common Rule", "45 CFR 46", "human subjects protection",
                      "research regulations", "federal policy for protection of human subjects"],
        "category": "clinical_trials",
        "weight": 0.9,
    },
    "ind": {
        "canonical": "investigational_new_drug",
        "synonyms": ["IND", "investigational new drug", "IND application",
                      "investigational drug", "21 CFR 312"],
        "category": "clinical_trials",
        "weight": 0.9,
    },
    # ---- PARITY ----
    "mhpaea": {
        "canonical": "mental_health_parity",
        "synonyms": ["MHPAEA", "Mental Health Parity", "parity act", "mental health parity act",
                      "addiction equity", "substance use parity", "29 USC 1185a"],
        "category": "parity",
        "weight": 1.0,
    },
    "nqtl": {
        "canonical": "nonquantitative_treatment_limitation",
        "synonyms": ["NQTL", "nonquantitative treatment limitation", "non-quantitative",
                      "prior authorization parity", "step therapy parity"],
        "category": "parity",
        "weight": 0.9,
    },
    # ---- OTHER ----
    "interoperability": {
        "canonical": "healthcare_interoperability",
        "synonyms": ["interoperability", "information blocking", "Cures Act",
                      "21st Century Cures", "data exchange", "health information exchange", "HIE"],
        "category": "interoperability",
        "weight": 0.9,
    },
    "con": {
        "canonical": "certificate_of_need",
        "synonyms": ["CON", "certificate of need", "CON law", "CON approval",
                      "certificate of need law"],
        "category": "healthcare_ma",
        "weight": 0.8,
    },
    "501r": {
        "canonical": "tax_exempt_hospital_501r",
        "synonyms": ["501(r)", "501r", "tax-exempt hospital", "charitable hospital",
                      "community health needs assessment", "CHNA", "financial assistance policy"],
        "category": "tax_exempt",
        "weight": 0.8,
    },
    "part2": {
        "canonical": "substance_abuse_confidentiality",
        "synonyms": ["Part 2", "42 CFR Part 2", "substance abuse records", "SUD confidentiality",
                      "substance use disorder records"],
        "category": "substance_abuse",
        "weight": 0.9,
    },
    "prep_act": {
        "canonical": "prep_act",
        "synonyms": ["PREP Act", "Public Readiness and Emergency Preparedness",
                      "countermeasure immunity", "42 USC 247d-6d"],
        "category": "public_health",
        "weight": 0.8,
    },
    "pharmacy": {
        "canonical": "pharmacy_law",
        "synonyms": ["pharmacy law", "pharmacy regulation", "controlled substances",
                      "DEA", "CSA", "drug dispensing", "pharmacy practice act"],
        "category": "pharmacy",
        "weight": 0.9,
    },
    "340b": {
        "canonical": "340b_drug_pricing",
        "synonyms": ["340B", "340B program", "340B drug pricing", "drug discount program",
                      "covered entity 340B"],
        "category": "pharmacy",
        "weight": 0.8,
    },
}


# ============================================================================
# CATEGORY MAP
# ============================================================================

CATEGORY_MAP: Dict[str, Dict[str, Any]] = {
    "hipaa": {
        "label": "HIPAA Privacy, Security, and Breach Notification",
        "keywords": ["hipaa", "privacy", "security", "breach", "phi", "ephi", "covered entity",
                      "business associate", "authorization", "disclosure", "access", "amendment",
                      "safeguard", "encryption", "risk analysis", "notice of privacy practices"],
        "related_categories": ["interoperability", "substance_abuse"],
    },
    "fraud_abuse": {
        "label": "Healthcare Fraud and Abuse",
        "keywords": ["fraud", "abuse", "false claims", "kickback", "stark", "referral",
                      "remuneration", "safe harbor", "oig", "exclusion", "whistleblower",
                      "qui tam", "fair market value", "compliance", "overpayment"],
        "related_categories": ["malpractice", "aca"],
    },
    "malpractice": {
        "label": "Medical Malpractice and Liability",
        "keywords": ["malpractice", "negligence", "standard of care", "informed consent",
                      "damages", "tort", "liability", "duty", "breach", "causation",
                      "expert", "screening panel", "certificate of merit"],
        "related_categories": ["fraud_abuse", "licensing"],
    },
    "fda": {
        "label": "FDA Drug and Device Regulation",
        "keywords": ["fda", "drug", "device", "approval", "510k", "pma", "ind", "nda",
                      "clinical trial", "labeling", "recall", "adverse event", "cgmp",
                      "premarket", "postmarket", "eua"],
        "related_categories": ["clinical_trials", "pharmacy"],
    },
    "emtala": {
        "label": "Emergency Medical Treatment (EMTALA)",
        "keywords": ["emtala", "emergency", "screening", "stabilization", "transfer",
                      "patient dumping", "on-call", "dedicated emergency department"],
        "related_categories": ["malpractice", "patient_rights"],
    },
    "aca": {
        "label": "Affordable Care Act Compliance",
        "keywords": ["aca", "affordable care", "employer mandate", "marketplace", "exchange",
                      "essential health benefits", "individual mandate", "medicaid expansion",
                      "premium tax credit", "large employer"],
        "related_categories": ["parity", "fraud_abuse"],
    },
    "telemedicine": {
        "label": "Telemedicine Regulation",
        "keywords": ["telemedicine", "telehealth", "virtual", "remote", "video visit",
                      "interstate", "licensure compact", "ryan haight", "prescribing"],
        "related_categories": ["licensing", "malpractice"],
    },
    "clinical_trials": {
        "label": "Clinical Trials and Research",
        "keywords": ["clinical trial", "irb", "research", "human subjects", "protocol",
                      "consent", "investigational", "ind", "ide", "common rule", "dsmb"],
        "related_categories": ["fda", "malpractice"],
    },
    "parity": {
        "label": "Mental Health Parity",
        "keywords": ["parity", "mental health", "substance use", "mhpaea", "nqtl",
                      "treatment limitation", "quantitative", "nonquantitative"],
        "related_categories": ["aca", "substance_abuse"],
    },
    "interoperability": {
        "label": "Healthcare Interoperability",
        "keywords": ["interoperability", "information blocking", "cures act", "uscdi",
                      "data exchange", "health information", "ehr", "health it"],
        "related_categories": ["hipaa"],
    },
    "tax_exempt": {
        "label": "Tax-Exempt Hospital Requirements",
        "keywords": ["501r", "tax exempt", "chna", "financial assistance", "charitable",
                      "community benefit", "billing", "collection"],
        "related_categories": ["aca", "patient_rights"],
    },
    "substance_abuse": {
        "label": "Substance Abuse Confidentiality",
        "keywords": ["part 2", "42 cfr part 2", "substance abuse", "substance use",
                      "sud", "addiction", "drug treatment", "redisclosure"],
        "related_categories": ["hipaa", "parity"],
    },
    "public_health": {
        "label": "Public Health Emergency Law",
        "keywords": ["public health emergency", "phe", "prep act", "eua", "quarantine",
                      "waiver", "countermeasure", "emergency declaration"],
        "related_categories": ["fda", "emtala"],
    },
    "pharmacy": {
        "label": "Pharmacy Law",
        "keywords": ["pharmacy", "controlled substance", "dea", "dispensing", "compounding",
                      "340b", "drug supply chain", "prescription"],
        "related_categories": ["fda", "fraud_abuse"],
    },
    "healthcare_ma": {
        "label": "Healthcare M&A and CON Laws",
        "keywords": ["merger", "acquisition", "con", "certificate of need", "antitrust",
                      "change of ownership", "chow", "due diligence"],
        "related_categories": ["licensing", "fraud_abuse"],
    },
    "licensing": {
        "label": "Medical Licensing and Scope of Practice",
        "keywords": ["license", "licensure", "medical board", "scope of practice",
                      "credentialing", "privileging", "discipline", "compact"],
        "related_categories": ["telemedicine", "malpractice"],
    },
    "patient_rights": {
        "label": "Patient Rights",
        "keywords": ["patient rights", "access", "advance directive", "self-determination",
                      "nondiscrimination", "ada", "section 1557", "language access"],
        "related_categories": ["hipaa", "emtala"],
    },
}


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization of a healthcare law query."""
    original_query: str
    normalized_query: str
    tokens: List[str]
    matched_terms: List[Dict[str, Any]]
    unmatched_tokens: List[str]
    detected_categories: List[str]
    detected_hc_type: Optional[str] = None
    detected_jurisdiction: Optional[str] = None
    citation_refs: List[str] = dc_field(default_factory=list)
    medical_entities: List[str] = dc_field(default_factory=list)
    normalization_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "tokens": self.tokens,
            "matched_terms": self.matched_terms,
            "unmatched_tokens": self.unmatched_tokens,
            "detected_categories": self.detected_categories,
            "detected_hc_type": self.detected_hc_type,
            "detected_jurisdiction": self.detected_jurisdiction,
            "citation_refs": self.citation_refs,
            "medical_entities": self.medical_entities,
            "normalization_time_ms": round(self.normalization_time_ms, 3),
        }


# ============================================================================
# JURISDICTION MAP
# ============================================================================

JURISDICTION_MAP: Dict[str, str] = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
}


# ============================================================================
# CITATION PATTERNS
# ============================================================================

CITATION_PATTERNS: List[tuple[str, re.Pattern]] = [
    ("usc", re.compile(r"\b(\d+)\s*U\.?S\.?C\.?\s*(?:SS|Section|Sec\.?)?\s*(\d+[a-z\-]*)", re.IGNORECASE)),
    ("cfr", re.compile(r"\b(\d+)\s*C\.?F\.?R\.?\s*(?:Part|SS|Section)?\s*(\d+[\.\d]*)", re.IGNORECASE)),
    ("fr", re.compile(r"\b(\d+)\s*F\.?R\.?\s*(\d+)", re.IGNORECASE)),
    ("us_reporter", re.compile(r"\b(\d+)\s*U\.?S\.?\s*(\d+)", re.IGNORECASE)),
    ("fed_reporter", re.compile(r"\b(\d+)\s*F\.?\s*(?:2d|3d|4th)?\s*(\d+)", re.IGNORECASE)),
    ("scotus", re.compile(r"\b(\d+)\s*S\.?\s*Ct\.?\s*(\d+)", re.IGNORECASE)),
    ("irc", re.compile(r"\bI\.?R\.?C\.?\s*(?:SS|Section|Sec\.?)?\s*(\d+[a-z\(\)]*)", re.IGNORECASE)),
]


# ============================================================================
# CORE NORMALIZATION FUNCTIONS
# ============================================================================

def normalize_query(query: str) -> NormalizationResult:
    """Normalize a healthcare law query through semantic mapping, citation extraction, and entity detection."""
    start = time.monotonic()
    query_lower = query.lower().strip()
    tokens = _tokenize(query_lower)
    matched_terms: List[Dict[str, Any]] = []
    matched_token_indices: Set[int] = set()
    detected_categories: List[str] = []
    category_scores: Dict[str, float] = {}

    # Match against semantic map
    for key, entry in SEMANTIC_MAP.items():
        canonical = entry["canonical"]
        category = entry["category"]
        weight = entry.get("weight", 1.0)

        for synonym in entry["synonyms"]:
            syn_lower = synonym.lower()
            if syn_lower in query_lower:
                matched_terms.append({
                    "original": synonym,
                    "canonical": canonical,
                    "category": category,
                    "weight": weight,
                })
                category_scores[category] = category_scores.get(category, 0) + weight
                # Mark matched tokens
                syn_tokens = set(syn_lower.split())
                for i, t in enumerate(tokens):
                    if t in syn_tokens:
                        matched_token_indices.add(i)
                break

    # Category keyword matching
    for cat_key, cat_info in CATEGORY_MAP.items():
        for keyword in cat_info["keywords"]:
            if keyword.lower() in query_lower:
                category_scores[cat_key] = category_scores.get(cat_key, 0) + 0.5

    # Sort categories by score
    sorted_cats = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    detected_categories = [cat for cat, score in sorted_cats if score >= 0.5]

    # Detect primary healthcare type
    detected_hc_type = detected_categories[0] if detected_categories else None

    # Unmatched tokens
    unmatched = [tokens[i] for i in range(len(tokens)) if i not in matched_token_indices]

    # Extract citations
    citations = extract_citations(query)

    # Detect jurisdiction
    jurisdiction = detect_jurisdiction(query_lower)

    # Extract medical entities
    entities = extract_medical_entities(query)

    # Build normalized query
    normalized_parts = []
    for term in matched_terms:
        normalized_parts.append(term["canonical"])
    for token in unmatched:
        if len(token) >= 2:
            normalized_parts.append(token)
    normalized_query = " ".join(normalized_parts) if normalized_parts else query_lower

    elapsed = (time.monotonic() - start) * 1000.0

    return NormalizationResult(
        original_query=query,
        normalized_query=normalized_query,
        tokens=tokens,
        matched_terms=matched_terms,
        unmatched_tokens=unmatched,
        detected_categories=detected_categories,
        detected_hc_type=detected_hc_type,
        detected_jurisdiction=jurisdiction,
        citation_refs=citations,
        medical_entities=entities,
        normalization_time_ms=elapsed,
    )


def _tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase words."""
    return [t for t in re.split(r"[\s\-_/,;:()\[\]{}\"']+", text) if t and len(t) >= 2]


def extract_citations(text: str) -> List[str]:
    """Extract legal citations from text."""
    citations: List[str] = []
    for label, pattern in CITATION_PATTERNS:
        for match in pattern.finditer(text):
            citations.append(f"{label}:{match.group(0).strip()}")
    return citations


def detect_jurisdiction(text: str) -> Optional[str]:
    """Detect jurisdiction from query text."""
    text_lower = text.lower()
    # Check state abbreviations
    state_pattern = re.compile(r"\b([A-Z]{2})\b")
    for match in state_pattern.finditer(text):
        abbrev = match.group(1)
        if abbrev in set(JURISDICTION_MAP.values()):
            return abbrev
    # Check state names
    for name, abbrev in JURISDICTION_MAP.items():
        if name in text_lower:
            return abbrev
    return None


def extract_medical_entities(text: str) -> List[str]:
    """Extract healthcare-specific entities from text."""
    entities: List[str] = []
    entity_patterns = [
        (r"\b(hospital|clinic|medical center|health system|nursing home|skilled nursing|ambulatory surgery)\b", "facility"),
        (r"\b(physician|doctor|surgeon|nurse|pharmacist|therapist|dentist|optometrist)\b", "provider"),
        (r"\b(Medicare|Medicaid|Tricare|VA|CHIP|FEHB|marketplace)\b", "program"),
        (r"\b(HHS|CMS|OIG|OCR|FDA|DEA|FTC|DOJ|SAMHSA|ONC|HRSA)\b", "agency"),
        (r"\b(EHR|EMR|health IT|medical record|patient portal|health information exchange)\b", "technology"),
        (r"\b(vaccine|drug|device|biologic|pharmaceutical|prescription|controlled substance)\b", "product"),
    ]
    text_lower = text.lower()
    for pattern, entity_type in entity_patterns:
        for match in re.finditer(pattern, text_lower, re.IGNORECASE):
            entities.append(f"{entity_type}:{match.group(0)}")
    return list(dict.fromkeys(entities))


def classify_healthcare_issue(query: str) -> Dict[str, Any]:
    """Classify a healthcare law query into issue categories with confidence scores."""
    result = normalize_query(query)
    category_details: List[Dict[str, Any]] = []

    for cat in result.detected_categories[:5]:
        cat_info = CATEGORY_MAP.get(cat, {})
        category_details.append({
            "category": cat,
            "label": cat_info.get("label", cat),
            "related_categories": cat_info.get("related_categories", []),
            "matched_keywords": [
                kw for kw in cat_info.get("keywords", [])
                if kw.lower() in query.lower()
            ],
        })

    return {
        "primary_category": result.detected_hc_type,
        "categories": category_details,
        "medical_entities": result.medical_entities,
        "citations_found": result.citation_refs,
        "jurisdiction": result.detected_jurisdiction,
    }


def compute_semantic_similarity(query_a: str, query_b: str) -> float:
    """Compute semantic similarity between two queries based on shared normalized terms."""
    result_a = normalize_query(query_a)
    result_b = normalize_query(query_b)

    terms_a = set(t["canonical"] for t in result_a.matched_terms)
    terms_b = set(t["canonical"] for t in result_b.matched_terms)

    if not terms_a and not terms_b:
        tokens_a = set(result_a.tokens)
        tokens_b = set(result_b.tokens)
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = tokens_a & tokens_b
        union = tokens_a | tokens_b
        return len(intersection) / len(union)

    if not terms_a or not terms_b:
        return 0.0

    intersection = terms_a & terms_b
    union = terms_a | terms_b
    return len(intersection) / len(union)


# ============================================================================
# HIPAA ANALYZER
# ============================================================================

class HIPAAAnalyzer:
    """Specialized analyzer for HIPAA-related queries."""

    HIPAA_RULES: Dict[str, Dict[str, str]] = {
        "privacy_rule": {
            "cfr": "45 CFR 164 Subpart E",
            "scope": "Uses and disclosures of PHI by covered entities and business associates",
        },
        "security_rule": {
            "cfr": "45 CFR 164 Subpart C",
            "scope": "Administrative, physical, and technical safeguards for ePHI",
        },
        "breach_notification": {
            "cfr": "45 CFR 164 Subpart D",
            "scope": "Notification requirements following breach of unsecured PHI",
        },
        "enforcement_rule": {
            "cfr": "45 CFR 160 Subpart D",
            "scope": "Investigation, penalties, and enforcement procedures",
        },
        "transactions_rule": {
            "cfr": "45 CFR Parts 160, 162",
            "scope": "Standard electronic transactions and code sets",
        },
    }

    def analyze(self, query: str) -> Dict[str, Any]:
        """Analyze a query for HIPAA-specific issues."""
        query_lower = query.lower()
        applicable_rules: List[Dict[str, str]] = []

        for rule_name, rule_info in self.HIPAA_RULES.items():
            keywords = rule_name.replace("_", " ").split()
            if any(kw in query_lower for kw in keywords):
                applicable_rules.append({
                    "rule": rule_name,
                    "cfr": rule_info["cfr"],
                    "scope": rule_info["scope"],
                })

        phi_indicators = ["phi", "protected health information", "patient data",
                          "health information", "medical record", "patient record"]
        phi_detected = any(ind in query_lower for ind in phi_indicators)

        breach_indicators = ["breach", "unauthorized", "stolen", "lost", "hacked",
                             "ransomware", "phishing", "data incident"]
        breach_detected = any(ind in query_lower for ind in breach_indicators)

        return {
            "hipaa_relevant": len(applicable_rules) > 0 or phi_detected,
            "applicable_rules": applicable_rules,
            "phi_detected": phi_detected,
            "breach_indicators": breach_detected,
            "recommendation": self._recommendation(applicable_rules, phi_detected, breach_detected),
        }

    def _recommendation(self, rules: List[Dict[str, str]], phi: bool, breach: bool) -> str:
        """Generate a recommendation based on analysis."""
        if breach:
            return "Potential HIPAA breach detected. Conduct 4-factor risk assessment per 45 CFR 164.402. Notify affected individuals within 60 days of discovery if breach confirmed."
        if phi:
            return "PHI involvement detected. Ensure minimum necessary standard is applied and valid authorization or TPO exception exists for any use or disclosure."
        if rules:
            return f"Query implicates {len(rules)} HIPAA rule(s). Analyze compliance with applicable regulatory requirements."
        return "No specific HIPAA indicators detected. Evaluate whether the scenario involves PHI or covered entity/business associate obligations."


# ============================================================================
# STARK LAW ANALYZER
# ============================================================================

class StarkLawAnalyzer:
    """Specialized analyzer for Stark Law referral issues."""

    EXCEPTIONS_MAP: Dict[str, str] = {
        "employment": "42 CFR 411.357(c) - Bona fide employment relationship",
        "personal_services": "42 CFR 411.357(d) - Personal services and management contracts",
        "rental_space": "42 CFR 411.357(a) - Rental of office space",
        "rental_equipment": "42 CFR 411.357(b) - Rental of equipment",
        "in_office_ancillary": "42 CFR 411.355(b) - In-office ancillary services",
        "fair_market_value": "42 CFR 411.357(l) - Fair market value compensation",
        "isolated_transactions": "42 CFR 411.357(f) - Isolated transactions",
        "academic_medical_centers": "42 CFR 411.355(e) - Academic medical centers",
        "value_based": "42 CFR 411.357(aa) - Value-based arrangements",
        "group_practice": "42 CFR 411.352 - Group practice requirements",
    }

    def analyze(self, query: str) -> Dict[str, Any]:
        """Analyze a query for Stark Law issues."""
        query_lower = query.lower()

        referral_detected = any(kw in query_lower for kw in [
            "referral", "refer", "self-referral", "physician referral",
            "designated health services", "dhs",
        ])

        financial_relationship = any(kw in query_lower for kw in [
            "financial relationship", "ownership", "investment", "compensation",
            "salary", "bonus", "lease", "rental", "contract", "payment",
        ])

        applicable_exceptions: List[Dict[str, str]] = []
        for exc_key, exc_desc in self.EXCEPTIONS_MAP.items():
            keywords = exc_key.replace("_", " ").split()
            if any(kw in query_lower for kw in keywords):
                applicable_exceptions.append({
                    "exception": exc_key,
                    "description": exc_desc,
                })

        stark_risk = "HIGH" if referral_detected and financial_relationship else \
                     "MEDIUM" if referral_detected or financial_relationship else "LOW"

        return {
            "stark_relevant": referral_detected or financial_relationship,
            "referral_detected": referral_detected,
            "financial_relationship_detected": financial_relationship,
            "applicable_exceptions": applicable_exceptions,
            "risk_level": stark_risk,
            "recommendation": (
                "Physician financial relationship with DHS entity detected. Map all referral patterns and verify applicable Stark exception compliance."
                if stark_risk == "HIGH"
                else "Evaluate whether a financial relationship exists between the referring physician and the DHS entity."
                if stark_risk == "MEDIUM"
                else "No significant Stark Law indicators detected based on the query."
            ),
        }


# ============================================================================
# MODULE-LEVEL ACCESSORS
# ============================================================================

def get_semantic_map() -> Dict[str, Dict[str, Any]]:
    """Return the full semantic map."""
    return SEMANTIC_MAP


def get_semantic_map_version() -> str:
    """Return the semantic map version identifier."""
    return "LG14-HC-2.0.0"


def get_semantic_map_hash() -> str:
    """Compute SHA-256 hash of the semantic map for integrity verification."""
    content = json.dumps(SEMANTIC_MAP, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get_jurisdiction_map() -> Dict[str, str]:
    """Return the jurisdiction mapping."""
    return JURISDICTION_MAP


def verify_dictionary_integrity() -> Dict[str, Any]:
    """Verify the integrity of the semantic dictionary."""
    issues: List[str] = []
    canonicals_seen: Set[str] = set()

    for key, entry in SEMANTIC_MAP.items():
        if "canonical" not in entry:
            issues.append(f"Entry '{key}' missing canonical field")
        if "synonyms" not in entry or not entry["synonyms"]:
            issues.append(f"Entry '{key}' missing synonyms")
        if "category" not in entry:
            issues.append(f"Entry '{key}' missing category")
        canonical = entry.get("canonical", "")
        if canonical in canonicals_seen:
            issues.append(f"Duplicate canonical: {canonical}")
        canonicals_seen.add(canonical)

    return {
        "valid": len(issues) == 0,
        "total_entries": len(SEMANTIC_MAP),
        "total_synonyms": sum(len(e.get("synonyms", [])) for e in SEMANTIC_MAP.values()),
        "categories": list(set(e.get("category", "") for e in SEMANTIC_MAP.values())),
        "issues": issues,
        "hash": get_semantic_map_hash(),
    }
