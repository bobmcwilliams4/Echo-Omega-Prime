"""
LG13 Environmental Law Engine - Semantic Normalization Module
==============================================================
Deterministic semantic normalization for environmental law queries.

Maps natural language environmental terms to canonical legal identifiers.
Handles statute abbreviations, regulatory program names, contaminant names,
permit types, agency names, and environmental domain terminology.

Rules:
    - Purely deterministic (no ML, no vectors, no embeddings)
    - Case-insensitive matching
    - Longest-match-first for multi-word terms
    - Returns NormalizationResult with full provenance
    - No side effects, no state mutation

Port: 8403
Engine: LG13 Environmental Law
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import re
import time
from dataclasses import dataclass, field as dc_field
from enum import Enum
from typing import Any, ClassVar, Dict, FrozenSet, List, Optional, Set, Tuple

from loguru import logger


# ============================================================================
# NORMALIZATION RESULT
# ============================================================================

@dataclass
class NormalizationResult:
    """Result of semantic normalization on a query."""
    original_query: str
    normalized_query: str
    mappings_applied: List[Dict[str, str]] = dc_field(default_factory=list)
    statutes_detected: List[str] = dc_field(default_factory=list)
    agencies_detected: List[str] = dc_field(default_factory=list)
    contaminants_detected: List[str] = dc_field(default_factory=list)
    permit_types_detected: List[str] = dc_field(default_factory=list)
    environmental_domains: List[str] = dc_field(default_factory=list)
    jurisdiction_detected: str = ""
    confidence_boost: float = 0.0
    normalization_hash: str = ""
    duration_ms: float = 0.0

    def __post_init__(self) -> None:
        if not self.normalization_hash:
            content = f"{self.original_query}|{self.normalized_query}|{len(self.mappings_applied)}"
            self.normalization_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


# ============================================================================
# STATUTE NORMALIZATION MAP
# ============================================================================

STATUTE_SYNONYMS: Dict[str, str] = {
    # NEPA
    "national environmental policy act": "NEPA",
    "nepa": "NEPA",
    "environmental impact statement": "NEPA_EIS",
    "eis": "NEPA_EIS",
    "environmental assessment": "NEPA_EA",
    "ea": "NEPA_EA",
    "finding of no significant impact": "NEPA_FONSI",
    "fonsi": "NEPA_FONSI",
    "categorical exclusion": "NEPA_CATEX",
    "catex": "NEPA_CATEX",
    "ceq regulations": "NEPA_CEQ",
    "council on environmental quality": "NEPA_CEQ",
    "40 cfr 1500": "NEPA_CEQ",
    "42 usc 4321": "NEPA",
    "record of decision": "NEPA_ROD",
    "programmatic eis": "NEPA_PEIS",
    "supplemental eis": "NEPA_SEIS",
    "tiering": "NEPA_TIERING",
    # Clean Air Act
    "clean air act": "CAA",
    "caa": "CAA",
    "42 usc 7401": "CAA",
    "naaqs": "CAA_NAAQS",
    "national ambient air quality standards": "CAA_NAAQS",
    "sip": "CAA_SIP",
    "state implementation plan": "CAA_SIP",
    "nsps": "CAA_NSPS",
    "new source performance standards": "CAA_NSPS",
    "neshap": "CAA_NESHAP",
    "national emission standards for hazardous air pollutants": "CAA_NESHAP",
    "mact": "CAA_MACT",
    "maximum achievable control technology": "CAA_MACT",
    "title v permit": "CAA_TITLE_V",
    "title v": "CAA_TITLE_V",
    "operating permit": "CAA_TITLE_V",
    "new source review": "CAA_NSR",
    "nsr": "CAA_NSR",
    "prevention of significant deterioration": "CAA_PSD",
    "psd": "CAA_PSD",
    "nonattainment area": "CAA_NONATTAINMENT",
    "attainment area": "CAA_ATTAINMENT",
    "criteria pollutant": "CAA_CRITERIA",
    "hap": "CAA_HAP",
    "hazardous air pollutant": "CAA_HAP",
    "bact": "CAA_BACT",
    "best available control technology": "CAA_BACT",
    "laer": "CAA_LAER",
    "lowest achievable emission rate": "CAA_LAER",
    "acid rain program": "CAA_ACID_RAIN",
    "title iv": "CAA_ACID_RAIN",
    "ozone depleting substance": "CAA_ODS",
    "greenhouse gas": "CAA_GHG",
    "ghg": "CAA_GHG",
    "tailoring rule": "CAA_TAILORING",
    # Clean Water Act
    "clean water act": "CWA",
    "cwa": "CWA",
    "33 usc 1251": "CWA",
    "federal water pollution control act": "CWA",
    "fwpca": "CWA",
    "npdes": "CWA_NPDES",
    "national pollutant discharge elimination system": "CWA_NPDES",
    "npdes permit": "CWA_NPDES",
    "discharge permit": "CWA_NPDES",
    "point source": "CWA_POINT_SOURCE",
    "section 404": "CWA_404",
    "cwa 404": "CWA_404",
    "dredge and fill": "CWA_404",
    "wetlands permit": "CWA_404",
    "section 401": "CWA_401",
    "cwa 401": "CWA_401",
    "water quality certification": "CWA_401",
    "tmdl": "CWA_TMDL",
    "total maximum daily load": "CWA_TMDL",
    "effluent limitation": "CWA_EFFLUENT",
    "water quality standards": "CWA_WQS",
    "stormwater": "CWA_STORMWATER",
    "ms4": "CWA_MS4",
    "swppp": "CWA_SWPPP",
    "stormwater pollution prevention plan": "CWA_SWPPP",
    "pretreatment": "CWA_PRETREATMENT",
    "potw": "CWA_POTW",
    "publicly owned treatment works": "CWA_POTW",
    "spill prevention": "CWA_SPCC",
    "spcc": "CWA_SPCC",
    "waters of the united states": "CWA_WOTUS",
    "wotus": "CWA_WOTUS",
    "navigable waters": "CWA_WOTUS",
    "wetlands": "CWA_WETLANDS",
    "nonpoint source": "CWA_NPS",
    "section 319": "CWA_319",
    # RCRA
    "resource conservation and recovery act": "RCRA",
    "rcra": "RCRA",
    "42 usc 6901": "RCRA",
    "subtitle c": "RCRA_SUBTITLE_C",
    "hazardous waste": "RCRA_SUBTITLE_C",
    "subtitle d": "RCRA_SUBTITLE_D",
    "solid waste": "RCRA_SUBTITLE_D",
    "subtitle i": "RCRA_SUBTITLE_I",
    "underground storage tank": "RCRA_UST",
    "ust": "RCRA_UST",
    "tsdf": "RCRA_TSDF",
    "treatment storage disposal facility": "RCRA_TSDF",
    "hazardous waste generator": "RCRA_GENERATOR",
    "large quantity generator": "RCRA_LQG",
    "lqg": "RCRA_LQG",
    "small quantity generator": "RCRA_SQG",
    "sqg": "RCRA_SQG",
    "conditionally exempt": "RCRA_CESQG",
    "vsqg": "RCRA_VSQG",
    "very small quantity generator": "RCRA_VSQG",
    "rcra corrective action": "RCRA_CORRECTIVE",
    "land disposal restriction": "RCRA_LDR",
    "ldr": "RCRA_LDR",
    "manifest system": "RCRA_MANIFEST",
    "hazardous waste manifest": "RCRA_MANIFEST",
    "characteristic waste": "RCRA_CHARACTERISTIC",
    "listed waste": "RCRA_LISTED",
    "derived from rule": "RCRA_DERIVED_FROM",
    "mixture rule": "RCRA_MIXTURE",
    "boiler and industrial furnace": "RCRA_BIF",
    "used oil": "RCRA_USED_OIL",
    "universal waste": "RCRA_UNIVERSAL",
    # CERCLA / Superfund
    "comprehensive environmental response compensation and liability act": "CERCLA",
    "cercla": "CERCLA",
    "superfund": "CERCLA",
    "42 usc 9601": "CERCLA",
    "potentially responsible party": "CERCLA_PRP",
    "prp": "CERCLA_PRP",
    "national contingency plan": "CERCLA_NCP",
    "ncp": "CERCLA_NCP",
    "national priorities list": "CERCLA_NPL",
    "npl": "CERCLA_NPL",
    "cerclis": "CERCLA_CERCLIS",
    "sara": "CERCLA_SARA",
    "superfund amendments and reauthorization act": "CERCLA_SARA",
    "remedial investigation": "CERCLA_RI",
    "feasibility study": "CERCLA_FS",
    "ri/fs": "CERCLA_RIFS",
    "record of decision": "CERCLA_ROD",
    "superfund rod": "CERCLA_ROD",
    "remedial design": "CERCLA_RD",
    "remedial action": "CERCLA_RA",
    "removal action": "CERCLA_REMOVAL",
    "applicable or relevant and appropriate requirements": "CERCLA_ARAR",
    "arar": "CERCLA_ARAR",
    "cost recovery": "CERCLA_COST_RECOVERY",
    "107 action": "CERCLA_107",
    "contribution action": "CERCLA_CONTRIBUTION",
    "113 action": "CERCLA_113",
    "innocent purchaser": "CERCLA_INNOCENT_PURCHASER",
    "innocent landowner": "CERCLA_INNOCENT_PURCHASER",
    "bona fide prospective purchaser": "CERCLA_BFPP",
    "bfpp": "CERCLA_BFPP",
    "contiguous property owner": "CERCLA_CPO",
    "brownfield": "CERCLA_BROWNFIELD",
    "all appropriate inquiries": "CERCLA_AAI",
    "aai": "CERCLA_AAI",
    "hazard ranking system": "CERCLA_HRS",
    "hrs": "CERCLA_HRS",
    "preliminary assessment": "CERCLA_PA",
    "site inspection": "CERCLA_SI",
    "five year review": "CERCLA_5YR",
    "lien": "CERCLA_LIEN",
    "superfund lien": "CERCLA_LIEN",
    # TSCA
    "toxic substances control act": "TSCA",
    "tsca": "TSCA",
    "15 usc 2601": "TSCA",
    "lautenberg act": "TSCA_LAUTENBERG",
    "frank r lautenberg chemical safety": "TSCA_LAUTENBERG",
    "pcb": "TSCA_PCB",
    "polychlorinated biphenyl": "TSCA_PCB",
    "asbestos": "TSCA_ASBESTOS",
    "lead paint": "TSCA_LEAD",
    "lead based paint": "TSCA_LEAD",
    "lead rrp": "TSCA_LEAD_RRP",
    "renovation repair painting": "TSCA_LEAD_RRP",
    "chemical data reporting": "TSCA_CDR",
    "cdr": "TSCA_CDR",
    "tsca inventory": "TSCA_INVENTORY",
    "premanufacture notice": "TSCA_PMN",
    "pmn": "TSCA_PMN",
    "significant new use rule": "TSCA_SNUR",
    "snur": "TSCA_SNUR",
    "risk evaluation": "TSCA_RISK_EVAL",
    "pfas": "TSCA_PFAS",
    "per and polyfluoroalkyl": "TSCA_PFAS",
    "forever chemicals": "TSCA_PFAS",
    # ESA
    "endangered species act": "ESA",
    "esa": "ESA",
    "16 usc 1531": "ESA",
    "section 7 consultation": "ESA_SECTION_7",
    "esa section 7": "ESA_SECTION_7",
    "biological opinion": "ESA_BIOP",
    "biop": "ESA_BIOP",
    "jeopardy finding": "ESA_JEOPARDY",
    "incidental take": "ESA_INCIDENTAL_TAKE",
    "incidental take statement": "ESA_ITS",
    "incidental take permit": "ESA_ITP",
    "section 9 take prohibition": "ESA_SECTION_9",
    "esa section 9": "ESA_SECTION_9",
    "section 10 permit": "ESA_SECTION_10",
    "esa section 10": "ESA_SECTION_10",
    "habitat conservation plan": "ESA_HCP",
    "hcp": "ESA_HCP",
    "critical habitat": "ESA_CRITICAL_HABITAT",
    "candidate species": "ESA_CANDIDATE",
    "threatened species": "ESA_THREATENED",
    "endangered species": "ESA_ENDANGERED",
    "recovery plan": "ESA_RECOVERY",
    "listing decision": "ESA_LISTING",
    "delisting": "ESA_DELISTING",
    # FIFRA
    "federal insecticide fungicide and rodenticide act": "FIFRA",
    "fifra": "FIFRA",
    "7 usc 136": "FIFRA",
    "pesticide registration": "FIFRA_REGISTRATION",
    "pesticide tolerance": "FIFRA_TOLERANCE",
    "restricted use pesticide": "FIFRA_RUP",
    "general use pesticide": "FIFRA_GUP",
    "fifra label": "FIFRA_LABEL",
    "pesticide label": "FIFRA_LABEL",
    "fqpa": "FIFRA_FQPA",
    "food quality protection act": "FIFRA_FQPA",
    "special review": "FIFRA_SPECIAL_REVIEW",
    # SDWA
    "safe drinking water act": "SDWA",
    "sdwa": "SDWA",
    "42 usc 300f": "SDWA",
    "maximum contaminant level": "SDWA_MCL",
    "mcl": "SDWA_MCL",
    "maximum contaminant level goal": "SDWA_MCLG",
    "mclg": "SDWA_MCLG",
    "underground injection control": "SDWA_UIC",
    "uic": "SDWA_UIC",
    "sole source aquifer": "SDWA_SSA",
    "wellhead protection": "SDWA_WHP",
    "public water system": "SDWA_PWS",
    "national primary drinking water regulation": "SDWA_NPDWR",
    "lead and copper rule": "SDWA_LCR",
    # OPA
    "oil pollution act": "OPA",
    "opa": "OPA",
    "33 usc 2701": "OPA",
    "oil spill": "OPA_SPILL",
    "facility response plan": "OPA_FRP",
    "frp": "OPA_FRP",
    "spcc plan": "OPA_SPCC",
    "spill prevention control and countermeasure": "OPA_SPCC",
    "natural resource damage": "OPA_NRD",
    "nrd": "OPA_NRD",
    "oil spill liability": "OPA_LIABILITY",
    "responsible party": "OPA_RP",
    # EPCRA
    "emergency planning and community right to know": "EPCRA",
    "epcra": "EPCRA",
    "42 usc 11001": "EPCRA",
    "toxic release inventory": "EPCRA_TRI",
    "tri": "EPCRA_TRI",
    "tier ii": "EPCRA_TIER_II",
    "material safety data sheet": "EPCRA_MSDS",
    "sds": "EPCRA_SDS",
    "local emergency planning committee": "EPCRA_LEPC",
    "lepc": "EPCRA_LEPC",
    # Texas agencies
    "tceq": "TCEQ",
    "texas commission on environmental quality": "TCEQ",
    "tnrcc": "TCEQ",
    "texas natural resource conservation commission": "TCEQ",
    "tceq air permit": "TCEQ_AIR",
    "tceq water permit": "TCEQ_WATER",
    "tceq waste permit": "TCEQ_WASTE",
    "tpdes": "TCEQ_TPDES",
    "texas pollutant discharge elimination system": "TCEQ_TPDES",
    "voluntary cleanup program": "TCEQ_VCP",
    "vcp": "TCEQ_VCP",
    "petroleum storage tank": "TCEQ_PST",
    "pst": "TCEQ_PST",
    "rrc": "RRC",
    "railroad commission": "RRC",
    "railroad commission of texas": "RRC",
    "rrc environmental": "RRC_ENVIRONMENTAL",
    "statewide rule 8": "RRC_SWR8",
    "swr 8": "RRC_SWR8",
    "statewide rule 9": "RRC_SWR9",
    "swr 9": "RRC_SWR9",
    "statewide rule 13": "RRC_SWR13",
    "statewide rule 14": "RRC_SWR14",
    "statewide rule 36": "RRC_SWR36",
    "tpwd": "TPWD",
    "texas parks and wildlife": "TPWD",
    # Environmental processes / topics
    "phase i environmental site assessment": "PHASE_I_ESA",
    "phase i esa": "PHASE_I_ESA",
    "phase i": "PHASE_I_ESA",
    "astm e1527": "PHASE_I_ESA",
    "all appropriate inquiries": "PHASE_I_ESA_AAI",
    "phase ii environmental site assessment": "PHASE_II_ESA",
    "phase ii esa": "PHASE_II_ESA",
    "phase ii": "PHASE_II_ESA",
    "environmental due diligence": "ENV_DUE_DILIGENCE",
    "environmental site assessment": "ENV_SITE_ASSESSMENT",
    "environmental impact assessment": "ENV_IMPACT_ASSESSMENT",
    "eia": "ENV_IMPACT_ASSESSMENT",
    "environmental justice": "ENV_JUSTICE",
    "ej": "ENV_JUSTICE",
    "executive order 12898": "ENV_JUSTICE_EO",
    "environmental audit privilege": "ENV_AUDIT_PRIVILEGE",
    "environmental disclosure": "ENV_DISCLOSURE",
    "environmental insurance": "ENV_INSURANCE",
    "environmental lien": "ENV_LIEN",
    "citizen suit": "CITIZEN_SUIT",
    "citizen suit provision": "CITIZEN_SUIT",
    "supplemental environmental project": "SEP",
    "sep": "SEP",
    "toxic tort": "TOXIC_TORT",
    "mass tort environmental": "TOXIC_TORT",
    "cancer cluster": "TOXIC_TORT_CANCER",
    "contaminated groundwater": "CONTAMINATION_GW",
    "groundwater contamination": "CONTAMINATION_GW",
    "soil contamination": "CONTAMINATION_SOIL",
    "air pollution": "AIR_POLLUTION",
    "water pollution": "WATER_POLLUTION",
    "noise pollution": "NOISE_POLLUTION",
    "light pollution": "LIGHT_POLLUTION",
    "carbon credit": "CARBON_CREDIT",
    "carbon offset": "CARBON_OFFSET",
    "carbon trading": "CARBON_TRADING",
    "cap and trade": "CAP_AND_TRADE",
    "carbon tax": "CARBON_TAX",
    "climate change regulation": "CLIMATE_REGULATION",
    "climate regulation": "CLIMATE_REGULATION",
    "paris agreement": "PARIS_AGREEMENT",
    "greenhouse gas regulation": "GHG_REGULATION",
    # Permian Basin specific
    "produced water": "PERMIAN_PRODUCED_WATER",
    "produced water disposal": "PERMIAN_PRODUCED_WATER",
    "saltwater disposal": "PERMIAN_SWD",
    "saltwater disposal well": "PERMIAN_SWD",
    "swd well": "PERMIAN_SWD",
    "induced seismicity": "PERMIAN_SEISMICITY",
    "earthquake from injection": "PERMIAN_SEISMICITY",
    "flaring": "PERMIAN_FLARING",
    "gas flaring": "PERMIAN_FLARING",
    "routine flaring": "PERMIAN_FLARING",
    "venting": "PERMIAN_VENTING",
    "methane emissions": "PERMIAN_METHANE",
    "methane leaks": "PERMIAN_METHANE",
    "fugitive emissions": "PERMIAN_FUGITIVE",
    "caliche pit": "PERMIAN_CALICHE_PIT",
    "pipeline spill": "PERMIAN_PIPELINE_SPILL",
    "oilfield waste": "PERMIAN_OILFIELD_WASTE",
    "drill cuttings": "PERMIAN_DRILL_CUTTINGS",
    "drilling mud": "PERMIAN_DRILLING_MUD",
    "frac fluid": "PERMIAN_FRAC_FLUID",
    "hydraulic fracturing": "PERMIAN_FRACKING",
    "fracking": "PERMIAN_FRACKING",
    "permian basin environmental": "PERMIAN_ENV",
    # Contaminants
    "benzene": "CONTAM_BENZENE",
    "toluene": "CONTAM_TOLUENE",
    "ethylbenzene": "CONTAM_ETHYLBENZENE",
    "xylene": "CONTAM_XYLENE",
    "btex": "CONTAM_BTEX",
    "trichloroethylene": "CONTAM_TCE",
    "tce": "CONTAM_TCE",
    "perchloroethylene": "CONTAM_PCE",
    "pce": "CONTAM_PCE",
    "tetrachloroethylene": "CONTAM_PCE",
    "mtbe": "CONTAM_MTBE",
    "methyl tert butyl ether": "CONTAM_MTBE",
    "arsenic": "CONTAM_ARSENIC",
    "mercury": "CONTAM_MERCURY",
    "lead contamination": "CONTAM_LEAD",
    "chromium": "CONTAM_CHROMIUM",
    "hexavalent chromium": "CONTAM_CHROMIUM_VI",
    "dioxin": "CONTAM_DIOXIN",
    "radionuclide": "CONTAM_RADIONUCLIDE",
    "norm": "CONTAM_NORM",
    "naturally occurring radioactive material": "CONTAM_NORM",
    "petroleum hydrocarbon": "CONTAM_TPH",
    "tph": "CONTAM_TPH",
    "total petroleum hydrocarbons": "CONTAM_TPH",
    "voc": "CONTAM_VOC",
    "volatile organic compound": "CONTAM_VOC",
    "svoc": "CONTAM_SVOC",
    "semi volatile organic compound": "CONTAM_SVOC",
    "heavy metal": "CONTAM_HEAVY_METAL",
    "pesticide contamination": "CONTAM_PESTICIDE",
    "herbicide contamination": "CONTAM_HERBICIDE",
    "per and polyfluoroalkyl substances": "CONTAM_PFAS",
    "pfas contamination": "CONTAM_PFAS",
    "pfoa": "CONTAM_PFOA",
    "pfos": "CONTAM_PFOS",
    "microplastic": "CONTAM_MICROPLASTIC",
    "radon": "CONTAM_RADON",
    "hydrogen sulfide": "CONTAM_H2S",
    "h2s": "CONTAM_H2S",
}

# ============================================================================
# AGENCY MAP
# ============================================================================

AGENCY_SYNONYMS: Dict[str, str] = {
    "epa": "EPA",
    "environmental protection agency": "EPA",
    "us epa": "EPA",
    "epa region 6": "EPA_REGION_6",
    "region 6": "EPA_REGION_6",
    "tceq": "TCEQ",
    "texas commission on environmental quality": "TCEQ",
    "railroad commission": "RRC",
    "rrc": "RRC",
    "railroad commission of texas": "RRC",
    "army corps of engineers": "USACE",
    "corps of engineers": "USACE",
    "usace": "USACE",
    "fish and wildlife service": "USFWS",
    "usfws": "USFWS",
    "fws": "USFWS",
    "nmfs": "NMFS",
    "national marine fisheries service": "NMFS",
    "noaa fisheries": "NMFS",
    "coast guard": "USCG",
    "uscg": "USCG",
    "department of interior": "DOI",
    "doi": "DOI",
    "blm": "BLM",
    "bureau of land management": "BLM",
    "forest service": "USFS",
    "usfs": "USFS",
    "nrc": "NRC",
    "nuclear regulatory commission": "NRC",
    "osha": "OSHA",
    "occupational safety and health": "OSHA",
    "dot": "DOT",
    "department of transportation": "DOT",
    "phmsa": "PHMSA",
    "pipeline and hazardous materials safety": "PHMSA",
    "atsdr": "ATSDR",
    "agency for toxic substances and disease registry": "ATSDR",
    "tpwd": "TPWD",
    "texas parks and wildlife department": "TPWD",
    "glc": "GLO",
    "glo": "GLO",
    "general land office": "GLO",
    "ceq": "CEQ",
    "council on environmental quality": "CEQ",
}

# ============================================================================
# JURISDICTION DETECTION
# ============================================================================

JURISDICTION_PATTERNS: Dict[str, str] = {
    "texas": "TX",
    "tx": "TX",
    "california": "CA",
    "ca": "CA",
    "new york": "NY",
    "ny": "NY",
    "florida": "FL",
    "fl": "FL",
    "louisiana": "LA",
    "la": "LA",
    "oklahoma": "OK",
    "ok": "OK",
    "new mexico": "NM",
    "nm": "NM",
    "colorado": "CO",
    "co": "CO",
    "pennsylvania": "PA",
    "pa": "PA",
    "ohio": "OH",
    "oh": "OH",
    "west virginia": "WV",
    "wv": "WV",
    "north dakota": "ND",
    "nd": "ND",
    "wyoming": "WY",
    "wy": "WY",
    "montana": "MT",
    "mt": "MT",
    "alaska": "AK",
    "ak": "AK",
    "federal": "FEDERAL",
    "midland": "TX",
    "ector county": "TX",
    "martin county": "TX",
    "reeves county": "TX",
    "permian basin": "TX",
    "west texas": "TX",
    "delaware basin": "TX",
    "midland basin": "TX",
    "central basin platform": "TX",
}

# ============================================================================
# DOMAIN CLASSIFICATION
# ============================================================================

DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "nepa": ["nepa", "eis", "ea", "fonsi", "catex", "environmental impact", "ceq", "scoping", "record of decision"],
    "air_quality": ["clean air", "caa", "naaqs", "nsps", "neshap", "title v", "air permit", "air quality", "emissions", "criteria pollutant", "hap", "attainment", "nonattainment", "bact", "laer", "psd", "new source review", "flaring", "methane", "ghg", "ozone"],
    "water_quality": ["clean water", "cwa", "npdes", "tpdes", "discharge", "effluent", "water quality", "stormwater", "wetlands", "section 404", "section 401", "tmdl", "potw", "swppp", "wotus", "navigable"],
    "hazardous_waste": ["rcra", "hazardous waste", "solid waste", "generator", "tsdf", "manifest", "ldr", "corrective action", "subtitle c", "subtitle d", "characteristic waste", "listed waste", "universal waste", "used oil"],
    "superfund": ["cercla", "superfund", "prp", "ncp", "npl", "brownfield", "ri/fs", "remedial", "removal action", "cost recovery", "contribution", "arar", "innocent purchaser", "bfpp", "contamination"],
    "toxic_substances": ["tsca", "pcb", "asbestos", "lead paint", "toxic", "chemical", "pfas", "pfoa", "pfos", "forever chemical", "premanufacture"],
    "endangered_species": ["esa", "endangered species", "threatened species", "critical habitat", "section 7", "section 9", "section 10", "biological opinion", "incidental take", "hcp", "jeopardy", "listing"],
    "pesticides": ["fifra", "pesticide", "herbicide", "insecticide", "fungicide", "rodenticide", "registration", "tolerance", "restricted use"],
    "drinking_water": ["sdwa", "safe drinking water", "mcl", "mclg", "uic", "injection well", "wellhead", "public water system", "drinking water"],
    "oil_spill": ["opa", "oil spill", "spcc", "facility response", "nrd", "natural resource damage", "oil pollution"],
    "permian_basin": ["permian", "produced water", "flaring", "venting", "induced seismicity", "saltwater disposal", "oilfield waste", "drill cutting", "frac fluid", "caliche pit", "pipeline spill", "h2s", "midland", "ector", "reeves"],
    "environmental_justice": ["environmental justice", "ej", "disproportionate impact", "executive order 12898", "vulnerable community", "cumulative impact"],
    "carbon_climate": ["carbon credit", "carbon offset", "cap and trade", "carbon tax", "climate", "greenhouse gas", "ghg", "paris agreement", "net zero", "carbon neutral"],
    "compliance_enforcement": ["compliance", "enforcement", "penalty", "violation", "citizen suit", "consent decree", "administrative order", "supplemental environmental project", "sep"],
    "site_assessment": ["phase i", "phase ii", "site assessment", "environmental assessment", "due diligence", "all appropriate inquiries", "astm e1527", "recognized environmental condition", "rec"],
    "remediation": ["remediation", "cleanup", "corrective action", "removal", "treatment", "monitored natural attenuation", "pump and treat", "soil vapor extraction", "bioremediation", "in situ", "ex situ"],
    "ust": ["underground storage tank", "ust", "petroleum storage tank", "leaking ust", "lust", "tank closure", "tank removal"],
    "epcra_reporting": ["epcra", "tri", "toxic release inventory", "tier ii", "emergency planning", "material safety", "sds", "lepc", "right to know"],
}

# ============================================================================
# PERMIT TYPE DETECTION
# ============================================================================

PERMIT_KEYWORDS: Dict[str, List[str]] = {
    "title_v": ["title v", "operating permit", "title v permit"],
    "nsr_psd": ["new source review", "nsr", "psd", "prevention of significant deterioration"],
    "npdes": ["npdes", "discharge permit", "npdes permit"],
    "tpdes": ["tpdes", "texas pollutant discharge"],
    "section_404": ["section 404", "dredge and fill", "wetland permit", "404 permit"],
    "rcra_part_b": ["rcra permit", "part b permit", "hazardous waste permit"],
    "uic": ["uic permit", "injection well permit", "underground injection"],
    "ust_registration": ["ust registration", "tank registration"],
    "spcc": ["spcc plan", "spill prevention plan"],
    "stormwater": ["stormwater permit", "swppp", "ms4 permit", "construction general permit"],
    "air_minor": ["minor source permit", "standard permit", "permit by rule"],
    "rrc_drilling": ["drilling permit", "oil well permit", "gas well permit"],
    "rrc_disposal": ["disposal well permit", "saltwater disposal permit", "swd permit"],
    "rrc_flaring": ["flaring permit", "flare permit", "exception to flaring"],
}


# ============================================================================
# SEMANTIC NORMALIZER
# ============================================================================

class EnvironmentalSemanticNormalizer:
    """Deterministic semantic normalizer for environmental law queries."""

    def __init__(self) -> None:
        self._sorted_statutes = sorted(STATUTE_SYNONYMS.keys(), key=len, reverse=True)
        self._sorted_agencies = sorted(AGENCY_SYNONYMS.keys(), key=len, reverse=True)
        self._sorted_jurisdictions = sorted(JURISDICTION_PATTERNS.keys(), key=len, reverse=True)
        self._compiled_patterns: Dict[str, re.Pattern[str]] = {}
        for term in self._sorted_statutes:
            escaped = re.escape(term)
            self._compiled_patterns[term] = re.compile(r"\b" + escaped + r"\b", re.IGNORECASE)
        logger.info(f"EnvironmentalSemanticNormalizer initialized: {len(STATUTE_SYNONYMS)} statute terms, "
                     f"{len(AGENCY_SYNONYMS)} agency terms, {len(JURISDICTION_PATTERNS)} jurisdictions")

    def normalize(self, query: str) -> NormalizationResult:
        """Normalize an environmental law query to canonical terms."""
        start = time.time()
        result = NormalizationResult(original_query=query, normalized_query=query)
        lowered = query.lower().strip()
        # Detect jurisdiction
        result.jurisdiction_detected = self._detect_jurisdiction(lowered)
        # Detect statutes via longest-match-first
        normalized_text = query
        for term in self._sorted_statutes:
            pattern = self._compiled_patterns.get(term)
            if pattern and pattern.search(lowered):
                canonical = STATUTE_SYNONYMS[term]
                if canonical not in result.statutes_detected:
                    result.statutes_detected.append(canonical)
                    result.mappings_applied.append({"from": term, "to": canonical, "type": "statute"})
                    result.confidence_boost += 0.05
                # Replace in normalized text (first match only for readability)
                pattern_norm = re.compile(re.escape(term), re.IGNORECASE)
                normalized_text = pattern_norm.sub(canonical, normalized_text, count=1)
        # Detect agencies
        for term in self._sorted_agencies:
            if term in lowered:
                canonical = AGENCY_SYNONYMS[term]
                if canonical not in result.agencies_detected:
                    result.agencies_detected.append(canonical)
                    result.mappings_applied.append({"from": term, "to": canonical, "type": "agency"})
        # Detect environmental domains
        result.environmental_domains = self._detect_domains(lowered)
        # Detect permit types
        result.permit_types_detected = self._detect_permit_types(lowered)
        # Detect contaminants
        result.contaminants_detected = self._detect_contaminants(lowered)
        result.normalized_query = normalized_text
        result.confidence_boost = min(result.confidence_boost, 0.30)
        result.duration_ms = (time.time() - start) * 1000
        content = f"{result.original_query}|{result.normalized_query}|{len(result.mappings_applied)}"
        result.normalization_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
        return result

    def _detect_jurisdiction(self, lowered: str) -> str:
        """Detect jurisdiction from query text."""
        for term in self._sorted_jurisdictions:
            if term in lowered:
                return JURISDICTION_PATTERNS[term]
        return "FEDERAL"

    def _detect_domains(self, lowered: str) -> List[str]:
        """Classify which environmental domains are referenced."""
        domains: List[str] = []
        for domain, keywords in DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw in lowered:
                    if domain not in domains:
                        domains.append(domain)
                    break
        return domains

    def _detect_permit_types(self, lowered: str) -> List[str]:
        """Detect permit types referenced."""
        permits: List[str] = []
        for permit_type, keywords in PERMIT_KEYWORDS.items():
            for kw in keywords:
                if kw in lowered:
                    if permit_type not in permits:
                        permits.append(permit_type)
                    break
        return permits

    def _detect_contaminants(self, lowered: str) -> List[str]:
        """Detect contaminants mentioned in the query."""
        contaminants: List[str] = []
        for term, canonical in STATUTE_SYNONYMS.items():
            if canonical.startswith("CONTAM_") and term in lowered:
                if canonical not in contaminants:
                    contaminants.append(canonical)
        return contaminants


# ============================================================================
# MODULE SINGLETON
# ============================================================================

_normalizer: Optional[EnvironmentalSemanticNormalizer] = None


def get_normalizer() -> EnvironmentalSemanticNormalizer:
    """Get or create the global semantic normalizer."""
    global _normalizer
    if _normalizer is None:
        _normalizer = EnvironmentalSemanticNormalizer()
    return _normalizer


def normalize_semantics(query: str) -> NormalizationResult:
    """Convenience: normalize an environmental law query."""
    return get_normalizer().normalize(query)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_statutes_from_text(text: str) -> List[str]:
    """Extract all recognized environmental statute references from text."""
    result = get_normalizer().normalize(text)
    return result.statutes_detected


def extract_agencies_from_text(text: str) -> List[str]:
    """Extract all recognized agency references from text."""
    result = get_normalizer().normalize(text)
    return result.agencies_detected


def extract_contaminants_from_text(text: str) -> List[str]:
    """Extract all recognized contaminant references from text."""
    result = get_normalizer().normalize(text)
    return result.contaminants_detected


def detect_jurisdiction(text: str) -> str:
    """Detect the primary jurisdiction from text."""
    return get_normalizer()._detect_jurisdiction(text.lower())


def classify_environmental_domains(text: str) -> List[str]:
    """Classify which environmental domains a text references."""
    return get_normalizer()._detect_domains(text.lower())


def identify_permit_types(text: str) -> List[str]:
    """Identify permit types referenced in text."""
    return get_normalizer()._detect_permit_types(text.lower())


def get_statute_canonical(term: str) -> Optional[str]:
    """Get the canonical identifier for a statute synonym."""
    return STATUTE_SYNONYMS.get(term.lower().strip())


def get_agency_canonical(term: str) -> Optional[str]:
    """Get the canonical identifier for an agency synonym."""
    return AGENCY_SYNONYMS.get(term.lower().strip())


def get_all_statute_synonyms() -> Dict[str, str]:
    """Get the complete statute synonym dictionary."""
    return dict(STATUTE_SYNONYMS)


def get_all_agency_synonyms() -> Dict[str, str]:
    """Get the complete agency synonym dictionary."""
    return dict(AGENCY_SYNONYMS)


def get_normalization_stats() -> Dict[str, Any]:
    """Get statistics about the normalization dictionaries."""
    return {
        "statute_synonyms": len(STATUTE_SYNONYMS),
        "agency_synonyms": len(AGENCY_SYNONYMS),
        "jurisdiction_patterns": len(JURISDICTION_PATTERNS),
        "domain_keyword_categories": len(DOMAIN_KEYWORDS),
        "domain_keywords_total": sum(len(v) for v in DOMAIN_KEYWORDS.values()),
        "permit_keyword_categories": len(PERMIT_KEYWORDS),
        "permit_keywords_total": sum(len(v) for v in PERMIT_KEYWORDS.values()),
        "contaminant_terms": sum(1 for v in STATUTE_SYNONYMS.values() if v.startswith("CONTAM_")),
    }


def batch_normalize(queries: List[str]) -> List[NormalizationResult]:
    """Normalize multiple queries in batch."""
    normalizer = get_normalizer()
    return [normalizer.normalize(q) for q in queries]


def compute_normalization_hash(query: str) -> str:
    """Compute the normalization hash for a query without full normalization."""
    result = get_normalizer().normalize(query)
    return result.normalization_hash
