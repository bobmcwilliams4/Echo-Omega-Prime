import hashlib
import re

SEMANTIC_MAP_VERSION = "2024.06.01"
SEMANTIC_MAP_AUTHOR = "E01_engine_team"
SEMANTIC_MAP_ENGINE = "E01_document_classifier"

SEMANTIC_MAP = {
    # General Warranty Deed
    "general warranty deed": "general_warranty_deed",
    "warranty deed": "general_warranty_deed",
    "gwd": "general_warranty_deed",
    "warranty": "general_warranty_deed",
    "full warranty deed": "general_warranty_deed",
    "warrenty deed": "general_warranty_deed",
    "warrenty": "general_warranty_deed",
    "warrantydeed": "general_warranty_deed",
    "warr deed": "general_warranty_deed",
    "warr. deed": "general_warranty_deed",
    "warrnty deed": "general_warranty_deed",
    "warrentydeed": "general_warranty_deed",
    "warrenty d": "general_warranty_deed",
    "warr deed": "general_warranty_deed",
    "warr. d.": "general_warranty_deed",
    "warr deed doc": "general_warranty_deed",
    "warranty deed document": "general_warranty_deed",
    "warranty deed form": "general_warranty_deed",
    "warranty deed record": "general_warranty_deed",
    "warranty deed file": "general_warranty_deed",
    "warranty deed instrument": "general_warranty_deed",
    "warranty deed agreement": "general_warranty_deed",

    # Special Warranty Deed
    "special warranty deed": "special_warranty_deed",
    "swd": "special_warranty_deed",
    "special warranty": "special_warranty_deed",
    "sp warranty deed": "special_warranty_deed",
    "sp. warranty deed": "special_warranty_deed",
    "special warrenty deed": "special_warranty_deed",
    "special warrenty": "special_warranty_deed",
    "special warrantydeed": "special_warranty_deed",
    "special warr deed": "special_warranty_deed",
    "special warr. deed": "special_warranty_deed",
    "special warrnty deed": "special_warranty_deed",
    "special warrentydeed": "special_warranty_deed",
    "special warrenty d": "special_warranty_deed",
    "special warr deed": "special_warranty_deed",
    "special warr. d.": "special_warranty_deed",
    "special warranty deed document": "special_warranty_deed",
    "special warranty deed form": "special_warranty_deed",
    "special warranty deed record": "special_warranty_deed",
    "special warranty deed file": "special_warranty_deed",
    "special warranty deed instrument": "special_warranty_deed",
    "special warranty deed agreement": "special_warranty_deed",

    # Quitclaim Deed
    "quitclaim deed": "quitclaim_deed",
    "quit claim deed": "quitclaim_deed",
    "qcd": "quitclaim_deed",
    "quitclaim": "quitclaim_deed",
    "quit claim": "quitclaim_deed",
    "quitclaimdeed": "quitclaim_deed",
    "quit claimdeed": "quitclaim_deed",
    "quit claim d": "quitclaim_deed",
    "quitclaim d": "quitclaim_deed",
    "quit claim doc": "quitclaim_deed",
    "quitclaim doc": "quitclaim_deed",
    "quitclaim deed document": "quitclaim_deed",
    "quitclaim deed form": "quitclaim_deed",
    "quitclaim deed record": "quitclaim_deed",
    "quitclaim deed file": "quitclaim_deed",
    "quitclaim deed instrument": "quitclaim_deed",
    "quitclaim deed agreement": "quitclaim_deed",
    "quick claim deed": "quitclaim_deed",
    "quickclaim deed": "quitclaim_deed",
    "quick claim": "quitclaim_deed",

    # Oil and Gas Lease
    "oil and gas lease": "oil_and_gas_lease",
    "o&g lease": "oil_and_gas_lease",
    "og lease": "oil_and_gas_lease",
    "oil gas lease": "oil_and_gas_lease",
    "oil & gas lease": "oil_and_gas_lease",
    "oil gas leasing": "oil_and_gas_lease",
    "oil and gas leasing": "oil_and_gas_lease",
    "oil and gas lease agreement": "oil_and_gas_lease",
    "oil and gas lease document": "oil_and_gas_lease",
    "oil and gas lease form": "oil_and_gas_lease",
    "oil and gas lease record": "oil_and_gas_lease",
    "oil and gas lease file": "oil_and_gas_lease",
    "oil and gas lease instrument": "oil_and_gas_lease",
    "oil and gas lease contract": "oil_and_gas_lease",
    "oil and gas lease instrument": "oil_and_gas_lease",
    "oil gas lease agreement": "oil_and_gas_lease",
    "oil gas lease document": "oil_and_gas_lease",
    "oil gas lease form": "oil_and_gas_lease",
    "oil gas lease record": "oil_and_gas_lease",
    "oil gas lease file": "oil_and_gas_lease",
    "oil gas lease instrument": "oil_and_gas_lease",

    # Mineral Deed
    "mineral deed": "mineral_deed",
    "min deed": "mineral_deed",
    "mineraldeed": "mineral_deed",
    "mineral deed document": "mineral_deed",
    "mineral deed form": "mineral_deed",
    "mineral deed record": "mineral_deed",
    "mineral deed file": "mineral_deed",
    "mineral deed instrument": "mineral_deed",
    "mineral deed agreement": "mineral_deed",
    "mineral conveyance": "mineral_deed",
    "mineral transfer": "mineral_deed",
    "mineral assignment": "mineral_deed",

    # Royalty Deed
    "royalty deed": "royalty_deed",
    "roy deed": "royalty_deed",
    "royaltydeed": "royalty_deed",
    "royalty deed document": "royalty_deed",
    "royalty deed form": "royalty_deed",
    "royalty deed record": "royalty_deed",
    "royalty deed file": "royalty_deed",
    "royalty deed instrument": "royalty_deed",
    "royalty deed agreement": "royalty_deed",
    "royalty conveyance": "royalty_deed",
    "royalty transfer": "royalty_deed",
    "royalty assignment": "royalty_deed",

    # Deed of Trust
    "deed of trust": "deed_of_trust",
    "dot": "deed_of_trust",
    "deed trust": "deed_of_trust",
    "trust deed": "deed_of_trust",
    "deedoftrust": "deed_of_trust",
    "deed of trust document": "deed_of_trust",
    "deed of trust form": "deed_of_trust",
    "deed of trust record": "deed_of_trust",
    "deed of trust file": "deed_of_trust",
    "deed of trust instrument": "deed_of_trust",
    "deed of trust agreement": "deed_of_trust",
    "mortgage deed": "deed_of_trust",
    "mortgage": "deed_of_trust",

    # Release of Lien
    "release of lien": "release_of_lien",
    "rol": "release_of_lien",
    "lien release": "release_of_lien",
    "release lien": "release_of_lien",
    "releaseoflien": "release_of_lien",
    "release of lien document": "release_of_lien",
    "release of lien form": "release_of_lien",
    "release of lien record": "release_of_lien",
    "release of lien file": "release_of_lien",
    "release of lien instrument": "release_of_lien",
    "release of lien agreement": "release_of_lien",
    "lien discharge": "release_of_lien",
    "lien satisfaction": "release_of_lien",

    # Affidavit of Heirship
    "affidavit of heirship": "affidavit_of_heirship",
    "aoh": "affidavit_of_heirship",
    "heirship affidavit": "affidavit_of_heirship",
    "affidavit heirship": "affidavit_of_heirship",
    "affidavitofheirship": "affidavit_of_heirship",
    "affidavit of heirship document": "affidavit_of_heirship",
    "affidavit of heirship form": "affidavit_of_heirship",
    "affidavit of heirship record": "affidavit_of_heirship",
    "affidavit of heirship file": "affidavit_of_heirship",
    "affidavit of heirship instrument": "affidavit_of_heirship",
    "affidavit of heirship agreement": "affidavit_of_heirship",
    "heirship declaration": "affidavit_of_heirship",

    # Probate Court Order
    "probate court order": "probate_court_order",
    "probate order": "probate_court_order",
    "court order probate": "probate_court_order",
    "probatecourtorder": "probate_court_order",
    "probate court order document": "probate_court_order",
    "probate court order form": "probate_court_order",
    "probate court order record": "probate_court_order",
    "probate court order file": "probate_court_order",
    "probate court order instrument": "probate_court_order",
    "probate court order agreement": "probate_court_order",
    "probate decree": "probate_court_order",
    "probate judgment": "probate_court_order",

    # Divorce Decree Property Division
    "divorce decree property division": "divorce_decree_property_division",
    "divorce decree": "divorce_decree_property_division",
    "property division decree": "divorce_decree_property_division",
    "divorce property division": "divorce_decree_property_division",
    "divorce decree property": "divorce_decree_property_division",
    "divorce decree property division document": "divorce_decree_property_division",
    "divorce decree property division form": "divorce_decree_property_division",
    "divorce decree property division record": "divorce_decree_property_division",
    "divorce decree property division file": "divorce_decree_property_division",
    "divorce decree property division instrument": "divorce_decree_property_division",
    "divorce decree property division agreement": "divorce_decree_property_division",
    "divorce judgment": "divorce_decree_property_division",
    "divorce court order": "divorce_decree_property_division",

    # Assignment of Overriding Royalty Interest
    "assignment of overriding royalty interest": "assignment_of_overriding_royalty_interest",
    "aori": "assignment_of_overriding_royalty_interest",
    "overriding royalty assignment": "assignment_of_overriding_royalty_interest",
    "assignment overriding royalty": "assignment_of_overriding_royalty_interest",
    "assignment of overriding royalty": "assignment_of_overriding_royalty_interest",
    "assignment of overriding royalty interest document": "assignment_of_overriding_royalty_interest",
    "assignment of overriding royalty interest form": "assignment_of_overriding_royalty_interest",
    "assignment of overriding royalty interest record": "assignment_of_overriding_royalty_interest",
    "assignment of overriding royalty interest file": "assignment_of_overriding_royalty_interest",
    "assignment of overriding royalty interest instrument": "assignment_of_overriding_royalty_interest",
    "assignment of overriding royalty interest agreement": "assignment_of_overriding_royalty_interest",
    "overriding royalty conveyance": "assignment_of_overriding_royalty_interest",

    # Assignment of Working Interest
    "assignment of working interest": "assignment_of_working_interest",
    "awi": "assignment_of_working_interest",
    "working interest assignment": "assignment_of_working_interest",
    "assignment working interest": "assignment_of_working_interest",
    "assignment of working interest document": "assignment_of_working_interest",
    "assignment of working interest form": "assignment_of_working_interest",
    "assignment of working interest record": "assignment_of_working_interest",
    "assignment of working interest file": "assignment_of_working_interest",
    "assignment of working interest instrument": "assignment_of_working_interest",
    "assignment of working interest agreement": "assignment_of_working_interest",
    "working interest conveyance": "assignment_of_working_interest",

    # Pipeline Right of Way
    "pipeline right of way": "pipeline_right_of_way",
    "prow": "pipeline_right_of_way",
    "pipeline row": "pipeline_right_of_way",
    "pipeline right-of-way": "pipeline_right_of_way",
    "pipeline right of way agreement": "pipeline_right_of_way",
    "pipeline right of way document": "pipeline_right_of_way",
    "pipeline right of way form": "pipeline_right_of_way",
    "pipeline right of way record": "pipeline_right_of_way",
    "pipeline right of way file": "pipeline_right_of_way",
    "pipeline right of way instrument": "pipeline_right_of_way",
    "pipeline right of way contract": "pipeline_right_of_way",
    "pipeline easement": "pipeline_right_of_way",

    # Division Order
    "division order": "division_order",
    "do": "division_order",
    "divisionorder": "division_order",
    "division order agreement": "division_order",
    "division order document": "division_order",
    "division order form": "division_order",
    "division order record": "division_order",
    "division order file": "division_order",
    "division order instrument": "division_order",
    "division order contract": "division_order",
    "division of interest order": "division_order",

    # Pooling Agreement
    "pooling agreement": "pooling_agreement",
    "pooling": "pooling_agreement",
    "pool agreement": "pooling_agreement",
    "poolingagreement": "pooling_agreement",
    "pooling agreement document": "pooling_agreement",
    "pooling agreement form": "pooling_agreement",
    "pooling agreement record": "pooling_agreement",
    "pooling agreement file": "pooling_agreement",
    "pooling agreement instrument": "pooling_agreement",
    "pooling agreement contract": "pooling_agreement",
    "pooling contract": "pooling_agreement",

    # Unitization Agreement
    "unitization agreement": "unitization_agreement",
    "unit agreement": "unitization_agreement",
    "unitization": "unitization_agreement",
    "unitizationagreement": "unitization_agreement",
    "unitization agreement document": "unitization_agreement",
    "unitization agreement form": "unitization_agreement",
    "unitization agreement record": "unitization_agreement",
    "unitization agreement file": "unitization_agreement",
    "unitization agreement instrument": "unitization_agreement",
    "unitization agreement contract": "unitization_agreement",
    "unit contract": "unitization_agreement",

    # Power of Attorney
    "power of attorney": "power_of_attorney",
    "poa": "power_of_attorney",
    "power attorney": "power_of_attorney",
    "powerofattorney": "power_of_attorney",
    "power of attorney document": "power_of_attorney",
    "power of attorney form": "power_of_attorney",
    "power of attorney record": "power_of_attorney",
    "power of attorney file": "power_of_attorney",
    "power of attorney instrument": "power_of_attorney",
    "power of attorney agreement": "power_of_attorney",
    "attorney in fact": "power_of_attorney",

    # Correction Deed
    "correction deed": "correction_deed",
    "corr deed": "correction_deed",
    "correctiondeed": "correction_deed",
    "corrective deed": "correction_deed",
    "corrected deed": "correction_deed",
    "correction deed document": "correction_deed",
    "correction deed form": "correction_deed",
    "correction deed record": "correction_deed",
    "correction deed file": "correction_deed",
    "correction deed instrument": "correction_deed",
    "correction deed agreement": "correction_deed",

    # Gift Deed
    "gift deed": "gift_deed",
    "giftdeed": "gift_deed",
    "gift deed document": "gift_deed",
    "gift deed form": "gift_deed",
    "gift deed record": "gift_deed",
    "gift deed file": "gift_deed",
    "gift deed instrument": "gift_deed",
    "gift deed agreement": "gift_deed",
    "deed of gift": "gift_deed",

    # Surface Lease
    "surface lease": "surface_lease",
    "surfacelease": "surface_lease",
    "surface lease document": "surface_lease",
    "surface lease form": "surface_lease",
    "surface lease record": "surface_lease",
    "surface lease file": "surface_lease",
    "surface lease instrument": "surface_lease",
    "surface lease agreement": "surface_lease",
    "surface lease contract": "surface_lease",

    # Affidavit of Identity
    "affidavit of identity": "affidavit_of_identity",
    "affidavit identity": "affidavit_of_identity",
    "affidavitofidentity": "affidavit_of_identity",
    "affidavit of identity document": "affidavit_of_identity",
    "affidavit of identity form": "affidavit_of_identity",
    "affidavit of identity record": "affidavit_of_identity",
    "affidavit of identity file": "affidavit_of_identity",
    "affidavit of identity instrument": "affidavit_of_identity",
    "affidavit of identity agreement": "affidavit_of_identity",
    "identity affidavit": "affidavit_of_identity",

    # Affidavit of Non-Production
    "affidavit of non-production": "affidavit_of_non_production",
    "affidavit non production": "affidavit_of_non_production",
    "affidavitofnonproduction": "affidavit_of_non_production",
    "affidavit of non-production document": "affidavit_of_non_production",
    "affidavit of non-production form": "affidavit_of_non_production",
    "affidavit of non-production record": "affidavit_of_non_production",
    "affidavit of non-production file": "affidavit_of_non_production",
    "affidavit of non-production instrument": "affidavit_of_non_production",
    "affidavit of non-production agreement": "affidavit_of_non_production",
    "non-production affidavit": "affidavit_of_non_production",

    # Ratification of Lease
    "ratification of lease": "ratification_of_lease",
    "lease ratification": "ratification_of_lease",
    "ratification lease": "ratification_of_lease",
    "ratificationoflease": "ratification_of_lease",
    "ratification of lease document": "ratification_of_lease",
    "ratification of lease form": "ratification_of_lease",
    "ratification of lease record": "ratification_of_lease",
    "ratification of lease file": "ratification_of_lease",
    "ratification of lease instrument": "ratification_of_lease",
    "ratification of lease agreement": "ratification_of_lease",

    # Subordination Agreement
    "subordination agreement": "subordination_agreement",
    "subordination": "subordination_agreement",
    "subordinationagreement": "subordination_agreement",
    "subordination agreement document": "subordination_agreement",
    "subordination agreement form": "subordination_agreement",
    "subordination agreement record": "subordination_agreement",
    "subordination agreement file": "subordination_agreement",
    "subordination agreement instrument": "subordination_agreement",
    "subordination agreement contract": "subordination_agreement",

    # UCC Financing Statement
    "ucc financing statement": "ucc_financing_statement",
    "ucc statement": "ucc_financing_statement",
    "ucc": "ucc_financing_statement",
    "ucc financing": "ucc_financing_statement",
    "uccfinancingstatement": "ucc_financing_statement",
    "ucc financing statement document": "ucc_financing_statement",
    "ucc financing statement form": "ucc_financing_statement",
    "ucc financing statement record": "ucc_financing_statement",
    "ucc financing statement file": "ucc_financing_statement",
    "ucc financing statement instrument": "ucc_financing_statement",
    "ucc financing statement agreement": "ucc_financing_statement",
    "financing statement": "ucc_financing_statement",

    # Partition Order
    "partition order": "partition_order",
    "partitionorder": "partition_order",
    "partition order document": "partition_order",
    "partition order form": "partition_order",
    "partition order record": "partition_order",
    "partition order file": "partition_order",
    "partition order instrument": "partition_order",
    "partition order agreement": "partition_order",
    "partition decree": "partition_order",
    "partition judgment": "partition_order",

    # Wind/Solar Energy Lease
    "wind/solar energy lease": "wind_solar_energy_lease",
    "wind solar lease": "wind_solar_energy_lease",
    "wind lease": "wind_solar_energy_lease",
    "solar lease": "wind_solar_energy_lease",
    "wind/solar lease": "wind_solar_energy_lease",
    "wind energy lease": "wind_solar_energy_lease",
    "solar energy lease": "wind_solar_energy_lease",
    "wind/solar energy lease document": "wind_solar_energy_lease",
    "wind/solar energy lease form": "wind_solar_energy_lease",
    "wind/solar energy lease record": "wind_solar_energy_lease",
    "wind/solar energy lease file": "wind_solar_energy_lease",
    "wind/solar energy lease instrument": "wind_solar_energy_lease",
    "wind/solar energy lease agreement": "wind_solar_energy_lease",

    # Receivership Order
    "receivership order": "receivership_order",
    "receivershiporder": "receivership_order",
    "receivership order document": "receivership_order",
    "receivership order form": "receivership_order",
    "receivership order record": "receivership_order",
    "receivership order file": "receivership_order",
    "receivership order instrument": "receivership_order",
    "receivership order agreement": "receivership_order",
    "receivership decree": "receivership_order",
    "receivership judgment": "receivership_order",

    # Stipulation of Interest
    "stipulation of interest": "stipulation_of_interest",
    "stipulationinterest": "stipulation_of_interest",
    "stipulation interest": "stipulation_of_interest",
    "stipulation of interest document": "stipulation_of_interest",
    "stipulation of interest form": "stipulation_of_interest",
    "stipulation of interest record": "stipulation_of_interest",
    "stipulation of interest file": "stipulation_of_interest",
    "stipulation of interest instrument": "stipulation_of_interest",
    "stipulation of interest agreement": "stipulation_of_interest",
    "stipulation agreement": "stipulation_of_interest",

    # Additional synonyms, misspellings, abbreviations, related terms (sampled for coverage)
    "warrenty": "general_warranty_deed",
    "warrenty deed": "general_warranty_deed",
    "special warrenty": "special_warranty_deed",
    "special warrenty deed": "special_warranty_deed",
    "quit claim": "quitclaim_deed",
    "quick claim": "quitclaim_deed",
    "quickclaim": "quitclaim_deed",
    "oil gas lease": "oil_and_gas_lease",
    "mineral conveyance": "mineral_deed",
    "royalty conveyance": "royalty_deed",
    "mortgage": "deed_of_trust",
    "lien satisfaction": "release_of_lien",
    "heirship declaration": "affidavit_of_heirship",
    "probate decree": "probate_court_order",
    "divorce judgment": "divorce_decree_property_division",
    "overriding royalty conveyance": "assignment_of_overriding_royalty_interest",
    "working interest conveyance": "assignment_of_working_interest",
    "pipeline easement": "pipeline_right_of_way",
    "division of interest order": "division_order",
    "pooling contract": "pooling_agreement",
    "unit contract": "unitization_agreement",
    "attorney in fact": "power_of_attorney",
    "corrective deed": "correction_deed",
    "deed of gift": "gift_deed",
    "identity affidavit": "affidavit_of_identity",
    "non-production affidavit": "affidavit_of_non_production",
    "partition decree": "partition_order",
    "partition judgment": "partition_order",
    "wind energy lease": "wind_solar_energy_lease",
    "solar energy lease": "wind_solar_energy_lease",
    "receivership decree": "receivership_order",
    "receivership judgment": "receivership_order",
    "stipulation agreement": "stipulation_of_interest",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash():
    items = sorted(SEMANTIC_MAP.items())
    concat = "".join(f"{k}:{v};" for k, v in items)
    concat += SEMANTIC_MAP_VERSION + SEMANTIC_MAP_ENGINE + SEMANTIC_MAP_AUTHOR
    return hashlib.sha256(concat.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity():
    actual_count = len(SEMANTIC_MAP)
    actual_hash = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (actual_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "ok" if is_valid else "error",
        "entries": actual_count,
        "hash": actual_hash,
        "is_valid": is_valid,
        "expected_count": _EXPECTED_ENTRY_COUNT,
        "expected_hash": _MAP_INTEGRITY_HASH,
        "version": SEMANTIC_MAP_VERSION,
        "author": SEMANTIC_MAP_AUTHOR,
        "engine": SEMANTIC_MAP_ENGINE,
    }

def normalize_term(term: str) -> str:
    if not isinstance(term, str):
        return ""
    norm = term.strip().lower()
    norm = re.sub(r"[\s\-_/]+", " ", norm)
    norm = norm.replace(".", "")
    norm = norm.replace(",", "")
    norm = norm.replace("agreement", "")
    norm = norm.replace("document", "")
    norm = norm.replace("form", "")
    norm = norm.replace("record", "")
    norm = norm.replace("file", "")
    norm = norm.replace("instrument", "")
    norm = norm.replace("contract", "")
    norm = norm.replace("decree", "")
    norm = norm.replace("judgment", "")
    norm = norm.replace("conveyance", "")
    norm = norm.replace("assignment", "")
    norm = norm.replace("transfer", "")
    norm = norm.replace("satisfaction", "")
    norm = norm.replace("discharge", "")
    norm = norm.replace("deed", " deed")
    norm = norm.replace("lease", " lease")
    norm = norm.replace("order", " order")
    norm = norm.replace("affidavit", " affidavit")
    norm = norm.replace("ratification", " ratification")
    norm = norm.replace("partition", " partition")
    norm = norm.replace("stipulation", " stipulation")
    norm = norm.replace("release", " release")
    norm = norm.replace("power", " power")
    norm = norm.replace("correction", " correction")
    norm = norm.replace("gift", " gift")
    norm = norm.replace("surface", " surface")
    norm = norm.replace("identity", " identity")
    norm = norm.replace("non production", " non production")
    norm = norm.replace("heirship", " heirship")
    norm = norm.replace("probate", " probate")
    norm = norm.replace("divorce", " divorce")
    norm = norm.replace("overriding royalty", " overriding royalty")
    norm = norm.replace("working interest", " working interest")
    norm = norm.replace("pipeline", " pipeline")
    norm = norm.replace("division", " division")
    norm = norm.replace("pooling", " pooling")
    norm = norm.replace("unitization", " unitization")
    norm = norm.replace("attorney", " attorney")
    norm = norm.replace("corrective", " correction")
    norm = norm.replace("gift", " gift")
    norm = norm.replace("surface", " surface")
    norm = norm.replace("identity", " identity")
    norm = norm.replace("non production", " non production")
    norm = norm.replace("ratification", " ratification")
    norm = norm.replace("subordination", " subordination")
    norm = norm.replace("ucc", " ucc")
    norm = norm.replace("partition", " partition")
    norm = norm.replace("wind", " wind")
    norm = norm.replace("solar", " solar")
    norm = norm.replace("receivership", " receivership")
    norm = norm.replace("stipulation", " stipulation")
    norm = re.sub(r"\s+", " ", norm)
    norm = norm.strip()
    return SEMANTIC_MAP.get(norm, norm.replace(" ", "_"))

def get_related_terms(term: str) -> list:
    normalized = normalize_term(term)
    related = []
    for k, v in SEMANTIC_MAP.items():
        if v == normalized and k != term:
            related.append(k)
    return related

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)