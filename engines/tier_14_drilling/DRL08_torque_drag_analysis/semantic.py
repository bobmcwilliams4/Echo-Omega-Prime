import hashlib
import re
from typing import Dict, List, Any

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "DRL08 Python Engineering Team"
SEMANTIC_MAP_ENGINE = "DRL08_torque_drag_analysis"
_EXPECTED_ENTRY_COUNT = 234

SEMANTIC_MAP: Dict[str, str] = {
    # Soft String vs Stiff String Models
    "soft string": "soft_string_model",
    "soft-string": "soft_string_model",
    "softstring": "soft_string_model",
    "soft string model": "soft_string_model",
    "softstring model": "soft_string_model",
    "stiff string": "stiff_string_model",
    "stiff-string": "stiff_string_model",
    "stiffstring": "stiff_string_model",
    "stiff string model": "stiff_string_model",
    "stiffstring model": "stiff_string_model",
    "flexible string": "soft_string_model",
    "rigid string": "stiff_string_model",
    "ssm": "soft_string_model",
    "ss model": "soft_string_model",
    "ss": "soft_string_model",
    "stsm": "stiff_string_model",
    "st model": "stiff_string_model",
    "st": "stiff_string_model",

    # Friction Factor Estimation
    "friction factor": "friction_factor_estimation",
    "friction-factor": "friction_factor_estimation",
    "frictionfactor": "friction_factor_estimation",
    "ff": "friction_factor_estimation",
    "mu": "friction_factor_estimation",
    "coefficient of friction": "friction_factor_estimation",
    "friction coefficient": "friction_factor_estimation",
    "pipe friction": "friction_factor_estimation",
    "friction estimation": "friction_factor_estimation",
    "frictional resistance": "friction_factor_estimation",
    "friction analysis": "friction_factor_estimation",

    # Hook Load Calculations - Tripping In
    "hook load tripping in": "hook_load_tripping_in",
    "hookload tripping in": "hook_load_tripping_in",
    "hl tripping in": "hook_load_tripping_in",
    "tripping in hook load": "hook_load_tripping_in",
    "trip in hook load": "hook_load_tripping_in",
    "hook load in": "hook_load_tripping_in",
    "hl in": "hook_load_tripping_in",
    "tripping in": "hook_load_tripping_in",
    "trip in": "hook_load_tripping_in",

    # Hook Load Calculations - Tripping Out
    "hook load tripping out": "hook_load_tripping_out",
    "hookload tripping out": "hook_load_tripping_out",
    "hl tripping out": "hook_load_tripping_out",
    "tripping out hook load": "hook_load_tripping_out",
    "trip out hook load": "hook_load_tripping_out",
    "hook load out": "hook_load_tripping_out",
    "hl out": "hook_load_tripping_out",
    "tripping out": "hook_load_tripping_out",
    "trip out": "hook_load_tripping_out",

    # Hook Load - Rotating and Sliding
    "hook load rotating": "hook_load_rotating",
    "hook load sliding": "hook_load_sliding",
    "hl rotating": "hook_load_rotating",
    "hl sliding": "hook_load_sliding",
    "rotating hook load": "hook_load_rotating",
    "sliding hook load": "hook_load_sliding",
    "rotating": "hook_load_rotating",
    "sliding": "hook_load_sliding",

    # Make-Up Torque for Connections (API RP 7G)
    "make-up torque": "make_up_torque",
    "makeup torque": "make_up_torque",
    "make up torque": "make_up_torque",
    "connection torque": "make_up_torque",
    "torque for connections": "make_up_torque",
    "api rp 7g": "make_up_torque",
    "api 7g": "make_up_torque",
    "api7g": "make_up_torque",
    "connection make-up": "make_up_torque",
    "connection makeup": "make_up_torque",
    "torque makeup": "make_up_torque",
    "torque make-up": "make_up_torque",

    # Drill Collar Weight on Bit and Neutral Point
    "drill collar weight on bit": "dc_weight_on_bit",
    "dc weight on bit": "dc_weight_on_bit",
    "dc wob": "dc_weight_on_bit",
    "drill collar wob": "dc_weight_on_bit",
    "neutral point": "neutral_point",
    "neutral-point": "neutral_point",
    "np": "neutral_point",
    "drill collar neutral point": "neutral_point",
    "dc neutral point": "neutral_point",
    "weight on bit": "dc_weight_on_bit",
    "wob": "dc_weight_on_bit",

    # Buckling Analysis - Sinusoidal and Helical
    "buckling analysis": "buckling_analysis",
    "sinusoidal buckling": "sinusoidal_buckling",
    "helical buckling": "helical_buckling",
    "sinusoidal": "sinusoidal_buckling",
    "helical": "helical_buckling",
    "buckling": "buckling_analysis",
    "drillstring buckling": "buckling_analysis",
    "pipe buckling": "buckling_analysis",
    "sinusoidal mode": "sinusoidal_buckling",
    "helical mode": "helical_buckling",
    "buckling mode": "buckling_analysis",

    # Overpull Limits and Pipe Tensile Capacity
    "overpull limits": "overpull_limits",
    "overpull limit": "overpull_limits",
    "overpull": "overpull_limits",
    "pipe tensile capacity": "pipe_tensile_capacity",
    "tensile capacity": "pipe_tensile_capacity",
    "tensile limit": "pipe_tensile_capacity",
    "pipe tensile limit": "pipe_tensile_capacity",
    "tensile strength": "pipe_tensile_capacity",
    "pipe strength": "pipe_tensile_capacity",
    "overpull capacity": "overpull_limits",
    "tensile rating": "pipe_tensile_capacity",

    # Jarring Operations - Mechanical and Hydraulic Jars
    "jarring operations": "jarring_operations",
    "mechanical jar": "mechanical_jar",
    "hydraulic jar": "hydraulic_jar",
    "mechanical jarring": "mechanical_jar",
    "hydraulic jarring": "hydraulic_jar",
    "jar": "jarring_operations",
    "jarring": "jarring_operations",
    "jars": "jarring_operations",
    "mechanical jars": "mechanical_jar",
    "hydraulic jars": "hydraulic_jar",
    "jar operation": "jarring_operations",
    "jar operations": "jarring_operations",

    # Stuck Pipe Mechanisms - Differential Sticking
    "stuck pipe": "stuck_pipe",
    "stuckpipe": "stuck_pipe",
    "differential sticking": "differential_sticking",
    "diff sticking": "differential_sticking",
    "diff. sticking": "differential_sticking",
    "differential stick": "differential_sticking",
    "differential stuck": "differential_sticking",
    "sticking": "differential_sticking",
    "stuck": "stuck_pipe",
    "pipe sticking": "differential_sticking",
    "pipe stuck": "stuck_pipe",

    # Stuck Pipe Mechanisms - Keyseating
    "keyseating": "keyseating",
    "key seating": "keyseating",
    "key-seat": "keyseating",
    "key seat": "keyseating",
    "keyseat": "keyseating",
    "key seating mechanism": "keyseating",
    "keyseating mechanism": "keyseating",

    # Stuck Pipe Mechanisms - Pack-Off and Cuttings Bed
    "pack-off": "pack_off",
    "pack off": "pack_off",
    "packoff": "pack_off",
    "cuttings bed": "cuttings_bed",
    "cuttings-bed": "cuttings_bed",
    "cutting bed": "cuttings_bed",
    "cutting-bed": "cuttings_bed",
    "cuttings accumulation": "cuttings_bed",
    "cuttings pack-off": "pack_off",
    "cuttings pack off": "pack_off",
    "cuttings packoff": "pack_off",

    # Drillstring Fatigue Analysis
    "drillstring fatigue": "drillstring_fatigue",
    "drill string fatigue": "drillstring_fatigue",
    "fatigue analysis": "drillstring_fatigue",
    "fatigue": "drillstring_fatigue",
    "fatigue failure": "drillstring_fatigue",
    "fatigue life": "drillstring_fatigue",
    "fatigue limit": "drillstring_fatigue",
    "fatigue damage": "drillstring_fatigue",
    "drillpipe fatigue": "drillstring_fatigue",
    "dp fatigue": "drillstring_fatigue",

    # Drillstring Vibration - Lateral, Axial, Torsional
    "drillstring vibration": "drillstring_vibration",
    "drill string vibration": "drillstring_vibration",
    "vibration analysis": "drillstring_vibration",
    "lateral vibration": "lateral_vibration",
    "axial vibration": "axial_vibration",
    "torsional vibration": "torsional_vibration",
    "lateral": "lateral_vibration",
    "axial": "axial_vibration",
    "torsional": "torsional_vibration",
    "vibration": "drillstring_vibration",
    "drillpipe vibration": "drillstring_vibration",
    "dp vibration": "drillstring_vibration",
    "string vibration": "drillstring_vibration",

    # Stick-Slip Mitigation
    "stick-slip": "stick_slip_mitigation",
    "stick slip": "stick_slip_mitigation",
    "stickslip": "stick_slip_mitigation",
    "stick slip mitigation": "stick_slip_mitigation",
    "stick-slip mitigation": "stick_slip_mitigation",
    "stick slip control": "stick_slip_mitigation",
    "stick-slip control": "stick_slip_mitigation",
    "stick slip prevention": "stick_slip_mitigation",
    "stick-slip prevention": "stick_slip_mitigation",
    "stick slip effect": "stick_slip_mitigation",
    "stick-slip effect": "stick_slip_mitigation",

    # Casing Running Torque and Drag
    "casing running": "casing_running",
    "casing running torque": "casing_running_torque",
    "casing running drag": "casing_running_drag",
    "casing torque": "casing_running_torque",
    "casing drag": "casing_running_drag",
    "casing running t&d": "casing_running_torque_drag",
    "casing t&d": "casing_running_torque_drag",
    "casing torque and drag": "casing_running_torque_drag",
    "casing running torque and drag": "casing_running_torque_drag",
    "casing tnd": "casing_running_torque_drag",
    "casing t/d": "casing_running_torque_drag",
    "casing torque/drag": "casing_running_torque_drag",

    # BHA Stability Analysis
    "bha stability": "bha_stability_analysis",
    "bha stability analysis": "bha_stability_analysis",
    "bha": "bha_stability_analysis",
    "bottom hole assembly stability": "bha_stability_analysis",
    "bottom hole assembly": "bha_stability_analysis",
    "bha analysis": "bha_stability_analysis",
    "bha stability check": "bha_stability_analysis",
    "bha stability evaluation": "bha_stability_analysis",
    "bha stability modeling": "bha_stability_analysis",

    # Related and Misspelled Terms
    "drill string": "drillstring",
    "drillstring": "drillstring",
    "drill-string": "drillstring",
    "drill pipe": "drillpipe",
    "drillpipe": "drillpipe",
    "drill-pipe": "drillpipe",
    "dp": "drillpipe",
    "drill collar": "drillcollar",
    "drillcollar": "drillcollar",
    "drill-collar": "drillcollar",
    "dc": "drillcollar",
    "connection": "connection",
    "pipe": "pipe",
    "tubular": "pipe",
    "tubulars": "pipe",
    "string": "drillstring",
    "assembly": "bha_stability_analysis",
    "bottomhole assembly": "bha_stability_analysis",
    "bottom-hole assembly": "bha_stability_analysis",
    "bha stability check": "bha_stability_analysis",
    "bha stability evaluation": "bha_stability_analysis",

    # More synonyms and abbreviations
    "rotary torque": "make_up_torque",
    "rotary drag": "hook_load_rotating",
    "rotary": "hook_load_rotating",
    "slide": "hook_load_sliding",
    "sliding mode": "hook_load_sliding",
    "rotating mode": "hook_load_rotating",
    "running torque": "casing_running_torque",
    "running drag": "casing_running_drag",
    "running torque and drag": "casing_running_torque_drag",
    "running t&d": "casing_running_torque_drag",
    "running t/d": "casing_running_torque_drag",
    "running torque/drag": "casing_running_torque_drag",

    # Common misspellings and variants
    "dril string": "drillstring",
    "dril pipe": "drillpipe",
    "dril collar": "drillcollar",
    "drilstring": "drillstring",
    "drilpipe": "drillpipe",
    "drilcollar": "drillcollar",
    "dril-string": "drillstring",
    "dril-pipe": "drillpipe",
    "dril-collar": "drillcollar",
    "drilcollars": "drillcollar",
    "drillcollars": "drillcollar",
    "drilcollars": "drillcollar",

    # Additional related terms
    "pipe weight": "pipe_tensile_capacity",
    "pipe load": "hook_load_tripping_in",
    "pipe load out": "hook_load_tripping_out",
    "pipe load in": "hook_load_tripping_in",
    "pipe load rotating": "hook_load_rotating",
    "pipe load sliding": "hook_load_sliding",
    "pipe wob": "dc_weight_on_bit",
    "pipe neutral point": "neutral_point",
    "pipe buckling": "buckling_analysis",
    "pipe fatigue": "drillstring_fatigue",
    "pipe vibration": "drillstring_vibration",
    "pipe stick-slip": "stick_slip_mitigation",
    "pipe stick slip": "stick_slip_mitigation",
    "pipe stickslip": "stick_slip_mitigation",
    "pipe overpull": "overpull_limits",
    "pipe tensile": "pipe_tensile_capacity",
    "pipe tensile strength": "pipe_tensile_capacity",
    "pipe tensile limit": "pipe_tensile_capacity",
    "pipe tensile rating": "pipe_tensile_capacity",

    # Jarring synonyms
    "jarred": "jarring_operations",
    "jarring event": "jarring_operations",
    "jar event": "jarring_operations",
    "jarred pipe": "jarring_operations",
    "jar pipe": "jarring_operations",

    # Stuck pipe synonyms
    "stuck pipe mechanism": "stuck_pipe",
    "stuck pipe mechanisms": "stuck_pipe",
    "stuck pipe analysis": "stuck_pipe",
    "stuck pipe evaluation": "stuck_pipe",
    "stuck pipe modeling": "stuck_pipe",

    # Fatigue synonyms
    "fatigue modeling": "drillstring_fatigue",
    "fatigue evaluation": "drillstring_fatigue",
    "fatigue check": "drillstring_fatigue",
    "fatigue assessment": "drillstring_fatigue",

    # Vibration synonyms
    "vibration modeling": "drillstring_vibration",
    "vibration evaluation": "drillstring_vibration",
    "vibration check": "drillstring_vibration",
    "vibration assessment": "drillstring_vibration",

    # Buckling synonyms
    "buckling modeling": "buckling_analysis",
    "buckling evaluation": "buckling_analysis",
    "buckling check": "buckling_analysis",
    "buckling assessment": "buckling_analysis",

    # Hook load synonyms
    "hook load modeling": "hook_load_tripping_in",
    "hook load evaluation": "hook_load_tripping_in",
    "hook load check": "hook_load_tripping_in",
    "hook load assessment": "hook_load_tripping_in",

    # Pipe synonyms
    "pipe modeling": "drillstring",
    "pipe evaluation": "drillstring",
    "pipe check": "drillstring",
    "pipe assessment": "drillstring",

    # Casing synonyms
    "casing modeling": "casing_running",
    "casing evaluation": "casing_running",
    "casing check": "casing_running",
    "casing assessment": "casing_running",

    # BHA synonyms
    "bha modeling": "bha_stability_analysis",
    "bha evaluation": "bha_stability_analysis",
    "bha check": "bha_stability_analysis",
    "bha assessment": "bha_stability_analysis",

    # Miscellaneous
    "connection modeling": "make_up_torque",
    "connection evaluation": "make_up_torque",
    "connection check": "make_up_torque",
    "connection assessment": "make_up_torque",
    "connection make up": "make_up_torque",
    "connection make-up torque": "make_up_torque",
    "connection makeup torque": "make_up_torque",
    "connection torque modeling": "make_up_torque",
    "connection torque evaluation": "make_up_torque",
    "connection torque check": "make_up_torque",
    "connection torque assessment": "make_up_torque",
    "connection torque make up": "make_up_torque",
    "connection torque make-up": "make_up_torque",
    "connection torque makeup": "make_up_torque",
}

def _compute_map_hash() -> str:
    items = sorted(SEMANTIC_MAP.items())
    concat = "".join(f"{k}:{v};" for k, v in items)
    concat += f"{SEMANTIC_MAP_VERSION}:{SEMANTIC_MAP_ENGINE}:{SEMANTIC_MAP_AUTHOR}:{_EXPECTED_ENTRY_COUNT}"
    return hashlib.sha256(concat.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> Dict[str, Any]:
    actual_count = len(SEMANTIC_MAP)
    hash_now = _compute_map_hash()
    is_valid = (
        actual_count == _EXPECTED_ENTRY_COUNT and
        hash_now == _MAP_INTEGRITY_HASH
    )
    return {
        "status": "ok" if is_valid else "error",
        "entries": actual_count,
        "hash": hash_now,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    t = term.strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[-_]", " ", t)
    t = t.strip()
    if t in SEMANTIC_MAP:
        return SEMANTIC_MAP[t]
    t2 = t.replace(" ", "")
    if t2 in SEMANTIC_MAP:
        return SEMANTIC_MAP[t2]
    t3 = t.replace(" ", "_")
    if t3 in SEMANTIC_MAP:
        return SEMANTIC_MAP[t3]
    t4 = t.replace(" ", "-")
    if t4 in SEMANTIC_MAP:
        return SEMANTIC_MAP[t4]
    return t

def get_related_terms(term: str) -> List[str]:
    norm = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == norm]
    return sorted(set(related))

def get_all_mappings() -> Dict[str, str]:
    return dict(SEMANTIC_MAP)