"""
LM22 Coal/Mineral Specific — Semantic Normalization Layer
Deterministic term normalization for coal, hard rock, and specialty mineral operations.

GOVERNANCE: This is a preprocessing layer. It must remain deterministic.
No vector inference. No embeddings. No auto-learning.

Author: ECHO OMEGA PRIME
Engine: LM22 Coal/Mineral Specific
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from loguru import logger

# ==============================================================================
# NORMALIZATION RESULT
# ==============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization."""
    original_term: str
    normalized_term: str
    canonical_form: str
    domain: str
    confidence: float
    synonyms_matched: List[str] = field(default_factory=list)
    context_hints: List[str] = field(default_factory=list)


# ==============================================================================
# COAL / MINERAL SEMANTIC DICTIONARY
# ==============================================================================

# Maps raw input terms to canonical forms within coal/mineral domain
COAL_MINERAL_SYNONYMS: Dict[str, str] = {
    # SMCRA / Surface Mining
    "smcra": "surface_mining_control_reclamation_act",
    "surface mining act": "surface_mining_control_reclamation_act",
    "strip mining": "surface_coal_mining",
    "strip mine": "surface_coal_mining",
    "surface mine": "surface_coal_mining",
    "open pit coal": "surface_coal_mining",
    "open cast mining": "surface_coal_mining",
    "mountaintop removal": "mountaintop_removal_mining",
    "mtr": "mountaintop_removal_mining",
    "mountain top removal": "mountaintop_removal_mining",
    "valley fill": "mountaintop_removal_mining",
    "osmre": "office_surface_mining_reclamation_enforcement",
    "office of surface mining": "office_surface_mining_reclamation_enforcement",
    "aml": "abandoned_mine_land",
    "abandoned mine": "abandoned_mine_land",
    "acid mine drainage": "acid_mine_drainage",
    "amd": "acid_mine_drainage",
    "acid drainage": "acid_mine_drainage",

    # Coal Types and Mining Methods
    "underground coal": "underground_coal_mining",
    "deep mine": "underground_coal_mining",
    "room and pillar": "room_and_pillar_mining",
    "longwall": "longwall_mining",
    "longwall mining": "longwall_mining",
    "auger mining": "auger_mining",
    "highwall mining": "highwall_mining",
    "bituminous": "bituminous_coal",
    "bituminous coal": "bituminous_coal",
    "anthracite": "anthracite_coal",
    "anthracite coal": "anthracite_coal",
    "sub-bituminous": "subbituminous_coal",
    "subbituminous": "subbituminous_coal",
    "lignite": "lignite_coal",
    "brown coal": "lignite_coal",
    "met coal": "metallurgical_coal",
    "metallurgical coal": "metallurgical_coal",
    "coking coal": "metallurgical_coal",
    "thermal coal": "thermal_coal",
    "steam coal": "thermal_coal",

    # Broad Form Deeds
    "broad form deed": "broad_form_deed",
    "broad form": "broad_form_deed",
    "mineral severance": "mineral_estate_severance",
    "severed minerals": "mineral_estate_severance",
    "mineral reservation": "mineral_reservation",
    "reserved minerals": "mineral_reservation",
    "dominant estate": "mineral_estate_dominance",
    "dominant mineral": "mineral_estate_dominance",
    "servient estate": "surface_estate_servient",

    # Coal Bed Methane
    "cbm": "coal_bed_methane",
    "coal bed methane": "coal_bed_methane",
    "coalbed methane": "coal_bed_methane",
    "coal seam gas": "coal_bed_methane",
    "csg": "coal_bed_methane",
    "coal mine methane": "coal_mine_methane",
    "cmm": "coal_mine_methane",
    "methane drainage": "mine_degasification",
    "degasification": "mine_degasification",
    "gob gas": "mine_degasification",

    # Hard Rock Mining
    "hard rock": "hardrock_mining",
    "hardrock": "hardrock_mining",
    "hard rock mining": "hardrock_mining",
    "metallic mining": "hardrock_mining",
    "1872 mining law": "general_mining_law_1872",
    "general mining law": "general_mining_law_1872",
    "mining law of 1872": "general_mining_law_1872",
    "locatable mineral": "locatable_mineral",
    "locatable minerals": "locatable_mineral",
    "mining claim": "mining_claim",
    "lode claim": "lode_claim",
    "placer claim": "placer_claim",
    "mill site": "mill_site_claim",
    "tunnel site": "tunnel_site_claim",
    "extralateral rights": "extralateral_rights",
    "apex rule": "extralateral_rights",

    # Mining Claims Maintenance
    "assessment work": "annual_assessment_work",
    "annual labor": "annual_assessment_work",
    "assessment labor": "annual_assessment_work",
    "maintenance fee": "annual_maintenance_fee",
    "claim maintenance": "annual_maintenance_fee",
    "165 fee": "annual_maintenance_fee",
    "small miner waiver": "small_miner_waiver",
    "small miner": "small_miner_waiver",

    # Patent System
    "mineral patent": "mining_claim_patent",
    "patent": "mining_claim_patent",
    "unpatented claim": "unpatented_mining_claim",
    "unpatented": "unpatented_mining_claim",
    "patent moratorium": "patent_moratorium",

    # Mineral Leasing
    "mineral leasing act": "mineral_leasing_act_1920",
    "mla": "mineral_leasing_act_1920",
    "coal lease": "federal_coal_lease",
    "federal coal lease": "federal_coal_lease",
    "coal leasing": "federal_coal_lease",
    "leasable mineral": "leasable_mineral",
    "leasable minerals": "leasable_mineral",
    "materials act": "materials_act_1947",
    "salable mineral": "salable_mineral",
    "common variety": "common_variety_mineral",

    # Uranium
    "uranium": "uranium_mining",
    "uranium mining": "uranium_mining",
    "yellowcake": "uranium_concentrate",
    "u3o8": "uranium_concentrate",
    "in situ leaching": "in_situ_recovery",
    "in situ recovery": "in_situ_recovery",
    "isl": "in_situ_recovery",
    "isr": "in_situ_recovery",
    "nrc": "nuclear_regulatory_commission",
    "nuclear regulatory commission": "nuclear_regulatory_commission",
    "source material": "nrc_source_material",
    "agreement state": "nrc_agreement_state",

    # Reclamation
    "reclamation": "mine_reclamation",
    "reclamation bond": "reclamation_performance_bond",
    "performance bond": "reclamation_performance_bond",
    "surety bond": "surety_bond",
    "self bond": "self_bonding",
    "self-bond": "self_bonding",
    "self-bonding": "self_bonding",
    "pool bond": "alternative_bonding_system",
    "bond release": "bond_release_phased",
    "phase release": "bond_release_phased",
    "aoc": "approximate_original_contour",
    "approximate original contour": "approximate_original_contour",
    "revegetation": "reclamation_revegetation",
    "topsoil": "topsoil_preservation",

    # Support Doctrines
    "lateral support": "lateral_support_doctrine",
    "subjacent support": "subjacent_support_doctrine",
    "mine subsidence": "mine_subsidence",
    "subsidence": "mine_subsidence",
    "surface subsidence": "mine_subsidence",
    "pillar removal": "pillar_extraction",

    # Surface Rights
    "surface consent": "surface_owner_consent",
    "surface owner consent": "surface_owner_consent",
    "surface damage act": "surface_damage_act",
    "accommodation doctrine": "accommodation_doctrine",
    "reasonable use": "reasonable_use_doctrine",

    # Geothermal
    "geothermal": "geothermal_resource",
    "geothermal energy": "geothermal_resource",
    "geothermal lease": "geothermal_lease",
    "steam act": "geothermal_steam_act_1970",
    "geothermal steam act": "geothermal_steam_act_1970",
    "kgra": "known_geothermal_resource_area",
    "hot springs": "geothermal_hot_springs",

    # Lithium / Rare Earth
    "lithium": "lithium_mineral",
    "lithium mining": "lithium_mineral",
    "lithium brine": "lithium_brine_deposit",
    "spodumene": "lithium_hardrock_spodumene",
    "rare earth": "rare_earth_elements",
    "ree": "rare_earth_elements",
    "rare earth elements": "rare_earth_elements",
    "critical mineral": "critical_mineral",
    "critical minerals": "critical_mineral",
    "dle": "direct_lithium_extraction",
    "direct lithium extraction": "direct_lithium_extraction",

    # Carbon Sequestration
    "carbon sequestration": "carbon_capture_sequestration",
    "ccs": "carbon_capture_sequestration",
    "ccus": "carbon_capture_utilization_storage",
    "co2 storage": "carbon_capture_sequestration",
    "pore space": "subsurface_pore_space",
    "pore space rights": "subsurface_pore_space",
    "45q": "section_45q_tax_credit",
    "45q credit": "section_45q_tax_credit",
    "class vi well": "epa_class_vi_well",
    "class vi": "epa_class_vi_well",

    # Helium
    "helium": "helium_extraction",
    "helium rights": "helium_extraction",
    "federal helium reserve": "federal_helium_reserve",
    "noble gas": "noble_gas_extraction",

    # Aggregate
    "aggregate": "aggregate_extraction",
    "sand and gravel": "sand_gravel_extraction",
    "sand gravel": "sand_gravel_extraction",
    "gravel pit": "sand_gravel_extraction",
    "quarry": "quarry_operation",
    "limestone": "limestone_quarrying",
    "caliche": "caliche_extraction",
    "crushed stone": "crushed_stone_production",

    # Severance Tax
    "severance tax": "mineral_severance_tax",
    "production tax": "mineral_severance_tax",
    "mining tax": "mineral_severance_tax",
    "extraction tax": "mineral_severance_tax",

    # Subsurface Trespass
    "subsurface trespass": "subsurface_trespass",
    "underground trespass": "subsurface_trespass",
    "mineral trespass": "subsurface_trespass",
    "mining trespass": "subsurface_trespass",
    "good faith trespass": "good_faith_mineral_trespass",
    "bad faith trespass": "bad_faith_mineral_trespass",

    # Agencies
    "blm": "bureau_land_management",
    "bureau of land management": "bureau_land_management",
    "msha": "mine_safety_health_administration",
    "mine safety": "mine_safety_health_administration",
    "epa": "environmental_protection_agency",
    "bia": "bureau_indian_affairs",
    "usfs": "us_forest_service",
    "forest service": "us_forest_service",
}

# Domain classification for normalized terms
DOMAIN_MAP: Dict[str, str] = {
    "surface_mining_control_reclamation_act": "coal_regulation",
    "surface_coal_mining": "coal_mining",
    "mountaintop_removal_mining": "coal_mining",
    "office_surface_mining_reclamation_enforcement": "coal_regulation",
    "abandoned_mine_land": "coal_regulation",
    "acid_mine_drainage": "environmental",
    "underground_coal_mining": "coal_mining",
    "room_and_pillar_mining": "coal_mining",
    "longwall_mining": "coal_mining",
    "auger_mining": "coal_mining",
    "highwall_mining": "coal_mining",
    "bituminous_coal": "coal_classification",
    "anthracite_coal": "coal_classification",
    "subbituminous_coal": "coal_classification",
    "lignite_coal": "coal_classification",
    "metallurgical_coal": "coal_classification",
    "thermal_coal": "coal_classification",
    "broad_form_deed": "mineral_estates",
    "mineral_estate_severance": "mineral_estates",
    "mineral_reservation": "mineral_estates",
    "mineral_estate_dominance": "mineral_estates",
    "surface_estate_servient": "mineral_estates",
    "coal_bed_methane": "cbm",
    "coal_mine_methane": "cbm",
    "mine_degasification": "cbm",
    "hardrock_mining": "hardrock",
    "general_mining_law_1872": "hardrock",
    "locatable_mineral": "mineral_classification",
    "mining_claim": "claims",
    "lode_claim": "claims",
    "placer_claim": "claims",
    "mill_site_claim": "claims",
    "tunnel_site_claim": "claims",
    "extralateral_rights": "claims",
    "annual_assessment_work": "claims_maintenance",
    "annual_maintenance_fee": "claims_maintenance",
    "small_miner_waiver": "claims_maintenance",
    "mining_claim_patent": "patent",
    "unpatented_mining_claim": "patent",
    "patent_moratorium": "patent",
    "mineral_leasing_act_1920": "leasing",
    "federal_coal_lease": "leasing",
    "leasable_mineral": "mineral_classification",
    "salable_mineral": "mineral_classification",
    "common_variety_mineral": "mineral_classification",
    "materials_act_1947": "leasing",
    "uranium_mining": "uranium",
    "uranium_concentrate": "uranium",
    "in_situ_recovery": "uranium",
    "nuclear_regulatory_commission": "uranium",
    "nrc_source_material": "uranium",
    "nrc_agreement_state": "uranium",
    "mine_reclamation": "reclamation",
    "reclamation_performance_bond": "bonding",
    "surety_bond": "bonding",
    "self_bonding": "bonding",
    "alternative_bonding_system": "bonding",
    "bond_release_phased": "bonding",
    "approximate_original_contour": "reclamation",
    "reclamation_revegetation": "reclamation",
    "topsoil_preservation": "reclamation",
    "lateral_support_doctrine": "support",
    "subjacent_support_doctrine": "support",
    "mine_subsidence": "support",
    "pillar_extraction": "coal_mining",
    "surface_owner_consent": "surface_rights",
    "surface_damage_act": "surface_rights",
    "accommodation_doctrine": "surface_rights",
    "reasonable_use_doctrine": "surface_rights",
    "geothermal_resource": "geothermal",
    "geothermal_lease": "geothermal",
    "geothermal_steam_act_1970": "geothermal",
    "known_geothermal_resource_area": "geothermal",
    "geothermal_hot_springs": "geothermal",
    "lithium_mineral": "critical_minerals",
    "lithium_brine_deposit": "critical_minerals",
    "lithium_hardrock_spodumene": "critical_minerals",
    "rare_earth_elements": "critical_minerals",
    "critical_mineral": "critical_minerals",
    "direct_lithium_extraction": "critical_minerals",
    "carbon_capture_sequestration": "carbon_storage",
    "carbon_capture_utilization_storage": "carbon_storage",
    "subsurface_pore_space": "carbon_storage",
    "section_45q_tax_credit": "carbon_storage",
    "epa_class_vi_well": "carbon_storage",
    "helium_extraction": "specialty_gas",
    "federal_helium_reserve": "specialty_gas",
    "noble_gas_extraction": "specialty_gas",
    "aggregate_extraction": "construction_minerals",
    "sand_gravel_extraction": "construction_minerals",
    "quarry_operation": "construction_minerals",
    "limestone_quarrying": "construction_minerals",
    "caliche_extraction": "construction_minerals",
    "crushed_stone_production": "construction_minerals",
    "mineral_severance_tax": "taxation",
    "subsurface_trespass": "trespass",
    "good_faith_mineral_trespass": "trespass",
    "bad_faith_mineral_trespass": "trespass",
    "bureau_land_management": "agencies",
    "mine_safety_health_administration": "agencies",
    "environmental_protection_agency": "agencies",
    "bureau_indian_affairs": "agencies",
    "us_forest_service": "agencies",
}


def normalize_semantics(query: str) -> NormalizationResult:
    """
    Normalize a coal/mineral domain query into canonical form.
    Deterministic — no probabilistic models, no embeddings.
    """
    query_lower = query.lower().strip()
    matched_synonyms: List[str] = []
    best_match: Optional[str] = None
    best_confidence: float = 0.0

    # Phase 1: Exact match
    if query_lower in COAL_MINERAL_SYNONYMS:
        canonical = COAL_MINERAL_SYNONYMS[query_lower]
        domain = DOMAIN_MAP.get(canonical, "general")
        return NormalizationResult(
            original_term=query,
            normalized_term=canonical,
            canonical_form=canonical,
            domain=domain,
            confidence=1.0,
            synonyms_matched=[query_lower],
            context_hints=[f"Exact match in coal/mineral dictionary → {canonical}"],
        )

    # Phase 2: Substring match — find longest matching synonym within query
    for synonym, canonical in sorted(COAL_MINERAL_SYNONYMS.items(), key=lambda x: -len(x[0])):
        if synonym in query_lower:
            if len(synonym) > len(best_match or ""):
                best_match = canonical
                best_confidence = 0.85
                matched_synonyms.append(synonym)

    if best_match:
        domain = DOMAIN_MAP.get(best_match, "general")
        return NormalizationResult(
            original_term=query,
            normalized_term=best_match,
            canonical_form=best_match,
            domain=domain,
            confidence=best_confidence,
            synonyms_matched=matched_synonyms,
            context_hints=[f"Substring match: '{matched_synonyms[0]}' → {best_match}"],
        )

    # Phase 3: Token overlap — match individual words
    query_tokens = set(query_lower.split())
    best_overlap_score = 0.0
    best_overlap_match: Optional[str] = None
    best_overlap_synonyms: List[str] = []

    for synonym, canonical in COAL_MINERAL_SYNONYMS.items():
        synonym_tokens = set(synonym.split())
        overlap = query_tokens & synonym_tokens
        if overlap:
            score = len(overlap) / max(len(synonym_tokens), 1)
            if score > best_overlap_score:
                best_overlap_score = score
                best_overlap_match = canonical
                best_overlap_synonyms = [synonym]

    if best_overlap_match and best_overlap_score >= 0.5:
        domain = DOMAIN_MAP.get(best_overlap_match, "general")
        return NormalizationResult(
            original_term=query,
            normalized_term=best_overlap_match,
            canonical_form=best_overlap_match,
            domain=domain,
            confidence=round(best_overlap_score * 0.7, 2),
            synonyms_matched=best_overlap_synonyms,
            context_hints=[f"Token overlap match (score={best_overlap_score:.2f})"],
        )

    # Phase 4: No match — return identity normalization
    logger.debug(f"No semantic normalization match for: {query}")
    return NormalizationResult(
        original_term=query,
        normalized_term=query_lower.replace(" ", "_"),
        canonical_form=query_lower.replace(" ", "_"),
        domain="unknown",
        confidence=0.0,
        synonyms_matched=[],
        context_hints=["No match in coal/mineral semantic dictionary"],
    )


def get_domain_terms(domain: str) -> List[str]:
    """Return all canonical terms belonging to a specific domain."""
    return [term for term, dom in DOMAIN_MAP.items() if dom == domain]


def get_all_domains() -> List[str]:
    """Return list of all domains in the semantic dictionary."""
    return sorted(set(DOMAIN_MAP.values()))


def get_synonym_count() -> int:
    """Return total number of synonym mappings."""
    return len(COAL_MINERAL_SYNONYMS)


def get_canonical_count() -> int:
    """Return total number of unique canonical forms."""
    return len(set(COAL_MINERAL_SYNONYMS.values()))


def reverse_lookup(canonical: str) -> List[str]:
    """Find all synonyms that map to a given canonical form."""
    return [syn for syn, can in COAL_MINERAL_SYNONYMS.items() if can == canonical]
