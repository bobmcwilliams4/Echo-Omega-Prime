"""
P01 Heirship Determiner — Semantic Normalization
Domain-specific term mapping for probate/intestacy queries
"""

from typing import Dict, List, Set
import re


class SemanticNormalizer:
    """Normalize probate terminology to canonical forms"""

    def __init__(self):
        self.term_map: Dict[str, str] = {
            # Intestacy terms
            "died without a will": "intestate",
            "no will": "intestate",
            "intestacy": "intestate",
            "without testament": "intestate",
            "ab intestato": "intestate",

            # Distribution methods
            "by representation": "per_stirpes",
            "per stirpes": "per_stirpes",
            "by roots": "per_stirpes",
            "per capita": "per_capita",
            "by heads": "per_capita",

            # Property types
            "community estate": "community_property",
            "marital property": "community_property",
            "conjugal property": "community_property",
            "separate estate": "separate_property",
            "sole property": "separate_property",

            # Relationship terms
            "kids": "children",
            "offspring": "descendants",
            "issue": "descendants",
            "heirs of the body": "descendants",
            "lineal descendants": "descendants",
            "half brother": "half_blood_sibling",
            "half sister": "half_blood_sibling",
            "stepchild": "non_heir_stepchild",
            "adopted kid": "adopted_child",

            # Spouse terms
            "widow": "surviving_spouse",
            "widower": "surviving_spouse",
            "husband": "spouse",
            "wife": "spouse",

            # Estate administration
            "probate": "estate_administration",
            "estate proceedings": "estate_administration",
            "independent administration": "independent_admin",
            "dependent administration": "dependent_admin",
            "muniment of title": "muniment_of_title",

            # Heirship determination
            "affidavit of heirship": "affidavit_heirship",
            "heirship affidavit": "affidavit_heirship",
            "declaration of heirship": "determination_heirship",
            "adjudication of heirship": "determination_heirship",

            # Homestead
            "family home": "homestead",
            "primary residence": "homestead",
            "principal residence": "homestead",

            # Advancement
            "gift during life": "advancement",
            "inter vivos transfer": "advancement",
            "advancement against inheritance": "advancement",

            # Escheat
            "no heirs": "escheat",
            "estate to state": "escheat",
            "no takers": "escheat",
        }

        self.synonym_groups: List[Set[str]] = [
            {"intestate", "died_without_will", "no_will"},
            {"per_stirpes", "by_representation", "by_roots"},
            {"community_property", "community_estate", "marital_property"},
            {"separate_property", "separate_estate", "sole_property"},
            {"descendants", "children", "issue", "offspring"},
            {"surviving_spouse", "widow", "widower"},
            {"homestead", "family_home", "primary_residence"},
        ]

    def normalize(self, text: str) -> str:
        """Normalize probate terminology in text"""
        normalized = text.lower()

        # Apply term mappings
        for variant, canonical in self.term_map.items():
            normalized = re.sub(
                r'\b' + re.escape(variant) + r'\b',
                canonical,
                normalized,
                flags=re.IGNORECASE
            )

        return normalized

    def extract_keywords(self, text: str) -> List[str]:
        """Extract normalized keywords from query"""
        normalized = self.normalize(text)

        keywords = []
        for canonical in set(self.term_map.values()):
            if canonical in normalized:
                keywords.append(canonical)

        return keywords

    def expand_synonyms(self, term: str) -> Set[str]:
        """Get all synonyms for a canonical term"""
        for group in self.synonym_groups:
            if term in group:
                return group
        return {term}


class ProbateTaxonomy:
    """Hierarchical classification of probate concepts"""

    @staticmethod
    def get_issue_hierarchy() -> Dict[str, List[str]]:
        return {
            "INTESTATE_SUCCESSION": [
                "separate_property_distribution",
                "community_property_distribution",
                "collateral_heirs",
                "per_stirpes",
                "per_capita"
            ],
            "PROPERTY_CHARACTERIZATION": [
                "community_property",
                "separate_property",
                "quasi_community",
                "inception_of_title",
                "commingling"
            ],
            "HEIR_QUALIFICATION": [
                "adopted_children",
                "half_blood_relatives",
                "posthumous_heirs",
                "simultaneous_death",
                "120_hour_survivorship"
            ],
            "HOMESTEAD_EXEMPTION": [
                "spouse_life_estate",
                "minor_children_rights",
                "homestead_definition",
                "partition_prohibition"
            ],
            "AFFIDAVIT_HEIRSHIP": [
                "disinterested_witnesses",
                "prima_facie_evidence",
                "five_year_rule",
                "recording_requirements"
            ]
        }

    @staticmethod
    def get_authority_hierarchy() -> Dict[str, int]:
        """Authority source weights (higher = more authoritative)"""
        return {
            "texas_constitution": 100,
            "texas_estates_code": 95,
            "texas_family_code": 90,
            "texas_supreme_court": 85,
            "court_of_appeals": 75,
            "attorney_general_opinion": 70,
            "state_bar_guidance": 60,
            "secondary_sources": 50
        }


def calculate_semantic_similarity(query: str, doctrine_keywords: List[str]) -> float:
    """Calculate semantic similarity between query and doctrine keywords"""
    normalizer = SemanticNormalizer()

    query_normalized = normalizer.normalize(query)
    query_keywords = set(normalizer.extract_keywords(query))

    # Expand doctrine keywords with synonyms
    expanded_doctrine = set()
    for keyword in doctrine_keywords:
        expanded_doctrine.update(normalizer.expand_synonyms(keyword))

    # Calculate Jaccard similarity
    if not expanded_doctrine:
        return 0.0

    intersection = query_keywords & expanded_doctrine
    union = query_keywords | expanded_doctrine

    if not union:
        return 0.0

    return len(intersection) / len(union)


__all__ = ['SemanticNormalizer', 'ProbateTaxonomy', 'calculate_semantic_similarity']
