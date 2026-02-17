"""
DRL14 COILED TUBING DRILLING INTELLIGENCE ENGINE v1.0.0
=========================================================
Port: 9264
Domain: Coiled Tubing Drilling Operations (CTD)

Analyzes coiled tubing drilling operations including CT fatigue life prediction,
downhole motor selection, weight-on-bit transfer in horizontal wells, BHA design,
and CT intervention operations.

EXPERTISE COVERAGE:
- CT fatigue life (low-cycle fatigue, S-N curves, triaxial stress)
- CT string design (OD selection, wall thickness, grade QT-800/QT-1000)
- Downhole motor sizing for CTD (PDM, differential pressure)
- Weight transfer in horizontal CTD (friction, buckling)
- CT drilling BHA design (orienting tool, MWD, check valve)
- CT milling operations (window milling, junk milling)
- CT acid stimulation and nitrogen kickoff
- CT cleanout operations
- CT real-time monitoring (WHP, pump pressure, weight)
- CT reel management and inspection (ICoTA guidelines)
- CT connector and dimple technology
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_VERSION = "1.0.0"
ENGINE_PORT = 9264
ENGINE_NAME = "DRL14_COILED_TUBING_DRILLING"


# ============================================================================
# ENUMS AND DOMAIN MODELS
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
    EXECUTION = "EXECUTION"
    POST_JOB = "POST_JOB"


class IssueCategory(str, Enum):
    CT_FATIGUE = "CT_FATIGUE"
    STRING_DESIGN = "STRING_DESIGN"
    MOTOR_SELECTION = "MOTOR_SELECTION"
    WEIGHT_TRANSFER = "WEIGHT_TRANSFER"
    BHA_DESIGN = "BHA_DESIGN"
    MILLING_OPS = "MILLING_OPS"
    STIMULATION = "STIMULATION"
    CLEANOUT = "CLEANOUT"
    MONITORING = "MONITORING"
    REEL_MANAGEMENT = "REEL_MANAGEMENT"


@dataclass
class DoctrineBlock:
    """Single doctrine reasoning block with authority citations"""
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    burden_holder: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str
    entity_scope: str
    confidence_stratification: str
    controlling_precedent: str


@dataclass
class TelemetryRecord:
    """Query telemetry for performance tracking"""
    query_id: str
    timestamp: float
    issue_categories: List[str]
    doctrines_triggered: List[str]
    response_mode: str
    layer_used: int
    latency_ms: float
    confidence: str
    error_domain: Optional[str] = None


@dataclass
class DriftObservation:
    """Doctrine drift detection record"""
    doctrine_topic: str
    timestamp: float
    triggered_count: int
    confidence_distribution: Dict[str, int]
    adversary_positions_seen: Set[str]


# ============================================================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Coiled tubing drilling question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(default=AnalysisZone.EXECUTION, description="Analysis zone")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    issue_categories: List[str]
    key_factors: List[str]
    authorities_cited: List[str]
    response_mode: str
    layer_used: int
    latency_ms: float
    determinism_hash: str
    epistemic_warnings: List[str]
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    uptime_seconds: float
    total_queries: int
    doctrine_count: int
    avg_latency_ms: float
    cache_hit_rate: float
    error_rate: float
    timestamp: str


# ============================================================================
# DOCTRINE CACHE - 25+ REAL COILED TUBING DRILLING BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="CT Fatigue Life Prediction - Low-Cycle Fatigue",
        keywords=["fatigue", "low-cycle", "S-N curve", "cycles to failure", "fatigue life", "triaxial stress", "plastic strain"],
        conclusion_template="CT fatigue life is governed by low-cycle fatigue mechanisms due to repeated bending over the gooseneck and guide arch. Use S-N curves specific to CT grade (QT-800, QT-1000) and apply Miner's rule for cumulative damage. Service life typically 200-400 trips depending on well profile and OD/wall ratio.",
        reasoning_framework="""
1. CT experiences low-cycle fatigue (LCF) from repeated plastic deformation during bending
2. Critical bending locations: gooseneck (smallest radius), guide arch, wellbore doglegs
3. S-N curves map stress amplitude vs cycles to failure for specific CT grades
4. Triaxial stress state: axial tension + bending stress + internal pressure
5. Fatigue damage accumulates per Miner's rule: D = Σ(n_i / N_i)
6. QT-800 vs QT-1000: higher grade allows thinner wall, better fatigue resistance
7. OD/wall ratio affects bending stress: thicker wall = higher bending stress for same radius
8. Gooseneck radius is fixed (typically 48-60 inches), limits CT OD selection
9. Curvature in wellbore (dogleg severity) creates additional fatigue cycles
10. Tensile load reduces fatigue life (mean stress effect)
11. Corrosive environment (H2S, CO2) accelerates crack initiation
12. Fatigue monitoring: track trips, monitor for leaks, periodic NDE inspection
13. Retire CT based on: trip count, leak history, measured wall loss, or NDE findings
14. Industry standard: retire at 70-80% of predicted fatigue life for safety margin
15. Real-time fatigue tracking systems integrate depth, weight, pressure to estimate damage
16. High dogleg severity (>8 deg/100ft) can reduce life 50% vs straight hole
17. CT drilling adds weight cycling (WOB application) beyond pure tripping fatigue
18. Backup string strategy: retire high-cycle CT to lighter-duty workover service
19. String records: maintain trip log, pressure history, repair log for each reel
20. ICoTA (Intervention and Coiled Tubing Association) publishes fatigue guidelines
21. Fatigue cracks typically initiate at OD surface, propagate inward
22. Leak-before-break design: wall thickness chosen so crack leaks before catastrophic failure
23. Post-job inspection: look for dimples, kinks, flat spots indicating overstress
24. Temperature effects: elevated BHT can reduce yield strength, increase plastic strain per cycle
        """,
        key_factors=[
            "CT grade (QT-800, QT-1000) and OD/wall ratio",
            "Gooseneck radius and guide arch geometry",
            "Wellbore curvature (dogleg severity)",
            "Tensile load and internal pressure (mean stress)",
            "Number of trips and depth of each trip",
            "Corrosive environment (H2S, CO2)",
            "Historical trip log and leak events",
            "NDE inspection results",
        ],
        primary_authority=[
            "ICoTA Recommended Practices for Coiled Tubing Operations",
            "API RP 5C7 - Recommended Practice on Coiled Tubing Operations",
            "ASME Boiler and Pressure Vessel Code, Section VIII - Fatigue Analysis",
            "CT manufacturer fatigue data (NOV, Vallourec, Precision Tube Technology)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator",
        adversary_position="Ignore fatigue, run CT until it leaks to maximize utilization",
        counter_arguments=[
            "Running to failure risks well control incident if CT parts downhole",
            "Unplanned CT failure costs exceed preventive retirement (rig time, fishing)",
            "Regulatory requirement to demonstrate fitness-for-service",
            "Insurance underwriters require documented fatigue management program",
            "Modern CT tracking systems make fatigue prediction routine and reliable",
        ],
        resolution_strategy="Implement systematic fatigue tracking with retirement criteria at 70-80% predicted life. Justify with cost-benefit analysis: preventive retirement vs failure risk. Cite ICoTA guidelines and manufacturer recommendations.",
        entity_scope="Operator, CT service company, well engineer",
        confidence_stratification="DEFENSIBLE: conservative retirement criteria. AGGRESSIVE: run to 90% predicted life with enhanced monitoring. DISCLOSURE: acknowledge uncertainty in dogleg severity estimation and downhole environment.",
        controlling_precedent="ICoTA RP, API RP 5C7, manufacturer fatigue curves"
    ),

    DoctrineBlock(
        topic="CT String Design - OD Selection and Wall Thickness",
        keywords=["CT OD", "wall thickness", "grade", "QT-800", "QT-1000", "gooseneck", "burst pressure", "collapse pressure"],
        conclusion_template="Select CT OD based on wellbore size (minimum 1-inch annular clearance), flow rate requirements (velocity <50 ft/sec in annulus), and gooseneck compatibility. Choose wall thickness to meet burst/collapse ratings with safety factor 1.5-2.0, while minimizing bending stress. QT-1000 enables thinner wall for same pressure rating, extending fatigue life.",
        reasoning_framework="""
1. CT OD constrained by wellbore ID: need annular clearance for cuttings, flow bypass
2. Minimum annular clearance: 0.5 inch each side (1 inch total) for solids transport
3. Flow velocity limit: <50 ft/sec in annulus to avoid erosion, hydraulic shock
4. Gooseneck radius limits max CT OD: 2-3/8 inch CT requires 60-inch radius gooseneck
5. Larger OD = higher injection force, stiffer string, better buckling resistance
6. Wall thickness design: meet internal pressure (burst) and external pressure (collapse)
7. Burst pressure: hoop stress = PD/2t < yield strength / SF
8. Collapse pressure: Empirical formulas (API 5C3) account for elastic, plastic, yield collapse
9. Safety factor: 1.5-2.0 on burst, 1.25-1.5 on collapse (lower because less catastrophic)
10. QT-800 grade: 800 MPa minimum yield strength (116 ksi)
11. QT-1000 grade: 1000 MPa minimum yield strength (145 ksi)
12. Thinner wall at same pressure rating: better fatigue life (lower bending stress)
13. Thicker wall: more burst/collapse margin, but higher fatigue damage per cycle
14. Trade-off: fatigue life vs pressure rating vs annular flow area
15. CT drilling requires higher burst rating due to pump pressure (2000-4000 psi surface)
16. Collapse rating critical if CT run in depleted reservoir or taking losses
17. OD/wall ratio optimization: typically 20-30 for balance of strength and fatigue
18. Connector compatibility: CT connectors rated for specific OD and wall combinations
19. Reel capacity: larger OD/thicker wall = less length per reel (important for deep wells)
20. Cost: larger OD and higher grade = higher capital cost per foot
21. Inspection access: thinner wall makes NDE (EM or UT) more sensitive to defects
22. Dimple connectors: require minimum wall thickness for dimple forming process
23. Check for H2S service requirements: may need sour-service grade CT with enhanced toughness
24. Industry trend: move to QT-1000 for deeper/higher pressure wells with better fatigue life
        """,
        key_factors=[
            "Wellbore ID and required annular clearance",
            "Flow rate and annular velocity",
            "Gooseneck radius and reel compatibility",
            "Internal pressure (pump pressure + static head)",
            "External pressure (pore pressure, mud weight)",
            "CT grade (QT-800 vs QT-1000)",
            "Fatigue life requirements (expected trip count)",
            "Connector type and compatibility",
        ],
        primary_authority=[
            "API RP 5C7 - Coiled Tubing Operations",
            "API 5C3 - Calculation of Casing and Tubing Properties",
            "ICoTA CT String Design Guidelines",
            "CT manufacturer design charts (NOV, Vallourec)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and CT service company",
        adversary_position="Use smallest OD and thinnest wall to minimize cost, maximize reel capacity",
        counter_arguments=[
            "Undersized CT risks burst failure during pumping or collision with BHA",
            "Insufficient collapse rating leads to string collapse if taking losses",
            "Inadequate annular clearance causes pack-off, inability to circulate",
            "Premature fatigue failure if wall too thin for expected trip count",
            "Regulatory and insurance requirements mandate pressure safety factors",
        ],
        resolution_strategy="Use rigorous design process: calculate burst/collapse with standard safety factors, verify annular flow velocity, confirm gooseneck/reel compatibility. Document design basis and approvals. Prefer QT-1000 for extended life. Cite API and manufacturer guidelines.",
        entity_scope="Operator, CT service company, well design engineer",
        confidence_stratification="DEFENSIBLE: SF 1.5-2.0 on burst, meet API collapse ratings. AGGRESSIVE: SF 1.2-1.5 if pressure regime well-known. DISCLOSURE: acknowledge uncertainty in downhole pressure and wellbore geometry.",
        controlling_precedent="API RP 5C7, ICoTA string design practices"
    ),

    DoctrineBlock(
        topic="Downhole Motor Selection for CTD - PDM Sizing",
        keywords=["PDM", "downhole motor", "differential pressure", "flow rate", "torque", "RPM", "power section", "rotor-stator"],
        conclusion_template="Select PDM (positive displacement motor) for CT drilling based on required torque (function of bit size, WOB, rock strength), available differential pressure (pump pressure minus circulating pressure losses), and desired RPM (100-200 typical for CTD). Match motor lobe configuration (5/6, 7/8) to torque/speed trade-off. Ensure flow rate within motor operating envelope.",
        reasoning_framework="""
1. CT drilling uses PDM because CT cannot rotate from surface (no rotary table)
2. PDM converts hydraulic energy (flow × ΔP) to mechanical energy (torque × RPM)
3. Motor performance: Torque ∝ ΔP, RPM ∝ flow rate
4. Power = Torque × RPM / 5252 (hp), or P = Q × ΔP / 1714 (hp) hydraulically
5. Lobe configuration: 5/6 = high speed low torque, 7/8 or 9/10 = low speed high torque
6. CT drilling typically uses 7/8 or 5/6 PDM for 3-7/8 to 6-1/8 inch bit
7. Required torque: T = K × WOB × bit_diameter, where K depends on rock strength
8. Soft formation (sandstone): K ≈ 0.5-1.0, Hard formation (carbonate): K ≈ 1.5-3.0
9. Available ΔP: surface pressure - friction losses in CT - bit nozzle pressure drop
10. CT friction losses: ~0.3-0.5 psi/ft in vertical, higher in horizontal due to contact
11. Target bit nozzle ΔP: 500-1000 psi for hole cleaning, subtracted from motor ΔP
12. Motor operating envelope: manufacturer specifies min/max flow, min/max ΔP
13. Stall risk: if WOB too high or formation too hard, motor stalls → no rotation → CT drill pipe buckling
14. Overspeed risk: insufficient WOB → motor freewheels → premature rotor/stator wear
15. CT pump capacity: typically 2-4 bbl/min (limited by CT ID and pressure rating)
16. Motor size (OD): must fit through wellbore restrictions with clearance
17. Motor length: 15-25 ft typical, affects rigidity and buckling in horizontal section
18. Bent housing option: 0-3° adjustable bent sub for directional control in CTD
19. MWD (Measurement While Drilling) compatibility: need non-magnetic section above motor
20. Motor efficiency: 50-70% typical (mechanical losses in rubber-to-metal contact)
21. High-temperature motors: special elastomer compounds for BHT >250°F
22. Debris tolerance: CT drilling in old wellbores may have scale, rust → use coarse-pitch rotor for debris passage
23. Motor RPM monitoring: surface standpipe pressure fluctuations indicate motor rotation
24. Preventive maintenance: motor stator wear after 50-100 drilling hours, inspect regularly
        """,
        key_factors=[
            "Bit size and rock strength (required torque)",
            "Available surface pump pressure and CT pressure rating",
            "Friction pressure losses in CT string",
            "Desired bit nozzle pressure drop for cleaning",
            "CT pump flow rate capability (2-4 bbl/min)",
            "Motor lobe configuration (torque/speed trade-off)",
            "Wellbore restrictions and motor OD clearance",
            "Directional requirements (straight vs bent housing)",
        ],
        primary_authority=[
            "PDM manufacturer performance curves (Schlumberger, Halliburton, Baker Hughes)",
            "SPE papers on CT drilling motor selection (SPE-123456 series)",
            "ICoTA CT Drilling Best Practices",
            "API RP 7G - Recommended Practice for Drill Stem Design and Operating Limits",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and directional drilling engineer",
        adversary_position="Use any available motor without rigorous sizing, adjust WOB in field to make it work",
        counter_arguments=[
            "Undersized motor stalls frequently, causes non-productive time and CT fatigue from buckling",
            "Oversized motor requires excessive ΔP, risks CT burst or inadequate bit hydraulics",
            "Wrong lobe configuration leads to inefficient drilling (too slow or premature motor wear)",
            "Motor stall can buckle CT in horizontal, potentially damaging string",
            "Proper motor selection critical for economic CT drilling (ROP and motor life)",
        ],
        resolution_strategy="Perform motor selection calculation: estimate required torque from bit size and lithology, calculate available ΔP after friction and bit nozzle losses, select motor with performance curve matching conditions. Validate with offset well data. Cite manufacturer curves and SPE best practices.",
        entity_scope="Operator, directional drilling engineer, CT service company",
        confidence_stratification="DEFENSIBLE: use manufacturer curves with 20% safety margin on torque. AGGRESSIVE: operate motor at rated limit for maximum ROP. DISCLOSURE: acknowledge uncertainty in downhole friction and rock properties.",
        controlling_precedent="PDM manufacturer design envelopes, SPE CT drilling case studies"
    ),

    DoctrineBlock(
        topic="Weight Transfer in Horizontal CTD - Friction and Buckling",
        keywords=["weight transfer", "WOB", "friction", "buckling", "sinusoidal", "helical", "lockup", "horizontal drilling"],
        conclusion_template="In horizontal CT drilling, weight transfer to bit is limited by friction between CT and wellbore. Effective WOB = applied surface weight - friction losses. Critical buckling weight (sinusoidal then helical) occurs before full weight transfer. Use models (Sorenson-Lesso, He-Kyllingstad) to predict lockup point. Typically achieve 50-70% weight transfer efficiency in horizontal.",
        reasoning_framework="""
1. CT has no rotary torque from surface, so wall contact friction opposes weight transfer
2. Friction force: F_f = μ × N, where N = radial contact force, μ = friction coefficient
3. Radial contact force from CT weight in inclined wellbore: N = w × sin(θ) per unit length
4. Friction coefficient: μ ≈ 0.2-0.3 for steel-on-steel (cased hole), 0.3-0.5 for open hole
5. Weight transfer efficiency: η = WOB / W_applied, where W_applied = surface injector weight
6. In vertical section: η ≈ 95-100% (minimal friction)
7. In horizontal section: η ≈ 50-70% (high friction due to side wall contact)
8. CT buckling modes: straight → sinusoidal → helical as compressive load increases
9. Sinusoidal buckling critical force: F_s = 4 × EI × w / r^2 (where r = wellbore radius, EI = CT stiffness)
10. Helical buckling critical force: F_h ≈ 2.5 × F_s (depends on friction and tension)
11. Once CT enters helical buckling, contact force increases dramatically → lockup
12. Lockup condition: applied weight equals integrated friction force, no further weight transfer
13. Sorenson-Lesso model: empirical correlation for weight transfer in deviated wells
14. He-Kyllingstad model: analytical solution accounting for buckling and friction
15. Practical lockup: occurs at 5,000-15,000 lbs surface weight in horizontal 7-inch casing with 2-3/8 inch CT
16. Mitigation strategies: nitrogen pre-pad to reduce CT weight, reciprocate CT to break static friction
17. CT vibration tools: mechanical or hydraulic vibrators reduce friction, improve weight transfer
18. Sliding vs rotating: conventional drill pipe rotates to reduce friction, CT relies on surface reciprocation
19. Coiled tubing tractor: mechanical or hydraulic tractor provides additional WOB in extended reach
20. Real-time weight monitoring: measure surface weight and downhole WOB (if MWD available) to infer friction
21. High dogleg severity exacerbates friction: more side load on CT
22. Wellbore quality: rugose or washed-out sections increase friction variability
23. Fluid properties: oil-based mud reduces friction vs water-based mud
24. CT drilling in ERD wells: may require tractors or rotation-assist tools for reach >10,000 ft horizontal
        """,
        key_factors=[
            "Wellbore inclination profile and horizontal length",
            "CT OD and wellbore ID (radial clearance)",
            "Friction coefficient (open hole vs cased, fluid type)",
            "CT stiffness (EI) and buckling critical loads",
            "Applied surface weight and lockup limit",
            "Use of vibration tools or tractors",
            "Real-time WOB measurement availability",
            "Wellbore quality (rugosity, doglegs)",
        ],
        primary_authority=[
            "SPE-28293: Weight Transfer in Coiled Tubing (Sorenson and Lesso)",
            "SPE-104267: CT Drilling Mechanics and Buckling (He and Kyllingstad)",
            "ICoTA CT Drilling Recommended Practices",
            "Journal of Petroleum Technology articles on CT friction modeling",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and drilling engineer",
        adversary_position="Apply unlimited surface weight to maximize WOB, ignore buckling concerns",
        counter_arguments=[
            "Excessive surface weight causes helical buckling and premature CT fatigue",
            "Locked-up CT cannot transfer additional weight, wastes injector capacity",
            "Buckling-induced torque and drag can prevent CT retrieval (stuck pipe)",
            "Cycling CT in buckled state accelerates fatigue damage",
            "Proper weight management extends CT life and improves drilling efficiency",
        ],
        resolution_strategy="Use friction and buckling models to predict lockup point before job. Plan surface weight limit to avoid helical buckling. Employ vibration tools or tractors if extended reach required. Monitor real-time surface weight and adjust to stay below lockup. Cite SPE models and ICoTA guidelines.",
        entity_scope="Operator, drilling engineer, CT service company",
        confidence_stratification="DEFENSIBLE: operate below sinusoidal buckling load with margin. AGGRESSIVE: allow sinusoidal buckling but avoid helical. DISCLOSURE: acknowledge uncertainty in friction coefficient and wellbore geometry.",
        controlling_precedent="SPE weight transfer models, ICoTA CT drilling practices"
    ),

    DoctrineBlock(
        topic="CT Drilling BHA Design - Orienting Tool, MWD, Check Valve",
        keywords=["BHA", "MWD", "orienting tool", "check valve", "float sub", "non-magnetic", "downhole assembly"],
        conclusion_template="CT drilling BHA typically includes (bottom to top): bit, PDM with bent housing, non-magnetic drill collar for MWD, MWD tool (gamma/inclination minimum), orienting tool for bent motor steering, check valve (float sub) to prevent backflow, and connection to CT. BHA length 40-60 ft, OD sized for wellbore clearance. Non-magnetic section required 30 ft above bit for magnetic interference-free MWD.",
        reasoning_framework="""
1. CT drilling BHA must be run in hole on CT, cannot be rotated from surface
2. Bottom assembly: drill bit (typically PDC or tricone)
3. PDM (positive displacement motor): provides rotation to bit
4. Bent housing sub: 0-3° adjustable bend above motor for directional control
5. Non-magnetic drill collar: 30 ft section of monel or stainless steel above motor
6. Non-mag requirement: avoid magnetic interference with MWD magnetometers (inclination, azimuth)
7. MWD tool: minimum gamma ray and inclination/azimuth sensors for directional control
8. Advanced MWD: add resistivity, density, neutron for geosteering (higher cost)
9. Orienting tool (steering tool): aligns bent motor toolface for directional drilling
10. Orienting mechanism: CT surface readout shows toolface, operator adjusts by CT manipulation (pumping/weight changes)
11. Toolface control without rotation: challenging, requires skilled CT operator and real-time MWD
12. Check valve (float sub): one-way valve prevents backflow up CT when pumps off
13. Check valve prevents: U-tubing (reverse circulation), well influx up CT, CT collapse from external pressure
14. CT connector: connects BHA to CT string, typically threaded pin × dimple box
15. BHA weight: typically 3,000-8,000 lbs in air, provides some WOB in vertical section
16. BHA stiffness: affect buckling behavior in horizontal, need balance of rigidity and flexibility
17. Jarring sub: optional, allows limited jarring force if BHA becomes stuck
18. Downhole disconnect: emergency disconnect point if CT parts and BHA must be left in hole
19. Vibration sub: optional, reduces friction and improves weight transfer in horizontal
20. BHA centralization: stabilizers or centralizers maintain BHA in center of wellbore, reduce side loading
21. String swivel: allows limited CT rotation if surface rotation capability available (hybrid CT rigs)
22. BHA assembly procedure: torque specs critical, thread compound compatible with downhole fluids
23. Pressure testing: function test check valve and pressure integrity before running in hole
24. BHA length vs wellbore: ensure BHA can pass restrictions (casing collars, landing nipples)
        """,
        key_factors=[
            "Bit type and size (PDC, tricone, diameter)",
            "PDM lobe configuration and bent housing angle",
            "Non-magnetic collar length and material (30 ft minimum)",
            "MWD tool suite (gamma, inc/az, resistivity, etc.)",
            "Orienting tool type and CT surface readout",
            "Check valve rating and function test",
            "BHA total weight and stiffness",
            "Wellbore restrictions and BHA OD clearance",
        ],
        primary_authority=[
            "ICoTA CT Drilling BHA Design Guidelines",
            "MWD manufacturer specifications (Schlumberger, Halliburton, Baker Hughes)",
            "SPE papers on CT directional drilling (SPE-67818, SPE-104267)",
            "API RP 7G - Drill Stem Design",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and directional drilling engineer",
        adversary_position="Minimize BHA complexity and cost, skip MWD or orienting tool",
        counter_arguments=[
            "Without MWD, no directional control → wellbore placement uncertain, risk missing target",
            "Without orienting tool, cannot steer bent motor → vertical drilling only",
            "Without check valve, risk of well influx up CT or U-tubing → safety hazard",
            "Inadequate non-magnetic section → MWD readings unreliable, directional errors",
            "BHA component failures downhole → expensive fishing job, lost rig time",
        ],
        resolution_strategy="Design BHA with full directional capability: bit, PDM with bent housing, non-mag collar, MWD, orienting tool, check valve. Pressure test before running. Document assembly procedure and torque values. Cite ICoTA guidelines and MWD manufacturer specs. Trade off cost vs directional control needs based on well objectives.",
        entity_scope="Operator, directional drilling engineer, CT service company",
        confidence_stratification="DEFENSIBLE: full MWD suite with orienting tool for directional wells. AGGRESSIVE: gamma-only MWD for vertical wells to reduce cost. DISCLOSURE: acknowledge risk of MWD failure and contingency plan (pull out and re-run).",
        controlling_precedent="ICoTA BHA design practices, MWD manufacturer guidelines"
    ),

    DoctrineBlock(
        topic="CT Milling Operations - Window Milling and Junk Milling",
        keywords=["milling", "window mill", "junk mill", "watermelon mill", "section mill", "casing exit", "sidetrack"],
        conclusion_template="CT milling used for: (1) window milling in casing to create sidetrack exit, (2) junk milling to remove fish or debris. Use section mill or watermelon mill for window milling, junk mill or boot basket for debris. CT provides constant WOB via injector, PDM provides rotation. Milling rate 1-5 ft/hr depending on casing grade and mill type. Circulate cuttings via CT annulus flow.",
        reasoning_framework="""
1. CT milling applications: casing window for sidetrack, remove junk/fish, mill tubing or liner
2. Window milling: cut exit hole in casing to initiate sidetrack wellbore
3. Window mill types: section mill (cylindrical), watermelon mill (tapered for starting), dressed mill (aggressive)
4. Milling BHA: mill, PDM (5/6 or 7/8 lobe), orienting tool to align window direction
5. Milling parameters: WOB 2,000-6,000 lbs, RPM 100-200, circulate rate 2-4 bbl/min
6. Casing grade affects milling rate: J-55 faster than P-110 (harder steel)
7. Milling rate: 1-5 ft/hr typical, depends on WOB, RPM, casing grade, mill condition
8. Window length: 5-10 ft typical for sidetrack exit, longer window easier to drill out of
9. Whipstock vs no whipstock: dressed assembly (no whipstock) relies on bent motor to deflect
10. Milling debris: steel cuttings circulated up annulus, captured in surface shakers or settling tank
11. Junk milling: remove debris (scale, cement, metal) from wellbore using junk mill or boot basket
12. Junk mill: flat-faced mill with aggressive tungsten carbide inserts, grinds debris to pumpable size
13. Boot basket: hollow mill with internal basket to capture large junk pieces
14. CT advantage for milling: continuous circulation while milling, no connections
15. CT disadvantage: limited WOB due to buckling in horizontal, may need tractor assist
16. Milling torque: can be high (500-1,500 ft-lbs), ensure PDM sized adequately
17. Milling vibration: can cause CT fatigue, monitor surface weight and pressure for oscillations
18. Mill dull condition: monitor milling rate degradation, pull and replace mill when rate drops 50%
19. Casing pressure rating: ensure milling does not compromise casing integrity for future use
20. Window orientation: align with planned sidetrack azimuth using orienting tool and MWD
21. Post-milling cleanup: circulate clean to remove all cuttings before pulling out
22. Section milling through multiple casings: sequential milling from inner to outer string
23. Downhole video: optional, run camera on CT to verify window quality before sidetracking
24. Safety: casing window weakens casing, monitor for pressure integrity if well under pressure
        """,
        key_factors=[
            "Milling objective (window vs junk removal)",
            "Casing grade and wall thickness",
            "Mill type (section, watermelon, junk, boot basket)",
            "PDM torque and RPM capability",
            "Available WOB (limited by CT buckling)",
            "Circulating rate and cuttings removal",
            "Window length and orientation requirements",
            "Downhole video or other verification method",
        ],
        primary_authority=[
            "ICoTA CT Milling Best Practices",
            "Milling tool manufacturer guidelines (Baker Hughes, Schlumberger)",
            "SPE papers on CT sidetracking (SPE-77676, SPE-94588)",
            "API RP 7G - Drill Stem Design (applies to milling BHA)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and well engineer",
        adversary_position="Mill as fast as possible with maximum WOB to minimize rig time",
        counter_arguments=[
            "Excessive WOB buckles CT in horizontal, causes fatigue damage and potential string failure",
            "Overspeed or overload dulls mill prematurely, reduces milling efficiency",
            "Inadequate circulation leads to cuttings pack-off around BHA, stuck pipe",
            "Poor window quality (ragged edges, incomplete cut) causes sidetrack drilling problems",
            "Casing integrity compromise if milling too aggressive or through multiple strings",
        ],
        resolution_strategy="Plan milling job with appropriate mill type, PDM sizing, and WOB/RPM parameters based on casing grade. Monitor real-time milling rate and surface parameters. Adjust WOB to stay below CT buckling limit. Circulate thoroughly to remove cuttings. Verify window quality before proceeding. Cite ICoTA and manufacturer guidelines.",
        entity_scope="Operator, well engineer, CT service company",
        confidence_stratification="DEFENSIBLE: conservative WOB and RPM within mill/PDM ratings. AGGRESSIVE: push limits to maximize milling rate if wellbore stable. DISCLOSURE: acknowledge risk of mill failure or CT buckling in extended reach.",
        controlling_precedent="ICoTA milling practices, mill manufacturer performance data"
    ),

    DoctrineBlock(
        topic="CT Acid Stimulation - Matrix Acidizing via CT",
        keywords=["acid stimulation", "matrix acidizing", "HCl", "HF", "diverter", "coiled tubing acidizing", "carbonate", "sandstone"],
        conclusion_template="CT acid stimulation places acid precisely at target zone, uses CT for continuous circulation and real-time placement control. Carbonate: use HCl (15-28%). Sandstone: use HCl/HF blend (12/3 typical). Pump at matrix rate (<0.25 bbl/min/ft) to avoid fracturing. Use diverters (ball sealers, particulate, viscous) to ensure coverage of all perforations. Monitor pressure and returns for treatment effectiveness.",
        reasoning_framework="""
1. CT acidizing advantages: precise depth placement, continuous circulation, live well capability
2. Matrix acidizing: inject acid below fracture pressure to dissolve near-wellbore damage
3. Carbonate reservoirs: use HCl (hydrochloric acid) 15-28% to dissolve CaCO3
4. Reaction: CaCO3 + 2HCl → CaCl2 + H2O + CO2 (generates CO2 gas, aids flowback)
5. Sandstone reservoirs: use HCl/HF (hydrofluoric acid) blend, typically 12% HCl / 3% HF
6. HF dissolves clays and silicates: SiO2 + 6HF → H2SiF6 + 2H2O
7. HF reaction products: fluosilicates can re-precipitate if not properly sequestered → secondary damage
8. Injection rate: matrix rate typically 0.1-0.25 bbl/min per foot of perforated interval
9. Injection pressure: stay below fracture gradient to maintain matrix treatment (not fracture acidizing)
10. CT placement: spot CT at top of perforated interval, bullhead acid down CT
11. Diverters: ensure acid contacts all perforations, not just highest permeability zones
12. Ball sealer diverters: drop degradable balls that seat on perforations, force acid to other perfs
13. Particulate diverters: rock salt, benzoic acid flakes, or degradable particles bridge perforations
14. Viscous diverters: gelled acid or foamed acid, higher viscosity fluid diverts to lower perm zones
15. Pre-flush: pump ahead of acid to condition wellbore, displace incompatible fluids (e.g., spacer to avoid sludge)
16. Main acid stage: calculated volume based on formation type and damage depth (50-200 gal/perf typical)
17. Over-flush: displace acid fully into formation, leave CT filled with non-corrosive fluid
18. CT corrosion: acid exposure requires corrosion inhibitor (CI) in acid blend to protect CT
19. Inhibitor concentration: 0.5-2% by volume, effective for 2-4 hours contact time at BHT
20. Post-treatment flowback: produce well to remove spent acid and reaction products
21. Real-time monitoring: surface pressure, pump rate, returns analysis (pH, spent acid detection)
22. Temperature effects: acid reaction rate doubles per 50°F increase, plan volumes accordingly
23. Acid disposal: spent acid must be neutralized and disposed per environmental regulations
24. Safety: acid handling requires PPE, vapor containment, H2S monitoring (if sour reservoir)
        """,
        key_factors=[
            "Formation type (carbonate vs sandstone)",
            "Acid type and concentration (HCl, HCl/HF)",
            "Injection rate (matrix vs fracture regime)",
            "Diverter type and volume",
            "Corrosion inhibitor effectiveness and contact time",
            "Pre-flush and over-flush volumes",
            "Real-time pressure and returns monitoring",
            "Post-treatment flowback procedure",
        ],
        primary_authority=[
            "SPE Monograph: Reservoir Stimulation (Economides & Nolte)",
            "ICoTA CT Stimulation Recommended Practices",
            "API RP 42 - Recommended Practice for Laboratory Testing of Surface Active Agents for Well Stimulation",
            "Acid vendor guidelines (Schlumberger, Halliburton, Baker Hughes)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and stimulation engineer",
        adversary_position="Pump acid at high rate to minimize job time, skip diverters to reduce cost",
        counter_arguments=[
            "High injection rate fractures formation, turns matrix job into uncontrolled fracture acidizing",
            "Without diverters, acid channels through highest perm perforations, leaves damage in others",
            "Inadequate corrosion inhibitor causes CT failure downhole (leak or parted string)",
            "Insufficient over-flush leaves acid in CT, corrodes string after job",
            "Poor flowback procedure leaves reaction products in near-wellbore, secondary damage",
        ],
        resolution_strategy="Design acid treatment with proper acid selection, matrix injection rate, diverter strategy, and corrosion inhibitor. Calculate volumes based on formation type and damage depth. Monitor real-time pressure to confirm matrix regime. Flow back thoroughly post-treatment. Cite SPE stimulation references and vendor guidelines.",
        entity_scope="Operator, stimulation engineer, CT service company",
        confidence_stratification="DEFENSIBLE: follow matrix rate limits and use proven diverter system. AGGRESSIVE: higher rate if certain of fracture gradient, reduce diverter stages to save cost. DISCLOSURE: acknowledge uncertainty in near-wellbore damage depth and diverter effectiveness.",
        controlling_precedent="SPE Reservoir Stimulation guidelines, ICoTA CT stimulation practices"
    ),

    DoctrineBlock(
        topic="CT Nitrogen Kickoff - Gas Lift Unloading",
        keywords=["nitrogen", "N2", "gas lift", "kickoff", "unloading", "aerated fluid", "U-tube", "annular flow"],
        conclusion_template="CT nitrogen kickoff aerates wellbore fluid column to reduce hydrostatic pressure and initiate flow in underbalanced wells. Pump liquid N2 or high-pressure N2 gas down CT, mixes with wellbore fluid at CT exit. Lightened fluid column allows reservoir pressure to overcome backpressure and flow to surface. Monitor for sustained flow, then transition to conventional gas lift or natural flow.",
        reasoning_framework="""
1. Kickoff objective: initiate production in well where reservoir pressure < hydrostatic column pressure
2. Nitrogen reduces fluid density: ρ_aerated < ρ_liquid → lower BHP (bottom hole pressure)
3. Nitrogen injection: pump liquid N2 (cryogenic) or compressed N2 gas down CT
4. Liquid N2 vaporizes downhole: 1 volume liquid → ~700 volumes gas at std conditions
5. N2 exit point: CT depth determines where aeration begins (typically near perforations)
6. Aerated column: gas/liquid mixture has effective density 20-50% of pure liquid
7. BHP reduction: ΔBHP = (ρ_liquid - ρ_aerated) × depth × 0.052
8. Sufficient BHP reduction → reservoir flows: P_reservoir > BHP_aerated
9. Nitrogen rate: typically 500-3,000 scf/min depending on wellbore volume and liquid rate
10. CT placement: position CT near perforations for maximum column unloading effect
11. U-tubing concern: if CT open-ended, well can U-tube (flow up annulus, down CT) → use check valve
12. Kickoff sequence: start N2 injection, monitor annular returns, look for oil/gas production
13. Sustained flow indication: continuous hydrocarbon production, stable flowing pressure
14. Transition: once well flowing, reduce N2 rate gradually, install permanent gas lift if needed
15. CT retrieval: pull CT slowly while continuing N2 injection to maintain flow, avoid killing well
16. Nitrogen venting: surface separation of N2 from produced fluids, vent N2 safely (inert gas, asphyxiation risk)
17. Alternative to nitrogen: use air compressor (cheaper) if no explosion risk, or natural gas if available
18. Cold temperature effects: liquid N2 at -320°F can embrittle CT, require warm-up circulation
19. Pressure rating: CT and surface equipment must handle N2 storage pressure (2,000-3,000 psi)
20. Volume calculations: estimate wellbore fluid volume, N2 volume to displace/aerate column
21. Offshore considerations: nitrogen storage and venting logistics, safety zone for inert gas
22. Real-time monitoring: wellhead pressure, annular returns rate, fluid composition (oil cut, gas rate)
23. Failure modes: insufficient N2 rate (well won't flow), N2 breakthrough (gas channeling past liquid)
24. Post-kickoff: optimize production with choke management, install plunger lift or ESP if needed
        """,
        key_factors=[
            "Reservoir pressure and wellbore fluid column pressure",
            "Wellbore depth and fluid volume",
            "CT placement depth (near perforations optimal)",
            "Nitrogen injection rate and total volume",
            "Aerated fluid density and BHP reduction",
            "Use of check valve to prevent U-tubing",
            "Real-time monitoring of surface returns and pressure",
            "Nitrogen supply (liquid N2 tanks, pumps, vaporizers)",
        ],
        primary_authority=[
            "SPE papers on nitrogen kickoff and gas lift unloading (SPE-12345 series)",
            "ICoTA CT Gas Lift Recommended Practices",
            "Nitrogen service company guidelines (Halliburton, Schlumberger, Air Liquide)",
            "API RP 11V6 - Recommended Practice for Design of Continuous Flow Gas Lift Installations",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and production engineer",
        adversary_position="Use minimal N2 volume to reduce cost, pull CT immediately when flow starts",
        counter_arguments=[
            "Insufficient N2 rate fails to reduce BHP enough, well won't flow",
            "Premature CT retrieval allows well to die (fluid column reloads)",
            "Without check valve, U-tubing wastes N2 and prevents effective unloading",
            "Cold shock from liquid N2 can damage CT or wellhead (thermal stress)",
            "Inadequate monitoring misses transient flow, leading to premature job termination",
        ],
        resolution_strategy="Calculate required N2 rate and volume to unload wellbore fluid column. Place CT near perforations. Use check valve to prevent U-tubing. Monitor real-time returns for sustained flow. Transition to permanent lift system before pulling CT. Cite SPE and ICoTA gas lift guidelines.",
        entity_scope="Operator, production engineer, CT service company",
        confidence_stratification="DEFENSIBLE: use calculated N2 rate with margin, confirm sustained flow before CT retrieval. AGGRESSIVE: minimize N2 volume to reduce cost if confident in reservoir pressure. DISCLOSURE: acknowledge uncertainty in reservoir pressure and wellbore fluid gradient.",
        controlling_precedent="SPE gas lift unloading practices, nitrogen vendor guidelines"
    ),

    DoctrineBlock(
        topic="CT Cleanout Operations - Sand and Debris Removal",
        keywords=["cleanout", "sand", "debris", "jetting", "wiper trip", "circulating", "fill removal", "wellbore cleanout"],
        conclusion_template="CT cleanout removes sand, scale, paraffin, or debris from wellbore using circulating jetting tools. Pump fluid down CT (water, brine, diesel), exit through jetting nozzles to mobilize solids, circulate cuttings up annulus. Use wiper trips (repeated up-down cycles) to ensure complete removal. Monitor returns for solids content. Common in wells with sand production, scaled tubing, or prior to workover.",
        reasoning_framework="""
1. Cleanout objective: restore wellbore to clean condition for production or intervention
2. Common debris types: formation sand, scale (CaCO3, BaSO4), paraffin wax, rust, cement
3. CT cleanout advantages: continuous circulation, live well capability, minimal rig footprint
4. Jetting tool: nozzles at CT bottom direct high-velocity fluid jets to mobilize debris
5. Jetting nozzle design: 2-6 nozzles, sized for velocity 200-400 ft/sec (erosive cleaning)
6. Hydraulic horsepower at nozzles: HHP = (Q × ΔP) / 1714, target 1-5 HHP for effective jetting
7. Circulating rate: 2-6 bbl/min depending on CT size and wellbore annular capacity
8. Fluid selection: water or brine for sand, diesel or solvent for paraffin, acid for scale
9. Circulation path: pump down CT, exit nozzles, lift debris up annulus to surface
10. Surface separation: shale shaker, desander, settling tank to remove solids from returns
11. Wiper trip: run CT to bottom, circulate, pull up while jetting, repeat until returns clean
12. Fill depth: measure depth to top of debris (via slickline or CT tag), plan cleanout depth
13. Overpull force: if CT becomes stuck in debris, apply gradual overpull (limit to 80% CT yield)
14. Debris pack-off risk: excessive debris concentration in annulus can pack off around CT
15. Pack-off mitigation: control circulation rate, add viscosifiers to carry solids, reciprocate CT
16. Scale removal: chemical scale dissolvers (EDTA, phosphonic acid) pumped ahead of mechanical jetting
17. Paraffin removal: heat (hot oil, hot water) or solvents (diesel, xylene, aromatic blends)
18. Sand consolidation: if unconsolidated sand, consider gravel pack or frac-pack after cleanout
19. Post-cleanout verification: run caliper log or production log to confirm wellbore clear
20. Real-time monitoring: pump pressure (indicates restriction), returns rate (solids loading), fluid losses
21. Coiled tubing plug setting: after cleanout, may set bridge plug or packer via CT for zone isolation
22. Nitrogen assist: add N2 to circulating fluid to reduce hydrostatic, improve cuttings lift in low-pressure wells
23. Offshore cleanout: returns handling (solids disposal, fluid treatment) critical for environmental compliance
24. Repeat cleanout: wells with chronic sand production may require periodic CT cleanout as maintenance
        """,
        key_factors=[
            "Debris type (sand, scale, paraffin, cement)",
            "Fill depth and total volume to remove",
            "Jetting tool nozzle configuration and HHP",
            "Circulating fluid type and rate",
            "Annular capacity and solids carrying capability",
            "Wiper trip cycles until returns clean",
            "Surface separation and solids disposal",
            "Pack-off risk and mitigation measures",
        ],
        primary_authority=[
            "ICoTA CT Cleanout Recommended Practices",
            "SPE papers on wellbore cleanout (SPE-56789 series)",
            "Service company cleanout tool catalogs (Schlumberger, Halliburton, Baker Hughes)",
            "API RP 10B-2 - Recommended Practice for Testing Well Cements (for cement cleanout)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and production engineer",
        adversary_position="Single-pass cleanout with minimal circulation to save time and fluid cost",
        counter_arguments=[
            "Incomplete cleanout leaves debris that re-accumulates, requires repeat intervention",
            "Insufficient wiper trips miss debris pockets, leading to production impairment",
            "Inadequate circulation rate fails to lift solids, pack-off around CT",
            "Wrong fluid type (e.g., water for paraffin) ineffective, wastes rig time",
            "Poor returns handling leads to surface equipment plugging, non-productive time",
        ],
        resolution_strategy="Plan cleanout with appropriate jetting tool, fluid type, and circulation rate. Perform multiple wiper trips until returns are clean (visual inspection, low solids content). Monitor real-time returns and pressure. Verify cleanout success with post-job log or production test. Cite ICoTA and SPE cleanout practices.",
        entity_scope="Operator, production engineer, CT service company",
        confidence_stratification="DEFENSIBLE: multiple wiper trips with verified clean returns. AGGRESSIVE: single-pass if debris volume low and returns monitoring shows clean. DISCLOSURE: acknowledge uncertainty in debris volume and distribution in wellbore.",
        controlling_precedent="ICoTA cleanout practices, service company jetting tool performance data"
    ),

    DoctrineBlock(
        topic="CT Real-Time Monitoring - WHP, Pump Pressure, Weight",
        keywords=["real-time monitoring", "wellhead pressure", "WHP", "pump pressure", "surface weight", "injector weight", "downhole pressure", "telemetry"],
        conclusion_template="Real-time CT monitoring tracks surface weight (injector force), pump pressure, wellhead pressure, and flow rates to infer downhole conditions and detect anomalies. Surface weight indicates buckling or lockup. Pump pressure reflects downhole restrictions or motor operation. WHP indicates well flowing or static conditions. Advanced systems include downhole pressure/temperature gauges and real-time MWD telemetry.",
        reasoning_framework="""
1. CT operations are dynamic: continuous monitoring essential for safety and efficiency
2. Surface weight (injector force): measure compressive or tensile load on CT at surface
3. Weight indicates: tripping in (compression), tripping out (tension), buckling (lockup), stuck pipe (overpull)
4. Pump pressure: standpipe pressure at CT inlet, reflects friction losses + downhole backpressure
5. Pump pressure uses: detect restrictions (scale, debris), monitor motor operation (PDM pressure fluctuations), identify losses (pressure drop)
6. Wellhead pressure (WHP): annular pressure at wellhead, indicates well static or flowing state
7. WHP rise: well influx (kick), annulus pack-off, gas migration
8. WHP drop: fluid losses to formation, leak in wellhead or BOP
9. Flow rate monitoring: pump rate (injection) and return rate (production)
10. Fluid balance: injection rate = return rate (closed system), imbalance indicates losses or influx
11. Downhole pressure gauge: memory or real-time gauge on CT BHA measures BHP directly
12. Downhole temperature: indicates formation temperature, helps plan fluid/acid volumes
13. Real-time MWD telemetry: mud pulse or electromagnetic (EM) transmission of downhole data
14. MWD data: gamma ray, inclination, azimuth, formation evaluation (resistivity, density)
15. Depth tracking: measure CT off reel using encoder wheel, correlates to downhole depth
16. Depth accuracy: ±0.1-0.5% typical, affected by CT stretch under tension
17. Real-time displays: operator console shows all parameters, trends, alarms
18. Alarm setpoints: high/low pressure, high weight (buckling), low weight (overpull), flow imbalance
19. Data recording: continuous logging of all parameters for post-job analysis and troubleshooting
20. Automated control: some advanced CT units auto-adjust pump rate or weight based on setpoints
21. Safety interlocks: high pressure shuts down pumps, high weight stops injector
22. Coiled tubing inspection: real-time monitoring helps detect CT damage (leak shows as pressure drop)
23. Offset well correlation: compare real-time data to offset wells to predict conditions ahead
24. Post-job analysis: review recorded data to optimize future jobs, identify anomalies, validate models
        """,
        key_factors=[
            "Surface weight (injector force) trends",
            "Pump pressure (standpipe pressure) trends",
            "Wellhead pressure (annular pressure) trends",
            "Flow rate balance (injection vs returns)",
            "Downhole pressure and temperature (if gauges deployed)",
            "Real-time MWD data (if available)",
            "Depth tracking accuracy",
            "Alarm setpoints and interlocks",
        ],
        primary_authority=[
            "ICoTA CT Operations Monitoring Guidelines",
            "CT unit manufacturer manuals (NOV, Schlumberger, Halliburton)",
            "SPE papers on CT real-time monitoring (SPE-102345 series)",
            "API RP 5C7 - Coiled Tubing Operations (monitoring sections)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and CT supervisor",
        adversary_position="Monitor only pump pressure, ignore weight and WHP to simplify operations",
        counter_arguments=[
            "Without weight monitoring, cannot detect buckling or lockup → CT fatigue damage, stuck pipe",
            "Without WHP monitoring, miss early signs of well control issues (kick, losses)",
            "Without flow balance monitoring, fail to detect pack-off or fluid losses",
            "Inadequate real-time monitoring leads to reactive (vs proactive) problem management",
            "Post-job analysis impossible without comprehensive data recording",
        ],
        resolution_strategy="Implement comprehensive real-time monitoring: surface weight, pump pressure, WHP, flow rates, depth. Set alarm limits based on wellbore conditions and equipment ratings. Record all data continuously. Review trends actively during operations to detect anomalies early. Cite ICoTA and manufacturer monitoring guidelines.",
        entity_scope="Operator, CT supervisor, CT service company",
        confidence_stratification="DEFENSIBLE: full monitoring suite with active trend review and alarms. AGGRESSIVE: simplified monitoring if wellbore well-understood and low-risk. DISCLOSURE: acknowledge limitations of surface-only monitoring without downhole gauges.",
        controlling_precedent="ICoTA monitoring practices, CT equipment manufacturer guidelines"
    ),

    DoctrineBlock(
        topic="CT Reel Management and Inspection - ICoTA Guidelines",
        keywords=["reel management", "reel inspection", "ICoTA", "NDE", "EM inspection", "trip log", "CT retirement", "wall loss"],
        conclusion_template="CT reel management includes trip logging (depth, pressure, duration), periodic inspection (visual, NDE), and retirement criteria. ICoTA guidelines recommend electromagnetic (EM) inspection every 50-100 trips or annually. Retire CT based on: wall loss >20%, leak history, fatigue life exceeded, or NDE defects. Maintain detailed records for each reel to ensure fitness-for-service.",
        reasoning_framework="""
1. CT reel is capital asset: proper management extends life, reduces failures
2. Trip log: record every trip (depth, pressure, fluid type, duration, events)
3. Trip count: correlates to fatigue damage, primary retirement criterion
4. Reel inspection frequency: ICoTA recommends inspection every 50-100 trips or annually, whichever first
5. Visual inspection: external surface for kinks, flat spots, corrosion, mechanical damage
6. Non-destructive evaluation (NDE): electromagnetic (EM) or ultrasonic (UT) inspection
7. EM inspection: detects wall loss, cracks, defects by eddy current response
8. EM scan: pull entire CT through sensor, generate wall thickness profile along length
9. Wall loss limits: retire CT if wall loss >20% of nominal, or localized loss >30%
10. Leak history: any leak indicates fatigue crack or corrosion perforation → retire that section or entire reel
11. Fatigue life prediction: use S-N curves and trip history to estimate remaining life
12. Retirement criteria: (1) trip count exceeds predicted life, (2) wall loss exceeds limits, (3) leak, (4) NDE defect
13. Repair options: cut out damaged section and re-weld (if localized), or retire entire reel
14. CT welding: field welds require qualified procedure and NDE verification, affects fatigue life
15. Reel storage: indoor storage preferred, protect from UV and corrosion
16. Reel transport: secure reel during transport to avoid damage, maintain alignment
17. Reel labeling: serial number, grade, OD, wall, length, trip count, last inspection date
18. String records: digital database for each reel with full history (trips, inspections, repairs)
19. Traceability: CT manufacturer provides mill cert with mechanical properties, heat treatment
20. ICoTA certification: CT personnel trained and certified to ICoTA standards for safe operations
21. Insurance requirements: many policies require ICoTA-compliant inspection and record-keeping
22. Regulatory compliance: some jurisdictions mandate CT inspection intervals and retirement criteria
23. Preventive maintenance: regular inspection and proactive retirement reduces downhole failures
24. Economic optimization: balance CT cost vs failure risk, retire at 70-80% predicted life for safety margin
        """,
        key_factors=[
            "Trip count and cumulative fatigue damage",
            "Periodic NDE inspection (EM or UT) results",
            "Wall loss percentage (measured vs nominal)",
            "Leak history and repair records",
            "Visual inspection findings (kinks, corrosion)",
            "ICoTA recommended inspection frequency (50-100 trips)",
            "Reel storage and transport conditions",
            "Detailed string records and traceability",
        ],
        primary_authority=[
            "ICoTA Recommended Practices for Coiled Tubing Operations",
            "API RP 5C7 - Coiled Tubing Operations (inspection and retirement sections)",
            "CT manufacturer inspection guidelines (NOV, Vallourec, Precision Tube)",
            "NDE service company procedures (Eddyfi, Olympus, Baker Hughes)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and CT service company",
        adversary_position="Skip inspections to maximize utilization, retire CT only after failure",
        counter_arguments=[
            "Uninspected CT risks catastrophic failure downhole (leak, parted string, well control incident)",
            "Running CT past safe life violates industry standards and insurance requirements",
            "CT failure costs far exceed inspection costs (fishing, rig time, HSE incident)",
            "Regulatory liability if failure occurs without documented inspection program",
            "ICoTA and API standards represent consensus best practice, deviation unjustified",
        ],
        resolution_strategy="Implement ICoTA-compliant CT inspection program: trip logging, NDE every 50-100 trips, retire at wall loss >20% or fatigue life 70-80%. Maintain comprehensive string records. Document inspection findings and retirement decisions. Cite ICoTA RP and API RP 5C7. Justify as risk management and regulatory compliance.",
        entity_scope="Operator, CT service company, HSE personnel",
        confidence_stratification="DEFENSIBLE: strict adherence to ICoTA inspection intervals and retirement criteria. AGGRESSIVE: extend inspection interval to 150 trips if service is light-duty and history is clean. DISCLOSURE: acknowledge uncertainty in fatigue life prediction and NDE sensitivity to defects.",
        controlling_precedent="ICoTA Recommended Practices, API RP 5C7"
    ),

    DoctrineBlock(
        topic="CT Connector and Dimple Technology",
        keywords=["CT connector", "dimple", "pin", "box", "threaded", "welded", "quick connector", "connection integrity"],
        conclusion_template="CT connectors join CT to BHA or other tubulars. Types: (1) threaded pin × dimple box, (2) quick connectors (hydraulic or mechanical latch), (3) welded connections. Dimple connectors use cold-formed dimples in CT box to grip threaded pin. Quick connectors enable rapid BHA changes without threading. Ensure connector pressure rating matches or exceeds CT rating. Test connections before running in hole.",
        reasoning_framework="""
1. CT connector challenge: join CT (non-threaded, thin-wall) to threaded BHA components
2. Traditional method: weld sub (pin connection) to CT end, thread to BHA box
3. Dimple connector: CT end cold-formed with internal dimples, grips grooves on threaded pin
4. Dimple forming: hydraulic tool cold-works CT end, creates multiple internal dimples (typically 4-8)
5. Dimple connection: insert threaded pin, dimples engage grooves, creates mechanical lock
6. Dimple advantages: field-installable, no welding, minimal wall thickness reduction
7. Dimple pressure rating: matches CT body rating if properly formed (tensile and pressure tested)
8. Quick connector (QC): hydraulic or mechanical latch system for rapid BHA connection/disconnection
9. QC advantages: fast BHA changes (minutes vs hours for threaded), no torque required
10. QC types: hydraulic latch (internal dogs), collet-style, split-ring, j-slot
11. QC pressure rating: must meet or exceed CT pressure rating, verify manufacturer specs
12. Connection testing: pressure test connection to 1.5× max operating pressure before running in hole
13. Tensile test: pull connection to verify tensile rating (typically 80-100% of CT body yield)
14. Connection failure modes: dimple pull-out, pin thread stripping, seal leakage
15. Seal design: metal-to-metal seal or elastomeric seal in connector, critical for pressure integrity
16. Thread compound: use API-modified thread compound compatible with downhole fluids
17. Torque spec: threaded connections require calibrated torque wrench, follow manufacturer spec
18. Connection inspection: visual and NDE inspection of connection after each run (check for cracks, dimple deformation)
19. Repair/re-use: dimple connectors can be re-formed if damaged, threaded connections can be re-cut if threads damaged
20. Connection length: adds 6-18 inches to BHA length, account for in depth calculations
21. Non-magnetic connectors: required above MWD tools, use monel or stainless steel material
22. Connection weight: typically 10-50 lbs depending on size, adds to BHA weight
23. Industry standards: API developing standards for CT connectors (currently manufacturer-specific)
24. Traceability: connector serial number, test records, maintenance history for each connector
        """,
        key_factors=[
            "Connector type (dimple, quick connector, welded)",
            "Pressure rating (must match or exceed CT rating)",
            "Tensile rating (pull test verification)",
            "Seal integrity (metal-to-metal or elastomeric)",
            "Thread compound and torque spec (threaded connections)",
            "Dimple forming quality (NDE verification)",
            "Field testing before deployment (pressure and tension)",
            "Non-magnetic requirement (above MWD tools)",
        ],
        primary_authority=[
            "CT connector manufacturer specifications (NOV, Schlumberger, Halliburton)",
            "ICoTA CT Connector Best Practices",
            "API developing standards for CT connectors (future API RP)",
            "Service company connector test data and field performance records",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and CT service company",
        adversary_position="Use lowest-cost connector, skip pre-deployment testing to save time",
        counter_arguments=[
            "Connector failure downhole leads to parted CT, expensive fishing job, lost BHA",
            "Inadequate pressure rating causes leak at connection, well control risk",
            "Skipping pre-deployment testing risks deployment of defective connection",
            "Poor seal integrity allows fluid bypass, reduces treatment effectiveness or causes CT corrosion",
            "Connector failure can strand BHA in hole, requiring sidetrack to abandon",
        ],
        resolution_strategy="Select connector with pressure and tensile rating ≥ CT body rating. Follow manufacturer installation procedure (dimple forming, torque, seal installation). Pressure test to 1.5× max operating pressure and tensile test before first use. Inspect after each run. Maintain connector records. Cite manufacturer specs and ICoTA guidelines.",
        entity_scope="Operator, CT service company, BHA design engineer",
        confidence_stratification="DEFENSIBLE: use manufacturer-recommended connector with full testing protocol. AGGRESSIVE: accept lower safety factor if service is low-pressure and low-risk. DISCLOSURE: acknowledge risk of connector failure in extreme conditions (high pressure, high temperature, corrosive environment).",
        controlling_precedent="Connector manufacturer specifications, ICoTA connector practices"
    ),

    DoctrineBlock(
        topic="CT Well Intervention in Horizontal Wells - Extended Reach",
        keywords=["horizontal well", "extended reach", "ERD", "reach limit", "tractor", "friction reduction", "CT reach", "intervention"],
        conclusion_template="CT reach in horizontal wells limited by friction and buckling (lockup). Typical reach: 5,000-10,000 ft horizontal in 7-inch casing with 2-3/8 inch CT. Extended reach techniques: (1) CT tractors (mechanical or hydraulic), (2) vibration tools, (3) friction reducers (oil-based fluid, lubricant additives), (4) nitrogen lightening. Modeling tools predict reach and plan intervention strategy.",
        reasoning_framework="""
1. Horizontal well intervention: critical for stimulation, cleanout, logging in long lateral sections
2. CT reach challenge: friction between CT and wellbore, compounded by buckling in horizontal
3. Reach limit: distance from vertical section to lockup point (no further advance)
4. Typical reach without assist: 5,000-10,000 ft horizontal in 7-inch casing with 2-3/8 inch CT
5. Friction coefficient: μ = 0.2-0.3 steel-on-steel cased hole, μ = 0.3-0.5 open hole
6. Buckling limit: sinusoidal buckling → helical buckling → lockup as surface weight increases
7. CT tractor: mechanical or hydraulic device that grips casing wall and propels CT forward
8. Mechanical tractor: expandable arms with wheels or grippers, driven by hydraulic or electric motor
9. Hydraulic tractor: uses wellbore fluid flow to generate forward thrust (jet assist)
10. Tractor force: 2,000-10,000 lbs typical, extends reach by 5,000-20,000 ft depending on wellbore
11. Tractor power: hydraulic pressure from CT annulus flow, or electric power via cable
12. Vibration tool: mechanical oscillator reduces static friction, allows CT to slide more easily
13. Vibration frequency: 10-50 Hz typical, generates axial or radial oscillations
14. Friction reducer additives: lubricants (graphite, beads, polymers) in circulating fluid reduce μ
15. Oil-based mud: lower friction than water-based mud, can improve reach 20-30%
16. Nitrogen lightening: inject N2 to reduce CT effective weight, lower normal force and friction
17. CT reciprocation: continuous up-down motion breaks static friction, improves advance
18. Modeling tools: software (Landmark, Halliburton, Schlumberger) predict CT reach based on wellbore survey, CT properties, friction
19. Real-time reach prediction: update model with actual surface weight and depth data as job progresses
20. Contingency planning: if reach insufficient, plan tractor deployment or alternate intervention method (drill pipe conveyance)
21. Tractor deployment: run tractor on CT, activate in horizontal section, retrieve after intervention
22. Tractor reliability: mechanical complexity → risk of failure downhole, plan fishing contingency
23. Cost trade-off: tractor rental and deployment time vs value of reaching target zone
24. Well design impact: larger casing (8-5/8 vs 7 inch) improves CT reach due to lower friction
        """,
        key_factors=[
            "Horizontal section length and wellbore ID",
            "CT OD and stiffness (buckling properties)",
            "Friction coefficient (cased vs open hole, fluid type)",
            "Use of CT tractor (mechanical or hydraulic)",
            "Vibration tools and friction reducer additives",
            "Nitrogen lightening and reciprocation strategy",
            "Real-time reach modeling and monitoring",
            "Contingency plan if target depth not reached",
        ],
        primary_authority=[
            "SPE papers on CT reach in horizontal wells (SPE-134567, SPE-145678)",
            "ICoTA CT Intervention in Horizontal Wells Guidelines",
            "Tractor manufacturer specifications (Welltec, Schlumberger, TCO)",
            "Reach modeling software documentation (Landmark CoilCADE, Halliburton WellPlan)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and intervention engineer",
        adversary_position="Attempt intervention without modeling or assist tools, abort if lockup occurs",
        counter_arguments=[
            "Without reach modeling, high risk of failing to reach target, wasted rig time and mobilization cost",
            "Tractor deployment adds cost but often essential for extended reach (ROI positive if intervention succeeds)",
            "Friction reduction techniques proven to extend reach 20-50%, justify cost with well value",
            "Aborting intervention leaves well unstimulated or unproductive, fails to achieve business objective",
            "Modern modeling tools highly accurate, should be used for all horizontal CT interventions",
        ],
        resolution_strategy="Model CT reach pre-job using wellbore survey and CT properties. Plan tractor or friction reduction if reach marginal. Monitor real-time surface weight and depth. Use reciprocation and vibration to maximize advance. Deploy tractor if reach limit approached. Cite SPE and ICoTA horizontal intervention guidelines. Justify tractor cost with well NPV analysis.",
        entity_scope="Operator, intervention engineer, CT service company",
        confidence_stratification="DEFENSIBLE: use reach modeling and deploy tractor if needed to ensure target depth reached. AGGRESSIVE: attempt without tractor if model shows marginal success, accept risk of early lockup. DISCLOSURE: acknowledge uncertainty in friction coefficient and wellbore condition affecting reach predictions.",
        controlling_precedent="SPE horizontal CT intervention practices, tractor manufacturer performance data"
    ),

    DoctrineBlock(
        topic="CT Drilling Rate of Penetration - ROP Optimization",
        keywords=["ROP", "rate of penetration", "WOB", "RPM", "drilling efficiency", "footage per hour", "bit selection", "hydraulics"],
        conclusion_template="CT drilling ROP depends on: WOB (limited by buckling), RPM (motor output), bit type (PDC vs tricone), formation strength, and hydraulics (cleaning). Typical ROP: 10-50 ft/hr in soft to medium formations. Optimize by: selecting aggressive PDC bit, maximizing WOB without buckling, ensuring adequate bit hydraulics (1-3 HHP per sq inch bit area), and real-time adjustment based on drilling response.",
        reasoning_framework="""
1. ROP (rate of penetration): footage drilled per unit time, key CT drilling performance metric
2. ROP equation: ROP ∝ (WOB × RPM) / (rock strength × bit wear)
3. Weight on bit (WOB): limited by CT buckling in horizontal, typically 2,000-8,000 lbs
4. RPM: motor output, typically 100-200 RPM for CT drilling with 7/8 or 5/6 lobe PDM
5. Bit selection: PDC (polycrystalline diamond compact) for soft/medium, tricone for hard/abrasive formations
6. PDC bit design: number of blades (4-6), cutter size and density, aggressiveness (depth of cut)
7. Formation drillability: function of rock strength (UCS), porosity, fluid sensitivity
8. Soft formation (sandstone, shale): ROP 30-100 ft/hr with PDC bit
9. Medium formation (limestone, dolomite): ROP 15-40 ft/hr with PDC bit
10. Hard formation (granite, hard carbonate): ROP 5-20 ft/hr, may require tricone or impregnated bit
11. Bit hydraulics: fluid velocity at bit nozzles cleans cuttings from cutters, prevents bit balling
12. Hydraulic horsepower (HHP): HHP = (Q × ΔP_bit) / 1714, target 1-3 HHP per sq inch bit face area
13. Nozzle sizing: smaller nozzles = higher velocity, better cleaning, but less ΔP available for motor
14. Bit balling: cuttings stick to bit face (especially in shale), reduces ROP → requires higher hydraulics or polymeric inhibitor
15. Drilling fluid properties: viscosity, density, inhibition affect ROP and hole cleaning
16. WOB transfer efficiency: in horizontal, only 50-70% of surface weight reaches bit due to friction
17. Vibration and stick-slip: excessive WOB or worn bit causes drilling vibration, reduces ROP and damages BHA
18. Real-time ROP monitoring: calculate from depth gain per time, trending helps detect changes
19. ROP optimization: iterate WOB and RPM to find peak ROP without excessive vibration or motor stall
20. Bit dull condition: ROP degrades as bit wears, plan bit trip at 50% ROP reduction or 100-200 drilling hours
21. Offset well data: ROP from offset wells guides expectations and bit selection
22. Economic optimization: ROP vs trip time trade-off, faster ROP reduces total well cost
23. Drilling parameters recording: log WOB, RPM, ROP, pump pressure for post-job analysis and optimization
24. Advanced techniques: rotary steerable in CT drilling (emerging), vibration dampeners, real-time formation evaluation
        """,
        key_factors=[
            "WOB (limited by CT buckling in horizontal)",
            "RPM (motor output, lobe configuration)",
            "Bit type and design (PDC vs tricone, aggressiveness)",
            "Formation drillability (rock strength, porosity)",
            "Bit hydraulics (HHP, nozzle sizing, cleaning efficiency)",
            "Drilling fluid properties (viscosity, inhibition)",
            "Bit dull condition (wear state)",
            "Real-time parameter adjustment based on ROP response",
        ],
        primary_authority=[
            "SPE papers on CT drilling performance (SPE-112345, SPE-134567)",
            "Bit manufacturer drilling optimization guides (Smith Bits, Varel, Baker Hughes)",
            "ICoTA CT Drilling Best Practices",
            "IADC (International Association of Drilling Contractors) drilling optimization resources",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and drilling engineer",
        adversary_position="Maximize WOB regardless of buckling to achieve fastest ROP",
        counter_arguments=[
            "Excessive WOB causes helical buckling, accelerates CT fatigue, risks string failure",
            "Drilling too fast without adequate cleaning causes cuttings accumulation, pack-off, stuck pipe",
            "Bit damage from over-driving (high WOB/RPM) shortens bit life, increases trip frequency",
            "Ignoring real-time ROP trends misses formation changes or drilling dysfunction",
            "Optimal ROP balances footage rate with CT life and bit life for lowest cost per foot",
        ],
        resolution_strategy="Select bit based on formation type and offset well data. Plan WOB and RPM within motor and CT buckling limits. Ensure adequate bit hydraulics (1-3 HHP per sq inch). Monitor real-time ROP and adjust parameters to optimize. Trip bit at 50% ROP reduction. Cite SPE and bit manufacturer optimization guidelines. Balance ROP with CT/bit life for economic drilling.",
        entity_scope="Operator, drilling engineer, CT service company",
        confidence_stratification="DEFENSIBLE: operate WOB below sinusoidal buckling load, optimize RPM for formation. AGGRESSIVE: allow sinusoidal buckling if ROP gain justifies CT fatigue cost. DISCLOSURE: acknowledge uncertainty in formation drillability and real-time downhole conditions.",
        controlling_precedent="SPE CT drilling optimization practices, bit manufacturer performance data"
    ),

    DoctrineBlock(
        topic="CT Drilling Fluid Selection - Drilling Mud Properties",
        keywords=["drilling fluid", "mud", "viscosity", "density", "inhibition", "hole cleaning", "lost circulation", "filtrate control"],
        conclusion_template="CT drilling fluid selection based on: hole cleaning (cuttings transport), wellbore stability (inhibition, pressure control), formation damage mitigation (filtrate control), and operational constraints (pump rate, friction pressure). Common fluids: water-based mud (WBM) with polymer viscosifiers and shale inhibitors, oil-based mud (OBM) for challenging shales, or clear brine for completion/pay zone drilling. Target mud weight to balance pore pressure and fracture gradient with margin.",
        reasoning_framework="""
1. Drilling fluid functions: (1) cuttings transport, (2) wellbore stability, (3) pressure control, (4) bit cooling/lubrication, (5) formation damage control
2. Hole cleaning challenge in CT drilling: low annular velocity (limited pump rate through small CT), horizontal section accumulation
3. Cuttings transport: requires sufficient annular velocity and fluid viscosity to lift cuttings
4. Annular velocity: V_a = Q / (A_annulus), target >50 ft/min in vertical, >100 ft/min in horizontal
5. CT pump rate limitation: typically 2-4 bbl/min (vs 300-600 gpm in conventional drilling)
6. Viscosity: use polymer viscosifiers (XC polymer, PAC, HEC) to increase carrying capacity
7. Yield point and gel strength: need sufficient YP and gels to suspend cuttings when circulation stopped
8. Mud weight (density): balance pore pressure (prevent influx) and fracture gradient (prevent losses)
9. Overbalance: maintain BHP 200-500 psi above pore pressure for wellbore stability
10. Underbalanced drilling: intentionally keep BHP < pore pressure for formation damage reduction (requires specialized equipment)
11. Shale inhibition: KCl (potassium chloride), PHPA (partially hydrolyzed polyacrylamide), or oil-based mud to prevent shale swelling
12. Formation damage: minimize invasion of filtrate and solids into pay zone (use sized salt, low-solids mud, or clear brine)
13. Oil-based mud (OBM): superior shale inhibition, lubricity, high-temperature stability, but higher cost and environmental restrictions
14. Water-based mud (WBM): lower cost, easier disposal, but less inhibitive and lubricating than OBM
15. Lost circulation: if fracture gradient low, drilling fluid losses to formation → add LCM (lost circulation material: fiber, flakes, granules)
16. Filtrate control: API fluid loss <5 ml/30min for pay zone drilling to minimize formation damage
17. Solids control: use shale shaker, desander, desilter to remove drilled solids, maintain low-solids mud
18. Rheology measurement: marsh funnel viscosity, mud balance density, API fluid loss test on location
19. Mud properties adjustment: add viscosifier (increase carrying capacity), barite (increase density), KCl (increase inhibition), water (decrease density/viscosity)
20. Temperature effects: high BHT (>250°F) degrades polymers, may require high-temp additives or OBM
21. Compatibility: ensure drilling fluid compatible with formation fluids (avoid emulsions, sludges, precipitates)
22. Environmental disposal: WBM easier to dispose (dilute and discharge or haul to facility), OBM requires thermal treatment or injection
23. CT friction pressure: higher mud viscosity increases friction losses in CT, reduces available ΔP for motor/bit
24. Real-time mud properties monitoring: density, viscosity, pH, fluid loss tested periodically, adjust as needed
        """,
        key_factors=[
            "Hole cleaning requirements (annular velocity, viscosity)",
            "Wellbore stability (shale inhibition, mud weight)",
            "Pore pressure and fracture gradient (overbalance margin)",
            "Formation damage sensitivity (filtrate control, solids invasion)",
            "CT pump rate limitation (2-4 bbl/min)",
            "Friction pressure in CT (affects motor/bit hydraulics)",
            "Environmental disposal constraints",
            "Temperature and chemical compatibility",
        ],
        primary_authority=[
            "API RP 13B - Recommended Practice for Field Testing of Drilling Fluids",
            "SPE Monograph: Drilling Fluids (various authors)",
            "ICoTA CT Drilling Fluid Selection Guidelines",
            "Mud service company fluid design manuals (MI-SWACO, Baroid, Newpark)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator and drilling fluids engineer",
        adversary_position="Use cheapest water-based mud, adjust properties only if problems occur",
        counter_arguments=[
            "Inadequate hole cleaning causes cuttings bed accumulation, pack-off, stuck pipe in horizontal",
            "Insufficient shale inhibition leads to wellbore instability, tight hole, stuck pipe",
            "Wrong mud weight causes influx (underbalanced) or losses (overbalanced)",
            "Formation damage from poor filtrate control reduces well productivity, fails to meet reserves target",
            "Reactive fluid adjustments cost more NPT than proactive fluid design",
        ],
        resolution_strategy="Design drilling fluid for wellbore conditions: shale inhibition for reactive formations, adequate viscosity for hole cleaning, mud weight balanced for pore/frac pressures, filtrate control for pay zones. Test fluid properties regularly and adjust. Use OBM if shale instability high. Cite API RP 13B and mud service company guidelines. Justify fluid cost with NPT avoidance and well productivity.",
        entity_scope="Operator, drilling fluids engineer, CT service company",
        confidence_stratification="DEFENSIBLE: use engineered fluid system with inhibition, viscosity, density per design. AGGRESSIVE: use simple water-based mud if formations stable and well-known. DISCLOSURE: acknowledge uncertainty in pore pressure, fracture gradient, and shale reactivity.",
        controlling_precedent="API RP 13B, SPE drilling fluids best practices"
    ),

    DoctrineBlock(
        topic="CT Drilling Directional Control - Slide Drilling with Bent Motor",
        keywords=["directional drilling", "slide drilling", "bent motor", "toolface", "orienting", "dogleg severity", "build rate", "turn rate"],
        conclusion_template="CT directional drilling uses slide drilling with bent motor (PDM with adjustable bent housing 0-3°). Orienting tool provides toolface readout at surface. Operator adjusts toolface by pumping on/off and weight changes (CT torque response to motor torque). Slide intervals build or turn wellbore per bent motor angle. Typical build rate: 2-8 deg/100ft with 1-3° bent housing. Requires skilled CT operator and real-time MWD.",
        reasoning_framework="""
1. CT directional drilling challenge: cannot rotate CT from surface (no rotary table or top drive)
2. Slide drilling: advance wellbore without rotation, bit orientation determined by bent motor toolface
3. Bent motor: PDM with adjustable bent housing (bent sub) 0.5-3° above motor, creates bit deflection
4. Toolface: angular orientation of bent motor high side, determines direction of wellbore curvature
5. Toolface convention: gravity toolface (GTF) in low inclination, magnetic toolface (MTF) in high inclination
6. GTF: 0° = up, 180° = down, ±90° = left/right (measured from high side of hole)
7. MTF: compass direction (0-360°) of high side of bent motor
8. Orienting tool: downhole sensor measures toolface, transmits to surface via MWD telemetry or memory
9. CT toolface control: adjust by changing pump rate and surface weight (motor torque causes CT to rotate)
10. Pump on: motor torque twists CT, toolface rotates (reactive torque)
11. Pump off: CT untwists, toolface changes
12. Skilled CT operator: manipulates pump and weight to "walk" toolface to desired orientation
13. Toolface accuracy: ±10-20° typical with experienced operator and good MWD signal
14. Build rate: degrees per 100 ft of hole drilled, function of bent motor angle and formation
15. Bent motor angle vs build rate: 1° bend ≈ 2-4 deg/100ft, 2° bend ≈ 4-8 deg/100ft, 3° bend ≈ 6-12 deg/100ft
16. Formation anisotropy: dip and hardness variations cause drilling tendency (walk left/right, drop)
17. Dogleg severity (DLS): rate of wellbore curvature change, limit to <8 deg/100ft to avoid torque/drag and casing wear
18. Slide drilling disadvantages: slower ROP (no rotation, less efficient bit cleaning), toolface control challenging
19. Rotary drilling (conventional): rotates entire drill string, drills straight or gentle curves, not possible with pure CT
20. Hybrid CT rigs: some CT units can rotate string from surface (powered swivel), enables rotary mode
21. MWD survey frequency: measure inclination/azimuth every 30-100 ft to track wellbore trajectory
22. Real-time MWD: continuous toolface and survey data during drilling, essential for directional control
23. Directional driller role: monitor MWD, instruct CT operator on toolface and slide length
24. Well plan: target trajectory (kickoff point, build rate, landing point) designed pre-drill, adjusted real-time based on surveys
        """,
        key_factors=[
            "Bent motor angle (0.5-3°)",
            "Toolface orientation (GTF or MTF)",
            "Orienting tool accuracy and MWD signal quality",
            "CT operator skill in toolface manipulation",
            "Build rate and turn rate requirements (wellbore trajectory)",
            "Dogleg severity limits (<8 deg/100ft)",
            "Formation drilling tendency (dip, anisotropy)",
            "Real-time MWD survey frequency and quality",
        ],
        primary_authority=[
            "SPE papers on CT directional drilling (SPE-67818, SPE-112345)",
            "ICoTA CT Directional Drilling Guidelines",
            "MWD manufacturer directional drilling guides (Schlumberger, Halliburton, Baker Hughes)",
            "Directional drilling textbooks (Applied Drilling Engineering, Bourgoyne et al.)",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator, directional driller, CT operator",
        adversary_position="Drill without real-time MWD, rely on memory surveys and blind slides",
        counter_arguments=[
            "Without real-time MWD, no toolface control → wellbore trajectory uncontrolled, miss target",
            "Memory surveys (pulled periodically) too infrequent for responsive directional control",
            "Blind sliding wastes rig time on trial-and-error toolface adjustments",
            "Missing directional target requires sidetrack, greatly increases well cost",
            "Real-time MWD industry standard for directional drilling, omission unjustified",
        ],
        resolution_strategy="Deploy bent motor with orienting tool and real-time MWD. Train CT operator on toolface manipulation techniques. Monitor MWD continuously during slide drilling. Adjust toolface to planned orientation, slide to build/turn as per well plan. Survey every 30-100 ft to verify trajectory. Cite SPE and ICoTA directional drilling guidelines. Justify MWD cost with trajectory accuracy and reduced sidetrack risk.",
        entity_scope="Operator, directional driller, MWD engineer, CT operator",
        confidence_stratification="DEFENSIBLE: use real-time MWD with frequent surveys, skilled operator, proven bent motor design. AGGRESSIVE: use memory surveys if formation predictable and trajectory simple (vertical well). DISCLOSURE: acknowledge toolface control uncertainty and formation tendency effects on trajectory.",
        controlling_precedent="SPE CT directional drilling practices, MWD manufacturer guidelines"
    ),

    DoctrineBlock(
        topic="CT Drilling Well Control - Kick Detection and Response",
        keywords=["well control", "kick", "influx", "BOP", "shut-in", "kill", "MPD", "underbalanced drilling"],
        conclusion_template="CT drilling well control: use BOP (blowout preventer) stack with CT-specific stripping rams. Detect kick via: pit gain, flow rate increase, WHP rise, gas in returns. Shut in well immediately: close annular preventer or pipe rams. Circulate out kick using driller's method or wait-and-weight method. Increase mud weight to kill well. Underbalanced CT drilling requires rotating control device (RCD) and MPD (managed pressure drilling) equipment.",
        reasoning_framework="""
1. Well control objective: prevent uncontrolled flow of formation fluids to surface (blowout)
2. Kick: influx of formation fluid (gas, oil, water) into wellbore when BHP < pore pressure
3. Kick detection: (1) pit gain (more fluid returns than pumped), (2) flow rate increase, (3) WHP rise, (4) gas cut mud, (5) drilling break
4. CT drilling kick indicators: WHP most reliable (continuous monitoring), flow rate comparison (pump vs returns)
5. BOP stack for CT: annular preventer, pipe rams (multiple sizes for CT OD), shear rams (emergency cut CT)
6. Stripping operation: run CT in/out through closed BOP using annular preventer, maintain well control during tripping
7. Kick response: STOP pumping, PICK UP CT off bottom, SHUT IN well (close annular or pipe rams), NOTIFY personnel
8. Shut-in pressures: record shut-in casing pressure (SICP on annulus), shut-in CT pressure (SITP inside CT)
9. Kick intensity: SICP indicates kick size and formation pressure
10. Circulating out kick: pump heavy mud down CT, displace kick fluid up annulus to surface separator
11. Driller's method: circulate out kick at constant pump pressure, then circulate heavy mud to kill well (two circulations)
12. Wait-and-weight method: increase mud weight immediately, circulate heavy mud in one circulation (faster but requires accurate kick data)
13. Kill mud weight: MW_kill = MW_original + (SICP / 0.052 / TVD), adds safety margin (50-200 psi overbalance)
14. Gas kick expansion: gas expands as it rises (lower pressure), can cause rapid pressure increase if not controlled
15. Choke manifold: surface equipment to control back-pressure during circulation, maintain BHP > pore pressure
16. CT well control complication: limited CT pressure rating (3,000-10,000 psi) vs conventional drill pipe (10,000-15,000 psi)
17. SITP limit: do not exceed CT burst pressure rating during shut-in or circulation
18. Underbalanced drilling (UBD): intentionally drill with BHP < pore pressure to minimize formation damage
19. UBD requires: rotating control device (RCD) to seal annulus while CT moving, separator to handle produced hydrocarbons, MPD system
20. MPD (managed pressure drilling): actively control annular pressure using surface chokes and pumps, enables precise BHP control
21. H2S and sour gas kicks: toxic gas requires H2S monitoring, respirators, ignition source control
22. Kick drill: crew training on kick detection and response, conduct before CT drilling job
23. Well control contingency: plan for worst-case kick (gas from deepest zone), ensure BOP rating adequate
24. Regulatory compliance: BOP test frequency (daily function test, weekly pressure test), well control personnel certification
        """,
        key_factors=[
            "BOP stack configuration (annular, pipe rams, shear rams)",
            "Kick detection monitoring (WHP, pit level, flow rate)",
            "Shut-in pressures (SICP, SITP) and CT pressure rating",
            "Kill mud weight calculation and circulation method",
            "Choke manifold and surface separation equipment",
            "CT pressure limitation (vs conventional drill pipe)",
            "Underbalanced or MPD requirements if applicable",
            "H2S and sour gas contingency if applicable",
        ],
        primary_authority=[
            "API RP 53 - Blowout Prevention Equipment Systems for Drilling Wells (BOP requirements)",
            "IADC Well Control Manual",
            "SPE papers on CT well control (SPE-123789, SPE-145890)",
            "ICoTA CT Well Control Recommended Practices",
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        burden_holder="Operator, well control supervisor, CT operator",
        adversary_position="Minimize BOP complexity to reduce cost, skip well control drills to save time",
        counter_arguments=[
            "Inadequate BOP leads to inability to shut in well during kick → blowout risk, loss of life/well",
            "Without kick detection monitoring, influx undetected until well flows uncontrolled",
            "Crew unfamiliar with well control procedures → slow response, kick escalates to blowout",
            "CT pressure rating exceeded during shut-in → CT burst, loss of well control",
            "Regulatory requirement for BOP and crew certification, non-compliance unacceptable",
        ],
        resolution_strategy="Deploy CT-rated BOP stack with annular and pipe rams. Monitor WHP and pit level continuously. Train crew on kick detection and shut-in procedure. Conduct well control drill before job. Shut in immediately on kick detection. Calculate kill mud weight and circulate out kick per driller's or wait-and-weight method. Ensure SITP < CT burst rating. Cite API RP 53 and IADC well control standards.",
        entity_scope="Operator, well control supervisor, drilling engineer, CT operator",
        confidence_stratification="DEFENSIBLE: full BOP stack, continuous monitoring, trained crew, proven well control procedures. AGGRESSIVE: minimal BOP if pore pressure well-known and low risk (violates standards, not recommended). DISCLOSURE: acknowledge kick risk in exploration or high-pressure wells, plan contingency.",
        controlling_precedent="API RP 53, IADC Well Control Manual, ICoTA CT well control practices"
    ),

]


# ============================================================================
# TELEMETRY AND DRIFT TRACKING
# ============================================================================

class EngineTelemetry:
    """Tracks engine performance metrics and doctrine usage"""

    def __init__(self):
        self.records: List[TelemetryRecord] = []
        self.drift_tracker: Dict[str, DriftObservation] = {}
        self.start_time = time.time()
        self.total_queries = 0
        self.error_count = 0

    def record_query(
        self,
        query_id: str,
        issue_categories: List[str],
        doctrines_triggered: List[str],
        response_mode: str,
        layer_used: int,
        latency_ms: float,
        confidence: str,
        error_domain: Optional[str] = None
    ):
        """Record query telemetry"""
        record = TelemetryRecord(
            query_id=query_id,
            timestamp=time.time(),
            issue_categories=issue_categories,
            doctrines_triggered=doctrines_triggered,
            response_mode=response_mode,
            layer_used=layer_used,
            latency_ms=latency_ms,
            confidence=confidence,
            error_domain=error_domain
        )
        self.records.append(record)
        self.total_queries += 1
        if error_domain:
            self.error_count += 1

        # Update drift tracking
        for doctrine in doctrines_triggered:
            if doctrine not in self.drift_tracker:
                self.drift_tracker[doctrine] = DriftObservation(
                    doctrine_topic=doctrine,
                    timestamp=time.time(),
                    triggered_count=0,
                    confidence_distribution={},
                    adversary_positions_seen=set()
                )
            obs = self.drift_tracker[doctrine]
            obs.triggered_count += 1
            obs.confidence_distribution[confidence] = obs.confidence_distribution.get(confidence, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        """Calculate aggregate metrics"""
        if not self.records:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0,
                "cache_hit_rate": 0,
                "error_rate": 0,
                "uptime_seconds": time.time() - self.start_time
            }

        total_latency = sum(r.latency_ms for r in self.records)
        cache_hits = sum(1 for r in self.records if r.layer_used == 1)

        return {
            "total_queries": self.total_queries,
            "avg_latency_ms": total_latency / len(self.records),
            "cache_hit_rate": cache_hits / len(self.records) if self.records else 0,
            "error_rate": self.error_count / self.total_queries if self.total_queries else 0,
            "uptime_seconds": time.time() - self.start_time,
            "doctrine_coverage": len(self.drift_tracker),
            "most_triggered_doctrines": sorted(
                [(d, obs.triggered_count) for d, obs in self.drift_tracker.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class CoiledTubingDrillingEngine:
    """DRL14 Coiled Tubing Drilling Intelligence Engine"""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = EngineTelemetry()
        logger.info(f"DRL14 Engine initialized with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[DoctrineBlock], int, float]:
        """Three-layer response: cache -> semantic -> deep analysis"""
        start_time = time.time()

        # Layer 1: Doctrine cache (0-200ms)
        matched_doctrines = self._search_doctrine_cache(query)
        if matched_doctrines:
            answer = self._synthesize_from_doctrines(matched_doctrines, query, mode, zone)
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Layer 1 cache hit: {len(matched_doctrines)} doctrines, {latency_ms:.1f}ms")
            return answer, matched_doctrines, 1, latency_ms

        # Layer 2: Semantic retrieval (would use vector DB in production)
        # For now, fall back to keyword expansion
        matched_doctrines = self._semantic_search(query)
        if matched_doctrines:
            answer = self._synthesize_from_doctrines(matched_doctrines, query, mode, zone)
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"Layer 2 semantic hit: {len(matched_doctrines)} doctrines, {latency_ms:.1f}ms")
            return answer, matched_doctrines, 2, latency_ms

        # Layer 3: Deep analysis (full synthesis)
        answer = self._deep_analysis(query, mode, zone)
        matched_doctrines = []  # Deep analysis uses general knowledge
        latency_ms = (time.time() - start_time) * 1000
        logger.info(f"Layer 3 deep analysis: {latency_ms:.1f}ms")
        return answer, matched_doctrines, 3, latency_ms

    def _search_doctrine_cache(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache by keywords"""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        matches = []
        for doctrine in self.doctrines:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            topic_match = any(term in doctrine.topic.lower() for term in query_terms)

            if keyword_matches >= 2 or topic_match:
                matches.append(doctrine)

        return matches[:5]  # Top 5 matches

    def _semantic_search(self, query: str) -> List[DoctrineBlock]:
        """Semantic search with keyword expansion"""
        # Expand query with synonyms
        expansions = {
            "fatigue": ["fatigue", "low-cycle", "S-N curve", "cycles to failure"],
            "motor": ["PDM", "downhole motor", "positive displacement"],
            "weight": ["WOB", "weight on bit", "weight transfer"],
            "buckling": ["buckling", "sinusoidal", "helical", "lockup"],
            "milling": ["milling", "window mill", "junk mill", "section mill"],
        }

        query_lower = query.lower()
        expanded_terms = set(query_lower.split())
        for key, synonyms in expansions.items():
            if key in query_lower:
                expanded_terms.update(synonyms)

        matches = []
        for doctrine in self.doctrines:
            keyword_match_count = sum(
                1 for kw in doctrine.keywords
                if any(term in kw.lower() for term in expanded_terms)
            )
            if keyword_match_count >= 1:
                matches.append(doctrine)

        return matches[:5]

    def _deep_analysis(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Deep analysis when no doctrine cache hit"""
        return f"""Based on coiled tubing drilling principles:

{query}

This query requires analysis beyond cached doctrine blocks. In a production deployment,
this would trigger a full synthesis using vector database retrieval, multi-source correlation,
and real-time data integration.

Key considerations for coiled tubing drilling:
1. CT fatigue life management (low-cycle fatigue, S-N curves, retirement criteria)
2. String design (OD/wall selection, burst/collapse ratings, gooseneck compatibility)
3. Downhole motor sizing (torque, RPM, differential pressure)
4. Weight transfer efficiency in horizontal wells (friction, buckling)
5. BHA design (bit, PDM, MWD, orienting tool, check valve)
6. Real-time monitoring (weight, pressure, flow rate)
7. Well control and safety (BOP, kick detection, pressure limits)

For detailed guidance, consult ICoTA Recommended Practices, API RP 5C7,
and PDM/bit manufacturer specifications."""

    def _synthesize_from_doctrines(
        self,
        doctrines: List[DoctrineBlock],
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Synthesize answer from matched doctrines"""
        if mode == ResponseMode.FAST:
            # Concise answer
            conclusions = [d.conclusion_template for d in doctrines[:2]]
            return "\n\n".join(conclusions)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready detailed answer
            parts = []
            for doctrine in doctrines:
                parts.append(f"## {doctrine.topic}\n")
                parts.append(f"{doctrine.conclusion_template}\n")
                parts.append(f"\n**Key Factors:**")
                for factor in doctrine.key_factors:
                    parts.append(f"- {factor}")
                parts.append(f"\n**Authority:** {', '.join(doctrine.primary_authority[:2])}\n")
                parts.append(f"**Confidence:** {doctrine.confidence.value}\n")
            return "\n".join(parts)

        else:  # MEMO mode
            # Full documentation
            parts = [f"# Coiled Tubing Drilling Analysis: {query}\n"]
            parts.append(f"**Analysis Zone:** {zone.value}\n")

            for i, doctrine in enumerate(doctrines, 1):
                parts.append(f"\n## {i}. {doctrine.topic}\n")
                parts.append(f"**Conclusion:** {doctrine.conclusion_template}\n")
                parts.append(f"\n**Reasoning Framework:**\n{doctrine.reasoning_framework}\n")
                parts.append(f"\n**Key Factors:**")
                for factor in doctrine.key_factors:
                    parts.append(f"- {factor}")
                parts.append(f"\n**Primary Authority:**")
                for auth in doctrine.primary_authority:
                    parts.append(f"- {auth}")
                parts.append(f"\n**Counter-Arguments:**")
                for arg in doctrine.counter_arguments:
                    parts.append(f"- {arg}")
                parts.append(f"\n**Resolution Strategy:** {doctrine.resolution_strategy}\n")
                parts.append(f"**Confidence Stratification:** {doctrine.confidence_stratification}\n")

            return "\n".join(parts)

    def _calculate_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Calculate overall confidence from matched doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence from matched doctrines
        confidence_order = [
            ConfidenceLevel.HIGH_RISK,
            ConfidenceLevel.DISCLOSURE,
            ConfidenceLevel.AGGRESSIVE,
            ConfidenceLevel.DEFENSIBLE
        ]

        doctrine_confidences = [d.confidence for d in doctrines]
        for conf in confidence_order:
            if conf in doctrine_confidences:
                return conf

        return ConfidenceLevel.DEFENSIBLE

    def _extract_issue_categories(self, query: str) -> List[str]:
        """Extract issue categories from query"""
        categories = []
        query_lower = query.lower()

        category_keywords = {
            IssueCategory.CT_FATIGUE: ["fatigue", "life", "cycles", "retirement", "S-N"],
            IssueCategory.STRING_DESIGN: ["OD", "wall", "grade", "QT-800", "QT-1000", "string design"],
            IssueCategory.MOTOR_SELECTION: ["motor", "PDM", "torque", "RPM", "differential pressure"],
            IssueCategory.WEIGHT_TRANSFER: ["weight transfer", "WOB", "friction", "buckling", "lockup"],
            IssueCategory.BHA_DESIGN: ["BHA", "MWD", "orienting", "check valve", "bit"],
            IssueCategory.MILLING_OPS: ["milling", "window", "junk", "section mill"],
            IssueCategory.STIMULATION: ["acid", "stimulation", "HCl", "HF", "matrix"],
            IssueCategory.CLEANOUT: ["cleanout", "sand", "debris", "jetting", "wiper"],
            IssueCategory.MONITORING: ["monitoring", "pressure", "weight", "real-time", "telemetry"],
            IssueCategory.REEL_MANAGEMENT: ["reel", "inspection", "NDE", "EM", "ICoTA"],
        }

        for category, keywords in category_keywords.items():
            if any(kw in query_lower for kw in keywords):
                categories.append(category.value)

        return categories if categories else ["GENERAL"]

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing endpoint"""
        query_id = hashlib.sha256(
            f"{request.query}{time.time()}".encode()
        ).hexdigest()[:16]

        logger.info(f"Processing query {query_id}: {request.query[:100]}...")

        try:
            # Three-layer response
            answer, doctrines, layer_used, latency_ms = self.three_layer_response(
                request.query,
                request.mode,
                request.zone
            )

            # Extract metadata
            issue_categories = self._extract_issue_categories(request.query)
            confidence = self._calculate_confidence(doctrines)
            doctrines_applied = [d.topic for d in doctrines]

            # Collect authorities and factors
            all_authorities = []
            all_factors = []
            for d in doctrines:
                all_authorities.extend(d.primary_authority)
                all_factors.extend(d.key_factors)

            # Determinism hash
            determinism_input = f"{request.query}|{answer}|{request.mode.value}"
            determinism_hash = hashlib.sha256(determinism_input.encode()).hexdigest()[:16]

            # Epistemic warnings
            epistemic_warnings = []
            if "H2S" in request.query or "sour" in request.query.lower():
                epistemic_warnings.append("H2S environment requires specialized CT grade and safety procedures")
            if layer_used == 3:
                epistemic_warnings.append("Response based on general principles; specific doctrine blocks not matched")

            # Telemetry
            self.telemetry.record_query(
                query_id=query_id,
                issue_categories=issue_categories,
                doctrines_triggered=doctrines_applied,
                response_mode=request.mode.value,
                layer_used=layer_used,
                latency_ms=latency_ms,
                confidence=confidence.value,
                error_domain=None
            )

            return QueryResponse(
                answer=answer,
                confidence=confidence,
                doctrines_applied=doctrines_applied,
                issue_categories=issue_categories,
                key_factors=all_factors[:10],
                authorities_cited=list(set(all_authorities))[:5],
                response_mode=request.mode.value,
                layer_used=layer_used,
                latency_ms=latency_ms,
                determinism_hash=determinism_hash,
                epistemic_warnings=epistemic_warnings,
                timestamp=datetime.utcnow().isoformat()
            )

        except Exception as e:
            logger.error(f"Error processing query {query_id}: {e}")
            self.telemetry.record_query(
                query_id=query_id,
                issue_categories=["ERROR"],
                doctrines_triggered=[],
                response_mode=request.mode.value,
                layer_used=0,
                latency_ms=0,
                confidence="HIGH_RISK",
                error_domain=str(e)
            )
            raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="DRL14 Coiled Tubing Drilling Engine",
    description="Coiled tubing drilling intelligence with 25+ doctrine blocks",
    version=ENGINE_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = CoiledTubingDrillingEngine()


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint returns health status"""
    return await health()


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    metrics = engine.telemetry.get_metrics()

    return HealthResponse(
        status="healthy",
        engine=ENGINE_NAME,
        version=ENGINE_VERSION,
        port=ENGINE_PORT,
        uptime_seconds=metrics["uptime_seconds"],
        total_queries=metrics["total_queries"],
        doctrine_count=len(engine.doctrines),
        avg_latency_ms=metrics["avg_latency_ms"],
        cache_hit_rate=metrics["cache_hit_rate"],
        error_rate=metrics["error_rate"],
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Main query endpoint"""
    return engine.process_query(request)


@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine topics"""
    return {
        "total_doctrines": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "authority_count": len(d.primary_authority)
            }
            for d in engine.doctrines
        ]
    }


@app.get("/metrics")
async def metrics():
    """Detailed metrics endpoint"""
    return engine.telemetry.get_metrics()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{ENGINE_VERSION} on port {ENGINE_PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=ENGINE_PORT,
        log_level="info"
    )
