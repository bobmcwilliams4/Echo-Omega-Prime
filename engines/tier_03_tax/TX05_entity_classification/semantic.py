"""
TX05 Entity Classification Engine - Semantic Normalization
Domain-specific term normalization for entity classification queries
"""

from typing import Dict, List, Set
import re


class SemanticNormalizer:
    """Normalize entity classification terminology to canonical forms"""

    def __init__(self):
        self.term_map = self._build_term_map()
        self.acronym_map = self._build_acronym_map()
        self.phrase_patterns = self._build_phrase_patterns()

    def _build_term_map(self) -> Dict[str, str]:
        """Map variant terms to canonical forms"""
        return {
            # Entity types
            "llc": "limited_liability_company",
            "l.l.c.": "limited_liability_company",
            "l.l.c": "limited_liability_company",
            "pllc": "professional_limited_liability_company",
            "smllc": "single_member_llc",
            "single member llc": "single_member_llc",
            "multi-member llc": "multi_member_llc",
            "multimember llc": "multi_member_llc",
            "limited liability co": "limited_liability_company",

            # Corporation types
            "corp": "corporation",
            "inc": "incorporated",
            "c-corp": "c_corporation",
            "c corp": "c_corporation",
            "s-corp": "s_corporation",
            "s corp": "s_corporation",
            "s corporation": "s_corporation",
            "professional corp": "professional_corporation",
            "pc": "professional_corporation",
            "p.c.": "professional_corporation",

            # Partnership types
            "lp": "limited_partnership",
            "l.p.": "limited_partnership",
            "llp": "limited_liability_partnership",
            "l.l.p.": "limited_liability_partnership",
            "gp": "general_partnership",
            "g.p.": "general_partnership",
            "limited partnership": "limited_partnership",
            "general partnership": "general_partnership",

            # Classification concepts
            "check-the-box": "check_the_box",
            "ctb": "check_the_box",
            "check the box": "check_the_box",
            "entity classification election": "check_the_box",
            "disregarded entity": "disregarded_entity",
            "de": "disregarded_entity",
            "disregarded": "disregarded_entity",
            "pass-through": "flow_through",
            "pass through": "flow_through",
            "passthrough": "flow_through",
            "flow-through": "flow_through",
            "flow through": "flow_through",

            # S corporation terms
            "qsub": "qualified_subchapter_s_subsidiary",
            "q-sub": "qualified_subchapter_s_subsidiary",
            "qualified sub": "qualified_subchapter_s_subsidiary",
            "esbt": "electing_small_business_trust",
            "qsst": "qualified_subchapter_s_trust",
            "one class of stock": "single_class_stock",
            "single class of stock": "single_class_stock",

            # Foreign entity terms
            "foreign corp": "foreign_corporation",
            "foreign entity": "foreign_entity",
            "cfc": "controlled_foreign_corporation",
            "pfic": "passive_foreign_investment_company",
            "per se corp": "per_se_corporation",
            "per se corporation": "per_se_corporation",

            # Election/filing terms
            "form 8832": "entity_classification_election",
            "form 2553": "s_corporation_election",
            "form 8869": "qsub_election",
            "late election": "late_election_relief",
            "election relief": "late_election_relief",
            "rev proc 2009-41": "late_election_relief_procedure",

            # Conversion terms
            "conversion": "entity_conversion",
            "entity conversion": "entity_conversion",
            "reclassification": "entity_conversion",
            "change of classification": "entity_conversion",
            "deemed liquidation": "deemed_liquidation",
            "deemed contribution": "deemed_contribution",

            # Tax treatment terms
            "subchapter k": "partnership_taxation",
            "subchapter s": "s_corporation_taxation",
            "subchapter c": "c_corporation_taxation",
            "double tax": "double_taxation",
            "double taxation": "double_taxation",

            # Eligibility terms
            "eligible entity": "eligible_entity",
            "ineligible entity": "per_se_corporation",
            "per se": "per_se_corporation",
            "default classification": "default_classification",
            "automatic classification": "default_classification",

            # Member/shareholder terms
            "shareholder": "shareholder",
            "member": "member",
            "partner": "partner",
            "owner": "owner",
            "100% owned": "wholly_owned",
            "wholly owned": "wholly_owned",
            "100 percent owned": "wholly_owned",
        }

    def _build_acronym_map(self) -> Dict[str, str]:
        """Map acronyms to full terms"""
        return {
            "LLC": "limited liability company",
            "SMLLC": "single member LLC",
            "CTB": "check-the-box",
            "QSub": "qualified subchapter S subsidiary",
            "ESBT": "electing small business trust",
            "QSST": "qualified subchapter S trust",
            "CFC": "controlled foreign corporation",
            "PFIC": "passive foreign investment company",
            "GILTI": "global intangible low-taxed income",
            "IRC": "Internal Revenue Code",
            "FMV": "fair market value",
            "E&P": "earnings and profits",
            "NOL": "net operating loss",
            "SE": "self-employment",
        }

    def _build_phrase_patterns(self) -> List[tuple]:
        """Regex patterns for common phrases"""
        return [
            (r'\b(?:treas\.?\s*)?reg\.?\s*§?\s*301\.7701-(\d+)', r'treasury_regulation_301_7701_\1'),
            (r'\b(?:irc\s*)?§?\s*(\d+)\(([a-z])\)(?:\((\d+)\))?', r'irc_section_\1_\2_\3'),
            (r'\b(?:irc\s*)?§?\s*(\d+)', r'irc_section_\1'),
            (r'\bform\s+(\d+)', r'form_\1'),
            (r'\brev\.?\s*proc\.?\s*(\d{4})-(\d+)', r'revenue_procedure_\1_\2'),
            (r'\brev\.?\s*rul\.?\s*(\d{2,4})-(\d+)', r'revenue_ruling_\1_\2'),
            (r'\b(\d+)%\s+owned', r'\1_percent_owned'),
            (r'\b(\d+)\s+shareholders?', r'\1_shareholders'),
        ]

    def normalize(self, query: str) -> str:
        """
        Normalize query text to canonical forms

        Args:
            query: Raw query text

        Returns:
            Normalized query with canonical terminology
        """
        text = query.lower().strip()

        # Apply phrase patterns
        for pattern, replacement in self.phrase_patterns:
            text = re.sub(pattern, replacement, text)

        # Replace multi-word terms first (longer matches take priority)
        for variant, canonical in sorted(self.term_map.items(), key=lambda x: len(x[0]), reverse=True):
            text = text.replace(variant, canonical)

        # Expand acronyms
        for acronym, expansion in self.acronym_map.items():
            text = re.sub(r'\b' + re.escape(acronym) + r'\b', expansion, text, flags=re.IGNORECASE)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def extract_keywords(self, query: str) -> Set[str]:
        """
        Extract relevant keywords from query

        Args:
            query: Normalized query text

        Returns:
            Set of extracted keywords
        """
        normalized = self.normalize(query)

        # Split on non-alphanumeric and filter
        tokens = re.findall(r'\b\w+\b', normalized)

        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'can', 'what',
            'when', 'where', 'how', 'why', 'which', 'who', 'whom', 'this', 'that'
        }

        keywords = {token for token in tokens if token not in stop_words and len(token) > 2}

        return keywords

    def identify_entity_type(self, query: str) -> str:
        """
        Identify primary entity type from query

        Args:
            query: Query text

        Returns:
            Entity type identifier or 'unknown'
        """
        normalized = self.normalize(query)

        entity_indicators = {
            'limited_liability_company': ['limited_liability_company', 'llc'],
            'single_member_llc': ['single_member_llc', 'smllc'],
            'multi_member_llc': ['multi_member_llc'],
            'partnership': ['partnership', 'partner', 'limited_partnership', 'general_partnership'],
            's_corporation': ['s_corporation', 's_corp', 'subchapter_s'],
            'c_corporation': ['c_corporation', 'c_corp', 'subchapter_c'],
            'corporation': ['corporation', 'incorporated'],
            'disregarded_entity': ['disregarded_entity', 'disregarded'],
            'qsub': ['qualified_subchapter_s_subsidiary', 'qsub'],
            'foreign_entity': ['foreign_entity', 'foreign_corporation', 'cfc', 'pfic'],
        }

        for entity_type, indicators in entity_indicators.items():
            if any(ind in normalized for ind in indicators):
                return entity_type

        return 'unknown'

    def identify_issue_category(self, query: str) -> List[str]:
        """
        Identify issue categories from query

        Args:
            query: Query text

        Returns:
            List of applicable issue categories
        """
        normalized = self.normalize(query)
        categories = []

        category_patterns = {
            'ENTITY_FORMATION': ['formation', 'forming', 'create', 'establish', 'organize'],
            'ENTITY_ELECTIONS': ['election', 'elect', 'form_8832', 'form_2553', 'check_the_box'],
            'DEFAULT_CLASSIFICATION': ['default', 'automatic', 'default_classification'],
            'CHECK_THE_BOX': ['check_the_box', 'ctb', 'entity_classification_election'],
            'S_CORPORATION': ['s_corporation', 's_corp', 'subchapter_s', 'form_2553'],
            'PARTNERSHIP': ['partnership', 'subchapter_k', 'form_1065', 'k_1'],
            'DISREGARDED_ENTITY': ['disregarded_entity', 'disregarded', 'smllc'],
            'CONVERSION_CONSEQUENCES': ['conversion', 'convert', 'reclassification', 'change_classification'],
            'ELECTION_RELIEF': ['late_election', 'relief', 'rev_proc_2009_41'],
            'FOREIGN_ENTITIES': ['foreign_entity', 'foreign_corporation', 'cfc', 'pfic'],
            'PER_SE_CORPORATIONS': ['per_se', 'ineligible_entity', 'per_se_corporation'],
            'QSUB_ELECTIONS': ['qsub', 'qualified_subchapter_s_subsidiary', 'form_8869'],
        }

        for category, patterns in category_patterns.items():
            if any(pattern in normalized for pattern in patterns):
                categories.append(category)

        return categories if categories else ['ENTITY_CLASSIFICATION_GENERAL']


def normalize_entity_query(query: str) -> Dict[str, any]:
    """
    Comprehensive query normalization

    Args:
        query: Raw query text

    Returns:
        Dict with normalized_query, keywords, entity_type, categories
    """
    normalizer = SemanticNormalizer()

    return {
        'normalized_query': normalizer.normalize(query),
        'keywords': list(normalizer.extract_keywords(query)),
        'entity_type': normalizer.identify_entity_type(query),
        'issue_categories': normalizer.identify_issue_category(query),
        'original_query': query
    }
