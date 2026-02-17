"""
DRL04 - Casing Design & Selection Engine
ECHO OMEGA PRIME - Drilling Engineering Intelligence

TIE Gold Standard: Real casing design expertise for drilling operations.
Covers casing programs, grades, connections, design factors, and API specifications.

Port: 9014
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION & LOGGING
# ============================================================================

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "drl04_casing_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

APP = FastAPI(
    title="DRL04 - Casing Design & Selection Engine",
    version="1.0.0",
    description="TIE Gold Standard drilling engineering intelligence for casing programs"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class IssueCategory(str, Enum):
    STRING_DESIGN = "STRING_DESIGN"
    GRADE_SELECTION = "GRADE_SELECTION"
    CONNECTION_SELECTION = "CONNECTION_SELECTION"
    LOAD_ANALYSIS = "LOAD_ANALYSIS"
    SEAT_SELECTION = "SEAT_SELECTION"
    WEAR_ANALYSIS = "WEAR_ANALYSIS"
    PRESSURE_INTEGRITY = "PRESSURE_INTEGRITY"
    RUNNING_PROCEDURES = "RUNNING_PROCEDURES"
    THERMAL_EFFECTS = "THERMAL_EFFECTS"
    CORROSION_DESIGN = "CORROSION_DESIGN"
    HPHT_DESIGN = "HPHT_DESIGN"
    LINER_DESIGN = "LINER_DESIGN"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    DESIGN = "DESIGN"
    AUDIT = "AUDIT"

BANNED_PHRASES = [
    "always safe", "never fails", "guaranteed", "zero risk",
    "absolutely certain", "no chance of failure", "impossible to fail"
]

API_CASING_GRADES = {
    "H-40": {"yield_psi": 40000, "min_tensile_psi": 60000, "typical_use": "shallow surface casing"},
    "J-55": {"yield_psi": 55000, "min_tensile_psi": 75000, "typical_use": "surface and intermediate strings"},
    "K-55": {"yield_psi": 55000, "min_tensile_psi": 95000, "typical_use": "intermediate and production casing"},
    "N-80": {"yield_psi": 80000, "min_tensile_psi": 100000, "typical_use": "production casing, moderate depths"},
    "L-80": {"yield_psi": 80000, "min_tensile_psi": 95000, "typical_use": "sour service environments"},
    "C-90": {"yield_psi": 90000, "min_tensile_psi": 100000, "typical_use": "deep intermediate strings"},
    "T-95": {"yield_psi": 95000, "min_tensile_psi": 105000, "typical_use": "deep production casing"},
    "P-110": {"yield_psi": 110000, "min_tensile_psi": 125000, "typical_use": "HPHT production strings"},
    "Q-125": {"yield_psi": 125000, "min_tensile_psi": 135000, "typical_use": "ultra-deep HPHT wells"}
}

CONNECTION_TYPES = {
    "STC": "Short Thread and Coupling - API round thread, lowest cost",
    "LTC": "Long Thread and Coupling - API round thread, better tensile",
    "BTC": "Buttress Thread and Coupling - API buttress thread, best tensile for API",
    "VAM": "Premium connection - metal-to-metal seal, gas-tight",
    "TenarisHydril": "Premium connection - wedge thread, high torque capacity",
    "PTC": "Premium Threaded Connection - various manufacturers"
}

DESIGN_FACTORS = {
    "burst": {"minimum": 1.0, "recommended": 1.1, "conservative": 1.25},
    "collapse": {"minimum": 1.0, "recommended": 1.125, "conservative": 1.25},
    "tension": {"minimum": 1.3, "recommended": 1.6, "conservative": 1.8}
}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: str
    adversary_position: Optional[str]
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str

class CasingQuery(BaseModel):
    question: str
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None
    depth_ft: Optional[float] = None
    grade: Optional[str] = None
    pressure_psi: Optional[float] = None

class CasingResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    response_time_ms: float
    determinism_hash: str
    zone: AnalysisZone
    fragility_score: float
    audit_trail: List[str]

class HealthStatus(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    cache_size: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE CACHE - 25+ REAL CASING DESIGN BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="conductor_casing_design",
        keywords=["conductor", "structural casing", "20 inch", "24 inch", "30 inch", "36 inch", "shallow", "surface protection"],
        conclusion_template=[
            "Conductor casing (typically 16-36 inch diameter) is the first string set to protect shallow aquifers and provide structural support for subsequent drilling operations.",
            "Design is governed by soil mechanics, not pressure containment, with minimum penetration per regulatory requirements (e.g., 50-100 feet below surface).",
            "Drive pipe or drilled-and-cemented conductor depends on soil conditions and rig capabilities."
        ],
        reasoning_framework="""
        Conductor casing serves structural and environmental protection functions:
        1. STRUCTURAL: Support for wellhead equipment and subsequent casing strings
        2. ENVIRONMENTAL: Protect freshwater aquifers from drilling fluids and hydrocarbons
        3. SHALLOW HAZARD ISOLATION: Case off unconsolidated formations and shallow gas zones

        Design considerations:
        - Soil bearing capacity and penetration depth (NOT pressure containment)
        - Regulatory minimums (e.g., Texas Railroad Commission: 50 ft below base of usable quality water)
        - Wellhead load analysis: cumulative weight of all subsequent strings + BOP stack
        - Drive-ability: soil resistance vs hammer energy for driven pipe
        - Cement coverage: to surface mandatory in most jurisdictions

        Typical sizes: 20" (common onshore), 30" (offshore), 36" (deep offshore)
        Grades: H-40 or J-55 sufficient (low stress environment)
        Connections: Plain-end welded (driven) or STC/LTC (drilled-and-cemented)
        """,
        key_factors=[
            "Minimum penetration depth per state regulations",
            "Soil bearing capacity and penetration resistance",
            "Cumulative wellhead load from all subsequent strings",
            "Freshwater protection depth (base of usable quality water)",
            "Shallow gas hazard potential",
            "Surface location stability (onshore vs offshore)"
        ],
        primary_authority=[
            "API Bulletin 5C2 - Bulletin on Performance Properties of Casing, Tubing, and Drill Pipe",
            "API RP 10B-2 - Recommended Practice for Testing Well Cements",
            "Texas Railroad Commission Rule 13: Casing, Cementing, Drilling, and Completion Requirements",
            "30 CFR 250.420 - Casing and Cementing Requirements (Offshore)"
        ],
        burden_holder="Operator - must demonstrate adequate protection per regulatory standards",
        adversary_position="Regulator may require deeper conductor if shallow gas or aquifer protection insufficient",
        counter_arguments=[
            "Soil conditions prevent deeper penetration without specialty equipment",
            "Historical offset wells demonstrate adequate protection at shallower depth",
            "Intermediate casing string provides redundant protection",
            "Cementing to surface provides migration barrier regardless of conductor depth"
        ],
        resolution_strategy="Demonstrate compliance with minimum regulatory depth AND protection of all usable quality water zones; offset well data supports proposed design; contingency plan for shallow gas if indicated by seismic or offset experience.",
        entity_scope="All well types: onshore, offshore, vertical, directional",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Design based on explicit regulatory requirements and standard industry practice; soil mechanics govern over pressure analysis.",
        controlling_precedent="API RP 10B-2 and jurisdiction-specific casing regulations (Texas RRC Rule 13, MMS/BOEM regulations offshore)"
    ),

    DoctrineBlock(
        topic="surface_casing_seat_selection",
        keywords=["surface casing", "seat selection", "kick tolerance", "fracture gradient", "pore pressure", "shoe depth"],
        conclusion_template=[
            "Surface casing shoe depth is determined by the deepest depth at which kick tolerance is maintained during subsequent intermediate hole drilling.",
            "Set surface casing below all freshwater zones with margin, and deep enough that fracture gradient at shoe exceeds maximum anticipated pore pressure + kick margin in the next hole section.",
            "Typical setting depths: 1,000-4,000 ft onshore, 2,000-5,000 ft offshore, deeper in HPHT environments."
        ],
        reasoning_framework="""
        Surface casing seat selection is the most critical casing design decision:

        PRIMARY CRITERION: Kick Tolerance
        - During intermediate hole drilling, if influx occurs, must be able to shut in well and circulate out kick without fracturing formation at surface casing shoe
        - Fracture gradient at shoe must exceed: SIDPP (shut-in drillpipe pressure) + hydrostatic of kill mud + safety margin
        - If shoe fractures during well control, lost circulation results in uncontrolled influx (blowout scenario)

        CALCULATION:
        1. Plot pore pressure and fracture gradient vs depth from offset data, seismic, logs
        2. Identify depth where fracture gradient margin is adequate for kick scenario
        3. Ensure all freshwater zones are cased off with margin (typically 100-200 ft below base)
        4. Check against maximum anticipated surface pressure (MASP) for BOP rating

        TYPICAL DEPTHS:
        - Onshore normal pressure: 1,200-2,500 ft (below freshwater, adequate frac gradient)
        - Onshore high pressure: 3,000-4,500 ft (deeper margin for overpressured formations)
        - Offshore Gulf of Mexico: 2,500-4,000 ft (shallow water flow zones)
        - HPHT wells: 5,000-8,000 ft (requires substantial margin for narrow drilling window)

        REGULATORY CONSTRAINTS:
        - Must case off all freshwater (usable quality water per state definition)
        - Must provide adequate well control capacity per blowout prevention requirements
        - Offshore: must case off shallow water flow zones (gas-charged shallow sands)
        """,
        key_factors=[
            "Fracture gradient at proposed shoe depth",
            "Maximum anticipated pore pressure in next hole section",
            "Kick tolerance calculation (gas kick volume, mud weight increase)",
            "Freshwater protection depth (regulatory requirement)",
            "Shallow water flow zones (offshore)",
            "BOP pressure rating vs maximum anticipated surface pressure",
            "Offset well experience and LOT (leak-off test) data"
        ],
        primary_authority=[
            "API RP 53 - Recommended Practice for Blowout Prevention Equipment Systems for Drilling Wells",
            "API RP 92L - Recommended Practice for Evaluation of Remotely Operated Vehicles",
            "IADC Drilling Manual - Well Control Section",
            "SPE 20429 - Casing Seat Selection Using Quantitative Risk Assessment"
        ],
        burden_holder="Operator - must demonstrate adequate kick tolerance margin with engineering calculations",
        adversary_position="Regulator may require deeper surface casing if kick tolerance analysis shows insufficient margin or if shallow hazards present",
        counter_arguments=[
            "Offset wells successfully drilled with shallower surface casing",
            "Formation integrity test (FIT) confirms adequate fracture gradient",
            "BOP rating provides surface pressure margin",
            "Intermediate casing planned to isolate pressure transition zone"
        ],
        resolution_strategy="Quantitative kick tolerance analysis using offset pore pressure and fracture gradient data; demonstrate positive margin (typically 0.5-1.0 ppg equivalent) at proposed shoe depth; contingency plan for intermediate string if pressure transition shallower than anticipated.",
        entity_scope="All well types; particularly critical in HPHT, deepwater, and overpressured basins",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Based on quantitative engineering analysis (kick tolerance calculations) and offset well data; some uncertainty in predrill pore pressure and fracture gradient estimates.",
        controlling_precedent="API RP 53 for well control; jurisdiction-specific casing regulations for freshwater protection"
    ),

    DoctrineBlock(
        topic="casing_grade_selection_burst",
        keywords=["burst", "internal pressure", "grade selection", "API 5CT", "yield strength", "design factor"],
        conclusion_template=[
            "Casing grade for burst resistance is selected such that API internal yield pressure exceeds maximum anticipated internal pressure multiplied by design factor (typically 1.0-1.25).",
            "Burst load cases include: gas kick to surface, full gas column, fracture treatment pressure, and formation pressure communication.",
            "Higher grade steel (N-80, L-80, P-110, Q-125) required for deeper wells, higher pressure, or HPHT environments."
        ],
        reasoning_framework="""
        Burst (internal pressure) is the most common casing failure mode:

        BURST RATING CALCULATION (API 5C2):
        Internal Yield Pressure (psi) = 2 * Yield Strength * (t / OD)
        Where: t = wall thickness, OD = outer diameter

        For premium connections, use manufacturer's published ratings (may exceed API yield)

        DESIGN EQUATION:
        Required Burst Resistance = Max Internal Pressure * Design Factor
        Design Factor: 1.0 (minimum), 1.1 (recommended), 1.25 (HPHT)

        LOAD CASES (select worst case):
        1. GAS KICK TO SURFACE: Full gas column (0.1 psi/ft) to shoe, mud below
        2. FULL EVACUATION: Gas gradient to TD, no mud hydrostatic
        3. STIMULATION: Fracture treatment pressure at perforations
        4. INJECTION: Maximum injection pressure for water/gas injection wells
        5. FORMATION COMMUNICATION: Higher pressure zone communicates to lower zone behind pipe

        GRADE SELECTION LOGIC:
        - H-40: Shallow wells < 3,000 ft, low pressure
        - J-55/K-55: Intermediate depths 3,000-8,000 ft, normal pressure
        - N-80: Deep wells 8,000-12,000 ft, moderate pressure
        - L-80: Sour service (H2S) environments
        - C-90/T-95: Deep wells 12,000-16,000 ft, high pressure
        - P-110: HPHT wells > 15,000 ft, > 10,000 psi
        - Q-125: Ultra-deep HPHT > 20,000 ft, > 15,000 psi

        ADJUSTMENTS:
        - Reduce rating for wear (casing wear from drill pipe rotation)
        - Reduce rating for corrosion (CO2, H2S environments per NACE MR0175)
        - Increase design factor for critical strings (production casing)
        """,
        key_factors=[
            "Maximum anticipated surface pressure (gas kick scenario)",
            "Formation pressure at total depth",
            "Fracture treatment pressure (if completion planned)",
            "Wear percentage from drilling operations",
            "Corrosive environment (CO2, H2S content)",
            "Well temperature (affects yield strength)",
            "Connection type (API vs premium ratings)"
        ],
        primary_authority=[
            "API Specification 5CT - Specification for Casing and Tubing",
            "API Bulletin 5C3 - Formulas and Calculations for Casing, Tubing, Drill Pipe",
            "ISO 10400 - Petroleum and natural gas industries — Formulas and calculations for casing, tubing, drill pipe",
            "NACE MR0175/ISO 15156 - Petroleum and natural gas industries — Materials for use in H2S-containing environments"
        ],
        burden_holder="Operator - must demonstrate casing burst rating exceeds maximum anticipated pressure with design factor",
        adversary_position="Regulator or peer reviewer may challenge load case assumptions or require higher design factor for critical wells",
        counter_arguments=[
            "Offset wells use same grade successfully",
            "BOP pressure rating limits surface pressure below casing rating",
            "Annular pressure monitoring provides early detection",
            "Premium connection provides margin above API rating"
        ],
        resolution_strategy="Conservative load case analysis (worst-case gas kick, full evacuation); apply standard design factors per API guidance; account for wear and corrosion; select next available grade if close to limit.",
        entity_scope="All well types; particularly critical for production casing and HPHT wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Based on API standardized calculations and industry-accepted design factors; uncertainty in maximum pressure scenarios addressed by design factor.",
        controlling_precedent="API Specification 5CT and API Bulletin 5C3 for burst rating calculations"
    ),

    DoctrineBlock(
        topic="casing_grade_selection_collapse",
        keywords=["collapse", "external pressure", "evacuation", "lost circulation", "design factor", "API collapse rating"],
        conclusion_template=[
            "Casing grade for collapse resistance is selected such that API collapse pressure rating exceeds maximum external pressure minus internal pressure, multiplied by design factor (typically 1.0-1.125).",
            "Collapse load cases include: full evacuation (no internal fluid), partial evacuation during lost circulation, and cementing operations.",
            "Collapse is often the governing design criterion for intermediate casing strings in depleted zones."
        ],
        reasoning_framework="""
        Collapse (external pressure) becomes critical when internal pressure support is lost:

        COLLAPSE RATING CALCULATION (API 5C2):
        Four failure modes (yield, plastic, transition, elastic) depending on D/t ratio
        API Bulletin 5C3 provides complex formulas; use manufacturer's tables

        DESIGN EQUATION:
        Required Collapse Resistance = (External Pressure - Internal Pressure) * Design Factor
        Design Factor: 1.0 (minimum), 1.125 (recommended), 1.25 (severe service)

        LOAD CASES (select worst case):
        1. FULL EVACUATION: No internal fluid (equipment failure, lost circulation), full mud gradient externally
        2. PARTIAL EVACUATION: Lost circulation zone, mud level drops inside casing
        3. CEMENTING: Heavy cement slurry outside, light mud inside
        4. PRODUCTION: Depleted reservoir (low internal pressure), higher external pressure from overburden or offset zones
        5. GAS MIGRATION: Gas cut mud inside (reduced density), full mud gradient outside

        GRADE SELECTION FOR COLLAPSE:
        - Higher D/t ratio (thin wall) = lower collapse resistance
        - Heavier wall weights provide better collapse resistance
        - Higher grade steel provides better collapse resistance (within same D/t range)
        - Multi-grade string: heavier wall in high collapse zone, lighter wall shallow (cost optimization)

        CRITICAL SCENARIOS:
        - Deepwater: Large water depth creates high external pressure
        - Depleted zones: Low reservoir pressure, high overburden stress
        - Lost circulation: Cannot maintain fluid level inside casing
        - Salt sections: Plastic salt flow creates high external stress

        ADJUSTMENTS:
        - Temperature reduces collapse resistance (high temp = lower yield strength)
        - Wear reduces wall thickness, significantly impacts collapse
        - Ovality from handling or running reduces collapse resistance
        """,
        key_factors=[
            "Maximum mud weight in annulus (external pressure)",
            "Minimum internal fluid level (worst-case evacuation)",
            "Temperature at depth (affects yield strength)",
            "Wear percentage (reduces wall thickness)",
            "Depleted zone pressure (production casing)",
            "Water depth (offshore wells)",
            "Wall thickness and D/t ratio"
        ],
        primary_authority=[
            "API Specification 5CT - Specification for Casing and Tubing",
            "API Bulletin 5C3 - Formulas and Calculations for Casing, Tubing, Drill Pipe",
            "ISO 10400 - Formulas and calculations for casing, tubing, drill pipe",
            "API RP 5C5 - Recommended Practice for Evaluation Procedure for Casing and Tubing Connections"
        ],
        burden_holder="Operator - must demonstrate collapse rating exceeds differential pressure with design factor",
        adversary_position="Conservative reviewer may require higher design factor or challenge evacuation assumptions",
        counter_arguments=[
            "Well control procedures prevent full evacuation scenario",
            "Lost circulation mitigation (LCM) available to maintain fluid level",
            "Annulus monitoring detects pressure changes early",
            "Heavier wall weight available if standard rating insufficient"
        ],
        resolution_strategy="Conservative evacuation scenario (full or partial based on offset experience); apply API-recommended design factors; use heavier wall weight in critical collapse zones; consider multi-grade string for optimization.",
        entity_scope="All well types; particularly critical for deepwater, depleted reservoirs, and salt sections",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Based on API standardized calculations and conservative evacuation assumptions; temperature and wear effects introduce some uncertainty.",
        controlling_precedent="API Specification 5CT and API Bulletin 5C3 for collapse rating calculations"
    ),

    DoctrineBlock(
        topic="casing_tensile_design",
        keywords=["tension", "axial load", "joint strength", "running load", "buoyancy", "design factor"],
        conclusion_template=[
            "Casing tensile strength must exceed maximum axial load multiplied by design factor (typically 1.3-1.8), with connection joint strength as the limiting factor.",
            "Tensile load includes pipe weight (less buoyant weight in mud), bending loads in deviated wells, shock loads during running, and overpull during cementing.",
            "Premium connections (BTC, VAM, Tenaris) provide higher joint strength than API round thread connections (STC, LTC)."
        ],
        reasoning_framework="""
        Tensile (axial) load is the accumulated weight of the casing string:

        TENSILE STRENGTH (API 5CT):
        Pipe Body Yield = 0.7854 * (OD² - ID²) * Yield Strength
        Joint Strength = Connection rating from API tables or manufacturer data
        GOVERNING STRENGTH = Minimum of (Pipe Body, Joint Strength)

        DESIGN EQUATION:
        Required Tensile Strength = Maximum Axial Load * Design Factor
        Design Factor: 1.3 (minimum), 1.6 (recommended), 1.8 (severe service/HPHT)

        AXIAL LOAD CALCULATION:
        1. TRUE WEIGHT: Sum of joint weights from casing tally
        2. BUOYANT WEIGHT: True weight * (1 - mud_density / steel_density)
           Steel density = 65.4 ppg → Buoyancy factor = 1 - (mud_wt / 65.4)
        3. BENDING LOAD: In deviated wells, add bending contribution
        4. SHOCK LOAD: Running speed, sudden stops (use dynamic factor 1.2-1.5)
        5. OVERPULL: Cementing operations, stuck pipe scenarios (design contingency)

        CONNECTION SELECTION FOR TENSILE:
        - STC (Short Thread Coupling): 60-70% of pipe body strength
        - LTC (Long Thread Coupling): 80-90% of pipe body strength
        - BTC (Buttress Thread Coupling): 90-95% of pipe body strength
        - Premium connections: 100%+ of pipe body strength (some exceed pipe body)

        MULTI-GRADE STRING DESIGN:
        - Heavier wall or higher grade at top (highest tensile load)
        - Lighter/lower grade at bottom (lower tensile, may be governed by collapse/burst)
        - Transition joint location optimized for load distribution and cost

        SPECIAL CONSIDERATIONS:
        - Deviated/horizontal wells: Add bending load (dog leg severity effect)
        - Thermal expansion: Temperature change causes length change, affects tensile
        - Green cement: Setting during cementing creates compressive load
        - Landing vs hanging: Landing on bottom reduces tensile, but compression effects
        """,
        key_factors=[
            "Total true weight of casing string from tally",
            "Mud weight (affects buoyancy factor)",
            "Connection type (STC, LTC, BTC, premium)",
            "Dog leg severity in deviated sections",
            "Running speed and shock loads",
            "Cementing overpull requirements",
            "Temperature differential (thermal expansion/contraction)"
        ],
        primary_authority=[
            "API Specification 5CT - Specification for Casing and Tubing",
            "API Bulletin 5C3 - Formulas and Calculations for Casing, Tubing, Drill Pipe",
            "API RP 5C1 - Care and Use of Casing and Tubing",
            "ISO 10400 - Formulas and calculations for casing, tubing, drill pipe"
        ],
        burden_holder="Operator - must provide casing tally demonstrating tensile capacity with design factor",
        adversary_position="Conservative reviewer may require higher design factor or challenge shock load assumptions",
        counter_arguments=[
            "Controlled running speed minimizes shock loads",
            "Premium connection provides margin above API rating",
            "Multi-grade string optimized for tensile distribution",
            "Landing string on bottom eliminates full tensile load"
        ],
        resolution_strategy="Detailed casing tally with actual joint weights; apply buoyancy correction for mud weight; use API-recommended design factors (1.6 typical); select connection type adequate for tensile load; consider premium connections if standard API connections insufficient.",
        entity_scope="All well types; particularly critical for deep wells and deviated/horizontal wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Based on API standardized calculations and manufacturer connection data; shock load estimates introduce moderate uncertainty, addressed by design factor.",
        controlling_precedent="API Specification 5CT and API Bulletin 5C3 for tensile strength calculations; API RP 5C1 for running practices"
    ),

    DoctrineBlock(
        topic="biaxial_triaxial_stress_analysis",
        keywords=["von Mises", "biaxial", "triaxial", "combined loading", "stress ellipse", "API ellipse"],
        conclusion_template=[
            "Biaxial (burst + tension or collapse + tension) and triaxial (burst/collapse + tension + bending) stress analysis using von Mises equivalent stress accounts for combined loading conditions.",
            "API 5C3 provides simplified elliptical interaction equations; finite element analysis may be required for complex load cases.",
            "Combined loading reduces allowable capacity in each load direction compared to uniaxial analysis."
        ],
        reasoning_framework="""
        Real-world casing experiences combined loads simultaneously:

        VON MISES EQUIVALENT STRESS:
        σ_vm = sqrt(σ_axial² + σ_hoop² - σ_axial*σ_hoop + 3*τ²)
        Where: σ_axial = axial stress (tension/compression)
               σ_hoop = hoop stress (burst/collapse)
               τ = shear stress (torsion, bending)

        Failure criterion: σ_vm ≤ Yield Strength / Design Factor

        API SIMPLIFIED APPROACH (5C3 Section 5):
        Biaxial ellipse for tension + burst or tension + collapse:
        (Tension / Tension_capacity)² + (Burst / Burst_capacity)² ≤ 1.0

        CRITICAL LOAD COMBINATIONS:
        1. RUNNING: Tension (string weight) + burst (pressure test) + bending (dog legs)
        2. CEMENTING: Tension (buoyed weight) + burst (internal cement pressure) + external pressure
        3. PRODUCTION: Burst (tubing leak) + tension (thermal growth) + bending (buckling)
        4. STIMULATION: Burst (frac pressure) + tension (packer setting) + thermal (fluid temp)

        WHEN BIAXIAL ANALYSIS REQUIRED:
        - Any design where single load component exceeds 80% of capacity (interaction effects significant)
        - HPHT wells (high pressure + high temperature + deep = combined loads)
        - Thermal wells (steam injection, cold injection creates thermal stress)
        - Horizontal wells (bending + drag + tension + pressure)

        TRIAXIAL CONSIDERATIONS:
        - Add bending stress from dog legs in deviated sections
        - Torsion from rotation (drill casing, casing while drilling)
        - Body yield strength vs connection yield (different failure modes)

        DESIGN APPROACH:
        1. Calculate each load component independently (uniaxial)
        2. Check if any exceeds 80% of capacity → biaxial analysis required
        3. Apply API ellipse equation or von Mises FEA
        4. Iterate grade/wall thickness until combined stress within yield
        """,
        key_factors=[
            "Axial load magnitude (tension or compression)",
            "Hoop stress magnitude (burst or collapse)",
            "Bending stress from dog leg severity",
            "Thermal stress from temperature differential",
            "Connection vs pipe body strength differences",
            "Load phasing (which loads occur simultaneously)",
            "Design factor application (to individual loads or combined stress)"
        ],
        primary_authority=[
            "API Bulletin 5C3 Section 5 - Combined Loading",
            "ISO 10400 Annex B - Combined Loading Equations",
            "API TR 5C3 - Technical Report on Equations and Calculations for Casing, Tubing, and Line Pipe",
            "ASME Section VIII - Pressure Vessel Design (von Mises theory)"
        ],
        burden_holder="Operator - must demonstrate combined loads within yield envelope using biaxial or triaxial analysis",
        adversary_position="Conservative reviewer may require finite element analysis for complex load cases or challenge load phasing assumptions",
        counter_arguments=[
            "Conservative uniaxial analysis with high design factors bounds combined loading",
            "API ellipse method widely accepted for standard applications",
            "Manufacturer FEA analysis validates design for premium connections",
            "Field performance in offset wells demonstrates adequacy"
        ],
        resolution_strategy="Apply API 5C3 biaxial ellipse for standard cases (tension + pressure); use finite element analysis for complex triaxial cases (HPHT, thermal, high dog leg); ensure all load components within 90% of ellipse boundary (10% margin); document load phasing assumptions.",
        entity_scope="HPHT wells, thermal wells, horizontal/deviated wells, and any case where single load > 80% capacity",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="API ellipse method is simplified approximation; FEA provides higher accuracy but requires validation; load phasing assumptions introduce uncertainty.",
        controlling_precedent="API Bulletin 5C3 Section 5 for biaxial analysis; ISO 10400 for comprehensive combined loading"
    ),

    DoctrineBlock(
        topic="casing_wear_analysis",
        keywords=["wear", "dog leg", "drill pipe rotation", "wall thickness", "wear factor", "tool joint"],
        conclusion_template=[
            "Casing wear from drill pipe rotation in deviated wells reduces wall thickness, thereby reducing burst and collapse capacity.",
            "Wear percentage is calculated from dog leg severity, rotary hours, and wear factor (tool joint hardness vs casing grade).",
            "Design approach: Calculate wear, reduce original wall thickness by wear percentage, recalculate burst/collapse ratings, apply design factors."
        ],
        reasoning_framework="""
        Drill pipe rotation in deviated wells causes casing wear:

        WEAR MECHANISM:
        - Drill pipe tool joints (hard surface) contact casing inner diameter at dog legs
        - Rotation creates abrasive wear, removing casing material
        - Wear rate depends on: contact force, rotary hours, relative hardness, dog leg severity

        WEAR CALCULATION (API RP 7G):
        Wear Factor (W) = f(Dog Leg Severity, Rotary Hours, Hardness Ratio)
        Reduced Wall Thickness = Original Thickness * (1 - W)

        SIMPLIFIED APPROACH:
        W = K * DLS * Hours * Hardness_Ratio
        Where: K = empirical constant (0.0001 to 0.0005)
               DLS = dog leg severity (°/100 ft)
               Hours = cumulative rotary hours at that depth
               Hardness_Ratio = tool joint / casing grade

        IMPACT ON RATINGS:
        - Burst: Directly proportional to wall thickness → W% wear = W% reduction in burst
        - Collapse: Exponentially sensitive to D/t ratio → W% wear = 2-3*W% reduction in collapse
        - Tension: Proportional to cross-sectional area → W% wear ≈ W% reduction (typically minor)

        CRITICAL WEAR SCENARIOS:
        - Horizontal wells: Extended lateral, high dog legs, long rotary hours
        - Pad drilling: Multiple wells through same intermediate casing
        - Hard formations: Slow ROP, high rotary hours per foot
        - Build sections: High dog leg severity creates high contact force

        MITIGATION STRATEGIES:
        1. DESIGN FOR WEAR: Pre-calculate expected wear, use heavier wall weight or higher grade
        2. NON-ROTATING PROTECTORS: Reduce contact area and friction
        3. CASING ROTATION: Distribute wear circumferentially (rare)
        4. DRILLING PRACTICES: Minimize rotary time, use downhole motors in critical sections
        5. INSPECTION: Caliper logs after drilling to measure actual wear

        ACCEPTANCE CRITERIA:
        - Regulatory: Typically no specific limit, but must maintain design factors after wear
        - Industry practice: <20% wear acceptable, 20-30% requires engineering review, >30% requires remediation
        - Re-rate casing: Calculate new burst/collapse with reduced wall thickness, confirm design factors still met
        """,
        key_factors=[
            "Dog leg severity in build/turn sections (°/100 ft)",
            "Cumulative rotary hours at each depth interval",
            "Tool joint hardness vs casing grade hardness ratio",
            "Drill pipe weight and stiffness (contact force)",
            "Mud properties (lubricity affects wear rate)",
            "Number of bit runs (multiple trips increase wear)",
            "Planned vs actual trajectory (deviation changes)"
        ],
        primary_authority=[
            "API RP 7G - Recommended Practice for Drill Stem Design and Operating Limits",
            "ISO 10405 - Petroleum and natural gas industries — Care and use of casing and tubing",
            "SPE 52850 - Casing Wear: Laboratory Measurements and Field Predictions",
            "IADC Drilling Manual - Casing Wear Section"
        ],
        burden_holder="Operator - must calculate expected wear and demonstrate casing ratings remain adequate after wear",
        adversary_position="Conservative reviewer may challenge wear factor assumptions or require caliper log confirmation",
        counter_arguments=[
            "Conservative wear factors (upper bound) used in design",
            "Post-drill caliper log shows actual wear less than predicted",
            "Heavier wall weight specified in critical wear zones",
            "Drilling practices (motor, low RPM) minimize wear"
        ],
        resolution_strategy="Calculate expected wear using API RP 7G methods with conservative assumptions; reduce wall thickness by wear percentage; recalculate burst and collapse ratings; ensure design factors still met after wear; consider heavier wall weight in high dog leg sections; plan caliper log to confirm actual wear.",
        entity_scope="Deviated and horizontal wells; particularly critical for intermediate casing in shale plays with long laterals",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Wear prediction models have significant uncertainty (actual wear depends on many variables); conservative wear factors and design margins address uncertainty; caliper log confirmation recommended.",
        controlling_precedent="API RP 7G for wear calculation methodology; no specific regulatory wear limits, but must maintain design factors"
    ),

    DoctrineBlock(
        topic="pore_pressure_fracture_gradient",
        keywords=["pore pressure", "fracture gradient", "leak-off test", "LOT", "FIT", "XLOT", "overburden", "drilling window"],
        conclusion_template=[
            "Pore pressure is the fluid pressure within formation pores; fracture gradient is the pressure required to fracture the formation and initiate lost circulation.",
            "Drilling window is the margin between pore pressure (minimum mud weight to control formation fluids) and fracture gradient (maximum mud weight before losses).",
            "Predrill estimates from seismic, offset wells, and correlations; confirmed by leak-off tests (LOT) at each casing shoe."
        ],
        reasoning_framework="""
        Pore pressure and fracture gradient define safe drilling envelope:

        PORE PRESSURE ESTIMATION:
        1. NORMAL PRESSURE: 0.433-0.465 psi/ft (formation water gradient)
        2. OVERPRESSURE: Exceeds normal (compaction disequilibrium, hydrocarbon generation, tectonics)
        3. SUBNORMAL: Below normal (depleted reservoirs, shallow gas)

        Predrill methods:
        - Offset well data: Kick indicators, connection gas, trip gas
        - Seismic velocity: Low velocity = high pore pressure (undercompacted shale)
        - D-exponent: Drilling rate normalized for RPM, WOB, bit size
        - Shale density: Low density = high pore pressure (from density logs)

        FRACTURE GRADIENT ESTIMATION:
        Empirical correlations:
        - Eaton: Fg = (σv - P) * K + P, where K = Poisson effect (0.33-0.5)
        - Matthews-Kelly: Fg/σv = 1 - (σv - P)/σv * (1 - K)
        - Hubbert-Willis: Fg = σmin + Tensile Strength

        Variables:
        - σv = Overburden stress (psi) = ∫(density * 0.052 * depth)
        - P = Pore pressure (psi)
        - σmin = Minimum horizontal stress
        - K = Stress coefficient (depends on tectonics, depth, lithology)

        LEAK-OFF TEST (LOT):
        Procedure at each casing shoe:
        1. Drill out shoe, clean hole, pull bit into casing
        2. Close annular BOP or pipe rams
        3. Pump slowly into well, monitor pressure
        4. Continue until pressure breaks from linear trend (leak-off point)
        5. Calculate equivalent mud weight: EMW = LOT pressure / (0.052 * TVD)

        Variations:
        - FIT (Formation Integrity Test): Pump to predetermined pressure, hold, no leak-off
        - XLOT (Extended LOT): Continue past leak-off to closure (propagate fracture)

        DRILLING WINDOW:
        Minimum MW = Pore Pressure / 0.052 + Kick margin (0.5 ppg typical)
        Maximum MW = Fracture Gradient / 0.052 - Safety margin (0.5 ppg typical)

        NARROW WINDOW IMPLICATIONS:
        - Requires precise mud weight control (0.1 ppg tolerance)
        - May require additional casing string to section off pressure transition
        - Managed pressure drilling (MPD) if conventional drilling not viable
        - Underbalanced drilling for extremely narrow windows

        CASING DESIGN IMPACT:
        - Surface casing seat: Deep enough that frac gradient exceeds next section pore pressure + kick margin
        - Intermediate casing seats: At pressure transitions where window narrows
        - Number of strings: More strings in HPHT, fewer in normal pressure regimes
        """,
        key_factors=[
            "Offset well pore pressure and LOT data",
            "Seismic velocity anomalies indicating overpressure",
            "Formation lithology (shale vs sand compaction)",
            "Tectonic regime (extensional, compressional, strike-slip)",
            "Depletion (production in area reduces pore pressure)",
            "Depth (overburden stress increases with depth)",
            "Temperature (affects fluid density and rock strength)"
        ],
        primary_authority=[
            "SPE Monograph - Geopressure and Wellbore Stability Prediction (Mouchet & Mitchell)",
            "API RP 13D - Rheology and Hydraulics of Oil-well Drilling Fluids",
            "IADC Drilling Manual - Pressure Control Section",
            "SPE 118525 - Fracture Gradient Prediction: An Overview and Update"
        ],
        burden_holder="Operator - must provide predrill pore pressure and fracture gradient estimates; confirm with LOT at each shoe",
        adversary_position="Regulator may require additional casing strings if drilling window narrow or pressure uncertainties high",
        counter_arguments=[
            "Offset well data provides reliable pore pressure estimates",
            "LOT confirms adequate fracture gradient at each shoe",
            "Managed pressure drilling can handle narrow windows",
            "Seismic inversion reduces predrill uncertainty"
        ],
        resolution_strategy="Conservative predrill estimates using multiple methods (seismic, offsets, correlations); plan LOT at each casing shoe; drilling window analysis for each hole section; contingency casing string if window narrows; real-time pore pressure monitoring while drilling.",
        entity_scope="All well types; particularly critical in HPHT, deepwater, and overpressured basins",
        confidence=ConfidenceLevel.DISCLOSURE,
        confidence_stratification="Predrill estimates have significant uncertainty; LOT provides confirmation but only at casing shoes, not while drilling; real-time monitoring reduces risk.",
        controlling_precedent="No specific API standard for pore pressure prediction; industry practice based on SPE literature and offset well data"
    ),

    DoctrineBlock(
        topic="premium_connections",
        keywords=["VAM", "TenarisHydril", "premium connection", "metal-to-metal seal", "gas-tight", "sealability", "torque"],
        conclusion_template=[
            "Premium connections (VAM, TenarisHydril, PTC, etc.) provide superior performance over API connections: higher torque, metal-to-metal seal (gas-tight), better compression resistance, and enhanced structural integrity.",
            "Applications: HPHT wells, sour service, thermal wells, horizontal wells, and critical production strings where API connections insufficient.",
            "Higher cost justified by improved performance and reduced leak risk."
        ],
        reasoning_framework="""
        Premium connections overcome API connection limitations:

        API CONNECTION LIMITATIONS:
        - STC/LTC/BTC: Thread compound seal (not metal-to-metal) → potential leak path
        - Tensile efficiency: 60-95% of pipe body (connection is weak point)
        - Compression: Prone to jump-out under compression load
        - Sealability: Not gas-tight under thermal cycling or severe loads

        PREMIUM CONNECTION FEATURES:
        1. METAL-TO-METAL SEAL: Engineered interference fit creates gas-tight barrier
        2. TORQUE SHOULDER: Dedicated shoulder distributes torque, prevents galling
        3. STRUCTURAL LOAD RING: Handles compression without jump-out
        4. TENSILE: 100%+ pipe body efficiency (some designs exceed pipe body)

        COMMON PREMIUM DESIGNS:

        VAM (Vallourec):
        - Wedge thread with metal-to-metal seal
        - High compression and bending resistance
        - Wide range: VAM TOP, VAM 21, VAM FJL, VAM HTF
        - Applications: HPHT, sour service, horizontal wells

        TenarisHydril (Blue®, Wedge):
        - Proprietary thread form, metal seal
        - Ultra-high torque capacity
        - Applications: Deep HPHT, thermal, high-dogleg

        PTC (various manufacturers):
        - Generic term for non-API premium connections
        - Performance varies by manufacturer
        - Verify ratings and test data

        SELECTION CRITERIA:
        1. SEALABILITY: Gas-tight requirement (HPHT, gas injection, CO2/H2S)
        2. COMPRESSION: Horizontal wells, thermal expansion, buckling
        3. BENDING: High dog leg severity in directional wells
        4. TORQUE: Horizontal wells requiring casing rotation
        5. THERMAL CYCLING: Steam injection, geothermal, cold injection

        TESTING & QUALIFICATION:
        - ISO 13679 (CAL IV): Seal test under load (tension, compression, internal/external pressure, thermal)
        - Manufacturer qualification data: Load envelopes, finite element analysis
        - Field performance: Track record in similar applications

        COST-BENEFIT:
        - Premium connections: 2-5x cost of API connections
        - Justified by: Reduced leak risk, higher performance, longer well life
        - Critical wells (HPHT production): Premium mandatory
        - Non-critical wells (shallow surface): API adequate

        MAKE-UP:
        - Torque to manufacturer specification (critical for seal integrity)
        - Torque-turn method: Monitor torque vs turns, verify shoulder contact
        - Inspection: Magnetic particle, visual, thread damage assessment
        - Sealing compound: Manufacturer-specified (some dry-seal, some require compound)
        """,
        key_factors=[
            "Gas-tight seal requirement (yes/no)",
            "Maximum load conditions (tension, compression, bending, pressure)",
            "Thermal cycling (steam, cold water injection)",
            "Sour service environment (H2S corrosion resistance)",
            "Dog leg severity (bending moment capacity)",
            "Well criticality (production vs non-critical)",
            "Budget constraints (premium cost justifiable?)"
        ],
        primary_authority=[
            "ISO 13679 - Petroleum and natural gas industries — Procedures for testing casing and tubing connections",
            "API RP 5C5 - Recommended Practice for Evaluation Procedure for Casing and Tubing Connections",
            "Manufacturer technical manuals (VAM, Tenaris, etc.)",
            "SPE 90045 - Premium Connection Performance in HPHT Wells"
        ],
        burden_holder="Operator - must justify premium connection selection based on load analysis and performance requirements",
        adversary_position="Cost-conscious reviewer may challenge premium connection necessity if API connections sufficient",
        counter_arguments=[
            "Critical well (HPHT production) justifies premium cost",
            "API connections have leak history in similar applications (offset data)",
            "ISO 13679 CAL IV testing demonstrates superior performance",
            "Long-term well economics favor reliability over upfront cost"
        ],
        resolution_strategy="Quantify load conditions (biaxial/triaxial analysis); compare API vs premium ratings; demonstrate API insufficient or unacceptable risk; cost-benefit analysis (premium cost vs leak remediation cost); select manufacturer with proven track record in similar applications.",
        entity_scope="HPHT wells, sour service, thermal wells, horizontal/high-dogleg wells, critical production strings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Premium connections proven in field applications; ISO 13679 testing provides objective performance data; proper make-up critical to achieving rated performance.",
        controlling_precedent="ISO 13679 for connection qualification; manufacturer technical data for specific connection performance"
    ),

    DoctrineBlock(
        topic="liner_design_tieback",
        keywords=["liner", "liner hanger", "tieback", "overlap", "seal assembly", "polished bore receptacle", "PBR"],
        conclusion_template=[
            "Liner is a casing string that does not extend to surface, hung from the previous casing string via liner hanger, typically with 300-500 ft overlap.",
            "Tieback liner to surface converts liner to full casing string, providing additional pressure integrity and barrier element.",
            "Liner design requires: hanger capacity analysis, overlap length, seal assembly design, contingency for tieback."
        ],
        reasoning_framework="""
        Liner vs full casing string trade-off:

        LINER ADVANTAGES:
        - Cost savings: Less pipe, smaller rig, faster running time
        - Weight savings: Reduced load on previous strings (tensile margin)
        - Flexibility: Can run liner to TD if hole conditions deteriorate

        LINER DISADVANTAGES:
        - No direct surface access (must work through previous string)
        - Hanger is potential leak point (vs welded/coupled full string)
        - Tieback required for pressure barrier (regulatory or operational)

        LINER HANGER TYPES:
        1. MECHANICAL: Slips set by rotation, weight, or hydraulic
        2. HYDRAULIC: Inflatable packer element, high pressure rating
        3. EXPANSION: Cone expands liner into previous casing, metal-to-metal seal

        HANGER CAPACITY:
        - Tension: Must support liner weight + overpull + dynamic loads
        - Pressure: Sealing element rated for differential pressure
        - Slips: Prevent liner from falling (backup to seal)
        - Torque: If rotation required (cemented liner, tight spots)

        OVERLAP LENGTH:
        - Minimum: 200 ft (industry practice)
        - Typical: 300-500 ft (allows tieback landing nipple placement)
        - Factors: Hanger setting depth, previous shoe depth, wellbore stability

        TIEBACK DESIGN:
        - Tieback string: Casing from surface to PBR (polished bore receptacle) in overlap
        - Seal assembly: Latches into PBR, creates pressure barrier
        - Pressure rating: Must handle full wellhead pressure
        - Uses: Regulatory requirement (offshore), well control barrier, production isolation

        TIEBACK SCENARIOS:
        1. PLANNED: Regulatory mandate (MMS/BOEM offshore), HPHT wells
        2. CONTINGENT: Available if needed (hanger leak, pressure integrity issue)
        3. PRODUCTION: Install during completion (isolate annuli)

        PBR (POLISHED BORE RECEPTACLE):
        - Installed in overlap: PBR collar or PBR pup joint
        - Tieback seal stinger lands and seals in PBR
        - Pressure rating: Match tieback pressure requirement
        - Redundancy: Some designs run dual PBRs (primary + backup)

        REGULATORY:
        - Offshore US (BOEM): Production liners typically require tieback to surface
        - Onshore: State-specific (some require, some allow liner without tieback)
        - International: Varies by jurisdiction (North Sea strict, some basins flexible)

        DESIGN PROCESS:
        1. Determine liner setting depth and length
        2. Calculate overlap with previous casing (typically 300-500 ft)
        3. Select hanger type and rating (tension, pressure, environment)
        4. Design tieback (if required or contingent)
        5. Specify PBR location and rating
        6. Cement design: Liner top 500+ ft above hanger for stability
        """,
        key_factors=[
            "Cost savings vs full casing string",
            "Regulatory tieback requirement (jurisdiction-specific)",
            "Hanger pressure and tension rating",
            "Overlap length (minimum 200 ft, typical 300-500 ft)",
            "Tieback contingency (even if not planned initially)",
            "Cement coverage (liner top to surface or to previous shoe)",
            "Well control barriers (liner + tieback = two barriers)"
        ],
        primary_authority=[
            "API Specification 11D1 - Specification for Packers and Bridge Plugs",
            "30 CFR 250.420 - Casing and Cementing Requirements (BOEM offshore)",
            "NORSOK D-010 - Well integrity in drilling and well operations",
            "ISO 16530-1 - Petroleum and natural gas industries — Well integrity — Part 1: Life cycle governance"
        ],
        burden_holder="Operator - must demonstrate liner hanger capacity adequate and tieback available if required",
        adversary_position="Regulator may mandate tieback even if not technically required (additional barrier element)",
        counter_arguments=[
            "Liner hanger qualified per ISO testing, proven in field",
            "Overlap length provides cement barrier above hanger",
            "Tieback available as contingency (PBR installed)",
            "Offset wells use liner without tieback successfully"
        ],
        resolution_strategy="Conservative hanger selection (high pressure/tension rating); adequate overlap (300-500 ft); install PBR for tieback contingency even if not initially planned; comply with regulatory tieback requirements; cement liner top to previous shoe or surface per jurisdiction.",
        entity_scope="Intermediate and production liners; particularly common in deepwater and multi-stage completions",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Liner hanger technology mature and proven; tieback provides redundant barrier; regulatory requirements vary by jurisdiction.",
        controlling_precedent="30 CFR 250.420 for offshore US; API Spec 11D1 for hanger specifications; jurisdiction-specific regulations"
    ),

    DoctrineBlock(
        topic="casing_centralizer_placement",
        keywords=["centralizer", "standoff", "API RP 10D-2", "cement sheath", "eccentric", "mud removal"],
        conclusion_template=[
            "Casing centralizers maintain annular standoff, ensuring uniform cement sheath thickness for zonal isolation and structural support.",
            "API RP 10D-2 provides centralizer placement guidelines: 67% standoff minimum in critical zones, 100% in production intervals.",
            "Centralizer spacing based on hole deviation, casing stiffness, and cement design requirements."
        ],
        reasoning_framework="""
        Centralizers are critical for cement job success:

        PURPOSE:
        1. STANDOFF: Maintain casing concentric in wellbore (prevent casing resting on low side)
        2. CEMENT SHEATH: Uniform annular thickness → structural integrity, zonal isolation
        3. MUD REMOVAL: Turbulent flow path → better mud displacement efficiency
        4. BUCKLING PREVENTION: Support points reduce buckling in deviated sections

        STANDOFF DEFINITION:
        Standoff (%) = [(Hole Diameter - Casing OD) - (2 * Eccentricity)] / (Hole Diameter - Casing OD) * 100

        Where eccentricity = distance from casing center to hole center
        - 100% standoff: Casing perfectly centered
        - 67% standoff: API minimum for critical zones
        - 0% standoff: Casing touching formation (worst case)

        API RP 10D-2 GUIDELINES:

        CRITICAL ZONES (production intervals, weak formations, corrosive zones):
        - Target: 100% standoff (casing centered)
        - Minimum: 67% standoff
        - Centralizer spacing: Every joint (40-45 ft) or per modeling software

        NON-CRITICAL ZONES (intermediate sections, no zonal isolation requirements):
        - Target: 67% standoff
        - Minimum: 50% standoff
        - Centralizer spacing: Every 2-4 joints (80-180 ft)

        VERTICAL WELLS:
        - Gravity keeps casing relatively centered
        - Centralizers at: casing shoe, float collar, critical zones, every 3-5 joints

        DEVIATED/HORIZONTAL WELLS:
        - Casing tends to rest on low side (0% standoff without centralizers)
        - Centralizer spacing: Every joint in high-angle and horizontal sections
        - Rigid vs bow-spring: Rigid centralizers for high-angle, bow-spring for moderate deviation

        CENTRALIZER TYPES:

        BOW-SPRING:
        - Flexible, restoring force when compressed
        - Pros: Easy to run, low drag, self-centering
        - Cons: Lower restoring force, can collapse in tight spots
        - Applications: Moderate deviation (0-60°), good hole conditions

        RIGID (SOLID BODY):
        - Fixed diameter, high restoring force
        - Pros: Maintain standoff in high-angle, strong support
        - Cons: High drag, can cause stuck pipe if oversized
        - Applications: High-angle (60-90°), horizontal sections

        HINGED RIGID:
        - Hybrid design, rigid when deployed, hinged for running
        - Applications: High standoff requirement, difficult hole conditions

        DESIGN PROCESS:
        1. Determine critical zones (production, weak formations)
        2. Calculate required standoff per API RP 10D-2 (67% or 100%)
        3. Model centralizer placement using software (START, CentraDesign, etc.)
        4. Input: hole size, deviation, casing OD, centralizer type, restoring force
        5. Output: Standoff profile, recommended centralizer spacing
        6. Verify: Running forces, drag, torque within rig/string capacity

        INSTALLATION:
        - Stop collars or set screws prevent centralizer movement during running
        - Centralizer near casing shoe: 2-3 joints above shoe (prevents plug-out)
        - Float collar centralizer: Support cement column during WOC
        """,
        key_factors=[
            "Hole deviation angle (vertical, deviated, horizontal)",
            "Critical zones requiring zonal isolation (production, corrosive)",
            "Hole size vs casing OD (annular clearance)",
            "Centralizer restoring force (must overcome casing weight component)",
            "Cement design (turbulent vs laminar, cement weight)",
            "Running forces (drag, torque must be within limits)",
            "Hole quality (tight spots, washouts affect centralizer sizing)"
        ],
        primary_authority=[
            "API RP 10D-2 - Recommended Practice for Centralizer Placement and Cementing",
            "API Spec 10D - Specification for Bow-Spring Casing Centralizers",
            "ISO 10427-1 - Petroleum and natural gas industries — Equipment for well cementing — Part 1: Casing centralizers",
            "SPE 98892 - Casing Centralizer Placement Optimization"
        ],
        burden_holder="Operator - must demonstrate centralizer design achieves minimum standoff per API RP 10D-2",
        adversary_position="Conservative reviewer may require 100% standoff throughout well, or modeling software validation",
        counter_arguments=[
            "API RP 10D-2 compliance with 67% standoff minimum",
            "Modeling software predicts adequate standoff with proposed spacing",
            "Offset wells with similar centralizer program achieved good cement jobs",
            "Over-centralization increases drag and stuck pipe risk"
        ],
        resolution_strategy="Use centralizer modeling software (START, CentraDesign) to predict standoff profile; target 100% in critical zones, 67% minimum elsewhere; select centralizer type appropriate for deviation (bow-spring <60°, rigid >60°); verify running forces acceptable; follow API RP 10D-2 spacing guidelines.",
        entity_scope="All wells; particularly critical in deviated/horizontal wells and zones requiring zonal isolation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API RP 10D-2 provides industry-standard guidelines; modeling software predicts standoff (validation with caliper logs post-job recommended); field performance demonstrates adequacy.",
        controlling_precedent="API RP 10D-2 for centralizer placement and standoff criteria"
    ),

    DoctrineBlock(
        topic="hpht_casing_design",
        keywords=["HPHT", "high pressure high temperature", "thermal expansion", "API de-rating", "combined loading"],
        conclusion_template=[
            "HPHT (High Pressure High Temperature) wells require enhanced casing design: higher grades (P-110, Q-125), premium connections, thermal effects analysis, and combined loading (biaxial/triaxial).",
            "Temperature reduces yield strength (API de-rating curves); thermal expansion creates axial load; narrow drilling windows require additional casing strings.",
            "Design factors increased: burst 1.25 (vs 1.1 standard), collapse 1.25 (vs 1.125), tension 1.8 (vs 1.6)."
        ],
        reasoning_framework="""
        HPHT wells push casing design limits:

        HPHT DEFINITION:
        - HIGH PRESSURE: Pore pressure > 0.8 psi/ft (> 16 ppg equivalent mud weight)
        - HIGH TEMPERATURE: BHT > 300°F (149°C)
        - ULTRA-HPHT: Pressure > 15,000 psi AND/OR Temperature > 350°F

        DESIGN CHALLENGES:

        1. TEMPERATURE EFFECTS:
        - Yield strength reduction: 10-30% at 300-500°F (API de-rating curves)
        - Thermal expansion: Casing grows ~6-8 inches per 1,000 ft per 100°F (steel expansion coefficient 6.5e-6/°F)
        - Young's modulus reduction: Affects collapse and buckling
        - Creep: Time-dependent deformation at high temperature

        API TEMPERATURE DE-RATING (API Bulletin 5C3 Appendix F):
        - P-110 at 300°F: ~95% of room temp yield
        - P-110 at 400°F: ~85% of room temp yield
        - P-110 at 500°F: ~75% of room temp yield
        - Q-125 has better high-temp performance than P-110

        2. COMBINED LOADING:
        - Burst + tension + thermal stress = triaxial analysis required
        - Von Mises or API ellipse method
        - Cannot analyze loads independently (interaction effects significant)

        3. NARROW DRILLING WINDOW:
        - High pore pressure + low fracture gradient = 1-2 ppg window
        - Requires additional intermediate strings to section off transitions
        - Managed pressure drilling (MPD) may be necessary

        4. MATERIAL SELECTION:
        - Grades: P-110, Q-125 (sometimes V-150 for ultra-HPHT)
        - Connections: Premium only (VAM HTF, TenarisHydril, proprietary designs)
        - Sour service: L-80 Type 13Cr, 25Cr duplex, CRA clad if H2S present

        5. CORROSION:
        - CO2: High partial pressure at high temp accelerates corrosion
        - H2S: Sour service (NACE MR0175/ISO 15156) material requirements
        - Corrosion allowance: 0.05-0.10 inch additional wall thickness

        DESIGN PROCESS:

        STEP 1: THERMAL ANALYSIS
        - Predict temperature profile (geothermal gradient + fluid circulation)
        - De-rate yield strength per API Bulletin 5C3 Appendix F
        - Calculate thermal expansion: ΔL = α * L * ΔT
        - Determine if constrained (landed) or free to expand (hung)

        STEP 2: LOAD ANALYSIS
        - Burst: High formation pressure, potential well control scenarios
        - Collapse: Full evacuation (lost circulation in high-pressure zone)
        - Tension: True weight + thermal load if constrained
        - Bending: Deviated sections (HPHT often in deepwater → directional)

        STEP 3: COMBINED LOADING
        - Biaxial or triaxial analysis (von Mises equivalent stress)
        - Check all load combinations (running, cementing, production, stimulation)
        - Apply HPHT design factors (higher than standard)

        STEP 4: CONNECTION SELECTION
        - Premium connections mandatory (metal-to-metal seal, gas-tight)
        - ISO 13679 CAL IV testing for HPHT conditions
        - Thermal cycling test data (expansion/contraction)

        STEP 5: STRINGS AND SEATS
        - Additional intermediate strings to manage narrow drilling window
        - Deeper surface casing (kick tolerance in high pore pressure)
        - Contingency for unplanned intermediate if pressure transition shallower

        DESIGN FACTORS (HPHT):
        - Burst: 1.25 (vs 1.1 standard)
        - Collapse: 1.25 (vs 1.125 standard)
        - Tension: 1.8 (vs 1.6 standard)
        - Rationale: Greater uncertainty in loads, material behavior, and higher consequence of failure

        CONTINGENCY PLANNING:
        - Alternate casing seats if pore pressure/frac gradient different than predicted
        - Managed pressure drilling (MPD) equipment if window too narrow
        - Lost circulation materials (LCM) for fracture gradient management
        - Well control equipment rated for HPHT (BOP stack, choke manifold)
        """,
        key_factors=[
            "Maximum bottomhole temperature (BHT)",
            "Maximum pore pressure and fracture gradient",
            "Drilling window width (ppg margin)",
            "Thermal expansion (constrained vs free)",
            "Corrosive environment (CO2, H2S)",
            "Well trajectory (vertical vs deviated)",
            "Material availability (P-110, Q-125 long lead items)",
            "Regulatory HPHT requirements (jurisdiction-specific)"
        ],
        primary_authority=[
            "API Bulletin 5C3 Appendix F - Temperature Effects on Casing Strength",
            "ISO 10400 - Casing and tubing design formulas",
            "NACE MR0175/ISO 15156 - Materials for H2S environments",
            "SPE 56755 - HPHT Well Design and Construction Best Practices"
        ],
        burden_holder="Operator - must demonstrate casing design adequate for HPHT conditions with enhanced design factors",
        adversary_position="Conservative reviewer may require additional intermediate strings or higher design factors given uncertainty",
        counter_arguments=[
            "Detailed thermal and load analysis with conservative assumptions",
            "Premium connections ISO 13679 qualified for HPHT",
            "Offset HPHT wells demonstrate design adequacy",
            "Contingency plan for MPD if drilling window narrows"
        ],
        resolution_strategy="Comprehensive thermal analysis (temperature de-rating); combined loading analysis (biaxial/triaxial); apply HPHT design factors (1.25 burst/collapse, 1.8 tension); premium connections with HPHT qualification; additional intermediate strings to manage narrow window; contingency planning for pressure uncertainties.",
        entity_scope="HPHT and ultra-HPHT wells globally; common in Gulf of Mexico, North Sea, Middle East",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="HPHT design involves significant uncertainties (temperature profile, pressure transitions, material behavior at high temp); enhanced design factors and conservative assumptions address uncertainty.",
        controlling_precedent="API Bulletin 5C3 for temperature de-rating; ISO 13679 for HPHT connection qualification; NACE MR0175 for sour service materials"
    ),

    DoctrineBlock(
        topic="casing_running_landing_procedures",
        keywords=["running speed", "landing", "hanging", "green cement", "float equipment", "casing tally"],
        conclusion_template=[
            "Casing running procedures: controlled running speed to minimize shock loads, careful handling to prevent thread damage, accurate tally for depth control.",
            "Landing vs hanging: Landing on bottom creates compressive load (green cement effect); hanging from wellhead creates full tensile load.",
            "Float equipment (float collar, float shoe) prevents backflow during cementing and provides landing point for cement plugs."
        ],
        reasoning_framework="""
        Casing running is critical phase where many failures occur:

        RUNNING PREPARATION:

        1. CASING TALLY:
        - Measure each joint: length, weight, grade, coupling type
        - Calculate cumulative depth vs joint number
        - Identify: Heavy wall sections, grade transitions, centralizer locations
        - Purpose: Precise depth control, verify design vs actual string

        2. INSPECTION:
        - Thread inspection: Gauging, visual, magnetic particle (critical connections)
        - Drift: Pass drift mandrel through each joint (ensures clear ID)
        - Body inspection: Coating damage, dents, ovality
        - Reject criteria: Thread damage, body damage >5% wall, out-of-round >1%

        3. THREAD PROTECTION:
        - Thread compound: API-modified or manufacturer-specified (premium connections)
        - Protectors: Plastic or metal thread protectors during storage/transport
        - Handling: Avoid dropping, dragging (thread damage)

        RUNNING PROCEDURE:

        1. RUNNING SPEED:
        - Vertical wells: 30-60 ft/min typical, 90 ft/min maximum
        - Deviated wells: 15-30 ft/min (drag increases, control critical)
        - Tight spots: Slow to 5-10 ft/min, monitor weight indicator
        - Rationale: High speed → shock load on connections (tensile impact)

        2. WEIGHT MONITORING:
        - Free hang weight: Weight indicator shows cumulative string weight (buoyed)
        - Drag: Additional weight in deviated wells (friction on low side)
        - Overpull: If weight drops suddenly (possible tight spot, ledge, keyseating)
        - Underpull: Weight higher than expected (buckling, corkscrewing in horizontal)

        3. CIRCULATION:
        - Circulate every 5-10 stands (500-1,000 ft) to clean hole
        - Full circulation before cementing (bottoms up, verify returns)
        - Pump rate: Maintain <150 psi friction pressure (prevent fracture at shoe)

        4. CENTRALIZER INSTALLATION:
        - Install per centralizer plan (spacing, type)
        - Stop collars or set screws: Prevent movement during running
        - Verify: Centralizer diameter correct for hole size (check tally)

        LANDING VS HANGING:

        LANDING (setting on bottom):
        - Casing shoe contacts bottom, weight transferred to formation
        - Advantages: Reduces tensile load on upper connections, green cement creates compression
        - Disadvantages: Compressive buckling risk, piston effect (pressure increase from WOC)
        - Procedure: Slack off 20,000-50,000 lbs (set slips with compression)

        HANGING (suspended from wellhead):
        - Full string weight on wellhead and upper connections
        - Advantages: No buckling, thermal expansion free to occur
        - Disadvantages: Full tensile load (must design for), wellhead load capacity
        - Procedure: Pick up to desired weight, set slips (tension)

        GREEN CEMENT EFFECT:
        - During cement WOC (waiting on cement), cement solidifies and bonds to casing
        - Creates compressive load: Cement column weight trying to pull casing down
        - Magnitude: 50-80% of cement column weight (depends on bond strength)
        - Design impact: If landing, design for compression + green cement

        FLOAT EQUIPMENT:

        FLOAT COLLAR:
        - 1-2 joints above shoe, contains check valves (prevent backflow)
        - Landing point for top cement plug (bump plug)
        - Converts casing to U-tube (fill as running, float effect reduces running weight)

        FLOAT SHOE:
        - Shoe contains check valve, no separate float collar
        - Advantages: One less connection, lower cost
        - Disadvantages: If shoe valve fails, entire cement column can U-tube back

        AUTO-FILL FLOAT:
        - Allows casing to fill automatically as run (equalizes pressure)
        - Converts to check valve after cement pumped (ball/dart closes valve)
        - Advantages: Faster running, automatic fill, no manual fill-up

        DIFFERENTIAL FILL:
        - Calculate fill rate to match running speed (prevent collapse from external pressure)
        - Full if collapse risk (thin wall, deep well)
        - Partial fill if burst risk (pressure test planned, gas zone)

        CONTINGENCY:
        - Stuck pipe: Overpull limit (80% of tensile rating), jar if equipped
        - Tight spot: Ream, circulate, slow running speed
        - Lost circulation: LCM, reduce pump rate, stage cement if severe
        - Thread leak: Pressure test before cementing, replace joint if leak detected
        """,
        key_factors=[
            "Running speed (controlled to prevent shock loads)",
            "Casing tally accuracy (depth control, grade transitions)",
            "Thread inspection and protection (prevent galling, leaks)",
            "Landing vs hanging decision (load distribution)",
            "Float equipment type and location (auto-fill, float collar, float shoe)",
            "Centralizer installation per design",
            "Circulation for hole cleaning before cementing",
            "Contingency for stuck pipe, tight spots, lost circulation"
        ],
        primary_authority=[
            "API RP 5C1 - Care and Use of Casing and Tubing",
            "API RP 10B-2 - Testing Well Cements (WOC time, green cement)",
            "IADC Drilling Manual - Casing Running Procedures",
            "ISO 10405 - Care and use of casing and tubing"
        ],
        burden_holder="Operator - must provide casing running procedure demonstrating safe practices and design compliance",
        adversary_position="Conservative reviewer may require slower running speed, more frequent circulation, or additional inspection",
        counter_arguments=[
            "Running speed within API RP 5C1 guidelines",
            "Tally verified against design string",
            "Float equipment tested before running (pressure test on surface)",
            "Offset wells use similar running procedure successfully"
        ],
        resolution_strategy="Follow API RP 5C1 running practices; accurate casing tally; controlled running speed (30-60 ft/min vertical, 15-30 ft/min deviated); thread inspection per API standards; landing vs hanging based on load analysis; install float equipment per cement design; contingency plan for stuck pipe and lost circulation.",
        entity_scope="All well types; particularly critical for deep wells, deviated wells, and large-diameter strings",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API RP 5C1 provides industry-standard running practices; field experience demonstrates adequacy; proper execution critical to achieving design performance.",
        controlling_precedent="API RP 5C1 for casing running and handling practices"
    ),

    DoctrineBlock(
        topic="corrosion_design_h2s_co2",
        keywords=["corrosion", "H2S", "CO2", "NACE MR0175", "sour service", "sweet corrosion", "corrosion allowance"],
        conclusion_template=[
            "Corrosive environments (H2S sour service, CO2 sweet corrosion) require: NACE MR0175/ISO 15156 compliant materials, corrosion allowance added to wall thickness, and corrosion-resistant alloys (CRA) for severe cases.",
            "Sour service (H2S): Use L-80 Type 1 or 13Cr minimum; avoid high-strength steels (>110 ksi yield) due to sulfide stress cracking (SSC).",
            "Sweet corrosion (CO2): Carbon steel acceptable with inhibitor treatment, or corrosion allowance (0.05-0.10 inch) if uninhibited."
        ],
        reasoning_framework="""
        Corrosive environments reduce casing life and integrity:

        SOUR SERVICE (H2S):

        SULFIDE STRESS CRACKING (SSC):
        - Mechanism: H2S + high-strength steel + tensile stress → brittle fracture
        - Critical concentration: >0.05 psi H2S partial pressure (NACE threshold)
        - Susceptible materials: High-strength carbon steels (P-110, Q-125, V-150)
        - Prevention: Material selection per NACE MR0175/ISO 15156

        NACE MR0175/ISO 15156 MATERIAL REQUIREMENTS:

        Region 0 (< 0.05 psi H2S): No restrictions, standard carbon steel OK

        Region 1 (< 10 psi H2S):
        - Carbon steel: ≤80 ksi yield (L-80, J-55, K-55 acceptable)
        - P-110, Q-125: NOT ALLOWED (SSC risk)

        Region 2 (10-45 psi H2S):
        - Low-alloy steel: 13Cr (modified L-80 Type 13Cr)
        - Hardness limit: ≤22 HRC (prevents SSC)

        Region 3 (> 45 psi H2S):
        - Corrosion-resistant alloys (CRA): 22Cr, 25Cr duplex, Inconel, titanium
        - Carbon steel NOT allowed

        MATERIAL OPTIONS FOR SOUR SERVICE:
        - L-80 Type 1: 80 ksi yield, NACE compliant up to 10 psi H2S
        - 13Cr L-80: Modified chemistry, up to 45 psi H2S
        - 22Cr/25Cr Duplex: High strength + corrosion resistance, > 45 psi H2S
        - CRA Clad: Carbon steel body, CRA inner liner (cost-effective)

        SWEET CORROSION (CO2):

        MECHANISM:
        - CO2 + water → carbonic acid (H2CO3) → metal dissolution
        - Rate depends on: CO2 partial pressure, temperature, flow velocity, water cut

        CORROSION RATE PREDICTION:
        - De Waard-Milliams model: CR = f(pCO2, T, pH)
        - Typical rates: 5-50 mils/year (uninhibited), <2 mils/year (inhibited)

        MITIGATION:
        1. INHIBITOR TREATMENT:
        - Inject corrosion inhibitor (filming amine) continuously or batch
        - Target: <2 mils/year corrosion rate
        - Monitoring: Corrosion coupons, ER (electrical resistance) probes

        2. CORROSION ALLOWANCE:
        - Add extra wall thickness (0.05-0.10 inch) to account for metal loss over well life
        - Design life: 20-30 years typical
        - Example: 10 mils/year × 20 years = 200 mils (0.2 inch) allowance

        3. CRA MATERIALS:
        - 13Cr stainless steel: Good CO2 resistance, cost-effective
        - 22Cr/25Cr duplex: High strength + excellent corrosion resistance
        - Inconel/titanium: Severe environments (HPHT + high CO2)

        COMBINED H2S + CO2:
        - Both present: Sour service requirements govern (NACE MR0175)
        - CO2 accelerates SSC: Use lower yield strength or CRA
        - Field experience: Offset well corrosion data critical

        DESIGN PROCESS:

        1. CHARACTERIZE ENVIRONMENT:
        - H2S partial pressure (psi) from reservoir fluid analysis
        - CO2 partial pressure (psi) from fluid analysis
        - Temperature (affects corrosion rate)
        - Water cut (corrosion requires water phase)

        2. SELECT MATERIAL:
        - If H2S > 0.05 psi: NACE MR0175 material (L-80, 13Cr, CRA)
        - If CO2 only: Carbon steel + inhibitor OR corrosion allowance OR 13Cr
        - If both: Sour service material (NACE governs)

        3. CALCULATE CORROSION ALLOWANCE:
        - Predict uninhibited corrosion rate (De Waard model or lab testing)
        - Multiply by design life (years)
        - Add to wall thickness (e.g., 0.05-0.10 inch)

        4. VERIFICATION:
        - Lab testing: Autoclave corrosion tests with reservoir fluids
        - Field monitoring: Corrosion coupons, ER probes, caliper logs
        - Inhibitor program: Continuous injection or batch treatment

        REGULATORY:
        - NACE MR0175/ISO 15156: Industry standard for sour service (not regulatory, but universally adopted)
        - Some jurisdictions mandate NACE compliance (e.g., offshore regulations)
        """,
        key_factors=[
            "H2S partial pressure (psi) from reservoir fluid",
            "CO2 partial pressure (psi)",
            "Temperature (affects corrosion rate)",
            "Water cut and water chemistry (pH, salinity)",
            "Design well life (years)",
            "Material availability (CRA long lead time, high cost)",
            "Inhibitor program feasibility (continuous injection)",
            "Offset well corrosion experience"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156 - Materials for use in H2S-containing environments",
            "API Specification 5CT - Material grades and properties",
            "NACE RP0775 - Preparation, Installation, Analysis, and Interpretation of Corrosion Coupons",
            "De Waard-Milliams Corrosion Model - CO2 corrosion rate prediction"
        ],
        burden_holder="Operator - must demonstrate material selection appropriate for corrosive environment per NACE standards",
        adversary_position="Conservative reviewer may require CRA materials even for moderate H2S/CO2 if long well life or critical well",
        counter_arguments=[
            "NACE MR0175 compliance with L-80 for H2S partial pressure",
            "Corrosion inhibitor program reduces CO2 corrosion to <2 mils/year",
            "Corrosion allowance added to wall thickness for uninhibited case",
            "Offset well corrosion monitoring shows acceptable rates"
        ],
        resolution_strategy="Characterize reservoir fluids (H2S, CO2, water chemistry); select material per NACE MR0175 if H2S present; calculate corrosion allowance for CO2 environments; consider CRA materials for severe cases (high partial pressures, long life); implement corrosion monitoring program (coupons, ER probes); inhibitor treatment if cost-effective vs CRA.",
        entity_scope="Sour gas wells (H2S), CO2-rich fields, water injection wells, and long-life production wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="NACE MR0175 provides industry-consensus material selection criteria; corrosion rate prediction models have uncertainty (field monitoring recommended); CRA materials proven in severe environments.",
        controlling_precedent="NACE MR0175/ISO 15156 for sour service material selection; API 5CT for material specifications"
    ),

    DoctrineBlock(
        topic="expandable_casing_technology",
        keywords=["expandable", "solid expandable", "mono-bore", "wellbore strengthening", "lost circulation"],
        conclusion_template=[
            "Expandable casing is run at reduced diameter and mechanically expanded in-situ to larger diameter, enabling: elimination of casing strings, wellbore strengthening, and lost circulation remediation.",
            "Applications: Deepwater wells (reduce casing strings), trouble zones (strengthen wellbore), and sidetrack/re-entry (maintain drift).",
            "Limitations: High cost, reduced pressure ratings post-expansion, limited expansion ratio (30-40%), and specialized running procedures."
        ],
        reasoning_framework="""
        Expandable casing overcomes conventional casing size limitations:

        CONVENTIONAL CASING PROBLEM:
        - Each casing string reduces drift ID for next string
        - Deep wells: Run out of hole size (telescoping strings)
        - Example: 26" hole → 20" casing (18.73" drift) → 17.5" hole → 13.375" casing (12.415" drift)
        - Eventually: Cannot reach target depth with desired production casing size

        EXPANDABLE SOLUTION:
        - Run smaller OD casing, expand to larger ID in-situ
        - Example: 13.375" casing expanded to 13.625" ID (vs 12.415" conventional)
        - Eliminates one or more intermediate strings → maintains drift for deeper sections

        EXPANSION PROCESS:

        1. RUN CASING:
        - Expandable casing run on drillpipe or tubing
        - Smaller OD than conventional (e.g., 11.75" expands to 13.375")
        - Special connections: Expandable couplings that expand with pipe body

        2. EXPANSION:
        - Hydraulic or mechanical expansion cone pulled through casing
        - Cone diameter > original ID, plastically deforms casing outward
        - Expansion ratio: 20-40% increase in diameter
        - Force required: 50,000-200,000 lbf depending on size/grade

        3. POST-EXPANSION:
        - Casing remains permanently expanded (plastic deformation)
        - Cement through expanded casing (conventional cementing)
        - Connections expanded and sealed (metal-to-metal interference)

        EXPANSION TYPES:

        SOLID EXPANDABLE:
        - Entire casing string expanded uniformly
        - Applications: Eliminate intermediate string, maintain drift

        LINER HANGER EXPANSION:
        - Expandable liner hanger expanded into previous casing
        - Creates metal-to-metal seal (no cement required for seal)
        - Applications: Sidetrack, lost circulation zones

        PATCH EXPANSION:
        - Short section (50-100 ft) expanded to repair casing damage or seal off zone
        - Applications: Casing repair, lost circulation, water shutoff

        APPLICATIONS:

        1. DEEPWATER WELLS:
        - Eliminate one intermediate string → reduces casing strings from 6-7 to 5-6
        - Cost savings: Fewer strings, smaller BOP, shorter well construction time
        - Enables: Drilling to deeper targets with adequate production casing size

        2. WELLBORE STRENGTHENING:
        - Expand casing across weak formation (lost circulation zone)
        - Strengthens wellbore by creating hoop stress (compression)
        - Increases fracture gradient by 1-2 ppg equivalent

        3. SIDETRACK / RE-ENTRY:
        - Sidetrack through existing casing without reducing drift
        - Expandable liner patch maintains original drift ID
        - Enables: Multiple sidetracks from same parent wellbore

        4. LOST CIRCULATION:
        - Set expandable liner across lost circulation zone
        - Metal-to-metal seal isolates zone without cement
        - Continue drilling with restored circulation

        ADVANTAGES:
        - Mono-bore well design (constant drift ID)
        - Eliminate casing strings (cost, time savings)
        - Wellbore strengthening (increase fracture gradient)
        - Lost circulation remediation

        LIMITATIONS:

        1. COST:
        - 3-5x cost of conventional casing (per foot)
        - Specialized equipment (expansion cone, pulling tool)
        - Justified only when conventional methods fail or impractical

        2. PRESSURE RATINGS:
        - Expansion reduces wall thickness (ID increases, OD constant)
        - Burst/collapse/tension ratings 20-40% lower than conventional
        - Must design for post-expansion ratings, not pre-expansion

        3. EXPANSION RATIO:
        - Limited to 20-40% diameter increase (material ductility limit)
        - Cannot expand 9-5/8" to 13-3/8" (too large a ratio)
        - Must select base size to achieve target expanded ID

        4. RUNNING PROCEDURES:
        - Cannot rotate during expansion (risk of connection failure)
        - Expansion rate controlled (prevent overstressing)
        - Post-expansion inspection (caliper, pressure test)

        5. GRADE LIMITATIONS:
        - Requires high ductility (ability to expand without fracture)
        - Typically limited to L-80, lower-strength grades
        - HPHT applications challenging (need high strength AND ductility)

        DESIGN PROCESS:
        1. Identify application (eliminate string, strengthen wellbore, remediate loss)
        2. Select base casing OD and expansion ratio to achieve target ID
        3. Calculate post-expansion ratings (burst, collapse, tension)
        4. Verify post-expansion ratings meet design requirements
        5. Select expansion equipment (cone size, pulling capacity)
        6. Develop expansion procedure (rate, monitoring, acceptance criteria)
        """,
        key_factors=[
            "Application (eliminate string, wellbore strengthening, lost circulation)",
            "Target expanded ID (maintain drift for next section)",
            "Expansion ratio achievable (20-40% limit)",
            "Post-expansion pressure ratings (reduced vs conventional)",
            "Cost vs conventional approach (3-5x per foot)",
            "Material ductility (L-80 typical, high-strength limited)",
            "Expansion equipment availability",
            "Wellbore conditions (stable vs unstable formations)"
        ],
        primary_authority=[
            "SPE 48942 - Expandable Tubular Technology: Field Applications",
            "API Specification 5CT - Casing grades suitable for expansion",
            "ISO 10427-2 - Expandable Casing",
            "Enventure/Weatherford technical manuals (proprietary expansion systems)"
        ],
        burden_holder="Operator - must demonstrate expandable casing design achieves objectives with acceptable post-expansion ratings",
        adversary_position="Cost-conscious reviewer may challenge necessity vs conventional approach; technical reviewer may question pressure ratings",
        counter_arguments=[
            "Conventional approach not viable (run out of hole size, lost circulation)",
            "Cost-benefit analysis shows net savings (eliminate string, reduce NPT)",
            "Post-expansion ratings adequate for design loads (detailed analysis)",
            "Field performance in similar applications demonstrates success"
        ],
        resolution_strategy="Clear technical justification for expandable vs conventional; detailed design with post-expansion load analysis; vendor qualification data (expansion testing, pressure ratings); cost-benefit analysis; contingency plan if expansion fails (cement, sidetrack).",
        entity_scope="Deepwater wells, challenging lost circulation zones, sidetrack/re-entry operations, and wells approaching hole size limits",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Expandable technology proven in field applications but remains specialized; post-expansion ratings have uncertainty (testing and modeling required); high cost limits applications to cases where conventional methods fail.",
        controlling_precedent="No specific API standard for expandable casing; industry practice based on vendor qualifications and field performance"
    ),

    DoctrineBlock(
        topic="casing_design_software_validation",
        keywords=["Wellcat", "StressCheck", "TDAS", "software validation", "quality control", "hand calculations"],
        conclusion_template=[
            "Casing design software (Wellcat, StressCheck, TDAS, proprietary tools) automates load calculations, optimizes string design, and performs biaxial/triaxial analysis.",
            "Software validation: Spot-check results with hand calculations per API Bulletin 5C3, verify input data (casing properties, mud weights, pressures), and peer review critical designs.",
            "Software is a tool, not a substitute for engineering judgment; understand assumptions and limitations."
        ],
        reasoning_framework="""
        Casing design software streamlines complex calculations:

        COMMON SOFTWARE:
        - Wellcat (Landmark/Halliburton): Industry-standard, comprehensive
        - StressCheck (Baker Hughes): Load analysis, multi-grade optimization
        - TDAS (Drilling Engineering Association): Torque and drag, casing design
        - Proprietary tools: Operator-specific, often integrated with drilling systems

        SOFTWARE CAPABILITIES:

        1. LOAD CALCULATIONS:
        - Burst: Multiple scenarios (gas kick, full evacuation, stimulation)
        - Collapse: Evacuation scenarios, temperature effects
        - Tension: Buoyant weight, bending, shock loads
        - Biaxial/triaxial: Von Mises or API ellipse

        2. STRING OPTIMIZATION:
        - Multi-grade design: Optimize cost vs performance
        - Connection selection: Match load requirements
        - Centralizer placement: Modeling per API RP 10D-2
        - Wear analysis: Predict wear, re-rate casing

        3. SCENARIO ANALYSIS:
        - Sensitivity: Vary input parameters (mud weight, pressure, temperature)
        - What-if: Alternate string designs, grade combinations
        - Risk assessment: Probability of failure for different scenarios

        4. REPORTING:
        - Design summary: Grades, weights, connections, design factors
        - Load plots: Burst, collapse, tension vs depth
        - Margin plots: Design factor vs depth (identify weak points)
        - Regulatory compliance: Format for submission (state, federal)

        VALIDATION PROCESS:

        1. INPUT VERIFICATION:
        - Casing properties: Match API Bulletin 5C2 tables (burst, collapse, tension)
        - Mud weights: Verify vs drilling plan
        - Pressures: Pore pressure and fracture gradient from offset data
        - Temperatures: Geothermal gradient, circulating temp

        2. HAND CALCULATION SPOT-CHECKS:
        - Select critical depth (max load point)
        - Calculate burst/collapse/tension per API Bulletin 5C3 by hand
        - Compare to software result (should match within 1-2%)
        - If discrepancy: Investigate assumptions, software version, input errors

        3. SENSITIVITY ANALYSIS:
        - Vary key inputs (mud weight ±0.5 ppg, pressure ±500 psi)
        - Verify design remains adequate (design factors > minimum)
        - Identify critical variables (largest impact on margin)

        4. PEER REVIEW:
        - Independent engineer reviews design and software output
        - Check: Load scenarios appropriate, design factors adequate, multi-grade transitions logical
        - Particularly important for: HPHT, deepwater, critical wells

        COMMON SOFTWARE ERRORS:

        1. INPUT ERRORS:
        - Wrong casing grade (e.g., J-55 instead of L-80)
        - Incorrect mud weight (drilling mud vs cement slurry)
        - Wrong depth reference (MD vs TVD, KB vs GL)

        2. ASSUMPTION ERRORS:
        - Load case not representative (e.g., no kick scenario included)
        - Temperature profile unrealistic (affects yield strength, buoyancy)
        - Wear percentage too optimistic (actual wear exceeds prediction)

        3. SOFTWARE BUGS:
        - Version-specific issues (check release notes)
        - Rare calculation errors (known issues in some versions)
        - Mitigation: Keep software updated, validate critical results

        4. INTERPRETATION ERRORS:
        - Misreading output (design factor < 1.0 mistaken for > 1.0)
        - Units confusion (psi vs ppg, feet vs meters)
        - Critical zone identification (miss peak load location)

        QUALITY CONTROL CHECKLIST:

        □ Casing properties verified against API tables
        □ Mud weights, pressures, temperatures verified vs plan
        □ Load scenarios cover worst-case (kick, evacuation, etc.)
        □ Hand calculations performed at critical depth
        □ Software results within 2% of hand calculations
        □ Design factors meet minimum (burst 1.1, collapse 1.125, tension 1.6)
        □ Multi-grade transitions logical and optimized
        □ Peer review performed by independent engineer
        □ Design documented and ready for regulatory submission

        ENGINEERING JUDGMENT:

        Software provides calculations, but engineer must:
        - Select appropriate load cases (software doesn't know well history, risks)
        - Choose design factors (software uses defaults, may not be conservative enough)
        - Optimize cost vs safety (software can optimize cost, but engineer sets constraints)
        - Approve final design (software is a tool, not the decision-maker)

        Example: Software says P-110 adequate with 1.0 design factor for burst.
        Engineer decision: Use 1.1 design factor (industry standard) OR upgrade to Q-125 (HPHT well, higher risk).
        Software provides data; engineer makes call.
        """,
        key_factors=[
            "Software selection (Wellcat, StressCheck, proprietary)",
            "Input data quality (casing properties, pressures, mud weights)",
            "Load scenario selection (worst-case vs typical)",
            "Hand calculation validation (spot-check critical depths)",
            "Peer review (independent verification)",
            "Design factor selection (minimum vs recommended vs conservative)",
            "Multi-grade optimization (cost vs performance)",
            "Documentation (audit trail, regulatory submission)"
        ],
        primary_authority=[
            "API Bulletin 5C3 - Formulas and Calculations for Casing (hand calculation reference)",
            "ISO 10400 - Casing and tubing design formulas",
            "Software vendor manuals (Wellcat, StressCheck, TDAS user guides)",
            "Internal QA/QC procedures (operator-specific)"
        ],
        burden_holder="Operator - must validate software results and demonstrate design adequacy",
        adversary_position="Peer reviewer or regulator may question software assumptions or require independent verification",
        counter_arguments=[
            "Industry-standard software (Wellcat) widely accepted",
            "Hand calculations validate software at critical depths",
            "Peer review performed by independent senior engineer",
            "Sensitivity analysis demonstrates design robustness"
        ],
        resolution_strategy="Use industry-accepted software (Wellcat, StressCheck); verify inputs against source data; perform hand calculations at critical depths (within 2% of software); peer review by independent engineer; document assumptions and load scenarios; sensitivity analysis to demonstrate margin; maintain audit trail for regulatory submission.",
        entity_scope="All casing design; software particularly valuable for complex multi-grade strings, HPHT wells, and optimization",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Software calculations based on API/ISO formulas (validated); input errors and assumption errors are primary risks (mitigated by QC process); peer review adds confidence.",
        controlling_precedent="API Bulletin 5C3 for calculation methods; no specific API standard for software validation, but industry practice requires hand-check and peer review"
    ),
]

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

START_TIME = time.time()
QUERY_COUNT = 0
DOCTRINE_HIT_COUNT = defaultdict(int)
RESPONSE_TIMES: List[float] = []

def calculate_determinism_hash(query: str, response: str) -> str:
    """Generate SHA-256 hash for determinism verification."""
    combined = f"{query}||{response}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]

def record_telemetry(triggered: List[str], response_time_ms: float):
    """Record query telemetry."""
    global QUERY_COUNT
    QUERY_COUNT += 1
    for topic in triggered:
        DOCTRINE_HIT_COUNT[topic] += 1
    RESPONSE_TIMES.append(response_time_ms)

def calculate_fragility_score(triggered: List[str]) -> float:
    """Calculate fact fragility score (0.0 = rock solid, 1.0 = highly uncertain)."""
    if not triggered:
        return 0.8

    confidence_map = {
        ConfidenceLevel.DEFENSIBLE: 0.2,
        ConfidenceLevel.AGGRESSIVE: 0.5,
        ConfidenceLevel.DISCLOSURE: 0.7,
        ConfidenceLevel.HIGH_RISK: 0.9
    }

    scores = [confidence_map.get(d.confidence, 0.5) for d in DOCTRINE_CACHE if d.topic in triggered]
    return sum(scores) / len(scores) if scores else 0.5

# ============================================================================
# CORE INTELLIGENCE ENGINE
# ============================================================================

def three_layer_response(query: CasingQuery) -> CasingResponse:
    """
    Three-layer response system:
    Layer 1: Doctrine cache (0-200ms)
    Layer 2: Semantic retrieval (would use vector DB in production)
    Layer 3: Deep analysis (full reasoning)
    """
    start = time.time()

    # Layer 1: Fast doctrine cache lookup
    triggered_doctrines = []
    query_lower = query.question.lower()

    for doctrine in DOCTRINE_CACHE:
        if any(kw.lower() in query_lower for kw in doctrine.keywords):
            triggered_doctrines.append(doctrine.topic)

    # Select best matching doctrines
    relevant_doctrines = [d for d in DOCTRINE_CACHE if d.topic in triggered_doctrines]

    # Build response based on mode
    if query.mode == ResponseMode.FAST:
        answer = build_fast_response(relevant_doctrines, query)
    elif query.mode == ResponseMode.DEFENSE:
        answer = build_defense_response(relevant_doctrines, query)
    else:  # MEMO
        answer = build_memo_response(relevant_doctrines, query)

    # Apply epistemic guardrails
    answer = apply_epistemic_guardrails(answer)

    # Calculate metrics
    response_time_ms = (time.time() - start) * 1000
    fragility = calculate_fragility_score(triggered_doctrines)
    conf = relevant_doctrines[0].confidence if relevant_doctrines else ConfidenceLevel.DISCLOSURE

    response = CasingResponse(
        answer=answer,
        confidence=conf,
        triggered_doctrines=triggered_doctrines,
        response_time_ms=round(response_time_ms, 2),
        determinism_hash=calculate_determinism_hash(query.question, answer),
        zone=determine_analysis_zone(query.question),
        fragility_score=round(fragility, 2),
        audit_trail=[f"Triggered {len(triggered_doctrines)} doctrines", f"Mode: {query.mode}"]
    )

    record_telemetry(triggered_doctrines, response_time_ms)
    return response

def build_fast_response(doctrines: List[DoctrineBlock], query: CasingQuery) -> str:
    """Fast mode: Concise answer with key points."""
    if not doctrines:
        return "No specific casing design doctrine matched. Please provide more details about the design aspect (grade selection, load analysis, seat selection, etc.)."

    primary = doctrines[0]
    response_parts = [
        f"**{primary.topic.replace('_', ' ').title()}**\n",
        "\n".join(primary.conclusion_template),
        f"\n\nKey factors: {', '.join(primary.key_factors[:3])}",
        f"\n\nPrimary authority: {primary.primary_authority[0]}"
    ]

    return "\n".join(response_parts)

def build_defense_response(doctrines: List[DoctrineBlock], query: CasingQuery) -> str:
    """Defense mode: Audit-ready response with citations."""
    if not doctrines:
        return "Insufficient doctrine match for defense-grade analysis."

    primary = doctrines[0]
    response_parts = [
        f"**CASING DESIGN ANALYSIS: {primary.topic.replace('_', ' ').upper()}**\n",
        "**CONCLUSION:**",
        "\n".join(primary.conclusion_template),
        "\n\n**REASONING FRAMEWORK:**",
        primary.reasoning_framework,
        "\n\n**KEY FACTORS:**",
        "\n".join(f"• {factor}" for factor in primary.key_factors),
        "\n\n**PRIMARY AUTHORITY:**",
        "\n".join(f"• {auth}" for auth in primary.primary_authority),
        f"\n\n**CONFIDENCE LEVEL:** {primary.confidence.value}",
        f"\n**CONFIDENCE STRATIFICATION:** {primary.confidence_stratification}",
        f"\n\n**CONTROLLING PRECEDENT:** {primary.controlling_precedent}"
    ]

    return "\n".join(response_parts)

def build_memo_response(doctrines: List[DoctrineBlock], query: CasingQuery) -> str:
    """Memo mode: Comprehensive analysis with all details."""
    if not doctrines:
        return "No matching doctrines for comprehensive memo."

    primary = doctrines[0]
    response_parts = [
        f"# CASING DESIGN MEMORANDUM\n## {primary.topic.replace('_', ' ').title()}\n",
        "### EXECUTIVE SUMMARY",
        "\n".join(primary.conclusion_template),
        "\n\n### DETAILED ANALYSIS",
        primary.reasoning_framework,
        "\n\n### KEY DESIGN FACTORS",
        "\n".join(f"{i+1}. {factor}" for i, factor in enumerate(primary.key_factors)),
        "\n\n### REGULATORY FRAMEWORK & AUTHORITY",
        "\n".join(f"• {auth}" for auth in primary.primary_authority),
        "\n\n### DESIGN RESPONSIBILITY",
        f"**Burden Holder:** {primary.burden_holder}",
        "\n\n### ADVERSARY POSITIONS & COUNTER-ARGUMENTS",
        f"**Potential Challenge:** {primary.adversary_position}",
        "\n\n**Counter-Arguments:**",
        "\n".join(f"• {arg}" for arg in primary.counter_arguments),
        "\n\n### RESOLUTION STRATEGY",
        primary.resolution_strategy,
        f"\n\n### CONFIDENCE ASSESSMENT",
        f"**Level:** {primary.confidence.value}",
        f"\n**Stratification:** {primary.confidence_stratification}",
        f"\n\n**Controlling Precedent:** {primary.controlling_precedent}",
        f"\n\n**Applicable Scope:** {primary.entity_scope}"
    ]

    return "\n".join(response_parts)

def apply_epistemic_guardrails(text: str) -> str:
    """Apply epistemic guardrails - remove banned overconfident phrases."""
    for phrase in BANNED_PHRASES:
        text = text.replace(phrase, "[EPISTEMIC GUARDRAIL: overconfident claim removed]")

    return text

def determine_analysis_zone(question: str) -> AnalysisZone:
    """Determine if question is PLANNING, DESIGN, or AUDIT zone."""
    question_lower = question.lower()
    if any(word in question_lower for word in ["plan", "estimate", "predict", "future"]):
        return AnalysisZone.PLANNING
    elif any(word in question_lower for word in ["audit", "review", "verify", "check", "compliance"]):
        return AnalysisZone.AUDIT
    else:
        return AnalysisZone.DESIGN

# ============================================================================
# API ENDPOINTS
# ============================================================================

@APP.post("/query", response_model=CasingResponse)
async def query_engine(query: CasingQuery):
    """Main query endpoint - TIE-20 three-layer response."""
    try:
        logger.info(f"Query received: {query.question[:100]}... | Mode: {query.mode}")
        response = three_layer_response(query)
        logger.info(f"Response generated: {response.response_time_ms}ms | Doctrines: {len(response.triggered_doctrines)}")
        return response
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthStatus)
async def health_check():
    """Health endpoint - comprehensive status."""
    return HealthStatus(
        status="operational",
        version="1.0.0",
        port=9014,
        doctrines_loaded=len(DOCTRINE_CACHE),
        cache_size=len(DOCTRINE_CACHE),
        uptime_seconds=round(time.time() - START_TIME, 2)
    )

@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
        "by_category": {
            cat.value: [d.topic for d in DOCTRINE_CACHE if cat.value.lower() in d.topic.lower()]
            for cat in IssueCategory
        }
    }

@APP.get("/metrics")
async def get_metrics():
    """Get telemetry metrics."""
    avg_response = sum(RESPONSE_TIMES) / len(RESPONSE_TIMES) if RESPONSE_TIMES else 0
    return {
        "queries_processed": QUERY_COUNT,
        "avg_response_time_ms": round(avg_response, 2),
        "doctrine_hit_counts": dict(DOCTRINE_HIT_COUNT),
        "most_triggered": sorted(DOCTRINE_HIT_COUNT.items(), key=lambda x: x[1], reverse=True)[:5],
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }

@APP.get("/")
async def root():
    """Root endpoint - engine info."""
    return {
        "engine": "DRL04 - Casing Design & Selection Engine",
        "version": "1.0.0",
        "status": "operational",
        "doctrines": len(DOCTRINE_CACHE),
        "port": 9014,
        "endpoints": ["/query", "/health", "/doctrines", "/metrics"]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info("DRL04 Casing Design Engine starting on port 9014...")
    uvicorn.run(APP, host="0.0.0.0", port=9014)
