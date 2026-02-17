"""
CHEM18 Chemical Thermodynamics Intelligence Engine
TIE-Grade Engine for Equation of State Models, Phase Equilibria, Reaction Equilibria

Port: 9300
Version: 1.0.0
Lines: 1000-1400 target with 25+ doctrine blocks
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_ID = "CHEM18"
ENGINE_NAME = "Chemical Thermodynamics Intelligence Engine"
VERSION = "1.0.0"
PORT = 9300

logger.add(
    f"chem18_thermodynamics_{datetime.now():%Y%m%d}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS AND DATACLASSES
# ═══════════════════════════════════════════════════════════════════════════

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
    EQUATION_OF_STATE = "EQUATION_OF_STATE"
    PHASE_EQUILIBRIA = "PHASE_EQUILIBRIA"
    REACTION_EQUILIBRIA = "REACTION_EQUILIBRIA"
    ACTIVITY_COEFFICIENTS = "ACTIVITY_COEFFICIENTS"
    THERMODYNAMIC_PROPERTIES = "THERMODYNAMIC_PROPERTIES"
    PROCESS_SIMULATION = "PROCESS_SIMULATION"
    FUGACITY_ANALYSIS = "FUGACITY_ANALYSIS"
    EXCESS_PROPERTIES = "EXCESS_PROPERTIES"
    CRITICAL_PHENOMENA = "CRITICAL_PHENOMENA"
    THERMAL_ANALYSIS = "THERMAL_ANALYSIS"


@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: List[str]
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
    issue_category: IssueCategory
    zoned_use: AnalysisZone


@dataclass
class TelemetryData:
    query_id: str
    timestamp: float
    mode: ResponseMode
    latency_ms: float
    cache_hit: bool
    doctrine_triggered: List[str]
    confidence: ConfidenceLevel
    error_domain: Optional[str] = None


@dataclass
class MetricsSnapshot:
    total_queries: int = 0
    cache_hits: int = 0
    avg_latency_ms: float = 0.0
    error_rate: float = 0.0
    doctrine_coverage: float = 0.0
    uptime_seconds: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    context: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    query_id: str
    answer: str
    confidence: ConfidenceLevel
    doctrine_triggered: List[str]
    latency_ms: float
    mode: ResponseMode
    determinism_hash: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    doctrine_count: int
    last_query: Optional[str]


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL CHEMICAL THERMODYNAMICS BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Peng-Robinson Equation of State Application",
        keywords=["peng-robinson", "cubic eos", "hydrocarbon", "natural gas", "critical properties"],
        conclusion_template=[
            "The Peng-Robinson equation of state is recommended for hydrocarbon systems.",
            "Critical properties and acentric factor must be accurately determined.",
            "Mixing rules significantly affect multi-component predictions."
        ],
        reasoning_framework=[
            "The Peng-Robinson (PR) EOS is a cubic equation of state developed in 1976.",
            "Form: P = RT/(V-b) - a*alpha(T)/(V^2 + 2bV - b^2)",
            "Parameter a relates to attractive forces, b to molecular volume.",
            "Temperature dependency through alpha function improves vapor pressure prediction.",
            "Acentric factor omega captures molecular non-sphericity.",
            "PR excels for hydrocarbon vapor-liquid equilibria over wide temperature ranges.",
            "Accurate critical temperature Tc, critical pressure Pc, and omega are essential.",
            "Binary interaction parameters kij improve mixture predictions.",
            "van der Waals mixing rules: a_mix = sum(xi*xj*(ai*aj)^0.5*(1-kij))",
            "PR typically superior to Soave-Redlich-Kwong for liquid densities.",
            "Fails for highly polar systems or hydrogen bonding without modifications.",
            "Volume translation improves liquid density without affecting VLE.",
            "Widely implemented in process simulators (Aspen, HYSYS, ProMax).",
            "GERG-2008 preferred for natural gas custody transfer applications.",
            "PR provides good estimates for enthalpy and entropy departures.",
            "Fugacity coefficient derivation enables phase equilibrium calculations.",
            "Two-phase flash calculations require iterative solution of Rachford-Rice equation.",
            "Stability analysis via tangent plane distance prevents false solutions.",
            "Near-critical region requires careful numerical handling.",
            "Supercritical extraction applications benefit from PR accuracy.",
            "Recent modifications include volume-translated PR (VTPR) and group contribution methods.",
            "Quantum corrections needed for hydrogen and helium at cryogenic temperatures."
        ],
        key_factors=[
            "Accurate critical property data",
            "Binary interaction parameter regression",
            "Appropriate mixing rule selection",
            "Temperature and pressure operating range",
            "System polarity and hydrogen bonding",
            "Required property accuracy (VLE, density, enthalpy)",
            "Computational efficiency requirements",
            "Availability of experimental data for validation"
        ],
        primary_authority=[
            "Peng, D.-Y., Robinson, D.B. (1976). A New Two-Constant Equation of State. Ind. Eng. Chem. Fundam.",
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics, 5th Ed.",
            "Kunz, O., Wagner, W. (2012). The GERG-2008 Wide-Range Equation of State for Natural Gases."
        ],
        burden_holder="Engineer selecting thermodynamic model",
        adversary_position="Simpler ideal gas law or generalized correlations suffice",
        counter_arguments=[
            "Ideal gas law fails at high pressures and low temperatures",
            "Generalized correlations lack accuracy for design calculations",
            "Safety margins cannot compensate for systematic thermodynamic errors",
            "Process optimization requires accurate property predictions",
            "Equipment sizing errors from poor thermodynamics are costly"
        ],
        resolution_strategy="Validate EOS predictions against experimental data; use PR for hydrocarbons, activity coefficient models for polar systems",
        entity_scope="Hydrocarbon processing, natural gas, petroleum refining",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for non-polar hydrocarbons, moderate for polar systems",
        controlling_precedent="Industry standard for hydrocarbon VLE calculations per API and GPA guidelines",
        issue_category=IssueCategory.EQUATION_OF_STATE,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="NRTL Activity Coefficient Model for Non-Ideal Liquids",
        keywords=["nrtl", "activity coefficient", "non-ideal", "liquid-liquid", "azeotrope"],
        conclusion_template=[
            "NRTL accurately models non-ideal liquid mixtures with significant deviations from ideality.",
            "Three binary parameters per pair required; regression from VLE or LLE data.",
            "Handles both VLE and LLE in same framework unlike UNIQUAC/Wilson."
        ],
        reasoning_framework=[
            "Non-Random Two Liquid (NRTL) model developed by Renon and Prausnitz (1968).",
            "Activity coefficient ln(gamma_i) derived from local composition concept.",
            "Key equation: ln(gamma_i) = [sum_j(tau_ji*G_ji*x_j)/sum_k(G_ki*x_k)] + sum_j[x_j*G_ij/sum_k(G_kj*x_k) * (tau_ij - sum_m(x_m*tau_mj*G_mj)/sum_k(G_kj*x_k))]",
            "Parameters tau_ij and tau_ji are temperature-dependent energy parameters.",
            "Non-randomness parameter alpha_ij (typically 0.2-0.47) controls local ordering.",
            "G_ij = exp(-alpha_ij * tau_ij) is Boltzmann-like factor.",
            "Three binary parameters: tau_12, tau_21, alpha_12 for each binary.",
            "Parameter regression requires experimental VLE or LLE data.",
            "NRTL predicts both vapor-liquid and liquid-liquid equilibria.",
            "Particularly effective for systems with partial miscibility.",
            "Alcohol-water, alcohol-hydrocarbon systems well-represented.",
            "Azeotrope prediction capability superior to ideal solution models.",
            "Excess Gibbs energy framework ensures thermodynamic consistency.",
            "Temperature dependence: tau_ij = a_ij + b_ij/T or a_ij + b_ij/T + c_ij*ln(T)",
            "Ternary and multicomponent predictions from binary parameters only.",
            "Database: DECHEMA VLE data, NIST ThermoData Engine.",
            "Aspen Plus uses modified NRTL for electrolyte systems (eNRTL).",
            "Limitations: poor extrapolation beyond data range, no predictive capability without data.",
            "Group contribution methods like UNIFAC offer predictive alternative.",
            "Must satisfy Gibbs-Duhem equation for thermodynamic consistency.",
            "Activity coefficients affect distillation column design, liquid-liquid extraction.",
            "Infinite dilution activity coefficients validate model accuracy."
        ],
        key_factors=[
            "Availability of binary VLE or LLE data",
            "Temperature range of operation",
            "Presence of azeotropes or immiscibility",
            "System polarity and hydrogen bonding strength",
            "Required accuracy for process design",
            "Computational cost for flash calculations",
            "Extrapolation beyond experimental data",
            "Thermodynamic consistency validation"
        ],
        primary_authority=[
            "Renon, H., Prausnitz, J.M. (1968). Local Compositions in Thermodynamic Excess Functions. AIChE J.",
            "Prausnitz, J.M., Lichtenthaler, R.N., Azevedo, E.G. Molecular Thermodynamics of Fluid-Phase Equilibria, 3rd Ed.",
            "Gmehling, J., et al. Azeotropic Data, 3 volumes. VCH Publishers."
        ],
        burden_holder="Process engineer designing separation equipment",
        adversary_position="Raoult's law or ideal solution assumption is adequate",
        counter_arguments=[
            "Non-ideal systems show large deviations from Raoult's law",
            "Azeotropes cannot be predicted by ideal models",
            "Liquid-liquid phase splits require activity coefficient models",
            "Equipment sizing based on ideal assumptions leads to failure",
            "Safety analysis requires accurate composition predictions"
        ],
        resolution_strategy="Use NRTL for highly non-ideal systems; validate predictions; consider UNIFAC if no data available",
        entity_scope="Chemical processing, distillation, liquid extraction, pharmaceutical separations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence within data range, low confidence for extrapolation",
        controlling_precedent="DIPPR and NIST standard for non-ideal liquid activity coefficients",
        issue_category=IssueCategory.ACTIVITY_COEFFICIENTS,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Gibbs Free Energy Minimization for Chemical Equilibrium",
        keywords=["gibbs energy", "chemical equilibrium", "reaction", "equilibrium constant", "minimization"],
        conclusion_template=[
            "Chemical equilibrium occurs when Gibbs free energy is minimized at constant T and P.",
            "Equilibrium composition calculated from equilibrium constant K(T).",
            "Temperature dependence of K follows van't Hoff equation."
        ],
        reasoning_framework=[
            "At equilibrium, total Gibbs free energy G = sum(n_i * mu_i) is at minimum.",
            "Chemical potential mu_i = mu_i_standard + RT*ln(a_i) where a_i is activity.",
            "For ideal gas: a_i = P_i/P_standard = y_i*P/P_standard.",
            "Equilibrium condition: sum(nu_i * mu_i) = 0 for reaction sum(nu_i * A_i) = 0.",
            "Equilibrium constant K = exp(-Delta_G_standard/RT).",
            "van't Hoff equation: d(ln K)/dT = Delta_H_standard/(R*T^2).",
            "Integrated form: ln(K2/K1) = -(Delta_H_standard/R)*(1/T2 - 1/T1) if Delta_H constant.",
            "More accurate: Delta_G_standard(T) = Delta_H_standard(T) - T*Delta_S_standard(T).",
            "Heat capacity integration: Delta_H(T) = Delta_H(T_ref) + integral(Delta_Cp dT).",
            "For non-ideal systems, activity a_i = gamma_i * x_i (liquid) or phi_i * y_i * P (gas).",
            "Simultaneous reactions require solving multiple equilibrium expressions.",
            "Le Chatelier's principle: system shifts to counteract imposed change.",
            "Pressure increase favors side with fewer moles (gases).",
            "Temperature increase favors endothermic direction (Delta_H > 0).",
            "Inert addition at constant P shifts equilibrium via dilution effect.",
            "Gibbs reactor in process simulators minimizes G subject to atom balances.",
            "Lagrange multipliers enforce elemental conservation constraints.",
            "Successive substitution or Newton-Raphson solve equilibrium equations.",
            "Haber ammonia synthesis: N2 + 3H2 <-> 2NH3, exothermic, favored by high P.",
            "Methane steam reforming: CH4 + H2O <-> CO + 3H2, endothermic, high T.",
            "Water-gas shift: CO + H2O <-> CO2 + H2, moderately exothermic.",
            "Thermodynamic databases: NASA polynomials, JANAF tables, Barin compilations."
        ],
        key_factors=[
            "Reaction stoichiometry and elemental balances",
            "Standard Gibbs energy of formation data",
            "Temperature and pressure of reaction",
            "Phase of reactants and products",
            "Activity coefficient models for non-ideality",
            "Simultaneous equilibria interactions",
            "Kinetic vs. thermodynamic control",
            "Catalyst effect on rate but not equilibrium"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M. Introduction to Chemical Engineering Thermodynamics, 8th Ed.",
            "Chase, M.W. NIST-JANAF Thermochemical Tables, 4th Ed.",
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics."
        ],
        burden_holder="Reaction engineer predicting equilibrium conversion",
        adversary_position="Kinetics or catalyst performance more important than thermodynamics",
        counter_arguments=[
            "Thermodynamics sets upper limit on conversion",
            "Catalyst cannot overcome unfavorable equilibrium",
            "Economic viability requires understanding equilibrium constraints",
            "Process conditions (T, P) optimize based on equilibrium",
            "Bypassing equilibrium limitations requires different chemistry"
        ],
        resolution_strategy="Calculate equilibrium conversion; design reactor and separation to approach maximum thermodynamic yield",
        entity_scope="Chemical reactors, synthesis, combustion, biochemical processes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with accurate thermodynamic data",
        controlling_precedent="Fundamental thermodynamic principle, ASME and AIChE standards",
        issue_category=IssueCategory.REACTION_EQUILIBRIA,
        zoned_use=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Rachford-Rice Flash Calculation for Two-Phase Equilibrium",
        keywords=["flash", "rachford-rice", "vle", "bubble point", "dew point"],
        conclusion_template=[
            "Flash calculations determine vapor and liquid compositions and amounts at equilibrium.",
            "Rachford-Rice equation iteratively solved for vapor fraction beta.",
            "K-values (y_i/x_i) from thermodynamic models (EOS or gamma-phi)."
        ],
        reasoning_framework=[
            "Flash calculation: given T, P, and feed composition z_i, find vapor fraction beta and compositions.",
            "Material balance: F = V + L, component: F*z_i = V*y_i + L*x_i.",
            "Phase equilibrium: K_i = y_i/x_i from fugacity equality.",
            "Substitute to get: x_i = z_i/[1 + beta*(K_i - 1)], y_i = K_i*x_i.",
            "Rachford-Rice objective function: f(beta) = sum[z_i*(K_i - 1)/(1 + beta*(K_i - 1))] = 0.",
            "Derivative: f'(beta) = -sum[z_i*(K_i - 1)^2/(1 + beta*(K_i - 1))^2] < 0, monotonic.",
            "Newton-Raphson iteration: beta_new = beta - f(beta)/f'(beta).",
            "Bounds: 1/(1 - K_max) < beta < 1/(1 - K_min) for two-phase region.",
            "Trivial solutions: beta = 0 (all liquid) if all K_i < 1, beta = 1 (all vapor) if all K_i > 1.",
            "K-value from EOS: K_i = phi_i_liquid / phi_i_vapor * (P/P).",
            "K-value from gamma-phi: K_i = gamma_i * P_i_sat / (phi_i_vapor * P).",
            "Bubble point: given T, z_i (liquid), find P such that sum(y_i) = sum(K_i*x_i) = 1.",
            "Dew point: given T, z_i (vapor), find P such that sum(x_i) = sum(y_i/K_i) = 1.",
            "Isothermal flash: T, P given; isenthalpic flash: P, H given (requires energy balance).",
            "Stability test via Michelsen tangent plane distance prevents false single-phase solutions.",
            "Near-critical region: K-values approach 1, flash becomes ill-conditioned.",
            "Three-phase flash (two liquids, one vapor) requires additional Rachford-Rice equation.",
            "Process simulators: flash drum, partial condenser, separator modeling.",
            "Crude oil flash at topping column feed conditions determines vapor/liquid split.",
            "Natural gas processing: inlet separator flash at wellhead conditions.",
            "Convergence failures indicate phase boundary or critical point proximity."
        ],
        key_factors=[
            "Accurate K-value predictions",
            "Feed composition and conditions",
            "Pressure and temperature specification",
            "Stability analysis to confirm two-phase region",
            "Numerical robustness near critical point",
            "Phase envelope boundaries",
            "Initialization strategy for iterations",
            "Handling of trivial solutions"
        ],
        primary_authority=[
            "Rachford, H.H., Rice, J.D. (1952). Procedure for Use of Electronic Digital Computers in Calculating Flash Vaporization Hydrocarbon Equilibrium. J. Pet. Tech.",
            "Michelsen, M.L. (1982). The Isothermal Flash Problem. Fluid Phase Equilib.",
            "Whitson, C.H., Brule, M.R. Phase Behavior, SPE Monograph."
        ],
        burden_holder="Process engineer designing separators or distillation",
        adversary_position="Simple rule-of-thumb or average K-values adequate",
        counter_arguments=[
            "K-values vary strongly with composition and conditions",
            "Equipment sizing errors from inaccurate flash calculations",
            "Safety incidents from unexpected phase behavior",
            "Product quality depends on accurate composition predictions",
            "Optimization requires rigorous thermodynamic models"
        ],
        resolution_strategy="Use rigorous flash with validated thermodynamic models; cross-check with experimental data",
        entity_scope="Petroleum refining, natural gas processing, chemical separations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with good K-value models, lower near critical point",
        controlling_precedent="Standard algorithm in all process simulators, API/GPA methods",
        issue_category=IssueCategory.PHASE_EQUILIBRIA,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="UNIFAC Group Contribution Method for Predictive VLE",
        keywords=["unifac", "group contribution", "predictive", "functional group", "activity coefficient"],
        conclusion_template=[
            "UNIFAC predicts activity coefficients from functional group interactions without experimental data.",
            "Useful for preliminary design when no VLE data available.",
            "Accuracy lower than regressed NRTL/UNIQUAC but valuable for screening."
        ],
        reasoning_framework=[
            "UNIFAC: UNIQUAC Functional-group Activity Coefficients method.",
            "Developed by Fredenslund, Jones, Prausnitz (1975).",
            "Activity coefficient has combinatorial and residual parts: ln(gamma) = ln(gamma_comb) + ln(gamma_res).",
            "Combinatorial part from UNIQUAC, accounts for size/shape differences.",
            "Residual part from group interactions, sum over groups in molecule.",
            "Molecule divided into functional groups (CH3, CH2, OH, COOH, aromatic CH, etc.).",
            "Group interaction parameters a_mn determined from large VLE database.",
            "Over 50 main groups, 100+ subgroups in modern UNIFAC.",
            "No binary experimental data required for prediction.",
            "Temperature dependence: a_mn = a_mn(T) allows extrapolation.",
            "Modified UNIFAC (Dortmund, Lyngby versions) improve accuracy.",
            "Particularly useful for pharmaceutical, biochemical, polymer systems.",
            "Limitations: accuracy 10-20% typical, worse than regressed models.",
            "Fails for proximity effects (ortho/meta/para isomers).",
            "No representation of specific molecular interactions beyond groups.",
            "UNIFAC-LLE variant optimized for liquid-liquid equilibria.",
            "Databases: Dortmund Data Bank (DDB), UNIFAC consortium.",
            "Process simulators implement multiple UNIFAC variants.",
            "Solvent screening for extraction or crystallization applications.",
            "Environmental fate modeling uses UNIFAC for partition coefficients.",
            "Mixture design and formulation in specialty chemicals.",
            "Validation against experimental data essential for critical applications."
        ],
        key_factors=[
            "Availability of group parameters for molecules",
            "Temperature range of interest",
            "Required accuracy level",
            "Polarity and hydrogen bonding strength",
            "Presence of multifunctional groups",
            "Proximity effects in molecule",
            "Version of UNIFAC (original, modified, LLE)",
            "Validation data for similar systems"
        ],
        primary_authority=[
            "Fredenslund, A., Jones, R.L., Prausnitz, J.M. (1975). Group-Contribution Estimation of Activity Coefficients. AIChE J.",
            "Gmehling, J., et al. UNIFAC Parameter Table. DECHEMA Chemistry Data Series.",
            "Poling, B.E., Prausnitz, J.M., O'Connell, J.P. Properties of Gases and Liquids, 5th Ed."
        ],
        burden_holder="Engineer needing VLE predictions without experimental data",
        adversary_position="Cannot rely on predictions without experimental validation",
        counter_arguments=[
            "Experimental data often unavailable or expensive",
            "UNIFAC enables preliminary screening and feasibility",
            "Predictions guide experimental program design",
            "Better than ideal solution assumption",
            "Industry accepted for early-stage design"
        ],
        resolution_strategy="Use UNIFAC for preliminary estimates; validate predictions; conduct experiments for final design",
        entity_scope="Pharmaceutical, chemical, polymer, biotechnology industries",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence for screening, low for detailed design",
        controlling_precedent="Widely used predictive method in absence of data",
        issue_category=IssueCategory.ACTIVITY_COEFFICIENTS,
        zoned_use=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Fugacity and Fugacity Coefficient in Phase Equilibria",
        keywords=["fugacity", "fugacity coefficient", "chemical potential", "phase equilibrium", "isofugacity"],
        conclusion_template=[
            "Fugacity replaces pressure in equilibrium calculations for non-ideal systems.",
            "Phase equilibrium: fugacity of component i is equal in all phases.",
            "Fugacity coefficient phi from equation of state or activity coefficient model."
        ],
        reasoning_framework=[
            "Fugacity f_i is effective pressure accounting for non-ideality.",
            "Chemical potential: mu_i = mu_i_standard(T) + RT*ln(f_i/f_standard).",
            "For ideal gas: f_i = P_i, fugacity equals partial pressure.",
            "Fugacity coefficient: phi_i = f_i/(x_i*P) for mixture, f_i/(P) for pure.",
            "Phase equilibrium criterion: f_i_vapor = f_i_liquid for all i.",
            "Equivalently: phi_i_V * y_i * P = phi_i_L * x_i * P, or K_i = (phi_i_L/phi_i_V).",
            "Fugacity coefficient from EOS: ln(phi_i) = integral[(1/RT)*(dP_i/dn_i - RT/V)*dV] from V=infinity to V.",
            "For Peng-Robinson: analytical expression for ln(phi_i) derived from residual Helmholtz energy.",
            "Mixing rule effects appear in partial molar property derivatives.",
            "Activity coefficient approach: f_i_L = gamma_i * x_i * f_i_pure_L.",
            "Pure component fugacity: f_i_pure from vapor pressure and Poynting correction.",
            "Poynting factor: exp[V_i_L*(P - P_sat)/RT] corrects liquid fugacity for pressure.",
            "Henry's law for dilute solutes: f_i = H_i * x_i where H_i is Henry constant.",
            "Supercritical components have no vapor pressure; use EOS for fugacity.",
            "Fugacity of solids from sublimation pressure or solubility data.",
            "High-pressure phase equilibria require accurate fugacity calculations.",
            "CO2 sequestration, enhanced oil recovery use fugacity-based models.",
            "Fugacity drives component partitioning in multiphase systems.",
            "Accurate fugacity coefficients essential for cryogenic separations.",
            "Gas processing, LNG, air separation industries rely on fugacity methods.",
            "Reference state choice (pure component or infinite dilution) affects calculations."
        ],
        key_factors=[
            "Equation of state or activity model selection",
            "Pressure and temperature levels",
            "System ideality or non-ideality",
            "Phase (vapor, liquid, solid, supercritical)",
            "Mixture composition effects",
            "Accurate critical properties and parameters",
            "Reference state definition",
            "Numerical precision in integrations"
        ],
        primary_authority=[
            "Prausnitz, J.M., Lichtenthaler, R.N., Azevedo, E.G. Molecular Thermodynamics of Fluid-Phase Equilibria.",
            "Elliott, J.R., Lira, C.T. Introductory Chemical Engineering Thermodynamics, 2nd Ed.",
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics."
        ],
        burden_holder="Thermodynamics specialist calculating phase equilibria",
        adversary_position="Simpler ideal models or correlations sufficient",
        counter_arguments=[
            "Non-ideal systems deviate significantly from ideality",
            "High-pressure processes require rigorous fugacity treatment",
            "Fugacity framework is thermodynamically rigorous",
            "Modern process simulation relies on fugacity calculations",
            "Safety and economics depend on accurate predictions"
        ],
        resolution_strategy="Use fugacity-based equilibrium for non-ideal and high-pressure systems; validate against data",
        entity_scope="High-pressure processing, cryogenics, supercritical fluids, petroleum",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with rigorous EOS or activity models",
        controlling_precedent="Fundamental thermodynamic concept, universally applied",
        issue_category=IssueCategory.FUGACITY_ANALYSIS,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Hess's Law and Standard Enthalpy of Reaction",
        keywords=["hess law", "enthalpy", "formation", "reaction", "thermochemistry"],
        conclusion_template=[
            "Hess's law: enthalpy change independent of reaction path, only initial and final states.",
            "Standard enthalpy of reaction from enthalpies of formation of products minus reactants.",
            "Temperature correction via heat capacity integration."
        ],
        reasoning_framework=[
            "Hess's law: Delta_H_reaction = sum of Delta_H for any path from reactants to products.",
            "Consequence of enthalpy being a state function.",
            "Standard enthalpy of reaction: Delta_H_rxn_standard = sum(nu_i * Delta_H_f_standard(products)) - sum(nu_j * Delta_H_f_standard(reactants)).",
            "Standard enthalpy of formation Delta_H_f_standard: enthalpy change forming 1 mole from elements in standard states.",
            "Standard state: pure substance at 1 bar (or 1 atm) and specified temperature (usually 298.15 K).",
            "Elements in standard states have Delta_H_f_standard = 0 by definition.",
            "Thermochemical databases: NIST Chemistry WebBook, JANAF tables, Barin.",
            "Temperature dependence: Delta_H(T) = Delta_H(T_ref) + integral(Delta_Cp dT) from T_ref to T.",
            "Heat capacity difference: Delta_Cp = sum(nu_i*Cp_i(products)) - sum(nu_j*Cp_j(reactants)).",
            "Kirchhoff's equation relates enthalpy change at different temperatures.",
            "Combustion reactions: heats of combustion tabulated, useful for fuels.",
            "Bond enthalpy method: approximate Delta_H_rxn from bond energies.",
            "Group contribution methods (Benson, Joback) estimate Delta_H_f for compounds.",
            "Exothermic reactions: Delta_H_rxn < 0, release heat.",
            "Endothermic reactions: Delta_H_rxn > 0, absorb heat.",
            "Reactor energy balance requires Delta_H_rxn for heat duty calculation.",
            "Adiabatic temperature rise from Delta_H_rxn and heat capacities.",
            "Safety analysis: runaway reaction potential from exothermicity.",
            "Thermodynamic cycles (Born-Haber, etc.) use Hess's law.",
            "Hydrogenation, oxidation, hydrolysis reactions common in industry.",
            "Standard enthalpies of combustion for organic compounds typically -300 to -5000 kJ/mol."
        ],
        key_factors=[
            "Accuracy of formation enthalpy data",
            "Reference temperature and pressure",
            "Phase of reactants and products",
            "Heat capacity data for temperature corrections",
            "Reaction stoichiometry",
            "Presence of side reactions",
            "Standard state definitions",
            "Experimental vs. estimated values"
        ],
        primary_authority=[
            "Chase, M.W. NIST-JANAF Thermochemical Tables, 4th Ed.",
            "Linstrom, P.J., Mallard, W.G. NIST Chemistry WebBook, NIST Standard Reference Database Number 69.",
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics."
        ],
        burden_holder="Reaction engineer designing reactor thermal management",
        adversary_position="Heat of reaction negligible or can be estimated roughly",
        counter_arguments=[
            "Accurate heat duties essential for heat exchanger sizing",
            "Reactor temperature control depends on Delta_H_rxn",
            "Safety requires knowing exothermic potential",
            "Economic optimization needs precise energy balances",
            "Hess's law enables calculation from available data"
        ],
        resolution_strategy="Use tabulated Delta_H_f data; apply Hess's law; validate with calorimetry if critical",
        entity_scope="Chemical reactors, combustion, process energy integration",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with quality thermochemical data",
        controlling_precedent="Fundamental thermochemistry principle, standard engineering practice",
        issue_category=IssueCategory.THERMODYNAMIC_PROPERTIES,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Second Law Analysis and Entropy Generation",
        keywords=["second law", "entropy", "irreversibility", "exergy", "thermodynamic efficiency"],
        conclusion_template=[
            "Second law quantifies irreversibility and limits on energy conversion efficiency.",
            "Entropy generation identifies sources of inefficiency in processes.",
            "Exergy analysis optimizes process design beyond first law."
        ],
        reasoning_framework=[
            "Second law of thermodynamics: entropy of isolated system never decreases.",
            "For any process: Delta_S_universe = Delta_S_system + Delta_S_surroundings >= 0.",
            "Equality holds for reversible processes, inequality for irreversible.",
            "Entropy generation S_gen = Delta_S_universe > 0 quantifies irreversibility.",
            "Sources of irreversibility: heat transfer across finite Delta_T, friction, mixing, chemical reaction.",
            "Entropy balance: dS/dt = sum(Q_k/T_k) + sum(m_in*s_in - m_out*s_out) + S_gen_dot.",
            "Reversible process: maximum work or minimum work input.",
            "Carnot efficiency: eta_Carnot = 1 - T_cold/T_hot, maximum for heat engine.",
            "Real efficiencies always less than Carnot due to irreversibilities.",
            "Exergy (availability): maximum useful work obtainable from system relative to environment.",
            "Exergy destroyed = T_0 * S_gen, where T_0 is environment temperature.",
            "Exergy efficiency: eta_exergy = exergy_out / exergy_in, more meaningful than energy efficiency.",
            "Pinch analysis uses second law to minimize energy consumption in heat exchanger networks.",
            "Distillation column: entropy generation from mixing, heat transfer, pressure drop.",
            "Refrigeration: minimum work from reversed Carnot cycle, COP = T_cold/(T_hot - T_cold).",
            "Cryogenic processes: exergy analysis essential due to low temperatures.",
            "Chemical exergy: maximum work from reaction to environmental equilibrium.",
            "Combustion irreversibility large due to high temperature gradients.",
            "Process integration: reduce entropy generation by better heat integration.",
            "Thermodynamic optimization: minimize exergy destruction subject to constraints.",
            "Sustainability: exergy analysis assesses resource utilization efficiency."
        ],
        key_factors=[
            "Operating temperatures relative to environment",
            "Heat transfer driving forces",
            "Pressure drops and flow irreversibilities",
            "Mixing of streams at different conditions",
            "Chemical reaction driving forces",
            "Equipment efficiencies",
            "Environmental reference state selection",
            "Economic tradeoffs vs. thermodynamic ideality"
        ],
        primary_authority=[
            "Bejan, A. Advanced Engineering Thermodynamics, 4th Ed.",
            "Moran, M.J., Shapiro, H.N., Boettner, D.D., Bailey, M.B. Fundamentals of Engineering Thermodynamics, 9th Ed.",
            "Szargut, J., Morris, D.R., Steward, F.R. Exergy Analysis of Thermal, Chemical, and Metallurgical Processes."
        ],
        burden_holder="Process engineer optimizing energy efficiency",
        adversary_position="First law energy balance sufficient for design",
        counter_arguments=[
            "Second law reveals inefficiency sources invisible to first law",
            "Exergy analysis identifies optimization opportunities",
            "Energy costs justify thermodynamic optimization",
            "Sustainability requires minimizing exergy destruction",
            "Regulatory drivers (carbon emissions) favor efficient processes"
        ],
        resolution_strategy="Conduct exergy analysis to identify major irreversibilities; optimize process configuration to reduce entropy generation",
        entity_scope="Energy-intensive industries, power generation, refrigeration, chemical processing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for quantifying inefficiency, moderate for optimization impact",
        controlling_precedent="Fundamental thermodynamic principle, ISO 50001 energy management",
        issue_category=IssueCategory.THERMAL_ANALYSIS,
        zoned_use=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Azeotrope Formation and Breaking Strategies",
        keywords=["azeotrope", "minimum boiling", "maximum boiling", "extractive distillation", "pressure swing"],
        conclusion_template=[
            "Azeotropes are constant-boiling mixtures that cannot be separated by simple distillation.",
            "Non-ideal activity coefficients cause azeotrope formation.",
            "Breaking strategies: pressure swing, extractive distillation, or azeotropic distillation."
        ],
        reasoning_framework=[
            "Azeotrope: mixture with same composition in vapor and liquid phases (x = y).",
            "Equivalently: all K-values = 1 simultaneously, no separation possible.",
            "Minimum boiling azeotrope: boiling point lower than pure components (positive deviation from Raoult).",
            "Maximum boiling azeotrope: boiling point higher than pure components (negative deviation).",
            "Ethanol-water: minimum boiling azeotrope at 95.6 wt% ethanol, 78.2 deg C, 1 atm.",
            "Thermodynamic cause: Gibbs energy of mixing has extremum at azeotrope composition.",
            "Activity coefficients: gamma_1 * x_1 * P_1_sat = gamma_2 * x_2 * P_2_sat at azeotrope.",
            "Azeotrope composition changes with pressure (shift along phase envelope).",
            "Pressure swing distillation: exploit pressure sensitivity if azeotrope moves significantly.",
            "Ethanol-water azeotrope moves from 95.6% to 99.5% ethanol as pressure decreases to 70 mmHg.",
            "Extractive distillation: add high-boiling entrainer to alter relative volatility.",
            "Entrainer selectively interacts with one component, breaking azeotrope.",
            "Ethylene glycol for ethanol-water, phenol for acetone-methanol.",
            "Azeotropic distillation: add entrainer that forms new azeotrope, enabling separation.",
            "Benzene historically used for ethanol dehydration (now banned, use cyclohexane).",
            "Heterogeneous azeotropes: two liquid phases, enable decanting (ethanol-water-benzene).",
            "Ternary azeotropes more complex, may require multiple separation steps.",
            "Prediction: NRTL, UNIQUAC, UNIFAC models predict azeotrope existence and composition.",
            "Residue curve maps guide distillation column sequencing.",
            "Molecular sieves or membrane pervaporation alternative to distillation.",
            "Economic comparison: capital and energy costs of different separation strategies."
        ],
        key_factors=[
            "Azeotrope type (minimum or maximum boiling)",
            "Pressure sensitivity of azeotrope composition",
            "Availability of suitable entrainer",
            "Relative volatility with and without entrainer",
            "Energy consumption of different methods",
            "Capital cost of additional columns or equipment",
            "Product purity requirements",
            "Environmental and safety constraints on entrainers"
        ],
        primary_authority=[
            "Gmehling, J., Menke, J., Krafczyk, J., Fischer, K. Azeotropic Data, 3 volumes.",
            "Doherty, M.F., Malone, M.F. Conceptual Design of Distillation Systems.",
            "Seader, J.D., Henley, E.J., Roper, D.K. Separation Process Principles, 4th Ed."
        ],
        burden_holder="Separation engineer designing distillation system",
        adversary_position="Simple distillation can achieve required purity",
        counter_arguments=[
            "Azeotropes are thermodynamic limits on simple distillation",
            "Infinite reflux cannot overcome azeotrope barrier",
            "Product specifications may require breaking azeotrope",
            "Process economics favor optimal separation strategy",
            "Multiple separation methods available and proven"
        ],
        resolution_strategy="Identify azeotrope via VLE data or modeling; select breaking method based on economics and purity needs",
        entity_scope="Distillation in chemical, pharmaceutical, beverage alcohol industries",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in azeotrope identification and breaking methods",
        controlling_precedent="Well-established separation engineering practice",
        issue_category=IssueCategory.PHASE_EQUILIBRIA,
        zoned_use=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Soave-Redlich-Kwong (SRK) Equation of State",
        keywords=["srk", "soave", "redlich-kwong", "cubic eos", "vapor pressure"],
        conclusion_template=[
            "SRK is cubic equation of state widely used in petroleum and chemical industries.",
            "Alpha function improves vapor pressure prediction over original RK equation.",
            "Generally less accurate than Peng-Robinson for liquid densities."
        ],
        reasoning_framework=[
            "Redlich-Kwong (1949): P = RT/(V-b) - a/(T^0.5 * V*(V+b)).",
            "Soave modification (1972): replace a/T^0.5 with a*alpha(T) where alpha depends on acentric factor.",
            "Alpha function: alpha = [1 + m*(1 - sqrt(T/Tc))]^2.",
            "Parameter m = 0.480 + 1.574*omega - 0.176*omega^2 for omega <= 0.49.",
            "Parameters: a = 0.42748*R^2*Tc^2/Pc, b = 0.08664*R*Tc/Pc.",
            "Mixing rules: a_mix = sum(xi*xj*sqrt(ai*aj)*(1-kij)), b_mix = sum(xi*bi).",
            "Binary interaction parameters kij fitted to experimental data.",
            "SRK predicts vapor pressures well, critical point exactly.",
            "Liquid density typically 5-15% error, worse than PR.",
            "Widely used in oil and gas industry (Aspen HYSYS default for many applications).",
            "Fugacity coefficient formula: ln(phi_i) = (bi/b_mix)*(Z-1) - ln(Z-B) - (A/B)*[(2*sum(xj*sqrt(ai*aj)*(1-kij))/a_mix) - bi/b_mix]*ln(1+B/Z).",
            "Cubic equation solver: three roots possible, select correct root based on Gibbs energy.",
            "Volume translation can improve liquid density without affecting VLE.",
            "PSRK variant incorporates UNIFAC group contributions for kij prediction.",
            "Suitable for non-polar and slightly polar mixtures.",
            "Fails for strong polar interactions, hydrogen bonding, electrolytes.",
            "Natural gas pipelines, LNG, hydrocarbon processing applications.",
            "Gas condensate reservoirs modeled with SRK or PR.",
            "Enthalpy and entropy departure functions available analytically.",
            "Comparison with PR: SRK simpler, PR better liquid density, both widely validated."
        ],
        key_factors=[
            "System polarity and hydrogen bonding",
            "Required accuracy for liquid density",
            "Vapor pressure prediction needs",
            "Temperature and pressure range",
            "Availability of critical properties",
            "Binary interaction parameter data",
            "Computational efficiency requirements",
            "Industry standards and familiarity"
        ],
        primary_authority=[
            "Soave, G. (1972). Equilibrium Constants from a Modified Redlich-Kwong Equation of State. Chem. Eng. Sci.",
            "Reid, R.C., Prausnitz, J.M., Poling, B.E. Properties of Gases and Liquids, 4th Ed.",
            "Whitson, C.H., Brule, M.R. Phase Behavior, SPE Monograph."
        ],
        burden_holder="Process engineer selecting thermodynamic model",
        adversary_position="Any cubic EOS gives similar results",
        counter_arguments=[
            "SRK and PR have different accuracy profiles",
            "Liquid density differences affect equipment sizing",
            "Model selection affects simulation convergence",
            "Industry standards often specify particular EOS",
            "Validation against data guides choice"
        ],
        resolution_strategy="Use SRK for vapor-dominated systems or when industry standard; use PR when liquid density accuracy critical",
        entity_scope="Oil and gas, refining, natural gas processing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for VLE, moderate for liquid properties",
        controlling_precedent="Widely used industry standard, API and ISO methods",
        issue_category=IssueCategory.EQUATION_OF_STATE,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="UNIQUAC Activity Coefficient Model",
        keywords=["uniquac", "activity coefficient", "universal quasi-chemical", "polymers", "size asymmetry"],
        conclusion_template=[
            "UNIQUAC extends local composition theory to molecules with large size differences.",
            "Particularly effective for polymer solutions and systems with size asymmetry.",
            "Combinatorial term accounts for entropy of mixing based on size and shape."
        ],
        reasoning_framework=[
            "UNIQUAC: Universal Quasi-Chemical theory by Abrams and Prausnitz (1975).",
            "Activity coefficient: ln(gamma_i) = ln(gamma_i_combinatorial) + ln(gamma_i_residual).",
            "Combinatorial part: ln(gamma_i_comb) = ln(phi_i/x_i) + (z/2)*q_i*ln(theta_i/phi_i) + l_i - (phi_i/x_i)*sum(x_j*l_j).",
            "Residual part: ln(gamma_i_res) = q_i*[1 - ln(sum_j(theta_j*tau_ji)) - sum_j(theta_j*tau_ij/sum_k(theta_k*tau_kj))].",
            "Volume fraction: phi_i = x_i*r_i / sum(x_j*r_j).",
            "Surface area fraction: theta_i = x_i*q_i / sum(x_j*q_j).",
            "Molecular parameters r_i (volume) and q_i (surface area) from van der Waals volumes.",
            "Parameter l_i = (z/2)*(r_i - q_i) - (r_i - 1), coordination number z = 10.",
            "Binary interaction parameters tau_ij = exp(-u_ij/RT) where u_ij is energy parameter.",
            "Temperature dependence: u_ij = a_ij + b_ij*T enables extrapolation.",
            "UNIQUAC reduces to Flory-Huggins for athermal polymer solutions.",
            "Particularly accurate for polymer-solvent systems.",
            "Size asymmetry (large r_i ratio) handled better than NRTL or Wilson.",
            "Thermodynamic consistency ensured by Gibbs-Duhem relation.",
            "Group contribution version: UNIFAC uses UNIQUAC residual term.",
            "Databases: DECHEMA, DDB provide r, q, and tau parameters.",
            "Predicts liquid-liquid equilibria, vapor-liquid equilibria.",
            "Pharmaceutical crystallization, polymer processing applications.",
            "Electrolyte UNIQUAC (eUNIQUAC) extends to ionic systems.",
            "Limitations: requires binary data for parameter fitting, extrapolation uncertain.",
            "Comparison with NRTL: UNIQUAC better for polymers, NRTL simpler for small molecules."
        ],
        key_factors=[
            "Molecular size asymmetry",
            "Availability of r and q parameters",
            "Binary interaction parameter data",
            "Temperature range of operation",
            "Polymer vs. small molecule systems",
            "Liquid-liquid or vapor-liquid equilibria",
            "Computational complexity acceptable",
            "Accuracy requirements for design"
        ],
        primary_authority=[
            "Abrams, D.S., Prausnitz, J.M. (1975). Statistical Thermodynamics of Liquid Mixtures. AIChE J.",
            "Prausnitz, J.M., Lichtenthaler, R.N., Azevedo, E.G. Molecular Thermodynamics of Fluid-Phase Equilibria.",
            "Fredenslund, A., Gmehling, J., Rasmussen, P. Vapor-Liquid Equilibria Using UNIFAC."
        ],
        burden_holder="Process engineer modeling polymer or highly non-ideal systems",
        adversary_position="Simpler models like NRTL adequate",
        counter_arguments=[
            "UNIQUAC specifically designed for size asymmetry",
            "Polymer systems poorly represented by simpler models",
            "Predictive capability via UNIFAC for preliminary design",
            "Widely validated in polymer processing",
            "Industry standard for pharmaceutical applications"
        ],
        resolution_strategy="Use UNIQUAC for polymer solutions or large size ratios; use NRTL for small molecules unless UNIQUAC gives better fit",
        entity_scope="Polymer processing, pharmaceuticals, biotechnology",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for polymer systems with data, moderate for extrapolation",
        controlling_precedent="Standard model for polymer-solvent equilibria",
        issue_category=IssueCategory.ACTIVITY_COEFFICIENTS,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Wilson Activity Coefficient Model",
        keywords=["wilson", "activity coefficient", "local composition", "excess gibbs energy"],
        conclusion_template=[
            "Wilson equation uses local composition theory for activity coefficients.",
            "Cannot predict liquid-liquid phase splits unlike NRTL or UNIQUAC.",
            "Accurate for miscible systems, simple two-parameter model."
        ],
        reasoning_framework=[
            "Wilson equation developed by Grant Wilson (1964).",
            "Based on local composition concept: molecules near species i differ from bulk.",
            "Activity coefficient: ln(gamma_i) = -ln(sum_j(x_j*Lambda_ij)) + 1 - sum_k[x_k*Lambda_ki / sum_j(x_j*Lambda_kj)].",
            "Wilson parameters: Lambda_ij = (V_j/V_i) * exp(-lambda_ij/RT).",
            "Energy parameters lambda_ij = u_ij - u_ii characterize interactions.",
            "Molar volumes V_i typically at normal boiling point or other reference.",
            "Two binary parameters: lambda_12 and lambda_21 for each pair.",
            "Temperature dependence through exp(-lambda/RT) allows extrapolation.",
            "Limitation: Wilson equation CANNOT predict liquid-liquid immiscibility.",
            "Mathematical constraint: always yields single liquid phase.",
            "Use NRTL or UNIQUAC if LLE possible or unknown.",
            "Excellent for highly non-ideal but miscible systems (alcohol-hydrocarbon).",
            "Thermodynamically consistent via Gibbs-Duhem.",
            "Simpler than NRTL (two parameters vs. three).",
            "Widely used in distillation design for miscible systems.",
            "Parameter regression from isothermal or isobaric VLE data.",
            "Multicomponent prediction from binary parameters only.",
            "Databases: DECHEMA, NIST have Wilson parameters for many systems.",
            "Process simulators implement Wilson as option.",
            "Fewer parameters reduce overfitting risk vs. NRTL.",
            "Cannot represent strong associating systems as well as NRTL.",
            "Comparison: Wilson for miscible, NRTL for general use, UNIQUAC for polymers."
        ],
        key_factors=[
            "System miscibility (single or two liquid phases)",
            "Availability of binary VLE data",
            "Temperature range of interest",
            "Degree of non-ideality",
            "Simplicity vs. generality tradeoff",
            "Computational efficiency",
            "Validation data quality",
            "Extrapolation requirements"
        ],
        primary_authority=[
            "Wilson, G.M. (1964). Vapor-Liquid Equilibrium. XI. A New Expression for Excess Free Energy. J. Am. Chem. Soc.",
            "Prausnitz, J.M., Lichtenthaler, R.N., Azevedo, E.G. Molecular Thermodynamics of Fluid-Phase Equilibria.",
            "Gmehling, J., Onken, U. Vapor-Liquid Equilibrium Data Collection, DECHEMA."
        ],
        burden_holder="Process engineer selecting activity coefficient model",
        adversary_position="Raoult's law or simple correlations sufficient",
        counter_arguments=[
            "Non-ideal systems show large deviations from ideality",
            "Wilson equation proven accurate for many systems",
            "Equipment design requires validated thermodynamics",
            "Azeotrope prediction needs non-ideal models",
            "Wilson simpler than NRTL with fewer parameters"
        ],
        resolution_strategy="Use Wilson for known miscible systems; switch to NRTL if LLE risk exists or better fit needed",
        entity_scope="Distillation, chemical separations, miscible liquid processing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for miscible VLE, inapplicable for LLE",
        controlling_precedent="Classic activity coefficient model, widely validated",
        issue_category=IssueCategory.ACTIVITY_COEFFICIENTS,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Virial Equation of State for Moderate Pressures",
        keywords=["virial", "equation of state", "second virial coefficient", "third virial", "moderate pressure"],
        conclusion_template=[
            "Virial equation expresses compressibility as power series in density or pressure.",
            "Second virial coefficient B(T) dominates at moderate pressures.",
            "Theoretical basis in statistical mechanics, more rigorous than cubic EOS."
        ],
        reasoning_framework=[
            "Virial equation: Z = PV/RT = 1 + B/V + C/V^2 + ... (density series).",
            "Pressure series: Z = 1 + B'*P + C'*P^2 + ... where B' = B/RT.",
            "Second virial coefficient B(T) accounts for two-body interactions.",
            "Third virial coefficient C(T) for three-body interactions.",
            "Truncated virial (B only) accurate to moderate pressures (~10 bar for gases).",
            "Statistical mechanics: B related to pair potential integral.",
            "Corresponding states: generalized charts for B as f(Tr, omega).",
            "Tsonopoulos correlation: B*Pc/(R*Tc) = f0(Tr) + omega*f1(Tr).",
            "Pitzer-Curl correlation: similar form, different functions.",
            "Temperature dependence: B typically negative at low T, becomes less negative or positive at high T.",
            "Boyle temperature: B = 0, ideal gas behavior even at moderate pressure.",
            "Mixture virial: B_mix = sum(yi*yj*Bij), cross-coefficient Bij for unlike pairs.",
            "Combining rules for Bij: (Bij = (Bii + Bjj)/2 or more complex).",
            "Virial cutoff: higher terms needed above moderate pressure (~50 bar).",
            "More accurate than ideal gas, simpler than full EOS for moderate conditions.",
            "Gas metering, compressor design use virial corrections.",
            "Natural gas properties: AGA-8 model is extended virial equation.",
            "Quantum gases (He, H2): virial coefficients from quantum statistical mechanics.",
            "Experimental determination: PVT data regression.",
            "Theoretical calculation: from intermolecular potential (Lennard-Jones, etc.).",
            "Advantage: theoretical foundation, systematic improvement.",
            "Disadvantage: limited pressure range, not applicable to liquids."
        ],
        key_factors=[
            "Pressure and temperature range",
            "Gas ideality or non-ideality",
            "Availability of virial coefficient data",
            "Required accuracy level",
            "Computational simplicity needs",
            "Mixture composition effects",
            "Quantum effects for light gases",
            "Truncation error assessment"
        ],
        primary_authority=[
            "Tsonopoulos, C. (1974). An Empirical Correlation of Second Virial Coefficients. AIChE J.",
            "Dymond, J.H., Smith, E.B. The Virial Coefficients of Pure Gases and Mixtures.",
            "Poling, B.E., Prausnitz, J.M., O'Connell, J.P. Properties of Gases and Liquids, 5th Ed."
        ],
        burden_holder="Engineer calculating gas properties at moderate pressures",
        adversary_position="Ideal gas law adequate or full EOS necessary",
        counter_arguments=[
            "Ideal gas errors significant at moderate pressure",
            "Virial more accurate than ideal with minimal complexity",
            "Truncated virial fills gap between ideal and complex EOS",
            "Theoretical basis superior to empirical correlations",
            "Industry standards (ISO, AGA) use virial corrections"
        ],
        resolution_strategy="Use virial equation for gases at moderate pressures; use ideal gas law only at low P; use cubic EOS for high P or liquids",
        entity_scope="Gas processing, compressor design, flow measurement",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence at moderate P, low at high P or near saturation",
        controlling_precedent="Standard approach for gas property corrections",
        issue_category=IssueCategory.EQUATION_OF_STATE,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Bubble Point and Dew Point Calculations",
        keywords=["bubble point", "dew point", "vle", "saturation", "k-value"],
        conclusion_template=[
            "Bubble point: temperature or pressure where first bubble of vapor forms from liquid.",
            "Dew point: conditions where first drop of liquid condenses from vapor.",
            "Iterative calculations using K-values and summation equations."
        ],
        reasoning_framework=[
            "Bubble point (T given, find P): liquid at temperature T starts to boil at pressure P.",
            "Condition: sum(yi) = sum(Ki*xi) = 1 where xi given (liquid composition).",
            "Algorithm: guess P, calculate Ki(T,P), compute sum(Ki*xi), adjust P until sum = 1.",
            "Bubble point (P given, find T): similar, iterate on T.",
            "Dew point (T given, find P): vapor at temperature T starts to condense at pressure P.",
            "Condition: sum(xi) = sum(yi/Ki) = 1 where yi given (vapor composition).",
            "Algorithm: guess P, calculate Ki(T,P), compute sum(yi/Ki), adjust P until sum = 1.",
            "Dew point (P given, find T): iterate on T.",
            "K-values from EOS or activity coefficient models.",
            "Initial guess: Raoult's law P_bubble = sum(xi*Pi_sat), T from Antoine.",
            "Newton-Raphson or successive substitution for convergence.",
            "Phase envelope: locus of bubble and dew points over composition range.",
            "Cricondenbar: maximum pressure on phase envelope.",
            "Cricondentherm: maximum temperature on phase envelope.",
            "Retrograde condensation: vapor condenses upon isothermal pressure decrease.",
            "Natural gas dew point critical for pipeline hydrate prevention.",
            "Hydrocarbon dew point (HDP) spec in gas sales contracts.",
            "Water dew point for corrosion prevention.",
            "Distillation column: bubble point of bottoms, dew point of distillate.",
            "Safety: flash point related to bubble point of liquid mixture.",
            "Convergence issues near critical point or azeotrope."
        ],
        key_factors=[
            "Feed composition accuracy",
            "Thermodynamic model selection",
            "Temperature or pressure specification",
            "K-value accuracy and convergence",
            "Numerical method robustness",
            "Proximity to critical point or azeotrope",
            "Initialization strategy",
            "Tolerance and convergence criteria"
        ],
        primary_authority=[
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics.",
            "Whitson, C.H., Brule, M.R. Phase Behavior, SPE Monograph.",
            "Seader, J.D., Henley, E.J., Roper, D.K. Separation Process Principles."
        ],
        burden_holder="Process engineer designing separators or phase behavior analysis",
        adversary_position="Simple vapor pressure correlation adequate",
        counter_arguments=[
            "Mixture behavior differs from pure components",
            "Non-ideal effects significant in many systems",
            "Accurate phase behavior essential for equipment design",
            "Safety margins cannot compensate for incorrect phase predictions",
            "Process optimization requires accurate bubble/dew point"
        ],
        resolution_strategy="Use rigorous K-value models; validate against experimental phase envelopes; check convergence carefully",
        entity_scope="Phase behavior analysis, distillation, gas processing, petroleum",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with good models and data, lower near critical point",
        controlling_precedent="Standard phase equilibrium calculation, universally applied",
        issue_category=IssueCategory.PHASE_EQUILIBRIA,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Excess Gibbs Energy and Excess Properties",
        keywords=["excess property", "gibbs energy", "enthalpy", "entropy", "non-ideal mixing"],
        conclusion_template=[
            "Excess properties quantify deviation from ideal solution behavior.",
            "Excess Gibbs energy G^E relates directly to activity coefficients.",
            "Excess enthalpy H^E affects heat of mixing and energy balances."
        ],
        reasoning_framework=[
            "Excess property: M^E = M_real - M_ideal, difference from ideal solution.",
            "Ideal solution: enthalpy and volume of mixing zero, only entropy of mixing.",
            "Excess Gibbs energy: G^E = RT*sum(xi*ln(gamma_i)).",
            "Activity coefficient: ln(gamma_i) = (1/RT)*(partial G^E/partial ni)_T,P,nj.",
            "Gibbs-Duhem equation ensures consistency: sum(xi*d(ln(gamma_i))) = 0 at constant T,P.",
            "Excess enthalpy H^E: heat of mixing, measured calorimetrically.",
            "H^E positive: endothermic mixing (breaking interactions), common for non-polar mixtures.",
            "H^E negative: exothermic mixing (forming new interactions), hydrogen bonding systems.",
            "Excess entropy S^E: G^E = H^E - T*S^E.",
            "Excess volume V^E: volume change upon mixing, usually small.",
            "Temperature dependence of G^E via H^E: (partial(G^E/T)/partial T)_P = -H^E/T^2.",
            "Activity coefficient models (NRTL, Wilson, UNIQUAC) are G^E models.",
            "Redlich-Kister expansion: G^E/(x1*x2*RT) = A + B*(x1-x2) + C*(x1-x2)^2 + ...",
            "Margules equations: one-constant, two-constant, three-constant forms.",
            "Van Laar equation: historic, assumes regular solution theory.",
            "UNIFAC predicts G^E from group contributions.",
            "Excess property databases: DECHEMA, NIST ThermoData Engine.",
            "Heat of mixing affects reactor design, thermal safety.",
            "Exothermic mixing can cause temperature rise, vaporization, runaway.",
            "Distillation: excess enthalpy affects tray or packing heat balances.",
            "Mixing rules for EOS relate to excess Gibbs energy at infinite pressure."
        ],
        key_factors=[
            "Magnitude and sign of G^E or H^E",
            "Temperature dependence",
            "Concentration dependence (symmetric or asymmetric)",
            "Experimental data availability",
            "Model selection for G^E",
            "Thermodynamic consistency validation",
            "Impact on process design (energy, separations)",
            "Safety implications of exothermic mixing"
        ],
        primary_authority=[
            "Prausnitz, J.M., Lichtenthaler, R.N., Azevedo, E.G. Molecular Thermodynamics of Fluid-Phase Equilibria.",
            "Gmehling, J., Kolbe, B., Kleiber, M., Rarey, J. Chemical Thermodynamics for Process Simulation.",
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics."
        ],
        burden_holder="Thermodynamics engineer modeling non-ideal solutions",
        adversary_position="Ideal solution assumption simplifies calculations",
        counter_arguments=[
            "Non-ideal behavior is the norm, not exception",
            "Excess properties essential for accurate predictions",
            "Heat of mixing affects energy balances and safety",
            "Activity coefficients derived from G^E data",
            "Process design errors from ignoring non-ideality"
        ],
        resolution_strategy="Measure or estimate excess properties; use validated G^E models; check thermodynamic consistency",
        entity_scope="Chemical processing, separations, reactor design, solution thermodynamics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with experimental data, moderate with predictions",
        controlling_precedent="Fundamental solution thermodynamics, widely applied",
        issue_category=IssueCategory.EXCESS_PROPERTIES,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Supercritical Fluid Thermodynamics and CO2 Applications",
        keywords=["supercritical", "critical point", "co2", "extraction", "density"],
        conclusion_template=[
            "Supercritical fluids have liquid-like density and gas-like transport properties.",
            "CO2 above 31.1 deg C and 73.8 bar is widely used for extraction and processing.",
            "Density tunable with pressure, enabling selective solubility."
        ],
        reasoning_framework=[
            "Critical point: temperature Tc and pressure Pc where liquid-vapor distinction vanishes.",
            "Supercritical region: T > Tc and P > Pc, single dense phase.",
            "No phase transition, continuous property changes.",
            "Density intermediate between liquid and gas, adjustable by P and T.",
            "Transport properties: diffusivity higher than liquid, viscosity lower.",
            "CO2 critical point: Tc = 31.1 deg C (304.25 K), Pc = 73.8 bar (7.38 MPa).",
            "Supercritical CO2 (scCO2): non-toxic, non-flammable, inexpensive, environmentally benign.",
            "Solvent power tunable by varying pressure near critical point.",
            "Compressibility large near critical point, density highly pressure-sensitive.",
            "Extraction applications: caffeine from coffee, hops from beer, essential oils, pharmaceuticals.",
            "Enhanced oil recovery: scCO2 injection reduces oil viscosity, miscible displacement.",
            "Carbon capture and sequestration: CO2 stored underground as supercritical fluid.",
            "Thermodynamic modeling: Peng-Robinson or specialized EOS (CPA, SAFT).",
            "Phase behavior complex near critical point, requires accurate EOS.",
            "Retrograde phenomena in supercritical region.",
            "scCO2 as reaction medium: green chemistry, polymer synthesis.",
            "Critical opalescence: light scattering near critical point due to density fluctuations.",
            "Widom line: locus of maxima in response functions in supercritical region.",
            "Safety: rapid pressure changes can cause large density swings.",
            "Equipment design: high-pressure vessels, specialized materials.",
            "Other supercritical fluids: water (Tc 374 deg C), ethane, propane."
        ],
        key_factors=[
            "Critical temperature and pressure of fluid",
            "Operating conditions relative to critical point",
            "Density and solubility requirements",
            "Equipment pressure rating",
            "Safety and environmental considerations",
            "Thermodynamic model accuracy near critical point",
            "Transport property predictions",
            "Economic comparison with conventional solvents"
        ],
        primary_authority=[
            "McHugh, M.A., Krukonis, V.J. Supercritical Fluid Extraction: Principles and Practice, 2nd Ed.",
            "Span, R., Wagner, W. (1996). A New Equation of State for Carbon Dioxide. J. Phys. Chem. Ref. Data.",
            "Prausnitz, J.M., Lichtenthaler, R.N., Azevedo, E.G. Molecular Thermodynamics of Fluid-Phase Equilibria."
        ],
        burden_holder="Process engineer designing supercritical extraction or processing",
        adversary_position="Conventional solvents or processes adequate",
        counter_arguments=[
            "Supercritical processes offer environmental benefits",
            "Solvent elimination or reduction via scCO2",
            "Enhanced selectivity and product quality",
            "scCO2 properties uniquely advantageous",
            "Industry adoption in pharmaceuticals, food processing"
        ],
        resolution_strategy="Evaluate scCO2 feasibility; model phase behavior rigorously; pilot test to validate predictions",
        entity_scope="Extraction, pharmaceuticals, polymers, carbon capture, enhanced oil recovery",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Moderate confidence near critical point, high confidence with validated models",
        controlling_precedent="Established technology with growing applications, environmental drivers",
        issue_category=IssueCategory.CRITICAL_PHENOMENA,
        zoned_use=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Thermodynamic Package Selection in Process Simulation",
        keywords=["property package", "aspen plus", "hysys", "model selection", "thermodynamic method"],
        conclusion_template=[
            "Thermodynamic package selection critical for simulation accuracy and convergence.",
            "Peng-Robinson for hydrocarbons, NRTL for highly non-ideal liquids, electrolyte models for aqueous ionic.",
            "Validate predictions against experimental data before design decisions."
        ],
        reasoning_framework=[
            "Process simulators (Aspen Plus, HYSYS, ProMax, etc.) offer multiple property packages.",
            "Property package specifies: EOS or activity model, mixing rules, parameters, secondary models.",
            "Incorrect package choice leads to wrong results, poor convergence, design errors.",
            "Hydrocarbon systems (oil, gas, refining): Peng-Robinson or Soave-Redlich-Kwong.",
            "Polar non-electrolyte (chemicals): NRTL, UNIQUAC, Wilson for liquid activity.",
            "Electrolyte systems (aqueous salts, acids): Electrolyte-NRTL, Pitzer models.",
            "Polymers: UNIFAC, UNIQUAC with polymer-specific parameters.",
            "Cryogenics (LNG, air separation): GERG-2008, Lee-Kesler-Plocker, BWR.",
            "Steam systems: ASME steam tables (IAPWS-IF97).",
            "Sour water (H2S, NH3, CO2 in water): Amine package, OLI Electrolyte.",
            "Secondary models: Henry's law for dissolved gases, solids solubility, salt precipitation.",
            "Binary interaction parameters essential for mixtures, regressed from data.",
            "Default parameters often inadequate, require validation or regression.",
            "Thermodynamic consistency checks built into simulators (area test, etc.).",
            "Sensitivity analysis: vary thermodynamic method to assess uncertainty.",
            "Phase stability: some packages better at detecting multiple phases.",
            "Convergence issues often traceable to thermodynamic model mismatch.",
            "Industry guidelines: API, GPSA, AIChE Design Institute for Physical Properties (DIPPR).",
            "Custom packages: user-defined models, parameters, or correlations.",
            "Cloud point, pour point, flash point: empirical correlations often added.",
            "Aspen Plus packages: ELECNRTL, PC-SAFT, PR-BM, SRK, Wilson, NRTL, UNIQUAC, UNIFAC, etc.",
            "HYSYS packages: PR, SRK, NRTL, UNIQUAC, AMINE, Glycol, Sour PR, etc."
        ],
        key_factors=[
            "Chemical system type (hydrocarbons, polar, electrolyte, polymer)",
            "Phase behavior (VLE, LLE, VLLE, solids)",
            "Temperature and pressure range",
            "Required accuracy for design",
            "Availability of experimental validation data",
            "Convergence and computational efficiency",
            "Industry standards and precedents",
            "Simulator defaults vs. recommended packages"
        ],
        primary_authority=[
            "Carlson, E.C. (1996). Don't Gamble with Physical Properties for Simulations. Chem. Eng. Prog.",
            "Aspen Technology. Aspen Physical Property System: Physical Property Methods.",
            "GPSA Engineering Data Book, 14th Ed., Section 23: Thermodynamic Properties."
        ],
        burden_holder="Process engineer setting up simulation",
        adversary_position="Simulator defaults are adequate",
        counter_arguments=[
            "Defaults often chosen for broad applicability, not accuracy",
            "Many documented cases of wrong package causing errors",
            "Validation against data is engineering responsibility",
            "Equipment sizing, safety analysis depend on accurate properties",
            "Thermodynamic package selection first step in rigorous simulation"
        ],
        resolution_strategy="Select package based on chemistry and conditions; validate key properties; consult guidelines and literature",
        entity_scope="All process simulation applications across industries",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with proper selection and validation",
        controlling_precedent="Best practice in process engineering, taught in all curricula",
        issue_category=IssueCategory.PROCESS_SIMULATION,
        zoned_use=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="GERG-2008 Equation of State for Natural Gas",
        keywords=["gerg-2008", "natural gas", "aga-8", "reference equation", "custody transfer"],
        conclusion_template=[
            "GERG-2008 is wide-range reference equation of state for natural gas mixtures.",
            "Highly accurate for custody transfer, pipeline, and LNG applications.",
            "Covers 21 components including hydrocarbons, nitrogen, CO2, hydrogen."
        ],
        reasoning_framework=[
            "GERG-2008: Groupe Europeen de Recherches Gazieres reference EOS.",
            "Developed by Kunz and Wagner (2012), international collaboration.",
            "Multi-fluid approximation using high-accuracy pure component Helmholtz equations.",
            "Mixture Helmholtz energy: a = sum(xi*ai_pure) + a_residual_mix.",
            "Covers 21 components: C1-C10, N2, CO2, H2, CO, H2S, He, Ar, H2O, O2.",
            "Temperature range: 90-450 K, pressure up to 35 MPa for most compositions.",
            "Uncertainty: 0.1% in density for typical natural gas, better than cubic EOS.",
            "Used for custody transfer metering per ISO 20765 and AGA Report No. 8.",
            "Replaces older AGA-8 detail and gross methods in many applications.",
            "Speed of sound, heat capacity, Joule-Thomson coefficient accurately predicted.",
            "LNG applications: density critical for inventory, safety, energy content.",
            "Pipeline simulation: compressibility factor affects flow and pressure drop.",
            "Binary and higher-order interaction parameters fitted to experimental data.",
            "Computationally intensive: iterative solution of implicit equation.",
            "Simplified versions (GERG-2004) for faster calculation with slight accuracy loss.",
            "Comparison with PR: GERG-2008 far superior accuracy, but more complex.",
            "Industry adoption: European and international standards, replacing older methods.",
            "Natural gas quality: heating value, Wobbe index calculated from GERG.",
            "Validation: extensive comparisons against experimental PVT and phase equilibrium data.",
            "Software implementation: NIST REFPROP, process simulators, specialized tools.",
            "Future: extensions to bio-methane, hydrogen blending in pipelines."
        ],
        key_factors=[
            "Natural gas composition range",
            "Accuracy requirements (custody transfer vs. process)",
            "Temperature and pressure operating conditions",
            "Computational resources available",
            "Regulatory and contractual standards",
            "Presence of non-hydrocarbon components",
            "Speed of calculation vs. accuracy tradeoff",
            "Software and implementation availability"
        ],
        primary_authority=[
            "Kunz, O., Wagner, W. (2012). The GERG-2008 Wide-Range Equation of State for Natural Gases and Other Mixtures. J. Chem. Eng. Data.",
            "ISO 20765-2:2015 Natural Gas - Calculation of Thermodynamic Properties - Part 2: GERG-2008.",
            "AGA Report No. 8, Compressibility Factors of Natural Gas and Other Related Hydrocarbon Gases, 3rd Ed."
        ],
        burden_holder="Gas measurement engineer or pipeline operator",
        adversary_position="Simpler equations like Peng-Robinson adequate",
        counter_arguments=[
            "Custody transfer accuracy requirements mandate GERG-2008",
            "Financial stakes in gas measurement justify precise EOS",
            "Regulatory standards specify GERG or equivalent",
            "Accuracy differences translate to significant monetary value",
            "Modern software handles computational complexity"
        ],
        resolution_strategy="Use GERG-2008 for high-accuracy gas properties, custody transfer, and LNG; use simpler EOS for preliminary design only",
        entity_scope="Natural gas pipelines, LNG facilities, gas processing, custody transfer",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Highest confidence for natural gas within stated range",
        controlling_precedent="International standard (ISO) and industry standard (AGA) for natural gas",
        issue_category=IssueCategory.EQUATION_OF_STATE,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Le Chatelier's Principle and Reaction Equilibrium Shifts",
        keywords=["le chatelier", "equilibrium shift", "stress", "reaction", "counteract"],
        conclusion_template=[
            "Le Chatelier's principle: system at equilibrium shifts to counteract imposed change.",
            "Concentration, pressure, temperature changes shift equilibrium position.",
            "Catalyst affects rate but not equilibrium position."
        ],
        reasoning_framework=[
            "Le Chatelier's principle: if stress applied to system at equilibrium, system shifts to relieve stress.",
            "Stress types: concentration change, pressure change, temperature change.",
            "Concentration increase of reactant: equilibrium shifts toward products.",
            "Concentration decrease of product (removal): equilibrium shifts toward products.",
            "Pressure increase (volume decrease): shifts toward side with fewer moles of gas.",
            "Example: N2 + 3H2 <-> 2NH3, increase P shifts right (4 moles -> 2 moles).",
            "Temperature increase: shifts in endothermic direction (absorbs heat).",
            "Temperature decrease: shifts in exothermic direction (releases heat).",
            "Exothermic reaction (Delta_H < 0): raising T decreases K, shifts left.",
            "Endothermic reaction (Delta_H > 0): raising T increases K, shifts right.",
            "Inert gas addition at constant volume: no shift (partial pressures unchanged).",
            "Inert gas addition at constant pressure: volume increases, shifts toward more moles.",
            "Catalyst addition: increases rate of forward and reverse equally, no equilibrium shift.",
            "Catalyst lowers activation energy, speeds approach to equilibrium.",
            "Quantitative analysis: calculate new equilibrium via K and mass balances.",
            "Industrial applications: Haber ammonia synthesis uses high P, moderate T.",
            "Sulfuric acid Contact process: SO2 + 1/2 O2 <-> SO3, exothermic, high P, moderate T.",
            "Methanol synthesis: CO + 2H2 <-> CH3OH, exothermic, high P favors product.",
            "Weak acid ionization: addition of common ion shifts equilibrium (suppresses ionization).",
            "Buffering in biochemical systems relies on Le Chatelier shifts.",
            "Qualitative understanding guides process design before detailed calculations."
        ],
        key_factors=[
            "Type of stress imposed (concentration, pressure, temperature)",
            "Stoichiometry of balanced reaction",
            "Sign of enthalpy change (exothermic or endothermic)",
            "Number of moles of gas on each side",
            "Magnitude of equilibrium constant",
            "Kinetic considerations (catalyst, rate)",
            "Practical constraints (equipment, economics)",
            "Multiple equilibria interactions"
        ],
        primary_authority=[
            "Atkins, P., de Paula, J. Physical Chemistry, 10th Ed.",
            "Smith, J.M., Van Ness, H.C., Abbott, M.M. Introduction to Chemical Engineering Thermodynamics.",
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics."
        ],
        burden_holder="Process engineer optimizing reaction conditions",
        adversary_position="Empirical trial-and-error sufficient for process development",
        counter_arguments=[
            "Le Chatelier provides qualitative guidance quickly",
            "Systematic approach reduces trial-and-error",
            "Understanding equilibrium shifts essential for optimization",
            "Process economics depend on conversion and selectivity",
            "Fundamental principle taught universally"
        ],
        resolution_strategy="Apply Le Chatelier qualitatively first; then calculate equilibrium quantitatively; design process to favor desired products",
        entity_scope="Chemical reactors, industrial synthesis, biochemical processes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for qualitative predictions, quantitative requires equilibrium constant",
        controlling_precedent="Fundamental chemical principle, universally applicable",
        issue_category=IssueCategory.REACTION_EQUILIBRIA,
        zoned_use=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Activity and Activity Coefficient in Non-Ideal Solutions",
        keywords=["activity", "activity coefficient", "non-ideal", "fugacity", "chemical potential"],
        conclusion_template=[
            "Activity a_i generalizes concentration to account for non-ideal interactions.",
            "Activity coefficient gamma_i = a_i/x_i quantifies deviation from ideality.",
            "Activity appears in equilibrium expressions, kinetics, and electrochemistry."
        ],
        reasoning_framework=[
            "Chemical potential: mu_i = mu_i_standard + RT*ln(a_i).",
            "Activity a_i: effective concentration accounting for interactions.",
            "Ideal solution: a_i = x_i (mole fraction), activity coefficient gamma_i = 1.",
            "Non-ideal solution: a_i = gamma_i * x_i.",
            "Fugacity relationship: a_i = f_i / f_i_standard for gases/liquids.",
            "Standard state: pure component at system T and P (symmetric convention).",
            "Unsymmetric convention: standard state is infinite dilution (Henry's law).",
            "Activity coefficient models: NRTL, UNIQUAC, Wilson, UNIFAC.",
            "gamma_i > 1: positive deviation, molecules prefer dissimilar neighbors (less stable).",
            "gamma_i < 1: negative deviation, molecules prefer similar neighbors (more stable).",
            "Infinite dilution activity coefficient: gamma_i_infinity, important for trace components.",
            "Equilibrium constant in terms of activity: K_a = product(a_i^nu_i).",
            "Reaction quotient Q vs K determines reaction direction.",
            "Electrochemistry: Nernst equation uses activities, not concentrations.",
            "Solubility: solid-liquid equilibrium S = K_sp / (gamma_+ * gamma_-).",
            "pH calculation: activity of H+ differs from concentration in non-ideal solutions.",
            "Debye-Huckel theory for dilute electrolytes: ln(gamma_i) proportional to sqrt(ionic strength).",
            "Activity measurements: vapor pressure, freezing point depression, osmotic pressure.",
            "Biological systems: enzyme kinetics use activities in concentrated protein solutions.",
            "Geochemistry: mineral solubility depends on activity in natural waters.",
            "Process design: activity-based models essential for accurate separations."
        ],
        key_factors=[
            "Solution ideality or non-ideality",
            "Concentration range (dilute or concentrated)",
            "Temperature and pressure",
            "Solvent and solute interactions",
            "Electrolyte vs. non-electrolyte",
            "Standard state choice",
            "Measurement or estimation method",
            "Application (phase equilibrium, reaction, electrochemistry)"
        ],
        primary_authority=[
            "Prausnitz, J.M., Lichtenthaler, R.N., Azevedo, E.G. Molecular Thermodynamics of Fluid-Phase Equilibria.",
            "Sandler, S.I. Chemical, Biochemical, and Engineering Thermodynamics.",
            "Atkins, P., de Paula, J. Physical Chemistry."
        ],
        burden_holder="Chemist or engineer analyzing non-ideal systems",
        adversary_position="Concentrations adequate, activity corrections unnecessary",
        counter_arguments=[
            "Non-ideal behavior common in real systems",
            "Activity framework rigorously correct thermodynamically",
            "Equilibrium and kinetics require activities for accuracy",
            "Industrial separations depend on activity coefficient models",
            "Electrochemical processes fail without activity corrections"
        ],
        resolution_strategy="Use activities in equilibrium and rate expressions for non-ideal systems; measure or model activity coefficients",
        entity_scope="Chemical engineering, electrochemistry, biochemistry, geochemistry",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with validated models, moderate for extrapolation",
        controlling_precedent="Fundamental thermodynamic concept, universally taught",
        issue_category=IssueCategory.ACTIVITY_COEFFICIENTS,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="van der Waals Mixing Rules in Equation of State",
        keywords=["mixing rule", "van der waals", "binary interaction", "equation of state", "quadratic"],
        conclusion_template=[
            "Mixing rules combine pure component EOS parameters for mixtures.",
            "van der Waals one-fluid mixing rules are quadratic in composition.",
            "Binary interaction parameters kij correct unlike-pair interactions."
        ],
        reasoning_framework=[
            "EOS parameters for mixtures require mixing rules.",
            "van der Waals one-fluid theory: mixture treated as pseudo-pure fluid.",
            "Quadratic mixing for attractive parameter: a_mix = sum_i(sum_j(xi*xj*aij)).",
            "Cross parameter combining rule: aij = sqrt(ai*aj) * (1 - kij).",
            "Binary interaction parameter kij fitted to experimental binary VLE or LLE data.",
            "kij = 0 for similar molecules (geometric mean rule exact).",
            "kij ≠ 0 for dissimilar molecules, compensates for combining rule error.",
            "Linear mixing for covolume: b_mix = sum(xi*bi).",
            "Justification: volume is additive for hard spheres.",
            "Limitations: quadratic mixing fails for highly asymmetric or polar systems.",
            "Advanced mixing rules: Wong-Sandler, MHV2, LCVM combine EOS with G^E models.",
            "Wong-Sandler: matches EOS and activity coefficient model at infinite pressure.",
            "MHV2 (Modified Huron-Vidal): improved match between EOS and G^E.",
            "Huron-Vidal original: (a/b)_mix = sum(xi*ai/bi) + (G^E_infinity/C).",
            "LCVM (Linear Combination of Vidal and Michelsen): more accurate than MHV2.",
            "Advanced rules enable PR or SRK to handle polar systems better.",
            "Ternary and higher: no ternary interaction parameters typically, use binaries only.",
            "Parameter regression: minimize error in bubble point, K-values, or other properties.",
            "Databases: DIPPR, NIST TDE, Aspen databanks contain kij values.",
            "Default kij = 0 often inadequate, especially for polar-nonpolar or size-asymmetric pairs.",
            "Process simulator warnings if kij missing or extrapolated."
        ],
        key_factors=[
            "Similarity of mixture components",
            "Availability of binary VLE or LLE data",
            "Quality of kij parameter regression",
            "System polarity and asymmetry",
            "Pressure and temperature range",
            "Mixing rule complexity vs. accuracy tradeoff",
            "Software implementation of advanced rules",
            "Validation against experimental data"
        ],
        primary_authority=[
            "Sandler, S.I. (1999). Chemical and Engineering Thermodynamics, 3rd Ed.",
            "Wong, D.S.H., Sandler, S.I. (1992). A Theoretically Correct Mixing Rule. AIChE J.",
            "Michelsen, M.L., Kistenmacher, H. (1990). On Composition-Dependent Interaction Coefficients. Fluid Phase Equilib."
        ],
        burden_holder="Thermodynamics expert configuring EOS for mixtures",
        adversary_position="Default mixing rules in simulator adequate",
        counter_arguments=[
            "Default kij = 0 often gives poor results",
            "Accurate VLE predictions require good kij",
            "Polar or asymmetric systems need advanced mixing rules",
            "Process design accuracy depends on mixing rule quality",
            "Literature and databases provide kij for common pairs"
        ],
        resolution_strategy="Use van der Waals mixing with regressed kij for non-polar; use advanced mixing rules (Wong-Sandler, MHV2) for polar/asymmetric systems",
        entity_scope="Process simulation, VLE modeling, EOS applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with good kij data, lower without",
        controlling_precedent="Standard practice in EOS-based simulation",
        issue_category=IssueCategory.EQUATION_OF_STATE,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Joule-Thomson Effect and Coefficient",
        keywords=["joule-thomson", "throttling", "isenthalpic", "temperature", "coefficient"],
        conclusion_template=[
            "Joule-Thomson effect: temperature change when gas expands through throttle at constant enthalpy.",
            "JT coefficient mu = (dT/dP)_H positive for cooling, negative for heating.",
            "Natural gas processing uses JT cooling for dehydration and NGL recovery."
        ],
        reasoning_framework=[
            "Throttling process: adiabatic expansion through valve or porous plug, no work.",
            "First law: enthalpy constant (H1 = H2) for throttling.",
            "Joule-Thomson coefficient: mu_JT = (partial T/partial P)_H.",
            "For ideal gas: mu_JT = 0 (temperature unchanged).",
            "Real gases: mu_JT ≠ 0 due to intermolecular forces.",
            "mu_JT > 0: gas cools upon expansion (most gases at room T).",
            "mu_JT < 0: gas heats upon expansion (hydrogen, helium at room T).",
            "Inversion temperature T_inv: mu_JT changes sign.",
            "Above T_inv: gas heats on expansion; below T_inv: gas cools.",
            "For van der Waals gas: T_inv = 2a/(Rb), approximately 6.75*Tc.",
            "Linde liquefaction cycle: exploit JT cooling below inversion temperature.",
            "Precooling needed if initial T > T_inv.",
            "Natural gas: JT expansion in choke valve cools gas, condenses water and heavy HCs.",
            "Dehydration: JT cooling drops temperature below water dew point, water condenses.",
            "NGL recovery: JT cooling condenses C3+ hydrocarbons for separation.",
            "Pipeline pressure letdown: JT cooling can cause hydrate formation risk.",
            "Thermodynamic relation: mu_JT = (1/Cp) * [T*(dV/dT)_P - V].",
            "From EOS: calculate (dV/dT)_P and Cp, then mu_JT.",
            "Maximum cooling at intermediate pressure (optimization of expansion).",
            "Safety: rapid expansion can cause embrittlement of metal (cold spots).",
            "Cryogenic applications: hydrogen and helium require pre-cooling below inversion."
        ],
        key_factors=[
            "Initial temperature relative to inversion temperature",
            "Pressure drop magnitude",
            "Gas composition and properties",
            "Heat capacity at constant pressure",
            "Equation of state for real gas behavior",
            "Presence of condensable components",
            "Hydrate formation risk",
            "Equipment metallurgy and cold embrittlement"
        ],
        primary_authority=[
            "Smith, J.M., Van Ness, H.C., Abbott, M.M. Introduction to Chemical Engineering Thermodynamics.",
            "GPSA Engineering Data Book, Section 6: Thermodynamics.",
            "Poling, B.E., Prausnitz, J.M., O'Connell, J.P. Properties of Gases and Liquids."
        ],
        burden_holder="Gas processing engineer designing expansion or letdown systems",
        adversary_position="Joule-Thomson effect negligible or can be ignored",
        counter_arguments=[
            "JT cooling significant in high-pressure gas systems",
            "Hydrate formation from JT cooling causes pipeline blockages",
            "NGL recovery economics depend on JT separation",
            "Safety requires prediction of cold spots",
            "Thermodynamic calculations predict JT effect accurately"
        ],
        resolution_strategy="Calculate JT coefficient from EOS; design for hydrate prevention (inhibitors, heating) if JT cooling severe",
        entity_scope="Natural gas processing, pipeline operations, cryogenics, refrigeration",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence with good thermodynamic data and EOS",
        controlling_precedent="Well-established thermodynamic phenomenon, standard engineering consideration",
        issue_category=IssueCategory.THERMODYNAMIC_PROPERTIES,
        zoned_use=AnalysisZone.REPORTING
    ),

    DoctrineBlock(
        topic="Critical Point and Critical Phenomena",
        keywords=["critical point", "critical temperature", "critical pressure", "phase transition", "continuous"],
        conclusion_template=[
            "Critical point: highest temperature and pressure where liquid-vapor distinction exists.",
            "Above critical point, single supercritical phase with no phase boundary.",
            "Critical properties (Tc, Pc, Vc) essential parameters for equation of state."
        ],
        reasoning_framework=[
            "Critical point: terminus of vapor-liquid coexistence curve on PT diagram.",
            "At critical point: liquid and vapor densities become equal.",
            "Critical temperature Tc: maximum T for liquid-vapor equilibrium.",
            "Critical pressure Pc: vapor pressure at Tc.",
            "Critical volume Vc: molar volume at critical point.",
            "Critical compressibility Zc = Pc*Vc/(R*Tc), typically 0.27-0.30.",
            "van der Waals EOS: Zc = 3/8 = 0.375 (overestimates real gases).",
            "Peng-Robinson: Zc ≈ 0.307, Soave-RK: Zc ≈ 0.333.",
            "Phase diagram: critical point is apex of liquid-vapor dome.",
            "Critical isotherm: (dP/dV)_Tc = 0 and (d2P/dV2)_Tc = 0 at critical point.",
            "Near critical point: properties (Cp, compressibility) diverge.",
            "Critical opalescence: light scattering due to large density fluctuations.",
            "Law of rectilinear diameters: (rho_liquid + rho_vapor)/2 linear in T near Tc.",
            "Reduced properties: Tr = T/Tc, Pr = P/Pc, principle of corresponding states.",
            "Acentric factor omega: measure of molecular non-sphericity, omega = -log10(Pr_sat at Tr=0.7) - 1.",
            "For simple fluids (Ar, Kr): omega ≈ 0; for complex molecules: omega > 0.",
            "Critical properties from group contributions (Joback, Lydersen, Ambrose methods).",
            "Experimental determination: observe phase boundary vanishing, or fit EOS.",
            "Retrograde condensation near critical: unusual phase behavior in gas-condensate reservoirs.",
            "Mixture critical point: locus of mixture critical points as composition varies.",
            "Type I, II, III phase behavior classification based on critical loci.",
            "Engineering: avoid operation near critical (instability, property sensitivity)."
        ],
        key_factors=[
            "Pure component or mixture",
            "Experimental vs. estimated critical properties",
            "Proximity of operating conditions to critical point",
            "Equation of state accuracy near critical point",
            "Measurement techniques for critical properties",
            "Corresponding states correlations",
            "Mixture critical loci complexity",
            "Process stability and control near critical point"
        ],
        primary_authority=[
            "Poling, B.E., Prausnitz, J.M., O'Connell, J.P. Properties of Gases and Liquids, 5th Ed.",
            "Sengers, J.V., Kayser, R.F., Peters, C.J., White, H.J. Equations of State for Fluids and Fluid Mixtures.",
            "Reid, R.C., Prausnitz, J.M., Poling, B.E. Properties of Gases and Liquids, 4th Ed."
        ],
        burden_holder="Thermodynamicist estimating or using critical properties",
        adversary_position="Critical properties not needed for process conditions far from critical",
        counter_arguments=[
            "Critical properties required for EOS parametrization",
            "Corresponding states methods use Tc, Pc universally",
            "Near-critical processes (supercritical extraction) require precise values",
            "Property prediction accuracy depends on critical property quality",
            "Mixture phase behavior modeling requires mixture critical loci"
        ],
        resolution_strategy="Use experimental critical properties when available; estimate via group contributions if necessary; avoid near-critical operation when possible",
        entity_scope="Equation of state development, property estimation, supercritical processes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for pure components with data, moderate for estimated or mixtures",
        controlling_precedent="Fundamental phase behavior concept, universally applied",
        issue_category=IssueCategory.CRITICAL_PHENOMENA,
        zoned_use=AnalysisZone.REPORTING
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# ENGINE STATE
# ═══════════════════════════════════════════════════════════════════════════

class EngineState:
    def __init__(self):
        self.start_time = time.time()
        self.query_count = 0
        self.cache_hits = 0
        self.total_latency = 0.0
        self.last_query: Optional[str] = None
        self.telemetry_log: List[TelemetryData] = []
        self.doctrine_hit_count: Dict[str, int] = {}
        self.error_count = 0

    def record_query(self, telemetry: TelemetryData):
        self.query_count += 1
        if telemetry.cache_hit:
            self.cache_hits += 1
        self.total_latency += telemetry.latency_ms
        self.last_query = telemetry.query_id
        self.telemetry_log.append(telemetry)
        for doc in telemetry.doctrine_triggered:
            self.doctrine_hit_count[doc] = self.doctrine_hit_count.get(doc, 0) + 1
        if telemetry.error_domain:
            self.error_count += 1

    def get_metrics(self) -> MetricsSnapshot:
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / self.query_count if self.query_count > 0 else 0.0
        cache_rate = self.cache_hits / self.query_count if self.query_count > 0 else 0.0
        error_rate = self.error_count / self.query_count if self.query_count > 0 else 0.0
        coverage = len(self.doctrine_hit_count) / len(DOCTRINE_CACHE) if DOCTRINE_CACHE else 0.0

        return MetricsSnapshot(
            total_queries=self.query_count,
            cache_hits=self.cache_hits,
            avg_latency_ms=avg_latency,
            error_rate=error_rate,
            doctrine_coverage=coverage,
            uptime_seconds=uptime
        )


STATE = EngineState()


# ═══════════════════════════════════════════════════════════════════════════
# TIE-20 COMPONENT IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════════════════════

def doctrine_cache_lookup(query: str, zone: AnalysisZone) -> Tuple[bool, List[DoctrineBlock]]:
    """Layer 1: Fast doctrine cache lookup (0-200ms target)."""
    query_lower = query.lower()
    matches = []

    for doctrine in DOCTRINE_CACHE:
        if doctrine.zoned_use != zone:
            continue
        score = 0
        for keyword in doctrine.keywords:
            if keyword.lower() in query_lower:
                score += 1
        if score >= 2:
            matches.append(doctrine)

    cache_hit = len(matches) > 0
    return cache_hit, matches


def semantic_normalization(query: str) -> str:
    """Normalize domain-specific terminology."""
    mapping = {
        "equation of state": ["eos", "cubic equation", "peng robinson", "srk"],
        "activity coefficient": ["activity model", "gamma", "excess gibbs", "nrtl"],
        "phase equilibrium": ["vle", "lle", "flash", "bubble point", "dew point"],
        "fugacity": ["fugacity coefficient", "phi", "chemical potential"],
        "gibbs energy": ["gibbs free energy", "free energy", "g"],
        "enthalpy": ["heat", "delta h", "heat of reaction"],
        "entropy": ["disorder", "delta s", "second law"],
        "equilibrium constant": ["k value", "keq", "equilibrium"],
        "critical point": ["critical temperature", "critical pressure", "tc", "pc"],
        "supercritical": ["scf", "supercritical fluid", "sc-co2"],
        "azeotrope": ["constant boiling", "minimum boiling", "maximum boiling"],
        "excess property": ["excess gibbs", "excess enthalpy", "non-ideal"],
        "mixing rule": ["van der waals", "wong-sandler", "binary interaction"],
        "virial": ["virial coefficient", "second virial", "third virial"],
    }

    normalized = query.lower()
    for canonical, variants in mapping.items():
        for variant in variants:
            if variant in normalized:
                normalized = normalized.replace(variant, canonical)
    return normalized


def confidence_stratification(doctrines: List[DoctrineBlock], query: str) -> ConfidenceLevel:
    """Determine confidence level based on doctrine matches and query."""
    if not doctrines:
        return ConfidenceLevel.DISCLOSURE

    confidence_scores = [d.confidence for d in doctrines]

    # Check for high-risk keywords
    high_risk_terms = ["novel", "untested", "experimental", "no data", "extrapolation"]
    if any(term in query.lower() for term in high_risk_terms):
        return ConfidenceLevel.HIGH_RISK

    # If multiple DEFENSIBLE doctrines, return DEFENSIBLE
    defensible_count = sum(1 for c in confidence_scores if c == ConfidenceLevel.DEFENSIBLE)
    if defensible_count >= 2:
        return ConfidenceLevel.DEFENSIBLE

    # Return most conservative
    if ConfidenceLevel.HIGH_RISK in confidence_scores:
        return ConfidenceLevel.HIGH_RISK
    if ConfidenceLevel.DISCLOSURE in confidence_scores:
        return ConfidenceLevel.DISCLOSURE
    if ConfidenceLevel.AGGRESSIVE in confidence_scores:
        return ConfidenceLevel.AGGRESSIVE

    return ConfidenceLevel.DEFENSIBLE


def authority_hardening(doctrines: List[DoctrineBlock]) -> List[str]:
    """Extract and rank authorities from triggered doctrines."""
    authorities = []
    for doctrine in doctrines:
        authorities.extend(doctrine.primary_authority)
    # Deduplicate and return
    return list(set(authorities))


def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[str], ConfidenceLevel, float]:
    """TIE-20 Component: Three-layer response (cache -> semantic -> deep)."""
    start_time = time.time()

    # Layer 1: Doctrine cache
    cache_hit, doctrines = doctrine_cache_lookup(query, zone)

    if not cache_hit:
        # Layer 2: Semantic retrieval (placeholder - would use vector DB)
        normalized_query = semantic_normalization(query)
        _, doctrines = doctrine_cache_lookup(normalized_query, zone)

    if not doctrines:
        # Layer 3: Deep analysis (fallback)
        answer = f"Deep analysis required for: {query}. No direct doctrine match found. Recommend consulting thermodynamics specialist."
        confidence = ConfidenceLevel.DISCLOSURE
        authorities = []
    else:
        # Construct answer from doctrines
        if mode == ResponseMode.FAST:
            answer = " ".join(doctrines[0].conclusion_template)
        elif mode == ResponseMode.DEFENSE:
            answer = "\n\n".join([
                f"DOCTRINE: {d.topic}",
                f"CONCLUSION: {' '.join(d.conclusion_template)}",
                f"AUTHORITY: {'; '.join(d.primary_authority[:2])}",
                f"CONFIDENCE: {d.confidence_stratification}"
            ] for d in doctrines[:3])
        else:  # MEMO
            answer = "\n\n".join([
                f"=== {d.topic.upper()} ===",
                f"Conclusion: {' '.join(d.conclusion_template)}",
                f"Reasoning: {' '.join(d.reasoning_framework[:10])}...",
                f"Key Factors: {', '.join(d.key_factors[:5])}",
                f"Primary Authority: {'; '.join(d.primary_authority)}",
                f"Confidence: {d.confidence_stratification}",
                f"Issue Category: {d.issue_category.value}"
            ] for d in doctrines[:5])

        confidence = confidence_stratification(doctrines, query)
        authorities = authority_hardening(doctrines)

    latency_ms = (time.time() - start_time) * 1000
    doctrine_names = [d.topic for d in doctrines]

    return answer, doctrine_names, confidence, latency_ms


def determinism_hash(query: str, answer: str, mode: ResponseMode) -> str:
    """Generate SHA-256 hash for reproducibility."""
    content = f"{query}|{answer}|{mode.value}"
    return hashlib.sha256(content.encode()).hexdigest()


def audit_trail_append(query_id: str, query: str, answer: str, doctrines: List[str], confidence: ConfidenceLevel):
    """Append to JSONL audit trail."""
    log_file = Path(__file__).parent / f"chem18_audit_{datetime.now():%Y%m%d}.jsonl"
    entry = {
        "query_id": query_id,
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "doctrines_triggered": doctrines,
        "confidence": confidence.value
    }
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def fact_fragility_scoring(doctrines: List[DoctrineBlock]) -> Dict[str, Any]:
    """Score fact fragility based on doctrine characteristics."""
    if not doctrines:
        return {"fragility": "HIGH", "reason": "No doctrine support"}

    authority_count = sum(len(d.primary_authority) for d in doctrines)
    if authority_count >= 5:
        fragility = "LOW"
    elif authority_count >= 3:
        fragility = "MEDIUM"
    else:
        fragility = "HIGH"

    return {
        "fragility": fragility,
        "authority_count": authority_count,
        "doctrine_count": len(doctrines)
    }


def coverage_map() -> Dict[str, Any]:
    """Generate doctrine coverage map."""
    total_doctrines = len(DOCTRINE_CACHE)
    triggered = STATE.doctrine_hit_count
    coverage_pct = (len(triggered) / total_doctrines * 100) if total_doctrines > 0 else 0.0

    untriggered = [d.topic for d in DOCTRINE_CACHE if d.topic not in triggered]

    return {
        "total_doctrines": total_doctrines,
        "triggered_doctrines": len(triggered),
        "coverage_percent": round(coverage_pct, 1),
        "most_used": sorted(triggered.items(), key=lambda x: x[1], reverse=True)[:5],
        "untriggered_sample": untriggered[:10]
    }


def drift_watcher() -> Dict[str, Any]:
    """Detect doctrine drift over time (placeholder)."""
    return {
        "drift_detected": False,
        "message": "Drift detection requires longitudinal query analysis"
    }


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title=ENGINE_NAME,
    version=VERSION,
    description="TIE-Grade Chemical Thermodynamics Intelligence Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Dict[str, str])
async def root():
    return {
        "engine": ENGINE_ID,
        "name": ENGINE_NAME,
        "version": VERSION,
        "status": "operational"
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """TIE-20 Component: Health endpoint."""
    metrics = STATE.get_metrics()
    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        uptime_seconds=metrics.uptime_seconds,
        total_queries=metrics.total_queries,
        cache_hit_rate=metrics.cache_hits / metrics.total_queries if metrics.total_queries > 0 else 0.0,
        avg_latency_ms=metrics.avg_latency_ms,
        doctrine_count=len(DOCTRINE_CACHE),
        last_query=STATE.last_query
    )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Main query endpoint with TIE-20 components."""
    query_id = hashlib.sha256(f"{request.query}{time.time()}".encode()).hexdigest()[:16]

    logger.info(f"Query {query_id}: {request.query[:100]}")

    # Three-layer response
    answer, doctrines, confidence, latency_ms = three_layer_response(
        request.query, request.mode, request.zone
    )

    # Determinism hash
    det_hash = determinism_hash(request.query, answer, request.mode)

    # Audit trail
    audit_trail_append(query_id, request.query, answer, doctrines, confidence)

    # Telemetry
    telemetry = TelemetryData(
        query_id=query_id,
        timestamp=time.time(),
        mode=request.mode,
        latency_ms=latency_ms,
        cache_hit=len(doctrines) > 0,
        doctrine_triggered=doctrines,
        confidence=confidence
    )
    STATE.record_query(telemetry)

    return QueryResponse(
        query_id=query_id,
        answer=answer,
        confidence=confidence,
        doctrine_triggered=doctrines,
        latency_ms=latency_ms,
        mode=request.mode,
        determinism_hash=det_hash,
        timestamp=datetime.now().isoformat()
    )


@app.get("/metrics", response_model=MetricsSnapshot)
async def metrics():
    """TIE-20 Component: Metrics collector."""
    return STATE.get_metrics()


@app.get("/coverage", response_model=Dict[str, Any])
async def coverage():
    """TIE-20 Component: Coverage map."""
    return coverage_map()


@app.get("/drift", response_model=Dict[str, Any])
async def drift():
    """TIE-20 Component: Drift watcher."""
    return drift_watcher()


@app.get("/doctrines", response_model=List[Dict[str, Any]])
async def list_doctrines():
    """List all doctrine blocks."""
    return [
        {
            "topic": d.topic,
            "category": d.issue_category.value,
            "keywords": d.keywords,
            "confidence": d.confidence.value,
            "zone": d.zoned_use.value
        }
        for d in DOCTRINE_CACHE
    ]


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
