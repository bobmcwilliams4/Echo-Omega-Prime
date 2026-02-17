"""
TX04 Depreciation Calculator - Semantic Normalization
Domain-specific term normalization and synonym mapping for depreciation queries.
"""

from typing import Dict, List, Set
import re


class SemanticNormalizer:
    """Normalize depreciation-specific terminology to canonical forms."""

    def __init__(self):
        self.synonym_map: Dict[str, str] = {
            # MACRS terminology
            "macrs": "modified_accelerated_cost_recovery_system",
            "modified accelerated cost recovery": "modified_accelerated_cost_recovery_system",
            "modified accelerated cost recovery system": "modified_accelerated_cost_recovery_system",
            "gds": "general_depreciation_system",
            "general depreciation system": "general_depreciation_system",
            "ads": "alternative_depreciation_system",
            "alternative depreciation system": "alternative_depreciation_system",

            # Depreciation methods
            "declining balance": "declining_balance_method",
            "double declining": "200_percent_declining_balance",
            "200% db": "200_percent_declining_balance",
            "200db": "200_percent_declining_balance",
            "150% db": "150_percent_declining_balance",
            "150db": "150_percent_declining_balance",
            "straight line": "straight_line_method",
            "straight-line": "straight_line_method",
            "sl": "straight_line_method",

            # Conventions
            "half year": "half_year_convention",
            "half-year": "half_year_convention",
            "mid quarter": "mid_quarter_convention",
            "mid-quarter": "mid_quarter_convention",
            "mid month": "mid_month_convention",
            "mid-month": "mid_month_convention",

            # Section 179
            "section 179": "section_179_expensing",
            "§179": "section_179_expensing",
            "179 election": "section_179_expensing",
            "expensing election": "section_179_expensing",
            "first year expensing": "section_179_expensing",

            # Bonus depreciation
            "bonus": "bonus_depreciation",
            "bonus depreciation": "bonus_depreciation",
            "section 168k": "bonus_depreciation",
            "§168(k)": "bonus_depreciation",
            "168k": "bonus_depreciation",
            "first year depreciation": "bonus_depreciation",
            "additional first year": "bonus_depreciation",

            # Recovery periods
            "3 year": "3_year_property",
            "3-year": "3_year_property",
            "5 year": "5_year_property",
            "5-year": "5_year_property",
            "7 year": "7_year_property",
            "7-year": "7_year_property",
            "10 year": "10_year_property",
            "15 year": "15_year_property",
            "20 year": "20_year_property",
            "27.5 year": "27_5_year_property",
            "27.5-year": "27_5_year_property",
            "residential rental": "27_5_year_property",
            "39 year": "39_year_property",
            "39-year": "39_year_property",
            "nonresidential real property": "39_year_property",
            "commercial building": "39_year_property",

            # Listed property
            "listed property": "listed_property",
            "luxury auto": "luxury_automobile",
            "luxury automobile": "luxury_automobile",
            "luxury car": "luxury_automobile",
            "passenger auto": "passenger_automobile",
            "passenger automobile": "passenger_automobile",
            "section 280f": "section_280f_limits",
            "§280F": "section_280f_limits",
            "280f": "section_280f_limits",

            # Recapture
            "recapture": "depreciation_recapture",
            "section 1245": "section_1245_recapture",
            "§1245": "section_1245_recapture",
            "1245": "section_1245_recapture",
            "section 1250": "section_1250_recapture",
            "§1250": "section_1250_recapture",
            "1250": "section_1250_recapture",
            "unrecaptured 1250": "unrecaptured_section_1250_gain",
            "25% gain": "unrecaptured_section_1250_gain",

            # Property types
            "qip": "qualified_improvement_property",
            "qualified improvement": "qualified_improvement_property",
            "qualified improvement property": "qualified_improvement_property",
            "leasehold improvement": "qualified_improvement_property",
            "computer": "computer_equipment",
            "computer equipment": "computer_equipment",
            "machinery": "machinery_and_equipment",
            "equipment": "machinery_and_equipment",
            "furniture": "office_furniture",
            "office furniture": "office_furniture",
            "fixtures": "fixtures_and_equipment",
            "building": "nonresidential_real_property",
            "structure": "nonresidential_real_property",
            "rental property": "residential_rental_property",
            "apartment": "residential_rental_property",

            # Intangibles
            "section 197": "section_197_intangibles",
            "§197": "section_197_intangibles",
            "197": "section_197_intangibles",
            "goodwill": "section_197_intangibles",
            "intangible": "section_197_intangibles",
            "amortization": "amortization_15_year",

            # Cost segregation
            "cost seg": "cost_segregation",
            "cost segregation": "cost_segregation",
            "cost segregation study": "cost_segregation",
            "component depreciation": "cost_segregation",

            # Tangible property regulations
            "repair": "repair_vs_capitalization",
            "capitalize": "repair_vs_capitalization",
            "capitalization": "repair_vs_capitalization",
            "tangible property regs": "tangible_property_regulations",
            "tpr": "tangible_property_regulations",
            "de minimis": "de_minimis_safe_harbor",
            "safe harbor": "safe_harbor_election",

            # Placed in service
            "placed in service": "placed_in_service_date",
            "in service": "placed_in_service_date",
            "service date": "placed_in_service_date",
            "ready for use": "placed_in_service_date",

            # Disposition
            "disposition": "asset_disposition",
            "disposal": "asset_disposition",
            "retire": "asset_disposition",
            "retirement": "asset_disposition",
            "partial disposition": "partial_disposition_election",

            # Elections
            "gaa": "general_asset_account",
            "general asset account": "general_asset_account",
            "election out": "election_out_of_bonus",
            "revoke election": "revoke_election",

            # Other
            "unicap": "section_263a_unicap",
            "§263A": "section_263a_unicap",
            "section 263a": "section_263a_unicap",
            "like-kind": "like_kind_exchange_1031",
            "1031": "like_kind_exchange_1031",
            "like kind exchange": "like_kind_exchange_1031",
        }

        self.acronyms: Set[str] = {
            "MACRS", "GDS", "ADS", "QIP", "GAA", "UNICAP", "DB", "SL",
            "ACRS", "LTCG", "AMT", "GVWR", "FMV", "IRC"
        }

        self.section_patterns = [
            (re.compile(r'§\s*(\d+[A-Za-z]?)(?:\(([a-z0-9]+)\))?'), r'section_\1_\2'),
            (re.compile(r'section\s+(\d+[A-Za-z]?)(?:\(([a-z0-9]+)\))?', re.IGNORECASE), r'section_\1_\2'),
        ]

    def normalize(self, text: str) -> str:
        """
        Normalize depreciation query text to canonical forms.

        Args:
            text: Raw query text

        Returns:
            Normalized text with standardized terminology
        """
        # Preserve acronyms
        preserved_acronyms = {}
        for acronym in self.acronyms:
            if acronym in text:
                placeholder = f"__ACRONYM_{acronym}__"
                preserved_acronyms[placeholder] = acronym
                text = text.replace(acronym, placeholder)

        # Normalize to lowercase for processing
        text_lower = text.lower()

        # Apply synonym mapping
        for synonym, canonical in self.synonym_map.items():
            text_lower = text_lower.replace(synonym, canonical)

        # Restore acronyms
        for placeholder, acronym in preserved_acronyms.items():
            text_lower = text_lower.replace(placeholder.lower(), acronym)

        # Normalize section references
        for pattern, replacement in self.section_patterns:
            text_lower = pattern.sub(replacement, text_lower)

        # Clean up multiple underscores
        text_lower = re.sub(r'_+', '_', text_lower)

        return text_lower

    def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key depreciation-related terms from query.

        Args:
            text: Query text

        Returns:
            List of key terms found
        """
        normalized = self.normalize(text)
        key_terms = []

        # Extract canonical terms from normalized text
        for canonical in set(self.synonym_map.values()):
            if canonical in normalized:
                key_terms.append(canonical)

        # Extract section references
        for pattern, _ in self.section_patterns:
            matches = pattern.findall(text)
            key_terms.extend([f"section_{m[0]}_{m[1]}" if m[1] else f"section_{m[0]}" for m in matches])

        return list(set(key_terms))

    def classify_query_type(self, text: str) -> str:
        """
        Classify depreciation query into category.

        Args:
            text: Query text

        Returns:
            Query classification: 'calculation', 'recapture', 'election', 'qualification', 'general'
        """
        text_lower = text.lower()

        if any(term in text_lower for term in ["calculate", "compute", "schedule", "amount", "how much"]):
            return "calculation"

        if any(term in text_lower for term in ["recapture", "1245", "1250", "disposition", "sale"]):
            return "recapture"

        if any(term in text_lower for term in ["elect", "election", "179", "opt out", "choose"]):
            return "election"

        if any(term in text_lower for term in ["qualify", "eligible", "requirement", "can i", "does it"]):
            return "qualification"

        return "general"

    def extract_property_type(self, text: str) -> str:
        """
        Extract property type from query.

        Args:
            text: Query text

        Returns:
            Property type: 'personal_property', 'real_property', 'intangible', 'unknown'
        """
        text_lower = text.lower()

        personal_property_indicators = [
            "equipment", "machinery", "computer", "furniture", "vehicle", "auto", "car",
            "truck", "fixture", "tool", "personal property"
        ]

        real_property_indicators = [
            "building", "structure", "land improvement", "real property", "nonresidential",
            "residential rental", "commercial", "apartment", "warehouse"
        ]

        intangible_indicators = [
            "goodwill", "intangible", "patent", "copyright", "trademark", "covenant not to compete",
            "customer list", "franchise"
        ]

        if any(indicator in text_lower for indicator in intangible_indicators):
            return "intangible"

        if any(indicator in text_lower for indicator in real_property_indicators):
            return "real_property"

        if any(indicator in text_lower for indicator in personal_property_indicators):
            return "personal_property"

        return "unknown"

    def extract_recovery_period(self, text: str) -> str:
        """
        Extract recovery period from query.

        Args:
            text: Query text

        Returns:
            Recovery period: '3', '5', '7', '10', '15', '20', '27.5', '39', 'unknown'
        """
        recovery_period_patterns = [
            (r'\b3[- ]?year\b', '3'),
            (r'\b5[- ]?year\b', '5'),
            (r'\b7[- ]?year\b', '7'),
            (r'\b10[- ]?year\b', '10'),
            (r'\b15[- ]?year\b', '15'),
            (r'\b20[- ]?year\b', '20'),
            (r'\b27\.5[- ]?year\b', '27.5'),
            (r'\b39[- ]?year\b', '39'),
        ]

        text_lower = text.lower()
        for pattern, period in recovery_period_patterns:
            if re.search(pattern, text_lower):
                return period

        return "unknown"
