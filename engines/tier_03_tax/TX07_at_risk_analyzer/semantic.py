"""
Semantic normalization for IRC §465 at-risk analysis
Domain-specific term standardization and concept mapping
"""

from typing import Dict, List, Set
import re


class AtRiskSemanticNormalizer:
    """Normalizes at-risk terminology to canonical forms for deterministic doctrine matching"""

    def __init__(self):
        self.term_mappings = self._build_term_mappings()
        self.phrase_patterns = self._build_phrase_patterns()

    def _build_term_mappings(self) -> Dict[str, str]:
        """Map synonyms and variations to canonical terms"""
        return {
            # At-risk amount synonyms
            "amount at risk": "at_risk_amount",
            "at risk amount": "at_risk_amount",
            "at-risk basis": "at_risk_amount",
            "risk amount": "at_risk_amount",
            "amount at-risk": "at_risk_amount",

            # Non-recourse debt
            "non-recourse": "nonrecourse_debt",
            "nonrecourse": "nonrecourse_debt",
            "non recourse": "nonrecourse_debt",
            "without recourse": "nonrecourse_debt",
            "no personal liability": "nonrecourse_debt",

            # Recourse debt
            "recourse debt": "recourse_debt",
            "personal liability": "recourse_debt",
            "personally liable": "recourse_debt",
            "with recourse": "recourse_debt",

            # Qualified nonrecourse financing
            "qualified nonrecourse": "qualified_nonrecourse_financing",
            "qualified non-recourse": "qualified_nonrecourse_financing",
            "QNF": "qualified_nonrecourse_financing",
            "qnrf": "qualified_nonrecourse_financing",
            "465(b)(6)": "qualified_nonrecourse_financing",

            # Guarantees
            "personal guarantee": "personal_guarantee",
            "guarantee": "personal_guarantee",
            "guaranteed by": "personal_guarantee",

            # Stop-loss
            "stop loss": "stop_loss_agreement",
            "stop-loss": "stop_loss_agreement",
            "loss limitation": "stop_loss_agreement",
            "protected against loss": "stop_loss_agreement",

            # Related party
            "related party": "related_party",
            "related person": "related_party",
            "family member": "related_party",
            "controlled entity": "related_party",

            # Activities
            "real estate": "real_property_activity",
            "real property": "real_property_activity",
            "rental property": "real_property_activity",
            "oil and gas": "oil_gas_activity",
            "oil & gas": "oil_gas_activity",
            "working interest": "oil_gas_working_interest",
            "equipment leasing": "equipment_leasing_activity",
            "1245 property": "equipment_leasing_activity",

            # Recapture
            "recapture": "loss_recapture",
            "465(e) recapture": "loss_recapture",
            "recapture income": "loss_recapture",

            # Loss limitations
            "loss limitation": "loss_limitation",
            "suspended loss": "suspended_loss",
            "disallowed loss": "suspended_loss",
            "carryforward": "suspended_loss",

            # Partnership/S-corp
            "partner": "partner",
            "partnership": "partnership",
            "S corporation": "s_corporation",
            "S-corporation": "s_corporation",
            "S corp": "s_corporation",
            "shareholder": "shareholder",

            # Basis concepts
            "outside basis": "partner_outside_basis",
            "tax basis": "adjusted_basis",
            "adjusted basis": "adjusted_basis",
            "cost basis": "adjusted_basis",
        }

    def _build_phrase_patterns(self) -> List[tuple]:
        """Pattern matching for complex at-risk concepts"""
        return [
            (r"amount.*at[\s-]?risk", "at_risk_amount"),
            (r"qualified.*nonrecourse.*financing", "qualified_nonrecourse_financing"),
            (r"465\(b\)\(6\)", "qualified_nonrecourse_financing"),
            (r"personal.*liab", "recourse_debt"),
            (r"non[\s-]?recourse", "nonrecourse_debt"),
            (r"stop[\s-]?loss", "stop_loss_agreement"),
            (r"related.*party", "related_party"),
            (r"real.*estate|real.*property", "real_property_activity"),
            (r"oil.*gas|gas.*oil", "oil_gas_activity"),
            (r"working.*interest", "oil_gas_working_interest"),
            (r"equipment.*leas", "equipment_leasing_activity"),
            (r"465\(e\)", "loss_recapture"),
            (r"suspended.*loss", "suspended_loss"),
        ]

    def normalize_query(self, query: str) -> str:
        """Normalize query text to canonical at-risk terminology"""
        normalized = query.lower()

        # Apply phrase patterns first (longer matches)
        for pattern, replacement in self.phrase_patterns:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

        # Apply term mappings
        for term, canonical in self.term_mappings.items():
            normalized = normalized.replace(term.lower(), canonical)

        return normalized

    def extract_at_risk_concepts(self, text: str) -> Set[str]:
        """Extract at-risk concepts from text for doctrine matching"""
        concepts = set()
        text_lower = text.lower()
        normalized = self.normalize_query(text)

        # Extract canonical terms that appear in normalized text
        for canonical in set(self.term_mappings.values()):
            if canonical in normalized:
                concepts.add(canonical)

        # Also check original text for key terms
        if any(term in text_lower for term in ["at risk", "at-risk", "amount at risk"]):
            concepts.add("at_risk_amount")

        if any(term in text_lower for term in ["compute", "computation", "calculate"]):
            concepts.add("at_risk_amount")

        if any(term in text_lower for term in ["partnership", "partner"]):
            concepts.add("partner")
            concepts.add("partnership")

        if any(term in text_lower for term in ["non-recourse", "nonrecourse", "without recourse"]):
            concepts.add("nonrecourse_debt")

        if any(term in text_lower for term in ["qualified nonrecourse", "qnrf", "465(b)(6)"]):
            concepts.add("qualified_nonrecourse_financing")

        if any(term in text_lower for term in ["related party", "family", "relative"]):
            concepts.add("related_party")

        return concepts

    def get_related_doctrines(self, concept: str) -> List[str]:
        """Map concepts to related doctrine topics"""
        doctrine_map = {
            "at_risk_amount": ["at_risk_basic_computation", "loss_recapture_465"],
            "nonrecourse_debt": ["non_recourse_debt_exclusion", "qualified_nonrecourse_financing"],
            "recourse_debt": ["at_risk_basic_computation", "partner_loans_at_risk"],
            "qualified_nonrecourse_financing": ["qualified_nonrecourse_financing"],
            "personal_guarantee": ["non_recourse_debt_exclusion", "stop_loss_agreements"],
            "stop_loss_agreement": ["stop_loss_agreements"],
            "related_party": ["partner_loans_at_risk"],
            "real_property_activity": ["qualified_nonrecourse_financing"],
            "oil_gas_activity": ["aggregation_rules"],
            "oil_gas_working_interest": ["aggregation_rules"],
            "equipment_leasing_activity": ["aggregation_rules"],
            "loss_recapture": ["loss_recapture_465"],
            "suspended_loss": ["at_risk_basic_computation"],
            "partner": ["partner_loans_at_risk"],
            "partnership": ["partner_loans_at_risk"],
            "s_corporation": ["s_corp_shareholder_at_risk"],
        }

        return doctrine_map.get(concept, [])


def normalize_irc_citation(citation: str) -> str:
    """Normalize IRC section citations to canonical format"""
    # Remove extra whitespace
    citation = re.sub(r'\s+', ' ', citation.strip())

    # Normalize section symbol
    citation = citation.replace('Section ', '§').replace('section ', '§').replace('Sec. ', '§')

    # Normalize IRC prefix
    citation = re.sub(r'IRC\s*§?\s*', '§', citation, flags=re.IGNORECASE)
    citation = re.sub(r'Internal Revenue Code\s*§?\s*', '§', citation, flags=re.IGNORECASE)

    # Standardize subsection format: §465(b)(6) not § 465 (b)(6)
    citation = re.sub(r'§\s*(\d+)\s*\(', r'§\1(', citation)

    return citation
