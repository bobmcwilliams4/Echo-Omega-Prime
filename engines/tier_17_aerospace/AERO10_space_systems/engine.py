"""
AERO10 Space Systems Engineering Intelligence Engine
TIE-Grade Engine for Orbital Mechanics, Spacecraft Design, and Mission Analysis

Port: 9205
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import math
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION & LOGGING
# ═══════════════════════════════════════════════════════════════════════════

ENGINE_NAME = "AERO10_Space_Systems"
VERSION = "1.0.0"
PORT = 9205

logger.add(
    f"logs/{ENGINE_NAME}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS & DATA CLASSES
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

class IssueCategory(str, Enum):
    ORBITAL_MECHANICS = "ORBITAL_MECHANICS"
    THERMAL_CONTROL = "THERMAL_CONTROL"
    ADCS = "ADCS"
    PROPULSION = "PROPULSION"
    POWER_SYSTEMS = "POWER_SYSTEMS"
    SPACE_ENVIRONMENT = "SPACE_ENVIRONMENT"
    MISSION_DESIGN = "MISSION_DESIGN"
    STRUCTURES = "STRUCTURES"
    COMMUNICATIONS = "COMMUNICATIONS"
    SYSTEMS_ENGINEERING = "SYSTEMS_ENGINEERING"

@dataclass
class DoctrineBlock:
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    category: IssueCategory
    counter_arguments: List[str] = field(default_factory=list)
    resolution_strategy: str = ""
    controlling_precedent: str = ""

@dataclass
class QueryMetrics:
    query_id: str
    start_time: float
    cache_hit: bool
    doctrine_blocks_triggered: List[str]
    response_mode: str
    total_latency_ms: float
    confidence_level: str

# ═══════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query_id: str
    response: str
    confidence: ConfidenceLevel
    doctrine_blocks_used: List[str]
    latency_ms: float
    cache_hit: bool
    determinism_hash: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_blocks: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL SPACE SYSTEMS BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Hohmann Transfer Orbit Delta-V Calculation",
        keywords=["hohmann", "transfer", "delta-v", "orbital maneuver", "two-burn", "coplanar"],
        conclusion_template="The Hohmann transfer between circular orbits requires delta-V = sqrt(mu/r1) * [sqrt(2*r2/(r1+r2)) - 1] + sqrt(mu/r2) * [1 - sqrt(2*r1/(r1+r2))]. This represents the minimum-energy two-impulse transfer for coplanar circular orbits.",
        reasoning_framework="""
Hohmann Transfer Analysis Protocol:
1. Verify coplanar circular orbit assumption (if eccentric, use vis-viva)
2. Calculate transfer ellipse semi-major axis: a_transfer = (r1 + r2) / 2
3. First burn (perigee): delta_v1 = sqrt(mu/r1) * [sqrt(2*r2/(r1+r2)) - 1]
4. Second burn (apogee): delta_v2 = sqrt(mu/r2) * [1 - sqrt(2*r1/(r1+r2))]
5. Total delta-V: sum of absolute values of both burns
6. Transfer time: T = pi * sqrt(a^3 / mu)
7. For Earth (mu = 398600 km^3/s^2), LEO-GEO transfer ~= 3.9 km/s total
8. Compare to bi-elliptic transfer for large radius ratios (>11.94)
9. Account for inclination changes (add vectorial component if non-coplanar)
10. Consider launch window constraints and phasing orbits
11. Verify thrust availability for impulsive burn assumption
12. Calculate propellant mass via Tsiolkovsky rocket equation
13. Factor in gravity losses if finite burn duration
14. Check for collision avoidance during transfer arc
15. Validate against ground station visibility requirements
16. Assess radiation exposure during Van Allen belt transit
17. Plan trajectory correction maneuvers (TCMs) for midcourse errors
18. Size propulsion system for required thrust and Isp
19. Consider time-optimal vs fuel-optimal trade-offs
20. Document assumptions: spherical gravity, no perturbations, impulsive burns
""",
        key_factors=[
            "Circular orbit radii (r1, r2)",
            "Gravitational parameter mu",
            "Impulsive burn assumption",
            "Coplanar constraint",
            "Two-body problem simplification",
            "Transfer time = half orbital period of transfer ellipse",
            "Minimum energy for given radius ratio"
        ],
        primary_authority=[
            "Vallado, Fundamentals of Astrodynamics and Applications (4th ed.)",
            "Bate, Mueller, White - Fundamentals of Astrodynamics",
            "Curtis - Orbital Mechanics for Engineering Students",
            "AIAA Space Flight Mechanics Technical Committee standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ORBITAL_MECHANICS,
        counter_arguments=[
            "Bi-elliptic transfer may be more efficient for large radius ratios",
            "Low-thrust spirals can achieve lower propellant mass for long durations",
            "Gravity assists can reduce delta-V for interplanetary missions",
            "Non-Keplerian trajectories (solar sails) avoid propellant entirely"
        ],
        resolution_strategy="Use Hohmann for quick coplanar transfers between similar-sized circular orbits; analyze alternatives for extreme cases.",
        controlling_precedent="Apollo lunar missions used Hohmann-like translunar injection with midcourse corrections"
    ),

    DoctrineBlock(
        topic="Multi-Layer Insulation (MLI) Thermal Performance",
        keywords=["MLI", "thermal", "insulation", "radiation", "emissivity", "crinkled aluminized mylar"],
        conclusion_template="MLI effective emissivity scales as epsilon_eff ~= (N+1) * epsilon_layer for N layers, achieving values <0.01 for 15+ layers. Performance degrades in presence of conduction paths (penetrations, fasteners) and requires high vacuum (<1e-4 torr).",
        reasoning_framework="""
MLI Design and Performance Analysis:
1. MLI blocks radiative heat transfer via multiple low-emissivity surfaces
2. Each layer acts as radiation shield with emissivity epsilon (typically 0.03 for aluminized mylar)
3. Effective emissivity: epsilon_eff = epsilon / (2N - 1) for N layers (ideal case)
4. Real-world: epsilon_eff = (N+1) * epsilon_layer due to imperfect contact and edge effects
5. Layer count typically 15-30 for spacecraft, 40-60 for cryogenic systems
6. Layer density: 3-8 layers per cm, trade-off between performance and mass
7. Outer layer: silver or white Teflon for optical properties and atomic oxygen resistance
8. Inner layers: double-aluminized mylar or Kapton for dimensional stability
9. Spacers: Dacron net, silk, or embossed mylar to prevent layer contact
10. Degradation mechanisms: compression (launch loads), outgassing (contamination), micrometeoroid damage
11. Vacuum requirement: performance drops sharply above 1e-4 torr due to gas conduction
12. Seams and penetrations create thermal shorts (joints, fasteners, harness pass-throughs)
13. Edge effects: lateral conduction along layers at boundaries
14. Testing: requires thermal-vacuum chamber with cold shroud and calorimetry
15. Model validation: use Monte Carlo ray tracing for complex geometries
16. Compare to aerogel (lower density but higher thermal conductivity)
17. Installation care: avoid wrinkles, tears, and compression during integration
18. Grounding: electrically bond layers to prevent charge buildup
19. Tape edges: use aluminized Kapton tape for sealing and mechanical attachment
20. Flight heritage: 50+ years of use from early satellites to ISS modules
""",
        key_factors=[
            "Layer count and spacing",
            "Vacuum level (high vacuum required)",
            "Emissivity of layer material",
            "Penetrations and seams (thermal shorts)",
            "Compression and handling damage",
            "Outer layer optical properties (alpha/epsilon ratio)",
            "Micrometeoroid and atomic oxygen exposure"
        ],
        primary_authority=[
            "Gilmore - Spacecraft Thermal Control Handbook (2nd ed.)",
            "NASA SP-8093 - Spacecraft Thermal Control",
            "ECSS-E-HB-31-01A - Thermal design handbook",
            "AIAA Thermophysics Technical Committee publications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.THERMAL_CONTROL,
        counter_arguments=[
            "Phase-change materials can provide thermal buffering without vacuum",
            "Active cooling (louvers, heat pumps) offers better control",
            "Aerogel insulation provides comparable performance at lower mass for some applications"
        ],
        resolution_strategy="MLI is standard for deep-space and high-temperature differential missions; use aerogel or foam for cryo tanks where handling is easier.",
        controlling_precedent="Apollo Service Module used 13-layer MLI; Hubble Space Telescope uses 40+ layers for cryogenic instruments"
    ),

    DoctrineBlock(
        topic="Reaction Wheel Momentum Management",
        keywords=["reaction wheel", "momentum", "desaturation", "angular momentum", "CMG", "attitude control"],
        conclusion_template="Reaction wheels accumulate angular momentum from external torques (gravity gradient, solar pressure, magnetic). Desaturation via magnetic torquers or thrusters is required when momentum approaches wheel saturation limit (typically 10-100 Nms).",
        reasoning_framework="""
Reaction Wheel Sizing and Management:
1. Reaction wheels exchange angular momentum with spacecraft bus
2. Wheel momentum H_wheel = I_wheel * omega_wheel (wheel inertia × spin rate)
3. Torque output: T = dH/dt = I_wheel * alpha (wheel angular acceleration)
4. Sizing constraint: must store worst-case momentum accumulation between desat events
5. External torques: gravity gradient ~1e-6 Nm for LEO, solar pressure ~1e-7 Nm at 1 AU
6. Secular momentum buildup: dH/dt = T_external (integrate over orbit)
7. Cyclic torques (gravity gradient) average to zero over one orbit for nadir-pointing
8. Residual dipole creates secular buildup in Earth's magnetic field
9. Desaturation methods: magnetic torquers (LEO), thrusters (GEO/deep space), or CMG null mode
10. Magnetic torquer cross product: T = M × B (dipole moment × field)
11. Wheel saturation limit: typically 80% of max momentum to preserve control authority
12. Redundancy: 4-wheel pyramid configuration for single-fault tolerance
13. Wheel failure modes: bearing seizure, motor burnout, encoder failure
14. CMG alternative: gyroscopic torque from gimbaled high-speed rotor, higher torque density
15. Power consumption: P = T * omega / efficiency (torque × wheel speed / ~0.8)
16. Jitter: wheel imbalance creates disturbance torques at harmonics of spin frequency
17. Vibration isolation: passive (elastomeric mounts) or active (accelerometer feedback)
18. Wheel unloading logic: prioritize magnetic torquers to conserve propellant
19. Momentum envelope: 3D plot of achievable angular momentum vector
20. Life testing: 15+ year missions require 1e9+ revolutions without failure
""",
        key_factors=[
            "Wheel momentum capacity (Nms)",
            "External torque environment",
            "Desaturation authority (magnetic or propulsive)",
            "Control bandwidth and pointing accuracy",
            "Redundancy and fault tolerance",
            "Mass and power budget",
            "Jitter and vibration isolation requirements"
        ],
        primary_authority=[
            "Wertz - Spacecraft Attitude Determination and Control",
            "Sidi - Spacecraft Dynamics and Control",
            "NASA GSFC Flight Dynamics Analysis Handbook",
            "Honeywell, Rockwell Collins reaction wheel datasheets"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ADCS,
        counter_arguments=[
            "CMGs provide higher torque density for large agile spacecraft",
            "Thrusters avoid momentum saturation but consume propellant",
            "Passive gravity-gradient stabilization requires no active control"
        ],
        resolution_strategy="Use reaction wheels for precision pointing (<0.01 deg) with magnetic or thruster desat; CMGs for large agile platforms; gravity-gradient for simple missions.",
        controlling_precedent="Hubble Space Telescope uses 6 reaction wheels (4 active, 2 spares); ISS uses 4 CMGs"
    ),

    DoctrineBlock(
        topic="Bipropellant Rocket Engine Specific Impulse",
        keywords=["bipropellant", "specific impulse", "Isp", "LOX", "RP-1", "hydrazine", "NTO", "chamber pressure"],
        conclusion_template="Bipropellant Isp depends on propellant combination, mixture ratio, chamber pressure, and nozzle expansion ratio. LOX/LH2 achieves ~450s vacuum Isp, LOX/RP-1 ~350s, NTO/MMH ~330s. Higher chamber pressure and expansion ratio improve Isp but add system complexity.",
        reasoning_framework="""
Bipropellant Performance Analysis:
1. Specific impulse: Isp = T / (mdot * g0) = exhaust_velocity / g0 (seconds)
2. Theoretical Isp from thermochemistry: use CEA (Chemical Equilibrium with Applications) code
3. LOX/LH2: highest Isp (~450s vac) but cryogenic handling and low density (bulky tanks)
4. LOX/RP-1: moderate Isp (~350s) but storable at room temp, high density (compact)
5. NTO/MMH: hypergolic (self-igniting), storable, lower Isp (~330s), toxic
6. Mixture ratio: O/F ratio for optimal Isp differs from stoichiometric (typically fuel-rich)
7. Chamber pressure: Pc = 100-200 bar for high performance, trades with turbopump complexity
8. Nozzle expansion ratio: epsilon = A_exit / A_throat, limited by altitude and nozzle length
9. Altitude compensation: under-expanded at sea level, over-expanded in vacuum
10. Frozen vs equilibrium flow: chemical reactions in nozzle affect Isp
11. Combustion efficiency: typically 95-99%, losses from incomplete mixing and cooling
12. Nozzle efficiency: ~98% for well-designed bell or aerospike nozzle
13. Propellant density: rho_LOX/LH2 ~300 kg/m3, rho_LOX/RP-1 ~1000 kg/m3
14. Tank mass fraction: higher density → smaller tanks → lower structural mass
15. Cooling: regenerative (fuel-cooled chamber), ablative, or radiative
16. Throttling: control via valve or multiple chambers, deep throttle (10:1) is challenging
17. Restart capability: critical for in-space stages, requires hypergolic or igniter
18. Propellant storability: cryogens require active cooling (boiloff), hypergols are toxic
19. Cost and complexity: LOX/LH2 is most complex, NTO/MMH is simplest (hypergolic)
20. Flight heritage: F-1 (LOX/RP-1), RL-10 (LOX/LH2), Aestus (NTO/MMH)
""",
        key_factors=[
            "Propellant combination (LOX/LH2, LOX/RP-1, NTO/MMH, etc.)",
            "Mixture ratio (O/F)",
            "Chamber pressure and temperature",
            "Nozzle expansion ratio and efficiency",
            "Altitude (sea level vs vacuum)",
            "Propellant density and storability",
            "Cooling method and regenerative compatibility"
        ],
        primary_authority=[
            "Sutton - Rocket Propulsion Elements (9th ed.)",
            "Humble, Henry, Larson - Space Propulsion Analysis and Design",
            "NASA CEA (Chemical Equilibrium with Applications) software",
            "AIAA Propulsion Technical Committee standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PROPULSION,
        counter_arguments=[
            "Electric propulsion (ion, Hall) achieves 10x higher Isp but much lower thrust",
            "Monopropellant (hydrazine) is simpler but ~50s lower Isp",
            "Solid rockets avoid complexity but cannot be throttled or restarted"
        ],
        resolution_strategy="LOX/LH2 for upper stages (max delta-V), LOX/RP-1 for boosters (high thrust), NTO/MMH for in-space maneuvering (storable, restartable).",
        controlling_precedent="Saturn V: S-IC (LOX/RP-1), S-II (LOX/LH2), S-IVB (LOX/LH2); Space Shuttle OMS (NTO/MMH)"
    ),

    DoctrineBlock(
        topic="Van Allen Belt Radiation Dose Calculation",
        keywords=["van allen", "radiation", "trapped particles", "total ionizing dose", "TID", "single event upset", "SEU"],
        conclusion_template="Van Allen belts contain trapped protons and electrons causing Total Ionizing Dose (TID) and Single Event Effects (SEE). Shielding trades: aluminum thickness vs mass penalty. LEO: <10 krad mission dose, GEO transfer: 10-100 krad, careful trajectory planning reduces exposure.",
        reasoning_framework="""
Radiation Environment and Mitigation:
1. Van Allen belts: inner belt (protons, 1000-6000 km), outer belt (electrons, 13000-60000 km)
2. Total Ionizing Dose (TID): cumulative charge deposition in materials (rads or Gy)
3. Single Event Effects (SEE): SEU (bit flip), SEL (latchup), SEB (burnout) from individual particles
4. Radiation models: AP-8 (protons), AE-8 (electrons), CREME96 (cosmic rays)
5. Shielding: aluminum equivalent thickness, mass penalty ~7 kg/m^2 per mm Al
6. Dose calculation: integrate flux × cross-section × time over orbit and energy spectrum
7. LEO altitude matters: 400 km (ISS) sees <1 krad/year, 800 km sees 10x more (SAA crossings)
8. South Atlantic Anomaly (SAA): inner belt dips to 200 km, high flux region
9. GEO transfer orbit: long dwell in belts during apogee raising, minimize pass count
10. Electronics hardening: radiation-hardened (rad-hard) parts rated to 100 krad (Si) or more
11. RHBD (Radiation-Hardening By Design): triple modular redundancy, error correction
12. Spot shielding: protect critical components (processors) with localized Al or tantalum
13. Solar particle events (SPE): sporadic, high-energy protons from solar flares
14. Galactic cosmic rays (GCR): always present, high-energy heavy ions, difficult to shield
15. Secondary radiation: bremsstrahlung (electrons hitting shielding create X-rays)
16. Annealing: some TID damage recovers at elevated temperature (not always beneficial)
17. Dose-depth curve: surface dose higher than interior, shielding reduces flux exponentially
18. Mission duration: dose accumulates linearly with time in radiation environment
19. Trajectory optimization: avoid high-flux regions via inclination and altitude choices
20. Flight heritage: GPS satellites (MEO) require rad-hard parts; GEO comsats use moderate hardening
""",
        key_factors=[
            "Orbit altitude and inclination (LEO, MEO, GEO, transfer)",
            "Mission duration",
            "Shielding thickness (aluminum equivalent)",
            "Electronics radiation tolerance (TID, SEU rates)",
            "Trajectory through Van Allen belts",
            "South Atlantic Anomaly passage frequency",
            "Solar activity cycle (SPE probability)"
        ],
        primary_authority=[
            "NASA GSFC Radiation Effects and Analysis Group (REAG)",
            "ESA SPENVIS (Space Environment Information System)",
            "MIL-STD-883 Method 1019 (Ionizing Radiation Testing)",
            "ECSS-E-ST-10-12C - Methods for calculation of radiation received and its effects"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPACE_ENVIRONMENT,
        counter_arguments=[
            "Active shielding (magnetic fields) could reduce mass but is immature technology",
            "Optimized trajectories can avoid belts entirely (e.g., polar LEO)",
            "Commercial parts with SEU mitigation (scrubbing) may suffice for LEO missions"
        ],
        resolution_strategy="Use rad-hard parts for MEO/GEO and long LEO missions; spot shield critical components; plan GEO transfer to minimize belt dwell time.",
        controlling_precedent="Apollo missions minimized belt passage time (<1 hour); Mars missions avoid belts entirely"
    ),

    DoctrineBlock(
        topic="Hall Thruster Performance and Efficiency",
        keywords=["hall thruster", "electric propulsion", "xenon", "specific impulse", "thrust efficiency", "anode efficiency"],
        conclusion_template="Hall thrusters achieve Isp of 1500-3000s with thrust efficiency 45-65%. Xenon propellant is standard (high mass, easy ionization). Power consumption 1-10 kW, thrust 20-500 mN. Life limited by cathode erosion and channel wear to 10,000-30,000 hours.",
        reasoning_framework="""
Hall Thruster Design and Operation:
1. Hall effect: electrons trapped in radial magnetic field, ions accelerated axially
2. Specific impulse: Isp = 1500-3000s, far exceeds chemical (300-450s)
3. Thrust: T = mdot * ve = mdot * Isp * g0 (millinewtons to newtons)
4. Power: P = 0.5 * mdot * ve^2 / eta (kinetic power / efficiency)
5. Thrust efficiency: eta_T = T^2 / (2 * mdot * P) = 0.45-0.65
6. Anode efficiency: eta_a includes cathode and magnetic circuit losses, ~0.5-0.6
7. Propellant: xenon (high mass 131 amu, low ionization energy 12.1 eV)
8. Alternatives: krypton (cheaper, lower performance), iodine (storable, corrosive)
9. Magnetic circuit: electromagnets or permanent magnets create radial field
10. Channel material: boron nitride ceramic, erodes over time from ion bombardment
11. Cathode: hollow cathode emits electrons, life-limiting component (barium depletion)
12. Voltage: 200-500 V between anode and cathode
13. Current: 1-50 A depending on power level
14. Plume divergence: ~30-40 deg half-angle, contamination concern for solar arrays
15. Throttling: adjust voltage and flow rate, maintain efficiency over 3:1 range
16. Startup: requires ignition sequence with elevated cathode flow
17. Lifetime: 10,000-30,000 hours at full power, limited by channel erosion
18. Specific mass: 1-3 kg/kW (thruster + PPU), improving with technology maturation
19. Applications: orbit raising (GEO satellites), station-keeping, deep-space missions
20. Flight heritage: SMART-1 (ESA), Dawn (NASA), Starlink, commercial GEO satellites
""",
        key_factors=[
            "Specific impulse (Isp) and thrust efficiency",
            "Power level (kW) and thrust (mN)",
            "Propellant choice (xenon, krypton, iodine)",
            "Lifetime (operating hours before failure)",
            "Throttle range and efficiency variation",
            "Plume characteristics (divergence, contamination)",
            "Specific mass (kg/kW) of thruster and PPU"
        ],
        primary_authority=[
            "Goebel, Katz - Fundamentals of Electric Propulsion",
            "Martinez-Sanchez, Pollard - Spacecraft Electric Propulsion",
            "NASA GRC Electric Propulsion Group publications",
            "AIAA Electric Propulsion Technical Committee"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PROPULSION,
        counter_arguments=[
            "Ion thrusters achieve higher Isp (3000-9000s) but lower thrust density",
            "Chemical propulsion provides much higher thrust for rapid maneuvers",
            "Resistojets and arcjets offer middle ground (500-1000s Isp, simpler)"
        ],
        resolution_strategy="Hall thrusters are optimal for GEO orbit raising and station-keeping (high Isp, moderate thrust); use chemical for rapid maneuvers, ion for deep-space.",
        controlling_precedent="Dawn mission to Vesta and Ceres used ion thrusters; most modern GEO comsats use Hall thrusters for NSSK"
    ),

    DoctrineBlock(
        topic="Solar Array Power Degradation in LEO",
        keywords=["solar array", "degradation", "atomic oxygen", "ATOX", "UV radiation", "plasma", "BOL", "EOL"],
        conclusion_template="LEO solar arrays degrade from atomic oxygen (ATOX) erosion, UV radiation, plasma interactions, and thermal cycling. Annual degradation: 2-5% in 400 km LEO. BOL to EOL power sizing must account for 15-year mission = 25-40% total degradation. Protective coatings (ITO, silicones) extend life.",
        reasoning_framework="""
Solar Array Degradation Analysis for LEO:
1. Beginning of Life (BOL) power: rated output under AM0 (1367 W/m^2) at 28°C
2. End of Life (EOL) power: BOL × (1 - annual_deg)^years, must meet mission requirements
3. Atomic oxygen (ATOX): RAM-facing surfaces erode at ~0.1 micron/year at 400 km
4. ATOX flux: 10^14-10^15 atoms/cm^2/s in LEO, decreases with altitude
5. UV radiation: degrades coverglass and adhesives, causes darkening
6. Charged particle radiation: creates defects in silicon cells, reduces voltage and current
7. Thermal cycling: -150°C (eclipse) to +120°C (sun), 5000-90000 cycles for 15-year mission
8. Micrometeoroid and debris: coverslip cracks, cell short circuits
9. Contamination: outgassing products deposit on arrays, reduce transmittance
10. Plasma interactions: differential charging can cause arcing and damage
11. Degradation models: JPL/NASA empirical curves, validated by flight telemetry
12. Protective measures: indium tin oxide (ITO) coatings for ATOX protection
13. Coverglass: 50-150 micron thick fused silica or CMX, provides radiation shielding
14. Cell technology: triple-junction (InGaP/GaAs/Ge) more radiation-resistant than Si
15. String architecture: bypass diodes prevent shaded cell from dragging down entire string
16. Articulation: single or dual-axis tracking improves power but adds complexity
17. Array sizing: EOL power + margin (typically 30% for contingency and reserves)
18. Deployable vs body-mounted: deployable allows larger area, body-mounted is simpler
19. Shadowing analysis: consider spacecraft geometry and solar beta angle variation
20. Flight data: ISS arrays show 2.7% annual degradation, Hubble 3-4% at 550 km
""",
        key_factors=[
            "Altitude and ATOX flux (lower orbit = faster degradation)",
            "Mission duration (years)",
            "Cell technology (Si, GaAs, triple-junction)",
            "Protective coatings (ITO, silicones)",
            "Thermal cycling count and range",
            "Radiation dose (protons, electrons)",
            "Micrometeoroid and debris environment"
        ],
        primary_authority=[
            "NASA GSFC Solar Array Design Handbook",
            "ESA ECSS-E-HB-20-05A - Space engineering: Solar Array design",
            "Spectrolab and Azur Space solar cell datasheets",
            "AIAA Space Power Technical Committee publications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.POWER_SYSTEMS,
        counter_arguments=[
            "Higher altitude (GEO) eliminates ATOX but increases radiation dose",
            "Advanced coatings (graphene, diamond-like carbon) may reduce degradation",
            "Nuclear power (RTG, fission) avoids solar array degradation entirely"
        ],
        resolution_strategy="Size arrays for EOL power with 30% margin; use ITO coatings for LEO below 600 km; triple-junction cells for radiation tolerance.",
        controlling_precedent="ISS solar arrays designed for 15-year life with 2.7% annual degradation; Hubble arrays replaced after 10 years due to >30% loss"
    ),

    DoctrineBlock(
        topic="Geostationary Orbit Station-Keeping Delta-V Budget",
        keywords=["GEO", "station-keeping", "NSSK", "EWSK", "delta-v", "longitude drift", "inclination control"],
        conclusion_template="GEO satellites require ~50 m/s/year delta-V for station-keeping: ~2 m/s/year for East-West (EWSK) to counter solar/lunar gravity and pressure, ~48 m/s/year for North-South (NSSK) to control inclination drift from sun-moon perturbations. 15-year mission ~= 750 m/s total.",
        reasoning_framework="""
GEO Station-Keeping Analysis:
1. GEO orbit: 42,164 km from Earth center, 35,786 km altitude, period = 23h 56m 4s
2. Station-keeping: maintain longitude slot (±0.05°) and inclination (<0.05°)
3. East-West Station-Keeping (EWSK): counters solar radiation pressure, Sun/Moon gravity
4. EWSK delta-V: ~2 m/s/year, maneuvers every few weeks
5. North-South Station-Keeping (NSSK): counters inclination drift from Sun/Moon
6. NSSK delta-V: ~48 m/s/year (dominates budget), maneuvers daily or weekly
7. Inclination drift: ~0.85°/year if uncontrolled, due to Moon's orbital plane tilt
8. Longitude drift: natural equilibrium points at 75°E and 105°W (stable), 165°E and 15°W (unstable)
9. Solar radiation pressure: ~5e-8 N/m^2 at 1 AU, depends on spacecraft area-to-mass ratio
10. Triaxial Earth gravity: J2, J22 perturbations cause longitude drift
11. Propulsion options: chemical (high thrust, low Isp), electric (low thrust, high Isp)
12. Electric propulsion: Hall or ion thrusters, Isp ~1500-3000s, reduces propellant mass by 5-10x
13. Chemical propulsion: bipropellant (Isp ~300s), fast maneuvers but high propellant mass
14. Propellant mass fraction: 40-50% for 15-year chem mission, 10-15% for electric
15. Maneuver strategy: combine NSSK/EWSK into single burns to save delta-V (vector sum)
16. Orbit raising: from GTO to GEO requires ~1500 m/s, separate from SK budget
17. Eccentricity control: maintain near-circular orbit, small delta-V (~1 m/s/year)
18. Collision avoidance: coordinate with neighboring satellites, occasional extra maneuvers
19. Deorbit at EOL: raise to graveyard orbit 200+ km above GEO (~10 m/s)
20. Flight heritage: Intelsat, SES, Eutelsat fleets demonstrate 15+ year missions with margin
""",
        key_factors=[
            "Mission duration (years)",
            "Station-keeping box (longitude and latitude tolerance)",
            "Spacecraft area-to-mass ratio (solar pressure effect)",
            "Propulsion system (chemical vs electric Isp)",
            "Maneuver efficiency (combined NSSK/EWSK)",
            "Deorbit reserve at end of life",
            "Margin for anomalies and avoidance maneuvers"
        ],
        primary_authority=[
            "Soop - Handbook of Geostationary Orbits",
            "Chao - Applied Orbit Perturbation and Maintenance",
            "ITU Radio Regulations (GEO orbital slot assignments)",
            "ECSS-E-ST-10-04C - Space environment: GEO orbit perturbations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MISSION_DESIGN,
        counter_arguments=[
            "All-electric propulsion eliminates NSSK mass penalty but requires longer orbit raising",
            "Allowing inclination drift saves delta-V but limits coverage to equatorial regions",
            "Constellation architecture may relax station-keeping requirements"
        ],
        resolution_strategy="Use electric propulsion for NSSK (dominates budget); chemical for EWSK and rapid maneuvers; size for 15-year mission with 20% margin.",
        controlling_precedent="Modern GEO comsats (Intelsat, SES) use all-electric or hybrid propulsion for station-keeping"
    ),

    DoctrineBlock(
        topic="Thermal Radiator Sizing for Heat Rejection",
        keywords=["radiator", "thermal", "heat rejection", "stefan-boltzmann", "emissivity", "view factor", "spacecraft cooling"],
        conclusion_template="Radiator heat rejection: Q = epsilon * sigma * A * T^4 (Stefan-Boltzmann), where epsilon = surface emissivity (0.8-0.9 for white paint), sigma = 5.67e-8 W/m^2/K^4, A = area, T = temperature. Two-sided radiator doubles area. Must account for solar input, albedo, and Earth IR on hot side.",
        reasoning_framework="""
Radiator Design and Sizing:
1. Stefan-Boltzmann law: Q_radiated = epsilon * sigma * A * T^4
2. Net heat rejection: Q_net = Q_radiated - Q_absorbed (solar, albedo, Earth IR)
3. Emissivity: epsilon ~= 0.85 for white paint, 0.05 for polished aluminum, 0.9 for black paint
4. Solar absorptivity: alpha ~= 0.2 for white paint, 0.9 for black paint
5. Alpha/epsilon ratio: low for radiators (white paint alpha/epsilon ~= 0.23), high for solar absorbers
6. View factor to space: F = 1 for unobstructed view, <1 if radiator sees spacecraft or Earth
7. Two-sided radiator: both sides radiate if free-standing, doubles effective area
8. Heat pipe radiator: embedded heat pipes for isothermal surface and redundancy
9. Pumped loop radiator: active fluid circulation, heavier but handles higher heat loads
10. Operating temperature: trade-off between area (lower T needs more A) and system compatibility
11. Typical range: 0-40°C for electronics, -40°C to +80°C for propellant, 200+°C for power systems
12. Solar input: 1367 W/m^2 at Earth, varies with distance (1/r^2 for heliocentric missions)
13. Earth albedo: ~30% of solar flux reflected, relevant for LEO/GEO facing Earth
14. Earth IR: ~240 W/m^2 emitted by Earth, relevant for radiators facing planet
15. Orbital variation: hot case (sun-pointing) vs cold case (eclipse or deep space view)
16. Deployment: fixed radiator size, or deployable for large heat loads (ISS radiators)
17. Coating degradation: UV, ATOX, and contamination degrade alpha/epsilon over time
18. Micrometeor protection: radiators are vulnerable, consider redundancy or shielding
19. Power system waste heat: solar array generates ~1 kW, batteries ~10% losses, electronics ~50 W
20. Sizing margin: typically 20-30% for uncertainty in heat load and degradation
""",
        key_factors=[
            "Heat rejection requirement (W)",
            "Operating temperature (K)",
            "Surface emissivity and solar absorptivity (alpha/epsilon ratio)",
            "View factor to space (obstruction by spacecraft)",
            "Two-sided vs one-sided radiator",
            "Solar, albedo, and Earth IR inputs",
            "Coating degradation over mission life"
        ],
        primary_authority=[
            "Gilmore - Spacecraft Thermal Control Handbook",
            "Incropera, DeWitt - Fundamentals of Heat and Mass Transfer",
            "NASA SP-8105 - Spacecraft Radiator Design",
            "ECSS-E-HB-31-01A - Thermal design handbook"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.THERMAL_CONTROL,
        counter_arguments=[
            "Active cooling (heat pumps, cryocoolers) can reduce radiator area but adds power load",
            "Deployable radiators increase area but add mechanical complexity and risk",
            "Phase-change materials can buffer transient loads and reduce radiator size"
        ],
        resolution_strategy="Size radiators for hot case with 30% margin; use white paint for low alpha/epsilon; consider deployment for heat loads >1 kW.",
        controlling_precedent="ISS uses deployable ammonia-loop radiators (14 panels, ~1800 m^2 total) for 70+ kW heat rejection"
    ),

    DoctrineBlock(
        topic="Star Tracker Accuracy and Noise Sources",
        keywords=["star tracker", "attitude determination", "quaternion", "centroiding", "arc-second", "stray light"],
        conclusion_template="Star trackers achieve 1-30 arc-second (3-sigma) attitude accuracy by centroiding star images. Error sources: photon noise, detector noise, stray light, thermal distortion, and catalog errors. Multi-head configuration improves availability and redundancy.",
        reasoning_framework="""
Star Tracker Performance Analysis:
1. Operating principle: image star field, match pattern to catalog, solve attitude quaternion
2. Accuracy: 1-30 arc-seconds (1 arc-sec = 4.8 microradians), limited by centroiding precision
3. Centroiding: sub-pixel star position from PSF (point spread function) fitting
4. Photon noise: sqrt(N) uncertainty in star signal (N photons), dominates for faint stars
5. Detector noise: read noise, dark current, typically 5-50 electrons RMS
6. Star catalog: Tycho, Hipparcos, Gaia; position errors ~1 milliarcsec (negligible)
7. Lens distortion: calibrated via ground test with known star field
8. Thermal distortion: focal length change with temperature, requires stable thermal design
9. Stray light: Sun, Earth, Moon exclusion angles (typically 20-45°), baffling critical
10. Dynamic range: magnitude 2-7 stars for typical tracker, avoid saturation and faint limit
11. Lost-in-space acquisition: identify star pattern without a priori attitude, 1-60 sec
12. Update rate: 1-20 Hz, trade-off with integration time and signal-to-noise
13. Field of view: 8°×8° to 20°×20°, larger FOV aids acquisition but reduces angular resolution
14. Multi-head: 2-3 trackers at orthogonal mounting for full-sky coverage and redundancy
15. Blinding: Sun, Moon, or bright planets can saturate detector, requires safe mode
16. Processing: FPGA or DSP for real-time centroiding, pattern matching, and attitude solve
17. Radiation effects: SEU in memory can corrupt star catalog, use EDAC
18. Calibration: ground test with theodolite or star field projector for alignment
19. Flight heritage: Hubble (Fine Guidance Sensors, <10 milliarcsec), GPS (Goodrich, ~5 arcsec)
20. Complementary sensors: gyros for high-rate, sun sensors for coarse safe mode
""",
        key_factors=[
            "Centroiding accuracy (sub-pixel precision)",
            "Photon and detector noise levels",
            "Stray light rejection (baffling, exclusion angles)",
            "Thermal stability (focal length variation)",
            "Field of view and star density",
            "Update rate and integration time",
            "Multi-head configuration for redundancy"
        ],
        primary_authority=[
            "Wertz - Spacecraft Attitude Determination and Control",
            "Liebe - Accuracy Performance of Star Trackers (IEEE AES)",
            "ESA Sodern, Ball Aerospace star tracker datasheets",
            "AIAA Guidance, Navigation, and Control Technical Committee"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ADCS,
        counter_arguments=[
            "Sun sensors provide coarse attitude at lower cost and no exclusion angles",
            "Gyroscopes offer high update rate but drift over time without absolute reference",
            "GPS can provide attitude via multi-antenna phase measurements (LEO only)"
        ],
        resolution_strategy="Star trackers are standard for precision pointing (<0.01°); use multi-head for redundancy; combine with gyros for high-rate dynamics.",
        controlling_precedent="Hubble Space Telescope uses Fine Guidance Sensors (essentially star trackers) for 7 milliarcsec pointing"
    ),

    DoctrineBlock(
        topic="Launch Vehicle Fairing Acoustic Environment",
        keywords=["fairing", "acoustic", "payload", "noise", "OASPL", "random vibration", "sound pressure level"],
        conclusion_template="Launch vehicle fairings expose payloads to 130-145 dB OASPL (Overall Sound Pressure Level) during ascent, with peak acoustic loads at Max-Q and transonic regime. Acoustic blankets, damping materials, and structural isolation reduce transmitted loads. Test to 3 dB above flight prediction.",
        reasoning_framework="""
Fairing Acoustic Environment and Mitigation:
1. Acoustic sources: aerodynamic turbulence over fairing (transonic, Max-Q), engine noise
2. OASPL: 130-145 dB depending on launch vehicle and fairing size (140 dB = 200 Pa RMS)
3. Frequency range: 31.5 Hz to 10 kHz, typically octave or 1/3-octave band specification
4. Peak loads: Max-Q (maximum dynamic pressure) at ~10-20 km altitude, transonic buffet
5. Duration: 60-120 seconds of high acoustic load during ascent
6. Acoustic blankets: fiberglass or foam inside fairing, absorbs sound energy
7. Damping materials: viscoelastic layers on fairing structure reduce panel resonance
8. Payload isolation: soft-mount spacecraft to reduce transmitted vibration
9. Random vibration: acoustic loads induce structural vibration, specified in g^2/Hz PSD
10. Acoustic-to-vibration coupling: panel modes excited by acoustic pressure fluctuations
11. Testing: reverberant chamber or direct field acoustic test (DFA), progressive wave
12. Test levels: typically 3 dB above flight prediction (factor of ~1.4 in pressure)
13. Fairing venting: pressure equalization ports prevent pressure buildup during ascent
14. Structural dynamics: panel modes, ring modes, and shell modes of fairing
15. Payload sensitivity: solar arrays, antennas, and thin structures most vulnerable
16. Fatigue: high-cycle acoustic loading can cause fatigue in thin-walled structures
17. Nonlinear effects: large-amplitude panel vibrations can shift resonance frequencies
18. Launch vehicle comparison: Falcon 9 ~135 dB, Delta IV ~138 dB, Ariane 5 ~140 dB
19. Risk mitigation: modal survey before/after acoustic test to detect damage
20. Flight data: instrumented fairings provide acoustic measurements for future predictions
""",
        key_factors=[
            "Launch vehicle and fairing type",
            "OASPL (dB) and frequency spectrum",
            "Acoustic blanket thickness and coverage",
            "Payload structure natural frequencies",
            "Test margin (typically 3 dB above flight)",
            "Duration of high acoustic load",
            "Fairing venting and pressure equalization"
        ],
        primary_authority=[
            "NASA GEVS (General Environmental Verification Standard)",
            "MIL-STD-1540E - Test Requirements for Launch, Upper-Stage, and Space Vehicles",
            "ESA ECSS-E-ST-10-03C - Testing specification",
            "Launch vehicle user's guides (SpaceX, ULA, Arianespace)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STRUCTURES,
        counter_arguments=[
            "Thicker fairings with better damping can reduce acoustic loads but add mass",
            "Active noise cancellation is emerging technology but not yet flight-proven",
            "Some small satellites use ride-share adapters that may alter acoustic environment"
        ],
        resolution_strategy="Design to launch vehicle user's guide acoustic specification with 3 dB margin; test to qualification levels; use acoustic blankets for attenuation.",
        controlling_precedent="NASA and ESA require acoustic testing for all payloads; commercial launch providers specify acoustic environments in user guides"
    ),

    DoctrineBlock(
        topic="S-Band Communication Link Budget",
        keywords=["s-band", "link budget", "EIRP", "G/T", "data rate", "bit error rate", "modulation"],
        conclusion_template="S-band (2-4 GHz) link budget: EIRP - path_loss + G/T - system_losses >= Eb/N0_required + 10*log10(data_rate) + margin. Typical LEO: 1 Mbps with 10 W transmit, 0.5 m antenna. Atmospheric attenuation <1 dB at low elevation angles.",
        reasoning_framework="""
Communication Link Budget Analysis:
1. Link equation: Pr = Pt + Gt + Gr - path_loss - losses (dBW)
2. EIRP: Effective Isotropic Radiated Power = Pt + Gt (dBW)
3. G/T: Gain-to-Noise-Temperature ratio = Gr - 10*log10(T_sys) (dB/K)
4. Path loss: 20*log10(4*pi*range/lambda) for free space, ~190 dB for 1000 km at S-band
5. S-band frequency: 2025-2120 MHz uplink, 2200-2290 MHz downlink (NASA allocations)
6. Atmospheric attenuation: <1 dB for S-band at low elevation, worse for rain (X/Ka-band)
7. Polarization loss: 0.5 dB for linear, RHCP/LHCP typically matched to avoid 20+ dB loss
8. Required Eb/N0: depends on modulation and coding (BPSK ~10 dB for BER 1e-6, turbo code reduces)
9. Data rate: R bps, increases required received power by 10*log10(R)
10. Modulation: BPSK, QPSK, 8PSK; higher order increases spectral efficiency but needs more SNR
11. Coding: convolutional, turbo, LDPC; coding gain 5-10 dB at cost of overhead
12. Antenna gain: parabolic dish (Gt = eta * (pi*D/lambda)^2), typical 20-40 dBi for spacecraft
13. Pointing loss: off-axis gain reduction, typically 0.5-2 dB budget allowance
14. Ground station: 10-30 m dishes, G/T = 20-40 dB/K, high-power amplifiers 1-20 kW
15. Doppler shift: LEO satellite approaching/receding causes ±40 kHz shift at S-band
16. Link margin: 3-6 dB above required Eb/N0 for fading, rain, and uncertainty
17. Link availability: percentage of time link closes, typically 95-99% for LEO
18. Multi-path: ground reflections cause fading, mitigated by antenna elevation >5°
19. Rain fade: S-band sees <1 dB for typical rain, much worse at Ka-band (20+ dB)
20. Flight heritage: TDRSS (NASA), DSN (Deep Space Network), commercial LEO constellations
""",
        key_factors=[
            "Frequency band (S, X, Ka) and allocated bandwidth",
            "Transmit power and antenna gain (EIRP)",
            "Range and path loss",
            "Ground station G/T ratio",
            "Data rate and required Eb/N0",
            "Modulation and coding scheme",
            "Link margin and availability requirement"
        ],
        primary_authority=[
            "Wertz, Larson - Space Mission Analysis and Design (SMAD)",
            "Ippolito - Satellite Communications Systems Engineering",
            "NASA TDRSS User's Guide",
            "ITU Radio Regulations (frequency allocations)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.COMMUNICATIONS,
        counter_arguments=[
            "X-band (8 GHz) offers higher gain with same antenna size but more rain fade",
            "Ka-band (26-40 GHz) enables very high data rates but requires large link margin",
            "Optical communications (laser) offers massive bandwidth but requires precision pointing"
        ],
        resolution_strategy="S-band for LEO command/telemetry (robust, low cost); X-band for science data (higher rate); Ka-band or optical for GEO or deep-space high-rate links.",
        controlling_precedent="Most LEO satellites use S-band for TT&C; Mars missions use X-band for science downlink"
    ),

    DoctrineBlock(
        topic="Tsiolkovsky Rocket Equation and Mass Ratio",
        keywords=["tsiolkovsky", "rocket equation", "delta-v", "mass ratio", "exhaust velocity", "specific impulse"],
        conclusion_template="Tsiolkovsky equation: delta_v = Isp * g0 * ln(m_initial / m_final), where mass ratio MR = m_initial / m_final. For single stage, MR = exp(delta_v / (Isp * g0)). High delta-V missions require high Isp or staging to avoid excessive propellant mass.",
        reasoning_framework="""
Rocket Equation Application and Staging:
1. Tsiolkovsky equation: delta_v = ve * ln(m0 / mf) = Isp * g0 * ln(MR)
2. Mass ratio: MR = m0 / mf = (m_structure + m_propellant + m_payload) / (m_structure + m_payload)
3. Propellant mass fraction: zeta = m_propellant / m0 = 1 - 1/MR
4. Single-stage-to-orbit (SSTO): requires MR ~10-15 (90-93% propellant), very challenging
5. Staging: break into multiple stages, each with smaller MR, overall performance improved
6. Payload fraction: m_payload / m0, typically 1-5% for expendable launch vehicles
7. Structural coefficient: epsilon = m_structure / (m_structure + m_propellant), typically 0.05-0.15
8. Example: LEO requires ~9 km/s, with Isp 350s → MR = exp(9000/(350*9.81)) ~= 7.8
9. Parallel staging: strap-on boosters, reduces core stage MR by offloading liftoff mass
10. Series staging: stacked stages, each optimized for different flight regimes
11. Optimal staging: Isp and structural mass vary by stage (boosters lower Isp, upper stages higher)
12. Gravity losses: vertical flight wastes delta-V fighting gravity, pitch over early
13. Drag losses: atmospheric flight incurs drag penalty, ~1-2 km/s for typical ascent
14. Steering losses: non-optimal trajectory adds ~0.5 km/s
15. Total launch delta-V: ~9.5-10 km/s for LEO accounting for losses (orbit velocity ~7.8 km/s)
16. Mars mission: ~6 km/s from LEO, total from Earth surface ~15.5 km/s
17. Reusable stages: reserve propellant for landing reduces payload but enables reuse
18. Electric propulsion: very high Isp (1500-3000s) enables high delta-V with low propellant mass
19. Oberth effect: burn at periapsis (high velocity) amplifies delta-V effect
20. Flight heritage: Saturn V (3 stages), Falcon 9 (2 stages + reusable booster), Delta IV Heavy
""",
        key_factors=[
            "Required delta-V (km/s)",
            "Specific impulse (Isp, seconds)",
            "Structural mass fraction (epsilon)",
            "Number of stages and staging strategy",
            "Gravity, drag, and steering losses",
            "Payload mass and mission",
            "Reusability vs expendable trade-off"
        ],
        primary_authority=[
            "Sutton - Rocket Propulsion Elements",
            "Turner - Rocket and Spacecraft Propulsion",
            "NASA SP-8057 - Structural Design Criteria for Launch Vehicles",
            "Humble, Henry, Larson - Space Propulsion Analysis and Design"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MISSION_DESIGN,
        counter_arguments=[
            "Air-breathing propulsion (scramjet) can reduce oxidizer mass for atmospheric flight",
            "Space tethers or momentum exchange could enable propellantless delta-V",
            "Nuclear propulsion offers very high Isp (800-1000s) but adds complexity and politics"
        ],
        resolution_strategy="Use staging for high delta-V missions (LEO and beyond); optimize Isp and structural mass per stage; electric propulsion for in-space high delta-V.",
        controlling_precedent="All orbital launch vehicles use staging; SSTO remains unproven for practical payloads"
    ),

    DoctrineBlock(
        topic="Spacecraft Bus Structural Design for Launch Loads",
        keywords=["spacecraft structure", "launch loads", "quasi-static", "random vibration", "central cylinder", "honeycomb"],
        conclusion_template="Spacecraft primary structure must survive launch quasi-static loads (10-20 g axial, 2-6 g lateral) and random vibration (0.01-0.1 g^2/Hz). Central cylinder or box-frame with aluminum honeycomb panels is standard. Design to ultimate load (1.4 × limit load) with positive margin of safety.",
        reasoning_framework="""
Structural Design for Launch Environment:
1. Load cases: quasi-static (steady acceleration), random vibration, acoustic, shock
2. Quasi-static loads: 10-20 g axial (thrust), 2-6 g lateral (wind shear, steering)
3. Ultimate load: 1.4 × limit load (safety factor), structure must not fail
4. Yield load: typically 1.1 × limit load, no permanent deformation allowed
5. Margin of safety: MS = (allowable / applied) - 1, must be positive (>0)
6. Random vibration: power spectral density (PSD) in g^2/Hz, broadband excitation
7. Acoustic loads: 130-145 dB OASPL, induces panel vibration and fatigue
8. Pyroshock: separation events (staging, fairing jettison) create high-frequency shock
9. Central cylinder: common architecture, load path through cylinder to launch adapter
10. Box-frame: alternative for large spacecraft, distributes loads through corner posts
11. Aluminum honeycomb panels: high stiffness-to-weight, buckling resistance
12. Aluminum alloys: 6061-T6, 7075-T73, 2024-T3 for high strength-to-weight
13. Composite structures: carbon fiber for ultra-light, but CTE mismatch and conductivity issues
14. Finite element analysis (FEA): NASTRAN, ANSYS for stress, buckling, and modal analysis
15. Modal survey: measure natural frequencies and mode shapes, validate FEA model
16. Coupled loads analysis (CLA): spacecraft + launch vehicle dynamic interaction
17. Qualification testing: vibration (proto-flight or acceptance), static load, acoustic
18. Workmanship factors: 1.25-1.5 on stress to account for manufacturing variability
19. Fatigue: high-cycle loads during launch and mission, check S-N curves for aluminum
20. Flight heritage: previous missions provide confidence in design approach and margins
""",
        key_factors=[
            "Quasi-static load factors (axial and lateral g)",
            "Random vibration PSD levels",
            "Structural configuration (central cylinder, box-frame)",
            "Material choice (aluminum, composite)",
            "Natural frequencies (avoid launch vehicle coupling)",
            "Margin of safety (positive required)",
            "Testing: qualification vibration, static load, acoustic"
        ],
        primary_authority=[
            "NASA GSFC GEVS - General Environmental Verification Standard",
            "ECSS-E-ST-32C - Structural design and verification",
            "MIL-HDBK-5J - Metallic Materials and Elements for Aerospace Vehicle Structures",
            "Sarafin - Spacecraft Structures and Mechanisms"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STRUCTURES,
        counter_arguments=[
            "Composite structures offer higher stiffness-to-weight but require careful design for CTE",
            "Additive manufacturing (3D printing) enables complex load paths but maturity is limited",
            "Inflatable structures could reduce launch mass but are unproven for primary structure"
        ],
        resolution_strategy="Use aluminum central cylinder or box-frame with honeycomb panels for most missions; composite for mass-critical applications; design to positive margin.",
        controlling_precedent="Hubble, GPS satellites, GEO comsats use aluminum central cylinder; ISS modules use aluminum frames"
    ),

    DoctrineBlock(
        topic="Constellation Design for Global Coverage",
        keywords=["constellation", "walker", "polar orbit", "coverage", "satellite network", "revisit time"],
        conclusion_template="Global coverage constellations use polar or inclined orbits with multiple planes. Walker constellation: T/P/F notation (T satellites, P planes, F phasing). Iridium: 66 satellites in 6 planes at 780 km, polar. GPS: 24 satellites in 6 planes at 20,200 km, 55° inclination.",
        reasoning_framework="""
Constellation Design and Optimization:
1. Coverage objective: global, regional, or specific latitude band
2. Walker constellation: T/P/F (Total satellites, Planes, relative phasing Factor)
3. Iridium example: 66/6/2 at 780 km, polar (86.4° inclination), global coverage
4. GPS example: 24/6/1 at 20,200 km, 55° inclination, 4+ satellites visible globally
5. Orbital altitude: lower = better resolution/link budget, higher = wider coverage per satellite
6. Inclination: polar (90°) for global, inclined (45-60°) for mid-latitudes, equatorial (0°) for tropics
7. Coverage metrics: percentage of time, number of satellites visible, revisit time
8. Minimum elevation angle: typically 5-10° to avoid atmospheric attenuation and obstructions
9. Latitude coverage: polar orbits cover poles, equatorial orbits miss high latitudes
10. Revisit time: time between successive passes over a given location
11. Continuous coverage: requires sufficient satellites to always have one in view
12. Handoff: satellite-to-satellite communication or ground station relay
13. Plane spacing: evenly distributed (360°/P) for uniform coverage
14. Phasing: relative position of satellites in adjacent planes, optimized for coverage gaps
15. Perturbations: J2 causes nodal precession, must maintain plane separation over time
16. Differential nodal precession: planes at different inclinations drift apart
17. Station-keeping: small maneuvers to maintain constellation geometry
18. Launch strategy: multiple satellites per launch, or dedicated rideshare
19. Deorbit planning: end-of-life disposal to avoid space debris
20. Flight heritage: GPS (1978-present), Iridium (1997), Starlink (2019), OneWeb (2020)
""",
        key_factors=[
            "Coverage requirement (global, regional, latitude band)",
            "Number of satellites and orbital planes",
            "Orbital altitude and inclination",
            "Minimum elevation angle for service",
            "Revisit time and continuous coverage",
            "Launch cost and constellation deployment strategy",
            "Station-keeping delta-V budget"
        ],
        primary_authority=[
            "Wertz, Larson - Space Mission Analysis and Design (SMAD)",
            "Walker - Satellite Constellations (Journal of the British Interplanetary Society)",
            "Rider - Optimized Polar Orbit Constellations for Redundant Earth Coverage",
            "FCC and ITU regulations for constellation licensing"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MISSION_DESIGN,
        counter_arguments=[
            "GEO satellites provide continuous coverage over one-third of Earth but miss poles",
            "Highly elliptical orbits (Molniya) offer long dwell time over high latitudes",
            "Single large satellite may suffice for regional missions instead of constellation"
        ],
        resolution_strategy="Polar LEO constellation for global coverage (Iridium model); inclined MEO for navigation (GPS model); GEO for regional communication.",
        controlling_precedent="GPS uses 24-satellite MEO constellation; Iridium uses 66-satellite LEO polar constellation"
    ),

    DoctrineBlock(
        topic="Technology Readiness Level (TRL) Assessment",
        keywords=["TRL", "technology readiness", "NASA", "maturity", "flight heritage", "risk reduction"],
        conclusion_template="TRL scale 1-9 assesses technology maturity: TRL 1 = basic principles, TRL 6 = prototype in relevant environment, TRL 9 = flight-proven. NASA requires TRL 6+ for Phase C/D (implementation). New technology must retire risk via testing and demonstration before integration.",
        reasoning_framework="""
TRL Framework and Risk Management:
1. TRL 1: Basic principles observed and reported (paper study)
2. TRL 2: Technology concept formulated (analytical model)
3. TRL 3: Proof of concept demonstrated (lab experiment)
4. TRL 4: Component validated in laboratory environment
5. TRL 5: Component validated in relevant environment (thermal vac, vibration)
6. TRL 6: System/subsystem prototype in relevant environment (integration test)
7. TRL 7: System prototype in operational environment (flight-like conditions)
8. TRL 8: Actual system completed and qualified (flight acceptance testing)
9. TRL 9: Actual system flight-proven (on-orbit operation)
10. NASA gate requirement: TRL 6 at Preliminary Design Review (PDR), TRL 8 at launch
11. Technology infusion: new tech requires parallel development and risk mitigation
12. Risk reduction: testing, analysis, and heritage reduce uncertainty
13. Flight heritage: previous successful missions raise TRL to 9 for similar applications
14. Breadboard: TRL 3-4, laboratory prototype demonstrating function
15. Brassboard: TRL 5-6, engineering model in flight-like configuration
16. Engineering model: TRL 6-7, full functionality in relevant environment
17. Qualification model: TRL 8, tested to flight qualification levels
18. Flight unit: TRL 8-9, accepted for launch and on-orbit operation
19. Technology demonstration missions: CubeSats, ISS payloads for rapid TRL advancement
20. Program risk: low TRL (<6) at Phase C/D entry creates schedule and cost risk
""",
        key_factors=[
            "Current TRL level (1-9)",
            "Required TRL for mission phase",
            "Testing completed (lab, thermal vac, vibration, flight)",
            "Flight heritage in similar applications",
            "Development timeline and budget",
            "Risk tolerance of mission",
            "Availability of alternative mature technologies"
        ],
        primary_authority=[
            "NASA TRL Definitions (NPR 7123.1C)",
            "DoD Technology Readiness Assessment Guidance",
            "ESA Technology Readiness Level Handbook",
            "GAO Technology Readiness Assessment Guide"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SYSTEMS_ENGINEERING,
        counter_arguments=[
            "TRL scale is subjective and can be gamed by optimistic assessments",
            "Some technologies (software) don't fit hardware-centric TRL definitions well",
            "Commercial space may accept lower TRL for cost or schedule advantage"
        ],
        resolution_strategy="Require TRL 6+ at PDR for critical path items; use technology demonstration missions to advance TRL; have backup options for low-TRL components.",
        controlling_precedent="NASA requires TRL 6 at PDR per NPR 7123.1; Mars missions have strict TRL requirements due to cost and lack of repair options"
    ),

    DoctrineBlock(
        topic="Solar Sail Propulsion and Characteristic Acceleration",
        keywords=["solar sail", "photon pressure", "characteristic acceleration", "propellantless", "interstellar", "lightsail"],
        conclusion_template="Solar sails use photon pressure for propellantless propulsion. Characteristic acceleration: a_c = (2 * P_sun / c) * (A / m) * (reflectivity), where P_sun = 1367 W/m^2 at 1 AU. Thin films (2-10 micron aluminized mylar) achieve 0.1-1 mm/s^2. Scales as 1/r^2 from Sun.",
        reasoning_framework="""
Solar Sail Design and Performance:
1. Photon pressure: F = (2 * P / c) * A * cos^2(theta) for perfect reflector
2. Solar constant: P_sun = 1367 W/m^2 at 1 AU (Earth orbit)
3. Characteristic acceleration: a_c = F / m (mm/s^2), defines sail performance
4. Sail loading: sigma = m / A (g/m^2), lower is better, typical 5-20 g/m^2
5. Film thickness: 2-10 micron aluminized mylar or Kapton, trade-off with strength
6. Reflectivity: aluminized surface ~90%, dielectric coatings can improve to 95%
7. Distance scaling: pressure scales as 1/r^2, acceleration drops rapidly beyond 1 AU
8. Thrust vector: normal to sail, steering by tilting sail relative to Sun line
9. Spiral trajectory: gradual orbit raising by tilting sail for tangential thrust component
10. Interstellar missions: solar sail to ~5 AU, then coast (Voyager approach but faster)
11. LightSail 2 (Planetary Society): 32 m^2, 5 kg, a_c ~= 0.058 mm/s^2, flight-proven 2019
12. IKAROS (JAXA): 196 m^2, 310 kg, first interplanetary solar sail, Venus mission 2010
13. Deployment: folded sail in canister, deployed by centrifugal force or booms
14. Boom materials: carbon fiber or inflatable for stiffness and low mass
15. Attitude control: control vanes, or center-of-pressure offset for torque
16. Degradation: UV, atomic oxygen, micrometeoroid damage over time
17. Thermal: sail reaches equilibrium ~400 K at 1 AU, must avoid overheating
18. Mission applications: orbit raising, station-keeping (GEO with no propellant), deorbit
19. Laser-pushed sails: Breakthrough Starshot concept, ~1 g acceleration to relativistic speeds
20. Limitations: very low thrust, long mission duration, requires large area
""",
        key_factors=[
            "Sail area (m^2) and film thickness (microns)",
            "Total mass including boom and payload (kg)",
            "Sail loading (g/m^2) and characteristic acceleration (mm/s^2)",
            "Reflectivity and optical properties",
            "Distance from Sun (photon pressure scales as 1/r^2)",
            "Deployment mechanism and reliability",
            "Mission duration and delta-V requirement"
        ],
        primary_authority=[
            "McInnes - Solar Sailing: Technology, Dynamics and Mission Applications",
            "Wright - Space Sailing",
            "LightSail 2 mission reports (Planetary Society)",
            "AIAA Solar Sail Technical Committee"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.PROPULSION,
        counter_arguments=[
            "Electric propulsion (ion, Hall) provides controllable thrust and higher acceleration",
            "Chemical propulsion offers vastly higher thrust for rapid maneuvers",
            "Laser-pushed sails require massive ground infrastructure and are unproven"
        ],
        resolution_strategy="Solar sails for long-duration propellantless missions (deorbit, station-keeping, interplanetary); not suitable for rapid maneuvers or high delta-V in short time.",
        controlling_precedent="IKAROS (JAXA) demonstrated interplanetary solar sail in 2010; LightSail 2 demonstrated orbit raising in 2019"
    ),

    DoctrineBlock(
        topic="Satellite Drag and Orbital Decay in LEO",
        keywords=["drag", "atmospheric density", "orbital decay", "ballistic coefficient", "solar activity", "deorbit"],
        conclusion_template="LEO satellites experience atmospheric drag: F_drag = 0.5 * rho * v^2 * Cd * A. Orbital decay rate depends on ballistic coefficient (m / Cd*A) and atmospheric density (solar activity dependent). Below 400 km, lifetime <1 year. Above 600 km, lifetime >25 years.",
        reasoning_framework="""
Atmospheric Drag and Lifetime Analysis:
1. Drag force: F_drag = 0.5 * rho * v^2 * Cd * A (Newtons)
2. Atmospheric density: rho varies with altitude, solar activity, geomagnetic storms
3. Velocity: v ~= 7.5-7.8 km/s for LEO (nearly constant for drag purposes)
4. Drag coefficient: Cd ~= 2.2 for typical spacecraft (depends on shape and orientation)
5. Cross-sectional area: A (m^2), varies with attitude (sun-tracking vs nadir-pointing)
6. Ballistic coefficient: B = m / (Cd * A), higher B = slower decay
7. Altitude dependence: rho ~= rho0 * exp(-h / H), where H = scale height ~60 km at 400 km
8. Solar activity: density increases by 10x at solar maximum vs minimum (11-year cycle)
9. Orbital decay rate: da/dt proportional to -rho * A / m, semi-major axis decreases
10. Lifetime estimation: integrate da/dt over altitude, accounting for density variation
11. 400 km altitude: lifetime ~1 year at solar max, ~3 years at solar min (for typical satellite)
12. 600 km altitude: lifetime ~25 years at solar max, ~100+ years at solar min
13. 800 km altitude: lifetime >>100 years, space debris concern
14. Deorbit strategies: active (thruster burn), passive (drag sail), natural (wait)
15. Drag sail: deployable area to increase A and accelerate decay
16. 25-year rule: FCC/NASA require deorbit within 25 years of end-of-life
17. Atmospheric models: NRLMSISE-00, JB2008 for density prediction
18. Uncertainty: solar activity prediction is poor beyond ~1 solar cycle
19. Orbital perturbations: J2, luni-solar gravity also affect lifetime but drag dominates in LEO
20. Flight heritage: ISS requires periodic reboost due to drag; Hubble altitude maintenance
""",
        key_factors=[
            "Orbital altitude (km)",
            "Ballistic coefficient (mass / Cd*A)",
            "Solar activity level (solar flux F10.7)",
            "Mission duration and end-of-life planning",
            "Deorbit strategy (active, passive, natural)",
            "Cross-sectional area and orientation",
            "Atmospheric density model uncertainty"
        ],
        primary_authority=[
            "Vallado - Fundamentals of Astrodynamics and Applications",
            "King-Hele - Satellite Orbits in an Atmosphere",
            "NASA Orbital Debris Program Office guidelines",
            "IADC (Inter-Agency Space Debris Coordination Committee) standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MISSION_DESIGN,
        counter_arguments=[
            "Active deorbit with thrusters is faster but consumes propellant",
            "Electrodynamic tethers can deorbit without propellant but add complexity",
            "Natural decay below 400 km is reliable and requires no additional hardware"
        ],
        resolution_strategy="Design for natural decay <400 km altitude within 25 years; use drag sail for 400-600 km; active deorbit for >600 km to meet debris mitigation.",
        controlling_precedent="NASA and FCC require 25-year deorbit per ODMSP (Orbital Debris Mitigation Standard Practices)"
    ),

    DoctrineBlock(
        topic="Cryogenic Propellant Boiloff and Storage",
        keywords=["cryogenic", "boiloff", "LOX", "LH2", "liquid hydrogen", "liquid oxygen", "zero boiloff", "active cooling"],
        conclusion_template="Cryogenic propellants (LOX 90K, LH2 20K) boil off due to heat leak. Passive boiloff: 0.1-1% per day for LOX, 1-3% per day for LH2. Zero-boiloff storage (ZBO) uses cryocoolers to remove heat leak, enabling long-duration missions (Mars, lunar surface).",
        reasoning_framework="""
Cryogenic Propellant Management:
1. Liquid oxygen (LOX): boiling point 90.2 K (-183°C), density 1141 kg/m^3
2. Liquid hydrogen (LH2): boiling point 20.3 K (-253°C), density 70.8 kg/m^3
3. Heat leak sources: conduction (tank supports), radiation (MLI imperfect), residual gas
4. Boiloff rate: Q_leak / (m * h_fg), where Q_leak = heat leak (W), h_fg = latent heat
5. Passive thermal protection: MLI (15-60 layers), vacuum-jacketed tanks, minimal supports
6. Typical boiloff: LOX 0.1-0.5%/day, LH2 1-3%/day for well-insulated tanks
7. Mission impact: 30-day Mars transit loses 3-9% LH2, 30-90% LOX depending on insulation
8. Zero-boiloff storage (ZBO): cryocooler removes heat leak, maintains liquid state
9. Cryocooler types: Stirling, pulse-tube, Brayton cycle, turbo-Brayton
10. Cryocooler performance: 20-50 W cooling at 20K for 500-1000 W input power (COP ~2-5%)
11. Trade-off: cryocooler mass/power vs boiloff propellant loss
12. Venting: boiloff gas must be vented to prevent pressure buildup, lost propellant
13. Slosh baffles: prevent liquid motion in microgravity, maintain thermal stratification
14. Vapor-cooled shield (VCS): boiloff gas cools intermediate shield before venting
15. Mixing: prevent thermal stratification (hot gas on top, cold liquid below)
16. Liquid acquisition: capillary devices (screens, vanes) to ensure liquid at tank outlet
17. Long-duration storage: lunar surface missions require ZBO for months to years
18. Flight heritage: Centaur upper stage (LOX/LH2), Space Shuttle ET, SLS core stage
19. Future missions: Mars landers, lunar ISRU propellant depots require advanced storage
20. Cost: cryocoolers add complexity, mass, and power but enable long missions
""",
        key_factors=[
            "Propellant type (LOX, LH2, liquid methane)",
            "Mission duration (days to months)",
            "Tank insulation quality (MLI layers, vacuum)",
            "Boiloff rate (%/day)",
            "Cryocooler availability (mass, power, reliability)",
            "Venting strategy (waste vs recondense)",
            "Thermal environment (deep space vs lunar surface)"
        ],
        primary_authority=[
            "Sutton - Rocket Propulsion Elements",
            "NASA Cryogenics Technology Development Roadmap",
            "Notardonato - Zero Boil-Off Storage of Cryogenic Propellants (NASA KSC)",
            "AIAA Cryogenic Propellant Management Technical Committee"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PROPULSION,
        counter_arguments=[
            "Storable propellants (NTO/MMH) avoid boiloff entirely but lower Isp",
            "Liquid methane (111K) has lower boiloff than LH2 and higher density",
            "In-situ propellant production (Mars ISRU) can replenish boiloff losses"
        ],
        resolution_strategy="Use passive insulation for short missions (<30 days); ZBO cryocoolers for long missions (Mars, lunar surface); consider methane as compromise.",
        controlling_precedent="Apollo LM used passive LOX/fuel storage for ~10 days; future Mars missions require ZBO for 6-9 month transits"
    ),

    DoctrineBlock(
        topic="Gravity Assist Trajectory Design",
        keywords=["gravity assist", "flyby", "slingshot", "planetary encounter", "oberth effect", "delta-v", "patched conic"],
        conclusion_template="Gravity assist uses planetary flyby to change spacecraft velocity magnitude and direction without propellant. Delta-V gain scales with planet mass and encounter velocity. Patched-conic method: solve heliocentric and planetocentric trajectories separately, match at sphere of influence.",
        reasoning_framework="""
Gravity Assist Mechanics and Mission Design:
1. Principle: spacecraft enters planet's gravity well, deflects trajectory, exits with different velocity
2. Energy conservation: v_infinity magnitude is same before/after flyby (planet frame), but direction changes
3. Heliocentric frame: velocity change relative to Sun, can increase or decrease orbital energy
4. Delta-V equivalent: change in heliocentric velocity magnitude, no propellant consumed
5. Turning angle: delta = 2 * arcsin(1 / (1 + r_p * v_inf^2 / mu)), where r_p = periapsis radius
6. Maximum deflection: close flyby (low r_p), high v_infinity, massive planet
7. Jupiter gravity assist: typical delta-V gain ~5-10 km/s, enables outer planet missions
8. Venus gravity assist: enables solar approach missions (Parker Solar Probe)
9. Multiple flybys: chain assists to build up energy incrementally (Voyager Grand Tour)
10. Launch window: planetary alignment dictates optimal launch date, repeats every synodic period
11. Patched-conic method: assume sphere of influence separates heliocentric and planetocentric motion
12. Sphere of influence: r_SOI ~= a * (m_planet / m_sun)^(2/5), where a = semi-major axis
13. Design variables: launch date, arrival date, flyby altitude, flyby sequence
14. Trajectory optimization: minimize delta-V or flight time, constrained by launch window
15. B-plane targeting: flyby aim point defined by impact parameter vector in B-plane
16. Tisserand parameter: conserved quantity for restricted 3-body problem, used to classify orbits
17. Oberth effect: burn at periapsis (high velocity) amplifies delta-V effect, synergistic with gravity assist
18. Radiation belts: close flybys expose spacecraft to high radiation (Jupiter), design constraint
19. Navigation: accurate trajectory control requires deep-space maneuvers (TCMs)
20. Flight heritage: Voyager (Jupiter/Saturn/Uranus/Neptune), Cassini (Venus/Venus/Earth/Jupiter), Parker Solar Probe (Venus×7)
""",
        key_factors=[
            "Planet mass and gravitational parameter mu",
            "Approach velocity v_infinity",
            "Periapsis radius (flyby altitude)",
            "Turning angle and deflection",
            "Heliocentric velocity change (delta-V gain)",
            "Launch window and planetary alignment",
            "Mission constraints (radiation, time, delta-V budget)"
        ],
        primary_authority=[
            "Vallado - Fundamentals of Astrodynamics and Applications",
            "Battin - An Introduction to the Mathematics and Methods of Astrodynamics",
            "Strange, Longuski - Graphical Method for Gravity-Assist Trajectory Design (JGR)",
            "JPL Mission Design and Navigation Section publications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MISSION_DESIGN,
        counter_arguments=[
            "Direct transfer with high-thrust propulsion avoids long flight times but requires more propellant",
            "Electric propulsion with long spirals can achieve similar delta-V without planetary flybys",
            "Gravity assists add mission complexity and risk (flyby navigation errors)"
        ],
        resolution_strategy="Use gravity assists for outer planet missions (Jupiter and beyond); Venus/Earth assists for inner solar system; optimize sequence for minimum delta-V or time.",
        controlling_precedent="Voyager Grand Tour used Jupiter/Saturn gravity assists; Parker Solar Probe uses repeated Venus flybys to reach Sun"
    ),

    DoctrineBlock(
        topic="Micrometeoroid and Orbital Debris (MMOD) Shielding",
        keywords=["MMOD", "micrometeoroid", "orbital debris", "whipple shield", "hypervelocity impact", "debris mitigation"],
        conclusion_template="MMOD protection uses Whipple shields: bumper breaks up projectile, rear wall stops fragments. Shield effectiveness scales with bumper spacing and thickness. Critical diameter: 1 cm debris at 10 km/s can penetrate single-wall aluminum. ISS uses multi-layer Whipple with Kevlar/Nextel stuffing.",
        reasoning_framework="""
MMOD Environment and Protection:
1. Micrometeoroid flux: ~1e-6 impacts/m^2/year for >1 cm diameter (varies with orbit)
2. Orbital debris: cataloged objects >10 cm, ~1 million objects 1-10 cm, billions <1 cm
3. Impact velocity: 10-15 km/s average in LEO (relative orbital velocity)
4. Kinetic energy: E = 0.5 * m * v^2, 1 cm at 10 km/s ~= 50 MJ (equivalent to TNT)
5. Whipple shield: bumper sheet breaks up projectile, rear wall stops fragment cloud
6. Spacing: 10-20 cm between bumper and rear wall, allows fragment dispersion
7. Bumper thickness: 1-3 mm aluminum, optimized for critical diameter ~1 cm
8. Rear wall: thicker (5-10 mm), or composite with Kevlar/Nextel for fragment capture
9. Multi-layer: 2-3 bumpers for enhanced protection, ISS modules use this approach
10. Critical diameter: d_c ~= function of shield thickness, spacing, velocity, material
11. Ballistic limit equation: empirical formula for penetration vs non-penetration
12. Stuffing materials: Kevlar, Nextel, beta cloth between bumper and rear wall
13. Hypervelocity impact physics: shock waves, melting, vaporization, fragmentation
14. Testing: light-gas gun up to 8 km/s, two-stage guns, numerical simulation (CTH, AUTODYN)
15. Design trade-off: shield mass vs protection level, typically 5-10% of spacecraft mass
16. Critical zones: pressurized modules require full MMOD protection, external boxes less critical
17. Debris avoidance: maneuver if predicted collision probability >1e-4 (ISS standard)
18. Collision probability: calculate using conjunction analysis and debris catalog
19. Debris mitigation: deorbit at EOL, passivation, avoid breakup events
20. Flight heritage: ISS shielding validated by flight data (minor impacts, no critical penetrations)
""",
        key_factors=[
            "Orbital altitude and inclination (debris flux)",
            "Mission duration (cumulative impact probability)",
            "Critical diameter for protection (typically 1 cm)",
            "Shield configuration (single vs multi-layer Whipple)",
            "Shield mass budget (5-10% of spacecraft)",
            "Impact velocity distribution (LEO vs GEO)",
            "Testing and validation (hypervelocity impact tests)"
        ],
        primary_authority=[
            "NASA TP-2003-210788 - MMOD Protection for Spacecraft",
            "ESA Space Debris Mitigation Handbook",
            "Christiansen - Handbook for Designing MMOD Protection",
            "IADC Space Debris Mitigation Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPACE_ENVIRONMENT,
        counter_arguments=[
            "Active debris removal could reduce MMOD risk but is expensive and unproven",
            "Self-healing materials may repair small penetrations autonomously",
            "Higher orbits (GEO) have lower debris flux but micrometeoroid risk increases"
        ],
        resolution_strategy="Use multi-layer Whipple shields for crewed and critical spacecraft; size for 1 cm protection in LEO; debris avoidance for larger objects.",
        controlling_precedent="ISS uses multi-layer stuffed Whipple shields; no critical penetrations in 25+ years despite minor impacts"
    ),

    DoctrineBlock(
        topic="Nuclear Thermal Propulsion (NTP) Specific Impulse",
        keywords=["nuclear thermal", "NTP", "NERVA", "reactor", "hydrogen propellant", "specific impulse", "bimodal"],
        conclusion_template="Nuclear thermal propulsion heats hydrogen propellant in fission reactor, achieving Isp ~800-1000s (double chemical). Thrust ~25-250 kN. NERVA program demonstrated technology in 1960s-70s. Challenges: radiation shielding, reactor licensing, public acceptance. Ideal for crewed Mars missions.",
        reasoning_framework="""
Nuclear Thermal Propulsion Analysis:
1. Operating principle: fission reactor heats H2 propellant to ~2500-3000 K, expelled through nozzle
2. Specific impulse: Isp = v_e / g0, where v_e = sqrt(2 * k * R * T / M) for ideal nozzle
3. Typical Isp: 800-1000s (vs 450s for LOX/LH2 chemical)
4. Propellant: hydrogen only (no oxidizer), low molecular weight maximizes exhaust velocity
5. Reactor core: graphite or carbide fuel elements, moderated with hydrogen
6. Thrust level: 25 kN (NERVA derivative) to 250 kN (large NTP), moderate vs chemical
7. Thrust-to-weight: ~3-4 (vs 50-100 for chemical), limits use to in-space propulsion
8. Reactor power: 1000-5000 MW thermal, requires radiation shielding
9. Shielding: shadow shield protects crew/payload, adds mass (~2-10 tons)
10. Radiation dose: external neutron and gamma flux during burn, requires safe distance
11. NERVA program: 1960s-70s NASA/AEC, 20+ reactor tests, demonstrated 800s Isp and 1+ hour burn
12. Bimodal NTP: reactor provides both thrust and electrical power (100s kW)
13. Mission applications: crewed Mars (reduced trip time 6→4 months), outer planet missions
14. Delta-V capability: 2-3x chemical for same propellant mass, enables faster missions
15. Restart capability: multiple burns demonstrated in NERVA tests
16. Fuel burnup: limits reactor lifetime to ~10-20 hours cumulative burn time
17. Cooling after shutdown: residual decay heat requires active cooling or radiators
18. Licensing: requires nuclear launch approval, no active restrictions but public concern
19. Alternatives: nuclear electric propulsion (ion/Hall thruster with reactor power, higher Isp but lower thrust)
20. Flight heritage: zero (NERVA was ground-test only), but technology readiness high
""",
        key_factors=[
            "Specific impulse (800-1000s, double chemical)",
            "Thrust level (25-250 kN) and thrust-to-weight (~3-4)",
            "Reactor power and fuel type",
            "Radiation shielding mass and crew dose",
            "Mission delta-V requirement (Mars, outer planets)",
            "Licensing and public acceptance",
            "Propellant (H2 only) storage and boiloff"
        ],
        primary_authority=[
            "Gunn, Ehresman - Nuclear Thermal Propulsion (NASA TP-2011-217091)",
            "NERVA Program Final Report (1972)",
            "Borowski - Nuclear Thermal Propulsion: A Proven Growth Technology for Human Mars Exploration",
            "AIAA Nuclear and Future Flight Propulsion Technical Committee"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.PROPULSION,
        counter_arguments=[
            "Chemical propulsion is flight-proven and avoids nuclear licensing issues",
            "Nuclear electric propulsion offers higher Isp (3000-9000s) but much lower thrust",
            "Solar electric propulsion avoids nuclear concerns and is sufficient for many missions"
        ],
        resolution_strategy="NTP is optimal for crewed Mars (trip time reduction, delta-V advantage); requires investment in reactor development and licensing; not competitive for cargo.",
        controlling_precedent="NERVA program demonstrated 800s Isp and multiple restarts in ground tests; no flight missions flown"
    ),

    DoctrineBlock(
        topic="Pointing Stability and Jitter Requirements",
        keywords=["pointing", "jitter", "stability", "line of sight", "imaging", "telescope", "PSD", "root-mean-square"],
        conclusion_template="Pointing stability: slow drift (<1 Hz), specified in arc-seconds over averaging time. Jitter: high-frequency vibration (>1 Hz), specified as RMS displacement or PSD. Optical telescopes require <0.01 arc-sec jitter for diffraction-limited imaging. Mitigation: vibration isolation, reaction wheel balancing.",
        reasoning_framework="""
Pointing Performance Analysis and Requirements:
1. Pointing accuracy: absolute orientation error relative to inertial frame (arc-seconds)
2. Pointing stability: low-frequency drift over integration time (arc-seconds over seconds)
3. Jitter: high-frequency vibration causing line-of-sight (LOS) motion (arc-seconds RMS)
4. Frequency separation: stability <1 Hz, jitter 1-100 Hz, structural modes >100 Hz
5. Optical requirement: jitter < diffraction limit / 10 for near-diffraction-limited imaging
6. Diffraction limit: theta = 1.22 * lambda / D (radians), e.g., 0.1 arc-sec for 1m telescope at visible
7. Jitter budget: allocate error among sources (reaction wheels, solar array, slosh, thermal snap)
8. Reaction wheel jitter: imbalance creates disturbance torques at harmonics of spin frequency
9. Wheel balancing: reduce static and dynamic imbalance to <g-cm, limits jitter
10. Vibration isolation: passive (elastomeric mounts) or active (voice coil actuators)
11. Solar array jitter: thermal snap (sun/eclipse transitions), panel modes excited by slew
12. Thermal snap: sudden temperature change causes structural deformation and vibration
13. Slosh: liquid propellant motion creates time-varying center-of-mass, low frequency (<1 Hz)
14. Control bandwidth: ADCS bandwidth must be >10x jitter frequency to attenuate
15. Gyro noise: sensor noise propagates to LOS error, must be low relative to jitter budget
16. PSD specification: power spectral density (arc-sec^2 / Hz), integrate over bandwidth for RMS
17. Image smearing: jitter during exposure time causes point spread function (PSF) broadening
18. Mission examples: Hubble <7 milliarcsec jitter, Kepler <20 milliarcsec stability
19. Testing: measure LOS motion with autocollimator, star tracker, or laser metrology
20. Trade-off: stiffer structure raises modes above control bandwidth but adds mass
""",
        key_factors=[
            "Required pointing accuracy and stability (arc-seconds)",
            "Jitter frequency range and RMS magnitude",
            "Optical diffraction limit (wavelength, aperture)",
            "Disturbance sources (wheels, solar array, thermal, slosh)",
            "Vibration isolation effectiveness",
            "ADCS control bandwidth",
            "Integration time and allowable smearing"
        ],
        primary_authority=[
            "Wertz - Spacecraft Attitude Determination and Control",
            "Sirlin, Liu - Spacecraft Jitter Attenuation (AIAA Journal)",
            "NASA GSFC Hubble Pointing Control System documentation",
            "AIAA Guidance, Navigation, and Control Technical Committee"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ADCS,
        counter_arguments=[
            "Post-processing (image deconvolution) can partially compensate for jitter-induced smearing",
            "Faster detectors (shorter exposure) reduce jitter sensitivity but increase noise",
            "Active optics (fast steering mirrors) can correct jitter in real-time"
        ],
        resolution_strategy="Allocate jitter budget across disturbance sources; use wheel balancing and isolation for reaction wheels; test with autocollimator or star tracker.",
        controlling_precedent="Hubble achieves 7 milliarcsec jitter via balanced wheels and isolation; Kepler used solar array dampers for thermal snap mitigation"
    )
]

# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY & METRICS
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    def __init__(self):
        self.queries: List[QueryMetrics] = []
        self.start_time = time.time()

    def record_query(self, metrics: QueryMetrics):
        self.queries.append(metrics)

    def get_stats(self) -> Dict[str, Any]:
        if not self.queries:
            return {
                "total_queries": 0,
                "cache_hit_rate": 0.0,
                "avg_latency_ms": 0.0,
                "uptime_seconds": time.time() - self.start_time
            }

        cache_hits = sum(1 for q in self.queries if q.cache_hit)
        total_latency = sum(q.total_latency_ms for q in self.queries)

        return {
            "total_queries": len(self.queries),
            "cache_hit_rate": cache_hits / len(self.queries),
            "avg_latency_ms": total_latency / len(self.queries),
            "uptime_seconds": time.time() - self.start_time
        }

telemetry = TelemetryCollector()

# ═══════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def semantic_normalize(query: str) -> str:
    """Normalize space systems terminology for consistent matching."""
    normalized = query.lower()

    # Orbital mechanics
    normalized = normalized.replace("hohmann transfer", "hohmann_transfer")
    normalized = normalized.replace("delta v", "delta_v")
    normalized = normalized.replace("delta-v", "delta_v")
    normalized = normalized.replace("specific impulse", "isp")

    # Thermal
    normalized = normalized.replace("multi-layer insulation", "mli")
    normalized = normalized.replace("multi layer insulation", "mli")

    # ADCS
    normalized = normalized.replace("attitude control", "adcs")
    normalized = normalized.replace("reaction wheels", "reaction_wheel")
    normalized = normalized.replace("star tracker", "star_tracker")

    # Propulsion
    normalized = normalized.replace("hall thruster", "hall_thruster")
    normalized = normalized.replace("ion engine", "ion_thruster")
    normalized = normalized.replace("specific impulse", "isp")

    return normalized

def search_doctrine_cache(query: str) -> List[DoctrineBlock]:
    """Search doctrine cache for relevant blocks."""
    normalized = semantic_normalize(query)
    query_terms = set(normalized.split())

    matches = []
    for block in DOCTRINE_CACHE:
        block_keywords = set([k.lower() for k in block.keywords])
        block_topic = set(block.topic.lower().split())

        keyword_overlap = len(query_terms & block_keywords)
        topic_overlap = len(query_terms & block_topic)

        if keyword_overlap > 0 or topic_overlap > 0:
            score = keyword_overlap * 2 + topic_overlap
            matches.append((score, block))

    matches.sort(reverse=True, key=lambda x: x[0])
    return [block for score, block in matches[:5]]

def generate_response(query: str, mode: ResponseMode, doctrine_blocks: List[DoctrineBlock]) -> str:
    """Generate response based on mode and doctrine blocks."""
    if not doctrine_blocks:
        return "No relevant space systems doctrine found for this query. Please provide more specific orbital mechanics, thermal, ADCS, propulsion, or mission design details."

    if mode == ResponseMode.FAST:
        # Concise answer from top doctrine
        top = doctrine_blocks[0]
        return f"{top.conclusion_template}\n\nKey factors: {', '.join(top.key_factors[:3])}."

    elif mode == ResponseMode.DEFENSE:
        # Audit-ready detailed analysis
        response_parts = []
        for block in doctrine_blocks[:3]:
            response_parts.append(f"## {block.topic}\n")
            response_parts.append(f"{block.conclusion_template}\n")
            response_parts.append(f"\n**Analysis Framework:**\n{block.reasoning_framework[:500]}...\n")
            response_parts.append(f"\n**Primary Authority:** {'; '.join(block.primary_authority)}\n")
            response_parts.append(f"**Confidence:** {block.confidence.value}\n")
        return "\n".join(response_parts)

    else:  # MEMO
        # Full documentation with all blocks
        response_parts = [f"# Space Systems Engineering Analysis\n"]
        response_parts.append(f"**Query:** {query}\n")
        response_parts.append(f"**Analysis Date:** {datetime.utcnow().isoformat()}Z\n\n")

        for idx, block in enumerate(doctrine_blocks, 1):
            response_parts.append(f"## {idx}. {block.topic}\n")
            response_parts.append(f"**Category:** {block.category.value}\n")
            response_parts.append(f"**Confidence:** {block.confidence.value}\n\n")
            response_parts.append(f"### Conclusion\n{block.conclusion_template}\n\n")
            response_parts.append(f"### Reasoning Framework\n{block.reasoning_framework}\n\n")
            response_parts.append(f"### Key Factors\n")
            for factor in block.key_factors:
                response_parts.append(f"- {factor}\n")
            response_parts.append(f"\n### Primary Authority\n")
            for auth in block.primary_authority:
                response_parts.append(f"- {auth}\n")
            if block.counter_arguments:
                response_parts.append(f"\n### Counter-Arguments\n")
                for arg in block.counter_arguments:
                    response_parts.append(f"- {arg}\n")
            response_parts.append(f"\n### Resolution Strategy\n{block.resolution_strategy}\n\n")
            response_parts.append("---\n\n")

        return "".join(response_parts)

def calculate_determinism_hash(query: str, response: str, doctrine_blocks: List[str]) -> str:
    """Generate SHA-256 hash for determinism verification."""
    content = f"{query}|{response}|{'|'.join(sorted(doctrine_blocks))}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="AERO10 Space Systems Engineering Intelligence Engine",
    version=VERSION,
    description="TIE-grade engine for orbital mechanics, spacecraft design, and mission analysis"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer response."""
    query_id = hashlib.md5(f"{request.query}{time.time()}".encode()).hexdigest()[:12]
    start_time = time.time()

    logger.info(f"Query {query_id}: {request.query[:100]}")

    # Search doctrine cache
    doctrine_blocks = search_doctrine_cache(request.query)
    cache_hit = len(doctrine_blocks) > 0

    # Generate response
    response_text = generate_response(request.query, request.mode, doctrine_blocks)

    # Determine confidence
    confidence = doctrine_blocks[0].confidence if doctrine_blocks else ConfidenceLevel.DISCLOSURE

    # Calculate metrics
    latency_ms = (time.time() - start_time) * 1000
    doctrine_names = [b.topic for b in doctrine_blocks]
    determinism_hash = calculate_determinism_hash(request.query, response_text, doctrine_names)

    # Record telemetry
    metrics = QueryMetrics(
        query_id=query_id,
        start_time=start_time,
        cache_hit=cache_hit,
        doctrine_blocks_triggered=doctrine_names,
        response_mode=request.mode.value,
        total_latency_ms=latency_ms,
        confidence_level=confidence.value
    )
    telemetry.record_query(metrics)

    logger.info(f"Query {query_id} completed: {latency_ms:.1f}ms, cache_hit={cache_hit}, doctrines={len(doctrine_names)}")

    return QueryResponse(
        query_id=query_id,
        response=response_text,
        confidence=confidence,
        doctrine_blocks_used=doctrine_names,
        latency_ms=latency_ms,
        cache_hit=cache_hit,
        determinism_hash=determinism_hash,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    stats = telemetry.get_stats()

    return HealthResponse(
        status="healthy",
        engine=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        doctrine_blocks=len(DOCTRINE_CACHE),
        uptime_seconds=stats["uptime_seconds"],
        total_queries=stats["total_queries"],
        cache_hit_rate=stats["cache_hit_rate"],
        avg_latency_ms=stats["avg_latency_ms"]
    )

@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": block.topic,
                "category": block.category.value,
                "keywords": block.keywords,
                "confidence": block.confidence.value
            }
            for block in DOCTRINE_CACHE
        ]
    }

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
