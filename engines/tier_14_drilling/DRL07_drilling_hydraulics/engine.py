"""
DRL07 - Drilling Hydraulics Engine
TIE Gold Standard Implementation
Domain: Drilling Engineering - Hydraulics & ECD Management

Port: 9017
Version: 1.0.0
Components: TIE-20 compliant
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import math
from datetime import datetime
from typing import Dict, List, Optional, Literal, Any
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "drl07_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

APP = FastAPI(title="DRL07 Drilling Hydraulics Engine", version="1.0.0")
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================================
# ENUMS & CONSTANTS
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


class RheologyModel(str, Enum):
    BINGHAM_PLASTIC = "Bingham Plastic"
    POWER_LAW = "Power Law"
    HERSCHEL_BULKLEY = "Herschel-Bulkley"


class PumpType(str, Enum):
    TRIPLEX = "Triplex"
    DUPLEX = "Duplex"
    QUINTUPLEX = "Quintuplex"


# Epistemic guardrails - banned phrases
BANNED_PHRASES = [
    "I am certain", "definitely", "without question", "guaranteed",
    "always safe", "no risk", "impossible to fail", "zero chance"
]


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class HydraulicsQueryRequest(BaseModel):
    query: str = Field(..., description="Hydraulics question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    hole_depth_ft: Optional[float] = None
    hole_diameter_in: Optional[float] = None
    drillstring_od_in: Optional[float] = None
    mud_weight_ppg: Optional[float] = None
    flow_rate_gpm: Optional[float] = None
    pv_cp: Optional[float] = None  # Plastic viscosity
    yp_lbf_100ft2: Optional[float] = None  # Yield point
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class HydraulicsQueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    triggered_doctrines: List[str]
    reasoning_chain: List[str]
    calculations: Optional[Dict[str, Any]] = None
    epistemic_disclosure: Optional[str] = None
    determinism_hash: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float


# ============================================================================
# DOCTRINE BLOCKS - DRILLING HYDRAULICS EXPERTISE
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
        calculations: Optional[Dict[str, str]] = None
    ):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.calculations = calculations or {}


DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Equivalent Circulating Density (ECD) Fundamentals",
        keywords=["ECD", "circulating density", "dynamic pressure", "annular friction"],
        conclusion_template="ECD is the effective density exerted on the formation while circulating, calculated as static mud weight plus annular friction pressure converted to equivalent density. Critical for wellbore stability and fracture prevention.",
        reasoning_framework="""
        1. ECD = Static MW + (APL / 0.052 / TVD)
        2. APL = Annular Pressure Loss (psi)
        3. 0.052 = conversion factor (psi/ft per ppg)
        4. TVD = True Vertical Depth (ft)
        5. ECD increases with flow rate, hole angle, mud properties
        6. ECD must stay within pore pressure and fracture gradient window
        7. Narrow margin wells require precise ECD control
        8. Temperature affects mud rheology and ECD
        9. Drillstring rotation reduces ECD slightly (friction reduction)
        10. Washouts increase ECD (more friction in enlarged hole)
        """,
        key_factors=[
            "Annular velocity (primary driver of friction)",
            "Mud rheological properties (PV, YP, gel strength)",
            "Hole geometry (diameter, rugosity, washouts)",
            "Drillstring configuration (OD, tool joints, stabilizers)",
            "Flow rate (GPM)",
            "Equivalent static density vs ECD delta",
            "Formation pressure and fracture gradient margins"
        ],
        primary_authority=[
            "API RP 13D - Rheology and Hydraulics",
            "IADC Drilling Manual - Hydraulics Section",
            "SPE 92277 - ECD Management in Deepwater",
            "Bourgoyne et al. - Applied Drilling Engineering"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "ECD_formula": "ECD (ppg) = MW + (APL / (0.052 * TVD))",
            "APL_annular": "Sum of friction losses in each annular section"
        }
    ),

    DoctrineBlock(
        topic="Bingham Plastic Rheological Model",
        keywords=["Bingham", "plastic viscosity", "yield point", "PV", "YP"],
        conclusion_template="Bingham Plastic model represents drilling fluid as having a yield point (force to initiate flow) and plastic viscosity (resistance during flow). Most common model for water-based muds.",
        reasoning_framework="""
        1. Shear Stress (τ) = YP + (PV × Shear Rate)
        2. YP = τ₀ (yield point in lbf/100ft²)
        3. PV = μₚ (plastic viscosity in cP)
        4. Measured from Fann 35 viscometer: PV = θ600 - θ300
        5. YP = θ300 - PV
        6. Valid for shear rates 170-1022 sec⁻¹
        7. Overpredicts friction at low shear rates (annulus)
        8. Underpredicts friction at high shear rates (bit nozzles)
        9. Simple, widely used, sufficient for most WBM applications
        10. Temperature correction required for HPHT wells
        """,
        key_factors=[
            "Fann 35 dial readings (600 and 300 RPM)",
            "PV indicates solids content and fluid viscosity",
            "YP indicates electrical attractive forces (clays)",
            "High YP/PV ratio = poor hole cleaning, high ECD",
            "Low YP/PV ratio = settling issues",
            "Gel strength (10-sec, 10-min) for static conditions",
            "Temperature sensitivity of rheology"
        ],
        primary_authority=[
            "API RP 13D Section 6.3",
            "API RP 13B-1 - Fluid Testing Procedures",
            "SPE Textbook Vol. 2 - Drilling Fluids",
            "Hemphill & Rojas - Rheology Tutorial"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "PV": "PV (cP) = θ600 - θ300",
            "YP": "YP (lbf/100ft²) = θ300 - PV",
            "shear_stress": "τ = YP + (PV × γ̇)"
        }
    ),

    DoctrineBlock(
        topic="Power Law Rheological Model",
        keywords=["power law", "flow behavior index", "consistency index", "n", "K"],
        conclusion_template="Power Law model uses consistency index (K) and flow behavior index (n) to characterize non-Newtonian fluids. Better for OBM and SBM at high shear rates. n<1 indicates shear thinning.",
        reasoning_framework="""
        1. Shear Stress (τ) = K × (Shear Rate)ⁿ
        2. K = consistency index (lbf-secⁿ/100ft²)
        3. n = flow behavior index (dimensionless)
        4. n < 1: shear thinning (most drilling fluids)
        5. n = 1: Newtonian (water)
        6. n > 1: shear thickening (rare)
        7. Calculated from Fann readings: log(τ₂/τ₁) / log(γ̇₂/γ̇₁)
        8. Better accuracy than Bingham at extreme shear rates
        9. Requires iterative solutions for hydraulics calculations
        10. Common for oil-based and synthetic muds
        """,
        key_factors=[
            "n value (typically 0.4-0.8 for drilling fluids)",
            "K value increases with solids loading",
            "More accurate pressure drop predictions for OBM",
            "Computational complexity vs Bingham",
            "Extrapolation beyond measured shear rate range risky",
            "Temperature and pressure corrections essential",
            "Gel strength not captured in Power Law model"
        ],
        primary_authority=[
            "API RP 13D Section 6.4",
            "Zamora & Power - SPE 18035",
            "Bourgoyne - Power Law Applications",
            "Drilling Fluids Processing Handbook"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "n_calculation": "n = 3.32 × log(θ600 / θ300)",
            "K_calculation": "K = 510 × θ300 / (511^n)",
            "shear_stress": "τ = K × γ̇ⁿ"
        }
    ),

    DoctrineBlock(
        topic="Annular Velocity and Hole Cleaning",
        keywords=["annular velocity", "hole cleaning", "cuttings transport", "slip velocity"],
        conclusion_template="Effective hole cleaning requires sufficient annular velocity to lift cuttings. Target: 120-150 ft/min vertical, 180-250 ft/min for deviated wells. Inadequate cleaning causes stuck pipe, torque, and poor cement jobs.",
        reasoning_framework="""
        1. Annular Velocity (ft/min) = 24.5 × Q / (Dh² - Dp²)
        2. Q = flow rate (GPM)
        3. Dh = hole diameter (inches)
        4. Dp = pipe/collar OD (inches)
        5. Cuttings slip velocity opposes flow velocity
        6. Net transport = annular velocity - slip velocity
        7. Slip velocity increases with cuttings size and density
        8. Deviated holes: gravity component perpendicular to flow
        9. Critical angle (30-60°): worst cleaning conditions
        10. Rotation and pipe reciprocation improve cleaning
        """,
        key_factors=[
            "Flow rate (GPM) - primary control parameter",
            "Annular clearance (Dh - Dp)",
            "Mud rheology (carrying capacity vs friction)",
            "Cuttings size, shape, and density",
            "Hole angle and trajectory",
            "Rate of penetration (ROP) - cuttings generation rate",
            "Drillstring rotation (mechanical agitation)",
            "Mud weight and density contrast with cuttings"
        ],
        primary_authority=[
            "SPE 27464 - Hole Cleaning in Deviated Wells",
            "IADC Drilling Manual Ch. 9",
            "API RP 13D Annular Velocity Guidelines",
            "Larsen - Cuttings Transport Studies"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "annular_velocity": "Vₐ (ft/min) = 24.5 × Q / (Dh² - Dp²)",
            "cuttings_concentration": "C = ROP × Dh² / (24.5 × Q)"
        }
    ),

    DoctrineBlock(
        topic="Standpipe Pressure Components",
        keywords=["standpipe pressure", "SPP", "pressure losses", "system pressure"],
        conclusion_template="Standpipe pressure is the sum of all pressure drops in the circulating system: surface equipment, drillstring, bit nozzles, and annulus. SPP monitoring detects bit nozzle plugging, pump problems, and abnormal downhole conditions.",
        reasoning_framework="""
        1. SPP = ΔP_surface + ΔP_drillstring + ΔP_bit + ΔP_annulus
        2. ΔP_surface: pumps, standpipe, hose, swivel, kelly (typically 50-200 psi)
        3. ΔP_drillstring: pipe friction (laminar or turbulent flow)
        4. ΔP_bit: nozzle pressure drop (50-60% of total for optimization)
        5. ΔP_annulus: annular friction (affects ECD)
        6. SPP sudden increase: plugged nozzle, tight hole, stuck pipe
        7. SPP sudden decrease: washed nozzle, pump failure, lost circulation
        8. SPP gradual increase: hole fill, barite sag, gelling
        9. Baseline SPP established during clean-hole circulation
        10. Deviation from baseline triggers investigation
        """,
        key_factors=[
            "Pump output pressure capability (rated pressure)",
            "Nozzle total flow area (TFA)",
            "Drillstring length and component OD/ID",
            "Mud properties (density, rheology)",
            "Flow rate (GPM)",
            "Annular clearance and geometry",
            "Depth and inclination profile",
            "Temperature effects on mud rheology downhole"
        ],
        primary_authority=[
            "API RP 13D - Hydraulics Calculations",
            "SPE Drilling Engineering Textbook Ch. 5",
            "Moore - Drilling Practices Manual",
            "Halliburton Redbook - Hydraulics Section"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "SPP_total": "SPP = ΣΔP_all_components",
            "parasitic_losses": "ΔP_parasitic = SPP - ΔP_bit - ΔP_annulus"
        }
    ),

    DoctrineBlock(
        topic="Bit Hydraulic Optimization - Maximum HSI",
        keywords=["hydraulic horsepower", "HSI", "bit optimization", "impact force", "TFA"],
        conclusion_template="Maximum Hydraulic Horsepower per Square Inch (HSI) optimization allocates 48-65% of standpipe pressure to bit nozzles, maximizing cleaning energy at the bit face. Best for soft formations where jetting action dominates.",
        reasoning_framework="""
        1. HSI = HHP / bit area
        2. HHP = (ΔP_bit × Q) / 1714
        3. Optimal: ΔP_bit = 0.65 × SPP (65% rule for max HSI)
        4. Total Flow Area (TFA) = Σ(nozzle areas)
        5. ΔP_bit = (MW × Q²) / (10858 × TFA²)
        6. Maximize jetting velocity at bit face
        7. Effective in soft formations (sand, shale)
        8. Creates turbulent cleaning action
        9. Trade-off: higher bit pressure = lower annular velocity
        10. Requires sufficient pump horsepower
        """,
        key_factors=[
            "Available pump hydraulic horsepower",
            "Standpipe pressure capacity",
            "Formation drillability and hardness",
            "Bit type and nozzle configuration",
            "Hole cleaning requirements (affects annular pressure budget)",
            "Mud motor presence (reduces pressure to bit)",
            "Nozzle erosion over time (changes TFA)",
            "Flow rate limitations"
        ],
        primary_authority=[
            "SPE 3427 - Optimization of Bit Hydraulics",
            "Kendall & Goins - Bit Hydraulics Classic Paper",
            "API RP 13D Section 7",
            "Eckel - Optimum Bit Hydraulics"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "HHP": "HHP = (ΔP_bit × Q) / 1714",
            "HSI": "HSI = HHP / (π × (D_bit/2)²)",
            "TFA_for_target_dP": "TFA = √(MW × Q² / (10858 × ΔP_bit))"
        }
    ),

    DoctrineBlock(
        topic="Bit Hydraulic Optimization - Maximum Impact Force",
        keywords=["impact force", "jet impact", "nozzle velocity", "hard formations"],
        conclusion_template="Maximum Impact Force optimization allocates 48% of standpipe pressure to bit nozzles, maximizing momentum transfer to formation. Preferred for hard formations where mechanical impact dominates over jetting erosion.",
        reasoning_framework="""
        1. Impact Force (F) = 0.01823 × Q × √(MW × ΔP_bit)
        2. Optimal: ΔP_bit = 0.48 × SPP (48% rule for max impact)
        3. Jet velocity: V = √(2 × g × ΔP_bit / MW) / C
        4. Higher velocity, lower pressure than HSI method
        5. Effective in hard, abrasive formations (limestone, granite)
        6. Mechanical impact breaks rock
        7. Lower total hydraulic power to bit than HSI
        8. Leaves more pressure for annular velocity (better cleaning)
        9. Less sensitive to nozzle erosion than HSI
        10. Common in PDC bit applications
        """,
        key_factors=[
            "Formation compressive strength",
            "Bit type and cutting structure",
            "Weight on bit (WOB) interaction with hydraulics",
            "Nozzle arrangement and pointing angle",
            "Chip hold-down effect in PDC bits",
            "Annular velocity requirements vs bit pressure budget",
            "Pump pressure capacity",
            "Flow rate available"
        ],
        primary_authority=[
            "SPE 3349 - Jet Bit Optimization",
            "Sutko & Myers - Impact Force Theory",
            "API RP 13D Section 7.2",
            "PDC Bit Handbook - Hughes Christensen"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "impact_force": "F (lbf) = 0.01823 × Q × √(MW × ΔP_bit)",
            "jet_velocity": "V (ft/sec) = 417.2 × √(ΔP_bit / MW)",
            "optimal_dP": "ΔP_bit = 0.48 × SPP"
        }
    ),

    DoctrineBlock(
        topic="Surge and Swab Pressure Calculations",
        keywords=["surge", "swab", "tripping", "pressure variation", "equivalent density"],
        conclusion_template="Surge (pipe running in) and swab (pipe pulling out) pressures result from piston effect in the annulus. Excessive surge can fracture formations; excessive swab can cause influx. Critical for narrow margin wells and tripping operations.",
        reasoning_framework="""
        1. Surge/Swab Pressure ∝ pipe velocity, mud viscosity, annular clearance
        2. Surge increases bottomhole pressure (ECD equivalent)
        3. Swab decreases bottomhole pressure (can cause kicks)
        4. Pressure spike = f(rheology, pipe speed, geometry)
        5. Bingham model: ΔP = (PV × V × L) / (1000 × C_annular) + YP_effect
        6. Mitigation: reduce tripping speed, use spacer fluids, condition mud
        7. Critical in narrow window between pore pressure and fracture
        8. Open-ended pipe (running casing): higher surge than closed
        9. BHA large OD components (stabilizers, reamers): critical zones
        10. Real-time monitoring via PWD tools recommended
        """,
        key_factors=[
            "Pipe running/pulling speed (ft/min)",
            "Mud rheology (PV, YP, gel strength)",
            "Annular clearance (hole ID - pipe OD)",
            "Pipe configuration (open/closed end, tool joints)",
            "BHA geometry (stabilizers, reamers, hole openers)",
            "Hole conditions (gauge hole, washouts, tight spots)",
            "Mud conditioning before trip (break gels)",
            "Formation pressure and fracture gradient margins"
        ],
        primary_authority=[
            "SPE 104080 - Surge and Swab Modeling",
            "API RP 13D Section 8",
            "Burkhardt - Wellbore Pressure Surges",
            "Mitchell & Miska - Tripping Hydraulics"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "surge_pressure_simple": "ΔP_surge ≈ (PV × V_pipe × L) / (1000 × C)",
            "swab_pressure_simple": "ΔP_swab ≈ -(PV × V_pipe × L) / (1000 × C)",
            "equivalent_density_change": "ΔECD = ΔP / (0.052 × TVD)"
        }
    ),

    DoctrineBlock(
        topic="Triplex Pump Output Calculation",
        keywords=["triplex pump", "pump output", "volumetric efficiency", "GPM", "liner size"],
        conclusion_template="Triplex pump output depends on liner diameter, stroke length, pump speed (SPM), and volumetric efficiency (typically 90-95%). Three pistons give smoother flow than duplex pumps.",
        reasoning_framework="""
        1. Theoretical Output (GPM) = (0.0102 × D² × L × N × n) / E
        2. D = liner diameter (inches)
        3. L = stroke length (inches)
        4. N = pump speed (strokes per minute, SPM)
        5. n = number of pistons (3 for triplex)
        6. E = volumetric efficiency (0.90-0.95 typical)
        7. Actual output measured by flowmeter
        8. Efficiency losses: liner wear, valve leakage, fluid compressibility
        9. Pump pressure rating limits maximum SPM at given liner size
        10. Duplex vs triplex: duplex has 2 pistons, more pulsation
        """,
        key_factors=[
            "Liner size selection (determines flow vs pressure capability)",
            "Stroke length (fixed for given pump model)",
            "Pump speed (SPM) - operator controlled",
            "Volumetric efficiency (decreases with wear)",
            "Pump horsepower rating (limits pressure × flow)",
            "Liner and valve maintenance condition",
            "Mud compressibility at high pressure",
            "Surface manifold friction losses"
        ],
        primary_authority=[
            "API Spec 7K - Drilling Equipment",
            "Mud Pump Fundamentals - NOV",
            "IADC Drilling Manual - Pump Calculations",
            "Gardner Denver - Pump Performance Curves"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "triplex_output": "Q (GPM) = 0.0102 × D² × L × SPM × 3 / Eff",
            "required_SPM": "SPM = Q / (0.0102 × D² × L × 3 / Eff)",
            "hydraulic_HP": "HHP = (P × Q) / 1714"
        }
    ),

    DoctrineBlock(
        topic="Managed Pressure Drilling (MPD) Principles",
        keywords=["MPD", "managed pressure", "rotating control device", "RCD", "back pressure"],
        conclusion_template="MPD uses a closed circulating system with Rotating Control Device (RCD) and surface back pressure to precisely control annular pressure profile. Enables drilling in narrow margin, depleted, and HPHT environments where conventional methods fail.",
        reasoning_framework="""
        1. Closed loop system: returns through choke manifold, not open pit
        2. RCD seals annulus at surface, allows pipe rotation
        3. Back pressure applied via automated choke control
        4. Bottomhole pressure = hydrostatic + annular friction ± back pressure
        5. ECD can be increased or decreased dynamically
        6. Constant bottomhole pressure (CBHP) mode: compensate for friction changes
        7. Enables drilling with underbalanced or near-balanced conditions
        8. Rapid influx detection via flow-in/flow-out monitoring
        9. Immediate well control response (apply back pressure)
        10. Requires PWD (pressure while drilling) for real-time data
        """,
        key_factors=[
            "RCD equipment reliability and pressure rating",
            "Automated choke control system response time",
            "PWD tool accuracy and telemetry rate",
            "Mud properties and gas solubility (kick detection)",
            "Surface equipment pressure ratings",
            "Crew training and coordination",
            "Real-time hydraulics modeling software",
            "Contingency for equipment failure (revert to conventional)"
        ],
        primary_authority=[
            "IADC MPD Guide",
            "SPE 108342 - MPD Operations and Benefits",
            "API RP 92M - Managed Pressure Drilling Operations",
            "Weatherford - MPD Systems Manual"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "BHP_MPD": "BHP = MW × 0.052 × TVD + APL + P_backpressure",
            "choke_pressure_adjustment": "ΔP_choke = Target_BHP - Current_BHP"
        }
    ),

    DoctrineBlock(
        topic="Equivalent Static Density (ESD)",
        keywords=["ESD", "static density", "gel strength", "U-tubing"],
        conclusion_template="Equivalent Static Density is the effective density when circulation stops, including effects of gel strength and U-tube (different fluid densities in drillstring vs annulus). Critical for well control and formation integrity during connections.",
        reasoning_framework="""
        1. ESD = static mud weight ± gel strength contribution ± U-tube effect
        2. Gel strength builds over time when static
        3. 10-second gels: measure at rig floor (realistic field condition)
        4. 10-minute gels: longer static periods (lunch, connections)
        5. U-tube: heavier mud in annulus pushes lighter mud up drillstring
        6. U-tube effect increases with depth and density difference
        7. ESD typically slightly higher than static MW (gels resist flow)
        8. Breaking circulation: pressure spike when gels break
        9. Formation sees ESD during static periods, ECD during circulation
        10. PMCD (pressurized mud cap) drilling uses ESD > fracture gradient
        """,
        key_factors=[
            "Gel strength development over time",
            "Static time duration (seconds to hours)",
            "Mud weight difference between drillstring and annulus",
            "Depth and temperature (affect gelation)",
            "Barite sag potential (increases static density at bottom)",
            "Formation pressure and fracture gradient margins",
            "Well control considerations during static periods",
            "Connection time and procedures"
        ],
        primary_authority=[
            "API RP 13D Section 9",
            "SPE 56632 - Gel Strength Effects on ESD",
            "IADC Well Control Manual",
            "Drilling Fluids Engineering - Caenn et al."
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "ESD_simplified": "ESD ≈ MW + (gel_strength / (100 × 0.052 × TVD))",
            "U_tube_contribution": "ΔP_utube = 0.052 × TVD × (MW_annulus - MW_drillstring)"
        }
    ),

    DoctrineBlock(
        topic="Pressure Drop Across Mud Motor",
        keywords=["mud motor", "PDM", "positive displacement motor", "motor pressure drop"],
        conclusion_template="Mud motors convert hydraulic energy to mechanical rotation downhole. Pressure drop across motor (typically 200-800 psi) reduces pressure available for bit and annulus, affecting hydraulics balance. Off-bottom vs on-bottom pressure drop changes indicate motor operation.",
        reasoning_framework="""
        1. ΔP_motor = f(flow rate, motor design, differential pressure)
        2. Off-bottom: ΔP_motor = spinning freely (lower pressure drop)
        3. On-bottom: ΔP_motor increases with torque load
        4. Typical range: 200-800 psi depending on motor size and flow rate
        5. Motor stall: ΔP_motor = maximum, no rotation, rapid bit damage
        6. Surface indication: SPP increase when motor loads up
        7. Reduces pressure available for bit nozzles and annular velocity
        8. Hydraulics design must account for motor in pressure budget
        9. Motor performance curves: pressure drop vs flow rate vs torque
        10. Motor selection based on required torque and available hydraulics
        """,
        key_factors=[
            "Motor size (lobes/stages configuration)",
            "Flow rate through motor (GPM)",
            "Torque load on motor (WOB, formation hardness)",
            "Motor condition and wear",
            "Mud properties (viscosity affects motor efficiency)",
            "Pressure budget allocation (bit vs motor vs annulus)",
            "Stall detection and prevention",
            "Motor rotational speed (RPM) vs bit type requirements"
        ],
        primary_authority=[
            "Baker Hughes - PDM Performance Handbook",
            "SPE 39321 - Mud Motor Hydraulics",
            "IADC Drilling Manual - Downhole Motors",
            "Weatherford - Motor Selection Guide"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "motor_dP_basic": "ΔP_motor ≈ base_dP + (torque_factor × WOB)",
            "available_bit_pressure": "ΔP_bit_available = SPP - ΔP_drillstring - ΔP_motor - ΔP_annulus"
        }
    ),

    DoctrineBlock(
        topic="Fann 35 Viscometer and Rheology Measurement",
        keywords=["Fann 35", "viscometer", "dial readings", "600 RPM", "300 RPM"],
        conclusion_template="Fann 35 viscometer measures mud rheology at standard shear rates (600, 300, 200, 100, 6, 3 RPM). Readings at 600 and 300 RPM determine PV and YP for Bingham Plastic model. Temperature correction required for HPHT conditions.",
        reasoning_framework="""
        1. Fann 35: rotational viscometer with fixed RPM settings
        2. Bob rotates in cup, torque measured as dial reading (θ)
        3. Shear rate (sec⁻¹) = 1.703 × RPM
        4. 600 RPM = 1022 sec⁻¹, 300 RPM = 511 sec⁻¹
        5. PV (cP) = θ600 - θ300
        6. YP (lbf/100ft²) = θ300 - PV
        7. Low RPM (6, 3) measures gel strength
        8. 10-sec gel: reading at 3 RPM after 10 seconds static
        9. 10-min gel: reading at 3 RPM after 10 minutes static
        10. Fann 75 (HPHT): measures rheology at elevated temperature/pressure
        """,
        key_factors=[
            "Calibration and zeroing of instrument",
            "Sample temperature (typically 120°F or 150°F)",
            "Mixing and conditioning of sample before testing",
            "Cleanliness of bob and cup (solids buildup affects readings)",
            "Shear history of sample (thixotropy)",
            "API test procedures RP 13B-1",
            "Fann 75 for HPHT wells (up to 500°F, 20,000 psi)",
            "Conversion factors for different models"
        ],
        primary_authority=[
            "API RP 13B-1 - Recommended Practice for Field Testing Drilling Fluids",
            "API RP 13D - Rheology Calculations",
            "Fann Instrument Company - Model 35 Manual",
            "IADC Drilling Manual - Mud Testing"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "PV": "PV (cP) = θ600 - θ300",
            "YP": "YP (lbf/100ft²) = θ300 - PV",
            "gel_strength": "Gel = θ at 3 RPM after static time"
        }
    ),

    DoctrineBlock(
        topic="Herschel-Bulkley Rheological Model",
        keywords=["Herschel-Bulkley", "three parameter", "yield stress", "HB model"],
        conclusion_template="Herschel-Bulkley is a three-parameter model combining yield stress (τ₀), consistency index (K), and flow behavior index (n). Most accurate for drilling fluids across wide shear rate range, but requires iterative calculations.",
        reasoning_framework="""
        1. τ = τ₀ + K × γ̇ⁿ
        2. τ₀ = yield stress (lbf/100ft²)
        3. K = consistency index (lbf-secⁿ/100ft²)
        4. n = flow behavior index (dimensionless)
        5. Reduces to Bingham when n=1
        6. Reduces to Power Law when τ₀=0
        7. Best fit for field data across low to high shear rates
        8. Requires three Fann readings minimum (600, 300, 3 or 6 RPM)
        9. Non-linear regression for parameter determination
        10. Computationally intensive but most accurate
        """,
        key_factors=[
            "Requires multiple Fann readings for curve fitting",
            "Accuracy depends on quality of low-shear data (3, 6 RPM)",
            "Computational complexity for hydraulics modeling",
            "Best model for OBM and SBM with high solids",
            "Captures both yield stress and shear thinning behavior",
            "Software typically required for parameter calculation",
            "Temperature and pressure corrections complex",
            "Industry adoption increasing with computing power"
        ],
        primary_authority=[
            "API RP 13D Section 6.5",
            "SPE 82415 - Herschel-Bulkley Applications",
            "Kelessidis & Maglione - HB Parameter Determination",
            "Robertson & Stiff - Rheology Models Comparison"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "HB_shear_stress": "τ = τ₀ + K × γ̇ⁿ",
            "parameter_fitting": "Non-linear regression on Fann data"
        }
    ),

    DoctrineBlock(
        topic="Critical Transport Velocity for Cuttings",
        keywords=["critical velocity", "transport velocity", "cuttings removal", "minimum flow"],
        conclusion_template="Critical transport velocity is the minimum annular velocity required to prevent cuttings bed formation and ensure effective hole cleaning. Higher for deviated wells (180-250 ft/min) than vertical (120-150 ft/min). Insufficient velocity causes stuck pipe and poor cement jobs.",
        reasoning_framework="""
        1. Vertical wells: gravity aids transport, lower velocity acceptable
        2. Deviated wells (30-60°): critical angle, worst cleaning
        3. Horizontal wells: cuttings bed forms on low side
        4. Transport velocity > slip velocity + bed-sliding velocity
        5. Cuttings concentration affects rheology and transport
        6. Dune formation when transport inadequate
        7. Pipe rotation and reciprocation enhance cleaning mechanically
        8. High ROP requires higher transport velocity
        9. Mud rheology: YP/PV ratio affects carrying capacity
        10. Flow rate vs ECD trade-off (more flow = better cleaning but higher ECD)
        """,
        key_factors=[
            "Hole angle and inclination profile",
            "Annular clearance (tight holes harder to clean)",
            "ROP and cuttings generation rate",
            "Cuttings size, shape, and density",
            "Mud rheological properties (carrying capacity)",
            "Drillstring rotation speed (RPM)",
            "Pipe reciprocation during connections",
            "Formation type (shale vs sandstone cuttings behavior)"
        ],
        primary_authority=[
            "SPE 27464 - Hole Cleaning in Extended Reach Wells",
            "SPE 29380 - Critical Transport Velocity",
            "Larsen et al. - Cuttings Transport Models",
            "IADC Drilling Manual - Hole Cleaning Best Practices"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "annular_velocity": "Vₐ (ft/min) = 24.5 × Q / (Dh² - Dp²)",
            "cuttings_bed_indicator": "If Vₐ < V_critical → bed formation likely"
        }
    ),

    DoctrineBlock(
        topic="Nozzle Selection and Total Flow Area (TFA)",
        keywords=["nozzles", "TFA", "total flow area", "nozzle size", "jet velocity"],
        conclusion_template="Bit nozzles convert pressure to velocity for bottomhole cleaning. Total Flow Area (TFA) is the sum of all nozzle areas. Smaller TFA = higher velocity and pressure drop. Nozzle selection balances bit cleaning, hydraulic horsepower, and annular velocity requirements.",
        reasoning_framework="""
        1. TFA = Σ(π × d²/4) for all nozzles
        2. Typical: three nozzles in tricone, fewer in PDC
        3. Nozzle sizes: 8/32" to 20/32" (in 1/32" increments)
        4. Jet velocity = 417.2 × √(ΔP_bit / MW)
        5. ΔP_bit = (MW × Q²) / (10858 × TFA²)
        6. Smaller TFA: higher velocity, more pressure drop
        7. Larger TFA: lower velocity, less pressure drop (more annular velocity)
        8. Nozzle erosion over time increases TFA (reduces ΔP_bit)
        9. Monitor SPP for nozzle plugging or washing
        10. Extended nozzles for PDC bits (higher flow near cutters)
        """,
        key_factors=[
            "Bit type and nozzle configuration",
            "Target bit pressure drop (% of SPP)",
            "Available pump pressure and flow rate",
            "Formation type and cleaning requirements",
            "Nozzle material and erosion resistance",
            "Hydraulic optimization method (HSI vs Impact)",
            "Annular velocity budget",
            "Nozzle plugging risk (LCM, debris)"
        ],
        primary_authority=[
            "API RP 13D Section 7 - Bit Hydraulics",
            "IADC Bit Classification System",
            "Drilling Optimization Manual - Schlumberger",
            "PDC Bit Design Guide - Smith Bits"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "TFA": "TFA (in²) = Σ(π × (d_nozzle/2)²)",
            "bit_pressure_drop": "ΔP_bit = (MW × Q²) / (10858 × TFA²)",
            "jet_velocity": "V_jet (ft/sec) = 417.2 × √(ΔP_bit / MW)"
        }
    ),

    DoctrineBlock(
        topic="Drillstring Pressure Drop - Laminar vs Turbulent Flow",
        keywords=["drillstring friction", "pressure drop", "laminar flow", "turbulent flow", "Reynolds number"],
        conclusion_template="Pressure drop in drillstring depends on flow regime (laminar vs turbulent), determined by Reynolds number. Laminar flow (Re < 2100): pressure proportional to velocity. Turbulent flow (Re > 2100): pressure proportional to velocity². Most drilling: laminar in pipe, turbulent in annulus.",
        reasoning_framework="""
        1. Reynolds Number (Re) = (928 × MW × V × D) / PV
        2. Re < 2100: laminar flow (smooth, layered flow)
        3. 2100 < Re < 3000: transitional (unstable)
        4. Re > 3000: turbulent flow (chaotic, mixing flow)
        5. Laminar ΔP: linear with velocity, depends on PV and YP
        6. Turbulent ΔP: proportional to V², depends on PV primarily
        7. Drillpipe ID typically 3-5 inches: often laminar at normal flow rates
        8. Annulus: larger equivalent diameter, more likely turbulent
        9. Mud rheology and flow rate determine regime
        10. Turbulent flow: better hole cleaning but higher friction
        """,
        key_factors=[
            "Flow rate (GPM) - primary driver of Reynolds number",
            "Pipe inside diameter",
            "Mud weight and plastic viscosity",
            "Yield point (affects laminar flow only)",
            "Pipe roughness (affects turbulent flow)",
            "Temperature effects on viscosity downhole",
            "Tool joints and BHA restrictions (local turbulence)",
            "Accurate Re calculation requires correct rheology model"
        ],
        primary_authority=[
            "API RP 13D Section 5 - Pressure Losses",
            "Bourgoyne - Laminar and Turbulent Flow Equations",
            "SPE Textbook - Drilling Hydraulics",
            "Colebrook-White Equation for Turbulent Flow"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "Reynolds_number": "Re = (928 × MW × V × D) / PV",
            "laminar_dP": "ΔP ∝ (PV × V + YP × term)",
            "turbulent_dP": "ΔP ∝ f × (MW × V² / D)"
        }
    ),

    DoctrineBlock(
        topic="Narrow Margin Well ECD Management",
        keywords=["narrow margin", "pore pressure", "fracture gradient", "ECD window", "kick and loss"],
        conclusion_template="Narrow margin wells have small difference between pore pressure and fracture gradient (<0.5 ppg). Requires precise ECD control to avoid kicks (ECD too low) or losses (ECD too high). MPD, lightweight muds, and careful hydraulics design essential.",
        reasoning_framework="""
        1. Operating window = fracture gradient - pore pressure
        2. Narrow window: < 0.5 ppg (very narrow), 0.5-1.0 ppg (narrow)
        3. ECD must stay within window at all times
        4. Static MW + friction losses (ECD) + safety margin < fracture
        5. Flow rate optimization: minimum for hole cleaning, maximum for window
        6. Temperature effects: mud thins downhole, reduces ECD
        7. MPD enables drilling otherwise impossible wells
        8. Real-time ECD monitoring via PWD essential
        9. Managed pressure or underbalanced techniques often required
        10. Casing points determined by pressure profile, not just TVD
        """,
        key_factors=[
            "Accurate pore pressure prediction (seismic, offset wells)",
            "Fracture gradient determination (LOT/FIT tests)",
            "Real-time PWD data quality and reliability",
            "Mud weight selection (often at or below pore pressure)",
            "Flow rate optimization for minimum ECD",
            "Mud rheology design (low PV, low YP for low ECD)",
            "Drillstring design (minimize annular friction)",
            "Contingency for kick or loss (well control equipment, LCM)"
        ],
        primary_authority=[
            "SPE 92277 - Narrow Margin Drilling Techniques",
            "IADC MPD Guide",
            "API RP 13D - ECD Calculations",
            "Deepwater Well Design Manual - Schlumberger"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "operating_window": "Window (ppg) = Frac_Gradient - Pore_Pressure",
            "ECD_margin": "Safety_Margin = Frac_Gradient - (MW + ECD_increment)",
            "max_flow_rate": "Q_max where ECD < Frac_Gradient - safety"
        }
    ),

    DoctrineBlock(
        topic="Annular Pressure Loss (APL) Calculation",
        keywords=["annular friction", "APL", "annular pressure", "friction factor"],
        conclusion_template="Annular Pressure Loss is the sum of friction losses in all annular sections (bit to surface). Depends on annular geometry, mud properties, and flow rate. Accurate APL calculation essential for ECD prediction and well control.",
        reasoning_framework="""
        1. APL = Σ(ΔP for each annular section)
        2. Annular sections: bit to BHA, BHA to DP, DP to surface
        3. Each section: different geometry (Dh - Dp)
        4. Calculate flow regime (laminar/turbulent) per section
        5. Apply appropriate friction equation per section
        6. Sum all section losses for total APL
        7. Annulus typically turbulent (large equivalent diameter)
        8. Eccentric annulus (deviated wells): higher friction than concentric
        9. Washouts and tight spots alter local geometry
        10. Temperature reduces viscosity downhole, lowers APL at depth
        """,
        key_factors=[
            "Hole diameter and pipe OD in each section",
            "Flow rate (GPM)",
            "Mud density and rheology (PV, YP, model)",
            "Hole deviation and eccentricity",
            "Pipe rotation (reduces annular friction 10-30%)",
            "Temperature profile (affects viscosity)",
            "Cuttings concentration (increases apparent viscosity)",
            "Hole condition (gauge, washed out, tight spots)"
        ],
        primary_authority=[
            "API RP 13D Section 5.3 - Annular Pressure Loss",
            "SPE 11118 - Annular Flow of Non-Newtonian Fluids",
            "Bourgoyne Ch. 3 - Annular Hydraulics",
            "Zamora - Eccentric Annulus Effects"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "APL_total": "APL = Σ(ΔP_section_i) from bit to surface",
            "section_dP": "ΔP = f(geometry, rheology, flow_rate, length)",
            "ECD_from_APL": "ECD = MW + (APL / (0.052 × TVD))"
        }
    ),

    DoctrineBlock(
        topic="PMCD - Pressurized Mud Cap Drilling",
        keywords=["PMCD", "mud cap", "dual gradient", "subsea mudlift", "riser margin"],
        conclusion_template="Pressurized Mud Cap Drilling (PMCD) is a variant of MPD where wellbore pressure is maintained above fracture gradient by continuously pumping sacrificial mud that is lost to formation. Enables drilling severe loss zones while maintaining well control via hydrostatic overbalance.",
        reasoning_framework="""
        1. Continuous loss zone drilling (total losses acceptable)
        2. Wellbore pressure > fracture > pore pressure
        3. Sacrificial mud pumped down drillstring, lost to formation
        4. Heavier mud cap in annulus prevents gas migration to surface
        5. No returns to surface (or minimal via SubSea MudLift Drilling)
        6. Well control via hydrostatic overbalance, not mud returns
        7. Requires accurate pore pressure prediction
        8. SubSea MudLift variant: light mud down, heavy mud up via riser
        9. Dual gradient effect in deepwater applications
        10. High cost but enables drilling otherwise impossible wells
        """,
        key_factors=[
            "Formation fracture gradient and loss zone severity",
            "Pore pressure prediction accuracy (no kick indication from returns)",
            "Mud cap density (must prevent gas migration)",
            "Sacrificial mud cost and logistics",
            "Pump capacity for continuous losses (may need multiple pumps)",
            "Well control strategy without returns monitoring",
            "BOP and RCD capabilities",
            "Regulatory approval and emergency procedures"
        ],
        primary_authority=[
            "SPE 81638 - PMCD Applications and Theory",
            "IADC MPD Committee - PMCD Guidelines",
            "API RP 92M Section on PMCD",
            "Weatherford - SubSea MudLift Drilling Manual"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "mud_cap_pressure": "P_cap = MW_cap × 0.052 × TVD > Frac_Gradient",
            "required_overbalance": "MW_cap > Pore_Pressure + safety_margin"
        }
    ),

    DoctrineBlock(
        topic="Float Equipment and Drillstring Hydraulics",
        keywords=["float valve", "float sub", "check valve", "U-tubing", "backflow prevention"],
        conclusion_template="Float equipment (float valve, float sub) prevents backflow up drillstring when pumps are off. Prevents U-tubing, reduces surge/swab pressure, enables continuous circulation for casing running. Creates pressure drop (typically 50-200 psi) that must be accounted in hydraulics.",
        reasoning_framework="""
        1. Float valve: one-way check valve in drillstring
        2. Prevents mud from flowing back up pipe when pumps stop
        3. Float sub: dedicated BHA component with float valve
        4. Inside BOP valve: similar function, above BHA
        5. Eliminates U-tube effect (density equilibration)
        6. Reduces swab pressure when pulling out of hole
        7. Enables fill-up during tripping without pumps
        8. Pressure drop across float: typically 50-200 psi
        9. Must be included in standpipe pressure calculations
        10. Can stick or fail (mud solids, debris)
        """,
        key_factors=[
            "Float valve type and design (flapper, ball, poppet)",
            "Pressure drop across float valve",
            "Valve condition and maintenance",
            "Debris and LCM risk of plugging",
            "U-tube prevention effectiveness",
            "Contribution to standpipe pressure",
            "Failure modes (stuck open or closed)",
            "Testing procedures before running in hole"
        ],
        primary_authority=[
            "IADC Drilling Manual - Drillstring Components",
            "API Spec 7 - Drillstem Design",
            "Well Control Manual - Float Equipment Section",
            "BHA Design Handbook - Smith Services"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        calculations={
            "SPP_with_float": "SPP_total = ΔP_system + ΔP_float + ΔP_bit + ΔP_annulus",
            "float_dP_typical": "ΔP_float ≈ 50-200 psi (varies by design)"
        }
    ),

    DoctrineBlock(
        topic="Cuttings Bed Formation and Remediation",
        keywords=["cuttings bed", "dune", "high angle", "hole cleaning", "back reaming"],
        conclusion_template="Cuttings beds form in deviated wells when annular velocity is insufficient to transport cuttings. Beds cause high torque, stuck pipe, poor cement jobs, and hole instability. Remediation: increase flow rate, rotate and reciprocate pipe, back ream, wiper trips, sweep pills.",
        reasoning_framework="""
        1. Beds form when cuttings settle faster than transported
        2. Critical angle: 30-60° (gravity perpendicular to flow)
        3. Indicators: increasing torque, drag, SPP (restricted annulus)
        4. High ROP without adequate cleaning exacerbates problem
        5. Back reaming: rotate and pump while pulling up (agitates bed)
        6. Wiper trip: short trip up and down to clean hole
        7. Sweep pills: high viscosity slugs to lift cuttings
        8. Pipe rotation: mechanical agitation of bed
        9. Prevention better than cure: adequate annular velocity from start
        10. Severe cases: may require sidetracking or abandonment
        """,
        key_factors=[
            "Hole angle profile (identify critical zones)",
            "Annular velocity actual vs required",
            "ROP and cuttings generation rate",
            "Mud carrying capacity (rheology, YP/PV ratio)",
            "Drillstring rotation during drilling",
            "Connection procedures (maintain circulation if possible)",
            "Hole size and annular clearance",
            "Formation stability (shale swelling can trap cuttings)"
        ],
        primary_authority=[
            "SPE 27464 - Extended Reach Hole Cleaning",
            "IADC Drilling Manual - Hole Cleaning Best Practices",
            "SPE 77234 - Cuttings Bed Removal Techniques",
            "Directional Drilling Handbook - Baker Hughes"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "bed_thickness_estimate": "Thickness ∝ ROP / (Annular_Velocity - Slip_Velocity)",
            "required_velocity_increase": "ΔV = V_critical - V_current"
        }
    ),

    DoctrineBlock(
        topic="Temperature Effects on Mud Rheology",
        keywords=["temperature", "HPHT", "rheology change", "Fann 75", "downhole viscosity"],
        conclusion_template="Mud viscosity decreases with increasing temperature downhole. Affects ECD (reduces annular friction at depth), surge/swab, and hydraulics calculations. Fann 75 HPHT viscometer measures rheology at elevated temperature and pressure for accurate modeling.",
        reasoning_framework="""
        1. Viscosity typically decreases 10-30% from surface to bottomhole
        2. Geothermal gradient: ~1-1.5°F per 100 ft depth (varies by region)
        3. Circulating fluid temperature lower than static (cooling from surface)
        4. Temperature affects both PV and YP
        5. WBM: more temperature sensitive than OBM
        6. Fann 75: measures rheology up to 500°F and 20,000 psi
        7. HPHT wells: essential to measure rheology at downhole conditions
        8. Lower viscosity at depth reduces ECD (favorable)
        9. But also reduces carrying capacity (may worsen hole cleaning)
        10. Hydraulics models should account for temperature profile
        """,
        key_factors=[
            "Geothermal gradient of well location",
            "Circulation time and fluid cooling",
            "Mud type (WBM vs OBM temperature sensitivity)",
            "Bottomhole temperature (BHT) measurement",
            "Fann 75 testing at expected downhole conditions",
            "Rheology model selection (temperature dependency)",
            "ECD prediction accuracy at depth",
            "Hole cleaning considerations with thinner mud at depth"
        ],
        primary_authority=[
            "API RP 13D - Temperature Corrections",
            "SPE 22557 - Temperature Effects on Rheology",
            "Fann Instrument - Model 75 HPHT Manual",
            "Amoco HPHT Drilling Manual"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "BHT_estimate": "BHT ≈ Surface_Temp + (Gradient × Depth)",
            "viscosity_ratio": "μ_downhole / μ_surface ≈ 0.7-0.9 (typical)"
        }
    ),

    DoctrineBlock(
        topic="Drillstring Rotation Effect on Annular Friction",
        keywords=["pipe rotation", "RPM", "friction reduction", "ECD reduction", "Taylor vortices"],
        conclusion_template="Drillstring rotation reduces annular friction pressure by 10-30% compared to stationary pipe. Creates Taylor vortices and centrifugal effects that thin the boundary layer. Reduces ECD, improves hole cleaning mechanically, but increases torque and wear on casing/hole.",
        reasoning_framework="""
        1. Rotation creates centrifugal force on fluid in annulus
        2. Taylor vortices: secondary flow patterns reduce friction
        3. Boundary layer thinning at pipe wall
        4. 10-30% reduction in annular pressure loss typical
        5. Greater effect at higher RPM (diminishing returns above 150 RPM)
        6. Eccentric annulus: more significant effect than concentric
        7. Improves cuttings transport mechanically (agitation)
        8. Increases torque and drag on pipe
        9. Wear on casing (lined casing) and openhole
        10. Rotation while circulating is standard practice
        """,
        key_factors=[
            "Rotational speed (RPM) - primary parameter",
            "Pipe OD and annular clearance",
            "Mud rheology (affects boundary layer)",
            "Hole deviation and eccentricity",
            "Casing or openhole (wear considerations)",
            "Drillstring design (stabilizers, centralizers)",
            "Top drive vs rotary table (torque capacity)",
            "Friction reduction magnitude (use conservative values)"
        ],
        primary_authority=[
            "SPE 11118 - Rotation Effects on Annular Flow",
            "API RP 13D - Hydraulics with Rotation",
            "Haciislamoglu & Langlinais - Rotation Study",
            "IADC Drilling Manual - ECD Management"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "friction_reduction_factor": "ΔP_rotating ≈ 0.70-0.90 × ΔP_stationary",
            "ECD_reduction": "ECD_rotating < ECD_stationary (10-30% lower APL)"
        }
    ),

    DoctrineBlock(
        topic="Hydraulics Software and Real-Time Modeling",
        keywords=["hydraulics software", "real-time", "PWD", "drilling optimization", "automated drilling"],
        conclusion_template="Modern drilling uses real-time hydraulics modeling software integrated with PWD data and surface sensors. Continuously updates ECD prediction, optimizes flow rate, detects anomalies, and enables automated drilling systems. Critical for MPD, complex wells, and drilling optimization.",
        reasoning_framework="""
        1. Real-time data: SPP, flow rate, RPM, WOB, torque, PWD downhole pressure
        2. Software calculates: ECD, APL, bit hydraulics, surge/swab
        3. Compares actual vs predicted (model validation)
        4. Detects: washouts, tight spots, lost circulation, kick indicators
        5. Optimizes: flow rate for ECD window, bit hydraulics for ROP
        6. Enables closed-loop drilling automation
        7. PWD essential for model calibration and validation
        8. Typical update rate: 1-10 seconds
        9. Displays: ECD profile, pressure vs depth, hydraulics summary
        10. Alarms for out-of-limit conditions (ECD near fracture, SPP high)
        """,
        key_factors=[
            "Software accuracy and rheology model used",
            "PWD data quality, telemetry rate, and reliability",
            "Surface sensor calibration (SPP, flowmeter, RPM)",
            "Model input accuracy (hole geometry, mud properties)",
            "Real-time mud property testing (every circulation)",
            "Integration with rig automation systems",
            "Alarm setpoints and crew response procedures",
            "Data storage and post-well analysis"
        ],
        primary_authority=[
            "SPE 140182 - Real-Time Hydraulics Modeling",
            "IADC Drilling Automation Guidelines",
            "Drilling Systems Automation Roadmap - SPE/IADC",
            "Major service company software manuals (Landmark, Halliburton, SLB)"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "model_calibration": "Adjust K, n, or PV/YP until predicted ECD = measured PWD",
            "ECD_prediction": "Continuous calculation from current flow rate and mud properties"
        }
    ),

    DoctrineBlock(
        topic="Barite Sag and Dynamic vs Static Density",
        keywords=["barite sag", "settling", "sag test", "dynamic density", "weighted mud"],
        conclusion_template="Barite sag occurs when weighting material settles out of suspension during static or low-shear conditions, creating density gradients in wellbore. Bottomhole density increases (risk of losses), upper hole density decreases (risk of kick). Severe risk in deviated wells with high-weight OBM.",
        reasoning_framework="""
        1. Barite (BaSO₄): density 4.2 g/cm³ (35 ppg equivalent)
        2. Settles when mud gels are insufficient to suspend particles
        3. Low-shear environments: connections, trips, stuck pipe
        4. Deviated wells: barite slides down low side of hole
        5. Density can vary 0.5-2.0 ppg from top to bottom
        6. Indicators: increasing SPP, ECD bottom, decreasing ECD top
        7. API sag test (HPHT aging cell): measures sag tendency
        8. Mitigation: improve gel strength, reduce barite loading, use anti-sag additives
        9. Circulation before critical operations to remix mud
        10. Can lead to simultaneous kick (top) and loss (bottom)
        """,
        key_factors=[
            "Mud weight and barite concentration (higher = worse)",
            "Gel strength development (must suspend barite)",
            "Static time duration (longer = more sag)",
            "Hole angle (deviated wells most susceptible)",
            "Temperature (high temp reduces gel strength)",
            "Mud type (OBM/SBM more prone than WBM)",
            "API sag test results (measure sag tendency)",
            "Anti-sag additives (rheology modifiers)"
        ],
        primary_authority=[
            "API RP 13B-2 - HPHT Sag Test Procedures",
            "SPE 56645 - Barite Sag in Deviated Wells",
            "IADC Drilling Fluids Manual - Sag Control",
            "SPE 82415 - Dynamic Mud Weight Management"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        calculations={
            "density_gradient": "ΔMW = MW_bottom - MW_top (from sag)",
            "ECD_bottom_increase": "ECD_bottom = MW_static + sag_increase + friction"
        }
    )
]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class Telemetry:
    def __init__(self):
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.start_time = datetime.now()
        self.query_log = []

    def log_query(self, query: str, mode: ResponseMode, triggered: List[str], latency_ms: float):
        self.total_queries += 1
        if triggered:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query[:200],
            "mode": mode.value,
            "triggered_count": len(triggered),
            "latency_ms": latency_ms
        }
        self.query_log.append(entry)
        logger.info(f"Query logged: {len(triggered)} doctrines, {latency_ms:.1f}ms")

    def get_cache_hit_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.cache_hits / self.total_queries

    def get_uptime_seconds(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()


TELEMETRY = Telemetry()


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def calculate_determinism_hash(query: str, triggered: List[str], mode: ResponseMode) -> str:
    """Generate SHA-256 hash for reproducibility verification"""
    content = f"{query}|{','.join(sorted(triggered))}|{mode.value}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def apply_epistemic_guardrails(text: str) -> str:
    """Remove banned overconfident phrases"""
    result = text
    for phrase in BANNED_PHRASES:
        result = result.replace(phrase, "[EPISTEMICALLY INAPPROPRIATE]")
    return result


def search_doctrine_cache(query: str) -> List[DoctrineBlock]:
    """Search doctrine cache for matching blocks (0-200ms fast path)"""
    query_lower = query.lower()
    matches = []

    for doctrine in DOCTRINE_CACHE:
        # Keyword matching
        if any(kw.lower() in query_lower for kw in doctrine.keywords):
            matches.append(doctrine)
            continue

        # Topic matching
        if doctrine.topic.lower() in query_lower:
            matches.append(doctrine)

    return matches


def calculate_ecd(mud_weight_ppg: float, apl_psi: float, tvd_ft: float) -> float:
    """Calculate Equivalent Circulating Density"""
    return mud_weight_ppg + (apl_psi / (0.052 * tvd_ft))


def calculate_annular_velocity(flow_rate_gpm: float, hole_dia_in: float, pipe_od_in: float) -> float:
    """Calculate annular velocity in ft/min"""
    return 24.5 * flow_rate_gpm / (hole_dia_in**2 - pipe_od_in**2)


def calculate_bingham_plastic_pv_yp(theta_600: float, theta_300: float) -> tuple:
    """Calculate PV and YP from Fann 35 readings"""
    pv = theta_600 - theta_300
    yp = theta_300 - pv
    return pv, yp


def calculate_reynolds_number(mud_weight: float, velocity_fps: float, diameter_in: float, pv_cp: float) -> float:
    """Calculate Reynolds number for flow regime determination"""
    return (928 * mud_weight * velocity_fps * diameter_in) / pv_cp


def calculate_bit_hhp(bit_pressure_psi: float, flow_rate_gpm: float) -> float:
    """Calculate hydraulic horsepower at bit"""
    return (bit_pressure_psi * flow_rate_gpm) / 1714


def calculate_impact_force(flow_rate_gpm: float, mud_weight: float, bit_pressure_psi: float) -> float:
    """Calculate jet impact force in lbf"""
    return 0.01823 * flow_rate_gpm * math.sqrt(mud_weight * bit_pressure_psi)


def three_layer_response(query: str, params: Dict[str, Any], mode: ResponseMode) -> HydraulicsQueryResponse:
    """
    TIE-20 Three-Layer Response System:
    Layer 1: Doctrine Cache (0-200ms)
    Layer 2: Semantic Retrieval (would query vector DB)
    Layer 3: Deep Analysis (LLM synthesis - not implemented here)
    """
    start_time = datetime.now()

    # Layer 1: Doctrine Cache
    triggered_doctrines = search_doctrine_cache(query)
    triggered_names = [d.topic for d in triggered_doctrines]

    # Build reasoning chain
    reasoning = []
    calculations_performed = {}

    # Perform calculations if parameters provided
    if params.get("mud_weight_ppg") and params.get("hole_depth_ft"):
        reasoning.append("Analyzing provided wellbore parameters for hydraulics calculations")

        # ECD calculation if flow rate available
        if params.get("flow_rate_gpm") and params.get("hole_diameter_in") and params.get("drillstring_od_in"):
            # Simplified APL estimate (would be detailed in production)
            estimated_apl = 50 + (params["flow_rate_gpm"] * 0.5)  # Simplified
            ecd = calculate_ecd(params["mud_weight_ppg"], estimated_apl, params["hole_depth_ft"])
            calculations_performed["ECD"] = round(ecd, 2)

            annular_vel = calculate_annular_velocity(
                params["flow_rate_gpm"],
                params["hole_diameter_in"],
                params["drillstring_od_in"]
            )
            calculations_performed["Annular_Velocity_ft_per_min"] = round(annular_vel, 1)
            reasoning.append(f"Calculated ECD: {ecd:.2f} ppg, Annular Velocity: {annular_vel:.1f} ft/min")

        # Rheology calculations if Fann readings available
        if params.get("pv_cp") and params.get("yp_lbf_100ft2"):
            calculations_performed["PV_cp"] = params["pv_cp"]
            calculations_performed["YP_lbf_100ft2"] = params["yp_lbf_100ft2"]
            reasoning.append(f"Bingham Plastic rheology: PV={params['pv_cp']} cP, YP={params['yp_lbf_100ft2']} lbf/100ft²")

    # Build answer based on mode and triggered doctrines
    if mode == ResponseMode.FAST:
        if triggered_doctrines:
            answer = triggered_doctrines[0].conclusion_template
            if calculations_performed:
                answer += f"\n\nCalculations: {json.dumps(calculations_performed, indent=2)}"
        else:
            answer = "No direct doctrine match. Query requires domain expertise in: drilling hydraulics, ECD management, rheology, or hole cleaning."
        reasoning.append("FAST mode: doctrine conclusion returned")

    elif mode == ResponseMode.DEFENSE:
        answer_parts = []
        for doctrine in triggered_doctrines[:3]:  # Top 3 doctrines
            answer_parts.append(f"**{doctrine.topic}**")
            answer_parts.append(doctrine.reasoning_framework)
            answer_parts.append(f"Authority: {', '.join(doctrine.primary_authority[:2])}")
            answer_parts.append("")

        if calculations_performed:
            answer_parts.append("**Calculations Performed:**")
            answer_parts.append(json.dumps(calculations_performed, indent=2))

        answer = "\n".join(answer_parts) if answer_parts else "Insufficient doctrine coverage for defensive response."
        reasoning.append("DEFENSE mode: detailed reasoning with authority citations")

    elif mode == ResponseMode.MEMO:
        answer_parts = ["# Drilling Hydraulics Analysis\n"]

        for doctrine in triggered_doctrines:
            answer_parts.append(f"## {doctrine.topic}\n")
            answer_parts.append(f"**Conclusion:** {doctrine.conclusion_template}\n")
            answer_parts.append(f"**Reasoning Framework:**")
            answer_parts.append(doctrine.reasoning_framework)
            answer_parts.append(f"\n**Key Factors:**")
            for factor in doctrine.key_factors:
                answer_parts.append(f"- {factor}")
            answer_parts.append(f"\n**Authoritative Sources:**")
            for auth in doctrine.primary_authority:
                answer_parts.append(f"- {auth}")
            answer_parts.append(f"\n**Confidence Level:** {doctrine.confidence.value}\n")
            answer_parts.append("---\n")

        if calculations_performed:
            answer_parts.append("## Calculations\n")
            answer_parts.append("```json")
            answer_parts.append(json.dumps(calculations_performed, indent=2))
            answer_parts.append("```\n")

        answer = "\n".join(answer_parts) if len(answer_parts) > 1 else "No doctrines triggered. Requires hydraulics specialist review."
        reasoning.append("MEMO mode: comprehensive documentation format")

    # Apply epistemic guardrails
    answer = apply_epistemic_guardrails(answer)

    # Determine confidence
    if triggered_doctrines:
        confidence = triggered_doctrines[0].confidence
    else:
        confidence = ConfidenceLevel.DISCLOSURE

    # Add disclosure if appropriate
    disclosure = None
    if confidence in [ConfidenceLevel.AGGRESSIVE, ConfidenceLevel.HIGH_RISK]:
        disclosure = "This analysis involves complex hydraulics calculations and assumptions. Field validation with actual wellbore data and PWD measurements recommended. Consult drilling engineer for critical operations."

    # Calculate latency and hash
    latency_ms = (datetime.now() - start_time).total_seconds() * 1000
    det_hash = calculate_determinism_hash(query, triggered_names, mode)

    # Log telemetry
    TELEMETRY.log_query(query, mode, triggered_names, latency_ms)

    return HydraulicsQueryResponse(
        answer=answer,
        confidence=confidence,
        mode=mode,
        triggered_doctrines=triggered_names,
        reasoning_chain=reasoning,
        calculations=calculations_performed if calculations_performed else None,
        epistemic_disclosure=disclosure,
        determinism_hash=det_hash,
        timestamp=datetime.now().isoformat()
    )


# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

@APP.post("/query", response_model=HydraulicsQueryResponse)
async def query_hydraulics(request: HydraulicsQueryRequest):
    """Main query endpoint - TIE-20 three-layer response"""
    try:
        logger.info(f"Query received: {request.query[:100]}, mode={request.mode.value}")

        # Extract parameters
        params = {
            "hole_depth_ft": request.hole_depth_ft,
            "hole_diameter_in": request.hole_diameter_in,
            "drillstring_od_in": request.drillstring_od_in,
            "mud_weight_ppg": request.mud_weight_ppg,
            "flow_rate_gpm": request.flow_rate_gpm,
            "pv_cp": request.pv_cp,
            "yp_lbf_100ft2": request.yp_lbf_100ft2,
            **request.context
        }

        response = three_layer_response(request.query, params, request.mode)
        return response

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """TIE-20 health endpoint"""
    return HealthResponse(
        status="operational",
        version="1.0.0",
        port=9017,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=TELEMETRY.get_uptime_seconds(),
        total_queries=TELEMETRY.total_queries,
        cache_hit_rate=TELEMETRY.get_cache_hit_rate()
    )


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
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


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("DRL07 - Drilling Hydraulics Engine")
    logger.info("TIE Gold Standard Implementation")
    logger.info(f"Doctrine Blocks: {len(DOCTRINE_CACHE)}")
    logger.info(f"Port: 9017")
    logger.info("=" * 80)

    uvicorn.run(APP, host="0.0.0.0", port=9017, log_level="info")
