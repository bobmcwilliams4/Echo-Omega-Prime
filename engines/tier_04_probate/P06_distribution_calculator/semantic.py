"""
P06_distribution_calculator - Semantic Normalization Module
TIE-20 Component 6: Domain-specific term normalization for estate distribution.
"""

from typing import Dict, List, Set
import re


class SemanticNormalizer:
    """
    Normalize estate distribution terminology to canonical forms.
    Ensures consistent interpretation of will language, beneficiary descriptions, and asset classifications.
    """

    def __init__(self):
        # Bequest type synonyms
        self.bequest_type_map = {
            "specific bequest": "SPECIFIC",
            "specific devise": "SPECIFIC",
            "specific legacy": "SPECIFIC",
            "identified property": "SPECIFIC",
            "particular property": "SPECIFIC",

            "general bequest": "GENERAL",
            "general legacy": "GENERAL",
            "pecuniary bequest": "GENERAL",
            "cash bequest": "GENERAL",
            "dollar amount": "GENERAL",

            "demonstrative legacy": "DEMONSTRATIVE",
            "demonstrative bequest": "DEMONSTRATIVE",
            "from specific fund": "DEMONSTRATIVE",

            "residuary": "RESIDUARY",
            "residue": "RESIDUARY",
            "remainder": "RESIDUARY",
            "rest, residue, remainder": "RESIDUARY",
            "everything else": "RESIDUARY"
        }

        # Property type synonyms
        self.property_type_map = {
            "community": "COMMUNITY",
            "community property": "COMMUNITY",
            "marital property": "COMMUNITY",

            "separate": "SEPARATE",
            "separate property": "SEPARATE",
            "individual property": "SEPARATE",
            "sole property": "SEPARATE",

            "real property": "REAL",
            "real estate": "REAL",
            "realty": "REAL",
            "land": "REAL",
            "immovable property": "REAL",

            "personal property": "PERSONAL",
            "personalty": "PERSONAL",
            "movable property": "PERSONAL",
            "chattels": "PERSONAL"
        }

        # Distribution method synonyms
        self.distribution_method_map = {
            "per stirpes": "PER_STIRPES",
            "by roots": "PER_STIRPES",
            "by stocks": "PER_STIRPES",
            "strict per stirpes": "PER_STIRPES",
            "by right of representation": "PER_STIRPES",

            "per capita at each generation": "PER_CAPITA_EACH_GEN",
            "by representation": "PER_CAPITA_EACH_GEN",
            "modern per stirpes": "PER_CAPITA_EACH_GEN",

            "per capita": "PER_CAPITA",
            "equally": "EQUAL",
            "share and share alike": "EQUAL"
        }

        # Relationship synonyms
        self.relationship_map = {
            "child": "CHILD",
            "son": "CHILD",
            "daughter": "CHILD",
            "issue": "DESCENDANT",
            "descendant": "DESCENDANT",
            "offspring": "DESCENDANT",
            "lineal descendant": "DESCENDANT",

            "grandchild": "GRANDCHILD",
            "grandson": "GRANDCHILD",
            "granddaughter": "GRANDCHILD",

            "spouse": "SPOUSE",
            "husband": "SPOUSE",
            "wife": "SPOUSE",
            "surviving spouse": "SPOUSE",

            "parent": "PARENT",
            "father": "PARENT",
            "mother": "PARENT",

            "sibling": "SIBLING",
            "brother": "SIBLING",
            "sister": "SIBLING",

            "niece": "NIECE_NEPHEW",
            "nephew": "NIECE_NEPHEW",

            "cousin": "COUSIN",
            "first cousin": "COUSIN"
        }

        # Estate administration terms
        self.admin_terms_map = {
            "executor": "EXECUTOR",
            "personal representative": "EXECUTOR",
            "administrator": "EXECUTOR",
            "executrix": "EXECUTOR",

            "beneficiary": "BENEFICIARY",
            "devisee": "BENEFICIARY",
            "legatee": "BENEFICIARY",
            "heir": "HEIR",

            "testator": "TESTATOR",
            "decedent": "DECEDENT",
            "deceased": "DECEDENT",

            "intestate": "INTESTATE",
            "testate": "TESTATE",
            "died with a will": "TESTATE",
            "died without a will": "INTESTATE"
        }

        # Debt priority terms
        self.debt_priority_map = {
            "secured debt": 1,
            "mortgage": 1,
            "lien": 1,
            "security interest": 1,

            "administration expenses": 2,
            "admin expenses": 2,
            "executor fees": 2,
            "attorney fees": 2,

            "taxes": 3,
            "estate tax": 3,
            "income tax": 3,
            "property tax": 3,

            "unsecured debt": 4,
            "general creditor": 4,
            "credit card": 4,
            "medical bills": 4
        }

    def normalize_bequest_type(self, text: str) -> str:
        """Normalize bequest type description to canonical form."""
        text_lower = text.lower().strip()
        for pattern, canonical in self.bequest_type_map.items():
            if pattern in text_lower:
                return canonical
        return "UNKNOWN"

    def normalize_property_type(self, text: str) -> str:
        """Normalize property type description to canonical form."""
        text_lower = text.lower().strip()
        for pattern, canonical in self.property_type_map.items():
            if pattern in text_lower:
                return canonical
        return "UNKNOWN"

    def normalize_distribution_method(self, text: str) -> str:
        """Normalize distribution method language to canonical form."""
        text_lower = text.lower().strip()
        for pattern, canonical in self.distribution_method_map.items():
            if pattern in text_lower:
                return canonical
        return "EQUAL"  # Default

    def normalize_relationship(self, text: str) -> str:
        """Normalize relationship description to canonical form."""
        text_lower = text.lower().strip()
        for pattern, canonical in self.relationship_map.items():
            if pattern in text_lower:
                return canonical
        return "OTHER"

    def extract_survival_language(self, will_text: str) -> Dict[str, any]:
        """Extract survival conditions from will language."""
        survival_patterns = {
            "survives_me": r"(?:if|provided|who|that)\s+(?:he|she|they)\s+survives?\s+me",
            "survives_by_days": r"survives?\s+(?:me|testator)\s+(?:by|for)\s+(\d+)\s+days",
            "simultaneous_death": r"simultaneous death",
            "survival_period": r"(\d+)[\s-](?:day|month|year)\s+survival"
        }

        results = {}
        will_lower = will_text.lower()

        for key, pattern in survival_patterns.items():
            match = re.search(pattern, will_lower)
            if match:
                results[key] = match.group(0)
                if "by_days" in key or "period" in key:
                    days_match = re.search(r"(\d+)", match.group(0))
                    if days_match:
                        results[f"{key}_days"] = int(days_match.group(1))

        return results

    def classify_bequest_from_language(self, bequest_text: str) -> Dict[str, str]:
        """
        Classify bequest based on language used in will.
        Returns classification and reasoning.
        """
        text_lower = bequest_text.lower()

        # Specific bequest indicators
        specific_indicators = ["my", "the", "located at", "known as", "identified as", "bearing serial number"]
        if any(indicator in text_lower for indicator in specific_indicators):
            if any(word in text_lower for word in ["house", "car", "watch", "ring", "property at"]):
                return {
                    "type": "SPECIFIC",
                    "reasoning": "Bequest describes identified property with particularity"
                }

        # General bequest indicators
        general_indicators = ["$", "dollar", "sum of", "amount of"]
        if any(indicator in text_lower for indicator in general_indicators):
            if "from" not in text_lower or "sale of" not in text_lower:
                return {
                    "type": "GENERAL",
                    "reasoning": "Bequest of dollar amount payable from general estate"
                }

        # Demonstrative bequest indicators
        if any(word in text_lower for word in ["from sale of", "from my", "out of"]):
            if any(indicator in text_lower for indicator in general_indicators):
                return {
                    "type": "DEMONSTRATIVE",
                    "reasoning": "Bequest of dollar amount from identified fund or property"
                }

        # Residuary bequest indicators
        residuary_indicators = ["rest", "residue", "remainder", "all the rest", "everything else", "all remaining"]
        if any(indicator in text_lower for indicator in residuary_indicators):
            return {
                "type": "RESIDUARY",
                "reasoning": "Bequest of remainder after specific and general bequests satisfied"
            }

        return {
            "type": "UNKNOWN",
            "reasoning": "Unable to classify bequest from language provided"
        }

    def normalize_asset_description(self, description: str) -> str:
        """Normalize asset description to consistent format."""
        # Remove extra whitespace
        normalized = " ".join(description.split())

        # Standardize common abbreviations
        replacements = {
            "approx.": "approximately",
            "approx": "approximately",
            "~": "approximately",
            "acct": "account",
            "acct.": "account",
            "#": "number",
            "s.f.": "square feet",
            "sf": "square feet"
        }

        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        return normalized.strip()

    def detect_ademption_risk(self, specific_bequest: str, current_assets: List[str]) -> Dict[str, any]:
        """
        Detect if specific bequest may have been adeemed (property no longer in estate).
        Returns risk assessment.
        """
        bequest_lower = specific_bequest.lower()
        current_assets_lower = [a.lower() for a in current_assets]

        # Extract key identifiers from bequest
        key_terms = self._extract_key_terms(bequest_lower)

        # Check if any current asset matches key terms
        matches = []
        for asset in current_assets_lower:
            if any(term in asset for term in key_terms):
                matches.append(asset)

        if matches:
            return {
                "ademption_risk": "LOW",
                "matching_assets": matches,
                "reasoning": "Property appears to be in estate with matching description"
            }
        else:
            return {
                "ademption_risk": "HIGH",
                "matching_assets": [],
                "reasoning": "No current asset matches specific bequest description - possible ademption"
            }

    def _extract_key_terms(self, text: str) -> Set[str]:
        """Extract key identifying terms from text."""
        # Remove common words
        stop_words = {"my", "the", "a", "an", "to", "of", "in", "at", "on", "for", "with"}
        words = set(text.split())
        key_terms = words - stop_words

        # Add multi-word phrases
        phrases = re.findall(r'(?:located at|known as|bearing)\s+\w+(?:\s+\w+)*', text)
        key_terms.update(phrase.strip() for phrase in phrases)

        return key_terms

    def standardize_dollar_amount(self, text: str) -> float:
        """Extract and standardize dollar amount from text."""
        # Remove currency symbols and commas
        cleaned = text.replace("$", "").replace(",", "").strip()

        # Handle written numbers
        written_map = {
            "thousand": 1000,
            "million": 1000000,
            "k": 1000,
            "m": 1000000
        }

        for word, multiplier in written_map.items():
            if word in cleaned.lower():
                number_part = re.search(r'([\d.]+)', cleaned)
                if number_part:
                    return float(number_part.group(1)) * multiplier

        # Extract numeric value
        number_match = re.search(r'([\d,]+(?:\.\d{2})?)', cleaned)
        if number_match:
            return float(number_match.group(1).replace(",", ""))

        return 0.0
