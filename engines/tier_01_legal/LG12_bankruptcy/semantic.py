"""
LG12 Bankruptcy Law Engine - Semantic Normalization Module
===========================================================
Normalizes bankruptcy-specific terminology, maps synonyms, handles
chapter-specific terms, means test vocabulary, exemption terminology,
discharge/dischargeability concepts, avoidance action language,
plan confirmation terms, BAPCPA requirements, FRBP references,
and Texas-specific bankruptcy exemptions.

Components:
    - SemanticMap: Core term normalization dictionary
    - normalize_query(): Main entry point for query normalization
    - Citation Patterns: Bankruptcy statute/case citation extraction
    - FRBP Rule Parser: Federal Rules of Bankruptcy Procedure patterns
    - Texas Exemption Mapper: Texas Property Code section mapping

Version: 2.0.0
Engine: LG12 Bankruptcy Law
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
# SEMANTIC MAP - BANKRUPTCY TERMINOLOGY NORMALIZATION
# ============================================================================

SEMANTIC_MAP: Dict[str, Dict[str, Any]] = {
    # ---- CHAPTER TYPES ----
    "chapter_7": {
        "canonical": "chapter_7_liquidation",
        "synonyms": ["chapter 7", "ch 7", "ch7", "liquidation", "straight bankruptcy",
                      "complete bankruptcy", "fresh start bankruptcy", "total discharge"],
        "category": "chapter_type",
        "weight": 1.0,
    },
    "chapter_11": {
        "canonical": "chapter_11_reorganization",
        "synonyms": ["chapter 11", "ch 11", "ch11", "reorganization", "reorg",
                      "corporate bankruptcy", "business bankruptcy", "restructuring",
                      "debtor in possession", "DIP"],
        "category": "chapter_type",
        "weight": 1.0,
    },
    "chapter_13": {
        "canonical": "chapter_13_wage_earner",
        "synonyms": ["chapter 13", "ch 13", "ch13", "wage earner plan", "repayment plan",
                      "individual reorganization", "debt adjustment", "payment plan bankruptcy"],
        "category": "chapter_type",
        "weight": 1.0,
    },
    "chapter_12": {
        "canonical": "chapter_12_family_farmer",
        "synonyms": ["chapter 12", "ch 12", "ch12", "family farmer bankruptcy",
                      "family fisherman", "farmer bankruptcy", "agricultural bankruptcy"],
        "category": "chapter_type",
        "weight": 0.9,
    },
    "chapter_15": {
        "canonical": "chapter_15_cross_border",
        "synonyms": ["chapter 15", "ch 15", "ch15", "cross-border insolvency",
                      "foreign bankruptcy", "international insolvency", "ancillary proceeding"],
        "category": "chapter_type",
        "weight": 0.9,
    },
    "subchapter_v": {
        "canonical": "subchapter_v_small_business",
        "synonyms": ["subchapter v", "sub v", "sub-v", "small business reorganization",
                      "SBRA", "small business debtor", "subchapter 5"],
        "category": "chapter_type",
        "weight": 0.9,
    },
    # ---- MEANS TEST ----
    "means_test": {
        "canonical": "means_test",
        "synonyms": ["means test", "707(b) means test", "income test", "abuse test",
                      "form 122A", "current monthly income", "CMI", "median income test",
                      "presumption of abuse"],
        "category": "eligibility",
        "weight": 1.0,
    },
    "current_monthly_income": {
        "canonical": "current_monthly_income",
        "synonyms": ["CMI", "monthly income", "average monthly income",
                      "six month income average", "gross monthly income for means test"],
        "category": "eligibility",
        "weight": 0.9,
    },
    "median_income": {
        "canonical": "state_median_family_income",
        "synonyms": ["median income", "state median", "census median",
                      "household median", "family median income"],
        "category": "eligibility",
        "weight": 0.9,
    },
    "disposable_income": {
        "canonical": "disposable_income",
        "synonyms": ["disposable income", "projected disposable income",
                      "net disposable", "income available for unsecured creditors",
                      "PDI"],
        "category": "eligibility",
        "weight": 0.9,
    },
    # ---- AUTOMATIC STAY ----
    "automatic_stay": {
        "canonical": "automatic_stay",
        "synonyms": ["automatic stay", "stay", "362 stay", "section 362",
                      "stay of proceedings", "bankruptcy stay", "collection stay",
                      "litigation stay", "foreclosure stay"],
        "category": "stay",
        "weight": 1.0,
    },
    "stay_relief": {
        "canonical": "relief_from_automatic_stay",
        "synonyms": ["lift stay", "stay relief", "relief from stay", "motion to lift stay",
                      "motion for relief from stay", "362(d) motion", "adequate protection"],
        "category": "stay",
        "weight": 1.0,
    },
    "stay_violation": {
        "canonical": "willful_stay_violation",
        "synonyms": ["stay violation", "362(k) violation", "willful violation",
                      "contempt of stay", "violating the automatic stay",
                      "damages for stay violation"],
        "category": "stay",
        "weight": 0.9,
    },
    "codebtor_stay": {
        "canonical": "codebtor_stay",
        "synonyms": ["codebtor stay", "co-debtor stay", "1301 stay",
                      "cosigner stay", "guarantor stay"],
        "category": "stay",
        "weight": 0.8,
    },
    # ---- DISCHARGE ----
    "discharge": {
        "canonical": "bankruptcy_discharge",
        "synonyms": ["discharge", "debt discharge", "bankruptcy discharge",
                      "fresh start", "elimination of debt", "discharged debts",
                      "discharge order"],
        "category": "discharge",
        "weight": 1.0,
    },
    "nondischargeable": {
        "canonical": "nondischargeable_debt",
        "synonyms": ["nondischargeable", "non-dischargeable", "523 exception",
                      "exception to discharge", "surviving debt",
                      "debt that survives bankruptcy"],
        "category": "discharge",
        "weight": 1.0,
    },
    "discharge_denial": {
        "canonical": "denial_of_discharge",
        "synonyms": ["denial of discharge", "727 denial", "objection to discharge",
                      "discharge denied", "no discharge", "complete denial"],
        "category": "discharge",
        "weight": 0.9,
    },
    "student_loan_discharge": {
        "canonical": "student_loan_undue_hardship",
        "synonyms": ["student loan discharge", "student loan bankruptcy",
                      "Brunner test", "undue hardship", "adversary student loan",
                      "educational loan discharge", "523(a)(8)"],
        "category": "discharge",
        "weight": 1.0,
    },
    "tax_discharge": {
        "canonical": "tax_debt_discharge",
        "synonyms": ["tax discharge", "tax debt discharge", "IRS debt bankruptcy",
                      "income tax discharge", "3 year rule", "2 year rule",
                      "240 day rule", "tax debt in bankruptcy"],
        "category": "discharge",
        "weight": 1.0,
    },
    "reaffirmation": {
        "canonical": "reaffirmation_agreement",
        "synonyms": ["reaffirmation", "reaffirmation agreement", "reaffirm debt",
                      "524(c) agreement", "keep and pay", "reaffirm",
                      "voluntary repayment agreement"],
        "category": "discharge",
        "weight": 0.9,
    },
    # ---- EXEMPTIONS ----
    "exemptions": {
        "canonical": "bankruptcy_exemptions",
        "synonyms": ["exemptions", "exempt property", "protected property",
                      "exempt assets", "section 522 exemptions", "homestead exemption",
                      "personal property exemption"],
        "category": "exemptions",
        "weight": 1.0,
    },
    "homestead_exemption": {
        "canonical": "homestead_exemption",
        "synonyms": ["homestead", "homestead exemption", "home exemption",
                      "principal residence exemption", "house exemption",
                      "homestead protection"],
        "category": "exemptions",
        "weight": 1.0,
    },
    "texas_homestead": {
        "canonical": "texas_homestead_exemption",
        "synonyms": ["texas homestead", "TX homestead", "unlimited homestead",
                      "texas home exemption", "texas property code 41",
                      "urban 10 acres", "rural 200 acres", "texas unlimited homestead"],
        "category": "exemptions",
        "weight": 1.0,
    },
    "wildcard_exemption": {
        "canonical": "wildcard_exemption",
        "synonyms": ["wildcard", "wildcard exemption", "522(d)(5)",
                      "general exemption", "catch-all exemption",
                      "unused homestead exemption"],
        "category": "exemptions",
        "weight": 0.8,
    },
    "federal_exemptions": {
        "canonical": "federal_bankruptcy_exemptions",
        "synonyms": ["federal exemptions", "522(d) exemptions",
                      "federal list", "federal exemption schedule"],
        "category": "exemptions",
        "weight": 0.9,
    },
    "opt_out": {
        "canonical": "state_opt_out",
        "synonyms": ["opt out", "opt-out", "state opt out", "texas opt out",
                      "state exemptions only", "no federal exemptions"],
        "category": "exemptions",
        "weight": 0.8,
    },
    "exemption_planning": {
        "canonical": "pre_bankruptcy_exemption_planning",
        "synonyms": ["exemption planning", "asset conversion", "pre-filing conversion",
                      "converting nonexempt to exempt", "homestead conversion",
                      "retirement account conversion"],
        "category": "exemptions",
        "weight": 0.9,
    },
    # ---- AVOIDANCE ACTIONS ----
    "preference": {
        "canonical": "preferential_transfer",
        "synonyms": ["preference", "preferential transfer", "547 action",
                      "preference action", "voidable preference", "preference claim",
                      "insider preference", "90 day preference"],
        "category": "avoidance",
        "weight": 1.0,
    },
    "fraudulent_transfer": {
        "canonical": "fraudulent_transfer",
        "synonyms": ["fraudulent transfer", "fraudulent conveyance", "548 action",
                      "actual fraud transfer", "constructive fraud transfer",
                      "UFTA", "UVTA", "badges of fraud"],
        "category": "avoidance",
        "weight": 1.0,
    },
    "strong_arm": {
        "canonical": "strong_arm_power",
        "synonyms": ["strong arm", "strong-arm", "544 power", "hypothetical lien creditor",
                      "trustee avoidance power", "unperfected security interest"],
        "category": "avoidance",
        "weight": 0.9,
    },
    "ordinary_course": {
        "canonical": "ordinary_course_defense",
        "synonyms": ["ordinary course", "ordinary course of business",
                      "OCB defense", "547(c)(2)", "regular payment defense"],
        "category": "avoidance",
        "weight": 0.9,
    },
    # ---- PLAN CONFIRMATION ----
    "plan_confirmation": {
        "canonical": "plan_confirmation",
        "synonyms": ["plan confirmation", "confirm plan", "plan approval",
                      "1129 confirmation", "1325 confirmation", "plan effective date"],
        "category": "plan",
        "weight": 1.0,
    },
    "cramdown": {
        "canonical": "cramdown",
        "synonyms": ["cramdown", "cram down", "cram-down", "1129(b) cramdown",
                      "forced confirmation", "nonconsensual confirmation",
                      "fair and equitable"],
        "category": "plan",
        "weight": 1.0,
    },
    "absolute_priority": {
        "canonical": "absolute_priority_rule",
        "synonyms": ["absolute priority", "absolute priority rule", "APR",
                      "senior before junior", "full payment rule",
                      "no equity retention without full payment"],
        "category": "plan",
        "weight": 0.9,
    },
    "best_interests_test": {
        "canonical": "best_interests_test",
        "synonyms": ["best interests test", "best interests of creditors",
                      "liquidation analysis", "chapter 7 comparison test",
                      "1325(a)(4)"],
        "category": "plan",
        "weight": 0.9,
    },
    "feasibility": {
        "canonical": "plan_feasibility",
        "synonyms": ["feasibility", "feasibility test", "plan feasibility",
                      "ability to make payments", "plan viability",
                      "not likely to be followed by liquidation"],
        "category": "plan",
        "weight": 0.9,
    },
    "disclosure_statement": {
        "canonical": "disclosure_statement",
        "synonyms": ["disclosure statement", "DS", "adequate information",
                      "1125 disclosure", "plan disclosure", "information statement"],
        "category": "plan",
        "weight": 0.9,
    },
    "lien_stripping": {
        "canonical": "lien_stripping",
        "synonyms": ["lien stripping", "lien strip", "strip lien",
                      "strip off lien", "second mortgage strip",
                      "junior lien strip", "506 valuation", "wholly unsecured"],
        "category": "plan",
        "weight": 0.9,
    },
    # ---- ADVERSARY PROCEEDINGS ----
    "adversary_proceeding": {
        "canonical": "adversary_proceeding",
        "synonyms": ["adversary proceeding", "AP", "adversary action",
                      "7001 proceeding", "adversary complaint",
                      "bankruptcy lawsuit"],
        "category": "adversary",
        "weight": 1.0,
    },
    # ---- TRUSTEE / ESTATE ----
    "bankruptcy_estate": {
        "canonical": "bankruptcy_estate",
        "synonyms": ["bankruptcy estate", "estate", "541 estate",
                      "property of the estate", "debtor's estate"],
        "category": "estate",
        "weight": 1.0,
    },
    "trustee": {
        "canonical": "bankruptcy_trustee",
        "synonyms": ["trustee", "chapter 7 trustee", "panel trustee",
                      "standing trustee", "case trustee", "interim trustee"],
        "category": "estate",
        "weight": 1.0,
    },
    "us_trustee": {
        "canonical": "united_states_trustee",
        "synonyms": ["US trustee", "U.S. trustee", "UST", "United States Trustee",
                      "office of the US trustee", "OUST"],
        "category": "estate",
        "weight": 0.9,
    },
    "debtor_in_possession": {
        "canonical": "debtor_in_possession",
        "synonyms": ["debtor in possession", "DIP", "D.I.P.", "DIP debtor",
                      "operating debtor", "self-administered debtor"],
        "category": "estate",
        "weight": 1.0,
    },
    "dip_financing": {
        "canonical": "dip_financing",
        "synonyms": ["DIP financing", "DIP loan", "364 financing",
                      "debtor in possession financing", "superpriority financing",
                      "priming lien"],
        "category": "estate",
        "weight": 0.9,
    },
    "proof_of_claim": {
        "canonical": "proof_of_claim",
        "synonyms": ["proof of claim", "POC", "claim filing", "file a claim",
                      "creditor claim", "form 410", "bar date claim"],
        "category": "claims",
        "weight": 1.0,
    },
    "priority_claim": {
        "canonical": "priority_claim",
        "synonyms": ["priority claim", "507 priority", "administrative claim",
                      "domestic support priority", "tax priority claim",
                      "wage priority", "priority debt"],
        "category": "claims",
        "weight": 0.9,
    },
    "secured_claim": {
        "canonical": "secured_claim",
        "synonyms": ["secured claim", "secured creditor", "collateral",
                      "security interest", "lien", "506(a) valuation",
                      "secured portion", "undersecured"],
        "category": "claims",
        "weight": 0.9,
    },
    # ---- BAPCPA ----
    "bapcpa": {
        "canonical": "bapcpa",
        "synonyms": ["BAPCPA", "bankruptcy reform act", "2005 bankruptcy act",
                      "bankruptcy abuse prevention", "Bankruptcy Abuse Prevention and Consumer Protection Act"],
        "category": "legislation",
        "weight": 1.0,
    },
    "credit_counseling": {
        "canonical": "pre_filing_credit_counseling",
        "synonyms": ["credit counseling", "pre-filing counseling", "109(h) requirement",
                      "budget counseling", "approved credit counseling agency"],
        "category": "eligibility",
        "weight": 0.8,
    },
    "financial_management": {
        "canonical": "post_filing_financial_management",
        "synonyms": ["financial management course", "debtor education",
                      "post-filing course", "1328 requirement", "personal financial management"],
        "category": "eligibility",
        "weight": 0.8,
    },
    # ---- EXECUTORY CONTRACTS ----
    "executory_contract": {
        "canonical": "executory_contract",
        "synonyms": ["executory contract", "unexpired lease", "365 assumption",
                      "assume or reject", "contract assumption",
                      "contract rejection", "cure and assume"],
        "category": "contracts",
        "weight": 0.9,
    },
    # ---- PROPERTY-SPECIFIC ----
    "cash_collateral": {
        "canonical": "cash_collateral",
        "synonyms": ["cash collateral", "363 use", "use of cash collateral",
                      "cash management", "cash collateral order"],
        "category": "operations",
        "weight": 0.9,
    },
    "adequate_protection": {
        "canonical": "adequate_protection",
        "synonyms": ["adequate protection", "361 protection", "adequate protection payment",
                      "equity cushion", "replacement lien", "periodic payments"],
        "category": "stay",
        "weight": 0.9,
    },
    "chapter_20": {
        "canonical": "chapter_20_strategy",
        "synonyms": ["chapter 20", "ch 20", "chapter 7 then 13",
                      "sequential filing", "discharge then strip",
                      "post-discharge chapter 13"],
        "category": "strategy",
        "weight": 0.8,
    },
    "serial_filer": {
        "canonical": "serial_filer",
        "synonyms": ["serial filer", "repeat filer", "multiple filings",
                      "successive filings", "362(c)(3)", "362(c)(4)",
                      "presumption no stay"],
        "category": "stay",
        "weight": 0.8,
    },
}


# ============================================================================
# JURISDICTION MAP
# ============================================================================

JURISDICTION_MAP: Dict[str, Dict[str, Any]] = {
    "federal": {
        "label": "Federal Bankruptcy Court",
        "authority": "Title 11 USC, Title 28 USC, FRBP",
        "scope": "nationwide",
    },
    "5th_circuit": {
        "label": "U.S. Court of Appeals for the Fifth Circuit",
        "authority": "Covers TX, LA, MS",
        "scope": "regional",
        "key_bankruptcy_precedent": [
            "In re Pac-Fab Inc. (avoidance actions)",
            "Matter of T-H New Orleans Ltd. (cramdown)",
            "In re Cowin (homestead exemption)",
        ],
    },
    "texas_western": {
        "label": "Western District of Texas Bankruptcy Court",
        "authority": "Local Bankruptcy Rules W.D. Tex.",
        "scope": "district",
        "divisions": ["austin", "el_paso", "midland_odessa", "san_antonio", "waco"],
    },
    "texas_northern": {
        "label": "Northern District of Texas Bankruptcy Court",
        "authority": "Local Bankruptcy Rules N.D. Tex.",
        "scope": "district",
        "divisions": ["dallas", "fort_worth", "amarillo", "lubbock", "abilene", "san_angelo", "wichita_falls"],
    },
    "texas_southern": {
        "label": "Southern District of Texas Bankruptcy Court",
        "authority": "Local Bankruptcy Rules S.D. Tex.",
        "scope": "district",
        "divisions": ["houston", "galveston", "corpus_christi", "brownsville", "laredo", "mcallen", "victoria"],
    },
    "texas_eastern": {
        "label": "Eastern District of Texas Bankruptcy Court",
        "authority": "Local Bankruptcy Rules E.D. Tex.",
        "scope": "district",
        "divisions": ["beaumont", "lufkin", "marshall", "sherman", "texarkana", "tyler"],
    },
    "texas_state": {
        "label": "Texas State Law (exemptions and non-bankruptcy)",
        "authority": "Texas Property Code, Texas Constitution Art. XVI",
        "scope": "state",
    },
}


# ============================================================================
# CITATION PATTERNS
# ============================================================================

CITATION_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("title_11_usc", re.compile(
        r"(?:11\s*U\.?S\.?C\.?\s*(?:\xA7|[Ss](?:ec(?:tion)?\.?))\s*(\d+(?:\([a-z]\)(?:\(\d+\))?)?)|"
        r"(?:Section|Sec\.?)\s*(\d+(?:\([a-z]\)(?:\(\d+\))?)?)\s*(?:of\s+(?:the\s+)?(?:Bankruptcy\s+Code|Title\s+11)))",
        re.IGNORECASE
    )),
    ("title_28_usc", re.compile(
        r"28\s*U\.?S\.?C\.?\s*(?:\xA7|[Ss](?:ec(?:tion)?\.?))\s*(\d+)",
        re.IGNORECASE
    )),
    ("frbp", re.compile(
        r"(?:FRBP|Fed\.?\s*R\.?\s*Bankr\.?\s*P\.?|Bankruptcy\s+Rule)\s*(\d{4}(?:\.\d+)?)",
        re.IGNORECASE
    )),
    ("form", re.compile(
        r"(?:Official\s+)?(?:Bankruptcy\s+)?Form\s+(\d{1,3}[A-Z]?(?:-\d+)?)",
        re.IGNORECASE
    )),
    ("texas_property_code", re.compile(
        r"(?:Tex(?:as)?\.?\s*Prop(?:erty)?\.?\s*Code\s*(?:\xA7|[Ss](?:ec)?\.?)\s*(\d+(?:\.\d+)?))",
        re.IGNORECASE
    )),
    ("texas_constitution", re.compile(
        r"(?:Tex(?:as)?\.?\s*Const(?:itution)?\.?\s*Art(?:icle)?\.?\s*(XVI|XVI\s*,?\s*\xA7\s*\d+))",
        re.IGNORECASE
    )),
    ("case_citation", re.compile(
        r"(\d+)\s+(U\.?S\.?|F\.?\s*(?:2d|3d|4th)|B\.?R\.?|Bankr\.?\s*(?:L\.?\s*Rep\.?)?)\s+(\d+)",
        re.IGNORECASE
    )),
    ("cfr", re.compile(
        r"(\d+)\s*C\.?F\.?R\.?\s*(?:\xA7|[Ss](?:ec)?\.?)\s*(\d+(?:\.\d+)?)",
        re.IGNORECASE
    )),
    ("in_re", re.compile(
        r"(?:In\s+re|Matter\s+of)\s+([A-Z][A-Za-z\s&,.'-]+?)(?:,\s*\d+\s+(?:B\.?R\.?|F\.)|\s*\()",
        re.IGNORECASE
    )),
]


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of normalizing a bankruptcy query."""

    original_query: str
    normalized_query: str
    canonical_terms: List[str]
    matched_synonyms: Dict[str, str]
    detected_citations: List[Dict[str, str]]
    detected_chapter: Optional[str]
    detected_categories: List[str]
    jurisdiction_hint: Optional[str]
    confidence: float
    normalization_time_ms: float
    tokens: List[str]
    stop_words_removed: int
    texas_specific: bool

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "canonical_terms": self.canonical_terms,
            "matched_synonyms": self.matched_synonyms,
            "detected_citations": self.detected_citations,
            "detected_chapter": self.detected_chapter,
            "detected_categories": self.detected_categories,
            "jurisdiction_hint": self.jurisdiction_hint,
            "confidence": round(self.confidence, 4),
            "normalization_time_ms": round(self.normalization_time_ms, 3),
            "tokens": self.tokens[:50],
            "stop_words_removed": self.stop_words_removed,
            "texas_specific": self.texas_specific,
        }


# ============================================================================
# STOP WORDS
# ============================================================================

STOP_WORDS: Set[str] = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "shall", "must", "need", "to", "of",
    "in", "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "above", "below", "between", "under",
    "about", "against", "and", "but", "or", "nor", "not", "so", "yet",
    "both", "either", "neither", "each", "every", "all", "any", "few",
    "more", "most", "other", "some", "such", "no", "only", "own", "same",
    "than", "too", "very", "just", "because", "if", "when", "where",
    "while", "how", "what", "which", "who", "whom", "this", "that",
    "these", "those", "i", "me", "my", "myself", "we", "our", "ours",
    "you", "your", "he", "him", "his", "she", "her", "it", "its",
    "they", "them", "their", "up", "out", "off", "over", "here", "there",
}


# ============================================================================
# CHAPTER DETECTION PATTERNS
# ============================================================================

CHAPTER_PATTERNS: Dict[str, re.Pattern] = {
    "chapter_7": re.compile(r"\b(?:chapter\s*7|ch\.?\s*7|liquidation)\b", re.IGNORECASE),
    "chapter_11": re.compile(r"\b(?:chapter\s*11|ch\.?\s*11|reorganiz|reorg|DIP\b|debtor.in.possession)\b", re.IGNORECASE),
    "chapter_13": re.compile(r"\b(?:chapter\s*13|ch\.?\s*13|wage\s*earner|repayment\s*plan)\b", re.IGNORECASE),
    "chapter_12": re.compile(r"\b(?:chapter\s*12|ch\.?\s*12|family\s*farmer|family\s*fisherman)\b", re.IGNORECASE),
    "chapter_15": re.compile(r"\b(?:chapter\s*15|ch\.?\s*15|cross.border|foreign\s*(?:main|nonmain)\s*proceeding)\b", re.IGNORECASE),
    "subchapter_v": re.compile(r"\b(?:sub(?:chapter)?\s*v|SBRA|small\s*business\s*(?:debtor|reorganization))\b", re.IGNORECASE),
}

TEXAS_PATTERNS: List[re.Pattern] = [
    re.compile(r"\btex(?:as)?\b", re.IGNORECASE),
    re.compile(r"\b(?:TX|Tex\.)\s*(?:Prop|Const)", re.IGNORECASE),
    re.compile(r"\b(?:unlimited\s*homestead|urban\s*10\s*acre|rural\s*200\s*acre)\b", re.IGNORECASE),
    re.compile(r"\b(?:western|northern|southern|eastern)\s*district\s*(?:of\s*)?texas\b", re.IGNORECASE),
]


# ============================================================================
# CORE NORMALIZATION FUNCTION
# ============================================================================

def normalize_query(query: str) -> NormalizationResult:
    """Normalize a bankruptcy-related query.

    Performs:
        1. Lowercase and whitespace normalization
        2. Stop word removal
        3. Synonym mapping to canonical terms
        4. Citation extraction
        5. Chapter type detection
        6. Category inference
        7. Texas-specific detection
        8. Jurisdiction hint extraction
    """
    start = time.monotonic()
    original = query.strip()
    lower = original.lower()

    # Tokenize
    raw_tokens = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", lower)
    stop_removed = 0
    filtered_tokens: List[str] = []
    for tok in raw_tokens:
        if tok in STOP_WORDS:
            stop_removed += 1
        else:
            filtered_tokens.append(tok)

    # Synonym matching
    canonical_terms: List[str] = []
    matched_synonyms: Dict[str, str] = {}
    detected_categories: Set[str] = set()

    for key, entry in SEMANTIC_MAP.items():
        for synonym in entry["synonyms"]:
            syn_lower = synonym.lower()
            if syn_lower in lower:
                canonical = entry["canonical"]
                if canonical not in canonical_terms:
                    canonical_terms.append(canonical)
                matched_synonyms[synonym] = canonical
                detected_categories.add(entry["category"])
                break

    # Citation extraction
    detected_citations: List[Dict[str, str]] = []
    for citation_type, pattern in CITATION_PATTERNS:
        for match in pattern.finditer(original):
            detected_citations.append({
                "type": citation_type,
                "text": match.group(0).strip(),
                "groups": [g for g in match.groups() if g],
            })

    # Chapter detection
    detected_chapter: Optional[str] = None
    for ch_key, ch_pattern in CHAPTER_PATTERNS.items():
        if ch_pattern.search(original):
            detected_chapter = ch_key
            break

    # Texas-specific detection
    texas_specific = any(pat.search(original) for pat in TEXAS_PATTERNS)

    # Jurisdiction hint
    jurisdiction_hint: Optional[str] = None
    if texas_specific:
        jurisdiction_hint = "texas_state"
        for dist_key in ["texas_western", "texas_northern", "texas_southern", "texas_eastern"]:
            dist_data = JURISDICTION_MAP.get(dist_key, {})
            label = dist_data.get("label", "")
            if label.lower().split()[-4:-1] == ["district", "of", "texas"]:
                pass
            district_name = dist_key.replace("texas_", "")
            if re.search(rf"\b{district_name}\b", lower):
                jurisdiction_hint = dist_key
                break
    elif detected_citations:
        jurisdiction_hint = "federal"

    # Build normalized query
    norm_parts = list(canonical_terms) if canonical_terms else filtered_tokens
    normalized_query = " ".join(norm_parts)

    # Confidence calculation
    base_confidence = 0.5
    if canonical_terms:
        base_confidence += min(len(canonical_terms) * 0.08, 0.3)
    if detected_citations:
        base_confidence += min(len(detected_citations) * 0.05, 0.15)
    if detected_chapter:
        base_confidence += 0.05
    confidence = min(base_confidence, 0.99)

    elapsed = (time.monotonic() - start) * 1000.0

    return NormalizationResult(
        original_query=original,
        normalized_query=normalized_query,
        canonical_terms=canonical_terms,
        matched_synonyms=matched_synonyms,
        detected_citations=detected_citations,
        detected_chapter=detected_chapter,
        detected_categories=sorted(detected_categories),
        jurisdiction_hint=jurisdiction_hint,
        confidence=confidence,
        normalization_time_ms=elapsed,
        tokens=filtered_tokens,
        stop_words_removed=stop_removed,
        texas_specific=texas_specific,
    )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

_SEMANTIC_MAP_HASH: Optional[str] = None


def get_semantic_map() -> Dict[str, Dict[str, Any]]:
    """Return the full semantic map."""
    return SEMANTIC_MAP


def get_semantic_map_hash() -> str:
    """Return a SHA-256 hash of the semantic map for integrity verification."""
    global _SEMANTIC_MAP_HASH
    if _SEMANTIC_MAP_HASH is None:
        content = json.dumps(SEMANTIC_MAP, sort_keys=True)
        _SEMANTIC_MAP_HASH = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return _SEMANTIC_MAP_HASH


def get_semantic_map_version() -> str:
    """Return the semantic map version string."""
    return f"2.0.0-{get_semantic_map_hash()[:8]}"


def get_jurisdiction_map() -> Dict[str, Dict[str, Any]]:
    """Return the jurisdiction map."""
    return JURISDICTION_MAP


def verify_dictionary_integrity() -> Dict[str, Any]:
    """Verify semantic dictionary structural integrity."""
    errors: List[str] = []
    warnings: List[str] = []
    total_synonyms = 0
    categories: Set[str] = set()

    for key, entry in SEMANTIC_MAP.items():
        if "canonical" not in entry:
            errors.append(f"Missing 'canonical' in entry '{key}'")
        if "synonyms" not in entry or not entry["synonyms"]:
            errors.append(f"Missing or empty 'synonyms' in entry '{key}'")
        else:
            total_synonyms += len(entry["synonyms"])
        if "category" not in entry:
            warnings.append(f"Missing 'category' in entry '{key}'")
        else:
            categories.add(entry["category"])
        if "weight" not in entry:
            warnings.append(f"Missing 'weight' in entry '{key}'")

    return {
        "valid": len(errors) == 0,
        "total_entries": len(SEMANTIC_MAP),
        "total_synonyms": total_synonyms,
        "categories": sorted(categories),
        "category_count": len(categories),
        "errors": errors,
        "warnings": warnings,
        "hash": get_semantic_map_hash(),
        "version": get_semantic_map_version(),
    }
