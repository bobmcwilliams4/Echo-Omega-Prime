"""
CHEM10 Electrochemistry Intelligence Engine
TIE-Grade Engine for Electrochemical Analysis

Domain: Electrode kinetics, battery chemistry, fuel cells, electrolysis,
        corrosion electrochemistry, electroanalytical methods

Port: 9292
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "CHEM10"
ENGINE_NAME = "Electrochemistry Intelligence Engine"
VERSION = "1.0.0"
PORT = 9292

logger.add(
    Path(__file__).parent / "logs" / "chem10_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)

# ============================================================================
# ENUMS
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
    ELECTRODE_KINETICS = "ELECTRODE_KINETICS"
    BATTERY_CHEMISTRY = "BATTERY_CHEMISTRY"
    FUEL_CELLS = "FUEL_CELLS"
    ELECTROLYSIS = "ELECTROLYSIS"
    CORROSION = "CORROSION"
    ELECTROANALYTICAL = "ELECTROANALYTICAL"
    ELECTROPLATING = "ELECTROPLATING"
    CAPACITANCE = "CAPACITANCE"
    SENSOR_DESIGN = "SENSOR_DESIGN"
    IMPEDANCE_SPECTROSCOPY = "IMPEDANCE_SPECTROSCOPY"

# ============================================================================
# DATA MODELS
# ============================================================================

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
    category: IssueCategory

class QueryRequest(BaseModel):
    question: str = Field(..., description="Electrochemistry question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response mode")
    zone: AnalysisZone = Field(AnalysisZone.PLANNING, description="Analysis zone")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    answer: str
    confidence: str
    reasoning: str
    authorities_cited: List[str]
    triggered_doctrines: List[str]
    analysis_zone: str
    determinism_hash: str
    telemetry: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float

# ============================================================================
# DOCTRINE CACHE - ELECTROCHEMISTRY EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Nernst Equation and Electrode Potential",
        keywords=["nernst", "electrode potential", "equilibrium", "activity", "concentration"],
        conclusion_template="Standard electrode potential E_0 and actual potential E are related by the Nernst equation. At 298K, E = E_0 - (RT/nF)ln(Q) = E_0 - (0.0592/n)log(Q).",
        reasoning_framework="""
The Nernst equation governs equilibrium electrode potential:

1. Standard Conditions (298K):
   E = E_0 - (RT/nF)ln(Q)
   E = E_0 - (0.0592V/n)log(Q)  [base-10 form]

2. Temperature Dependence:
   R = 8.314 J/(mol·K)
   T in Kelvin
   F = 96485 C/mol (Faraday constant)

3. Reaction Quotient Q:
   Q = [products]/[reactants]
   Use activities for rigorous analysis
   Approximate with concentrations for dilute solutions

4. Sign Conventions:
   Reduction half-cell: E_cathode
   Oxidation half-cell: E_anode
   Cell potential: E_cell = E_cathode - E_anode

5. Practical Implications:
   10-fold concentration change → 59.2mV/n shift at 298K
   pH dependence for H+/OH- reactions
   Reference electrodes (SHE, Ag/AgCl, SCE) anchor measurements

6. Non-Ideality Corrections:
   Activity coefficients (Debye-Huckel, Davies)
   Ionic strength effects
   Junction potentials

7. Application to Batteries:
   Open-circuit voltage (OCV) tracking SOC
   Concentration polarization at high currents
   Voltage fade with cycling
""",
        key_factors=[
            "Standard potential E_0 from reduction half-reactions",
            "Number of electrons n in balanced equation",
            "Temperature T (usually 298K assumed)",
            "Reaction quotient Q (activities preferred, concentrations approximate)",
            "pH dependence for proton-coupled reactions",
            "Reference electrode choice and junction potential"
        ],
        primary_authority=[
            "Atkins Physical Chemistry (Electrode Thermodynamics)",
            "Bard & Faulkner Electrochemical Methods (Chapter 2)",
            "Newman & Thomas-Alyea Electrochemical Systems (Nernst derivation)"
        ],
        burden_holder="Analyst must measure or estimate all species concentrations and verify standard potential source.",
        adversary_position="Nernst equation assumes thermodynamic equilibrium; at finite current, kinetic overpotentials dominate.",
        counter_arguments=[
            "Nernst applies rigorously only at zero current",
            "Activity coefficients needed for concentrated solutions",
            "Mixed potentials complicate multi-redox systems",
            "Surface adsorption and electrostatic effects unmodeled"
        ],
        resolution_strategy="Use Nernst for OCV predictions; add Butler-Volmer kinetics for current-voltage analysis.",
        entity_scope="All electrochemical cells at equilibrium or near-equilibrium.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for dilute aqueous systems at 298K; moderate for non-aqueous or extreme T/P.",
        controlling_precedent="Thermodynamic foundation of electrochemistry; universally accepted.",
        category=IssueCategory.ELECTRODE_KINETICS
    ),

    DoctrineBlock(
        topic="Butler-Volmer Kinetics and Exchange Current Density",
        keywords=["butler-volmer", "exchange current", "overpotential", "transfer coefficient", "kinetics"],
        conclusion_template="Butler-Volmer equation describes current-overpotential relationship: i = i_0[exp(alpha_a * n * F * eta / RT) - exp(-alpha_c * n * F * eta / RT)]. Exchange current density i_0 is key kinetic parameter.",
        reasoning_framework="""
Butler-Volmer equation for electrode kinetics:

1. General Form:
   i = i_0 * [exp(alpha_a * n * F * eta / RT) - exp(-alpha_c * n * F * eta / RT)]
   eta = E - E_eq (overpotential)
   i_0 = exchange current density (A/cm^2)

2. Transfer Coefficients:
   alpha_a + alpha_c = n (symmetry)
   Typically alpha_a = alpha_c = 0.5 (symmetric barrier)
   Asymmetric barriers: alpha != 0.5

3. Exchange Current Density i_0:
   Measure of reaction reversibility
   High i_0 → fast kinetics, small overpotential
   Low i_0 → sluggish kinetics, large overpotential
   Temperature dependent: i_0 = i_0_ref * exp(-E_act/RT)

4. Limiting Cases:
   Small eta (<10mV): Linear i = (n*F*i_0/RT)*eta (charge-transfer resistance)
   Large anodic eta: i ≈ i_0 * exp(alpha_a*n*F*eta/RT) (Tafel exponential)
   Large cathodic eta: i ≈ -i_0 * exp(-alpha_c*n*F*eta/RT)

5. Tafel Analysis:
   log|i| = log|i_0| + (alpha*n*F/(2.303*RT))*eta
   Tafel slope b = 2.303*RT/(alpha*n*F) ≈ 120mV/decade (alpha=0.5, n=1, 298K)
   Extract i_0 and alpha from log|i| vs eta plot

6. Multi-Step Mechanisms:
   Rate-determining step controls overall alpha
   Pre-equilibrium steps shift effective E_eq
   Adsorption isotherms (Langmuir, Frumkin) modify i_0

7. Mass Transport Coupling:
   At high current, concentration polarization reduces surface concentration
   Butler-Volmer assumes infinite mass transport
   Real systems: combine with Fick's law or limiting current
""",
        key_factors=[
            "Exchange current density i_0 (intrinsic kinetic parameter)",
            "Transfer coefficients alpha_a, alpha_c (barrier symmetry)",
            "Overpotential eta = E - E_eq",
            "Temperature T (affects exponential terms)",
            "Electrode material and surface condition (impacts i_0)",
            "Electrolyte composition (supports i_0 via surface coverage)"
        ],
        primary_authority=[
            "Bard & Faulkner Electrochemical Methods (Chapter 3)",
            "Newman Electrochemical Systems (Butler-Volmer derivation)",
            "Bockris & Reddy Modern Electrochemistry (Kinetics volume)"
        ],
        burden_holder="Analyst must measure i_0 and alpha via Tafel analysis or EIS; verify single-step vs multi-step mechanism.",
        adversary_position="Butler-Volmer assumes single rate-determining step; multi-step mechanisms require modified models.",
        counter_arguments=[
            "Real reactions often multi-step (e.g., HER, ORR)",
            "Mass transport limits not included in Butler-Volmer",
            "Surface roughness and catalyst dispersion complicate i_0 interpretation",
            "Non-Tafel behavior at small overpotentials (linear regime)"
        ],
        resolution_strategy="Use Butler-Volmer for initial kinetic modeling; refine with mechanism-specific models and mass transport corrections.",
        entity_scope="All electrode reactions with charge-transfer kinetics.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for well-characterized single-step reactions; moderate for complex multi-step mechanisms.",
        controlling_precedent="Foundational kinetic model in electrochemistry; empirically validated for many systems.",
        category=IssueCategory.ELECTRODE_KINETICS
    ),

    DoctrineBlock(
        topic="Cyclic Voltammetry Interpretation",
        keywords=["cyclic voltammetry", "CV", "peak current", "reversibility", "scan rate"],
        conclusion_template="Cyclic voltammetry (CV) reveals redox reversibility, electron stoichiometry, and diffusion coefficients. Peak separation and scan-rate dependence distinguish reversible, quasi-reversible, and irreversible systems.",
        reasoning_framework="""
Cyclic Voltammetry analysis framework:

1. Reversible (Nernstian) Systems:
   Peak current: i_p = 0.4463 * n * F * A * C * sqrt(n * F * v * D / RT)
   (Randles-Sevcik equation at 298K)
   Peak separation: delta_E_p = E_pa - E_pc ≈ 59mV/n (independent of v)
   i_pa / i_pc = 1 (peak current ratio)
   E_1/2 = (E_pa + E_pc)/2 ≈ E_0' (formal potential)

2. Quasi-Reversible Systems:
   delta_E_p > 59mV/n and increases with scan rate v
   i_pa / i_pc ≈ 1 but peak shapes broaden
   Kinetic parameter: k_0 (standard rate constant)
   Dimensionless parameter lambda = k_0 / sqrt(D*n*F*v/RT)

3. Irreversible Systems:
   Single peak (anodic or cathodic, no reverse peak)
   E_p shifts with scan rate: E_p = E_0' + (RT/alpha*n*F)*ln(v)
   Peak current still proportional to sqrt(v)

4. Scan Rate Dependence:
   Plot i_p vs sqrt(v): linear → diffusion-controlled
   Plot i_p vs v: linear → adsorption-controlled
   Plot E_p vs log(v): slope reveals alpha and n

5. Multi-Electron Transfers:
   Multiple peaks if E_0 values separated >200mV
   Overlapping peaks if E_0 values close
   Peak area ratio for n determination

6. Coupled Chemical Reactions (EC, CE, ECE):
   EC: electro-chemical follow-up reduces i_pc
   CE: chemical pre-equilibrium shifts E_p
   ECE: two-electron with intermediate chemical step
   Diagnostic criteria: i_pc/i_pa ratio, peak shape

7. Practical Considerations:
   iR drop compensation for resistive solutions
   Double-layer charging background subtraction
   Working electrode area A determination (geometric vs electroactive)
   Supporting electrolyte concentration (minimize migration)
""",
        key_factors=[
            "Peak separation delta_E_p (reversibility indicator)",
            "Peak current i_p (proportional to concentration and sqrt(v))",
            "Scan rate v (mV/s)",
            "Peak current ratio i_pa/i_pc (unity for reversible)",
            "Formal potential E_0' from (E_pa + E_pc)/2",
            "Number of electrons n from peak separation or Randles-Sevcik"
        ],
        primary_authority=[
            "Bard & Faulkner Electrochemical Methods (Chapter 6, CV)",
            "Nicholson & Shain Anal. Chem. 36, 706 (1964) - reversibility criteria",
            "Randles Trans. Faraday Soc. 44, 327 (1948) - peak current theory"
        ],
        burden_holder="Analyst must perform multi-scan-rate CV, measure accurate peak positions and currents, and account for background charging.",
        adversary_position="CV peaks can overlap or be masked by high background currents; requires careful baseline correction.",
        counter_arguments=[
            "iR drop distorts peak positions in resistive media",
            "Adsorption of reactants/products violates diffusion assumption",
            "Coupled homogeneous reactions complicate interpretation",
            "Non-planar electrode geometry (microelectrodes) alters peak shape"
        ],
        resolution_strategy="Use multiple scan rates, iR compensation, and simulation software (DigiElch, COMSOL) to fit experimental CV.",
        entity_scope="All redox-active species in solution or at electrode surface.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for simple reversible systems in low-resistance media; moderate for complex mechanisms.",
        controlling_precedent="CV is standard electroanalytical technique; Randles-Sevcik and Nicholson-Shain criteria widely accepted.",
        category=IssueCategory.ELECTROANALYTICAL
    ),

    DoctrineBlock(
        topic="Electrochemical Impedance Spectroscopy (EIS)",
        keywords=["EIS", "impedance", "nyquist", "bode", "equivalent circuit"],
        conclusion_template="EIS measures impedance Z(omega) = V(omega)/I(omega) over frequency range. Nyquist and Bode plots reveal charge-transfer resistance, double-layer capacitance, mass transport, and film/coating properties via equivalent circuit fitting.",
        reasoning_framework="""
Electrochemical Impedance Spectroscopy framework:

1. Fundamental Concept:
   Apply small AC voltage: V(t) = V_0 * sin(omega*t)
   Measure current response: I(t) = I_0 * sin(omega*t + phi)
   Impedance: Z(omega) = V_0/I_0 * exp(j*phi) = Z_real + j*Z_imag

2. Nyquist Plot (-Z_imag vs Z_real):
   Semicircle: charge-transfer resistance R_ct and double-layer capacitance C_dl
   High-frequency intercept: solution resistance R_s
   Low-frequency tail: Warburg impedance (mass transport)
   Diameter of semicircle = R_ct

3. Bode Plot (log|Z| and phase vs log(f)):
   Plateau at high f: R_s dominates
   Plateau at low f: R_s + R_ct
   Phase peak indicates capacitive/inductive behavior
   Slope -1 on log|Z| → pure capacitance

4. Equivalent Circuit Elements:
   R_s: solution (electrolyte) resistance
   R_ct: charge-transfer resistance (1/i_0 related)
   C_dl: double-layer capacitance (~10-40 microF/cm^2)
   W: Warburg diffusion impedance Z_W = sigma/sqrt(omega) * (1 - j)
   CPE: constant phase element Q, accounts for non-ideal capacitance

5. Warburg Impedance:
   Semi-infinite diffusion: Z_W = sigma/sqrt(omega) - j*sigma/sqrt(omega)
   Finite diffusion: bounded Warburg (low-f plateau)
   Appears as 45-degree line on Nyquist plot at low frequencies

6. Constant Phase Element (CPE):
   Z_CPE = 1 / (Q * (j*omega)^alpha)
   alpha = 1: pure capacitor
   alpha = 0.5: Warburg
   alpha < 1: non-ideal capacitance (surface roughness, porous electrode)

7. Fitting and Interpretation:
   Use software (ZView, EC-Lab, Gamry) to fit equivalent circuit
   Chi-squared minimization with Kramers-Kronig validation
   Physical meaning: R_ct → kinetics, C_dl → surface area, W → diffusion
   Battery SOC estimation via R_ct and C_dl trends
   Corrosion rate from R_ct (Stern-Geary equation)
   Coating defects via pore resistance and capacitance
""",
        key_factors=[
            "Frequency range (typically 100kHz to 10mHz)",
            "AC voltage amplitude (5-10mV to maintain linearity)",
            "Solution resistance R_s (high-frequency intercept)",
            "Charge-transfer resistance R_ct (semicircle diameter)",
            "Double-layer capacitance C_dl or CPE Q",
            "Warburg coefficient sigma (diffusion limitation)"
        ],
        primary_authority=[
            "Bard & Faulkner Electrochemical Methods (Chapter 10, Impedance)",
            "Orazem & Tribollet Electrochemical Impedance Spectroscopy (definitive text)",
            "Lasia Electrochemical Impedance Spectroscopy and its Applications (practical guide)"
        ],
        burden_holder="Analyst must select appropriate equivalent circuit model, validate with Kramers-Kronig, and verify parameter physical plausibility.",
        adversary_position="Multiple equivalent circuits can fit same data; physical interpretation requires independent validation (e.g., Tafel analysis for R_ct).",
        counter_arguments=[
            "Non-uniqueness of equivalent circuit models",
            "CPE parameters difficult to interpret physically",
            "Inductive loops at high frequency (instrumentation artifact or real?)",
            "Time-domain drift during low-frequency measurements"
        ],
        resolution_strategy="Combine EIS with CV, chronoamperometry, and material characterization; use simplest physically justified model.",
        entity_scope="All electrochemical systems: batteries, fuel cells, corrosion, coatings, sensors.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence when Kramers-Kronig valid and model parameters physically reasonable; moderate for complex multi-layer systems.",
        controlling_precedent="EIS is gold-standard non-destructive electrochemical diagnostic; equivalent circuit modeling widely accepted.",
        category=IssueCategory.IMPEDANCE_SPECTROSCOPY
    ),

    DoctrineBlock(
        topic="Lithium-Ion Battery Electrochemistry",
        keywords=["lithium-ion", "intercalation", "LiCoO2", "graphite", "battery", "SEI"],
        conclusion_template="Li-ion batteries store energy via intercalation: Li+ inserts into layered cathode (e.g., LiCoO2) and anode (graphite) without structural destruction. SEI layer on anode passivates surface; capacity fade from Li loss and impedance growth.",
        reasoning_framework="""
Lithium-ion battery electrochemistry:

1. Cathode Reactions (Intercalation):
   LiCoO2 ⇌ Li(1-x)CoO2 + x Li+ + x e-
   Layered oxide structure: Li in octahedral sites
   Voltage ~3.7-4.2V vs Li/Li+
   Capacity ~140 mAh/g (theoretical)
   Other cathodes: LiFePO4 (3.45V, 170 mAh/g), NMC (Li(Ni,Mn,Co)O2), NCA

2. Anode Reactions (Graphite):
   6C + x Li+ + x e- ⇌ LixC6  (x ≤ 1)
   Staging phenomenon: LiC12 → LiC6 (full lithiation)
   Voltage ~0.05-0.2V vs Li/Li+
   Capacity ~372 mAh/g (theoretical LiC6)
   Alternative: Li4Ti5O12 (1.5V, safer but lower energy)

3. Solid Electrolyte Interphase (SEI):
   Forms on first charge via electrolyte reduction:
   EC + 2Li+ + 2e- → (CH2OCO2Li)2 (lithium ethylene dicarbonate)
   SEI passivates anode, prevents continuous decomposition
   Composed of Li2CO3, LiF, ROLi, polymers
   Thickness 10-100nm; ionically conductive, electronically insulating
   SEI growth consumes Li → capacity fade

4. Electrolyte:
   LiPF6 in EC:DMC or EC:DEC (1M concentration)
   Organic carbonates: EC (high dielectric), DMC (low viscosity)
   LiPF6 dissociates: Li+ solvated, PF6- conducts
   Additives: FEC (SEI stabilizer), VC (film-former)

5. Voltage Profile:
   Cell voltage V_cell = V_cathode - V_anode - iR - overpotentials
   Open-circuit voltage (OCV) from Nernst with x (SOC)
   Voltage plateaus indicate two-phase regions
   Sloping regions: solid-solution intercalation

6. Capacity Fade Mechanisms:
   SEI growth (continuous electrolyte reduction)
   Li plating (anode overpotential at low T or high charge rate)
   Cathode structural degradation (oxygen loss, transition metal dissolution)
   Electrolyte oxidation at cathode (high voltage)
   Current collector corrosion (Al at cathode, Cu at anode)

7. Rate Capability:
   Limited by Li+ diffusion in solid (D ~ 10^-10 to 10^-14 cm^2/s)
   Overpotential = charge-transfer + ohmic + diffusion
   High-rate cathodes: nanoparticles, carbon coating
   Fast-charging anodes: Si, Li4Ti5O12, graphite spheroidization
""",
        key_factors=[
            "Intercalation capacity (mAh/g) and voltage of cathode/anode",
            "SEI formation and stability on anode",
            "Electrolyte composition (salt, solvents, additives)",
            "Li+ diffusion coefficients in active materials",
            "Charge-transfer kinetics (exchange current density)",
            "Operating temperature and C-rate"
        ],
        primary_authority=[
            "Goodenough & Park J. Am. Chem. Soc. 135, 1167 (2013) - Li-ion review",
            "Xu Chem. Rev. 104, 4303 (2004) - electrolytes",
            "Peled J. Electrochem. Soc. 126, 2047 (1979) - SEI formation"
        ],
        burden_holder="Battery designer must balance energy density, power density, cycle life, and safety via material and operating condition selection.",
        adversary_position="High energy density cathodes (high-Ni NMC) are chemically unstable; SEI is imperfect passivation leading to continuous Li loss.",
        counter_arguments=[
            "SEI never fully stable; grows throughout cell life",
            "High-voltage cathodes oxidize electrolyte",
            "Graphite anode exfoliates in propylene carbonate solvents",
            "Li plating risk at low temperature or high current"
        ],
        resolution_strategy="Use FEC additive for SEI stabilization; limit upper cutoff voltage; thermal management; pre-lithiation to offset SEI loss.",
        entity_scope="All lithium-ion batteries (consumer electronics, EVs, grid storage).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard LiCoO2/graphite chemistry; moderate for advanced high-Ni or Si-based systems.",
        controlling_precedent="Intercalation mechanism and SEI concept universally accepted; empirical validation across billions of cells.",
        category=IssueCategory.BATTERY_CHEMISTRY
    ),

    DoctrineBlock(
        topic="Proton Exchange Membrane Fuel Cells (PEMFC)",
        keywords=["PEMFC", "fuel cell", "Nafion", "ORR", "HOR", "platinum"],
        conclusion_template="PEMFC converts H2 and O2 to electricity via Pt-catalyzed HOR (anode) and ORR (cathode). Nafion membrane conducts protons. Key losses: activation (slow ORR), ohmic (membrane resistance), mass transport (O2 depletion).",
        reasoning_framework="""
PEMFC electrochemistry and operation:

1. Anode Reaction (HOR):
   H2 → 2H+ + 2e-  (E_0 = 0V vs SHE)
   Fast kinetics: i_0 ~ 10^-3 A/cm^2 on Pt
   Tafel slope ~30mV/decade
   Minimal overpotential (<10mV at typical current densities)

2. Cathode Reaction (ORR):
   O2 + 4H+ + 4e- → 2H2O  (E_0 = 1.23V vs SHE)
   Slow kinetics: i_0 ~ 10^-9 A/cm^2 on Pt
   Tafel slope ~60-120mV/decade
   Dominant overpotential: 300-400mV at 1 A/cm^2

3. Nafion Membrane:
   Sulfonated tetrafluoroethylene polymer: -(CF2-CF2)n-(CF2-CF(O-CF2-CF(CF3)-O-CF2-CF2-SO3H))m-
   Proton conductivity: 0.1 S/cm (hydrated, 80°C)
   Water management critical: dry → low conductivity, flood → O2 transport loss
   Thickness 25-175 microns

4. Catalyst Layers:
   Pt/C nanoparticles: 20-40 wt% Pt on carbon black
   Ionomer (Nafion) mixed in for proton conduction
   Porous structure for gas diffusion
   Pt loading: 0.1-0.4 mg/cm^2 (cathode higher than anode)

5. Voltage Losses (Polarization Curve):
   V_cell = E_0 - eta_act - eta_ohmic - eta_conc
   Activation loss: Tafel equation, dominates at low current
   Ohmic loss: iR (membrane + contact resistance), linear with i
   Concentration loss: mass transport limitation, exponential at high i

6. Water Management:
   Water produced at cathode (ORR)
   Electro-osmotic drag: H+ carries water from anode to cathode (~2.5 H2O per H+)
   Back-diffusion from cathode to anode (concentration gradient)
   Humidification required to keep membrane hydrated
   Liquid water flooding blocks pores → mass transport loss

7. Performance Optimization:
   Temperature: 60-80°C (higher → better kinetics, but membrane dry-out risk)
   Pressure: 1-3 bar (higher → better mass transport, higher ORR rate)
   Stoichiometry: excess H2/O2 to avoid starvation
   Pt catalyst improvements: alloying (PtCo, PtNi), core-shell structures
   Non-Pt catalysts: Fe-N-C (lower activity but cheaper)
""",
        key_factors=[
            "ORR overpotential at cathode (dominant loss)",
            "Membrane proton conductivity (hydration-dependent)",
            "Pt catalyst loading and activity",
            "Water balance (humidification vs flooding)",
            "Operating temperature and pressure",
            "Gas stoichiometry and utilization"
        ],
        primary_authority=[
            "O'Hayre Fuel Cell Fundamentals (comprehensive textbook)",
            "Gasteiger & Markovic Science 324, 48 (2009) - ORR review",
            "Weber & Newman Chem. Rev. 104, 4679 (2004) - PEMFC modeling"
        ],
        burden_holder="Fuel cell designer must optimize catalyst, membrane, and operating conditions to maximize power density and durability.",
        adversary_position="ORR is inherently slow on Pt; water flooding is difficult to avoid at high current densities; Pt cost prohibitive for mass market.",
        counter_arguments=[
            "ORR kinetics fundamentally limited by 4-electron pathway",
            "Pt dissolution and agglomeration reduce activity over time",
            "Membrane degradation (chemical and mechanical) limits lifetime",
            "CO poisoning of Pt anode from reformed H2"
        ],
        resolution_strategy="Develop non-PGM catalysts; improve membrane durability; use two-phase flow modeling for water management; purify H2 feed.",
        entity_scope="All PEM fuel cells (automotive, stationary, portable power).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for Pt-based PEMFC fundamentals; moderate for non-Pt catalysts and long-term degradation.",
        controlling_precedent="ORR as rate-limiting step and Nafion as standard membrane universally accepted.",
        category=IssueCategory.FUEL_CELLS
    ),

    DoctrineBlock(
        topic="Water Electrolysis (Alkaline, PEM, SOEC)",
        keywords=["electrolysis", "water splitting", "HER", "OER", "alkaline", "PEM electrolyzer"],
        conclusion_template="Water electrolysis produces H2 via 2H2O → 2H2 + O2 (E_0 = 1.23V). Alkaline uses KOH electrolyte, PEM uses Nafion, SOEC operates at high T. OER overpotential is dominant loss; iridium/ruthenium oxides are state-of-art catalysts.",
        reasoning_framework="""
Water electrolysis technologies and electrochemistry:

1. Overall Reaction:
   2H2O → 2H2 + O2
   Thermodynamic voltage: E_0 = 1.23V at 25°C, 1 bar
   Thermoneutral voltage: 1.48V (includes entropy)
   Practical cell voltage: 1.8-2.4V (depends on technology and current density)

2. Alkaline Electrolysis (AEL):
   Cathode (HER): 2H2O + 2e- → H2 + 2OH-  (in KOH)
   Anode (OER): 4OH- → O2 + 2H2O + 4e-
   Electrolyte: 20-40% KOH, 60-80°C
   Catalysts: Ni, Raney Ni (HER); NiFe, CoOx (OER)
   Separator: Zirfon, asbestos-free diaphragm (gas separation)
   Current density: 0.2-0.4 A/cm^2
   Efficiency: 60-70% (HHV basis)

3. PEM Electrolysis (PEMEL):
   Cathode (HER): 2H+ + 2e- → H2
   Anode (OER): 2H2O → O2 + 4H+ + 4e-
   Membrane: Nafion (proton conductor)
   Catalysts: Pt (HER), IrO2/RuO2 (OER)
   Current density: 1-3 A/cm^2 (higher than AEL)
   Advantages: compact, high purity H2, fast response
   Disadvantages: expensive Ir/Ru, membrane degradation

4. Solid Oxide Electrolysis (SOEC):
   Operates 700-900°C
   Cathode: H2O + 2e- → H2 + O2-  (in ceramic)
   Anode: 2O2- → O2 + 4e-
   Electrolyte: yttria-stabilized zirconia (YSZ)
   Higher efficiency (80-90%) due to thermal energy input
   Steam input; can co-electrolyze CO2 + H2O → syngas

5. Overpotential Analysis:
   V_cell = 1.23V + eta_OER + eta_HER + iR_ohmic + eta_conc
   eta_OER dominates: 300-500mV at 1 A/cm^2 (IrO2)
   eta_HER: 50-150mV (Pt), 200-400mV (Ni)
   iR_ohmic: electrolyte/membrane resistance

6. Oxygen Evolution Reaction (OER) Mechanisms:
   4-electron process, multiple intermediates:
   * OH- → *OH → *O → *OOH → O2 (alkaline)
   Volcano plot: IrO2, RuO2 near optimum
   Scaling relations limit activity (Sabatier principle)

7. Hydrogen Evolution Reaction (HER) Mechanisms:
   Volmer: H2O + e- → H_ad + OH- (or H+ + e- → H_ad in acid)
   Tafel: 2H_ad → H2
   Heyrovsky: H_ad + H2O + e- → H2 + OH-
   Pt is optimal HER catalyst (exchange current ~10^-3 A/cm^2)
""",
        key_factors=[
            "OER overpotential (dominant loss)",
            "Catalyst stability and cost (Ir/Ru scarce)",
            "Electrolyte/membrane conductivity",
            "Operating current density (A/cm^2)",
            "Gas crossover and purity requirements",
            "System efficiency (electricity to H2 HHV)"
        ],
        primary_authority=[
            "Carmo et al. Int. J. Hydrogen Energy 38, 4901 (2013) - review of technologies",
            "McCrory et al. J. Am. Chem. Soc. 137, 4347 (2015) - OER benchmarking",
            "Trasatti J. Electroanal. Chem. 39, 163 (1972) - volcano plot for OER"
        ],
        burden_holder="Electrolyzer designer must select technology based on scale, cost, efficiency, and H2 purity requirements; balance catalyst cost vs performance.",
        adversary_position="OER is fundamentally limited by scaling relations; earth-abundant catalysts (NiFe) have high overpotentials; membrane degradation in PEMEL.",
        counter_arguments=[
            "IrO2/RuO2 scarce and expensive (global Ir production ~3 tons/year)",
            "Alkaline cells have lower current density and slower dynamics",
            "PEM membranes degrade under high voltage and humidity cycling",
            "SOEC materials (ceramics) brittle and sensitive to thermal cycling"
        ],
        resolution_strategy="Develop earth-abundant OER catalysts (NiFe, CoOx optimization); improve membrane durability; hybrid systems (AEL for base load, PEMEL for transient).",
        entity_scope="All water electrolysis for H2 production (renewable energy storage, industrial H2).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for fundamental OER/HER mechanisms; moderate for long-term catalyst stability and membrane lifetime.",
        controlling_precedent="OER as bottleneck and IrO2/RuO2 as best catalysts widely accepted; ongoing research on alternatives.",
        category=IssueCategory.ELECTROLYSIS
    ),

    DoctrineBlock(
        topic="Corrosion Electrochemistry and Polarization Curves",
        keywords=["corrosion", "polarization", "Tafel", "corrosion potential", "passivation"],
        conclusion_template="Corrosion occurs when anodic metal dissolution and cathodic reduction (O2 or H+) proceed at equal rates at corrosion potential E_corr. Polarization curves reveal corrosion current i_corr via Tafel extrapolation or linear polarization resistance.",
        reasoning_framework="""
Corrosion electrochemistry framework:

1. Mixed Potential Theory:
   At open-circuit (E_corr), anodic and cathodic currents balance:
   i_anodic(E_corr) = i_cathodic(E_corr) = i_corr
   E_corr is between anodic and cathodic equilibrium potentials

2. Anodic Reaction (Metal Dissolution):
   M → M^n+ + ne-
   Example: Fe → Fe2+ + 2e-  (E_0 = -0.44V vs SHE)
   Tafel behavior: i_a = i_corr * 10^((E - E_corr)/b_a)

3. Cathodic Reactions:
   Oxygen reduction (aerated): O2 + 2H2O + 4e- → 4OH-  (E_0 = 0.40V)
   Hydrogen evolution (acidic): 2H+ + 2e- → H2  (E_0 = 0V)
   Tafel behavior: i_c = -i_corr * 10^(-(E - E_corr)/b_c)

4. Polarization Curve Measurement:
   Potentiodynamic sweep from E_corr - 250mV to E_corr + 250mV
   Tafel extrapolation: plot log|i| vs E, extrapolate linear regions to E_corr
   Intersection gives i_corr
   Tafel slopes b_a and b_c from anodic and cathodic branches

5. Linear Polarization Resistance (LPR):
   For small overpotentials (±10mV from E_corr):
   R_p = (dE/di)_{E=E_corr} = (b_a * b_c) / (2.303 * i_corr * (b_a + b_c))
   Stern-Geary equation: i_corr = B / R_p
   B = (b_a * b_c) / (2.303 * (b_a + b_c)) (typically 26mV for Fe)

6. Passivation:
   Active-passive transition: oxide film forms, reduces i_a
   Passive current density i_pass << i_corr (factor of 100-1000 lower)
   Breakdown potential E_b: pitting corrosion initiates (Cl- attack)
   Repassivation potential E_rp: pitting stops on reverse scan

7. Corrosion Rate Calculation:
   Faraday's law: Corrosion rate (mm/year) = (i_corr * M) / (n * F * rho) * K
   M = atomic mass (g/mol)
   rho = density (g/cm^3)
   K = unit conversion factor
   For Fe: 1 microA/cm^2 ≈ 11.6 microns/year
""",
        key_factors=[
            "Corrosion potential E_corr (mixed potential)",
            "Corrosion current density i_corr (from Tafel or LPR)",
            "Tafel slopes b_a and b_c (kinetic parameters)",
            "Polarization resistance R_p (inversely proportional to i_corr)",
            "Passivation current i_pass and breakdown potential E_b",
            "Environmental factors: pH, Cl- concentration, dissolved O2"
        ],
        primary_authority=[
            "Fontana Corrosion Engineering (definitive textbook)",
            "Stern & Geary J. Electrochem. Soc. 104, 56 (1957) - LPR method",
            "Pourbaix Atlas of Electrochemical Equilibria (E-pH diagrams)"
        ],
        burden_holder="Corrosion engineer must measure polarization curves in service environment; account for solution resistance and mass transport effects.",
        adversary_position="Tafel extrapolation assumes pure activation control; real systems have ohmic drop and diffusion limitations; localized corrosion (pitting, crevice) not captured by i_corr.",
        counter_arguments=[
            "Tafel regions often obscured by mass transport or ohmic drop",
            "LPR assumes uniform corrosion; invalid for pitting or crevice attack",
            "Passive films metastable; breakdown potential depends on surface defects",
            "Galvanic coupling in multi-metal assemblies complicates E_corr"
        ],
        resolution_strategy="Combine polarization curves with EIS, weight-loss coupons, and visual inspection; use localized techniques (SVET, SIET) for pitting.",
        entity_scope="All metallic corrosion in aqueous environments.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for uniform corrosion in well-defined electrolytes; moderate for localized corrosion and complex geometries.",
        controlling_precedent="Mixed potential theory and Stern-Geary equation widely validated; ASTM standards for polarization testing.",
        category=IssueCategory.CORROSION
    ),

    DoctrineBlock(
        topic="Electroplating and Electrodeposition",
        keywords=["electroplating", "electrodeposition", "nucleation", "throwing power", "current efficiency"],
        conclusion_template="Electroplating deposits metal layer via cathodic reduction: M^n+ + ne- → M. Deposit quality depends on current density, additive chemistry, mass transport, and nucleation kinetics. Faradaic efficiency and throwing power are key metrics.",
        reasoning_framework="""
Electroplating electrochemistry and process control:

1. Cathodic Deposition Reaction:
   M^n+ + ne- → M  (metal ion to solid metal)
   Example: Cu2+ + 2e- → Cu  (E_0 = +0.34V vs SHE)
   Deposit thickness: d = (i * t * M) / (n * F * rho * A)

2. Faradaic Efficiency:
   Percentage of current that deposits metal (vs H2 evolution or other side reactions)
   eta_F = (actual mass deposited) / (theoretical mass from Faraday's law)
   Ideal: 100%; practical: 85-98% (depends on chemistry)

3. Current Density Distribution:
   Primary distribution: geometry-driven (edges get higher i)
   Secondary distribution: kinetics modify (activation overpotential)
   Tertiary distribution: mass transport and additives further modify
   Throwing power: ability to deposit uniformly in recessed areas

4. Nucleation and Growth:
   Initial nucleation: 3D island growth on substrate
   Volmer-Weber (island), Frank-van der Merwe (layer-by-layer), Stranski-Krastanov (mixed)
   Grain size controlled by nucleation density
   Additives (suppressors, brighteners, levelers) modify nucleation

5. Additive Chemistry:
   Suppressors: polymers (PEG) that adsorb and inhibit deposition
   Accelerators: SPS, MPS (thiols) that locally enhance deposition
   Levelers: high MW molecules that preferentially adsorb at peaks
   Brighteners: reduce grain size → reflective surface

6. Pulse Plating:
   Alternate high current pulses with off-time or reverse pulses
   Advantages: finer grain size, improved throwing power, reduced porosity
   Duty cycle and frequency control deposit properties

7. Mass Transport Limitations:
   At high current density, M^n+ concentration at surface depletes
   Limiting current: i_L = n * F * D * C_bulk / delta
   Beyond i_L: dendritic growth, powdery deposit, H2 evolution
   Agitation and convection increase i_L

8. Common Plating Systems:
   Cu (damascene, PCB): CuSO4 + H2SO4 + additives
   Ni (corrosion protection): Watts bath (NiSO4, NiCl2, boric acid)
   Au (electronics): cyanide or sulfite baths
   Zn (galvanizing): alkaline or acid chloride
   Cr (decorative, hard): hexavalent Cr (CrO3) or trivalent Cr
""",
        key_factors=[
            "Current density (A/dm^2) - controls deposit rate and morphology",
            "Bath composition (metal salt, pH, additives)",
            "Temperature (affects conductivity and kinetics)",
            "Agitation (mass transport enhancement)",
            "Substrate surface preparation (cleanliness, roughness)",
            "Faradaic efficiency (current utilization)"
        ],
        primary_authority=[
            "Schlesinger & Paunovic Modern Electroplating (comprehensive reference)",
            "Bard & Faulkner Electrochemical Methods (Chapter 13, Electrodeposition)",
            "Paunovic & Schlesinger Fundamentals of Electrochemical Deposition"
        ],
        burden_holder="Process engineer must optimize current density, bath composition, and agitation to achieve target deposit thickness, uniformity, and properties.",
        adversary_position="High current density enables fast deposition but risks poor quality (porosity, dendrites); additives improve deposit but complicate bath control.",
        counter_arguments=[
            "Throwing power fundamentally limited by geometry",
            "Additives decompose over time, requiring replenishment",
            "Hydrogen co-evolution causes embrittlement in high-strength steels",
            "Hexavalent Cr toxic; trivalent Cr baths have lower throwing power"
        ],
        resolution_strategy="Use Hull cell testing to optimize current density; monitor additive concentrations via CVS (cyclic voltammetric stripping); pulse plating for critical applications.",
        entity_scope="All electroplating applications (decorative, functional, PCB fabrication).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for well-established chemistries (Cu, Ni, Zn); moderate for emerging systems (trivalent Cr, nanocrystalline deposits).",
        controlling_precedent="Faraday's law and additive chemistry empirically validated across billions of plating cycles.",
        category=IssueCategory.ELECTROPLATING
    ),

    DoctrineBlock(
        topic="Supercapacitors and Double-Layer Capacitance",
        keywords=["supercapacitor", "EDLC", "double layer", "pseudocapacitance", "activated carbon"],
        conclusion_template="Supercapacitors store energy electrostatically in electric double layer (EDLC) or via fast surface redox (pseudocapacitance). Capacitance C = epsilon * A / d; high surface area carbon (1000-2000 m^2/g) gives 100-300 F/g.",
        reasoning_framework="""
Supercapacitor electrochemistry and energy storage:

1. Electric Double-Layer Capacitance (EDLC):
   Helmholtz model: C = epsilon_0 * epsilon_r * A / d
   d ~ few angstroms (compact layer)
   Gouy-Chapman-Stern model: diffuse layer + compact layer
   Specific capacitance: C_sp = epsilon / (d * rho_carbon)
   High surface area → high C

2. Activated Carbon Electrodes:
   Surface area: 1000-2500 m^2/g (BET)
   Pore size distribution: micropores (<2nm), mesopores (2-50nm)
   Specific capacitance: 100-300 F/g (aqueous), 50-150 F/g (organic)
   Carbide-derived carbons (CDC): tunable pore size

3. Electrolytes:
   Aqueous (H2SO4, KOH): high conductivity, low voltage window (1.2V)
   Organic (TEABF4 in ACN or PC): wider voltage window (2.7-3.0V), lower conductivity
   Ionic liquids: non-flammable, wide window (3.5V), very viscous

4. Pseudocapacitance:
   Fast surface redox reactions (not bulk diffusion)
   RuO2: Ru(III) ⇌ Ru(IV) + e-  (capacitance ~720 F/g)
   MnO2: Mn(III) ⇌ Mn(IV) + e-  (capacitance ~200 F/g)
   Conducting polymers (PANI, PPy): doping/dedoping
   Charge storage > EDLC but rate limited by redox kinetics

5. Energy and Power Density:
   Energy: E = 0.5 * C * V^2
   Power: P = V^2 / (4 * ESR)  (ESR = equivalent series resistance)
   Ragone plot: supercaps between batteries and conventional capacitors
   Typical: 5-10 Wh/kg, 10 kW/kg

6. Voltage Distribution in Symmetric Cells:
   Two identical electrodes in series
   V_cell = V_+ + V_-  (each electrode ~1.35V in 2.7V organic cell)
   Asymmetric cells: different materials on + and - to extend voltage

7. Cycle Life and Degradation:
   EDLC: >500,000 cycles (no phase change, purely electrostatic)
   Pseudocapacitors: 10,000-100,000 cycles (redox reactions cause structural change)
   Degradation: electrolyte decomposition at high voltage, carbon oxidation
   Voltage management critical (stay below electrolyte stability window)
""",
        key_factors=[
            "Specific surface area of carbon (m^2/g)",
            "Pore size distribution (ion-accessible pores)",
            "Electrolyte ionic conductivity and voltage window",
            "Equivalent series resistance ESR (ohmic losses)",
            "Operating voltage (V^2 in energy equation)",
            "Temperature (affects conductivity and capacitance)"
        ],
        primary_authority=[
            "Conway Electrochemical Supercapacitors (definitive text)",
            "Simon & Gogotsi Nature Materials 7, 845 (2008) - review",
            "Beguin & Frackowiak Carbons for Electrochemical Energy Storage"
        ],
        burden_holder="Supercapacitor designer must balance surface area (high C) with pore accessibility (ion transport) and electrolyte stability (voltage window).",
        adversary_position="High surface area carbons have narrow micropores that exclude solvated ions; organic electrolytes have low conductivity reducing power density.",
        counter_arguments=[
            "Micropores (<1nm) inaccessible to solvated ions",
            "Organic electrolytes viscous → high ESR → low power",
            "Pseudocapacitors degrade faster than EDLC",
            "Voltage balancing required in series stacks (cell-to-cell variation)"
        ],
        resolution_strategy="Use carbide-derived carbons with tuned pore size; ionic liquid electrolytes for safety; hybrid supercap-battery for energy-power balance.",
        entity_scope="All supercapacitor applications (automotive regenerative braking, UPS, grid frequency regulation).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for EDLC fundamentals; moderate for pseudocapacitors and ionic liquid stability.",
        controlling_precedent="Double-layer capacitance model and Ragone plot framework universally accepted.",
        category=IssueCategory.CAPACITANCE
    ),

    DoctrineBlock(
        topic="Potentiostats and Electrochemical Instrumentation",
        keywords=["potentiostat", "galvanostat", "three-electrode", "reference electrode", "working electrode"],
        conclusion_template="Potentiostat controls working electrode potential vs reference electrode using feedback amplifier and counter electrode for current. Three-electrode setup isolates reference from current path, enabling accurate potential control.",
        reasoning_framework="""
Potentiostat operation and electrochemical cell design:

1. Three-Electrode Configuration:
   Working Electrode (WE): where reaction of interest occurs
   Reference Electrode (RE): stable potential, zero current
   Counter Electrode (CE): completes circuit, passes all current
   Potentiostat maintains V_WE - V_RE = V_set by adjusting V_CE

2. Reference Electrodes:
   Standard Hydrogen Electrode (SHE): 0.000V by definition (impractical)
   Ag/AgCl (saturated KCl): +0.197V vs SHE
   Saturated Calomel Electrode (SCE): +0.241V vs SHE
   Hg/Hg2SO4 (saturated K2SO4): +0.64V vs SHE
   Requirements: stable, reproducible, low polarizability

3. Potentiostatic Control:
   Error amplifier: V_error = V_set - (V_WE - V_RE)
   Feedback adjusts V_CE to drive V_error → 0
   Bandwidth: kHz for fast techniques (CV, EIS)
   Compliance voltage: max V_CE (typically ±10 to ±15V)

4. Galvanostatic Control:
   Galvanostat controls current I_WE, measures V_WE
   Used for constant-current charging/discharging
   Chronopotentiometry: step I, measure V(t)

5. iR Compensation:
   Uncompensated resistance R_u between WE and RE causes error
   V_WE_true = V_WE_measured - i * R_u
   Positive feedback compensation: potentiostat adds i * R_u offset
   Over-compensation → oscillation
   Optimal: 85-95% compensation

6. Current Measurement:
   Transimpedance amplifier: V_out = -i * R_feedback
   Current ranges: pA to A (via switchable feedback resistors)
   Bandwidth vs noise tradeoff

7. Common Techniques:
   Cyclic Voltammetry (CV): triangle wave voltage scan
   Linear Sweep Voltammetry (LSV): single sweep
   Chronoamperometry: step voltage, measure i(t)
   Electrochemical Impedance Spectroscopy (EIS): AC voltage, measure Z(omega)
   Chronopotentiometry: step current, measure V(t)

8. Cell Design Considerations:
   RE placement: close to WE surface (minimize R_u)
   Luggin capillary: fine tip for local potential measurement
   CE area >> WE area (avoid CE polarization)
   Solution resistance: use supporting electrolyte (0.1-1M)
""",
        key_factors=[
            "Reference electrode stability and potential",
            "Uncompensated resistance R_u (minimize via RE positioning)",
            "Potentiostat bandwidth (for fast techniques like CV)",
            "Current measurement range and noise",
            "iR compensation settings (85-95% optimal)",
            "Counter electrode area and material (Pt mesh typical)"
        ],
        primary_authority=[
            "Bard & Faulkner Electrochemical Methods (Appendix B, Instrumentation)",
            "Kissinger & Heineman Laboratory Techniques in Electroanalytical Chemistry",
            "Gamry Instruments Application Notes (practical guidance)"
        ],
        burden_holder="Electrochemist must select appropriate reference electrode, minimize R_u via cell design, and calibrate iR compensation.",
        adversary_position="iR compensation can destabilize potentiostat if over-compensated; reference electrode drift over time; junction potentials add systematic error.",
        counter_arguments=[
            "Ag/AgCl potential depends on Cl- concentration (varies if leakage)",
            "RE contamination by sample diffusion into salt bridge",
            "CE polarization if area too small or material unsuitable",
            "High-frequency EIS distorted by potentiostat bandwidth limits"
        ],
        resolution_strategy="Use double-junction reference electrodes; calibrate RE vs standard; verify iR compensation via EIS Nyquist plot (no inductive loop at high f).",
        entity_scope="All controlled-potential electrochemical experiments.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for standard three-electrode setup; moderate for ultra-low current (pA) or ultra-high frequency (>100kHz) techniques.",
        controlling_precedent="Three-electrode potentiostatic control is standard in electrochemistry; widely validated.",
        category=IssueCategory.ELECTROANALYTICAL
    ),

    DoctrineBlock(
        topic="Electrochemical Sensors and Biosensors",
        keywords=["sensor", "biosensor", "glucose", "amperometric", "potentiometric", "enzyme electrode"],
        conclusion_template="Electrochemical sensors detect analytes via current (amperometric), potential (potentiometric), or impedance changes. Glucose sensor (enzyme electrode) oxidizes glucose at electrode, measuring current proportional to concentration.",
        reasoning_framework="""
Electrochemical sensor design and operation:

1. Amperometric Sensors:
   Measure current at fixed potential
   Current proportional to analyte concentration (via Cottrell or steady-state)
   Example: O2 sensor (Clark electrode), glucose sensor
   Advantages: fast response, simple electronics
   Disadvantages: requires analyte to be electroactive or coupled to electroactive species

2. Potentiometric Sensors:
   Measure open-circuit potential (zero current)
   Nernst equation: E = E_0 + (RT/nF)ln(a)
   Example: pH electrode (glass membrane), ion-selective electrodes (ISE)
   Advantages: no reagent consumption, thermodynamic basis
   Disadvantages: slow response, interference from other ions

3. Impedimetric Sensors:
   Measure impedance (EIS) as function of analyte binding
   Surface functionalization: antibody, aptamer, etc.
   Binding changes interfacial capacitance or charge-transfer resistance

4. Glucose Sensor (Enzyme Electrode):
   Glucose oxidase (GOx) catalyzes: glucose + O2 → gluconic acid + H2O2
   1st generation: oxidize H2O2 at Pt: H2O2 → O2 + 2H+ + 2e-  (E ~ +0.6V)
   2nd generation: mediator (ferrocene) shuttles e- from GOx to electrode (lower E)
   3rd generation: direct electron transfer (GOx immobilized on electrode)
   Current proportional to glucose concentration

5. Selectivity and Interference:
   Nafion or polyurethane membrane: size exclusion (reject interferents like ascorbic acid, uric acid)
   Permselective membranes: charge exclusion
   Enzyme specificity: GOx highly selective for glucose

6. Sensor Calibration:
   Linear range: typically 1-20 mM glucose
   Sensitivity: nA per mM (depends on enzyme loading and electrode area)
   Detection limit: microM range
   Michaelis-Menten kinetics at high concentration (enzyme saturation)

7. Stability and Lifetime:
   Enzyme deactivation: thermal, pH, oxidative stress
   Membrane fouling: protein adsorption
   Electrode passivation: oxide formation
   Typical lifetime: days to months (implantable), >1 year (ex vivo with storage)

8. Other Electrochemical Biosensors:
   Lactate (lactate oxidase), cholesterol (cholesterol oxidase)
   DNA sensors (hybridization detection via redox label)
   Immunosensors (antibody-antigen binding)
   Microfluidic integration for point-of-care
""",
        key_factors=[
            "Selectivity (enzyme specificity, membrane exclusion)",
            "Sensitivity (current per unit concentration)",
            "Response time (enzyme kinetics, diffusion)",
            "Stability (enzyme lifetime, membrane fouling)",
            "Linear range (Michaelis-Menten saturation)",
            "Operating potential (minimize interferents)"
        ],
        primary_authority=[
            "Wang Analytical Electrochemistry (sensor design)",
            "Clark & Lyons Ann. N.Y. Acad. Sci. 102, 29 (1962) - enzyme electrode concept",
            "Heller & Feldman Chem. Rev. 108, 2482 (2008) - electrochemical glucose sensors"
        ],
        burden_holder="Sensor designer must optimize enzyme loading, membrane permeability, and operating potential to maximize selectivity and lifetime.",
        adversary_position="Enzyme electrodes suffer from O2 dependence (1st gen), mediator leaching (2nd gen), and limited direct electron transfer (3rd gen); interferents still problematic.",
        counter_arguments=[
            "Ascorbic acid, uric acid oxidize at +0.6V (interfere with 1st gen glucose sensor)",
            "Enzyme activity depends on temperature and pH (calibration drift)",
            "Implantable sensors biofouled by protein layer within hours",
            "Mediators (ferrocene) can leach out over time"
        ],
        resolution_strategy="Use 2nd or 3rd generation glucose sensors with mediators; Nafion membrane for interferent rejection; temperature-compensated calibration; periodic recalibration.",
        entity_scope="All electrochemical sensors (clinical glucose monitoring, environmental monitoring, food industry).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for glucose sensors (mature technology); moderate for novel biosensors and implantable devices.",
        controlling_precedent="Enzyme electrode concept (Clark) and mediator approach universally accepted; glucose sensors FDA-approved.",
        category=IssueCategory.SENSOR_DESIGN
    ),

    DoctrineBlock(
        topic="Electrochemical Capacitors vs Batteries",
        keywords=["battery", "capacitor", "supercapacitor", "energy density", "power density", "Ragone plot"],
        conclusion_template="Batteries store energy via bulk redox (high energy density, ~150 Wh/kg); capacitors via surface charge (high power density, ~10 kW/kg). Supercapacitors intermediate: 5-10 Wh/kg, 1-10 kW/kg. Ragone plot maps tradeoff.",
        reasoning_framework="""
Comparative electrochemical energy storage:

1. Batteries (Bulk Redox):
   Energy storage: chemical bonds, phase transformations
   Discharge: Li+ diffusion through solid (slow, D ~ 10^-10 cm^2/s)
   Energy density: 100-250 Wh/kg (Li-ion), 300+ Wh/kg (Li-S target)
   Power density: 100-500 W/kg (rate limited by solid-state diffusion)
   Cycle life: 500-5000 cycles (structural degradation)

2. Conventional Capacitors (Dielectric):
   Energy storage: electrostatic (dielectric polarization)
   Discharge: nanoseconds (speed of light in dielectric)
   Energy density: 0.01-0.1 Wh/kg (limited by breakdown voltage)
   Power density: 10,000+ kW/kg
   Cycle life: unlimited (no chemical change)

3. Supercapacitors (Double-Layer + Pseudo):
   Energy storage: electrostatic (EDLC) + surface redox (pseudo)
   Discharge: seconds (ion transport in pores)
   Energy density: 5-15 Wh/kg (higher than conventional capacitor)
   Power density: 1-10 kW/kg (higher than battery)
   Cycle life: 100,000-1,000,000 cycles

4. Ragone Plot Analysis:
   Log(energy density) vs log(power density)
   Batteries: upper left (high E, low P)
   Capacitors: lower right (low E, high P)
   Supercapacitors: middle (bridge the gap)
   Tradeoff: E*P ~ constant for a given technology

5. Hybrid Devices:
   Lithium-ion capacitor: Li-ion anode + AC cathode
   Asymmetric supercapacitor: battery-type + capacitor-type electrode
   Target: 20-30 Wh/kg, 5 kW/kg

6. Application Mapping:
   Long duration (>1 hour): batteries (EVs, grid storage)
   Short bursts (<1 min): supercapacitors (regen braking, pulse power)
   Ultra-fast (<1 sec): conventional capacitors (camera flash, power conditioning)

7. Cost Considerations:
   Batteries: $/kWh metric (currently ~$100-150/kWh for Li-ion pack)
   Supercapacitors: $/kW metric (currently ~$1000-5000/kW)
   Lifetime cost: supercaps win on cycle life (no replacement)
""",
        key_factors=[
            "Energy density (Wh/kg) - determines range/runtime",
            "Power density (W/kg) - determines acceleration/peak load",
            "Cycle life (number of charge/discharge cycles)",
            "Cost ($/kWh for energy, $/kW for power)",
            "Self-discharge rate (supercaps higher than batteries)",
            "Operating temperature range"
        ],
        primary_authority=[
            "Winter & Brodd Chem. Rev. 104, 4245 (2004) - battery comparison",
            "Simon & Gogotsi Nature Materials 7, 845 (2008) - supercapacitor review",
            "Christen & Carlen J. Power Sources 91, 210 (2000) - Ragone plot theory"
        ],
        burden_holder="System designer must select energy storage based on application power/energy profile and cost constraints.",
        adversary_position="No single technology optimizes both energy and power; hybrids add complexity and cost; supercapacitors still expensive per kWh.",
        counter_arguments=[
            "Supercapacitors too expensive for long-duration storage",
            "Batteries too slow for high-power pulses",
            "Hybrid systems require two converters (cost and complexity)",
            "Self-discharge of supercaps problematic for long standby"
        ],
        resolution_strategy="Use batteries for base energy, supercaps for peak power assist; optimize via Ragone plot and duty cycle analysis; model lifecycle cost.",
        entity_scope="All electrochemical energy storage applications.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for fundamental tradeoffs; moderate for hybrid system optimization and cost projections.",
        controlling_precedent="Ragone plot framework and battery vs supercapacitor distinction universally accepted.",
        category=IssueCategory.CAPACITANCE
    ),

    DoctrineBlock(
        topic="Electrowinning and Electrorefining of Metals",
        keywords=["electrowinning", "electrorefining", "copper", "zinc", "current efficiency", "metal recovery"],
        conclusion_template="Electrowinning extracts metal from solution: M^n+ + ne- → M (cathode). Electrorefining purifies crude metal: impure anode dissolves, pure metal plates on cathode. Cu, Zn, Al major applications; current efficiency and energy consumption key metrics.",
        reasoning_framework="""
Electrowinning and electrorefining processes:

1. Electrowinning (EW):
   Cathode: M^n+ + ne- → M  (metal deposition)
   Anode: 2H2O → O2 + 4H+ + 4e-  (inert Pb or Ti-IrO2 anode)
   Example: Cu EW from leach solution (CuSO4 + H2SO4)
   Cu2+ + 2e- → Cu  at stainless steel or Cu cathode

2. Electrorefining (ER):
   Anode: impure metal (e.g., 99% Cu) dissolves
   Cathode: pure metal (99.99% Cu) plates
   Impurities: noble metals (Au, Ag) fall as anode slime (recovered)
                less noble metals (Fe, Ni, Zn) stay in solution
   Example: Cu refining, anode 98-99.5% Cu → cathode 99.99% Cu

3. Copper Electrowinning:
   Electrolyte: 35-45 g/L Cu2+, 150-200 g/L H2SO4
   Current density: 200-400 A/m^2
   Cathode: stainless steel or Ti starter sheet
   Anode: Pb-Ca-Sn alloy (inert, resistant to corrosion)
   Cell voltage: 1.8-2.2V (higher than thermodynamic 1.0V due to overpotentials)
   Energy: 1.8-2.2 kWh/kg Cu

4. Zinc Electrowinning:
   Electrolyte: 50-80 g/L Zn2+, 100-180 g/L H2SO4
   Current density: 400-600 A/m^2
   Cathode: Al sheet (Zn stripped off periodically)
   Anode: Pb-Ag alloy
   Cell voltage: 3.0-3.5V (high due to O2 overpotential)
   Energy: 3.0-3.5 kWh/kg Zn

5. Aluminum Smelting (Hall-Heroult Process):
   Not aqueous electrowinning (Al too reactive)
   Molten cryolite (Na3AlF6) at 960°C
   Cathode: carbon lining of cell
   Anode: carbon blocks (consumed: C + 2O2- → CO2 + 4e-)
   Al2O3 dissolved in cryolite, reduced to Al metal
   Energy: 13-15 kWh/kg Al (very energy-intensive)

6. Current Efficiency:
   eta_I = (actual metal deposited) / (theoretical from Faraday's law)
   Loss mechanisms: H2 evolution, short-circuiting, metal redissolution
   Cu EW: 85-95%, Zn EW: 88-92%
   Optimize: lower acidity, additives (gelatin, glue) to smooth deposit

7. Impurity Management:
   Fe, Mn oxidize at anode, precipitate as oxides (scavenge via bleeding electrolyte)
   Cl- increases anode corrosion → keep <20 ppm
   Organic impurities reduce current efficiency → activated carbon treatment
   Temperature control: 35-45°C (higher T → higher conductivity but more impurity issues)
""",
        key_factors=[
            "Current density (A/m^2) - tradeoff between rate and quality",
            "Electrolyte composition (metal concentration, acidity)",
            "Current efficiency (minimize H2 evolution, maximize metal deposition)",
            "Energy consumption (kWh/kg metal)",
            "Deposit quality (smoothness, purity)",
            "Temperature (affects conductivity and side reactions)"
        ],
        primary_authority=[
            "Schlesinger et al. Extractive Metallurgy of Copper (5th ed, Chapter 20)",
            "Free Hydrometallurgy (electrowinning chapter)",
            "Grjotheim & Kvande Aluminum Electrolysis (Hall-Heroult process)"
        ],
        burden_holder="Plant operator must optimize current density and electrolyte composition to maximize throughput and current efficiency while maintaining deposit quality.",
        adversary_position="High current density enables fast production but increases H2 evolution and dendritic growth; impurity buildup requires continuous bleed and makeup.",
        counter_arguments=[
            "H2 evolution unavoidable at high current (competes with metal deposition)",
            "Anode corrosion products contaminate electrolyte over time",
            "Deposit morphology sensitive to trace impurities (ppm level)",
            "Energy cost dominates economics (especially for Al smelting)"
        ],
        resolution_strategy="Use leveling agents and low-concentration impurity scavengers; bleed electrolyte periodically; optimize current density via pilot testing; recover noble metals from anode slime.",
        entity_scope="All primary metal production from ores or secondary from scrap.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for Cu and Zn electrowinning (mature processes); moderate for novel metal systems and energy optimization.",
        controlling_precedent="Faraday's law and current efficiency concept universally applied in extractive metallurgy.",
        category=IssueCategory.ELECTROPLATING
    ),

    DoctrineBlock(
        topic="Electron Transfer Kinetics and Marcus Theory",
        keywords=["Marcus theory", "electron transfer", "reorganization energy", "rate constant", "outer sphere"],
        conclusion_template="Marcus theory describes electron transfer rate k_ET via activation barrier determined by reorganization energy lambda and driving force delta_G_0. Outer-sphere ET (no bond breaking) follows parabolic rate vs overpotential. Inner-sphere ET involves bond formation.",
        reasoning_framework="""
Marcus electron transfer theory:

1. Outer-Sphere Electron Transfer:
   No chemical bonds broken/formed during ET
   Only solvent and reactant reorganization
   Example: [Fe(CN)6]3- + e- → [Fe(CN)6]4-
   Rate constant: k_ET = A * exp(-delta_G_act / RT)

2. Activation Energy (Marcus Equation):
   delta_G_act = (lambda + delta_G_0)^2 / (4*lambda)
   lambda = reorganization energy (solvent + inner-sphere)
   delta_G_0 = driving force (Gibbs free energy change)

3. Reorganization Energy Components:
   lambda_o: outer-sphere (solvent reorganization)
   lambda_i: inner-sphere (bond length changes)
   lambda = lambda_o + lambda_i

4. Rate Constant Regimes:
   Normal region (delta_G_0 < lambda): k_ET increases with driving force
   Barrierless (delta_G_0 = -lambda): maximum rate, no barrier
   Inverted region (delta_G_0 > lambda): k_ET decreases with driving force

5. Solvent Reorganization Energy:
   lambda_o depends on: ionic radii, dielectric constants (optical, static)
   Polar solvents (high epsilon): large lambda_o
   lambda_o = (e^2 / 4*pi*epsilon_0) * (1/2a - 1/r) * (1/epsilon_op - 1/epsilon_s)

6. Inner-Sphere Electron Transfer:
   Chemical bonds form in transition state (bridging ligand)
   Example: [Co(NH3)5Cl]2+ + [Cr(H2O)6]2+ → products (Cl- bridge)
   Activation energy higher than outer-sphere
   Rate constants 10^2 to 10^6 times slower than outer-sphere

7. Application to Electrode Reactions:
   Electrode = one reactant with continuum of states (metal Fermi level)
   Butler-Volmer equation as low-overpotential limit of Marcus
   Exchange current density i_0 related to lambda and delta_G_0
   Tafel slope deviations at high overpotential (inverted region)
""",
        key_factors=[
            "Reorganization energy lambda (solvent + inner-sphere)",
            "Driving force delta_G_0 (overpotential related)",
            "Pre-exponential factor A (collision frequency, electronic coupling)",
            "Temperature T (Arrhenius dependence)",
            "Solvent dielectric constants (epsilon_s, epsilon_op)",
            "Ionic radii and separation distance r"
        ],
        primary_authority=[
            "Marcus J. Chem. Phys. 24, 966 (1956) - original theory",
            "Marcus & Sutin Biochim. Biophys. Acta 811, 265 (1985) - review",
            "Bard & Faulkner Electrochemical Methods (Chapter 3, Marcus theory)"
        ],
        burden_holder="Analyst must estimate lambda from molecular parameters and solvent properties; validate via rate-overpotential curves.",
        adversary_position="Marcus theory assumes weak electronic coupling (non-adiabatic); strong coupling cases require modified models; inverted region rarely observed in electrochemistry.",
        counter_arguments=[
            "Inverted region hard to access at electrodes (electronic states continuous)",
            "lambda estimation requires detailed molecular structure",
            "Solvent dynamics not instantaneous (dynamic solvent effects)",
            "Inner-sphere pathways complicate interpretation"
        ],
        resolution_strategy="Use Marcus theory for outer-sphere redox; combine with transition state theory for inner-sphere; fit experimental Tafel slopes to extract lambda.",
        entity_scope="All homogeneous and heterogeneous electron transfer reactions.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for outer-sphere ET in well-defined solvents; moderate for inner-sphere and interfacial ET.",
        controlling_precedent="Marcus theory Nobel Prize 1992; widely validated for molecular ET.",
        category=IssueCategory.ELECTRODE_KINETICS
    ),

    DoctrineBlock(
        topic="Electrochemical CO2 Reduction",
        keywords=["CO2 reduction", "electrocatalysis", "formate", "CO", "C2+", "Faradaic efficiency"],
        conclusion_template="Electrochemical CO2 reduction converts CO2 to fuels/chemicals: CO2 + n H+ + n e- → products. Cu unique for C2+ (ethylene, ethanol); Au/Ag produce CO; Sn/Pb give formate. Faradaic efficiency and overpotential key metrics; competing HER major challenge.",
        reasoning_framework="""
Electrochemical CO2 reduction (CO2RR) framework:

1. Reduction Products by Catalyst:
   C1 products (2e-): CO, formate (HCOO-), formaldehyde, methanol
   C2+ products (multi-electron): ethylene (C2H4), ethanol (C2H5OH), acetate
   Cu: only metal producing C2+ at appreciable rates
   Au, Ag: high selectivity for CO (FE >90%)
   Sn, Pb, Hg: high selectivity for formate
   Ni, Fe, Pt: predominantly H2 (poor CO2RR selectivity)

2. Reaction Pathways:
   CO2 + e- → CO2*-  (first electron transfer, rate-limiting)
   CO2*- + H+ + e- → *COOH → CO + H2O  (proton-coupled ET)
   CO further reduced: *CO + 6H+ + 6e- → CH4 (on Ru, Ni)
   C-C coupling on Cu: 2*CO → *OCCO → C2H4 (ethylene)

3. Competing Hydrogen Evolution (HER):
   2H+ + 2e- → H2  (E_0 = 0V vs SHE)
   CO2 reduction potentials more negative (-0.1 to -0.5V)
   HER kinetically favored on most metals
   Suppression strategies: alkaline pH, CO2 saturation, selective catalysts

4. Faradaic Efficiency (FE):
   FE_product = (n_product * F) / Q_total * 100%
   Ideal: FE_CO + FE_formate + FE_C2+ + FE_H2 = 100%
   Best Cu catalysts: FE_C2H4 ~ 60% at -1.0V vs RHE
   Au nanoparticles: FE_CO > 90%

5. Overpotential Analysis:
   eta = E_applied - E_eq (typically 0.3-1.0V for CO2RR)
   Trade-off: higher current density requires higher overpotential
   Energy efficiency = (E_eq * FE) / E_applied

6. Mass Transport and Solubility:
   CO2 solubility in water: 34 mM at 1 atm, 25°C
   At high current density (>100 mA/cm^2), CO2 depletion
   Gas diffusion electrodes (GDE): supply CO2 directly to catalyst
   Flow cells: continuous CO2 feed

7. Electrolyte Effects:
   pH: acidic (suppress HER via proton availability), alkaline (carbonate buffer)
   Cations: Cs+ > K+ > Na+ > Li+ (larger cations stabilize CO2*-)
   Ionic liquids: high CO2 solubility, suppress HER

8. Catalyst Strategies:
   Nanostructuring: increase active sites, stabilize intermediates
   Alloying: CuAg, CuAu for tuned binding energies
   Oxide-derived Cu: subsurface defects, grain boundaries
   Molecular catalysts: porphyrins, phthalocyanines (homogeneous or immobilized)
""",
        key_factors=[
            "Catalyst material and morphology (determines product selectivity)",
            "Faradaic efficiency for target product",
            "Overpotential (energy efficiency)",
            "Current density (productivity, mA/cm^2)",
            "pH and electrolyte composition (suppresses HER, stabilizes intermediates)",
            "CO2 mass transport (GDE vs liquid electrolyte)"
        ],
        primary_authority=[
            "Hori Electrochemical CO2 Reduction on Metal Electrodes (in Modern Aspects of Electrochemistry)",
            "Kortlever et al. J. Phys. Chem. Lett. 6, 4073 (2015) - product distribution",
            "Nitopi et al. Chem. Rev. 119, 7610 (2019) - CO2RR comprehensive review"
        ],
        burden_holder="Researcher must optimize catalyst, electrolyte, and cell design to maximize FE for target product while minimizing overpotential.",
        adversary_position="CO2 reduction fundamentally challenging: CO2*- intermediate unstable, HER thermodynamically and kinetically favored, C-C coupling selectivity low on most catalysts.",
        counter_arguments=[
            "HER dominates on most metals (only Cu viable for C2+)",
            "C2+ selectivity limited by *CO dimerization kinetics",
            "High overpotentials (0.5-1.0V) reduce energy efficiency",
            "Catalyst stability issues (oxidation, poisoning, sintering)",
            "CO2 crossover to anode in membrane cells"
        ],
        resolution_strategy="Use oxide-derived Cu for C2+ products; Au/Ag for CO; alkaline electrolyte + Cs+ cations; GDE cell design; tandem catalysis (CO2→CO→C2+).",
        entity_scope="All electrochemical CO2 utilization and renewable fuel synthesis.",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence; CO2RR highly active research area, mechanisms debated, catalyst stability unproven at scale.",
        controlling_precedent="Hori's product distribution on metals widely cited; C-C coupling on Cu accepted but mechanisms under investigation.",
        category=IssueCategory.ELECTROLYSIS
    ),

    DoctrineBlock(
        topic="Ionic Conductivity in Solid Electrolytes",
        keywords=["solid electrolyte", "ionic conductivity", "NASICON", "garnet", "LLZO", "lithium"],
        conclusion_template="Solid electrolytes conduct ions (Li+, Na+) without liquid, enabling safer batteries. Ionic conductivity sigma = n * q * mu (carrier density, charge, mobility). LLZO garnet (Li7La3Zr2O12) and NASICON reach 10^-3 S/cm, competitive with liquid electrolytes.",
        reasoning_framework="""
Solid electrolyte electrochemistry and ion transport:

1. Ionic Conductivity Fundamentals:
   sigma = n * q * mu
   n = mobile ion concentration (ions/cm^3)
   q = ionic charge
   mu = ionic mobility (related to diffusion coefficient D via Nernst-Einstein)
   sigma = (n * q^2 * D) / (k_B * T)

2. Activation Energy for Conduction:
   sigma(T) = sigma_0 * exp(-E_a / k_B * T)
   E_a = activation energy (typically 0.3-0.6 eV for good solid electrolytes)
   Arrhenius plot: log(sigma) vs 1/T yields E_a

3. Lithium-Conducting Solid Electrolytes:
   LLZO garnet: Li7La3Zr2O12, cubic phase, sigma ~ 10^-3 S/cm at RT
   NASICON: Li1.3Al0.3Ti1.7(PO4)3, sigma ~ 10^-3 S/cm
   Sulfides: Li10GeP2S12 (LGPS), sigma ~ 10^-2 S/cm (highest reported)
   Polymers: PEO-LiTFSI, sigma ~ 10^-5 S/cm at RT, 10^-3 at 60°C

4. Interfacial Resistance:
   Solid-solid contacts have high resistance (poor wetting)
   Interface impedance >> bulk impedance in many systems
   Strategies: interlayers (polymer gel, LiPON), surface coating, pressing

5. Garnet (LLZO) Specifics:
   Cubic phase (Ia-3d) required for high conductivity
   Al or Ga doping stabilizes cubic phase: Li6.5La3Zr1.5Ta0.5O12
   Challenges: Li dendrite penetration along grain boundaries
   Surface Li2CO3 layer (from air exposure) blocks Li+ transport

6. Sulfide Electrolytes (LGPS):
   Higher ionic conductivity than oxides
   Soft material: better interfacial contact
   Disadvantages: air-sensitive, narrow electrochemical window, H2S release

7. Sodium-Conducting Solid Electrolytes:
   NASICON: Na1+xZr2SixP3-xO12, sigma ~ 10^-3 S/cm
   Beta-alumina: NaAl11O17, sigma ~ 10^-2 S/cm (high T)
   Applications: Na-S battery (300°C), Na-NiCl2 (ZEBRA battery)

8. Transport Number and Selectivity:
   Ideal solid electrolyte: t_+ = 1 (only cation conducts)
   Liquid electrolytes: t_+ ~ 0.3-0.5 (anion also mobile)
   Concentration polarization minimized with t_+ = 1
""",
        key_factors=[
            "Ionic conductivity sigma (S/cm) at operating temperature",
            "Activation energy E_a (eV)",
            "Interfacial resistance (contact impedance)",
            "Electrochemical stability window (V)",
            "Chemical stability vs Li metal and cathode materials",
            "Mechanical properties (dendrite resistance, fracture toughness)"
        ],
        primary_authority=[
            "Bachman et al. Chem. Rev. 116, 140 (2016) - solid electrolyte review",
            "Thangadurai et al. Chem. Soc. Rev. 43, 4714 (2014) - garnet electrolytes",
            "Kamaya et al. Nature Materials 10, 682 (2011) - LGPS discovery"
        ],
        burden_holder="Battery designer must select solid electrolyte balancing conductivity, stability, and interfacial resistance; optimize processing to minimize grain boundary impedance.",
        adversary_position="Solid electrolytes suffer from high interfacial resistance and brittleness; Li dendrite penetration along grain boundaries; lower conductivity than liquids at RT.",
        counter_arguments=[
            "Interfacial impedance dominates total resistance in many cells",
            "LLZO reacts with CO2/H2O forming insulating Li2CO3 layer",
            "Sulfides unstable vs high-voltage cathodes (decompose)",
            "Li dendrite propagation through grain boundaries causes shorts",
            "Manufacturing cost high (sintering at >1000°C for oxides)"
        ],
        resolution_strategy="Use LGPS for high conductivity; LLZO for stability; interlayers for interface; hot-pressing or spark plasma sintering to densify; surface treatments to remove Li2CO3.",
        entity_scope="All solid-state batteries (Li, Na) and high-temperature systems.",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence; solid-state battery technology still maturing, interfacial issues unsolved at scale.",
        controlling_precedent="LLZO and LGPS as leading solid electrolytes widely accepted; interface problem recognized as major barrier.",
        category=IssueCategory.BATTERY_CHEMISTRY
    ),

    DoctrineBlock(
        topic="Redox Flow Batteries",
        keywords=["flow battery", "vanadium", "redox", "membrane", "energy storage", "electrolyte"],
        conclusion_template="Redox flow batteries store energy in external electrolyte tanks: decoupled energy (tank size) and power (stack size). Vanadium redox flow battery (VRFB) uses V2+/V3+ (anode), V4+/V5+ (cathode). Membrane crossover and electrolyte cost are key challenges.",
        reasoning_framework="""
Redox flow battery electrochemistry and design:

1. Operating Principle:
   Energy stored in liquid electrolytes pumped through electrochemical cell
   Anode tank: V2+ ⇌ V3+ + e-  (E_0 ~ -0.26V vs SHE)
   Cathode tank: V4+ + e- ⇌ V5+  (E_0 ~ +1.0V vs SHE)
   Cell voltage: ~1.26V (open-circuit), ~1.0-1.4V (operating)

2. Energy and Power Decoupling:
   Energy capacity: tank volume × electrolyte concentration × voltage
   Power: electrode area × current density
   Scale energy: larger tanks
   Scale power: larger stack or more cells

3. Vanadium Redox Flow Battery (VRFB):
   All-vanadium chemistry: same element in both half-cells
   Crossover of V species doesn't cause permanent capacity loss (can rebalance)
   Electrolyte: 1-2 M VOSO4 in 2-5 M H2SO4
   Energy density: 20-35 Wh/L (electrolyte), 10-20 Wh/kg (system)
   Round-trip efficiency: 75-85%

4. Membrane Requirements:
   Separate anolyte and catholyte
   Proton conductive (H+ balances charge)
   Block vanadium crossover (V species diffusion → capacity loss)
   Nafion: high H+ conductivity but significant V crossover
   Anion exchange membranes: lower V crossover but lower conductivity

5. Electrode Materials:
   Carbon felt or graphite felt: high surface area, porous
   Activation: thermal or chemical treatment to increase wettability
   Catalysis: oxygen functional groups accelerate V redox kinetics

6. Alternative Flow Battery Chemistries:
   Zinc-bromine: Zn2+/Zn (anode), Br-/Br2 (cathode) - low cost, Br2 hazard
   Iron-chromium: Fe2+/Fe3+, Cr2+/Cr3+ - low cost, low voltage (1.18V)
   Organic redox flow: quinones, viologens - tunable potential, lower solubility

7. Performance Metrics:
   Current density: 50-100 mA/cm^2 (limited by kinetics and mass transport)
   Voltage efficiency: eta_V = V_discharge / V_charge (typically 85-90%)
   Coulombic efficiency: eta_C = Q_discharge / Q_charge (90-95%, crossover loss)
   Energy efficiency: eta_E = eta_V * eta_C (75-85%)

8. Applications:
   Grid-scale energy storage: MW-scale, 4-8 hour duration
   Renewable integration: solar/wind firming
   Advantages: long cycle life (10,000+ cycles), no depth-of-discharge limit
   Disadvantages: low energy density, electrolyte cost, footprint
""",
        key_factors=[
            "Electrolyte concentration and volume (energy capacity)",
            "Membrane selectivity (H+ transport, V crossover)",
            "Electrode kinetics and mass transport (power density)",
            "Round-trip efficiency (voltage, coulombic, energy)",
            "Electrolyte cost ($/kWh)",
            "Cycle life and degradation (membrane fouling, V precipitation)"
        ],
        primary_authority=[
            "Skyllas-Kazacos et al. J. Electrochem. Soc. 158, R55 (2011) - VRFB review",
            "Weber et al. J. Appl. Electrochem. 41, 1137 (2011) - flow battery modeling",
            "Ponce de Leon et al. J. Power Sources 160, 716 (2006) - flow battery fundamentals"
        ],
        burden_holder="Flow battery designer must optimize electrolyte concentration, membrane selectivity, and stack design to balance energy density, power, and cost.",
        adversary_position="Flow batteries have low energy density vs Li-ion; electrolyte cost high; membrane crossover causes capacity fade; large footprint.",
        counter_arguments=[
            "Energy density 10-20 Wh/kg << Li-ion 150-250 Wh/kg",
            "V2O5 (vanadium source) expensive and supply-limited",
            "Nafion membranes allow V crossover (1-3%/year capacity loss)",
            "Electrolyte precipitation at high SOC or low temperature",
            "Pumping parasitic losses reduce system efficiency"
        ],
        resolution_strategy="Use flow batteries for stationary grid storage (not mobile); develop low-cost organic redox species; improve membrane selectivity; hybrid pumping strategies.",
        entity_scope="Grid-scale energy storage, microgrids, renewable integration.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for VRFB fundamentals; moderate for alternative chemistries and long-term degradation.",
        controlling_precedent="VRFB as leading flow battery chemistry widely accepted; membrane crossover recognized as key challenge.",
        category=IssueCategory.BATTERY_CHEMISTRY
    ),

    DoctrineBlock(
        topic="pH Measurement and Glass Electrode",
        keywords=["pH", "glass electrode", "ISE", "ion-selective", "Nernst", "reference electrode"],
        conclusion_template="Glass electrode measures pH via Nernst equation: E = E_0 + (2.303*RT/F)*pH. Glass membrane selective to H+ via ion-exchange; combines with reference electrode for complete cell. Calibration with buffer solutions required.",
        reasoning_framework="""
pH measurement electrochemistry and glass electrode:

1. Nernst Equation for pH:
   E = E_0 + (RT/F)*ln(a_H+)
   E = E_0 - (2.303*RT/F)*pH  (since pH = -log(a_H+))
   At 25°C: E = E_0 - 0.0592*pH  (59.2 mV/pH unit)

2. Glass Electrode Structure:
   Thin glass membrane (50-100 microns, pH-sensitive)
   Inner reference: Ag/AgCl in HCl solution (fixed pH)
   Outer membrane: ion-exchange with solution H+
   High-resistance glass (10^8 to 10^9 ohms)

3. Glass Membrane Chemistry:
   Silicate glass doped with alkali (Na+, Li+)
   Hydrated gel layer (~10nm) on surface
   H+ exchanges with Na+ in gel: Na+ (glass) + H+ (solution) ⇌ H+ (glass) + Na+ (solution)
   Membrane potential: E_membrane = k * log(a_H+_inner / a_H+_outer)

4. Complete pH Cell:
   Glass electrode + external reference electrode
   E_cell = E_glass - E_ref = E_0 - 0.0592*pH
   Reference: Ag/AgCl or SCE (stable potential)
   Junction potential: minimized with salt bridge (KCl)

5. Calibration:
   Two-point calibration: pH 4 and pH 7, or pH 7 and pH 10
   Buffer solutions: phthalate (pH 4.01), phosphate (pH 7.00), borate (pH 10.01)
   Slope calibration: verify 59.2 mV/pH at 25°C (Nernst slope)
   Temperature compensation: 2.303*RT/F varies with T

6. Sources of Error:
   Asymmetry potential: glass membrane aging (recalibrate regularly)
   Alkaline error: at pH >12, Na+ interferes (glass responds to Na+ not just H+)
   Acid error: at pH <1, activity coefficient effects
   Junction potential drift: KCl leakage, contamination
   Temperature: 59.2 mV/pH at 25°C, 61.5 at 40°C, 57.2 at 10°C

7. Ion-Selective Electrodes (ISE):
   Extend concept to other ions: F-, Cl-, Ca2+, K+, NO3-
   Different membrane materials: LaF3 for F-, liquid ion exchanger for Ca2+
   Nernst response: E = E_0 + (2.303*RT/zF)*log(a_ion)
   z = ion charge
   Selectivity coefficient: response to interfering ions

8. Solid-State pH Sensors:
   ISFET (ion-selective field-effect transistor): no glass membrane
   Gate surface (SiO2 or Si3N4) responds to H+
   Advantages: miniaturizable, robust, fast response
   Disadvantages: drift, temperature sensitivity
""",
        key_factors=[
            "Glass membrane integrity and hydration",
            "Calibration buffer accuracy (traceability to NIST)",
            "Temperature (affects Nernst slope)",
            "Reference electrode stability (Ag/AgCl, SCE)",
            "Junction potential (salt bridge composition)",
            "pH range (alkaline error >12, acid error <1)"
        ],
        primary_authority=[
            "Bates Determination of pH (NBS monograph)",
            "IUPAC Recommendations for pH measurement",
            "Bard & Faulkner Electrochemical Methods (Chapter 14, ISE)"
        ],
        burden_holder="Analyst must calibrate electrode with fresh buffers, verify Nernst slope, and account for temperature; recalibrate regularly.",
        adversary_position="Glass electrode fragile, requires hydration, drifts over time; alkaline error limits high pH measurement; junction potential adds systematic error.",
        counter_arguments=[
            "Glass membrane breaks easily (fragile)",
            "Alkaline error at pH >12 (Na+ interference)",
            "Drift requires frequent recalibration",
            "Junction potential varies with sample ionic strength",
            "Response time slow in low ionic strength solutions"
        ],
        resolution_strategy="Use fresh buffers, two-point calibration, temperature compensation; for pH >12 use ISFET or colorimetric methods; low-maintenance reference electrodes.",
        entity_scope="All pH measurement applications (chemistry, biology, environmental, industrial).",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for pH 2-12 range with proper calibration; moderate for extreme pH or very low ionic strength.",
        controlling_precedent="Glass electrode and Nernst pH response universally accepted; NIST buffer standards.",
        category=IssueCategory.ELECTROANALYTICAL
    ),

    DoctrineBlock(
        topic="Electrochemical Machining (ECM)",
        keywords=["electrochemical machining", "ECM", "anodic dissolution", "metal removal", "current density", "electrolyte flow"],
        conclusion_template="Electrochemical machining removes metal via anodic dissolution: M → M^n+ + ne-. Controlled by current density and electrolyte flow. Non-contact process (no tool wear), high precision, applicable to hard materials. Faraday's law governs material removal rate.",
        reasoning_framework="""
Electrochemical machining fundamentals:

1. Anodic Dissolution Process:
   Workpiece (anode): M → M^n+ + ne-
   Tool (cathode): often H+ reduction or O2 reduction (no deposition)
   Material removal: purely electrochemical, no mechanical force

2. Material Removal Rate (MRR):
   Faraday's law: MRR = (I * M) / (n * F * rho) * 60  (mm^3/min)
   I = current (A)
   M = atomic mass (g/mol)
   n = valence (electrons per atom)
   rho = density (g/cm^3)
   Typical: 1000 A removes ~1 cm^3/min for steel

3. Electrolyte:
   High conductivity: NaCl, NaNO3 (5-30 wt%)
   pH control: neutral to slightly acidic (passivation avoidance)
   Flow rate: 10-60 m/s (remove dissolved metal ions, dissipate heat)
   Temperature: 20-50°C (controlled via cooling)

4. Current Density and Gap:
   Interelectrode gap: 0.1-0.5 mm (small gap → high resolution)
   Current density: 10-100 A/cm^2 (high → fast removal)
   Gap profile: equilibrium shape where dissolution rate matches tool feed rate
   Ohmic control: current distribution follows conductivity field

5. Surface Finish:
   Roughness Ra: 0.1-1 micron (better than machining, similar to grinding)
   No mechanical stress or heat-affected zone (HAZ)
   Passivation: in some alloys, oxide forms reducing removal rate
   Pulsed ECM: improve precision, reduce stray current

6. Advantages:
   No tool wear (cathode not consumed)
   Machinable hard materials (tool steel, titanium, Inconel)
   Complex shapes (turbine blades, dies)
   No burrs or residual stress

7. Disadvantages:
   Low material removal rate vs mechanical machining
   Electrolyte disposal (environmental cost)
   Stray current causes overcut (dimensional tolerance)
   Surface finish dependent on alloy microstructure

8. Applications:
   Aerospace: turbine blade cooling holes, engine components
   Medical: surgical instruments (stainless steel)
   Tooling: die sinking, EDM electrode production
   Deburring: electrochemical deburring (ECD) after machining
""",
        key_factors=[
            "Current density (A/cm^2) - controls removal rate",
            "Interelectrode gap (mm) - precision tradeoff",
            "Electrolyte conductivity and flow rate",
            "Tool feed rate (matches dissolution rate)",
            "Material valence and density (MRR calculation)",
            "Surface passivation (reduces efficiency for some alloys)"
        ],
        primary_authority=[
            "McGeough Principles of Electrochemical Machining (definitive text)",
            "Rajurkar et al. CIRP Annals 48, 567 (1999) - ECM review",
            "Kozak J. Mater. Process. Technol. 76, 170 (1998) - pulse ECM"
        ],
        burden_holder="Machinist must optimize current density, gap, and electrolyte flow to achieve target removal rate and surface finish; control passivation for difficult alloys.",
        adversary_position="ECM slower than mechanical machining; stray current causes overcut reducing precision; electrolyte management complex; passivating alloys problematic.",
        counter_arguments=[
            "MRR low vs milling/turning (cm^3/min vs cm^3/sec)",
            "Overcut from stray current (0.1-0.3mm typical)",
            "Electrolyte corrosive (NaCl) and disposal cost",
            "Passivating alloys (stainless steel, Ti) resist uniform dissolution",
            "Capital cost of ECM equipment high"
        ],
        resolution_strategy="Use pulsed ECM for precision; passivation inhibitors in electrolyte; combine with mechanical pre-machining for roughing; recycle electrolyte.",
        entity_scope="All precision metal removal applications where hardness or complexity precludes mechanical methods.",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for Faraday's law and fundamental process; moderate for surface finish prediction and passivation control.",
        controlling_precedent="Faraday's law for MRR universally applied; ECM mature technology in aerospace.",
        category=IssueCategory.ELECTROPLATING
    ),
]

# ============================================================================
# METRICS AND TELEMETRY
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.query_count = 0
        self.total_latency = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.error_count = 0
        self.triggered_doctrines = defaultdict(int)
        self.start_time = time.time()

    def record_query(self, latency: float, doctrines: List[str], cache_hit: bool):
        self.query_count += 1
        self.total_latency += latency
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        for d in doctrines:
            self.triggered_doctrines[d] += 1

    def record_error(self):
        self.error_count += 1

    def get_stats(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "total_queries": self.query_count,
            "avg_latency_ms": (self.total_latency / self.query_count * 1000) if self.query_count > 0 else 0,
            "cache_hit_rate": (self.cache_hits / (self.cache_hits + self.cache_misses)) if (self.cache_hits + self.cache_misses) > 0 else 0,
            "error_count": self.error_count,
            "uptime_seconds": uptime,
            "doctrines_triggered": len(self.triggered_doctrines),
            "top_doctrines": sorted(self.triggered_doctrines.items(), key=lambda x: x[1], reverse=True)[:10]
        }

TELEMETRY = TelemetryCollector()

# ============================================================================
# CORE ENGINE
# ============================================================================

class CHEM10Engine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.doctrine_index = self._build_index()
        logger.info(f"CHEM10 Engine initialized with {len(self.doctrines)} doctrine blocks")

    def _build_index(self) -> Dict[str, List[int]]:
        """Build keyword index for fast doctrine lookup"""
        index = defaultdict(list)
        for i, doctrine in enumerate(self.doctrines):
            for keyword in doctrine.keywords:
                index[keyword.lower()].append(i)
            index[doctrine.topic.lower()].append(i)
        return index

    def search_doctrines(self, query: str) -> List[Tuple[DoctrineBlock, float]]:
        """Search doctrines by keyword matching"""
        query_lower = query.lower()
        query_tokens = set(query_lower.split())

        scores = defaultdict(float)
        for token in query_tokens:
            if token in self.doctrine_index:
                for idx in self.doctrine_index[token]:
                    scores[idx] += 1.0

        # Boost for topic/keyword exact matches
        for i, doctrine in enumerate(self.doctrines):
            if any(kw in query_lower for kw in doctrine.keywords):
                scores[i] += 2.0
            if doctrine.topic.lower() in query_lower:
                scores[i] += 3.0

        results = [(self.doctrines[i], score) for i, score in scores.items() if score > 0]
        return sorted(results, key=lambda x: x[1], reverse=True)

    def three_layer_response(self, question: str, mode: ResponseMode, zone: AnalysisZone) -> QueryResponse:
        """TIE-20 Component: Three-layer response with doctrine cache, semantic search, deep analysis"""
        start_time = time.time()

        # Layer 1: Doctrine Cache Search
        matched_doctrines = self.search_doctrines(question)
        cache_hit = len(matched_doctrines) > 0

        if not matched_doctrines:
            TELEMETRY.record_query(time.time() - start_time, [], False)
            return QueryResponse(
                answer="No relevant electrochemistry doctrines found for this query.",
                confidence=ConfidenceLevel.DISCLOSURE.value,
                reasoning="Query did not match any cached doctrine blocks.",
                authorities_cited=[],
                triggered_doctrines=[],
                analysis_zone=zone.value,
                determinism_hash=self._hash_response("No match"),
                telemetry={"latency_ms": (time.time() - start_time) * 1000, "layer": "cache_miss"}
            )

        # Use top doctrines
        top_doctrines = matched_doctrines[:3]
        triggered = [d.topic for d, _ in top_doctrines]

        # Build response based on mode
        if mode == ResponseMode.FAST:
            answer = self._build_fast_response(top_doctrines, question)
        elif mode == ResponseMode.DEFENSE:
            answer = self._build_defense_response(top_doctrines, question)
        else:  # MEMO
            answer = self._build_memo_response(top_doctrines, question)

        # Collect authorities
        authorities = []
        for doctrine, _ in top_doctrines:
            authorities.extend(doctrine.primary_authority)

        # Confidence stratification
        confidence = top_doctrines[0][0].confidence.value if top_doctrines else ConfidenceLevel.DISCLOSURE.value

        # Reasoning summary
        reasoning = f"Matched {len(top_doctrines)} doctrines: {', '.join(triggered)}. "
        reasoning += f"Analysis zone: {zone.value}. Response mode: {mode.value}."

        latency = time.time() - start_time
        TELEMETRY.record_query(latency, triggered, cache_hit)

        return QueryResponse(
            answer=answer,
            confidence=confidence,
            reasoning=reasoning,
            authorities_cited=list(set(authorities)),
            triggered_doctrines=triggered,
            analysis_zone=zone.value,
            determinism_hash=self._hash_response(answer),
            telemetry={"latency_ms": latency * 1000, "layer": "doctrine_cache", "doctrines": len(top_doctrines)}
        )

    def _build_fast_response(self, doctrines: List[Tuple[DoctrineBlock, float]], question: str) -> str:
        """Build concise FAST mode response"""
        primary = doctrines[0][0]
        answer = f"{primary.conclusion_template}\n\n"
        answer += f"Key factors: {', '.join(primary.key_factors[:3])}.\n\n"
        answer += f"Primary authority: {primary.primary_authority[0]}"
        return answer

    def _build_defense_response(self, doctrines: List[Tuple[DoctrineBlock, float]], question: str) -> str:
        """Build audit-ready DEFENSE mode response"""
        answer = "ELECTROCHEMISTRY ANALYSIS\n\n"
        for doctrine, score in doctrines[:2]:
            answer += f"**{doctrine.topic}**\n\n"
            answer += f"{doctrine.conclusion_template}\n\n"
            answer += f"Reasoning Framework:\n{doctrine.reasoning_framework[:500]}...\n\n"
            answer += f"Key Factors:\n"
            for factor in doctrine.key_factors:
                answer += f"- {factor}\n"
            answer += f"\nPrimary Authority:\n"
            for auth in doctrine.primary_authority:
                answer += f"- {auth}\n"
            answer += f"\nConfidence: {doctrine.confidence.value}\n"
            answer += f"Confidence Stratification: {doctrine.confidence_stratification}\n\n"
            answer += "---\n\n"
        return answer

    def _build_memo_response(self, doctrines: List[Tuple[DoctrineBlock, float]], question: str) -> str:
        """Build comprehensive MEMO mode response"""
        answer = "ELECTROCHEMISTRY INTELLIGENCE MEMORANDUM\n\n"
        answer += f"QUERY: {question}\n\n"
        answer += "EXECUTIVE SUMMARY\n\n"
        primary = doctrines[0][0]
        answer += f"{primary.conclusion_template}\n\n"
        answer += "DETAILED ANALYSIS\n\n"

        for i, (doctrine, score) in enumerate(doctrines, 1):
            answer += f"{i}. {doctrine.topic}\n\n"
            answer += f"Conclusion: {doctrine.conclusion_template}\n\n"
            answer += f"Reasoning Framework:\n{doctrine.reasoning_framework}\n\n"
            answer += f"Key Factors:\n"
            for factor in doctrine.key_factors:
                answer += f"  - {factor}\n"
            answer += f"\nPrimary Authority:\n"
            for auth in doctrine.primary_authority:
                answer += f"  - {auth}\n"
            answer += f"\nBurden: {doctrine.burden_holder}\n"
            answer += f"Adversary Position: {doctrine.adversary_position}\n"
            answer += f"Counter-Arguments:\n"
            for arg in doctrine.counter_arguments:
                answer += f"  - {arg}\n"
            answer += f"\nResolution Strategy: {doctrine.resolution_strategy}\n"
            answer += f"Confidence: {doctrine.confidence.value}\n"
            answer += f"Confidence Stratification: {doctrine.confidence_stratification}\n\n"
            answer += "---\n\n"

        return answer

    def _hash_response(self, text: str) -> str:
        """TIE-20 Component: Determinism hash (SHA-256)"""
        return hashlib.sha256(text.encode()).hexdigest()[:16]

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Electrochemistry Intelligence Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CHEM10Engine()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE-20 Component: Health endpoint"""
    stats = TELEMETRY.get_stats()
    return HealthResponse(
        status="operational",
        engine_id=ENGINE_ID,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=stats["uptime_seconds"],
        total_queries=stats["total_queries"],
        avg_latency_ms=stats["avg_latency_ms"],
        cache_hit_rate=stats["cache_hit_rate"]
    )

@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint with TIE-20 three-layer response"""
    try:
        response = engine.three_layer_response(
            question=request.question,
            mode=request.mode,
            zone=request.zone
        )

        # Audit trail logging (TIE-20 component)
        logger.info(f"QUERY | Mode: {request.mode.value} | Zone: {request.zone.value} | Doctrines: {len(response.triggered_doctrines)} | Hash: {response.determinism_hash}")

        return response
    except Exception as e:
        TELEMETRY.record_error()
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/stats")
async def get_stats():
    """Get detailed telemetry statistics"""
    return TELEMETRY.get_stats()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"Categories: {len(set(d.category for d in DOCTRINE_CACHE))}")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
