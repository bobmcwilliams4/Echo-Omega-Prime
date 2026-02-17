"""
RAIL06 - Rolling Stock Maintenance Intelligence Engine
TIE-Grade Railroad Maintenance Analysis System

Analyzes locomotive overhaul cycles, railcar inspection (FRA Class I-III),
wheel/axle maintenance, brake system testing, and predictive maintenance.

Port: 9212
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import re
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "RAIL06"
ENGINE_NAME = "Rolling Stock Maintenance Intelligence Engine"
VERSION = "1.0.0"
PORT = 9212

# Configure loguru
logger.add(
    f"logs/{ENGINE_ID}_{{time}}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ============================================================================
# ENUMS AND CONSTANTS
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
    LOCOMOTIVE_OVERHAUL = "LOCOMOTIVE_OVERHAUL"
    WHEEL_AXLE_MAINTENANCE = "WHEEL_AXLE_MAINTENANCE"
    BRAKE_SYSTEM = "BRAKE_SYSTEM"
    BEARING_INSPECTION = "BEARING_INSPECTION"
    COUPLER_DRAWBAR = "COUPLER_DRAWBAR"
    TANK_CAR_QUALIFICATION = "TANK_CAR_QUALIFICATION"
    PREDICTIVE_MAINTENANCE = "PREDICTIVE_MAINTENANCE"
    SUSPENSION_TRUCK = "SUSPENSION_TRUCK"
    ELECTRICAL_TRACTION = "ELECTRICAL_TRACTION"
    PRIME_MOVER = "PRIME_MOVER"
    AIR_SYSTEM = "AIR_SYSTEM"
    SAFETY_APPLIANCES = "SAFETY_APPLIANCES"

BANNED_PHRASES = [
    "I think", "probably", "maybe", "might be",
    "in my opinion", "I believe", "I feel"
]

FRA_INSPECTION_CLASSES = {
    "CLASS_I": "1,000 mile or annual inspection",
    "CLASS_IA": "1,000 mile inspection alternate",
    "CLASS_II": "Intermediate inspection",
    "CLASS_III": "5,000 mile inspection",
    "COT_1": "Clean, oil, test Class I",
    "COT_5": "Clean, oil, test Class III"
}


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Core maintenance doctrine reasoning block"""
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
    issue_category: IssueCategory

@dataclass
class AuthorityWeight:
    """Hierarchical authority system"""
    level: int
    source: str
    weight: float
    citation: str

class QueryRequest(BaseModel):
    question: str = Field(..., description="Maintenance analysis question")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.REPORTING, description="Analysis context zone")
    confidence_target: ConfidenceLevel = Field(ConfidenceLevel.DEFENSIBLE, description="Target confidence level")

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    authorities_cited: List[str]
    reasoning_chain: List[str]
    triggered_doctrines: List[str]
    epistemic_warnings: List[str]
    determinism_hash: str
    response_mode: ResponseMode
    zone: AnalysisZone
    metadata: Dict[str, Any]


# ============================================================================
# DOCTRINE CACHE - 25+ REAL ROLLING STOCK MAINTENANCE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Locomotive Prime Mover Overhaul Cycles",
        keywords=["overhaul", "prime mover", "EMD", "GE", "engine rebuild", "component life", "TBO"],
        conclusion_template="Prime mover overhaul intervals are determined by manufacturer specifications, operating conditions, and condition monitoring data. EMD 710 series typically require major overhaul at 750,000-1,000,000 miles or 8-10 years. GE Evolution series (ES44AC) target 1,000,000+ miles between overhauls with proper maintenance.",
        reasoning_framework="""
1. MANUFACTURER SPECIFICATIONS:
   - EMD 710G3C: Major overhaul 750K-1M miles, intermediate at 375K-500K miles
   - GE GEVO-12: Major overhaul target 1M+ miles, condition-based scheduling
   - Caterpillar 3512C: 24,000-36,000 hours between major overhauls
   - Cummins QSK95: 8,000-12,000 hours for genset applications

2. OVERHAUL TRIGGERS:
   - Power assembly wear (liner, piston, rings) exceeding tolerance
   - Main bearing clearances beyond service limits (0.010-0.015 inch typical max)
   - Crankshaft deflection or journal wear requiring machining
   - Cylinder head cracking or valve seat recession
   - Fuel system deterioration affecting efficiency/emissions

3. COMPONENT LIFE LIMITS:
   - Turbocharger rebuild: 200K-300K miles or 5,000-7,500 hours
   - Fuel injectors: 100K-150K miles or signs of spray pattern degradation
   - Piston crowns: Inspect at intermediate overhaul, replace if eroded
   - Cylinder liners: Re-use if within bore/taper limits, typically 0.002-0.003 inch max

4. CONDITION-BASED EXTENSION:
   - Oil analysis trending (viscosity, TBN, wear metals, soot, fuel dilution)
   - Vibration monitoring at main bearings and power assemblies
   - Thermal imaging of exhaust manifolds (hot spots indicate misfiring cylinders)
   - Compression testing (minimum 350-400 psi per cylinder at cranking)
   - Load box testing to verify full horsepower output

5. ECONOMIC FACTORS:
   - Major overhaul cost: $250K-$500K for typical road locomotive
   - Component exchange programs reduce downtime (remanufactured power assemblies)
   - Life extension vs. new unit purchase analysis (remaining frame/underframe life)
   - Fuel efficiency degradation over component life (3-8% loss triggers rebuild)

6. OPERATIONAL INTENSITY ADJUSTMENTS:
   - Heavy haul/coal service: Reduce interval 20-30% due to high loads
   - Intermodal/manifest: Standard intervals apply
   - Switching service: Hours-based scheduling more appropriate than miles
   - Genset/idle time: Adjust for actual loaded hours vs. total operating hours

7. REGULATORY COMPLIANCE:
   - FRA Part 229.23: Periodic inspection requirements (92-day, annual)
   - EPA Tier emissions compliance during rebuild (Tier 0-4 standards)
   - Noise emission limits (90 dBA at 100 feet for switchers)
   - Asbestos abatement if rebuilding pre-1980 units
        """,
        key_factors=[
            "Manufacturer TBO specifications and warranty limits",
            "Actual operating hours and load factors (ton-miles, gross trailing tons)",
            "Oil analysis trending showing wear metal increase or additive depletion",
            "Compression test results and power output degradation",
            "Component availability and remanufacturing lead times",
            "Budget cycles and capital planning constraints",
            "Fleet age and replacement strategy alignment"
        ],
        primary_authority=[
            "EMD Service Manual 710G3C Series (Major Overhaul Procedures)",
            "GE Transportation ES44AC Maintenance Manual (Component Life Limits)",
            "AAR Manual of Standards and Recommended Practices S-5507 (Locomotive Maintenance)",
            "FRA 49 CFR Part 229.23 (Periodic Inspection Requirements)",
            "ISO 13379-1:2012 (Condition Monitoring and Diagnostics of Machines)"
        ],
        burden_holder="Railroad mechanical department",
        adversary_position="Extend overhaul intervals to reduce costs and downtime",
        counter_arguments=[
            "Premature overhaul wastes remaining component life",
            "Condition-based maintenance more cost-effective than fixed intervals",
            "Modern diagnostics allow safe extension beyond OEM recommendations",
            "Overhaul cost may exceed residual locomotive value for older units",
            "Component exchange programs mitigate risk of catastrophic failures"
        ],
        resolution_strategy="Balance OEM specifications with condition monitoring data. Trend analysis of oil samples, vibration, thermal imaging, and performance testing provides objective evidence for interval adjustment. Document all extensions with engineering analysis and increased inspection frequency.",
        entity_scope="Class I railroads, shortlines, locomotive lessors, contract maintenance providers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Manufacturer specifications are authoritative baseline. Condition monitoring allows defensible extensions with proper documentation. Economic factors influence timing but cannot override safety considerations.",
        controlling_precedent="AAR S-5507 establishes industry standards. FRA Part 229 sets minimum regulatory requirements. Manufacturer manuals control warranty coverage.",
        issue_category=IssueCategory.PRIME_MOVER
    ),

    DoctrineBlock(
        topic="Wheel Impact Load Detector (WILD) Response and Wheel Condemning Limits",
        keywords=["WILD", "wheel defects", "impact load", "condemning limits", "wheel removal", "shelling"],
        conclusion_template="Wheel Impact Load Detector (WILD) systems measure dynamic wheel impacts to identify defective wheels before catastrophic failure. Impact readings above 90,000 lbs trigger immediate removal from service. Wheels are condemned when rim thickness is less than 1 inch, flange height less than 7/8 inch, or tread hollow exceeds 1/8 inch depth.",
        reasoning_framework="""
1. WILD SYSTEM OPERATION:
   - Trackside sensors measure vertical wheel impact forces
   - Baseline impact: 20K-40K lbs for good wheel on typical freight car
   - Defect indication: Impacts >60K lbs warrant inspection
   - Critical threshold: Impacts >90K lbs require immediate car setout
   - System accuracy: ±5% of measured load under normal conditions

2. CONDEMNING LIMITS (AAR FIELD MANUAL RULE 41):
   - Rim thickness: Minimum 1.0 inch (new wheel 2.0-2.5 inch)
   - Flange height: Minimum 7/8 inch, maximum 1.5 inch (new wheel 1.25 inch)
   - Flange thickness: Minimum 7/8 inch at 3/8 inch above tread
   - Tread hollow: Maximum 1/8 inch depth across tread width
   - Shelling: Any progressive shelling exceeding 1 inch length
   - Flat spots: Depth >3/32 inch or length >2.5 inch

3. DEFECT PROGRESSION MECHANISMS:
   - Thermal cracking: Repeated brake applications cause heat checking, propagates to shelling
   - Mechanical shelling: Spalling starts at subsurface defects, grows to surface
   - Out-of-round: Uneven wear or flat spots create harmonic loading
   - Tread buildup: Wheel slip deposits metal, creates high spots
   - Flange wear: Tight radius curves and poor lubrication thin flange

4. INSPECTION RESPONSE PROTOCOL:
   - >90K lbs: Immediate setout, wheel inspection, likely wheel change
   - 70K-90K lbs: Set out at next available location, inspect within 24 hours
   - 60K-70K lbs: Inspect at next terminal stop
   - Multiple cars with elevated impacts: Check track geometry for contributing conditions

5. WHEEL MAINTENANCE ACTIONS:
   - Turning/truing: Remove 1/16 to 1/8 inch material to restore profile
   - Maximum material removal per turning: 1/4 inch to avoid heat stress
   - Minimum turnings before replacement: Wheel must meet condemning limits after cut
   - Profile restoration: AAR 1:20 taper standard, match wheel diameter within 1/32 inch

6. ECONOMIC ANALYSIS:
   - New wheel cost: $400-$600 per wheel (freight car)
   - Wheel turning cost: $50-$100 per wheel
   - Average wheel life: 500K-750K miles with 2-3 turnings
   - Derailment cost of wheel failure: $500K-$5M+ (equipment damage, track, delays)

7. PREVENTIVE MEASURES:
   - Proper brake shoe material selection (composition vs. cast iron)
   - Wayside lubrication systems on tight radius curves (<12 degree)
   - Truck hunting detection and damper maintenance
   - Load distribution verification (avoid overloading one axle)
        """,
        key_factors=[
            "WILD impact force readings and trend over time",
            "Actual measured wheel dimensions vs. AAR condemning limits",
            "Presence of visible defects (shelling, cracks, flat spots)",
            "Wheel service history (miles since new, number of turnings)",
            "Car type and loading conditions (unit coal trains have higher wear)",
            "Track conditions and curvature on typical routes",
            "Brake system type and adjustment status"
        ],
        primary_authority=[
            "AAR Field Manual of the AAR Interchange Rules, Rule 41 (Wheels)",
            "AAR Manual of Standards S-660 (Wheels, Carbon Steel)",
            "AAR Circular OT-55 (Wayside Wheel Impact Load Detector Systems)",
            "FRA Track Safety Standards 49 CFR Part 213 (Track Geometry)",
            "TTCI Research Report R-986 (Wheel Defect Detection and Progression)"
        ],
        burden_holder="Car owner and operating railroad (joint responsibility under interchange rules)",
        adversary_position="Challenge necessity of wheel replacement if measurements are marginal",
        counter_arguments=[
            "WILD readings can be affected by track anomalies, not just wheel defects",
            "Condemning limits include safety margin, some exceedance may be acceptable short-term",
            "Wheel turning can restore serviceability without full replacement",
            "Cost of premature replacement vs. risk of failure is not always favorable",
            "Multiple WILD systems may give inconsistent readings"
        ],
        resolution_strategy="WILD readings are screening tool, not final determination. Physical inspection and measurement are authoritative. When dimensions violate AAR Rule 41 limits, replacement is mandatory for interchange service. Document measurements and defect photos for owner accountability.",
        entity_scope="All freight cars in AAR interchange service, private car owners, railroads",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="AAR Rule 41 condemning limits are absolute for interchange service. WILD thresholds are guidelines that trigger inspection. Actual measurements control disposition.",
        controlling_precedent="AAR Field Manual Rule 41 is binding on all interchange participants. TTCI research informs industry practice but does not override rules.",
        issue_category=IssueCategory.WHEEL_AXLE_MAINTENANCE
    ),

    DoctrineBlock(
        topic="Air Brake Testing Requirements - Class I/IA/III Freight Car Inspections",
        keywords=["air brake", "COT", "Class I", "Class III", "brake test", "FRA", "leakage"],
        conclusion_template="Freight car air brake systems require periodic testing per FRA Part 232. Class I (COT-1) inspection required annually or at 1,000 miles, whichever occurs first. Class III (COT-5) inspection required at 5,000 miles or when repairs are made. Testing includes piston travel, brake shoe thickness, release, and leakage rate verification.",
        reasoning_framework="""
1. INSPECTION CLASS REQUIREMENTS (49 CFR 232.305):
   - Class I (COT-1): Annual or 1,000 miles, includes complete brake system teardown
   - Class IA: Alternate 1,000 mile inspection, less intensive than Class I
   - Class II: Intermediate inspection at terminal locations
   - Class III (COT-5): 5,000 miles, less intensive than COT-1
   - Single Car Test: After any repair affecting brake performance

2. CLASS I (COT-1) INSPECTION ITEMS:
   - Complete disassembly and cleaning of brake valve
   - Piston travel measurement: 7-9 inch for empty, 9-11 inch for loaded (typical ABD)
   - Brake shoe thickness: Minimum 1/2 inch at thinnest point (new shoe 1.25-1.5 inch)
   - Release time: Car brakes release within 60-90 seconds of brake pipe pressure increase
   - Leakage rate: <5 psi loss per minute with brakes applied, system charged
   - Hand brake effectiveness: Must hold car on 3% grade
   - Air reservoir drainage and inspection for internal corrosion

3. CLASS III (COT-5) INSPECTION ITEMS:
   - External inspection of all brake components
   - Piston travel verification (same limits as Class I)
   - Brake shoe thickness check
   - Air hose condition and coupling test
   - Release time and leakage rate testing
   - Hand brake operation test
   - No disassembly required unless defects found

4. PISTON TRAVEL ADJUSTMENT:
   - Empty car (tare weight): 7-9 inch travel (ABD valve empty position)
   - Loaded car (gross weight): 9-11 inch travel (ABD valve loaded position)
   - Out-of-adjustment: <6 inch or >11 inch requires immediate correction
   - Dead engine: <2 inch travel indicates seized piston or broken rigging
   - Excessive travel: >13 inch indicates worn shoes or rigging failure

5. LEAKAGE RATE TESTING PROCEDURE:
   - Charge system to 70-90 psi brake pipe pressure
   - Apply brakes with 20 psi reduction
   - Measure auxiliary reservoir pressure drop over 1 minute
   - Acceptable: <5 psi loss per minute (newer cars <3 psi)
   - Common leak sources: Gaskets, valve diaphragms, cracked air hoses
   - Test must be conducted with reservoirs fully charged (110-120 psi)

6. BRAKE SHOE CONDEMNING AND REPLACEMENT:
   - Minimum thickness: 1/2 inch at any point on shoe
   - Maximum acceptable wear taper: 1/4 inch across shoe width
   - Composition shoes: Typical life 100K-150K miles
   - Cast iron shoes: Typical life 60K-100K miles (higher wheel wear)
   - Shoe key condition: Must be tight, not worn through

7. AUTOMATIC BRAKE VALVE (ABD/AB/ABDW):
   - Service portion: Modulates brake cylinder pressure based on brake pipe reduction
   - Emergency portion: Dumps brake pipe rapidly for emergency application
   - Load/empty sensor: Adjusts brake force based on car loading
   - Dirt collector: Requires annual cleaning to prevent malfunction
   - Gasket/diaphragm replacement: Every 5-8 years or if leaking

8. DOCUMENTATION REQUIREMENTS:
   - Form FRA F6180-49A: Record of inspection and testing
   - Date performed and performing railroad/contractor identification
   - Stencil on car: "COT [date] [location]"
   - Repair records for any components replaced
   - Retention period: 1 year for Class I/III inspections, 92 days for Class II
        """,
        key_factors=[
            "Mileage since last COT inspection (odometer or consist records)",
            "Date of last COT inspection (must be within 1 year regardless of miles)",
            "Piston travel measurements in empty and loaded positions",
            "Brake shoe thickness at thinnest point",
            "Leakage rate test results (psi loss per minute)",
            "Hand brake holding capability on grade",
            "Previous repair history indicating reliability issues"
        ],
        primary_authority=[
            "49 CFR Part 232 Subpart C (Inspection and Testing Requirements)",
            "FRA Safety Advisory 2011-01 (Freight Car Brake Inspections)",
            "AAR Field Manual Rule 74 (Air Brake and Train Line)",
            "TTCI Research Report R-924 (Brake System Performance Standards)",
            "Wabtec ABD Valve Service Manual (Maintenance Procedures)"
        ],
        burden_holder="Car owner responsible for compliance; operating railroad verifies before accepting in train",
        adversary_position="Extend inspection intervals to reduce costs and car shopping time",
        counter_arguments=[
            "Low-mileage cars sit idle and reach calendar limit without meaningful wear",
            "Modern brake valves are more reliable than older designs requiring annual teardown",
            "External inspections (Class III) are sufficient for well-maintained fleets",
            "Industry data shows low failure rate between COT inspections",
            "Automated condition monitoring could replace fixed-interval inspections"
        ],
        resolution_strategy="FRA Part 232 inspection intervals are regulatory minimums and cannot be extended without FRA waiver. Well-maintained cars may have minimal work at COT, but compliance is mandatory. Condition-based maintenance research is ongoing but not yet approved for freight cars.",
        entity_scope="All freight cars operating in general interchange service under FRA jurisdiction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory requirements are absolute. Inspection procedures are detailed and non-discretionary. Measurement limits (piston travel, shoe thickness, leakage) are objective and enforceable.",
        controlling_precedent="49 CFR Part 232 is federal regulation with civil penalty enforcement. AAR Field Manual provides industry consensus on acceptable practices.",
        issue_category=IssueCategory.BRAKE_SYSTEM
    ),

    DoctrineBlock(
        topic="Journal Bearing Hot Box Detection and Failure Prevention",
        keywords=["hot box", "journal bearing", "temperature", "wayside detector", "bearing failure", "seized bearing"],
        conclusion_template="Journal bearing failures (hot boxes) are detected by wayside hot box detectors (HBDs) measuring bearing temperature. Alarms trigger at 170°F above ambient or when bearing temperature exceeds 200°F. Roller bearing life is typically 1-3 million miles. Proper lubrication, sealing integrity, and load distribution are critical to preventing premature failure.",
        reasoning_framework="""
1. WAYSIDE HOT BOX DETECTOR OPERATION:
   - Infrared sensors scan each bearing as train passes at track speed
   - Absolute alarm: Bearing temp >200°F (typically indicates imminent failure)
   - Differential alarm: Bearing temp >170°F above ambient air temperature
   - Comparison alarm: Bearing >150°F hotter than opposite side bearing on same axle
   - Trending alarm: Bearing temperature increasing >50°F between successive detectors

2. BEARING FAILURE PROGRESSION:
   - Stage 1 - Spalling: Subsurface fatigue cracks propagate to surface (detectible vibration)
   - Stage 2 - Cage deterioration: Roller separator cage wears/breaks (increased friction)
   - Stage 3 - Roller skewing: Misaligned rollers generate excessive heat (HBD alarm)
   - Stage 4 - Seizure: Bearing locks up, wheel slides, potential derailment
   - Time from Stage 1 to Stage 4: Can be as short as 50-200 miles under heavy load

3. BEARING LIFE EXPECTANCY:
   - Timken/SKF freight car bearings: 1-3 million miles (L10 life)
   - Factors reducing life: Overloading (>286K lbs GRL), poor lubrication, contamination
   - Factors extending life: Proper preload, effective seals, moderate service
   - Typical failure rate: 1-3 per 10,000 car-years for well-maintained fleet

4. LUBRICATION REQUIREMENTS:
   - Grease type: NLGI Grade 2 lithium complex or polyurea (high temp stability)
   - Fill quantity: Manufacturer spec (typically 1.5-2.5 lbs per bearing)
   - Over-greasing consequence: Churning generates heat, breaks down grease
   - Under-greasing consequence: Metal-to-metal contact, rapid failure
   - Grease life: 5-7 years if seals remain intact, contamination-free

5. SEAL INTEGRITY VERIFICATION:
   - Wear ring condition: Must not contact axle (clearance 0.010-0.030 inch)
   - Labyrinth seal: Multi-stage design prevents dirt/water ingress
   - Inspection frequency: Every wheel removal or annually during Class I inspection
   - Seal failure indicators: Grease leakage, visible corrosion, water in bearing cavity

6. LOAD DISTRIBUTION EFFECTS:
   - Uneven loading: One axle carries >60% of truck load (increases bearing stress)
   - Hunting: Truck oscillation at high speed (fatigue loading on bearings)
   - Bolster friction: Prevents weight equalization between axles
   - Correction: Verify center plate clearance, friction shoes, spring condition

7. RESPONSE TO HOT BOX ALARM:
   - Absolute (>200°F): Set out car immediately, do not move to siding under power
   - Differential (>170°F): Set out at next available location, inspect before movement
   - Trending (increasing): Monitor at next HBD, set out if temp continues rising
   - Bearing replacement: Both bearings on axle, plus cup/cone if any damage visible

8. BEARING ADAPTER INSTALLATION CRITICAL POINTS:
   - Bearing preload: Set per manufacturer (typically 0.001-0.005 inch end play)
   - Torque sequence: Tighten backing ring to 250-300 ft-lbs in star pattern
   - Seal installation: Lubricate and align carefully to avoid damage
   - Cleanliness: Bearing cavity must be free of dirt, old grease, metal particles
   - Axle journal inspection: Check for fretting, scoring, out-of-round (max 0.003 inch)
        """,
        key_factors=[
            "Wayside HBD alarm history (absolute temp, differential, trending)",
            "Bearing service history (miles since installation, grease fill date)",
            "Visual inspection results (grease leakage, seal damage, corrosion)",
            "Car loading history (typically loaded, empty, or unit train service)",
            "Bearing manufacturer and model (Timken, SKF, FAG specifications)",
            "Track conditions and speed (rough track increases vibration loading)",
            "Climate factors (extreme cold affects grease viscosity, heat dissipation)"
        ],
        primary_authority=[
            "AAR Field Manual Rule 41 Section E (Axles and Bearings)",
            "AAR Manual of Standards S-293 (Roller Bearing Adapters)",
            "FRA Track Safety Standards 49 CFR Part 213 (Wayside Detector Requirements)",
            "Timken Freight Car Bearing Service Manual (Installation and Maintenance)",
            "TTCI Research Report R-967 (Bearing Temperature Analysis and Alarm Thresholds)"
        ],
        burden_holder="Car owner responsible for bearing maintenance; railroad operates HBD systems",
        adversary_position="HBD alarms are overly conservative, many cars set out have serviceable bearings",
        counter_arguments=[
            "Absolute 200°F threshold includes safety margin, actual failure temp may be higher",
            "Environmental factors (sunlight, brake heat transfer) can cause false alarms",
            "Cost of unnecessary setouts and bearing replacements is substantial",
            "Some bearings cool down if given time, don't require immediate replacement",
            "Bearing inspection may reveal no defects despite alarm"
        ],
        resolution_strategy="HBD alarms are statistically-based screening tools. Absolute temp >200°F has high correlation with bearing failure and mandates setout. Visual inspection and temperature re-check at siding determine if bearing replacement is necessary. Err on side of safety given derailment consequences.",
        entity_scope="All freight cars with roller bearings in AAR interchange service",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="HBD alarm thresholds are based on extensive industry data. AAR Field Manual provides clear response protocols. Bearing replacement decision requires physical inspection, not just alarm.",
        controlling_precedent="AAR Field Manual Rule 41 sets bearing condemning criteria. FRA regulations require functioning HBD systems at specified intervals along routes.",
        issue_category=IssueCategory.BEARING_INSPECTION
    ),

    DoctrineBlock(
        topic="Coupler Knuckle Inspection and Replacement Criteria",
        keywords=["coupler", "knuckle", "AAR M-211", "crack detection", "MPI", "fatigue", "E-type"],
        conclusion_template="Coupler knuckles are inspected using visual, magnetic particle (MPI), or ultrasonic methods. Knuckles with cracks, wear beyond limits, or deformation must be replaced. AAR M-211 standard defines dimensional limits. E-type knuckles are standard for 286,000 lbs GRL service. Typical knuckle life is 1-5 million gross tons depending on service.",
        reasoning_framework="""
1. AAR KNUCKLE STANDARDS (M-211):
   - E-type knuckle: Standard for 286K lbs GRL service (replaced F-type in 2000s)
   - Material: AAR Grade B+ or higher carbon steel, controlled chemistry
   - Manufacturing: Investment casting or forging, heat treated to 321-363 BHN
   - Dimensional tolerances: Pulling face, lock chamber, gathering face, tail lugs

2. INSPECTION METHODS:
   - Visual: Daily train crew inspection for obvious cracks, broken parts
   - Hammer test: Strike knuckle and listen for dead ring (indicates crack)
   - Magnetic Particle (MPI): Detects surface and near-surface cracks (annual or post-incident)
   - Ultrasonic Testing (UT): Detects internal defects (specialized use, not routine)
   - Frequency: MPI at major repairs or annually on high-utilization cars

3. CONDEMNING CRITERIA (AAR Field Manual Rule 35):
   - Any visible crack regardless of size or location
   - Wear on pulling face exceeding 5/8 inch vertically
   - Lock chamber wear >1/4 inch in any direction
   - Tail lug wear reducing thickness below 2.5 inch
   - Knuckle pin bore elongation >1/8 inch (oval shape)
   - Deformation from overload (bent tail, distorted lock chamber)

4. CRACK INITIATION SITES:
   - Pulling face: High tensile stress during train handling (start/stop)
   - Knuckle nose: Impact loading during coupling
   - Thrower arm root: Stress concentration during lock/unlock cycles
   - Lock chamber: Wear and impact from lock mechanism
   - Tail lugs: Bending loads from lateral forces in curves

5. FATIGUE LIFE FACTORS:
   - Train handling: Aggressive throttle/braking reduces life 30-50%
   - Loading: Unit coal trains with 286K GRL have higher knuckle loads than manifest
   - Track conditions: Rough track and tight curves increase lateral forces
   - Maintenance: Proper lubrication of knuckle pin and lock reduces wear
   - Typical life range: 1-2 million gross tons (heavy haul) to 5+ million (intermodal)

6. KNUCKLE REPLACEMENT PROCEDURE:
   - Support coupler shank to prevent drop when knuckle is removed
   - Drive out knuckle pin using brass drift (avoid steel hammer damage)
   - Inspect knuckle pin for wear (condemn if diameter <2.625 inch, new = 2.75 inch)
   - Install new E-type knuckle with correct orientation (pulling face marked)
   - Lubricate knuckle pin and lock mechanism with graphite or moly grease
   - Function test: Lock and unlock mechanism, verify full rotation

7. KNUCKLE FAILURE CONSEQUENCES:
   - In-train separation: Runaway cars, potential collision or derailment
   - Coupling failure: Unable to pick up car, blocks main line
   - Emergency response: FRA reportable if results in derailment or injury
   - Costs: Knuckle replacement $150-$300, train delay costs $5K-$50K+

8. PREVENTIVE MEASURES:
   - Avoid slack action: Smooth train handling reduces impact loads
   - Lubrication program: Grease knuckle pins at every shopping opportunity
   - MPI screening: Annual inspection of high-utilization cars
   - Track geometry: Maintain proper curve radius and superelevation
   - Knuckle pin inspection: Replace worn pins before they damage knuckle bore
        """,
        key_factors=[
            "Visual inspection results (cracks, wear, deformation)",
            "MPI or UT inspection findings (date, location, inspector)",
            "Service history (gross tons handled, train types, age of knuckle)",
            "Dimensional measurements vs. AAR condemning limits",
            "Knuckle pin condition (wear, elongation of knuckle bore)",
            "Failure mode if broken (fatigue crack, overload, manufacturing defect)",
            "Track profile and curvature on typical operating routes"
        ],
        primary_authority=[
            "AAR Field Manual Rule 35 (Couplers)",
            "AAR Manual of Standards M-211 (Knuckles for Freight Cars)",
            "AAR Circular C-II-60 (Knuckle Inspection and Testing)",
            "FRA 49 CFR Part 215 (Railroad Freight Car Safety Standards)",
            "TTCI Research Report R-945 (Knuckle Fatigue Life and Crack Detection)"
        ],
        burden_holder="Car owner responsible for coupler maintenance; crew responsible for daily inspection",
        adversary_position="Small cracks or wear slightly beyond limits are acceptable for continued service",
        counter_arguments=[
            "AAR limits are conservative, actual failure often occurs at greater wear",
            "MPI inspection is expensive and time-consuming for uncertain benefit",
            "Many knuckles removed for cracks could have continued in service safely",
            "Replacement knuckles may have manufacturing defects (need MPI on new parts)",
            "Economic pressure to minimize car shopping conflicts with safety margin"
        ],
        resolution_strategy="AAR condemning limits are non-negotiable for interchange service. Any crack indication requires removal regardless of size due to rapid propagation risk under cyclic loading. MPI annual inspection is industry best practice and FRA-recommended. Document all knuckle removals and analyze for failure trends.",
        entity_scope="All freight cars in AAR interchange service, private car fleets, car builders",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="AAR Field Manual Rule 35 provides objective condemning criteria. MPI inspection eliminates subjectivity in crack detection. Knuckle failures have significant safety and operational consequences justifying conservative approach.",
        controlling_precedent="AAR M-211 defines knuckle specifications. AAR Field Manual Rule 35 sets condemning limits. FRA Part 215 establishes federal regulatory baseline.",
        issue_category=IssueCategory.COUPLER_DRAWBAR
    ),

    DoctrineBlock(
        topic="Tank Car Qualification - DOT-111 vs DOT-117 Standards",
        keywords=["tank car", "DOT-111", "DOT-117", "CPC-1232", "flammable liquids", "crude oil", "ethanol", "qualification"],
        conclusion_template="Tank cars carrying flammable liquids must meet DOT-117 or CPC-1232 standards (enhanced DOT-111) after May 2015. DOT-117 requires 9/16 inch tank shell, full-height head shields, thermal protection, and pressure relief devices rated for fire exposure. Tank car qualification involves hydrostatic testing every 10 years and thickness measurements to verify corrosion allowance remains.",
        reasoning_framework="""
1. TANK CAR SPECIFICATION EVOLUTION:
   - DOT-111: Legacy non-pressure tank car (100 psi test pressure)
   - CPC-1232: Enhanced DOT-111 with 7/16 inch shell, half-height head shields (2011)
   - DOT-117: New construction standard post-2015 (9/16 inch shell, full shields)
   - DOT-117R: Retrofit standard for existing DOT-111/CPC-1232 cars
   - AAR-204W: Pressure tank car for LPG, ammonia (60-80 psi test pressure)

2. DOT-117 CONSTRUCTION REQUIREMENTS (49 CFR 179.202):
   - Tank shell: 9/16 inch minimum thickness (TC-128B normalized steel)
   - Head shields: Full-height, 1/2 inch minimum, extending to top of tank
   - Jacket/thermal protection: 4 inch ceramic fiber or equivalent
   - Top fittings protection: 1/2 inch steel housing around valves/manholes
   - Bottom outlet valve: Nozzle valve with excess flow protection
   - Pressure relief: Two devices, fire-rated at 75% MAWP for 100 minutes

3. RETROFIT REQUIREMENTS (DOT-117R):
   - Existing DOT-111 cars: Add head shields, jacket, top fittings protection
   - Timeline: Pacing schedule 2015-2029 based on commodity and service
   - Cost: $30K-$60K per car for retrofit vs. $150K-$200K for new DOT-117
   - Alternative: Retire non-compliant cars if retrofit economics unfavorable

4. HYDROSTATIC TESTING (10-year qualification):
   - Test pressure: 5-year = 1.5x MAWP, 10-year = 1.5x MAWP + visual inspection
   - Hold time: Minimum 10 minutes at test pressure, zero leakage
   - Expansion measurement: Permanent expansion <10% of total expansion
   - Inspection items: Internal corrosion, cracks, dents, bulges, weld integrity
   - Reinspection: Anytime car is damaged, repaired, or re-rated

5. THICKNESS MEASUREMENT REQUIREMENTS:
   - Ultrasonic testing at 8+ locations around tank circumference
   - Minimum remaining thickness: Original spec minus corrosion allowance
   - Typical allowance: 0.050-0.100 inch depending on service (crude oil more corrosive)
   - Condemning limit: Thickness below minimum OR remaining allowance <0.025 inch
   - Action: Remove from service, repair/re-rate, or scrap

6. COMMODITY-SPECIFIC REQUIREMENTS:
   - Crude oil (Class 3 flammable): DOT-117 or retrofit by 2029
   - Ethanol (Class 3 flammable): DOT-117 or retrofit by 2023
   - Denatured alcohol: DOT-117 or retrofit by 2023
   - Other flammable liquids: DOT-117 for new construction, legacy cars allowed if qualified
   - Exceptions: Residual crude (K018 listed waste) can use DOT-111 until retired

7. OPERATIONAL RESTRICTIONS:
   - High Hazard Flammable Trains (HHFT): 20+ tank cars or 1 unit train of flammables
   - Speed limits: 50 mph general, 40 mph high-threat urban areas (HTUA)
   - Routing: Avoid HTUAs where practicable, file routing analysis with FRA
   - Securement: DOT-117 does not exempt from brake securement rules

8. INSPECTION AND MARKING:
   - Specification stencil: DOT-117, DOT-111, CPC-1232 (visible on car sides)
   - Test date stencil: Month/year of last hydrostatic test (10-year cycle)
   - Capacity stencil: Gallons, pounds, nominal capacity, test pressure
   - Manway inspection: Annual external, 10-year internal during qualification
        """,
        key_factors=[
            "Tank car specification (DOT-111, CPC-1232, DOT-117, DOT-117R)",
            "Commodity being transported (crude oil, ethanol, other flammables)",
            "Date of last hydrostatic test and qualification (10-year cycle)",
            "Thickness measurements vs. minimum required for continued service",
            "Presence of required safety features (head shields, jacket, pressure relief)",
            "Compliance with retrofit timeline for non-DOT-117 cars",
            "Operating restrictions based on train composition (HHFT rules)"
        ],
        primary_authority=[
            "49 CFR Part 179 Subpart D (Tank Car Specifications)",
            "49 CFR 174.310 (Handling of Tank Cars)",
            "DOT-PHMSA Final Rule HM-251 (Enhanced Tank Car Standards)",
            "AAR Manual of Standards M-1002 (Tank Car Inspection and Test)",
            "RSPA/FRA Safety Advisory 2014-03 (Crude Oil Transportation)"
        ],
        burden_holder="Car owner responsible for maintaining qualification; shipper verifies car is appropriate for commodity",
        adversary_position="Retrofit requirements are excessively costly and force premature retirement of serviceable cars",
        counter_arguments=[
            "DOT-111 cars have acceptable safety record for non-crude service",
            "Retrofit costs ($30K-$60K) approach value of older cars",
            "Timeline is too aggressive given car builder capacity constraints",
            "Enhanced operational rules (speed, routing) mitigate risk without retrofits",
            "Statistical analysis shows marginal safety benefit for some commodities"
        ],
        resolution_strategy="DOT-117 standard is federal regulation and non-negotiable for new construction post-2015. Retrofit timeline has statutory deadlines with limited FRA discretion. Economic analysis may support early retirement vs. retrofit for older, low-utilization cars. Commodity-specific timelines allow prioritization of highest-risk traffic.",
        entity_scope="Tank car owners, crude oil and ethanol shippers, Class I and shortline railroads",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Federal regulation is unambiguous. Retrofit timeline is statutory with defined phase-in. Qualification testing procedures are detailed in AAR M-1002. Enforcement includes civil penalties and car service restrictions.",
        controlling_precedent="49 CFR Part 179 is federal regulation. HM-251 Final Rule established retrofit timeline. AAR M-1002 defines testing procedures.",
        issue_category=IssueCategory.TANK_CAR_QUALIFICATION
    ),

    DoctrineBlock(
        topic="Traction Motor Inspection and Commutator Maintenance",
        keywords=["traction motor", "commutator", "flashover", "insulation", "megger test", "carbon brushes"],
        conclusion_template="Locomotive traction motors convert electrical energy to mechanical torque. DC motors require commutator and brush maintenance every 92 days or 25,000 miles. AC motors (inverter-driven) have no brushes but require bearing and insulation testing. Commutator surface must be smooth within 0.010 inch runout. Insulation resistance (megger test) must exceed 1 megohm at 500V DC.",
        reasoning_framework="""
1. TRACTION MOTOR TYPES:
   - DC Series Wound: Legacy locomotives (EMD SD40-2, GE C40-8), high maintenance
   - DC Separately Excited: Transitional designs (EMD SD60M), better control
   - AC Induction: Modern standard (GE ES44AC, EMD SD70ACe), low maintenance
   - Permanent Magnet AC: Emerging (Wabtec FLXdrive), highest efficiency

2. DC MOTOR COMMUTATOR MAINTENANCE:
   - Inspection frequency: 92 days or 25,000 miles (FRA Part 229.23)
   - Surface condition: Smooth, no bars lifted, grooves <0.020 inch deep
   - Runout: Maximum 0.010 inch total indicator reading (TIR) at operating speed
   - Mica undercutting: 1/32 inch below bar surface (prevents bar-to-bar shorts)
   - Turning/grinding: Restore surface when runout >0.010 inch or grooving excessive

3. CARBON BRUSH INSPECTION:
   - Brush length: Minimum 1.5 inch remaining (new brush 3-4 inch)
   - Brush pressure: 2-3 psi against commutator (spring-loaded holder)
   - Brush seating: 75%+ contact area with commutator surface (check with carbon paper)
   - Brush wear rate: Typical 1 inch per 40K-60K miles (varies by service)
   - Replacement: All brushes in set when any reach minimum length

4. FLASHOVER CAUSES AND PREVENTION:
   - Flashover: Arcing between commutator bars, can cascade to full motor failure
   - Causes: Carbon dust buildup, oil contamination, high humidity, excessive load
   - Prevention: Regular blowout with compressed air (monthly), keep motor dry
   - Load management: Avoid excessive current (>900A per motor on SD40-2)
   - Warning signs: Blue arcing visible in inspection ports, ozone smell, carbon tracking

5. INSULATION RESISTANCE TESTING (MEGGER):
   - Test voltage: 500V DC for motors rated <1000V, 1000V DC for higher voltage
   - Minimum acceptable: 1 megohm (1,000,000 ohms) at operating temperature
   - Test points: Each field coil, armature to ground, field to armature
   - Failure indicators: <0.5 megohm suggests moisture or insulation breakdown
   - Corrective action: Bake motor at 200-250°F for 8-24 hours to remove moisture

6. AC TRACTION MOTOR MAINTENANCE:
   - No commutator or brushes: Eliminates 80% of DC motor maintenance
   - Bearing inspection: 92-day visual, annual greasing, 5-7 year replacement
   - Insulation testing: Annual megger test, same 1 megohm minimum
   - Rotor bar inspection: Check for cracks or looseness (vibration analysis)
   - Encoder/resolver: Speed sensor critical for inverter control, test during PMI

7. BEARING MAINTENANCE (AC AND DC MOTORS):
   - Bearing type: Roller or ball bearing, sealed or regreased design
   - Greasing interval: Annual for accessible bearings, sealed bearings lifetime-filled
   - Grease type: NLGI Grade 2 lithium complex, high temp (350°F+)
   - Failure indicators: Noise, vibration, elevated bearing temperature (>180°F)
   - Replacement: Both bearings when either fails, inspect rotor/stator for rub damage

8. MOTOR REMOVAL AND REPLACEMENT:
   - Typical life: DC motors 1-2 million miles, AC motors 2-3 million miles
   - Removal triggers: Insulation failure, bearing seizure, rotor/stator damage
   - Exchange program: Swap failed motor with remanufactured unit (24-48 hour turnaround)
   - Rebuild cost: $15K-$30K per DC motor, $25K-$50K per AC motor
   - New motor cost: $40K-$60K (DC), $60K-$100K (AC)
        """,
        key_factors=[
            "Motor type (DC series, DC sep-ex, AC induction, permanent magnet)",
            "Mileage and operating hours since last inspection/maintenance",
            "Commutator runout and surface condition (DC motors only)",
            "Carbon brush length and seating (DC motors only)",
            "Insulation resistance megger test results (all motor types)",
            "Bearing condition and noise/vibration levels",
            "Service type (heavy haul, intermodal, switching affects duty cycle)"
        ],
        primary_authority=[
            "49 CFR Part 229.23 (Periodic Inspection Requirements)",
            "AAR Manual of Standards S-5507 (Locomotive Maintenance)",
            "EMD Service Manual GT-46 (DC Traction Motor Maintenance)",
            "GE Transportation ES44AC Maintenance Manual (AC Traction Motor)",
            "IEEE Std 43-2013 (Recommended Practice for Insulation Resistance Testing)"
        ],
        burden_holder="Railroad mechanical department responsible for locomotive maintenance",
        adversary_position="Extend inspection intervals for AC motors given elimination of brush/commutator wear",
        counter_arguments=[
            "AC motors have dramatically lower maintenance requirements than DC",
            "92-day inspection interval is legacy requirement based on DC motor needs",
            "Insulation testing can be performed less frequently with condition monitoring",
            "Bearing failures are infrequent and detectable via vibration analysis",
            "Modern motors are more reliable and could support extended intervals"
        ],
        resolution_strategy="FRA Part 229.23 sets regulatory minimum inspection frequency (92 days) that applies to all locomotives regardless of motor type. Railroads may petition FRA for alternative inspection intervals with supporting data. Condition-based maintenance using sensors is allowed as supplement, not replacement for regulatory inspections.",
        entity_scope="Class I railroads, shortlines, locomotive leasing companies, industrial railroads",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="FRA Part 229 inspection requirements are regulatory and enforceable. Motor manufacturer specifications provide technical standards. AC motor maintenance is objectively less intensive than DC but regulatory requirements still apply.",
        controlling_precedent="49 CFR Part 229.23 establishes inspection intervals. IEEE standards provide testing methodology. Manufacturer manuals define maintenance procedures.",
        issue_category=IssueCategory.ELECTRICAL_TRACTION
    ),

    DoctrineBlock(
        topic="Condition-Based Maintenance Using Vibration Analysis and Oil Sampling",
        keywords=["predictive maintenance", "vibration analysis", "oil analysis", "CBM", "condition monitoring", "PdM"],
        conclusion_template="Condition-based maintenance (CBM) extends component life and reduces unplanned failures by monitoring actual equipment condition rather than relying solely on time/mileage intervals. Vibration analysis detects bearing, gear, and alignment problems. Oil analysis reveals wear metals, contamination, and lubricant degradation. CBM programs can reduce maintenance costs 20-30% while improving reliability.",
        reasoning_framework="""
1. VIBRATION ANALYSIS FUNDAMENTALS:
   - Accelerometer placement: Bearings, gearboxes, couplings, drive shafts
   - Measurement units: Velocity (in/sec RMS), acceleration (g's), displacement (mils)
   - Frequency analysis: FFT spectrum reveals specific defect frequencies
   - Trending: Establish baseline, monitor for increases >25% indicating developing problem

2. BEARING DEFECT FREQUENCIES:
   - Ball Pass Frequency Outer Race (BPFO): Number of balls × shaft speed × contact angle
   - Ball Pass Frequency Inner Race (BPFI): Higher frequency than BPFO
   - Ball Spin Frequency (BSF): Indicates spalling on ball surface
   - Fundamental Train Frequency (FTF): Cage wear or imbalance
   - Typical progression: Detectable vibration increase 1-3 months before failure

3. GEARBOX MONITORING:
   - Gearmesh frequency: Number of teeth × shaft RPM
   - Sidebands: Spacing indicates modulation source (bearing, shaft imbalance)
   - Amplitude increase: >6 dB rise from baseline indicates wear progression
   - Applications: Locomotive truck gearboxes, engine gear trains, turbocharger drives

4. OIL ANALYSIS PARAMETERS:
   - Wear metals: Iron, copper, aluminum, chromium, lead (measured in ppm)
   - Viscosity: Lubricant breakdown or fuel/coolant contamination (cSt at 40°C/100°C)
   - Total Base Number (TBN): Acid neutralization capability, depletion indicates oil age
   - Total Acid Number (TAN): Oxidation level, increases with oil degradation
   - Particle count: ISO cleanliness code (e.g., 18/16/13 = acceptable for gearbox)

5. DIESEL ENGINE OIL ANALYSIS:
   - Iron: <50 ppm normal, >100 ppm indicates abnormal cylinder/bearing wear
   - Copper: <25 ppm normal, elevated suggests bearing wear
   - Lead: <10 ppm normal, higher indicates bearing overlay wear
   - Chromium: Piston ring wear indicator
   - Silicon: Dirt ingress (air filter failure) if >15 ppm
   - Fuel dilution: >2% indicates injector leakage or incomplete combustion
   - Coolant: Glycol presence indicates head gasket or cooler leak

6. BEARING GREASE ANALYSIS:
   - Appearance: Color change (dark = oxidation), texture (chunky = contamination)
   - Cone penetration: NLGI grade verification (Grade 2 = 265-295)
   - Dropping point: Minimum 400°F for high-temp applications
   - Water content: <0.5% acceptable, >2% requires bearing cleaning/regreasing
   - Wear metals: Same interpretation as oil, elevated iron indicates bearing distress

7. CBM PROGRAM IMPLEMENTATION:
   - Baseline establishment: Measure all parameters when equipment is new/rebuilt
   - Sampling frequency: Monthly for critical equipment, quarterly for non-critical
   - Alarm limits: 2-sigma (caution), 3-sigma (alarm), 4-sigma (critical)
   - Integration: Combine vibration, oil, thermal imaging, electrical signature analysis
   - Work order triggers: Automated work order generation when alarms exceeded

8. ECONOMIC ANALYSIS:
   - Program cost: $50-$150 per sample (oil), $200-$500 per vibration route
   - Avoided failures: 1 avoided locomotive bearing failure = $5K-$15K (parts + labor + delay)
   - Component life extension: 15-25% typical for engines, gearboxes, bearings
   - ROI: Positive return typically achieved with 20+ unit fleet
   - Integration with CMMS: Predictive maintenance work orders prioritized by condition severity
        """,
        key_factors=[
            "Vibration amplitude and frequency spectrum changes vs. baseline",
            "Oil analysis wear metal trends (ppm increase over time)",
            "Viscosity and additive depletion (TBN, TAN) indicating oil age",
            "Contamination levels (silicon, water, fuel dilution)",
            "Equipment criticality and failure consequence (locomotive vs. MOW equipment)",
            "Sampling frequency and consistency (monthly, quarterly)",
            "Integration with maintenance planning systems (CMMS)"
        ],
        primary_authority=[
            "ISO 13379-1:2012 (Condition Monitoring and Diagnostics)",
            "ISO 4406:2021 (Hydraulic Fluid Contamination by Particle Count)",
            "ASTM D6595 (Wear Metals and Contaminants in Used Lubricating Oils)",
            "ISO 18436-2:2014 (Vibration Condition Monitoring and Diagnostics)",
            "SAE J300 (Engine Oil Viscosity Classification)"
        ],
        burden_holder="Railroad mechanical department implements and funds CBM program",
        adversary_position="CBM programs are expensive and duplicate time-based maintenance without proven benefit",
        counter_arguments=[
            "Initial program cost and training requirements are substantial",
            "False alarms lead to unnecessary component replacements",
            "Time-based maintenance is simpler and proven effective for decades",
            "Small fleets cannot justify dedicated CBM program investment",
            "Sensor installation and data collection infrastructure is expensive"
        ],
        resolution_strategy="CBM programs are most cost-effective for large fleets (100+ locomotives) with high equipment utilization. Start with pilot program on critical equipment (prime movers, traction motors). Establish baseline on known-good equipment. Set conservative alarm limits initially and refine based on false alarm rate. Integrate with existing maintenance planning systems.",
        entity_scope="Class I railroads, large shortlines, locomotive leasing companies, industrial operations",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="CBM technology and methodology are well-established in industrial settings. Railroad application requires adaptation to mobile equipment and harsh environments. ROI is demonstrated but requires upfront investment and program discipline.",
        controlling_precedent="ISO standards provide technical methodology. Industry best practices from airlines, maritime, manufacturing provide implementation guidance. No regulatory requirement for CBM but FRA encourages adoption.",
        issue_category=IssueCategory.PREDICTIVE_MAINTENANCE
    ),

    DoctrineBlock(
        topic="Locomotive Fuel System Maintenance - Injector Testing and Cleaning",
        keywords=["fuel injector", "nozzle", "spray pattern", "fuel system", "pop test", "EMD", "GE"],
        conclusion_template="Fuel injectors must atomize diesel fuel into fine spray for efficient combustion. Injector testing includes pop pressure (2,500-3,200 psi typical), spray pattern verification, and leakage testing. Fouled injectors cause incomplete combustion, black smoke, power loss, and increased fuel consumption. Cleaning or replacement is required every 100,000-150,000 miles in heavy service.",
        reasoning_framework="""
1. INJECTOR FUNCTION AND DESIGN:
   - Mechanical injectors: Spring-loaded valve opens at calibrated pressure
   - Unit injectors: Combined pump and nozzle (EMD 710 series)
   - Common rail injectors: Electronically controlled (GE GEVO series)
   - Spray pattern: 160-degree cone angle, atomized droplets <100 microns

2. POP TESTING PROCEDURE:
   - Mount injector in test bench, connect to pressurized test oil
   - Measure opening pressure: 2,500-3,200 psi depending on engine model
   - Verify spray pattern: Even cone, no streaming or dripping
   - Check back leakage: <10 drops per minute at holding pressure
   - Acceptance criteria: Within ±100 psi of specification, no defects

3. INJECTOR FOULING MECHANISMS:
   - Carbon deposits: Incomplete combustion products plug nozzle orifices
   - Varnish/lacquer: Fuel thermal degradation at high temperatures
   - Corrosion: Water contamination or sulfur in fuel
   - Cavitation erosion: Pressure cycling damages nozzle seat
   - Progression: Spray pattern deteriorates → power loss → black smoke → failure

4. CLEANING METHODS:
   - Ultrasonic cleaning: 40 kHz bath with detergent, 15-30 minutes
   - Chemical soak: Injector cleaning solution (alkaline or acidic), 4-8 hours
   - Mechanical reaming: Wire brushing nozzle tips (EMD unit injectors only, not common rail)
   - High-pressure reverse flush: 500-1000 psi clean diesel
   - Effectiveness: 80-90% of fouled injectors restored to specification

5. REPLACEMENT CRITERIA:
   - Spray pattern defects: Streaming, dripping, uneven cone
   - Pop pressure deviation: >200 psi from specification after cleaning
   - Excessive leakage: >20 drops per minute indicates seat damage
   - Nozzle erosion: Orifice diameter >10% over specification
   - Electrical failure: Solenoid coil resistance out of range (common rail)

6. FUEL QUALITY IMPACT:
   - Sulfur content: <15 ppm ULSD reduces injector deposits vs. 500 ppm
   - Cetane number: >40 required, >45 preferred for cold starting
   - Lubricity: Minimum 520 microns HFRR wear scar (ASTM D6079)
   - Water content: <200 ppm, excessive water causes corrosion
   - Particulate filtration: 2-5 micron absolute required for common rail

7. COMMON RAIL SYSTEM SPECIFICS (GE GEVO):
   - Rail pressure: 28,000-30,000 psi (10x mechanical injector pressure)
   - Electronic control: Injection timing and duration optimized per cylinder
   - Multiple injections: Pilot, main, post-injection for emissions control
   - Filter requirements: 2 micron absolute, change every 50K miles
   - High-pressure pump: Critical component, failure contaminates entire rail

8. TROUBLESHOOTING SYMPTOMS:
   - Black smoke: Overfueling or incomplete combustion (fouled injectors)
   - White smoke: Coolant in combustion (not injector-related, head gasket issue)
   - Rough idle: Uneven cylinder firing, check injectors and compression
   - Power loss: Injectors not delivering rated fuel flow
   - High fuel consumption: Leaking injectors or incorrect pop pressure
        """,
        key_factors=[
            "Injector pop pressure test results vs. specification",
            "Spray pattern visual inspection (cone angle, atomization, dripping)",
            "Back leakage rate (drops per minute at holding pressure)",
            "Mileage/hours since last injector service",
            "Fuel quality history (sulfur, cetane, water contamination)",
            "Engine symptoms (smoke color, power loss, fuel consumption)",
            "Injector type (mechanical, unit, common rail electronic)"
        ],
        primary_authority=[
            "EMD Service Manual 710G3C (Fuel System Maintenance)",
            "GE Transportation ES44AC Maintenance Manual (Common Rail Fuel System)",
            "Bosch Diesel Fuel Injection Manual (Injector Testing Procedures)",
            "ASTM D975 (Standard Specification for Diesel Fuel Oils)",
            "SAE J313 (Diesel Fuels - Specification)"
        ],
        burden_holder="Railroad mechanical department maintains locomotive fuel systems",
        adversary_position="Extend injector service intervals to reduce maintenance costs",
        counter_arguments=[
            "Modern ULSD fuel has lower sulfur and causes less injector fouling",
            "Cleaning/testing all injectors is time-consuming and labor-intensive",
            "Running injectors to failure and replacing only bad ones is more economical",
            "Fuel additives can reduce deposits and extend service life",
            "Common rail systems are more tolerant of marginal injector performance"
        ],
        resolution_strategy="Injector service interval should be based on fuel quality, engine load factors, and observed performance degradation. High-sulfur fuel or heavy loading justifies shorter intervals (100K miles). ULSD fuel in moderate service may extend to 200K+ miles. Pop testing is quick (<5 min per injector) and identifies marginal units before they cause operational issues.",
        entity_scope="All diesel locomotive operators, contract maintenance shops, component remanufacturers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Injector testing procedures are standardized and objective. Pop pressure and spray pattern are measurable parameters. Service intervals are experience-based and vary by operating conditions.",
        controlling_precedent="Manufacturer service manuals define testing procedures and acceptance criteria. ASTM fuel standards ensure minimum quality baseline.",
        issue_category=IssueCategory.PRIME_MOVER
    ),

    DoctrineBlock(
        topic="Locomotive Cooling System Maintenance - Radiator and Coolant Management",
        keywords=["cooling system", "radiator", "coolant", "antifreeze", "water treatment", "corrosion inhibitor"],
        conclusion_template="Locomotive cooling systems must maintain engine temperature between 160-200°F under full load. Coolant is typically 50/50 ethylene glycol and treated water. Radiator core fouling reduces heat transfer capacity. Coolant must be tested annually for freeze protection, pH, and inhibitor concentration. Systems should be flushed and refilled every 3-5 years or when contaminated.",
        reasoning_framework="""
1. COOLING SYSTEM DESIGN:
   - Radiator capacity: Sized to dissipate 35-40% of engine heat output (2,000-3,000 HP engine = 700-1,200 HP heat rejection)
   - Coolant flow rate: 150-300 GPM typical for road locomotive
   - Operating pressure: 15-20 psi (increases boiling point to 240-250°F)
   - Temperature control: Thermostat maintains 160-200°F range
   - Fan drive: Engine-driven, hydraulic, or electric, modulated by temperature

2. COOLANT COMPOSITION:
   - Ethylene glycol: 40-60% by volume (50% = -34°F freeze protection)
   - Water: Deionized or softened, <200 ppm total dissolved solids (TDS)
   - Supplemental Coolant Additive (SCA): Corrosion and cavitation inhibitors
   - pH: 8.0-11.0 (alkaline inhibits corrosion)
   - Nitrite: 1,200-2,400 ppm (cavitation protection for cylinder liners)

3. RADIATOR CORE FOULING:
   - External fouling: Diesel soot, oil mist, dirt, insects block airflow
   - Internal fouling: Scale, corrosion products, oil contamination reduce heat transfer
   - Detection: Elevated coolant temperature under load despite full radiator capacity
   - Cleaning: External - pressure wash or steam clean, Internal - chemical descaling
   - Frequency: External every 92-day inspection, internal every 3-5 years

4. COOLANT TESTING AND ANALYSIS:
   - Freeze point: Refractometer or hydrometer, maintain -20°F minimum protection
   - pH: Litmus paper or meter, 8.0-11.0 acceptable range
   - Nitrite: Test strips, 1,200-2,400 ppm (EMD spec), 1,600-3,000 ppm (GE spec)
   - Glycol concentration: Refractometer, 40-60% range
   - Contamination: Oil (indicates leak), fuel (combustion leak), chloride (corrosion)

5. SYSTEM FLUSHING PROCEDURE:
   - Drain coolant completely, inspect for sludge or debris
   - Fill with water and descaling chemical, run engine to operating temp
   - Circulate descaler for 2-4 hours, drain and flush with clean water
   - Repeat water flush until discharge is clear
   - Refill with 50/50 glycol/water mix plus SCA package
   - Pressure test system to 20 psi, verify no leaks

6. COMMON PROBLEMS:
   - Cavitation erosion: Cylinder liner pitting from coolant vapor bubble collapse
   - Electrolysis: Stray current causes metal corrosion, check ground paths
   - Silicate dropout: Gel formation if incompatible coolant types mixed
   - Oil contamination: Reduces heat transfer, indicates oil cooler leak
   - Aeration: Air in system from leaks or low coolant level, causes hot spots

7. COOLANT LIFE EXTENSION:
   - SCA addition: Replenish inhibitors every 50K-100K miles
   - Filtration: Spin-on coolant filter removes particulates and neutralizes acid
   - Monitoring: Test coolant every 92-day inspection, trending analysis
   - Avoid mixing: Don't mix conventional (green) with extended life (red/orange) coolants
   - Top-off with premixed: Prevents dilution of glycol concentration

8. COOLANT REPLACEMENT TRIGGERS:
   - Scheduled interval: 3-5 years or 500K-750K miles (whichever first)
   - pH out of range: <8.0 or >11.5 (acids damage gaskets, alkaline causes deposits)
   - Contamination: Oil, fuel, or chloride presence
   - Inhibitor depletion: Nitrite <1,000 ppm or SCA <50% of specification
   - Freeze protection loss: Freeze point >-10°F (indicates water dilution)
        """,
        key_factors=[
            "Coolant freeze point and glycol concentration",
            "pH and nitrite/inhibitor levels",
            "Presence of contamination (oil, fuel, chloride)",
            "Radiator core condition (external fouling, internal scale)",
            "Operating temperature under load (normal vs. elevated)",
            "Coolant age and mileage since last change",
            "Test history and trending data"
        ],
        primary_authority=[
            "EMD Service Manual 710G3C (Cooling System Maintenance)",
            "GE Transportation ES44AC Maintenance Manual (Cooling System)",
            "ASTM D6210 (Standard Specification for Fully-Formulated Glycol Base Engine Coolant)",
            "TMC RP 329 (Recommended Practice for Heavy Duty Engine Coolant)",
            "Fleetguard Coolant Analysis Service Manuals"
        ],
        burden_holder="Railroad mechanical department maintains locomotive cooling systems",
        adversary_position="Extend coolant change intervals beyond manufacturer recommendations to reduce costs",
        counter_arguments=[
            "Extended life coolants (ELC) are rated for 600K-1M miles vs. conventional 300K-500K",
            "Regular SCA additions can extend conventional coolant life indefinitely",
            "Coolant testing is inexpensive and allows condition-based replacement",
            "Modern engines have better corrosion resistance, less sensitive to marginal coolant",
            "Flushing and refilling is time-consuming and generates hazardous waste"
        ],
        resolution_strategy="Coolant replacement should be driven by test results, not arbitrary intervals. pH, inhibitor concentration, and contamination are objective criteria. Extended life coolants justify longer intervals but require compatible system components (no traditional rubber hoses). Regular testing (92-day) allows early detection of problems.",
        entity_scope="All diesel locomotive operators, maintenance contractors, coolant suppliers",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Coolant testing procedures are standardized (ASTM). Manufacturer specifications define acceptable parameter ranges. Condition-based replacement is supported by test data.",
        controlling_precedent="Manufacturer service manuals define coolant specifications and maintenance intervals. ASTM standards provide testing methodology.",
        issue_category=IssueCategory.PRIME_MOVER
    ),

    DoctrineBlock(
        topic="Truck (Bogie) Frame Inspection and Crack Detection",
        keywords=["truck frame", "bogie", "crack detection", "MPI", "fatigue", "pedestal", "side frame"],
        conclusion_template="Freight car truck frames (bogies) are subject to fatigue cracking from millions of load cycles. Cracks typically initiate at stress concentrations (pedestal fillets, bolster pockets, spring seats). Magnetic particle inspection (MPI) is required annually or after derailment/collision. Cracks exceeding AAR condemning limits require frame replacement. Weld repairs are restricted and require AAR approval.",
        reasoning_framework="""
1. TRUCK FRAME DESIGN AND LOADING:
   - Three-piece truck: Standard for North American freight cars (two side frames, one bolster)
   - Side frame: Cast or fabricated steel, carries vertical loads to wheelsets
   - Bolster: Connects car body to truck, allows rotation and suspension travel
   - Typical load: 286,000 lbs GRL = 71,500 lbs per wheelset (143K lbs per truck)
   - Stress cycles: 1-5 million cycles per million gross tons (dynamic loading)

2. CRACK-PRONE LOCATIONS:
   - Pedestal fillet: Transition from jaw to side frame column (highest stress concentration)
   - Bolster pocket: Side frame cutout where bolster nests
   - Spring seats: Support points for coil springs
   - Brake beam guides: Attachment points for brake rigging
   - Wear plate areas: Interface surfaces subject to fretting

3. MAGNETIC PARTICLE INSPECTION (MPI) PROCEDURE:
   - Clean area: Remove rust, paint, oil using wire brush or solvent
   - Magnetize: Apply DC or AC electromagnetic field using yoke or coil
   - Apply particles: Spray or dust ferromagnetic particles on surface
   - Interpret: Particle accumulation reveals crack location and orientation
   - Demagnetize: Remove residual magnetism after inspection

4. AAR CONDEMNING CRITERIA (Field Manual Rule 42):
   - Any crack >3/4 inch in length on load-bearing surface
   - Crack at pedestal fillet >1/2 inch length
   - Crack at bolster pocket >1 inch length
   - Any crack that propagates through section thickness
   - Multiple cracks in close proximity (<2 inch spacing)

5. REPAIR LIMITATIONS:
   - Welding repairs: Generally prohibited on cast side frames (residual stress issues)
   - Fabricated side frames: Limited weld repair allowed with AAR approval
   - Grinding: Surface defects <1/8 inch deep may be ground smooth if outside critical areas
   - Replacement: Standard response for cracks exceeding condemning limits
   - Service life: Truck frame replacement typically 30-50 years or 3-5 million gross tons

6. INSPECTION FREQUENCY:
   - Annual: All freight cars during COT-1 inspection
   - Post-derailment: 100% MPI of trucks involved in derailment
   - Post-collision: MPI of trucks if impact force exceeded 50,000 lbs
   - High-mileage cars: Some railroads perform MPI at 6-month intervals for unit trains

7. FATIGUE LIFE FACTORS:
   - Load magnitude: 286K GRL has 3-4x fatigue loading vs. 263K GRL
   - Load distribution: Uneven loading (bolster binding) accelerates cracking
   - Track quality: Rough track increases dynamic loads by 20-50%
   - Car utilization: Unit trains accumulate fatigue cycles faster than manifest cars
   - Manufacturing quality: Casting defects or weld flaws reduce fatigue life

8. PREVENTIVE MEASURES:
   - Shot peening: Compressive stress layer at surface inhibits crack initiation
   - Stress relief: Heat treatment reduces residual stresses from manufacturing
   - Geometry optimization: Modern frame designs minimize stress concentrations
   - Load management: Avoid overloading (>286K GRL), verify even load distribution
   - Track maintenance: Smooth track reduces dynamic loading
        """,
        key_factors=[
            "MPI inspection results (crack location, size, orientation)",
            "Truck frame type (cast vs. fabricated, manufacturer, model)",
            "Service history (gross tons accumulated, age, derailment history)",
            "Load type (unit coal train, intermodal, manifest, typically loaded or empty)",
            "Track conditions on typical operating routes (rough vs. well-maintained)",
            "AAR condemning limit comparison",
            "Repair history (previous cracks, weld repairs)"
        ],
        primary_authority=[
            "AAR Field Manual Rule 42 (Truck Components)",
            "AAR Manual of Standards S-369 (Truck Performance Requirements)",
            "ASTM E709 (Standard Guide for Magnetic Particle Testing)",
            "FRA Track Safety Standards 49 CFR Part 213 (Track Geometry)",
            "TTCI Research Report R-978 (Truck Frame Fatigue Life Analysis)"
        ],
        burden_holder="Car owner responsible for truck frame maintenance and inspection compliance",
        adversary_position="Small cracks are not immediately hazardous and can be monitored rather than requiring immediate replacement",
        counter_arguments=[
            "AAR condemning limits are conservative, actual failure often at larger crack sizes",
            "MPI inspection is expensive ($200-$400 per truck) and time-consuming",
            "Crack growth rate may be slow, allowing extended service with monitoring",
            "Replacement truck frames are expensive ($5K-$10K per truck)",
            "Some cracks are manufacturing artifacts that never propagate"
        ],
        resolution_strategy="AAR Field Manual condemning limits are mandatory for interchange service. Crack size, location, and orientation determine disposition. Conservative approach justified by derailment consequences (equipment damage $500K+, track, delays). Monitoring programs require frequent re-inspection (30-60 days) and documented crack growth rate data.",
        entity_scope="All freight cars in AAR interchange service, private car owners, car builders",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="AAR Field Manual Rule 42 provides objective crack size limits. MPI inspection eliminates subjectivity. Fatigue crack propagation is well-understood but car-specific factors (load, track, age) introduce variability.",
        controlling_precedent="AAR Field Manual Rule 42 is binding on all interchange participants. ASTM E709 defines MPI procedures. FRA Track Safety Standards affect fatigue loading.",
        issue_category=IssueCategory.SUSPENSION_TRUCK
    ),

    DoctrineBlock(
        topic="Safety Appliance Inspection - Ladders, Handholds, and Sill Steps",
        keywords=["safety appliances", "ladder", "handhold", "sill step", "FRA Part 231", "grab iron"],
        conclusion_template="Safety appliances (ladders, handholds, sill steps) must comply with FRA Part 231 dimensional and strength requirements. Handholds must project 2.5 inches from car side. Ladders must have 12-inch spacing between rungs. Sill steps must be 4 inches deep and project 8 inches from car end. Defective safety appliances must be repaired before car moves in interchange.",
        reasoning_framework="""
1. REGULATORY REQUIREMENTS (49 CFR PART 231):
   - Applicability: All railroad rolling stock in interchange service
   - Minimum number: Four vertical ladders (each corner), eight handholds (four per side)
   - Dimensional standards: Precise measurements for clearances, projections, spacing
   - Strength: Must support 250 lbs applied at any point without permanent deformation
   - Visibility: Yellow paint or yellow reflective tape on end ladders/handholds

2. HANDHOLD SPECIFICATIONS:
   - Projection: Minimum 2.5 inches, maximum 4 inches from car side
   - Diameter: 5/8 to 1 inch round stock or equivalent grip
   - Clearance: Minimum 2 inches between handhold and car side
   - Height: Top handhold 30 inches from roof, side handholds 60-66 inches from rail
   - End handholds: Located 8-12 inches from car end

3. VERTICAL LADDER REQUIREMENTS:
   - Rung spacing: 12 inches center-to-center (±2 inches tolerance)
   - Side rail: Minimum 36 inches above roof level
   - Bottom rung: 18-24 inches above top of coupler
   - Clearance: Minimum 6.5 inches from ladder to car side
   - Strength: Each rung must support 250 lbs without permanent deflection

4. SILL STEP SPECIFICATIONS:
   - Width: Minimum 8 inches (measured parallel to car end)
   - Depth: Minimum 4 inches (measured perpendicular to car end)
   - Projection: Minimum 8 inches from face of end sill
   - Height: 24-30 inches above top of rail
   - One on each end of car, centered or offset per design

5. INSPECTION FREQUENCY:
   - Daily: Train crew inspection before departure (visual for obvious defects)
   - COT-1: Annual detailed inspection, measure dimensions, test security
   - COT-5: 5,000-mile inspection, verify all appliances present and secure
   - Post-repair: After any car body work, verify no interference with appliances

6. COMMON DEFECTS:
   - Bent/broken: Impact damage from coupling, collisions, or vandalism
   - Loose: Bolts/welds failed, appliance rotates or rattles
   - Missing: Appliance broken off and not replaced
   - Wrong dimensions: Aftermarket replacement doesn't meet FRA specs
   - Paint/corrosion: Yellow paint worn off end ladders (required for visibility)

7. REPAIR REQUIREMENTS:
   - Immediate: Safety appliance defect renders car non-compliant for movement
   - Replacement parts: Must meet FRA Part 231 dimensions and strength
   - Welding: Preferred attachment method for permanence (bolts can loosen)
   - Torque spec: If bolted, minimum 50 ft-lbs for 5/8 inch bolts
   - Testing: After repair, apply 250 lb load to verify strength

8. SPECIAL CASES:
   - Covered hoppers: Roof hatches count as "roof" for ladder height measurement
   - Tank cars: Walkway brackets may substitute for side handholds if FRA-compliant
   - Intermodal wells: Unique safety appliance arrangement per AAR S-2043
   - End-of-train marker: Mounting bracket cannot interfere with sill step
        """,
        key_factors=[
            "Presence of all required safety appliances (ladders, handholds, sill steps)",
            "Dimensional compliance (projection, spacing, clearance measurements)",
            "Physical condition (bent, broken, loose, corroded)",
            "Attachment security (welds intact, bolts tight)",
            "Yellow visibility markings on end appliances",
            "Accessibility (no obstructions blocking use)",
            "Repair history (recent work, recurring failures)"
        ],
        primary_authority=[
            "49 CFR Part 231 (Railroad Safety Appliance Standards)",
            "AAR Field Manual Rule 4 (Safety Appliances)",
            "FRA Safety Advisory 2010-02 (Safety Appliance Compliance)",
            "AAR Plate C (Clearance Diagram)",
            "OSHA 1910.28 (Walking-Working Surfaces)"
        ],
        burden_holder="Car owner responsible for maintaining compliant safety appliances",
        adversary_position="Minor dimensional deviations or cosmetic damage should not prevent car from moving",
        counter_arguments=[
            "Part 231 dimensional tolerances are tight, minor variations are low risk",
            "Yellow paint requirement is cosmetic, doesn't affect functionality",
            "Slightly bent handholds are still usable and provide adequate grip",
            "Immediate repair requirement causes car delays and shopping costs",
            "Crew rarely uses every safety appliance, redundancy exists"
        ],
        resolution_strategy="FRA Part 231 compliance is non-discretionary for interchange movement. Dimensional standards are precise and measurable. Safety appliances are critical for crew safety during switching and emergencies. Minor cosmetic damage (paint) may be acceptable short-term but structural defects (bent, loose) require immediate repair.",
        entity_scope="All railroad rolling stock in interchange service under FRA jurisdiction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="FRA Part 231 is federal regulation with clear dimensional standards. Measurements are objective. Enforcement includes civil penalties and car service restrictions. Safety justification is compelling (injury prevention).",
        controlling_precedent="49 CFR Part 231 is federal regulation. AAR Field Manual Rule 4 provides industry consensus on inspection and condemning. OSHA regulations apply to workers accessing cars.",
        issue_category=IssueCategory.SAFETY_APPLIANCES
    )
]


# ============================================================================
# AUTHORITY HIERARCHY
# ============================================================================

AUTHORITY_HIERARCHY = [
    AuthorityWeight(1, "FRA Regulations (49 CFR Parts 213, 215, 229, 231, 232)", 1.0, "Federal regulation, highest authority"),
    AuthorityWeight(2, "AAR Field Manual of Interchange Rules", 0.95, "Binding on all AAR members"),
    AuthorityWeight(3, "AAR Manual of Standards and Recommended Practices", 0.90, "Industry consensus standards"),
    AuthorityWeight(4, "Manufacturer Service Manuals (EMD, GE, Wabtec)", 0.85, "OEM specifications and procedures"),
    AuthorityWeight(5, "TTCI Research Reports", 0.75, "Industry research and testing data"),
    AuthorityWeight(6, "ISO/ASTM/SAE Standards", 0.70, "International/national technical standards"),
    AuthorityWeight(7, "Railroad Internal Standards", 0.60, "Company-specific practices"),
    AuthorityWeight(8, "Industry Best Practices", 0.50, "Informal consensus methods")
]


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class RollingStockMaintenanceEngine:
    """Main engine class implementing TIE-20 components"""

    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.authority_hierarchy = AUTHORITY_HIERARCHY
        self.query_count = 0
        self.cache_hits = 0
        self.vector_searches = 0
        self.deep_analyses = 0

        logger.info(f"{ENGINE_ID} initialized with {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(
        self,
        question: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        confidence_target: ConfidenceLevel
    ) -> QueryResponse:
        """
        TIE Component 1: Three-layer response system
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (200-2000ms)
        Layer 3: Deep analysis (2-10s)
        """
        self.query_count += 1
        start_time = datetime.now()

        # Layer 1: Doctrine Cache
        triggered_doctrines, cache_answer = self._check_doctrine_cache(question)

        if cache_answer and mode == ResponseMode.FAST:
            self.cache_hits += 1
            return self._format_response(
                cache_answer,
                triggered_doctrines,
                mode,
                zone,
                confidence_target,
                start_time
            )

        # Layer 2: Semantic Retrieval
        if mode == ResponseMode.DEFENSE or not cache_answer:
            self.vector_searches += 1
            semantic_context = self._semantic_search(question)
            enhanced_answer = self._synthesize_with_context(
                question,
                triggered_doctrines,
                semantic_context
            )

            if mode == ResponseMode.DEFENSE:
                return self._format_response(
                    enhanced_answer,
                    triggered_doctrines,
                    mode,
                    zone,
                    confidence_target,
                    start_time
                )

        # Layer 3: Deep Analysis
        self.deep_analyses += 1
        deep_answer = self._deep_analysis_mode(
            question,
            triggered_doctrines,
            zone
        )

        return self._format_response(
            deep_answer,
            triggered_doctrines,
            mode,
            zone,
            confidence_target,
            start_time
        )

    def _check_doctrine_cache(self, question: str) -> Tuple[List[DoctrineBlock], Optional[str]]:
        """Check if question matches cached doctrine blocks"""
        question_lower = question.lower()
        triggered = []

        for doctrine in self.doctrine_cache:
            # Check keyword matches
            matches = sum(1 for kw in doctrine.keywords if kw.lower() in question_lower)
            if matches >= 2:  # Require at least 2 keyword matches
                triggered.append(doctrine)

        if not triggered:
            return [], None

        # Sort by relevance (keyword match count)
        triggered.sort(
            key=lambda d: sum(1 for kw in d.keywords if kw.lower() in question_lower),
            reverse=True
        )

        # Generate answer from top doctrine
        top_doctrine = triggered[0]
        answer = f"{top_doctrine.conclusion_template}\n\n{top_doctrine.reasoning_framework[:500]}..."

        return triggered, answer

    def _semantic_search(self, question: str) -> str:
        """Simulate semantic vector search (placeholder for real vector DB)"""
        # In production, this would query a vector database
        # For now, return relevant authority references
        relevant_authorities = []
        for doctrine in self.doctrine_cache[:5]:
            relevant_authorities.extend(doctrine.primary_authority[:2])

        return "Relevant authorities: " + "; ".join(set(relevant_authorities))

    def _synthesize_with_context(
        self,
        question: str,
        doctrines: List[DoctrineBlock],
        semantic_context: str
    ) -> str:
        """Synthesize answer combining doctrines and semantic context"""
        if not doctrines:
            return f"Analysis requires deeper research. {semantic_context}"

        primary = doctrines[0]
        answer_parts = [
            primary.conclusion_template,
            "",
            "REASONING:",
            primary.reasoning_framework[:800],
            "",
            "KEY FACTORS:",
            "\n".join(f"- {factor}" for factor in primary.key_factors[:5]),
            "",
            semantic_context
        ]

        return "\n".join(answer_parts)

    def _deep_analysis_mode(
        self,
        question: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone
    ) -> str:
        """
        TIE Component 19: Deep analysis mode
        Multi-source synthesis with full reasoning chain
        """
        if not doctrines:
            return "Deep analysis requires domain expertise not yet encoded in doctrine cache."

        sections = []

        # Executive Summary
        sections.append("EXECUTIVE SUMMARY:")
        sections.append(doctrines[0].conclusion_template)
        sections.append("")

        # Multi-Doctrine Analysis
        if len(doctrines) > 1:
            sections.append("MULTI-DOCTRINE ANALYSIS:")
            for i, doctrine in enumerate(doctrines[:3], 1):
                sections.append(f"\n{i}. {doctrine.topic}")
                sections.append(doctrine.reasoning_framework[:600])
            sections.append("")

        # Authority Hierarchy
        sections.append("AUTHORITY HIERARCHY:")
        all_authorities = []
        for doctrine in doctrines[:3]:
            all_authorities.extend(doctrine.primary_authority)

        for authority in set(all_authorities):
            weight = self._get_authority_weight(authority)
            sections.append(f"- [{weight:.2f}] {authority}")
        sections.append("")

        # Zone-Specific Guidance
        sections.append(f"GUIDANCE FOR {zone.value} CONTEXT:")
        if zone == AnalysisZone.PLANNING:
            sections.append("- Focus on preventive measures and maintenance scheduling")
            sections.append("- Consider cost-benefit analysis of maintenance intervals")
        elif zone == AnalysisZone.REPORTING:
            sections.append("- Document all measurements and observations objectively")
            sections.append("- Reference specific regulatory and industry standards")
        else:  # AUDIT
            sections.append("- Verify compliance with all applicable regulations")
            sections.append("- Retain documentation for FRA inspection")

        return "\n".join(sections)

    def _get_authority_weight(self, authority: str) -> float:
        """Get authority weight from hierarchy"""
        for auth in AUTHORITY_HIERARCHY:
            if auth.source in authority:
                return auth.weight
        return 0.5  # Default for unrecognized authorities

    def _format_response(
        self,
        answer: str,
        triggered_doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone,
        confidence_target: ConfidenceLevel,
        start_time: datetime
    ) -> QueryResponse:
        """Format final response with all TIE components"""

        # Apply epistemic guardrails
        cleaned_answer = self._apply_epistemic_guardrails(answer)

        # Extract authorities
        authorities = []
        for doctrine in triggered_doctrines[:3]:
            authorities.extend(doctrine.primary_authority[:2])

        # Build reasoning chain
        reasoning_chain = [
            f"Triggered {len(triggered_doctrines)} doctrine blocks",
            f"Primary doctrine: {triggered_doctrines[0].topic}" if triggered_doctrines else "No direct doctrine match",
            f"Response mode: {mode.value}",
            f"Analysis zone: {zone.value}"
        ]

        # Epistemic warnings
        warnings = self._generate_epistemic_warnings(cleaned_answer, triggered_doctrines)

        # Determinism hash
        det_hash = self._determinism_hash(answer, triggered_doctrines)

        # Metadata
        elapsed = (datetime.now() - start_time).total_seconds()
        metadata = {
            "query_count": self.query_count,
            "cache_hit": len(triggered_doctrines) > 0,
            "elapsed_seconds": elapsed,
            "doctrine_count": len(triggered_doctrines),
            "authority_count": len(set(authorities))
        }

        return QueryResponse(
            answer=cleaned_answer,
            confidence=triggered_doctrines[0].confidence if triggered_doctrines else ConfidenceLevel.DISCLOSURE,
            authorities_cited=list(set(authorities)),
            reasoning_chain=reasoning_chain,
            triggered_doctrines=[d.topic for d in triggered_doctrines],
            epistemic_warnings=warnings,
            determinism_hash=det_hash,
            response_mode=mode,
            zone=zone,
            metadata=metadata
        )

    def _apply_epistemic_guardrails(self, text: str) -> str:
        """TIE Component 14: Epistemic guardrails - remove banned phrases"""
        cleaned = text
        for phrase in BANNED_PHRASES:
            cleaned = re.sub(
                re.escape(phrase),
                "[EPISTEMIC_VIOLATION_REMOVED]",
                cleaned,
                flags=re.IGNORECASE
            )
        return cleaned

    def _generate_epistemic_warnings(
        self,
        answer: str,
        doctrines: List[DoctrineBlock]
    ) -> List[str]:
        """Generate warnings about epistemic limitations"""
        warnings = []

        if not doctrines:
            warnings.append("No direct doctrine match - answer is synthesized from general knowledge")

        if len(doctrines) == 1 and doctrines[0].confidence == ConfidenceLevel.DISCLOSURE:
            warnings.append("Single doctrine source with DISCLOSURE confidence level")

        # Check for fact fragility markers
        fragile_markers = ["may", "could", "potentially", "estimated", "approximately"]
        fragile_count = sum(1 for marker in fragile_markers if marker in answer.lower())
        if fragile_count > 3:
            warnings.append(f"Answer contains {fragile_count} fragility markers - verify with primary sources")

        return warnings

    def _determinism_hash(self, answer: str, doctrines: List[DoctrineBlock]) -> str:
        """TIE Component 16: SHA-256 determinism hash"""
        content = answer + "".join(d.topic for d in doctrines)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_health(self) -> Dict[str, Any]:
        """TIE Component 12: Health endpoint"""
        return {
            "engine_id": ENGINE_ID,
            "engine_name": ENGINE_NAME,
            "version": VERSION,
            "status": "healthy",
            "doctrine_blocks": len(self.doctrine_cache),
            "authority_levels": len(AUTHORITY_HIERARCHY),
            "queries_processed": self.query_count,
            "cache_hit_rate": self.cache_hits / max(self.query_count, 1),
            "vector_searches": self.vector_searches,
            "deep_analyses": self.deep_analyses,
            "uptime_seconds": 0  # Would track actual uptime in production
        }

    def get_coverage_map(self) -> Dict[str, Any]:
        """TIE Component 10: Coverage map - track triggered/missed doctrines"""
        category_coverage = {}
        for category in IssueCategory:
            matching = [d for d in self.doctrine_cache if d.issue_category == category]
            category_coverage[category.value] = {
                "doctrine_count": len(matching),
                "topics": [d.topic for d in matching]
            }

        return {
            "total_doctrines": len(self.doctrine_cache),
            "categories": len(IssueCategory),
            "category_coverage": category_coverage,
            "epistemic_gaps": self._identify_epistemic_gaps()
        }

    def _identify_epistemic_gaps(self) -> List[str]:
        """Identify areas lacking doctrine coverage"""
        gaps = []

        # Check for categories with few doctrines
        for category in IssueCategory:
            count = sum(1 for d in self.doctrine_cache if d.issue_category == category)
            if count < 2:
                gaps.append(f"{category.value}: Only {count} doctrine block(s)")

        return gaps


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    description="TIE-Grade Rolling Stock Maintenance Intelligence Engine",
    version=VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = RollingStockMaintenanceEngine()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": ENGINE_ID,
        "name": ENGINE_NAME,
        "version": VERSION,
        "status": "operational",
        "endpoints": ["/query", "/health", "/coverage", "/doctrines"]
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Main query endpoint
    TIE Component 17: FastAPI server with typed endpoints
    """
    try:
        logger.info(f"Query received: {request.question[:100]}... | Mode: {request.mode} | Zone: {request.zone}")

        response = engine.three_layer_response(
            request.question,
            request.mode,
            request.zone,
            request.confidence_target
        )

        logger.info(f"Query completed: {len(response.triggered_doctrines)} doctrines | Hash: {response.determinism_hash}")

        return response

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """
    Health check endpoint
    TIE Component 12: Health endpoint
    """
    return engine.get_health()


@app.get("/coverage")
async def coverage():
    """
    Coverage map endpoint
    TIE Component 10: Coverage map
    """
    return engine.get_coverage_map()


@app.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "count": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "category": d.issue_category.value,
                "confidence": d.confidence.value,
                "authorities": len(d.primary_authority)
            }
            for d in engine.doctrine_cache
        ]
    }


@app.get("/authorities")
async def list_authorities():
    """List authority hierarchy"""
    return {
        "hierarchy": [
            {
                "level": a.level,
                "source": a.source,
                "weight": a.weight,
                "citation": a.citation
            }
            for a in AUTHORITY_HIERARCHY
        ]
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Doctrine blocks loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Authority levels: {len(AUTHORITY_HIERARCHY)}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
