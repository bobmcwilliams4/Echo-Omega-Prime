"""
TX06 Basis Calculator - Semantic Normalization
Domain-specific term normalization for basis calculation queries
"""

from typing import Dict, List, Set
import re


class SemanticNormalizer:
    """Normalize basis calculation terminology to canonical forms"""

    def __init__(self):
        self.term_mappings = self._build_term_mappings()
        self.abbreviation_expansions = self._build_abbreviations()
        self.concept_synonyms = self._build_synonyms()

    def _build_term_mappings(self) -> Dict[str, str]:
        """Map variations to canonical terms"""
        return {
            # Basis types
            "cost basis": "cost_basis",
            "adjusted basis": "adjusted_basis",
            "stepped up basis": "stepped_up_basis",
            "stepped-up basis": "stepped_up_basis",
            "step up basis": "stepped_up_basis",
            "step-up basis": "stepped_up_basis",
            "carryover basis": "carryover_basis",
            "carry over basis": "carryover_basis",
            "transferred basis": "transferred_basis",
            "substituted basis": "substituted_basis",
            "exchanged basis": "exchanged_basis",

            # Acquisition types
            "inherited property": "inheritance",
            "inherited": "inheritance",
            "inherit": "inheritance",
            "estate property": "inheritance",
            "decedent property": "inheritance",
            "gift property": "gift",
            "gifted property": "gift",
            "donated property": "gift",
            "like-kind exchange": "like_kind_exchange",
            "like kind exchange": "like_kind_exchange",
            "1031 exchange": "like_kind_exchange",
            "tax-free exchange": "like_kind_exchange",
            "involuntary conversion": "involuntary_conversion",
            "condemnation": "involuntary_conversion",
            "casualty conversion": "involuntary_conversion",

            # Entity types
            "partnership contribution": "partnership_contribution",
            "capital contribution": "capital_contribution",
            "corporate contribution": "corporate_contribution",
            "351 exchange": "corporate_contribution",
            "721 contribution": "partnership_contribution",
            "partnership distribution": "partnership_distribution",
            "liquidating distribution": "liquidating_distribution",

            # Adjustments
            "depreciation": "depreciation_adjustment",
            "capital improvement": "capital_improvement",
            "betterment": "capital_improvement",
            "return of capital": "return_of_capital",
            "wash sale": "wash_sale",
            "wash sale loss": "wash_sale",

            # Special situations
            "divorce transfer": "divorce_transfer",
            "incident to divorce": "divorce_transfer",
            "marital transfer": "divorce_transfer",
            "community property": "community_property",
            "separate property": "separate_property",
            "boot": "boot_received",
            "debt relief": "debt_relief",
            "liability assumption": "liability_assumption",

            # Basis terms
            "inside basis": "inside_basis",
            "outside basis": "outside_basis",
            "dual basis": "dual_basis",
            "loss basis": "loss_basis",
            "gain basis": "gain_basis",
        }

    def _build_abbreviations(self) -> Dict[str, str]:
        """Expand common abbreviations"""
        return {
            "FMV": "fair_market_value",
            "AB": "adjusted_basis",
            "RB": "remaining_basis",
            "QI": "qualified_intermediary",
            "EAT": "exchange_accommodation_titleholder",
            "IRD": "income_in_respect_of_decedent",
            "AAA": "accumulated_adjustments_account",
            "K-1": "schedule_k1",
            "754": "section_754_election",
            "743(b)": "section_743b_adjustment",
            "734(b)": "section_734b_adjustment",
        }

    def _build_synonyms(self) -> Dict[str, List[str]]:
        """Group synonymous concepts"""
        return {
            "purchase": ["buy", "acquire", "acquisition", "bought", "purchased"],
            "sale": ["sell", "disposition", "dispose", "sold", "transfer"],
            "improvement": ["betterment", "renovation", "upgrade", "enhancement", "capital_expenditure"],
            "distribution": ["payout", "withdrawal", "distribution", "draw"],
            "contribution": ["capital_contribution", "investment", "infusion"],
            "exchange": ["swap", "trade", "exchange", "substitution"],
            "inheritance": ["inherit", "estate", "bequest", "devise", "inherited"],
            "gift": ["donation", "transfer", "gifted", "donate"],
        }

    def normalize_query(self, query: str) -> str:
        """Normalize a basis calculation query to canonical form"""
        normalized = query.lower().strip()

        # Expand abbreviations
        for abbr, expansion in self.abbreviation_expansions.items():
            normalized = re.sub(
                rf'\b{re.escape(abbr)}\b',
                expansion,
                normalized,
                flags=re.IGNORECASE
            )

        # Map terms to canonical forms
        for term, canonical in self.term_mappings.items():
            normalized = re.sub(
                rf'\b{re.escape(term)}\b',
                canonical,
                normalized,
                flags=re.IGNORECASE
            )

        return normalized

    def extract_basis_type(self, query: str) -> str:
        """Extract the primary basis calculation type from query"""
        normalized = self.normalize_query(query)

        # Priority order for basis type detection
        basis_types = [
            ("stepped_up_basis", "inheritance"),
            ("carryover_basis", "gift"),
            ("like_kind_exchange", "exchange"),
            ("corporate_contribution", "contribution"),
            ("partnership_contribution", "contribution"),
            ("partnership_distribution", "distribution"),
            ("wash_sale", "wash_sale"),
            ("divorce_transfer", "divorce"),
            ("involuntary_conversion", "conversion"),
            ("cost_basis", "purchase"),
        ]

        for pattern, basis_type in basis_types:
            if pattern in normalized:
                return basis_type

        return "general_basis"

    def extract_entity_type(self, query: str) -> str:
        """Extract entity type (individual, partnership, corporation, etc.)"""
        normalized = self.normalize_query(query)

        entity_patterns = {
            "partnership": ["partnership", "partner", "llc", "limited_liability"],
            "corporation": ["corporation", "corp", "c_corp", "corporate"],
            "s_corporation": ["s_corp", "s_corporation", "subchapter_s"],
            "trust": ["trust", "trustee", "fiduciary"],
            "estate": ["estate", "decedent", "executor"],
            "individual": ["individual", "person", "taxpayer"],
        }

        for entity, patterns in entity_patterns.items():
            if any(p in normalized for p in patterns):
                return entity

        return "individual"

    def extract_irc_sections(self, query: str) -> List[str]:
        """Extract IRC section references from query"""
        sections = []

        # Match patterns like "§1014", "IRC 1014", "section 1014", "1014(a)"
        patterns = [
            r'§\s*(\d+(?:\([a-z]\))?)',
            r'IRC\s*§?\s*(\d+(?:\([a-z]\))?)',
            r'section\s+(\d+(?:\([a-z]\))?)',
            r'\b(\d{3,4}(?:\([a-z]\))?)\b'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            sections.extend(matches)

        # Deduplicate and sort
        return sorted(list(set(sections)))

    def identify_keywords(self, query: str) -> Set[str]:
        """Extract relevant keywords for doctrine matching"""
        normalized = self.normalize_query(query)
        keywords = set()

        # Basis types
        basis_keywords = [
            "cost_basis", "adjusted_basis", "stepped_up_basis", "carryover_basis",
            "transferred_basis", "substituted_basis", "inside_basis", "outside_basis"
        ]
        keywords.update([kw for kw in basis_keywords if kw in normalized])

        # Transaction types
        transaction_keywords = [
            "inheritance", "gift", "like_kind_exchange", "involuntary_conversion",
            "partnership_contribution", "corporate_contribution", "distribution",
            "divorce_transfer", "wash_sale"
        ]
        keywords.update([kw for kw in transaction_keywords if kw in normalized])

        # Adjustment types
        adjustment_keywords = [
            "depreciation", "capital_improvement", "return_of_capital",
            "debt_relief", "liability_assumption", "boot"
        ]
        keywords.update([kw for kw in adjustment_keywords if kw in normalized])

        # Property types
        property_keywords = [
            "real_property", "personal_property", "stock", "partnership_interest",
            "business_property", "rental_property", "investment_property"
        ]
        keywords.update([kw for kw in property_keywords if kw in normalized])

        return keywords

    def normalize_amount(self, amount_str: str) -> float:
        """Normalize currency amounts to float"""
        # Remove currency symbols and commas
        cleaned = re.sub(r'[$,]', '', amount_str)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def detect_confidence_indicators(self, query: str) -> str:
        """Detect language suggesting desired confidence level"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["audit", "defensible", "conservative", "safe"]):
            return "DEFENSIBLE"
        elif any(word in query_lower for word in ["aggressive", "favorable", "maximize"]):
            return "AGGRESSIVE"
        elif any(word in query_lower for word in ["disclosure", "reportable", "risky"]):
            return "DISCLOSURE"
        elif any(word in query_lower for word in ["high risk", "uncertain", "novel"]):
            return "HIGH_RISK"

        return "DEFENSIBLE"  # Default to conservative
