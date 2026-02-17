"""
TX03 Credit Calculator Engine - Semantic Normalization
Domain-specific term normalization for tax credit queries
"""

from typing import Dict, List, Set
from pathlib import Path
import json


class SemanticNormalizer:
    """Normalize tax credit terminology for consistent processing"""

    def __init__(self, config_path: Path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.normalization_maps: Dict[str, Dict[str, List[str]]] = config.get('semantic_normalization', {})

        # Build reverse lookup for efficient normalization
        self.term_to_canonical: Dict[str, str] = {}
        self._build_reverse_maps()

    def _build_reverse_maps(self) -> None:
        """Build reverse lookup from variants to canonical terms"""
        for category, mappings in self.normalization_maps.items():
            for canonical, variants in mappings.items():
                # Canonical term maps to itself
                self.term_to_canonical[canonical.lower()] = canonical
                # Each variant maps to canonical
                for variant in variants:
                    self.term_to_canonical[variant.lower()] = canonical

    def normalize_credit_type(self, credit_term: str) -> str:
        """Normalize credit type terminology

        Examples:
            "refund_credit" -> "refundable"
            "EITC" -> "refundable"
            "GBC" -> "business"
        """
        term_lower = credit_term.lower().strip()

        # Check direct mapping
        if term_lower in self.term_to_canonical:
            return self.term_to_canonical[term_lower]

        # Check if it's a partial match in credit_types
        for canonical, variants in self.normalization_maps.get('credit_types', {}).items():
            if term_lower in [v.lower() for v in variants]:
                return canonical

        return credit_term  # Return original if no mapping found

    def normalize_credit_name(self, credit_name: str) -> str:
        """Normalize credit name to canonical form

        Examples:
            "CTC" -> "child_tax_credit"
            "IRC_24" -> "child_tax_credit"
            "EIC" -> "earned_income_credit"
        """
        name_lower = credit_name.lower().strip()

        # Check direct mapping in credit_names
        for canonical, variants in self.normalization_maps.get('credit_names', {}).items():
            if name_lower == canonical.lower():
                return canonical
            if name_lower in [v.lower() for v in variants]:
                return canonical

        return credit_name

    def extract_irc_section(self, text: str) -> List[str]:
        """Extract IRC section references from text

        Examples:
            "IRC §24" -> ["24"]
            "section 45Q" -> ["45Q"]
            "IRC 32 and 24" -> ["32", "24"]
        """
        import re
        patterns = [
            r'IRC\s*§?\s*(\d+[A-Z]?)',
            r'section\s+(\d+[A-Z]?)',
            r'§\s*(\d+[A-Z]?)'
        ]

        sections = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            sections.extend(matches)

        return list(set(sections))  # Remove duplicates

    def normalize_query(self, query: str) -> Dict[str, any]:
        """Comprehensive query normalization

        Returns:
            {
                'normalized_text': str,
                'credit_types': List[str],
                'credit_names': List[str],
                'irc_sections': List[str],
                'keywords': List[str]
            }
        """
        query_lower = query.lower()

        # Extract IRC sections
        irc_sections = self.extract_irc_section(query)

        # Identify credit types mentioned
        credit_types = []
        for canonical, variants in self.normalization_maps.get('credit_types', {}).items():
            if canonical.lower() in query_lower or any(v.lower() in query_lower for v in variants):
                credit_types.append(canonical)

        # Identify credit names mentioned
        credit_names = []
        for canonical, variants in self.normalization_maps.get('credit_names', {}).items():
            if canonical.lower() in query_lower or any(v.lower() in query_lower for v in variants):
                credit_names.append(canonical)

        # Extract keywords (simple tokenization, exclude common words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}
        tokens = query_lower.split()
        keywords = [token.strip('.,;:!?') for token in tokens if token.strip('.,;:!?') not in stop_words and len(token) > 2]

        # Normalize text by replacing variants with canonical terms
        normalized_text = query
        for canonical, variants in self.normalization_maps.get('credit_names', {}).items():
            for variant in variants:
                normalized_text = normalized_text.replace(variant, canonical)

        return {
            'normalized_text': normalized_text,
            'credit_types': credit_types,
            'credit_names': credit_names,
            'irc_sections': irc_sections,
            'keywords': keywords
        }

    def get_canonical_term(self, term: str) -> str:
        """Get canonical form of any term"""
        term_lower = term.lower().strip()
        return self.term_to_canonical.get(term_lower, term)

    def get_all_variants(self, canonical: str) -> List[str]:
        """Get all variants of a canonical term"""
        variants = []
        for category_maps in self.normalization_maps.values():
            if canonical in category_maps:
                variants.extend(category_maps[canonical])
        return variants

    def is_refundable_credit(self, credit_name: str) -> bool:
        """Determine if credit is refundable based on name"""
        normalized = self.normalize_credit_name(credit_name)

        # Known refundable credits
        refundable_credits = {
            'earned_income_credit',
            'child_tax_credit',  # Partially refundable (ACTC)
            'american_opportunity_credit'  # Partially refundable (40%)
        }

        return normalized in refundable_credits

    def categorize_credit(self, credit_name: str) -> str:
        """Categorize credit as individual, business, energy, etc."""
        normalized = self.normalize_credit_name(credit_name)

        # Categorization mapping
        individual_credits = {
            'child_tax_credit', 'earned_income_credit', 'american_opportunity_credit',
            'lifetime_learning_credit', 'child_dependent_care_credit'
        }
        business_credits = {
            'research_credit', 'low_income_housing_credit', 'work_opportunity_credit',
            'employer_provided_childcare_credit'
        }
        energy_credits = {
            'clean_vehicle_credit', 'renewable_electricity_production_credit',
            'energy_investment_credit', 'alternative_fuel_vehicle_refueling_property_credit',
            'enhanced_oil_recovery_credit', 'carbon_capture_sequestration_credit'
        }

        if normalized in individual_credits:
            return 'individual'
        elif normalized in business_credits:
            return 'business'
        elif normalized in energy_credits:
            return 'energy'
        else:
            return 'other'
