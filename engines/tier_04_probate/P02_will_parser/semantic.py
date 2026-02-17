"""
SEMANTIC NORMALIZATION LAYER — Will Construction Domain

Deterministic term mapping for will parsing and estate planning.
NO VECTOR INFERENCE. NO PROBABILISTIC MODELS. NO AUTO-LEARNING.

Purpose: Normalize will construction terminology to canonical doctrine terms
Domain: Testamentary devises, probate, estate planning, Texas Estates Code
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Optional


@dataclass
class NormalizationResult:
    """Result of semantic normalization."""
    original_query: str
    normalized_query: str
    mapped_terms: Dict[str, str]
    domain_concepts: List[str]
    confidence: float


# ==============================================================================
# WILL EXECUTION AND FORMALITIES TERMS
# ==============================================================================

WILL_EXECUTION_TERMS = {
    # Execution formalities
    "attested will": ["witnessed will", "formal will", "§251.051", "two witness will"],
    "holographic will": ["handwritten will", "unwitnessed will", "§251.052", "holograph"],
    "self-proving affidavit": ["self-proving", "§251.104", "notarized attestation", "affidavit"],
    "witnesses": ["attestation", "attesting witnesses", "credible witnesses", "subscribing witnesses"],
    "testator presence": ["line of sight", "conscious presence", "presence test"],
    "signature": ["execution", "signing", "testator signature", "mark"],

    # Will types
    "nuncupative will": ["oral will", "deathbed will", "spoken will"],
    "codicil": ["amendment", "will modification", "supplement"],
    "mutual will": ["reciprocal will", "joint will", "contractual will"],

    # Capacity and validity
    "testamentary capacity": ["sound mind", "mental capacity", "competency", "§251.001"],
    "undue influence": ["coercion", "manipulation", "overreaching", "fraud"],
    "lucid interval": ["temporary clarity", "momentary capacity"],
    "confidential relationship": ["fiduciary relationship", "trust relationship", "dominant influence"],
}

# ==============================================================================
# DEVISE CLASSIFICATION TERMS
# ==============================================================================

DEVISE_CLASSIFICATION_TERMS = {
    # Types of devises
    "specific devise": ["specific bequest", "specific legacy", "particular property"],
    "general devise": ["general legacy", "pecuniary bequest", "cash gift"],
    "demonstrative devise": ["demonstrative legacy", "specified source gift"],
    "residuary devise": ["residuary clause", "rest and remainder", "residue"],

    # Related concepts
    "ademption": ["ademption by extinction", "§255.151", "failed specific devise"],
    "abatement": ["reduction", "priority of payment", "§355.109"],
    "lapse": ["failed gift", "predeceased beneficiary", "void devise"],
    "anti-lapse": ["§255.153", "substitute gift", "lapse prevention"],

    # Property interests
    "fee simple": ["absolute ownership", "fee simple absolute", "complete ownership"],
    "life estate": ["life tenancy", "estate for life", "life interest"],
    "remainder": ["future interest", "remainder interest", "vested remainder"],
    "reversion": ["reversionary interest", "estate reversion"],
}

# ==============================================================================
# WILL CONSTRUCTION AND INTERPRETATION TERMS
# ==============================================================================

CONSTRUCTION_TERMS = {
    # Beneficiary classifications
    "class gift": ["group gift", "collective devise", "class bequest"],
    "per stirpes": ["by representation", "by roots", "by stocks"],
    "per capita": ["by heads", "equal shares", "share and share alike"],
    "natural objects of bounty": ["natural heirs", "expected beneficiaries", "family members"],

    # Construction doctrines
    "testator's intent": ["testamentary intent", "donor's intent", "will maker's purpose"],
    "plain meaning": ["ordinary meaning", "common understanding", "clear language"],
    "four corners": ["intrinsic evidence", "within the will", "document itself"],
    "extrinsic evidence": ["parol evidence", "outside evidence", "external facts"],
    "ambiguity": ["uncertainty", "unclear provision", "conflicting terms"],
    "latent ambiguity": ["hidden ambiguity", "undiscoverable from will face"],
    "patent ambiguity": ["apparent ambiguity", "obvious from will face"],

    # Special provisions
    "power of appointment": ["donee power", "appointive power", "§181.001"],
    "general power": ["general power of appointment", "unlimited power"],
    "special power": ["limited power", "special power of appointment", "restricted power"],
    "in terrorem clause": ["no-contest clause", "forfeiture clause", "§254.005"],
}

# ==============================================================================
# WILL REVOCATION AND MODIFICATION TERMS
# ==============================================================================

REVOCATION_TERMS = {
    # Revocation methods
    "revocation": ["cancellation", "voiding", "nullification", "§253.002"],
    "express revocation": ["explicit revocation", "stated revocation"],
    "implied revocation": ["revocation by inconsistency", "constructive revocation"],
    "physical act": ["destruction", "cancellation by act", "§253.002(b)"],
    "subsequent writing": ["later will", "new will", "revoking instrument"],

    # Related doctrines
    "revival": ["§253.004", "restoration", "renewed validity"],
    "dependent relative revocation": ["DRR", "conditional revocation", "mistaken revocation"],
    "republication": ["re-execution", "codicil republication", "renewal"],

    # Partial revocation
    "partial revocation": ["limited revocation", "specific provision revocation"],
    "interlineation": ["handwritten changes", "marginal notations"],
}

# ==============================================================================
# PROBATE AND CONTEST TERMS
# ==============================================================================

PROBATE_TERMS = {
    # Will contests
    "will contest": ["will challenge", "§256.201", "probate contest"],
    "lack of capacity": ["mental incompetence", "unsound mind", "incapacity"],
    "fraud": ["misrepresentation", "deceit", "fraudulent procurement"],
    "mistake": ["error", "drafting mistake", "§255.451 reformation"],
    "duress": ["compulsion", "coercion", "threat"],

    # Probate procedures
    "muniment of title": ["§257.12A", "simplified probate", "will as title"],
    "independent administration": ["§401", "minimal court supervision"],
    "dependent administration": ["court-supervised", "regular administration"],
    "small estate affidavit": ["§205", "affidavit of heirship", "no probate"],

    # Estate administration
    "personal representative": ["executor", "administrator", "estate representative"],
    "letters testamentary": ["executor authority", "probate letters"],
    "inventory": ["estate inventory", "§309", "asset listing"],
    "accounting": ["estate accounting", "§360", "financial report"],
}

# ==============================================================================
# TEXAS ESTATES CODE SECTION REFERENCES
# ==============================================================================

STATUTE_REFERENCES = {
    "§251.051": ["attested will requirements", "formal will execution"],
    "§251.052": ["holographic will", "handwritten will requirements"],
    "§251.104": ["self-proving affidavit", "notarized attestation"],
    "§253.002": ["will revocation", "revocation by writing or act"],
    "§253.004": ["revival of revoked will"],
    "§255.151": ["ademption by extinction"],
    "§255.153": ["anti-lapse statute", "substitute gift to descendants"],
    "§255.154": ["failed residuary devise"],
    "§255.451": ["reformation for mistake"],
    "§256.201": ["will contest grounds"],
    "§254.005": ["no-contest clause enforceability"],
    "§355.109": ["abatement order"],
}

# ==============================================================================
# ENTITY AND BENEFICIARY TERMS
# ==============================================================================

ENTITY_TERMS = {
    # Family relationships
    "spouse": ["husband", "wife", "surviving spouse", "widow", "widower"],
    "children": ["issue", "offspring", "descendants", "kids"],
    "descendants": ["lineal descendants", "issue", "posterity"],
    "heirs": ["intestate heirs", "legal heirs", "successors"],
    "ancestors": ["ascendants", "forebears", "lineal ascendants"],
    "collaterals": ["siblings", "nieces", "nephews", "cousins"],

    # Estate planning entities
    "trust": ["testamentary trust", "will trust", "trust created by will"],
    "trustee": ["trust administrator", "fiduciary"],
    "beneficiary": ["devisee", "legatee", "donee", "recipient"],
    "guardian": ["conservator", "custodian", "estate guardian"],

    # Property types
    "real property": ["real estate", "land", "realty", "immovable property"],
    "personal property": ["personalty", "chattels", "movable property"],
    "community property": ["marital property", "community estate"],
    "separate property": ["individual property", "sole property"],
}


# ==============================================================================
# NORMALIZATION ENGINE
# ==============================================================================

def normalize_semantics(query: str) -> NormalizationResult:
    """
    Normalize will construction query to canonical doctrine terminology.

    This is a deterministic mapping. No ML. No embeddings. No auto-learning.
    """
    original_query = query
    normalized_query = query.lower()
    mapped_terms: Dict[str, str] = {}
    domain_concepts: Set[str] = set()

    # Combine all term dictionaries
    all_term_maps = {
        **WILL_EXECUTION_TERMS,
        **DEVISE_CLASSIFICATION_TERMS,
        **CONSTRUCTION_TERMS,
        **REVOCATION_TERMS,
        **PROBATE_TERMS,
        **STATUTE_REFERENCES,
        **ENTITY_TERMS,
    }

    # Map colloquial terms to canonical terms
    for canonical, variants in all_term_maps.items():
        for variant in variants:
            if variant.lower() in normalized_query:
                normalized_query = normalized_query.replace(variant.lower(), canonical)
                mapped_terms[variant] = canonical
                domain_concepts.add(canonical)

    # Extract domain concepts from canonical terms appearing in query
    for canonical in all_term_maps.keys():
        if canonical.lower() in normalized_query:
            domain_concepts.add(canonical)

    # Calculate confidence (higher if more terms mapped)
    confidence = min(1.0, 0.6 + (len(mapped_terms) * 0.1))

    return NormalizationResult(
        original_query=original_query,
        normalized_query=normalized_query,
        mapped_terms=mapped_terms,
        domain_concepts=sorted(list(domain_concepts)),
        confidence=confidence
    )


def get_related_concepts(concept: str) -> List[str]:
    """Get related canonical concepts for a given term."""
    concept_lower = concept.lower()
    related: Set[str] = set()

    all_term_maps = {
        **WILL_EXECUTION_TERMS,
        **DEVISE_CLASSIFICATION_TERMS,
        **CONSTRUCTION_TERMS,
        **REVOCATION_TERMS,
        **PROBATE_TERMS,
        **STATUTE_REFERENCES,
        **ENTITY_TERMS,
    }

    # Find canonical term
    canonical = None
    for canon, variants in all_term_maps.items():
        if concept_lower == canon.lower() or concept_lower in [v.lower() for v in variants]:
            canonical = canon
            break

    if not canonical:
        return []

    # Add all variants of the canonical term
    if canonical in all_term_maps:
        related.update(all_term_maps[canonical])

    return sorted(list(related))


def extract_statute_references(query: str) -> List[str]:
    """Extract Texas Estates Code section references from query."""
    import re
    # Match §XXX.XXX or Section XXX.XXX patterns
    pattern = r'§\s*(\d{3}\.\d{3})'
    matches = re.findall(pattern, query)
    return [f"§{match}" for match in matches]
