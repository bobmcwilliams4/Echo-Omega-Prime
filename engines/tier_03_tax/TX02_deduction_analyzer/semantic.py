"""
TX02 Deduction Analyzer — Semantic Normalization

Domain-specific term normalization for tax deduction analysis.
Ensures consistent doctrine matching across varied query phrasings.
"""

from __future__ import annotations

import re
from typing import Dict, List, Set

from loguru import logger


# ═══════════════════════════════════════════════════════════════════
# DEDUCTION-SPECIFIC NORMALIZATION MAPS
# ═══════════════════════════════════════════════════════════════════

IRC_SECTION_ALIASES = {
    "section 162": "§162",
    "irc 162": "§162",
    "code section 162": "§162",
    "internal revenue code 162": "§162",
    "163": "§163",
    "163j": "§163(j)",
    "business interest limitation": "§163(j)",
    "164": "§164",
    "salt": "§164",
    "salt cap": "§164",
    "state and local tax": "§164",
    "165": "§165",
    "casualty loss": "§165",
    "167": "§167",
    "168": "§168",
    "macrs": "§168",
    "depreciation": "§168",
    "170": "§170",
    "charitable contribution": "§170",
    "179": "§179",
    "expensing": "§179",
    "section 179": "§179",
    "195": "§195",
    "startup costs": "§195",
    "199a": "§199A",
    "qbi": "§199A",
    "qualified business income": "§199A",
    "212": "§212",
    "investment expenses": "§212",
    "213": "§213",
    "medical expenses": "§213",
    "217": "§217",
    "moving expenses": "§217",
    "280a": "§280A",
    "home office": "§280A",
    "280e": "§280E",
    "cannabis": "§280E",
    "marijuana": "§280E",
    "461l": "§461(l)",
    "excess business loss": "§461(l)",
    "469": "§469",
    "passive loss": "§469",
    "passive activity": "§469",
    "267": "§267",
    "related party": "§267",
}

DEDUCTION_CONCEPT_MAP = {
    "business expense": "ordinary_and_necessary_business_expense",
    "ordinary and necessary": "ordinary_and_necessary_business_expense",
    "trade or business": "trade_or_business_requirement",
    "capital expenditure": "capital_vs_expense",
    "repair vs improvement": "capital_vs_expense",
    "betterment": "capital_vs_expense",
    "restoration": "capital_vs_expense",
    "interest deduction": "interest_deduction_rules",
    "mortgage interest": "qualified_residence_interest",
    "home equity": "qualified_residence_interest",
    "business interest": "§163(j)_limitation",
    "30 percent": "§163(j)_limitation",
    "ati": "adjusted_taxable_income",
    "ebitda": "adjusted_taxable_income",
    "ebit": "adjusted_taxable_income",
    "salt deduction": "state_local_tax_deduction",
    "$10000 cap": "salt_cap",
    "property tax": "real_property_tax",
    "income tax": "state_income_tax",
    "casualty": "casualty_loss",
    "theft": "theft_loss",
    "federally declared disaster": "federal_disaster_declaration",
    "depreciation": "depreciation_deduction",
    "macrs": "modified_accelerated_cost_recovery",
    "gds": "general_depreciation_system",
    "ads": "alternative_depreciation_system",
    "bonus depreciation": "§168(k)_bonus_depreciation",
    "100 percent": "§168(k)_bonus_depreciation",
    "recovery period": "macrs_recovery_period",
    "charitable": "charitable_contribution",
    "donation": "charitable_contribution",
    "501c3": "qualified_charity",
    "60 percent": "cash_contribution_limit",
    "30 percent": "capital_gain_property_limit",
    "substantiation": "charitable_substantiation",
    "quid pro quo": "quid_pro_quo_disclosure",
    "section 179": "immediate_expensing",
    "expensing election": "§179_election",
    "startup": "startup_expenditures",
    "organizational costs": "organizational_expenditures",
    "$5000": "startup_first_year_deduction",
    "qbi deduction": "qualified_business_income_deduction",
    "20 percent": "§199A_deduction",
    "sstb": "specified_service_trade_business",
    "w-2 wages": "w2_wage_limitation",
    "ubia": "unadjusted_basis_qualified_property",
    "medical": "medical_expense_deduction",
    "7.5 percent": "medical_expense_floor",
    "moving": "moving_expense_deduction",
    "home office": "home_office_deduction",
    "principal place of business": "home_office_requirements",
    "cannabis deduction": "§280E_limitation",
    "marijuana business": "§280E_limitation",
    "excess business loss": "§461(l)_limitation",
    "passive activity loss": "passive_loss_rules",
    "real estate professional": "real_estate_professional_exception",
    "related party": "related_party_limitation",
    "constructive ownership": "attribution_rules",
}

TCJA_TERMS = {
    "tax cuts and jobs act": "tcja",
    "tcja": "tcja_2017",
    "tax reform": "tcja_2017",
    "2017 tax act": "tcja_2017",
    "suspended 2018": "tcja_suspension",
    "suspended through 2025": "tcja_suspension",
    "sunset 2025": "tcja_sunset",
    "temporary provision": "tcja_temporary",
}

ENTITY_TYPE_NORMALIZATION = {
    "s corporation": "s_corp",
    "s-corp": "s_corp",
    "s corp": "s_corp",
    "scorp": "s_corp",
    "c corporation": "c_corp",
    "c-corp": "c_corp",
    "c corp": "c_corp",
    "ccorp": "c_corp",
    "partnership": "partnership",
    "llc": "llc_entity",
    "limited liability company": "llc_entity",
    "sole proprietorship": "sole_prop",
    "sole prop": "sole_prop",
    "schedule c": "schedule_c_business",
    "individual": "individual_taxpayer",
}

POSITION_ZONE_TERMS = {
    "planning": "PLANNING",
    "tax planning": "PLANNING",
    "prospective": "PLANNING",
    "return": "REPORTING",
    "reporting": "REPORTING",
    "filing": "REPORTING",
    "compliance": "REPORTING",
    "audit": "AUDIT",
    "examination": "AUDIT",
    "irs challenge": "AUDIT",
    "controversy": "AUDIT",
}


# ═══════════════════════════════════════════════════════════════════
# SEMANTIC NORMALIZER
# ═══════════════════════════════════════════════════════════════════

class SemanticNormalizer:
    """
    Normalize tax deduction query text for consistent doctrine matching.

    Transformations:
        - IRC section notation (§162, IRC 162 → §162)
        - Deduction concept mapping (business expense → ordinary_and_necessary)
        - TCJA terminology (tax reform → tcja_2017)
        - Entity type standardization (S-Corp → s_corp)
        - Position zone detection (audit, planning, reporting)
    """

    def __init__(self) -> None:
        self._irc_pattern = re.compile(
            r'\b(?:section|irc|code section|internal revenue code)?\s*(\d{1,4})([a-z]|\([a-z0-9]+\))?\b',
            re.IGNORECASE
        )
        self._stopwords: Set[str] = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "be", "been",
        }

    def normalize(self, query: str) -> str:
        """Full normalization pipeline."""
        text = query.lower()

        # IRC section notation
        text = self._normalize_irc_sections(text)

        # Apply all normalization maps
        text = self._apply_map(text, IRC_SECTION_ALIASES)
        text = self._apply_map(text, DEDUCTION_CONCEPT_MAP)
        text = self._apply_map(text, TCJA_TERMS)
        text = self._apply_map(text, ENTITY_TYPE_NORMALIZATION)

        # Remove stopwords
        text = self._remove_stopwords(text)

        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        logger.debug(f"Normalized: '{query[:50]}...' → '{text[:50]}...'")
        return text

    def _normalize_irc_sections(self, text: str) -> str:
        """Convert IRC section references to § notation."""
        def replacer(match):
            section_num = match.group(1)
            subsection = match.group(2) or ""
            return f"§{section_num}{subsection}"

        return self._irc_pattern.sub(replacer, text)

    def _apply_map(self, text: str, mapping: Dict[str, str]) -> str:
        """Apply term mapping with whole-word matching."""
        for term, replacement in mapping.items():
            pattern = r'\b' + re.escape(term) + r'\b'
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def _remove_stopwords(self, text: str) -> str:
        """Remove common stopwords (preserves domain terms)."""
        words = text.split()
        filtered = [w for w in words if w not in self._stopwords or len(w) <= 2]
        return ' '.join(filtered)

    def extract_irc_sections(self, query: str) -> List[str]:
        """Extract all IRC section references from query."""
        normalized = self.normalize(query)
        sections = re.findall(r'§\d{1,4}(?:[a-z]|\([a-z0-9]+\))?', normalized)
        return list(set(sections))

    def detect_position_zone(self, query: str) -> str:
        """Detect position zone (PLANNING, REPORTING, AUDIT) from query."""
        text = query.lower()
        for term, zone in POSITION_ZONE_TERMS.items():
            if term in text:
                return zone
        return "REPORTING"  # Default to reporting if ambiguous

    def extract_entity_types(self, query: str) -> List[str]:
        """Extract entity types mentioned in query."""
        text = query.lower()
        entities = []
        for term, normalized in ENTITY_TYPE_NORMALIZATION.items():
            if term in text and normalized not in entities:
                entities.append(normalized)
        return entities

    def is_tcja_related(self, query: str) -> bool:
        """Check if query involves TCJA provisions."""
        text = query.lower()
        return any(term in text for term in TCJA_TERMS.keys())


# ═══════════════════════════════════════════════════════════════════
# MODULE SINGLETON
# ═══════════════════════════════════════════════════════════════════

_normalizer: SemanticNormalizer | None = None


def get_normalizer() -> SemanticNormalizer:
    """Get or create module-level normalizer singleton."""
    global _normalizer
    if _normalizer is None:
        _normalizer = SemanticNormalizer()
    return _normalizer


def normalize_query(query: str) -> str:
    """Convenience function for normalization."""
    return get_normalizer().normalize(query)
