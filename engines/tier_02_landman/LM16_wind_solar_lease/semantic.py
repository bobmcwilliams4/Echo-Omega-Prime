"""
LM16 Wind/Solar Lease Engine - Semantic Normalization Module
=============================================================
Domain-specific term normalization, synonym resolution, and
concept mapping for renewable energy land acquisition terminology.

Engine: LM16 | Port: 8516
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ENGINE_ID: str = "LM16"


# ---------------------------------------------------------------------------
# Concept taxonomy for wind/solar lease domain
# ---------------------------------------------------------------------------
class ConceptDomain(str, Enum):
    """Top-level concept domains for renewable energy leases."""
    WIND_LEASE = "wind_lease"
    SOLAR_LEASE = "solar_lease"
    PAYMENT_STRUCTURE = "payment_structure"
    SURFACE_USE = "surface_use"
    LANDOWNER_PROTECTION = "landowner_protection"
    OIL_GAS_COEXISTENCE = "oil_gas_coexistence"
    EASEMENT = "easement"
    DECOMMISSIONING = "decommissioning"
    TAX_INCENTIVE = "tax_incentive"
    REGULATORY = "regulatory"
    ENVIRONMENTAL = "environmental"
    TRANSMISSION = "transmission"
    BATTERY_STORAGE = "battery_storage"
    ESTATE_PLANNING = "estate_planning"
    FINANCING = "financing"
    RESOURCE_ASSESSMENT = "resource_assessment"
    INTERCONNECTION = "interconnection"
    ACCOMMODATION = "accommodation"
    AGRICULTURAL = "agricultural"
    NOISE_FLICKER = "noise_flicker"


# ---------------------------------------------------------------------------
# Synonym map: maps variant terms to canonical form
# ---------------------------------------------------------------------------
SYNONYM_MAP: dict[str, str] = {
    # Wind lease variants
    "wind farm lease": "wind_energy_lease",
    "wind energy lease": "wind_energy_lease",
    "wind lease": "wind_energy_lease",
    "wind power lease": "wind_energy_lease",
    "wind turbine lease": "wind_energy_lease",
    "wind farm agreement": "wind_energy_lease",
    "wecs lease": "wind_energy_lease",
    "wind energy conversion system lease": "wind_energy_lease",
    "wind rights lease": "wind_energy_lease",
    "wind option agreement": "wind_option",
    "wind option": "wind_option",
    "wind development option": "wind_option",
    # Solar lease variants
    "solar lease": "solar_energy_lease",
    "solar farm lease": "solar_energy_lease",
    "solar energy lease": "solar_energy_lease",
    "solar panel lease": "solar_energy_lease",
    "photovoltaic lease": "solar_energy_lease",
    "pv lease": "solar_energy_lease",
    "solar power purchase agreement": "solar_ppa",
    "solar ppa": "solar_ppa",
    "solar option": "solar_option",
    "solar development option": "solar_option",
    "solar development agreement": "solar_energy_lease",
    "utility scale solar lease": "solar_energy_lease",
    "community solar lease": "community_solar_lease",
    # Payment terms
    "royalty": "royalty_payment",
    "royalties": "royalty_payment",
    "lease payment": "lease_payment",
    "rent": "lease_payment",
    "rental": "lease_payment",
    "per acre payment": "per_acre_payment",
    "per megawatt payment": "per_mw_payment",
    "per mw": "per_mw_payment",
    "per turbine payment": "per_turbine_payment",
    "escalation clause": "payment_escalation",
    "escalation": "payment_escalation",
    "cpi adjustment": "cpi_escalation",
    "cpi escalation": "cpi_escalation",
    "annual escalation": "payment_escalation",
    "signing bonus": "signing_bonus",
    "option payment": "option_payment",
    "option fee": "option_payment",
    "gross revenue": "gross_revenue_royalty",
    "revenue share": "gross_revenue_royalty",
    "percentage of revenue": "gross_revenue_royalty",
    "minimum rent": "minimum_rent_guarantee",
    "guaranteed minimum": "minimum_rent_guarantee",
    # Surface use
    "surface use": "surface_use_restriction",
    "surface damage": "surface_damage_payment",
    "surface damages": "surface_damage_payment",
    "crop damage": "crop_damage_payment",
    "crop loss": "crop_damage_payment",
    "setback": "setback_requirement",
    "setback requirement": "setback_requirement",
    "setback distance": "setback_requirement",
    "building setback": "setback_requirement",
    "property line setback": "property_line_setback",
    "dwelling setback": "dwelling_setback",
    "road setback": "road_setback",
    "noise setback": "noise_setback",
    "shadow flicker": "shadow_flicker",
    "flicker": "shadow_flicker",
    "shadow": "shadow_flicker",
    "noise": "noise_restriction",
    "noise level": "noise_restriction",
    "decibel limit": "noise_restriction",
    "sound level": "noise_restriction",
    # Landowner protections
    "landowner protection": "landowner_protective_provision",
    "landowner rights": "landowner_protective_provision",
    "surface owner rights": "landowner_protective_provision",
    "surface owner": "surface_owner",
    "surface estate": "surface_estate",
    "mineral owner": "mineral_owner",
    "mineral estate": "mineral_estate",
    "dominant estate": "dominant_mineral_estate",
    "servient estate": "servient_surface_estate",
    # Oil and gas coexistence
    "accommodation doctrine": "accommodation_doctrine",
    "accommodation": "accommodation_doctrine",
    "surface use conflict": "surface_use_conflict",
    "oil and gas conflict": "surface_use_conflict",
    "mineral rights conflict": "mineral_rights_conflict",
    "split estate": "split_estate",
    "severed mineral": "severed_minerals",
    "severed minerals": "severed_minerals",
    "dominant mineral estate": "dominant_mineral_estate",
    # Decommissioning
    "decommissioning": "decommissioning_obligation",
    "decommissioning bond": "decommissioning_bond",
    "decommissioning plan": "decommissioning_plan",
    "removal obligation": "decommissioning_obligation",
    "site restoration": "site_restoration",
    "reclamation": "site_restoration",
    "abandonment": "decommissioning_obligation",
    "salvage value": "salvage_value",
    "surety bond": "decommissioning_bond",
    "performance bond": "decommissioning_bond",
    "letter of credit": "decommissioning_financial_assurance",
    # Tax incentives
    "ptc": "production_tax_credit",
    "production tax credit": "production_tax_credit",
    "itc": "investment_tax_credit",
    "investment tax credit": "investment_tax_credit",
    "macrs": "macrs_depreciation",
    "macrs depreciation": "macrs_depreciation",
    "accelerated depreciation": "macrs_depreciation",
    "bonus depreciation": "bonus_depreciation",
    "inflation reduction act": "ira_2022",
    "ira": "ira_2022",
    "section 45": "production_tax_credit",
    "section 48": "investment_tax_credit",
    "section 168": "macrs_depreciation",
    "tax equity": "tax_equity_financing",
    "tax equity investor": "tax_equity_financing",
    "safe harbor": "safe_harbor_provision",
    # Transmission
    "transmission line": "transmission_line",
    "transmission easement": "transmission_easement",
    "crez": "crez_transmission",
    "competitive renewable energy zone": "crez_transmission",
    "gen-tie": "gen_tie_line",
    "generation tie line": "gen_tie_line",
    "interconnection": "grid_interconnection",
    "ercot": "ercot",
    "ercot interconnection": "ercot_interconnection",
    "point of interconnection": "poi",
    "poi": "poi",
    "substation": "substation",
    "collector system": "collector_system",
    # Battery storage
    "bess": "battery_energy_storage",
    "battery storage": "battery_energy_storage",
    "battery energy storage system": "battery_energy_storage",
    "energy storage": "battery_energy_storage",
    "co-located storage": "colocated_storage",
    "hybrid project": "hybrid_project",
    "solar plus storage": "solar_plus_storage",
    "wind plus storage": "wind_plus_storage",
    # Environmental
    "eagle take permit": "eagle_take_permit",
    "eagle permit": "eagle_take_permit",
    "bald and golden eagle": "eagle_take_permit",
    "esa": "endangered_species_act",
    "endangered species": "endangered_species_act",
    "nepa": "nepa_review",
    "environmental impact": "environmental_impact",
    "environmental review": "environmental_review",
    "migratory bird": "migratory_bird_treaty",
    "bat survey": "bat_survey",
    "avian survey": "avian_survey",
    "cultural resource": "cultural_resource_survey",
    "wetland": "wetland_delineation",
    "phase 1": "phase_1_esa",
    "phase 1 esa": "phase_1_esa",
    # Easement types
    "access easement": "access_easement",
    "construction easement": "construction_easement",
    "temporary easement": "temporary_easement",
    "permanent easement": "permanent_easement",
    "meteorological tower": "met_tower_easement",
    "met tower": "met_tower_easement",
    "anemometer": "met_tower_easement",
    "resource assessment easement": "resource_assessment_easement",
    # Estate planning
    "estate planning": "estate_planning",
    "trust": "trust_ownership",
    "life estate": "life_estate",
    "remainder interest": "remainder_interest",
    "undivided interest": "undivided_interest",
    "tenants in common": "tenants_in_common",
    "joint tenancy": "joint_tenancy",
    "mineral trust": "mineral_trust",
    # Financing
    "project finance": "project_finance",
    "lender consent": "lender_consent",
    "snda": "subordination_nondisturbance",
    "subordination nondisturbance": "subordination_nondisturbance",
    "estoppel": "estoppel_certificate",
    "estoppel certificate": "estoppel_certificate",
    "assignment": "assignment_provision",
    "assignment provision": "assignment_provision",
    "change of control": "change_of_control",
    "mortgage": "mortgagee_protection",
    "mortgagee": "mortgagee_protection",
    # Agricultural
    "ag exemption": "agricultural_exemption",
    "agricultural exemption": "agricultural_exemption",
    "ag valuation": "agricultural_valuation",
    "1-d-1": "agricultural_valuation",
    "open space valuation": "agricultural_valuation",
    "grazing": "grazing_compatibility",
    "farming": "farming_compatibility",
    "ranch": "ranching_compatibility",
    "ranching": "ranching_compatibility",
    # Eminent domain
    "eminent domain": "eminent_domain",
    "condemnation": "condemnation",
    "taking": "eminent_domain",
    "inverse condemnation": "inverse_condemnation",
    "just compensation": "just_compensation",
    "public use": "public_use_requirement",
    "public necessity": "public_necessity",
}

# ---------------------------------------------------------------------------
# Concept to domain mapping
# ---------------------------------------------------------------------------
CONCEPT_DOMAIN_MAP: dict[str, ConceptDomain] = {
    "wind_energy_lease": ConceptDomain.WIND_LEASE,
    "wind_option": ConceptDomain.WIND_LEASE,
    "solar_energy_lease": ConceptDomain.SOLAR_LEASE,
    "solar_ppa": ConceptDomain.SOLAR_LEASE,
    "solar_option": ConceptDomain.SOLAR_LEASE,
    "community_solar_lease": ConceptDomain.SOLAR_LEASE,
    "royalty_payment": ConceptDomain.PAYMENT_STRUCTURE,
    "lease_payment": ConceptDomain.PAYMENT_STRUCTURE,
    "per_acre_payment": ConceptDomain.PAYMENT_STRUCTURE,
    "per_mw_payment": ConceptDomain.PAYMENT_STRUCTURE,
    "per_turbine_payment": ConceptDomain.PAYMENT_STRUCTURE,
    "payment_escalation": ConceptDomain.PAYMENT_STRUCTURE,
    "cpi_escalation": ConceptDomain.PAYMENT_STRUCTURE,
    "signing_bonus": ConceptDomain.PAYMENT_STRUCTURE,
    "option_payment": ConceptDomain.PAYMENT_STRUCTURE,
    "gross_revenue_royalty": ConceptDomain.PAYMENT_STRUCTURE,
    "minimum_rent_guarantee": ConceptDomain.PAYMENT_STRUCTURE,
    "surface_use_restriction": ConceptDomain.SURFACE_USE,
    "surface_damage_payment": ConceptDomain.SURFACE_USE,
    "crop_damage_payment": ConceptDomain.SURFACE_USE,
    "setback_requirement": ConceptDomain.SURFACE_USE,
    "property_line_setback": ConceptDomain.SURFACE_USE,
    "dwelling_setback": ConceptDomain.SURFACE_USE,
    "road_setback": ConceptDomain.SURFACE_USE,
    "noise_setback": ConceptDomain.SURFACE_USE,
    "shadow_flicker": ConceptDomain.NOISE_FLICKER,
    "noise_restriction": ConceptDomain.NOISE_FLICKER,
    "landowner_protective_provision": ConceptDomain.LANDOWNER_PROTECTION,
    "surface_owner": ConceptDomain.LANDOWNER_PROTECTION,
    "surface_estate": ConceptDomain.LANDOWNER_PROTECTION,
    "mineral_owner": ConceptDomain.OIL_GAS_COEXISTENCE,
    "mineral_estate": ConceptDomain.OIL_GAS_COEXISTENCE,
    "dominant_mineral_estate": ConceptDomain.OIL_GAS_COEXISTENCE,
    "servient_surface_estate": ConceptDomain.OIL_GAS_COEXISTENCE,
    "accommodation_doctrine": ConceptDomain.ACCOMMODATION,
    "surface_use_conflict": ConceptDomain.OIL_GAS_COEXISTENCE,
    "mineral_rights_conflict": ConceptDomain.OIL_GAS_COEXISTENCE,
    "split_estate": ConceptDomain.OIL_GAS_COEXISTENCE,
    "severed_minerals": ConceptDomain.OIL_GAS_COEXISTENCE,
    "decommissioning_obligation": ConceptDomain.DECOMMISSIONING,
    "decommissioning_bond": ConceptDomain.DECOMMISSIONING,
    "decommissioning_plan": ConceptDomain.DECOMMISSIONING,
    "site_restoration": ConceptDomain.DECOMMISSIONING,
    "salvage_value": ConceptDomain.DECOMMISSIONING,
    "decommissioning_financial_assurance": ConceptDomain.DECOMMISSIONING,
    "production_tax_credit": ConceptDomain.TAX_INCENTIVE,
    "investment_tax_credit": ConceptDomain.TAX_INCENTIVE,
    "macrs_depreciation": ConceptDomain.TAX_INCENTIVE,
    "bonus_depreciation": ConceptDomain.TAX_INCENTIVE,
    "ira_2022": ConceptDomain.TAX_INCENTIVE,
    "tax_equity_financing": ConceptDomain.FINANCING,
    "safe_harbor_provision": ConceptDomain.TAX_INCENTIVE,
    "transmission_line": ConceptDomain.TRANSMISSION,
    "transmission_easement": ConceptDomain.TRANSMISSION,
    "crez_transmission": ConceptDomain.TRANSMISSION,
    "gen_tie_line": ConceptDomain.TRANSMISSION,
    "grid_interconnection": ConceptDomain.INTERCONNECTION,
    "ercot": ConceptDomain.INTERCONNECTION,
    "ercot_interconnection": ConceptDomain.INTERCONNECTION,
    "poi": ConceptDomain.INTERCONNECTION,
    "substation": ConceptDomain.INTERCONNECTION,
    "collector_system": ConceptDomain.INTERCONNECTION,
    "battery_energy_storage": ConceptDomain.BATTERY_STORAGE,
    "colocated_storage": ConceptDomain.BATTERY_STORAGE,
    "hybrid_project": ConceptDomain.BATTERY_STORAGE,
    "solar_plus_storage": ConceptDomain.BATTERY_STORAGE,
    "wind_plus_storage": ConceptDomain.BATTERY_STORAGE,
    "eagle_take_permit": ConceptDomain.ENVIRONMENTAL,
    "endangered_species_act": ConceptDomain.ENVIRONMENTAL,
    "nepa_review": ConceptDomain.ENVIRONMENTAL,
    "environmental_impact": ConceptDomain.ENVIRONMENTAL,
    "environmental_review": ConceptDomain.ENVIRONMENTAL,
    "migratory_bird_treaty": ConceptDomain.ENVIRONMENTAL,
    "bat_survey": ConceptDomain.ENVIRONMENTAL,
    "avian_survey": ConceptDomain.ENVIRONMENTAL,
    "cultural_resource_survey": ConceptDomain.ENVIRONMENTAL,
    "wetland_delineation": ConceptDomain.ENVIRONMENTAL,
    "phase_1_esa": ConceptDomain.ENVIRONMENTAL,
    "access_easement": ConceptDomain.EASEMENT,
    "construction_easement": ConceptDomain.EASEMENT,
    "temporary_easement": ConceptDomain.EASEMENT,
    "permanent_easement": ConceptDomain.EASEMENT,
    "met_tower_easement": ConceptDomain.RESOURCE_ASSESSMENT,
    "resource_assessment_easement": ConceptDomain.RESOURCE_ASSESSMENT,
    "estate_planning": ConceptDomain.ESTATE_PLANNING,
    "trust_ownership": ConceptDomain.ESTATE_PLANNING,
    "life_estate": ConceptDomain.ESTATE_PLANNING,
    "remainder_interest": ConceptDomain.ESTATE_PLANNING,
    "undivided_interest": ConceptDomain.ESTATE_PLANNING,
    "tenants_in_common": ConceptDomain.ESTATE_PLANNING,
    "joint_tenancy": ConceptDomain.ESTATE_PLANNING,
    "mineral_trust": ConceptDomain.ESTATE_PLANNING,
    "project_finance": ConceptDomain.FINANCING,
    "lender_consent": ConceptDomain.FINANCING,
    "subordination_nondisturbance": ConceptDomain.FINANCING,
    "estoppel_certificate": ConceptDomain.FINANCING,
    "assignment_provision": ConceptDomain.FINANCING,
    "change_of_control": ConceptDomain.FINANCING,
    "mortgagee_protection": ConceptDomain.FINANCING,
    "agricultural_exemption": ConceptDomain.AGRICULTURAL,
    "agricultural_valuation": ConceptDomain.AGRICULTURAL,
    "grazing_compatibility": ConceptDomain.AGRICULTURAL,
    "farming_compatibility": ConceptDomain.AGRICULTURAL,
    "ranching_compatibility": ConceptDomain.AGRICULTURAL,
    "eminent_domain": ConceptDomain.TRANSMISSION,
    "condemnation": ConceptDomain.TRANSMISSION,
    "inverse_condemnation": ConceptDomain.TRANSMISSION,
    "just_compensation": ConceptDomain.TRANSMISSION,
    "public_use_requirement": ConceptDomain.TRANSMISSION,
    "public_necessity": ConceptDomain.TRANSMISSION,
}


# ---------------------------------------------------------------------------
# Keyword extraction patterns
# ---------------------------------------------------------------------------
KEYWORD_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("wind_energy_lease", re.compile(r"\bwind\s+(?:farm|energy|power|turbine)?\s*lease\b", re.IGNORECASE)),
    ("solar_energy_lease", re.compile(r"\bsolar\s+(?:farm|energy|panel|power)?\s*lease\b", re.IGNORECASE)),
    ("royalty_payment", re.compile(r"\broyalt(?:y|ies)\b", re.IGNORECASE)),
    ("per_mw_payment", re.compile(r"\bper\s+(?:mega\s*watt|mw)\b", re.IGNORECASE)),
    ("per_acre_payment", re.compile(r"\bper\s+acre\b", re.IGNORECASE)),
    ("setback_requirement", re.compile(r"\bsetback\b", re.IGNORECASE)),
    ("shadow_flicker", re.compile(r"\bshadow\s+flicker\b", re.IGNORECASE)),
    ("noise_restriction", re.compile(r"\bnoise\s+(?:level|limit|restriction|standard)\b", re.IGNORECASE)),
    ("decommissioning_obligation", re.compile(r"\bdecommission\w*\b", re.IGNORECASE)),
    ("production_tax_credit", re.compile(r"\b(?:ptc|production\s+tax\s+credit)\b", re.IGNORECASE)),
    ("investment_tax_credit", re.compile(r"\b(?:itc|investment\s+tax\s+credit)\b", re.IGNORECASE)),
    ("macrs_depreciation", re.compile(r"\b(?:macrs|accelerated\s+depreciation)\b", re.IGNORECASE)),
    ("accommodation_doctrine", re.compile(r"\baccommodation\s+doctrine\b", re.IGNORECASE)),
    ("split_estate", re.compile(r"\bsplit\s+estate\b", re.IGNORECASE)),
    ("eagle_take_permit", re.compile(r"\beagle\s+(?:take|permit)\b", re.IGNORECASE)),
    ("ercot_interconnection", re.compile(r"\bercot\b", re.IGNORECASE)),
    ("crez_transmission", re.compile(r"\b(?:crez|competitive\s+renewable\s+energy\s+zone)\b", re.IGNORECASE)),
    ("battery_energy_storage", re.compile(r"\b(?:bess|battery\s+(?:energy\s+)?storage)\b", re.IGNORECASE)),
    ("agricultural_exemption", re.compile(r"\b(?:ag\s+exemption|agricultural\s+exemption)\b", re.IGNORECASE)),
    ("eminent_domain", re.compile(r"\beminent\s+domain\b", re.IGNORECASE)),
    ("lender_consent", re.compile(r"\blender\s+consent\b", re.IGNORECASE)),
    ("subordination_nondisturbance", re.compile(r"\b(?:snda|subordination)\b", re.IGNORECASE)),
    ("tax_equity_financing", re.compile(r"\btax\s+equity\b", re.IGNORECASE)),
    ("met_tower_easement", re.compile(r"\b(?:met\s+tower|anemometer|meteorological)\b", re.IGNORECASE)),
    ("payment_escalation", re.compile(r"\bescalation\s+(?:clause|rate|provision)\b", re.IGNORECASE)),
    ("ira_2022", re.compile(r"\b(?:inflation\s+reduction\s+act|ira)\b", re.IGNORECASE)),
    ("estate_planning", re.compile(r"\bestate\s+planning\b", re.IGNORECASE)),
    ("life_estate", re.compile(r"\blife\s+estate\b", re.IGNORECASE)),
]


# ---------------------------------------------------------------------------
# Semantic Normalizer
# ---------------------------------------------------------------------------
class SemanticNormalizer:
    """
    Deterministic semantic normalization engine for wind/solar lease terminology.
    Maps variant phrasings to canonical concepts and identifies concept domains.
    """

    def __init__(self) -> None:
        self._synonym_map: dict[str, str] = SYNONYM_MAP
        self._concept_domain_map: dict[str, ConceptDomain] = CONCEPT_DOMAIN_MAP
        self._keyword_patterns: list[tuple[str, re.Pattern[str]]] = KEYWORD_PATTERNS
        logger.info(
            "SemanticNormalizer initialized: {syn} synonyms, {dom} concept mappings, {pat} patterns",
            syn=len(self._synonym_map),
            dom=len(self._concept_domain_map),
            pat=len(self._keyword_patterns),
        )

    def normalize_term(self, term: str) -> str:
        """Normalize a term to its canonical form."""
        cleaned = term.strip().lower()
        cleaned = re.sub(r"\s+", " ", cleaned)
        if cleaned in self._synonym_map:
            canonical = self._synonym_map[cleaned]
            logger.debug("Normalized '{term}' -> '{canonical}'", term=term, canonical=canonical)
            return canonical
        return cleaned

    def normalize_query(self, query: str) -> NormalizedQuery:
        """
        Normalize a full query string, extracting canonical concepts,
        domains, and keywords.
        """
        query_lower = query.strip().lower()
        query_clean = re.sub(r"\s+", " ", query_lower)

        # Phase 1: Direct synonym matching on substrings
        matched_concepts: list[str] = []
        for phrase, canonical in sorted(
            self._synonym_map.items(), key=lambda x: len(x[0]), reverse=True
        ):
            if phrase in query_clean:
                if canonical not in matched_concepts:
                    matched_concepts.append(canonical)

        # Phase 2: Regex keyword pattern matching
        for concept_key, pattern in self._keyword_patterns:
            if pattern.search(query_clean) and concept_key not in matched_concepts:
                matched_concepts.append(concept_key)

        # Phase 3: Determine domains
        matched_domains: list[ConceptDomain] = []
        for concept in matched_concepts:
            domain = self._concept_domain_map.get(concept)
            if domain and domain not in matched_domains:
                matched_domains.append(domain)

        # Phase 4: Extract raw keywords
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "to", "of", "in", "for",
            "on", "with", "at", "by", "from", "as", "into", "through", "during",
            "before", "after", "above", "below", "between", "under", "about",
            "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
            "neither", "each", "every", "all", "any", "few", "more", "most",
            "other", "some", "such", "no", "than", "too", "very", "just",
            "how", "what", "when", "where", "which", "who", "whom", "why",
            "this", "that", "these", "those", "my", "your", "his", "her",
            "its", "our", "their", "i", "me", "you", "he", "she", "it",
            "we", "they", "them", "if", "then", "else",
        }
        words = re.findall(r"\b[a-z]+\b", query_clean)
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        result = NormalizedQuery(
            original=query,
            normalized=query_clean,
            canonical_concepts=matched_concepts,
            domains=matched_domains,
            keywords=keywords,
        )

        logger.debug(
            "Query normalized: {n_concepts} concepts, {n_domains} domains",
            n_concepts=len(matched_concepts),
            n_domains=len(matched_domains),
        )
        return result

    def get_domain_for_concept(self, concept: str) -> Optional[ConceptDomain]:
        """Look up the domain for a canonical concept."""
        return self._concept_domain_map.get(concept)

    def get_all_concepts_in_domain(self, domain: ConceptDomain) -> list[str]:
        """Return all canonical concepts belonging to a specific domain."""
        return [
            concept
            for concept, d in self._concept_domain_map.items()
            if d == domain
        ]

    def suggest_related_concepts(self, concept: str) -> list[str]:
        """Suggest related concepts based on shared domain."""
        domain = self._concept_domain_map.get(concept)
        if not domain:
            return []
        related = self.get_all_concepts_in_domain(domain)
        return [c for c in related if c != concept]


# ---------------------------------------------------------------------------
# Normalized Query Result
# ---------------------------------------------------------------------------
@dataclass
class NormalizedQuery:
    """Result of semantic normalization on a query string."""
    original: str
    normalized: str
    canonical_concepts: list[str] = field(default_factory=list)
    domains: list[ConceptDomain] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)

    @property
    def primary_domain(self) -> Optional[ConceptDomain]:
        """Return the first matched domain, if any."""
        return self.domains[0] if self.domains else None

    @property
    def primary_concept(self) -> Optional[str]:
        """Return the first matched canonical concept, if any."""
        return self.canonical_concepts[0] if self.canonical_concepts else None

    def has_domain(self, domain: ConceptDomain) -> bool:
        """Check if a specific domain was matched."""
        return domain in self.domains

    def has_concept(self, concept: str) -> bool:
        """Check if a specific canonical concept was matched."""
        return concept in self.canonical_concepts


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
_normalizer: Optional[SemanticNormalizer] = None


def get_normalizer() -> SemanticNormalizer:
    """Get or create the module-level normalizer singleton."""
    global _normalizer
    if _normalizer is None:
        _normalizer = SemanticNormalizer()
    return _normalizer
