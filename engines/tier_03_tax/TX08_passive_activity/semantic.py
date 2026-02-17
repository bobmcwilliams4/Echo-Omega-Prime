"""
TX08 Passive Activity Loss - Semantic Normalization
Domain-specific term normalization for IRC §469 queries
"""

from typing import Dict, Set, List
import re


class PassiveActivitySemanticNormalizer:
    """Normalize passive activity terminology for consistent doctrine matching."""

    def __init__(self):
        self.term_map = self._build_term_map()
        self.stop_words = self._build_stop_words()
        self.phrase_patterns = self._build_phrase_patterns()

    def _build_term_map(self) -> Dict[str, str]:
        """Build semantic equivalence map for passive activity terms."""
        return {
            # Material participation synonyms
            "materially participate": "material_participation",
            "material participation": "material_participation",
            "materially participated": "material_participation",
            "substantial participation": "material_participation",
            "regular continuous substantial": "material_participation",
            "500 hour test": "material_participation_test_1",
            "500 hours": "material_participation_test_1",
            "test 1": "material_participation_test_1",
            "substantially all test": "material_participation_test_2",
            "test 2": "material_participation_test_2",
            "100 hours not less than": "material_participation_test_3",
            "test 3": "material_participation_test_3",
            "significant participation": "material_participation_test_4",
            "test 4": "material_participation_test_4",
            "spa": "significant_participation_activity",
            "5 of 10 years": "material_participation_test_5",
            "test 5": "material_participation_test_5",
            "personal service activity": "material_participation_test_6",
            "test 6": "material_participation_test_6",
            "facts and circumstances": "material_participation_test_7",
            "test 7": "material_participation_test_7",

            # Rental activity terms
            "rental": "rental_activity",
            "rental activity": "rental_activity",
            "rental real estate": "rental_real_estate",
            "rental property": "rental_activity",
            "per se passive": "per_se_passive",
            "rental personal property": "rental_personal_property",
            "7 day rule": "average_period_7_days",
            "30 day rule": "average_period_30_days",
            "extraordinary services": "extraordinary_personal_services",
            "significant services": "significant_personal_services",

            # Real estate professional
            "real estate professional": "real_estate_professional_469c7",
            "rep": "real_estate_professional_469c7",
            "750 hour": "real_estate_professional_750_hours",
            "750 hours": "real_estate_professional_750_hours",
            "more than half": "real_estate_professional_50_percent",
            "greater than 50%": "real_estate_professional_50_percent",
            "real property trade or business": "real_property_trade_business",
            "rptob": "real_property_trade_business",

            # Active participation
            "active participation": "active_participation",
            "actively participate": "active_participation",
            "actively participated": "active_participation",
            "25000 allowance": "active_participation_25k_allowance",
            "$25,000 allowance": "active_participation_25k_allowance",
            "$25k allowance": "active_participation_25k_allowance",
            "25k allowance": "active_participation_25k_allowance",
            "agi phaseout": "agi_phaseout_100k_150k",
            "100k phaseout": "agi_phaseout_100k_150k",

            # Grouping
            "grouping": "grouping_of_activities",
            "group activities": "grouping_of_activities",
            "appropriate economic unit": "appropriate_economic_unit",
            "regrouping": "regrouping_material_change",
            "regroup": "regrouping_material_change",
            "undertaking": "undertaking_activity_definition",

            # Disposition
            "disposition": "disposition_entire_interest",
            "dispose": "disposition_entire_interest",
            "sale": "disposition_entire_interest",
            "suspended loss": "suspended_passive_loss",
            "suspended losses": "suspended_passive_loss",
            "carryforward": "suspended_passive_loss_carryforward",
            "entire interest": "entire_interest_disposition",
            "fully taxable": "fully_taxable_transaction",
            "installment sale": "installment_sale_469g3",

            # Recharacterization
            "self rental": "self_rental_recharacterization",
            "self-rental": "self_rental_recharacterization",
            "recharacterize": "recharacterization",
            "recharacterization": "recharacterization",
            "portfolio income": "portfolio_income_recharacterization",

            # PTP
            "ptp": "publicly_traded_partnership",
            "publicly traded partnership": "publicly_traded_partnership",
            "master limited partnership": "publicly_traded_partnership",
            "mlp": "publicly_traded_partnership",
            "separate basket": "ptp_separate_basket",

            # NIIT
            "niit": "net_investment_income_tax",
            "net investment income": "net_investment_income_tax",
            "3.8% tax": "net_investment_income_tax",
            "section 1411": "net_investment_income_tax",
            "1411": "net_investment_income_tax",

            # Entity types
            "limited partner": "limited_partner_material_participation",
            "llc member": "llc_member_material_participation",
            "closely held c corp": "closely_held_c_corporation",
            "personal service corporation": "personal_service_corporation",
            "psc": "personal_service_corporation",

            # Working interest
            "working interest": "working_interest_oil_gas",
            "oil and gas": "working_interest_oil_gas",

            # Participation measurement
            "hours": "participation_hours",
            "hour substantiation": "hour_substantiation",
            "time log": "contemporaneous_time_log",
            "contemporaneous record": "contemporaneous_time_log",
            "participation standard": "participation_standard",
            "spouse participation": "spouse_participation_aggregation",

            # Authority
            "469": "irc_469",
            "section 469": "irc_469",
            "reg 1.469-4": "reg_1_469_4_grouping",
            "reg 1.469-5t": "temp_reg_1_469_5t_material_participation",
            "temp reg": "temporary_regulation"
        }

    def _build_stop_words(self) -> Set[str]:
        """Stop words to exclude from semantic analysis."""
        return {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
            "be", "have", "has", "had", "do", "does", "did", "will", "would",
            "should", "could", "may", "might", "must", "can", "shall"
        }

    def _build_phrase_patterns(self) -> List[tuple]:
        """Build regex patterns for multi-word phrase detection."""
        return [
            (r"material\s+participation\s+test\s+(\d+)", r"material_participation_test_\1"),
            (r"(\d+)\s+hour(?:s)?\s+test", r"material_participation_test_\1_hours"),
            (r"real\s+estate\s+professional", "real_estate_professional_469c7"),
            (r"\$?25,?000\s+allowance", "active_participation_25k_allowance"),
            (r"appropriate\s+economic\s+unit", "appropriate_economic_unit"),
            (r"entire\s+interest", "entire_interest_disposition"),
            (r"fully\s+taxable\s+transaction", "fully_taxable_transaction"),
            (r"self[- ]rental", "self_rental_recharacterization"),
            (r"publicly\s+traded\s+partnership", "publicly_traded_partnership"),
            (r"net\s+investment\s+income\s+tax", "net_investment_income_tax"),
            (r"suspended\s+(?:passive\s+)?loss(?:es)?", "suspended_passive_loss"),
            (r"significant\s+participation\s+activity", "significant_participation_activity"),
            (r"rental\s+real\s+estate", "rental_real_estate"),
            (r"working\s+interest", "working_interest_oil_gas")
        ]

    def normalize(self, query: str) -> str:
        """
        Normalize query text for semantic matching.

        Args:
            query: Raw query text

        Returns:
            Normalized query with standardized terminology
        """
        # Convert to lowercase
        normalized = query.lower().strip()

        # Apply phrase patterns first (before tokenization breaks them)
        for pattern, replacement in self.phrase_patterns:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

        # Tokenize
        tokens = re.findall(r'\b\w+\b', normalized)

        # Remove stop words
        tokens = [t for t in tokens if t not in self.stop_words]

        # Apply term map
        normalized_tokens = []
        for token in tokens:
            # Check direct match
            if token in self.term_map:
                normalized_tokens.append(self.term_map[token])
            else:
                # Check if token is part of a phrase in term_map
                matched = False
                for phrase, canonical in self.term_map.items():
                    if token in phrase.split():
                        normalized_tokens.append(canonical)
                        matched = True
                        break
                if not matched:
                    normalized_tokens.append(token)

        # Deduplicate while preserving order
        seen = set()
        deduplicated = []
        for token in normalized_tokens:
            if token not in seen:
                deduplicated.append(token)
                seen.add(token)

        return " ".join(deduplicated)

    def extract_keywords(self, query: str) -> List[str]:
        """
        Extract key domain terms from query.

        Args:
            query: Raw query text

        Returns:
            List of canonical domain keywords
        """
        normalized = self.normalize(query)
        tokens = normalized.split()

        # Filter to domain-specific keywords (from term_map values)
        domain_keywords = set(self.term_map.values())
        keywords = [t for t in tokens if t in domain_keywords]

        return keywords

    def detect_issue_category(self, query: str) -> str:
        """
        Detect primary issue category from query.

        Args:
            query: Raw query text

        Returns:
            Issue category (MATERIAL_PARTICIPATION, RENTAL_ACTIVITY_CLASSIFICATION, etc.)
        """
        normalized = self.normalize(query)

        # Category detection rules (order matters - most specific first)
        if any(term in normalized for term in ["material_participation_test", "500_hours", "substantially_all", "significant_participation_activity"]):
            return "MATERIAL_PARTICIPATION"

        if any(term in normalized for term in ["rental_activity", "per_se_passive", "rental_real_estate", "7_day", "30_day", "extraordinary_services"]):
            return "RENTAL_ACTIVITY_CLASSIFICATION"

        if any(term in normalized for term in ["real_estate_professional_469c7", "750_hours", "real_property_trade_business"]):
            return "MATERIAL_PARTICIPATION"  # Real estate professional enables material participation

        if any(term in normalized for term in ["grouping_of_activities", "appropriate_economic_unit", "regrouping"]):
            return "GROUPING_ELECTIONS"

        if any(term in normalized for term in ["disposition_entire_interest", "suspended_passive_loss", "installment_sale", "fully_taxable"]):
            return "DISPOSITION_RULES"

        if any(term in normalized for term in ["self_rental_recharacterization", "portfolio_income_recharacterization"]):
            return "RECHARACTERIZATION"

        if any(term in normalized for term in ["net_investment_income_tax", "niit", "1411"]):
            return "NIIT_INTERACTION"

        if any(term in normalized for term in ["hour_substantiation", "contemporaneous_time_log"]):
            return "SUBSTANTIATION"

        # Default
        return "MATERIAL_PARTICIPATION"

    def expand_query(self, query: str) -> List[str]:
        """
        Expand query with semantic variants for broader doctrine matching.

        Args:
            query: Raw query text

        Returns:
            List of query variants including synonyms and related terms
        """
        variants = [query]

        # Add normalized version
        normalized = self.normalize(query)
        if normalized != query.lower():
            variants.append(normalized)

        # Add variants based on detected keywords
        keywords = self.extract_keywords(query)

        # Material participation variants
        if "material_participation" in keywords:
            variants.extend([
                "material participation test 1 500 hours",
                "material participation test 2 substantially all",
                "material participation test 3 100 hours",
                "material participation test 4 significant participation",
                "material participation substantiation"
            ])

        # Rental activity variants
        if any(k in keywords for k in ["rental_activity", "rental_real_estate"]):
            variants.extend([
                "rental activity per se passive",
                "rental real estate exceptions",
                "real estate professional 469(c)(7)",
                "active participation $25,000 allowance"
            ])

        # Grouping variants
        if "grouping" in keywords:
            variants.extend([
                "grouping of activities appropriate economic unit",
                "regrouping material change",
                "rental trade or business grouping"
            ])

        # Disposition variants
        if "disposition" in keywords or "suspended" in keywords:
            variants.extend([
                "disposition entire interest suspended losses",
                "installment sale passive loss release",
                "fully taxable transaction 469(g)"
            ])

        return list(set(variants))  # Deduplicate
