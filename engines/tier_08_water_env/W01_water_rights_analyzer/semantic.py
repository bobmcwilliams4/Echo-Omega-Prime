import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "W01_engine_team"
SEMANTIC_MAP_ENGINE = "W01_water_rights_analyzer"

SEMANTIC_MAP = {
    # Texas Water Code Fundamentals
    "texas water code": "texas_water_code",
    "twc": "texas_water_code",
    "tx water code": "texas_water_code",
    "texas water law": "texas_water_code",
    "water code": "texas_water_code",
    "texas water statutes": "texas_water_code",
    "water statutes": "texas_water_code",
    "texas water regulations": "texas_water_code",
    "water regulations": "texas_water_code",
    "texas water policy": "texas_water_code",
    "water policy": "texas_water_code",
    "twc fundamentals": "texas_water_code",
    "twc basics": "texas_water_code",

    # Prior Appropriation Doctrine
    "prior appropriation": "prior_appropriation_doctrine",
    "prior appropriation doctrine": "prior_appropriation_doctrine",
    "first in time first in right": "prior_appropriation_doctrine",
    "fitfir": "prior_appropriation_doctrine",
    "appropriation doctrine": "prior_appropriation_doctrine",
    "water appropriations": "prior_appropriation_doctrine",
    "water rights doctrine": "prior_appropriation_doctrine",
    "appropriation system": "prior_appropriation_doctrine",
    "prior rights": "prior_appropriation_doctrine",
    "senior rights": "prior_appropriation_doctrine",
    "junior rights": "prior_appropriation_doctrine",

    # Rule of Capture for Groundwater
    "rule of capture": "rule_of_capture",
    "groundwater rule of capture": "rule_of_capture",
    "roc": "rule_of_capture",
    "capture rule": "rule_of_capture",
    "texas groundwater law": "rule_of_capture",
    "groundwater ownership": "rule_of_capture",
    "ownership in place": "rule_of_capture",
    "absolute ownership": "rule_of_capture",
    "groundwater rights": "rule_of_capture",
    "groundwater extraction": "rule_of_capture",
    "well ownership": "rule_of_capture",

    # Groundwater Conservation District Rules
    "groundwater conservation district": "groundwater_conservation_district_rules",
    "gcd": "groundwater_conservation_district_rules",
    "gcd rules": "groundwater_conservation_district_rules",
    "groundwater district rules": "groundwater_conservation_district_rules",
    "conservation district": "groundwater_conservation_district_rules",
    "conservation district rules": "groundwater_conservation_district_rules",
    "local groundwater regulation": "groundwater_conservation_district_rules",
    "district management plan": "groundwater_conservation_district_rules",
    "gcd management plan": "groundwater_conservation_district_rules",
    "gcd permit": "groundwater_conservation_district_rules",
    "groundwater permitting": "groundwater_conservation_district_rules",
    "gcd permitting": "groundwater_conservation_district_rules",
    "gcd registration": "groundwater_conservation_district_rules",
    "gcd monitoring": "groundwater_conservation_district_rules",

    # Permian Basin GCD Regulations
    "permian basin gcd": "permian_basin_gcd_regulations",
    "permian basin groundwater conservation district": "permian_basin_gcd_regulations",
    "pb gcd": "permian_basin_gcd_regulations",
    "permian basin regulations": "permian_basin_gcd_regulations",
    "permian basin groundwater": "permian_basin_gcd_regulations",
    "permian basin district": "permian_basin_gcd_regulations",
    "permian basin management": "permian_basin_gcd_regulations",
    "permian basin rules": "permian_basin_gcd_regulations",
    "pb groundwater": "permian_basin_gcd_regulations",
    "pb district": "permian_basin_gcd_regulations",

    # Surface Water Permits (TCEQ)
    "surface water permit": "surface_water_permits",
    "surface water permits": "surface_water_permits",
    "surface water permitting": "surface_water_permits",
    "tceq surface water permit": "surface_water_permits",
    "tceq permit": "surface_water_permits",
    "texas commission on environmental quality": "surface_water_permits",
    "tceq": "surface_water_permits",
    "surface water application": "surface_water_permits",
    "water permit": "surface_water_permits",
    "water permitting": "surface_water_permits",
    "surface water rights": "surface_water_permits",
    "surface water allocation": "surface_water_permits",
    "surface water diversion": "surface_water_permits",
    "surface water withdrawal": "surface_water_permits",
    "surface water use": "surface_water_permits",

    # Water Rights Transfers
    "water rights transfer": "water_rights_transfers",
    "water rights transfers": "water_rights_transfers",
    "transfer of water rights": "water_rights_transfers",
    "water rights assignment": "water_rights_transfers",
    "water rights sale": "water_rights_transfers",
    "water rights lease": "water_rights_transfers",
    "water rights exchange": "water_rights_transfers",
    "water rights conveyance": "water_rights_transfers",
    "water rights transaction": "water_rights_transfers",
    "water rights market": "water_rights_transfers",
    "water rights trading": "water_rights_transfers",
    "water rights purchase": "water_rights_transfers",

    # Produced Water Regulations
    "produced water": "produced_water_regulations",
    "produced water regulations": "produced_water_regulations",
    "oilfield water": "produced_water_regulations",
    "oil and gas produced water": "produced_water_regulations",
    "pw": "produced_water_regulations",
    "produced water management": "produced_water_regulations",
    "produced water disposal": "produced_water_regulations",
    "produced water reuse": "produced_water_regulations",
    "produced water treatment": "produced_water_regulations",
    "produced water permit": "produced_water_regulations",
    "produced water discharge": "produced_water_regulations",
    "produced water recycling": "produced_water_regulations",
    "produced water injection": "produced_water_regulations",

    # Recycled Water Permits
    "recycled water": "recycled_water_permits",
    "recycled water permit": "recycled_water_permits",
    "recycled water permits": "recycled_water_permits",
    "water recycling": "recycled_water_permits",
    "water reuse": "recycled_water_permits",
    "reuse permit": "recycled_water_permits",
    "reuse water permit": "recycled_water_permits",
    "reclaimed water": "recycled_water_permits",
    "reclaimed water permit": "recycled_water_permits",
    "reclaimed water permits": "recycled_water_permits",
    "recycled water application": "recycled_water_permits",
    "recycled water regulation": "recycled_water_permits",
    "recycled water management": "recycled_water_permits",

    # Water Marketing
    "water marketing": "water_marketing",
    "water market": "water_marketing",
    "water markets": "water_marketing",
    "water trading": "water_marketing",
    "water exchange": "water_marketing",
    "water sale": "water_marketing",
    "water purchase": "water_marketing",
    "water lease": "water_marketing",
    "water auction": "water_marketing",
    "water commodity": "water_marketing",
    "water price": "water_marketing",
    "water transaction": "water_marketing",
    "water transfer": "water_marketing",

    # Edwards Aquifer Authority
    "edwards aquifer authority": "edwards_aquifer_authority",
    "eaa": "edwards_aquifer_authority",
    "edwards aquifer": "edwards_aquifer_authority",
    "edwards aquifer regulation": "edwards_aquifer_authority",
    "edwards aquifer permit": "edwards_aquifer_authority",
    "edwards aquifer management": "edwards_aquifer_authority",
    "edwards aquifer rules": "edwards_aquifer_authority",
    "edwards aquifer district": "edwards_aquifer_authority",
    "edwards aquifer conservation": "edwards_aquifer_authority",
    "edwards aquifer recharge": "edwards_aquifer_authority",

    # Ogallala Aquifer Depletion
    "ogallala aquifer": "ogallala_aquifer_depletion",
    "ogallala": "ogallala_aquifer_depletion",
    "ogallala depletion": "ogallala_aquifer_depletion",
    "ogallala aquifer depletion": "ogallala_aquifer_depletion",
    "ogallala aquifer decline": "ogallala_aquifer_depletion",
    "ogallala aquifer management": "ogallala_aquifer_depletion",
    "ogallala aquifer conservation": "ogallala_aquifer_depletion",
    "ogallala aquifer recharge": "ogallala_aquifer_depletion",
    "ogallala aquifer rules": "ogallala_aquifer_depletion",
    "ogallala aquifer regulation": "ogallala_aquifer_depletion",

    # Brackish Water Zones
    "brackish water": "brackish_water_zones",
    "brackish water zone": "brackish_water_zones",
    "brackish water zones": "brackish_water_zones",
    "brackish groundwater": "brackish_water_zones",
    "brackish aquifer": "brackish_water_zones",
    "brackish water regulation": "brackish_water_zones",
    "brackish water management": "brackish_water_zones",
    "brackish water permit": "brackish_water_zones",
    "brackish water extraction": "brackish_water_zones",
    "brackish water use": "brackish_water_zones",

    # Desalination Permits
    "desalination": "desalination_permits",
    "desalination permit": "desalination_permits",
    "desalination permits": "desalination_permits",
    "desalination regulation": "desalination_permits",
    "desalination management": "desalination_permits",
    "desalination plant": "desalination_permits",
    "desalination facility": "desalination_permits",
    "desalination application": "desalination_permits",
    "desalination water": "desalination_permits",
    "desalination project": "desalination_permits",

    # Interstate Compacts
    "interstate compact": "interstate_compacts",
    "interstate compacts": "interstate_compacts",
    "water compact": "interstate_compacts",
    "water compacts": "interstate_compacts",
    "river compact": "interstate_compacts",
    "river compacts": "interstate_compacts",
    "interstate water agreement": "interstate_compacts",
    "interstate water agreements": "interstate_compacts",
    "interstate water regulation": "interstate_compacts",
    "interstate water management": "interstate_compacts",

    # Rio Grande Compact
    "rio grande compact": "rio_grande_compact",
    "rio grande": "rio_grande_compact",
    "rgc": "rio_grande_compact",
    "rio grande agreement": "rio_grande_compact",
    "rio grande water": "rio_grande_compact",
    "rio grande regulation": "rio_grande_compact",
    "rio grande management": "rio_grande_compact",
    "rio grande allocation": "rio_grande_compact",
    "rio grande permit": "rio_grande_compact",
    "rio grande treaty": "rio_grande_compact",

    # Pecos River Compact
    "pecos river compact": "pecos_river_compact",
    "pecos river": "pecos_river_compact",
    "prc": "pecos_river_compact",
    "pecos river agreement": "pecos_river_compact",
    "pecos river regulation": "pecos_river_compact",
    "pecos river management": "pecos_river_compact",
    "pecos river allocation": "pecos_river_compact",
    "pecos river permit": "pecos_river_compact",
    "pecos river treaty": "pecos_river_compact",

    # Water Conservation Requirements
    "water conservation": "water_conservation_requirements",
    "water conservation requirement": "water_conservation_requirements",
    "water conservation requirements": "water_conservation_requirements",
    "water conservation regulation": "water_conservation_requirements",
    "water conservation rules": "water_conservation_requirements",
    "water conservation plan": "water_conservation_requirements",
    "water conservation policy": "water_conservation_requirements",
    "water conservation program": "water_conservation_requirements",
    "water conservation mandate": "water_conservation_requirements",
    "water conservation initiative": "water_conservation_requirements",

    # Drought Contingency
    "drought contingency": "drought_contingency",
    "drought contingency plan": "drought_contingency",
    "drought contingency planning": "drought_contingency",
    "drought contingency regulation": "drought_contingency",
    "drought contingency rules": "drought_contingency",
    "drought contingency requirement": "drought_contingency",
    "drought contingency requirements": "drought_contingency",
    "drought contingency policy": "drought_contingency",
    "drought contingency program": "drought_contingency",
    "drought contingency mandate": "drought_contingency",

    # Water Availability Modeling
    "water availability modeling": "water_availability_modeling",
    "water availability model": "water_availability_modeling",
    "water availability models": "water_availability_modeling",
    "wam": "water_availability_modeling",
    "water modeling": "water_availability_modeling",
    "water model": "water_availability_modeling",
    "water models": "water_availability_modeling",
    "water supply modeling": "water_availability_modeling",
    "water supply model": "water_availability_modeling",
    "water supply models": "water_availability_modeling",
    "water allocation modeling": "water_availability_modeling",
    "water allocation model": "water_availability_modeling",
    "water allocation models": "water_availability_modeling",
    "hydrologic modeling": "water_availability_modeling",
    "hydrologic model": "water_availability_modeling",
    "hydrologic models": "water_availability_modeling",

    # Additional synonyms, misspellings, abbreviations, and related terms
    "texas water": "texas_water_code",
    "texas surface water": "surface_water_permits",
    "texas groundwater": "rule_of_capture",
    "water law": "texas_water_code",
    "water rights": "prior_appropriation_doctrine",
    "water right": "prior_appropriation_doctrine",
    "water allocation": "surface_water_permits",
    "water transfer": "water_rights_transfers",
    "water regulation": "texas_water_code",
    "water permit": "surface_water_permits",
    "water permits": "surface_water_permits",
    "water management": "groundwater_conservation_district_rules",
    "water district": "groundwater_conservation_district_rules",
    "water district rules": "groundwater_conservation_district_rules",
    "water district regulation": "groundwater_conservation_district_rules",
    "water district management": "groundwater_conservation_district_rules",
    "water district permit": "groundwater_conservation_district_rules",
    "water district monitoring": "groundwater_conservation_district_rules",
    "water district registration": "groundwater_conservation_district_rules",
    "water district conservation": "groundwater_conservation_district_rules",

    # Misspellings and variants
    "texas watter code": "texas_water_code",
    "texas water cdoe": "texas_water_code",
    "prior apropriation": "prior_appropriation_doctrine",
    "prior appropriaton": "prior_appropriation_doctrine",
    "rule of captur": "rule_of_capture",
    "groundwater conservation distrct": "groundwater_conservation_district_rules",
    "permian basin groundwatr": "permian_basin_gcd_regulations",
    "surface watter permit": "surface_water_permits",
    "water rights tranfer": "water_rights_transfers",
    "produced watter": "produced_water_regulations",
    "recyled water": "recycled_water_permits",
    "water markting": "water_marketing",
    "edwards aquifer authrity": "edwards_aquifer_authority",
    "ogallala aquifer depletin": "ogallala_aquifer_depletion",
    "brackish watter": "brackish_water_zones",
    "desalintion permit": "desalination_permits",
    "interstate compct": "interstate_compacts",
    "rio grande compct": "rio_grande_compact",
    "pecos river compct": "pecos_river_compact",
    "water conservaton": "water_conservation_requirements",
    "drought contigency": "drought_contingency",
    "water availabilty modeling": "water_availability_modeling",

    # Related terms (cross-references)
    "water supply": "water_availability_modeling",
    "water supply planning": "water_availability_modeling",
    "water supply regulation": "water_availability_modeling",
    "water supply allocation": "water_availability_modeling",
    "water supply requirement": "water_availability_modeling",
    "water supply requirements": "water_availability_modeling",
    "water supply permit": "water_availability_modeling",
    "water supply permits": "water_availability_modeling",
    "water supply management": "water_availability_modeling",
    "water supply models": "water_availability_modeling",

    # More abbreviations and acronyms
    "gcds": "groundwater_conservation_district_rules",
    "pb gcds": "permian_basin_gcd_regulations",
    "pw regs": "produced_water_regulations",
    "rw permits": "recycled_water_permits",
    "eaa regs": "edwards_aquifer_authority",
    "ogallala regs": "ogallala_aquifer_depletion",
    "bw zones": "brackish_water_zones",
    "desal permits": "desalination_permits",
    "ic": "interstate_compacts",
    "rgc regs": "rio_grande_compact",
    "prc regs": "pecos_river_compact",
    "wcr": "water_conservation_requirements",
    "dc": "drought_contingency",
    "wam models": "water_availability_modeling",

    # Misspellings of abbreviations
    "twc fundementals": "texas_water_code",
    "fitfirr": "prior_appropriation_doctrine",
    "roc rule": "rule_of_capture",
    "gcd rule": "groundwater_conservation_district_rules",
    "pb gcd regs": "permian_basin_gcd_regulations",
    "tceq surface water permits": "surface_water_permits",
    "pw regulation": "produced_water_regulations",
    "rw permit": "recycled_water_permits",
    "eaa regulation": "edwards_aquifer_authority",
    "ogallala regulation": "ogallala_aquifer_depletion",
    "bw zone": "brackish_water_zones",
    "desal permit": "desalination_permits",
    "ic regulation": "interstate_compacts",
    "rgc regulation": "rio_grande_compact",
    "prc regulation": "pecos_river_compact",
    "wcr regulation": "water_conservation_requirements",
    "dc regulation": "drought_contingency",
    "wam model": "water_availability_modeling",

    # More related terms
    "water reuse permit": "recycled_water_permits",
    "water reuse regulation": "recycled_water_permits",
    "water reuse management": "recycled_water_permits",
    "water reuse application": "recycled_water_permits",
    "water reuse project": "recycled_water_permits",
    "water reuse facility": "recycled_water_permits",
    "water reuse plant": "recycled_water_permits",
    "water reuse program": "recycled_water_permits",
    "water reuse initiative": "recycled_water_permits",

    # Water marketing variants
    "water trading permit": "water_marketing",
    "water trading regulation": "water_marketing",
    "water trading management": "water_marketing",
    "water trading application": "water_marketing",
    "water trading project": "water_marketing",
    "water trading facility": "water_marketing",
    "water trading plant": "water_marketing",
    "water trading program": "water_marketing",
    "water trading initiative": "water_marketing",

    # Water conservation variants
    "water conservation application": "water_conservation_requirements",
    "water conservation project": "water_conservation_requirements",
    "water conservation facility": "water_conservation_requirements",
    "water conservation plant": "water_conservation_requirements",
    "water conservation program": "water_conservation_requirements",
    "water conservation initiative": "water_conservation_requirements",

    # Drought contingency variants
    "drought contingency application": "drought_contingency",
    "drought contingency project": "drought_contingency",
    "drought contingency facility": "drought_contingency",
    "drought contingency plant": "drought_contingency",
    "drought contingency program": "drought_contingency",
    "drought contingency initiative": "drought_contingency",

    # Water availability modeling variants
    "water availability modeling application": "water_availability_modeling",
    "water availability modeling project": "water_availability_modeling",
    "water availability modeling facility": "water_availability_modeling",
    "water availability modeling plant": "water_availability_modeling",
    "water availability modeling program": "water_availability_modeling",
    "water availability modeling initiative": "water_availability_modeling",

    # Brackish water variants
    "brackish water application": "brackish_water_zones",
    "brackish water project": "brackish_water_zones",
    "brackish water facility": "brackish_water_zones",
    "brackish water plant": "brackish_water_zones",
    "brackish water program": "brackish_water_zones",
    "brackish water initiative": "brackish_water_zones",

    # Desalination variants
    "desalination application": "desalination_permits",
    "desalination project": "desalination_permits",
    "desalination facility": "desalination_permits",
    "desalination plant": "desalination_permits",
    "desalination program": "desalination_permits",
    "desalination initiative": "desalination_permits",

    # Interstate compact variants
    "interstate compact application": "interstate_compacts",
    "interstate compact project": "interstate_compacts",
    "interstate compact facility": "interstate_compacts",
    "interstate compact plant": "interstate_compacts",
    "interstate compact program": "interstate_compacts",
    "interstate compact initiative": "interstate_compacts",

    # Rio Grande compact variants
    "rio grande compact application": "rio_grande_compact",
    "rio grande compact project": "rio_grande_compact",
    "rio grande compact facility": "rio_grande_compact",
    "rio grande compact plant": "rio_grande_compact",
    "rio grande compact program": "rio_grande_compact",
    "rio grande compact initiative": "rio_grande_compact",

    # Pecos River compact variants
    "pecos river compact application": "pecos_river_compact",
    "pecos river compact project": "pecos_river_compact",
    "pecos river compact facility": "pecos_river_compact",
    "pecos river compact plant": "pecos_river_compact",
    "pecos river compact program": "pecos_river_compact",
    "pecos river compact initiative": "pecos_river_compact",

    # Produced water variants
    "produced water application": "produced_water_regulations",
    "produced water project": "produced_water_regulations",
    "produced water facility": "produced_water_regulations",
    "produced water plant": "produced_water_regulations",
    "produced water program": "produced_water_regulations",
    "produced water initiative": "produced_water_regulations",

    # Surface water variants
    "surface water application": "surface_water_permits",
    "surface water project": "surface_water_permits",
    "surface water facility": "surface_water_permits",
    "surface water plant": "surface_water_permits",
    "surface water program": "surface_water_permits",
    "surface water initiative": "surface_water_permits",

    # Water rights transfer variants
    "water rights transfer application": "water_rights_transfers",
    "water rights transfer project": "water_rights_transfers",
    "water rights transfer facility": "water_rights_transfers",
    "water rights transfer plant": "water_rights_transfers",
    "water rights transfer program": "water_rights_transfers",
    "water rights transfer initiative": "water_rights_transfers",

    # Groundwater conservation district variants
    "groundwater conservation district application": "groundwater_conservation_district_rules",
    "groundwater conservation district project": "groundwater_conservation_district_rules",
    "groundwater conservation district facility": "groundwater_conservation_district_rules",
    "groundwater conservation district plant": "groundwater_conservation_district_rules",
    "groundwater conservation district program": "groundwater_conservation_district_rules",
    "groundwater conservation district initiative": "groundwater_conservation_district_rules",

    # Permian Basin GCD variants
    "permian basin gcd application": "permian_basin_gcd_regulations",
    "permian basin gcd project": "permian_basin_gcd_regulations",
    "permian basin gcd facility": "permian_basin_gcd_regulations",
    "permian basin gcd plant": "permian_basin_gcd_regulations",
    "permian basin gcd program": "permian_basin_gcd_regulations",
    "permian basin gcd initiative": "permian_basin_gcd_regulations",

    # Edwards Aquifer Authority variants
    "edwards aquifer authority application": "edwards_aquifer_authority",
    "edwards aquifer authority project": "edwards_aquifer_authority",
    "edwards aquifer authority facility": "edwards_aquifer_authority",
    "edwards aquifer authority plant": "edwards_aquifer_authority",
    "edwards aquifer authority program": "edwards_aquifer_authority",
    "edwards aquifer authority initiative": "edwards_aquifer_authority",

    # Ogallala Aquifer Depletion variants
    "ogallala aquifer depletion application": "ogallala_aquifer_depletion",
    "ogallala aquifer depletion project": "ogallala_aquifer_depletion",
    "ogallala aquifer depletion facility": "ogallala_aquifer_depletion",
    "ogallala aquifer depletion plant": "ogallala_aquifer_depletion",
    "ogallala aquifer depletion program": "ogallala_aquifer_depletion",
    "ogallala aquifer depletion initiative": "ogallala_aquifer_depletion",

    # Prior Appropriation variants
    "prior appropriation application": "prior_appropriation_doctrine",
    "prior appropriation project": "prior_appropriation_doctrine",
    "prior appropriation facility": "prior_appropriation_doctrine",
    "prior appropriation plant": "prior_appropriation_doctrine",
    "prior appropriation program": "prior_appropriation_doctrine",
    "prior appropriation initiative": "prior_appropriation_doctrine",

    # Rule of Capture variants
    "rule of capture application": "rule_of_capture",
    "rule of capture project": "rule_of_capture",
    "rule of capture facility": "rule_of_capture",
    "rule of capture plant": "rule_of_capture",
    "rule of capture program": "rule_of_capture",
    "rule of capture initiative": "rule_of_capture",

    # General water variants
    "water application": "texas_water_code",
    "water project": "texas_water_code",
    "water facility": "texas_water_code",
    "water plant": "texas_water_code",
    "water program": "texas_water_code",
    "water initiative": "texas_water_code",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash():
    items = sorted(SEMANTIC_MAP.items())
    map_bytes = "".join(f"{k}:{v};" for k, v in items).encode("utf-8")
    return hashlib.sha256(map_bytes).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    hash_val = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (hash_val == _MAP_INTEGRITY_HASH)
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": actual_count,
        "hash": hash_val,
        "is_valid": is_valid
    }

def _normalize_string(s):
    s = s.lower()
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

def normalize_term(term: str) -> str:
    norm = _normalize_string(term)
    return SEMANTIC_MAP.get(norm, norm)

def get_related_terms(term: str) -> list:
    norm = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == norm]
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)