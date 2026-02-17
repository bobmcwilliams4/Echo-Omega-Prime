"""
R01_rrc_parser Semantic Normalizer — RRC-specific term normalization

Normalizes Texas Railroad Commission terminology to canonical forms for
deterministic doctrine cache matching.
"""

from __future__ import annotations

import re
from typing import Dict, List, Set


class SemanticNormalizer:
    """
    RRC-specific semantic normalization for deterministic cache hits.

    Normalizes:
    - Abbreviations → full terms (W-1 → permit to drill)
    - Synonyms → canonical terms (SWD → saltwater disposal)
    - Case/whitespace → lowercase, single space
    - Hyphenation variations → consistent form
    """

    def __init__(self) -> None:
        # RRC form abbreviations
        self._form_expansions: Dict[str, str] = {
            "w-1": "permit to drill",
            "w1": "permit to drill",
            "w-2": "completion report",
            "w2": "completion report",
            "p-4": "production report",
            "p4": "production report",
            "p-5": "organization report",
            "p5": "organization report",
            "g-1": "gas well report",
            "g1": "gas well report",
            "h-10": "plugging report",
            "h10": "plugging report",
            "h-1": "plugging notification",
            "h1": "plugging notification",
            "t-4": "pipeline permit",
            "t4": "pipeline permit",
            "w-10": "injection report",
            "w10": "injection report",
            "w-14": "injection permit",
            "w14": "injection permit",
        }

        # RRC terminology synonyms
        self._synonyms: Dict[str, str] = {
            "swd": "saltwater disposal",
            "disposal well": "saltwater disposal",
            "injection well": "saltwater disposal",
            "uic": "underground injection control",
            "mit": "mechanical integrity test",
            "permit to drill": "drilling permit",
            "drilling application": "drilling permit",
            "gor": "gas oil ratio",
            "gas-oil ratio": "gas oil ratio",
            "oil-gas ratio": "gas oil ratio",
            "plugging": "plug and abandon",
            "p and a": "plug and abandon",
            "p&a": "plug and abandon",
            "shut-in": "shut in",
            "shutin": "shut in",
            "lateral section": "horizontal wellbore",
            "lateral wellbore": "horizontal wellbore",
            "deviated well": "directional well",
            "slant well": "directional well",
            "maop": "maximum allowable operating pressure",
            "casing program": "casing design",
            "cementing program": "cementing design",
            "discovery allowable": "discovery well allowable",
            "market demand": "proration",
            "proration schedule": "allowable",
            "surface casing": "conductor casing",
            "production casing": "long string",
            "intermediate casing": "protection string",
            "tubing": "production tubing",
            "packer": "production packer",
            "usable quality water": "underground source of drinking water",
            "usdw": "underground source of drinking water",
            "freshwater": "underground source of drinking water",
            "confining zone": "cap rock",
            "sealing formation": "cap rock",
            "h2s": "hydrogen sulfide",
            "sour gas": "hydrogen sulfide gas",
            "sweet gas": "non-hydrogen sulfide gas",
            "casinghead gas": "associated gas",
            "solution gas": "associated gas",
            "dry gas": "non-associated gas",
            "wet gas": "gas with condensate",
            "condensate": "natural gas liquids",
            "ngls": "natural gas liquids",
            "blanket bond": "financial assurance bond",
            "individual bond": "single well bond",
            "letter of credit": "financial assurance",
            "operator of record": "designated operator",
            "working interest owner": "operator",
            "royalty owner": "non-operating interest",
            "mineral owner": "lessor",
            "lessee": "operator",
            "surface owner": "landowner",
            "offset operator": "adjacent operator",
            "pooling": "unitization",
            "pooling agreement": "unit agreement",
            "drilling unit": "proration unit",
            "spacing unit": "proration unit",
            "field rules": "special field rules",
            "district rules": "field rules",
            "permit denial": "permit rejection",
            "administrative penalty": "enforcement penalty",
            "notice of violation": "enforcement action",
            "agreed order": "settlement",
            "contested case": "hearing",
            "soah": "state office of administrative hearings",
        }

        # Multi-word canonical forms (preserved during normalization)
        self._canonical_phrases: Set[str] = {
            "rule 37", "rule 13", "rule 14", "rule 36", "rule 32", "rule 38", "rule 26", "rule 46",
            "permit to drill", "completion report", "production report", "organization report",
            "plugging report", "saltwater disposal", "underground injection control",
            "mechanical integrity test", "gas oil ratio", "plug and abandon",
            "horizontal wellbore", "directional well", "maximum allowable operating pressure",
            "underground source of drinking water", "hydrogen sulfide", "natural gas liquids",
            "financial assurance", "single well bond", "designated operator", "proration unit",
            "special field rules", "enforcement penalty", "state office of administrative hearings",
            "texas railroad commission", "texas natural resources code", "texas administrative code",
            "statewide rule", "field rule", "discovery well allowable", "exception to rule 37",
            "lateral section survey", "directional survey", "initial potential test",
            "cement bond log", "temperature survey", "caliper log", "electric log",
            "surface casing", "production casing", "intermediate casing",
            "usable quality water", "confining zone", "injection zone",
            "area of review", "offset operator", "lease line", "unit line",
            "pooling agreement", "unitization", "proration schedule", "allowable production",
            "severance tax", "common carrier", "gathering line", "transmission line",
        }

        # Compile regex patterns
        self._whitespace_pattern = re.compile(r"\s+")
        self._hyphen_pattern = re.compile(r"(\w)-(\w)")

    def normalize(self, text: str) -> str:
        """
        Normalize RRC terminology to canonical form.

        Steps:
        1. Lowercase
        2. Expand form abbreviations (W-1 → permit to drill)
        3. Replace synonyms with canonical terms
        4. Normalize whitespace
        5. Standardize hyphenation
        """
        if not text:
            return ""

        # Lowercase
        text = text.lower()

        # Expand form abbreviations
        for abbrev, expansion in self._form_expansions.items():
            text = re.sub(rf"\b{re.escape(abbrev)}\b", expansion, text)

        # Replace synonyms
        for synonym, canonical in self._synonyms.items():
            text = re.sub(rf"\b{re.escape(synonym)}\b", canonical, text)

        # Normalize whitespace
        text = self._whitespace_pattern.sub(" ", text).strip()

        # Standardize hyphenation (e.g., "shut in" vs "shut-in" → "shut in")
        # Preserve canonical phrases
        for phrase in self._canonical_phrases:
            if phrase.replace(" ", "-") in text or phrase.replace("-", " ") in text:
                text = text.replace(phrase.replace(" ", "-"), phrase)
                text = text.replace(phrase.replace("-", " "), phrase)

        return text

    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract normalized keywords from text.

        Filters out common stop words and returns unique normalized keywords.
        """
        normalized = self.normalize(text)

        # Stop words (RRC-specific)
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
            "been", "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "should", "could", "may", "might", "must", "can", "shall",
            "this", "that", "these", "those", "it", "its", "they", "them", "their",
            "what", "which", "who", "whom", "whose", "when", "where", "why", "how",
        }

        # Split and filter
        tokens = normalized.split()
        keywords = [
            token for token in tokens
            if len(token) >= min_length and token not in stop_words
        ]

        # Remove duplicates while preserving order
        seen: Set[str] = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                unique_keywords.append(kw)
                seen.add(kw)

        return unique_keywords

    def is_match(self, query: str, target: str, threshold: float = 0.5) -> bool:
        """
        Check if normalized query matches normalized target.

        Returns True if keyword overlap exceeds threshold.
        """
        query_kw = set(self.extract_keywords(query))
        target_kw = set(self.extract_keywords(target))

        if not query_kw or not target_kw:
            return False

        overlap = len(query_kw & target_kw)
        min_size = min(len(query_kw), len(target_kw))

        return (overlap / min_size) >= threshold if min_size > 0 else False
