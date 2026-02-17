"""
CHEM12 Nuclear Chemistry Intelligence Engine
TIE-Grade Domain Expert System

Analyzes nuclear chemistry: radioactive decay, nuclear reactions, radiation detection,
radiochemical separations, nuclear waste management, and radiation protection.

Port: 9294
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMS AND DATA MODELS
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


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    RADIOACTIVE_DECAY = "RADIOACTIVE_DECAY"
    NUCLEAR_REACTIONS = "NUCLEAR_REACTIONS"
    RADIATION_DETECTION = "RADIATION_DETECTION"
    DOSIMETRY = "DOSIMETRY"
    RADIATION_PROTECTION = "RADIATION_PROTECTION"
    NUCLEAR_WASTE = "NUCLEAR_WASTE"
    RADIOCHEMISTRY = "RADIOCHEMISTRY"
    FISSION_FUSION = "FISSION_FUSION"
    NEUTRON_ACTIVATION = "NEUTRON_ACTIVATION"
    NORM_OILFIELD = "NORM_OILFIELD"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    SHIELDING_DESIGN = "SHIELDING_DESIGN"


@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str


class QueryRequest(BaseModel):
    question: str = Field(..., description="Nuclear chemistry question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    sources: List[str]
    reasoning_chain: List[str]
    triggered_doctrines: List[str]
    response_time_ms: float
    determinism_hash: str
    epistemic_disclosure: Optional[str] = None


# ============================================================================
# DOCTRINE CACHE - 25+ REAL NUCLEAR CHEMISTRY BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Alpha Decay Fundamentals",
        keywords=["alpha decay", "alpha particle", "helium nucleus", "transmutation", "decay energy", "tunneling", "Q-value"],
        conclusion_template="Alpha decay occurs when a nucleus emits a helium-4 nucleus (2 protons, 2 neutrons), reducing atomic number by 2 and mass number by 4. The process is governed by quantum tunneling through the Coulomb barrier, with decay energy (Q-value) determining half-life via the Geiger-Nuttall relationship.",
        reasoning_framework="""
Alpha decay mechanism and energetics:
1. Parent nucleus (Z, A) → Daughter nucleus (Z-2, A-4) + α particle (He-4)
2. Q-value calculation: Q = [M(parent) - M(daughter) - M(α)] × c²
3. Energy partitioning: Most energy goes to α particle (lighter product)
   E_α ≈ Q × [A-4]/A (typically 4-9 MeV for natural α emitters)
4. Geiger-Nuttall law: log(λ) = A + B × log(E_α)
   Higher decay energy → shorter half-life
5. Quantum tunneling: α particle escapes despite insufficient classical energy
   Barrier penetration probability ∝ exp(-2π × Z × √(μ/E))
6. Angular momentum considerations: l = 0 (ground-to-ground) fastest
   Higher l values (excited states) suppress decay rate
7. Energy levels: α spectrum reveals nuclear structure
   Discrete energies correspond to daughter nuclear states
8. Range in matter: R(cm in air) ≈ 0.31 × E³ for 4-7 MeV
   Very short range, stopped by paper/dead skin layer
9. Biological hazard: High LET, serious internal hazard if ingested/inhaled
   Low external hazard due to short range
10. Common emitters: U-238 (4.47 MeV, 4.5×10⁹ yr), Ra-226 (4.78 MeV, 1600 yr)
    Po-210 (5.30 MeV, 138 days), Pu-239 (5.16 MeV, 24,110 yr)
""",
        key_factors=[
            "Q-value determines decay energy and kinetics",
            "Geiger-Nuttall relationship links energy to half-life",
            "Quantum tunneling enables decay below classical barrier",
            "Angular momentum conservation affects decay rate",
            "Short range in matter limits external hazard",
            "High LET creates serious internal contamination risk",
            "Mass number decreases by 4, atomic number by 2"
        ],
        primary_authority=[
            "Krane, Introductory Nuclear Physics (1988)",
            "Friedlander, Kennedy, Macias, Nuclear and Radiochemistry (1981)",
            "Turner, Atoms, Radiation, and Radiation Protection (2007)"
        ],
        burden_holder="Analyst must calculate Q-value and predict decay products",
        adversary_position="Classical mechanics cannot explain decay of bound states",
        counter_arguments=[
            "Quantum tunneling provides mechanism",
            "Experimental half-lives confirm Geiger-Nuttall predictions",
            "Alpha spectra reveal discrete nuclear energy levels"
        ],
        resolution_strategy="Apply quantum mechanical barrier penetration model with experimental calibration",
        entity_scope="All alpha-emitting radionuclides",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established theory with extensive experimental validation",
        controlling_precedent="Geiger-Nuttall law (1911), Gamow tunneling theory (1928)"
    ),

    DoctrineBlock(
        topic="Beta Decay Modes and Neutrino Physics",
        keywords=["beta minus", "beta plus", "electron capture", "neutrino", "antineutrino", "weak interaction", "fermi theory"],
        conclusion_template="Beta decay involves weak interaction conversion of neutron to proton (β⁻), proton to neutron (β⁺), or orbital electron capture. All modes conserve lepton number via neutrino emission. Maximum beta energy equals Q-value, but continuous spectrum results from three-body decay kinematics.",
        reasoning_framework="""
Beta decay mechanisms and selection rules:
1. β⁻ decay: n → p + e⁻ + ν̄ₑ (neutron-rich nuclei)
   Example: C-14 → N-14 + e⁻ + ν̄ₑ (Q = 0.156 MeV)
2. β⁺ decay: p → n + e⁺ + νₑ (proton-rich nuclei)
   Requires Q > 1.022 MeV (two electron rest masses)
   Example: F-18 → O-18 + e⁺ + νₑ (Q = 0.634 MeV)
3. Electron capture (EC): p + e⁻ → n + νₑ
   Competes with β⁺, especially at low Q-values
   Example: Fe-55 + e⁻ → Mn-55 + νₑ (Q = 0.231 MeV)
4. Fermi theory: Decay rate ∝ f(Z, E₀) × |M|² (phase space × matrix element)
   f(Z, E₀) = statistical factor (energy-dependent)
   |M|² = nuclear matrix element (transition strength)
5. Allowed vs forbidden transitions:
   Allowed: Δl = 0, ΔS = 0 (Fermi) or ΔS = 1 (Gamow-Teller)
   Forbidden: Higher angular momentum changes, longer half-lives
6. ft value (comparative half-life): log(ft) classifies transitions
   log(ft) ≈ 3-4: superallowed (0⁺ → 0⁺)
   log(ft) ≈ 4-6: allowed
   log(ft) > 6: forbidden
7. Continuous beta spectrum: Three-body decay shares energy
   Maximum Eβ = Q-value, but average Eβ ≈ Q/3
   Neutrino carries away missing energy and momentum
8. Kurie plot: √(N(E)/f(Z,E)) vs E linear for allowed transitions
   Endpoint extrapolation gives Q-value
9. Double beta decay: (Z, A) → (Z+2, A) + 2e⁻ + 2ν̄ₑ
   Extremely rare, half-lives > 10¹⁹ years
   Neutrinoless mode (0νββ) would prove neutrino is Majorana particle
10. Biological effects: Continuous energy spectrum, medium LET
    Penetrates skin but stopped by mm of Al or plastic
""",
        key_factors=[
            "Weak interaction changes nuclear charge without changing mass number",
            "Neutrino emission conserves energy, momentum, and lepton number",
            "Continuous spectrum results from three-body kinematics",
            "Selection rules determine allowed vs forbidden transitions",
            "EC competes with β⁺ at low Q-values",
            "ft values classify transition types",
            "Average beta energy approximately one-third of maximum"
        ],
        primary_authority=[
            "Fermi, Z. Phys. 88, 161 (1934) - Original beta decay theory",
            "Krane, Introductory Nuclear Physics, Ch. 9",
            "ICRP Publication 38 - Radionuclide transformations"
        ],
        burden_holder="Analyst must determine decay mode from nuclear stability considerations",
        adversary_position="Why does beta spectrum appear continuous if energy quantized?",
        counter_arguments=[
            "Neutrino hypothesis (Pauli 1930) resolves energy conservation",
            "Recoil experiments confirm three-body decay",
            "Neutrino detection experiments (Cowan-Reines 1956) proved existence"
        ],
        resolution_strategy="Apply Fermi theory with selection rules and phase space calculations",
        entity_scope="All beta-emitting radionuclides",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established weak interaction theory with experimental validation",
        controlling_precedent="Fermi theory (1934), neutrino discovery (1956)"
    ),

    DoctrineBlock(
        topic="Gamma Emission and Internal Conversion",
        keywords=["gamma ray", "isomeric transition", "internal conversion", "conversion electron", "metastable state", "E2 transition", "M1 transition"],
        conclusion_template="Gamma emission de-excites nuclear excited states via electromagnetic radiation. Competing internal conversion process ejects orbital electrons instead of photons, with conversion coefficient α = e⁻/γ depending on transition multipolarity and atomic number.",
        reasoning_framework="""
Gamma decay and internal conversion mechanisms:
1. Nuclear de-excitation: Excited state → ground state + γ photon
   Monoenergetic photons (unlike continuous beta spectrum)
   Energies typically 0.1-3 MeV for common radionuclides
2. Isomeric states: Metastable excited states with measurable half-lives
   Example: Tc-99m (6.01 hr) → Tc-99 + γ (140 keV)
   Medical imaging workhorse (90% of nuclear medicine)
3. Transition multipolarity: Electric (E) or Magnetic (M)
   E1 (electric dipole): fastest, Δl = ±1, π changes
   M1 (magnetic dipole): Δl = 0, ±1, π unchanged
   E2 (electric quadrupole): Δl = ±2, π unchanged
   Higher multipoles (E3, M2, etc.) increasingly forbidden
4. Weisskopf estimates: Predict transition rates
   τ(E1) ≈ 10⁻¹⁴ s, τ(M1) ≈ 10⁻¹³ s, τ(E2) ≈ 10⁻⁹ s
   Actual rates can differ by factors due to nuclear structure
5. Internal conversion: Alternative de-excitation path
   Nuclear electromagnetic field ejects inner shell electron
   Conversion coefficient α = λₑ/λᵧ (ratio of rates)
   α increases with: higher Z, lower Eᵧ, higher multipolarity
6. Conversion electron energies: E_e = E_transition - B_shell
   Discrete energies for K, L, M shells
   Example: Cs-137 → Ba-137m (662 keV γ)
     K-conversion electron: 662 - 37 = 625 keV
7. Auger electrons: Follow internal conversion or EC
   Outer electron fills inner shell vacancy, energy to another electron
   Low energy (typically < 20 keV), high abundance
8. X-ray fluorescence: Characteristic X-rays from orbital rearrangement
   Accompanies EC and internal conversion
   Energy diagnostic of element (Z determination)
9. Angular correlation: γ-γ coincidence reveals spin sequences
   Cascade emissions show directional correlations
   Used in nuclear spectroscopy and Mössbauer effect
10. Pair production: High-energy γ (>1.022 MeV) → e⁺ + e⁻ in nuclear field
    Threshold = 2mₑc² = 1.022 MeV
    Important for shielding high-energy emitters
""",
        key_factors=[
            "Monoenergetic photon emission from discrete nuclear levels",
            "Metastable isomers enable medical imaging applications",
            "Transition multipolarity determines decay rate",
            "Internal conversion competes with gamma emission",
            "Conversion coefficient increases with Z and multipolarity",
            "Auger electrons and X-rays accompany orbital rearrangements",
            "Pair production becomes significant above 1.022 MeV"
        ],
        primary_authority=[
            "Krane, Introductory Nuclear Physics, Ch. 10",
            "Firestone, Table of Isotopes (8th ed.)",
            "ICRP Publication 107 - Nuclear decay data"
        ],
        burden_holder="Analyst must identify transition type from energy and half-life",
        adversary_position="How can nucleus emit electromagnetic radiation without charged constituents?",
        counter_arguments=[
            "Proton charge distribution creates nuclear electromagnetic moments",
            "Time-varying quadrupole/dipole moments radiate",
            "Internal conversion proves nuclear origin (not atomic)"
        ],
        resolution_strategy="Apply electromagnetic transition theory with multipolarity selection rules",
        entity_scope="All gamma-emitting radionuclides and isomeric states",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established electromagnetic theory with extensive spectroscopic data",
        controlling_precedent="Weisskopf estimates, internal conversion theory (1930s)"
    ),

    DoctrineBlock(
        topic="Radioactive Decay Kinetics and Secular Equilibrium",
        keywords=["decay constant", "half-life", "activity", "secular equilibrium", "transient equilibrium", "bateman equations", "branching ratio"],
        conclusion_template="Radioactive decay follows first-order kinetics with characteristic half-life t₁/₂ = ln(2)/λ. Decay chains reach secular equilibrium when parent half-life exceeds daughter by factor >100, resulting in equal activities despite different decay constants.",
        reasoning_framework="""
Decay kinetics and equilibrium conditions:
1. Fundamental decay law: N(t) = N₀ × e^(-λt)
   λ = decay constant (probability per unit time)
   Independent of temperature, pressure, chemical state
2. Half-life relationship: t₁/₂ = ln(2)/λ = 0.693/λ
   Mean lifetime τ = 1/λ = 1.443 × t₁/₂
3. Activity: A(t) = λN(t) = A₀ × e^(-λt)
   Units: Becquerel (Bq) = 1 dps, Curie (Ci) = 3.7×10¹⁰ Bq
   Specific activity: A/m = λNₐ/M (Bq/g)
4. Bateman equations for decay chains:
   For A → B → C: N_B(t) = (λ_A/(λ_B - λ_A)) × N_A(0) × [e^(-λ_A×t) - e^(-λ_B×t)]
   General solution accounts for all chain members
5. Secular equilibrium: λ_parent << λ_daughter
   Condition: t₁/₂(parent) > 100 × t₁/₂(daughter)
   Result: A_daughter = A_parent at equilibrium
   Example: Ra-226 (1600 yr) / Rn-222 (3.82 days)
   Time to reach: ~7 × t₁/₂(daughter)
6. Transient equilibrium: λ_parent < λ_daughter
   Condition: 10 < t₁/₂(parent)/t₁/₂(daughter) < 100
   Result: A_daughter/A_parent = λ_daughter/(λ_daughter - λ_parent) > 1
   Example: Mo-99 (66 hr) / Tc-99m (6 hr)
   Daughter activity exceeds parent at equilibrium
7. No equilibrium: λ_parent > λ_daughter
   Parent decays faster than daughter accumulates
   Daughter activity continuously increases after parent decay
8. Branching decay: Single parent → multiple daughters
   λ_total = Σλᵢ, branching ratio = λᵢ/λ_total
   Example: K-40 → Ca-40 (89%) + Ar-40 (11%)
9. Radioisotope generators: Exploit transient equilibrium
   Mo-99/Tc-99m generator: Elute Tc-99m daily
   Sr-90/Y-90 generator: 64 hr to 90% Y-90 equilibrium
10. Dating applications: C-14 (5730 yr), U-238/Th-230 series
    Assumption: Closed system, known initial ratio
""",
        key_factors=[
            "First-order kinetics with exponential decay",
            "Half-life independent of physical/chemical conditions",
            "Activity equals decay constant times number of atoms",
            "Secular equilibrium when parent much longer-lived than daughter",
            "Transient equilibrium enables radioisotope generators",
            "Bateman equations solve general decay chains",
            "Branching decay produces multiple daughter products"
        ],
        primary_authority=[
            "Bateman, Proc. Cambridge Phil. Soc. 15, 423 (1910)",
            "Friedlander, Nuclear and Radiochemistry, Ch. 3",
            "NCRP Report 160 - Ionizing radiation exposure"
        ],
        burden_holder="Analyst must solve Bateman equations for decay chain activities",
        adversary_position="Why should decay be random rather than deterministic?",
        counter_arguments=[
            "Quantum mechanics inherently probabilistic",
            "Exponential decay validated across 20+ orders of magnitude in half-life",
            "Statistical fluctuations match Poisson distribution predictions"
        ],
        resolution_strategy="Apply first-order kinetics with appropriate equilibrium approximations",
        entity_scope="All radioactive decay processes and chains",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fundamental theory with universal experimental validation",
        controlling_precedent="Rutherford-Soddy decay law (1902), Bateman equations (1910)"
    ),

    DoctrineBlock(
        topic="Nuclear Fission Mechanism and Energetics",
        keywords=["fission", "critical mass", "chain reaction", "neutron multiplication", "fission products", "delayed neutrons", "breeding ratio"],
        conclusion_template="Nuclear fission splits heavy nucleus into two fragments plus 2-3 neutrons, releasing ~200 MeV per event. Sustained chain reaction requires k_eff ≥ 1, controlled by delayed neutrons (β_eff ≈ 0.0065 for U-235) which provide ~100× longer response time than prompt neutrons.",
        reasoning_framework="""
Fission process and chain reaction dynamics:
1. Fission mechanism: Heavy nucleus (A > 230) → 2 fragments + neutrons
   Induced fission: U-235 + n → compound nucleus → fission products
   Spontaneous fission: Rare for U-235 (SF/α ≈ 10⁻⁹), dominant for Cf-252
2. Liquid drop model: Fission barrier E_barrier ≈ 5-6 MeV
   Fissility parameter: Z²/A > 47 for spontaneous fission
   Thermal neutrons (0.025 eV) induce fission in U-235, Pu-239, U-233
   Fast neutrons (>1 MeV) required for U-238, Th-232
3. Energy release: Q ≈ 200 MeV per fission
   Kinetic energy of fragments: 168 MeV (85%)
   Prompt neutrons: 5 MeV (2.5%)
   Prompt gamma rays: 7 MeV (3.5%)
   Beta decay of products: 8 MeV (4%)
   Neutrinos: 12 MeV (6%, escapes detector)
4. Fission products: Mass distribution bimodal
   Light peak: A ≈ 95 (Sr-90, Y-91, Zr-95)
   Heavy peak: A ≈ 138 (Cs-137, Ba-140, I-131)
   Symmetric fission (A ≈ 117) much less probable
5. Neutron balance: Average ν = 2.43 neutrons per U-235 fission
   Prompt neutrons: 99.3%, emitted in 10⁻¹⁴ seconds
   Delayed neutrons: 0.7%, from fission product decay (0.1-60 sec)
   Six precursor groups with different half-lives
6. Multiplication factor: k = (neutrons in generation n+1)/(neutrons in generation n)
   k < 1: subcritical (decay)
   k = 1: critical (steady state)
   k > 1: supercritical (exponential growth)
7. Effective multiplication factor: k_eff = k_∞ × P_NL
   k_∞ = ηfpε (infinite medium: eta, thermal utilization, resonance escape, fast fission)
   P_NL = non-leakage probability (geometry-dependent)
8. Critical mass: Minimum mass for k_eff = 1
   U-235 bare sphere: ~52 kg
   Pu-239 bare sphere: ~10 kg
   Reduced by neutron reflector (BeO, graphite)
9. Reactivity: ρ = (k - 1)/k
   Dollar unit: ρ/$1 = ρ/β_eff (delayed neutron fraction)
   Prompt critical: ρ > β_eff (uncontrollable exponential rise)
10. Breeding: Fertile material (U-238, Th-232) → fissile via neutron capture
    Breeding ratio = fissile produced / fissile consumed
    BR > 1: breeder reactor (Pu-239 from U-238)
""",
        key_factors=[
            "~200 MeV released per fission event",
            "Average 2.43 neutrons per U-235 fission",
            "Delayed neutrons enable reactor control",
            "Critical mass depends on geometry and reflectors",
            "Bimodal fission product mass distribution",
            "Prompt critical threshold at one dollar reactivity",
            "Breeding converts fertile to fissile material"
        ],
        primary_authority=[
            "Lamarsh, Introduction to Nuclear Reactor Theory (1966)",
            "Duderstadt & Hamilton, Nuclear Reactor Analysis (1976)",
            "Glasstone & Sesonske, Nuclear Reactor Engineering (1994)"
        ],
        burden_holder="Analyst must calculate multiplication factor and critical mass",
        adversary_position="How can delayed neutrons control process 100× faster?",
        counter_arguments=[
            "Reactor period dominated by longest timescale (delayed neutrons)",
            "Without delayed neutrons, control impossible (prompt critical)",
            "Six precursor groups provide distributed response times"
        ],
        resolution_strategy="Apply neutron balance equations with delayed neutron dynamics",
        entity_scope="Fissile and fertile isotopes in reactor and weapons contexts",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established reactor physics with 70+ years of operational data",
        controlling_precedent="Fermi pile (1942), reactor kinetics equations"
    ),

    DoctrineBlock(
        topic="Nuclear Fusion Reactions and Stellar Nucleosynthesis",
        keywords=["fusion", "coulomb barrier", "tunneling probability", "pp chain", "CNO cycle", "binding energy", "plasma confinement"],
        conclusion_template="Nuclear fusion combines light nuclei to release energy via mass-energy conversion. Requires extreme temperatures (10⁷-10⁸ K) to overcome Coulomb repulsion. Stellar fusion (pp chain, CNO cycle) powers stars and synthesizes elements up to iron; heavier elements form in supernovae.",
        reasoning_framework="""
Fusion mechanisms and astrophysical implications:
1. Coulomb barrier: Two protons must approach within ~10⁻¹⁵ m to fuse
   Barrier height: V = e²/(4πε₀r) ≈ 1.4 MeV at r = 1 fm
   Thermal energy: kT = 1 keV at T = 10⁷ K << barrier
   Quantum tunneling enables fusion at sub-barrier energies
2. Gamow peak: Convolution of barrier penetration and Maxwell-Boltzmann
   Optimal energy E₀ ≈ (bkT/2)^(2/3) where b = 31.3 × Z₁Z₂ × √(μ)
   Fusion rate peaks at E₀, not at kT
3. Proton-proton chain (Sun, M < 1.3 M☉):
   Step 1: p + p → ²H + e⁺ + νₑ (slowest, rate-limiting)
   Step 2: ²H + p → ³He + γ
   Step 3a: ³He + ³He → ⁴He + 2p (85%)
   Step 3b: ³He + ⁴He → ⁷Be + γ → ... (15%)
   Net: 4p → ⁴He + 2e⁺ + 2νₑ + 26.7 MeV
4. CNO cycle (massive stars, M > 1.3 M☉):
   ¹²C + p → ¹³N → ¹³C + p → ¹⁴N + p → ¹⁵O → ¹⁵N + p → ¹²C + ⁴He
   Carbon acts as catalyst, regenerated at cycle end
   Temperature-sensitive: rate ∝ T¹⁸
5. Binding energy per nucleon: Maximum at Fe-56 (~8.8 MeV)
   Fusion releases energy for A < 56
   Fission releases energy for A > 56
   No energy gain from Fe fusion (stellar death)
6. Deuterium-tritium fusion (D-T, terrestrial reactors):
   ²H + ³H → ⁴He (3.5 MeV) + n (14.1 MeV)
   Lowest Coulomb barrier, highest cross-section
   Plasma temperature ~10⁸ K required
7. Lawson criterion: Confinement parameter nτ > threshold
   Magnetic confinement (tokamak): nτ > 10²⁰ s/m³
   Inertial confinement (laser fusion): nτ > 10²⁸ s/m³
   Energy break-even: Q = E_out/E_in > 1
8. Triple-alpha process: ⁴He + ⁴He ⇌ ⁸Be (unstable)
   ⁸Be + ⁴He → ¹²C + γ (requires T > 10⁸ K)
   Produces carbon in red giant stars
9. Supernova nucleosynthesis: r-process (rapid neutron capture)
   Neutron flux ~10²⁵ n/cm²/s, timescale < β⁻ decay
   Builds neutron-rich isotopes beyond Fe
   s-process (slow capture) in AGB stars: timescale > β⁻ decay
10. Solar neutrino problem: Measured flux < predicted
    Resolved by neutrino oscillations (mass eigenstates)
    Confirms solar fusion model
""",
        key_factors=[
            "Coulomb barrier requires extreme temperatures for fusion",
            "Quantum tunneling enables sub-barrier fusion",
            "pp chain dominates in Sun-like stars",
            "CNO cycle temperature-sensitive, dominates in massive stars",
            "Binding energy per nucleon peaks at iron",
            "D-T reaction most favorable for terrestrial fusion",
            "Lawson criterion defines confinement requirements"
        ],
        primary_authority=[
            "Rolfs & Rodney, Cauldrons in the Cosmos (1988)",
            "Clayton, Principles of Stellar Evolution and Nucleosynthesis (1983)",
            "Krane, Introductory Nuclear Physics, Ch. 19"
        ],
        burden_holder="Analyst must calculate fusion cross-sections and energy yields",
        adversary_position="How can fusion occur below Coulomb barrier energy?",
        counter_arguments=[
            "Quantum tunneling provides finite barrier penetration probability",
            "Gamow peak calculation predicts observed fusion rates",
            "Solar neutrino flux confirms fusion model"
        ],
        resolution_strategy="Apply quantum tunneling theory with astrophysical reaction networks",
        entity_scope="Stellar interiors and terrestrial fusion devices",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established stellar physics with helioseismology and neutrino validation",
        controlling_precedent="Bethe CNO cycle (1939), pp chain (1939)"
    ),

    DoctrineBlock(
        topic="Radiation Detection - Gas-Filled Detectors",
        keywords=["geiger mueller", "proportional counter", "ionization chamber", "gas multiplication", "quenching gas", "dead time", "plateau"],
        conclusion_template="Gas-filled detectors measure radiation via ionization of fill gas. Ionization chambers operate in recombination-free region, proportional counters use controlled gas multiplication (M ≈ 10³-10⁴), and GM tubes operate in saturated avalanche mode with dead time 50-300 μs limiting count rate.",
        reasoning_framework="""
Gas detector operating regions and characteristics:
1. Ionization chamber: Operates in plateau region (V < 500 V)
   No gas multiplication, current proportional to ionization rate
   W-value: Average energy per ion pair (~30 eV in air)
   Applications: Dose rate measurement, smoke detectors
   Advantages: Energy proportional, no dead time
   Disadvantages: Low signal, requires electrometer amplification
2. Proportional counter: Moderate voltage (500-1000 V)
   Gas multiplication factor M = exp(αd) where α = Townsend coefficient
   Typical M = 10³-10⁴, preserves energy information
   Fill gas: P-10 (90% Ar + 10% CH₄), or Ar + CO₂
   Quenching gas prevents continuous discharge
   Applications: X-ray spectroscopy, low-energy beta counting
3. Geiger-Müller tube: High voltage (900-1200 V), saturated avalanche
   GM plateau: Count rate constant over 200-300 V range
   Plateau slope: <5% per 100 V indicates good tube
   Dead time: τ_dead = 50-300 μs (halogen-quenched < organic)
   Resolving time: τ_res ≈ 1.5 × τ_dead
   Correction for dead time: N_true = N_obs/(1 - N_obs × τ)
   Maximum count rate: ~10,000 cpm before significant losses
4. Energy dependence: GM tubes energy-independent (all-or-nothing)
   Proportional counters energy-proportional
   Window thickness limits low-energy response
5. Efficiency factors:
   Geometric efficiency: Solid angle fraction 4π
   Intrinsic efficiency: P(interaction | entered detector)
   Overall efficiency: ε = ε_geom × ε_int × other factors
6. Alpha vs beta discrimination: Proportional mode
   Pulse height proportional to energy and dE/dx
   Alpha pulses ~10× larger than beta at same energy
7. Quenching mechanisms:
   Self-quenching: Halogen additives (Cl₂, Br₂)
   Organic quenching: Ethanol, isobutane (limited tube life)
   Photon-induced secondary discharges suppressed
8. Tube construction: Central anode wire (10-50 μm diameter)
   Cylindrical cathode, thin window for beta/gamma
   Fill pressure: 0.1 atm (GM) to several atm (proportional)
9. Background reduction: Anticoincidence shielding
   Pulse shape discrimination
   Lead shielding (≥2 inch for GM survey)
10. Common GM tubes: Pancake probe (44 cm² window, α/β/γ)
    End-window tube (thin mica, low-energy β)
    Energy-compensated (metal filter, flat γ response)
""",
        key_factors=[
            "Operating voltage determines detector mode",
            "Gas multiplication factor ranges from 1 (chamber) to 10⁸ (GM)",
            "GM tubes have dead time limiting count rate",
            "Proportional counters preserve energy information",
            "Quenching gas prevents continuous discharge",
            "Dead time correction critical above 1000 cpm",
            "Window thickness limits low-energy response"
        ],
        primary_authority=[
            "Knoll, Radiation Detection and Measurement (4th ed.)",
            "Tsoulfanidis, Measurement and Detection of Radiation (2010)",
            "ANSI N42.17 - Performance specifications for portable GM detectors"
        ],
        burden_holder="Analyst must correct for dead time and determine efficiency",
        adversary_position="Why does GM tube lose energy information?",
        counter_arguments=[
            "Saturated avalanche produces maximum signal regardless of initial energy",
            "Trade-off: Simplicity and robustness vs energy resolution",
            "Proportional mode preserves energy at cost of complexity"
        ],
        resolution_strategy="Select detector mode based on measurement requirements and correct for operational limitations",
        entity_scope="All gas-filled radiation detectors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature technology with well-characterized performance",
        controlling_precedent="Geiger-Müller theory (1928), proportional counter development (1940s)"
    ),

    DoctrineBlock(
        topic="Scintillation Detectors and Photomultipliers",
        keywords=["scintillator", "NaI(Tl)", "photomultiplier", "light yield", "energy resolution", "pulse height spectrum", "photoelectric peak"],
        conclusion_template="Scintillation detectors convert radiation energy to light photons collected by photomultiplier tube. NaI(Tl) provides 38,000 photons/MeV with 7-8% energy resolution at 662 keV. Organic scintillators offer fast timing (ns) but lower light yield and energy resolution than inorganic crystals.",
        reasoning_framework="""
Scintillation detection mechanisms and performance:
1. Scintillation process: Radiation → excitation → photon emission
   Inorganic (NaI(Tl), CsI(Tl), BGO): Band gap transitions
   Organic (anthracene, stilbene, plastic): Molecular fluorescence
   Noble liquids (LXe, LAr): Excimer emission
2. NaI(Tl) properties: Workhorse gamma spectroscopy detector
   Light yield: 38,000 photons/MeV (vs 10,000 for plastic)
   Emission peak: 415 nm (matches bialkali photocathode)
   Decay time: 230 ns (limits count rate to ~50,000 cps)
   Energy resolution: 7-8% FWHM at 662 keV (Cs-137)
   Hygroscopic: Requires hermetic seal
3. Photomultiplier tube (PMT): Converts light to electrical signal
   Photocathode: Bialkali (Na₂KSb), quantum efficiency ~25% at 415 nm
   Dynode chain: 8-14 stages, gain 10⁶-10⁸
   Anode signal: V = Q/C = (G × Nph × e)/C
   Timing resolution: ~1 ns with fast scintillator
4. Energy resolution: σ/E = √[(σ_stat)² + (σ_inhom)² + (σ_noise)²]
   Statistical: σ_stat/E ≈ 2.35/√(Npe) where Npe = photons collected
   Inhomogeneity: Light collection non-uniformity
   Electronic noise: PMT dark current, preamplifier
   Intrinsic resolution: ~3% for NaI(Tl), limited by statistics
5. Pulse height spectrum: Gamma interactions produce characteristic features
   Photopeak: Full energy deposition (photoelectric absorption)
   Compton edge: Maximum Compton scatter energy
   Compton continuum: Partial energy deposition
   Backscatter peak: 180° scattering from surroundings (≈200 keV)
   X-ray escape peak: Iodine K-shell X-rays escape detector
6. Gamma interaction mechanisms:
   Photoelectric: Dominant at low E, cross-section ∝ Z⁵/E³·⁵
   Compton scattering: Dominant at medium E (0.2-2 MeV)
   Pair production: Threshold 1.022 MeV, dominant at high E
7. Efficiency: Depends on crystal size and gamma energy
   3×3 inch NaI(Tl): ~100% for 100 keV, ~20% for 1 MeV
   Peak-to-total ratio: Photopeak area / total spectrum
   Absolute efficiency: ε_abs = counts / emissions from source
8. Organic scintillators: Fast timing, pulse shape discrimination
   Plastic (BC-400): 10,000 photons/MeV, 1-2 ns decay
   Anthracene: 20,000 photons/MeV (standard reference)
   Stilbene: n/γ discrimination via pulse shape
   Applications: Neutron detection, fast timing, large-area detectors
9. Other inorganics:
   BGO (Bi₄Ge₃O₁₂): High density (7.1 g/cm³), PET scanners
   CsI(Tl): Non-hygroscopic, rugged, 565 nm emission
   LSO/LYSO: Fast (40 ns), high light yield, PET
10. Semiconductor competition: HPGe superior resolution (0.2% at 1.33 MeV)
    But requires liquid nitrogen cooling
    NaI(Tl) remains standard for field surveys
""",
        key_factors=[
            "Light yield determines statistical energy resolution limit",
            "NaI(Tl) standard for gamma spectroscopy with 7-8% resolution",
            "PMT converts scintillation photons to electrical signal with gain 10⁶-10⁸",
            "Photopeak identifies full energy deposition",
            "Organic scintillators offer fast timing but lower resolution",
            "Energy resolution degrades with decreasing photon energy",
            "Crystal size and density determine detection efficiency"
        ],
        primary_authority=[
            "Knoll, Radiation Detection and Measurement, Ch. 8-10",
            "Birks, Theory and Practice of Scintillation Counting (1964)",
            "ANSI N42.14 - Calibration and use of NaI(Tl) systems"
        ],
        burden_holder="Analyst must calibrate energy scale and determine efficiencies",
        adversary_position="Why can't scintillators match semiconductor resolution?",
        counter_arguments=[
            "Scintillation process inherently has poor photon statistics",
            "~38,000 photons/MeV vs 300,000 electron-hole pairs/MeV in Ge",
            "Trade-off: Room temperature operation vs resolution"
        ],
        resolution_strategy="Apply scintillation physics with statistical limits and calibration curves",
        entity_scope="All scintillation-based radiation detectors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature technology with 70+ years of development and standardization",
        controlling_precedent="NaI(Tl) development (1948), PMT theory"
    ),

    DoctrineBlock(
        topic="Semiconductor Detectors - HPGe and Si(Li)",
        keywords=["HPGe", "germanium detector", "silicon detector", "energy resolution", "charge collection", "depletion depth", "liquid nitrogen"],
        conclusion_template="High-purity germanium (HPGe) detectors provide superior energy resolution (0.2% at 1.33 MeV) via direct ionization with W-value of 2.96 eV. Requires liquid nitrogen cooling (77 K) to suppress thermal leakage current. Silicon detectors operate at room temperature for charged particles and low-energy X-rays.",
        reasoning_framework="""
Semiconductor detector physics and performance:
1. Direct ionization: Radiation creates electron-hole pairs
   W-value: Average energy per pair
   Ge: 2.96 eV (vs 30 eV for gas, 100 eV effective for scintillator)
   Si: 3.62 eV
   Superior statistics: Neh = E/W ~ 300,000 for 1 MeV gamma in Ge
2. Energy resolution: Statistical limit ΔE/E = 2.35 × √(F × W/E)
   Fano factor F ≈ 0.13 for Ge (reduces statistical spread)
   Theoretical resolution: 0.1% at 1 MeV
   Actual resolution: 0.2% (1.8 keV FWHM at 1.33 MeV Co-60)
   Electronic noise adds ~1 keV
3. HPGe detector construction:
   Zone-refined germanium: <10¹⁰ impurities/cm³
   P-type or N-type, coaxial or planar geometry
   Depletion depth: d = √(2ε₀ε_rV/eN_d) typically 1-5 cm
   Active volume: 50-500 cm³ for spectroscopy
4. Cooling requirement: Band gap E_g = 0.67 eV (Ge) at 300 K
   Thermal excitation rate ∝ exp(-E_g/2kT)
   At 300 K: Leakage current swamps signal
   At 77 K: Leakage negligible, detector operable
   LN₂ dewar: 30-50 L capacity, 1-2 week hold time
5. Charge collection: Electrons and holes drift to electrodes
   Drift velocity v_d = μE where μ = mobility, E = field
   Collection time: t_c ≈ d²/(μV) ~ 100 ns for 5 cm detector
   Incomplete collection degrades resolution (ballistic deficit)
6. Dead layer: Outer contact region (0.3-0.5 mm)
   Attenuates low-energy photons (<50 keV)
   Thin-window detectors for X-ray spectroscopy
7. Peak-to-Compton ratio: Merit figure for spectroscopy
   High-efficiency detectors: P/C ≈ 60:1 at 1.33 MeV
   Indicates good photoelectric absorption vs scattering
8. Silicon detectors: Room temperature operation
   E_g = 1.1 eV (larger gap than Ge)
   Applications: Charged particle spectroscopy (α, β, proton)
   X-ray fluorescence (thin-window Si(Li) or SDD)
   Thickness: 0.3-5 mm (charged particles stopped, gammas inefficient)
9. Passivated implanted planar silicon (PIPS):
   Alpha spectroscopy standard
   Resolution: 12-20 keV FWHM (pulse height defect for heavy ions)
   Thin dead layer (<0.1 μm), large area (up to 5000 mm²)
10. Silicon drift detector (SDD): X-ray spectroscopy
    Integrated FET, Peltier cooling sufficient
    Energy resolution: 130 eV at 5.9 keV (Mn K-alpha)
    Count rate: >10⁵ cps (vs 10⁴ for Si(Li))
""",
        key_factors=[
            "W-value of 3 eV enables 300,000 charge pairs per MeV",
            "Fano factor 0.13 reduces statistical spread",
            "Energy resolution 0.2% at 1.33 MeV (10× better than NaI)",
            "HPGe requires liquid nitrogen cooling",
            "Silicon operates at room temperature for charged particles",
            "Depletion depth determines active volume",
            "Peak-to-Compton ratio indicates spectroscopy quality"
        ],
        primary_authority=[
            "Knoll, Radiation Detection and Measurement, Ch. 12-13",
            "Semiconductor Detector Systems, ORTEC Application Note AN34",
            "ANSI N42.14 - Gamma spectroscopy calibration"
        ],
        burden_holder="Analyst must maintain detector at 77 K and calibrate energy scale",
        adversary_position="Why need expensive LN₂ cooling system?",
        counter_arguments=[
            "Small band gap (0.67 eV) causes thermal leakage at room temperature",
            "Resolution improvement justifies operational complexity",
            "Alternatives (CdZnTe, SiC) exist but inferior performance"
        ],
        resolution_strategy="Apply semiconductor physics with temperature-dependent leakage current models",
        entity_scope="All semiconductor radiation detectors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established solid-state physics with 50+ years of detector development",
        controlling_precedent="HPGe development (1970s), Si(Li) theory"
    ),

    DoctrineBlock(
        topic="Radiation Dosimetry - Absorbed Dose and Equivalent Dose",
        keywords=["absorbed dose", "gray", "rad", "equivalent dose", "sievert", "rem", "quality factor", "dose equivalent", "RBE"],
        conclusion_template="Absorbed dose D (gray, Gy) measures energy deposited per unit mass: 1 Gy = 1 J/kg. Equivalent dose H (sievert, Sv) accounts for biological effectiveness via radiation weighting factor w_R: H = w_R × D. For photons/electrons w_R = 1, neutrons 5-20, alpha particles 20.",
        reasoning_framework="""
Dosimetric quantities and radiation protection framework:
1. Absorbed dose D: Energy imparted per unit mass
   SI unit: Gray (Gy) = 1 J/kg
   Traditional unit: Rad = 0.01 Gy = 1 cGy
   Measured quantity, instrument-readable
2. Exposure X: Ionization in air (historical quantity)
   Unit: Roentgen (R) = 2.58×10⁻⁴ C/kg air
   Conversion: 1 R ≈ 0.87 rad (air) ≈ 0.96 rad (tissue)
   Applies only to photons in air
3. Radiation weighting factor w_R (ICRP 103, 2007):
   Photons (all energies): w_R = 1
   Electrons/muons: w_R = 1
   Protons (>2 MeV): w_R = 2
   Alpha particles, fission fragments: w_R = 20
   Neutrons: w_R = 2.5 + 18.2×exp[-(ln(E_n))²/6] (continuous function)
     1 MeV neutrons: w_R ≈ 20
     Thermal neutrons: w_R ≈ 2.5
4. Equivalent dose H: H_T = Σw_R × D_T,R
   Accounts for radiation type biological effectiveness
   Unit: Sievert (Sv) = J/kg with biological weighting
   Traditional: Rem = 0.01 Sv
5. Effective dose E: Whole-body dose accounting for tissue sensitivity
   E = Σw_T × H_T where w_T = tissue weighting factor
   Brain/gonads: w_T = 0.08 (high sensitivity)
   Lung/stomach: w_T = 0.12
   Liver/bladder: w_T = 0.04
   Skin/bone surface: w_T = 0.01
   Sum of w_T = 1.0
6. Relative biological effectiveness (RBE):
   RBE = D_ref / D_test for same biological endpoint
   Reference radiation: 250 kVp X-rays or Co-60 gamma
   Depends on: Radiation type, dose, dose rate, endpoint
   Alpha RBE ≈ 10-20 for most endpoints
7. Linear energy transfer (LET):
   LET = -dE/dx (energy loss per unit path length)
   Units: keV/μm or MeV·cm²/g
   Photons/electrons: Low LET (~0.2 keV/μm in tissue)
   Protons: Medium LET (10-100 keV/μm)
   Alpha particles: High LET (100-200 keV/μm)
   High LET → more ionization per track → greater biological damage
8. Dose rate effects: Chronic vs acute exposure
   Dose rate effectiveness factor (DREF): ~2 for low-LET
   Low dose rates allow DNA repair → less damage per unit dose
   High-LET radiation: Minimal dose rate effect
9. Committed dose: 50-year integral for internal contamination
   H_committed = ∫₀⁵⁰ H(t) dt
   Accounts for biological half-life and radioactive decay
   Example: I-131 thyroid dose from single intake
10. Operational dose quantities (ICRU):
    Ambient dose equivalent H*(10) at 10 mm depth
    Personal dose equivalent Hp(10) at 10 mm body depth
    Directional dose equivalent H'(0.07) at 0.07 mm (skin)
""",
        key_factors=[
            "Absorbed dose measures energy deposition (physical quantity)",
            "Equivalent dose accounts for radiation quality (protection quantity)",
            "Effective dose accounts for tissue sensitivity (risk assessment)",
            "Radiation weighting factors range from 1 (photons) to 20 (alpha)",
            "LET correlates with biological effectiveness",
            "Dose rate effects significant for low-LET radiation",
            "Committed dose integrates internal contamination over 50 years"
        ],
        primary_authority=[
            "ICRP Publication 103 - 2007 Recommendations",
            "ICRU Report 51 - Quantities and Units in Radiation Protection",
            "10 CFR 20 - NRC Standards for Protection Against Radiation"
        ],
        burden_holder="Analyst must apply correct weighting factors and sum tissue doses",
        adversary_position="Why different dose quantities for same energy deposition?",
        counter_arguments=[
            "Biological damage depends on radiation quality, not just energy",
            "High-LET radiation causes dense ionization and complex DNA damage",
            "Protection standards must account for both physical and biological factors"
        ],
        resolution_strategy="Apply ICRP/ICRU dosimetric framework with appropriate weighting factors",
        entity_scope="All radiation exposure scenarios requiring dose assessment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="International consensus framework with regulatory adoption",
        controlling_precedent="ICRP recommendations, 10 CFR 20, ICRU reports"
    ),

    DoctrineBlock(
        topic="ALARA Principle and Radiation Protection Standards",
        keywords=["ALARA", "as low as reasonably achievable", "dose limit", "10 CFR 20", "occupational exposure", "public exposure", "time distance shielding"],
        conclusion_template="ALARA principle requires doses be kept as low as reasonably achievable, economic and social factors considered. 10 CFR 20 sets occupational limits: 50 mSv/yr (5 rem/yr) total effective dose, 500 mSv/yr (50 rem/yr) extremity dose. Public limit: 1 mSv/yr (100 mrem/yr). Optimization achieved via time, distance, and shielding.",
        reasoning_framework="""
Radiation protection philosophy and regulatory framework:
1. ALARA definition (10 CFR 20.1003):
   "As Low As Reasonably Achievable, taking into account the state of technology,
   economics of improvements in relation to state of technology, economics of
   improvements in relation to benefits to public health and safety, and other
   societal and socioeconomic considerations."
   Not just meeting limits, but optimizing to minimum practical dose
2. Regulatory dose limits (10 CFR 20.1201):
   Occupational workers:
     50 mSv/yr (5 rem/yr) total effective dose equivalent (TEDE)
     500 mSv/yr (50 rem/yr) shallow dose to skin or extremity
     150 mSv/yr (15 rem/yr) lens of eye
     50 mSv (5 rem) declared pregnant worker (entire gestation)
   Public (10 CFR 20.1301):
     1 mSv/yr (100 mrem/yr) TEDE
     0.02 mSv/hr (2 mrem/hr) in unrestricted area
3. Time-distance-shielding (TDS) optimization:
   Time: Minimize duration of exposure
     Dose ∝ time: D = D_rate × t
     Pre-plan tasks, practice with mockups, use remote tools
   Distance: Inverse square law for point sources
     D ∝ 1/r²: Doubling distance reduces dose by factor 4
     Use long-handled tools, remote manipulators
   Shielding: Interpose attenuating material
     Exponential attenuation: I = I₀ × e^(-μx)
     Select material by radiation type (Pb for γ, plastic for β, polyethylene for n)
4. Half-value layer (HVL): Thickness reducing intensity by 50%
   HVL = ln(2)/μ = 0.693/μ
   Gamma rays in lead:
     100 keV: HVL ≈ 0.03 mm
     500 keV: HVL ≈ 4 mm
     1 MeV: HVL ≈ 8 mm
     2 MeV: HVL ≈ 11 mm
   Number of HVLs: n = log₂(I₀/I) = 3.32 × log₁₀(I₀/I)
5. Tenth-value layer (TVL): Reduces intensity by factor 10
   TVL = ln(10)/μ = 2.303/μ ≈ 3.32 × HVL
   Concrete for 1 MeV gamma: TVL ≈ 16 inch
   Lead for 1 MeV gamma: TVL ≈ 1.6 inch
6. Dose rate calculations: Point source approximation
   Ḋ(r) = (A × Γ) / r² where Γ = specific gamma constant
   Γ for Co-60: 1.32 R·m²/(hr·Ci) or 0.35 mSv·m²/(hr·GBq)
   Example: 1 Ci Co-60 at 1 meter → 1.32 R/hr ≈ 13 mSv/hr
7. Contamination control:
   Surface limits (10 CFR 20.1402):
     Total: 5000 dpm/100 cm² beta-gamma
     Removable: 1000 dpm/100 cm² beta-gamma
     Transuranics: 100/20 dpm/100 cm² (total/removable)
   Airborne limits (10 CFR 20 Appendix B): DAC values
     Derived air concentration: Activity concentration in air
     Example: H-3 DAC = 2×10⁻⁵ μCi/mL = 0.7 MBq/m³
8. Bioassay and internal dosimetry:
   Annual limit on intake (ALI): Activity causing 50 mSv committed dose
   Derived air concentration: DAC = ALI / (2000 hr × 1.2 m³/hr)
   Whole-body counting: In-vivo measurement of gamma emitters
   Urinalysis/fecal analysis: Chemical separation for alpha emitters
9. Posting and labeling (10 CFR 20.1902-1903):
   Radiation area: >5 mrem/hr (0.05 mSv/hr) at 30 cm
   High radiation area: >100 mrem/hr (1 mSv/hr)
   Very high radiation area: >500 rad/hr (5 Gy/hr) at 1 meter
   Airborne radioactivity area: >1 DAC or 12 DAC-hours/week
10. Optimization techniques:
    Collective dose: Person-sievert for worker groups
    Cost-benefit analysis: α = Δcost / Δdose ($/person-Sv)
    Typical α: $10,000-100,000 per person-Sv averted
    ALARA investigations: Doses exceeding administrative limits
""",
        key_factors=[
            "ALARA requires optimization beyond mere compliance with limits",
            "Occupational limit 50 mSv/yr, public limit 1 mSv/yr",
            "Time-distance-shielding triad for dose reduction",
            "Inverse square law applies to point source geometry",
            "HVL and TVL quantify shielding effectiveness",
            "Surface and airborne contamination limits prevent intake",
            "Cost-benefit analysis guides ALARA implementation"
        ],
        primary_authority=[
            "10 CFR Part 20 - Standards for Protection Against Radiation",
            "ICRP Publication 103 - 2007 Recommendations",
            "Regulatory Guide 8.10 - Operating Philosophy for ALARA"
        ],
        burden_holder="Licensee must demonstrate ALARA program and document optimization efforts",
        adversary_position="Why optimize below regulatory limits?",
        counter_arguments=[
            "Linear no-threshold (LNT) model: No safe dose exists",
            "Collective dose reduction has societal benefit",
            "Regulatory requirement per 10 CFR 20.1101(b)"
        ],
        resolution_strategy="Implement TDS optimization with documented cost-benefit analysis",
        entity_scope="All licensed radioactive material users and radiation-producing devices",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory standard with 50+ years of implementation experience",
        controlling_precedent="10 CFR Part 20 (1991 revision), ICRP recommendations"
    ),

    DoctrineBlock(
        topic="Shielding Calculations - Attenuation and Buildup",
        keywords=["linear attenuation", "mass attenuation", "buildup factor", "broad beam", "narrow beam", "effective atomic number", "shielding design"],
        conclusion_template="Gamma ray attenuation follows I = I₀ × e^(-μx) for narrow beam geometry. Broad beam requires buildup factor B accounting for scattered radiation: I = I₀ × B × e^(-μx). Buildup factor depends on material atomic number, gamma energy, and shield thickness in mean free paths.",
        reasoning_framework="""
Photon shielding theory and engineering calculations:
1. Linear attenuation coefficient μ (cm⁻¹):
   Probability per unit path length of interaction
   μ = μ_photoelectric + μ_Compton + μ_pair
   Energy-dependent: μ decreases with E (Compton dominates 0.2-2 MeV)
   Then increases for pair production (E > 1.022 MeV)
2. Mass attenuation coefficient μ/ρ (cm²/g):
   Independent of physical density (compares materials)
   Narrow beam attenuation: I/I₀ = exp(-μx) = exp[-(μ/ρ)×ρx]
   NIST XCOM database: Tabulated μ/ρ for all elements and compounds
3. Mean free path: λ = 1/μ
   Average distance to first interaction
   For 1 MeV gamma in lead: μ = 0.77 cm⁻¹, λ = 1.3 cm
   Shield thickness often expressed in MFP units
4. Buildup factor B(μx, E, Z):
   Accounts for scattered photons reaching detector
   Narrow beam: Only unscattered photons (good geometry)
   Broad beam: Includes single and multiple scatters
   Taylor buildup: B ≈ 1 + μx (simple approximation)
   Berger form: B = A₁ × e^(-α₁μx) + A₂ × e^(-α₂μx) (two-parameter)
5. ANSI/ANS-6.4.3 buildup factor database:
   23 elements and 3 mixtures (air, concrete, water)
   Energies: 0.015-15 MeV
   Depths: 0.5-40 mean free paths
   Exposure and energy absorption buildup
6. Effective atomic number for mixtures:
   Z_eff = [Σwᵢ × Zᵢ^n]^(1/n) where n ≈ 2.94 for buildup
   Concrete (Z_eff ≈ 11): Interpolate between Al and Si data
   Used to estimate buildup when mixture data unavailable
7. Point kernel integration for extended sources:
   D(r) = ∫∫∫ [S(r') × B(μR, E) × e^(-μR)] / (4πR²) dV'
   S(r') = source strength distribution
   R = distance from volume element to dose point
   Numerical integration required for complex geometries
8. Multilayer shields: Product of transmission factors
   T_total = T₁ × T₂ × ... × T_n
   Buildup: Use material properties where most scattering occurs
   Graded shields: High-Z inner (stop high E), low-Z outer (stop bremsstrahlung)
9. Skyshine: Scattered radiation over barriers
   Important for outdoor accelerators, reactor facilities
   Requires Monte Carlo or specific skyshine codes (e.g., ISOSHLD)
10. Common shield materials and properties (1 MeV gamma):
    Lead: ρ = 11.3 g/cm³, μ = 0.77 cm⁻¹, HVL = 0.9 cm
    Iron: ρ = 7.87 g/cm³, μ = 0.47 cm⁻¹, HVL = 1.5 cm
    Concrete: ρ = 2.3 g/cm³, μ = 0.15 cm⁻¹, HVL = 4.6 cm
    Water: ρ = 1.0 g/cm³, μ = 0.071 cm⁻¹, HVL = 9.8 cm
""",
        key_factors=[
            "Exponential attenuation for narrow beam geometry",
            "Buildup factor accounts for scattered photons in broad beams",
            "μ/ρ enables material comparison independent of density",
            "Mean free path quantifies interaction probability",
            "ANSI/ANS-6.4.3 provides standardized buildup data",
            "Point kernel integration for complex source geometries",
            "Shield effectiveness depends on Z and thickness"
        ],
        primary_authority=[
            "ANSI/ANS-6.4.3 - Gamma-Ray Attenuation Coefficients and Buildup Factors",
            "NIST XCOM - Photon Cross Sections Database",
            "Shultis & Faw, Radiation Shielding (2000)"
        ],
        burden_holder="Shielding designer must calculate transmission with buildup factors",
        adversary_position="Why can't we just use exponential attenuation?",
        counter_arguments=[
            "Scattered photons contribute significantly in realistic geometries",
            "Buildup factor can be 2-10× for thick shields",
            "Regulatory calculations require buildup per ANSI/ANS-6.4.3"
        ],
        resolution_strategy="Apply narrow beam attenuation with appropriate buildup factors for geometry",
        entity_scope="All gamma ray shielding design and verification",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established radiation transport theory with standardized calculation methods",
        controlling_precedent="ANSI/ANS-6.4.3 standard, NCRP Report 151"
    ),

    DoctrineBlock(
        topic="Nuclear Waste Classification and Management",
        keywords=["low level waste", "intermediate level waste", "high level waste", "spent fuel", "TRU waste", "greater than class C", "disposal pathway"],
        conclusion_template="Nuclear waste classified by activity and heat generation. Low-level waste (LLW, Classes A-C) disposed in near-surface facilities. Transuranic waste (>100 nCi/g, >5730 yr half-life) requires geologic disposal (WIPP). High-level waste (HLW) from reprocessing or spent fuel requires shielding and cooling before disposal in deep geologic repository.",
        reasoning_framework="""
Nuclear waste categorization and disposal pathways:
1. Low-level waste (LLW, 10 CFR 61):
   Class A: Lowest activity, shortest half-lives
     Segregation not required
     Limits: C-14 <0.8 Ci/m³, Ni-63 <3.5 Ci/m³
     Example: Contaminated tools, protective clothing
   Class B: Intermediate activity
     Stability required if disposed without intruder barrier
     Limits: C-14 <8 Ci/m³, Ni-63 <70 Ci/m³
     Example: Ion exchange resins, contaminated equipment
   Class C: Highest LLW activity
     Requires intruder barrier for 500 years
     Limits: C-14 <80 Ci/m³, Ni-63 <700 Ci/m³
     Example: Activated reactor components
   Greater than Class C (GTCC): Exceeds Class C limits
     Not suitable for near-surface disposal
     DOE responsibility for commercial GTCC
2. Transuranic (TRU) waste (10 CFR 71.4):
   Definition: >100 nCi/g of alpha-emitting transuranics (Z > 92, t₁/₂ > 20 yr)
   Includes: Pu-238, Pu-239, Pu-240, Am-241, Cm-244
   Sources: Weapons production (Rocky Flats), fuel reprocessing
   Disposal: Waste Isolation Pilot Plant (WIPP), Carlsbad, NM
     2150 ft underground in Permian salt formation
     Contact-handled TRU: <200 mrem/hr surface dose
     Remote-handled TRU: >200 mrem/hr, requires shielding
3. High-level waste (HLW):
   Definition: Highly radioactive material from reprocessing
   Commercial HLW: Spent nuclear fuel (SNF) or reprocessing waste
   Defense HLW: Reprocessing of weapons production fuel
   Characteristics:
     Activity: 10⁶-10⁹ Ci/m³
     Heat generation: Requires active or passive cooling
     Radiation: Requires remote handling and heavy shielding
     Long-lived isotopes: Cs-137, Sr-90 (30 yr), transuranics (10³-10⁶ yr)
4. Spent nuclear fuel composition:
   PWR fuel: 33 GWd/MTU burnup, 10 year cooling
     U-238: 94.5%, U-235: 0.8%, Pu: 1.0%, fission products: 3.5%
     Activity: ~10⁶ Ci/MTU (dominated by Cs-137, Sr-90)
     Decay heat: 1-2 kW/MTU (requires cooling)
   Decay stages:
     0-10 yr: Fission products (Cs-137, Sr-90) dominate
     10-500 yr: Transition to transuranic dominance
     >500 yr: Long-lived actinides (Pu-239, Am-241) dominate
5. Waste disposal facilities:
   LLW: Barnwell (SC), Clive (UT), Andrews County (TX), Richland (WA)
   TRU: WIPP (operational since 1999)
   HLW/SNF: Yucca Mountain (NV, license pending)
     Deep geologic repository in volcanic tuff
     Engineered barriers: Waste form, canister, drip shield
     Natural barriers: 300 m unsaturated zone, arid climate
6. Waste treatment and conditioning:
   Volume reduction: Compaction, incineration, evaporation
   Solidification: Cement, bitumen, polymer encapsulation
   Vitrification: HLW incorporated into borosilicate glass
     Reduces leachability, stable waste form
     Savannah River Defense Waste Processing Facility
7. Regulatory framework:
   10 CFR 61: Land disposal of LLW
   10 CFR 63: Yucca Mountain licensing (proposed)
   40 CFR 191: EPA environmental standards for disposal
   40 CFR 197: Yucca Mountain compliance criteria
8. Disposal performance requirements:
   10 CFR 61: 500-year intruder protection for Class C
   40 CFR 191: <15 mrem/yr to maximally exposed individual
   10,000-year compliance period for geologic disposal
9. Alternative disposal concepts:
   Deep borehole: 3-5 km depth in crystalline basement rock
   Seabed disposal: Abyssal clay, international moratorium
   Subduction zone: Ocean trench, technically infeasible
   Transmutation: Accelerator-driven systems to reduce long-lived inventory
10. NORM waste (oilfield context):
    Ra-226, Ra-228 concentrated in scale and sludge
    Exempt from NRC if <5 pCi/g (state-regulated)
    TENORM (Technologically Enhanced NORM): Requires special disposal
    West Texas: Significant NORM in Permian Basin production equipment
""",
        key_factors=[
            "Waste classification drives disposal pathway",
            "LLW Classes A-C based on activity and half-life limits",
            "TRU waste requires geologic disposal (WIPP)",
            "HLW generates heat and requires shielding for centuries",
            "Spent fuel decay heat decreases exponentially (1-2 kW/MTU at 10 yr)",
            "Multiple barriers (engineered and natural) for long-term isolation",
            "10,000-year compliance period for HLW disposal"
        ],
        primary_authority=[
            "10 CFR Part 61 - Licensing Requirements for Land Disposal of Radioactive Waste",
            "40 CFR Part 191 - Environmental Radiation Protection Standards",
            "Blue Ribbon Commission on America's Nuclear Future (2012)"
        ],
        burden_holder="Waste generator must classify waste and select appropriate disposal pathway",
        adversary_position="How can we guarantee safety for 10,000 years?",
        counter_arguments=[
            "Multiple independent barrier systems",
            "Natural analogs (Oklo reactor) demonstrate long-term containment",
            "Performance assessment models validated against short-term monitoring"
        ],
        resolution_strategy="Apply waste classification criteria per 10 CFR 61 and select disposal pathway matching waste hazard",
        entity_scope="All radioactive waste from nuclear fuel cycle and medical/industrial uses",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory framework with 40+ years of LLW disposal experience, limited HLW experience",
        controlling_precedent="10 CFR 61 (1982), WIPP opening (1999)"
    ),

    DoctrineBlock(
        topic="Neutron Activation Analysis (NAA)",
        keywords=["neutron activation", "thermal neutrons", "activation cross section", "prompt gamma", "delayed gamma", "INAA", "RNAA"],
        conclusion_template="Neutron activation analysis (NAA) uses neutron capture to produce radioactive isotopes for trace element detection. Thermal neutron flux (10¹²-10¹⁴ n/cm²/s) in research reactor induces (n,γ) reactions. Instrumental NAA (INAA) achieves ppb-ppm sensitivity for 70+ elements via gamma spectroscopy of activation products.",
        reasoning_framework="""
Neutron activation mechanisms and analytical applications:
1. Activation reaction: ᴬX + n → ᴬ⁺¹X* → ᴬ⁺¹X + γ (prompt) + β⁻ (delayed)
   Target nucleus captures thermal neutron (~0.025 eV)
   Compound nucleus de-excites via prompt gamma emission
   Product nucleus may be radioactive (beta decay with delayed gammas)
2. Activation equation: A = N × σ × φ × [1 - e^(-λt_irr)] × e^(-λt_decay)
   N = number of target atoms
   σ = activation cross section (barns, 10⁻²⁴ cm²)
   φ = neutron flux (n/cm²/s)
   t_irr = irradiation time
   λ = decay constant of product
   Optimum t_irr ≈ 1-2 half-lives of product
3. Thermal neutron cross sections (examples):
   Au-197: σ = 98.7 b → Au-198 (2.7 days)
   Mn-55: σ = 13.3 b → Mn-56 (2.6 hr)
   Na-23: σ = 0.53 b → Na-24 (15 hr)
   Co-59: σ = 37 b → Co-60 (5.27 yr)
   Cl-35: σ = 43.6 b → Cl-36 (3.0×10⁵ yr)
4. Instrumental NAA (INAA): No chemical separation
   Sample irradiation in reactor (minutes to days)
   Cooling period to allow short-lived interferences to decay
   Gamma spectroscopy with HPGe detector
   Multi-element analysis: Identify elements by photopeak energy
   Quantification: Compare to standards or k₀ method
5. Radiochemical NAA (RNAA): Chemical separation after activation
   Removes matrix interferences
   Concentrates analytes of interest
   Enables determination of elements with low cross-sections
   Example: Rare earths separation by ion exchange
6. Prompt gamma NAA (PGNAA): Measure gammas during irradiation
   Cold neutron beam (reactor or spallation source)
   Detects elements with stable products: H, B, C, N, S, Cd
   Non-destructive, real-time analysis
   Applications: Cement, coal, ore analysis
7. Sensitivity and detection limits:
   Absolute method: Detection limit ∝ 1/(σ × φ)
   Relative method: Compare to known standard
   Typical detection limits (1 hr irradiation, 10¹³ n/cm²/s):
     Au: 0.001 μg/g (1 ppb)
     Mn: 0.01 μg/g
     Na: 0.1 μg/g
     Fe: 1 μg/g
   Depends on: Cross section, flux, half-life, gamma yield, interferences
8. Interferences and corrections:
   Spectral interferences: Photopeaks overlap (e.g., As-76/Sc-46 at 1121 keV)
   Activation interferences: Multiple reactions produce same isotope
   Matrix effects: Self-shielding of neutrons, self-absorption of gammas
   Fission product contamination: U/Th in sample produces fission gammas
9. Advantages of NAA:
   Multi-element capability (70+ elements)
   High sensitivity (ppb-ppt for some elements)
   Small sample size (10-100 mg)
   Non-destructive (INAA)
   Matrix-independent (standards need not match sample composition)
   Minimal sample preparation
10. Applications:
    Geology: REE patterns in rocks, meteorite classification
    Archaeology: Pottery provenance, tool stone sourcing
    Forensics: Gunshot residue (Sb, Ba), hair analysis
    Environmental: Trace pollutants in air filters, sediments
    Biology: Essential elements in tissue, selenium in food
    Semiconductor: Ultra-trace impurities in Si wafers
""",
        key_factors=[
            "Thermal neutron capture produces radioactive isotopes",
            "Activation rate proportional to cross section and neutron flux",
            "HPGe gamma spectroscopy identifies and quantifies products",
            "INAA enables non-destructive multi-element analysis",
            "Detection limits in ppb-ppm range for many elements",
            "k₀ standardization method avoids matrix-matched standards",
            "Interferences require spectral deconvolution or chemical separation"
        ],
        primary_authority=[
            "Alfassi, Activation Analysis (1990)",
            "Glascock, MURR NAA Laboratory Procedures Manual",
            "IAEA Technical Report 278 - Quality control in NAA"
        ],
        burden_holder="Analyst must select irradiation parameters and resolve spectral interferences",
        adversary_position="Why use reactor when ICP-MS faster and cheaper?",
        counter_arguments=[
            "NAA truly non-destructive for solids (INAA)",
            "No dissolution errors for refractory materials",
            "Superior for volatile elements (As, Sb, Hg)",
            "Unaffected by matrix effects plaguing ICP-MS"
        ],
        resolution_strategy="Apply activation equations with optimized irradiation and decay times",
        entity_scope="All elements with suitable (n,γ) cross sections and product half-lives",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Mature analytical technique with 60+ years of method development",
        controlling_precedent="NAA development (1930s), reactor NAA standardization (1960s)"
    ),

    DoctrineBlock(
        topic="PUREX Process and Spent Fuel Reprocessing",
        keywords=["PUREX", "plutonium uranium extraction", "tributyl phosphate", "TBP", "REDOX", "reprocessing", "partitioning"],
        conclusion_template="PUREX (Plutonium Uranium Redox EXtraction) process separates U and Pu from spent fuel via solvent extraction with tributyl phosphate (TBP) in kerosene. Nitric acid dissolution, oxidation state adjustment (Pu⁴⁺ extractable, Pu³⁺ remains aqueous), and sequential stripping recover >99.5% U and Pu. Raffinates contain fission products and minor actinides.",
        reasoning_framework="""
PUREX chemistry and reprocessing flowsheet:
1. Head-end operations: Fuel disassembly and dissolution
   Chop-leach: Fuel rods chopped, Zircaloy cladding discarded
   Dissolution: UO₂ + 8HNO₃ → UO₂(NO₃)₂ + 2NO₂ + 4H₂O
   Clarification: Undissolved solids removed (cladding hulls, noble metals)
   Feed adjustment: 3-4 M HNO₃, addition of salting agents
2. Solvent extraction principles:
   Extractant: 30% tributyl phosphate (TBP) in kerosene diluent
   Mechanism: Neutral complexes extracted into organic phase
     UO₂²⁺ + 2NO₃⁻ + 2TBP ⇌ UO₂(NO₃)₂·2TBP (organic)
     Pu⁴⁺ + 4NO₃⁻ + 2TBP ⇌ Pu(NO₃)₄·2TBP (organic)
   Distribution coefficient D = [M]_org / [M]_aq
   Separation factor β = D_A / D_B
3. Oxidation state control:
   Pu⁴⁺: Extractable (high D value)
   Pu³⁺: Inextractable (remains in aqueous phase)
   Pu⁶⁺: Extractable but less stable
   Redox adjustment:
     Oxidation: NaNO₂ converts Pu³⁺ → Pu⁴⁺
     Reduction: Hydroxylamine nitrate (HAN), U⁴⁺, or Fe²⁺ converts Pu⁴⁺ → Pu³⁺
4. PUREX flowsheet stages:
   Co-decontamination cycle:
     Feed + TBP/kerosene → U and Pu extracted, fission products in raffinate
     Scrub with HNO₃ to remove entrained fission products
     Partition: Reduce Pu⁴⁺ → Pu³⁺ with U⁴⁺, Pu strips to aqueous
   Uranium purification cycle:
     Re-extract U from organic, scrub, strip to product
     Final product: UO₂(NO₃)₂ (99.9% pure)
   Plutonium purification cycle:
     Oxidize Pu³⁺ → Pu⁴⁺, extract into TBP
     Strip to HNO₃, adjust to Pu(NO₃)₄ (99.9% pure)
5. Decontamination factors (DF):
   DF = (activity in feed) / (activity in product)
   Typical PUREX performance:
     U decontamination: DF > 10⁷ for fission products
     Pu decontamination: DF > 10⁶
     U/Pu separation: DF > 10⁵
6. High-level waste (raffinate):
   Contains 99% of fission products (Cs-137, Sr-90, Ru-106)
   Minor actinides: Np-237, Am-241, Cm-244 (not extracted)
   Highly acidic (3-5 M HNO₃), highly radioactive
   Treatment: Neutralization, calcination, vitrification
   Volume reduction: ~1000× via calcination and glass incorporation
7. TBP degradation and solvent cleanup:
   Radiolysis: TBP → dibutyl phosphate (DBP), monobutyl phosphate (MBP)
   DBP forms stable complexes, degrades separation
   Solvent washing: Na₂CO₃ solution removes degradation products
   Solvent recycle: Distillation to recover TBP
8. Alternative processes:
   THOREX: Thorium fuel reprocessing (Th → U-233)
   REDOX: Hexone solvent, obsolete (fire hazard)
   DIAMEX: Diamide extractants for minor actinide separation
   TRUEX: TRU (transuranic) extraction for waste treatment
9. Partitioning and transmutation (P&T):
   Advanced fuel cycles: Separate minor actinides
   Transmutation: Neutron bombardment converts long-lived → short-lived
   UREX+: Variations on PUREX for separations without pure Pu product
   Goal: Reduce long-term radiotoxicity of HLW
10. Proliferation concerns:
    PUREX produces separated weapons-usable Pu
    IAEA safeguards: Material accountancy, containment/surveillance
    Burnup credit: High Pu-240 content (reactor-grade) undesirable for weapons
    Alternative cycles: Thorium, pyroprocessing (proliferation-resistant claims)
""",
        key_factors=[
            "TBP/kerosene selectively extracts U and Pu from nitric acid",
            "Pu oxidation state controls extraction and stripping",
            "Co-decontamination cycle removes >99.9% fission products",
            "Sequential partitioning separates U and Pu to high purity",
            "Raffinate contains fission products and minor actinides",
            "Solvent degradation requires cleanup via washing",
            "Decontamination factors >10⁷ for uranium product"
        ],
        primary_authority=[
            "Benedict, Pigford, Levi, Nuclear Chemical Engineering (1981)",
            "Nash & Lumetta, Advanced Separation Techniques for Nuclear Fuel Reprocessing (2011)",
            "IAEA Technical Report 427 - PUREX Process"
        ],
        burden_holder="Process operator must maintain oxidation states and achieve target DFs",
        adversary_position="Why reprocess when once-through fuel cycle available?",
        counter_arguments=[
            "Closes fuel cycle, reduces natural uranium requirements",
            "Reduces HLW volume via actinide removal",
            "Counter: Proliferation risk, economics unfavorable vs enrichment"
        ],
        resolution_strategy="Apply solvent extraction theory with redox chemistry control",
        entity_scope="Spent nuclear fuel reprocessing plants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established industrial process with 60+ years of operational experience (France, UK, Russia)",
        controlling_precedent="PUREX development (1950s), La Hague and Sellafield plants"
    ),

    DoctrineBlock(
        topic="NORM in Oil and Gas Operations",
        keywords=["NORM", "naturally occurring radioactive material", "radium 226", "radium 228", "scale", "sludge", "TENORM", "radon"],
        conclusion_template="Naturally occurring radioactive material (NORM) in oil and gas production concentrates Ra-226 (t₁/₂ = 1600 yr) and Ra-228 (t₁/₂ = 5.75 yr) in scale, sludge, and produced water. Permian Basin wells show Ra-226 concentrations up to 1000 pCi/g in scale, exceeding TENORM disposal thresholds (30 pCi/g Texas, 5 pCi/g federal). Workers face external gamma and radon progeny inhalation hazards during maintenance.",
        reasoning_framework="""
NORM occurrence, accumulation, and regulatory framework in oilfield:
1. Source of NORM: U-238 and Th-232 decay series in formations
   U-238 → Ra-226 (α, 1600 yr) → Rn-222 (α, 3.82 days) → Pb-210 (β, 22.3 yr)
   Th-232 → Ra-228 (β, 5.75 yr) → Th-228 (α, 1.91 yr) → Ra-224 (α, 3.66 days)
   Radium soluble in formation brines as Ra²⁺ or RaCl⁺ complexes
2. Scale formation mechanisms:
   Pressure/temperature changes: Solubility decreases
   Mixing of incompatible waters: Sulfate (seawater) + barium (formation water)
   Precipitation: BaSO₄ (barite), SrSO₄ (celestite), CaCO₃ (calcite)
   Ra²⁺ co-precipitates with Ba²⁺ (similar ionic radius)
   Concentration factor: 100-10,000× formation concentration
3. Sludge accumulation:
   Production equipment: Tanks, separators, heater-treaters
   Solids settle from produced water and crude
   Composition: Sand, clay, Fe/Mn oxides, carbonates, sulfides
   NORM adsorbs onto Fe/Mn oxides and clays
   Ra-228/Ra-226 ratio diagnostic of Th/U ratio in formation
4. Activity concentrations in Permian Basin (field data):
   Scale (barite):
     Ra-226: 10-1000 pCi/g (0.4-40 kBq/kg)
     Ra-228: 2-200 pCi/g
     Total: Up to 1200 pCi/g reported
   Sludge (tank bottoms):
     Ra-226: 5-500 pCi/g
     Pb-210: 10-1000 pCi/g (grows in from Ra-226 decay)
   Produced water:
     Ra-226 + Ra-228: 100-5000 pCi/L
     Radon-222: 500-20,000 pCi/L (dissolved gas)
5. Exposure pathways:
   External gamma: Ra-226 daughters (Pb-214, Bi-214 emit 0.3-2 MeV gammas)
     Dose rate: 1-100 mrem/hr at contact with high-activity scale
     Inverse square law: Distance reduces exposure
   Radon inhalation: Rn-222 gas emanates from scale/sludge
     Equilibrium with Ra-226: Activity_Rn = Activity_Ra (if sealed)
     Progeny attach to dust: Po-218, Pb-214, Bi-214, Po-214
     Working level (WL): Any combination of short-lived progeny in 1 L air
       with 1.3×10⁵ MeV potential alpha energy
     Occupational limit: 4 WLM/yr (working level months)
   Ingestion/inhalation of dust: Ra-226 incorporated into bone
     ALI for Ra-226: 0.2 μCi (7.4 kBq) by ingestion
6. Regulatory thresholds:
   NRC exempt: <5 pCi/g Ra-226 + Ra-228 (10 CFR 20.1003)
   Texas NORM Rule: 30 pCi/g threshold for NORM waste designation
   Louisiana: 5 pCi/g above background
   North Dakota: 50 pCi/g for disposal in oilfield waste facility
   TENORM (Technologically Enhanced NORM): Human activity concentrates
7. Survey and characterization:
   Field screening: Ludlum Model 44-9 pancake GM probe
   Laboratory gamma spectroscopy: HPGe analysis for Ra-226, Ra-228, Pb-210
   Emanation method: Seal sample, measure Rn-222 after equilibrium (21 days)
   Swipe tests: Removable contamination (2000 dpm/100 cm² action level)
8. Waste management:
   Cleaning: High-pressure water jetting, chemical cleaning (EDTA, acids)
   Volume reduction: Separate high-activity scale from low-activity debris
   Disposal options:
     <30 pCi/g (Texas): Oilfield waste disposal facility
     >30 pCi/g: Exempt or licensed radioactive waste facility
     Injection: Dispose in Class II injection well (if approved)
   Reuse: Barite scale recycled to weighting material (if <5 pCi/g)
9. Worker protection:
   Respiratory protection: P100 filters for dust, supplied air for high radon
   Time-distance-shielding: Minimize duration, maximize distance, shield pipes
   Ventilation: Dilute radon to <10% DAC (30 pCi/L annual average)
   Training: NORM awareness, survey techniques, safe handling
10. West Texas NORM hotspots:
    Permian Basin formations: Devonian, Mississippian, Pennsylvanian
    High salinity brines (>200,000 ppm TDS) correlate with high NORM
    Older fields: Decades of accumulation in infrastructure
    Tank batteries: Sludge in gun barrels, wash tanks
    Water disposal: Scale in injection wells, surface equipment
""",
        key_factors=[
            "Ra-226 and Ra-228 co-precipitate with barium sulfate scale",
            "Concentration factors 100-10,000× over formation water",
            "Scale activities range 10-1000 pCi/g in Permian Basin",
            "External gamma and radon progeny inhalation are primary hazards",
            "Regulatory thresholds: 5 pCi/g (federal), 30 pCi/g (Texas)",
            "Radon emanation from scale creates confined space hazard",
            "Pb-210 grows in from Ra-226 decay (22.3 yr half-life)"
        ],
        primary_authority=[
            "API RP 7G - Recommended Practice on Drilling Fluids Processing Systems",
            "IAEA Safety Report 34 - Radiation Protection and NORM Residues (2003)",
            "Texas NORM Rule 31 TAC §336 - Licensing of NORM Facilities"
        ],
        burden_holder="Operator must survey equipment, protect workers, and properly dispose NORM waste",
        adversary_position="Why regulate naturally occurring materials?",
        counter_arguments=[
            "Human activity concentrates NORM above natural levels (TENORM)",
            "Workers receive measurable doses during maintenance",
            "Radon in confined spaces can exceed occupational limits"
        ],
        resolution_strategy="Survey equipment with calibrated instruments, classify waste by activity, select disposal pathway per regulations",
        entity_scope="All oil and gas production and disposal operations with NORM potential",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established health physics practice with 30+ years of NORM regulation in oil states",
        controlling_precedent="Texas NORM Rule (1993), API guidance documents"
    ),

    DoctrineBlock(
        topic="Radiation Effects on Materials - Displacement Damage",
        keywords=["displacement damage", "displacements per atom", "DPA", "radiation embrittlement", "swelling", "reactor pressure vessel", "PKA"],
        conclusion_template="Energetic particles (neutrons >0.1 MeV, ions) create displacement cascades in crystalline materials. Cumulative damage measured in displacements per atom (DPA) causes hardening, embrittlement, swelling, and creep. Reactor pressure vessel embrittlement limits plant lifetime; surveillance programs track ΔT_NDT (nil-ductility transition temperature shift) vs fluence.",
        reasoning_framework="""
Atomic displacement mechanisms and material property degradation:
1. Primary knock-on atom (PKA): Incident particle transfers energy to lattice atom
   Threshold displacement energy E_d: ~25 eV for Fe, 40 eV for graphite
   If recoil energy T > E_d, atom displaced from lattice site
   High-energy PKA (T > 1 keV) creates displacement cascade
2. Displacement cascade evolution (picosecond timescale):
   Ballistic phase: PKA collides with neighbors, creating subcascades
   Thermal spike: Localized melting along cascade core
   Quench phase: Rapid cooling, defects freeze in
   Result: Frenkel pairs (vacancy + interstitial), clusters, loops
3. Displacements per atom (DPA): Cumulative damage metric
   DPA = ∫∫ σ_d(E) × φ(E) dE dt / N
   σ_d(E) = displacement cross section (calculated via NRT model)
   φ(E) = energy-dependent particle flux
   Typical LWR pressure vessel: 0.01-0.1 DPA over 40-year lifetime
   Fast reactor cladding: 100-200 DPA over lifetime
4. NRT (Norgett-Robinson-Torrens) model:
   Number of Frenkel pairs: ν = 0.8 × T / (2E_d)
   T = recoil energy from PKA
   Factor 0.8 accounts for recombination during cascade
5. Radiation hardening: Obstacle density increases
   Yield strength: Δσ_y ∝ √(N_d × d) (dispersed barrier hardening)
   N_d = defect density, d = defect size
   Irradiated steel: σ_y increases 50-200 MPa at 0.01 DPA
   Hardness increase correlates with embrittlement
6. Radiation embrittlement: Loss of ductility at low temperatures
   Nil-ductility transition temperature (NDT): Temperature above which ductile
   Shift: ΔT_NDT ∝ √(fluence) for reactor steels
   Typical shift: 50-150°C at 10¹⁹ n/cm² (E > 1 MeV)
   Mechanisms: Precipitation of Cu-rich clusters, matrix hardening
   Charpy V-notch test: Surveillance specimens measure impact energy vs T
7. Void swelling: Accumulation of vacancy clusters
   Interstitials prefer dislocations (bias), vacancies form voids
   Swelling: ΔV/V = 0.1-10% at 50-100 DPA (fast reactor)
   Temperature dependent: Peak swelling at ~0.4 T_m (melting point)
   Stainless steel 316: ~1% per DPA at 500°C
8. Irradiation creep: Stress-enhanced diffusion of defects
   Strain rate: dε/dt = B × σ × dDPA/dt
   Occurs at stresses below thermal creep threshold
   Important for fuel cladding dimensional stability
9. Reactor pressure vessel (RPV) surveillance:
   10 CFR 50 Appendix H: Fracture toughness requirements
   Surveillance capsules: Charpy specimens withdrawn periodically
   Fluence limits: Some plants approaching 10¹⁹ n/cm² license limit
   Mitigation: Low-leakage core loading patterns, annealing (Russian VVER)
10. Materials selection for radiation environments:
    Austenitic stainless steels: Good swelling resistance (fcc structure)
    Ferritic-martensitic steels: Lower swelling than austenitic
    Refractory metals (W, Mo): High melting point, low swelling
    SiC composites: Fusion reactor candidate, low activation
    Damage-resistant microstructures: Fine grain size, precipitate dispersion
""",
        key_factors=[
            "Displacement cascades create Frenkel pairs and clusters",
            "DPA quantifies cumulative displacement damage",
            "Radiation hardening increases yield strength and brittleness",
            "Embrittlement shifts NDT temperature upward",
            "Void swelling can reach 10% at 100 DPA in stainless steel",
            "RPV surveillance programs track ΔT_NDT vs neutron fluence",
            "Temperature strongly affects swelling (peak at 0.4 T_m)"
        ],
        primary_authority=[
            "Zinkle & Was, Acta Materialia 61 (2013) - Materials challenges in nuclear energy",
            "ASTM E693 - Standard Practice for Characterizing Neutron Exposures",
            "10 CFR 50 Appendix H - Reactor Vessel Material Surveillance Program"
        ],
        burden_holder="Reactor operator must track fluence and demonstrate RPV integrity",
        adversary_position="Can't we just build thicker pressure vessels?",
        counter_arguments=[
            "Embrittlement is a bulk property change, not just surface",
            "Thickness limited by thermal stress and fabricability",
            "Surveillance and low-leakage cores more cost-effective"
        ],
        resolution_strategy="Apply NRT model to calculate DPA, correlate with material property changes via empirical models",
        entity_scope="All structural materials in neutron radiation fields",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established radiation effects science with 60+ years of reactor materials data",
        controlling_precedent="NRT model (1975), RPV surveillance programs (1970s-present)"
    ),

    DoctrineBlock(
        topic="Monte Carlo Radiation Transport - MCNP Methods",
        keywords=["monte carlo", "MCNP", "random walk", "cross sections", "tallies", "variance reduction", "criticality"],
        conclusion_template="Monte Carlo N-Particle (MCNP) code simulates radiation transport via random sampling of interaction probabilities from cross section libraries. Particle histories tracked until absorption, escape, or cutoff energy. Tallies (flux, dose, reaction rate) estimated with statistical uncertainty ~1/√N where N = number of histories. Variance reduction techniques (splitting, Russian roulette, implicit capture) improve efficiency.",
        reasoning_framework="""
Monte Carlo transport theory and computational implementation:
1. Random walk concept: Simulate individual particle trajectories
   Start: Source particle sampled from distribution (position, direction, energy)
   Transport: Distance to next interaction: s = -ln(ξ)/Σ_t
     ξ = random number [0,1], Σ_t = total macroscopic cross section
   Interaction: Sample type (scatter, absorption, fission) from probabilities
     P_scatter = Σ_s/Σ_t, P_absorption = Σ_a/Σ_t, P_fission = Σ_f/Σ_t
   Continue: Scattered particle new direction/energy, repeat until termination
2. Cross section data: ENDF/B (Evaluated Nuclear Data File)
   Pointwise data: σ(E) tabulated at thousands of energy points
   Reaction channels: (n,γ), (n,2n), (n,f), (n,elastic), (n,inelastic)
   Thermal scattering: S(α,β) law for bound atoms (H₂O, graphite)
   MCNP libraries: ENDF/B-VII.1 (released 2011), continuous-energy
3. Tallies: Estimate physical quantities from histories
   F1: Surface current (particles/cm²)
   F2: Surface flux (particles/cm²)
   F4: Track-length flux in cell (particles/cm²)
   F5: Flux at point detector
   F6: Energy deposition (MeV/g)
   F7: Fission energy deposition
   F8: Pulse height (energy spectrum in detector)
   Multipliers: Apply reaction cross sections (e.g., dose response)
4. Statistical uncertainty: Central limit theorem
   Estimated mean: x̄ = (1/N) × Σxᵢ
   Standard deviation: s = √[(Σxᵢ² - Nx̄²)/(N-1)]
   Relative error: R = s/(x̄√N)
   Convergence: R ∝ 1/√N (double histories → √2 reduction in error)
   Target: R < 0.05 (5%) for reliable results, <0.01 for precision
5. Variance reduction: Improve figure of merit FOM = 1/(R²T)
   Analog Monte Carlo: No biasing, inefficient for deep penetration
   Implicit capture: Particle weight reduced instead of absorbed
     Weight after absorption: w' = w × (1 - Σ_a/Σ_t)
   Splitting/Russian roulette: Increase importance in critical regions
     Split particle entering shield (n → n+1 lower-weight particles)
     Roulette in unimportant regions (probabilistically kill particles)
   Weight windows: Automated splitting/roulette based on importance function
   Exponential transform: Bias direction toward detector
6. Criticality calculations (KCODE):
   Effective multiplication factor: k_eff
   Fission source iteration: Converge spatial distribution
   Shannon entropy: Measure source convergence (should stabilize)
   Discard initial cycles (default 50), run 200+ active cycles
   Standard deviation of k_eff: Typically 0.00050 (50 pcm) for well-converged
7. Geometry specification:
   Cells: Defined by Boolean combinations of surfaces
   Surfaces: Planes, spheres, cylinders, cones, tori (quadratic equations)
   Lattices: Hexagonal or rectangular for fuel assemblies
   Universe concept: Hierarchical geometry (cell-in-cell)
8. Materials and cross sections:
   ZAID format: ZZZAAA.nnc (Z=atomic number, A=mass number, nn=library ID, c=class)
   Example: 92235.80c = U-235, ENDF/B-VII.1 continuous-energy
   S(α,β) thermal libraries: lwtr.20t (light water), grph.10t (graphite)
   Natural element expansions: Mg (natural) → isotopic abundances
9. Output interpretation:
   Tally fluctuation chart (TFC): 10 statistical checks
     Mean, relative error, variance of variance (VOV), figure of merit (FOM)
     Slope of FOM vs history: Should approach 0 (constant efficiency)
   Physical reasonableness: Check for negative flux, energy conservation
   Mesh tallies: Superimpose Cartesian/cylindrical mesh for spatial detail
10. Applications in nuclear chemistry:
    Activation calculations: Track (n,γ) reactions, output to CINDER90
    Shielding design: Dose rates outside casks, hot cells
    Criticality safety: Verify k_eff < 0.95 for fissile material storage
    Detector response: Model NaI(Tl), HPGe pulse height spectra
    Radiography: Simulate neutron/gamma imaging
""",
        key_factors=[
            "Random sampling of cross sections simulates particle transport",
            "Statistical uncertainty decreases as 1/√N histories",
            "Tallies estimate flux, dose, reaction rates with confidence intervals",
            "Variance reduction improves efficiency without biasing results",
            "ENDF/B cross section libraries provide reaction probabilities",
            "k_eff criticality calculations require source convergence",
            "Monte Carlo gold standard for complex geometries"
        ],
        primary_authority=[
            "X-5 Monte Carlo Team, MCNP Users Manual (LA-UR-17-29981, 2017)",
            "Lux & Koblinger, Monte Carlo Particle Transport Methods (1991)",
            "ANSI/ANS-6.1.2 - Neutron and Gamma-Ray Flux-to-Dose-Rate Factors"
        ],
        burden_holder="Analyst must verify statistical convergence and validate geometry model",
        adversary_position="Why use statistical method when deterministic transport codes exist?",
        counter_arguments=[
            "Monte Carlo handles arbitrary 3D geometry without approximation",
            "Continuous-energy cross sections (no group collapse errors)",
            "Statistical uncertainty quantifiable and controllable"
        ],
        resolution_strategy="Apply Monte Carlo transport with variance reduction and verify statistical quality per TFC criteria",
        entity_scope="All radiation transport problems amenable to statistical simulation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Gold standard method with 70+ years of development and validation",
        controlling_precedent="MCNP development (Los Alamos, 1977-present), ANSI/ANS standards"
    ),
]


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

BANNED_PHRASES = [
    "will always", "will never", "guarantees", "absolutely certain",
    "impossible", "100% safe", "zero risk", "perfectly", "infinitely"
]

DISCLOSURE_TRIGGERS = [
    "novel material", "new isotope", "untested condition", "beyond design basis",
    "no experimental data", "extrapolation", "theoretical only"
]


# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

@dataclass
class QueryTelemetry:
    timestamp: str
    question: str
    mode: ResponseMode
    zone: AnalysisZone
    triggered_doctrines: List[str]
    response_time_ms: float
    confidence: ConfidenceLevel
    epistemic_flags: List[str]
    determinism_hash: str


class MetricsCollector:
    def __init__(self):
        self.query_count = 0
        self.total_response_time = 0.0
        self.doctrine_hit_counts: Dict[str, int] = {}
        self.confidence_distribution: Dict[ConfidenceLevel, int] = {
            ConfidenceLevel.DEFENSIBLE: 0,
            ConfidenceLevel.AGGRESSIVE: 0,
            ConfidenceLevel.DISCLOSURE: 0,
            ConfidenceLevel.HIGH_RISK: 0
        }

    def record_query(self, telemetry: QueryTelemetry):
        self.query_count += 1
        self.total_response_time += telemetry.response_time_ms
        for doctrine in telemetry.triggered_doctrines:
            self.doctrine_hit_counts[doctrine] = self.doctrine_hit_counts.get(doctrine, 0) + 1
        self.confidence_distribution[telemetry.confidence] += 1

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self.query_count,
            "avg_response_time_ms": self.total_response_time / max(1, self.query_count),
            "doctrine_coverage": len(self.doctrine_hit_counts),
            "confidence_distribution": {k.value: v for k, v in self.confidence_distribution.items()},
            "top_doctrines": sorted(self.doctrine_hit_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }


# ============================================================================
# CORE ENGINE
# ============================================================================

class CHEM12NuclearChemistryEngine:
    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.metrics = MetricsCollector()
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"
        logger.add(
            Path(__file__).parent / "chem12_nuclear.log",
            rotation="100 MB",
            retention="30 days",
            level="INFO"
        )
        logger.info("CHEM12 Nuclear Chemistry Engine initialized with {} doctrine blocks", len(self.doctrine_cache))

    def three_layer_response(self, question: str, mode: ResponseMode, zone: AnalysisZone) -> QueryResponse:
        start_time = time.time()

        # Layer 1: Doctrine cache (0-200ms)
        triggered_doctrines, cache_answer = self._search_doctrine_cache(question)

        if cache_answer and mode == ResponseMode.FAST:
            confidence = self._assess_confidence(triggered_doctrines, zone)
            reasoning = [f"Doctrine cache hit: {d.topic}" for d in triggered_doctrines[:3]]
            sources = self._extract_sources(triggered_doctrines)

            response_time = (time.time() - start_time) * 1000
            determinism_hash = self._compute_hash(question, cache_answer)

            epistemic_disclosure = self._check_epistemic_guardrails(cache_answer)

            telemetry = QueryTelemetry(
                timestamp=datetime.utcnow().isoformat(),
                question=question,
                mode=mode,
                zone=zone,
                triggered_doctrines=[d.topic for d in triggered_doctrines],
                response_time_ms=response_time,
                confidence=confidence,
                epistemic_flags=epistemic_disclosure or [],
                determinism_hash=determinism_hash
            )
            self.metrics.record_query(telemetry)
            self._write_audit_log(telemetry, cache_answer)

            return QueryResponse(
                answer=cache_answer,
                confidence=confidence,
                sources=sources,
                reasoning_chain=reasoning,
                triggered_doctrines=[d.topic for d in triggered_doctrines],
                response_time_ms=response_time,
                determinism_hash=determinism_hash,
                epistemic_disclosure=epistemic_disclosure[0] if epistemic_disclosure else None
            )

        # Layer 2: Semantic retrieval (200-2000ms)
        if mode in [ResponseMode.DEFENSE, ResponseMode.MEMO]:
            semantic_answer = self._semantic_search(question, triggered_doctrines)
            if semantic_answer:
                confidence = ConfidenceLevel.AGGRESSIVE if mode == ResponseMode.DEFENSE else ConfidenceLevel.DEFENSIBLE
                reasoning = [
                    f"Doctrine: {d.topic}" for d in triggered_doctrines[:3]
                ] + ["Semantic context applied"]

                response_time = (time.time() - start_time) * 1000
                determinism_hash = self._compute_hash(question, semantic_answer)
                epistemic_disclosure = self._check_epistemic_guardrails(semantic_answer)

                telemetry = QueryTelemetry(
                    timestamp=datetime.utcnow().isoformat(),
                    question=question,
                    mode=mode,
                    zone=zone,
                    triggered_doctrines=[d.topic for d in triggered_doctrines],
                    response_time_ms=response_time,
                    confidence=confidence,
                    epistemic_flags=epistemic_disclosure or [],
                    determinism_hash=determinism_hash
                )
                self.metrics.record_query(telemetry)
                self._write_audit_log(telemetry, semantic_answer)

                return QueryResponse(
                    answer=semantic_answer,
                    confidence=confidence,
                    sources=self._extract_sources(triggered_doctrines),
                    reasoning_chain=reasoning,
                    triggered_doctrines=[d.topic for d in triggered_doctrines],
                    response_time_ms=response_time,
                    determinism_hash=determinism_hash,
                    epistemic_disclosure=epistemic_disclosure[0] if epistemic_disclosure else None
                )

        # Layer 3: Deep analysis (only for MEMO mode)
        deep_answer = self._deep_analysis(question, triggered_doctrines, zone)
        confidence = ConfidenceLevel.DISCLOSURE
        reasoning = [
            f"Multi-doctrine analysis: {len(triggered_doctrines)} doctrines",
            "Deep synthesis applied",
            f"Zone-specific analysis: {zone.value}"
        ]

        response_time = (time.time() - start_time) * 1000
        determinism_hash = self._compute_hash(question, deep_answer)
        epistemic_disclosure = self._check_epistemic_guardrails(deep_answer)

        telemetry = QueryTelemetry(
            timestamp=datetime.utcnow().isoformat(),
            question=question,
            mode=mode,
            zone=zone,
            triggered_doctrines=[d.topic for d in triggered_doctrines],
            response_time_ms=response_time,
            confidence=confidence,
            epistemic_flags=epistemic_disclosure or [],
            determinism_hash=determinism_hash
        )
        self.metrics.record_query(telemetry)
        self._write_audit_log(telemetry, deep_answer)

        return QueryResponse(
            answer=deep_answer,
            confidence=confidence,
            sources=self._extract_sources(triggered_doctrines),
            reasoning_chain=reasoning,
            triggered_doctrines=[d.topic for d in triggered_doctrines],
            response_time_ms=response_time,
            determinism_hash=determinism_hash,
            epistemic_disclosure=epistemic_disclosure[0] if epistemic_disclosure else None
        )

    def _search_doctrine_cache(self, question: str) -> Tuple[List[DoctrineBlock], Optional[str]]:
        question_lower = question.lower()
        matches = []

        for doctrine in self.doctrine_cache:
            score = 0
            for keyword in doctrine.keywords:
                if keyword.lower() in question_lower:
                    score += 1

            if doctrine.topic.lower() in question_lower:
                score += 3

            if score > 0:
                matches.append((doctrine, score))

        matches.sort(key=lambda x: x[1], reverse=True)
        triggered = [m[0] for m in matches[:5]]

        if triggered and matches[0][1] >= 2:
            answer = triggered[0].conclusion_template
            return triggered, answer

        return triggered, None

    def _semantic_search(self, question: str, triggered_doctrines: List[DoctrineBlock]) -> Optional[str]:
        if not triggered_doctrines:
            return None

        # Synthesize from top 3 doctrines
        synthesis = []
        for doctrine in triggered_doctrines[:3]:
            synthesis.append(f"{doctrine.topic}: {doctrine.conclusion_template}")

        return " ".join(synthesis)

    def _deep_analysis(self, question: str, triggered_doctrines: List[DoctrineBlock], zone: AnalysisZone) -> str:
        if not triggered_doctrines:
            return "No relevant doctrine blocks found for this nuclear chemistry question."

        # Multi-doctrine synthesis with zone-specific framing
        analysis_parts = []

        if zone == AnalysisZone.PLANNING:
            analysis_parts.append("PLANNING ANALYSIS:")
        elif zone == AnalysisZone.REPORTING:
            analysis_parts.append("TECHNICAL REPORT:")
        else:
            analysis_parts.append("AUDIT DOCUMENTATION:")

        for i, doctrine in enumerate(triggered_doctrines[:5], 1):
            analysis_parts.append(f"\n{i}. {doctrine.topic}")
            analysis_parts.append(f"   {doctrine.conclusion_template}")
            analysis_parts.append(f"   Key factors: {'; '.join(doctrine.key_factors[:3])}")
            analysis_parts.append(f"   Authority: {doctrine.primary_authority[0]}")

        return "\n".join(analysis_parts)

    def _assess_confidence(self, triggered_doctrines: List[DoctrineBlock], zone: AnalysisZone) -> ConfidenceLevel:
        if not triggered_doctrines:
            return ConfidenceLevel.HIGH_RISK

        if zone == AnalysisZone.AUDIT:
            return ConfidenceLevel.DEFENSIBLE

        avg_confidence = sum(1 for d in triggered_doctrines if d.confidence == ConfidenceLevel.DEFENSIBLE)
        if avg_confidence >= len(triggered_doctrines) * 0.8:
            return ConfidenceLevel.DEFENSIBLE

        return ConfidenceLevel.AGGRESSIVE

    def _extract_sources(self, triggered_doctrines: List[DoctrineBlock]) -> List[str]:
        sources = set()
        for doctrine in triggered_doctrines[:5]:
            sources.update(doctrine.primary_authority)
        return sorted(sources)[:10]

    def _check_epistemic_guardrails(self, answer: str) -> Optional[List[str]]:
        flags = []

        for phrase in BANNED_PHRASES:
            if phrase.lower() in answer.lower():
                flags.append(f"Epistemic overreach: '{phrase}' should be qualified")

        for trigger in DISCLOSURE_TRIGGERS:
            if trigger.lower() in answer.lower():
                flags.append(f"Disclosure required: '{trigger}' indicates knowledge boundary")

        return flags if flags else None

    def _compute_hash(self, question: str, answer: str) -> str:
        content = f"{question}||{answer}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _write_audit_log(self, telemetry: QueryTelemetry, answer: str):
        log_entry = {
            **asdict(telemetry),
            "answer_preview": answer[:200]
        }
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def health_check(self) -> Dict[str, Any]:
        stats = self.metrics.get_stats()
        return {
            "status": "operational",
            "engine": "CHEM12_nuclear_chemistry",
            "version": "1.0.0",
            "port": 9294,
            "doctrine_blocks": len(self.doctrine_cache),
            "categories": len(set(IssueCategory)),
            "metrics": stats,
            "epistemic_guardrails": {
                "banned_phrases": len(BANNED_PHRASES),
                "disclosure_triggers": len(DISCLOSURE_TRIGGERS)
            }
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title="CHEM12 Nuclear Chemistry Intelligence Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CHEM12NuclearChemistryEngine()


@app.get("/health")
async def health():
    return engine.health_check()


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        response = engine.three_layer_response(
            question=request.question,
            mode=request.mode,
            zone=request.zone
        )
        return response
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/metrics")
async def get_metrics():
    return engine.metrics.get_stats()


if __name__ == "__main__":
    logger.info("Starting CHEM12 Nuclear Chemistry Engine on port 9294")
    uvicorn.run(app, host="0.0.0.0", port=9294)
