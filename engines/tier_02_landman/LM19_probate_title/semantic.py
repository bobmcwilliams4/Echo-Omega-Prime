"""
LM19 Probate Title Engine — Semantic Normalization
===================================================
Domain-specific term normalization for probate and estate title examination.
Maps common variations to canonical terms for doctrine matching.
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
    canonical_terms: list[str]
    confidence: float


class SemanticNormalizer:
    """Semantic normalization for probate title domain."""

    def __init__(self) -> None:
        """Initialize normalizer with probate-specific term mappings."""
        self.term_map: dict[str, str] = {
            # Intestate succession
            "no will": "intestate",
            "died without a will": "intestate",
            "died intestate": "intestate",
            "no testament": "intestate",
            "descent and distribution": "intestate succession",
            "statutory succession": "intestate succession",
            "heirs at law": "intestate heirs",
            "statutory heirs": "intestate heirs",

            # Testate succession
            "last will and testament": "will",
            "testament": "will",
            "testamentary instrument": "will",
            "codicil": "will amendment",
            "holographic will": "handwritten will",
            "attested will": "formal will",
            "self-proved will": "self-proving will",
            "nuncupative will": "oral will",

            # Administration types
            "independent executor": "independent administration",
            "iaea": "independent administration",
            "independent executrix": "independent administration",
            "dependent executor": "dependent administration",
            "court supervised": "dependent administration",
            "administrator": "dependent administration",
            "administratrix": "dependent administration",
            "personal representative": "executor",

            # Probate procedures
            "probate as muniment": "muniment of title",
            "muniment only": "muniment of title",
            "small estate affidavit": "affidavit of heirship",
            "heirship affidavit": "affidavit of heirship",
            "affidavit of descent": "affidavit of heirship",
            "determination of heirs": "determination of heirship",
            "declaratory judgment of heirship": "determination of heirship",
            "adjudication of heirship": "determination of heirship",

            # Property types
            "community estate": "community property",
            "marital property": "community property",
            "separate estate": "separate property",
            "sole and separate": "separate property",
            "quasi-community property": "community property",

            # Family relationships
            "surviving spouse": "widow",
            "widower": "widow",
            "spouse": "widow",
            "children": "descendants",
            "kids": "descendants",
            "issue": "descendants",
            "offspring": "descendants",
            "lineal descendants": "descendants",
            "heirs of the body": "descendants",
            "next of kin": "heirs",
            "kindred": "heirs",
            "blood relatives": "heirs",

            # Distribution methods
            "by representation": "per stirpes",
            "per capita": "per capita",
            "by right of representation": "per stirpes",
            "equally": "per capita",

            # Estate concepts
            "mineral estate": "mineral interest",
            "mineral rights": "mineral interest",
            "royalty interest": "mineral interest",
            "mineral ownership": "mineral interest",
            "undivided interest": "fractional interest",
            "fractional share": "fractional interest",
            "percentage interest": "fractional interest",

            # Life estates
            "life tenancy": "life estate",
            "estate for life": "life estate",
            "life use": "life estate",
            "remainderman": "remainder interest",
            "remainder beneficiary": "remainder interest",
            "reversionary interest": "remainder interest",

            # Trusts
            "living trust": "revocable trust",
            "inter vivos trust": "revocable trust",
            "testamentary trust": "trust in will",
            "trust under will": "trust in will",
            "trustee": "trust administrator",

            # Homestead
            "family homestead": "homestead",
            "homestead property": "homestead",
            "constitutional homestead": "homestead",
            "probate homestead": "homestead allowance",

            # Deeds and transfers
            "enhanced life estate deed": "lady bird deed",
            "ladybird deed": "lady bird deed",
            "transfer on death": "tod deed",
            "beneficiary deed": "tod deed",
            "payable on death": "pod designation",

            # Other concepts
            "predeceased beneficiary": "lapsed gift",
            "deceased devisee": "lapsed gift",
            "omitted child": "pretermitted heir",
            "afterborn child": "pretermitted heir",
            "omitted spouse": "pretermitted spouse",
            "forgotten heir": "pretermitted heir",
            "simultaneous death": "common disaster",
            "common calamity": "common disaster",
            "concurrent death": "simultaneous death",
            "escheat": "state ownership",
            "forfeiture to state": "escheat",
            "unclaimed property": "abandoned property",

            # Mineral specific
            "oil and gas lease": "mineral lease",
            "mineral lease": "mineral lease",
            "lease bonus": "lease signing bonus",
            "delay rental": "lease rental payment",
            "shut-in royalty": "shut-in payment",
            "production royalty": "royalty payment",
            "overriding royalty": "orri",
            "net revenue interest": "nri",
            "working interest": "operating interest",
        }

        # Regex patterns for common variations
        self.patterns: list[tuple[re.Pattern, str]] = [
            (re.compile(r"\bsection\s+(\d+)", re.I), r"§\1"),
            (re.compile(r"\btx\s+estates\s+code", re.I), "TX Estates Code"),
            (re.compile(r"\btx\s+property\s+code", re.I), "TX Property Code"),
            (re.compile(r"\btx\s+family\s+code", re.I), "TX Family Code"),
            (re.compile(r"\b1/(\d+)\b"), r"one-\1"),
            (re.compile(r"\b(\d+)%\b"), r"\1 percent"),
            (re.compile(r"\bdecedent'?s?\b", re.I), "decedent"),
            (re.compile(r"\bestate of\s+([A-Z][a-z]+)", re.I), r"\1 estate"),
        ]

    def normalize(self, text: str) -> NormalizationResult:
        """
        Normalize probate title query text.

        Args:
            text: Original query text

        Returns:
            NormalizationResult with normalized text and canonical terms
        """
        original = text
        normalized = text.lower().strip()
        canonical_terms: list[str] = []

        # Apply term mappings
        for term, canonical in self.term_map.items():
            if term in normalized:
                normalized = normalized.replace(term, canonical)
                if canonical not in canonical_terms:
                    canonical_terms.append(canonical)

        # Apply regex patterns
        for pattern, replacement in self.patterns:
            normalized = pattern.sub(replacement, normalized)

        # Extract key canonical terms from normalized text
        for canonical in self.term_map.values():
            if canonical in normalized and canonical not in canonical_terms:
                canonical_terms.append(canonical)

        # Calculate confidence based on number of normalizations
        normalizations = len(canonical_terms)
        confidence = min(1.0, 0.6 + (normalizations * 0.1))

        return NormalizationResult(
            original=original,
            normalized=normalized,
            canonical_terms=canonical_terms,
            confidence=confidence
        )

    def extract_entities(self, text: str) -> dict[str, list[str]]:
        """
        Extract probate-specific entities from text.

        Args:
            text: Query text

        Returns:
            Dictionary of entity types to extracted values
        """
        entities: dict[str, list[str]] = {
            "statutes": [],
            "family_members": [],
            "property_types": [],
            "procedures": [],
            "interests": [],
        }

        # Extract statute citations
        statute_pattern = re.compile(r"(?:TX|Texas)\s+(?:Estates|Property|Family)\s+Code\s+§?\s*(\d+(?:\.\d+)?)", re.I)
        for match in statute_pattern.finditer(text):
            entities["statutes"].append(match.group(0))

        # Extract family member references
        family_terms = ["spouse", "widow", "widower", "child", "children", "parent", "sibling", "heir", "descendant", "issue"]
        for term in family_terms:
            if re.search(rf"\b{term}s?\b", text, re.I):
                entities["family_members"].append(term)

        # Extract property types
        property_terms = ["mineral", "royalty", "surface", "community", "separate", "homestead"]
        for term in property_terms:
            if re.search(rf"\b{term}\b", text, re.I):
                entities["property_types"].append(term)

        # Extract procedures
        procedure_terms = ["probate", "administration", "muniment", "affidavit", "determination", "escheat"]
        for term in procedure_terms:
            if re.search(rf"\b{term}\b", text, re.I):
                entities["procedures"].append(term)

        # Extract interest types
        interest_terms = ["fee simple", "life estate", "remainder", "undivided", "fractional"]
        for term in interest_terms:
            if re.search(rf"\b{term}\b", text, re.I):
                entities["interests"].append(term)

        return entities

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two probate terms.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score 0.0-1.0
        """
        norm1 = self.normalize(text1)
        norm2 = self.normalize(text2)

        # Exact match
        if norm1.normalized == norm2.normalized:
            return 1.0

        # Canonical term overlap
        common_terms = set(norm1.canonical_terms) & set(norm2.canonical_terms)
        if common_terms:
            overlap = len(common_terms) / max(len(norm1.canonical_terms), len(norm2.canonical_terms))
            return 0.5 + (overlap * 0.5)

        # Token overlap
        tokens1 = set(norm1.normalized.split())
        tokens2 = set(norm2.normalized.split())
        common_tokens = tokens1 & tokens2
        if common_tokens:
            return len(common_tokens) / max(len(tokens1), len(tokens2))

        return 0.0


# Global normalizer instance
_NORMALIZER: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get global normalizer instance."""
    global _NORMALIZER
    if _NORMALIZER is None:
        _NORMALIZER = SemanticNormalizer()
    return _NORMALIZER
