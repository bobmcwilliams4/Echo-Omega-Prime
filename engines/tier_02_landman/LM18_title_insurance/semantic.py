"""
LM18 Title Insurance Engine — Semantic Normalization
====================================================
Domain-specific term normalization for title insurance analysis.
Ensures consistent terminology and phrase standardization.

Engine: LM18 | Port: 8518 | Domain: title_insurance
Version: 1.0.0 | TIE Gold Standard Component 6
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class NormalizationResult:
    """Result of semantic normalization."""
    original: str
    normalized: str
    terms_replaced: dict[str, str]
    confidence: float


class SemanticNormalizer:
    """Normalize title insurance terminology for consistent analysis."""

    def __init__(self):
        """Initialize normalizer with title insurance term mappings."""

        # Policy type normalization
        self.policy_type_map = {
            r"\b(owner'?s? policy|owner policy|op)\b": "owner's policy",
            r"\b(lender'?s? policy|loan policy|mortgagee policy|lp)\b": "lender's policy",
            r"\b(leasehold policy|leasehold title insurance)\b": "leasehold policy",
            r"\b(homeowner'?s? policy|alta homeowner)\b": "homeowner's policy",
        }

        # Commitment/policy section normalization
        self.section_map = {
            r"\b(schedule a|sched a|sch a)\b": "Schedule A",
            r"\b(schedule b-i|sched b-1|sch b1|schedule b1)\b": "Schedule B-I",
            r"\b(schedule b-ii|sched b-2|sch b2|schedule b2|schedule b part 2)\b": "Schedule B-II",
            r"\b(schedule b|sched b|sch b)\b": "Schedule B",
        }

        # Estate/interest normalization
        self.estate_map = {
            r"\b(fee simple|fee|fee simple absolute)\b": "fee simple",
            r"\b(leasehold|leasehold estate|leasehold interest)\b": "leasehold",
            r"\b(easement|easement interest)\b": "easement",
            r"\b(mineral estate|mineral interest|minerals)\b": "mineral estate",
            r"\b(surface estate|surface rights|surface)\b": "surface estate",
            r"\b(royalty interest|royalty|npri|non-participating royalty)\b": "royalty interest",
        }

        # Lien type normalization
        self.lien_map = {
            r"\b(deed of trust|dot|trust deed)\b": "deed of trust",
            r"\b(mortgage|mtg)\b": "mortgage",
            r"\b(mechanic'?s? lien|materialman'?s? lien|construction lien|m&m lien)\b": "mechanic's lien",
            r"\b(judgment lien|abstract of judgment)\b": "judgment lien",
            r"\b(tax lien|property tax lien|ad valorem lien)\b": "tax lien",
            r"\b(federal tax lien|irs lien|nftl)\b": "federal tax lien",
            r"\b(hoa lien|homeowner'?s? association lien|assessment lien)\b": "HOA lien",
            r"\b(ucc lien|ucc filing|ucc-1)\b": "UCC lien",
        }

        # Endorsement normalization
        self.endorsement_map = {
            r"\b(alta 2|alta 2\.0|access endorsement)\b": "ALTA 2 Access",
            r"\b(alta 3\.1|zoning endorsement)\b": "ALTA 3.1 Zoning",
            r"\b(alta 4\.1|condominium endorsement)\b": "ALTA 4.1 Condominium",
            r"\b(alta 5\.1|pud endorsement)\b": "ALTA 5.1 PUD",
            r"\b(alta 6\.2|variable rate mortgage)\b": "ALTA 6.2 Variable Rate",
            r"\b(alta 8\.1|environmental protection|environmental lien)\b": "ALTA 8.1 Environmental",
            r"\b(alta 9|comprehensive|restrictions encroachments)\b": "ALTA 9 Comprehensive",
            r"\b(alta 19|contiguity endorsement)\b": "ALTA 19 Contiguity",
            r"\b(alta 22|location endorsement)\b": "ALTA 22 Location",
        }

        # Defect type normalization
        self.defect_map = {
            r"\b(wild deed|stranger to title)\b": "wild deed",
            r"\b(forged deed|forged signature|forgery)\b": "forged deed",
            r"\b(gap in title|missing deed|chain gap)\b": "gap in title",
            r"\b(heirship issue|missing heir|probate defect)\b": "heirship defect",
            r"\b(entity authority|lack of authority|corporate authority)\b": "entity authority defect",
            r"\b(improper acknowledgment|defective notary|notary defect)\b": "improper acknowledgment",
            r"\b(encroachment|boundary dispute)\b": "encroachment",
            r"\b(adverse possession|ap claim)\b": "adverse possession",
        }

        # Authority/source normalization
        self.authority_map = {
            r"\b(texas insurance code|tic)\b": "Texas Insurance Code",
            r"\b(tdi|texas department of insurance)\b": "Texas Department of Insurance",
            r"\b(alta|american land title association)\b": "ALTA",
            r"\b(tlta|texas land title association)\b": "TLTA",
            r"\b(texas property code|tpc)\b": "Texas Property Code",
            r"\b(texas estates code|tec)\b": "Texas Estates Code",
        }

        # Combined map for single-pass normalization
        self.combined_map = {}
        self.combined_map.update(self.policy_type_map)
        self.combined_map.update(self.section_map)
        self.combined_map.update(self.estate_map)
        self.combined_map.update(self.lien_map)
        self.combined_map.update(self.endorsement_map)
        self.combined_map.update(self.defect_map)
        self.combined_map.update(self.authority_map)

    def normalize(self, text: str) -> NormalizationResult:
        """
        Normalize title insurance terminology in text.

        Args:
            text: Input text with potentially non-standard terminology

        Returns:
            NormalizationResult with normalized text and replacement tracking
        """
        original = text
        normalized = text.lower()
        terms_replaced = {}

        # Apply all normalization rules
        for pattern, replacement in self.combined_map.items():
            matches = re.finditer(pattern, normalized, re.IGNORECASE)
            for match in matches:
                original_term = match.group(0)
                if original_term.lower() != replacement.lower():
                    terms_replaced[original_term] = replacement
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

        # Calculate confidence based on number of normalizations
        confidence = 1.0 if not terms_replaced else max(0.85, 1.0 - (len(terms_replaced) * 0.02))

        return NormalizationResult(
            original=original,
            normalized=normalized,
            terms_replaced=terms_replaced,
            confidence=confidence
        )

    def normalize_phrase(self, phrase: str) -> str:
        """Normalize a phrase and return only normalized text."""
        result = self.normalize(phrase)
        return result.normalized

    def extract_policy_type(self, text: str) -> Optional[str]:
        """Extract policy type from text."""
        text_lower = text.lower()
        for pattern, normalized in self.policy_type_map.items():
            if re.search(pattern, text_lower):
                return normalized
        return None

    def extract_schedule_section(self, text: str) -> Optional[str]:
        """Extract schedule section from text."""
        text_lower = text.lower()
        for pattern, normalized in self.section_map.items():
            if re.search(pattern, text_lower):
                return normalized
        return None

    def extract_estate_type(self, text: str) -> Optional[str]:
        """Extract estate/interest type from text."""
        text_lower = text.lower()
        for pattern, normalized in self.estate_map.items():
            if re.search(pattern, text_lower):
                return normalized
        return None

    def extract_lien_type(self, text: str) -> Optional[str]:
        """Extract lien type from text."""
        text_lower = text.lower()
        for pattern, normalized in self.lien_map.items():
            if re.search(pattern, text_lower):
                return normalized
        return None

    def extract_endorsements(self, text: str) -> list[str]:
        """Extract all endorsement types from text."""
        text_lower = text.lower()
        found = []
        for pattern, normalized in self.endorsement_map.items():
            if re.search(pattern, text_lower):
                found.append(normalized)
        return found

    def extract_defects(self, text: str) -> list[str]:
        """Extract all defect types from text."""
        text_lower = text.lower()
        found = []
        for pattern, normalized in self.defect_map.items():
            if re.search(pattern, text_lower):
                found.append(normalized)
        return found

    def is_mineral_related(self, text: str) -> bool:
        """Check if text relates to mineral rights/interests."""
        mineral_indicators = [
            "mineral", "royalty", "npri", "oil", "gas", "subsurface",
            "executive rights", "mineral estate", "surface estate"
        ]
        text_lower = text.lower()
        return any(ind in text_lower for ind in mineral_indicators)

    def is_lien_related(self, text: str) -> bool:
        """Check if text relates to liens."""
        lien_indicators = [
            "lien", "mortgage", "deed of trust", "encumbrance",
            "judgment", "mechanic", "tax lien", "priority"
        ]
        text_lower = text.lower()
        return any(ind in text_lower for ind in lien_indicators)

    def is_survey_related(self, text: str) -> bool:
        """Check if text relates to surveys or boundaries."""
        survey_indicators = [
            "survey", "boundary", "encroachment", "easement",
            "metes and bounds", "legal description", "plat",
            "alta survey", "shortage in area"
        ]
        text_lower = text.lower()
        return any(ind in text_lower for ind in survey_indicators)


# ===================================================================
# Global Normalizer Instance
# ===================================================================

_NORMALIZER: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get global normalizer instance (singleton)."""
    global _NORMALIZER
    if _NORMALIZER is None:
        _NORMALIZER = SemanticNormalizer()
    return _NORMALIZER


def normalize_text(text: str) -> NormalizationResult:
    """Normalize text using global normalizer."""
    normalizer = get_normalizer()
    return normalizer.normalize(text)


def normalize_phrase(phrase: str) -> str:
    """Normalize phrase and return normalized text only."""
    normalizer = get_normalizer()
    return normalizer.normalize_phrase(phrase)
