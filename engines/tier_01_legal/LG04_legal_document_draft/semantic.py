"""
LG04 Legal Document Draft Engine - Semantic Normalization Module
=================================================================
Semantic normalization, term mapping, and query analysis for legal
document drafting. Maps user-language to canonical legal drafting
terminology and provides structural analysis of document requests.

Engine ID: LG04
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# VERSION AND INTEGRITY
# ============================================================================

_SEMANTIC_MAP_VERSION = "1.0.0"
_SEMANTIC_MAP_BUILD_DATE = "2026-02-10"


# ============================================================================
# ENUMS
# ============================================================================


class DocumentDomain(str, Enum):
    """Primary document domain categories."""

    CONTRACT = "contract"
    REAL_ESTATE = "real_estate"
    EMPLOYMENT = "employment"
    CORPORATE = "corporate"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    FINANCE = "finance"
    ESTATE_PLANNING = "estate_planning"
    REGULATORY = "regulatory"
    LITIGATION = "litigation"
    GENERAL = "general"


class ClauseCategory(str, Enum):
    """Standard clause classification categories."""

    DEFINITIONS = "definitions"
    REPRESENTATIONS = "representations_warranties"
    COVENANTS = "covenants"
    CONDITIONS = "conditions_precedent"
    INDEMNIFICATION = "indemnification"
    LIMITATION_LIABILITY = "limitation_of_liability"
    CONFIDENTIALITY = "confidentiality"
    NON_COMPETE = "non_compete"
    NON_SOLICITATION = "non_solicitation"
    IP_RIGHTS = "intellectual_property"
    TERMINATION = "termination"
    DISPUTE_RESOLUTION = "dispute_resolution"
    GOVERNING_LAW = "governing_law"
    FORCE_MAJEURE = "force_majeure"
    ASSIGNMENT = "assignment"
    NOTICES = "notices"
    SEVERABILITY = "severability"
    ENTIRE_AGREEMENT = "entire_agreement"
    AMENDMENT = "amendment"
    WAIVER = "waiver"
    COUNTERPARTS = "counterparts"
    SURVIVAL = "survival"
    INSURANCE = "insurance"
    COMPLIANCE = "compliance_with_laws"
    BOILERPLATE = "boilerplate"


# ============================================================================
# SEMANTIC DICTIONARY - LEGAL DRAFTING TERMS
# ============================================================================

LEGAL_DRAFTING_SYNONYMS: Dict[str, List[str]] = {
    # Document types
    "contract": ["agreement", "compact", "pact", "covenant", "accord", "understanding", "deal", "arrangement"],
    "deed": ["conveyance", "instrument of transfer", "grant deed", "title transfer"],
    "lease": ["rental agreement", "tenancy agreement", "letting", "demise", "lease agreement"],
    "mortgage": ["deed of trust", "security instrument", "encumbrance", "lien instrument"],
    "promissory_note": ["note", "IOU", "debt instrument", "negotiable instrument", "loan note"],
    "trust": ["trust agreement", "trust instrument", "declaration of trust", "trust deed", "indenture"],
    "will": ["last will and testament", "testament", "testamentary instrument"],
    "power_of_attorney": ["POA", "proxy", "letter of attorney", "mandate"],
    "bylaws": ["by-laws", "articles of association", "operating rules", "governing rules"],
    "articles_of_incorporation": ["charter", "certificate of incorporation", "articles of organization"],
    "operating_agreement": ["LLC agreement", "company agreement", "member agreement"],
    "nda": ["non-disclosure agreement", "confidentiality agreement", "secrecy agreement", "proprietary information agreement"],

    # Clause types
    "indemnification": ["indemnity", "hold harmless", "save harmless", "indemnify and defend"],
    "limitation_of_liability": ["liability cap", "damage limitation", "liability limitation", "cap on damages"],
    "force_majeure": ["act of god", "unforeseeable circumstances", "impossibility", "impracticability", "frustration of purpose"],
    "severability": ["savings clause", "separability", "blue pencil", "reformation clause"],
    "entire_agreement": ["integration clause", "merger clause", "zipper clause", "whole agreement"],
    "governing_law": ["choice of law", "applicable law", "governing jurisdiction", "law selection"],
    "dispute_resolution": ["arbitration clause", "mediation clause", "ADR", "forum selection"],
    "assignment": ["transfer", "delegation", "novation", "assumption"],
    "termination": ["expiration", "cancellation", "rescission", "revocation"],
    "waiver": ["release", "relinquishment", "estoppel", "forfeiture of rights"],
    "amendment": ["modification", "change", "alteration", "supplement", "addendum"],
    "counterparts": ["duplicate originals", "multiple copies", "execution copies"],
    "survival": ["post-termination obligations", "surviving provisions", "continuing obligations"],
    "representations": ["reps and warranties", "warranties", "representations and warranties", "covenants of fact"],
    "confidentiality": ["secrecy", "non-disclosure", "proprietary information", "trade secrets"],
    "non_compete": ["restrictive covenant", "covenant not to compete", "competition restriction", "non-competition"],
    "non_solicitation": ["anti-solicitation", "no-hire", "employee non-solicitation", "customer non-solicitation"],

    # Legal concepts
    "consideration": ["quid pro quo", "bargained-for exchange", "mutual obligation", "value exchanged"],
    "breach": ["default", "violation", "non-compliance", "failure to perform", "material breach"],
    "remedy": ["relief", "damages", "cure", "specific performance", "injunctive relief"],
    "jurisdiction": ["venue", "forum", "court selection", "applicable forum"],
    "party": ["contracting party", "signatory", "counterparty", "participant", "principal"],
    "recital": ["whereas clause", "preamble", "background", "preliminary statement"],
    "term": ["duration", "period", "tenure", "effective period", "contract period"],
    "renewal": ["extension", "continuation", "prolongation", "evergreen", "auto-renewal"],
    "notice": ["notification", "written notice", "formal notice", "service of notice"],
    "default": ["event of default", "breach", "non-performance", "failure to pay", "acceleration event"],
    "closing": ["settlement", "completion", "consummation", "execution date"],
    "escrow": ["trust account", "holdback", "security deposit", "custodial account"],
    "lien": ["encumbrance", "charge", "security interest", "pledge", "hypothecation"],
    "conveyance": ["transfer of title", "grant", "alienation", "passing of title"],
    "easement": ["right of way", "servitude", "privilege", "license over land"],
    "subordination": ["junior lien", "second position", "lower priority", "subordinate interest"],
}

DOCUMENT_TYPE_PATTERNS: Dict[str, List[str]] = {
    "sales_agreement": [r"sale\s+of\s+goods", r"purchase\s+agreement", r"buy\s+sell", r"bill\s+of\s+sale", r"sales\s+contract"],
    "service_agreement": [r"services?\s+agreement", r"consulting\s+agreement", r"professional\s+services", r"master\s+service"],
    "license_agreement": [r"licens[ec]\s+agreement", r"software\s+license", r"end\s*user\s+license", r"EULA", r"patent\s+license"],
    "employment_agreement": [r"employment\s+(agreement|contract)", r"offer\s+letter", r"hiring\s+agreement", r"at.will\s+employment"],
    "lease_agreement": [r"lease\s+agreement", r"rental\s+agreement", r"tenancy", r"commercial\s+lease", r"residential\s+lease"],
    "nda": [r"non.?disclosure", r"confidentiality\s+agreement", r"NDA", r"secrecy\s+agreement", r"proprietary\s+info"],
    "operating_agreement": [r"operating\s+agreement", r"LLC\s+agreement", r"member\s+agreement", r"company\s+agreement"],
    "shareholder_agreement": [r"shareholder", r"stockholder", r"equity\s+holders?", r"stock\s+purchase"],
    "merger_agreement": [r"merger", r"acquisition", r"M\s*&\s*A", r"combination\s+agreement", r"consolidation"],
    "promissory_note": [r"promissory\s+note", r"loan\s+agreement", r"debt\s+instrument", r"note\s+payable"],
    "deed": [r"warranty\s+deed", r"quitclaim", r"grant\s+deed", r"deed\s+of\s+trust", r"conveyance"],
    "trust": [r"trust\s+(agreement|instrument|declaration)", r"revocable\s+trust", r"irrevocable\s+trust", r"living\s+trust"],
    "will": [r"last\s+will", r"testament", r"testamentary", r"bequeath", r"devise"],
    "power_of_attorney": [r"power\s+of\s+attorney", r"POA", r"durable\s+power", r"limited\s+power"],
    "bylaws": [r"bylaws?", r"by.laws?", r"articles\s+of\s+association", r"governing\s+rules"],
    "articles_of_incorporation": [r"articles?\s+of\s+incorporation", r"certificate\s+of\s+incorporation", r"charter", r"articles?\s+of\s+organization"],
    "non_compete": [r"non.?compet[ei]", r"restrictive\s+covenant", r"covenant\s+not\s+to\s+compete"],
    "privacy_policy": [r"privacy\s+policy", r"data\s+protection", r"GDPR", r"CCPA", r"personal\s+data"],
    "terms_of_service": [r"terms\s+of\s+service", r"terms\s+of\s+use", r"TOS", r"user\s+agreement", r"website\s+terms"],
}

JURISDICTION_PATTERNS: Dict[str, List[str]] = {
    "TX": [r"\bTexas\b", r"\bTX\b", r"Lone\s+Star", r"Tex\.\s+Bus", r"Tex\.\s+Prop"],
    "CA": [r"\bCalifornia\b", r"\bCA\b", r"Cal\.\s+Civ", r"Cal\.\s+Bus"],
    "NY": [r"\bNew\s+York\b", r"\bNY\b", r"N\.Y\.\s+Gen", r"N\.Y\.\s+Bus"],
    "DE": [r"\bDelaware\b", r"\bDE\b", r"Del\.\s+Code", r"DGCL"],
    "FL": [r"\bFlorida\b", r"\bFL\b", r"Fla\.\s+Stat"],
    "IL": [r"\bIllinois\b", r"\bIL\b", r"ILCS"],
    "NV": [r"\bNevada\b", r"\bNV\b", r"Nev\.\s+Rev"],
    "WA": [r"\bWashington\b", r"\bWA\b", r"Wash\.\s+Rev"],
    "PA": [r"\bPennsylvania\b", r"\bPA\b", r"Pa\.\s+Cons"],
    "OH": [r"\bOhio\b", r"\bOH\b", r"Ohio\s+Rev"],
    "GA": [r"\bGeorgia\b", r"\bGA\b", r"Ga\.\s+Code"],
    "MA": [r"\bMassachusetts\b", r"\bMA\b", r"Mass\.\s+Gen"],
    "CO": [r"\bColorado\b", r"\bCO\b", r"Colo\.\s+Rev"],
    "NJ": [r"\bNew\s+Jersey\b", r"\bNJ\b", r"N\.J\.\s+Stat"],
    "federal": [r"\bfederal\b", r"\bUnited\s+States\b", r"\bU\.S\.C\.", r"\bCFR\b"],
}

CLAUSE_CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "definitions": ["defined terms", "definitions", "means", "shall mean", "as used herein"],
    "representations_warranties": ["represents", "warrants", "representation", "warranty", "covenants of fact"],
    "covenants": ["covenant", "obligation", "undertaking", "promise", "shall"],
    "conditions_precedent": ["condition precedent", "subject to", "contingency", "prerequisite", "unless"],
    "indemnification": ["indemnify", "hold harmless", "indemnification", "indemnitor", "indemnitee"],
    "limitation_of_liability": ["liability cap", "limitation of liability", "consequential damages", "aggregate liability"],
    "confidentiality": ["confidential", "proprietary", "trade secret", "non-disclosure", "confidential information"],
    "non_compete": ["non-compete", "restrictive covenant", "competition", "competitive activity"],
    "non_solicitation": ["non-solicitation", "solicit", "hire", "recruit", "entice"],
    "intellectual_property": ["intellectual property", "patent", "trademark", "copyright", "trade secret", "IP rights"],
    "termination": ["termination", "expiration", "cancel", "rescind", "terminate"],
    "dispute_resolution": ["dispute", "arbitration", "mediation", "litigation", "forum", "venue"],
    "governing_law": ["governing law", "choice of law", "applicable law", "governed by"],
    "force_majeure": ["force majeure", "act of god", "unforeseeable", "impossibility", "impracticability"],
    "assignment": ["assignment", "transfer", "delegate", "assignable", "successor"],
    "notices": ["notice", "notification", "written notice", "email notice", "certified mail"],
    "severability": ["severability", "severable", "invalid provision", "blue pencil", "reformation"],
    "entire_agreement": ["entire agreement", "integration", "merger clause", "supersedes"],
    "amendment": ["amendment", "modification", "written consent", "supplement", "addendum"],
    "waiver": ["waiver", "waive", "relinquish", "estoppel", "forfeiture"],
    "counterparts": ["counterparts", "duplicate", "execution copies", "electronic signature"],
    "survival": ["survival", "surviving provisions", "post-termination", "continue in effect"],
    "insurance": ["insurance", "coverage", "policy", "premium", "insured"],
    "compliance_with_laws": ["compliance", "applicable law", "regulation", "statute", "ordinance"],
}

LEGAL_STOPWORDS: FrozenSet[str] = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "must",
    "it", "its", "this", "that", "these", "those", "such", "any", "all",
    "each", "every", "some", "no", "not", "only", "than", "so", "very",
    "just", "about", "above", "after", "again", "between", "into", "through",
    "during", "before", "under", "over", "here", "there", "where", "when",
    "who", "whom", "which", "what", "how", "if", "then", "because", "while",
})

DOMAIN_KEYWORD_MAP: Dict[str, DocumentDomain] = {
    "contract": DocumentDomain.CONTRACT,
    "agreement": DocumentDomain.CONTRACT,
    "sale": DocumentDomain.CONTRACT,
    "purchase": DocumentDomain.CONTRACT,
    "service": DocumentDomain.CONTRACT,
    "license": DocumentDomain.CONTRACT,
    "deed": DocumentDomain.REAL_ESTATE,
    "mortgage": DocumentDomain.REAL_ESTATE,
    "property": DocumentDomain.REAL_ESTATE,
    "lease": DocumentDomain.REAL_ESTATE,
    "easement": DocumentDomain.REAL_ESTATE,
    "conveyance": DocumentDomain.REAL_ESTATE,
    "title": DocumentDomain.REAL_ESTATE,
    "employment": DocumentDomain.EMPLOYMENT,
    "employee": DocumentDomain.EMPLOYMENT,
    "hire": DocumentDomain.EMPLOYMENT,
    "severance": DocumentDomain.EMPLOYMENT,
    "compensation": DocumentDomain.EMPLOYMENT,
    "corporate": DocumentDomain.CORPORATE,
    "bylaws": DocumentDomain.CORPORATE,
    "shareholder": DocumentDomain.CORPORATE,
    "board": DocumentDomain.CORPORATE,
    "resolution": DocumentDomain.CORPORATE,
    "merger": DocumentDomain.CORPORATE,
    "incorporation": DocumentDomain.CORPORATE,
    "patent": DocumentDomain.INTELLECTUAL_PROPERTY,
    "trademark": DocumentDomain.INTELLECTUAL_PROPERTY,
    "copyright": DocumentDomain.INTELLECTUAL_PROPERTY,
    "trade secret": DocumentDomain.INTELLECTUAL_PROPERTY,
    "loan": DocumentDomain.FINANCE,
    "promissory": DocumentDomain.FINANCE,
    "security interest": DocumentDomain.FINANCE,
    "guaranty": DocumentDomain.FINANCE,
    "trust": DocumentDomain.ESTATE_PLANNING,
    "will": DocumentDomain.ESTATE_PLANNING,
    "estate": DocumentDomain.ESTATE_PLANNING,
    "beneficiary": DocumentDomain.ESTATE_PLANNING,
    "power of attorney": DocumentDomain.ESTATE_PLANNING,
    "compliance": DocumentDomain.REGULATORY,
    "privacy": DocumentDomain.REGULATORY,
    "regulation": DocumentDomain.REGULATORY,
    "GDPR": DocumentDomain.REGULATORY,
    "terms of service": DocumentDomain.REGULATORY,
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class NormalizationResult(BaseModel):
    """Result of normalizing a user query into canonical legal drafting terms."""

    original_query: str
    normalized_query: str
    detected_domain: DocumentDomain = DocumentDomain.GENERAL
    detected_document_type: str = ""
    detected_jurisdiction: str = ""
    detected_clause_categories: List[str] = Field(default_factory=list)
    canonical_terms: List[str] = Field(default_factory=list)
    synonym_expansions: Dict[str, List[str]] = Field(default_factory=dict)
    tokens: List[str] = Field(default_factory=list)
    token_count: int = 0
    confidence: float = 0.0
    normalization_time_ms: float = 0.0
    query_hash: str = ""


class SemanticMapEntry(BaseModel):
    """A single entry in the semantic map."""

    canonical_term: str
    synonyms: List[str] = Field(default_factory=list)
    domain: DocumentDomain = DocumentDomain.GENERAL
    clause_category: str = ""
    description: str = ""
    weight: float = 1.0


class GovernanceMetadata(BaseModel):
    """Metadata about the semantic dictionary governance."""

    version: str = _SEMANTIC_MAP_VERSION
    build_date: str = _SEMANTIC_MAP_BUILD_DATE
    total_canonical_terms: int = 0
    total_synonyms: int = 0
    total_domains: int = 0
    dictionary_hash: str = ""
    last_validated: str = ""


# ============================================================================
# TOKENIZER
# ============================================================================


def _tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase terms, removing legal stopwords."""
    cleaned = re.sub(r"[^\w\s\-\.]", " ", text.lower())
    tokens = cleaned.split()
    return [t.strip("-. ") for t in tokens if t.strip("-. ") and t not in LEGAL_STOPWORDS and len(t) >= 2]


def _bigrams(tokens: List[str]) -> List[str]:
    """Generate bigrams from token list."""
    return [f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)]


def _trigrams(tokens: List[str]) -> List[str]:
    """Generate trigrams from token list."""
    return [f"{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}" for i in range(len(tokens) - 2)]


# ============================================================================
# CORE NORMALIZATION FUNCTIONS
# ============================================================================


def normalize_query(query: str) -> NormalizationResult:
    """
    Normalize a user query into canonical legal drafting terminology.

    Steps:
        1. Tokenize the input
        2. Detect document domain
        3. Detect specific document type
        4. Detect jurisdiction
        5. Detect relevant clause categories
        6. Expand synonyms to canonical terms
        7. Compute confidence score
    """
    start_time = time.time()

    tokens = _tokenize(query)
    bigram_tokens = _bigrams(tokens)
    trigram_tokens = _trigrams(tokens)
    all_ngrams = tokens + bigram_tokens + trigram_tokens

    # Detect domain
    domain = _detect_domain(query, tokens, bigram_tokens)

    # Detect document type
    doc_type = _detect_document_type(query)

    # Detect jurisdiction
    jurisdiction = _detect_jurisdiction(query)

    # Detect clause categories
    clause_cats = _detect_clause_categories(query, tokens, bigram_tokens)

    # Expand synonyms
    canonical_terms, expansions = _expand_synonyms(tokens, bigram_tokens)

    # Build normalized query
    normalized_parts = list(canonical_terms)
    if doc_type:
        normalized_parts.insert(0, doc_type)
    if jurisdiction:
        normalized_parts.append(f"jurisdiction:{jurisdiction}")
    normalized_query = " ".join(normalized_parts) if normalized_parts else query.lower().strip()

    # Compute confidence
    confidence = _compute_normalization_confidence(
        tokens=tokens,
        domain=domain,
        doc_type=doc_type,
        jurisdiction=jurisdiction,
        clause_cats=clause_cats,
        canonical_terms=canonical_terms,
    )

    query_hash = hashlib.sha256(query.encode("utf-8")).hexdigest()[:16]
    elapsed_ms = (time.time() - start_time) * 1000.0

    result = NormalizationResult(
        original_query=query,
        normalized_query=normalized_query,
        detected_domain=domain,
        detected_document_type=doc_type,
        detected_jurisdiction=jurisdiction,
        detected_clause_categories=clause_cats,
        canonical_terms=list(canonical_terms),
        synonym_expansions=expansions,
        tokens=tokens,
        token_count=len(tokens),
        confidence=round(confidence, 4),
        normalization_time_ms=round(elapsed_ms, 2),
        query_hash=query_hash,
    )

    logger.debug(
        "Normalized query | domain={} type={} jurisdiction={} confidence={:.2f} time={:.1f}ms",
        domain.value,
        doc_type,
        jurisdiction,
        confidence,
        elapsed_ms,
    )

    return result


def _detect_domain(query: str, tokens: List[str], bigrams: List[str]) -> DocumentDomain:
    """Detect the primary document domain from query content."""
    domain_scores: Dict[DocumentDomain, float] = defaultdict(float)
    query_lower = query.lower()

    for keyword, domain in DOMAIN_KEYWORD_MAP.items():
        if keyword in query_lower:
            domain_scores[domain] += 2.0
        for token in tokens:
            if keyword in token:
                domain_scores[domain] += 1.0
        for bg in bigrams:
            if keyword in bg:
                domain_scores[domain] += 1.5

    if not domain_scores:
        return DocumentDomain.GENERAL

    best_domain = max(domain_scores, key=lambda d: domain_scores[d])
    if domain_scores[best_domain] < 1.0:
        return DocumentDomain.GENERAL
    return best_domain


def _detect_document_type(query: str) -> str:
    """Detect specific document type from query patterns."""
    query_lower = query.lower()
    best_match = ""
    best_score = 0

    for doc_type, patterns in DOCUMENT_TYPE_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = re.findall(pattern, query_lower, re.IGNORECASE)
            score += len(matches) * 2
        if score > best_score:
            best_score = score
            best_match = doc_type

    return best_match if best_score >= 2 else ""


def _detect_jurisdiction(query: str) -> str:
    """Detect jurisdiction from query content."""
    for jurisdiction, patterns in JURISDICTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return jurisdiction
    return ""


def _detect_clause_categories(query: str, tokens: List[str], bigrams: List[str]) -> List[str]:
    """Detect which clause categories are relevant to the query."""
    query_lower = query.lower()
    detected: List[str] = []

    for category, keywords in CLAUSE_CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in query_lower:
                if category not in detected:
                    detected.append(category)
                break

    return detected


def _expand_synonyms(tokens: List[str], bigrams: List[str]) -> Tuple[Set[str], Dict[str, List[str]]]:
    """Expand query tokens to canonical legal terms via synonym lookup."""
    canonical: Set[str] = set()
    expansions: Dict[str, List[str]] = {}

    reverse_map: Dict[str, str] = {}
    for canonical_term, synonyms in LEGAL_DRAFTING_SYNONYMS.items():
        for syn in synonyms:
            reverse_map[syn.lower()] = canonical_term
        reverse_map[canonical_term.lower()] = canonical_term

    all_terms = tokens + bigrams
    for term in all_terms:
        term_lower = term.lower()
        if term_lower in reverse_map:
            canon = reverse_map[term_lower]
            canonical.add(canon)
            if canon not in expansions:
                expansions[canon] = LEGAL_DRAFTING_SYNONYMS.get(canon, [])

    return canonical, expansions


def _compute_normalization_confidence(
    tokens: List[str],
    domain: DocumentDomain,
    doc_type: str,
    jurisdiction: str,
    clause_cats: List[str],
    canonical_terms: Set[str],
) -> float:
    """Compute confidence score for the normalization result."""
    score = 0.0

    if domain != DocumentDomain.GENERAL:
        score += 0.25
    if doc_type:
        score += 0.25
    if jurisdiction:
        score += 0.15
    if clause_cats:
        score += min(0.15, len(clause_cats) * 0.05)
    if canonical_terms:
        term_ratio = len(canonical_terms) / max(len(tokens), 1)
        score += min(0.20, term_ratio * 0.20)

    return min(1.0, score)


# ============================================================================
# SEMANTIC MAP ACCESS
# ============================================================================


def get_semantic_map() -> Dict[str, SemanticMapEntry]:
    """Get the full semantic map as a dictionary of canonical terms."""
    result: Dict[str, SemanticMapEntry] = {}

    for canonical_term, synonyms in LEGAL_DRAFTING_SYNONYMS.items():
        domain = DocumentDomain.GENERAL
        for kw, dom in DOMAIN_KEYWORD_MAP.items():
            if kw in canonical_term or canonical_term in kw:
                domain = dom
                break

        clause_cat = ""
        for cat, keywords in CLAUSE_CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if canonical_term.replace("_", " ") in kw or kw in canonical_term.replace("_", " "):
                    clause_cat = cat
                    break
            if clause_cat:
                break

        result[canonical_term] = SemanticMapEntry(
            canonical_term=canonical_term,
            synonyms=synonyms,
            domain=domain,
            clause_category=clause_cat,
        )

    return result


def get_governance_metadata() -> GovernanceMetadata:
    """Get governance metadata about the semantic dictionary."""
    sem_map = get_semantic_map()
    total_synonyms = sum(len(entry.synonyms) for entry in sem_map.values())
    domains_used = set(entry.domain for entry in sem_map.values())

    dict_content = json.dumps(
        {k: v.model_dump() for k, v in sorted(sem_map.items())},
        sort_keys=True,
    )
    dict_hash = hashlib.sha256(dict_content.encode("utf-8")).hexdigest()

    return GovernanceMetadata(
        version=_SEMANTIC_MAP_VERSION,
        build_date=_SEMANTIC_MAP_BUILD_DATE,
        total_canonical_terms=len(sem_map),
        total_synonyms=total_synonyms,
        total_domains=len(domains_used),
        dictionary_hash=dict_hash,
        last_validated=datetime.now(timezone.utc).isoformat(),
    )


def get_semantic_map_version() -> str:
    """Return the semantic map version string."""
    return _SEMANTIC_MAP_VERSION


def get_semantic_map_hash() -> str:
    """Compute and return the SHA-256 hash of the semantic map."""
    return get_governance_metadata().dictionary_hash


def verify_dictionary_integrity() -> Tuple[bool, str]:
    """Verify internal consistency of the semantic dictionary."""
    issues: List[str] = []

    for term, synonyms in LEGAL_DRAFTING_SYNONYMS.items():
        if not synonyms:
            issues.append(f"Empty synonym list for '{term}'")
        if not isinstance(synonyms, list):
            issues.append(f"Synonyms for '{term}' is not a list")
        for syn in synonyms:
            if not syn.strip():
                issues.append(f"Blank synonym in '{term}'")

    for doc_type, patterns in DOCUMENT_TYPE_PATTERNS.items():
        for p in patterns:
            try:
                re.compile(p)
            except re.error as exc:
                issues.append(f"Invalid regex in DOCUMENT_TYPE_PATTERNS['{doc_type}']: {exc}")

    for jur, patterns in JURISDICTION_PATTERNS.items():
        for p in patterns:
            try:
                re.compile(p)
            except re.error as exc:
                issues.append(f"Invalid regex in JURISDICTION_PATTERNS['{jur}']: {exc}")

    if issues:
        return False, "; ".join(issues)
    return True, "Dictionary integrity verified"


def get_document_type_patterns() -> Dict[str, List[str]]:
    """Return the document type detection patterns."""
    return dict(DOCUMENT_TYPE_PATTERNS)


def get_jurisdiction_patterns() -> Dict[str, List[str]]:
    """Return the jurisdiction detection patterns."""
    return dict(JURISDICTION_PATTERNS)


def get_clause_category_keywords() -> Dict[str, List[str]]:
    """Return the clause category keyword map."""
    return dict(CLAUSE_CATEGORY_KEYWORDS)


# ============================================================================
# UTILITY IMPORTS FOR ENGINE
# ============================================================================

import json  # noqa: E402 (already imported above, re-export for clarity)
