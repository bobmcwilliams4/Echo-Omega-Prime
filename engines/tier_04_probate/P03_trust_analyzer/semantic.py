"""
Semantic Normalization Layer for Trust Analyzer
Deterministic term mapping for trust law concepts.
NO probabilistic inference. NO embeddings at this stage.
"""

from typing import List, Dict, Set
from dataclasses import dataclass
from loguru import logger


@dataclass
class NormalizationResult:
    """Result of semantic normalization"""
    original_query: str
    normalized_terms: List[str]
    detected_concepts: List[str]
    confidence: float = 1.0


class TrustSemanticNormalizer:
    """
    Deterministic semantic normalization for trust law terminology.
    Maps colloquial/variant terms to canonical trust law concepts.
    """

    def __init__(self):
        # Trust type synonyms
        self.trust_type_map = {
            "living trust": "revocable_trust",
            "family trust": "revocable_trust",
            "intervivos trust": "revocable_trust",
            "testamentary trust": "irrevocable_trust_at_death",
            "will trust": "irrevocable_trust_at_death",
            "irrevocable": "irrevocable_trust",
            "permanent trust": "irrevocable_trust",
            "idgt": "intentionally_defective_grantor_trust",
            "slat": "spousal_lifetime_access_trust",
            "qprt": "qualified_personal_residence_trust",
            "grat": "grantor_retained_annuity_trust",
            "grut": "grantor_retained_unitrust",
            "ilit": "irrevocable_life_insurance_trust",
            "crt": "charitable_remainder_trust",
            "crut": "charitable_remainder_unitrust",
            "crat": "charitable_remainder_annuity_trust",
            "clat": "charitable_lead_annuity_trust",
            "clut": "charitable_lead_unitrust",
            "dynasty": "dynasty_trust",
            "perpetual trust": "dynasty_trust",
            "generation skipping": "dynasty_trust"
        }

        # Grantor trust terminology
        self.grantor_terms = {
            "grantor trust": "irc_671_679_grantor_trust",
            "defective trust": "intentionally_defective_grantor_trust",
            "intentionally defective": "intentionally_defective_grantor_trust",
            "reversionary interest": "grantor_trust_671_reversionary",
            "power to revoke": "grantor_trust_676_revocation_power",
            "administrative powers": "grantor_trust_675_administrative_powers",
            "income for benefit": "grantor_trust_677_income_distribution",
            "substitution power": "grantor_trust_675_substitution_power"
        }

        # Distribution standards
        self.distribution_standards = {
            "hems": "health_education_maintenance_support",
            "health education maintenance support": "health_education_maintenance_support",
            "ascertainable standard": "health_education_maintenance_support",
            "discretionary": "discretionary_distribution",
            "absolute discretion": "discretionary_distribution",
            "sole discretion": "discretionary_distribution",
            "mandatory": "mandatory_distribution",
            "required distribution": "mandatory_distribution",
            "unitrust": "unitrust_distribution",
            "annuity": "annuity_distribution",
            "income only": "income_only_distribution",
            "spray": "spray_sprinkle_distribution",
            "sprinkle": "spray_sprinkle_distribution"
        }

        # Trustee powers
        self.trustee_powers = {
            "trustee power": "trustee_powers_general",
            "administrative powers": "trustee_administrative_powers",
            "investment powers": "trustee_investment_powers",
            "distribution powers": "trustee_distribution_powers",
            "removal power": "trustee_removal_power",
            "directed trustee": "directed_trustee",
            "trust protector": "trust_protector",
            "independent trustee": "independent_trustee",
            "corporate trustee": "corporate_trustee"
        }

        # Spendthrift and creditor protection
        self.protection_terms = {
            "spendthrift": "spendthrift_provision_112035",
            "creditor protection": "spendthrift_provision_112035",
            "asset protection": "asset_protection_trust",
            "self settled": "self_settled_asset_protection_trust",
            "domestic asset protection": "domestic_asset_protection_trust",
            "dapt": "domestic_asset_protection_trust"
        }

        # Modification and termination
        self.modification_terms = {
            "trust modification": "trust_modification_112054",
            "trust termination": "trust_termination_112054",
            "decanting": "trust_decanting",
            "reformation": "trust_reformation",
            "virtual representation": "virtual_representation_115013"
        }

        # Perpetuities and duration
        self.duration_terms = {
            "rule against perpetuities": "rule_against_perpetuities",
            "rap": "rule_against_perpetuities",
            "perpetuities period": "perpetuities_period",
            "lives in being": "lives_in_being_plus_21",
            "texas abolished rap": "texas_rap_abolition_112036",
            "trust duration": "trust_duration_rules"
        }

        # Charitable trust terms
        self.charitable_terms = {
            "charitable trust": "charitable_trust_123",
            "charitable remainder": "charitable_remainder_trust",
            "charitable lead": "charitable_lead_trust",
            "private foundation": "private_foundation",
            "supporting organization": "supporting_organization_509a3"
        }

        # Minor beneficiary trusts
        self.minor_trust_terms = {
            "2503c trust": "minors_trust_2503c",
            "minor trust": "minors_trust_2503c",
            "crummey": "crummey_power",
            "demand right": "crummey_power",
            "withdrawal right": "crummey_power",
            "hanging power": "hanging_crummey_power"
        }

        # Build master normalization map
        self.normalization_map = {}
        for mapping in [
            self.trust_type_map,
            self.grantor_terms,
            self.distribution_standards,
            self.trustee_powers,
            self.protection_terms,
            self.modification_terms,
            self.duration_terms,
            self.charitable_terms,
            self.minor_trust_terms
        ]:
            self.normalization_map.update(mapping)

        # Concept detectors (keywords that trigger specific doctrine areas)
        self.concept_patterns = {
            "grantor_trust_analysis": [
                "grantor", "defective", "671", "676", "677", "reversionary"
            ],
            "distribution_standard": [
                "hems", "discretionary", "mandatory", "distribution", "ascertainable"
            ],
            "trustee_duties": [
                "trustee", "fiduciary", "duty", "prudent investor", "loyalty"
            ],
            "modification_termination": [
                "modify", "terminate", "decant", "reform", "112.054"
            ],
            "perpetuities": [
                "rap", "perpetuities", "dynasty", "duration", "lives in being"
            ],
            "charitable_planning": [
                "charitable", "crt", "clt", "private foundation"
            ],
            "creditor_protection": [
                "spendthrift", "creditor", "asset protection", "dapt"
            ]
        }

    def normalize(self, query: str) -> NormalizationResult:
        """
        Normalize a trust law query to canonical terms.
        Returns normalized terms and detected concepts.
        """
        query_lower = query.lower()

        # Extract normalized terms
        normalized_terms = []
        for term, canonical in self.normalization_map.items():
            if term in query_lower:
                normalized_terms.append(canonical)

        # Detect broader concepts
        detected_concepts = []
        for concept, keywords in self.concept_patterns.items():
            if any(kw in query_lower for kw in keywords):
                detected_concepts.append(concept)

        # Deduplicate
        normalized_terms = list(set(normalized_terms))
        detected_concepts = list(set(detected_concepts))

        logger.debug(
            f"Normalized query | "
            f"Terms: {len(normalized_terms)} | "
            f"Concepts: {len(detected_concepts)}"
        )

        return NormalizationResult(
            original_query=query,
            normalized_terms=normalized_terms,
            detected_concepts=detected_concepts,
            confidence=1.0  # Deterministic = always confident
        )

    def get_canonical_term(self, variant: str) -> str:
        """Get canonical form of a variant term"""
        return self.normalization_map.get(variant.lower(), variant.lower())


# Global normalizer instance
_normalizer: TrustSemanticNormalizer = None


def get_normalizer() -> TrustSemanticNormalizer:
    """Get global normalizer instance"""
    global _normalizer
    if _normalizer is None:
        _normalizer = TrustSemanticNormalizer()
    return _normalizer


def normalize_semantics(query: str) -> NormalizationResult:
    """Convenience function for normalization"""
    return get_normalizer().normalize(query)
