"""
LM11 Lease Negotiation Engine — Semantic Normalization Layer
Deterministic term normalization for oil and gas lease negotiation domain.

Architecture:
    This is a PREPROCESSING layer. It must remain deterministic.
    No vector inference. No embeddings. No auto-learning.
    Pure dictionary-based canonical form resolution.

Author: ECHO OMEGA PRIME
Engine: LM11 Lease Negotiation
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger

# ==============================================================================
# CONSTANTS
# ==============================================================================

ENGINE_ID = "LM11"
NORMALIZATION_VERSION = "1.0.0"


# ==============================================================================
# NORMALIZATION RESULT
# ==============================================================================

class NormalizationConfidence(str, Enum):
    """Confidence level of a normalization mapping."""
    EXACT = "exact"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    UNMAPPED = "unmapped"


@dataclass
class NormalizationResult:
    """Result of semantic normalization on a query."""
    original_text: str
    normalized_text: str
    canonical_terms: List[str]
    mappings_applied: List[Dict[str, str]]
    confidence: NormalizationConfidence
    domain_signals: List[str]
    lease_type_detected: Optional[str] = None
    basin_context: Optional[str] = None
    party_role: Optional[str] = None
    normalization_hash: str = ""

    def __post_init__(self) -> None:
        content = f"{self.normalized_text}|{'|'.join(self.canonical_terms)}"
        self.normalization_hash = hashlib.sha256(content.encode()).hexdigest()[:16]


# ==============================================================================
# SEMANTIC DICTIONARY — OIL & GAS LEASE NEGOTIATION
# ==============================================================================

# Canonical term mappings: variant -> canonical form
LEASE_TERM_SYNONYMS: Dict[str, str] = {
    # Royalty clause variants
    "royalty": "royalty_clause",
    "royalty rate": "royalty_clause",
    "royalty interest": "royalty_clause",
    "landowner royalty": "royalty_clause",
    "lessor royalty": "royalty_clause",
    "overriding royalty": "overriding_royalty_interest",
    "orri": "overriding_royalty_interest",
    "override": "overriding_royalty_interest",
    "cost-free royalty": "cost_free_royalty",
    "free of cost royalty": "cost_free_royalty",
    "royalty free of costs": "cost_free_royalty",
    "net royalty": "net_royalty",
    "gross royalty": "gross_royalty",
    "market value royalty": "market_value_royalty",
    "proceeds royalty": "proceeds_royalty",
    "amount realized": "proceeds_royalty",
    "at the well": "at_wellhead_valuation",
    "wellhead": "at_wellhead_valuation",
    "at the wellhead": "at_wellhead_valuation",
    "one-eighth": "royalty_one_eighth",
    "1/8": "royalty_one_eighth",
    "12.5%": "royalty_one_eighth",
    "one-fifth": "royalty_one_fifth",
    "1/5": "royalty_one_fifth",
    "20%": "royalty_one_fifth",
    "one-fourth": "royalty_one_fourth",
    "1/4": "royalty_one_fourth",
    "25%": "royalty_one_fourth",
    "three-sixteenths": "royalty_three_sixteenths",
    "3/16": "royalty_three_sixteenths",
    "18.75%": "royalty_three_sixteenths",

    # Bonus and consideration
    "bonus": "bonus_consideration",
    "lease bonus": "bonus_consideration",
    "signing bonus": "bonus_consideration",
    "bonus per acre": "bonus_consideration",
    "delay rental": "delay_rental",
    "delay rentals": "delay_rental",
    "annual delay rental": "delay_rental",
    "paid-up lease": "paid_up_lease",
    "paid up lease": "paid_up_lease",
    "paid up": "paid_up_lease",
    "no delay rentals": "paid_up_lease",

    # Primary term and habendum
    "primary term": "primary_term",
    "initial term": "primary_term",
    "lease term": "primary_term",
    "exploration period": "primary_term",
    "habendum": "habendum_clause",
    "habendum clause": "habendum_clause",
    "granting clause": "granting_clause",
    "so long thereafter": "habendum_production_language",
    "secondary term": "habendum_production_language",
    "held by production": "held_by_production",
    "hbp": "held_by_production",

    # Drilling and development
    "continuous drilling": "continuous_drilling_clause",
    "continuous development": "continuous_development_clause",
    "cdc": "continuous_drilling_clause",
    "drill or release": "continuous_drilling_clause",
    "commencement of drilling": "commencement_definition",
    "spud": "commencement_definition",
    "spudding": "commencement_definition",
    "operations clause": "operations_clause",
    "substitute operations": "operations_clause",
    "reworking": "operations_clause",
    "workover": "operations_clause",

    # Pugh clause
    "pugh clause": "pugh_clause",
    "pugh": "pugh_clause",
    "freestone rider": "pugh_clause",
    "depth severance": "vertical_pugh",
    "vertical pugh": "vertical_pugh",
    "horizontal pugh": "horizontal_pugh",
    "acreage release": "horizontal_pugh",

    # Surface use
    "surface use": "surface_use_provisions",
    "surface damage": "surface_damage_payment",
    "surface damages": "surface_damage_payment",
    "surface restoration": "surface_restoration",
    "location restrictions": "location_restrictions",
    "no surface operations": "no_surface_operations",
    "surface waiver": "surface_waiver",
    "accommodation doctrine": "accommodation_doctrine",

    # Pooling and unitization
    "pooling": "pooling_clause",
    "pooling clause": "pooling_clause",
    "unitization": "unitization_clause",
    "unit": "unitization_clause",
    "force pooling": "force_pooling",
    "forced pooling": "force_pooling",
    "compulsory pooling": "force_pooling",
    "community lease": "community_lease",
    "voluntary pooling": "voluntary_pooling",
    "pooling declaration": "pooling_declaration",
    "proration unit": "proration_unit",
    "spacing unit": "spacing_unit",

    # Shut-in
    "shut-in": "shut_in_royalty",
    "shut in": "shut_in_royalty",
    "shut-in royalty": "shut_in_royalty",
    "shut in royalty": "shut_in_royalty",
    "shut-in well": "shut_in_royalty",
    "capable of producing": "capable_of_production",

    # Cessation of production
    "cessation": "cessation_of_production",
    "cessation of production": "cessation_of_production",
    "temporary cessation": "temporary_cessation",
    "sixty-day clause": "cessation_savings_clause",
    "90-day clause": "cessation_savings_clause",
    "savings clause": "cessation_savings_clause",

    # Depth limitations
    "depth limitation": "depth_limitation",
    "depth clause": "depth_limitation",
    "shallow rights": "shallow_rights",
    "deep rights": "deep_rights_reservation",
    "deep rights reservation": "deep_rights_reservation",
    "retained acreage": "retained_acreage",

    # Release
    "release": "release_provisions",
    "partial release": "partial_release",
    "surrender clause": "surrender_clause",
    "termination": "lease_termination",
    "expiration": "lease_expiration",

    # Assignment
    "assignment": "assignment_clause",
    "assignment restriction": "assignment_restrictions",
    "consent to assign": "consent_requirement",
    "rofr": "right_of_first_refusal",
    "right of first refusal": "right_of_first_refusal",
    "change of operator": "change_of_operator",

    # Environmental
    "environmental": "environmental_indemnification",
    "environmental indemnity": "environmental_indemnification",
    "indemnification": "environmental_indemnification",
    "environmental liability": "environmental_indemnification",
    "plugging obligation": "plugging_obligation",
    "well plugging": "plugging_obligation",
    "site remediation": "site_remediation",

    # Audit and records
    "audit": "audit_rights",
    "audit rights": "audit_rights",
    "records access": "records_access",
    "books and records": "records_access",
    "accounting": "accounting_provisions",

    # Top lease
    "top lease": "top_lease",
    "top leasing": "top_lease",
    "bottom lease": "bottom_lease",

    # Amendments and extensions
    "amendment": "lease_amendment",
    "lease amendment": "lease_amendment",
    "extension": "lease_extension",
    "lease extension": "lease_extension",
    "ratification": "lease_ratification",
    "renewal": "lease_renewal",

    # Market enhancement
    "market enhancement": "market_enhancement_clause",
    "enhancement clause": "market_enhancement_clause",
    "marketing clause": "marketing_clause",
    "take-or-pay": "take_or_pay",
    "gas balancing": "gas_balancing",
    "gas storage": "gas_storage_rights",

    # Party roles
    "lessor": "lessor",
    "mineral owner": "lessor",
    "landowner": "lessor",
    "lessee": "lessee",
    "operator": "lessee",
    "oil company": "lessee",
    "working interest owner": "working_interest_owner",
    "wio": "working_interest_owner",
    "non-operating interest": "non_operating_interest",
    "nopwi": "non_operating_interest",

    # Lease types
    "oil and gas lease": "oil_gas_lease",
    "mineral lease": "oil_gas_lease",
    "producers 88": "producers_88_lease",
    "producers 88 lease": "producers_88_lease",
    "cabot form": "cabot_oil_gas_lease",
    "aapl form": "aapl_form_lease",
    "federal lease": "federal_lease",
    "state lease": "state_lease",
    "indian lease": "indian_lease",
}

# Domain signal keywords
DOMAIN_SIGNALS: Dict[str, List[str]] = {
    "royalty_negotiation": [
        "royalty", "fraction", "cost-free", "market value", "proceeds",
        "deductions", "post-production costs", "gross", "net",
    ],
    "bonus_negotiation": [
        "bonus", "per acre", "signing", "delay rental", "paid-up",
        "consideration", "cash bonus",
    ],
    "term_negotiation": [
        "primary term", "years", "habendum", "secondary term", "hbp",
        "held by production", "expiration",
    ],
    "drilling_obligations": [
        "continuous drilling", "development", "commencement", "spud",
        "operations", "reworking", "workover",
    ],
    "pugh_negotiation": [
        "pugh", "depth severance", "vertical", "horizontal",
        "acreage release", "retained acreage",
    ],
    "surface_negotiation": [
        "surface", "damage", "restoration", "location", "accommodation",
        "surface owner", "site access",
    ],
    "pooling_negotiation": [
        "pooling", "unitization", "force pooling", "community lease",
        "spacing", "proration",
    ],
    "cessation_negotiation": [
        "cessation", "shut-in", "temporary", "sixty-day", "savings clause",
        "capable of producing",
    ],
    "assignment_negotiation": [
        "assignment", "transfer", "consent", "rofr", "change of operator",
    ],
    "environmental_negotiation": [
        "environmental", "indemnity", "plugging", "remediation",
        "liability", "contamination",
    ],
    "top_lease_strategy": [
        "top lease", "expiring lease", "renewal", "extension",
        "replacement lease",
    ],
}

# Basin-specific context detection
BASIN_KEYWORDS: Dict[str, List[str]] = {
    "permian_midland": [
        "midland basin", "midland", "spraberry", "wolfcamp", "martin county",
        "howard county", "reagan county", "upton county", "glasscock",
    ],
    "permian_delaware": [
        "delaware basin", "delaware", "bone spring", "wolfcamp",
        "reeves county", "loving county", "ward county", "pecos county",
        "culberson county",
    ],
    "eagle_ford": [
        "eagle ford", "south texas", "dimmit county", "la salle county",
        "webb county", "karnes county", "dewitt county",
    ],
    "haynesville": [
        "haynesville", "bossier", "north louisiana", "east texas",
        "caddo parish", "desoto parish", "harrison county",
    ],
    "marcellus": [
        "marcellus", "appalachian", "pennsylvania", "west virginia",
        "susquehanna county", "bradford county", "greene county",
    ],
    "bakken": [
        "bakken", "williston basin", "north dakota", "montana",
        "mckenzie county", "williams county", "mountrail county",
    ],
    "scoop_stack": [
        "scoop", "stack", "merge", "oklahoma", "blaine county",
        "canadian county", "grady county", "kingfisher county",
    ],
}

# Party role detection
PARTY_ROLE_KEYWORDS: Dict[str, List[str]] = {
    "lessor": [
        "mineral owner", "landowner", "lessor", "royalty owner",
        "surface owner rights", "mineral interest holder",
    ],
    "lessee": [
        "lessee", "operator", "oil company", "exploration company",
        "working interest", "drilling company",
    ],
    "landman": [
        "landman", "land professional", "title examiner", "lease broker",
        "lease acquisition", "lease negotiator",
    ],
}


# ==============================================================================
# NORMALIZATION ENGINE
# ==============================================================================

class SemanticNormalizer:
    """
    Deterministic semantic normalizer for oil and gas lease negotiation terms.

    Responsibilities:
    - Map variant terminology to canonical forms
    - Detect domain signals (what area of lease negotiation)
    - Identify basin context from geographic references
    - Detect party role perspective
    - Produce deterministic normalization hash
    """

    def __init__(self) -> None:
        self._synonym_map: Dict[str, str] = dict(LEASE_TERM_SYNONYMS)
        self._compiled_patterns: List[Tuple[re.Pattern, str]] = []
        self._build_compiled_patterns()
        logger.info(
            f"SemanticNormalizer initialized: {len(self._synonym_map)} mappings, "
            f"{len(self._compiled_patterns)} compiled patterns"
        )

    def _build_compiled_patterns(self) -> None:
        """Pre-compile regex patterns for multi-word synonyms, longest first."""
        sorted_keys = sorted(self._synonym_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            if " " in key or "-" in key:
                pattern = re.compile(r"\b" + re.escape(key) + r"\b", re.IGNORECASE)
                self._compiled_patterns.append((pattern, self._synonym_map[key]))

    def normalize(self, text: str) -> NormalizationResult:
        """
        Normalize input text to canonical lease negotiation terminology.

        Steps:
        1. Lowercase and clean input
        2. Apply multi-word pattern replacements (longest first)
        3. Apply single-word synonym replacements
        4. Detect domain signals
        5. Detect basin context
        6. Detect party role perspective
        7. Compute normalization hash
        """
        original = text
        cleaned = text.lower().strip()
        canonical_terms: List[str] = []
        mappings: List[Dict[str, str]] = []

        # Step 1: Multi-word pattern replacements
        normalized = cleaned
        for pattern, canonical in self._compiled_patterns:
            match = pattern.search(normalized)
            if match:
                canonical_terms.append(canonical)
                mappings.append({"from": match.group(), "to": canonical})
                normalized = pattern.sub(canonical, normalized)

        # Step 2: Single-word synonym check for remaining words
        words = normalized.split()
        result_words = []
        for word in words:
            clean_word = re.sub(r"[^\w/-]", "", word)
            if clean_word in self._synonym_map and clean_word not in canonical_terms:
                canon = self._synonym_map[clean_word]
                if canon not in canonical_terms:
                    canonical_terms.append(canon)
                    mappings.append({"from": clean_word, "to": canon})
                result_words.append(canon)
            else:
                result_words.append(word)
        normalized = " ".join(result_words)

        # Step 3: Detect domain signals
        domain_signals = self._detect_domain_signals(cleaned)

        # Step 4: Detect basin context
        basin_context = self._detect_basin(cleaned)

        # Step 5: Detect party role
        party_role = self._detect_party_role(cleaned)

        # Step 6: Detect lease type
        lease_type = self._detect_lease_type(cleaned)

        # Step 7: Compute confidence
        confidence = self._assess_confidence(canonical_terms, mappings, domain_signals)

        return NormalizationResult(
            original_text=original,
            normalized_text=normalized,
            canonical_terms=canonical_terms,
            mappings_applied=mappings,
            confidence=confidence,
            domain_signals=domain_signals,
            lease_type_detected=lease_type,
            basin_context=basin_context,
            party_role=party_role,
        )

    def _detect_domain_signals(self, text: str) -> List[str]:
        """Detect which negotiation domains are relevant."""
        detected: List[str] = []
        for domain, keywords in DOMAIN_SIGNALS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score >= 1:
                detected.append(domain)
        return detected

    def _detect_basin(self, text: str) -> Optional[str]:
        """Detect basin context from geographic references."""
        best_basin: Optional[str] = None
        best_score = 0
        for basin, keywords in BASIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_basin = basin
        return best_basin if best_score > 0 else None

    def _detect_party_role(self, text: str) -> Optional[str]:
        """Detect the perspective/role of the querying party."""
        best_role: Optional[str] = None
        best_score = 0
        for role, keywords in PARTY_ROLE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_role = role
        return best_role if best_score > 0 else None

    def _detect_lease_type(self, text: str) -> Optional[str]:
        """Detect specific lease form type."""
        lease_forms = {
            "producers_88": ["producers 88", "producers88", "p88"],
            "aapl_form": ["aapl", "aapl form", "aapl 610"],
            "federal_lease": ["federal lease", "blm lease", "federal oil"],
            "state_lease": ["state lease", "glo lease", "university lands"],
            "cabot_form": ["cabot form", "cabot oil"],
        }
        for form_type, keywords in lease_forms.items():
            for kw in keywords:
                if kw in text:
                    return form_type
        return None

    def _assess_confidence(
        self,
        canonical_terms: List[str],
        mappings: List[Dict[str, str]],
        domain_signals: List[str],
    ) -> NormalizationConfidence:
        """Assess confidence of the normalization result."""
        if len(canonical_terms) >= 3 and len(domain_signals) >= 2:
            return NormalizationConfidence.EXACT
        if len(canonical_terms) >= 2 or len(domain_signals) >= 2:
            return NormalizationConfidence.STRONG
        if len(canonical_terms) >= 1 or len(domain_signals) >= 1:
            return NormalizationConfidence.MODERATE
        if mappings:
            return NormalizationConfidence.WEAK
        return NormalizationConfidence.UNMAPPED

    def get_canonical_term(self, variant: str) -> Optional[str]:
        """Look up canonical form for a single variant term."""
        return self._synonym_map.get(variant.lower().strip())

    def get_all_variants(self, canonical: str) -> List[str]:
        """Get all known variants that map to a canonical term."""
        return [k for k, v in self._synonym_map.items() if v == canonical]

    def get_stats(self) -> Dict[str, Any]:
        """Return normalizer statistics."""
        canonical_set = set(self._synonym_map.values())
        return {
            "total_mappings": len(self._synonym_map),
            "unique_canonical_terms": len(canonical_set),
            "compiled_patterns": len(self._compiled_patterns),
            "domain_signal_categories": len(DOMAIN_SIGNALS),
            "basin_contexts": len(BASIN_KEYWORDS),
            "party_roles": len(PARTY_ROLE_KEYWORDS),
            "version": NORMALIZATION_VERSION,
        }


# ==============================================================================
# MODULE-LEVEL CONVENIENCE
# ==============================================================================

_normalizer: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get or create the semantic normalizer singleton."""
    global _normalizer
    if _normalizer is None:
        _normalizer = SemanticNormalizer()
    return _normalizer


def normalize_semantics(text: str) -> NormalizationResult:
    """Normalize query text using the lease negotiation semantic dictionary."""
    return get_normalizer().normalize(text)
