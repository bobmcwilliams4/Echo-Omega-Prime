import hashlib
import re
from typing import Dict, List

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "OFE02 Engine Team"
SEMANTIC_MAP_ENGINE = "OFE02_BOP_stack_analysis"

# Core domain terms (normalized forms)
NORMALIZED_TERMS = [
    "annular preventer",
    "ram preventer",
    "bop testing",
    "api rp 53",
    "accumulator system",
    "accumulator sizing",
    "bop control system",
    "hydraulic control",
    "mux control",
    "electro-hydraulic control",
    "surface bop stack",
    "subsea bop system",
    "bop pressure rating",
    "kill line",
    "choke manifold",
    "h2s service",
    "bop equipment",
    "bop failure mode",
    "root cause analysis",
    "deepwater bop",
    "cameron bop",
    "nov bop",
    "hydril bop",
    "bop stack-up",
    "well conditions",
    "diverter system",
    "shallow gas hazard",
    "bop maintenance",
    "maasp calculation",
    "bop rating selection",
    "control system redundancy",
    "deadman configuration",
    "wellbore pressure calculation",
    "component leak detection",
    "troubleshooting",
    "bop component",
    "bop stack configuration",
    "bop system design",
    "bop selection",
    "kill line operation",
    "choke manifold operation",
    "bop testing protocol",
    "accumulator design",
    "bop control",
    "surface bop",
    "subsea bop",
    "pressure rating",
    "kill line procedure",
    "choke manifold design",
    "h2s equipment",
    "failure mode",
    "root cause",
    "deepwater",
    "cameron",
    "nov",
    "hydril",
    "stack-up design",
    "diverter",
    "shallow gas",
    "maintenance program",
    "intervals",
    "maasp",
    "rating selection",
    "redundancy",
    "deadman",
    "wellbore pressure",
    "leak detection",
    "troubleshooting procedure",
]

# Synonyms, abbreviations, acronyms, misspellings, related terms
SEMANTIC_MAP: Dict[str, str] = {
    # Annular Preventer
    "annular": "annular preventer",
    "annular bop": "annular preventer",
    "annular blowout preventer": "annular preventer",
    "annular preventor": "annular preventer",
    "annular seal": "annular preventer",
    "annular packing": "annular preventer",
    "annular element": "annular preventer",
    "annular closure": "annular preventer",
    "annular type bop": "annular preventer",
    "annular preventer function": "annular preventer",
    "annular operation": "annular preventer",
    "annular pressure": "annular preventer",
    "annular control": "annular preventer",
    "annular test": "annular preventer",

    # Ram Preventer
    "ram": "ram preventer",
    "ram bop": "ram preventer",
    "ram blowout preventer": "ram preventer",
    "ram preventor": "ram preventer",
    "ram type bop": "ram preventer",
    "ram function": "ram preventer",
    "ram operation": "ram preventer",
    "ram test": "ram preventer",
    "shear ram": "ram preventer",
    "blind ram": "ram preventer",
    "pipe ram": "ram preventer",
    "variable bore ram": "ram preventer",
    "vbr": "ram preventer",
    "ram block": "ram preventer",
    "ram element": "ram preventer",
    "ram closure": "ram preventer",

    # BOP Testing Protocols
    "bop test": "bop testing",
    "bop testing protocol": "bop testing",
    "bop pressure test": "bop testing",
    "bop function test": "bop testing",
    "bop stack test": "bop testing",
    "bop test procedure": "bop testing",
    "bop test interval": "bop testing",
    "bop test record": "bop testing",
    "bop test requirement": "bop testing",
    "bop test standard": "bop testing",
    "bop test api": "bop testing",
    "api rp53": "api rp 53",
    "api rp 53": "api rp 53",
    "api rp-53": "api rp 53",
    "api rp53 protocol": "api rp 53",
    "api rp 53 test": "api rp 53",
    "api 53": "api rp 53",
    "api standard 53": "api rp 53",

    # Accumulator System
    "accumulator": "accumulator system",
    "accumulator unit": "accumulator system",
    "accumulator bottle": "accumulator system",
    "accumulator bank": "accumulator system",
    "accumulator sizing": "accumulator sizing",
    "accumulator capacity": "accumulator sizing",
    "accumulator calculation": "accumulator sizing",
    "accumulator pressure": "accumulator system",
    "accumulator design": "accumulator system",
    "accumulator system design": "accumulator system",
    "accumulator stack": "accumulator system",
    "accumulator manifold": "accumulator system",
    "accumulator test": "accumulator system",
    "accumulator function": "accumulator system",
    "accumulator protocol": "accumulator system",

    # BOP Control Systems
    "bop control": "bop control system",
    "bop control system": "bop control system",
    "bop control panel": "bop control system",
    "bop control unit": "bop control system",
    "bop control pod": "bop control system",
    "bop control line": "bop control system",
    "bop control fluid": "bop control system",
    "hydraulic control": "hydraulic control",
    "hydraulic bop control": "hydraulic control",
    "hydraulic system": "hydraulic control",
    "hydraulic pod": "hydraulic control",
    "mux": "mux control",
    "mux control": "mux control",
    "mux pod": "mux control",
    "mux system": "mux control",
    "mux panel": "mux control",
    "mux line": "mux control",
    "electro-hydraulic control": "electro-hydraulic control",
    "eh control": "electro-hydraulic control",
    "electro hydraulic": "electro-hydraulic control",
    "electrohydraulic": "electro-hydraulic control",
    "electro hydraulic pod": "electro-hydraulic control",
    "electro hydraulic system": "electro-hydraulic control",

    # Surface BOP Stack Configuration
    "surface bop": "surface bop stack",
    "surface bop stack": "surface bop stack",
    "surface stack": "surface bop stack",
    "surface stack configuration": "surface bop stack",
    "surface bop configuration": "surface bop stack",
    "surface bop design": "surface bop stack",
    "surface bop system": "surface bop stack",
    "surface bop component": "surface bop stack",

    # Subsea BOP System Design and Components
    "subsea bop": "subsea bop system",
    "subsea bop stack": "subsea bop system",
    "subsea stack": "subsea bop system",
    "subsea bop configuration": "subsea bop system",
    "subsea bop design": "subsea bop system",
    "subsea bop component": "subsea bop system",
    "subsea bop system": "subsea bop system",
    "subsea bop pod": "subsea bop system",
    "subsea bop manifold": "subsea bop system",
    "subsea bop control": "subsea bop system",

    # BOP Pressure Ratings and Selection
    "pressure rating": "bop pressure rating",
    "bop pressure rating": "bop pressure rating",
    "bop rating": "bop pressure rating",
    "bop rating selection": "bop rating selection",
    "bop pressure": "bop pressure rating",
    "bop selection": "bop rating selection",
    "pressure selection": "bop rating selection",
    "pressure rating selection": "bop rating selection",
    "maasp": "maasp calculation",
    "maasp calculation": "maasp calculation",
    "maasp formula": "maasp calculation",
    "maasp value": "maasp calculation",
    "maasp test": "maasp calculation",
    "maximum allowable annular surface pressure": "maasp calculation",
    "maximum allowable annular pressure": "maasp calculation",
    "maasp determination": "maasp calculation",

    # Kill Line Operations and Procedures
    "kill line": "kill line",
    "kill line operation": "kill line",
    "kill line procedure": "kill line",
    "kill line test": "kill line",
    "kill line valve": "kill line",
    "kill line manifold": "kill line",
    "kill line function": "kill line",
    "kill line connection": "kill line",
    "kill line equipment": "kill line",
    "kill line pressure": "kill line",
    "kill line design": "kill line",

    # Choke Manifold Design and Operation
    "choke manifold": "choke manifold",
    "choke manifold operation": "choke manifold",
    "choke manifold design": "choke manifold",
    "choke manifold test": "choke manifold",
    "choke manifold valve": "choke manifold",
    "choke manifold function": "choke manifold",
    "choke manifold connection": "choke manifold",
    "choke manifold equipment": "choke manifold",
    "choke manifold pressure": "choke manifold",
    "choke manifold configuration": "choke manifold",
    "choke manifold sizing": "choke manifold",

    # H2S Service BOP Equipment Requirements
    "h2s service": "h2s service",
    "h2s equipment": "h2s service",
    "h2s bop": "h2s service",
    "h2s service bop": "h2s service",
    "h2s service equipment": "h2s service",
    "h2s requirement": "h2s service",
    "h2s resistant bop": "h2s service",
    "h2s resistant equipment": "h2s service",
    "h2s test": "h2s service",
    "h2s protocol": "h2s service",

    # BOP Failure Modes and Root Cause Analysis
    "failure mode": "bop failure mode",
    "bop failure mode": "bop failure mode",
    "bop failure": "bop failure mode",
    "failure analysis": "root cause analysis",
    "root cause analysis": "root cause analysis",
    "root cause": "root cause analysis",
    "failure investigation": "root cause analysis",
    "failure troubleshooting": "root cause analysis",
    "failure detection": "bop failure mode",
    "failure record": "bop failure mode",
    "failure report": "bop failure mode",
    "failure protocol": "bop failure mode",
    "failure prevention": "bop failure mode",

    # Deepwater BOP Considerations and Challenges
    "deepwater bop": "deepwater bop",
    "deepwater bop system": "deepwater bop",
    "deepwater bop stack": "deepwater bop",
    "deepwater bop configuration": "deepwater bop",
    "deepwater bop design": "deepwater bop",
    "deepwater bop component": "deepwater bop",
    "deepwater bop control": "deepwater bop",
    "deepwater bop operation": "deepwater bop",
    "deepwater bop challenge": "deepwater bop",
    "deepwater bop consideration": "deepwater bop",
    "deepwater bop issue": "deepwater bop",
    "deepwater bop test": "deepwater bop",
    "deepwater bop protocol": "deepwater bop",

    # Cameron vs NOV vs Hydril BOP Comparison
    "cameron bop": "cameron bop",
    "cameron bop stack": "cameron bop",
    "cameron bop system": "cameron bop",
    "cameron bop component": "cameron bop",
    "cameron bop design": "cameron bop",
    "cameron bop control": "cameron bop",
    "cameron bop operation": "cameron bop",
    "cameron bop test": "cameron bop",
    "cameron bop protocol": "cameron bop",
    "nov bop": "nov bop",
    "nov bop stack": "nov bop",
    "nov bop system": "nov bop",
    "nov bop component": "nov bop",
    "nov bop design": "nov bop",
    "nov bop control": "nov bop",
    "nov bop operation": "nov bop",
    "nov bop test": "nov bop",
    "nov bop protocol": "nov bop",
    "hydril bop": "hydril bop",
    "hydril bop stack": "hydril bop",
    "hydril bop system": "hydril bop",
    "hydril bop component": "hydril bop",
    "hydril bop design": "hydril bop",
    "hydril bop control": "hydril bop",
    "hydril bop operation": "hydril bop",
    "hydril bop test": "hydril bop",
    "hydril bop protocol": "hydril bop",

    # BOP Stack-Up Design for Specific Well Conditions
    "bop stack-up": "bop stack-up",
    "bop stack up": "bop stack-up",
    "stack-up design": "bop stack-up",
    "stack up design": "bop stack-up",
    "stack-up configuration": "bop stack-up",
    "stack up configuration": "bop stack-up",
    "stack-up protocol": "bop stack-up",
    "stack up protocol": "bop stack-up",
    "stack-up test": "bop stack-up",
    "stack up test": "bop stack-up",
    "stack-up operation": "bop stack-up",
    "stack up operation": "bop stack-up",
    "well condition": "well conditions",
    "well conditions": "well conditions",
    "well condition design": "well conditions",
    "well condition protocol": "well conditions",
    "well condition test": "well conditions",

    # Diverter Systems for Shallow Gas Hazards
    "diverter": "diverter system",
    "diverter system": "diverter system",
    "diverter stack": "diverter system",
    "diverter operation": "diverter system",
    "diverter test": "diverter system",
    "diverter protocol": "diverter system",
    "diverter design": "diverter system",
    "diverter component": "diverter system",
    "diverter function": "diverter system",
    "diverter equipment": "diverter system",
    "shallow gas": "shallow gas hazard",
    "shallow gas hazard": "shallow gas hazard",
    "shallow gas protocol": "shallow gas hazard",
    "shallow gas test": "shallow gas hazard",
    "shallow gas operation": "shallow gas hazard",
    "shallow gas design": "shallow gas hazard",
    "shallow gas equipment": "shallow gas hazard",

    # BOP Maintenance Programs and Intervals
    "maintenance": "bop maintenance",
    "bop maintenance": "bop maintenance",
    "maintenance program": "bop maintenance",
    "maintenance interval": "bop maintenance",
    "maintenance schedule": "bop maintenance",
    "maintenance record": "bop maintenance",
    "maintenance protocol": "bop maintenance",
    "maintenance test": "bop maintenance",
    "maintenance operation": "bop maintenance",
    "maintenance design": "bop maintenance",
    "maintenance equipment": "bop maintenance",
    "maintenance component": "bop maintenance",

    # BOP Control System Redundancy and Deadman Configuration
    "redundancy": "control system redundancy",
    "control system redundancy": "control system redundancy",
    "redundant control system": "control system redundancy",
    "redundant bop control": "control system redundancy",
    "redundant hydraulic control": "control system redundancy",
    "redundant mux control": "control system redundancy",
    "redundant electro-hydraulic control": "control system redundancy",
    "deadman": "deadman configuration",
    "deadman configuration": "deadman configuration",
    "deadman system": "deadman configuration",
    "deadman protocol": "deadman configuration",
    "deadman test": "deadman configuration",
    "deadman operation": "deadman configuration",
    "deadman design": "deadman configuration",
    "deadman equipment": "deadman configuration",
    "deadman component": "deadman configuration",

    # Wellbore Pressure Calculations During Well Control
    "wellbore pressure": "wellbore pressure calculation",
    "wellbore pressure calculation": "wellbore pressure calculation",
    "wellbore pressure test": "wellbore pressure calculation",
    "wellbore pressure protocol": "wellbore pressure calculation",
    "wellbore pressure operation": "wellbore pressure calculation",
    "wellbore pressure design": "wellbore pressure calculation",
    "wellbore pressure equipment": "wellbore pressure calculation",
    "wellbore pressure component": "wellbore pressure calculation",

    # BOP Component Leak Detection and Troubleshooting
    "leak detection": "component leak detection",
    "component leak detection": "component leak detection",
    "leak test": "component leak detection",
    "leak protocol": "component leak detection",
    "leak operation": "component leak detection",
    "leak design": "component leak detection",
    "leak equipment": "component leak detection",
    "leak component": "component leak detection",
    "troubleshooting": "troubleshooting",
    "troubleshooting procedure": "troubleshooting",
    "troubleshooting protocol": "troubleshooting",
    "troubleshooting test": "troubleshooting",
    "troubleshooting operation": "troubleshooting",
    "troubleshooting design": "troubleshooting",
    "troubleshooting equipment": "troubleshooting",
    "troubleshooting component": "troubleshooting",

    # General BOP Terms
    "bop": "bop component",
    "blowout preventer": "bop component",
    "blowout preventor": "bop component",
    "bop stack": "bop stack configuration",
    "bop stack configuration": "bop stack configuration",
    "bop stack design": "bop stack configuration",
    "bop stack system": "bop stack configuration",
    "bop stack component": "bop stack configuration",
    "bop stack protocol": "bop stack configuration",
    "bop stack test": "bop stack configuration",
    "bop stack operation": "bop stack configuration",
    "bop stack equipment": "bop stack configuration",
    "bop stack-up design": "bop stack-up",
    "bop stack-up configuration": "bop stack-up",
    "bop stack-up protocol": "bop stack-up",
    "bop stack-up test": "bop stack-up",
    "bop stack-up operation": "bop stack-up",
    "bop stack-up equipment": "bop stack-up",
    "bop stack-up component": "bop stack-up",

    # Misspellings and Variants
    "blow out preventer": "bop component",
    "blow out preventor": "bop component",
    "blow-out preventer": "bop component",
    "blow-out preventor": "bop component",
    "blowout preventer stack": "bop stack configuration",
    "blowout preventor stack": "bop stack configuration",
    "blow out preventer stack": "bop stack configuration",
    "blow out preventor stack": "bop stack configuration",
    "blow-out preventer stack": "bop stack configuration",
    "blow-out preventor stack": "bop stack configuration",

    # Additional synonyms and abbreviations
    "bop system": "bop system design",
    "bop system design": "bop system design",
    "bop system configuration": "bop system design",
    "bop system component": "bop system design",
    "bop system protocol": "bop system design",
    "bop system test": "bop system design",
    "bop system operation": "bop system design",
    "bop system equipment": "bop system design",

    # More related terms
    "component": "bop component",
    "component design": "bop component",
    "component protocol": "bop component",
    "component test": "bop component",
    "component operation": "bop component",
    "component equipment": "bop component",
    "component stack": "bop component",

    # General
    "stack": "bop stack configuration",
    "stack design": "bop stack configuration",
    "stack protocol": "bop stack configuration",
    "stack test": "bop stack configuration",
    "stack operation": "bop stack configuration",
    "stack equipment": "bop stack configuration",
    "stack component": "bop stack configuration",
}

# Add normalized terms as their own mapping
for term in NORMALIZED_TERMS:
    SEMANTIC_MAP[term] = term

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    items = sorted(SEMANTIC_MAP.items())
    joined = "".join(f"{k}:{v};" for k, v in items)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> Dict[str, object]:
    actual_count = len(SEMANTIC_MAP)
    hash_now = _compute_map_hash()
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (hash_now == _MAP_INTEGRITY_HASH)
    return {
        "status": "OK" if is_valid else "FAIL",
        "entries": actual_count,
        "hash": hash_now,
        "is_valid": is_valid,
    }

def _normalize_string(term: str) -> str:
    term = term.lower()
    term = re.sub(r"[^a-z0-9\s\-]", "", term)
    term = re.sub(r"\s+", " ", term)
    term = term.strip()
    return term

def normalize_term(term: str) -> str:
    norm = _normalize_string(term)
    return SEMANTIC_MAP.get(norm, norm)

def get_related_terms(term: str) -> List[str]:
    normalized = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == normalized]
    return sorted(set(related))

def get_all_mappings() -> Dict[str, str]:
    return dict(SEMANTIC_MAP)