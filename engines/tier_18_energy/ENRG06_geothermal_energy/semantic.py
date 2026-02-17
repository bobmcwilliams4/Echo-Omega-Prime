import hashlib
import re

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "ENRG06 Team"
SEMANTIC_MAP_ENGINE = "ENRG06_geothermal_energy"

SEMANTIC_MAP = {
    # USGS Geothermal Resource Classification System
    "usgs geothermal resource classification system": "usgs geothermal resource classification",
    "usgs geothermal classification": "usgs geothermal resource classification",
    "usgs resource classification": "usgs geothermal resource classification",
    "usgs geothermal system": "usgs geothermal resource classification",
    "usgs grcs": "usgs geothermal resource classification",
    "geothermal resource classification": "usgs geothermal resource classification",
    "resource classification system": "usgs geothermal resource classification",
    "resource classification": "usgs geothermal resource classification",
    "usgs geothermal": "usgs geothermal resource classification",
    "usgs": "usgs geothermal resource classification",

    # Geothermal Gradient and Heat Flow Assessment
    "geothermal gradient": "geothermal gradient and heat flow assessment",
    "heat flow": "geothermal gradient and heat flow assessment",
    "heat flow assessment": "geothermal gradient and heat flow assessment",
    "thermal gradient": "geothermal gradient and heat flow assessment",
    "temperature gradient": "geothermal gradient and heat flow assessment",
    "geothermal heat flow": "geothermal gradient and heat flow assessment",
    "subsurface temperature gradient": "geothermal gradient and heat flow assessment",
    "geothermal gradient assessment": "geothermal gradient and heat flow assessment",

    # Flash Steam vs Binary Cycle Technology Selection
    "flash steam": "flash steam vs binary cycle technology selection",
    "binary cycle": "flash steam vs binary cycle technology selection",
    "binary plant": "flash steam vs binary cycle technology selection",
    "flash plant": "flash steam vs binary cycle technology selection",
    "flash steam plant": "flash steam vs binary cycle technology selection",
    "binary cycle plant": "flash steam vs binary cycle technology selection",
    "technology selection": "flash steam vs binary cycle technology selection",
    "flash vs binary": "flash steam vs binary cycle technology selection",
    "binary vs flash": "flash steam vs binary cycle technology selection",
    "flash binary selection": "flash steam vs binary cycle technology selection",
    "steam cycle selection": "flash steam vs binary cycle technology selection",
    "binary cycle selection": "flash steam vs binary cycle technology selection",

    # Enhanced Geothermal Systems (EGS) Hydraulic Stimulation
    "enhanced geothermal systems": "egs hydraulic stimulation",
    "enhanced geothermal system": "egs hydraulic stimulation",
    "egs": "egs hydraulic stimulation",
    "egs stimulation": "egs hydraulic stimulation",
    "hydraulic stimulation": "egs hydraulic stimulation",
    "hydraulic fracturing": "egs hydraulic stimulation",
    "hydrofracturing": "egs hydraulic stimulation",
    "fracture stimulation": "egs hydraulic stimulation",
    "egs hydraulic stimulation": "egs hydraulic stimulation",
    "enhanced geothermal": "egs hydraulic stimulation",
    "enhanced system": "egs hydraulic stimulation",
    "enhanced systems": "egs hydraulic stimulation",

    # Geothermal Well Design for High Temperature Environments
    "geothermal well design": "geothermal well design high temperature",
    "well design": "geothermal well design high temperature",
    "high temperature well design": "geothermal well design high temperature",
    "high temp well design": "geothermal well design high temperature",
    "well design high temperature": "geothermal well design high temperature",
    "geothermal well": "geothermal well design high temperature",
    "well casing high temperature": "geothermal well design high temperature",
    "wellbore design": "geothermal well design high temperature",
    "well completion high temperature": "geothermal well design high temperature",
    "well construction high temperature": "geothermal well design high temperature",
    "high temperature environments": "geothermal well design high temperature",

    # Silica and Calcite Scaling Management
    "silica scaling": "silica and calcite scaling management",
    "calcite scaling": "silica and calcite scaling management",
    "scaling management": "silica and calcite scaling management",
    "scale management": "silica and calcite scaling management",
    "silica scale": "silica and calcite scaling management",
    "calcite scale": "silica and calcite scaling management",
    "scale inhibition": "silica and calcite scaling management",
    "scale control": "silica and calcite scaling management",
    "scaling control": "silica and calcite scaling management",
    "silica management": "silica and calcite scaling management",
    "calcite management": "silica and calcite scaling management",
    "scaling mitigation": "silica and calcite scaling management",

    # Induced Seismicity Traffic Light Protocol
    "induced seismicity": "induced seismicity traffic light protocol",
    "traffic light protocol": "induced seismicity traffic light protocol",
    "seismicity protocol": "induced seismicity traffic light protocol",
    "seismicity traffic light": "induced seismicity traffic light protocol",
    "induced seismicity protocol": "induced seismicity traffic light protocol",
    "induced seismicity tlp": "induced seismicity traffic light protocol",
    "tlp": "induced seismicity traffic light protocol",
    "seismicity management": "induced seismicity traffic light protocol",
    "seismic monitoring protocol": "induced seismicity traffic light protocol",
    "seismic traffic light": "induced seismicity traffic light protocol",

    # Ground-Source Heat Pump Coefficient of Performance (COP)
    "ground-source heat pump": "ground-source heat pump cop",
    "ground source heat pump": "ground-source heat pump cop",
    "gs heat pump": "ground-source heat pump cop",
    "gshp": "ground-source heat pump cop",
    "ground source pump": "ground-source heat pump cop",
    "heat pump cop": "ground-source heat pump cop",
    "coefficient of performance": "ground-source heat pump cop",
    "cop": "ground-source heat pump cop",
    "gs heat pump cop": "ground-source heat pump cop",
    "gshp cop": "ground-source heat pump cop",
    "ground-source cop": "ground-source heat pump cop",

    # Geothermal Reservoir Modeling with TOUGH2
    "geothermal reservoir modeling": "geothermal reservoir modeling tough2",
    "reservoir modeling": "geothermal reservoir modeling tough2",
    "tough2 modeling": "geothermal reservoir modeling tough2",
    "tough2": "geothermal reservoir modeling tough2",
    "reservoir simulation": "geothermal reservoir modeling tough2",
    "tough2 simulation": "geothermal reservoir modeling tough2",
    "geothermal simulation": "geothermal reservoir modeling tough2",
    "geothermal tough2": "geothermal reservoir modeling tough2",
    "reservoir model tough2": "geothermal reservoir modeling tough2",
    "tough2 model": "geothermal reservoir modeling tough2",

    # Geothermal Levelized Cost of Energy (LCOE) Analysis
    "levelized cost of energy": "geothermal lcoe analysis",
    "lcoe": "geothermal lcoe analysis",
    "geothermal lcoe": "geothermal lcoe analysis",
    "lcoe analysis": "geothermal lcoe analysis",
    "levelized cost analysis": "geothermal lcoe analysis",
    "cost of energy analysis": "geothermal lcoe analysis",
    "geothermal cost analysis": "geothermal lcoe analysis",
    "geothermal levelized cost": "geothermal lcoe analysis",
    "levelized energy cost": "geothermal lcoe analysis",

    # Non-Condensable Gas (NCG) Extraction and H2S Abatement
    "non-condensable gas": "ncg extraction and h2s abatement",
    "ncg": "ncg extraction and h2s abatement",
    "ncg extraction": "ncg extraction and h2s abatement",
    "h2s abatement": "ncg extraction and h2s abatement",
    "hydrogen sulfide abatement": "ncg extraction and h2s abatement",
    "hydrogen sulphide abatement": "ncg extraction and h2s abatement",
    "ncg removal": "ncg extraction and h2s abatement",
    "ncg abatement": "ncg extraction and h2s abatement",
    "noncondensable gas": "ncg extraction and h2s abatement",
    "non condensable gas": "ncg extraction and h2s abatement",
    "ncg management": "ncg extraction and h2s abatement",

    # Geothermal Reinjection Strategy and Pressure Maintenance
    "reinjection strategy": "geothermal reinjection strategy and pressure maintenance",
    "geothermal reinjection": "geothermal reinjection strategy and pressure maintenance",
    "reinjection": "geothermal reinjection strategy and pressure maintenance",
    "pressure maintenance": "geothermal reinjection strategy and pressure maintenance",
    "reinjection management": "geothermal reinjection strategy and pressure maintenance",
    "geothermal pressure maintenance": "geothermal reinjection strategy and pressure maintenance",
    "reinjection well": "geothermal reinjection strategy and pressure maintenance",
    "reinjection strategy geothermal": "geothermal reinjection strategy and pressure maintenance",
    "pressure support": "geothermal reinjection strategy and pressure maintenance",
    "re-injection": "geothermal reinjection strategy and pressure maintenance",

    # Geothermal Exploration Risk and Drilling Success Rates
    "exploration risk": "geothermal exploration risk and drilling success rates",
    "geothermal exploration risk": "geothermal exploration risk and drilling success rates",
    "drilling success rates": "geothermal exploration risk and drilling success rates",
    "exploration risk analysis": "geothermal exploration risk and drilling success rates",
    "geothermal drilling success": "geothermal exploration risk and drilling success rates",
    "exploration drilling risk": "geothermal exploration risk and drilling success rates",
    "exploration drilling success": "geothermal exploration risk and drilling success rates",
    "exploration risk geothermal": "geothermal exploration risk and drilling success rates",
    "drilling risk": "geothermal exploration risk and drilling success rates",
    "success rate drilling": "geothermal exploration risk and drilling success rates",

    # Binary Cycle Organic Rankine Cycle (ORC) Working Fluid Selection
    "orc": "binary cycle orc working fluid selection",
    "organic rankine cycle": "binary cycle orc working fluid selection",
    "orc working fluid": "binary cycle orc working fluid selection",
    "orc fluid selection": "binary cycle orc working fluid selection",
    "orc fluid": "binary cycle orc working fluid selection",
    "binary cycle orc": "binary cycle orc working fluid selection",
    "binary orc": "binary cycle orc working fluid selection",
    "working fluid selection": "binary cycle orc working fluid selection",
    "binary cycle working fluid": "binary cycle orc working fluid selection",
    "binary working fluid": "binary cycle orc working fluid selection",
    "binary orc working fluid": "binary cycle orc working fluid selection",
    "orc selection": "binary cycle orc working fluid selection",

    # Geothermal Power Plant Capacity Factor and Availability
    "capacity factor": "geothermal power plant capacity factor and availability",
    "plant capacity factor": "geothermal power plant capacity factor and availability",
    "availability": "geothermal power plant capacity factor and availability",
    "plant availability": "geothermal power plant capacity factor and availability",
    "geothermal capacity factor": "geothermal power plant capacity factor and availability",
    "geothermal plant availability": "geothermal power plant capacity factor and availability",
    "power plant capacity factor": "geothermal power plant capacity factor and availability",
    "power plant availability": "geothermal power plant capacity factor and availability",
    "capacity factor geothermal": "geothermal power plant capacity factor and availability",
    "availability geothermal": "geothermal power plant capacity factor and availability",

    # Geothermal Direct Use Applications
    "direct use": "geothermal direct use applications",
    "geothermal direct use": "geothermal direct use applications",
    "direct use applications": "geothermal direct use applications",
    "direct utilization": "geothermal direct use applications",
    "geothermal direct utilization": "geothermal direct use applications",
    "direct applications": "geothermal direct use applications",
    "direct heat use": "geothermal direct use applications",
    "direct heat applications": "geothermal direct use applications",
    "direct use geothermal": "geothermal direct use applications",

    # Geothermal Environmental Impact Assessment
    "environmental impact assessment": "geothermal environmental impact assessment",
    "geothermal environmental impact": "geothermal environmental impact assessment",
    "environmental assessment": "geothermal environmental impact assessment",
    "eia": "geothermal environmental impact assessment",
    "geothermal eia": "geothermal environmental impact assessment",
    "environmental impact": "geothermal environmental impact assessment",
    "environmental impact geothermal": "geothermal environmental impact assessment",
    "environmental impact study": "geothermal environmental impact assessment",
    "environmental impact analysis": "geothermal environmental impact assessment",

    # Additional Synonyms, Misspellings, Related Terms
    "usgs geothermal resource classifcation": "usgs geothermal resource classification",  # misspelling
    "geothermal gradent": "geothermal gradient and heat flow assessment",  # misspelling
    "flash steam technolgy": "flash steam vs binary cycle technology selection",  # misspelling
    "enhanced geothemal systems": "egs hydraulic stimulation",  # misspelling
    "well desgin": "geothermal well design high temperature",  # misspelling
    "silica and calcite scaling": "silica and calcite scaling management",
    "traffic light protcol": "induced seismicity traffic light protocol",  # misspelling
    "ground source heat pum": "ground-source heat pump cop",  # misspelling
    "tough 2": "geothermal reservoir modeling tough2",
    "levelized cost energy": "geothermal lcoe analysis",
    "noncondensable gases": "ncg extraction and h2s abatement",
    "reinjection stratgy": "geothermal reinjection strategy and pressure maintenance",  # misspelling
    "exploration rsk": "geothermal exploration risk and drilling success rates",  # misspelling
    "organic rankin cycle": "binary cycle orc working fluid selection",  # misspelling
    "power plant capacity": "geothermal power plant capacity factor and availability",
    "direct use application": "geothermal direct use applications",
    "environmental impact assesment": "geothermal environmental impact assessment",  # misspelling

    # Domain-specific abbreviations and related terms
    "hydraulic stim": "egs hydraulic stimulation",
    "fracturing": "egs hydraulic stimulation",
    "hydrofrac": "egs hydraulic stimulation",
    "thermal conductivity": "geothermal gradient and heat flow assessment",
    "heat loss": "geothermal gradient and heat flow assessment",
    "thermal regime": "geothermal gradient and heat flow assessment",
    "steam field": "flash steam vs binary cycle technology selection",
    "binary field": "flash steam vs binary cycle technology selection",
    "steam plant": "flash steam vs binary cycle technology selection",
    "binary plant technology": "flash steam vs binary cycle technology selection",
    "well integrity": "geothermal well design high temperature",
    "wellbore stability": "geothermal well design high temperature",
    "casing design": "geothermal well design high temperature",
    "wellhead design": "geothermal well design high temperature",
    "scale formation": "silica and calcite scaling management",
    "scale deposit": "silica and calcite scaling management",
    "scale removal": "silica and calcite scaling management",
    "scaling": "silica and calcite scaling management",
    "seismic risk": "induced seismicity traffic light protocol",
    "seismic hazard": "induced seismicity traffic light protocol",
    "seismic monitoring": "induced seismicity traffic light protocol",
    "ground source": "ground-source heat pump cop",
    "heat pump": "ground-source heat pump cop",
    "ground-coupled heat pump": "ground-source heat pump cop",
    "reservoir model": "geothermal reservoir modeling tough2",
    "reservoir engineering": "geothermal reservoir modeling tough2",
    "numerical modeling": "geothermal reservoir modeling tough2",
    "numerical simulation": "geothermal reservoir modeling tough2",
    "cost analysis": "geothermal lcoe analysis",
    "economic analysis": "geothermal lcoe analysis",
    "cost of electricity": "geothermal lcoe analysis",
    "hydrogen sulfide": "ncg extraction and h2s abatement",
    "h2s": "ncg extraction and h2s abatement",
    "gas extraction": "ncg extraction and h2s abatement",
    "gas abatement": "ncg extraction and h2s abatement",
    "pressure support strategy": "geothermal reinjection strategy and pressure maintenance",
    "pressure management": "geothermal reinjection strategy and pressure maintenance",
    "re-injection strategy": "geothermal reinjection strategy and pressure maintenance",
    "exploration drilling": "geothermal exploration risk and drilling success rates",
    "drilling success": "geothermal exploration risk and drilling success rates",
    "exploration success": "geothermal exploration risk and drilling success rates",
    "risk analysis": "geothermal exploration risk and drilling success rates",
    "risk assessment": "geothermal exploration risk and drilling success rates",
    "orc cycle": "binary cycle orc working fluid selection",
    "orc working fluids": "binary cycle orc working fluid selection",
    "working fluid": "binary cycle orc working fluid selection",
    "fluid selection": "binary cycle orc working fluid selection",
    "capacity": "geothermal power plant capacity factor and availability",
    "plant factor": "geothermal power plant capacity factor and availability",
    "plant performance": "geothermal power plant capacity factor and availability",
    "plant utilization": "geothermal power plant capacity factor and availability",
    "direct heating": "geothermal direct use applications",
    "district heating": "geothermal direct use applications",
    "greenhouse heating": "geothermal direct use applications",
    "aquaculture heating": "geothermal direct use applications",
    "spa heating": "geothermal direct use applications",
    "balneology": "geothermal direct use applications",
    "environmental assessment geothermal": "geothermal environmental impact assessment",
    "environmental review": "geothermal environmental impact assessment",
    "environmental permitting": "geothermal environmental impact assessment",
    "environmental compliance": "geothermal environmental impact assessment",

    # Misspellings and variants
    "usgs geothermal resource classfication": "usgs geothermal resource classification",
    "geothermal gradint": "geothermal gradient and heat flow assessment",
    "flash steem": "flash steam vs binary cycle technology selection",
    "enhanced geotermal systems": "egs hydraulic stimulation",
    "well desing": "geothermal well design high temperature",
    "silica and calicte scaling": "silica and calcite scaling management",
    "traffic light protocal": "induced seismicity traffic light protocol",
    "ground source heatp pump": "ground-source heat pump cop",
    "tough two": "geothermal reservoir modeling tough2",
    "levelized cost of enegy": "geothermal lcoe analysis",
    "noncondesable gas": "ncg extraction and h2s abatement",
    "reinjection stratgey": "geothermal reinjection strategy and pressure maintenance",
    "exploration risck": "geothermal exploration risk and drilling success rates",
    "organic rankine cycel": "binary cycle orc working fluid selection",
    "power plant capcity": "geothermal power plant capacity factor and availability",
    "direct use applicatons": "geothermal direct use applications",
    "environmental impact assesment": "geothermal environmental impact assessment",

    # More related terms and synonyms
    "resource assessment": "usgs geothermal resource classification",
    "resource evaluation": "usgs geothermal resource classification",
    "resource estimate": "usgs geothermal resource classification",
    "resource estimation": "usgs geothermal resource classification",
    "thermal assessment": "geothermal gradient and heat flow assessment",
    "thermal survey": "geothermal gradient and heat flow assessment",
    "temperature profile": "geothermal gradient and heat flow assessment",
    "steam cycle": "flash steam vs binary cycle technology selection",
    "binary cycle technology": "flash steam vs binary cycle technology selection",
    "binary technology": "flash steam vs binary cycle technology selection",
    "hydraulic fracturing egs": "egs hydraulic stimulation",
    "hydraulic stimulation egs": "egs hydraulic stimulation",
    "well design geothermal": "geothermal well design high temperature",
    "high temperature well": "geothermal well design high temperature",
    "scale inhibitor": "silica and calcite scaling management",
    "scale problems": "silica and calcite scaling management",
    "seismic protocol": "induced seismicity traffic light protocol",
    "seismic traffic protocol": "induced seismicity traffic light protocol",
    "ground-coupled pump": "ground-source heat pump cop",
    "gshp system": "ground-source heat pump cop",
    "reservoir simulation tough2": "geothermal reservoir modeling tough2",
    "tough2 code": "geothermal reservoir modeling tough2",
    "lcoe geothermal": "geothermal lcoe analysis",
    "energy cost analysis": "geothermal lcoe analysis",
    "ncg control": "ncg extraction and h2s abatement",
    "h2s control": "ncg extraction and h2s abatement",
    "reinjection control": "geothermal reinjection strategy and pressure maintenance",
    "pressure control": "geothermal reinjection strategy and pressure maintenance",
    "exploration drilling success rate": "geothermal exploration risk and drilling success rates",
    "orc binary cycle": "binary cycle orc working fluid selection",
    "orc binary": "binary cycle orc working fluid selection",
    "working fluid binary": "binary cycle orc working fluid selection",
    "plant capacity": "geothermal power plant capacity factor and availability",
    "plant availability factor": "geothermal power plant capacity factor and availability",
    "direct use system": "geothermal direct use applications",
    "direct use systems": "geothermal direct use applications",
    "environmental impact geothermal assessment": "geothermal environmental impact assessment",
    "environmental impact permit": "geothermal environmental impact assessment",
    "environmental impact compliance": "geothermal environmental impact assessment",
}

# Expand SEMANTIC_MAP with additional variants for coverage
for k in list(SEMANTIC_MAP.keys()):
    # Add lowercased, stripped versions if not already present
    norm = k.strip().lower()
    if norm not in SEMANTIC_MAP:
        SEMANTIC_MAP[norm] = SEMANTIC_MAP[k]
    # Add version with underscores
    norm_underscore = re.sub(r'\s+', '_', norm)
    if norm_underscore not in SEMANTIC_MAP:
        SEMANTIC_MAP[norm_underscore] = SEMANTIC_MAP[k]
    # Add version with hyphens
    norm_hyphen = re.sub(r'\s+', '-', norm)
    if norm_hyphen not in SEMANTIC_MAP:
        SEMANTIC_MAP[norm_hyphen] = SEMANTIC_MAP[k]

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash():
    items = sorted((k, v) for k, v in SEMANTIC_MAP.items())
    joined = "\n".join(f"{k}={v}" for k, v in items)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()

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
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "expected_hash": _MAP_INTEGRITY_HASH,
    }

def normalize_term(term: str) -> str:
    if not isinstance(term, str):
        return ""
    norm = term.strip().lower()
    if norm in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm]
    norm_underscore = re.sub(r'\s+', '_', norm)
    if norm_underscore in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm_underscore]
    norm_hyphen = re.sub(r'\s+', '-', norm)
    if norm_hyphen in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm_hyphen]
    # Try removing common punctuation
    norm_nopunct = re.sub(r'[^\w\s-]', '', norm)
    if norm_nopunct in SEMANTIC_MAP:
        return SEMANTIC_MAP[norm_nopunct]
    return norm

def get_related_terms(term: str) -> list:
    norm = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == norm]
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)