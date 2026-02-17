"""
P05 Creditor Claim Engine - Semantic Normalization
Domain-specific term normalization for creditor claim analysis
"""

from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import re
from loguru import logger


@dataclass
class NormalizationRule:
    """Rule for normalizing creditor claim terminology"""
    pattern: str
    canonical: str
    category: str
    aliases: List[str]


class CreditorClaimSemanticNormalizer:
    """Normalize creditor claim terminology to canonical forms"""

    def __init__(self):
        self.normalization_map: Dict[str, str] = {}
        self.category_map: Dict[str, str] = {}
        self.phrase_patterns: List[Tuple[re.Pattern, str]] = []

        self._initialize_rules()
        logger.info("Creditor claim semantic normalizer initialized")

    def _initialize_rules(self) -> None:
        """Initialize normalization rules for creditor claims"""

        rules = [
            # Claim types
            NormalizationRule(
                pattern=r"\b(secured\s+claim|security\s+interest|lien\s+holder|mortgage\s+claim)\b",
                canonical="SECURED_CLAIM",
                category="claim_type",
                aliases=["secured claim", "security interest", "lien holder", "mortgage claim", "deed of trust claim"]
            ),
            NormalizationRule(
                pattern=r"\b(unsecured\s+claim|general\s+claim|credit\s+card|unsecured\s+debt)\b",
                canonical="UNSECURED_CLAIM",
                category="claim_type",
                aliases=["unsecured claim", "general claim", "credit card debt", "unsecured debt", "general unsecured"]
            ),
            NormalizationRule(
                pattern=r"\b(priority\s+claim|class\s+1|administration\s+expense)\b",
                canonical="PRIORITY_CLAIM",
                category="claim_type",
                aliases=["priority claim", "class 1", "administration expense", "preferred claim"]
            ),
            NormalizationRule(
                pattern=r"\b(contingent\s+claim|unliquidated|disputed\s+claim)\b",
                canonical="CONTINGENT_CLAIM",
                category="claim_type",
                aliases=["contingent claim", "unliquidated claim", "disputed claim", "unmatured claim"]
            ),

            # Exemptions
            NormalizationRule(
                pattern=r"\b(homestead|homestead\s+exemption|protected\s+homestead)\b",
                canonical="HOMESTEAD_EXEMPTION",
                category="exemption",
                aliases=["homestead", "homestead exemption", "protected homestead", "homestead property"]
            ),
            NormalizationRule(
                pattern=r"\b(exempt\s+property|personal\s+property\s+exemption|exempt\s+assets)\b",
                canonical="EXEMPT_PROPERTY",
                category="exemption",
                aliases=["exempt property", "exempt assets", "personal property exemption", "protected property"]
            ),
            NormalizationRule(
                pattern=r"\b(family\s+allowance|year\'?s?\s+support|spousal\s+allowance)\b",
                canonical="FAMILY_ALLOWANCE",
                category="exemption",
                aliases=["family allowance", "year's support", "spousal allowance", "family support"]
            ),

            # Procedures
            NormalizationRule(
                pattern=r"\b(notice\s+to\s+creditors|creditor\s+notice|publication)\b",
                canonical="NOTICE_TO_CREDITORS",
                category="procedure",
                aliases=["notice to creditors", "creditor notice", "publication notice", "formal notice"]
            ),
            NormalizationRule(
                pattern=r"\b(proof\s+of\s+claim|claim\s+filing|verified\s+claim)\b",
                canonical="PROOF_OF_CLAIM",
                category="procedure",
                aliases=["proof of claim", "claim filing", "verified claim", "sworn claim"]
            ),
            NormalizationRule(
                pattern=r"\b(statute\s+of\s+limitations?|time\s+bar|nonclaim\s+statute)\b",
                canonical="STATUTE_OF_LIMITATIONS",
                category="procedure",
                aliases=["statute of limitations", "limitation period", "nonclaim statute", "time bar", "claim deadline"]
            ),
            NormalizationRule(
                pattern=r"\b(claim\s+rejection|rejected\s+claim|disallowed\s+claim)\b",
                canonical="REJECTED_CLAIM",
                category="procedure",
                aliases=["rejected claim", "disallowed claim", "claim rejection", "denied claim"]
            ),

            # Priority categories
            NormalizationRule(
                pattern=r"\b(funeral\s+expense|burial\s+cost|interment)\b",
                canonical="FUNERAL_EXPENSE",
                category="priority",
                aliases=["funeral expense", "burial cost", "interment cost", "funeral bill"]
            ),
            NormalizationRule(
                pattern=r"\b(last\s+illness|final\s+illness|medical\s+expense|hospital\s+bill)\b",
                canonical="LAST_ILLNESS_EXPENSE",
                category="priority",
                aliases=["last illness", "final illness", "medical expenses", "hospital bills", "healthcare costs"]
            ),
            NormalizationRule(
                pattern=r"\b(administration\s+expense|executor\s+fee|attorney\s+fee)\b",
                canonical="ADMINISTRATION_EXPENSE",
                category="priority",
                aliases=["administration expense", "executor fee", "attorney fees", "court costs", "probate costs"]
            ),
            NormalizationRule(
                pattern=r"\b(federal\s+tax|IRS|tax\s+lien|income\s+tax)\b",
                canonical="FEDERAL_TAX_CLAIM",
                category="priority",
                aliases=["federal tax", "IRS claim", "tax lien", "income tax", "estate tax"]
            ),

            # Creditor actions
            NormalizationRule(
                pattern=r"\b(foreclosure|foreclose|deed\s+of\s+trust\s+sale)\b",
                canonical="FORECLOSURE",
                category="creditor_action",
                aliases=["foreclosure", "foreclose", "deed of trust sale", "non-judicial foreclosure"]
            ),
            NormalizationRule(
                pattern=r"\b(set-?off|setoff|offset|mutual\s+debt)\b",
                canonical="SET_OFF",
                category="creditor_action",
                aliases=["set-off", "setoff", "offset", "mutual debt", "recoupment"]
            ),
            NormalizationRule(
                pattern=r"\b(subrogation|subrogate|subrogee)\b",
                canonical="SUBROGATION",
                category="creditor_action",
                aliases=["subrogation", "subrogate", "subrogee", "subrogation rights"]
            ),

            # Estate types
            NormalizationRule(
                pattern=r"\b(independent\s+administr|independent\s+execut)\b",
                canonical="INDEPENDENT_ADMINISTRATION",
                category="estate_type",
                aliases=["independent administration", "independent executor", "iaea", "independent admin"]
            ),
            NormalizationRule(
                pattern=r"\b(dependent\s+administr|court\s+supervised|supervised\s+estate)\b",
                canonical="DEPENDENT_ADMINISTRATION",
                category="estate_type",
                aliases=["dependent administration", "court supervised", "supervised estate", "dependent admin"]
            ),

            # Time periods
            NormalizationRule(
                pattern=r"\b(four[- ]month|4[- ]month|120[- ]day)\b",
                canonical="FOUR_MONTH_PERIOD",
                category="time_period",
                aliases=["four month", "4 month", "120 day", "four-month period"]
            ),
            NormalizationRule(
                pattern=r"\b(six[- ]month|6[- ]month|180[- ]day)\b",
                canonical="SIX_MONTH_PERIOD",
                category="time_period",
                aliases=["six month", "6 month", "180 day", "six-month period"]
            ),
            NormalizationRule(
                pattern=r"\b(two[- ]year|2[- ]year|statute\s+of\s+nonclaim)\b",
                canonical="TWO_YEAR_NONCLAIM",
                category="time_period",
                aliases=["two year", "2 year", "statute of nonclaim", "two-year statute"]
            ),

            # Documentation
            NormalizationRule(
                pattern=r"\b(affidavit|sworn\s+statement|verification|notarized)\b",
                canonical="SWORN_VERIFICATION",
                category="documentation",
                aliases=["affidavit", "sworn statement", "verification", "notarized statement", "oath"]
            ),
            NormalizationRule(
                pattern=r"\b(claim\s+form|proof\s+form|creditor\s+form)\b",
                canonical="CLAIM_FORM",
                category="documentation",
                aliases=["claim form", "proof of claim form", "creditor form", "standard form"]
            ),

            # Legal standards
            NormalizationRule(
                pattern=r"\b(matured\s+claim|due\s+and\s+owing|liquidated)\b",
                canonical="MATURED_CLAIM",
                category="legal_standard",
                aliases=["matured claim", "due and owing", "liquidated claim", "enforceable debt"]
            ),
            NormalizationRule(
                pattern=r"\b(permissive\s+claim|tort\s+claim|wrongful\s+death)\b",
                canonical="PERMISSIVE_CLAIM",
                category="legal_standard",
                aliases=["permissive claim", "tort claim", "wrongful death", "personal injury"]
            ),
            NormalizationRule(
                pattern=r"\b(statutory\s+claim|class\s+8|preferences?)\b",
                canonical="STATUTORY_CLAIM",
                category="legal_standard",
                aliases=["statutory claim", "class 8", "preference", "statutory preference"]
            ),
        ]

        # Build normalization map and phrase patterns
        for rule in rules:
            # Compile regex pattern
            pattern = re.compile(rule.pattern, re.IGNORECASE)
            self.phrase_patterns.append((pattern, rule.canonical))

            # Map aliases to canonical
            for alias in rule.aliases:
                normalized_alias = alias.lower().strip()
                self.normalization_map[normalized_alias] = rule.canonical
                self.category_map[normalized_alias] = rule.category

    def normalize_query(self, query: str) -> str:
        """Normalize a query to use canonical terms"""
        normalized = query

        # Apply phrase patterns
        for pattern, canonical in self.phrase_patterns:
            normalized = pattern.sub(canonical, normalized)

        # Additional cleanup
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        logger.debug(f"Normalized query: '{query}' -> '{normalized}'")
        return normalized

    def extract_claim_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract and categorize creditor claim entities from text"""
        entities: Dict[str, List[str]] = {
            "claim_types": [],
            "exemptions": [],
            "procedures": [],
            "priorities": [],
            "creditor_actions": [],
            "estate_types": [],
            "time_periods": [],
            "legal_standards": []
        }

        text_lower = text.lower()

        # Check each alias
        for alias, canonical in self.normalization_map.items():
            if alias in text_lower:
                category = self.category_map[alias]
                if canonical not in entities.get(category + "s", entities.get(category, [])):
                    category_key = category if category.endswith('s') else category + 's'
                    if category_key not in entities:
                        category_key = category
                    if category_key in entities:
                        entities[category_key].append(canonical)

        return {k: v for k, v in entities.items() if v}

    def get_canonical_term(self, term: str) -> str:
        """Get canonical form of a term"""
        term_lower = term.lower().strip()
        return self.normalization_map.get(term_lower, term)

    def identify_claim_category(self, text: str) -> List[str]:
        """Identify claim categories mentioned in text"""
        categories = set()
        text_lower = text.lower()

        category_keywords = {
            "SECURED_CLAIM": ["secured", "mortgage", "lien", "deed of trust", "security interest"],
            "UNSECURED_CLAIM": ["unsecured", "credit card", "general claim", "general unsecured"],
            "PRIORITY_CLAIM": ["priority", "class 1", "preferred"],
            "ADMINISTRATION_EXPENSE": ["administration", "executor fee", "attorney fee", "court costs"],
            "FUNERAL_EXPENSE": ["funeral", "burial", "interment"],
            "LAST_ILLNESS_EXPENSE": ["last illness", "medical", "hospital", "healthcare"],
            "FAMILY_ALLOWANCE": ["family allowance", "year's support", "spousal allowance"],
            "EXEMPT_PROPERTY": ["exempt property", "homestead", "personal property exemption"],
            "CONTINGENT_CLAIM": ["contingent", "unliquidated", "disputed"],
            "FEDERAL_TAX": ["federal tax", "irs", "tax lien"],
        }

        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.add(category)

        return list(categories)

    def expand_query_terms(self, query: str) -> List[str]:
        """Expand query with related terms for better semantic matching"""
        expanded = [query]
        query_lower = query.lower()

        # Add canonical forms
        for alias, canonical in self.normalization_map.items():
            if alias in query_lower and canonical not in expanded:
                expanded.append(canonical)

        return expanded
