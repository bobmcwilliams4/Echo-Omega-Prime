import hashlib

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "DRL09_formation_evaluation Team"
SEMANTIC_MAP_ENGINE = "DRL09 Semantic Normalizer"

SEMANTIC_MAP = {
    # Gamma Ray Log Lithology Identification
    "gamma ray": "gamma_ray",
    "gr": "gamma_ray",
    "gammaray": "gamma_ray",
    "gamma-ray": "gamma_ray",
    "gamma ray log": "gamma_ray",
    "gr log": "gamma_ray",
    "gamma ray logging": "gamma_ray",
    "gr logging": "gamma_ray",
    "gamma ray lithology": "gamma_ray",
    "gr lithology": "gamma_ray",
    "gamma ray litho": "gamma_ray",
    "gr litho": "gamma_ray",
    "gr lith": "gamma_ray",
    "gamma ray lith": "gamma_ray",
    "gammaray lithology": "gamma_ray",
    "gammaray log": "gamma_ray",

    # Shale Volume Calculation Models
    "shale volume": "shale_volume",
    "vsh": "shale_volume",
    "vshale": "shale_volume",
    "shale vol": "shale_volume",
    "shale volume model": "shale_volume",
    "shale volume calculation": "shale_volume",
    "shale vol calc": "shale_volume",
    "shale volume calc": "shale_volume",
    "shale volume estimation": "shale_volume",

    # Deep Resistivity Tools - Laterolog vs Induction
    "deep resistivity": "deep_resistivity",
    "laterolog": "laterolog",
    "lls": "laterolog",
    "lls log": "laterolog",
    "laterolog shallow": "laterolog_shallow",
    "laterolog deep": "laterolog_deep",
    "induction log": "induction_log",
    "induction": "induction_log",
    "ind log": "induction_log",
    "ind": "induction_log",
    "deep resistivity tool": "deep_resistivity",
    "deep res": "deep_resistivity",
    "deep res tool": "deep_resistivity",
    "laterolog deep resistivity": "laterolog_deep",
    "induction deep resistivity": "induction_log",

    # Micro-Resistivity and Rxo Measurement
    "micro resistivity": "micro_resistivity",
    "microresistivity": "micro_resistivity",
    "micro res": "micro_resistivity",
    "micro res log": "micro_resistivity",
    "rxo": "rxo",
    "rxo measurement": "rxo",
    "rxo resistivity": "rxo",
    "rxo log": "rxo",
    "micro resistivity rxo": "micro_resistivity_rxo",
    "micro res rxo": "micro_resistivity_rxo",
    "micro resistivity and rxo": "micro_resistivity_rxo",

    # Density Log - Bulk Density and Porosity
    "density log": "density_log",
    "bulk density": "bulk_density",
    "bulk density log": "bulk_density",
    "density": "density_log",
    "den": "density_log",
    "bulk den": "bulk_density",
    "bulk dens": "bulk_density",
    "porosity": "porosity",
    "density porosity": "porosity",
    "bulk density porosity": "porosity",
    "density log porosity": "porosity",
    "bulk density and porosity": "bulk_density_porosity",

    # Neutron Log - Hydrogen Index Porosity
    "neutron log": "neutron_log",
    "neutron": "neutron_log",
    "neutron porosity": "neutron_porosity",
    "hydrogen index porosity": "neutron_porosity",
    "hi porosity": "neutron_porosity",
    "hydrogen index": "neutron_porosity",
    "neutron hydrogen index": "neutron_porosity",
    "neutron log porosity": "neutron_porosity",

    # Sonic Log - Wyllie Time Average Equation
    "sonic log": "sonic_log",
    "sonic": "sonic_log",
    "sonic travel time": "sonic_travel_time",
    "dt": "sonic_travel_time",
    "delta t": "sonic_travel_time",
    "wyllie time average": "wyllie_time_average",
    "wyllie equation": "wyllie_time_average",
    "wyllie time average equation": "wyllie_time_average",
    "sonic log wyllie": "wyllie_time_average",
    "sonic dt": "sonic_travel_time",

    # Archie Equation - Water Saturation Calculation
    "archie equation": "archie_equation",
    "archie": "archie_equation",
    "water saturation": "water_saturation",
    "sw": "water_saturation",
    "saturation water": "water_saturation",
    "archie's equation": "archie_equation",
    "water saturation calculation": "water_saturation",
    "archie's water saturation": "water_saturation",
    "archie sw": "water_saturation",
    "sw calculation": "water_saturation",

    # Formation Water Resistivity (Rw) Determination
    "formation water resistivity": "formation_water_resistivity",
    "rw": "formation_water_resistivity",
    "formation water r": "formation_water_resistivity",
    "formation water resist": "formation_water_resistivity",
    "water resistivity": "formation_water_resistivity",
    "rw determination": "formation_water_resistivity",
    "formation water resistivity determination": "formation_water_resistivity",

    # Spontaneous Potential (SP) Log Interpretation
    "sp log": "sp_log",
    "spontaneous potential": "sp_log",
    "spontaneous potential log": "sp_log",
    "sp": "sp_log",
    "sp log interpretation": "sp_log",
    "sp interpretation": "sp_log",
    "spontaneous potential interpretation": "sp_log",

    # Caliper Log - Borehole Size and Formation Quality
    "caliper log": "caliper_log",
    "caliper": "caliper_log",
    "borehole size": "borehole_size",
    "borehole diameter": "borehole_size",
    "borehole caliper": "caliper_log",
    "formation quality": "formation_quality",
    "caliper formation quality": "formation_quality",
    "caliper log borehole size": "borehole_size",

    # NMR Logging - T2 Distributions and Permeability
    "nmr logging": "nmr_logging",
    "nmr": "nmr_logging",
    "t2 distribution": "t2_distribution",
    "t2 distributions": "t2_distribution",
    "nmr t2": "t2_distribution",
    "nmr t2 distribution": "t2_distribution",
    "permeability": "permeability",
    "nmr permeability": "permeability",
    "nmr log permeability": "permeability",

    # Formation Pressure Testing - MDT, RFT, DST
    "formation pressure testing": "formation_pressure_testing",
    "mdt": "mdt",
    "modular formation dynamics tester": "mdt",
    "rft": "rft",
    "repeat formation tester": "rft",
    "dst": "dst",
    "drill stem test": "dst",
    "formation pressure": "formation_pressure_testing",
    "pressure testing": "formation_pressure_testing",

    # Mud Logging - Gas Shows and Cuttings Analysis
    "mud logging": "mud_logging",
    "mud log": "mud_logging",
    "gas shows": "gas_shows",
    "mud gas shows": "gas_shows",
    "cuttings analysis": "cuttings_analysis",
    "mud cuttings": "cuttings_analysis",
    "mud logging gas shows": "gas_shows",
    "mud logging cuttings analysis": "cuttings_analysis",

    # LWD (Logging While Drilling) vs Wireline Comparison
    "lwd": "lwd",
    "logging while drilling": "lwd",
    "wireline logging": "wireline_logging",
    "wireline": "wireline_logging",
    "lwd vs wireline": "lwd_wireline_comparison",
    "logging while drilling vs wireline": "lwd_wireline_comparison",
    "lwd wireline comparison": "lwd_wireline_comparison",

    # Neutron-Density Crossplot for Lithology and Gas
    "neutron density crossplot": "neutron_density_crossplot",
    "neutron-density crossplot": "neutron_density_crossplot",
    "neutron density cross plot": "neutron_density_crossplot",
    "neutron density crossplot lithology": "neutron_density_crossplot",
    "neutron density gas crossplot": "neutron_density_crossplot",
    "neutron density crossplot gas": "neutron_density_crossplot",

    # M-N Plot and MID Plot for Complex Lithology
    "m-n plot": "m_n_plot",
    "mn plot": "m_n_plot",
    "m n plot": "m_n_plot",
    "mid plot": "mid_plot",
    "m-i-d plot": "mid_plot",
    "midplot": "mid_plot",
    "m-n plot lithology": "m_n_plot",
    "mid plot lithology": "mid_plot",
    "m-n plot complex lithology": "m_n_plot",
    "mid plot complex lithology": "mid_plot",

    # Thin Bed Analysis and Vertical Resolution
    "thin bed analysis": "thin_bed_analysis",
    "thinbed analysis": "thin_bed_analysis",
    "thin bed": "thin_bed",
    "vertical resolution": "vertical_resolution",
    "thin bed vertical resolution": "vertical_resolution",
    "thin bed analysis vertical resolution": "vertical_resolution",

    # Invasion Profile and Radial Resistivity Variations
    "invasion profile": "invasion_profile",
    "invasion": "invasion_profile",
    "radial resistivity variations": "radial_resistivity_variations",
    "radial resistivity": "radial_resistivity_variations",
    "invasion profile resistivity": "invasion_profile",
    "radial resistivity invasion": "radial_resistivity_variations",

    # Formation Damage Identification via Logs
    "formation damage": "formation_damage",
    "formation damage identification": "formation_damage",
    "damage identification": "formation_damage",
    "formation damage logs": "formation_damage",
    "damage logs": "formation_damage",

    # Core Analysis Correlation with Log Data
    "core analysis": "core_analysis",
    "core data": "core_analysis",
    "core log correlation": "core_log_correlation",
    "core analysis correlation": "core_log_correlation",
    "core log data correlation": "core_log_correlation",

    # Pay Zone Identification Criteria
    "pay zone": "pay_zone",
    "payzone": "pay_zone",
    "pay zone identification": "pay_zone",
    "pay zone criteria": "pay_zone",
    "pay zone evaluation": "pay_zone",

    # Net-to-Gross Calculation and Reservoir Volume
    "net to gross": "net_to_gross",
    "net-to-gross": "net_to_gross",
    "net/gross": "net_to_gross",
    "net to gross ratio": "net_to_gross",
    "net to gross calculation": "net_to_gross",
    "reservoir volume": "reservoir_volume",
    "reservoir vol": "reservoir_volume",
    "reservoir volume calculation": "reservoir_volume",

    # Petrophysical Cutoff Optimization
    "petrophysical cutoff": "petrophysical_cutoff",
    "cutoff optimization": "petrophysical_cutoff",
    "petrophysical cutoff optimization": "petrophysical_cutoff",
    "cutoff optimization petrophysics": "petrophysical_cutoff",

    # Permian Basin - Spraberry Formation Characteristics
    "spraberry formation": "spraberry_formation",
    "spraberry": "spraberry_formation",
    "permian spraberry": "spraberry_formation",
    "spraberry formation characteristics": "spraberry_formation",
    "spraberry formation evaluation": "spraberry_formation",

    # Permian Basin - Wolfcamp Formation Evaluation
    "wolfcamp formation": "wolfcamp_formation",
    "wolfcamp": "wolfcamp_formation",
    "permian wolfcamp": "wolfcamp_formation",
    "wolfcamp formation evaluation": "wolfcamp_formation",
    "wolfcamp formation characteristics": "wolfcamp_formation",

    # Permian Basin - Bone Spring Formation (Delaware Basin)
    "bone spring formation": "bone_spring_formation",
    "bone spring": "bone_spring_formation",
    "delaware basin bone spring": "bone_spring_formation",
    "bone spring formation delaware": "bone_spring_formation",
    "bone spring formation evaluation": "bone_spring_formation",

    # Additional synonyms and misspellings for coverage
    "gammaray log lithology": "gamma_ray",
    "shale volumn": "shale_volume",
    "laterolog deep resistivity tool": "laterolog_deep",
    "micro-resistivity": "micro_resistivity",
    "bulk densitiy": "bulk_density",
    "neutron porosity hydrogen index": "neutron_porosity",
    "sonic travel time dt": "sonic_travel_time",
    "archie water saturation": "water_saturation",
    "formation water resistivity rw": "formation_water_resistivity",
    "spontaneous potential sp": "sp_log",
    "caliper borehole size": "borehole_size",
    "nmr t2 distribution": "t2_distribution",
    "modular formation dynamics tester mdt": "mdt",
    "repeat formation tester rft": "rft",
    "drill stem test dst": "dst",
    "mud logging gas shows": "gas_shows",
    "logging while drilling lwd": "lwd",
    "wireline logging comparison": "wireline_logging",
    "neutron density cross plot": "neutron_density_crossplot",
    "m-n plot complex lithology": "m_n_plot",
    "mid plot complex lithology": "mid_plot",
    "thin bed vertical resolution": "vertical_resolution",
    "invasion profile resistivity": "invasion_profile",
    "formation damage logs": "formation_damage",
    "core analysis log correlation": "core_log_correlation",
    "pay zone evaluation criteria": "pay_zone",
    "net to gross ratio calculation": "net_to_gross",
    "petrophysical cutoff optimization": "petrophysical_cutoff",
    "permian basin spraberry": "spraberry_formation",
    "permian basin wolfcamp": "wolfcamp_formation",
    "permian basin bone spring": "bone_spring_formation",
    # Common misspellings and variants
    "gammaraylog": "gamma_ray",
    "shalevol": "shale_volume",
    "laterologdeep": "laterolog_deep",
    "microresistivityrxo": "micro_resistivity_rxo",
    "bulkdensity": "bulk_density",
    "neutronporosity": "neutron_porosity",
    "soniclog": "sonic_log",
    "archiewater": "water_saturation",
    "formationwaterresistivity": "formation_water_resistivity",
    "spontaneouspotential": "sp_log",
    "caliperlog": "caliper_log",
    "nmrlogging": "nmr_logging",
    "formationpressuretesting": "formation_pressure_testing",
    "mudlogging": "mud_logging",
    "lwdvswireline": "lwd_wireline_comparison",
    "neutrondensitycrossplot": "neutron_density_crossplot",
    "mnplot": "m_n_plot",
    "midplot": "mid_plot",
    "thinbedanalysis": "thin_bed_analysis",
    "invasionprofile": "invasion_profile",
    "formationdamage": "formation_damage",
    "coreanalysis": "core_analysis",
    "payzone": "pay_zone",
    "nettogross": "net_to_gross",
    "petrophysicalcutoff": "petrophysical_cutoff",
    "spraberryformation": "spraberry_formation",
    "wolfcampformation": "wolfcamp_formation",
    "bonespringformation": "bone_spring_formation",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    hasher = hashlib.sha256()
    for key in sorted(SEMANTIC_MAP.keys()):
        value = SEMANTIC_MAP[key]
        hasher.update(key.encode('utf-8'))
        hasher.update(b'\0')
        hasher.update(value.encode('utf-8'))
        hasher.update(b'\0')
    return hasher.hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> dict:
    current_count = len(SEMANTIC_MAP)
    current_hash = _compute_map_hash()
    is_valid = (current_count == _EXPECTED_ENTRY_COUNT) and (current_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": current_count,
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "hash": current_hash,
        "expected_hash": _MAP_INTEGRITY_HASH,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    if not isinstance(term, str):
        raise TypeError("term must be a string")
    key = term.strip().lower()
    return SEMANTIC_MAP.get(key, key)

def get_related_terms(term: str) -> list[str]:
    if not isinstance(term, str):
        raise TypeError("term must be a string")
    normalized = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == normalized]
    # Ensure normalized term itself is included if it appears as a key
    if normalized not in related:
        related.append(normalized)
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)  # return a shallow copy to prevent external modification