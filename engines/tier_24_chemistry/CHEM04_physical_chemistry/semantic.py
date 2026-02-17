import hashlib

SEMANTIC_MAP_ENGINE = "CHEM04_physical_chemistry"
SEMANTIC_MAP_AUTHOR = "ExpertPythonEngineer"
SEMANTIC_MAP_VERSION = "1.0.0"

SEMANTIC_MAP = {
    # First Law of Thermodynamics
    "first law of thermodynamics": "first_law_of_thermodynamics",
    "1st law of thermodynamics": "first_law_of_thermodynamics",
    "law of energy conservation": "first_law_of_thermodynamics",
    "energy conservation law": "first_law_of_thermodynamics",
    "first law": "first_law_of_thermodynamics",
    "1st law": "first_law_of_thermodynamics",
    "energy balance": "first_law_of_thermodynamics",
    "internal energy change": "first_law_of_thermodynamics",
    "delta u": "first_law_of_thermodynamics",
    "du": "first_law_of_thermodynamics",

    # Second Law and Entropy
    "second law of thermodynamics": "second_law_of_thermodynamics",
    "2nd law of thermodynamics": "second_law_of_thermodynamics",
    "entropy increase": "second_law_of_thermodynamics",
    "law of entropy": "second_law_of_thermodynamics",
    "entropy": "entropy",
    "s": "entropy",
    "disorder": "entropy",
    "irreversibility": "second_law_of_thermodynamics",
    "entropy change": "entropy",
    "delta s": "entropy",
    "ds": "entropy",

    # Gibbs Free Energy and Spontaneity
    "gibbs free energy": "gibbs_free_energy",
    "gibbs energy": "gibbs_free_energy",
    "gibbs function": "gibbs_free_energy",
    "g": "gibbs_free_energy",
    "gibbs free energy change": "gibbs_free_energy",
    "delta g": "gibbs_free_energy",
    "dg": "gibbs_free_energy",
    "free energy": "gibbs_free_energy",
    "spontaneity": "spontaneity",
    "reaction spontaneity": "spontaneity",
    "spontaneous reaction": "spontaneity",
    "nonspontaneous": "spontaneity",
    "non spontaneous": "spontaneity",

    # Chemical Potential
    "chemical potential": "chemical_potential",
    "mu": "chemical_potential",
    "partial molar gibbs energy": "chemical_potential",
    "partial molar free energy": "chemical_potential",
    "chemical potential energy": "chemical_potential",

    # Rate Laws and Reaction Order
    "rate law": "rate_law",
    "reaction rate law": "rate_law",
    "rate equation": "rate_law",
    "reaction order": "reaction_order",
    "order of reaction": "reaction_order",
    "reaction kinetics order": "reaction_order",
    "kinetic order": "reaction_order",
    "zero order": "zero_order_reaction",
    "first order": "first_order_reaction",
    "second order": "second_order_reaction",
    "third order": "third_order_reaction",
    "rate constant": "rate_constant",
    "k": "rate_constant",

    # Arrhenius Equation
    "arrhenius equation": "arrhenius_equation",
    "arrhenius law": "arrhenius_equation",
    "activation energy equation": "arrhenius_equation",
    "arrhenius eq": "arrhenius_equation",
    "activation energy": "activation_energy",
    "ea": "activation_energy",
    "pre-exponential factor": "pre_exponential_factor",
    "frequency factor": "pre_exponential_factor",
    "a factor": "pre_exponential_factor",

    # Transition State Theory
    "transition state theory": "transition_state_theory",
    "activated complex theory": "transition_state_theory",
    "tst": "transition_state_theory",
    "activated complex": "activated_complex",
    "transition state": "transition_state",
    "reaction coordinate": "reaction_coordinate",

    # Catalysis Mechanisms
    "catalysis": "catalysis",
    "catalytic mechanism": "catalysis",
    "catalyst": "catalyst",
    "enzyme catalysis": "enzyme_catalysis",
    "heterogeneous catalysis": "heterogeneous_catalysis",
    "homogeneous catalysis": "homogeneous_catalysis",
    "catalytic cycle": "catalytic_cycle",
    "activation energy lowering": "activation_energy",

    # Schrödinger Equation and Wavefunctions
    "schrödinger equation": "schrodinger_equation",
    "schrodinger equation": "schrodinger_equation",
    "wavefunction": "wavefunction",
    "psi": "wavefunction",
    "quantum wavefunction": "wavefunction",
    "time independent schrödinger equation": "time_independent_schrodinger_equation",
    "time dependent schrödinger equation": "time_dependent_schrodinger_equation",
    "hamiltonian operator": "hamiltonian_operator",
    "hamiltonian": "hamiltonian_operator",

    # Molecular Orbital Theory
    "molecular orbital theory": "molecular_orbital_theory",
    "mot": "molecular_orbital_theory",
    "molecular orbitals": "molecular_orbitals",
    "mo": "molecular_orbitals",
    "bonding orbital": "bonding_orbital",
    "antibonding orbital": "antibonding_orbital",
    "nonbonding orbital": "nonbonding_orbital",
    "homo": "highest_occupied_molecular_orbital",
    "lumo": "lowest_unoccupied_molecular_orbital",
    "highest occupied molecular orbital": "highest_occupied_molecular_orbital",
    "lowest unoccupied molecular orbital": "lowest_unoccupied_molecular_orbital",

    # Hartree-Fock Method
    "hartree-fock method": "hartree_fock_method",
    "hf method": "hartree_fock_method",
    "hartree-fock": "hartree_fock_method",
    "self-consistent field method": "hartree_fock_method",
    "scf method": "hartree_fock_method",
    "hartree-fock wavefunction": "hartree_fock_wavefunction",

    # Statistical Mechanics Foundations
    "statistical mechanics": "statistical_mechanics",
    "stat mech": "statistical_mechanics",
    "partition function": "partition_function",
    "z": "partition_function",
    "boltzmann distribution": "boltzmann_distribution",
    "boltzmann factor": "boltzmann_factor",
    "microstate": "microstate",
    "macrostate": "macrostate",
    "ensemble": "ensemble",
    "canonical ensemble": "canonical_ensemble",
    "grand canonical ensemble": "grand_canonical_ensemble",
    "microcanonical ensemble": "microcanonical_ensemble",

    # Adsorption Isotherms
    "adsorption isotherm": "adsorption_isotherm",
    "langmuir isotherm": "langmuir_isotherm",
    "freundlich isotherm": "freundlich_isotherm",
    "adsorption equilibrium": "adsorption_equilibrium",
    "surface coverage": "surface_coverage",
    "theta": "surface_coverage",

    # Electrochemistry and Nernst Equation
    "electrochemistry": "electrochemistry",
    "nernst equation": "nernst_equation",
    "nernst eq": "nernst_equation",
    "electrode potential": "electrode_potential",
    "standard electrode potential": "standard_electrode_potential",
    "cell potential": "cell_potential",
    "galvanic cell": "galvanic_cell",
    "voltaic cell": "galvanic_cell",
    "electrolytic cell": "electrolytic_cell",
    "redox reaction": "redox_reaction",
    "oxidation-reduction": "redox_reaction",

    # Spectroscopy Fundamentals
    "spectroscopy": "spectroscopy",
    "uv-vis spectroscopy": "uv_vis_spectroscopy",
    "infrared spectroscopy": "infrared_spectroscopy",
    "ir spectroscopy": "infrared_spectroscopy",
    "nmr spectroscopy": "nmr_spectroscopy",
    "nuclear magnetic resonance": "nmr_spectroscopy",
    "mass spectrometry": "mass_spectrometry",
    "ms": "mass_spectrometry",
    "absorption spectrum": "absorption_spectrum",
    "emission spectrum": "emission_spectrum",

    # Phase Diagrams and Phase Rule
    "phase diagram": "phase_diagram",
    "phase rule": "phase_rule",
    "gibbs phase rule": "phase_rule",
    "degrees of freedom": "degrees_of_freedom",
    "f": "degrees_of_freedom",
    "triple point": "triple_point",
    "critical point": "critical_point",
    "phase boundary": "phase_boundary",

    # Diffusion and Transport Phenomena
    "diffusion": "diffusion",
    "fick's law": "ficks_law",
    "ficks first law": "ficks_law",
    "ficks second law": "ficks_second_law",
    "transport phenomena": "transport_phenomena",
    "mass transport": "mass_transport",
    "heat transport": "heat_transport",
    "momentum transport": "momentum_transport",
    "diffusion coefficient": "diffusion_coefficient",
    "diffusivity": "diffusion_coefficient",

    # Colligative Properties
    "colligative properties": "colligative_properties",
    "boiling point elevation": "boiling_point_elevation",
    "bpe": "boiling_point_elevation",
    "freezing point depression": "freezing_point_depression",
    "fpd": "freezing_point_depression",
    "osmotic pressure": "osmotic_pressure",
    "vapor pressure lowering": "vapor_pressure_lowering",
    "raoult's law": "raoults_law",
    "raoults law": "raoults_law",

    # Computational Chemistry Methods
    "computational chemistry": "computational_chemistry",
    "ab initio methods": "ab_initio_methods",
    "density functional theory": "density_functional_theory",
    "dft": "density_functional_theory",
    "molecular dynamics": "molecular_dynamics",
    "md simulation": "molecular_dynamics",
    "monte carlo simulation": "monte_carlo_simulation",
    "semi-empirical methods": "semi_empirical_methods",

    # Photochemistry Principles
    "photochemistry": "photochemistry",
    "photoexcitation": "photoexcitation",
    "photolysis": "photolysis",
    "fluorescence": "fluorescence",
    "phosphorescence": "phosphorescence",
    "quantum yield": "quantum_yield",
    "excited state": "excited_state",

    # Polymer Physical Chemistry
    "polymer chemistry": "polymer_physical_chemistry",
    "polymer physical chemistry": "polymer_physical_chemistry",
    "polymerization": "polymerization",
    "degree of polymerization": "degree_of_polymerization",
    "dp": "degree_of_polymerization",
    "molecular weight distribution": "molecular_weight_distribution",
    "mw distribution": "molecular_weight_distribution",
    "glass transition temperature": "glass_transition_temperature",
    "t_g": "glass_transition_temperature",
    "melting temperature": "melting_temperature",
    "t_m": "melting_temperature",

    # Chemical Equilibrium Thermodynamics
    "chemical equilibrium": "chemical_equilibrium",
    "equilibrium constant": "equilibrium_constant",
    "k_eq": "equilibrium_constant",
    "reaction quotient": "reaction_quotient",
    "q": "reaction_quotient",
    "le chatelier's principle": "le_chateliers_principle",
    "le chatelier principle": "le_chateliers_principle",
    "equilibrium thermodynamics": "chemical_equilibrium",

    # Real Gas Behavior
    "real gas behavior": "real_gas_behavior",
    "van der waals equation": "van_der_waals_equation",
    "vdw equation": "van_der_waals_equation",
    "compressibility factor": "compressibility_factor",
    "z factor": "compressibility_factor",
    "fugacity": "fugacity",
    "fugacity coefficient": "fugacity_coefficient",
    "non-ideal gas": "real_gas_behavior",
    "non ideal gas": "real_gas_behavior",

    # Additional synonyms and misspellings for coverage
    "thermodynamics first law": "first_law_of_thermodynamics",
    "thermodynamics second law": "second_law_of_thermodynamics",
    "gibbs free energy g": "gibbs_free_energy",
    "chemical potenial": "chemical_potential",
    "rate kinetics": "rate_law",
    "arrhenius eqn": "arrhenius_equation",
    "transition state theory tst": "transition_state_theory",
    "catalyst mechanism": "catalysis",
    "schrodinger wavefunction": "wavefunction",
    "molecular orbital theory mot": "molecular_orbital_theory",
    "hartree fock": "hartree_fock_method",
    "stat mech partition function": "partition_function",
    "adsorption isotherm langmuir": "langmuir_isotherm",
    "nernst eqn": "nernst_equation",
    "uv visible spectroscopy": "uv_vis_spectroscopy",
    "phase diagram triple point": "triple_point",
    "diffusion coefficient d": "diffusion_coefficient",
    "colligative property": "colligative_properties",
    "computational chem": "computational_chemistry",
    "photo chemistry": "photochemistry",
    "polymer chem": "polymer_physical_chemistry",
    "chemical equilibrium k": "equilibrium_constant",
    "real gas vdW": "van_der_waals_equation",

    # Extended entries for coverage and redundancy
    "internal energy": "first_law_of_thermodynamics",
    "enthalpy": "enthalpy",
    "h": "enthalpy",
    "delta h": "enthalpy",
    "dh": "enthalpy",
    "heat": "heat",
    "work": "work",
    "w": "work",
    "entropy s": "entropy",
    "delta entropy": "entropy",
    "gibbs function g": "gibbs_free_energy",
    "chemical pot": "chemical_potential",
    "reaction rate": "rate_law",
    "rate constant k": "rate_constant",
    "activation energy ea": "activation_energy",
    "frequency factor a": "pre_exponential_factor",
    "activated complex ac": "activated_complex",
    "reaction coordinate rc": "reaction_coordinate",
    "enzyme catalyst": "enzyme_catalysis",
    "heterogeneous catalyst": "heterogeneous_catalysis",
    "homogeneous catalyst": "homogeneous_catalysis",
    "hamiltonian h": "hamiltonian_operator",
    "wave function psi": "wavefunction",
    "bonding mo": "bonding_orbital",
    "antibonding mo": "antibonding_orbital",
    "nonbonding mo": "nonbonding_orbital",
    "hartree-fock scf": "hartree_fock_method",
    "partition func": "partition_function",
    "boltzmann dist": "boltzmann_distribution",
    "langmuir iso": "langmuir_isotherm",
    "freundlich iso": "freundlich_isotherm",
    "electrode pot": "electrode_potential",
    "standard electrode pot": "standard_electrode_potential",
    "cell pot": "cell_potential",
    "redox rxn": "redox_reaction",
    "uv-vis spec": "uv_vis_spectroscopy",
    "infrared spec": "infrared_spectroscopy",
    "nmr spec": "nmr_spectroscopy",
    "mass spec": "mass_spectrometry",
    "phase rule f": "degrees_of_freedom",
    "ficks law": "ficks_law",
    "ficks 1st law": "ficks_law",
    "ficks 2nd law": "ficks_second_law",
    "boiling point elev": "boiling_point_elevation",
    "freezing point depress": "freezing_point_depression",
    "osmotic press": "osmotic_pressure",
    "raoults law": "raoults_law",
    "ab initio": "ab_initio_methods",
    "density functional theory dft": "density_functional_theory",
    "molecular dynamics md": "molecular_dynamics",
    "monte carlo": "monte_carlo_simulation",
    "semi empirical": "semi_empirical_methods",
    "photo excitation": "photoexcitation",
    "glass transition temp": "glass_transition_temperature",
    "melting temp": "melting_temperature",
    "le chatelier": "le_chateliers_principle",
    "van der waals eq": "van_der_waals_equation",
    "compressibility z": "compressibility_factor",
    "fugacity coeff": "fugacity_coefficient",
    "non ideal gas behavior": "real_gas_behavior",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    hasher = hashlib.sha256()
    # Sort keys for consistent hash
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
    normalized = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == normalized]
    return sorted(set(related))

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)