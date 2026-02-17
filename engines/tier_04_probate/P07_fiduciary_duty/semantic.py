"""
P07 Fiduciary Duty Engine - Semantic Normalization
Domain-specific term normalization and concept mapping
"""

from typing import Dict, List, Set
import re


class FiduciarySemanticNormalizer:
    """Normalize fiduciary duty terminology to canonical forms"""

    def __init__(self):
        self.term_map = self._build_term_map()
        self.concept_clusters = self._build_concept_clusters()
        self.synonym_groups = self._build_synonym_groups()

    def _build_term_map(self) -> Dict[str, str]:
        """Map variant terms to canonical forms"""
        return {
            # Fiduciary types
            "personal representative": "executor",
            "administrator": "executor",
            "executrix": "executor",
            "independent executor": "executor_independent",
            "dependent executor": "executor_dependent",
            "trustee": "trustee",
            "guardian": "guardian",
            "conservator": "guardian_estate",
            "custodian": "custodian",
            "agent": "agent_poa",
            "attorney in fact": "agent_poa",

            # Duties
            "duty of loyalty": "loyalty_duty",
            "undivided loyalty": "loyalty_duty",
            "duty of care": "care_duty",
            "duty of prudence": "care_duty",
            "prudent person standard": "care_duty",
            "duty to account": "accounting_duty",
            "duty of disclosure": "accounting_duty",
            "duty to invest": "investment_duty",
            "prudent investor rule": "investment_duty",
            "duty to diversify": "diversification_duty",
            "duty of impartiality": "impartiality_duty",
            "duty to inform": "disclosure_duty",

            # Breach concepts
            "breach of fiduciary duty": "fiduciary_breach",
            "violation of duty": "fiduciary_breach",
            "self-dealing": "self_dealing",
            "conflict of interest": "conflict_interest",
            "interested transaction": "self_dealing",
            "improper delegation": "improper_delegation",
            "failure to diversify": "diversification_breach",
            "commingling": "commingling_breach",
            "waste": "waste",

            # Remedies
            "surcharge": "surcharge_remedy",
            "damages": "monetary_damages",
            "restitution": "restitution_remedy",
            "disgorgement": "profit_disgorgement",
            "removal": "fiduciary_removal",
            "accounting": "formal_accounting",

            # Standards
            "prudent person": "prudent_person_standard",
            "reasonable care": "reasonable_care_standard",
            "good faith": "good_faith",
            "bad faith": "bad_faith",
            "reckless indifference": "recklessness",
            "gross negligence": "gross_negligence",
            "ordinary negligence": "ordinary_negligence",

            # Property concepts
            "trust property": "trust_property",
            "trust corpus": "trust_property",
            "trust principal": "trust_property",
            "estate property": "estate_property",
            "estate assets": "estate_property",
            "ward property": "ward_property",

            # Beneficiary types
            "beneficiary": "beneficiary",
            "cestui que trust": "beneficiary",
            "income beneficiary": "income_beneficiary",
            "remainder beneficiary": "remainder_beneficiary",
            "remainderman": "remainder_beneficiary",
            "ward": "ward",
            "incapacitated person": "ward",
            "protected person": "ward",

            # Legal concepts
            "no further inquiry rule": "no_further_inquiry",
            "voidable transaction": "voidable_transaction",
            "exculpatory clause": "exculpatory_clause",
            "liability waiver": "exculpatory_clause",
            "court supervision": "court_supervision",
            "independent administration": "independent_administration",

            # Investment terms
            "modern portfolio theory": "modern_portfolio_theory",
            "total return": "total_return",
            "diversification": "diversification",
            "asset allocation": "asset_allocation",
            "risk/return": "risk_return_tradeoff",
            "prudent investor act": "prudent_investor_act",

            # Procedural
            "inventory": "estate_inventory",
            "appraisement": "estate_inventory",
            "annual accounting": "annual_accounting",
            "final accounting": "final_accounting",
            "bond": "fiduciary_bond",
            "letters testamentary": "letters_testamentary",
            "letters of guardianship": "letters_guardianship"
        }

    def _build_concept_clusters(self) -> Dict[str, List[str]]:
        """Group related concepts for semantic expansion"""
        return {
            "loyalty_concepts": [
                "loyalty_duty", "undivided_loyalty", "exclusive_benefit",
                "no_self_dealing", "conflict_avoidance", "beneficiary_primacy"
            ],
            "care_concepts": [
                "care_duty", "prudent_person_standard", "reasonable_care",
                "diligence", "skill", "caution", "investigation"
            ],
            "self_dealing_concepts": [
                "self_dealing", "conflict_interest", "interested_transaction",
                "dual_capacity", "purchase_from_trust", "sale_to_trust",
                "fiduciary_profit", "family_transaction"
            ],
            "breach_concepts": [
                "fiduciary_breach", "duty_violation", "standard_deviation",
                "negligence", "misconduct", "impropriety"
            ],
            "remedy_concepts": [
                "surcharge_remedy", "monetary_damages", "restitution_remedy",
                "profit_disgorgement", "fiduciary_removal", "accounting_order",
                "injunctive_relief"
            ],
            "investment_concepts": [
                "investment_duty", "prudent_investor_act", "diversification_duty",
                "modern_portfolio_theory", "total_return", "asset_allocation",
                "risk_management"
            ],
            "accounting_concepts": [
                "accounting_duty", "disclosure_duty", "estate_inventory",
                "annual_accounting", "final_accounting", "transparency"
            ],
            "guardianship_concepts": [
                "guardian", "ward", "incapacitated_person", "guardian_person",
                "guardian_estate", "court_supervision", "best_interest"
            ],
            "executor_concepts": [
                "executor", "personal_representative", "estate_administration",
                "independent_executor", "dependent_executor", "probate"
            ],
            "trustee_concepts": [
                "trustee", "trust_administration", "trust_property",
                "beneficiary", "settlor_intent", "trust_terms"
            ]
        }

    def _build_synonym_groups(self) -> List[Set[str]]:
        """Define synonym groups for query expansion"""
        return [
            {"breach", "violation", "infringement", "transgression"},
            {"duty", "obligation", "responsibility", "burden"},
            {"loyalty", "fidelity", "allegiance", "faithfulness"},
            {"care", "prudence", "diligence", "caution"},
            {"damages", "loss", "harm", "injury"},
            {"removal", "discharge", "termination", "dismissal"},
            {"accounting", "report", "statement", "disclosure"},
            {"investment", "asset management", "portfolio management"},
            {"beneficiary", "cestui que trust", "trust beneficiary"},
            {"self-dealing", "conflict of interest", "interested transaction"},
            {"surcharge", "damages", "monetary penalty", "restitution"},
            {"waste", "dissipation", "depletion", "squandering"},
            {"impartiality", "fairness", "balance", "even-handedness"},
            {"delegation", "assignment", "entrustment", "authorization"},
            {"supervision", "oversight", "monitoring", "control"}
        ]

    def normalize_query(self, query: str) -> str:
        """Normalize query text to canonical terms"""
        normalized = query.lower()

        # Apply term mappings
        for variant, canonical in sorted(self.term_map.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = r'\b' + re.escape(variant) + r'\b'
            normalized = re.sub(pattern, canonical, normalized, flags=re.IGNORECASE)

        return normalized

    def expand_concepts(self, term: str) -> List[str]:
        """Expand term to related concepts"""
        canonical = self.term_map.get(term.lower(), term.lower())

        related = [canonical]

        # Add concepts from clusters
        for cluster_name, concepts in self.concept_clusters.items():
            if canonical in concepts:
                related.extend([c for c in concepts if c != canonical])

        # Add synonyms
        for synonym_group in self.synonym_groups:
            if canonical in synonym_group or term.lower() in synonym_group:
                related.extend(list(synonym_group))

        return list(set(related))

    def extract_domain_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract domain-specific entities from text"""
        entities = {
            "fiduciary_types": [],
            "duties": [],
            "breaches": [],
            "remedies": [],
            "statutes": [],
            "case_names": []
        }

        # Fiduciary types
        fiduciary_patterns = [
            r'\b(executor|trustee|guardian|administrator|personal representative|agent)\b',
            r'\bindependent (executor|administration)\b',
            r'\bguardian of (the )?(person|estate)\b'
        ]
        for pattern in fiduciary_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["fiduciary_types"].extend([m if isinstance(m, str) else m[0] for m in matches])

        # Duties
        duty_patterns = [
            r'\bduty of (loyalty|care|prudence|impartiality|disclosure)\b',
            r'\b(accounting|investment|diversification) duty\b',
            r'\bprudent (person|investor) (standard|rule)\b'
        ]
        for pattern in duty_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["duties"].extend([m if isinstance(m, str) else ' '.join(m) for m in matches])

        # Breach concepts
        breach_patterns = [
            r'\b(self-dealing|conflict of interest|commingling|waste)\b',
            r'\bbreach of (fiduciary )?duty\b',
            r'\b(gross |ordinary )?(negligence|misconduct)\b'
        ]
        for pattern in breach_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["breaches"].extend([m if isinstance(m, str) else ''.join(m) for m in matches])

        # Remedies
        remedy_patterns = [
            r'\b(surcharge|removal|damages|restitution|disgorgement)\b',
            r'\b(accounting|injunctive relief)\b'
        ]
        for pattern in remedy_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["remedies"].extend(matches)

        # Statutes
        statute_patterns = [
            r'\bTX (Estates Code|Property Code) §[\d.]+\b',
            r'\b§§? ?[\d.]+\b',
            r'\bChapter \d+\b'
        ]
        for pattern in statute_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["statutes"].extend(matches)

        # Case names
        case_pattern = r'\b[A-Z][a-z]+ v\. [A-Z][a-z]+(?:,? \d+ [A-Z.]{2,5}\d?\.?\d?d? \d+)?'
        entities["case_names"] = re.findall(case_pattern, text)

        # Remove duplicates and normalize
        for key in entities:
            entities[key] = list(set(entities[key]))

        return entities

    def semantic_distance(self, term1: str, term2: str) -> float:
        """Calculate semantic distance between two terms (0 = identical, 1 = unrelated)"""
        t1_canonical = self.term_map.get(term1.lower(), term1.lower())
        t2_canonical = self.term_map.get(term2.lower(), term2.lower())

        # Exact match
        if t1_canonical == t2_canonical:
            return 0.0

        # Check if in same concept cluster
        for cluster_concepts in self.concept_clusters.values():
            if t1_canonical in cluster_concepts and t2_canonical in cluster_concepts:
                return 0.3  # Close semantic relationship

        # Check if in same synonym group
        for synonym_group in self.synonym_groups:
            if (t1_canonical in synonym_group or term1.lower() in synonym_group) and \
               (t2_canonical in synonym_group or term2.lower() in synonym_group):
                return 0.2  # Very close (synonyms)

        # Check if one maps to concept cluster containing the other
        t1_concepts = self.expand_concepts(term1)
        t2_concepts = self.expand_concepts(term2)

        if t2_canonical in t1_concepts or t1_canonical in t2_concepts:
            return 0.5  # Related but not close

        # Check for overlap in expanded concepts
        overlap = set(t1_concepts) & set(t2_concepts)
        if overlap:
            return 0.7  # Tangentially related

        return 1.0  # Unrelated

    def identify_key_concepts(self, query: str) -> List[str]:
        """Identify key legal concepts in query for doctrine matching"""
        normalized = self.normalize_query(query)
        entities = self.extract_domain_entities(query)

        key_concepts = []

        # Add identified entities
        for entity_type, entity_list in entities.items():
            if entity_type != "case_names":  # Exclude case names from concept matching
                key_concepts.extend(entity_list)

        # Extract canonical terms present in query
        for variant, canonical in self.term_map.items():
            if variant in normalized:
                key_concepts.append(canonical)

        return list(set(key_concepts))
