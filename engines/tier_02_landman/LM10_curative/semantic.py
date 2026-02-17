"""
LM10 Curative Engine — Semantic Normalization Module
=====================================================
Domain-specific term normalization for curative title work.
Deterministic mapping of natural language variations to canonical
terms used in the doctrine cache and authority sources.

Engine: LM10 | Port: 8510 | Domain: title_curative
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID = "LM10"

# ---------------------------------------------------------------------------
# Canonical Term Mappings
# ---------------------------------------------------------------------------
# Maps natural language variations to canonical curative terms.
# Each key is the canonical term; values are known synonyms/variants.

CURATIVE_TERM_MAPPINGS: dict[str, list[str]] = {
    "affidavit_of_heirship": [
        "heirship affidavit", "affidavit of heirship", "heir affidavit",
        "declaration of heirship", "proof of heirship", "heirship proof",
        "determination of heirship", "affidavit establishing heirship",
        "sworn statement of heirship", "heirship declaration",
        "heir at law affidavit", "intestate heirship",
    ],
    "probate_independent_administration": [
        "independent administration", "independent executor",
        "independent executrix", "independent admin",
        "tex est code 401", "section 401",
        "unsupervised administration", "independent probate",
    ],
    "probate_dependent_administration": [
        "dependent administration", "supervised administration",
        "dependent executor", "court supervised probate",
        "managed administration", "dependent probate",
    ],
    "muniment_of_title": [
        "muniment of title", "muniment", "probate as muniment",
        "will as muniment", "muniment proceeding",
        "tex est code 257", "section 257",
    ],
    "small_estate_affidavit": [
        "small estate affidavit", "small estate", "sea",
        "tex est code 205", "section 205",
        "simplified probate", "small estate proceeding",
    ],
    "correction_deed": [
        "correction deed", "corrective deed", "deed of correction",
        "amended deed", "corrected deed", "reforming deed",
        "tex prop code 5.028", "tex prop code 5.029",
    ],
    "scriveners_affidavit": [
        "scrivener's affidavit", "scriveners affidavit",
        "clerical error affidavit", "drafting error affidavit",
        "typographical error affidavit", "scrivener affidavit",
        "correction affidavit", "material variance affidavit",
    ],
    "quiet_title_action": [
        "quiet title", "trespass to try title", "suit to quiet title",
        "action to quiet title", "trespass try title",
        "tex civ prac rem 22", "tex prop code 22",
        "declaratory judgment title",
    ],
    "adverse_possession": [
        "adverse possession", "squatters rights", "prescriptive title",
        "limitation title", "hostile possession", "open notorious",
        "continuous possession", "tex civ prac rem 16",
        "five year adverse", "ten year adverse", "twenty five year adverse",
        "5 year limitation", "10 year limitation", "25 year limitation",
    ],
    "tax_sale_curative": [
        "tax sale", "tax deed", "tax lien foreclosure",
        "redemption period", "tax sale redemption",
        "void tax sale", "voidable tax sale",
        "tax code chapter 34", "constable sale",
        "delinquent tax judgment",
    ],
    "lien_release": [
        "lien release", "release of lien", "satisfaction of lien",
        "mechanics lien release", "materialman lien release",
        "abstract of judgment release", "release of abstract",
        "expired lien", "stale lien", "lien expiration",
        "dormant lien",
    ],
    "ratification": [
        "ratification", "ratification deed", "ratification agreement",
        "ratification of conveyance", "confirmation deed",
        "ratify prior deed", "confirm prior conveyance",
    ],
    "stipulation_of_interest": [
        "stipulation of interest", "stipulated interest",
        "agreed interest allocation", "interest stipulation",
        "division order stipulation",
    ],
    "pooling_amendment": [
        "pooling amendment", "pooling designation amendment",
        "amended pooling", "unit amendment", "unitization amendment",
        "spacing amendment", "pooling modification",
        "tex nat res code 102",
    ],
    "dormant_mineral_interest": [
        "dormant mineral interest", "dormant mineral act",
        "mineral interest pooling act", "mipa",
        "tex nat res code 75", "abandoned mineral interest",
        "unused mineral interest", "lapsed mineral interest",
    ],
    "chain_of_title_gap": [
        "gap in chain", "chain of title gap", "title gap",
        "missing link", "broken chain", "chain break",
        "title deficiency", "wild deed", "stranger to title",
    ],
    "boundary_dispute": [
        "boundary dispute", "boundary line dispute", "survey conflict",
        "fence line dispute", "encroachment", "boundary agreement",
        "agreed boundary", "boundary by acquiescence",
    ],
    "name_variation_affidavit": [
        "name variation", "name affidavit", "aka affidavit",
        "also known as", "maiden name", "name change",
        "identity affidavit", "same person affidavit",
        "misspelled name", "name discrepancy",
    ],
    "entity_authority": [
        "entity authority", "corporate resolution", "llc authorization",
        "partnership authority", "corporate authority",
        "authority to convey", "certificate of authority",
        "good standing", "certificate of existence",
        "foreign entity registration",
    ],
    "lis_pendens": [
        "lis pendens", "notice of lis pendens", "pending litigation",
        "notice of pending action", "lis pendens release",
        "expunction of lis pendens", "tex prop code 12.007",
    ],
    "foreclosure_curative": [
        "foreclosure curative", "defective foreclosure",
        "foreclosure notice defect", "wrong party foreclosure",
        "substitute trustee", "defective trustee sale",
        "tex prop code 51", "power of sale defect",
    ],
    "abstract_of_judgment": [
        "abstract of judgment", "judgment lien", "judgment release",
        "expired judgment", "dormant judgment",
        "tex civ prac rem 34", "tex prop code 52",
    ],
    "mineral_estate_reunification": [
        "mineral reunification", "severed mineral estate",
        "surface mineral reunification", "estate merger",
        "mineral estate merger", "rejoinder of estates",
    ],
    "missing_instrument": [
        "missing instrument", "lost deed", "destroyed document",
        "unrecorded conveyance", "missing recorded document",
        "reconstructed instrument", "secondary evidence",
    ],
}


# ---------------------------------------------------------------------------
# Issue Category Classification
# ---------------------------------------------------------------------------
CATEGORY_KEYWORD_MAP: dict[str, list[str]] = {
    "HEIRSHIP": [
        "heir", "heirship", "intestate", "decedent", "died without will",
        "declaration of heirship", "family history", "genealogy",
    ],
    "PROBATE": [
        "probate", "executor", "executrix", "administrator",
        "personal representative", "will", "estate", "testate",
        "muniment", "small estate",
    ],
    "CORRECTION_INSTRUMENTS": [
        "correction", "corrective", "scrivener", "typo", "clerical",
        "reformation", "reformed", "amended deed", "typographical",
    ],
    "QUIET_TITLE": [
        "quiet title", "trespass try title", "declaratory judgment",
        "cloud on title", "suit to remove", "clear title",
    ],
    "MISSING_INSTRUMENTS": [
        "missing", "lost deed", "destroyed", "unrecorded",
        "reconstruct", "secondary evidence",
    ],
    "LIEN_RELEASE": [
        "lien release", "mechanics lien", "materialman", "expired lien",
        "satisfaction", "discharge", "release of lien",
    ],
    "RATIFICATION": [
        "ratification", "ratify", "confirm", "confirmation deed",
    ],
    "STIPULATION": [
        "stipulation", "stipulated interest", "agreed interest",
    ],
    "POOLING_AMENDMENTS": [
        "pooling", "unit", "unitization", "spacing", "pooling amendment",
    ],
    "TAX_SALE_CURATIVE": [
        "tax sale", "tax deed", "redemption", "tax lien",
        "delinquent tax", "void tax", "voidable",
    ],
    "ADVERSE_POSSESSION": [
        "adverse possession", "prescriptive", "limitation",
        "hostile possession", "squatter",
    ],
    "DORMANT_MINERALS": [
        "dormant mineral", "abandoned mineral", "mineral pooling act",
        "mipa", "lapsed mineral",
    ],
    "GAP_RESOLUTION": [
        "gap", "chain gap", "broken chain", "wild deed", "stranger",
    ],
    "BOUNDARY_DISPUTES": [
        "boundary", "survey", "encroachment", "fence line",
        "agreed boundary",
    ],
    "ESTATE_REUNIFICATION": [
        "reunification", "severed estate", "mineral estate merger",
        "surface mineral", "rejoinder",
    ],
    "JUDGMENT_RESOLUTION": [
        "abstract of judgment", "judgment lien", "expired judgment",
        "dormant judgment",
    ],
    "LIS_PENDENS": [
        "lis pendens", "pending litigation", "pending action",
        "expunction",
    ],
    "FORECLOSURE_CURATIVE": [
        "foreclosure", "trustee sale", "substitute trustee",
        "power of sale", "defective notice",
    ],
    "NAME_VARIATIONS": [
        "name variation", "aka", "maiden name", "name change",
        "misspelling", "identity",
    ],
    "ENTITY_AUTHORITY": [
        "entity authority", "corporate resolution", "llc authorization",
        "partnership", "good standing", "certificate of existence",
    ],
}


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------
class NormalizationResult(BaseModel):
    """Result of semantic normalization."""
    original_text: str
    normalized_text: str
    canonical_terms: list[str] = Field(default_factory=list)
    detected_categories: list[str] = Field(default_factory=list)
    primary_category: str = ""
    term_mappings: dict[str, str] = Field(default_factory=dict)
    confidence: float = 0.0
    normalization_hash: str = ""


class TermMatch(BaseModel):
    """A matched canonical term."""
    canonical: str
    matched_phrase: str
    position: int = 0
    context: str = ""


# ---------------------------------------------------------------------------
# Semantic Normalizer
# ---------------------------------------------------------------------------
class SemanticNormalizer:
    """
    Normalizes curative title queries into canonical terms and categories.
    Deterministic — same input always produces same output.
    """

    def __init__(self) -> None:
        self._term_map = CURATIVE_TERM_MAPPINGS
        self._category_map = CATEGORY_KEYWORD_MAP
        self._reverse_map: dict[str, str] = {}
        self._build_reverse_map()
        logger.info(
            "SemanticNormalizer initialized | terms={} | categories={}",
            len(self._term_map),
            len(self._category_map),
        )

    def _build_reverse_map(self) -> None:
        """Build reverse lookup from variant to canonical term."""
        for canonical, variants in self._term_map.items():
            for variant in variants:
                self._reverse_map[variant.lower().strip()] = canonical

    def normalize(self, text: str) -> NormalizationResult:
        """
        Normalize a query text into canonical curative terms.

        Steps:
        1. Lowercase and strip
        2. Match known term variants
        3. Classify into issue categories
        4. Compute determinism hash
        """
        original = text
        lower_text = text.lower().strip()
        normalized_parts: list[str] = []
        canonical_terms: list[str] = []
        term_mappings: dict[str, str] = {}

        # Match known variants
        matched_phrases: set[str] = set()
        for variant, canonical in sorted(
            self._reverse_map.items(), key=lambda x: len(x[0]), reverse=True
        ):
            if variant in lower_text and variant not in matched_phrases:
                canonical_terms.append(canonical)
                term_mappings[variant] = canonical
                matched_phrases.add(variant)
                lower_text = lower_text.replace(variant, canonical)

        # Deduplicate canonical terms while preserving order
        seen: set[str] = set()
        unique_terms: list[str] = []
        for term in canonical_terms:
            if term not in seen:
                unique_terms.append(term)
                seen.add(term)
        canonical_terms = unique_terms

        # Detect categories
        detected_categories = self._classify_categories(original.lower())
        primary_category = detected_categories[0] if detected_categories else ""

        # Confidence based on match density
        word_count = len(original.split())
        matched_word_count = sum(len(v.split()) for v in matched_phrases)
        confidence = min(1.0, matched_word_count / max(word_count, 1))

        # Normalized text
        normalized_text = lower_text.strip()

        # Determinism hash
        hash_input = f"{original}|{','.join(canonical_terms)}|{','.join(detected_categories)}"
        normalization_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        result = NormalizationResult(
            original_text=original,
            normalized_text=normalized_text,
            canonical_terms=canonical_terms,
            detected_categories=detected_categories,
            primary_category=primary_category,
            term_mappings=term_mappings,
            confidence=round(confidence, 4),
            normalization_hash=normalization_hash,
        )

        logger.debug(
            "Normalized | terms={} | categories={} | confidence={:.2f}",
            len(canonical_terms),
            detected_categories,
            confidence,
        )
        return result

    def _classify_categories(self, text: str) -> list[str]:
        """Classify text into issue categories by keyword density."""
        scores: dict[str, float] = defaultdict(float)
        for category, keywords in self._category_map.items():
            for keyword in keywords:
                if keyword in text:
                    weight = len(keyword.split())
                    scores[category] += weight

        sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, score in sorted_categories if score > 0]

    def get_canonical_term(self, phrase: str) -> Optional[str]:
        """Look up a single phrase in the reverse map."""
        return self._reverse_map.get(phrase.lower().strip())

    def get_all_variants(self, canonical_term: str) -> list[str]:
        """Get all known variants for a canonical term."""
        return self._term_map.get(canonical_term, [])

    def get_category_keywords(self, category: str) -> list[str]:
        """Get keywords for a specific category."""
        return self._category_map.get(category, [])

    def extract_statutory_references(self, text: str) -> list[dict[str, str]]:
        """Extract Texas statutory references from text."""
        refs: list[dict[str, str]] = []
        patterns = [
            (r"tex(?:as)?\s+(?:prop(?:erty)?)\s+code\s+(?:sec(?:tion)?\s*)?(\d+[\.\d]*)", "Texas Property Code"),
            (r"tex(?:as)?\s+(?:est(?:ates)?)\s+code\s+(?:sec(?:tion)?\s*)?(\d+[\.\d]*)", "Texas Estates Code"),
            (r"tex(?:as)?\s+(?:nat(?:ural)?\s+res(?:ources)?)\s+code\s+(?:sec(?:tion)?\s*)?(\d+[\.\d]*)", "Texas Natural Resources Code"),
            (r"tex(?:as)?\s+(?:civ(?:il)?\s+prac(?:tice)?\s+(?:and\s+)?rem(?:edies)?)\s+(?:code\s+)?(?:sec(?:tion)?\s*)?(\d+[\.\d]*)", "Texas Civil Practice and Remedies Code"),
            (r"tex(?:as)?\s+(?:bus(?:iness)?\s+org(?:anizations)?)\s+code\s+(?:sec(?:tion)?\s*)?(\d+[\.\d]*)", "Texas Business Organizations Code"),
            (r"tex(?:as)?\s+tax\s+code\s+(?:sec(?:tion)?\s*)?(\d+[\.\d]*)", "Texas Tax Code"),
            (r"section\s+(\d+[\.\d]*)", "Unspecified Code"),
        ]
        lower = text.lower()
        for pattern, code_name in patterns:
            for match in re.finditer(pattern, lower):
                refs.append({
                    "code": code_name,
                    "section": match.group(1),
                    "raw_match": match.group(0),
                })
        return refs

    def get_stats(self) -> dict[str, Any]:
        """Get normalizer statistics."""
        total_variants = sum(len(v) for v in self._term_map.values())
        return {
            "canonical_terms": len(self._term_map),
            "total_variants": total_variants,
            "categories": len(self._category_map),
            "reverse_map_entries": len(self._reverse_map),
        }


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
_normalizer: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get or create the singleton normalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = SemanticNormalizer()
    return _normalizer


def reset_normalizer() -> None:
    """Reset the singleton (for testing)."""
    global _normalizer
    _normalizer = None
