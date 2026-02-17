import hashlib

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "CHEM18_thermodynamics Team"
SEMANTIC_MAP_ENGINE = "CHEM18"

SEMANTIC_MAP = {
    # Peng-Robinson EOS and variants
    "peng-robinson": "peng-robinson",
    "peng robinson": "peng-robinson",
    "pr eos": "peng-robinson",
    "pr equation of state": "peng-robinson",
    "peng robinson eos": "peng-robinson",
    "peng-robinson equation of state": "peng-robinson",
    "pengrobinson": "peng-robinson",
    "pr-eos": "peng-robinson",
    "peng-robinson eos": "peng-robinson",
    "peng robinson eos model": "peng-robinson",
    "pr eos model": "peng-robinson",
    "pr model": "peng-robinson",
    "peng-robinson model": "peng-robinson",
    "pr": "peng-robinson",

    # Soave-Redlich-Kwong EOS and variants
    "soave-redlich-kwong": "soave-redlich-kwong",
    "soave redlich kwong": "soave-redlich-kwong",
    "srk eos": "soave-redlich-kwong",
    "srk equation of state": "soave-redlich-kwong",
    "soave-redlich-kwong eos": "soave-redlich-kwong",
    "srk": "soave-redlich-kwong",
    "soave redlich kwong eos": "soave-redlich-kwong",
    "soave-redlich-kwong model": "soave-redlich-kwong",
    "srk model": "soave-redlich-kwong",

    # NRTL Activity Coefficient Model
    "nrtl": "nrtl",
    "nrtl model": "nrtl",
    "nonrandom two liquid": "nrtl",
    "nonrandom two-liquid": "nrtl",
    "nonrandom two liquid model": "nrtl",
    "nrtl activity coefficient": "nrtl",
    "nrtl activity coefficient model": "nrtl",
    "nrtl acm": "nrtl",

    # UNIQUAC Activity Coefficient Model
    "uniquac": "uniquac",
    "uniquac model": "uniquac",
    "uniquac activity coefficient": "uniquac",
    "uniquac activity coefficient model": "uniquac",
    "uniquac acm": "uniquac",

    # Wilson Activity Coefficient Model
    "wilson": "wilson",
    "wilson model": "wilson",
    "wilson activity coefficient": "wilson",
    "wilson activity coefficient model": "wilson",
    "wilson acm": "wilson",

    # Virial Equation of State
    "virial": "virial",
    "virial eos": "virial",
    "virial equation of state": "virial",
    "virial equation": "virial",
    "virial model": "virial",
    "virial equation of state model": "virial",

    # Gibbs Free Energy Minimization
    "gibbs free energy minimization": "gibbs free energy minimization",
    "gibbs free energy": "gibbs free energy minimization",
    "gibbs energy minimization": "gibbs free energy minimization",
    "gibbs free energy minim": "gibbs free energy minimization",
    "gibbs minimization": "gibbs free energy minimization",
    "gibbs free energy minimization for chemical equilibrium": "gibbs free energy minimization",

    # Rachford-Rice Flash Calculation
    "rachford-rice": "rachford-rice",
    "rachford rice": "rachford-rice",
    "rachford-rice flash": "rachford-rice",
    "rachford rice flash": "rachford-rice",
    "flash calculation": "rachford-rice",
    "flash calc": "rachford-rice",
    "flash calculation for two-phase equilibrium": "rachford-rice",
    "two-phase flash": "rachford-rice",
    "two phase flash": "rachford-rice",

    # UNIFAC Group Contribution Method
    "unifac": "unifac",
    "unifac method": "unifac",
    "unifac group contribution": "unifac",
    "unifac group contribution method": "unifac",
    "unifac gc method": "unifac",
    "unifac gc": "unifac",

    # Fugacity and Fugacity Coefficient
    "fugacity": "fugacity",
    "fugacity coefficient": "fugacity",
    "fugacity coeff": "fugacity",
    "fugacity coef": "fugacity",
    "fugacity and fugacity coefficient": "fugacity",

    # Hess's Law and Standard Enthalpy of Reaction
    "hess's law": "hess's law",
    "hess law": "hess's law",
    "hess law": "hess's law",
    "standard enthalpy of reaction": "standard enthalpy of reaction",
    "standard enthalpy": "standard enthalpy of reaction",
    "enthalpy of reaction": "standard enthalpy of reaction",
    "reaction enthalpy": "standard enthalpy of reaction",
    "hess's law and standard enthalpy of reaction": "hess's law",

    # Second Law Analysis and Entropy Generation
    "second law analysis": "second law analysis",
    "entropy generation": "second law analysis",
    "entropy gen": "second law analysis",
    "second law": "second law analysis",
    "entropy generation analysis": "second law analysis",
    "second law analysis and entropy generation": "second law analysis",

    # Azeotrope Formation and Breaking Strategies
    "azeotrope": "azeotrope",
    "azeotrope formation": "azeotrope",
    "azeotrope breaking": "azeotrope",
    "azeotrope breaking strategies": "azeotrope",
    "azeotrope formation and breaking strategies": "azeotrope",

    # Bubble Point and Dew Point Calculations
    "bubble point": "bubble point",
    "bubble point calculation": "bubble point",
    "bubble point calc": "bubble point",
    "dew point": "dew point",
    "dew point calculation": "dew point",
    "dew point calc": "dew point",
    "bubble point and dew point calculations": "bubble point",

    # Excess Gibbs Energy and Excess Properties
    "excess gibbs energy": "excess gibbs energy",
    "excess gibbs": "excess gibbs energy",
    "excess properties": "excess gibbs energy",
    "excess gibbs energy and excess properties": "excess gibbs energy",

    # Supercritical Fluid Thermodynamics and CO2 Applications
    "supercritical fluid thermodynamics": "supercritical fluid thermodynamics",
    "supercritical fluids": "supercritical fluid thermodynamics",
    "supercritical co2": "supercritical fluid thermodynamics",
    "co2 supercritical": "supercritical fluid thermodynamics",
    "co2 supercritical fluid": "supercritical fluid thermodynamics",
    "co2 applications": "supercritical fluid thermodynamics",
    "supercritical fluid thermodynamics and co2 applications": "supercritical fluid thermodynamics",

    # Thermodynamic Package Selection in Process Simulation
    "thermodynamic package selection": "thermodynamic package selection",
    "thermodynamic package": "thermodynamic package selection",
    "package selection": "thermodynamic package selection",
    "process simulation thermodynamics": "thermodynamic package selection",
    "thermodynamic package selection in process simulation": "thermodynamic package selection",

    # GERG-2008 Equation of State for Natural Gas
    "gerg-2008": "gerg-2008",
    "gerg 2008": "gerg-2008",
    "gerg-2008 eos": "gerg-2008",
    "gerg-2008 equation of state": "gerg-2008",
    "gerg2008": "gerg-2008",
    "gerg-2008 eos model": "gerg-2008",
    "gerg": "gerg-2008",

    # Le Chatelier's Principle and Reaction Equilibrium Shifts
    "le chatelier's principle": "le chatelier's principle",
    "le chatelier principle": "le chatelier's principle",
    "le chatelier": "le chatelier's principle",
    "reaction equilibrium shifts": "le chatelier's principle",
    "equilibrium shifts": "le chatelier's principle",
    "le chatelier's principle and reaction equilibrium shifts": "le chatelier's principle",

    # Activity and Activity Coefficient in Non-Ideal Solutions
    "activity": "activity",
    "activity coefficient": "activity",
    "activity coeff": "activity",
    "activity coef": "activity",
    "activity and activity coefficient": "activity",
    "non-ideal solutions activity": "activity",
    "nonideal solutions activity": "activity",

    # van der Waals Mixing Rules in Equation of State
    "van der waals mixing rules": "van der waals mixing rules",
    "vdw mixing rules": "van der waals mixing rules",
    "van der waals rules": "van der waals mixing rules",
    "vdw rules": "van der waals mixing rules",
    "van der waals mixing": "van der waals mixing rules",
    "vdw mixing": "van der waals mixing rules",

    # Joule-Thomson Effect and Coefficient
    "joule-thomson effect": "joule-thomson effect",
    "joule thomson effect": "joule-thomson effect",
    "jt effect": "joule-thomson effect",
    "joule-thomson coefficient": "joule-thomson effect",
    "joule thomson coefficient": "joule-thomson effect",
    "jt coefficient": "joule-thomson effect",
    "joule-thomson effect and coefficient": "joule-thomson effect",

    # Critical Point and Critical Phenomena
    "critical point": "critical point",
    "critical phenomena": "critical point",
    "critical temp": "critical point",
    "critical temperature": "critical point",
    "critical pressure": "critical point",
    "critical properties": "critical point",
    "critical point and critical phenomena": "critical point",

    # Additional synonyms and related terms for coverage
    "pr-eos model": "peng-robinson",
    "srk-eos": "soave-redlich-kwong",
    "srk-eos model": "soave-redlich-kwong",
    "nrtl ac model": "nrtl",
    "uniquac ac model": "uniquac",
    "wilson ac model": "wilson",
    "virial eos model": "virial",
    "gibbs minim": "gibbs free energy minimization",
    "flash calc two phase": "rachford-rice",
    "unifac gc method": "unifac",
    "fugacity coeff.": "fugacity",
    "hess law enthalpy": "hess's law",
    "entropy gen analysis": "second law analysis",
    "azeotrope break": "azeotrope",
    "bubble point calc": "bubble point",
    "dew point calc": "dew point",
    "excess gibbs": "excess gibbs energy",
    "supercritical co2 fluids": "supercritical fluid thermodynamics",
    "thermo package selection": "thermodynamic package selection",
    "gerg eos": "gerg-2008",
    "le chatelier principle": "le chatelier's principle",
    "activity coeff.": "activity",
    "vdw mixing rules eos": "van der waals mixing rules",
    "jt effect coeff": "joule-thomson effect",
    "critical phenomena study": "critical point",

    # Common misspellings and variants
    "peng robison": "peng-robinson",
    "soave redlich kwng": "soave-redlich-kwong",
    "rachford rice flash calc": "rachford-rice",
    "unifac group contrib": "unifac",
    "hess law enthalpy reaction": "hess's law",
    "azeotrope formation breaking": "azeotrope",
    "bubblepoint calculation": "bubble point",
    "dewpoint calculation": "dew point",
    "excess gibbs energies": "excess gibbs energy",
    "supercritical fluids co2": "supercritical fluid thermodynamics",
    "gerg2008 eos": "gerg-2008",
    "le chatelier principle reaction": "le chatelier's principle",
    "activity coeffs": "activity",
    "vdw mixing rules eos model": "van der waals mixing rules",
    "joule thomson coeff": "joule-thomson effect",
    "critical points": "critical point",

    # Additional related terms and abbreviations for domain completeness
    "eos": "eos",
    "equation of state": "eos",
    "activity coeff model": "activity",
    "flash calculation two phase": "rachford-rice",
    "group contribution method": "unifac",
    "enthalpy reaction": "standard enthalpy of reaction",
    "entropy gen rate": "second law analysis",
    "azeotrope break strategies": "azeotrope",
    "bubble point temp": "bubble point",
    "dew point temp": "dew point",
    "excess properties thermodynamics": "excess gibbs energy",
    "supercritical co2 applications": "supercritical fluid thermodynamics",
    "thermodynamic package": "thermodynamic package selection",
    "gerg eos natural gas": "gerg-2008",
    "reaction equilibrium shift": "le chatelier's principle",
    "activity coefficient nonideal": "activity",
    "vdw mixing rules eos": "van der waals mixing rules",
    "jt coefficient": "joule-thomson effect",
    "critical phenomena thermodynamics": "critical point",

    # General terms mapped to themselves
    "eos": "eos",
    "equation of state": "eos",
    "activity coefficient": "activity",
    "activity": "activity",
    "enthalpy": "enthalpy",
    "entropy": "entropy",
    "flash calculation": "flash calculation",
    "phase equilibrium": "phase equilibrium",
    "chemical equilibrium": "chemical equilibrium",
    "thermodynamics": "thermodynamics",
    "thermodynamic model": "thermodynamics",
    "thermodynamic package": "thermodynamic package selection",
    "reaction equilibrium": "reaction equilibrium",
    "mixing rules": "mixing rules",
    "group contribution": "group contribution",
    "critical properties": "critical point",
    "supercritical fluids": "supercritical fluid thermodynamics",
    "azeotrope": "azeotrope",
    "hess law": "hess's law",
    "second law": "second law analysis",
    "joule-thomson": "joule-thomson effect",
    "virial eos": "virial",
    "rachford-rice flash": "rachford-rice",
    "unifac method": "unifac",
    "nrtl model": "nrtl",
    "uniquac model": "uniquac",
    "wilson model": "wilson",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    m = hashlib.sha256()
    # Sort keys for consistent hashing
    for key in sorted(SEMANTIC_MAP.keys()):
        value = SEMANTIC_MAP[key]
        m.update(key.encode('utf-8'))
        m.update(b'\0')
        m.update(value.encode('utf-8'))
        m.update(b'\0')
    m.update(SEMANTIC_MAP_VERSION.encode('utf-8'))
    m.update(SEMANTIC_MAP_AUTHOR.encode('utf-8'))
    m.update(SEMANTIC_MAP_ENGINE.encode('utf-8'))
    return m.hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> dict:
    actual_count = len(SEMANTIC_MAP)
    is_valid = (actual_count == _EXPECTED_ENTRY_COUNT) and (_MAP_INTEGRITY_HASH == _compute_map_hash())
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": actual_count,
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "hash": _MAP_INTEGRITY_HASH,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    if not isinstance(term, str):
        raise TypeError("term must be a string")
    key = term.strip().lower()
    return SEMANTIC_MAP.get(key, key)

def get_related_terms(term: str) -> list[str]:
    normalized = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == normalized]
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)