"""
LG16 ADR Engine - Semantic Normalization
==========================================
ADR terminology normalization, entity extraction, dispute classification,
arbitration clause analysis, mediation process design, and dispute routing.

Engine: LG16 | Version: 2.0.0
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# SYNONYM MAP - 50+ ADR terminology normalizations
# ---------------------------------------------------------------------------

SYNONYM_MAP: dict[str, str] = {
    "adr": "alternative dispute resolution",
    "batna": "best alternative to negotiated agreement",
    "watna": "worst alternative to negotiated agreement",
    "zopa": "zone of possible agreement",
    "faa": "federal arbitration act",
    "ruaa": "revised uniform arbitration act",
    "uaa": "uniform arbitration act",
    "uma": "uniform mediation act",
    "aaa": "american arbitration association",
    "jams": "judicial arbitration and mediation services",
    "finra": "financial industry regulatory authority",
    "icsid": "international centre for settlement of investment disputes",
    "icc": "international chamber of commerce",
    "uncitral": "united nations commission on international trade law",
    "lcia": "london court of international arbitration",
    "siac": "singapore international arbitration centre",
    "hkiac": "hong kong international arbitration centre",
    "scc": "stockholm chamber of commerce arbitration institute",
    "pca": "permanent court of arbitration",
    "cietac": "china international economic and trade arbitration commission",
    "isds": "investor state dispute settlement",
    "bit": "bilateral investment treaty",
    "nyc": "new york convention",
    "ene": "early neutral evaluation",
    "drb": "dispute review board",
    "odr": "online dispute resolution",
    "udrp": "uniform domain name dispute resolution policy",
    "cprc": "texas civil practice and remedies code",
    "aapl": "american association of professional landmen",
    "joa": "joint operating agreement",
    "copas": "council of petroleum accountants societies",
    "nar": "national association of realtors",
    "tar": "texas association of realtors",
    "aia": "american institute of architects",
    "acr": "association for conflict resolution",
    "aba": "american bar association",
    "iba": "international bar association",
    "fet": "fair and equitable treatment",
    "mfn": "most favored nation treatment",
    "nma": "net mineral acres",
    "cba": "collective bargaining agreement",
    "nlra": "national labor relations act",
    "paga": "private attorneys general act",
    "efaa": "ending forced arbitration act",
    "crd": "central registration depository",
    "esi": "electronically stored information",
    "frcp": "federal rules of civil procedure",
    "cam": "common area maintenance",
    "hoa": "homeowner association",
    "ccr": "covenants conditions and restrictions",
    "sec": "securities and exchange commission",
    "med-arb": "mediation then arbitration hybrid",
    "arb-med": "arbitration then mediation hybrid",
}

# ---------------------------------------------------------------------------
# CATEGORY MAP - 15 ADR dispute categories
# ---------------------------------------------------------------------------

CATEGORY_MAP: dict[str, dict[str, Any]] = {
    "commercial": {
        "label": "Commercial Disputes",
        "description": "Business-to-business disputes including contract breach, partnership dissolution, supply chain, IP licensing",
        "default_forum": "AAA Commercial Rules or ICC Arbitration Rules",
        "typical_process": "arbitration",
        "keywords": [
            "contract", "breach", "partnership", "joint venture", "licensing",
            "franchise", "supply chain", "distribution", "warranty", "indemnity",
            "trade secret", "non-compete", "confidentiality", "purchase agreement",
        ],
    },
    "employment": {
        "label": "Employment Disputes",
        "description": "Employer-employee disputes including discrimination, wrongful termination, wage claims, non-compete enforcement",
        "default_forum": "AAA Employment Rules or JAMS Employment Rules",
        "typical_process": "arbitration",
        "keywords": [
            "discrimination", "harassment", "wrongful termination", "retaliation",
            "wage", "overtime", "flsa", "title vii", "ada", "adea", "fmla",
            "non-compete", "severance", "whistleblower", "class action waiver",
        ],
    },
    "consumer": {
        "label": "Consumer Disputes",
        "description": "Consumer-business disputes including product liability, service complaints, financial products",
        "default_forum": "AAA Consumer Arbitration Rules",
        "typical_process": "arbitration",
        "keywords": [
            "consumer", "product liability", "warranty", "defective", "credit card",
            "cell phone", "internet service", "subscription", "billing", "refund",
            "deceptive practices", "unfair trade", "lemon law",
        ],
    },
    "securities": {
        "label": "Securities Disputes",
        "description": "Investor-broker disputes, suitability claims, churning, unauthorized trading",
        "default_forum": "FINRA Dispute Resolution",
        "typical_process": "arbitration",
        "keywords": [
            "securities", "broker", "suitability", "churning", "unauthorized trading",
            "misrepresentation", "fiduciary", "investment", "portfolio", "finra",
            "rule 10b-5", "securities fraud", "margin", "options", "variable annuity",
        ],
    },
    "construction": {
        "label": "Construction Disputes",
        "description": "Construction project disputes including delay, defect, payment, and design issues",
        "default_forum": "AAA Construction Industry Arbitration Rules",
        "typical_process": "arbitration",
        "keywords": [
            "construction", "contractor", "subcontractor", "delay", "defect",
            "change order", "mechanic lien", "payment bond", "retainage", "aia",
            "differing site conditions", "acceleration", "disruption", "punch list",
        ],
    },
    "real_estate": {
        "label": "Real Estate Disputes",
        "description": "Property transaction disputes, lease disputes, HOA disputes, title issues",
        "default_forum": "AAA Real Estate Industry Rules or Court-Annexed Mediation",
        "typical_process": "mediation",
        "keywords": [
            "real estate", "property", "lease", "landlord", "tenant", "easement",
            "title", "deed", "closing", "escrow", "hoa", "zoning", "commission",
            "boundary", "encroachment", "specific performance",
        ],
    },
    "oil_gas": {
        "label": "Oil and Gas Disputes",
        "description": "Upstream oil and gas disputes including JOA, royalty, operating, and title disputes",
        "default_forum": "AAA Commercial Rules (with AAPL JOA clause)",
        "typical_process": "arbitration",
        "keywords": [
            "oil", "gas", "joa", "operating agreement", "royalty", "working interest",
            "overriding royalty", "mineral rights", "surface damage", "drilling",
            "afe", "copas", "pooling", "unitization", "farmout", "aapl",
        ],
    },
    "international_commercial": {
        "label": "International Commercial Disputes",
        "description": "Cross-border business disputes governed by international arbitration rules",
        "default_forum": "ICC Arbitration Rules or UNCITRAL Rules",
        "typical_process": "arbitration",
        "keywords": [
            "international", "cross-border", "foreign", "treaty", "export",
            "import", "trade", "letter of credit", "incoterms", "force majeure",
            "currency", "sovereign immunity", "choice of law", "forum selection",
        ],
    },
    "investment_treaty": {
        "label": "Investment Treaty Disputes",
        "description": "Investor-State disputes under bilateral or multilateral investment treaties",
        "default_forum": "ICSID or UNCITRAL Rules",
        "typical_process": "arbitration",
        "keywords": [
            "investor", "state", "expropriation", "fair and equitable treatment",
            "bit", "bilateral investment treaty", "icsid", "nationalization",
            "regulatory taking", "most favored nation", "umbrella clause",
        ],
    },
    "family": {
        "label": "Family Law Disputes",
        "description": "Divorce, custody, property division, and support disputes",
        "default_forum": "Court-Annexed Mediation or Collaborative Law",
        "typical_process": "mediation",
        "keywords": [
            "divorce", "custody", "child support", "alimony", "spousal support",
            "property division", "prenuptial", "postnuptial", "parenting plan",
            "visitation", "collaborative law", "family mediation",
        ],
    },
    "intellectual_property": {
        "label": "Intellectual Property Disputes",
        "description": "Patent, trademark, copyright, trade secret, and domain name disputes",
        "default_forum": "WIPO Arbitration or AAA Commercial Rules",
        "typical_process": "arbitration",
        "keywords": [
            "patent", "trademark", "copyright", "trade secret", "domain name",
            "udrp", "licensing", "infringement", "royalty", "wipo", "misappropriation",
            "non-disclosure", "ip", "software", "technology transfer",
        ],
    },
    "insurance": {
        "label": "Insurance Disputes",
        "description": "Coverage disputes, claims handling, reinsurance, and bad faith claims",
        "default_forum": "AAA Commercial Rules or ARIAS-US (reinsurance)",
        "typical_process": "arbitration",
        "keywords": [
            "insurance", "coverage", "claim", "policy", "underwriting", "premium",
            "deductible", "subrogation", "bad faith", "reinsurance", "arias",
            "excess", "umbrella", "liability", "property damage",
        ],
    },
    "healthcare": {
        "label": "Healthcare Disputes",
        "description": "Medical malpractice, patient billing, provider-payer disputes, nursing home claims",
        "default_forum": "AAA Healthcare Rules or Court-Annexed Mediation",
        "typical_process": "mediation",
        "keywords": [
            "medical malpractice", "patient", "hospital", "physician", "nursing home",
            "health insurance", "medicare", "medicaid", "hipaa", "informed consent",
            "wrongful death", "billing", "provider", "managed care",
        ],
    },
    "labor": {
        "label": "Labor-Management Disputes",
        "description": "Union grievance arbitration, CBA interpretation, unfair labor practice charges",
        "default_forum": "FMCS or AAA Labor Arbitration Rules",
        "typical_process": "arbitration",
        "keywords": [
            "union", "grievance", "collective bargaining", "cba", "nlrb",
            "unfair labor practice", "strike", "lockout", "just cause",
            "seniority", "arbitration clause", "past practice", "management rights",
        ],
    },
    "environmental": {
        "label": "Environmental Disputes",
        "description": "Contamination, remediation cost allocation, regulatory compliance, natural resource damages",
        "default_forum": "AAA Commercial Rules or Court-Annexed Mediation",
        "typical_process": "mediation",
        "keywords": [
            "environmental", "contamination", "remediation", "cercla", "superfund",
            "clean water act", "clean air act", "epa", "tceq", "brownfield",
            "hazardous waste", "pollution", "natural resource damage",
        ],
    },
}

# ---------------------------------------------------------------------------
# ENUMS
# ---------------------------------------------------------------------------


class BindingType(str, Enum):
    BINDING = "binding"
    NON_BINDING = "non_binding"
    ADVISORY = "advisory"


class ProcessScope(str, Enum):
    DOMESTIC = "domestic"
    INTERNATIONAL = "international"


class AdministrationType(str, Enum):
    INSTITUTIONAL = "institutional"
    AD_HOC = "ad_hoc"


class MediationStyle(str, Enum):
    FACILITATIVE = "facilitative"
    EVALUATIVE = "evaluative"
    TRANSFORMATIVE = "transformative"
    HYBRID = "hybrid"


class DisputeComplexity(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"


# ---------------------------------------------------------------------------
# PYDANTIC MODELS
# ---------------------------------------------------------------------------


class NormalizedQuery(BaseModel):
    """Result of query normalization."""
    original: str
    normalized: str
    expanded_terms: list[str] = Field(default_factory=list)
    detected_categories: list[str] = Field(default_factory=list)
    detected_entities: list[str] = Field(default_factory=list)
    acronyms_resolved: dict[str, str] = Field(default_factory=dict)


# Alias so engine.py can import NormalizationResult
NormalizationResult = NormalizedQuery


class ADREntity(BaseModel):
    """Extracted ADR entity from text."""
    text: str
    entity_type: str
    normalized: str
    confidence: float
    start_pos: int = 0
    end_pos: int = 0


class ClauseAnalysisResult(BaseModel):
    """Result of arbitration clause analysis."""
    clause_text: str
    has_arbitration_clause: bool
    scope: str = ""
    institution: str = ""
    rules: str = ""
    seat: str = ""
    governing_law: str = ""
    num_arbitrators: int = 0
    language: str = ""
    confidentiality: bool = False
    class_waiver: bool = False
    delegation_clause: bool = False
    emergency_arbitrator: bool = False
    appeal_mechanism: bool = False
    enforceability_score: float = 0.0
    issues: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    unconscionability_factors: list[str] = Field(default_factory=list)


class MediationDesign(BaseModel):
    """Recommended mediation process design."""
    dispute_type: str
    recommended_style: MediationStyle
    mediator_qualifications: list[str] = Field(default_factory=list)
    process_steps: list[str] = Field(default_factory=list)
    estimated_duration: str = ""
    estimated_cost: str = ""
    success_factors: list[str] = Field(default_factory=list)
    contraindications: list[str] = Field(default_factory=list)


class DisputeClassification(BaseModel):
    """Classification of a dispute across multiple dimensions."""
    description: str
    category: str
    category_label: str
    binding_type: BindingType
    scope: ProcessScope
    administration: AdministrationType
    complexity: DisputeComplexity
    recommended_process: str
    recommended_forum: str
    applicable_rules: list[str] = Field(default_factory=list)
    relevant_statutes: list[str] = Field(default_factory=list)
    confidence: float = 0.0


# ---------------------------------------------------------------------------
# ENTITY PATTERNS - regex patterns for ADR entity extraction
# ---------------------------------------------------------------------------

_STATUTE_PATTERNS: list[tuple[str, str]] = [
    (r"\b9\s*U\.?S\.?C\.?\s*(?:(?:§|Sec(?:tion)?\.?\s*)?\d+(?:-\d+)?)", "federal_statute"),
    (r"\bFAA\s+(?:§|Section)\s*\d+(?:\([a-z]\)(?:\(\d+\))?)?", "federal_statute"),
    (r"\bFAA\s+Chapter\s+[23]", "federal_statute"),
    (r"\b28\s*U\.?S\.?C\.?\s*(?:§|Sec(?:tion)?\.?\s*)\d+", "federal_statute"),
    (r"\bCPRC\s+(?:Ch(?:apter)?\.?\s*)?\d+(?:\.\d+)?", "state_statute"),
    (r"\bTex\.\s*Civ\.\s*Prac\.\s*&\s*Rem\.\s*Code\s*(?:§|Ch\.?)\s*\d+", "state_statute"),
]

_CASE_PATTERNS: list[tuple[str, str]] = [
    (r"[A-Z][a-zA-Z'\-]+(?:\s+(?:v\.?|vs\.?)\s+)[A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)*", "case_name"),
    (r"\d+\s+(?:U\.?S\.?|F\.?\s*(?:2d|3d|4th)|S\.?\s*(?:Ct|W)\.\s*(?:2d|3d)?)\s+\d+", "case_citation"),
    (r"\d+\s+F\.\s*Supp\.\s*(?:2d|3d)\s+\d+", "case_citation"),
]

_INSTITUTION_PATTERNS: list[tuple[str, str]] = [
    (r"\b(?:AAA|American Arbitration Association)\b", "institution"),
    (r"\b(?:JAMS|Judicial Arbitration and Mediation Services?)\b", "institution"),
    (r"\b(?:FINRA|Financial Industry Regulatory Authority)\b", "institution"),
    (r"\b(?:ICC|International Chamber of Commerce)\b", "institution"),
    (r"\b(?:ICSID|International Centre for Settlement of Investment Disputes)\b", "institution"),
    (r"\b(?:UNCITRAL)\b", "institution"),
    (r"\b(?:LCIA|London Court of International Arbitration)\b", "institution"),
    (r"\b(?:SIAC|Singapore International Arbitration Centre)\b", "institution"),
    (r"\b(?:WIPO)\b", "institution"),
    (r"\b(?:PCA|Permanent Court of Arbitration)\b", "institution"),
]

_CONCEPT_PATTERNS: list[tuple[str, str]] = [
    (r"\b(?:BATNA|WATNA|ZOPA)\b", "negotiation_concept"),
    (r"\bkompetenz[- ]kompetenz\b", "legal_doctrine"),
    (r"\bseparability\s+doctrine\b", "legal_doctrine"),
    (r"\bmanifest\s+disregard\b", "legal_doctrine"),
    (r"\bevident\s+partiality\b", "legal_doctrine"),
    (r"\bdelegation\s+clause\b", "clause_type"),
    (r"\bclass\s+(?:action\s+)?waiver\b", "clause_type"),
    (r"\bmed-?arb\b", "process_type"),
    (r"\barb-?med\b", "process_type"),
    (r"\bearly\s+neutral\s+evaluation\b", "process_type"),
    (r"\bmini[- ]trial\b", "process_type"),
    (r"\bsummary\s+jury\s+trial\b", "process_type"),
    (r"\bdispute\s+review\s+board\b", "process_type"),
    (r"\bcollaborative\s+law\b", "process_type"),
    (r"\bfacilitative\s+mediation\b", "mediation_style"),
    (r"\bevaluative\s+mediation\b", "mediation_style"),
    (r"\btransformative\s+mediation\b", "mediation_style"),
    (r"\bunconsciona(?:bility|ble)\b", "legal_defense"),
    (r"\bpreemption\b", "legal_doctrine"),
    (r"\bNew\s+York\s+Convention\b", "treaty"),
    (r"\bPanama\s+Convention\b", "treaty"),
]


# ---------------------------------------------------------------------------
# CORE FUNCTIONS
# ---------------------------------------------------------------------------


def normalize_query(query: str) -> NormalizedQuery:
    """Normalize an ADR query by expanding acronyms, resolving synonyms, and detecting categories."""
    original = query.strip()
    normalized = original.lower()
    acronyms_resolved: dict[str, str] = {}
    expanded_terms: list[str] = []

    # Expand acronyms from SYNONYM_MAP
    words = re.split(r"(\W+)", normalized)
    result_words: list[str] = []
    for word in words:
        word_clean = word.strip().lower()
        if word_clean in SYNONYM_MAP:
            expansion = SYNONYM_MAP[word_clean]
            acronyms_resolved[word_clean] = expansion
            result_words.append(expansion)
            expanded_terms.append(expansion)
        else:
            result_words.append(word)

    normalized = "".join(result_words)

    # Detect matching categories
    detected_categories: list[str] = []
    query_tokens = set(re.split(r"\W+", normalized.lower()))
    query_tokens.discard("")

    for cat_key, cat_data in CATEGORY_MAP.items():
        keywords = cat_data["keywords"]
        overlap = sum(1 for kw in keywords if kw.lower() in normalized)
        token_overlap = sum(1 for kw in keywords if kw.lower() in query_tokens)
        if overlap >= 2 or token_overlap >= 1:
            detected_categories.append(cat_key)

    # Extract entities
    detected_entities: list[str] = []
    for pattern, etype in _INSTITUTION_PATTERNS + _CONCEPT_PATTERNS:
        for m in re.finditer(pattern, original, re.IGNORECASE):
            detected_entities.append(m.group(0))

    result = NormalizedQuery(
        original=original,
        normalized=normalized,
        expanded_terms=expanded_terms,
        detected_categories=detected_categories,
        detected_entities=detected_entities,
        acronyms_resolved=acronyms_resolved,
    )
    logger.debug("Normalized query: '{}' -> '{}' ({} acronyms, {} categories)",
                 original, normalized, len(acronyms_resolved), len(detected_categories))
    return result


def extract_adr_entities(text: str) -> list[ADREntity]:
    """Extract ADR-related entities from text (statutes, cases, institutions, concepts)."""
    entities: list[ADREntity] = []
    seen_spans: set[tuple[int, int]] = set()

    all_patterns = (
        _STATUTE_PATTERNS + _CASE_PATTERNS +
        _INSTITUTION_PATTERNS + _CONCEPT_PATTERNS
    )

    for pattern, entity_type in all_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start, end = match.start(), match.end()
            # Avoid overlapping entities
            overlap = False
            for s, e in seen_spans:
                if start < e and end > s:
                    overlap = True
                    break
            if overlap:
                continue

            raw_text = match.group(0).strip()
            normalized = _normalize_entity_text(raw_text, entity_type)
            confidence = _compute_entity_confidence(raw_text, entity_type)

            entities.append(ADREntity(
                text=raw_text,
                entity_type=entity_type,
                normalized=normalized,
                confidence=confidence,
                start_pos=start,
                end_pos=end,
            ))
            seen_spans.add((start, end))

    entities.sort(key=lambda e: e.start_pos)
    logger.debug("Extracted {} ADR entities from text ({} chars)", len(entities), len(text))
    return entities


def _normalize_entity_text(text: str, entity_type: str) -> str:
    """Normalize extracted entity text."""
    if entity_type == "institution":
        acronym = text.strip().upper()
        for key, expansion in SYNONYM_MAP.items():
            if key.upper() == acronym or expansion.lower() in text.lower():
                return expansion
        return text

    if entity_type == "federal_statute":
        normalized = re.sub(r"\s+", " ", text.strip())
        normalized = re.sub(r"U\.?S\.?C\.?", "USC", normalized)
        normalized = re.sub(r"Sec(?:tion)?\.?\s*", "Section ", normalized)
        return normalized

    if entity_type == "state_statute":
        normalized = re.sub(r"\s+", " ", text.strip())
        normalized = re.sub(r"Ch(?:apter)?\.?\s*", "Chapter ", normalized)
        return normalized

    if entity_type in ("negotiation_concept", "legal_doctrine", "clause_type", "process_type", "mediation_style"):
        return text.strip().lower()

    return text.strip()


def _compute_entity_confidence(text: str, entity_type: str) -> float:
    """Compute confidence score for an extracted entity."""
    base_scores: dict[str, float] = {
        "federal_statute": 0.92,
        "state_statute": 0.88,
        "case_name": 0.75,
        "case_citation": 0.90,
        "institution": 0.95,
        "negotiation_concept": 0.93,
        "legal_doctrine": 0.88,
        "clause_type": 0.85,
        "process_type": 0.87,
        "mediation_style": 0.90,
        "legal_defense": 0.82,
        "treaty": 0.91,
    }
    score = base_scores.get(entity_type, 0.70)

    # Boost for longer, more specific matches
    if len(text) > 30:
        score = min(score + 0.05, 1.0)
    elif len(text) < 5:
        score = max(score - 0.10, 0.30)

    return round(score, 3)


def classify_dispute_type(description: str) -> DisputeClassification:
    """Classify a dispute across multiple dimensions based on description."""
    desc_lower = description.lower()
    tokens = set(re.split(r"\W+", desc_lower))
    tokens.discard("")

    # Score each category
    category_scores: dict[str, float] = {}
    for cat_key, cat_data in CATEGORY_MAP.items():
        score = 0.0
        for kw in cat_data["keywords"]:
            if kw.lower() in desc_lower:
                score += 2.0
            elif kw.lower() in tokens:
                score += 1.0
        category_scores[cat_key] = score

    best_cat = max(category_scores, key=lambda k: category_scores[k])
    best_score = category_scores[best_cat]
    cat_data = CATEGORY_MAP[best_cat]

    # Determine binding type
    binding_type = BindingType.BINDING
    non_binding_indicators = [
        "mediation", "conciliation", "evaluation", "mini-trial",
        "summary jury", "non-binding", "advisory",
    ]
    for indicator in non_binding_indicators:
        if indicator in desc_lower:
            binding_type = BindingType.NON_BINDING
            break

    # Determine scope
    scope = ProcessScope.DOMESTIC
    international_indicators = [
        "international", "cross-border", "foreign", "treaty",
        "icsid", "icc", "uncitral", "lcia", "siac", "new york convention",
        "bilateral investment", "investor-state", "sovereign",
    ]
    for indicator in international_indicators:
        if indicator in desc_lower:
            scope = ProcessScope.INTERNATIONAL
            break

    # Determine administration type
    administration = AdministrationType.INSTITUTIONAL
    ad_hoc_indicators = ["ad hoc", "uncitral rules", "non-administered", "party-administered"]
    for indicator in ad_hoc_indicators:
        if indicator in desc_lower:
            administration = AdministrationType.AD_HOC
            break

    # Determine complexity
    complexity = _assess_complexity(description)

    # Determine applicable rules
    applicable_rules = _determine_applicable_rules(best_cat, scope, desc_lower)

    # Determine relevant statutes
    relevant_statutes = _determine_relevant_statutes(best_cat, scope, desc_lower)

    # Confidence based on best category score
    confidence = min(best_score / 8.0, 0.99) if best_score > 0 else 0.20

    recommended_process = cat_data.get("typical_process", "arbitration")
    recommended_forum = cat_data.get("default_forum", "AAA Commercial Arbitration Rules")

    classification = DisputeClassification(
        description=description,
        category=best_cat,
        category_label=cat_data["label"],
        binding_type=binding_type,
        scope=scope,
        administration=administration,
        complexity=complexity,
        recommended_process=recommended_process,
        recommended_forum=recommended_forum,
        applicable_rules=applicable_rules,
        relevant_statutes=relevant_statutes,
        confidence=round(confidence, 3),
    )

    logger.info(
        "Classified dispute as '{}' (confidence={}, binding={}, scope={})",
        best_cat, classification.confidence, binding_type.value, scope.value,
    )
    return classification


def _assess_complexity(description: str) -> DisputeComplexity:
    """Assess complexity of a dispute from its description."""
    desc_lower = description.lower()
    complexity_score = 0

    high_complexity_indicators = [
        "multi-party", "multiparty", "class action", "collective action",
        "international", "cross-border", "multiple jurisdictions",
        "investment treaty", "sovereign", "consolidation", "joinder",
        "derivative", "interpleader", "intervention",
    ]
    medium_complexity_indicators = [
        "multiple claims", "counterclaim", "discovery disputes",
        "expert testimony", "damages calculation", "lost profits",
        "consequential", "punitive damages", "injunctive relief",
        "statutory claims", "regulatory",
    ]
    simple_indicators = [
        "small claims", "simple", "straightforward", "single issue",
        "payment dispute", "billing", "refund",
    ]

    for indicator in high_complexity_indicators:
        if indicator in desc_lower:
            complexity_score += 3

    for indicator in medium_complexity_indicators:
        if indicator in desc_lower:
            complexity_score += 2

    for indicator in simple_indicators:
        if indicator in desc_lower:
            complexity_score -= 2

    if complexity_score >= 6:
        return DisputeComplexity.HIGHLY_COMPLEX
    elif complexity_score >= 3:
        return DisputeComplexity.COMPLEX
    elif complexity_score >= 1:
        return DisputeComplexity.MODERATE
    return DisputeComplexity.SIMPLE


def _determine_applicable_rules(category: str, scope: ProcessScope, desc_lower: str) -> list[str]:
    """Determine applicable ADR rules based on category and scope."""
    rules: list[str] = []

    if scope == ProcessScope.INTERNATIONAL:
        rules.append("UNCITRAL Arbitration Rules (2021)")
        rules.append("New York Convention (1958)")
        if "icc" in desc_lower:
            rules.append("ICC Rules of Arbitration (2021)")
        if "icsid" in desc_lower or "investment" in desc_lower:
            rules.append("ICSID Convention and Arbitration Rules (2022)")
        if "lcia" in desc_lower:
            rules.append("LCIA Arbitration Rules (2020)")
        rules.append("IBA Rules on the Taking of Evidence (2020)")
    else:
        rules.append("Federal Arbitration Act (9 USC 1-16)")

    category_rules_map: dict[str, list[str]] = {
        "commercial": ["AAA Commercial Arbitration Rules (2023)", "JAMS Comprehensive Arbitration Rules (2024)"],
        "employment": ["AAA Employment Arbitration Rules (2009)", "JAMS Employment Arbitration Rules (2024)", "AAA Due Process Protocol (1995)"],
        "consumer": ["AAA Consumer Arbitration Rules (2014)", "AAA Consumer Due Process Protocol (1998)"],
        "securities": ["FINRA Customer Code (Rule 12000 Series)", "FINRA Industry Code (Rule 13000 Series)"],
        "construction": ["AAA Construction Industry Arbitration Rules (2015)", "AIA A201-2017 Article 15"],
        "real_estate": ["AAA Real Estate Industry Rules", "NAR Code of Ethics Article 17"],
        "oil_gas": ["AAPL Form 610-2015 Article 17", "AAA Commercial Arbitration Rules", "COPAS Accounting Procedures"],
        "family": ["Uniform Mediation Act", "State Family Mediation Statutes"],
        "intellectual_property": ["WIPO Arbitration Rules", "ICANN UDRP", "AAA Commercial Arbitration Rules"],
        "insurance": ["AAA Commercial Arbitration Rules", "ARIAS-US Rules (Reinsurance)"],
        "labor": ["FMCS Arbitration Procedures", "AAA Labor Arbitration Rules"],
        "healthcare": ["AAA Healthcare Arbitration Rules"],
        "environmental": ["AAA Commercial Arbitration Rules", "EPA ADR Procedures"],
        "investment_treaty": ["ICSID Convention and Arbitration Rules", "UNCITRAL Arbitration Rules"],
        "international_commercial": ["ICC Rules of Arbitration (2021)", "UNCITRAL Arbitration Rules (2021)"],
    }

    cat_rules = category_rules_map.get(category, [])
    for rule in cat_rules:
        if rule not in rules:
            rules.append(rule)

    return rules


def _determine_relevant_statutes(category: str, scope: ProcessScope, desc_lower: str) -> list[str]:
    """Determine relevant statutes based on category and scope."""
    statutes: list[str] = ["9 USC 1-16 (Federal Arbitration Act)"]

    if scope == ProcessScope.INTERNATIONAL:
        statutes.append("9 USC 201-208 (FAA Chapter 2 - New York Convention)")
        statutes.append("9 USC 301-307 (FAA Chapter 3 - Panama Convention)")

    if "texas" in desc_lower or "tx" in desc_lower or category == "oil_gas":
        statutes.append("Tex. Civ. Prac. & Rem. Code Ch. 154 (ADR Procedures)")
        statutes.append("Tex. Civ. Prac. & Rem. Code Ch. 171 (Texas General Arbitration Act)")

    category_statutes_map: dict[str, list[str]] = {
        "employment": [
            "9 USC 401-402 (Ending Forced Arbitration Act)",
            "Title VII of the Civil Rights Act of 1964",
            "Americans with Disabilities Act",
            "Age Discrimination in Employment Act",
            "Fair Labor Standards Act",
        ],
        "consumer": [
            "9 USC 401-402 (Ending Forced Arbitration Act)",
            "Federal Trade Commission Act Section 5",
            "Magnuson-Moss Warranty Act",
        ],
        "securities": [
            "Securities Exchange Act of 1934 Section 10(b)",
            "Securities Act of 1933 Section 12",
            "Investment Advisers Act of 1940",
        ],
        "construction": [
            "Miller Act (40 USC 3131-3134) (federal construction)",
            "Texas Property Code Ch. 53 (Mechanic's Liens)",
        ],
        "oil_gas": [
            "Texas Natural Resources Code",
            "Texas Property Code (mineral interests)",
        ],
        "investment_treaty": [
            "ICSID Convention (1965)",
            "Relevant Bilateral Investment Treaty",
        ],
        "labor": [
            "National Labor Relations Act Section 7",
            "Labor Management Relations Act Section 301",
        ],
    }

    cat_statutes = category_statutes_map.get(category, [])
    for statute in cat_statutes:
        if statute not in statutes:
            statutes.append(statute)

    return statutes


# ---------------------------------------------------------------------------
# ARBITRATION CLAUSE ANALYZER
# ---------------------------------------------------------------------------


class ArbitrationClauseAnalyzer:
    """Analyze arbitration clauses for scope, enforceability, and drafting quality."""

    SCOPE_PATTERNS: list[tuple[str, str]] = [
        (r"any\s+(?:dispute|controversy|claim)\s+arising\s+(?:out\s+of|under|relating\s+to)", "broad"),
        (r"all\s+(?:disputes?|controversies|claims?)\s+(?:arising|relating|connected)", "broad"),
        (r"disputes?\s+under\s+this\s+(?:agreement|contract)", "narrow"),
        (r"may\s+(?:be\s+)?(?:submitted|referred)\s+to\s+arbitration", "optional"),
        (r"shall\s+(?:be\s+)?(?:settled|resolved|determined)\s+by\s+arbitration", "mandatory"),
    ]

    INSTITUTION_PATTERNS: list[tuple[str, str]] = [
        (r"American\s+Arbitration\s+Association|AAA", "AAA"),
        (r"JAMS|Judicial\s+Arbitration", "JAMS"),
        (r"FINRA", "FINRA"),
        (r"ICC|International\s+Chamber\s+of\s+Commerce", "ICC"),
        (r"UNCITRAL", "UNCITRAL"),
        (r"LCIA|London\s+Court", "LCIA"),
        (r"ICSID", "ICSID"),
        (r"SIAC|Singapore\s+International\s+Arbitration", "SIAC"),
    ]

    def analyze(self, clause_text: str) -> ClauseAnalysisResult:
        """Perform comprehensive analysis of an arbitration clause."""
        text_lower = clause_text.lower()

        has_arb = bool(re.search(r"\barbitrat(?:ion|e|ed|ing|or)\b", text_lower))

        scope = self._analyze_scope(clause_text)
        institution = self._detect_institution(clause_text)
        rules = self._detect_rules(clause_text)
        seat = self._detect_seat(clause_text)
        governing_law = self._detect_governing_law(clause_text)
        num_arbs = self._detect_num_arbitrators(clause_text)
        language = self._detect_language(clause_text)
        confidentiality = bool(re.search(r"\bconfidential(?:ity)?\b", text_lower))
        class_waiver = bool(re.search(r"\bclass\s+(?:action\s+)?waiver\b|\bno\s+class\b|\bindividual\s+basis\b", text_lower))
        delegation = bool(re.search(r"\bdelegat(?:ion|e)\b|\bjurisdiction\s+over\s+(?:its|their)\s+own\s+jurisdiction\b", text_lower))
        emergency = bool(re.search(r"\bemergency\s+(?:arbitrat(?:or|ion)|measures?|relief)\b", text_lower))
        appeal = bool(re.search(r"\bappeal(?:s|able)?\b|\bappellate\b", text_lower))

        issues = self._identify_issues(clause_text, has_arb, scope, institution, seat)
        recommendations = self._generate_recommendations(clause_text, has_arb, scope, institution, seat, num_arbs)
        unconscionability = self._assess_unconscionability(clause_text)
        enforceability = self._compute_enforceability_score(has_arb, scope, institution, seat, issues, unconscionability)

        result = ClauseAnalysisResult(
            clause_text=clause_text,
            has_arbitration_clause=has_arb,
            scope=scope,
            institution=institution,
            rules=rules,
            seat=seat,
            governing_law=governing_law,
            num_arbitrators=num_arbs,
            language=language,
            confidentiality=confidentiality,
            class_waiver=class_waiver,
            delegation_clause=delegation,
            emergency_arbitrator=emergency,
            appeal_mechanism=appeal,
            enforceability_score=enforceability,
            issues=issues,
            recommendations=recommendations,
            unconscionability_factors=unconscionability,
        )

        logger.info(
            "Clause analysis: has_arb={}, scope='{}', institution='{}', enforceability={:.2f}, issues={}",
            has_arb, scope, institution, enforceability, len(issues),
        )
        return result

    def _analyze_scope(self, text: str) -> str:
        """Determine the scope of the arbitration clause."""
        for pattern, scope_type in self.SCOPE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return scope_type
        if re.search(r"\barbitrat", text, re.IGNORECASE):
            return "indeterminate"
        return "none"

    def _detect_institution(self, text: str) -> str:
        """Detect the administering institution."""
        for pattern, name in self.INSTITUTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return name
        return ""

    def _detect_rules(self, text: str) -> str:
        """Detect specified arbitration rules."""
        rules_patterns: list[tuple[str, str]] = [
            (r"Commercial\s+Arbitration\s+Rules", "AAA Commercial Arbitration Rules"),
            (r"Construction\s+(?:Industry\s+)?(?:Arbitration\s+)?Rules", "AAA Construction Industry Rules"),
            (r"Employment\s+(?:Arbitration\s+)?Rules", "AAA Employment Arbitration Rules"),
            (r"Consumer\s+(?:Arbitration\s+)?Rules", "AAA Consumer Arbitration Rules"),
            (r"Comprehensive\s+(?:Arbitration\s+)?Rules", "JAMS Comprehensive Arbitration Rules"),
            (r"Streamlined\s+(?:Arbitration\s+)?Rules", "JAMS Streamlined Arbitration Rules"),
            (r"ICC\s+(?:Rules\s+of\s+)?Arbitration", "ICC Rules of Arbitration"),
            (r"UNCITRAL\s+(?:Arbitration\s+)?Rules", "UNCITRAL Arbitration Rules"),
            (r"LCIA\s+(?:Arbitration\s+)?Rules", "LCIA Arbitration Rules"),
            (r"FINRA\s+(?:Customer|Industry)\s+(?:Code|Rules?)", "FINRA Dispute Resolution Rules"),
        ]
        for pattern, rules_name in rules_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return rules_name
        return ""

    def _detect_seat(self, text: str) -> str:
        """Detect the seat/place of arbitration."""
        seat_patterns = [
            r"(?:seat|place|venue|location)\s+(?:of\s+(?:the\s+)?arbitration\s+(?:shall\s+be|is|will\s+be)\s+)([A-Z][a-zA-Z\s,]+?)(?:\.|;|$)",
            r"(?:arbitration\s+(?:shall\s+be\s+)?(?:held|conducted|take\s+place)\s+in\s+)([A-Z][a-zA-Z\s,]+?)(?:\.|;|$)",
            r"(?:in\s+)([A-Z][a-zA-Z]+(?:,\s*[A-Z][a-zA-Z]+)?)\s+(?:in\s+accordance|under|pursuant)",
        ]
        for pattern in seat_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip().rstrip(",.")
        return ""

    def _detect_governing_law(self, text: str) -> str:
        """Detect governing law clause."""
        gov_law_patterns = [
            r"(?:governed?\s+by|construed\s+(?:under|in\s+accordance\s+with)|subject\s+to)\s+(?:the\s+)?(?:laws?\s+of\s+)?(?:the\s+)?(?:State\s+of\s+)?([A-Z][a-zA-Z\s]+?)(?:\s+law)?(?:\.|;|,|$)",
            r"(?:law\s+of\s+)([A-Z][a-zA-Z\s]+?)(?:\s+shall\s+(?:apply|govern))",
        ]
        for pattern in gov_law_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip().rstrip(",.")
        return ""

    def _detect_num_arbitrators(self, text: str) -> int:
        """Detect the number of arbitrators specified."""
        patterns = [
            (r"\b(?:one|single|sole)\s+arbitrator\b", 1),
            (r"\b(?:three|3|panel\s+of\s+three)\s+arbitrators?\b", 3),
            (r"\b(?:two|2)\s+arbitrators?\b", 2),
        ]
        for pattern, count in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return count
        return 0

    def _detect_language(self, text: str) -> str:
        """Detect specified language of arbitration."""
        lang_pattern = r"(?:language\s+of\s+(?:the\s+)?arbitration\s+(?:shall\s+be|is|will\s+be)\s+)([A-Za-z]+)"
        match = re.search(lang_pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""

    def _identify_issues(self, text: str, has_arb: bool, scope: str, institution: str, seat: str) -> list[str]:
        """Identify potential issues with the arbitration clause."""
        issues: list[str] = []

        if not has_arb:
            issues.append("No arbitration language detected")
            return issues

        if scope == "none" or scope == "indeterminate":
            issues.append("Scope of arbitration clause is unclear or indeterminate")

        if scope == "narrow":
            issues.append("Narrow scope may exclude tort, statutory, or extra-contractual claims")

        if scope == "optional":
            issues.append("Optional arbitration language may not create a binding obligation")

        if not institution:
            issues.append("No administering institution specified; may create appointment difficulties")

        if not seat:
            issues.append("No seat/place of arbitration specified; critical for procedural law determination")

        # Check for conflicting provisions
        if re.search(r"\bfinal\b", text, re.IGNORECASE) and re.search(r"\bappeal\b", text, re.IGNORECASE):
            issues.append("Potential conflict between finality language and appeal provisions")

        # Check for multiple institutions
        detected_institutions = []
        for pattern, name in self.INSTITUTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                detected_institutions.append(name)
        if len(detected_institutions) > 1:
            issues.append(f"Multiple institutions referenced: {', '.join(detected_institutions)} - may create ambiguity")

        # Check for pathological clause indicators
        if re.search(r"\bmay\s+(?:elect|choose|opt)\b", text, re.IGNORECASE):
            issues.append("Permissive language ('may elect') may not create binding obligation")

        return issues

    def _generate_recommendations(self, text: str, has_arb: bool, scope: str,
                                   institution: str, seat: str, num_arbs: int) -> list[str]:
        """Generate drafting recommendations."""
        recommendations: list[str] = []

        if not has_arb:
            recommendations.append("Add an arbitration clause using the model clause from the chosen institution")
            return recommendations

        if scope != "broad":
            recommendations.append(
                "Broaden scope to 'any dispute, controversy, or claim arising out of or "
                "relating to this agreement, including breach, termination, or validity thereof'"
            )

        if not institution:
            recommendations.append("Specify an administering institution (AAA, JAMS, ICC) and applicable rules")

        if not seat:
            recommendations.append("Specify the seat/place of arbitration (determines supervisory court and procedural law)")

        if num_arbs == 0:
            recommendations.append("Specify number of arbitrators (one for smaller disputes, three for larger/complex)")

        if not re.search(r"\bconfidential", text, re.IGNORECASE):
            recommendations.append("Consider adding a confidentiality provision (not implied in most jurisdictions)")

        if not re.search(r"\binterim\b|\bpreliminary\b|\bprovisional\b|\binjunct", text, re.IGNORECASE):
            recommendations.append("Include a carve-out preserving the right to seek interim/injunctive relief from courts")

        if not re.search(r"\bgoverning\s+law\b|\bconstrued\b|\bapplicable\s+law\b", text, re.IGNORECASE):
            recommendations.append("Specify governing law for the contract and the arbitration agreement separately")

        return recommendations

    def _assess_unconscionability(self, text: str) -> list[str]:
        """Identify potential unconscionability factors."""
        factors: list[str] = []
        text_lower = text.lower()

        # Procedural unconscionability indicators
        if re.search(r"\bnon-?negotiable\b|\btake\s+it\s+or\s+leave\b|\badhesion\b", text_lower):
            factors.append("PROCEDURAL: Contract of adhesion / non-negotiable terms")

        if re.search(r"\bshort(?:ened)?\s+(?:limitations?|statute)\b|\b(?:30|60|90)\s+days?\s+(?:to\s+file|limitations?)\b", text_lower):
            factors.append("SUBSTANTIVE: Shortened limitations period may prevent vindication of statutory rights")

        if re.search(r"\bwaiv(?:e|er)\s+(?:of\s+)?(?:all\s+)?(?:punitive|statutory|consequential)\s+damages?\b", text_lower):
            factors.append("SUBSTANTIVE: Waiver of statutory or punitive damages may prevent effective vindication")

        if re.search(r"\bloser\s+pays?\b|\bfee[- ]shifting\b|\bprevailing\s+party\b", text_lower):
            factors.append("SUBSTANTIVE: Fee-shifting/loser-pays provision may deter pursuit of statutory claims")

        if re.search(r"\bone[- ]?(?:sided|way)\b|\bonly\s+(?:employer|company|one\s+party)\b", text_lower):
            factors.append("SUBSTANTIVE: One-sided/unilateral arbitration obligation (lack of mutuality)")

        if re.search(r"\bemployee\s+(?:shall\s+)?pay\b|\bcosts?\s+(?:shared|split)\s+equally\b", text_lower):
            factors.append("SUBSTANTIVE: Cost-splitting may impose prohibitive costs on employee/consumer")

        if re.search(r"\bno\s+(?:discovery|depositions?|document\s+exchange)\b|\bdiscovery\s+(?:is\s+)?prohibited\b", text_lower):
            factors.append("SUBSTANTIVE: Elimination of discovery may prevent adequate case preparation")

        if re.search(r"\bselect(?:ed|ion)\s+by\s+(?:employer|company)\b|\bcompany[- ]?appointed\b", text_lower):
            factors.append("SUBSTANTIVE: Employer/company-controlled arbitrator selection process")

        return factors

    def _compute_enforceability_score(self, has_arb: bool, scope: str, institution: str,
                                       seat: str, issues: list[str], unconscionability: list[str]) -> float:
        """Compute overall enforceability score (0.0 to 1.0)."""
        if not has_arb:
            return 0.0

        score = 0.70  # Base score for having an arbitration clause

        # Scope bonus/penalty
        scope_scores = {"broad": 0.10, "mandatory": 0.08, "narrow": -0.05, "optional": -0.15, "indeterminate": -0.10}
        score += scope_scores.get(scope, 0.0)

        # Institution bonus
        if institution:
            score += 0.08

        # Seat bonus
        if seat:
            score += 0.05

        # Issue penalties
        score -= len(issues) * 0.03

        # Unconscionability penalties
        score -= len(unconscionability) * 0.05

        return round(max(0.0, min(1.0, score)), 3)


# ---------------------------------------------------------------------------
# MEDIATION PROCESS DESIGNER
# ---------------------------------------------------------------------------


class MediationProcessDesigner:
    """Design appropriate mediation processes based on dispute characteristics."""

    def design(self, dispute_type: str, relationship_ongoing: bool = False,
               power_balance: str = "equal", complexity: str = "moderate",
               amount_in_dispute: float = 0.0) -> MediationDesign:
        """Design a mediation process based on dispute characteristics."""
        style = self._select_style(dispute_type, relationship_ongoing, power_balance, complexity)
        qualifications = self._determine_qualifications(dispute_type, style, amount_in_dispute)
        steps = self._design_process_steps(style, complexity)
        duration = self._estimate_duration(complexity, amount_in_dispute)
        cost = self._estimate_cost(style, duration, amount_in_dispute)
        success_factors = self._identify_success_factors(style, dispute_type, relationship_ongoing)
        contraindications = self._identify_contraindications(style, dispute_type, power_balance)

        design = MediationDesign(
            dispute_type=dispute_type,
            recommended_style=style,
            mediator_qualifications=qualifications,
            process_steps=steps,
            estimated_duration=duration,
            estimated_cost=cost,
            success_factors=success_factors,
            contraindications=contraindications,
        )

        logger.info(
            "Mediation design: type='{}', style='{}', duration='{}', cost='{}'",
            dispute_type, style.value, duration, cost,
        )
        return design

    def _select_style(self, dispute_type: str, relationship_ongoing: bool,
                      power_balance: str, complexity: str) -> MediationStyle:
        """Select appropriate mediation style."""
        dt_lower = dispute_type.lower()

        # Transformative: ongoing relationships, workplace, community
        if relationship_ongoing and dt_lower in ("employment", "family", "labor", "community", "workplace"):
            return MediationStyle.TRANSFORMATIVE

        # Evaluative: complex commercial, construction, IP, insurance
        if complexity in ("complex", "highly_complex") or dt_lower in (
            "construction", "insurance", "intellectual_property", "securities",
            "commercial", "real_estate",
        ):
            return MediationStyle.EVALUATIVE

        # Facilitative: default for most cases, especially balanced parties
        if power_balance == "equal":
            return MediationStyle.FACILITATIVE

        # Hybrid: unequal power, mixed complexity
        if power_balance == "unequal":
            return MediationStyle.HYBRID

        return MediationStyle.FACILITATIVE

    def _determine_qualifications(self, dispute_type: str, style: MediationStyle,
                                   amount: float) -> list[str]:
        """Determine required mediator qualifications."""
        qualifications: list[str] = [
            "Certified mediator (minimum 40 hours training)",
            "No conflicts of interest with any party",
        ]

        if style == MediationStyle.EVALUATIVE:
            qualifications.append("Subject-matter expertise in the relevant legal area")
            qualifications.append("Minimum 10 years legal practice experience")

        if style == MediationStyle.TRANSFORMATIVE:
            qualifications.append("Certified in transformative mediation methodology")
            qualifications.append("Experience with ongoing relationship disputes")

        dt_lower = dispute_type.lower()
        type_qualifications: dict[str, list[str]] = {
            "construction": ["Construction law expertise", "Understanding of AIA/ConsensusDocs contracts"],
            "securities": ["Securities law expertise", "FINRA mediation panel membership"],
            "employment": ["Employment law expertise", "Title VII/ADA/ADEA familiarity"],
            "family": ["Family mediation certification (40+ additional hours)", "Child development training"],
            "oil_gas": ["Oil and gas industry knowledge", "Familiarity with AAPL forms and COPAS"],
            "intellectual_property": ["IP law expertise", "Patent/trademark/copyright experience"],
            "international_commercial": ["International arbitration experience", "Multi-language capability"],
            "insurance": ["Insurance coverage expertise", "Reinsurance and excess coverage knowledge"],
            "healthcare": ["Healthcare law expertise", "Medical terminology familiarity"],
            "environmental": ["Environmental law expertise", "Technical remediation knowledge"],
        }

        for qual in type_qualifications.get(dt_lower, []):
            qualifications.append(qual)

        if amount > 1_000_000:
            qualifications.append("Experience with high-value disputes (>$1M)")

        return qualifications

    def _design_process_steps(self, style: MediationStyle, complexity: str) -> list[str]:
        """Design the mediation process steps."""
        base_steps = [
            "1. Mediator selection and conflict check",
            "2. Pre-mediation submissions (position statements, key documents)",
            "3. Pre-mediation conference call with mediator",
        ]

        if style == MediationStyle.FACILITATIVE:
            base_steps.extend([
                "4. Joint opening session with opening statements",
                "5. Identification of issues and interests (not positions)",
                "6. Private caucuses with each party",
                "7. Option generation (brainstorming without commitment)",
                "8. Evaluation of options against objective criteria",
                "9. Negotiation and reality testing in caucuses",
                "10. Agreement drafting and review",
            ])
        elif style == MediationStyle.EVALUATIVE:
            base_steps.extend([
                "4. Joint opening session with abbreviated case presentations",
                "5. Mediator questions on key legal and factual issues",
                "6. Private caucuses — mediator assessment of strengths/weaknesses",
                "7. Mediator reality testing: likely outcome range at trial",
                "8. Bracketing and mediator's proposal if appropriate",
                "9. Risk-adjusted negotiation in caucuses",
                "10. Settlement agreement drafting and execution",
            ])
        elif style == MediationStyle.TRANSFORMATIVE:
            base_steps.extend([
                "4. Joint session — parties set their own agenda",
                "5. Mediator reflects and summarizes party statements",
                "6. Empowerment: parties clarify their own situation and options",
                "7. Recognition: parties acknowledge each other's perspective",
                "8. Parties direct the conversation — mediator follows",
                "9. If parties choose: explore resolution options",
                "10. If agreement reached: memorialize in writing",
            ])
        else:  # HYBRID
            base_steps.extend([
                "4. Joint opening session with structured presentations",
                "5. Facilitative phase — interest identification in caucuses",
                "6. Option generation and collaborative problem-solving",
                "7. Evaluative phase — mediator assessment if impasse reached",
                "8. Mediator reality testing and risk analysis in caucuses",
                "9. Combined approach: mediator's proposal if needed",
                "10. Agreement drafting and execution",
            ])

        if complexity in ("complex", "highly_complex"):
            base_steps.append("11. Follow-up session if needed (within 14 days)")
            base_steps.append("12. Implementation monitoring and compliance check")

        return base_steps

    def _estimate_duration(self, complexity: str, amount: float) -> str:
        """Estimate mediation session duration."""
        duration_map = {
            "simple": "Half day (4 hours)",
            "moderate": "Full day (8 hours)",
            "complex": "1-2 full days (8-16 hours)",
            "highly_complex": "2-3 full days (16-24 hours), possibly over multiple sessions",
        }
        base = duration_map.get(complexity, "Full day (8 hours)")
        if amount > 5_000_000:
            base += " — high-value case may require additional sessions"
        return base

    def _estimate_cost(self, style: MediationStyle, duration: str, amount: float) -> str:
        """Estimate mediation costs."""
        if "half day" in duration.lower():
            range_str = "$2,000 - $5,000"
        elif "1-2" in duration:
            range_str = "$5,000 - $15,000"
        elif "2-3" in duration:
            range_str = "$10,000 - $30,000"
        else:
            range_str = "$3,000 - $8,000"

        if style == MediationStyle.EVALUATIVE:
            range_str += " (evaluative mediators typically command higher hourly rates: $400-$1,200/hour)"

        if amount > 1_000_000:
            range_str += " (complex, high-value cases may exceed these estimates)"

        return range_str

    def _identify_success_factors(self, style: MediationStyle, dispute_type: str,
                                   relationship_ongoing: bool) -> list[str]:
        """Identify factors that increase likelihood of mediation success."""
        factors: list[str] = [
            "Both parties attend with full settlement authority",
            "Good-faith participation by all parties",
            "Adequate pre-mediation preparation (exchange of key information)",
            "Realistic expectations about likely outcomes",
        ]

        if relationship_ongoing:
            factors.append("Parties' willingness to preserve the ongoing relationship")
            factors.append("Focus on future interests rather than past grievances")

        style_factors: dict[MediationStyle, list[str]] = {
            MediationStyle.FACILITATIVE: [
                "Parties willing to move beyond positions to explore interests",
                "Creative solutions possible (not purely zero-sum)",
            ],
            MediationStyle.EVALUATIVE: [
                "Both sides have engaged in sufficient discovery to understand the case",
                "Decision-makers present who can respond to mediator's assessment",
            ],
            MediationStyle.TRANSFORMATIVE: [
                "Parties willing to engage in genuine dialogue",
                "Recognition that relationship dynamics are central to the dispute",
            ],
            MediationStyle.HYBRID: [
                "Flexibility to shift between approaches as needed",
                "Willingness to hear mediator's evaluation if facilitation stalls",
            ],
        }
        factors.extend(style_factors.get(style, []))

        return factors

    def _identify_contraindications(self, style: MediationStyle, dispute_type: str,
                                     power_balance: str) -> list[str]:
        """Identify factors that may reduce mediation effectiveness."""
        contras: list[str] = []

        if power_balance == "severely_unequal":
            contras.append("Severe power imbalance may undermine voluntariness of agreement")

        if "domestic violence" in dispute_type.lower() or "abuse" in dispute_type.lower():
            contras.append("History of abuse/violence may make face-to-face mediation unsafe or coercive")

        if style == MediationStyle.TRANSFORMATIVE:
            contras.append("May not be effective for purely commercial/transactional disputes with no ongoing relationship")
            contras.append("Time-sensitive disputes may not benefit from open-ended transformative process")

        if style == MediationStyle.EVALUATIVE:
            contras.append("Parties may defer to mediator's opinion rather than exercising self-determination")
            contras.append("Early evaluation may entrench positions if parties disagree with assessment")

        general_contras = [
            "Party acting in bad faith or using mediation for delay/discovery purposes",
            "Precedent-setting dispute requiring published court decision",
            "Need for injunctive or emergency relief that mediation cannot provide",
        ]
        contras.extend(general_contras)

        return contras


# ---------------------------------------------------------------------------
# DISPUTE CLASSIFIER
# ---------------------------------------------------------------------------


class DisputeClassifier:
    """Classify disputes across binding/non-binding, domestic/international, institutional/ad-hoc dimensions."""

    def classify(self, description: str) -> DisputeClassification:
        """Full dispute classification from text description."""
        return classify_dispute_type(description)

    def classify_binding(self, process_description: str) -> BindingType:
        """Determine if a process is binding, non-binding, or advisory."""
        desc_lower = process_description.lower()

        binding_terms = [
            "arbitration", "binding", "final and binding", "final award",
            "med-arb", "baseball arbitration", "final offer",
        ]
        non_binding_terms = [
            "mediation", "non-binding", "advisory", "recommendation",
            "conciliation", "early neutral evaluation", "mini-trial",
            "summary jury", "dispute review board",
        ]

        binding_score = sum(1 for t in binding_terms if t in desc_lower)
        non_binding_score = sum(1 for t in non_binding_terms if t in desc_lower)

        if binding_score > non_binding_score:
            return BindingType.BINDING
        elif non_binding_score > binding_score:
            return BindingType.NON_BINDING
        return BindingType.ADVISORY

    def classify_scope(self, description: str) -> ProcessScope:
        """Determine domestic vs international scope."""
        desc_lower = description.lower()
        international_terms = [
            "international", "cross-border", "foreign", "treaty",
            "new york convention", "icsid", "icc", "lcia", "siac",
            "uncitral", "bilateral investment", "investor-state",
            "panama convention", "foreign arbitral award",
        ]
        for term in international_terms:
            if term in desc_lower:
                return ProcessScope.INTERNATIONAL
        return ProcessScope.DOMESTIC

    def classify_administration(self, description: str) -> AdministrationType:
        """Determine institutional vs ad hoc administration."""
        desc_lower = description.lower()
        institutional_terms = [
            "aaa", "jams", "icc", "finra", "icsid", "lcia", "siac",
            "hkiac", "scc", "wipo", "pca", "cietac", "administered",
            "institutional", "american arbitration", "international chamber",
        ]
        ad_hoc_terms = [
            "ad hoc", "non-administered", "party-administered",
            "uncitral rules", "self-administered",
        ]

        institutional_score = sum(1 for t in institutional_terms if t in desc_lower)
        ad_hoc_score = sum(1 for t in ad_hoc_terms if t in desc_lower)

        if ad_hoc_score > institutional_score:
            return AdministrationType.AD_HOC
        return AdministrationType.INSTITUTIONAL

    def recommend_process(self, description: str, prefer_speed: bool = False,
                          prefer_cost: bool = False, prefer_privacy: bool = False,
                          relationship_ongoing: bool = False) -> dict[str, Any]:
        """Recommend the optimal ADR process for a dispute."""
        classification = self.classify(description)

        process_scores: dict[str, float] = {
            "arbitration": 5.0,
            "mediation": 5.0,
            "med-arb": 4.0,
            "early_neutral_evaluation": 3.0,
            "negotiation": 3.0,
            "litigation": 2.0,
        }

        # Speed preference
        if prefer_speed:
            process_scores["mediation"] += 3.0
            process_scores["early_neutral_evaluation"] += 2.0
            process_scores["negotiation"] += 2.0
            process_scores["arbitration"] -= 1.0
            process_scores["litigation"] -= 3.0

        # Cost preference
        if prefer_cost:
            process_scores["negotiation"] += 3.0
            process_scores["mediation"] += 2.0
            process_scores["early_neutral_evaluation"] += 1.0
            process_scores["arbitration"] -= 1.0
            process_scores["litigation"] -= 3.0

        # Privacy preference
        if prefer_privacy:
            process_scores["arbitration"] += 2.0
            process_scores["mediation"] += 2.0
            process_scores["litigation"] -= 3.0

        # Ongoing relationship
        if relationship_ongoing:
            process_scores["mediation"] += 3.0
            process_scores["med-arb"] += 1.0
            process_scores["litigation"] -= 2.0

        # Category-specific adjustments
        if classification.category == "securities":
            process_scores["arbitration"] += 3.0  # FINRA mandatory
        elif classification.category == "family":
            process_scores["mediation"] += 3.0
        elif classification.category in ("construction", "oil_gas"):
            process_scores["med-arb"] += 2.0

        # Binding requirement
        if classification.binding_type == BindingType.BINDING:
            process_scores["arbitration"] += 2.0
            process_scores["mediation"] -= 1.0

        best_process = max(process_scores, key=lambda k: process_scores[k])

        recommendation = {
            "classification": classification.model_dump(),
            "recommended_process": best_process,
            "process_scores": {k: round(v, 1) for k, v in sorted(process_scores.items(), key=lambda x: -x[1])},
            "reasoning": self._generate_reasoning(best_process, classification, prefer_speed, prefer_cost, prefer_privacy, relationship_ongoing),
        }

        logger.info(
            "Process recommendation: '{}' for category '{}' (score={:.1f})",
            best_process, classification.category, process_scores[best_process],
        )
        return recommendation

    def _generate_reasoning(self, process: str, classification: DisputeClassification,
                            speed: bool, cost: bool, privacy: bool, relationship: bool) -> str:
        """Generate reasoning for the process recommendation."""
        reasons: list[str] = []

        reasons.append(f"Dispute classified as {classification.category_label} "
                       f"({classification.scope.value}, {classification.complexity.value} complexity).")

        process_reasons: dict[str, str] = {
            "arbitration": "Arbitration provides a binding, enforceable decision with limited judicial review, "
                           "subject-matter expert arbitrators, and procedural flexibility.",
            "mediation": "Mediation preserves party control over the outcome, is faster and less expensive "
                         "than arbitration or litigation, and is particularly effective for ongoing relationships.",
            "med-arb": "Med-arb combines the benefits of mediation (party control, speed) with the certainty "
                       "of arbitration if mediation fails, providing strong incentive to settle.",
            "early_neutral_evaluation": "ENE provides early, expert case assessment that helps parties "
                                        "calibrate expectations and often leads to settlement.",
            "negotiation": "Direct negotiation is the fastest and most cost-effective approach; "
                           "suitable for disputes where parties have good-faith interest in resolving quickly.",
            "litigation": "Litigation may be necessary when binding precedent is needed, injunctive "
                          "relief is required, or one party refuses to participate in ADR.",
        }
        reasons.append(process_reasons.get(process, ""))

        if speed:
            reasons.append("Speed was prioritized, favoring faster resolution methods.")
        if cost:
            reasons.append("Cost efficiency was prioritized, favoring lower-cost methods.")
        if privacy:
            reasons.append("Privacy was prioritized, favoring confidential processes.")
        if relationship:
            reasons.append("Ongoing relationship preservation was prioritized, favoring collaborative methods.")

        return " ".join(reasons)
