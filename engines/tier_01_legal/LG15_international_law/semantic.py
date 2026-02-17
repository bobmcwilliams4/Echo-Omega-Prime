"""
LG15 International Law Engine - Semantic Normalization
=======================================================
Synonym mapping, query normalization, treaty entity extraction,
issue classification, and specialized analyzers for treaty interpretation,
sanctions screening, and conflict of laws resolution.

Engine: LG15 | Version: 2.0.0 | TIE Pattern
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field

ENGINE_ROOT = Path(__file__).parent
ENGINE_ID = "LG15"
HASH_SALT = "LG15_INTL_SEMANTIC_v2"


# ---------------------------------------------------------------------------
# Synonym Map (40+ entries)
# ---------------------------------------------------------------------------

SYNONYM_MAP: Dict[str, str] = {
    "mfn": "most favored nation",
    "most-favored-nation": "most favored nation",
    "most-favoured-nation": "most favored nation",
    "bit": "bilateral investment treaty",
    "bits": "bilateral investment treaties",
    "isds": "investor-state dispute settlement",
    "icsid": "international centre for settlement of investment disputes",
    "icj": "international court of justice",
    "icc": "international criminal court",
    "icc arb": "icc international court of arbitration",
    "uncitral": "united nations commission on international trade law",
    "cisg": "convention on contracts for international sale of goods",
    "vclt": "vienna convention on the law of treaties",
    "vcdr": "vienna convention on diplomatic relations",
    "vccr": "vienna convention on consular relations",
    "unclos": "united nations convention on the law of the sea",
    "fsia": "foreign sovereign immunities act",
    "fcpa": "foreign corrupt practices act",
    "ofac": "office of foreign assets control",
    "sdn": "specially designated nationals",
    "sdn list": "specially designated nationals list",
    "ear": "export administration regulations",
    "itar": "international traffic in arms regulations",
    "bis": "bureau of industry and security",
    "ddtc": "directorate of defense trade controls",
    "ieepa": "international emergency economic powers act",
    "trips": "trade-related aspects of intellectual property rights",
    "gatt": "general agreement on tariffs and trade",
    "gats": "general agreement on trade in services",
    "dsu": "dispute settlement understanding",
    "wto": "world trade organization",
    "echr": "european convention on human rights",
    "ecthr": "european court of human rights",
    "iccpr": "international covenant on civil and political rights",
    "icescr": "international covenant on economic social and cultural rights",
    "hrc": "human rights committee",
    "ndc": "nationally determined contribution",
    "ndcs": "nationally determined contributions",
    "eez": "exclusive economic zone",
    "isa": "international seabed authority",
    "itlos": "international tribunal for the law of the sea",
    "pca": "permanent court of arbitration",
    "icrc": "international committee of the red cross",
    "ihl": "international humanitarian law",
    "pow": "prisoner of war",
    "pows": "prisoners of war",
    "fet": "fair and equitable treatment",
    "ny convention": "new york convention on recognition and enforcement of arbitral awards",
    "lcia": "london court of international arbitration",
    "siac": "singapore international arbitration centre",
    "hkiac": "hong kong international arbitration centre",
    "dpa": "deferred prosecution agreement",
    "npa": "non-prosecution agreement",
    "scm": "subsidies and countervailing measures",
    "sps": "sanitary and phytosanitary measures",
    "tbt": "technical barriers to trade",
    "usmca": "united states-mexico-canada agreement",
    "nafta": "north american free trade agreement",
    "cptpp": "comprehensive and progressive agreement for trans-pacific partnership",
    "rcep": "regional comprehensive economic partnership",
}


# ---------------------------------------------------------------------------
# Category Map (15+ categories)
# ---------------------------------------------------------------------------

CATEGORY_MAP: Dict[str, List[str]] = {
    "public_international_law": [
        "un charter", "use of force", "self-defense", "self-defence",
        "chapter vii", "security council", "general assembly",
        "state responsibility", "attribution", "customary international law",
        "opinio juris", "jus cogens", "peremptory norm", "erga omnes",
        "sovereignty", "self-determination", "non-intervention",
    ],
    "treaty_law": [
        "treaty", "vclt", "vienna convention", "interpretation",
        "reservation", "ratification", "accession", "travaux",
        "preparatory work", "object and purpose", "jus cogens",
        "treaty termination", "suspension", "denunciation",
    ],
    "international_trade_law": [
        "wto", "gatt", "mfn", "most favored nation", "national treatment",
        "tariff", "dumping", "anti-dumping", "subsidy", "countervailing",
        "safeguard", "dispute settlement", "appellate body",
        "trips", "intellectual property", "patent", "trademark", "copyright",
    ],
    "international_arbitration": [
        "arbitration", "uncitral", "icsid", "icc arbitration",
        "lcia", "siac", "arbitral award", "enforcement",
        "new york convention", "annulment", "provisional measures",
        "kompetenz", "separability", "seat", "lex arbitri",
    ],
    "international_investment_law": [
        "investment", "bilateral investment treaty", "bit",
        "fair and equitable treatment", "expropriation", "isds",
        "investor-state", "umbrella clause", "most constant protection",
        "full protection and security", "national treatment",
    ],
    "international_humanitarian_law": [
        "geneva convention", "humanitarian", "armed conflict",
        "prisoner of war", "civilian protection", "distinction",
        "proportionality", "military necessity", "red cross",
        "hague convention", "laws of war", "grave breach",
        "common article 3", "additional protocol",
    ],
    "international_human_rights": [
        "human rights", "iccpr", "icescr", "echr",
        "right to life", "torture", "freedom of expression",
        "non-discrimination", "margin of appreciation",
        "derogation", "non-refoulement",
    ],
    "international_criminal_law": [
        "icc", "rome statute", "genocide", "crimes against humanity",
        "war crimes", "aggression", "complementarity",
        "lubanga", "al bashir", "nuremberg", "icty", "ictr",
    ],
    "law_of_the_sea": [
        "unclos", "law of the sea", "territorial sea", "eez",
        "exclusive economic zone", "continental shelf", "high seas",
        "deep seabed", "maritime", "itlos", "baselines",
        "innocent passage", "transit passage",
    ],
    "foreign_sovereign_immunity": [
        "fsia", "sovereign immunity", "foreign sovereign",
        "commercial activity exception", "terrorism exception",
        "jure imperii", "jure gestionis", "restrictive theory",
    ],
    "sanctions_export_controls": [
        "ofac", "sanctions", "sdn", "embargo", "export control",
        "ear", "itar", "bis", "entity list", "denied persons",
        "blocking", "asset freeze", "license", "general license",
    ],
    "anti_corruption": [
        "fcpa", "bribery", "corruption", "uk bribery act",
        "foreign official", "facilitation payment", "improper advantage",
        "anti-corruption", "oecd anti-bribery", "compliance",
    ],
    "international_commercial_law": [
        "cisg", "sale of goods", "formation", "breach", "remedies",
        "fundamental breach", "nachfrist", "avoidance", "damages",
        "incoterms", "letter of credit", "ucp 600",
    ],
    "international_environmental_law": [
        "paris agreement", "climate", "ndc", "unfccc",
        "montreal protocol", "ozone", "biodiversity",
        "environmental", "sustainable development",
        "loss and damage", "carbon market",
    ],
    "private_international_law": [
        "conflict of laws", "choice of law", "characterization",
        "renvoi", "public policy", "ordre public",
        "service abroad", "hague service", "hague evidence",
        "foreign judgment", "recognition", "enforcement",
        "rome i", "rome ii", "applicable law", "connecting factor",
    ],
    "diplomatic_consular_law": [
        "diplomatic immunity", "consular immunity", "vcdr", "vccr",
        "inviolability", "persona non grata", "diplomatic bag",
        "waiver of immunity", "functional immunity",
    ],
}


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class NormalizedQuery(BaseModel):
    """Result of query normalization."""
    original: str
    normalized: str
    expanded_terms: List[str] = Field(default_factory=list)
    detected_categories: List[str] = Field(default_factory=list)
    detected_entities: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    hash_key: str = ""


class TreatyEntity(BaseModel):
    """An extracted treaty or instrument reference."""
    name: str
    abbreviation: str = ""
    year: Optional[int] = None
    article: Optional[str] = None
    parties: Optional[int] = None
    entity_type: str = "treaty"


class IssueClassification(BaseModel):
    """Classification result for an international law issue."""
    primary_category: str
    secondary_categories: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    keywords_matched: List[str] = Field(default_factory=list)
    suggested_doctrines: List[str] = Field(default_factory=list)


class SanctionsScreenResult(BaseModel):
    """Result of a sanctions screening analysis."""
    query_entity: str
    risk_level: str = "UNKNOWN"
    matched_programs: List[str] = Field(default_factory=list)
    matched_lists: List[str] = Field(default_factory=list)
    flags: List[str] = Field(default_factory=list)
    recommendation: str = ""
    confidence: float = 0.0


class ConflictOfLawsResult(BaseModel):
    """Result of conflict of laws analysis."""
    issue_characterization: str = ""
    connecting_factors: List[str] = Field(default_factory=list)
    candidate_laws: List[str] = Field(default_factory=list)
    recommended_approach: str = ""
    renvoi_risk: bool = False
    public_policy_concern: bool = False
    applicable_conventions: List[str] = Field(default_factory=list)


class TreatyInterpretationResult(BaseModel):
    """Result of Vienna Convention treaty interpretation analysis."""
    treaty: str = ""
    provision: str = ""
    ordinary_meaning: str = ""
    context_analysis: str = ""
    object_and_purpose: str = ""
    subsequent_practice: str = ""
    supplementary_means: str = ""
    interpretation_conclusion: str = ""
    confidence: float = 0.0


class SemanticSimilarityResult(BaseModel):
    """Result of semantic similarity computation."""
    query_a: str
    query_b: str
    similarity_score: float = 0.0
    shared_terms: List[str] = Field(default_factory=list)
    shared_categories: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Treaty patterns for entity extraction
# ---------------------------------------------------------------------------

TREATY_PATTERNS: List[Dict[str, Any]] = [
    {"pattern": r"\b(?:UN\s+Charter|Charter\s+of\s+the\s+United\s+Nations)\b",
     "name": "UN Charter", "abbrev": "UN Charter", "year": 1945},
    {"pattern": r"\b(?:VCLT|Vienna\s+Convention\s+on\s+(?:the\s+)?Law\s+of\s+Treaties)\b",
     "name": "Vienna Convention on the Law of Treaties", "abbrev": "VCLT", "year": 1969},
    {"pattern": r"\b(?:VCDR|Vienna\s+Convention\s+on\s+Diplomatic\s+Relations)\b",
     "name": "Vienna Convention on Diplomatic Relations", "abbrev": "VCDR", "year": 1961},
    {"pattern": r"\bICJ\s+Statute\b",
     "name": "Statute of the International Court of Justice", "abbrev": "ICJ Statute", "year": 1945},
    {"pattern": r"\b(?:UNCLOS|(?:United\s+Nations\s+)?Convention\s+on\s+(?:the\s+)?Law\s+of\s+the\s+Sea)\b",
     "name": "United Nations Convention on the Law of the Sea", "abbrev": "UNCLOS", "year": 1982},
    {"pattern": r"\b(?:CISG|Convention\s+on\s+(?:Contracts\s+for\s+(?:the\s+)?)?International\s+Sale\s+of\s+Goods)\b",
     "name": "Convention on Contracts for the International Sale of Goods", "abbrev": "CISG", "year": 1980},
    {"pattern": r"\b(?:New\s+York\s+Convention|NYC)\b",
     "name": "Convention on the Recognition and Enforcement of Foreign Arbitral Awards",
     "abbrev": "NYC", "year": 1958},
    {"pattern": r"\b(?:ICCPR|International\s+Covenant\s+on\s+Civil\s+and\s+Political\s+Rights)\b",
     "name": "International Covenant on Civil and Political Rights", "abbrev": "ICCPR", "year": 1966},
    {"pattern": r"\b(?:ICESCR|International\s+Covenant\s+on\s+Economic[,\s]+Social\s+and\s+Cultural\s+Rights)\b",
     "name": "International Covenant on Economic, Social and Cultural Rights", "abbrev": "ICESCR", "year": 1966},
    {"pattern": r"\b(?:ECHR|European\s+Convention\s+on\s+Human\s+Rights)\b",
     "name": "European Convention on Human Rights", "abbrev": "ECHR", "year": 1950},
    {"pattern": r"\b(?:Rome\s+Statute)\b",
     "name": "Rome Statute of the International Criminal Court", "abbrev": "Rome Statute", "year": 1998},
    {"pattern": r"\b(?:Geneva\s+Convention(?:s)?)\b",
     "name": "Geneva Conventions", "abbrev": "GC", "year": 1949},
    {"pattern": r"\b(?:Additional\s+Protocol\s+I)\b",
     "name": "Protocol Additional to the Geneva Conventions (Protocol I)", "abbrev": "AP I", "year": 1977},
    {"pattern": r"\b(?:Additional\s+Protocol\s+II)\b",
     "name": "Protocol Additional to the Geneva Conventions (Protocol II)", "abbrev": "AP II", "year": 1977},
    {"pattern": r"\b(?:GATT(?:\s+1994)?)\b",
     "name": "General Agreement on Tariffs and Trade 1994", "abbrev": "GATT", "year": 1994},
    {"pattern": r"\b(?:TRIPS\s+Agreement|TRIPS)\b",
     "name": "Agreement on Trade-Related Aspects of Intellectual Property Rights",
     "abbrev": "TRIPS", "year": 1994},
    {"pattern": r"\b(?:DSU|Dispute\s+Settlement\s+Understanding)\b",
     "name": "Understanding on Rules and Procedures Governing the Settlement of Disputes",
     "abbrev": "DSU", "year": 1994},
    {"pattern": r"\b(?:SCM\s+Agreement)\b",
     "name": "Agreement on Subsidies and Countervailing Measures", "abbrev": "SCM", "year": 1994},
    {"pattern": r"\b(?:ICSID\s+Convention)\b",
     "name": "Convention on the Settlement of Investment Disputes between States and Nationals of Other States",
     "abbrev": "ICSID Convention", "year": 1965},
    {"pattern": r"\b(?:Paris\s+Agreement)\b",
     "name": "Paris Agreement", "abbrev": "Paris Agreement", "year": 2015},
    {"pattern": r"\b(?:Genocide\s+Convention)\b",
     "name": "Convention on the Prevention and Punishment of the Crime of Genocide",
     "abbrev": "Genocide Convention", "year": 1948},
    {"pattern": r"\b(?:Hague\s+Service\s+Convention)\b",
     "name": "Hague Convention on the Service Abroad of Judicial and Extrajudicial Documents",
     "abbrev": "Hague Service Convention", "year": 1965},
    {"pattern": r"\b(?:Hague\s+Evidence\s+Convention)\b",
     "name": "Hague Convention on the Taking of Evidence Abroad",
     "abbrev": "Hague Evidence Convention", "year": 1970},
    {"pattern": r"\b(?:Montreal\s+Protocol)\b",
     "name": "Montreal Protocol on Substances that Deplete the Ozone Layer",
     "abbrev": "Montreal Protocol", "year": 1987},
    {"pattern": r"\bUK\s+Bribery\s+Act\b",
     "name": "UK Bribery Act 2010", "abbrev": "UK Bribery Act", "year": 2010},
]

ARTICLE_PATTERN = re.compile(
    r"\b(?:Art(?:icle)?\.?\s*)(\d+(?:\(\d+\))?(?:\([a-z]\))?(?:bis)?)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Sanctions programs data for screening
# ---------------------------------------------------------------------------

SANCTIONS_PROGRAMS: Dict[str, Dict[str, Any]] = {
    "iran": {
        "type": "comprehensive",
        "cfr": "31 CFR Part 560",
        "authority": "IEEPA, ISA, CISADA, IFCA, JCPOA",
        "restrictions": ["trade embargo", "financial transactions", "oil imports",
                         "shipping", "insurance", "metals", "automotive"],
        "risk_level": "CRITICAL",
    },
    "cuba": {
        "type": "comprehensive",
        "cfr": "31 CFR Part 515",
        "authority": "TWEA, CDA, Libertad Act",
        "restrictions": ["trade embargo", "financial transactions", "travel",
                         "investment", "tourism-related"],
        "risk_level": "CRITICAL",
    },
    "north_korea": {
        "type": "comprehensive",
        "cfr": "31 CFR Part 510",
        "authority": "IEEPA, NKSPEA, UNSCRs",
        "restrictions": ["trade embargo", "financial transactions", "luxury goods",
                         "coal", "textiles", "seafood", "weapons"],
        "risk_level": "CRITICAL",
    },
    "syria": {
        "type": "comprehensive",
        "cfr": "31 CFR Part 542",
        "authority": "IEEPA, Syria Accountability Act",
        "restrictions": ["trade embargo", "petroleum", "financial transactions",
                         "investment"],
        "risk_level": "CRITICAL",
    },
    "russia": {
        "type": "sectoral",
        "cfr": "31 CFR Part 589",
        "authority": "IEEPA, CAATSA, EO 14024",
        "restrictions": ["financial sector", "energy sector", "technology",
                         "defense", "mining", "quantum computing", "semiconductors"],
        "risk_level": "HIGH",
    },
    "belarus": {
        "type": "targeted",
        "cfr": "31 CFR Part 548",
        "authority": "IEEPA, Belarus Democracy Act",
        "restrictions": ["potash", "petroleum", "financial institutions",
                         "government officials"],
        "risk_level": "HIGH",
    },
    "venezuela": {
        "type": "targeted",
        "cfr": "31 CFR Part 591",
        "authority": "IEEPA, EO 13692, EO 13884",
        "restrictions": ["government of venezuela", "pdvsa", "gold sector",
                         "financial sector"],
        "risk_level": "HIGH",
    },
    "myanmar": {
        "type": "targeted",
        "cfr": "31 CFR Part 525",
        "authority": "IEEPA, JADE Act, EO 14014",
        "restrictions": ["military entities", "gems", "timber",
                         "state-owned enterprises"],
        "risk_level": "HIGH",
    },
    "china_military": {
        "type": "targeted",
        "cfr": "31 CFR Part 586",
        "authority": "EO 13959, EO 14032",
        "restrictions": ["chinese military-industrial complex companies",
                         "surveillance technology", "securities investment"],
        "risk_level": "MEDIUM",
    },
}

SANCTIONS_LISTS: Dict[str, str] = {
    "sdn_list": "Specially Designated Nationals and Blocked Persons List (OFAC)",
    "entity_list": "Entity List (BIS)",
    "military_end_user_list": "Military End-User List (BIS)",
    "unverified_list": "Unverified List (BIS)",
    "denied_persons_list": "Denied Persons List (BIS)",
    "debarred_list": "ITAR Debarred List (DDTC)",
    "non_sdn_cmic": "Non-SDN Chinese Military-Industrial Complex Companies List",
    "sectoral_sanctions": "Sectoral Sanctions Identifications List (OFAC)",
    "foreign_sanctions_evaders": "Foreign Sanctions Evaders List (OFAC)",
    "capta_list": "List of Foreign Financial Institutions Subject to CAPTA",
}


# ---------------------------------------------------------------------------
# Conflict of Laws connecting factors
# ---------------------------------------------------------------------------

CONNECTING_FACTORS: Dict[str, List[str]] = {
    "contract": [
        "lex loci contractus (law of place of contracting)",
        "lex loci solutionis (law of place of performance)",
        "proper law of the contract (closest connection)",
        "party autonomy (chosen law)",
        "characteristic performance (Rome I Art. 4)",
    ],
    "tort": [
        "lex loci delicti (law of place of wrong)",
        "lex loci damni (law of place of damage)",
        "law of common habitual residence",
        "most significant relationship (Restatement 2d)",
        "Rome II Art. 4 general rule",
    ],
    "property_immovable": [
        "lex situs (lex rei sitae) (law of location of property)",
    ],
    "property_movable": [
        "lex situs at time of relevant event",
        "law of domicile/habitual residence of owner",
    ],
    "succession": [
        "lex domicilii (law of domicile at death)",
        "lex patriae (law of nationality)",
        "lex situs for immovable property",
        "EU Succession Regulation Art. 21 (habitual residence)",
    ],
    "marriage": [
        "lex loci celebrationis (law of place of celebration)",
        "lex domicilii (dual domicile test)",
        "intended matrimonial home",
    ],
    "capacity": [
        "lex domicilii (common law tradition)",
        "lex patriae (civil law tradition)",
    ],
    "corporation": [
        "law of place of incorporation",
        "law of real seat (siege reel)",
        "law of central administration",
    ],
}


# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------

def normalize_query(query: str) -> NormalizedQuery:
    """
    Normalize an international law query by expanding abbreviations,
    detecting categories, and extracting entities.
    """
    original = query.strip()
    normalized = original.lower()

    expanded_terms: List[str] = []
    for abbrev, expansion in SYNONYM_MAP.items():
        pattern = re.compile(r"\b" + re.escape(abbrev) + r"\b", re.IGNORECASE)
        if pattern.search(normalized):
            expanded_terms.append(f"{abbrev} -> {expansion}")
            normalized = pattern.sub(expansion, normalized)

    detected_categories: List[str] = []
    for cat, keywords in CATEGORY_MAP.items():
        score = 0
        for kw in keywords:
            if kw.lower() in normalized:
                score += 1
        if score > 0:
            detected_categories.append(cat)

    detected_categories.sort(
        key=lambda c: sum(1 for kw in CATEGORY_MAP[c] if kw.lower() in normalized),
        reverse=True,
    )

    entities = extract_treaty_entities(original)
    detected_entity_names = [e.abbreviation or e.name for e in entities]

    total_signals = len(expanded_terms) + len(detected_categories) + len(entities)
    confidence = min(1.0, total_signals * 0.15 + 0.2) if total_signals > 0 else 0.1

    hash_payload = f"{HASH_SALT}:{normalized}"
    hash_key = hashlib.sha256(hash_payload.encode()).hexdigest()[:16]

    result = NormalizedQuery(
        original=original,
        normalized=normalized,
        expanded_terms=expanded_terms,
        detected_categories=detected_categories[:5],
        detected_entities=detected_entity_names,
        confidence=round(confidence, 4),
        hash_key=hash_key,
    )
    logger.debug("Normalized query: '{}' -> categories={}", original, detected_categories[:3])
    return result


def extract_treaty_entities(text: str) -> List[TreatyEntity]:
    """Extract treaty and instrument references from text."""
    entities: List[TreatyEntity] = []
    seen: Set[str] = set()

    for tp in TREATY_PATTERNS:
        matches = re.finditer(tp["pattern"], text, re.IGNORECASE)
        for match in matches:
            key = tp["abbrev"]
            if key in seen:
                continue
            seen.add(key)

            article_match = ARTICLE_PATTERN.search(text[match.end():match.end() + 60])
            article_str: Optional[str] = None
            if article_match:
                article_str = article_match.group(1)

            entities.append(TreatyEntity(
                name=tp["name"],
                abbreviation=tp["abbrev"],
                year=tp.get("year"),
                article=article_str,
                entity_type="treaty",
            ))

    return entities


def classify_international_issue(query: str) -> IssueClassification:
    """
    Classify a query into international law categories and suggest
    relevant doctrine topics.
    """
    normalized = normalize_query(query)
    query_lower = normalized.normalized

    category_scores: Dict[str, float] = {}
    keywords_matched_all: Dict[str, List[str]] = {}

    for cat, keywords in CATEGORY_MAP.items():
        score = 0.0
        matched: List[str] = []
        for kw in keywords:
            if kw.lower() in query_lower:
                score += 1.0
                matched.append(kw)
                if len(kw.split()) > 1:
                    score += 0.5
        if score > 0:
            category_scores[cat] = score
            keywords_matched_all[cat] = matched

    if not category_scores:
        return IssueClassification(
            primary_category="unclassified",
            confidence=0.1,
            keywords_matched=[],
            suggested_doctrines=[],
        )

    sorted_cats = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_cats[0][0]
    secondary = [c for c, _ in sorted_cats[1:4]]
    matched_kws = keywords_matched_all.get(primary, [])

    doctrine_suggestions = _suggest_doctrines(primary, query_lower, matched_kws)

    max_possible = max(len(CATEGORY_MAP[primary]) * 1.5, 1)
    confidence = min(1.0, category_scores[primary] / max_possible + 0.2)

    return IssueClassification(
        primary_category=primary,
        secondary_categories=secondary,
        confidence=round(confidence, 4),
        keywords_matched=matched_kws,
        suggested_doctrines=doctrine_suggestions,
    )


def _suggest_doctrines(category: str, query_lower: str, keywords: List[str]) -> List[str]:
    """Map category and keywords to suggested doctrine topic keys."""
    mapping: Dict[str, List[str]] = {
        "public_international_law": [
            "un_charter_use_of_force", "un_charter_self_defense",
            "un_charter_chapter_vii", "state_responsibility_attribution",
            "customary_international_law", "vclt_jus_cogens",
        ],
        "treaty_law": [
            "vclt_treaty_interpretation", "vclt_reservations",
            "vclt_jus_cogens",
        ],
        "international_trade_law": [
            "wto_mfn_principle", "wto_national_treatment",
            "wto_dispute_settlement", "wto_subsidies_scm",
            "wto_antidumping", "gatt_general_exceptions",
            "trips_ip_protection",
        ],
        "international_arbitration": [
            "uncitral_model_law_arbitration", "icc_rules_arbitration",
            "icsid_investment_arbitration", "ny_convention_arbitral_awards",
        ],
        "international_investment_law": [
            "bilateral_investment_treaties", "icsid_investment_arbitration",
        ],
        "international_humanitarian_law": [
            "geneva_conventions_common_art3", "geneva_conventions_pow",
            "geneva_conventions_civilian_protection",
            "geneva_conventions_grave_breaches", "hague_laws_of_war",
        ],
        "international_human_rights": [
            "iccpr_civil_political_rights", "icescr_economic_social_rights",
            "echr_human_rights",
        ],
        "international_criminal_law": [
            "icc_rome_statute_overview", "icc_war_crimes",
            "icc_crimes_against_humanity", "genocide_convention",
        ],
        "law_of_the_sea": [
            "unclos_law_of_the_sea", "unclos_eez",
            "unclos_continental_shelf", "unclos_deep_seabed",
        ],
        "foreign_sovereign_immunity": [
            "fsia_sovereign_immunity", "fsia_commercial_activity",
            "fsia_terrorism_exception",
        ],
        "sanctions_export_controls": [
            "ofac_sanctions_overview", "ear_export_controls",
            "itar_defense_articles",
        ],
        "anti_corruption": [
            "fcpa_anti_corruption", "uk_bribery_act",
        ],
        "international_commercial_law": [
            "cisg_formation_contracts", "cisg_remedies_breach",
        ],
        "international_environmental_law": [
            "paris_agreement_climate",
        ],
        "private_international_law": [
            "conflict_of_laws_characterization", "hague_service_evidence",
            "ny_convention_arbitral_awards",
        ],
        "diplomatic_consular_law": [
            "diplomatic_consular_immunity",
            "international_organizations_immunity",
        ],
    }
    return mapping.get(category, [])


def compute_semantic_similarity(query_a: str, query_b: str) -> SemanticSimilarityResult:
    """
    Compute semantic similarity between two international law queries using
    term overlap, synonym expansion, and category matching.
    """
    norm_a = normalize_query(query_a)
    norm_b = normalize_query(query_b)

    tokens_a = set(norm_a.normalized.split())
    tokens_b = set(norm_b.normalized.split())

    stopwords = {"the", "a", "an", "of", "on", "in", "to", "for", "and", "or",
                 "is", "are", "was", "were", "be", "been", "with", "by", "at",
                 "from", "that", "this", "it", "its", "not", "as", "but", "if",
                 "can", "may", "shall", "should", "would", "will", "do", "does",
                 "did", "has", "have", "had", "which", "what", "who", "whom",
                 "how", "when", "where", "why", "all", "each", "every", "any",
                 "no", "other", "such", "than", "so", "only", "also", "more",
                 "most", "very", "under", "between", "against", "into", "over"}
    tokens_a -= stopwords
    tokens_b -= stopwords

    if not tokens_a or not tokens_b:
        return SemanticSimilarityResult(
            query_a=query_a, query_b=query_b,
            similarity_score=0.0, shared_terms=[], shared_categories=[],
        )

    shared = tokens_a & tokens_b
    jaccard = len(shared) / len(tokens_a | tokens_b) if (tokens_a | tokens_b) else 0.0

    cats_a = set(norm_a.detected_categories)
    cats_b = set(norm_b.detected_categories)
    shared_cats = sorted(cats_a & cats_b)
    cat_bonus = len(shared_cats) * 0.1

    entity_a = set(norm_a.detected_entities)
    entity_b = set(norm_b.detected_entities)
    entity_bonus = len(entity_a & entity_b) * 0.08

    similarity = min(1.0, jaccard + cat_bonus + entity_bonus)

    return SemanticSimilarityResult(
        query_a=query_a,
        query_b=query_b,
        similarity_score=round(similarity, 4),
        shared_terms=sorted(shared),
        shared_categories=shared_cats,
    )


# ---------------------------------------------------------------------------
# TreatyInterpreter Class
# ---------------------------------------------------------------------------

class TreatyInterpreter:
    """
    Applies Vienna Convention on the Law of Treaties Articles 31-32
    interpretation methodology to treaty provisions.
    """

    VCLT_ART31_STEPS = [
        "ordinary_meaning",
        "context",
        "object_and_purpose",
        "subsequent_agreement",
        "subsequent_practice",
        "relevant_rules_of_international_law",
    ]

    VCLT_ART32_TRIGGERS = [
        "ambiguity_after_art31",
        "manifestly_absurd_result",
        "manifestly_unreasonable_result",
    ]

    def __init__(self) -> None:
        self._interpretation_log: List[Dict[str, Any]] = []

    def interpret(
        self,
        treaty: str,
        provision: str,
        text_of_provision: str,
        preamble_excerpt: str = "",
        subsequent_practice_notes: str = "",
        travaux_notes: str = "",
    ) -> TreatyInterpretationResult:
        """
        Perform a structured Vienna Convention Arts. 31-32 interpretation.
        """
        logger.info("Interpreting {} provision {}", treaty, provision)

        ordinary = self._analyze_ordinary_meaning(text_of_provision)
        context = self._analyze_context(text_of_provision, preamble_excerpt)
        obj_purpose = self._analyze_object_and_purpose(preamble_excerpt, treaty)
        subseq = self._analyze_subsequent_practice(subsequent_practice_notes)
        supplementary = self._analyze_supplementary_means(
            travaux_notes, ordinary, context
        )

        conclusion = self._synthesize(
            treaty, provision, ordinary, context, obj_purpose, subseq, supplementary
        )

        confidence = self._compute_confidence(
            ordinary, context, obj_purpose, subseq, supplementary
        )

        result = TreatyInterpretationResult(
            treaty=treaty,
            provision=provision,
            ordinary_meaning=ordinary,
            context_analysis=context,
            object_and_purpose=obj_purpose,
            subsequent_practice=subseq,
            supplementary_means=supplementary,
            interpretation_conclusion=conclusion,
            confidence=confidence,
        )

        self._interpretation_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "treaty": treaty,
            "provision": provision,
            "confidence": confidence,
        })

        return result

    def _analyze_ordinary_meaning(self, text: str) -> str:
        if not text.strip():
            return "No provision text provided for ordinary meaning analysis."
        words = text.split()
        key_legal_terms = []
        legal_indicators = {
            "shall", "must", "may", "should", "obligation", "right", "duty",
            "prohibit", "require", "permit", "exempt", "notwithstanding",
            "derogate", "comply", "enforce", "sovereign", "jurisdiction",
        }
        for w in words:
            if w.lower().strip(".,;:()") in legal_indicators:
                key_legal_terms.append(w.strip(".,;:()"))

        mandatory = any(t.lower() in ("shall", "must") for t in key_legal_terms)
        permissive = any(t.lower() in ("may",) for t in key_legal_terms)
        prohibitive = any(t.lower() in ("prohibit", "shall not") for t in key_legal_terms)

        tone = "mandatory" if mandatory else ("permissive" if permissive else (
            "prohibitive" if prohibitive else "declaratory"
        ))

        return (
            f"The ordinary meaning of the provision text suggests a {tone} character. "
            f"Key legal terms identified: {', '.join(key_legal_terms) if key_legal_terms else 'none identified'}. "
            f"Under VCLT Art. 31(1), terms are given their ordinary meaning in the context "
            f"of the treaty and in light of its object and purpose. The text contains "
            f"{len(words)} words requiring contextual interpretation."
        )

    def _analyze_context(self, text: str, preamble: str) -> str:
        context_elements = []
        if preamble.strip():
            context_elements.append(
                f"The preamble provides interpretive context: '{preamble[:200]}...'" if len(preamble) > 200
                else f"The preamble provides interpretive context: '{preamble}'"
            )
        else:
            context_elements.append(
                "No preamble excerpt was provided. Under Art. 31(2), context includes "
                "the preamble and annexes, as well as agreements and instruments made in "
                "connection with the conclusion of the treaty."
            )

        if "article" in text.lower() or "art." in text.lower():
            context_elements.append(
                "Cross-references to other provisions are present, indicating the "
                "provision must be read in conjunction with the broader treaty framework."
            )

        return " ".join(context_elements)

    def _analyze_object_and_purpose(self, preamble: str, treaty: str) -> str:
        known_purposes: Dict[str, str] = {
            "un charter": (
                "The UN Charter's primary objects and purposes include maintaining "
                "international peace and security, developing friendly relations among "
                "nations, achieving international cooperation, and serving as a center "
                "for harmonizing state actions (Art. 1)."
            ),
            "vclt": (
                "The VCLT aims to codify the law of treaties, ensure treaty stability "
                "through pacta sunt servanda, and promote the progressive development "
                "of international law."
            ),
            "cisg": (
                "The CISG's object and purpose is to promote uniformity in "
                "international sales law, reduce legal barriers to cross-border trade, "
                "and provide fair and balanced rules for both buyers and sellers."
            ),
            "gatt": (
                "The GATT/WTO system's object and purpose is to promote trade "
                "liberalization, reduce tariff and non-tariff barriers, eliminate "
                "discriminatory treatment, and provide a framework for negotiation."
            ),
        }

        treaty_lower = treaty.lower()
        for key, purpose in known_purposes.items():
            if key in treaty_lower:
                return purpose

        if preamble.strip():
            return (
                f"Based on the preamble, the treaty's object and purpose informs "
                f"interpretation. Recitals state: '{preamble[:300]}'. Under Art. 31(1), "
                f"terms must be interpreted in light of these stated objectives."
            )

        return (
            f"The object and purpose of '{treaty}' must be determined from its "
            f"preamble, structure, and the circumstances of its conclusion. This "
            f"teleological element is integral to Art. 31(1) interpretation."
        )

    def _analyze_subsequent_practice(self, notes: str) -> str:
        if not notes.strip():
            return (
                "No subsequent practice evidence was provided. Under Art. 31(3)(b), "
                "subsequent practice in the application of the treaty which establishes "
                "the agreement of the parties regarding its interpretation shall be "
                "taken into account. This includes consistent state practice, decisions "
                "of treaty bodies, and resolutions of conferences of parties."
            )
        return (
            f"Subsequent practice evidence: {notes}. Under Art. 31(3)(b), this "
            f"practice, if establishing party agreement on interpretation, is an "
            f"authoritative interpretive guide with the potential to modify or confirm "
            f"the ordinary meaning."
        )

    def _analyze_supplementary_means(
        self, travaux: str, ordinary: str, context: str
    ) -> str:
        if not travaux.strip():
            return (
                "No travaux preparatoires were provided. Under Art. 32, supplementary "
                "means of interpretation, including the preparatory work of the treaty "
                "and the circumstances of its conclusion, may be resorted to when "
                "Art. 31 interpretation leaves the meaning ambiguous or obscure, or "
                "leads to a manifestly absurd or unreasonable result."
            )
        return (
            f"Supplementary means of interpretation (Art. 32): The travaux "
            f"preparatoires indicate: {travaux}. This supplementary material "
            f"{'confirms' if 'ambig' not in ordinary.lower() else 'may resolve ambiguity in'} "
            f"the interpretation derived from Art. 31."
        )

    def _synthesize(
        self, treaty: str, provision: str,
        ordinary: str, context: str, obj_purpose: str,
        subseq: str, supplementary: str,
    ) -> str:
        return (
            f"Interpretation of {treaty} {provision}: Applying the VCLT Art. 31 "
            f"general rule holistically - the ordinary meaning of the terms, read in "
            f"context and in light of the treaty's object and purpose, with reference "
            f"to subsequent practice where available, yields the following conclusion. "
            f"The provision establishes binding obligations on the parties consistent "
            f"with the treaty's overall objectives. Where Art. 32 supplementary means "
            f"were consulted, they confirm rather than contradict the Art. 31 "
            f"interpretation. This analysis follows the methodology endorsed by the "
            f"ICJ in Territorial Dispute (Libya/Chad) and the WTO Appellate Body in "
            f"US - Gasoline."
        )

    def _compute_confidence(
        self, ordinary: str, context: str, obj_purpose: str,
        subseq: str, supplementary: str,
    ) -> float:
        score = 0.3
        if "key legal terms identified:" in ordinary and "none" not in ordinary:
            score += 0.15
        if "preamble provides" in context:
            score += 0.15
        if "party agreement" in subseq or "consistent state practice" in subseq:
            score += 0.1
        if "travaux" in supplementary.lower() and "no travaux" not in supplementary.lower():
            score += 0.1
        if "object and purpose" in obj_purpose:
            score += 0.1
        return round(min(1.0, score), 4)

    def get_interpretation_log(self) -> List[Dict[str, Any]]:
        """Return the log of all interpretations performed."""
        return list(self._interpretation_log)


# ---------------------------------------------------------------------------
# SanctionsAnalyzer Class
# ---------------------------------------------------------------------------

class SanctionsAnalyzer:
    """
    Performs OFAC-style sanctions screening and risk assessment.
    """

    def __init__(self) -> None:
        self._screening_log: List[Dict[str, Any]] = []

    def screen_entity(
        self,
        entity_name: str,
        country: str = "",
        industry: str = "",
        transaction_type: str = "",
    ) -> SanctionsScreenResult:
        """
        Screen an entity against sanctions programs and restricted party lists.
        """
        logger.info("Screening entity: {} (country={}, industry={})",
                     entity_name, country, industry)

        entity_lower = entity_name.lower()
        country_lower = country.lower()
        industry_lower = industry.lower()

        matched_programs: List[str] = []
        matched_lists: List[str] = []
        flags: List[str] = []

        for prog_name, prog_data in SANCTIONS_PROGRAMS.items():
            prog_name_clean = prog_name.replace("_", " ")
            if prog_name_clean in country_lower or prog_name_clean in entity_lower:
                matched_programs.append(prog_name)
                flags.append(f"Entity or country matches {prog_data['type']} "
                             f"sanctions program: {prog_name}")

        comprehensive_countries = {"iran", "cuba", "north korea", "dprk", "syria",
                                   "crimea", "donetsk", "luhansk"}
        for cc in comprehensive_countries:
            if cc in country_lower or cc in entity_lower:
                flags.append(f"CRITICAL: Comprehensive sanctions jurisdiction detected ({cc})")
                if cc not in [p.replace("_", " ") for p in matched_programs]:
                    for prog_name, prog_data in SANCTIONS_PROGRAMS.items():
                        if cc.replace(" ", "_") == prog_name or cc in prog_name:
                            matched_programs.append(prog_name)

        high_risk_industries = {
            "oil": "energy sector",
            "gas": "energy sector",
            "petroleum": "energy sector",
            "defense": "defense sector",
            "military": "defense sector",
            "weapons": "defense sector",
            "arms": "defense sector",
            "banking": "financial sector",
            "finance": "financial sector",
            "cryptocurrency": "financial sector (virtual currency)",
            "mining": "extractive sector",
            "semiconductor": "technology sector",
            "telecom": "telecommunications sector",
        }
        for ind_key, ind_label in high_risk_industries.items():
            if ind_key in industry_lower:
                flags.append(f"High-risk industry detected: {ind_label}")

        restricted_keywords = {
            "government", "ministry", "military", "armed forces",
            "central bank", "state-owned", "sovereign wealth",
        }
        for rk in restricted_keywords:
            if rk in entity_lower:
                flags.append(f"Restricted entity keyword: '{rk}'")
                matched_lists.append("sdn_list")

        if transaction_type:
            tx_lower = transaction_type.lower()
            high_risk_tx = ["arms sale", "technology transfer", "financial",
                            "investment", "joint venture", "merger"]
            for hrx in high_risk_tx:
                if hrx in tx_lower:
                    flags.append(f"High-risk transaction type: {hrx}")

        if matched_programs:
            for prog in matched_programs:
                prog_data = SANCTIONS_PROGRAMS.get(prog, {})
                if prog_data.get("type") == "comprehensive":
                    risk_level = "CRITICAL"
                    break
            else:
                risk_level = "HIGH"
        elif flags:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        recommendation = self._generate_recommendation(
            risk_level, matched_programs, matched_lists, flags
        )

        confidence = min(1.0, 0.3 + len(flags) * 0.1 + len(matched_programs) * 0.15)

        result = SanctionsScreenResult(
            query_entity=entity_name,
            risk_level=risk_level,
            matched_programs=matched_programs,
            matched_lists=list(set(matched_lists)),
            flags=flags,
            recommendation=recommendation,
            confidence=round(confidence, 4),
        )

        self._screening_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "entity": entity_name,
            "risk_level": risk_level,
            "programs": matched_programs,
        })

        return result

    def _generate_recommendation(
        self,
        risk_level: str,
        programs: List[str],
        lists: List[str],
        flags: List[str],
    ) -> str:
        if risk_level == "CRITICAL":
            return (
                "BLOCK TRANSACTION. Entity or jurisdiction falls under comprehensive "
                "sanctions program. All transactions are presumptively prohibited unless "
                "authorized by a specific or general license from OFAC. Consult legal "
                "counsel before any engagement. File a voluntary self-disclosure if any "
                "prior transactions may have occurred."
            )
        if risk_level == "HIGH":
            return (
                "ESCALATE FOR REVIEW. Entity triggers significant sanctions risk factors. "
                "Conduct enhanced due diligence including beneficial ownership analysis, "
                "SDN 50% ownership rule screening, and verification against all restricted "
                "party lists. Obtain legal opinion before proceeding with any transaction."
            )
        if risk_level == "MEDIUM":
            return (
                "PROCEED WITH CAUTION. Risk indicators are present but no definitive "
                "sanctions match identified. Conduct standard due diligence, screen "
                "against all applicable lists, verify end-use and end-user, and document "
                "compliance procedures. Monitor for changes in sanctions designations."
            )
        return (
            "LOW RISK. No significant sanctions indicators identified based on available "
            "information. Standard compliance procedures apply. Maintain records and "
            "re-screen periodically as sanctions lists are updated frequently."
        )

    def check_50_percent_rule(
        self, entity_name: str, owners: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Apply OFAC's 50 Percent Rule: entities owned 50% or more by one or
        more blocked persons are themselves blocked.
        """
        blocked_ownership = 0.0
        blocked_owners: List[str] = []

        for owner in owners:
            name = owner.get("name", "")
            pct = owner.get("ownership_pct", 0.0)
            is_sdn = owner.get("is_sdn", False)
            if is_sdn:
                blocked_ownership += pct
                blocked_owners.append(name)

        is_blocked = blocked_ownership >= 50.0

        return {
            "entity": entity_name,
            "blocked_ownership_pct": round(blocked_ownership, 2),
            "blocked_owners": blocked_owners,
            "is_blocked_by_50pct_rule": is_blocked,
            "recommendation": (
                "Entity is deemed blocked under OFAC's 50 Percent Rule. "
                "All property and interests in property are blocked. "
                "US persons are prohibited from dealing with this entity."
                if is_blocked else
                "Entity does not meet the 50 Percent Rule threshold. "
                "However, aggregate blocked ownership of "
                f"{blocked_ownership:.1f}% warrants enhanced monitoring."
                if blocked_ownership > 25.0 else
                "Entity does not trigger the 50 Percent Rule. "
                "Standard compliance procedures apply."
            ),
        }

    def get_screening_log(self) -> List[Dict[str, Any]]:
        """Return the log of all screening operations performed."""
        return list(self._screening_log)


# ---------------------------------------------------------------------------
# ConflictOfLawsResolver Class
# ---------------------------------------------------------------------------

class ConflictOfLawsResolver:
    """
    Analyzes conflict of laws issues including characterization,
    connecting factors, and applicable law determination.
    """

    ISSUE_TYPES = [
        "contract", "tort", "property_immovable", "property_movable",
        "succession", "marriage", "capacity", "corporation",
    ]

    APPLICABLE_CONVENTIONS: Dict[str, List[str]] = {
        "contract": [
            "Rome I Regulation (EC) No 593/2008 (EU)",
            "Hague Principles on Choice of Law in International Commercial Contracts (2015)",
            "Inter-American Convention on the Law Applicable to International Contracts (1994)",
            "Restatement (Second) of Conflict of Laws ss 187-188 (US)",
        ],
        "tort": [
            "Rome II Regulation (EC) No 864/2007 (EU)",
            "Hague Convention on the Law Applicable to Traffic Accidents (1971)",
            "Hague Convention on the Law Applicable to Products Liability (1973)",
            "Restatement (Second) of Conflict of Laws ss 145-146 (US)",
        ],
        "property_immovable": [
            "Lex situs rule (universal application)",
        ],
        "property_movable": [
            "Hague Convention on the Law Applicable to Trusts (1985)",
            "UNIDROIT Convention on Stolen or Illegally Exported Cultural Objects (1995)",
        ],
        "succession": [
            "EU Succession Regulation No 650/2012",
            "Hague Convention on the Conflicts of Laws Relating to the Form of Testamentary Dispositions (1961)",
        ],
        "marriage": [
            "Hague Convention on Celebration and Recognition of Validity of Marriages (1978)",
        ],
        "capacity": [
            "Generally determined by lex domicilii (common law) or lex patriae (civil law)",
        ],
        "corporation": [
            "EU Company Law Directives",
            "Hague Convention on the Law Applicable to Agency (1978)",
        ],
    }

    def __init__(self) -> None:
        self._resolution_log: List[Dict[str, Any]] = []

    def analyze(
        self,
        issue_description: str,
        forum_country: str = "",
        party_a_country: str = "",
        party_b_country: str = "",
        subject_matter: str = "",
        chosen_law: str = "",
    ) -> ConflictOfLawsResult:
        """
        Perform conflict of laws analysis: characterization, connecting
        factors, and applicable law determination.
        """
        logger.info("Conflict of laws analysis: {}", issue_description[:80])

        characterization = self._characterize(issue_description, subject_matter)
        connecting = self._identify_connecting_factors(characterization)
        candidates = self._determine_candidate_laws(
            characterization, forum_country, party_a_country,
            party_b_country, chosen_law,
        )
        renvoi_risk = self._assess_renvoi_risk(
            characterization, forum_country, candidates
        )
        public_policy = self._assess_public_policy(
            issue_description, forum_country
        )
        conventions = self.APPLICABLE_CONVENTIONS.get(characterization, [])
        approach = self._recommend_approach(
            characterization, candidates, chosen_law, renvoi_risk, public_policy
        )

        result = ConflictOfLawsResult(
            issue_characterization=characterization,
            connecting_factors=connecting,
            candidate_laws=candidates,
            recommended_approach=approach,
            renvoi_risk=renvoi_risk,
            public_policy_concern=public_policy,
            applicable_conventions=conventions,
        )

        self._resolution_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "characterization": characterization,
            "forum": forum_country,
            "candidate_laws_count": len(candidates),
        })

        return result

    def _characterize(self, description: str, subject: str) -> str:
        """Classify the legal issue into a conflict of laws category."""
        combined = f"{description} {subject}".lower()

        contract_signals = [
            "contract", "agreement", "breach", "performance", "obligation",
            "sale", "delivery", "payment", "warranty", "license",
        ]
        tort_signals = [
            "tort", "negligence", "injury", "damage", "liability",
            "defamation", "product liability", "personal injury",
            "wrongful", "accident",
        ]
        property_immovable_signals = [
            "real property", "land", "immovable", "real estate",
            "building", "house", "apartment",
        ]
        property_movable_signals = [
            "movable property", "chattel", "goods", "personal property",
            "artwork", "ship", "aircraft",
        ]
        succession_signals = [
            "succession", "inheritance", "estate", "will", "testament",
            "probate", "heir", "beneficiary", "decedent",
        ]
        marriage_signals = [
            "marriage", "divorce", "matrimonial", "marital", "spouse",
            "custody", "prenuptial",
        ]
        capacity_signals = [
            "capacity", "minor", "legal age", "competence",
            "power of attorney",
        ]
        corporation_signals = [
            "corporation", "company", "incorporation", "registered office",
            "shareholder", "director", "corporate governance",
        ]

        scores: Dict[str, int] = {}
        for issue_type, signals in [
            ("contract", contract_signals),
            ("tort", tort_signals),
            ("property_immovable", property_immovable_signals),
            ("property_movable", property_movable_signals),
            ("succession", succession_signals),
            ("marriage", marriage_signals),
            ("capacity", capacity_signals),
            ("corporation", corporation_signals),
        ]:
            score = sum(1 for s in signals if s in combined)
            if score > 0:
                scores[issue_type] = score

        if not scores:
            return "contract"

        return max(scores, key=scores.get)  # type: ignore[arg-type]

    def _identify_connecting_factors(self, characterization: str) -> List[str]:
        """Return the connecting factors relevant to the characterized issue."""
        return CONNECTING_FACTORS.get(characterization, CONNECTING_FACTORS["contract"])

    def _determine_candidate_laws(
        self,
        characterization: str,
        forum: str,
        party_a: str,
        party_b: str,
        chosen_law: str,
    ) -> List[str]:
        """Determine candidate applicable laws based on connecting factors."""
        candidates: List[str] = []

        if chosen_law.strip():
            candidates.append(
                f"Chosen law: {chosen_law} (party autonomy — strongest connecting factor "
                f"for {characterization} under most modern regimes)"
            )

        if forum.strip():
            candidates.append(f"Lex fori: {forum} (law of the forum)")

        if party_a.strip():
            if characterization == "contract":
                candidates.append(
                    f"Law of Party A's country: {party_a} "
                    f"(potentially characteristic performance)"
                )
            elif characterization == "tort":
                candidates.append(
                    f"Law of Party A's country: {party_a} "
                    f"(potentially lex loci delicti)"
                )
            else:
                candidates.append(f"Law of Party A's country: {party_a}")

        if party_b.strip():
            candidates.append(f"Law of Party B's country: {party_b}")

        if party_a.strip() and party_b.strip() and party_a.lower() == party_b.lower():
            candidates.append(
                f"Common habitual residence: {party_a} "
                f"(overrides general rule under Rome I Art. 4(3) / Rome II Art. 4(2))"
            )

        if not candidates:
            candidates.append(
                "Insufficient information to determine candidate laws. "
                "Forum country, party nationalities/domiciles, and place of "
                "performance or harm are needed."
            )

        return candidates

    def _assess_renvoi_risk(
        self, characterization: str, forum: str, candidates: List[str]
    ) -> bool:
        """Assess whether renvoi is a risk for this issue type."""
        no_renvoi_types = {"contract", "tort"}
        if characterization in no_renvoi_types:
            return False

        if len(candidates) > 2:
            return True

        return characterization in {"succession", "property_immovable",
                                    "capacity", "marriage"}

    def _assess_public_policy(self, description: str, forum: str) -> bool:
        """Assess whether public policy exception might apply."""
        desc_lower = description.lower()
        policy_triggers = [
            "punitive damages", "gambling", "usury", "polygamy",
            "child marriage", "forced marriage", "slavery",
            "discrimination", "confiscation", "expropriation without compensation",
            "death penalty", "torture", "terrorism",
        ]
        return any(trigger in desc_lower for trigger in policy_triggers)

    def _recommend_approach(
        self,
        characterization: str,
        candidates: List[str],
        chosen_law: str,
        renvoi_risk: bool,
        public_policy: bool,
    ) -> str:
        """Generate a recommended approach for resolving the conflict."""
        parts: List[str] = []

        if chosen_law.strip():
            parts.append(
                f"Party autonomy: The parties' choice of {chosen_law} should be "
                f"given effect, subject to mandatory rules of the forum and any "
                f"overriding mandatory provisions of a closely connected jurisdiction. "
                f"Under Rome I Art. 3 and the Hague Principles Art. 2, party autonomy "
                f"is the primary connecting factor for contractual obligations."
            )
        else:
            parts.append(
                f"In the absence of a choice of law, the applicable law is determined "
                f"by the objective connecting factors for a {characterization} issue."
            )

        if renvoi_risk:
            parts.append(
                "RENVOI ALERT: The characterization of this issue as "
                f"'{characterization}' may expose the analysis to renvoi. Modern "
                "instruments (Rome I, Rome II) exclude renvoi, but common law "
                "jurisdictions may apply it for status and property matters. "
                "Verify the forum's position on renvoi."
            )

        if public_policy:
            parts.append(
                "PUBLIC POLICY CONCERN: Elements in the issue description may "
                "trigger the forum's public policy exception (ordre public). The "
                "applicable foreign law may be displaced in favor of forum law to "
                "the extent its application would be manifestly incompatible with "
                "fundamental values. This exception is construed narrowly."
            )

        return " ".join(parts)

    def get_resolution_log(self) -> List[Dict[str, Any]]:
        """Return the log of all conflict of laws analyses performed."""
        return list(self._resolution_log)


# ---------------------------------------------------------------------------
# Module init
# ---------------------------------------------------------------------------

logger.info(
    "LG15 semantic module loaded: {} synonyms, {} categories, "
    "{} treaty patterns, {} sanctions programs",
    len(SYNONYM_MAP), len(CATEGORY_MAP),
    len(TREATY_PATTERNS), len(SANCTIONS_PROGRAMS),
)
