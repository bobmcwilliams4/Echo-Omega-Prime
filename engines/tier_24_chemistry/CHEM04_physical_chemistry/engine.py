import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
CHEM04 Physical Chemistry Intelligence Engine
Port: 9054 | Version: 1.0.0
Domain: Thermodynamics, Kinetics, Quantum Chemistry, Statistical Mechanics, Surface Chemistry, Electrochemistry
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from loguru import logger
import hashlib
import json
from enum import Enum

# Configure logging
logger.add(
    "physical_chemistry_engine.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)

APP = FastAPI(
    title="CHEM04 Physical Chemistry Engine",
    version="1.0.0",
    description="Physical Chemistry domain intelligence with thermodynamics, kinetics, quantum chemistry"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DOMAIN MODELS
# ============================================================================

class ResponseMode(str, Enum):
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"

class ConfidenceLevel(str, Enum):
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"

class QueryRequest(BaseModel):
    query: str = Field(..., description="Physical chemistry question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default=None)

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrine_blocks_triggered: List[str]
    reasoning_chain: List[str]
    determinism_hash: str
    response_mode: ResponseMode
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE BLOCKS
# ============================================================================

class DoctrineBlock:
    def __init__(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: str,
        reasoning_framework: str,
        key_factors: List[str],
        primary_authority: List[str],
        confidence: ConfidenceLevel,
        equations: Optional[List[str]] = None,
        applications: Optional[List[str]] = None
    ):
        self.topic = topic
        self.keywords = [k.lower() for k in keywords]
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.equations = equations or []
        self.applications = applications or []
        self.trigger_count = 0
        self.last_triggered = None

    def matches(self, query: str) -> bool:
        query_lower = query.lower()
        return any(kw in query_lower for kw in self.keywords)

    def trigger(self) -> None:
        self.trigger_count += 1
        self.last_triggered = datetime.utcnow().isoformat()

# Initialize doctrine cache
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="First Law of Thermodynamics",
        keywords=["first law", "energy conservation", "internal energy", "delta u", "work heat"],
        conclusion_template="Energy is conserved: ΔU = Q - W where internal energy change equals heat absorbed minus work done by system.",
        reasoning_framework="""
The First Law establishes energy conservation in thermochemical systems:

1. Internal Energy (U): State function representing total molecular energy
   - Kinetic energy of molecular motion
   - Potential energy of molecular interactions
   - Electronic, vibrational, rotational contributions

2. Heat (Q): Energy transfer due to temperature difference
   - Sign convention: Q > 0 when heat flows into system
   - Path-dependent quantity (not state function)
   - Measured via calorimetry

3. Work (W): Energy transfer via mechanical processes
   - PV work: W = ∫P dV for expansion/compression
   - Sign convention: W > 0 when system does work on surroundings
   - Reversible vs irreversible work

4. Mathematical Form: ΔU = Q - W
   - Differential form: dU = δQ - δW
   - For ideal gas: ΔU depends only on temperature
   - Cyclic process: ΔU_cycle = 0, so Q = W

5. Applications:
   - Constant volume: ΔU = Q_v (no PV work)
   - Constant pressure: ΔH = Q_p (enthalpy)
   - Adiabatic: Q = 0, so ΔU = -W
        """,
        key_factors=[
            "System vs surroundings definition",
            "Sign conventions for Q and W",
            "State function vs path function",
            "Process type (isothermal, adiabatic, isobaric, isochoric)",
            "Ideal vs real gas behavior"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry (11th ed)",
            "Thermodynamics and Statistical Mechanics (Greiner)",
            "NIST Chemistry WebBook"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=["ΔU = Q - W", "dU = δQ - δW", "ΔU = nC_v ΔT"],
        applications=["Calorimetry", "Engine cycles", "Phase transitions"]
    ),

    DoctrineBlock(
        topic="Second Law and Entropy",
        keywords=["second law", "entropy", "delta s", "spontaneity", "carnot", "irreversible"],
        conclusion_template="Entropy increases in spontaneous processes: ΔS_universe > 0. Carnot efficiency η = 1 - T_c/T_h represents maximum work extraction.",
        reasoning_framework="""
The Second Law defines directionality of spontaneous processes via entropy:

1. Entropy (S): Measure of molecular disorder and energy dispersal
   - State function: ΔS independent of path
   - Statistical definition: S = k_B ln(Ω) where Ω = microstates
   - Units: J/(mol·K)

2. Second Law Statements:
   - Clausius: Heat cannot spontaneously flow from cold to hot
   - Kelvin: Cannot convert heat fully to work in cyclic process
   - Entropy: ΔS_universe ≥ 0 for any process
   - Equality holds only for reversible processes

3. Entropy Changes:
   - Reversible: ΔS = ∫(δQ_rev/T)
   - Irreversible: ΔS > Q/T (entropy produced > heat transferred)
   - Phase transition: ΔS_fus = ΔH_fus/T_m
   - Ideal gas: ΔS = nC_p ln(T_f/T_i) - nR ln(P_f/P_i)

4. Carnot Cycle:
   - Most efficient heat engine between two reservoirs
   - Efficiency: η = 1 - T_cold/T_hot
   - All reversible engines have same efficiency
   - Real engines: η_real < η_Carnot

5. Spontaneity Criterion:
   - ΔS_universe = ΔS_system + ΔS_surroundings > 0
   - At constant T,P: ΔG < 0 (Gibbs free energy)
   - At constant T,V: ΔA < 0 (Helmholtz free energy)
        """,
        key_factors=[
            "Reversible vs irreversible processes",
            "System entropy can decrease if surroundings increase more",
            "Third Law: S → 0 as T → 0 K for perfect crystal",
            "Temperature dependence of spontaneity",
            "Maximum work from heat source"
        ],
        primary_authority=[
            "Dill & Bromberg - Molecular Driving Forces",
            "Callen - Thermodynamics",
            "Atkins' Physical Chemistry"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "ΔS_universe = ΔS_sys + ΔS_surr ≥ 0",
            "η_Carnot = 1 - T_c/T_h",
            "S = k_B ln(Ω)"
        ],
        applications=["Heat engines", "Refrigeration", "Chemical equilibrium"]
    ),

    DoctrineBlock(
        topic="Gibbs Free Energy and Spontaneity",
        keywords=["gibbs", "free energy", "delta g", "spontaneity", "equilibrium constant"],
        conclusion_template="At constant T and P, spontaneous processes have ΔG < 0. Equilibrium occurs when ΔG = 0, related to K via ΔG° = -RT ln(K).",
        reasoning_framework="""
Gibbs free energy combines enthalpy and entropy for spontaneity at constant T,P:

1. Definition: G = H - TS
   - State function combining energy and entropy
   - Natural variables: T (temperature), P (pressure)
   - Most relevant for chemical reactions at atmospheric conditions

2. Spontaneity Criterion:
   - ΔG < 0: Spontaneous (exergonic)
   - ΔG = 0: Equilibrium
   - ΔG > 0: Non-spontaneous (endergonic)
   - ΔG = ΔH - TΔS at constant T

3. Temperature Dependence:
   - ΔH < 0, ΔS > 0: Spontaneous at all T (exothermic, entropy increase)
   - ΔH > 0, ΔS < 0: Non-spontaneous at all T
   - ΔH < 0, ΔS < 0: Spontaneous at low T (enthalpy-driven)
   - ΔH > 0, ΔS > 0: Spontaneous at high T (entropy-driven)

4. Standard Free Energy Change:
   - ΔG° = ΔH° - TΔS°
   - ΔG° = -RT ln(K_eq) where K = equilibrium constant
   - ΔG_rxn = ΔG° + RT ln(Q) where Q = reaction quotient

5. Applications:
   - Phase transitions: ΔG = 0 at T_transition
   - Solubility: ΔG_sol relates to K_sp
   - Electrochemistry: ΔG = -nFE
   - Biochemistry: Coupled reactions, ATP hydrolysis
        """,
        key_factors=[
            "Sign of ΔH and ΔS determines temperature dependence",
            "Standard state: 1 bar, 298 K, 1 M concentration",
            "Non-standard conditions require reaction quotient Q",
            "Le Chatelier's principle from ΔG analysis",
            "Maximum non-PV work available: w_max = ΔG"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry",
            "Levine - Physical Chemistry (6th ed)",
            "NIST Thermochemical Data"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "ΔG = ΔH - TΔS",
            "ΔG° = -RT ln(K)",
            "ΔG = ΔG° + RT ln(Q)"
        ],
        applications=["Reaction spontaneity", "Equilibrium constants", "Coupled reactions"]
    ),

    DoctrineBlock(
        topic="Chemical Potential",
        keywords=["chemical potential", "mu", "fugacity", "activity", "partial molar"],
        conclusion_template="Chemical potential μ_i = (∂G/∂n_i)_T,P,n_j defines driving force for mass transfer. Equilibrium occurs when μ_i is equal in all phases.",
        reasoning_framework="""
Chemical potential quantifies thermodynamic tendency of species to react or transfer:

1. Definition: μ_i = (∂G/∂n_i)_T,P,n_j
   - Partial molar Gibbs free energy
   - Intensive property (independent of system size)
   - Fundamental variable in phase and reaction equilibria

2. Physical Meaning:
   - Change in Gibbs energy per mole of species i added
   - Driving force for diffusion and reaction
   - Species flows from high μ to low μ
   - Equilibrium: μ_i^α = μ_i^β for all phases α,β

3. Ideal Solutions:
   - μ_i = μ_i° + RT ln(x_i) where x_i = mole fraction
   - Raoult's law: P_i = x_i P_i*
   - Valid for similar molecules (ideal mixing)

4. Non-Ideal Solutions:
   - μ_i = μ_i° + RT ln(a_i) where a_i = activity
   - Activity: a_i = γ_i x_i where γ_i = activity coefficient
   - Fugacity: f_i = φ_i P_i for gases (φ = fugacity coefficient)
   - Deviations from ideality due to molecular interactions

5. Phase Equilibria:
   - Two-phase: μ_i^liquid = μ_i^vapor
   - Clausius-Clapeyron: d ln(P)/dT = ΔH_vap/(RT²)
   - Gibbs phase rule: F = C - P + 2
        """,
        key_factors=[
            "Temperature and pressure dependence",
            "Standard state definition varies by phase",
            "Activity coefficients from experiment or models (UNIQUAC, NRTL)",
            "Electrochemical potential for charged species",
            "Gibbs-Duhem equation constrains partial molar properties"
        ],
        primary_authority=[
            "Smith, Van Ness & Abbott - Thermodynamics",
            "Prausnitz - Molecular Thermodynamics",
            "Atkins' Physical Chemistry"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "μ_i = μ_i° + RT ln(a_i)",
            "dμ_i = -S_m,i dT + V_m,i dP",
            "Σ x_i dμ_i = 0 (Gibbs-Duhem)"
        ],
        applications=["Phase diagrams", "Solubility", "Electrochemistry"]
    ),

    DoctrineBlock(
        topic="Rate Laws and Reaction Order",
        keywords=["rate law", "reaction order", "rate constant", "integrated rate", "half-life"],
        conclusion_template="Reaction rate v = k[A]^m[B]^n where m,n are orders (not necessarily stoichiometric coefficients). Rate constant k has temperature dependence via Arrhenius equation.",
        reasoning_framework="""
Rate laws quantify reaction kinetics empirically:

1. Differential Rate Law: v = -d[A]/dt = k[A]^m[B]^n
   - k = rate constant (units depend on overall order)
   - m, n = reaction orders (determined experimentally)
   - Overall order = m + n
   - Elementary reactions: orders match stoichiometry

2. Zero Order (m=0):
   - Rate: v = k (constant, independent of [A])
   - Integrated: [A] = [A]₀ - kt
   - Half-life: t₁/₂ = [A]₀/(2k)
   - Example: Surface-catalyzed reactions at saturation

3. First Order (m=1):
   - Rate: v = k[A]
   - Integrated: ln[A] = ln[A]₀ - kt
   - Half-life: t₁/₂ = ln(2)/k = 0.693/k (constant!)
   - Example: Radioactive decay, unimolecular decomposition

4. Second Order (m=2 or m=n=1):
   - Type A: v = k[A]² → 1/[A] = 1/[A]₀ + kt
   - Type B: v = k[A][B] (pseudo-first if [B] >> [A])
   - Half-life: t₁/₂ = 1/(k[A]₀) (inversely proportional to initial conc)
   - Example: Dimerization, bimolecular reactions

5. Determination Methods:
   - Initial rates: Vary [A] and [B], measure v₀
   - Integrated form: Plot [A] vs t, ln[A] vs t, 1/[A] vs t
   - Half-life method: Measure t₁/₂ at different [A]₀
        """,
        key_factors=[
            "Reaction order ≠ stoichiometric coefficient for complex mechanisms",
            "Units of k: (conc)^(1-n) time^(-1) for overall order n",
            "Temperature dependence via Arrhenius equation",
            "Pseudo-order approximation when one reactant in excess",
            "Reversible reactions approach equilibrium"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry - Kinetics chapters",
            "Laidler - Chemical Kinetics (3rd ed)",
            "Houston - Chemical Kinetics"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "v = k[A]^m[B]^n",
            "ln[A] = ln[A]₀ - kt (1st order)",
            "1/[A] = 1/[A]₀ + kt (2nd order)"
        ],
        applications=["Reaction mechanism determination", "Reactor design", "Shelf-life prediction"]
    ),

    DoctrineBlock(
        topic="Arrhenius Equation",
        keywords=["arrhenius", "activation energy", "frequency factor", "temperature kinetics"],
        conclusion_template="Temperature dependence of rate constant: k = A exp(-E_a/RT) where E_a is activation energy and A is pre-exponential factor.",
        reasoning_framework="""
Arrhenius equation quantifies temperature effect on reaction rates:

1. Arrhenius Form: k(T) = A exp(-E_a/RT)
   - A = pre-exponential factor (frequency factor)
   - E_a = activation energy (J/mol)
   - R = gas constant (8.314 J/(mol·K))
   - T = absolute temperature (K)

2. Physical Interpretation:
   - exp(-E_a/RT) = fraction of molecules with energy > E_a
   - A relates to collision frequency and orientation factor
   - Higher T → more molecules exceed barrier → faster reaction
   - E_a represents minimum energy for reaction to occur

3. Logarithmic Form: ln(k) = ln(A) - E_a/(RT)
   - Slope of ln(k) vs 1/T plot = -E_a/R
   - Intercept = ln(A)
   - Linearization allows experimental determination of E_a

4. Temperature Coefficient:
   - d ln(k)/dT = E_a/(RT²)
   - Rule of thumb: Rate doubles per 10°C increase (E_a ≈ 50 kJ/mol)
   - More accurate: k₂/k₁ = exp[E_a/R (1/T₁ - 1/T₂)]

5. Limitations and Extensions:
   - Valid over limited T ranges
   - Modified Arrhenius: k = A T^n exp(-E_a/RT)
   - Transition state theory provides theoretical basis
   - Quantum tunneling at low T deviates from Arrhenius
        """,
        key_factors=[
            "E_a always positive for forward reaction",
            "E_a,forward - E_a,reverse = ΔH_rxn",
            "A has units of k (depends on reaction order)",
            "Steric factor included in A for complex molecules",
            "Catalysts lower E_a, increasing k without changing ΔG"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry",
            "Laidler - Chemical Kinetics",
            "NIST Kinetics Database"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "k = A exp(-E_a/RT)",
            "ln(k) = ln(A) - E_a/(RT)",
            "k₂/k₁ = exp[E_a/R (1/T₁ - 1/T₂)]"
        ],
        applications=["Temperature control in reactors", "Shelf-life prediction", "Catalyst screening"]
    ),

    DoctrineBlock(
        topic="Transition State Theory",
        keywords=["transition state", "activated complex", "eyring", "rate theory", "enthalpy activation"],
        conclusion_template="TST: k = (k_B T/h) K‡ where K‡ is equilibrium constant for forming activated complex. Relates rate to ΔG‡, ΔH‡, ΔS‡.",
        reasoning_framework="""
Transition State Theory (Eyring equation) provides molecular interpretation of kinetics:

1. Fundamental Postulate:
   - Reactants in equilibrium with activated complex (‡)
   - A + B ⇌ [AB]‡ → Products
   - Activated complex crosses barrier at frequency k_B T/h
   - Transmission coefficient κ (usually ≈ 1)

2. Eyring Equation: k = κ (k_B T/h) exp(-ΔG‡/RT)
   - k_B = Boltzmann constant (1.381×10⁻²³ J/K)
   - h = Planck constant (6.626×10⁻³⁴ J·s)
   - ΔG‡ = Gibbs free energy of activation
   - κ accounts for recrossing and quantum effects

3. Thermodynamic Form:
   - ΔG‡ = ΔH‡ - TΔS‡
   - k = κ (k_B T/h) exp(ΔS‡/R) exp(-ΔH‡/RT)
   - Compare with Arrhenius: E_a ≈ ΔH‡ + RT
   - A ≈ (k_B T/h) exp(ΔS‡/R + 1)

4. Activation Parameters:
   - ΔH‡: Enthalpy of activation (bond breaking/forming)
   - ΔS‡: Entropy of activation (ordering in transition state)
   - ΔV‡: Volume of activation (from pressure dependence)
   - Negative ΔS‡: Tight, ordered transition state
   - Positive ΔS‡: Loose, dissociative transition state

5. Applications:
   - Solvent effects on reaction rates
   - Isotope effects (kinetic isotope effects, KIE)
   - Enzyme catalysis (lowering ΔG‡)
   - Theoretical calculation of rate constants
        """,
        key_factors=[
            "Quasi-equilibrium assumption may fail for very fast reactions",
            "ΔG‡ from computational chemistry (DFT, ab initio)",
            "Hammond postulate: TS resembles nearby state on energy surface",
            "Marcus theory for electron transfer reactions",
            "Tunneling significant for H-transfer at low T"
        ],
        primary_authority=[
            "Eyring - Theory of Rate Processes",
            "Atkins' Physical Chemistry",
            "Truhlar - Variational Transition State Theory"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "k = (k_B T/h) exp(-ΔG‡/RT)",
            "ΔG‡ = ΔH‡ - TΔS‡",
            "E_a = ΔH‡ + RT"
        ],
        applications=["Enzyme mechanisms", "Solvent effects", "Isotope effect prediction"]
    ),

    DoctrineBlock(
        topic="Catalysis Mechanisms",
        keywords=["catalyst", "catalysis", "enzyme", "heterogeneous", "michaelis-menten", "turnover"],
        conclusion_template="Catalysts accelerate reactions by providing alternate pathway with lower E_a. They do not change ΔG or equilibrium position, only kinetics.",
        reasoning_framework="""
Catalysis lowers activation energy without being consumed:

1. Homogeneous Catalysis:
   - Catalyst in same phase as reactants (solution)
   - Forms intermediate complex with reactants
   - Acid-base catalysis: Proton transfer mechanisms
   - Organometallic catalysis: Coordination chemistry

2. Heterogeneous Catalysis:
   - Catalyst in different phase (solid surface)
   - Steps: Adsorption → Surface reaction → Desorption
   - Langmuir-Hinshelwood: Both reactants adsorbed
   - Eley-Rideal: One reactant from gas phase
   - Industrial: Haber-Bosch (Fe), catalytic converters (Pt/Pd/Rh)

3. Enzyme Catalysis:
   - Biological catalysts with extreme specificity
   - Michaelis-Menten: E + S ⇌ ES → E + P
   - Rate: v = V_max [S]/(K_m + [S])
   - K_m = Michaelis constant (affinity measure)
   - k_cat = turnover number (max rate per enzyme)

4. Catalyst Characteristics:
   - Lower E_a for forward AND reverse reactions
   - Increase rate, not yield (ΔG unchanged)
   - Specificity: Reaction selectivity and enantioselectivity
   - Turnover number: Moles product per mole catalyst per time
   - Poison resistance: Tolerance to inhibitors

5. Kinetic Models:
   - Zero order in [S] when [S] >> K_m (saturation)
   - First order when [S] << K_m
   - Lineweaver-Burk: 1/v vs 1/[S] for parameter determination
   - Competitive/non-competitive/uncompetitive inhibition
        """,
        key_factors=[
            "Catalyst does not appear in overall stoichiometry",
            "May shift product distribution in competing pathways",
            "Surface area critical for heterogeneous catalysts",
            "Temperature limits for enzyme activity (denaturation)",
            "Catalyst regeneration in industrial processes"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry - Catalysis chapter",
            "Fersht - Structure and Mechanism in Protein Science",
            "Ertl - Handbook of Heterogeneous Catalysis"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "v = V_max [S]/(K_m + [S])",
            "k_cat = V_max/[E]_total",
            "1/v = (K_m/V_max)(1/[S]) + 1/V_max"
        ],
        applications=["Industrial ammonia synthesis", "Enzyme assays", "Drug metabolism"]
    ),

    DoctrineBlock(
        topic="Schrödinger Equation and Wavefunctions",
        keywords=["schrodinger", "wavefunction", "hamiltonian", "eigenvalue", "quantum mechanics"],
        conclusion_template="Time-independent Schrödinger equation Ĥψ = Eψ yields energy levels and wavefunctions for quantum systems. |ψ|² gives probability density.",
        reasoning_framework="""
Schrödinger equation is fundamental to quantum chemistry:

1. Time-Independent Form: Ĥψ(x) = Eψ(x)
   - Ĥ = Hamiltonian operator (total energy)
   - ψ = wavefunction (eigenfunction)
   - E = energy eigenvalue
   - For particle in 3D: Ĥ = -ℏ²/(2m)∇² + V(x,y,z)

2. Physical Interpretation:
   - ψ itself has no direct physical meaning
   - |ψ|² = probability density for finding particle
   - ∫|ψ|² dV = 1 (normalization condition)
   - Observables from operators: ⟨A⟩ = ∫ψ*Âψ dV

3. Postulates:
   - State described by wavefunction ψ
   - Observables represented by Hermitian operators
   - Measurement yields eigenvalue, collapses to eigenstate
   - Time evolution: iℏ ∂ψ/∂t = Ĥψ

4. Simple Systems:
   - Particle in 1D box: ψ_n = √(2/L) sin(nπx/L), E_n = n²h²/(8mL²)
   - Harmonic oscillator: E_n = ℏω(n + 1/2), ψ_n involves Hermite polynomials
   - Hydrogen atom: E_n = -13.6 eV/n², ψ_nlm(r,θ,φ) with quantum numbers n,l,m

5. Quantum Numbers:
   - n = principal (energy level): 1,2,3,...
   - l = angular momentum: 0,1,...,n-1 (s,p,d,f)
   - m_l = magnetic: -l,...,0,...,+l
   - m_s = spin: ±1/2 for electrons
        """,
        key_factors=[
            "Uncertainty principle: Δx Δp ≥ ℏ/2",
            "Superposition: ψ = Σ c_n ψ_n",
            "Tunneling through classically forbidden regions",
            "Degeneracy: Multiple states with same energy",
            "Pauli exclusion principle for fermions"
        ],
        primary_authority=[
            "Levine - Quantum Chemistry (7th ed)",
            "Atkins & Friedman - Molecular Quantum Mechanics",
            "Griffiths - Quantum Mechanics"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "Ĥψ = Eψ",
            "Ĥ = -ℏ²/(2m)∇² + V",
            "⟨A⟩ = ∫ψ*Âψ dV"
        ],
        applications=["Electronic structure", "Spectroscopy", "Chemical bonding"]
    ),

    DoctrineBlock(
        topic="Molecular Orbital Theory",
        keywords=["molecular orbital", "lcao", "bonding antibonding", "homo lumo", "pi bond"],
        conclusion_template="MO theory: Atomic orbitals combine linearly (LCAO) to form bonding and antibonding molecular orbitals. Bond order = (bonding e⁻ - antibonding e⁻)/2.",
        reasoning_framework="""
Molecular Orbital Theory describes electron distribution in molecules:

1. LCAO Approximation:
   - MO = Linear Combination of Atomic Orbitals
   - ψ_MO = c₁φ₁ + c₂φ₂ + ... + c_nφ_n
   - Variational principle minimizes energy
   - Number of MOs = Number of AOs combined

2. Bonding vs Antibonding:
   - Bonding MO: Constructive interference, electron density between nuclei
   - Antibonding MO: Destructive interference, node between nuclei
   - σ orbitals: Cylindrical symmetry along bond axis
   - π orbitals: Nodal plane containing bond axis

3. Energy Ordering (Homonuclear Diatomics):
   - Second period: σ_1s < σ*_1s < σ_2s < σ*_2s < σ_2p < π_2p < π*_2p < σ*_2p
   - Orbital mixing: s-p mixing affects order (O₂, F₂ differ from B₂, C₂, N₂)
   - Aufbau principle: Fill lowest energy orbitals first
   - Hund's rule: Maximize unpaired spins in degenerate orbitals

4. Bond Order and Properties:
   - Bond order = (N_bonding - N_antibonding)/2
   - Higher bond order → stronger, shorter bond
   - Magnetic properties: Paramagnetic if unpaired electrons (O₂)
   - Photoelectron spectroscopy measures orbital energies

5. Heteronuclear Diatomics:
   - Different atomic energies → unequal contributions
   - Polar bonds: MO weighted toward more electronegative atom
   - CO: Large energy gap prevents s-p mixing
        """,
        key_factors=[
            "Orbitals must have similar energy to mix effectively",
            "Symmetry matching required for overlap",
            "HOMO = highest occupied MO (electron donor)",
            "LUMO = lowest unoccupied MO (electron acceptor)",
            "Frontier orbital theory explains reactivity"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry - MO theory",
            "Albright, Burdett, Whangbo - Orbital Interactions in Chemistry",
            "Fleming - Molecular Orbitals and Organic Chemical Reactions"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "Bond order = (N_b - N_a)/2",
            "ψ_MO = Σ c_i φ_i",
            "ΔE = α - β for bonding/antibonding"
        ],
        applications=["Bond strength prediction", "Spectroscopy", "Reactivity analysis"]
    ),

    DoctrineBlock(
        topic="Hartree-Fock Method",
        keywords=["hartree-fock", "self-consistent field", "scf", "slater determinant", "basis set"],
        conclusion_template="HF method approximates many-electron wavefunction as Slater determinant, solving SCF equations iteratively. Captures ~99% of total energy but neglects electron correlation.",
        reasoning_framework="""
Hartree-Fock provides approximate solutions for many-electron systems:

1. Many-Electron Problem:
   - Exact solution impossible for N>2 electrons
   - Schrödinger equation: Ĥψ(r₁,...,r_N) = Eψ
   - Electron-electron repulsion prevents separation
   - Need approximation methods

2. HF Approximation:
   - Wavefunction as Slater determinant of spin orbitals
   - Each electron in mean field of others
   - Antisymmetric wavefunction (Pauli principle)
   - Variational method: Minimize energy

3. Self-Consistent Field:
   - Start with guess orbitals
   - Calculate effective potential from electron density
   - Solve Fock equations for new orbitals
   - Iterate until convergence (E change < threshold)
   - Converged orbitals define final wavefunction

4. Basis Sets:
   - Represent molecular orbitals as LCAO
   - Minimal basis: One basis function per AO (STO-3G)
   - Double-zeta: Two functions per AO (more flexible)
   - Polarization functions: Higher angular momentum (d,f)
   - Diffuse functions: Long-range tails (important for anions)

5. Limitations:
   - Neglects dynamic electron correlation
   - Overestimates bond energies, underestimates bond lengths
   - Post-HF methods: CI, MPPT, CC for correlation
   - DFT includes correlation via exchange-correlation functional
        """,
        key_factors=[
            "Restricted HF (closed-shell) vs unrestricted HF (open-shell)",
            "Roothaan equations for LCAO-MO-SCF",
            "Koopman's theorem: Orbital energies approximate ionization energies",
            "Basis set superposition error in weak interactions",
            "Correlation energy = E_exact - E_HF"
        ],
        primary_authority=[
            "Szabo & Ostlund - Modern Quantum Chemistry",
            "Jensen - Introduction to Computational Chemistry",
            "Levine - Quantum Chemistry"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "F̂φ_i = ε_i φ_i (Fock equation)",
            "F̂ = ĥ + Σ_j (Ĵ_j - K̂_j)",
            "E_HF = Σ_i ε_i - 1/2 Σ_ij (J_ij - K_ij)"
        ],
        applications=["Electronic structure calculations", "Molecular geometry optimization", "Spectroscopy prediction"]
    ),

    DoctrineBlock(
        topic="Statistical Mechanics Foundations",
        keywords=["partition function", "boltzmann distribution", "ensemble", "canonical", "microstate"],
        conclusion_framework="""
Statistical mechanics connects molecular properties to macroscopic thermodynamics:

1. Ensembles:
   - Microcanonical (NVE): Isolated system, fixed energy
   - Canonical (NVT): Constant T via heat reservoir
   - Grand canonical (μVT): Constant chemical potential
   - Isothermal-isobaric (NPT): Constant T and P

2. Boltzmann Distribution:
   - Probability of state i: P_i = exp(-E_i/k_B T)/Q
   - Q = partition function = Σ_i exp(-E_i/k_B T)
   - Most probable distribution for canonical ensemble
   - Foundation of equilibrium statistical mechanics

3. Partition Function:
   - Q = Σ_i g_i exp(-E_i/k_B T) where g_i = degeneracy
   - Molecular: q = q_trans × q_rot × q_vib × q_elec
   - Thermodynamic properties from Q:
     * Helmholtz free energy: A = -k_B T ln(Q)
     * Internal energy: U = k_B T² (∂ln(Q)/∂T)_V
     * Entropy: S = k_B ln(Q) + U/T
     * Pressure: P = k_B T (∂ln(Q)/∂V)_T

4. Molecular Partition Functions:
   - Translational: q_trans = (2πmk_B T/h²)^(3/2) V
   - Rotational: q_rot = T/σΘ_rot (linear), (π/σ)^(1/2) (T³/Θ_A Θ_B Θ_C)^(1/2) (nonlinear)
   - Vibrational: q_vib = 1/(1 - exp(-Θ_vib/T)) per mode
   - Electronic: q_elec ≈ g₀ if excited states high energy

5. Applications:
   - Ideal gas law from translational partition function
   - Heat capacity from energy level spacing
   - Chemical equilibrium from partition function ratios
        """,
        conclusion_template="Partition function Q = Σ exp(-E_i/k_BT) connects molecular energy levels to macroscopic thermodynamic properties via A = -k_BT ln(Q).",
        key_factors=[
            "Distinguishability: Q_N = q^N/N! for identical particles",
            "Temperature regimes: Classical (high T) vs quantum (low T)",
            "Characteristic temperatures: Θ_rot, Θ_vib, Θ_elec",
            "Zero-point energy contributes to absolute values",
            "Maxwell-Boltzmann distribution for molecular speeds"
        ],
        primary_authority=[
            "McQuarrie - Statistical Mechanics",
            "Hill - Introduction to Statistical Thermodynamics",
            "Atkins' Physical Chemistry"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "Q = Σ exp(-E_i/k_B T)",
            "A = -k_B T ln(Q)",
            "P_i = exp(-E_i/k_B T)/Q"
        ],
        applications=["Heat capacity calculation", "Chemical equilibrium", "Gas properties"]
    ),

    DoctrineBlock(
        topic="Adsorption Isotherms",
        keywords=["adsorption", "langmuir", "bet", "surface coverage", "isotherm"],
        conclusion_template="Langmuir isotherm θ = KP/(1+KP) assumes monolayer adsorption with no lateral interactions. BET extends to multilayer adsorption for surface area measurement.",
        reasoning_framework="""
Adsorption isotherms describe gas-surface interactions:

1. Langmuir Isotherm:
   - Assumptions: Monolayer, equivalent sites, no interactions
   - Derivation from equilibrium: A(g) + S ⇌ A-S
   - Coverage: θ = V/V_m = KP/(1+KP)
   - K = adsorption equilibrium constant = k_ads/k_des
   - Linear form: P/V = P/V_m + 1/(KV_m)

2. BET Isotherm (Brunauer-Emmett-Teller):
   - Multilayer adsorption model
   - Each layer follows Langmuir-type equilibrium
   - BET equation: 1/[V(P₀/P - 1)] = 1/(V_m C) + (C-1)/(V_m C) × P/P₀
   - C = exp[(E₁-E_L)/RT] where E₁ = first layer, E_L = liquefaction
   - Surface area: S = V_m N_A σ where σ = molecular cross-section

3. Freundlich Isotherm:
   - Empirical: V = K P^(1/n)
   - Heterogeneous surface energies
   - Common for solution adsorption
   - No saturation limit (non-physical at high P)

4. Experimental Determination:
   - Gas adsorption apparatus (volumetric or gravimetric)
   - Nitrogen at 77 K for surface area (BET)
   - Pressure range: 0.05 < P/P₀ < 0.35 for BET
   - Desorption hysteresis indicates pore structure

5. Surface Area Calculation:
   - From V_m (monolayer volume at STP)
   - σ_N₂ = 16.2 Ų at 77 K
   - Specific surface area: m²/g
   - Mesoporous materials: 2-50 nm pores
        """,
        key_factors=[
            "Langmuir assumes energetically equivalent sites",
            "BET valid in limited pressure range (0.05-0.35 P/P₀)",
            "Type I-V isotherms classified by shape",
            "Chemisorption vs physisorption (stronger vs weaker)",
            "Temperature dependence from thermodynamic parameters"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry - Surface chemistry",
            "Adamson & Gast - Physical Chemistry of Surfaces",
            "Brunauer et al. - J. Am. Chem. Soc. (1938) BET paper"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "θ = KP/(1+KP) (Langmuir)",
            "1/[V(P₀/P-1)] = 1/(V_m C) + (C-1)P/(V_m C P₀) (BET)",
            "S = V_m N_A σ"
        ],
        applications=["Catalyst surface area", "Gas storage materials", "Porous material characterization"]
    ),

    DoctrineBlock(
        topic="Electrochemistry and Nernst Equation",
        keywords=["nernst", "electrode potential", "electrochemical cell", "standard potential", "redox"],
        conclusion_template="Nernst equation E = E° - (RT/nF) ln(Q) relates cell potential to concentration. Standard potential E° determines spontaneity via ΔG° = -nFE°.",
        reasoning_framework="""
Electrochemistry links electron transfer to thermodynamics:

1. Electrochemical Cells:
   - Galvanic (voltaic): Spontaneous, generates current (battery)
   - Electrolytic: Non-spontaneous, requires external voltage
   - Half-cells: Oxidation at anode, reduction at cathode
   - Salt bridge maintains charge neutrality

2. Standard Electrode Potentials:
   - E° measured vs Standard Hydrogen Electrode (SHE)
   - SHE: 2H⁺ + 2e⁻ → H₂, E° = 0.00 V by definition
   - Reduction potentials tabulated
   - Cell potential: E°_cell = E°_cathode - E°_anode
   - Positive E°_cell → spontaneous reaction

3. Nernst Equation:
   - General form: E = E° - (RT/nF) ln(Q)
   - At 25°C: E = E° - (0.0592 V/n) log₁₀(Q)
   - Q = reaction quotient ([products]/[reactants])
   - At equilibrium: E = 0, so E° = (RT/nF) ln(K)

4. Thermodynamic Relations:
   - ΔG = -nFE (free energy change)
   - ΔG° = -nFE° (standard free energy)
   - ΔS = nF(∂E/∂T)_P (entropy from temperature dependence)
   - ln(K) = nFE°/(RT) (equilibrium constant)

5. Concentration Cells:
   - Same electrode materials, different concentrations
   - E = (RT/nF) ln(c₂/c₁)
   - Used in pH electrodes, ion-selective electrodes
        """,
        key_factors=[
            "F = Faraday constant = 96,485 C/mol e⁻",
            "Activity vs concentration in Nernst equation",
            "Reference electrodes: SHE, Ag/AgCl, calomel",
            "Junction potentials at liquid-liquid interfaces",
            "Overpotential in electrochemical kinetics"
        ],
        primary_authority=[
            "Bard & Faulkner - Electrochemical Methods",
            "Atkins' Physical Chemistry - Electrochemistry",
            "Standard Electrode Potentials (IUPAC)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "E = E° - (RT/nF) ln(Q)",
            "ΔG° = -nFE°",
            "E°_cell = E°_cathode - E°_anode"
        ],
        applications=["Battery design", "Corrosion prediction", "Analytical chemistry"]
    ),

    DoctrineBlock(
        topic="Spectroscopy Fundamentals",
        keywords=["beer-lambert", "absorbance", "transition", "selection rule", "spectroscopy"],
        conclusion_template="Beer-Lambert law A = εbc relates absorbance to concentration. Selection rules (Δl = ±1, ΔS = 0, etc.) determine allowed transitions.",
        reasoning_framework="""
Spectroscopy probes molecular energy levels via electromagnetic radiation:

1. Beer-Lambert Law:
   - A = log₁₀(I₀/I) = εbc
   - A = absorbance (dimensionless)
   - ε = molar absorptivity (L mol⁻¹ cm⁻¹)
   - b = path length (cm)
   - c = concentration (mol/L)
   - Transmittance: T = I/I₀ = 10^(-A)

2. Selection Rules:
   - Electric dipole approximation (most transitions)
   - Rotational: ΔJ = ±1 (permanent dipole required)
   - Vibrational: Δv = ±1 (harmonic oscillator), change in dipole moment
   - Electronic: ΔL = ±1, ΔS = 0 (spin forbidden), Laporte (g↔u)
   - Allowed transitions have large ε (~10⁴-10⁵)
   - Forbidden transitions weak or absent

3. Types of Spectroscopy:
   - UV-Vis: Electronic transitions (π→π*, n→π*)
   - IR: Vibrational transitions (bond stretching/bending)
   - Raman: Inelastic scattering, different selection rules
   - NMR: Nuclear spin transitions
   - Microwave: Rotational transitions
   - X-ray: Core electron excitation

4. Line Broadening:
   - Natural: Heisenberg uncertainty ΔE Δt ≥ ℏ/2
   - Doppler: Thermal motion of molecules
   - Pressure (collision): Shortened excited state lifetime
   - Inhomogeneous: Distribution of local environments

5. Instrumentation:
   - Single-beam vs double-beam
   - Monochromators: Prism, grating, interferometer (FTIR)
   - Detectors: PMT, CCD, photodiode
   - Resolution: Ability to distinguish close peaks
        """,
        key_factors=[
            "Deviations from Beer-Lambert at high concentration",
            "Stray light causes nonlinearity",
            "Solvent absorption must be subtracted (blank)",
            "Chromophore = light-absorbing functional group",
            "Coupling of vibrational and rotational transitions"
        ],
        primary_authority=[
            "Atkins & de Paula - Physical Chemistry",
            "Hollas - Modern Spectroscopy",
            "Bernath - Spectra of Atoms and Molecules"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "A = εbc",
            "ΔE = hν = hc/λ",
            "Selection rules: ΔJ=±1, Δv=±1, ΔS=0"
        ],
        applications=["Concentration determination", "Molecular structure", "Kinetics monitoring"]
    ),

    DoctrineBlock(
        topic="Phase Diagrams and Phase Rule",
        keywords=["phase diagram", "phase rule", "triple point", "critical point", "gibbs phase"],
        conclusion_template="Gibbs phase rule F = C - P + 2 determines degrees of freedom. Phase diagrams map stability regions in T-P or T-composition space.",
        reasoning_framework="""
Phase diagrams represent equilibrium between phases:

1. Gibbs Phase Rule: F = C - P + 2
   - F = degrees of freedom (intensive variables that can vary independently)
   - C = number of components
   - P = number of phases in equilibrium
   - 2 accounts for T and P as variables
   - Single component: F = 3 - P

2. One-Component Phase Diagrams:
   - P-T diagram: Triple point (3 phases, F=0), critical point (F=1)
   - Slope of phase boundaries: Clapeyron equation
   - Supercritical region: T > T_c, P > P_c, no phase boundary
   - Water anomaly: dP/dT < 0 for solid-liquid (ice less dense)

3. Clapeyron Equation:
   - dP/dT = ΔH/(T ΔV)
   - Relates slope of coexistence curve to enthalpy and volume change
   - Clausius-Clapeyron (gas-liquid): d ln(P)/dT = ΔH_vap/(RT²)
   - Integrated form: ln(P₂/P₁) = -(ΔH_vap/R)(1/T₂ - 1/T₁)

4. Binary Phase Diagrams:
   - T-x diagrams at constant P (or P-x at constant T)
   - Eutectic: Lowest melting T for mixture
   - Peritectic: Solid reacts with liquid to form new solid
   - Azeotrope: Constant boiling composition (vapor = liquid)
   - Lever rule: Determine phase amounts in two-phase region

5. Lever Rule:
   - In two-phase region: n_α/n_β = (x_β - x_overall)/(x_overall - x_α)
   - Ratio of phase amounts from distances on tie line
   - Conservation of mass constraint
        """,
        key_factors=[
            "Intensive vs extensive variables",
            "Metastable phases (supercooled liquid)",
            "Incongruent melting in complex systems",
            "Ideal vs non-ideal solution behavior",
            "Ternary diagrams use triangular coordinates"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry - Phase diagrams",
            "West - Solid State Chemistry",
            "Hillert - Phase Equilibria, Phase Diagrams and Phase Transformations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "F = C - P + 2",
            "dP/dT = ΔH/(T ΔV)",
            "d ln(P)/dT = ΔH_vap/(RT²)"
        ],
        applications=["Alloy design", "Distillation", "Materials processing"]
    ),

    DoctrineBlock(
        topic="Diffusion and Transport Phenomena",
        keywords=["diffusion", "fick's law", "viscosity", "conductivity", "transport"],
        conclusion_template="Fick's first law J = -D(dc/dx) describes diffusion flux. Diffusion coefficient D relates to viscosity via Stokes-Einstein D = k_BT/(6πηr).",
        reasoning_framework="""
Transport phenomena describe irreversible processes:

1. Fick's Laws of Diffusion:
   - First law: J = -D(dc/dx)
     * J = flux (mol m⁻² s⁻¹)
     * D = diffusion coefficient (m² s⁻¹)
     * Negative sign: Flux down concentration gradient
   - Second law: ∂c/∂t = D(∂²c/∂x²)
     * Time evolution of concentration profile
     * Solution methods: Separation of variables, Laplace transform

2. Stokes-Einstein Relation:
   - D = k_B T/(6πηr)
   - Links diffusion to viscosity η and particle radius r
   - Valid for spherical particles in continuum solvent
   - Hydrodynamic radius from D measurement

3. Viscosity:
   - Resistance to flow, units: Pa·s (SI) or poise (cgs)
   - Newtonian fluid: τ = η(dv/dy) (shear stress ∝ shear rate)
   - Non-Newtonian: Shear-thinning, shear-thickening
   - Temperature dependence: η ∝ exp(E_a/RT) (Arrhenius-like)

4. Electrical Conductivity:
   - Κ = Σ_i z_i² F² D_i c_i / RT (Nernst-Einstein)
   - Molar conductivity: Λ_m = Κ/c
   - Kohlrausch's law: Λ_m = Λ°_m - K√c (weak electrolytes)
   - Limiting molar conductivity Λ°_m = ν₊λ°₊ + ν₋λ°₋

5. Thermal Conductivity:
   - Fourier's law: q = -k(dT/dx)
   - k = thermal conductivity (W m⁻¹ K⁻¹)
   - Kinetic theory for gases: k ∝ c_v √T (temperature dependence)
        """,
        key_factors=[
            "Einstein relation: D = μk_BT where μ = mobility",
            "Anomalous diffusion in crowded/confined systems",
            "Molecular dynamics simulations predict D",
            "Onsager reciprocal relations for coupled transport",
            "Knudsen diffusion in nanopores"
        ],
        primary_authority=[
            "Bird, Stewart, Lightfoot - Transport Phenomena",
            "Atkins' Physical Chemistry",
            "Cussler - Diffusion: Mass Transfer in Fluid Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "J = -D(dc/dx)",
            "D = k_B T/(6πηr)",
            "Κ = Σ z_i² F² D_i c_i / RT"
        ],
        applications=["Drug delivery", "Membrane separation", "Electrochemical devices"]
    ),

    DoctrineBlock(
        topic="Colligative Properties",
        keywords=["colligative", "boiling point elevation", "freezing point depression", "osmotic pressure", "vapor pressure lowering"],
        conclusion_template="Colligative properties depend on solute concentration, not identity: ΔT_b = K_b m, ΔT_f = K_f m, Π = MRT. Raoult's law P_A = x_A P°_A for ideal solutions.",
        reasoning_framework="""
Colligative properties arise from entropy of mixing:

1. Vapor Pressure Lowering:
   - Raoult's law (ideal): P_A = x_A P°_A
   - Solvent vapor pressure decreases with solute
   - ΔP = P°_A - P_A = x_B P°_A
   - Non-volatile solute assumed
   - Henry's law for solute if volatile: P_B = k_H x_B

2. Boiling Point Elevation:
   - ΔT_b = T_b - T°_b = K_b m
   - K_b = ebullioscopic constant (solvent-specific)
   - m = molality (mol solute / kg solvent)
   - Origin: Vapor pressure lowering shifts T_b upward
   - K_b = RT°_b² M_A / (1000 ΔH_vap)

3. Freezing Point Depression:
   - ΔT_f = T°_f - T_f = K_f m
   - K_f = cryoscopic constant (larger than K_b typically)
   - Used for molecular weight determination
   - K_f = RT°_f² M_A / (1000 ΔH_fus)
   - Assumes pure solvent freezes out

4. Osmotic Pressure:
   - Π = MRT (van 't Hoff equation)
   - M = molarity of solute
   - Most sensitive colligative property (largest effect)
   - Reverse osmosis for desalination
   - Important in biological systems (cell membranes)

5. van 't Hoff Factor:
   - i = actual particles / formula units
   - Ionic compounds: i > 1 (NaCl: i ≈ 2, CaCl₂: i ≈ 3)
   - Modified equations: ΔT_f = i K_f m, Π = i MRT
   - Ion pairing reduces effective i
        """,
        key_factors=[
            "Ideal solution assumptions (Raoult's law)",
            "Non-ideal: Activity coefficients needed",
            "Molality preferred (temperature-independent)",
            "Electrolyte solutions require Debye-Hückel theory",
            "Biomolecule molecular weight from osmometry"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry",
            "Levine - Physical Chemistry",
            "Laidler & Meiser - Physical Chemistry"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "ΔT_b = K_b m",
            "ΔT_f = K_f m",
            "Π = MRT"
        ],
        applications=["Molecular weight determination", "Antifreeze", "Desalination"]
    ),

    DoctrineBlock(
        topic="Computational Chemistry Methods",
        keywords=["dft", "density functional", "ab initio", "computational chemistry", "gaussian"],
        conclusion_template="DFT (Density Functional Theory) and ab initio methods (HF, MP2, CCSD) compute molecular properties from first principles. DFT scales better (N³) than correlated ab initio (N⁵-N⁷).",
        reasoning_framework="""
Computational chemistry calculates molecular properties without experiments:

1. Hierarchy of Methods:
   - Molecular mechanics: Classical force fields (MM3, AMBER, CHARMM)
   - Semi-empirical: Simplified quantum (AM1, PM3, MNDO)
   - Ab initio: First principles quantum (HF, MP2, CCSD)
   - DFT: Electron density-based quantum method
   - Higher accuracy: CCSD(T) "gold standard" for small molecules

2. Density Functional Theory:
   - Energy functional: E[ρ] = T[ρ] + V[ρ] + J[ρ] + E_xc[ρ]
   - Exchange-correlation functional approximations:
     * LDA: Local Density Approximation
     * GGA: Generalized Gradient (BLYP, PBE)
     * Hybrid: Partial exact exchange (B3LYP, PBE0)
     * Meta-GGA: TPSS, M06
   - Kohn-Sham equations solved self-consistently
   - Scales as N³, feasible for 100+ atoms

3. Post-Hartree-Fock Methods:
   - MP2: Møller-Plesset 2nd order perturbation
   - CI: Configuration Interaction
   - CCSD: Coupled Cluster Singles Doubles
   - CCSD(T): Adds perturbative triples, most accurate
   - Scaling: MP2 ~N⁵, CCSD ~N⁶, CCSD(T) ~N⁷
   - Size-extensivity: CCSD yes, CI no

4. Basis Sets:
   - Minimal: STO-3G (fast, inaccurate)
   - Split-valence: 6-31G, 6-311G
   - Polarization: 6-31G*, 6-31G**
   - Diffuse: 6-31+G, aug-cc-pVDZ
   - Correlation-consistent: cc-pVDZ, cc-pVTZ, cc-pVQZ
   - Complete basis set (CBS) extrapolation

5. Applications:
   - Geometry optimization
   - Vibrational frequencies (IR, Raman prediction)
   - Reaction barriers and transition states
   - Excited states (TD-DFT, CASSCF, EOM-CC)
   - NMR chemical shifts
        """,
        key_factors=[
            "DFT functional choice critical (no systematic improvability)",
            "Dispersion corrections (DFT-D3, wB97X-D) for van der Waals",
            "Implicit solvation (PCM, COSMO) for solution phase",
            "Thermochemical corrections (zero-point, thermal)",
            "Software: Gaussian, ORCA, Q-Chem, Psi4, NWChem"
        ],
        primary_authority=[
            "Cramer - Essentials of Computational Chemistry",
            "Jensen - Introduction to Computational Chemistry",
            "Parr & Yang - Density-Functional Theory of Atoms and Molecules"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "E[ρ] = T[ρ] + V_ext[ρ] + J[ρ] + E_xc[ρ]",
            "F̂_KS φ_i = ε_i φ_i",
            "E_MP2 = -Σ_ijab (ia|jb)[2(ia|jb) - (ib|ja)]/(ε_i+ε_j-ε_a-ε_b)"
        ],
        applications=["Drug design", "Catalysis", "Materials discovery"]
    ),

    DoctrineBlock(
        topic="Photochemistry Principles",
        keywords=["photochemistry", "excited state", "fluorescence", "phosphorescence", "jablonski"],
        conclusion_template="Photochemistry: Absorption → S₁/T₁ excited states → reactions or relaxation. Fluorescence (S₁→S₀, fast) vs phosphorescence (T₁→S₀, slow, spin-forbidden).",
        reasoning_framework="""
Photochemistry involves chemical reactions initiated by light absorption:

1. Jablonski Diagram:
   - Ground state: S₀ (singlet)
   - Excited singlet: S₁, S₂, ... (spin-paired electrons)
   - Excited triplet: T₁, T₂, ... (unpaired spins)
   - Absorption: S₀ → S_n (10⁻¹⁵ s, vertical transition)
   - Internal conversion: S_n → S₁ (fast, non-radiative)

2. Radiative Processes:
   - Fluorescence: S₁ → S₀ + hν
     * Spin-allowed, fast (10⁻⁹ to 10⁻⁶ s)
     * Stokes shift: λ_em > λ_abs (vibrational relaxation)
     * Quantum yield Φ_f = photons emitted / photons absorbed
   - Phosphorescence: T₁ → S₀ + hν
     * Spin-forbidden, slow (10⁻³ to 10² s)
     * Longer wavelength than fluorescence
     * Enhanced by heavy atoms (spin-orbit coupling)

3. Non-Radiative Processes:
   - Vibrational relaxation: S₁(v=n) → S₁(v=0) (~10⁻¹² s)
   - Internal conversion (IC): S_n → S_m (isoenergetic)
   - Intersystem crossing (ISC): S₁ → T₁ (spin flip)
   - Quenching: Energy transfer to other molecules

4. Photochemical Reactions:
   - Excited states have different reactivity than S₀
   - Norrish Type I: α-cleavage of carbonyl
   - Norrish Type II: γ-hydrogen abstraction
   - [2+2] Cycloaddition: Woodward-Hoffmann forbidden in ground state
   - Quantum yield: Φ = moles product / einsteins absorbed

5. Energy Transfer:
   - Förster (FRET): Dipole-dipole, 1-10 nm range
   - Dexter: Requires orbital overlap, short range
   - Sensitization: Donor* + Acceptor → Donor + Acceptor*
        """,
        key_factors=[
            "Kasha's rule: Emission typically from S₁ or T₁ only",
            "El-Sayed rules: ISC efficient for n→π* transitions",
            "Oxygen quenches T₁ (produces singlet oxygen ¹O₂)",
            "Photosensitizers for photodynamic therapy",
            "Stern-Volmer equation for quenching kinetics"
        ],
        primary_authority=[
            "Turro et al. - Modern Molecular Photochemistry",
            "Atkins' Physical Chemistry - Photochemistry",
            "Klan & Wirz - Photochemistry of Organic Compounds"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "Φ = moles product / einsteins absorbed",
            "k_ISC / k_IC ∝ ⟨S₁|Ĥ_SO|T₁⟩²",
            "I₀/I = 1 + K_SV [Q] (Stern-Volmer)"
        ],
        applications=["Photodynamic therapy", "Solar cells", "Vision biochemistry"]
    ),

    DoctrineBlock(
        topic="Polymer Physical Chemistry",
        keywords=["polymer", "molecular weight distribution", "glass transition", "viscosity polymer", "flory"],
        conclusion_template="Polymers: M_n (number average) and M_w (weight average) characterize molecular weight distribution. Glass transition T_g separates rubbery and glassy states.",
        reasoning_framework="""
Polymer physical chemistry addresses macromolecules:

1. Molecular Weight Averages:
   - Number average: M_n = Σ N_i M_i / Σ N_i
   - Weight average: M_w = Σ w_i M_i / Σ w_i = Σ N_i M_i² / Σ N_i M_i
   - Polydispersity index: PDI = M_w/M_n ≥ 1
   - PDI = 1: Monodisperse, PDI > 2: Broad distribution
   - Measurement: GPC (size exclusion chromatography)

2. Solution Properties:
   - Intrinsic viscosity: [η] = lim(c→0) (η_sp/c)
   - Mark-Houwink equation: [η] = K M^a
   - Flory-Huggins theory: Solution thermodynamics
   - Theta solvent: Excluded volume cancels, ideal coil
   - Good solvent: Coil expands, poor solvent: Coil contracts

3. Glass Transition (T_g):
   - Rubbery → glassy, 2nd order transition
   - Below T_g: Frozen chain motion, brittle
   - Above T_g: Segmental motion, elastomeric
   - Factors: Chain flexibility, side groups, crosslinking
   - Measurement: DSC, DMA, dilatometry

4. Crystallinity:
   - Semi-crystalline: Crystalline and amorphous regions
   - Degree of crystallinity: X_c = ΔH_m / ΔH_m°
   - Spherulites: Radial lamellar structures
   - Melting temperature T_m > T_g
   - Tacticity: Isotactic, syndiotactic, atactic

5. Viscoelasticity:
   - Time-dependent mechanical properties
   - Creep: Strain increases under constant stress
   - Stress relaxation: Stress decreases under constant strain
   - Maxwell model: Spring + dashpot in series
   - Voigt model: Spring + dashpot in parallel
        """,
        key_factors=[
            "Degree of polymerization DP = M/M_0",
            "End-to-end distance R ∝ N^(1/2) (random coil)",
            "Williams-Landel-Ferry (WLF) equation for T_g shift",
            "Crosslinking prevents flow, increases T_g",
            "Molecular weight distribution from step-growth vs chain-growth"
        ],
        primary_authority=[
            "Flory - Principles of Polymer Chemistry",
            "Hiemenz & Lodge - Polymer Chemistry",
            "Rubinstein & Colby - Polymer Physics"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "M_w/M_n = PDI",
            "[η] = K M^a",
            "log(a_T) = -C₁(T-T_g)/(C₂+T-T_g) (WLF)"
        ],
        applications=["Polymer synthesis", "Material selection", "Rheology"]
    ),

    DoctrineBlock(
        topic="Chemical Equilibrium Thermodynamics",
        keywords=["equilibrium constant", "reaction quotient", "le chatelier", "temperature equilibrium"],
        conclusion_template="Equilibrium constant K = exp(-ΔG°/RT) relates to standard free energy. Le Chatelier's principle: System shifts to counteract stress.",
        reasoning_framework="""
Chemical equilibrium from thermodynamic principles:

1. Equilibrium Constant:
   - General reaction: aA + bB ⇌ cC + dD
   - K = ([C]^c [D]^d) / ([A]^a [B]^b) at equilibrium
   - K_p for gases (partial pressures), K_c for concentrations
   - Relation: K_p = K_c (RT)^Δn where Δn = change in moles gas
   - Activities: K = (a_C^c a_D^d)/(a_A^a a_B^b) (exact)

2. Thermodynamic Relations:
   - ΔG° = -RT ln(K)
   - ΔG = ΔG° + RT ln(Q) where Q = reaction quotient
   - Spontaneity: ΔG < 0 when Q < K (forward), ΔG > 0 when Q > K (reverse)
   - At equilibrium: ΔG = 0, Q = K

3. Temperature Dependence:
   - van 't Hoff equation: d ln(K)/dT = ΔH°/(RT²)
   - Integrated: ln(K₂/K₁) = -(ΔH°/R)(1/T₂ - 1/T₁)
   - Exothermic (ΔH° < 0): K decreases with T
   - Endothermic (ΔH° > 0): K increases with T

4. Le Chatelier's Principle:
   - Add reactant: Shift right (toward products)
   - Add product: Shift left (toward reactants)
   - Increase T: Favor endothermic direction
   - Increase P: Shift toward fewer moles of gas
   - Catalyst: No effect on K, only on approach to equilibrium

5. Pressure Effects:
   - K_p independent of total pressure (standard state 1 bar)
   - Mole fractions shift with pressure change
   - Δn > 0: High P favors reactants
   - Δn < 0: High P favors products
        """,
        key_factors=[
            "Standard state: 1 bar for gases, 1 M for solutions",
            "Pure solids and liquids: Activity = 1, not in K expression",
            "Heterogeneous equilibria involve multiple phases",
            "Coupling endergonic reactions to exergonic (ATP in biology)",
            "Kinetic vs thermodynamic control"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry",
            "Levine - Physical Chemistry",
            "NIST Thermochemical Tables"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "ΔG° = -RT ln(K)",
            "ln(K₂/K₁) = -(ΔH°/R)(1/T₂-1/T₁)",
            "ΔG = ΔG° + RT ln(Q)"
        ],
        applications=["Ammonia synthesis", "Acid-base equilibria", "Solubility products"]
    ),

    DoctrineBlock(
        topic="Real Gas Behavior",
        keywords=["van der waals", "real gas", "compressibility factor", "virial", "fugacity"],
        conclusion_template="Real gases deviate from PV=nRT. Van der Waals equation (P + a/V²)(V - b) = RT accounts for intermolecular forces (a) and molecular volume (b).",
        reasoning_framework="""
Real gas equations of state correct for non-ideality:

1. Compressibility Factor:
   - Z = PV/(nRT) = Vm/Vm,ideal
   - Ideal gas: Z = 1 at all T, P
   - Z < 1: Attractive forces dominate (low T)
   - Z > 1: Repulsive forces dominate (high P, small V)
   - Boyle temperature T_B: Z = 1 over wide P range

2. Van der Waals Equation:
   - (P + a n²/V²)(V - nb) = nRT
   - a: Intermolecular attraction parameter
   - b: Excluded volume per mole
   - Reduces to ideal gas when a,b → 0
   - Critical point: (∂P/∂V)_T = 0 and (∂²P/∂V²)_T = 0

3. Critical Constants:
   - T_c = 8a/(27Rb), P_c = a/(27b²), V_c = 3b
   - Law of corresponding states: Z = f(T_r, P_r)
   - T_r = T/T_c (reduced temperature)
   - P_r = P/P_c (reduced pressure)
   - Universal compressibility charts

4. Virial Equation:
   - PV = RT(1 + B/V + C/V² + ...)
   - B = 2nd virial coefficient (pair interactions)
   - C = 3rd virial coefficient (triplet interactions)
   - B(T): Negative at low T (attractive), positive at high T (repulsive)
   - Boyle temperature: B(T_B) = 0

5. Other Equations of State:
   - Redlich-Kwong: Improved high-pressure accuracy
   - Peng-Robinson: Better for liquids and near-critical
   - Benedict-Webb-Rubin: Multi-constant, high accuracy
        """,
        key_factors=[
            "Fugacity f replaces P in thermodynamic relations for real gases",
            "Fugacity coefficient φ = f/P, approaches 1 as P → 0",
            "Joule-Thomson effect: Cooling/heating upon expansion",
            "Inversion temperature: μ_JT changes sign",
            "Supercritical fluids: T > T_c, P > P_c, no phase boundary"
        ],
        primary_authority=[
            "Atkins' Physical Chemistry",
            "Sandler - Chemical, Biochemical, and Engineering Thermodynamics",
            "Smith, Van Ness & Abbott - Thermodynamics"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        equations=[
            "(P + a/V²)(V - b) = RT",
            "Z = PV/(nRT)",
            "PV = RT(1 + B/V + C/V² + ...)"
        ],
        applications=["Gas liquefaction", "High-pressure processes", "Supercritical extraction"]
    ),
]

# Telemetry
TELEMETRY = {
    "queries_total": 0,
    "queries_by_mode": {"FAST": 0, "DEFENSE": 0, "MEMO": 0},
    "avg_response_time_ms": 0.0,
    "doctrine_trigger_counts": {},
    "last_query_time": None
}

COVERAGE_MAP = {block.topic: 0 for block in DOCTRINE_CACHE}
START_TIME = datetime.utcnow()

# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def calculate_determinism_hash(query: str, answer: str) -> str:
    """Generate SHA-256 hash for reproducibility verification."""
    content = f"{query}|{answer}|{datetime.utcnow().date().isoformat()}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def select_doctrine_blocks(query: str) -> List[DoctrineBlock]:
    """Match query to relevant doctrine blocks."""
    matched = []
    for block in DOCTRINE_CACHE:
        if block.matches(query):
            matched.append(block)
            block.trigger()
            COVERAGE_MAP[block.topic] += 1
    return matched

def generate_answer(query: str, mode: ResponseMode, blocks: List[DoctrineBlock]) -> tuple[str, ConfidenceLevel, List[str]]:
    """Generate answer based on matched doctrine blocks and mode."""

    if not blocks:
        return (
            "No specific doctrine blocks matched. Physical chemistry encompasses thermodynamics (laws, enthalpy, entropy, Gibbs free energy), kinetics (rate laws, Arrhenius, transition state theory), quantum chemistry (Schrödinger equation, MO theory, computational methods), statistical mechanics (partition functions, Boltzmann distribution), surface chemistry (adsorption, catalysis), electrochemistry (Nernst equation, batteries), spectroscopy (Beer-Lambert, selection rules), phase equilibria (phase diagrams, Gibbs phase rule), and transport phenomena (diffusion, viscosity, conductivity). Please provide more specific query.",
            ConfidenceLevel.DISCLOSURE,
            []
        )

    reasoning_chain = []

    if mode == ResponseMode.FAST:
        # Concise summary
        primary = blocks[0]
        answer = f"{primary.conclusion_template}\n\n"

        if primary.equations:
            answer += f"Key equations: {', '.join(primary.equations[:3])}\n\n"

        answer += f"Authority: {primary.primary_authority[0]}"
        confidence = primary.confidence
        reasoning_chain = [f"Primary doctrine: {primary.topic}"]

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready detailed response
        answer = f"PHYSICAL CHEMISTRY ANALYSIS\n{'='*50}\n\n"

        for i, block in enumerate(blocks[:3], 1):
            answer += f"{i}. {block.topic.upper()}\n\n"
            answer += f"{block.reasoning_framework}\n\n"

            if block.equations:
                answer += f"Governing Equations:\n"
                for eq in block.equations:
                    answer += f"  • {eq}\n"
                answer += "\n"

            answer += f"Key Factors:\n"
            for factor in block.key_factors[:4]:
                answer += f"  • {factor}\n"
            answer += "\n"

            answer += f"Primary References:\n"
            for ref in block.primary_authority:
                answer += f"  • {ref}\n"
            answer += "\n"

            reasoning_chain.append(f"Doctrine {i}: {block.topic}")

        confidence = ConfidenceLevel.DEFENSIBLE

    else:  # MEMO
        # Comprehensive memorandum format
        answer = f"PHYSICAL CHEMISTRY MEMORANDUM\n{'='*70}\n\n"
        answer += f"Query: {query}\n\n"
        answer += f"EXECUTIVE SUMMARY\n{'-'*70}\n\n"

        summary_block = blocks[0]
        answer += f"{summary_block.conclusion_template}\n\n"

        answer += f"DETAILED ANALYSIS\n{'-'*70}\n\n"

        for i, block in enumerate(blocks, 1):
            answer += f"\n{i}. {block.topic.upper()}\n\n"
            answer += f"{block.reasoning_framework}\n\n"

            if block.equations:
                answer += f"Mathematical Framework:\n"
                for eq in block.equations:
                    answer += f"  {eq}\n"
                answer += "\n"

            if block.applications:
                answer += f"Applications:\n"
                for app in block.applications:
                    answer += f"  • {app}\n"
                answer += "\n"

            answer += f"Critical Considerations:\n"
            for factor in block.key_factors:
                answer += f"  • {factor}\n"
            answer += "\n"

            answer += f"Authoritative Sources:\n"
            for ref in block.primary_authority:
                answer += f"  • {ref}\n"
            answer += "\n"

            reasoning_chain.append(f"Analysis {i}: {block.topic}")

        answer += f"\nCONCLUSION\n{'-'*70}\n\n"
        answer += f"This analysis draws from {len(blocks)} doctrine blocks in physical chemistry covering thermodynamics, kinetics, quantum mechanics, statistical mechanics, and related fields. All conclusions are supported by standard physical chemistry textbooks and peer-reviewed literature.\n"

        confidence = ConfidenceLevel.DEFENSIBLE

    return answer, confidence, reasoning_chain

# ============================================================================
# API ENDPOINTS
# ============================================================================

@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint for physical chemistry intelligence."""
    start = datetime.utcnow()

    try:
        logger.info(f"Query received: {request.query[:100]}... | Mode: {request.mode}")

        # Match doctrine blocks
        matched_blocks = select_doctrine_blocks(request.query)

        # Generate answer
        answer, confidence, reasoning = generate_answer(
            request.query,
            request.mode,
            matched_blocks
        )

        # Calculate hash
        det_hash = calculate_determinism_hash(request.query, answer)

        # Update telemetry
        elapsed_ms = (datetime.utcnow() - start).total_seconds() * 1000
        TELEMETRY["queries_total"] += 1
        TELEMETRY["queries_by_mode"][request.mode] += 1
        TELEMETRY["last_query_time"] = start.isoformat()

        prev_avg = TELEMETRY["avg_response_time_ms"]
        n = TELEMETRY["queries_total"]
        TELEMETRY["avg_response_time_ms"] = (prev_avg * (n-1) + elapsed_ms) / n

        for block in matched_blocks:
            TELEMETRY["doctrine_trigger_counts"][block.topic] = block.trigger_count

        logger.info(f"Query completed in {elapsed_ms:.2f}ms | Blocks: {len(matched_blocks)} | Confidence: {confidence}")

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            doctrine_blocks_triggered=[b.topic for b in matched_blocks],
            reasoning_chain=reasoning,
            determinism_hash=det_hash,
            response_mode=request.mode,
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    uptime = (datetime.utcnow() - START_TIME).total_seconds()

    return HealthResponse(
        status="operational",
        engine="CHEM04_physical_chemistry",
        version="1.0.0",
        port=9054,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=uptime
    )

@APP.get("/metrics")
async def get_metrics():
    """Return telemetry metrics."""
    return {
        "telemetry": TELEMETRY,
        "coverage_map": COVERAGE_MAP,
        "doctrine_cache_size": len(DOCTRINE_CACHE),
        "uptime_seconds": (datetime.utcnow() - START_TIME).total_seconds()
    }

@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks with trigger statistics."""
    return [
        {
            "topic": block.topic,
            "keywords": block.keywords,
            "trigger_count": block.trigger_count,
            "last_triggered": block.last_triggered,
            "confidence": block.confidence,
            "equations_count": len(block.equations),
            "applications_count": len(block.applications)
        }
        for block in DOCTRINE_CACHE
    ]

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CHEM04 Physical Chemistry Engine on port 9054")
    uvicorn.run(APP, host="0.0.0.0", port=9054)
