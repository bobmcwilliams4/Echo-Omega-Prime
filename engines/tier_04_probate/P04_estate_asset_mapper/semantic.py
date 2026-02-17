"""
P04 Estate Asset Mapper - Semantic Normalization
Domain-specific term normalization for estate planning and asset classification.
"""

from typing import Dict, List, Set
import re


class EstateSemanticNormalizer:
    """
    Normalize estate planning and asset classification terminology.
    Ensures deterministic query interpretation regardless of phrasing.
    """

    def __init__(self):
        # ═══════════════════════════════════════════════════════════════════
        # SYNONYM MAPS - Estate Planning Domain
        # ═══════════════════════════════════════════════════════════════════

        self.gross_estate_synonyms = {
            "gross estate", "estate property", "includible property", "taxable estate",
            "property subject to estate tax", "estate assets", "decedent's property"
        }

        self.fair_market_value_synonyms = {
            "fair market value", "fmv", "market value", "appraised value", "valuation",
            "estate value", "worth", "date of death value"
        }

        self.community_property_synonyms = {
            "community property", "marital property", "community assets",
            "property acquired during marriage", "spousal property"
        }

        self.separate_property_synonyms = {
            "separate property", "individual property", "sole property",
            "property owned before marriage", "inherited property", "gift property"
        }

        self.life_estate_synonyms = {
            "life estate", "life interest", "life tenancy", "retained life interest",
            "right to use for life", "lifetime possession"
        }

        self.remainder_interest_synonyms = {
            "remainder", "remainder interest", "future interest", "reversionary interest",
            "contingent interest", "vested remainder"
        }

        self.joint_tenancy_synonyms = {
            "joint tenancy", "joint ownership", "jtwros", "joint tenants with right of survivorship",
            "co-ownership with survivorship"
        }

        self.tenancy_in_common_synonyms = {
            "tenancy in common", "tic", "co-ownership", "undivided interest",
            "fractional ownership", "co-tenant"
        }

        self.power_of_appointment_synonyms = {
            "power of appointment", "poa", "general power", "special power",
            "limited power", "right to designate beneficiaries"
        }

        self.qtip_synonyms = {
            "qtip", "qualified terminable interest property", "qtip trust",
            "marital trust", "marital deduction trust"
        }

        self.irrevocable_trust_synonyms = {
            "irrevocable trust", "non-revocable trust", "fixed trust",
            "trust that cannot be changed", "permanent trust"
        }

        self.revocable_trust_synonyms = {
            "revocable trust", "living trust", "inter vivos trust", "amendable trust",
            "trust that can be changed", "grantor trust"
        }

        self.life_insurance_synonyms = {
            "life insurance", "life insurance policy", "death benefit",
            "insurance proceeds", "policy proceeds", "insurance payout"
        }

        self.incidents_of_ownership_synonyms = {
            "incidents of ownership", "ownership powers", "policy control",
            "right to change beneficiary", "right to borrow", "ownership rights"
        }

        self.closely_held_business_synonyms = {
            "closely held business", "private company", "family business",
            "non-public company", "privately owned entity", "closely held stock"
        }

        self.flp_synonyms = {
            "flp", "family limited partnership", "limited partnership",
            "family partnership", "lp"
        }

        self.llc_synonyms = {
            "llc", "limited liability company", "company", "entity"
        }

        self.mineral_interest_synonyms = {
            "mineral interest", "mineral rights", "oil and gas interest",
            "royalty interest", "working interest", "subsurface rights"
        }

        self.discount_synonyms = {
            "discount", "valuation discount", "reduction", "adjustment",
            "markdown", "decrease in value"
        }

        self.lack_of_marketability_synonyms = {
            "lack of marketability", "marketability discount", "dlom",
            "illiquidity discount", "no ready market", "restricted transferability"
        }

        self.lack_of_control_synonyms = {
            "lack of control", "control discount", "dloc", "minority discount",
            "minority interest discount", "non-controlling interest"
        }

        self.fractional_interest_synonyms = {
            "fractional interest", "undivided interest", "partial ownership",
            "co-ownership interest", "shared ownership"
        }

        self.partition_synonyms = {
            "partition", "division", "split", "forced sale", "partition action",
            "court-ordered division"
        }

        self.special_use_valuation_synonyms = {
            "special use valuation", "2032a", "farm valuation", "ranch valuation",
            "agricultural use valuation", "reduced valuation"
        }

        self.alternate_valuation_synonyms = {
            "alternate valuation", "2032", "six month valuation", "alternate date",
            "post-death valuation"
        }

        self.material_participation_synonyms = {
            "material participation", "active involvement", "regular participation",
            "substantial participation", "hands-on management"
        }

        self.qualified_heir_synonyms = {
            "qualified heir", "family member", "eligible heir", "lineal descendant",
            "spouse or child"
        }

        # ═══════════════════════════════════════════════════════════════════
        # CANONICAL TERM MAPPING
        # ═══════════════════════════════════════════════════════════════════

        self.canonical_map: Dict[str, str] = {}

        # Build reverse map: synonym → canonical term
        synonym_sets = [
            (self.gross_estate_synonyms, "gross_estate"),
            (self.fair_market_value_synonyms, "fair_market_value"),
            (self.community_property_synonyms, "community_property"),
            (self.separate_property_synonyms, "separate_property"),
            (self.life_estate_synonyms, "life_estate"),
            (self.remainder_interest_synonyms, "remainder_interest"),
            (self.joint_tenancy_synonyms, "joint_tenancy"),
            (self.tenancy_in_common_synonyms, "tenancy_in_common"),
            (self.power_of_appointment_synonyms, "power_of_appointment"),
            (self.qtip_synonyms, "qtip_property"),
            (self.irrevocable_trust_synonyms, "irrevocable_trust"),
            (self.revocable_trust_synonyms, "revocable_trust"),
            (self.life_insurance_synonyms, "life_insurance"),
            (self.incidents_of_ownership_synonyms, "incidents_of_ownership"),
            (self.closely_held_business_synonyms, "closely_held_business"),
            (self.flp_synonyms, "family_limited_partnership"),
            (self.llc_synonyms, "limited_liability_company"),
            (self.mineral_interest_synonyms, "mineral_interest"),
            (self.discount_synonyms, "valuation_discount"),
            (self.lack_of_marketability_synonyms, "lack_of_marketability_discount"),
            (self.lack_of_control_synonyms, "lack_of_control_discount"),
            (self.fractional_interest_synonyms, "fractional_interest"),
            (self.partition_synonyms, "partition"),
            (self.special_use_valuation_synonyms, "special_use_valuation"),
            (self.alternate_valuation_synonyms, "alternate_valuation_date"),
            (self.material_participation_synonyms, "material_participation"),
            (self.qualified_heir_synonyms, "qualified_heir"),
        ]

        for synonym_set, canonical in synonym_sets:
            for synonym in synonym_set:
                self.canonical_map[synonym.lower()] = canonical

        # ═══════════════════════════════════════════════════════════════════
        # IRC SECTION NORMALIZATION
        # ═══════════════════════════════════════════════════════════════════

        self.irc_section_patterns = {
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2031\b': 'irc_2031',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2032\b': 'irc_2032',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2032a\b': 'irc_2032a',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2033\b': 'irc_2033',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2034\b': 'irc_2034',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2035\b': 'irc_2035',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2036\b': 'irc_2036',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2037\b': 'irc_2037',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2038\b': 'irc_2038',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2039\b': 'irc_2039',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2040\b': 'irc_2040',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2041\b': 'irc_2041',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2042\b': 'irc_2042',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2043\b': 'irc_2043',
            r'\b(?:irc\s*)?(?:§|section|sec\.?)\s*2044\b': 'irc_2044',
        }

        # ═══════════════════════════════════════════════════════════════════
        # ENTITY TYPE NORMALIZATION
        # ═══════════════════════════════════════════════════════════════════

        self.entity_type_map = {
            "c corporation": "c_corporation",
            "c corp": "c_corporation",
            "c-corp": "c_corporation",
            "corporation": "c_corporation",
            "s corporation": "s_corporation",
            "s corp": "s_corporation",
            "s-corp": "s_corporation",
            "llc": "limited_liability_company",
            "limited liability company": "limited_liability_company",
            "partnership": "general_partnership",
            "general partnership": "general_partnership",
            "limited partnership": "limited_partnership",
            "lp": "limited_partnership",
            "flp": "family_limited_partnership",
            "family limited partnership": "family_limited_partnership",
            "sole proprietorship": "sole_proprietorship",
            "trust": "trust_entity",
            "estate": "estate_entity",
        }

        # ═══════════════════════════════════════════════════════════════════
        # PROPERTY TYPE NORMALIZATION
        # ═══════════════════════════════════════════════════════════════════

        self.property_type_map = {
            "real property": "real_property",
            "real estate": "real_property",
            "land": "real_property",
            "personal property": "personal_property",
            "tangible personal property": "tangible_personal_property",
            "intangible personal property": "intangible_personal_property",
            "stock": "publicly_traded_stock",
            "publicly traded stock": "publicly_traded_stock",
            "closely held stock": "closely_held_stock",
            "bonds": "bonds",
            "bank accounts": "bank_accounts",
            "cash": "cash",
            "mineral interest": "mineral_interest",
            "oil and gas": "mineral_interest",
            "business interest": "business_interest",
            "life insurance": "life_insurance",
            "annuity": "annuity",
            "retirement account": "retirement_account",
            "ira": "retirement_account",
            "401k": "retirement_account",
        }

    def normalize(self, text: str) -> str:
        """
        Normalize estate planning terminology in query text.
        Returns text with canonical terms substituted.
        """
        text_lower = text.lower()

        # Normalize IRC sections first
        for pattern, canonical in self.irc_section_patterns.items():
            text_lower = re.sub(pattern, canonical, text_lower, flags=re.IGNORECASE)

        # Normalize multi-word phrases (longest first to avoid partial matches)
        sorted_synonyms = sorted(self.canonical_map.keys(), key=len, reverse=True)
        for synonym in sorted_synonyms:
            if synonym in text_lower:
                canonical = self.canonical_map[synonym]
                # Replace whole word only (avoid partial matches)
                pattern = r'\b' + re.escape(synonym) + r'\b'
                text_lower = re.sub(pattern, canonical, text_lower)

        # Normalize entity types
        for entity_phrase, canonical in self.entity_type_map.items():
            pattern = r'\b' + re.escape(entity_phrase) + r'\b'
            text_lower = re.sub(pattern, canonical, text_lower, flags=re.IGNORECASE)

        # Normalize property types
        for property_phrase, canonical in self.property_type_map.items():
            pattern = r'\b' + re.escape(property_phrase) + r'\b'
            text_lower = re.sub(pattern, canonical, text_lower, flags=re.IGNORECASE)

        return text_lower

    def extract_irc_sections(self, text: str) -> List[str]:
        """Extract all IRC section references from text."""
        sections = []
        for pattern, canonical in self.irc_section_patterns.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                sections.append(canonical)
        return list(set(sections))

    def extract_entity_types(self, text: str) -> List[str]:
        """Extract all entity type mentions from text."""
        text_lower = text.lower()
        found_entities = []
        for entity_phrase, canonical in self.entity_type_map.items():
            if entity_phrase in text_lower:
                found_entities.append(canonical)
        return list(set(found_entities))

    def extract_property_types(self, text: str) -> List[str]:
        """Extract all property type mentions from text."""
        text_lower = text.lower()
        found_properties = []
        for property_phrase, canonical in self.property_type_map.items():
            if property_phrase in text_lower:
                found_properties.append(canonical)
        return list(set(found_properties))

    def is_inclusion_query(self, text: str) -> bool:
        """Detect if query is about property inclusion in gross estate."""
        inclusion_indicators = [
            "include", "includible", "part of estate", "gross estate",
            "subject to estate tax", "taxable", "estate property"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in inclusion_indicators)

    def is_valuation_query(self, text: str) -> bool:
        """Detect if query is about property valuation."""
        valuation_indicators = [
            "value", "valuation", "worth", "fmv", "fair market value",
            "appraisal", "discount", "appraised"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in valuation_indicators)

    def is_discount_query(self, text: str) -> bool:
        """Detect if query is about valuation discounts."""
        discount_indicators = [
            "discount", "dlom", "dloc", "lack of control", "lack of marketability",
            "fractional interest", "minority", "blockage"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in discount_indicators)

    def is_community_property_query(self, text: str) -> bool:
        """Detect if query involves community property classification."""
        community_indicators = [
            "community property", "marital property", "separate property",
            "acquired during marriage", "texas", "community vs separate"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in community_indicators)

    def is_retained_interest_query(self, text: str) -> bool:
        """Detect if query involves retained interests (§2036-2038)."""
        retained_indicators = [
            "retained", "life estate", "power to revoke", "power to alter",
            "2036", "2037", "2038", "grantor trust", "revocable"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in retained_indicators)

    def is_special_valuation_query(self, text: str) -> bool:
        """Detect if query involves special use valuation or alternate valuation."""
        special_val_indicators = [
            "special use", "2032a", "alternate valuation", "2032",
            "farm valuation", "ranch valuation", "six month"
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in special_val_indicators)


# ═══════════════════════════════════════════════════════════════════════════
# MODULE-LEVEL SINGLETON
# ═══════════════════════════════════════════════════════════════════════════

_normalizer_instance = None


def get_normalizer() -> EstateSemanticNormalizer:
    """Get singleton normalizer instance."""
    global _normalizer_instance
    if _normalizer_instance is None:
        _normalizer_instance = EstateSemanticNormalizer()
    return _normalizer_instance
