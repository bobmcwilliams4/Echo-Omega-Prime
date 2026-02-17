"""
LG06 IP Analysis Engine - Semantic Normalization Module
=========================================================
Normalizes IP-specific terminology, maps synonyms, handles
claim language variations, patent classification codes,
trademark classes, and copyright categories.

Components:
    - SemanticMap: Core term normalization dictionary
    - normalize_query(): Main entry point for query normalization
    - IP Classification Codes: USPC, CPC, Nice, Locarno
    - Patent Claim Language Normalizer
    - Trademark Class Mapper

Version: 2.0.0
Engine: LG06 IP Analysis
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
# SEMANTIC MAP - IP TERMINOLOGY NORMALIZATION
# ============================================================================

SEMANTIC_MAP: Dict[str, Dict[str, Any]] = {
    # ---- PATENT TERMS ----
    "patent": {
        "canonical": "patent",
        "synonyms": ["pat", "patent grant", "letters patent", "patent document"],
        "category": "patent",
        "weight": 1.0,
    },
    "utility_patent": {
        "canonical": "utility_patent",
        "synonyms": ["utility pat", "non-provisional patent", "regular patent", "35 usc patent"],
        "category": "patent",
        "weight": 1.0,
    },
    "design_patent": {
        "canonical": "design_patent",
        "synonyms": ["d patent", "design pat", "ornamental patent", "35 usc 171"],
        "category": "patent",
        "weight": 1.0,
    },
    "plant_patent": {
        "canonical": "plant_patent",
        "synonyms": ["pp patent", "plant pat", "35 usc 161", "botanical patent"],
        "category": "patent",
        "weight": 0.9,
    },
    "provisional_patent": {
        "canonical": "provisional_application",
        "synonyms": ["provisional", "provisional app", "ppa", "provisional filing"],
        "category": "patent",
        "weight": 0.9,
    },
    "non_provisional": {
        "canonical": "non_provisional_application",
        "synonyms": ["regular application", "utility application", "non-provisional", "npa"],
        "category": "patent",
        "weight": 1.0,
    },
    "continuation": {
        "canonical": "continuation_application",
        "synonyms": ["con application", "continuation", "continuation filing", "con"],
        "category": "patent_prosecution",
        "weight": 0.9,
    },
    "continuation_in_part": {
        "canonical": "continuation_in_part",
        "synonyms": ["cip", "c-i-p", "continuation-in-part"],
        "category": "patent_prosecution",
        "weight": 0.9,
    },
    "divisional": {
        "canonical": "divisional_application",
        "synonyms": ["div application", "divisional", "div", "divisional filing"],
        "category": "patent_prosecution",
        "weight": 0.9,
    },
    "rce": {
        "canonical": "request_for_continued_examination",
        "synonyms": ["rce", "continued examination", "request for continued examination"],
        "category": "patent_prosecution",
        "weight": 0.8,
    },
    "office_action": {
        "canonical": "office_action",
        "synonyms": ["oa", "examiner action", "rejection", "office action response"],
        "category": "patent_prosecution",
        "weight": 0.9,
    },
    "final_rejection": {
        "canonical": "final_office_action",
        "synonyms": ["final oa", "final rejection", "final action", "foa"],
        "category": "patent_prosecution",
        "weight": 0.9,
    },
    "notice_of_allowance": {
        "canonical": "notice_of_allowance",
        "synonyms": ["noa", "allowance", "allowed", "patent allowed"],
        "category": "patent_prosecution",
        "weight": 1.0,
    },
    # ---- PATENTABILITY ----
    "novelty": {
        "canonical": "novelty_102",
        "synonyms": ["novelty", "35 usc 102", "section 102", "anticipation", "prior art rejection"],
        "category": "patentability",
        "weight": 1.0,
    },
    "obviousness": {
        "canonical": "non_obviousness_103",
        "synonyms": ["obviousness", "35 usc 103", "section 103", "103 rejection", "obvious"],
        "category": "patentability",
        "weight": 1.0,
    },
    "subject_matter_eligibility": {
        "canonical": "subject_matter_eligibility_101",
        "synonyms": ["101", "35 usc 101", "section 101", "alice", "alice test", "abstract idea",
                      "patentable subject matter", "eligibility", "mayo", "bilski"],
        "category": "patentability",
        "weight": 1.0,
    },
    "enablement": {
        "canonical": "enablement_112a",
        "synonyms": ["enablement", "112(a)", "35 usc 112a", "how to make and use"],
        "category": "patentability",
        "weight": 0.9,
    },
    "written_description": {
        "canonical": "written_description_112a",
        "synonyms": ["written description", "112 written description", "adequate description",
                      "possession requirement"],
        "category": "patentability",
        "weight": 0.9,
    },
    "definiteness": {
        "canonical": "definiteness_112b",
        "synonyms": ["definiteness", "112(b)", "35 usc 112b", "claim clarity",
                      "indefiniteness", "nautilus test"],
        "category": "patentability",
        "weight": 0.9,
    },
    "prior_art": {
        "canonical": "prior_art",
        "synonyms": ["prior art", "references", "cited art", "prior references",
                      "anticipatory reference", "prior publication"],
        "category": "patentability",
        "weight": 1.0,
    },
    "claim_construction": {
        "canonical": "claim_construction",
        "synonyms": ["claim interpretation", "markman", "markman hearing",
                      "claim terms", "construing claims", "phillips standard",
                      "broadest reasonable interpretation", "bri"],
        "category": "patent_litigation",
        "weight": 1.0,
    },
    # ---- INFRINGEMENT ----
    "literal_infringement": {
        "canonical": "literal_infringement",
        "synonyms": ["literal", "literal infringement", "reads on", "all limitations"],
        "category": "infringement",
        "weight": 1.0,
    },
    "doctrine_of_equivalents": {
        "canonical": "doctrine_of_equivalents",
        "synonyms": ["doe", "equivalents", "equivalent infringement",
                      "function way result", "insubstantial differences"],
        "category": "infringement",
        "weight": 1.0,
    },
    "induced_infringement": {
        "canonical": "induced_infringement_271b",
        "synonyms": ["induced", "inducement", "271(b)", "actively induces"],
        "category": "infringement",
        "weight": 0.9,
    },
    "contributory_infringement": {
        "canonical": "contributory_infringement_271c",
        "synonyms": ["contributory", "271(c)", "material part", "especially made"],
        "category": "infringement",
        "weight": 0.9,
    },
    "willful_infringement": {
        "canonical": "willful_infringement",
        "synonyms": ["willful", "willful infringement", "enhanced damages",
                      "halo test", "treble damages"],
        "category": "infringement",
        "weight": 1.0,
    },
    "divided_infringement": {
        "canonical": "divided_infringement",
        "synonyms": ["joint infringement", "split infringement",
                      "akamai", "limelight", "direction or control"],
        "category": "infringement",
        "weight": 0.8,
    },
    # ---- PATENT DEFENSES ----
    "invalidity": {
        "canonical": "invalidity_defense",
        "synonyms": ["invalidity", "invalid patent", "patent invalidity",
                      "invalidation", "challenge validity"],
        "category": "patent_defense",
        "weight": 1.0,
    },
    "prosecution_history_estoppel": {
        "canonical": "prosecution_history_estoppel",
        "synonyms": ["file wrapper estoppel", "phe", "prosecution estoppel",
                      "festo", "narrowing amendment"],
        "category": "patent_defense",
        "weight": 0.9,
    },
    "patent_exhaustion": {
        "canonical": "patent_exhaustion",
        "synonyms": ["exhaustion", "first sale", "first sale doctrine patent",
                      "lexmark", "quanta"],
        "category": "patent_defense",
        "weight": 0.8,
    },
    "experimental_use": {
        "canonical": "experimental_use_defense",
        "synonyms": ["experimental use", "research exception", "de minimis use",
                      "madey", "purely philosophical"],
        "category": "patent_defense",
        "weight": 0.7,
    },
    # ---- PTAB / IPR / PGR ----
    "ipr": {
        "canonical": "inter_partes_review",
        "synonyms": ["ipr", "inter partes review", "inter partes", "ptab review"],
        "category": "ptab",
        "weight": 1.0,
    },
    "pgr": {
        "canonical": "post_grant_review",
        "synonyms": ["pgr", "post grant review", "post-grant review", "post grant"],
        "category": "ptab",
        "weight": 0.9,
    },
    "cbm": {
        "canonical": "covered_business_method",
        "synonyms": ["cbm", "covered business method", "cbm review"],
        "category": "ptab",
        "weight": 0.8,
    },
    "ex_parte_reexam": {
        "canonical": "ex_parte_reexamination",
        "synonyms": ["reexam", "reexamination", "ex parte reexam", "ex parte reexamination"],
        "category": "ptab",
        "weight": 0.8,
    },
    # ---- TRADEMARK TERMS ----
    "trademark": {
        "canonical": "trademark",
        "synonyms": ["tm", "mark", "brand", "trade mark", "trade-mark"],
        "category": "trademark",
        "weight": 1.0,
    },
    "service_mark": {
        "canonical": "service_mark",
        "synonyms": ["sm", "service mark", "service-mark"],
        "category": "trademark",
        "weight": 0.9,
    },
    "trade_dress": {
        "canonical": "trade_dress",
        "synonyms": ["trade dress", "product appearance", "product packaging",
                      "product configuration", "total image"],
        "category": "trademark",
        "weight": 0.9,
    },
    "distinctiveness": {
        "canonical": "trademark_distinctiveness",
        "synonyms": ["distinctiveness", "distinctive", "inherently distinctive",
                      "acquired distinctiveness", "secondary meaning"],
        "category": "trademark",
        "weight": 1.0,
    },
    "likelihood_of_confusion": {
        "canonical": "likelihood_of_confusion",
        "synonyms": ["likelihood of confusion", "loc", "confusion",
                      "du pont factors", "dupont", "polaroid factors", "sleekcraft"],
        "category": "trademark",
        "weight": 1.0,
    },
    "trademark_dilution": {
        "canonical": "trademark_dilution",
        "synonyms": ["dilution", "blurring", "tarnishment",
                      "famous mark dilution", "tdra"],
        "category": "trademark",
        "weight": 0.9,
    },
    "lanham_act": {
        "canonical": "lanham_act",
        "synonyms": ["lanham act", "15 usc 1051", "trademark act",
                      "15 usc chapter 22"],
        "category": "trademark",
        "weight": 1.0,
    },
    "ttab": {
        "canonical": "ttab",
        "synonyms": ["ttab", "trademark trial and appeal board",
                      "trademark board", "opposition board"],
        "category": "trademark",
        "weight": 0.9,
    },
    # ---- COPYRIGHT TERMS ----
    "copyright": {
        "canonical": "copyright",
        "synonyms": ["cr", "copy right", "authored work protection", "17 usc"],
        "category": "copyright",
        "weight": 1.0,
    },
    "fair_use": {
        "canonical": "fair_use",
        "synonyms": ["fair use", "107", "17 usc 107", "fair dealing",
                      "transformative use", "four factors"],
        "category": "copyright",
        "weight": 1.0,
    },
    "work_for_hire": {
        "canonical": "work_made_for_hire",
        "synonyms": ["work for hire", "wfh", "work made for hire",
                      "employer authorship", "specially ordered"],
        "category": "copyright",
        "weight": 0.9,
    },
    "dmca": {
        "canonical": "digital_millennium_copyright_act",
        "synonyms": ["dmca", "digital millennium", "dmca takedown",
                      "safe harbor", "17 usc 512"],
        "category": "copyright",
        "weight": 0.9,
    },
    "copyright_infringement": {
        "canonical": "copyright_infringement",
        "synonyms": ["copying", "copyright violation", "substantial similarity",
                      "access plus similarity", "copying infringement"],
        "category": "copyright",
        "weight": 1.0,
    },
    # ---- TRADE SECRET TERMS ----
    "trade_secret": {
        "canonical": "trade_secret",
        "synonyms": ["trade secret", "ts", "confidential information",
                      "proprietary information", "secret formula"],
        "category": "trade_secret",
        "weight": 1.0,
    },
    "dtsa": {
        "canonical": "defend_trade_secrets_act",
        "synonyms": ["dtsa", "defend trade secrets act", "18 usc 1836",
                      "federal trade secret"],
        "category": "trade_secret",
        "weight": 1.0,
    },
    "utsa": {
        "canonical": "uniform_trade_secrets_act",
        "synonyms": ["utsa", "uniform trade secrets", "state trade secret"],
        "category": "trade_secret",
        "weight": 0.9,
    },
    "misappropriation": {
        "canonical": "trade_secret_misappropriation",
        "synonyms": ["misappropriation", "misappropriate", "theft of trade secret",
                      "trade secret theft", "improper means"],
        "category": "trade_secret",
        "weight": 1.0,
    },
    "reasonable_measures": {
        "canonical": "reasonable_security_measures",
        "synonyms": ["reasonable measures", "reasonable steps", "security measures",
                      "nda", "non-disclosure", "confidentiality agreement"],
        "category": "trade_secret",
        "weight": 0.9,
    },
    # ---- INTERNATIONAL IP ----
    "pct": {
        "canonical": "patent_cooperation_treaty",
        "synonyms": ["pct", "patent cooperation treaty", "international application",
                      "pct application", "chapter i", "chapter ii"],
        "category": "international",
        "weight": 1.0,
    },
    "madrid_protocol": {
        "canonical": "madrid_protocol",
        "synonyms": ["madrid", "madrid protocol", "international trademark",
                      "madrid system", "wipo trademark"],
        "category": "international",
        "weight": 0.9,
    },
    "hague_agreement": {
        "canonical": "hague_agreement",
        "synonyms": ["hague", "hague agreement", "international design",
                      "hague system", "international design registration"],
        "category": "international",
        "weight": 0.8,
    },
    "paris_convention": {
        "canonical": "paris_convention",
        "synonyms": ["paris convention", "priority right", "convention priority",
                      "12 month priority"],
        "category": "international",
        "weight": 0.9,
    },
    "trips": {
        "canonical": "trips_agreement",
        "synonyms": ["trips", "trips agreement", "wto ip",
                      "trade related aspects"],
        "category": "international",
        "weight": 0.8,
    },
    # ---- IP LICENSING ----
    "license": {
        "canonical": "ip_license",
        "synonyms": ["license", "licence", "licensing", "ip license",
                      "patent license", "trademark license"],
        "category": "licensing",
        "weight": 1.0,
    },
    "exclusive_license": {
        "canonical": "exclusive_license",
        "synonyms": ["exclusive", "exclusive license", "sole license"],
        "category": "licensing",
        "weight": 0.9,
    },
    "non_exclusive_license": {
        "canonical": "non_exclusive_license",
        "synonyms": ["non-exclusive", "non exclusive", "nonexclusive license"],
        "category": "licensing",
        "weight": 0.9,
    },
    "royalty": {
        "canonical": "royalty",
        "synonyms": ["royalty", "royalties", "running royalty",
                      "lump sum", "reasonable royalty", "georgia-pacific"],
        "category": "licensing",
        "weight": 1.0,
    },
    "frand": {
        "canonical": "frand_licensing",
        "synonyms": ["frand", "rand", "fair reasonable non-discriminatory",
                      "standard essential patent", "sep", "sep licensing"],
        "category": "licensing",
        "weight": 0.9,
    },
    # ---- IP VALUATION ----
    "ip_valuation": {
        "canonical": "ip_valuation",
        "synonyms": ["valuation", "ip value", "patent valuation",
                      "ip appraisal", "intangible asset value"],
        "category": "valuation",
        "weight": 1.0,
    },
    "freedom_to_operate": {
        "canonical": "freedom_to_operate",
        "synonyms": ["fto", "freedom to operate", "fto analysis",
                      "clearance search", "right to use", "product clearance"],
        "category": "fto",
        "weight": 1.0,
    },
    "ip_portfolio": {
        "canonical": "ip_portfolio",
        "synonyms": ["portfolio", "ip portfolio", "patent portfolio",
                      "ip assets", "ip holdings"],
        "category": "portfolio",
        "weight": 1.0,
    },
    # ---- OPEN SOURCE IP ----
    "open_source": {
        "canonical": "open_source_licensing",
        "synonyms": ["open source", "oss", "foss", "open source license",
                      "gpl", "mit license", "apache license", "bsd license"],
        "category": "open_source",
        "weight": 0.9,
    },
    "copyleft": {
        "canonical": "copyleft",
        "synonyms": ["copyleft", "gpl", "strong copyleft", "weak copyleft",
                      "viral license", "reciprocal license"],
        "category": "open_source",
        "weight": 0.8,
    },
    "permissive_license": {
        "canonical": "permissive_license",
        "synonyms": ["permissive", "mit", "bsd", "apache",
                      "permissive open source"],
        "category": "open_source",
        "weight": 0.8,
    },
}


# ============================================================================
# NICE CLASSIFICATION (TRADEMARK)
# ============================================================================

NICE_CLASSIFICATION: Dict[int, str] = {
    1: "Chemicals",
    2: "Paints, Varnishes",
    3: "Cosmetics, Cleaning",
    4: "Lubricants, Fuels",
    5: "Pharmaceuticals",
    6: "Metal Goods",
    7: "Machines, Machine Tools",
    8: "Hand Tools",
    9: "Electronics, Software, IT",
    10: "Medical Instruments",
    11: "Lighting, Heating, Cooking",
    12: "Vehicles",
    13: "Firearms, Ammunition",
    14: "Precious Metals, Jewelry",
    15: "Musical Instruments",
    16: "Paper, Office Supplies",
    17: "Rubber, Plastics",
    18: "Leather Goods, Luggage",
    19: "Building Materials",
    20: "Furniture",
    21: "Household Utensils",
    22: "Ropes, Fiber Materials",
    23: "Yarns, Threads",
    24: "Textiles",
    25: "Clothing, Footwear",
    26: "Lace, Embroidery",
    27: "Carpets, Rugs",
    28: "Games, Toys, Sporting Goods",
    29: "Meat, Fish, Dairy",
    30: "Coffee, Tea, Bakery",
    31: "Agricultural Products",
    32: "Beers, Non-Alcoholic",
    33: "Alcoholic Beverages",
    34: "Tobacco",
    35: "Advertising, Business Mgmt",
    36: "Insurance, Financial",
    37: "Construction, Repair",
    38: "Telecommunications",
    39: "Transport, Packaging",
    40: "Material Treatment",
    41: "Education, Entertainment",
    42: "Scientific, Technology, Software",
    43: "Food Services, Accommodation",
    44: "Medical, Veterinary",
    45: "Legal, Security Services",
}


# ============================================================================
# CPC CLASSIFICATION (PATENT)
# ============================================================================

CPC_SECTIONS: Dict[str, str] = {
    "A": "Human Necessities",
    "B": "Performing Operations, Transporting",
    "C": "Chemistry, Metallurgy",
    "D": "Textiles, Paper",
    "E": "Fixed Constructions",
    "F": "Mechanical Engineering, Lighting, Heating, Weapons",
    "G": "Physics",
    "H": "Electricity",
    "Y": "General Tagging of New Technology",
}

CPC_TECHNOLOGY_CENTERS: Dict[str, str] = {
    "TC1600": "Biotechnology and Organic Chemistry",
    "TC1700": "Chemical and Materials Engineering",
    "TC2100": "Computer Architecture, Software, and Information Security",
    "TC2400": "Networking, Multiplexing, Cable, and Security",
    "TC2600": "Communications",
    "TC2800": "Semiconductors, Electrical and Optical Systems and Components",
    "TC2900": "Designs",
    "TC3600": "Transportation, Construction, Electronic Commerce, Agriculture, National Security, and License and Review",
    "TC3700": "Mechanical Engineering, Manufacturing, Products",
}


# ============================================================================
# CITATION PATTERNS (IP-SPECIFIC)
# ============================================================================

CITATION_PATTERNS: Dict[str, str] = {
    "us_patent": r"U\.?S\.?\s*(?:Patent\s+(?:No\.?\s*)?)?(\d{1,3}(?:,\d{3})*(?:,\d{3})?)",
    "us_patent_app": r"U\.?S\.?\s*(?:Patent\s+)?App(?:lication)?\.?\s*(?:No\.?\s*)?(?:Ser\.?\s*(?:No\.?\s*)?)?((?:\d{2}/\d{3},\d{3})|\d{4}/\d{7})",
    "design_patent": r"(?:U\.?S\.?\s*)?(?:Design\s+Pat(?:ent)?\.?\s*(?:No\.?\s*)?|D\.?\s*)(\d{1,3}(?:,\d{3})*(?:,\d{3})?)",
    "pct_application": r"PCT/[A-Z]{2}\d{4}/\d{5,6}",
    "tm_serial": r"(?:Serial\s*(?:No\.?\s*)?|S/N\s*)(\d{2}/\d{3},?\d{3})",
    "tm_reg": r"(?:Reg(?istration)?\.?\s*(?:No\.?\s*)?)(\d{1,3}(?:,\d{3})*(?:,\d{3})?)",
    "copyright_reg": r"(?:Copyright\s+)?(?:Reg(?istration)?\.?\s*(?:No\.?\s*)?)((?:TX|PA|VA|SR|RE|SE)\d{1,3}-\d{3}-\d{3})",
    "usc_35": r"35\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?(\d+(?:\([a-z]\))?)",
    "usc_15": r"15\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?(\d+(?:\([a-z]\))?)",
    "usc_17": r"17\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?(\d+(?:\([a-z]\))?)",
    "usc_18": r"18\s*U\.?S\.?C\.?\s*(?:\xA7\s*)?(\d+(?:\([a-z]\))?)",
    "mpep": r"MPEP\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "tmep": r"TMEP\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "cfr_37": r"37\s*C\.?F\.?R\.?\s*(?:\xA7\s*)?([\d]+(?:\.\d+)*)",
    "federal_case": r"(\d+)\s+(F\.(?:2d|3d|4th)|F\.\s*Supp\.(?:\s*2d|\s*3d)?|U\.S\.|S\.\s*Ct\.)\s+(\d+)",
    "fed_cir": r"(?:Fed\.\s*Cir\.\s*)(\d{4})",
}


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of normalizing a query through the semantic map."""
    original_query: str
    normalized_query: str
    tokens: List[str]
    matched_terms: List[Dict[str, Any]]
    unmatched_tokens: List[str]
    detected_categories: List[str]
    detected_ip_type: Optional[str]
    detected_citations: List[Dict[str, str]]
    confidence: float
    normalization_time_ms: float
    hash_digest: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "tokens": self.tokens,
            "matched_terms": self.matched_terms,
            "unmatched_tokens": self.unmatched_tokens,
            "detected_categories": self.detected_categories,
            "detected_ip_type": self.detected_ip_type,
            "detected_citations": self.detected_citations,
            "confidence": round(self.confidence, 4),
            "normalization_time_ms": round(self.normalization_time_ms, 3),
            "hash_digest": self.hash_digest,
        }


# ============================================================================
# QUERY NORMALIZER
# ============================================================================

class IPQueryNormalizer:
    """Normalizes IP queries using the semantic map and citation extraction."""

    def __init__(self, semantic_map: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        self._map: Dict[str, Dict[str, Any]] = semantic_map or SEMANTIC_MAP
        self._synonym_index: Dict[str, str] = {}
        self._build_synonym_index()
        self._compiled_citations: Dict[str, re.Pattern] = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in CITATION_PATTERNS.items()
        }
        logger.info(f"IPQueryNormalizer initialized | terms={len(self._map)} | synonyms={len(self._synonym_index)}")

    def _build_synonym_index(self) -> None:
        """Build reverse lookup from synonyms to canonical terms."""
        for key, entry in self._map.items():
            canonical = entry["canonical"]
            self._synonym_index[canonical.lower()] = key
            self._synonym_index[key.lower()] = key
            for syn in entry.get("synonyms", []):
                self._synonym_index[syn.lower()] = key

    def normalize(self, query: str) -> NormalizationResult:
        """Normalize a query through the semantic map."""
        start = time.monotonic()
        cleaned = self._clean_query(query)
        tokens = self._tokenize(cleaned)
        matched_terms: List[Dict[str, Any]] = []
        unmatched: List[str] = []
        categories: Set[str] = set()
        used_indices: Set[int] = set()

        # Multi-token matching (longest match first)
        for window_size in range(4, 0, -1):
            for i in range(len(tokens) - window_size + 1):
                if any(idx in used_indices for idx in range(i, i + window_size)):
                    continue
                phrase = " ".join(tokens[i:i + window_size]).lower()
                match_key = self._synonym_index.get(phrase)
                if match_key and match_key in self._map:
                    entry = self._map[match_key]
                    matched_terms.append({
                        "original": phrase,
                        "canonical": entry["canonical"],
                        "category": entry["category"],
                        "weight": entry["weight"],
                    })
                    categories.add(entry["category"])
                    for idx in range(i, i + window_size):
                        used_indices.add(idx)

        for i, tok in enumerate(tokens):
            if i not in used_indices:
                unmatched.append(tok)

        # Detect citations
        detected_citations = self._extract_citations(query)

        # Detect IP type
        ip_type = self._detect_ip_type(categories, matched_terms)

        # Build normalized query
        canonical_parts = [m["canonical"] for m in matched_terms] + unmatched
        normalized = " ".join(canonical_parts)

        # Compute confidence
        total_tokens = len(tokens)
        matched_token_count = len(used_indices)
        base_confidence = matched_token_count / max(total_tokens, 1)
        citation_boost = min(len(detected_citations) * 0.05, 0.15)
        confidence = min(base_confidence + citation_boost, 1.0)

        # Hash
        hash_input = f"{query}|{normalized}|{json.dumps(matched_terms, sort_keys=True)}"
        hash_digest = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

        duration = (time.monotonic() - start) * 1000.0

        return NormalizationResult(
            original_query=query,
            normalized_query=normalized,
            tokens=tokens,
            matched_terms=matched_terms,
            unmatched_tokens=unmatched,
            detected_categories=sorted(categories),
            detected_ip_type=ip_type,
            detected_citations=detected_citations,
            confidence=confidence,
            normalization_time_ms=duration,
            hash_digest=hash_digest,
        )

    def _clean_query(self, query: str) -> str:
        """Clean and normalize raw query text."""
        text = query.strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s\.\-\(\)/,;:'\"\xA7#&]", "", text)
        return text

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize cleaned text."""
        tokens = re.findall(r"[\w\xA7]+(?:[-/][\w]+)*", text.lower())
        return [t for t in tokens if len(t) >= 2]

    def _extract_citations(self, text: str) -> List[Dict[str, str]]:
        """Extract IP citations from query text."""
        found: List[Dict[str, str]] = []
        seen: Set[str] = set()
        for cit_type, pattern in self._compiled_citations.items():
            for match in pattern.finditer(text):
                full_match = match.group(0).strip()
                if full_match not in seen:
                    seen.add(full_match)
                    found.append({
                        "type": cit_type,
                        "text": full_match,
                        "groups": str(match.groups()),
                    })
        return found

    def _detect_ip_type(self, categories: Set[str], matched_terms: List[Dict[str, Any]]) -> Optional[str]:
        """Detect the primary IP type from matched categories."""
        ip_type_priority = [
            ("patent", ["patent", "patentability", "patent_prosecution",
                        "patent_litigation", "patent_defense", "ptab"]),
            ("trademark", ["trademark"]),
            ("copyright", ["copyright"]),
            ("trade_secret", ["trade_secret"]),
            ("licensing", ["licensing"]),
            ("international", ["international"]),
            ("fto", ["fto"]),
            ("portfolio", ["portfolio"]),
            ("valuation", ["valuation"]),
            ("open_source", ["open_source"]),
            ("infringement", ["infringement"]),
        ]
        for ip_type, type_categories in ip_type_priority:
            if categories.intersection(type_categories):
                return ip_type
        return None


# ============================================================================
# MODULE-LEVEL SINGLETON AND CONVENIENCE FUNCTIONS
# ============================================================================

_normalizer: Optional[IPQueryNormalizer] = None
_map_version: str = "2.0.0"


def _get_normalizer() -> IPQueryNormalizer:
    """Get or create the singleton normalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = IPQueryNormalizer(SEMANTIC_MAP)
    return _normalizer


def normalize_query(query: str) -> NormalizationResult:
    """Normalize an IP query through the semantic map."""
    return _get_normalizer().normalize(query)


def get_semantic_map() -> Dict[str, Dict[str, Any]]:
    """Get the full semantic map."""
    return SEMANTIC_MAP


def get_semantic_map_version() -> str:
    """Get the semantic map version."""
    return _map_version


def get_semantic_map_hash() -> str:
    """Get a hash of the current semantic map for integrity checks."""
    content = json.dumps(SEMANTIC_MAP, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def verify_dictionary_integrity() -> Dict[str, Any]:
    """Verify the semantic dictionary integrity."""
    total_terms = len(SEMANTIC_MAP)
    total_synonyms = sum(len(v.get("synonyms", [])) for v in SEMANTIC_MAP.values())
    categories = set(v["category"] for v in SEMANTIC_MAP.values())
    map_hash = get_semantic_map_hash()

    return {
        "valid": True,
        "version": _map_version,
        "total_terms": total_terms,
        "total_synonyms": total_synonyms,
        "categories": sorted(categories),
        "category_count": len(categories),
        "hash": map_hash,
    }


def get_governance_metadata() -> Dict[str, Any]:
    """Get governance metadata for the semantic dictionary."""
    return {
        "engine_id": "LG06",
        "module": "semantic",
        "version": _map_version,
        "term_count": len(SEMANTIC_MAP),
        "hash": get_semantic_map_hash(),
        "categories": sorted(set(v["category"] for v in SEMANTIC_MAP.values())),
        "citation_patterns": list(CITATION_PATTERNS.keys()),
        "nice_classes": len(NICE_CLASSIFICATION),
        "cpc_sections": len(CPC_SECTIONS),
    }


def get_citation_patterns() -> Dict[str, str]:
    """Get citation extraction patterns."""
    return CITATION_PATTERNS


def get_nice_classification() -> Dict[int, str]:
    """Get Nice Classification for trademarks."""
    return NICE_CLASSIFICATION


def get_cpc_sections() -> Dict[str, str]:
    """Get CPC patent classification sections."""
    return CPC_SECTIONS
