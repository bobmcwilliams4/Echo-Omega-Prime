"""
P08 Probate Procedure Engine - Semantic Normalization
Domain-specific term normalization for probate procedure queries.
"""

from typing import Dict, List, Set
import re


class SemanticNormalizer:
    """Normalizes probate procedure terminology for consistent doctrine matching."""

    def __init__(self):
        self.synonym_map = self._build_synonym_map()
        self.abbreviation_map = self._build_abbreviation_map()
        self.phrase_patterns = self._build_phrase_patterns()

    def normalize(self, query: str) -> str:
        """
        Normalize query text through multi-stage transformation.

        Args:
            query: Raw query text

        Returns:
            Normalized query text
        """
        text = query.lower().strip()
        text = self._expand_abbreviations(text)
        text = self._normalize_phrases(text)
        text = self._apply_synonyms(text)
        text = self._clean_whitespace(text)
        return text

    def extract_keywords(self, query: str) -> List[str]:
        """Extract key terms from normalized query."""
        normalized = self.normalize(query)
        words = normalized.split()
        # Remove stop words but keep probate-specific terms
        stop_words = {"a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
                      "have", "has", "had", "do", "does", "did", "will", "would", "should",
                      "could", "may", "might", "must", "can", "of", "in", "on", "at", "to",
                      "for", "with", "by", "from", "about", "as", "into", "through"}
        keywords = [w for w in words if w not in stop_words or w in {"will", "administration"}]
        return keywords

    def _build_synonym_map(self) -> Dict[str, str]:
        """Build comprehensive synonym mapping for probate terms."""
        return {
            # Probate procedures
            "independent executor": "independent administration",
            "independent representative": "independent administration",
            "independent personal representative": "independent administration",
            "muniment": "muniment of title",
            "muniment title": "muniment of title",
            "small estate": "small estate affidavit",
            "small estate procedure": "small estate affidavit",
            "affidavit procedure": "small estate affidavit",
            "heirship": "determination of heirship",
            "heirship proceeding": "determination of heirship",
            "declare heirs": "determination of heirship",
            "dependent executor": "dependent administration",
            "dependent representative": "dependent administration",
            "court supervised": "dependent administration",
            "supervised administration": "dependent administration",

            # Will types
            "foreign probate": "foreign will",
            "out of state will": "foreign will",
            "sister state will": "foreign will",
            "ancillary": "ancillary probate",
            "secondary probate": "ancillary probate",

            # Procedures
            "probate will": "will probate",
            "admit will": "will probate",
            "prove will": "will probate",
            "contest": "will contest",
            "challenge will": "will contest",
            "dispute will": "will contest",

            # Jurisdiction
            "proper county": "venue",
            "jurisdiction": "venue",
            "which court": "venue",
            "where to file": "venue",
            "domicile": "venue",

            # Notice
            "service": "citation",
            "notice to heirs": "citation",
            "notify beneficiaries": "citation",

            # Timing
            "four year limit": "four year limitation",
            "statute of limitations": "four year limitation",
            "late probate": "four year limitation",
            "deadline": "time limit",

            # Standing
            "who can contest": "standing",
            "eligible to challenge": "standing",
            "interested party": "standing",

            # Assets
            "estate size": "estate value",
            "estate worth": "estate value",
            "probate property": "estate assets",
            "exempt property": "homestead exemption",

            # Parties
            "personal representative": "executor",
            "administrator": "executor",
            "estate representative": "executor",
            "fiduciary": "executor",
            "beneficiary": "devisee",
            "legatee": "devisee",
            "heir": "heir at law",
            "next of kin": "heir at law",
        }

    def _build_abbreviation_map(self) -> Dict[str, str]:
        """Build abbreviation expansion mapping."""
        return {
            "§": "section",
            "sec.": "section",
            "admin": "administration",
            "indep": "independent",
            "dep": "dependent",
            "mot": "muniment of title",
            "sea": "small estate affidavit",
            "doh": "determination of heirship",
            "upc": "uniform probate code",
            "tx": "texas",
            "est": "estates",
            "prob": "probate",
        }

    def _build_phrase_patterns(self) -> List[tuple]:
        """Build phrase normalization patterns (regex, replacement)."""
        return [
            (r"probate\s+a\s+will", "will probate"),
            (r"probate\s+the\s+will", "will probate"),
            (r"probate\s+an\s+estate", "estate administration"),
            (r"open\s+probate", "initiate probate"),
            (r"close\s+probate", "final settlement"),
            (r"no\s+probate", "avoid probate"),
            (r"skip\s+probate", "avoid probate"),
            (r"without\s+probate", "non probate transfer"),
            (r"independent\s+executor", "independent administration"),
            (r"dependent\s+executor", "dependent administration"),
            (r"temporary\s+executor", "temporary administration"),
            (r"letters\s+testamentary", "executor authority"),
            (r"letters\s+of\s+administration", "administrator authority"),
            (r"affidavit\s+of\s+heirship", "heirship affidavit"),
            (r"community\s+property\s+agreement", "survivorship agreement"),
            (r"right\s+of\s+survivorship", "joint tenancy"),
            (r"transfer\s+on\s+death", "tod deed"),
            (r"payable\s+on\s+death", "pod account"),
        ]

    def _expand_abbreviations(self, text: str) -> str:
        """Expand abbreviations to full terms."""
        for abbrev, expansion in self.abbreviation_map.items():
            # Word boundary matching for abbreviations
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
        return text

    def _normalize_phrases(self, text: str) -> str:
        """Normalize common phrase patterns."""
        for pattern, replacement in self.phrase_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def _apply_synonyms(self, text: str) -> str:
        """Apply synonym replacements."""
        for synonym, canonical in self.synonym_map.items():
            # Use word boundary to avoid partial matches
            pattern = r'\b' + re.escape(synonym) + r'\b'
            text = re.sub(pattern, canonical, text, flags=re.IGNORECASE)
        return text

    def _clean_whitespace(self, text: str) -> str:
        """Normalize whitespace."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


class KeywordExtractor:
    """Extract probate-specific keywords and entities from queries."""

    def __init__(self):
        self.procedure_types = {
            "independent administration", "dependent administration",
            "muniment of title", "small estate affidavit",
            "determination of heirship", "foreign will", "ancillary probate",
            "temporary administration", "will probate"
        }
        self.jurisdictional_terms = {
            "venue", "domicile", "jurisdiction", "county", "resident", "non-resident"
        }
        self.temporal_terms = {
            "four year limitation", "deadline", "time limit", "late probate",
            "statute of limitations", "30 day waiting period"
        }
        self.party_terms = {
            "executor", "administrator", "heir", "beneficiary", "devisee",
            "creditor", "interested party", "ad litem"
        }

    def extract_entities(self, normalized_query: str) -> Dict[str, List[str]]:
        """
        Extract categorized entities from normalized query.

        Returns:
            Dict with keys: procedures, jurisdictional, temporal, parties
        """
        entities = {
            "procedures": [],
            "jurisdictional": [],
            "temporal": [],
            "parties": []
        }

        words = normalized_query.split()
        text = normalized_query

        # Check for multi-word procedure names
        for proc in self.procedure_types:
            if proc in text:
                entities["procedures"].append(proc)

        for term in self.jurisdictional_terms:
            if term in text:
                entities["jurisdictional"].append(term)

        for term in self.temporal_terms:
            if term in text:
                entities["temporal"].append(term)

        for term in self.party_terms:
            if term in text:
                entities["parties"].append(term)

        return entities


# Singleton instances
_normalizer = SemanticNormalizer()
_extractor = KeywordExtractor()


def normalize_query(query: str) -> str:
    """Public API: normalize query text."""
    return _normalizer.normalize(query)


def extract_keywords(query: str) -> List[str]:
    """Public API: extract keywords from query."""
    return _normalizer.extract_keywords(query)


def extract_entities(query: str) -> Dict[str, List[str]]:
    """Public API: extract categorized entities."""
    normalized = normalize_query(query)
    return _extractor.extract_entities(normalized)
