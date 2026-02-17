"""
CHEM19 Process Safety Intelligence Engine v1.0.0
TIE-Grade Chemical Process Safety Analysis System

Domain: Chemical process hazard identification (HAZOP, What-If, LOPA), consequence
analysis (dispersion, fire, explosion modeling), relief system design (API 520/521),
dust explosion prevention, OSHA PSM compliance (29 CFR 1910.119), EPA RMP, inherently
safer design principles, reactivity hazard assessment (DIERS).

Port: 9301
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS & DATA MODELS
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
    HAZOP = "HAZOP"
    LOPA = "LOPA"
    CONSEQUENCE = "CONSEQUENCE"
    RELIEF_SYSTEM = "RELIEF_SYSTEM"
    DUST_EXPLOSION = "DUST_EXPLOSION"
    REACTIVITY = "REACTIVITY"
    PSM_COMPLIANCE = "PSM_COMPLIANCE"
    ISD = "ISD"
    MOC = "MOC"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Process safety analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    include_authorities: bool = Field(default=True, description="Include regulatory citations")
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class QueryResponse(BaseModel):
    query_id: str
    timestamp: str
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    zone: AnalysisZone
    triggered_doctrines: List[str]
    authorities: List[str]
    warnings: List[str]
    response_time_ms: float
    determinism_hash: str


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    avg_response_ms: float
    cache_hit_rate: float


# ============================================================================
# DOCTRINE BLOCKS - REAL PROCESS SAFETY EXPERTISE
# ============================================================================

class DoctrineBlock:
    """Process safety doctrine with regulatory authority and technical reasoning."""

    def __init__(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: str,
        reasoning_framework: str,
        key_factors: List[str],
        primary_authority: List[str],
        confidence: ConfidenceLevel,
        category: IssueCategory,
        safeguards: Optional[List[str]] = None,
        calculation_methods: Optional[List[str]] = None
    ):
        self.topic = topic
        self.keywords = [k.lower() for k in keywords]
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.category = category
        self.safeguards = safeguards or []
        self.calculation_methods = calculation_methods or []
        self.trigger_count = 0
        self.last_triggered = None


# ============================================================================
# DOCTRINE CACHE - 30+ EXPERT PROCESS SAFETY BLOCKS
# ============================================================================

DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="HAZOP Node Selection and Deviation Analysis",
        keywords=["hazop", "node", "deviation", "guideword", "parameter", "process safety", "hazard identification"],
        conclusion_template="HAZOP nodes should be selected at points where process parameters change (pumps, reactors, separators, heat exchangers). For each node, apply guidewords (NO, MORE, LESS, REVERSE, PART OF, OTHER THAN) to design intent parameters (flow, pressure, temperature, level, composition) to identify deviations. Document cause-consequence-safeguard for each credible scenario.",
        reasoning_framework="""
HAZOP (Hazard and Operability Study) is the gold standard for process hazard identification:

1. Node Selection Criteria:
   - Equipment where reactions occur (reactors, mixers)
   - Equipment where phase changes occur (distillation columns, evaporators)
   - Major equipment interfaces (pump suction/discharge, heat exchanger inlet/outlet)
   - Points where composition changes (feed points, product takeoff)
   - Critical utilities (cooling water supply, instrument air)

2. Guideword Application:
   - NO/NOT: Complete absence (no flow, no agitation, no cooling)
   - MORE: Quantitative increase (higher flow, pressure, temperature, level)
   - LESS: Quantitative decrease (lower flow, pressure, temperature, level)
   - REVERSE: Logical opposite (backflow, reverse rotation)
   - PART OF: Qualitative decrease (wrong composition, contamination, impurity)
   - OTHER THAN: Complete substitution (wrong material, wrong operating step)

3. Consequence Severity Ranking (typical):
   - Category 1: Fatality or permanent total disability
   - Category 2: Disabling injury, major property damage (over $100K)
   - Category 3: Medical treatment injury, property damage ($10K-$100K)
   - Category 4: First aid injury, minor property damage (under $10K)

4. Safeguard Effectiveness:
   - Inherent: Eliminates hazard by design (lower inventory, lower temperature)
   - Passive: No moving parts (dikes, relief devices, flame arrestors)
   - Active: Requires action (automated shutdown, alarms, operator response)
   - Procedural: Administrative controls (permits, inspections, training)

5. HAZOP Team Composition:
   - Chairperson (experienced HAZOP facilitator, not line manager)
   - Process engineer (design authority)
   - Operations representative (understands actual plant behavior)
   - Maintenance representative (equipment failure modes)
   - Instrumentation engineer (control system logic)
   - Scribe (documents findings systematically)

6. Documentation Requirements (OSHA PSM):
   - Node description and P&ID boundaries
   - Design intent for each parameter
   - Deviation statement (guideword + parameter)
   - Causes (equipment failure, human error, external event)
   - Consequences (safety, environmental, business)
   - Existing safeguards (preventive and mitigative)
   - Risk ranking (before and after safeguards)
   - Recommendations with action party and due date
        """,
        key_factors=[
            "Node boundary definition on P&IDs",
            "Design intent clarity for each parameter",
            "Guideword systematic application to all parameters",
            "Credible cause identification (not just possible)",
            "Consequence modeling for high-severity scenarios",
            "Safeguard credit only for functioning systems",
            "Independent Protection Layer (IPL) identification for LOPA follow-up"
        ],
        primary_authority=[
            "IEC 61882:2016 Hazard and operability studies (HAZOP studies) - Application guide",
            "CCPS Guidelines for Hazard Evaluation Procedures, 3rd Edition",
            "OSHA 29 CFR 1910.119(e) Process Hazard Analysis"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.HAZOP,
        safeguards=[
            "High/low pressure alarms and interlocks",
            "Temperature alarms and automatic cooling/heating shutdown",
            "Level alarms and overflow protection",
            "Flow meters with low flow alarms",
            "Composition analyzers with out-of-spec alarms",
            "Automated shutdown systems (ESD, SIS)",
            "Relief valves and rupture disks",
            "Operator procedures and training"
        ]
    ),

    DoctrineBlock(
        topic="LOPA Independent Protection Layer Criteria",
        keywords=["lopa", "ipl", "layers of protection", "pfd", "probability", "initiating event", "risk reduction"],
        conclusion_template="An Independent Protection Layer (IPL) must meet strict criteria: effectiveness (PFD 0.01 to 0.001), independence from initiating event and other IPLs, auditability (proof testing), and management system to maintain effectiveness. Common IPLs include process design (inherent safety), basic process control (BPCS if independent), alarms with operator response, SIS/interlock systems, physical protection (relief devices), and post-release mitigation.",
        reasoning_framework="""
Layer of Protection Analysis (LOPA) is a semi-quantitative risk assessment method:

1. IPL Effectiveness Criteria (PFD = Probability of Failure on Demand):
   - Category A: PFD 0.1 (10x risk reduction) - Operator supervision, standard procedures
   - Category B: PFD 0.01 (100x risk reduction) - Operator response to alarm, check valves
   - Category C: PFD 0.001 (1000x risk reduction) - SIS/interlock SIL 1, relief valve
   - Category D: PFD 0.0001 (10000x risk reduction) - SIS/interlock SIL 2, blast walls
   - Category E: PFD 0.00001 (100000x risk reduction) - SIS/interlock SIL 3

2. Independence Requirements:
   - IPL must not be affected by the initiating event or its immediate consequences
   - IPL must not share sensors, logic solvers, or final elements with BPCS
   - IPL must not rely on the same utility as the failed system
   - Example VIOLATION: Using same temperature sensor for BPCS control and SIS shutdown
   - Example VALID: Separate high-temperature switch (independent sensor) for SIS

3. Auditability (Proof Testing):
   - IPL must be testable to verify it will function on demand
   - Test frequency based on required PFD (higher SIL = more frequent testing)
   - Test must reveal dangerous failures (not just nuisance trips)
   - Example: Relief valve set pressure verification every 3-5 years
   - Example: SIS partial stroke testing quarterly, full function test annually

4. Common Initiating Events and Frequencies:
   - Pump failure: 1 per year (1E-0)
   - Control valve failure: 0.1 per year (1E-1)
   - Instrument failure: 0.1 per year (1E-1)
   - Heat exchanger tube rupture: 0.01 per year (1E-2)
   - Operator error (per task): 0.01 per task (1E-2)
   - External event (lightning, vehicle impact): Site-specific

5. LOPA Calculation Example:
   Scenario: Cooling water loss to exothermic reactor causes runaway
   - Initiating Event (cooling water pump failure): 1E-0 per year
   - IPL 1 (High temperature alarm + operator action): PFD 0.01
   - IPL 2 (SIS high-high temperature shutdown): PFD 0.001
   - IPL 3 (Relief valve): PFD 0.01
   - Mitigated Risk = 1E-0 * 0.01 * 0.001 * 0.01 = 1E-7 per year
   - Typical Risk Tolerance: 1E-4 to 1E-6 per year for fatality
   - Conclusion: Risk acceptable (1E-7 < 1E-6)

6. IPL Credit Denial - Common Mistakes:
   - BPCS alarm relying on same sensor that could fail (not independent)
   - Operator response time too short (under 10 minutes = no credit)
   - Relief valve undersized or wrong set pressure (not effective)
   - Maintenance procedures not enforced (not auditable)
   - Secondary containment with no drain or overfill risk (not effective)
        """,
        key_factors=[
            "IPL effectiveness quantified as PFD (not just yes/no)",
            "Independence from initiating event and other IPLs",
            "Auditability through proof testing and documentation",
            "Management system to maintain IPL over time",
            "Credit only for functioning, tested, and maintained systems",
            "SIL rating appropriate to risk reduction required",
            "Operator response time realistic (typically 10-20 minutes minimum)"
        ],
        primary_authority=[
            "CCPS Layer of Protection Analysis: Simplified Process Risk Assessment",
            "IEC 61511 Functional safety - Safety instrumented systems for the process industry",
            "ISA-84.00.01-2004 (IEC 61511 Mod) Application of Safety Instrumented Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.LOPA,
        calculation_methods=[
            "Mitigated Event Frequency = Initiating Event Frequency * Product of IPL PFDs",
            "Risk = Mitigated Event Frequency * Consequence Severity",
            "Required SIL = log10(Risk without SIS / Risk tolerance)"
        ]
    ),

    DoctrineBlock(
        topic="Consequence Modeling - Toxic Gas Dispersion",
        keywords=["dispersion", "toxic release", "gaussian", "dense gas", "chlorine", "ammonia", "hydrogen sulfide", "downwind concentration"],
        conclusion_template="Toxic gas dispersion modeling predicts downwind concentration vs. distance and time after release. Use Gaussian plume models for neutrally buoyant gases (similar density to air). Use dense gas models (SLAB, DEGADIS) for heavier-than-air gases (chlorine, propane, hydrogen fluoride). Key inputs: release rate, molecular weight, atmospheric stability (Pasquill-Gifford class), wind speed, surface roughness. Output: concentration isopleths at ERPG-1, ERPG-2, ERPG-3 levels.",
        reasoning_framework="""
Toxic gas dispersion consequence modeling methodology:

1. Release Rate Determination:
   - Catastrophic rupture: Q = Cd * A * SQRT(2 * rho * (P - Patm))
     Where Cd = discharge coefficient (0.6-0.8), A = hole area, rho = liquid density, P = storage pressure
   - Gas jet release: Q = Cd * A * P * SQRT(MW / (Z * R * T))
     Where MW = molecular weight, Z = compressibility, R = gas constant, T = temperature
   - Evaporation from pool: Q = k * A * (Psat - Pa) * MW / (R * T)
     Where k = mass transfer coefficient, A = pool area, Psat = saturation vapor pressure

2. Atmospheric Stability Classes (Pasquill-Gifford):
   - Class A: Very unstable (strong daytime heating, light wind)
   - Class B: Unstable (moderate daytime heating)
   - Class C: Slightly unstable (weak daytime heating)
   - Class D: Neutral (overcast day or night, or moderate wind)
   - Class E: Slightly stable (nighttime, light wind)
   - Class F: Very stable (clear night, calm wind)
   - Worst case for toxic release: Class F (stable, low wind = minimal dilution)

3. Gaussian Plume Model (neutrally buoyant gas):
   C(x,y,z) = (Q / (2*pi*u*sigma_y*sigma_z)) * exp(-y^2 / (2*sigma_y^2)) * exp(-(z-H)^2 / (2*sigma_z^2))
   Where:
   - C = concentration (kg/m^3)
   - Q = release rate (kg/s)
   - u = wind speed (m/s)
   - sigma_y, sigma_z = dispersion coefficients (function of downwind distance and stability)
   - H = effective release height (m)
   Limitations: Assumes steady-state, flat terrain, constant wind, neutrally buoyant gas

4. Dense Gas Effects (slumping and gravity spreading):
   - Gases heavier than air (MW > 29) or cold gases (liquefied) initially spread along ground
   - Higher concentrations at ground level than Gaussian would predict
   - Dense gas models: SLAB (EPA), DEGADIS (DOE), PHAST, ALOHA
   - Transition to Gaussian behavior as gas warms and dilutes (Richardson number < 0.03)

5. Toxic Endpoint Concentrations (ERPG - Emergency Response Planning Guidelines):
   - ERPG-1: Mild, reversible health effects (odor, irritation)
   - ERPG-2: Irreversible or serious health effects (cannot escape)
   - ERPG-3: Life-threatening effects (1-hour exposure)
   Examples:
   - Chlorine: ERPG-1 = 1 ppm, ERPG-2 = 3 ppm, ERPG-3 = 20 ppm
   - Ammonia: ERPG-1 = 25 ppm, ERPG-2 = 150 ppm, ERPG-3 = 750 ppm
   - H2S: ERPG-1 = 0.1 ppm, ERPG-2 = 30 ppm, ERPG-3 = 100 ppm

6. Worst-Case vs. Alternative Scenario (EPA RMP Rule):
   - Worst-case: Largest vessel, worst weather (F stability, 1.5 m/s wind), total release in 10 min
   - Alternative: More realistic scenario (piping failure, D stability, 3 m/s wind, passive mitigation credit)
   - Must model both and report distances to toxic endpoints
        """,
        key_factors=[
            "Release rate from vessel or piping failure",
            "Gas density relative to air (dense gas models for heavy gases)",
            "Atmospheric stability (F class worst case for low dilution)",
            "Wind speed (lower = less dilution, longer travel distance)",
            "Surface roughness (urban vs. rural terrain)",
            "Toxic endpoint concentration (ERPG-2 or ERPG-3)",
            "Passive mitigation credit (water spray curtains, foam application)"
        ],
        primary_authority=[
            "EPA 40 CFR Part 68 Risk Management Program Rule (RMP)",
            "CCPS Guidelines for Use of Vapor Cloud Dispersion Models, 2nd Edition",
            "ALOHA (Areal Locations of Hazardous Atmospheres) - EPA/NOAA dispersion model"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CONSEQUENCE,
        calculation_methods=[
            "Gaussian plume for neutrally buoyant gas",
            "SLAB or DEGADIS for dense gas (heavier than air)",
            "Pool evaporation rate for liquid spills",
            "Pasquill-Gifford sigma_y and sigma_z coefficients"
        ]
    ),

    DoctrineBlock(
        topic="Consequence Modeling - Fire and Thermal Radiation",
        keywords=["fire", "pool fire", "jet fire", "bleve", "fireball", "thermal radiation", "flame length", "heat flux"],
        conclusion_template="Fire consequence modeling calculates thermal radiation heat flux at specified distances. Pool fire: burning liquid pool with height/diameter ratio typically 1.5-3.0, flame tilt from wind. Jet fire: high-pressure gas/liquid jet ignites, impinges on equipment. BLEVE (Boiling Liquid Expanding Vapor Explosion): catastrophic vessel failure with fireball, typically from external fire weakening vessel. Model outputs: heat flux (kW/m^2) vs. distance, used to assess injury (1st/2nd/3rd degree burns) and equipment damage.",
        reasoning_framework="""
Fire and thermal radiation consequence modeling:

1. Pool Fire Modeling:
   - Burning rate: m_dot = A_pool * m_double_prime
     Where m_double_prime = mass burning rate per unit area (kg/m^2/s, chemical-specific)
     Examples: Gasoline 0.055 kg/m^2/s, Methanol 0.017 kg/m^2/s, LNG 0.14 kg/m^2/s

   - Flame height: L = 42 * D * (m_dot / (rho_air * g^0.5 * D^2.5))^0.61
     Where D = pool diameter (m), rho_air = air density (1.2 kg/m^3), g = 9.81 m/s^2
     Typical L/D ratio: 1.5 to 3.0 for hydrocarbon pool fires

   - Surface Emissive Power (SEP): E = eta * Hc * m_dot / A_flame
     Where eta = radiative fraction (0.1-0.4), Hc = heat of combustion (kJ/kg)
     Typical SEP: 20-160 kW/m^2 (higher for smoky fires like diesel)

   - Heat Flux at distance r: q = E * F_view * tau_atm
     Where F_view = view factor (geometric), tau_atm = atmospheric transmissivity (0.7-1.0)

2. Jet Fire Modeling:
   - Flame length: L = 5.3 * m_dot^0.4 * (DP)^0.2
     Where m_dot = mass flow rate (kg/s), DP = pressure difference (bar)
   - Lift-off distance (for gases): X_lift = 5 * d_jet
   - Surface emissive power: Typically 150-350 kW/m^2 (much higher than pool fire)
   - Impingement heat flux: Up to 250 kW/m^2 if jet impinges on equipment

3. BLEVE (Boiling Liquid Expanding Vapor Explosion):
   - Fireball diameter: D_fb = 5.8 * M_fuel^0.333
     Where M_fuel = mass of fuel in vessel (kg), D_fb in meters
   - Fireball duration: t_fb = 0.45 * M_fuel^0.333 (seconds)
   - Fireball height: H_fb = 0.75 * D_fb (center of fireball above ground)
   - Surface emissive power: 200-350 kW/m^2 during fireball duration
   - Heat flux at distance r from fireball center: Same view factor calculation as pool fire
   - BLEVE triggers: External fire heating vessel, loss of pressure relief, overfilling

4. Thermal Radiation Injury Thresholds:
   - 1.4 kW/m^2: Pain threshold after 30 seconds
   - 4.7 kW/m^2: 1st degree burns (minor) after 30 sec, 2nd degree (blistering) after 20 sec
   - 9.5 kW/m^2: 2nd degree burns after 10 sec, 3rd degree (life-threatening) after 10-20 sec
   - 12.6 kW/m^2: 1% lethality (severe burns)
   - 25 kW/m^2: 50% lethality, thin steel structures ignite
   - 37.5 kW/m^2: 100% lethality if exposed for duration
   - Equipment damage: 12.6 kW/m^2 = plastic pipes fail, 15.8 kW/m^2 = PVC ignites, 25 kW/m^2 = wood ignites

5. Passive Fire Protection (PFP) Design:
   - PFP coating thickness based on required endurance time (typically 1-2 hours)
   - Endurance time = time for steel to reach 550 deg C (critical temperature)
   - Heat flux used to calculate PFP thickness: q = (T_flame - T_steel) / (R_PFP + R_convection)
   - Jet fire impingement: Much higher heat flux than pool fire, requires thicker PFP

6. View Factor Calculation (point source approximation):
   - F_view = (1 / (4*pi*r^2)) for small flames or distant observer
   - For large flames: Must integrate over flame surface (cylindrical or spherical geometry)
   - Conservative assumption: Assume entire flame radiates uniformly at SEP
        """,
        key_factors=[
            "Fuel type (affects burning rate and radiative fraction)",
            "Pool diameter or jet release rate",
            "Flame height and tilt from wind",
            "Surface emissive power (SEP) for fuel type",
            "Distance from flame to receptor",
            "Atmospheric transmissivity (humidity, smoke absorption)",
            "Injury or equipment damage threshold heat flux"
        ],
        primary_authority=[
            "CCPS Guidelines for Evaluating the Characteristics of Vapor Cloud Explosions, Flash Fires, and BLEVEs",
            "API 521 Pressure-relieving and Depressuring Systems (fire relief sizing)",
            "NFPA 30 Flammable and Combustible Liquids Code"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CONSEQUENCE,
        calculation_methods=[
            "Pool fire: SEP = eta * Hc * m_double_prime, q = SEP * F_view * tau_atm",
            "Jet fire: L = 5.3 * m_dot^0.4 * DP^0.2",
            "BLEVE fireball: D_fb = 5.8 * M_fuel^0.333",
            "View factor integration over flame surface"
        ]
    ),

    DoctrineBlock(
        topic="Consequence Modeling - Vapor Cloud Explosion (VCE)",
        keywords=["vce", "vapor cloud explosion", "overpressure", "tnt equivalency", "multi-energy", "congestion", "confinement", "blast"],
        conclusion_template="Vapor Cloud Explosion (VCE) models predict blast overpressure from ignition of unconfined flammable vapor. TNT equivalency method uses simple 1-10% efficiency factor but overpredicts far-field. Multi-Energy method (Baker-Strehlow-Tang) accounts for congestion and confinement, giving more accurate near-field overpressure. Congestion (piping, equipment) accelerates flame, increasing overpressure. Confinement (buildings, structures) prevents pressure relief. Typical injury thresholds: 0.14 bar (2 psi) eardrum rupture, 0.34 bar (5 psi) lung damage, 0.69 bar (10 psi) 50% lethality.",
        reasoning_framework="""
Vapor Cloud Explosion (VCE) consequence modeling approaches:

1. TNT Equivalency Method (simple, conservative):
   - Assumes fraction of fuel energy converts to blast (TNT yield efficiency)
   - TNT equivalent mass: M_TNT = eta_TNT * M_fuel * (Hc / Hc_TNT)
     Where eta_TNT = 1-10% (typically 5%), Hc = heat of combustion of fuel (kJ/kg), Hc_TNT = 4680 kJ/kg
   - Scaled distance: Z = R / (M_TNT^(1/3))
     Where R = distance (m), M_TNT in kg TNT
   - Overpressure from scaled distance curves (Kingery-Bulmash or simplified)
   - LIMITATION: Overpredicts far-field overpressure (cloud burns, doesn't detonate like TNT)

2. Multi-Energy Method (Baker-Strehlow-Tang, more accurate):
   - Divide vapor cloud into zones by congestion level:
     * Zone 1: Highly congested (flame speed 50-150 m/s, overpressure 0.5-3 bar)
     * Zone 2: Moderately congested (flame speed 20-50 m/s, overpressure 0.1-0.5 bar)
     * Zone 3: Lightly congested (flame speed 5-20 m/s, overpressure 0.01-0.1 bar)
     * Zone 4: Unconfined (flame speed 1-5 m/s, overpressure < 0.01 bar)
   - Energy in each zone: E_zone = M_fuel_zone * Hc * eta_combustion
     Where eta_combustion = 0.03 (3% of fuel energy for Zone 1, less for other zones)
   - Overpressure: P = f(E_zone, R, flame_speed)
     Use Baker-Strehlow-Tang charts or equations
   - Sum overpressure contributions from all zones

3. Congestion and Confinement Effects:
   - Congestion: Obstacles (pipes, vessels, structures) increase turbulence and flame acceleration
     * Blockage ratio: BR = A_obstructed / A_total (BR > 0.4 = high congestion)
     * Pitch (spacing between obstacles): Smaller pitch = higher flame speed
   - Confinement: Walls or ceilings prevent pressure relief, increasing overpressure
     * Open cloud (outdoors): Pressure relief in all directions (lower overpressure)
     * Partially confined (building with openings): Intermediate overpressure
     * Fully confined (closed building): Maximum overpressure (approaches detonation)

4. Overpressure Injury and Damage Thresholds:
   - 0.03 bar (0.5 psi): Minor structural damage (windows shatter)
   - 0.07 bar (1 psi): Partial building collapse (wood frame structures)
   - 0.14 bar (2 psi): Eardrum rupture (50% probability)
   - 0.21 bar (3 psi): Serious building damage, 1% lethality from debris
   - 0.34 bar (5 psi): Lung damage threshold, building collapse
   - 0.48 bar (7 psi): 50% lethality from lung damage
   - 0.69 bar (10 psi): 90% lethality, heavily reinforced concrete damage
   - 1.0 bar (14.5 psi): Total building destruction

5. Flammability and Ignition Probability:
   - Flammable mass: Only fuel within flammable limits (LFL to UFL) can burn
   - Lower Flammable Limit (LFL): Minimum concentration for combustion (typically 1-5% for hydrocarbons)
   - Upper Flammable Limit (UFL): Maximum concentration (typically 10-15%)
   - Ignition probability: Function of ignition sources (static, hot surfaces, open flame)
     * Immediate ignition: Flash fire (no overpressure, thermal radiation only)
     * Delayed ignition (after cloud disperses): VCE (overpressure hazard)

6. Mitigation Strategies:
   - Reduce inventory (smaller cloud = less energy)
   - Increase ventilation (dilute below LFL before ignition)
   - Remove congestion (clear area around high-risk equipment)
   - Eliminate ignition sources (hot work permits, electrical classification)
   - Blast-resistant buildings for control rooms (designed for 0.34-0.69 bar overpressure)
        """,
        key_factors=[
            "Mass of flammable fuel within LFL-UFL range",
            "Congestion level (blockage ratio, pitch)",
            "Confinement (open vs. enclosed space)",
            "Flame speed (function of congestion and fuel reactivity)",
            "Distance from explosion center to receptor",
            "Overpressure injury or structural damage threshold",
            "Ignition probability and timing (immediate vs. delayed)"
        ],
        primary_authority=[
            "CCPS Guidelines for Evaluating the Characteristics of Vapor Cloud Explosions, Flash Fires, and BLEVEs",
            "Baker-Strehlow-Tang (BST) Vapor Cloud Explosion Model",
            "API RP 752 Management of Hazards Associated with Location of Process Plant Permanent Buildings"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CONSEQUENCE,
        calculation_methods=[
            "TNT equivalency: M_TNT = eta_TNT * M_fuel * (Hc / 4680), Z = R / M_TNT^(1/3)",
            "Multi-Energy: E_zone = M_fuel_zone * Hc * eta_combustion, use BST charts",
            "Overpressure from scaled distance or BST method"
        ]
    ),

    DoctrineBlock(
        topic="Relief Valve Sizing - Fire Case (API 520/521)",
        keywords=["relief valve", "fire case", "api 520", "api 521", "wetted surface", "heat input", "required relief capacity"],
        conclusion_template="Fire case relief sizing (API 521) protects vessel from overpressure during external fire exposure. Heat input Q = C * F * A_wetted^0.82, where C = 21000 for uninsulated, 12600 for 2 inch insulation, F = environment factor (1.0 typical). Required relief capacity W = Q / latent_heat for pure component, or W = Q / (Cp * (T_relief - T_feed)) for non-vaporizing liquid. Size relief valve to pass W at set pressure (typically 10% over MAWP).",
        reasoning_framework="""
Relief valve sizing for fire exposure (API 521 methodology):

1. Wetted Surface Area Calculation:
   - Vertical vessel: A_wetted = pi * D * H_liquid + (pi/4) * D^2 (bottom head)
     Where D = vessel diameter, H_liquid = liquid height
   - Horizontal vessel: A_wetted = more complex (use API 521 charts or formula)
   - Spherical vessel: A_wetted = pi * D^2 (entire sphere if over 50% full)
   - CRITICAL: Only count wetted surface. Vapor space is not wetted.

2. Heat Input from Fire:
   - API 521 Formula: Q = C * F * A_wetted^0.82
     Where:
     * Q = heat input (Btu/hr or W)
     * C = coefficient (21000 Btu/hr/ft^1.64 for bare steel, 12600 for 2 inch insulation)
     * F = environment factor (1.0 typical, 0.5 for good drainage, 0.3 for water spray)
     * A_wetted in ft^2 (multiply by 0.82 exponent)
   - SI Units: Q (W) = C * F * A_wetted^0.82, C = 43200 W/m^1.64 for bare, 26000 for insulated

3. Required Relief Capacity:
   - Vaporizing liquid (pure component or azeotrope):
     W = Q / lambda
     Where W = relief rate (kg/hr), lambda = latent heat of vaporization (kJ/kg)

   - Non-vaporizing liquid (thermal expansion):
     W = Q / (Cp * (T_relief - T_feed))
     Where Cp = specific heat (kJ/kg/K), T_relief = relief valve set temp, T_feed = feed temp

   - Supercritical fluid (no phase change):
     W = Q / (H_relief - H_feed)
     Where H = specific enthalpy (kJ/kg)

4. Relief Valve Orifice Area (API 520):
   - Gas/vapor service: A = (W / (Kd * P1 * Kb * Kc)) * SQRT((T * Z) / M)
     Where:
     * A = orifice area (mm^2)
     * W = flow rate (kg/hr)
     * Kd = discharge coefficient (0.975 for API nozzle)
     * P1 = upstream relieving pressure (kPa absolute) = set pressure + overpressure + atmospheric
     * Kb = capacity correction for back pressure (1.0 for conventional, chart for balanced bellows)
     * Kc = combination correction (typically 1.0)
     * T = relieving temperature (K)
     * Z = compressibility factor
     * M = molecular weight

   - Liquid service: A = (W / (Kd * Kw * Kv)) * SQRT(1 / (rho * DP))
     Where:
     * Kw = correction for back pressure (0.9 typical)
     * Kv = correction for viscosity (1.0 for low viscosity)
     * rho = liquid density (kg/m^3)
     * DP = set pressure - back pressure (kPa)

5. Set Pressure Selection:
   - Typically 10% above MAWP (Maximum Allowable Working Pressure)
   - Accumulation allowed: 21% for fire case (ASME Section VIII)
   - Example: MAWP 10 barg, set pressure 11 barg, max relieving pressure 12.1 barg

6. Fire Protection Credit (Passive Fire Protection - PFP):
   - PFP coating (intumescent, cementitious) increases time to vessel failure
   - If PFP rated for 2+ hours endurance, can reduce required relief capacity
   - API 521: May reduce heat input by 50% if PFP prevents vessel reaching 650 deg F (343 deg C)
   - WARNING: PFP must be inspected and maintained (damage from corrosion, impact)

7. Depressuring System (alternative to relief valve):
   - Blow down valve opens on high pressure, rapidly depressures vessel
   - Reduces heat input by lowering boiling temperature
   - Common for high-pressure vessels where relief valve would be very large
   - Must calculate depressuring rate to keep vessel pressure below MAWP during fire
        """,
        key_factors=[
            "Wetted surface area (only liquid-covered surfaces count)",
            "Insulation thickness (reduces heat input by ~40%)",
            "Environment factor F (drainage, water spray mitigation)",
            "Latent heat of vaporization for pure components",
            "Relief valve set pressure (typically MAWP + 10%)",
            "Accumulation limit (21% for fire case per ASME)",
            "Back pressure effects on relief valve capacity"
        ],
        primary_authority=[
            "API 520 Sizing, Selection, and Installation of Pressure-Relieving Devices, Part I - Sizing and Selection",
            "API 521 Pressure-Relieving and Depressuring Systems, 6th Edition",
            "ASME Boiler and Pressure Vessel Code, Section VIII Division 1, UG-125 through UG-136"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RELIEF_SYSTEM,
        calculation_methods=[
            "Q = C * F * A_wetted^0.82 (heat input from fire)",
            "W = Q / lambda (vaporizing liquid relief rate)",
            "A = (W / (Kd * P1 * Kb * Kc)) * SQRT((T * Z) / M) (gas relief orifice area)"
        ],
        safeguards=[
            "Passive fire protection (PFP) coating on vessel (2-4 hour endurance)",
            "Water spray deluge system (activated by flame detectors)",
            "Fireproofing on vessel supports (prevent collapse)",
            "Depressuring system (blowdown valve) as alternative to relief valve",
            "Good drainage (F = 0.5) or water spray (F = 0.3) reduces heat input"
        ]
    ),

    DoctrineBlock(
        topic="Relief Valve Sizing - Blocked Outlet Case",
        keywords=["blocked outlet", "thermal expansion", "hydraulic expansion", "liquid relief", "double block", "trapped liquid"],
        conclusion_template="Blocked outlet scenario occurs when liquid trapped between two closed valves undergoes thermal expansion from ambient heat or process heat. Small temperature rise causes large pressure rise in confined liquid. Required relief capacity W = (beta * V * deltaT) / (Cp * t), where beta = volumetric thermal expansion coefficient, V = trapped volume, deltaT = temperature rise, t = time to reach set pressure. Relief valve must be liquid service rated.",
        reasoning_framework="""
Blocked outlet (thermal expansion) relief valve sizing:

1. Scenario Identification:
   - Liquid trapped between two block valves (double block and bleed not used)
   - Dead-end piping or equipment with isolation valves
   - Solar heating of piping or equipment (black pipe in sun can reach 150-180 deg F)
   - Process heating (steam tracing, heat exchanger tube-side with closed valves)
   - Cryogenic liquid warming (LNG, liquid nitrogen, liquid oxygen)

2. Thermal Expansion Theory:
   - Liquids are nearly incompressible: small volume change causes large pressure rise
   - Volumetric thermal expansion: deltaV / V = beta * deltaT
     Where beta = coefficient of volumetric expansion (typically 0.001 to 0.002 per deg F for hydrocarbons)
   - Pressure rise in rigid vessel: deltaP = (bulk modulus / beta) * deltaV / V
     Bulk modulus for liquids: 200,000 to 500,000 psi (very high)
   - Result: Temperature rise of 10 deg F can generate thousands of psi pressure

3. Required Relief Rate Calculation:
   - Volumetric expansion rate: Q_vol = beta * V * (dT/dt)
     Where V = trapped volume (gallons or m^3), dT/dt = heating rate (deg F/hr)
   - Mass relief rate: W = rho * Q_vol = rho * beta * V * (dT/dt)
   - Alternative form: W = (beta * V * deltaT) / t
     Where deltaT = temperature rise from ambient to relief temp, t = time (hours)

4. Heating Rate Estimation:
   - Solar heating: dT/dt = (solar_flux * A_exposed) / (rho * Cp * V)
     Solar flux: 250-300 Btu/hr/ft^2 (800-950 W/m^2) for direct sun
   - Process heating (steam tracing): dT/dt = (U * A * (T_steam - T_liquid)) / (rho * Cp * V)
     Where U = overall heat transfer coefficient (Btu/hr/ft^2/deg F)
   - Conservative assumption: Instant heating (use small t, like 1 minute)

5. Typical Expansion Coefficients (beta, per deg F):
   - Water: 0.00011 at 60 deg F
   - Gasoline: 0.00070
   - Diesel: 0.00045
   - Propane: 0.00172 (high, very sensitive to temperature)
   - LNG (methane): 0.00250 (extremely high)

6. Example Calculation:
   - Trapped volume: 100 gallons propane between two closed valves
   - Ambient temp: 60 deg F, Relief set pressure corresponds to 100 deg F (deltaT = 40 deg F)
   - Propane density: 4.2 lb/gal, beta = 0.00172 per deg F, Cp = 0.6 Btu/lb/deg F
   - Heating time (conservative): 10 minutes = 0.167 hours
   - W = (beta * V * deltaT) / (Cp * t) = (0.00172 * 100 gal * 4.2 lb/gal * 40 deg F) / (0.6 Btu/lb/deg F * 0.167 hr)
   - W = 28.9 / 0.1 = 289 lb/hr = very small relief valve (liquid service)

7. Mitigation Strategies:
   - Eliminate double block: Use block and bleed (vent trapped liquid before closing second valve)
   - Install thermal relief valve on all potential liquid trap locations
   - Use expansion loops or accumulators to absorb volume change
   - Insulate or shade piping to reduce solar heating
   - Remove heat sources (turn off steam tracing when valve closed)
        """,
        key_factors=[
            "Trapped liquid volume between block valves",
            "Volumetric thermal expansion coefficient (beta)",
            "Temperature rise (ambient to relief set temperature)",
            "Heating rate (solar, process heat, ambient)",
            "Relief valve must be liquid-rated (not gas service)",
            "Set pressure based on piping/equipment MAWP",
            "Small relief capacity typically required (sub-GPM flow)"
        ],
        primary_authority=[
            "API 521 Section 4.4.14 Thermal Expansion Relief",
            "ASME B31.3 Process Piping, Appendix Q (thermal expansion)",
            "Crane Technical Paper 410 Flow of Fluids Through Valves, Fittings, and Pipe"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.RELIEF_SYSTEM,
        calculation_methods=[
            "W = (beta * V * deltaT) / (Cp * t)",
            "Q_vol = beta * V * (dT/dt)",
            "deltaP_confined = (Bulk_Modulus / beta) * (deltaV / V)"
        ],
        safeguards=[
            "Block and bleed valve configuration (3-valve manifold)",
            "Thermal relief valves on dead-end piping",
            "Car-seal or lock-open on upstream valve (prevent double block)",
            "Expansion loops or bladder accumulators",
            "Insulation or sun shades to reduce heating rate"
        ]
    ),

    DoctrineBlock(
        topic="Dust Explosion Prevention - Kst Classification",
        keywords=["dust explosion", "kst", "deflagration index", "nfpa 652", "combustible dust", "pmax", "explosion venting", "explosion suppression"],
        conclusion_template="Combustible dust explosion severity characterized by Kst (deflagration index, bar*m/s) and Pmax (maximum explosion pressure, bar). St Class 1: Kst < 200 (weak), St Class 2: Kst 200-300 (strong), St Class 3: Kst > 300 (very strong). NFPA 652 requires Dust Hazard Analysis (DHA) for all facilities handling combustible dust. Mitigation: explosion venting (relief panels), explosion suppression (chemical injection), explosion isolation (fast-acting valves), inerting (nitrogen blanketing).",
        reasoning_framework="""
Dust explosion hazard assessment and mitigation (NFPA 652 methodology):

1. Combustible Dust Definition (NFPA 652):
   - Finely divided solid particles < 420 microns (passes through No. 40 sieve)
   - Capable of dispersing in air
   - Will ignite and deflagrate when in a cloud
   - Examples: grain, sugar, flour, metal powders (aluminum, magnesium), coal, plastics, pharmaceuticals

2. Dust Explosion Pentagon (all 5 required for explosion):
   - Combustible dust (fuel)
   - Oxygen (air)
   - Ignition source (spark, hot surface, static discharge, open flame)
   - Dispersion (dust cloud, not just dust layer)
   - Confinement (enclosed space, even partial)
   - Remove ANY one element = no explosion

3. Kst and Pmax Testing (ASTM E1226, 20-liter sphere):
   - Kst = deflagration index = (dP/dt)_max * V^(1/3)
     Where (dP/dt)_max = maximum rate of pressure rise (bar/s), V = vessel volume (m^3)
     Units: bar*m/s
   - Pmax = maximum explosion pressure (bar gauge)

   - St Class 1: Kst 0-200 bar*m/s (weak explosions - wood, sugar)
   - St Class 2: Kst 200-300 bar*m/s (strong - grain, plastics)
   - St Class 3: Kst > 300 bar*m/s (very strong - aluminum, magnesium)

   - Typical Pmax: 7-10 barg for most organic dusts

4. Minimum Ignition Energy (MIE):
   - MIE < 10 mJ: Extremely sensitive (can ignite from static discharge from human body)
   - MIE 10-100 mJ: Sensitive
   - MIE > 100 mJ: Less sensitive
   - Examples: Aluminum powder MIE = 10-50 mJ, Corn starch MIE = 40 mJ

5. Explosion Venting Design (NFPA 68):
   - Vent area calculation: A_vent = A_s * (C / P_red)^0.5 * (V / 10)^0.5
     Where:
     * A_s = surface area of enclosure (m^2)
     * C = venting constant (depends on Kst: C = 0.1 for St-1, 0.15 for St-2, 0.2 for St-3)
     * P_red = reduced explosion pressure (bar, typically 0.1-0.5 bar for weak structures)
     * V = enclosure volume (m^3)
   - Vent panels must open at low pressure (0.01-0.05 bar) before flame propagates
   - Vent discharge must be directed to safe location (away from personnel, ignition sources)

6. Explosion Suppression (NFPA 69):
   - Pressure detectors sense explosion initiation (< 50 milliseconds)
   - Chemical suppressant (dry powder, water mist) injected at high pressure
   - Suppressant quenches flame before pressure rises above Pmax
   - Effective for Kst < 400 bar*m/s (St-1 and St-2 dusts)
   - Requires fast detection and injection (total time < 50-100 ms)

7. Explosion Isolation (prevent propagation between vessels):
   - Fast-acting isolation valves (close in < 50 ms)
   - Rotary valves with explosion detection
   - Chemical barriers (suppressant injection in duct)
   - Passive isolation (flame diverters, choke points)

8. Inerting (NFPA 69):
   - Nitrogen or CO2 blanketing to reduce oxygen below LOC (Limiting Oxygen Concentration)
   - Typical LOC: 8-12% O2 for most organic dusts (in nitrogen)
   - Inerting reduces Pmax and prevents ignition
   - Requires continuous monitoring and makeup to maintain inert atmosphere

9. Housekeeping and Ignition Source Control:
   - NFPA 652: No dust layer over 1/32 inch (0.8 mm) thick
   - Regular cleaning (vacuum with bonded/grounded hose, not compressed air blow-down)
   - Electrical equipment: Class II Division 1 or 2 (dust-ignition-proof)
   - Hot work permit (grinding, welding in dust areas)
   - Bonding and grounding of all conductive equipment (prevent static accumulation)
        """,
        key_factors=[
            "Kst deflagration index (severity of explosion)",
            "Pmax maximum explosion pressure",
            "Minimum Ignition Energy (MIE)",
            "Dust layer thickness (housekeeping)",
            "Confinement (enclosed vs. open equipment)",
            "Ignition source control (electrical classification, hot work)",
            "Oxygen concentration (inerting if below LOC)"
        ],
        primary_authority=[
            "NFPA 652 Standard on the Fundamentals of Combustible Dust",
            "NFPA 68 Standard on Explosion Protection by Deflagration Venting",
            "NFPA 69 Standard on Explosion Prevention Systems",
            "OSHA Combustible Dust National Emphasis Program (NEP)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DUST_EXPLOSION,
        calculation_methods=[
            "Kst = (dP/dt)_max * V^(1/3)",
            "A_vent = A_s * (C / P_red)^0.5 * (V / 10)^0.5"
        ],
        safeguards=[
            "Explosion venting (relief panels to safe location)",
            "Explosion suppression (chemical injection < 50 ms)",
            "Explosion isolation (fast-acting valves, rotary airlocks)",
            "Inerting (nitrogen blanketing, O2 < LOC)",
            "Housekeeping (vacuum dust layers, no accumulation)",
            "Ignition source control (Class II electrical, hot work permits)",
            "Bonding and grounding (static dissipation)"
        ]
    ),

    DoctrineBlock(
        topic="Chemical Reactivity Hazards - DIERS Methodology",
        keywords=["reactivity", "runaway reaction", "diers", "adiabatic calorimetry", "vsp", "thermal stability", "exothermic decomposition"],
        conclusion_template="Chemical reactivity hazards assessed via DIERS (Design Institute for Emergency Relief Systems) methodology. Adiabatic calorimetry (VSP - Vent Sizing Package, ARC - Accelerating Rate Calorimeter) measures exotherm onset temperature, adiabatic temperature rise, and gas generation rate. Runaway scenario: loss of cooling to exothermic reaction causes temperature increase, accelerating reaction rate (Arrhenius). Relief system must handle vapor+gas two-phase flow.",
        reasoning_framework="""
Chemical reactivity hazard assessment (DIERS Design Institute):

1. Reactivity Hazard Categories:
   - Desired reaction runaway: Normal reaction loses control (cooling failure, catalyst overdose)
   - Decomposition: Material decomposes exothermically at elevated temperature
   - Polymerization: Uncontrolled polymerization (styrene, acrylates)
   - Side reactions: Unintended reaction between incompatible chemicals
   - Autocatalytic: Reaction products catalyze further reaction (peroxide decomposition)

2. Adiabatic Calorimetry Testing:
   - VSP (Vent Sizing Package): Low thermal inertia, measures exotherm under adiabatic conditions
   - ARC (Accelerating Rate Calorimeter): Higher thermal inertia, longer timescale
   - Measure:
     * T_onset: Temperature where exotherm begins (deg C)
     * T_final: Maximum adiabatic temperature (deg C)
     * dT_ad: Adiabatic temperature rise = T_final - T_onset (deg C)
     * dT/dt: Temperature rise rate (deg C/min)
     * dP/dt: Pressure rise rate (psi/min or bar/min)
     * Gas generation rate (moles/s or kg/s)

3. Time to Maximum Rate (TMR):
   - TMR = time from current temperature to maximum rate of exotherm
   - TMR at process temperature > 24 hours: Stable under normal conditions
   - TMR at process temperature 8-24 hours: Marginal stability, requires controls
   - TMR at process temperature < 8 hours: Unstable, redesign required
   - TMR calculated from Arrhenius: TMR = (R * T^2) / (E_a * (dT/dt))
     Where E_a = activation energy (J/mol), R = gas constant, T = temperature (K)

4. Two-Phase Flow Relief Sizing (DIERS Method):
   - Runaway reactions generate gas (from boiling or decomposition)
   - Relief valve must handle vapor-liquid mixture (two-phase flow)
   - Homogeneous flow (bubbly): Use omega method
     Omega = (1/Cp) * (dP/dT) * V_vapor / V_total
   - Churn-turbulent flow: Use equilibrium rate model
   - Relief area: A = (G * V) / (Kd * P * psi_function)
     Where G = mass generation rate (kg/s/m^3), V = reactor volume (m^3), psi = two-phase multiplier

5. Mitigation Strategies (Inherently Safer Design):
   - Minimize: Reduce inventory (smaller reactor, continuous vs. batch)
   - Moderate: Lower process temperature or concentration (dilute reactants)
   - Substitute: Replace reactive chemical with less hazardous alternative
   - Simplify: Eliminate unit operations (direct vs. multi-step synthesis)

6. Safeguards for Runaway Prevention:
   - Temperature control: High-reliability cooling system (SIL-rated interlock)
   - Emergency cooling: Backup cooling (quench addition, dump to quench tank)
   - Reactant feed control: Stop feed on high temperature (prevent further exotherm)
   - Inhibitor injection: Add polymerization inhibitor (for styrene, acrylates)
   - Emergency relief: Rupture disk or relief valve to catch tank or scrubber
   - Inert blanketing: Nitrogen to prevent oxygen-sensitive reactions

7. Thermal Stability Screening:
   - Differential Scanning Calorimetry (DSC): Screening test for exotherms
   - Measure heat of reaction: Q = integral(Cp * dT/dt * dt)
   - If Q > 400 J/g or dT_ad > 100 deg C: Highly energetic, requires further testing (VSP, ARC)
   - If onset temperature < 150 deg C: May decompose during storage or normal processing
        """,
        key_factors=[
            "Onset temperature of exotherm (T_onset)",
            "Adiabatic temperature rise (dT_ad)",
            "Time to Maximum Rate (TMR)",
            "Gas generation rate (affects relief sizing)",
            "Two-phase flow regime (homogeneous vs. churn-turbulent)",
            "Heat of reaction (kJ/kg)",
            "Activation energy (affects rate dependence on temperature)"
        ],
        primary_authority=[
            "DIERS (Design Institute for Emergency Relief Systems) - AIChE",
            "CCPS Guidelines for Chemical Reactivity Evaluation and Application to Process Design",
            "NFPA 704 Standard System for the Identification of the Hazards of Materials for Emergency Response"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.REACTIVITY,
        calculation_methods=[
            "TMR = (R * T^2) / (E_a * (dT/dt))",
            "Adiabatic temperature rise: dT_ad = T_final - T_onset",
            "Two-phase relief area: A = (G * V) / (Kd * P * psi)",
            "Omega parameter: omega = (1/Cp) * (dP/dT) * (V_vapor / V_total)"
        ],
        safeguards=[
            "SIL-rated high temperature interlock (shutdown on T > setpoint)",
            "Emergency quench system (dump to quench tank, inject inhibitor)",
            "Relief to catch tank or scrubber (not atmosphere)",
            "Backup cooling (redundant heat exchanger, emergency cooling water)",
            "Reactant feed interlock (stop feed on high T or high P)",
            "Inert blanketing (nitrogen purge to prevent air ingress)",
            "Adiabatic calorimetry testing (VSP, ARC) before scale-up"
        ]
    ),

    DoctrineBlock(
        topic="OSHA PSM 14 Elements Compliance",
        keywords=["psm", "osha 1910.119", "process safety management", "pha", "moc", "operating procedures", "mechanical integrity"],
        conclusion_template="OSHA PSM (29 CFR 1910.119) applies to processes with threshold quantities of hazardous chemicals (e.g., 10,000 lbs flammable, 1,500 lbs toxic). 14 elements: Process Safety Information, Process Hazard Analysis (PHA every 5 years), Operating Procedures, Training, Contractors, Pre-Startup Safety Review, Mechanical Integrity, Hot Work Permits, Management of Change (MOC), Incident Investigation, Emergency Planning, Compliance Audits (every 3 years), Trade Secrets, Employee Participation.",
        reasoning_framework="""
OSHA PSM (Process Safety Management) 14-element compliance framework:

1. Process Safety Information (PSI):
   - Hazard information: SDS (Safety Data Sheets) for all chemicals
   - Technology: Process chemistry, maximum intended inventory, safe operating limits
   - Equipment: P&IDs, electrical classification, relief system design, materials of construction
   - Must be accurate and up-to-date (basis for PHA)

2. Process Hazard Analysis (PHA):
   - Required for all covered processes
   - Revalidation every 5 years minimum (or after major MOC)
   - Methodology: HAZOP, What-If, Checklist, FMEA, Fault Tree (appropriate to complexity)
   - Team: Includes operations, engineering, employee representative
   - Resolve findings: Track recommendations to closure with action party and due date

3. Operating Procedures:
   - Written procedures covering: startup, normal operation, shutdown, emergency shutdown
   - Operating limits (pressure, temperature, composition, level)
   - Safety systems and interlocks
   - Steps to avoid or mitigate releases
   - Must be accessible to operators and kept current

4. Training:
   - Initial training before assignment
   - Refresher training at least every 3 years
   - Document: Name, date, means to verify understanding (test, demonstration)
   - Contractor employees: Same training as permanent employees for tasks performed

5. Contractors:
   - Select contractors with safety record evaluation
   - Inform contractors of process hazards and emergency actions
   - Explain safe work practices (hot work permit, confined space entry)
   - Document contractor training
   - Evaluate contractor performance periodically

6. Pre-Startup Safety Review (PSSR):
   - Required for new processes or after major modification
   - Verify:
     * Construction per design specs
     * Safety systems tested and functional
     * PHA recommendations resolved
     * Procedures and training complete
     * PSI updated to reflect as-built
   - Sign-off required before introducing hazardous materials

7. Mechanical Integrity (MI):
   - Applies to: Pressure vessels, piping, relief devices, controls, pumps, emergency shutdown
   - Written procedures for inspection and testing
   - Frequency based on manufacturer recommendation or engineering judgment
   - Inspection by qualified personnel
   - Deficiencies corrected before further use or in safe and timely manner
   - Quality assurance for new equipment and maintenance materials

8. Hot Work Permit:
   - Required for welding, grinding, cutting in or near covered process
   - Verify: Flammable atmosphere check, fire watch assigned, extinguisher available
   - Permit valid for one shift or specific job
   - Close out permit when work complete

9. Management of Change (MOC):
   - Required for any change to process chemistry, technology, equipment, procedures, facilities
   - Exceptions: Replacement in kind, changes covered by original PSI
   - MOC Review: Technical basis, impact on safety, modifications to procedures/training, PHA update
   - Authorization by qualified personnel before implementation
   - Notify affected employees and contractors

10. Incident Investigation:
    - Investigate incidents that did or could have resulted in catastrophic release
    - Initiate within 48 hours
    - Team includes operations, employee representative, others with knowledge
    - Report: Date, description, factors contributing, recommendations
    - Track recommendations to closure
    - Communicate findings to employees

11. Emergency Planning and Response:
    - Emergency Action Plan (OSHA 1910.38)
    - Procedures for handling small releases (before evacuation)
    - Evacuation routes and assembly points
    - Emergency contact list (fire, EMS, EPA, OSHA)
    - Drills at least annually

12. Compliance Audits:
    - At least every 3 years
    - Verify compliance with all 14 PSM elements
    - Report: Areas audited, deficiencies, corrective actions
    - Retain two most recent audit reports
    - Employer must respond to findings and document corrective actions

13. Trade Secrets:
    - Employees and contractors have access to PSI (even if trade secret)
    - Confidentiality agreement may be required
    - Must provide information in emergency situations

14. Employee Participation:
    - Consult with employees on PHA, incident investigations, audits
    - Provide access to PSI, PHA, and other PSM documents
    - Employee or representative participates in PHA and incident investigation teams
        """,
        key_factors=[
            "Threshold quantity of hazardous chemical (triggers PSM applicability)",
            "PHA revalidation every 5 years",
            "Operating procedures current and accessible",
            "Training initial + refresher every 3 years",
            "PSSR before startup of new or modified process",
            "Mechanical integrity inspection frequency",
            "MOC review before implementing changes",
            "Compliance audit every 3 years"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.119 Process Safety Management of Highly Hazardous Chemicals",
            "OSHA PSM Covered Chemical List (Appendix A, 1910.119)",
            "EPA 40 CFR Part 68 Chemical Accident Prevention Provisions (Risk Management Program)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PSM_COMPLIANCE,
        safeguards=[
            "Process Safety Information (PSI) accurate and current",
            "PHA every 5 years, resolve all findings",
            "Operating procedures covering all modes (startup, normal, shutdown, emergency)",
            "Training documented with test/demonstration",
            "PSSR checklist signed before startup",
            "Mechanical integrity program (inspection, testing, deficiency correction)",
            "MOC for all changes (not replacement in kind)",
            "Incident investigation within 48 hours, track recommendations",
            "Compliance audit every 3 years, correct deficiencies"
        ]
    ),

    DoctrineBlock(
        topic="Management of Change (MOC) Process",
        keywords=["moc", "management of change", "process change", "authorization", "pssr", "temporary change", "permanent change"],
        conclusion_template="Management of Change (MOC) is required for any deviation from Process Safety Information (PSI). Change categories: Permanent (design basis), Temporary (time-limited, requires expiration date and review), Replacement in Kind (same specs, no MOC). MOC review includes: technical basis, safety impact, PHA update, procedure/training changes, authorization, communication to affected personnel. Must complete PSSR before implementing change.",
        reasoning_framework="""
Management of Change (MOC) detailed implementation (OSHA PSM 1910.119(l)):

1. MOC Triggers (when MOC is REQUIRED):
   - Process chemistry change (different raw material, catalyst, solvent)
   - Process technology change (reaction pathway, separation method)
   - Equipment change (different design, capacity, materials of construction)
   - Procedure change (operating limits, startup/shutdown sequence)
   - Facility change (building, layout, utility systems)
   - Organizational change (IF impacts safety-critical roles)

2. MOC Exemptions (when MOC is NOT required):
   - Replacement in Kind: Same manufacturer, model, specs, materials, capacity
     * Example: Replace failed pump with identical spare (same GPM, head, materials)
     * Example: Replace pressure gauge with same range and accuracy
   - Changes already addressed in PSI (within design envelope)
     * Example: Operate at 80% of design capacity instead of 70% (if within design)

3. Temporary vs. Permanent Change:
   - Temporary Change:
     * Time-limited (specify expiration date, typically < 1 year)
     * Must revert to original or implement permanent MOC before expiration
     * Examples: Bypass interlock during maintenance (with compensating controls), use alternate raw material during supply disruption
     * Requires heightened oversight (more frequent inspection, operator awareness)
   - Permanent Change:
     * Indefinite duration
     * Update PSI, P&IDs, procedures to reflect new design basis
     * May trigger PHA revalidation

4. MOC Review Content (Comprehensive Checklist):
   a. Technical Basis:
      - Why is change necessary? (business case, safety improvement, regulatory)
      - Engineering calculations or modeling supporting change
      - Vendor documentation for new equipment

   b. Safety Impact Assessment:
      - Does change introduce new hazards?
      - Does change affect existing safeguards (alarms, interlocks, relief)?
      - What-If analysis: What could go wrong with this change?
      - Consequence if change fails or is reversed unexpectedly?

   c. PHA Impact:
      - Does change invalidate PHA assumptions?
      - If yes, update PHA or schedule revalidation
      - New recommendations from change review?

   d. Procedure and Training Updates:
      - Operating procedures need revision?
      - Training required for operators, maintenance, contractors?
      - Timeline to complete training before change implemented

   e. Regulatory and Code Compliance:
      - Does change affect permit limits (air, water discharge)?
      - Building code, fire code, electrical code implications?
      - EPA RMP or OSHA PSM notification required?

   f. Drawings and Documentation:
      - P&IDs updated (mark revision date and MOC number)
      - Equipment list, instrument list updated
      - As-built drawings for construction

   g. Pre-Startup Safety Review (PSSR):
      - PSSR checklist before change goes live
      - Verify construction per MOC, safety systems tested, training complete

5. MOC Authorization:
   - Must be approved by qualified personnel (typically Engineering Manager, Operations Manager)
   - Cannot implement change without signed authorization
   - If safety-critical, may require Plant Manager or corporate approval

6. Communication:
   - Notify affected employees BEFORE change implemented
   - Shift handover briefing if change occurs during operation
   - Contractors informed if change affects their work
   - Update permit boards (confined space, hot work) if change affects entry conditions

7. MOC Tracking and Closure:
   - Assign unique MOC number
   - Track status: Initiated, Under Review, Approved, Implemented, Closed
   - Closure checklist: PSSR complete, PSI updated, procedures updated, training complete
   - Retain MOC records for life of process (or until next PHA that incorporates change)

8. Common MOC Violations (What NOT to do):
   - Implementing change without written MOC (verbal approval not acceptable)
   - Claiming Replacement in Kind when specs differ (even slightly)
   - Temporary change that never expires (becomes de facto permanent)
   - Failing to update P&IDs after change (PSI out of date)
   - Training operators after change implemented (must train BEFORE)
        """,
        key_factors=[
            "Change triggers MOC (chemistry, equipment, procedures)",
            "Replacement in Kind exemption (same specs, no MOC required)",
            "Temporary change with expiration date and review",
            "Safety impact assessment (new hazards, safeguard impact)",
            "PHA update if assumptions invalidated",
            "Procedure and training updates BEFORE implementation",
            "PSSR before change goes live",
            "Communication to affected employees and contractors"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.119(l) Management of Change",
            "CCPS Guidelines for Management of Change for Process Safety",
            "API RP 750 Management of Process Hazards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MOC,
        safeguards=[
            "Written MOC procedure with approval workflow",
            "Technical review by engineering (safety impact, code compliance)",
            "Operations review (procedure impact, training needs)",
            "Authorization by qualified manager before implementation",
            "PSSR checklist (construction, testing, training, PSI update)",
            "Communication to affected personnel (operators, contractors)",
            "MOC tracking system (status, due dates, closure checklist)",
            "Periodic audit of MOC compliance (part of PSM audit)"
        ]
    ),

    DoctrineBlock(
        topic="Inherently Safer Design (ISD) Principles",
        keywords=["inherently safer", "minimize", "substitute", "moderate", "simplify", "hierarchy of controls", "isd"],
        conclusion_template="Inherently Safer Design (ISD) reduces hazards by design, not by adding safeguards. Four principles: Minimize (reduce inventory or energy), Substitute (less hazardous material), Moderate (less hazardous conditions), Simplify (eliminate complexity). ISD is top of hazard control hierarchy (more effective than engineered controls or PPE). Apply ISD early in design (retrofit is costly). Examples: Continuous process vs. batch (minimize), water-based coating vs. solvent (substitute), lower pressure/temperature (moderate), direct synthesis vs. multi-step (simplify).",
        reasoning_framework="""
Inherently Safer Design (ISD) philosophy and application:

1. Hierarchy of Hazard Controls (most to least effective):
   a. Elimination: Remove hazard entirely (best, often not feasible)
   b. Inherently Safer Design: Reduce hazard by design (minimize, substitute, moderate, simplify)
   c. Passive Safeguards: No moving parts (dikes, relief valves, flame arrestors)
   d. Active Safeguards: Require action (alarms, interlocks, shutdown systems)
   e. Procedural Controls: Administrative (permits, procedures, training)
   f. Personal Protective Equipment (PPE): Least effective (last line of defense)

2. ISD Principle 1 - MINIMIZE:
   - Reduce inventory of hazardous material:
     * Continuous process vs. batch (smaller working inventory)
     * Just-in-time delivery (reduce storage)
     * Smaller piping (less liquid holdup)
     * Elevated equipment (gravity drain, no pump-out needed)
   - Reduce energy:
     * Lower pressure (reduce relief load, smaller equipment)
     * Lower temperature (reduce reaction rate, less thermal hazard)
   - Example: Methyl isocyanate (MIC) in Bhopal disaster - 40+ tons stored. ISD: Produce MIC on-demand (kg quantities), no storage tank.

3. ISD Principle 2 - SUBSTITUTE:
   - Replace hazardous material with less hazardous alternative:
     * Water-based coating instead of solvent-based (eliminate flammable VOC)
     * Aqueous ammonia (28%) instead of anhydrous ammonia (eliminate toxic gas release)
     * Sodium hypochlorite (bleach) instead of chlorine gas (eliminate toxic gas)
   - Replace hazardous process with safer process:
     * Direct oxidation instead of chlorination + hydrolysis (fewer steps, less waste)
   - Trade-offs: Substitutes may have lower performance or higher cost
   - Example: Phosgene (COCl2) is highly toxic. Substitute: Diphosgene or triphosgene (less toxic, easier to handle).

4. ISD Principle 3 - MODERATE:
   - Use less hazardous process conditions:
     * Lower pressure (reduce explosion severity, smaller relief)
     * Lower temperature (reduce thermal decomposition risk)
     * Dilute concentration (reduce reactivity, increase ignition energy)
     * Refrigerated storage vs. pressurized (eliminate pressure hazard)
   - Example: LPG (liquefied petroleum gas) stored as refrigerated liquid at 1 atm (-42 deg C) vs. pressurized at ambient (8-10 barg). Refrigerated eliminates pressure hazard but adds refrigeration complexity.

5. ISD Principle 4 - SIMPLIFY:
   - Eliminate complexity:
     * Fewer process steps (fewer opportunities for error)
     * Fewer equipment items (less to maintain)
     * Simpler control system (easier to understand, less likely to fail)
     * Avoid exotic materials or processes (use proven technology)
   - Example: Direct synthesis of chemical vs. multi-step synthesis with intermediate isolation. Fewer steps = fewer tanks, less handling, lower inventory.

6. ISD Application Timing:
   - Most effective: Conceptual design (R&D, process selection)
   - Effective: Detailed design (equipment sizing, layout)
   - Less effective: Construction (some changes possible)
   - Least effective: Operations (retrofit is very costly)
   - Rule: Apply ISD as early as possible (change in R&D costs $1, in operations costs $1000+)

7. ISD vs. Safeguards Trade-off:
   - ISD reduces hazard inherently (always preferred)
   - Safeguards manage residual hazard (required when ISD insufficient)
   - Example: Flammable liquid storage
     * ISD: Reduce inventory (smaller tank = less fire severity)
     * Safeguard: Foam fire suppression system (active control)
     * Both used together: ISD + safeguards = defense in depth

8. Common ISD Retrofit Opportunities:
   - Eliminate storage tank (just-in-time delivery or on-demand production)
   - Replace batch reactor with continuous (flow chemistry)
   - Lower operating pressure by increasing pipe diameter (same flow, lower velocity)
   - Use closed-loop refrigeration instead of once-through (eliminate ammonia release to atmosphere)
        """,
        key_factors=[
            "Minimize inventory and energy",
            "Substitute less hazardous materials or processes",
            "Moderate conditions (pressure, temperature, concentration)",
            "Simplify (fewer steps, fewer equipment, proven technology)",
            "Apply ISD early in design (conceptual > detailed > construction > operations)",
            "ISD top of hierarchy (more effective than engineered safeguards)",
            "Trade-offs (performance, cost, complexity)"
        ],
        primary_authority=[
            "CCPS Inherently Safer Chemical Processes: A Life Cycle Approach, 2nd Edition",
            "EPA Compilation of Chemical Process Safety Information (ISD case studies)",
            "OSHA PSM Compliance Guidelines (ISD recommended for PHA alternatives)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ISD
    ),

    DoctrineBlock(
        topic="Static Electricity Hazards in Process Operations",
        keywords=["static electricity", "bonding", "grounding", "charge accumulation", "spark discharge", "flammable liquid transfer", "powder handling"],
        conclusion_template="Static electricity accumulation can cause ignition of flammable vapors or dust. Common scenarios: Liquid transfer (especially low-conductivity solvents), powder handling (pneumatic conveying, sieving), filter cartridge change-out. Mitigation: Bonding (electrically connect all conductive parts to same potential), grounding (connect to earth), increase conductivity (add antistatic agent), slow filling (reduce charge generation), inert atmosphere (eliminate oxygen). Minimum Ignition Energy (MIE) determines sensitivity: MIE < 0.1 mJ = highly sensitive to static.",
        reasoning_framework="""
Static electricity generation, accumulation, and ignition hazard management:

1. Static Charge Generation Mechanisms:
   - Liquid flow through pipe or filter: Charge separation at liquid-solid interface
   - Powder flow through chute or pneumatic line: Particle-particle and particle-wall friction
   - Splash filling: Liquid droplets break off and carry charge
   - Human body: Walking on insulating floor, removing clothing
   - Charge generation rate increases with: Flow velocity, low conductivity, low humidity

2. Charge Accumulation Conditions:
   - Material must be insulating (conductivity < 1E-9 S/m)
   - Conductive materials (metal, human body) do not accumulate charge IF grounded
   - Isolated conductors (floating metal, ungrounded vessel) can accumulate charge
   - Capacitance determines voltage: V = Q / C (low capacitance = high voltage for same charge)

3. Ignition Hazard Scenarios:
   a. Flammable Liquid Transfer:
      - Low-conductivity solvents (toluene, hexane, xylene): conductivity < 50 pS/m
      - Charge accumulates in liquid during pumping
      - If vapor space is flammable (LEL-UEL), spark can ignite
      - Brush discharge: 1-4 mJ energy (can ignite most solvent vapors)

   b. Powder Handling:
      - Pneumatic conveying: Powder particles charge by friction
      - Charge accumulates on vessel wall if insulating (plastic, coated)
      - Brush discharge or propagating brush discharge: 10-1000 mJ (can ignite dust clouds)
      - Filter change-out: Dust accumulated on filter is charged, can spark when filter removed

   c. Human Body:
      - Walking on insulating floor: Charge up to 10,000 V (10-20 mJ energy)
      - Spark discharge when touching grounded metal: 1-5 mJ typical
      - Can ignite flammable vapor if MIE < 5 mJ (many solvents)

4. Minimum Ignition Energy (MIE) for Common Materials:
   - Hydrogen gas: 0.02 mJ (extremely sensitive)
   - Carbon disulfide: 0.009 mJ (most sensitive solvent vapor)
   - Hexane, heptane, pentane: 0.24 mJ (typical hydrocarbon solvents)
   - Methanol, ethanol: 0.14 mJ
   - Acetone: 0.55 mJ
   - Toluene, xylene: 0.2-0.5 mJ
   - Aluminum powder (dust): 1-10 mJ
   - Organic dusts (grain, sugar, plastics): 10-100 mJ

5. Bonding and Grounding Requirements:
   - Bonding: Connect all conductive parts together (eliminates potential difference)
     * Example: Bond fill nozzle to receiving vessel (prevent spark between nozzle and tank)
   - Grounding: Connect bonded system to earth (dissipate charge)
     * Grounding resistance: < 10 ohm (NFPA 77) or < 1 Mohm for slower operations
   - Bonding cable: Minimum 1.3 mm dia (16 AWG), verified low resistance (< 10 ohm)
   - Clamp connection: Metal-to-metal contact (remove paint, rust)

6. Conductivity and Relaxation Time:
   - Conductivity: sigma (S/m or pS/m). High conductivity = charge dissipates quickly.
   - Relaxation time: tau = epsilon / sigma
     Where epsilon = permittivity (8.85E-12 F/m for vacuum, higher for liquids)
   - For liquids: If conductivity > 50 pS/m, relaxation time < 1 second (safe)
     If conductivity < 50 pS/m, charge can accumulate (hazardous)
   - Additive: Stadis 450 (antistatic agent for jet fuel, increases conductivity to 50-450 pS/m)

7. Filling Rate and Splash Control:
   - Initial filling: Use slow fill rate until nozzle submerged (< 1 m/s)
   - After submerged: Can increase fill rate (splash eliminated)
   - Top filling: Always higher static hazard than bottom filling (splash + mist)
   - Dip tube or bottom inlet preferred for low-conductivity liquids

8. Inerting (Eliminate Oxygen):
   - If oxygen < LOC (Limiting Oxygen Concentration, typically 8-12%), no ignition possible
   - Nitrogen or CO2 blanketing of vapor space
   - Effective mitigation when bonding/grounding not practical (insulating vessel)

9. Static Hazard Assessment Checklist:
   - Is material flammable or combustible? (vapor or dust)
   - Is vapor/dust concentration in flammable range? (LEL-UEL)
   - Is material low conductivity? (liquid < 50 pS/m, solid insulating)
   - Is there charge generation? (flow, pouring, pneumatic transfer)
   - Are there isolated conductors? (floating metal, ungrounded equipment)
   - What is Minimum Ignition Energy? (compare to expected spark energy)
   - Are bonding and grounding in place and verified?
        """,
        key_factors=[
            "Liquid conductivity (< 50 pS/m = hazardous accumulation)",
            "Flow velocity (higher velocity = more charge generation)",
            "Vapor space flammability (must be in LEL-UEL range for ignition)",
            "Minimum Ignition Energy (MIE) of vapor or dust",
            "Bonding and grounding of all conductive parts (< 10 ohm resistance)",
            "Fill rate control (slow until submerged)",
            "Isolated conductors (ungrounded metal parts)",
            "Humidity (higher humidity = faster charge dissipation)"
        ],
        primary_authority=[
            "NFPA 77 Recommended Practice on Static Electricity",
            "API RP 2003 Protection Against Ignitions Arising Out of Static, Lightning, and Stray Currents",
            "IEC 60079-32-1 Explosive atmospheres - Electrostatic hazards, guidance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.HAZOP,
        safeguards=[
            "Bonding and grounding (< 10 ohm verified before transfer)",
            "Increase liquid conductivity (additive, blend with conductive solvent)",
            "Slow initial fill rate (< 1 m/s until submerged)",
            "Bottom filling or dip tube (eliminate splash)",
            "Inerting (nitrogen blanketing, oxygen < LOC)",
            "Conductive or static-dissipative flooring",
            "Grounding wrist straps for operators (in ESD-sensitive areas)",
            "Humidification (maintain relative humidity > 50%)"
        ]
    ),

    DoctrineBlock(
        topic="Boiling Liquid Expanding Vapor Explosion (BLEVE) Prevention",
        keywords=["bleve", "boiling liquid expanding vapor explosion", "external fire", "pressure vessel failure", "fireball", "lpg", "propane", "water spray"],
        conclusion_template="BLEVE occurs when pressure vessel containing liquid above atmospheric boiling point fails catastrophically, typically from external fire weakening vessel. Liquid flashes to vapor (large volume expansion), creating blast wave and fireball if flammable. Prevention: Passive fire protection on vessel (2-4 hour endurance), water spray deluge (keep vessel cool), fireproofing on supports (prevent collapse), depressuring (rapid blowdown before vessel fails). High-risk materials: LPG, propane, butane, ammonia (stored above boiling point under pressure).",
        reasoning_framework="""
BLEVE (Boiling Liquid Expanding Vapor Explosion) mechanism and prevention:

1. BLEVE Triggering Mechanism:
   - Pressure vessel contains liquid above its atmospheric boiling point
     * Example: Propane (BP -42 deg C) stored at 20 deg C and 8 barg
   - External fire (pool fire, jet fire) heats vessel
   - Vapor space metal heats to 650+ deg C (steel weakens to 50% strength at 550 deg C)
   - Liquid wetted area stays cooler (boiling removes heat)
   - Unwetted vapor space: Metal weakens, vessel fails by rupture
   - Sudden pressure drop: Superheated liquid flashes to vapor (explosion)
   - If flammable: Vapor cloud ignites, creating fireball

2. BLEVE Energy Components:
   a. Pressure energy: E_pressure = P * V (expansion work)
   b. Superheat energy: E_superheat = M * Cp * (T_liquid - T_boiling)
   c. Vaporization energy: E_vaporization = M_flash * lambda
   - Total energy released in milliseconds (shock wave + fireball)

3. BLEVE Consequences:
   - Blast overpressure: 0.07-0.34 bar at 100 m for typical LPG tank (10-20 ton capacity)
   - Fireball: Diameter 5.8 * M^0.333 meters, duration 0.45 * M^0.333 seconds
   - Thermal radiation: 200-350 kW/m^2 during fireball (lethal at close range)
   - Projectiles: Vessel fragments travel 100-500 m (massive, high momentum)
   - Example: 1978 San Carlos, Spain - 23 tons propane BLEVE killed 215 people

4. Indicators of Impending BLEVE:
   - Vessel exposed to fire for 10-30 minutes (heating time to failure)
   - Rising pressure (relief valve lifts continuously)
   - Discoloration of vapor space metal (bluish tint = high temperature)
   - Vessel shell vibration or rumbling sound (boiling inside)
   - Fire impingement on vapor space (worst case, no liquid cooling)
   - Warning: Evacuate area, do not attempt firefighting near vessel

5. BLEVE Prevention - Passive Fire Protection (PFP):
   - Intumescent or cementitious coating on vessel exterior
   - Rated for 2-4 hour endurance (time to steel reaches 550 deg C critical temperature)
   - Applied thickness: 1-4 inches depending on fire scenario and required endurance
   - Coverage: Entire vessel including heads, nozzles, supports
   - Maintenance: Inspect for damage (cracks, spalling, corrosion), repair or recoat

6. BLEVE Prevention - Water Spray Deluge:
   - Water spray nozzles around vessel perimeter
   - Activation: Automatic (flame detectors, fusible links) or manual (remote valve)
   - Application rate: 0.25 gpm/ft^2 (10 L/min/m^2) minimum for LPG vessels (NFPA 15)
   - Effect: Cools vessel shell, prevents metal from reaching critical temperature
   - Requires: Reliable water supply (fire pump, gravity tank), drainage to prevent pool fire

7. BLEVE Prevention - Fireproofing of Supports:
   - Vessel supports (legs, saddles) must not fail before vessel
   - Fireproof supports to same endurance as vessel (2-4 hours)
   - Support failure: Vessel falls, piping ruptures, instant release (worse than BLEVE)

8. BLEVE Prevention - Depressuring (Emergency Blowdown):
   - Rapid blowdown before vessel fails
   - Opens large valve to flare or safe location, releases vapor and liquid
   - Reduces pressure, lowers boiling temperature, reduces superheat
   - Effective if initiated early (before metal weakens)
   - Limitation: Requires operator action or automatic system (flame detection)

9. BLEVE Prevention - Separation Distance:
   - Locate pressure vessels away from fire sources (furnaces, fired heaters)
   - NFPA 58 (LPG): Minimum 25 ft from building openings, 10 ft from property line
   - API 521: Isolate vessels from adjacent equipment (prevent domino effect)

10. Emergency Response - BLEVE Hazard Area:
    - Evacuation radius: 800 m (1/2 mile) for large LPG storage (NFPA 58)
    - Firefighters: Withdraw if vessel exposed to fire for > 10 min (imminent BLEVE)
    - Use unmanned monitors (deluge guns) from safe distance, do not approach vessel
        """,
        key_factors=[
            "Vessel contains liquid above atmospheric boiling point (LPG, ammonia)",
            "External fire exposure (pool fire, jet fire, wildfire)",
            "Vapor space metal reaches critical temperature (550 deg C for steel)",
            "Time to failure (typically 10-30 minutes of fire exposure)",
            "Passive fire protection (PFP) endurance rating",
            "Water spray deluge activation and coverage",
            "Fireproofing of supports (prevent collapse)",
            "Depressuring system availability and activation"
        ],
        primary_authority=[
            "NFPA 58 Liquefied Petroleum Gas Code",
            "API RP 521 Guide for Pressure-Relieving and Depressuring Systems (Section 4.4.12 Fire Exposure)",
            "CCPS Guidelines for Evaluating the Characteristics of Vapor Cloud Explosions, Flash Fires, and BLEVEs"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CONSEQUENCE,
        safeguards=[
            "Passive fire protection (PFP) on vessel (2-4 hour endurance)",
            "Water spray deluge system (0.25 gpm/ft^2, automatic activation)",
            "Fireproofing on vessel supports (prevent collapse)",
            "Emergency depressuring (blowdown valve to flare)",
            "Separation distance from fire sources (25+ ft per NFPA 58)",
            "Relief valve (reduces pressure but does not prevent BLEVE)",
            "Fire detection and alarm (early warning, evacuation)",
            "Emergency response plan (evacuation radius, firefighter withdrawal)"
        ]
    )
]


# ============================================================================
# ENGINE CORE
# ============================================================================

class CHEM19Engine:
    """
    CHEM19 Process Safety Intelligence Engine

    Provides expert-level process safety analysis covering hazard identification
    (HAZOP, What-If, LOPA), consequence modeling (dispersion, fire, explosion),
    relief system design, dust explosions, reactivity hazards, and PSM compliance.
    """

    def __init__(self):
        self.engine_name = "CHEM19_PROCESS_SAFETY"
        self.version = "1.0.0"
        self.port = 9301
        self.start_time = time.time()

        # Telemetry
        self.total_queries = 0
        self.total_response_time_ms = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.triggered_doctrine_log = []

        # Doctrine cache
        self.doctrines = DOCTRINE_CACHE

        logger.info(f"{self.engine_name} v{self.version} initialized on port {self.port}")
        logger.info(f"Loaded {len(self.doctrines)} process safety doctrine blocks")

    def _semantic_normalize(self, query: str) -> str:
        """Normalize query terms for consistent matching."""
        normalized = query.lower()

        # Process safety term normalization
        replacements = {
            "haz op": "hazop",
            "haz-op": "hazop",
            "layers of protection": "lopa",
            "safety instrumented system": "sis",
            "independent protection layer": "ipl",
            "process safety management": "psm",
            "pressure relief": "relief valve",
            "pressure relieving": "relief valve",
            "safety valve": "relief valve",
            "inherent safety": "inherently safer design",
            "inherent safer": "inherently safer design",
            "isd": "inherently safer design",
            "dust deflagration": "dust explosion",
            "combustible dust": "dust explosion",
            "thermal runaway": "runaway reaction",
            "reactive chemical": "reactivity",
            "bleve": "boiling liquid expanding vapor explosion",
            "vce": "vapor cloud explosion",
            "flash fire": "fire",
            "pool fire": "fire",
            "jet fire": "fire",
            "toxic release": "dispersion",
            "gas dispersion": "dispersion",
            "consequence analysis": "consequence modeling",
            "static charge": "static electricity",
            "static spark": "static electricity",
            "electrostatic": "static electricity"
        }

        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        return normalized

    def _match_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Match query to relevant doctrine blocks using keyword matching."""
        normalized_query = self._semantic_normalize(query)
        query_words = set(normalized_query.split())

        matches = []
        for doctrine in self.doctrines:
            # Count keyword matches
            keyword_matches = sum(1 for kw in doctrine.keywords if kw in normalized_query)

            # Check if any query word is in doctrine keywords
            word_matches = sum(1 for word in query_words if any(word in kw for kw in doctrine.keywords))

            total_score = keyword_matches * 2 + word_matches

            if total_score > 0:
                matches.append((total_score, doctrine))

        # Sort by score descending
        matches.sort(key=lambda x: x[0], reverse=True)

        # Return top 5 matches (or all if fewer)
        return [m[1] for m in matches[:5]]

    def _build_answer(
        self,
        matched_doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone,
        query: str
    ) -> str:
        """Build answer from matched doctrines based on mode and zone."""
        if not matched_doctrines:
            return "No specific process safety doctrine matches this query. Please provide more details about the hazard scenario, equipment type, or regulatory requirement."

        # Update doctrine trigger counts
        for doctrine in matched_doctrines:
            doctrine.trigger_count += 1
            doctrine.last_triggered = datetime.now().isoformat()

        if mode == ResponseMode.FAST:
            # Concise: Primary doctrine conclusion + key factors
            primary = matched_doctrines[0]
            answer = f"{primary.conclusion_template}\n\n"
            answer += "Key Factors:\n"
            for factor in primary.key_factors[:4]:
                answer += f"- {factor}\n"
            return answer.strip()

        elif mode == ResponseMode.DEFENSE:
            # Comprehensive with authorities and reasoning
            answer_parts = []
            for i, doctrine in enumerate(matched_doctrines[:3], 1):
                part = f"ASPECT {i}: {doctrine.topic}\n"
                part += f"{doctrine.conclusion_template}\n\n"
                part += f"Technical Framework:\n{doctrine.reasoning_framework}\n\n"
                part += "Regulatory Authorities:\n"
                for auth in doctrine.primary_authority:
                    part += f"- {auth}\n"
                answer_parts.append(part)

            return "\n\n".join(answer_parts).strip()

        else:  # MEMO mode
            # Full documentation with all matched doctrines
            answer_parts = [f"PROCESS SAFETY ANALYSIS: {query}\n"]
            answer_parts.append("=" * 80)

            for i, doctrine in enumerate(matched_doctrines, 1):
                part = f"\n{i}. {doctrine.topic}\n"
                part += "-" * 80 + "\n"
                part += f"Category: {doctrine.category.value}\n"
                part += f"Confidence: {doctrine.confidence.value}\n\n"
                part += f"Conclusion:\n{doctrine.conclusion_template}\n\n"
                part += f"Technical Reasoning:\n{doctrine.reasoning_framework}\n\n"
                part += "Key Factors:\n"
                for factor in doctrine.key_factors:
                    part += f"  - {factor}\n"
                part += "\nRegulatory Authority:\n"
                for auth in doctrine.primary_authority:
                    part += f"  - {auth}\n"

                if doctrine.safeguards:
                    part += "\nRecommended Safeguards:\n"
                    for safeguard in doctrine.safeguards:
                        part += f"  - {safeguard}\n"

                if doctrine.calculation_methods:
                    part += "\nCalculation Methods:\n"
                    for method in doctrine.calculation_methods:
                        part += f"  - {method}\n"

                answer_parts.append(part)

            return "\n".join(answer_parts).strip()

    def _assess_confidence(self, matched_doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine overall confidence level based on matched doctrines."""
        if not matched_doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use primary doctrine confidence
        primary_confidence = matched_doctrines[0].confidence

        # If top 2 doctrines both DEFENSIBLE, stay DEFENSIBLE
        if len(matched_doctrines) >= 2:
            if all(d.confidence == ConfidenceLevel.DEFENSIBLE for d in matched_doctrines[:2]):
                return ConfidenceLevel.DEFENSIBLE

        return primary_confidence

    def _generate_determinism_hash(self, query: str, answer: str) -> str:
        """Generate SHA-256 hash for determinism verification."""
        combined = f"{query}|{answer}|{self.version}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()[:16]

    def query(self, request: QueryRequest) -> QueryResponse:
        """
        Process process safety analysis query through three-layer response.

        Layer 1: Doctrine cache (0-50ms) - Pre-compiled expert reasoning
        Layer 2: Semantic matching (fallback) - Keyword-based doctrine retrieval
        Layer 3: Deep synthesis (not implemented, would integrate external sources)
        """
        start_time = time.time()
        self.total_queries += 1

        # Layer 1 & 2: Doctrine cache matching
        matched_doctrines = self._match_doctrines(request.query)

        if matched_doctrines:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        # Build answer based on mode and zone
        answer = self._build_answer(matched_doctrines, request.mode, request.zone, request.query)

        # Assess confidence
        confidence = self._assess_confidence(matched_doctrines)

        # Extract authorities
        authorities = []
        for doctrine in matched_doctrines[:3]:
            authorities.extend(doctrine.primary_authority)
        authorities = list(dict.fromkeys(authorities))  # Deduplicate

        # Generate warnings (epistemic guardrails)
        warnings = []
        if confidence in [ConfidenceLevel.DISCLOSURE, ConfidenceLevel.HIGH_RISK]:
            warnings.append("This analysis requires site-specific data and professional engineering judgment.")
        if request.zone == AnalysisZone.AUDIT:
            warnings.append("This analysis is for audit purposes. Verify all citations and calculations independently.")

        # Telemetry
        response_time_ms = (time.time() - start_time) * 1000
        self.total_response_time_ms += response_time_ms

        # Log triggered doctrines
        triggered_topics = [d.topic for d in matched_doctrines]
        self.triggered_doctrine_log.append({
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "doctrines": triggered_topics
        })

        # Determinism hash
        determinism_hash = self._generate_determinism_hash(request.query, answer)

        return QueryResponse(
            query_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            zone=request.zone,
            triggered_doctrines=triggered_topics,
            authorities=authorities if request.include_authorities else [],
            warnings=warnings,
            response_time_ms=round(response_time_ms, 2),
            determinism_hash=determinism_hash
        )

    def health(self) -> HealthResponse:
        """Comprehensive health check endpoint."""
        uptime = time.time() - self.start_time
        avg_response_ms = (
            self.total_response_time_ms / self.total_queries
            if self.total_queries > 0
            else 0.0
        )
        cache_hit_rate = (
            self.cache_hits / (self.cache_hits + self.cache_misses)
            if (self.cache_hits + self.cache_misses) > 0
            else 0.0
        )

        return HealthResponse(
            status="healthy",
            engine=self.engine_name,
            version=self.version,
            port=self.port,
            doctrine_count=len(self.doctrines),
            uptime_seconds=round(uptime, 2),
            total_queries=self.total_queries,
            avg_response_ms=round(avg_response_ms, 2),
            cache_hit_rate=round(cache_hit_rate, 3)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="CHEM19 Process Safety Intelligence Engine",
    description="TIE-grade chemical process safety analysis: HAZOP, LOPA, consequence modeling, relief systems, dust explosions, PSM compliance",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = CHEM19Engine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Process safety analysis query endpoint.

    Accepts process safety questions covering:
    - Hazard identification (HAZOP, What-If, LOPA)
    - Consequence modeling (dispersion, fire, explosion)
    - Relief system design (API 520/521)
    - Dust explosion prevention (NFPA 652)
    - Reactivity hazards (DIERS)
    - PSM compliance (OSHA 1910.119)
    - Inherently safer design
    - Static electricity hazards
    """
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Engine health check with telemetry."""
    return engine.health()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """Return all doctrine topics and categories."""
    return {
        "total_doctrines": len(engine.doctrines),
        "categories": list(set(d.category.value for d in engine.doctrines)),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "trigger_count": d.trigger_count
            }
            for d in engine.doctrines
        ]
    }


if __name__ == "__main__":
    logger.add(
        f"O:/ECHO_OMEGA_PRIME/SYSTEMS/engines/CHEM19_process_safety/engine_{datetime.now():%Y%m%d}.log",
        rotation="100 MB",
        retention="30 days",
        level="INFO"
    )

    logger.info(f"Starting {engine.engine_name} v{engine.version} on port {engine.port}")

    uvicorn.run(
        APP,
        host="127.0.0.1",
        port=engine.port,
        log_level="info"
    )
