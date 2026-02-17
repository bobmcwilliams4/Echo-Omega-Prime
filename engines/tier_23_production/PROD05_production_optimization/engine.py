"""
PROD05 - Production Optimization Engine
TIE Gold Standard - Production Engineering Intelligence

Provides expert guidance on well and field production optimization including:
- Artificial lift selection and optimization
- Wellbore integrity monitoring
- Scale, paraffin, and corrosion management
- Production surveillance and intervention planning
- Facility and gathering system optimization

Port: 9035
Version: 1.0.0
"""

import sys
from pathlib import Path

# CRITICAL: Add engine directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure loguru
logger.add(
    "logs/prod05_production_optimization_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
)

APP = FastAPI(
    title="PROD05 - Production Optimization Engine",
    version="1.0.0",
    description="TIE Gold Standard Production Engineering Intelligence"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ENUMS & MODELS
# ============================================================================

class ResponseMode(str, Enum):
    """Response depth modes"""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels"""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Production optimization issue categories"""
    ARTIFICIAL_LIFT = "ARTIFICIAL_LIFT"
    WELLBORE_INTEGRITY = "WELLBORE_INTEGRITY"
    SCALE_MANAGEMENT = "SCALE_MANAGEMENT"
    PARAFFIN_ASPHALTENE = "PARAFFIN_ASPHALTENE"
    CORROSION_CONTROL = "CORROSION_CONTROL"
    PRODUCTION_SURVEILLANCE = "PRODUCTION_SURVEILLANCE"
    WELL_INTERVENTION = "WELL_INTERVENTION"
    FACILITY_OPTIMIZATION = "FACILITY_OPTIMIZATION"
    GAS_GATHERING = "GAS_GATHERING"
    WATER_HANDLING = "WATER_HANDLING"
    ESG_METRICS = "ESG_METRICS"


class AnalysisZone(str, Enum):
    """Analysis context zones"""
    PLANNING = "PLANNING"
    OPERATIONS = "OPERATIONS"
    AUDIT = "AUDIT"


@dataclass
class DoctrineBlock:
    """Single doctrine block with production optimization expertise"""
    topic: str
    keywords: List[str]
    conclusion_template: List[str]
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
    """Production optimization query request"""
    query: str = Field(..., description="Production optimization question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response depth")
    zone: AnalysisZone = Field(default=AnalysisZone.OPERATIONS, description="Analysis context")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    """Production optimization query response"""
    query: str
    mode: ResponseMode
    zone: AnalysisZone
    answer: str
    confidence: ConfidenceLevel
    doctrine_blocks_used: List[str]
    reasoning_chain: List[str]
    key_factors: List[str]
    recommendations: List[str]
    alternatives_considered: List[str]
    determinism_hash: str
    telemetry: Dict[str, Any]
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    port: int
    doctrine_blocks: int
    categories: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - PRODUCTION OPTIMIZATION EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Artificial Lift Selection Matrix",
        keywords=["artificial lift", "rod pump", "ESP", "gas lift", "PCP", "plunger lift", "lift system", "selection criteria"],
        conclusion_template=[
            "Artificial lift selection depends on well depth, fluid properties, production rate, GLR, deviation, and operational constraints.",
            "Rod pumps excel in shallow to medium depth wells with high viscosity and low to medium rates.",
            "ESPs are optimal for high rate, deep wells with low GLR and minimal solids."
        ],
        reasoning_framework="""
Rod Pump Selection Criteria:
- Depth: Surface to 10,000 ft (practical limit ~7,000 ft)
- Rate: 10-1,500 BFPD (optimal 50-800 BFPD)
- Viscosity: Handles heavy oil well (up to 10,000 cp)
- GLR: Low to moderate (<500 scf/bbl preferred)
- Deviation: Vertical to 15° (can handle more with special rods)
- Advantages: Simple surface equipment, field serviceable, good solids handling
- Disadvantages: Limited depth, stroke frequency limitations, high torque requirements

ESP Selection Criteria:
- Depth: 1,000-20,000+ ft
- Rate: 200-80,000+ BFPD (sweet spot 1,000-10,000 BFPD)
- Viscosity: Light to medium oil (<200 cp optimal)
- GLR: Low (<10% free gas at intake)
- Deviation: Excellent for deviated/horizontal wells
- Advantages: High rate capability, low wellhead profile, good for deep wells
- Disadvantages: Sensitive to solids, expensive workovers, power quality critical

Gas Lift Selection Criteria:
- Depth: 2,000-20,000+ ft
- Rate: 100-20,000 BFPD
- GLR: Moderate to high (>200 scf/bbl, needs gas source)
- Deviation: Handles all deviations
- Advantages: Simple downhole, flexible, good for high GOR wells
- Disadvantages: Requires compression, limited efficiency at low GOR, gas availability

PCP Selection Criteria:
- Depth: Surface to 6,000 ft (practical limit ~4,000 ft)
- Rate: 50-5,000 BFPD
- Viscosity: Excellent for heavy oil (100-100,000 cp)
- Solids: Handles moderate sand production
- Temperature: Elastomer limited (<250°F)
- Advantages: Smooth flow, low shear (good for emulsions), simple operation
- Disadvantages: Elastomer wear, depth limitation, tubing rotation

Plunger Lift Selection Criteria:
- Depth: 2,000-15,000 ft
- Rate: 10-400 BFPD (low liquid rate wells)
- GLR: Very high (>1,000 scf/bbl, needs sufficient gas energy)
- Application: Ideal for dewatering gas wells, liquid loading
- Advantages: No external power, low cost, automatic cycling
- Disadvantages: Limited to high GOR wells, low liquid rates only

Decision Matrix Workflow:
1. Categorize by depth and rate requirements
2. Evaluate fluid properties (viscosity, GLR, water cut, solids)
3. Assess well configuration (deviation, tubular constraints)
4. Consider operational factors (power availability, gas source, service logistics)
5. Evaluate economics (capex, opex, intervention frequency)
6. Select primary system and identify backup options
        """,
        key_factors=[
            "Well depth and bottomhole pressure",
            "Target production rate and drawdown required",
            "Fluid properties (viscosity, GLR, water cut, solids content)",
            "Well deviation and tubular configuration",
            "Available infrastructure (power, gas source, compression)",
            "Operational constraints (remote location, service frequency)",
            "Economic considerations (NPV, payback period)"
        ],
        primary_authority=[
            "SPE 177675 - Artificial Lift Selection Strategy",
            "Brown, K.E. - The Technology of Artificial Lift Methods",
            "Takacs, G. - Electrical Submersible Pumps Manual",
            "API RP 11L - Recommended Practice for Design Calculations for Sucker Rod Pumping Systems"
        ],
        burden_holder="Production engineer must justify lift system selection based on well characteristics and economic analysis",
        adversary_position="Cheaper system (e.g., rod pump) should be tried first before expensive ESP installation",
        counter_arguments=[
            "Rod pump may not reach target depth or rate, requiring early replacement with ESP",
            "Initial low capex can result in higher NPV loss due to deferred production",
            "Well deviation or dogleg severity may preclude rod pump mechanically",
            "High solids content may cause frequent ESP failures, favoring rod pump despite depth"
        ],
        resolution_strategy="Perform full lifecycle economic analysis (10-20 year) including intervention costs, uptime, and production profile to determine optimal NPV",
        entity_scope="Applicable to oil and gas wells requiring artificial lift across all basins and fluid types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard selection criteria with extensive field validation across global operations",
        controlling_precedent="API RP 11L and SPE best practices for artificial lift selection",
        category=IssueCategory.ARTIFICIAL_LIFT
    ),

    DoctrineBlock(
        topic="Gas Lift Optimization - Injection Rate and Valve Spacing",
        keywords=["gas lift", "injection rate", "valve spacing", "unloading", "gas lift curve", "GLR optimization"],
        conclusion_template=[
            "Optimal gas lift injection rate is found at the peak of the production rate vs. injection rate curve.",
            "Valve spacing must account for wellbore temperature/pressure gradient, valve port size, and unloading sequence.",
            "Over-injection wastes compression horsepower and can cause liquid fallback and instability."
        ],
        reasoning_framework="""
Gas Lift Performance Curve Analysis:
- Plot production rate (BOPD or BFPD) vs. gas injection rate (Mscf/d)
- Curve typically shows increasing production to a peak, then decline with over-injection
- Peak = optimal injection rate where incremental gas provides maximum lift efficiency
- Beyond peak: excessive injection causes liquid fallback, turbulence, heading

Valve Spacing Design Methodology:
1. Build wellbore pressure/temperature traverse (measured or nodal analysis)
2. Select unloading valve positions (typically 5-7 valves for 8,000-12,000 ft wells)
3. Design valve sequence from deepest (operating valve) upward
4. Operating valve: Set below fluid level for continuous injection
5. Unloading valves: Spaced to sequentially kill upper zones as FBHP declines
6. Typical spacing: 800-1,500 ft between valves (shallower wells = wider spacing)
7. Port sizing: Larger ports for operating valve (reduce friction), smaller for unloading

Injection Rate Optimization Process:
1. Start at low injection rate (e.g., 100 Mscf/d)
2. Incrementally increase injection in 50-100 Mscf/d steps
3. Stabilize well at each rate for 6-24 hours
4. Measure production rate, wellhead pressure, casing pressure
5. Plot production curve and identify peak
6. Set operating injection rate at peak or slightly below for stability
7. Monitor for changes in PI, reservoir pressure, or water cut (requires re-optimization)

Common Gas Lift Problems and Solutions:
- Heading/instability: Reduce injection rate, check valve spacing, install wireline retrievable valve
- Insufficient lift: Increase compression capacity, lower operating valve depth, check for valve leaks
- High casing pressure: Valve may be closed or undersized, check for port plugging
- Poor unloading: Verify unloading sequence, check valve charge pressures, consider nitrogen-charged valves

Advanced Optimization:
- Install downhole flow/pressure monitoring for real-time optimization
- Use automated gas lift controllers with casing pressure setpoints
- Implement field-wide gas allocation optimization (maximize field production under compression constraint)
- Consider intermittent gas lift for very low PI wells or gas-limited fields
        """,
        key_factors=[
            "Wellbore pressure and temperature gradient",
            "Available gas injection volume and pressure",
            "Reservoir PI and flowing bottomhole pressure",
            "Valve design (port size, charge pressure, depth)",
            "Production stability (avoid heading and slugging)",
            "Compression horsepower cost and availability"
        ],
        primary_authority=[
            "SPE 172390 - Gas Lift Optimization Under Facility Constraints",
            "Winkler, H.W. - Gas Lift Manual",
            "API RP 11V6 - Design of Continuous Flow Gas Lift Installations Using Injection Pressure Operated Valves",
            "Beggs, H.D. - Production Optimization Using Nodal Analysis"
        ],
        burden_holder="Production engineer must optimize injection rate to maximize production while minimizing compression costs",
        adversary_position="Higher injection rates always increase production, so inject as much gas as available",
        counter_arguments=[
            "Over-injection causes liquid fallback and actually reduces net production",
            "Excessive injection wastes compression horsepower that could lift other wells",
            "Instability from over-injection causes production variance and measurement errors",
            "Gas cycling through separator reduces sales gas and wastes fuel gas"
        ],
        resolution_strategy="Build production vs. injection curve through well testing, operate at peak of curve, periodically re-optimize as reservoir conditions change",
        entity_scope="Applicable to all gas lift wells, especially critical for fields with limited compression capacity",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established gas lift engineering principles with decades of field application",
        controlling_precedent="API RP 11V6 and nodal analysis best practices",
        category=IssueCategory.ARTIFICIAL_LIFT
    ),

    DoctrineBlock(
        topic="Rod Pump Optimization - Pump Speed and Stroke Length",
        keywords=["rod pump", "pump speed", "stroke length", "pump fillage", "dynamometer", "pump efficiency", "downhole card"],
        conclusion_template=[
            "Rod pump optimization balances pump speed and stroke length to maximize production while avoiding pump-off and mechanical failures.",
            "Dynamometer analysis reveals actual pump fillage, load conditions, and mechanical problems.",
            "Optimal pumping speed is typically 10-15 SPM for most wells; higher speeds risk rod/tubing wear and gas locking."
        ],
        reasoning_framework="""
Rod Pump Performance Analysis:
- Theoretical displacement = 0.1166 × plunger area (in²) × stroke length (in) × pump speed (SPM) × 1440 min/day ÷ 5.615 bbl/ft³
- Actual production = theoretical × pump fillage (% submergence and fluid entry efficiency)
- Pump efficiency = actual production ÷ theoretical displacement (typically 70-85% for good operation)

Dynamometer Card Interpretation:
1. Surface card: Measured at polished rod (load vs. position)
2. Downhole card: Calculated from surface card using wave equation
3. Ideal card: Smooth parallelogram indicating full fillage
4. Pump-off: Reduced load at bottom of stroke (pump hitting fluid level)
5. Gas interference: Irregular card shape, reduced fillage
6. Fluid pound: Sharp spike at bottom of stroke (traveling valve hitting standing valve)
7. Tubing movement: Elongated card showing tubing stretch
8. Worn plunger/barrel: Reduced load differential, low fillage despite submergence

Pumping Speed Optimization:
- Low speed (5-8 SPM): Maximizes fillage, good for low PI wells, reduces wear, higher torque requirements
- Medium speed (10-15 SPM): Optimal for most wells, balances production and equipment life
- High speed (16-20+ SPM): Suitable for high PI wells, shallow depth, risks gas locking and mechanical failures
- Considerations: PI, submergence, gas content, pump depth, rod string strength

Stroke Length Selection:
- Longer stroke: Increases displacement per stroke, reduces cycles/barrel (less wear), requires larger unit
- Shorter stroke: Lower peak loads, better for deep or heavy wells, more cycles for same production
- Common sizes: 64", 74", 86", 100", 120", 144", 168", 192", 216", 240", 300"
- Selection based on: Production target, well depth, rod/tubing size, prime mover size

Optimization Workflow:
1. Establish baseline with current pump speed and stroke length
2. Analyze dynamometer card for fillage, gas interference, mechanical issues
3. Measure fluid level to confirm submergence (acoustic survey, pressure gradient)
4. Calculate current pump efficiency
5. If pump-off: Reduce speed, increase fillage time
6. If gas locked: Reduce speed, install gas separator or pump-off controller
7. If under-pumped (high submergence): Increase speed or install larger pump
8. Monitor power consumption (ампerage, wattage) to detect increasing loads or failures

Advanced Optimization Tools:
- Pump-off controllers: Automatically adjust speed to maintain optimal fillage
- Variable speed drives (VSD): Smooth speed control, reduce starting loads
- Downhole pump cards: Real-time monitoring of plunger dynamics
- Rod/tubing anchors: Eliminate tubing movement, improve card quality
- Gas separators: Improve fillage in gassy wells
        """,
        key_factors=[
            "Well productivity index and reservoir pressure",
            "Fluid level and pump submergence",
            "Gas-oil ratio and gas interference",
            "Pump depth and rod string design",
            "Prime mover capacity and efficiency",
            "Rod/tubing wear rates and failure history"
        ],
        primary_authority=[
            "API RP 11L - Sucker Rod Pumping System Design",
            "Gibbs, S.G. - Predicting the Behavior of Sucker-Rod Pumping Systems",
            "SPE 177889 - Rod Pump Optimization Using Downhole Monitoring",
            "Takacs, G. - Sucker-Rod Pumping Handbook"
        ],
        burden_holder="Production engineer must optimize pump speed and stroke to maximize production without causing mechanical failures or excessive energy consumption",
        adversary_position="Run pump at maximum speed to get maximum production",
        counter_arguments=[
            "Excessive speed causes gas locking, reducing actual production despite higher theoretical displacement",
            "High speed increases rod and tubing wear, leading to frequent failures and downtime",
            "Pump-off conditions waste energy and create mechanical shock loads",
            "Optimal speed depends on well PI and may be much lower than unit maximum"
        ],
        resolution_strategy="Use dynamometer analysis and fluid level surveys to determine actual pump fillage, then adjust speed to maintain 80-95% fillage without pump-off",
        entity_scope="Applicable to all rod-pumped wells, especially critical for wells with gas interference or low PI",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard rod pump optimization methodology validated across thousands of wells globally",
        controlling_precedent="API RP 11L and dynamometer analysis best practices",
        category=IssueCategory.ARTIFICIAL_LIFT
    ),

    DoctrineBlock(
        topic="ESP Optimization - Frequency and Staging",
        keywords=["ESP", "VSD", "frequency", "staging", "pump curve", "best efficiency point", "BEP", "head requirement"],
        conclusion_template=[
            "ESP optimization requires operating near the best efficiency point (BEP) by matching pump stages and frequency to well head requirements.",
            "Variable speed drives (VSD) allow fine-tuning frequency to maximize efficiency and protect pump from off-design operation.",
            "Operating below 40 Hz or above 70 Hz reduces pump efficiency and risks premature failures."
        ],
        reasoning_framework="""
ESP Performance Fundamentals:
- Centrifugal pump performance: Head (ft) vs. Flow Rate (BPD) at fixed frequency
- Best Efficiency Point (BEP): Flow rate where pump operates at peak hydraulic efficiency (typically 75-85%)
- Staging: Multiple pump stages in series multiply total head (TDH = stage head × number of stages)
- Frequency control: Changing Hz shifts entire pump curve (affinity laws)

Affinity Laws for Frequency Changes:
- Flow: Q₂ = Q₁ × (f₂/f₁)
- Head: H₂ = H₁ × (f₂/f₁)²
- Power: P₂ = P₁ × (f₂/f₁)³
- Example: Reducing from 60 Hz to 50 Hz reduces flow to 83%, head to 69%, and power to 58%

Head Requirement Calculation:
1. Wellhead pressure: Typically 50-200 psi for separator/flowline
2. Friction losses: Tubing ID, production rate, fluid properties (multiphase flow correlations)
3. Hydrostatic head: Fluid density × TVD (subtract if flowing up, add if flowing down)
4. Total Dynamic Head (TDH) = Pwh + Pfriction + Phydrostatic - Pbottomhole
5. Add safety margin: 10-20% for operational flexibility

Pump Selection and Staging:
- Select pump series based on casing ID, desired flow rate, and fluid properties
- Common series: 400 (4" casing), 538 (5.5"), 562 (5.5" high rate), 675 (6.75"), etc.
- Calculate stages required: Stages = TDH (ft) ÷ Head per stage (from pump curve at design rate)
- Verify operating point is within 80-120% of BEP flow rate
- Check motor HP: BHP = (Flow × TDH × SG) ÷ (3960 × efficiency)

Frequency Optimization Strategy:
1. Install VSD for variable frequency control (45-70 Hz range typical)
2. Start ESP at reduced frequency (45-50 Hz) to avoid surge during startup
3. Gradually increase frequency to achieve target production rate
4. Monitor intake pressure (must stay above bubble point to avoid gas locking)
5. Monitor motor temperature and vibration (high frequency = higher heat and shaft stress)
6. Operate as close to BEP as possible for maximum efficiency
7. Avoid operation below 40 Hz (poor cooling, low efficiency) or above 70 Hz (shaft stress, vibration)

Common ESP Problems and Solutions:
- Gas locking: Install gas separator or gas handler, reduce frequency to lower intake drawdown
- High motor temperature: Reduce frequency, improve shroud cooling, check for high-resistivity water
- Low production: Check for scaling, corrosion, worn stages; verify intake pressure and no wellbore restrictions
- Frequent failures: Verify power quality (voltage imbalance <2%, THD <5%), check for solids production
- Downthrust: Operating too far right of BEP; reduce frequency or re-stage

Advanced Optimization:
- Install downhole monitoring (intake/discharge pressure, motor temperature, vibration)
- Use real-time surveillance to adjust frequency based on reservoir pressure decline
- Implement automated VSD control with setpoint logic (maintain target rate or intake pressure)
- Model remaining pump life based on operating hours off-BEP and intervention planning
        """,
        key_factors=[
            "Total dynamic head requirement (wellhead + friction + lift)",
            "Target production rate and well PI",
            "Pump curve and best efficiency point",
            "Intake pressure and gas avoidance",
            "Motor cooling and temperature limits",
            "Power quality and VSD capabilities"
        ],
        primary_authority=[
            "Takacs, G. - Electrical Submersible Pumps Manual",
            "SPE 184177 - ESP Optimization Using Real-Time Surveillance",
            "API Spec 11AX - Subsurface Sucker Rod Pumps and Fittings",
            "Centrilift (Baker Hughes) - ESP Best Practices Guide"
        ],
        burden_holder="Production engineer must select proper staging and operate at optimal frequency to maximize run life and production efficiency",
        adversary_position="Run ESP at maximum frequency to get maximum production regardless of efficiency",
        counter_arguments=[
            "Operating far from BEP dramatically reduces efficiency (can drop from 75% to 40%)",
            "High frequency operation increases shaft stress and vibration, causing premature failures",
            "Off-design operation causes upthrust or downthrust, wearing thrust bearings",
            "Gas locking at high drawdown stops production entirely, requiring costly workover"
        ],
        resolution_strategy="Use nodal analysis to calculate TDH, select staging to operate near BEP at design rate, use VSD to maintain optimal frequency as reservoir declines",
        entity_scope="Applicable to all ESP installations, critical for high-value or deepwater wells where intervention costs are high",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established ESP engineering principles from major service companies and decades of field experience",
        controlling_precedent="ESP manufacturer design guidelines and SPE best practices",
        category=IssueCategory.ARTIFICIAL_LIFT
    ),

    DoctrineBlock(
        topic="Wellbore Integrity Monitoring - Casing and Tubing Leaks",
        keywords=["casing leak", "tubing leak", "sustained casing pressure", "SCP", "annular pressure", "mechanical integrity", "leak detection"],
        conclusion_template=[
            "Sustained casing pressure (SCP) indicates potential loss of wellbore integrity from casing or tubing leaks or annular communication.",
            "Mechanical integrity testing (MIT) including pressure tests and diagnostic surveys is required to locate and quantify leaks.",
            "Wellbore integrity failures pose HSE risks and can result in regulatory shutdowns and costly workovers."
        ],
        reasoning_framework="""
Types of Wellbore Integrity Failures:
1. Tubing leak: Perforation, corrosion, connection failure, fish bite
2. Casing leak: Corrosion (internal or external), mechanical damage, cement failure
3. Packer failure: Seal element damage, setting failure, thermal cycling
4. Annular communication: Gas migration through cement, microannulus, channels
5. Wellhead seal failure: BOP/tree seal degradation

Sustained Casing Pressure (SCP) Diagnosis:
- Definition: Pressure in casing annulus that rebuilds after bleed-down
- Pressure buildup rate indicates severity (fast buildup = large leak or high-pressure source)
- Common in Gulf of Mexico (shallow water flow), offshore Canada, and aging wells globally
- Regulatory trigger: Typically >50 psi in A-annulus or any pressure in outer annuli

Diagnostic Methods:
1. Pressure testing:
   - Tubing pressure test: Pressure tubing, monitor annuli for pressure increase
   - Annulus pressure test: Pressure annulus, monitor for leak-off or communication
   - Step-rate test: Incrementally increase pressure to locate leak depth
2. Temperature surveys:
   - Identify leak location by temperature anomaly (Joule-Thomson cooling)
   - Run flowing and shut-in surveys to isolate leak zone
3. Noise/acoustic logging:
   - Detect fluid flow through leak using noise amplitude
   - Can pinpoint leak depth to within 10-50 ft
4. Radioactive tracer surveys:
   - Inject tracer in annulus, detect in production or other annuli
   - Confirms communication path
5. Casing inspection tools:
   - Multifinger caliper, electromagnetic inspection, ultrasonic imaging
   - Quantify metal loss, cracks, holes

Leak Severity Classification:
- Minor: <10 psi SCP, slow buildup (days), no HSE risk
- Moderate: 10-100 psi SCP, moderate buildup (hours), monitor and plan intervention
- Severe: >100 psi SCP, rapid buildup (minutes), immediate HSE risk, shut in well

Remedial Actions:
1. Tubing leak:
   - Pull and replace tubing (complete workover)
   - Run tubing patch (temporary fix, may not hold long-term)
   - Squeeze cement across leak (requires perforation location)
2. Casing leak:
   - Run casing patch (internal or external)
   - Cement squeeze (requires isolation and sufficient cement bond)
   - Drill out and set scab liner
3. Packer failure:
   - Pull and reset packer (workover rig)
   - Pump external casing pack-off (annular sealant)
4. Annular communication:
   - Remedial cementing (squeeze jobs at suspected channels)
   - Monitor and manage if no surface vent or HSE risk

Prevention and Monitoring:
- Corrosion monitoring: Inhibitor programs, coupons, UT surveys
- Pressure monitoring: Continuous annulus pressure monitoring systems
- Regular mechanical integrity tests: Annual or per regulatory schedule
- Design for corrosion: Corrosion-resistant alloys (CRAs) in high-risk zones
- Proper cementing: Centralization, mud conditioning, cement evaluation logs
        """,
        key_factors=[
            "Sustained casing pressure magnitude and buildup rate",
            "Annulus configuration (A, B, C annuli) and fluid content",
            "Well age, production history, and fluid corrosivity",
            "Regulatory requirements for mechanical integrity",
            "HSE risk (surface vent, nearby wells, environmental sensitivity)",
            "Economic impact of repair vs. abandonment"
        ],
        primary_authority=[
            "API RP 90 - Annular Casing Pressure Management",
            "SPE 90496 - Sustained Casing Pressure in Offshore Wells",
            "BSEE NTL 2010-N06 - Sustained Casing Pressure Requirements",
            "API RP 65 Part 2 - Isolating Potential Flow Zones During Well Construction"
        ],
        burden_holder="Operator must maintain wellbore integrity and demonstrate mechanical integrity through testing and monitoring",
        adversary_position="Minor SCP is common and harmless, no action needed unless HSE risk exists",
        counter_arguments=[
            "SCP can indicate deeper integrity issues that worsen over time",
            "Regulatory agencies may require shut-in or repair regardless of operator risk assessment",
            "Uncontrolled annular pressure can cause wellhead or casing failure",
            "Cross-flow between zones can damage reservoir or cause uncontrolled production"
        ],
        resolution_strategy="Implement continuous annulus pressure monitoring, perform diagnostic testing to locate leaks, classify severity, and execute timely repairs per API RP 90 guidelines",
        entity_scope="Applicable to all producing and shut-in wells, especially critical in offshore and high-pressure environments",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard practices codified in API RPs and regulatory requirements globally",
        controlling_precedent="API RP 90 and BSEE requirements for SCP management",
        category=IssueCategory.WELLBORE_INTEGRITY
    ),

    DoctrineBlock(
        topic="Scale Management - Calcium Carbonate, Barium Sulfate, and Iron Sulfide",
        keywords=["scale", "calcium carbonate", "barium sulfate", "barite", "iron sulfide", "scale inhibitor", "squeeze treatment", "scale prediction"],
        conclusion_template=[
            "Scale formation occurs when produced water becomes supersaturated due to pressure/temperature changes or water mixing.",
            "Scale prediction models identify scaling risk and inform inhibitor program design.",
            "Scale inhibitor squeeze treatments provide long-term protection (3-12 months) when properly designed and executed."
        ],
        reasoning_framework="""
Common Oilfield Scale Types:
1. Calcium Carbonate (CaCO₃):
   - Formation: Pressure drop releases CO₂, increases pH, CaCO₃ precipitates
   - Location: Perforations, tubing, surface equipment
   - Solubility: Decreases with increasing temperature (inverse solubility)
   - Treatment: Acid soluble (HCl), easily removed
2. Barium Sulfate (BaSO₄) / Strontium Sulfate (SrSO₄):
   - Formation: Seawater injection mixes incompatible waters (high Ba²⁺ meets high SO₄²⁻)
   - Location: Near-wellbore, perforations, water injection zones
   - Solubility: Very low, extremely hard scale
   - Treatment: NOT acid soluble, requires mechanical removal or specialty dissolvers (DTPA)
3. Iron Sulfide (FeS):
   - Formation: Corrosion products react with H₂S or bacteria (SRB)
   - Location: Tubing, flowlines, separators
   - Solubility: Acid soluble (HCl + oxygen scavenger to prevent H₂S release)
   - Treatment: Inhibit corrosion, biocide for SRB control
4. Calcium Sulfate (CaSO₄):
   - Formation: High-salinity brines, seawater mixing
   - Solubility: Decreases with increasing temperature
   - Treatment: Partially acid soluble, scale inhibitor effective

Scale Prediction Methodology:
1. Water analysis: Cations (Ca²⁺, Ba²⁺, Sr²⁺, Fe²⁺) and anions (CO₃²⁻, SO₄²⁻, HCO₃⁻)
2. Reservoir conditions: Pressure, temperature, pH, CO₂/H₂S content
3. Production profile: Water cut, commingling zones, injection water composition
4. Thermodynamic modeling: Software (ScaleChem, OLI, MultiScale) calculates saturation index
5. Saturation Index (SI): SI > 0 = supersaturated, scaling likely; SI < 0 = undersaturated, no scaling
6. Scale tendency: Predict scale type, location, and mass deposition rate

Scale Inhibitor Chemistry:
- Phosphonates (ATMP, HEDP, DTPMP): Broad spectrum, threshold effect, good for CaCO₃ and CaSO₄
- Polymeric inhibitors (polyacrylates, maleic polymers): Better for BaSO₄, higher thermal stability
- Sulfonates: Specialty for high-temperature or high-salinity applications
- Green inhibitors: Environmentally acceptable for offshore (low toxicity, biodegradable)

Scale Inhibitor Squeeze Treatment Design:
1. Pre-flush: Low-salinity water to condition formation (2-5 bbl/ft)
2. Inhibitor stage: Concentrated inhibitor (5-20% active) at 0.5-2 bbl/ft of pay
3. Overflush: Push inhibitor into formation beyond near-wellbore (5-10 bbl/ft)
4. Shut-in: Allow inhibitor to adsorb onto rock (12-48 hours)
5. Return to production: Monitor inhibitor concentration in produced water
6. Squeeze life: Depends on adsorption, water production rate, reservoir temperature (typically 3-12 months)

Squeeze Design Optimization:
- Adsorption modeling: Predict inhibitor retention and return profile
- Formation compatibility: Avoid precipitation with formation brine
- Placement: Matrix squeeze (no fracture) vs. fracture squeeze (better coverage, shorter life)
- Temperature stability: Select inhibitor with thermal stability >reservoir temperature
- Continuous injection: Alternative to batch squeezes for high water cut wells (inject at 10-50 ppm continuously)

Scale Removal Methods:
- Acid dissolution: HCl (15-28%) for carbonate scales, FeS
- Mechanical: Coiled tubing jetting, scraping, milling
- Specialty solvents: DTPA/EDTA converters for BaSO₄ (slow, expensive)
- Prevention: Always preferred over removal (lower cost, no production downtime)

Monitoring and Management:
- Routine water sampling: Check Ca²⁺, Ba²⁺, SO₄²⁻, inhibitor residual
- Inhibitor residual target: 2-10 ppm in produced water (below = re-squeeze needed)
- Scale coupon monitoring: Expose metal coupons in flowline, weigh scale deposition
- Pressure monitoring: Increasing tubing pressure or declining PI may indicate scaling
- Caliper logs: Measure tubing ID reduction from scale buildup
        """,
        key_factors=[
            "Water chemistry (cation/anion composition, TDS, pH)",
            "Pressure and temperature profile (wellbore and surface)",
            "Water cut and production rate",
            "Commingling of incompatible waters (reservoir vs. injection)",
            "Scale type and location (perforations, tubing, surface)",
            "Economics of prevention vs. removal"
        ],
        primary_authority=[
            "SPE 60221 - Scale Prediction and Management in Oil and Gas Production",
            "Jordan, M.M. - Predicting Carbonate Scale Formation",
            "NACE SP0194 - Application of Corrosion-Resistant Alloys in Oilfield Environments",
            "Crabtree, M. et al. - Fighting Scale: Removal and Prevention (Oilfield Review)"
        ],
        burden_holder="Operator must predict scale risk, design effective inhibitor programs, and monitor treatment performance to prevent scale-related production losses",
        adversary_position="Scale problems can be addressed reactively by acid treatments or mechanical removal when production declines",
        counter_arguments=[
            "Acid treatments cause formation damage and have short-lived benefit if scale reforms quickly",
            "Mechanical removal requires workover rig and production downtime (high NPV loss)",
            "BaSO₄ scale is nearly impossible to remove once formed",
            "Proactive inhibitor programs cost far less than reactive interventions"
        ],
        resolution_strategy="Use water chemistry and thermodynamic modeling to predict scale risk, implement preventive scale inhibitor squeeze program, monitor residual concentrations, and re-squeeze before depletion",
        entity_scope="Applicable to all producing wells with water production, especially critical for waterflood projects and high-water-cut wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard scale management practices with extensive field validation across global operations",
        controlling_precedent="SPE scale prediction methodology and service company best practices",
        category=IssueCategory.SCALE_MANAGEMENT
    ),

    DoctrineBlock(
        topic="Paraffin and Asphaltene Management",
        keywords=["paraffin", "wax", "asphaltene", "cloud point", "pour point", "wax deposition", "chemical treatment", "hot oiling"],
        conclusion_template=[
            "Paraffin deposition occurs when crude temperature drops below the cloud point, causing wax crystallization on tubing walls.",
            "Asphaltene precipitation is triggered by pressure drop, CO₂ injection, or acid stimulation, forming irreversible deposits.",
            "Prevention through chemical treatment or insulated tubing is far more cost-effective than mechanical removal."
        ],
        reasoning_framework="""
Paraffin (Wax) Deposition Mechanism:
- Crude oil contains dissolved paraffins (C₁₈-C₅₀ alkanes)
- Cloud point: Temperature where wax crystals first appear (typically 80-120°F)
- Pour point: Temperature where crude stops flowing (~10-20°F below cloud point)
- Wellbore cooling: Geothermal gradient causes temperature drop from reservoir to surface
- Deposition zone: Where wellbore temperature < cloud point (often 2,000-5,000 ft from surface)
- Deposit characteristics: White/brown waxy solid, reduces tubing ID, increases friction

Asphaltene Precipitation Mechanism:
- Asphaltenes: Large polar molecules suspended in crude oil by resins
- Precipitation triggers:
  1. Pressure drop below bubble point (gas evolution destabilizes asphaltenes)
  2. CO₂ injection (alters oil polarity)
  3. Acid contact (removes carbonate fines that stabilize asphaltenes)
  4. Light hydrocarbon mixing (reduces solvent power)
- Deposit characteristics: Black, hard, adhesive solid, can plug perforations and tubing

Paraffin Prevention and Treatment:
1. Chemical inhibitors:
   - Crystal modifiers: Prevent wax crystal growth and adhesion (EVA copolymers, acrylates)
   - Dispersants: Keep wax particles small and suspended
   - Application: Continuous injection (50-500 ppm) or batch treatments
   - Effectiveness: 50-80% reduction in deposition rate
2. Solvents:
   - Xylene, toluene, kerosene, condensate
   - Dissolve existing paraffin deposits
   - Application: Batch treatments (20-50 bbl) or continuous injection
3. Hot oiling:
   - Circulate heated oil (150-180°F) to melt paraffin
   - Requires kill string or coiled tubing
   - Temporary solution (wells re-wax in weeks to months)
4. Mechanical removal:
   - Scraping: Wireline scraper tools (24-48 hour intervention)
   - Coiled tubing jetting: High-pressure hot oil/solvent
5. Insulated tubing:
   - Vacuum-insulated tubing (VIT) maintains higher temperature
   - Reduces heat loss by 70-90%
   - High capex, best for severe wax problems or deepwater

Asphaltene Prevention and Treatment:
1. Chemical inhibitors:
   - Asphaltene dispersants: Peptize asphaltenes, prevent flocculation
   - Application: Continuous injection (100-1,000 ppm) or squeeze treatments
   - Screening: Lab testing required (asphaltene chemistry varies widely)
2. Solvents:
   - Aromatics (toluene, xylene) dissolve asphaltenes
   - Application: Batch soaks or continuous injection
   - More effective than for paraffin
3. Production management:
   - Avoid excessive drawdown (keep pressure above asphaltene onset pressure, AOP)
   - CO₂ floods: Pre-treat with asphaltene inhibitor before gas breakthrough
   - Acid jobs: Add asphaltene inhibitor to acid to prevent post-stimulation damage
4. Mechanical removal:
   - Very difficult (asphaltenes are hard and adhesive)
   - May require milling or tubing replacement

Monitoring and Diagnosis:
- Cold finger test: Measure wax deposition tendency in lab
- Cloud/pour point testing: Define critical temperatures
- Asphaltene onset pressure (AOP): PVT analysis or field testing
- Tubing caliper surveys: Measure ID reduction over time
- Pressure surveys: Increasing FBHP or wellhead pressure indicates restriction
- Production decline: Gradual rate loss despite constant reservoir pressure

Prevention Strategy (Economic Optimization):
1. Characterize crude: Cloud point, pour point, asphaltene content, AOP
2. Model wellbore temperature profile: Identify deposition zone
3. Select prevention method:
   - Low risk: Monitor only
   - Moderate risk: Continuous chemical injection
   - High risk: Insulated tubing + chemicals
   - Severe risk: Heating + insulated tubing + chemicals
4. Monitor effectiveness: Pressure surveys, caliper logs, production trend
5. Adjust program: Increase chemical concentration or frequency if deposition observed

Cost Comparison (Typical):
- Continuous chemical injection: $500-2,000/well/month
- Hot oil treatment: $10,000-20,000 per treatment (every 1-6 months)
- Scraping: $5,000-10,000 per scraper run (every 1-3 months)
- Coiled tubing cleanout: $50,000-150,000 per intervention
- Insulated tubing: $100,000-500,000 capex (amortized over well life)
        """,
        key_factors=[
            "Crude oil paraffin content and cloud/pour point",
            "Wellbore temperature profile and heat loss rate",
            "Asphaltene stability and onset pressure",
            "Production rate and pressure drawdown",
            "Economic comparison of prevention vs. remediation",
            "Well depth and accessibility for mechanical intervention"
        ],
        primary_authority=[
            "SPE 121335 - Paraffin Deposition and Treatment Strategy",
            "SPE 142506 - Asphaltene Management in Deepwater Gulf of Mexico",
            "Creek, J.L. - Asphaltene Deposition (JPT Article)",
            "Hammami, A. - Paraffin Deposition from Crude Oils: Comparison of Laboratory Results"
        ],
        burden_holder="Operator must implement cost-effective prevention program based on crude characterization and wellbore thermal modeling",
        adversary_position="Wait for production decline, then hot oil or scrape reactively as needed",
        counter_arguments=[
            "Reactive treatments cost 5-10x more than proactive chemical programs",
            "Each hot oil or scraping intervention loses 1-3 days of production (NPV impact)",
            "Severe paraffin plugs may require coiled tubing or workover rig",
            "Asphaltene damage can be permanent if severe precipitation occurs in perforations"
        ],
        resolution_strategy="Perform crude characterization and wellbore thermal analysis, implement continuous chemical injection program for wells with deposition risk, monitor effectiveness through pressure surveys",
        entity_scope="Applicable to waxy crude and asphaltenic oil production, especially critical in deepwater and arctic environments with high heat loss",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established practices for paraffin and asphaltene management based on extensive field data and service company expertise",
        controlling_precedent="SPE methodologies and major operator best practices",
        category=IssueCategory.PARAFFIN_ASPHALTENE
    ),

    DoctrineBlock(
        topic="Corrosion Monitoring and Inhibition Programs",
        keywords=["corrosion", "CO2 corrosion", "H2S corrosion", "corrosion inhibitor", "corrosion coupon", "UT survey", "metal loss"],
        conclusion_template=[
            "Corrosion monitoring using coupons, UT surveys, and fluid analysis is essential to detect metal loss before failures occur.",
            "Corrosion inhibitor programs must be tailored to fluid chemistry (CO₂, H₂S, water cut, temperature) and continuously monitored.",
            "Sweet (CO₂) and sour (H₂S) corrosion require different inhibitor chemistries and metallurgy considerations."
        ],
        reasoning_framework="""
Oilfield Corrosion Mechanisms:
1. Sweet corrosion (CO₂):
   - CO₂ dissolves in water → carbonic acid (H₂CO₃)
   - Attacks carbon steel: Fe + H₂CO₃ → FeCO₃ + H₂
   - Accelerated by: High CO₂ partial pressure, high temperature, high flow velocity
   - Protective film: FeCO₃ can form protective scale if conditions right (pH >5.5, T >140°F)
2. Sour corrosion (H₂S):
   - H₂S dissolves → hydrogen sulfide acid
   - Sulfide stress cracking (SSC): Hydrogen embrittlement of high-strength steels
   - Stress corrosion cracking (SCC): Crack propagation under stress
   - Accelerated by: High H₂S partial pressure, chlorides, low pH
3. Oxygen corrosion:
   - O₂ + Fe → iron oxide (rust)
   - Common in surface facilities, injection wells, workover fluids
   - Prevention: Oxygen scavengers, nitrogen blanketing
4. Microbiologically influenced corrosion (MIC):
   - Sulfate-reducing bacteria (SRB) produce H₂S
   - Acid-producing bacteria (APB) lower pH
   - Prevention: Biocides, filtration

Corrosion Rate Calculation:
- Corrosion rate (mils/year) = (534 × Weight Loss (mg)) / (Density (g/cm³) × Area (in²) × Time (hours))
- Carbon steel density: 7.86 g/cm³
- Acceptable rate: <2 mils/year (low), 2-5 mils/year (moderate), >5 mils/year (high, requires action)

Corrosion Monitoring Methods:
1. Weight-loss coupons:
   - Carbon steel coupons exposed in flowline or sidestream
   - Retrieved after 30-90 days, cleaned, weighed
   - Measures average corrosion rate
   - Cheap, simple, widely used
2. Electrical resistance (ER) probes:
   - Continuous monitoring of metal loss via resistance change
   - Real-time data, detects corrosion events immediately
   - More expensive than coupons
3. Linear polarization resistance (LPR):
   - Electrochemical technique, instantaneous corrosion rate
   - Affected by scale, flow conditions
4. Ultrasonic thickness (UT) surveys:
   - Measures remaining wall thickness of tubing, casing, flowlines
   - Detects pitting and general corrosion
   - Run annually or per integrity management plan
5. Hydrogen probes:
   - Measure atomic hydrogen permeation (indicator of SSC risk)
   - Used in sour service
6. Fluid analysis:
   - Monitor pH, dissolved O₂, CO₂, H₂S, bacteria counts, inhibitor residual
   - Adjust inhibitor program based on chemistry changes

Corrosion Inhibitor Chemistry:
1. Filming amines (imidazolines, quaternary amines):
   - Form hydrophobic barrier on metal surface
   - Effective for CO₂ corrosion
   - Require continuous injection (10-50 ppm)
   - Water-soluble or oil-soluble formulations
2. Phosphate esters:
   - Adsorb on metal, form protective layer
   - Good for high-temperature applications
3. Neutralizing amines:
   - Raise pH to reduce acidity
   - Used in conjunction with filming inhibitors
4. Oxygen scavengers:
   - Sodium bisulfite, ammonium bisulfite
   - React with dissolved O₂ to prevent oxidation
5. H₂S scavengers:
   - Triazine, glyoxal
   - React with H₂S to form non-corrosive products
   - Used in sour wells or gas gathering

Inhibitor Program Design:
1. Fluid characterization: CO₂, H₂S partial pressures, water cut, pH, temperature
2. Select inhibitor chemistry: Match to corrosion mechanism (sweet vs. sour)
3. Determine injection rate: Based on water production rate and target concentration (ppm)
4. Injection point: Downhole (squeeze or continuous), wellhead, or surface facilities
5. Monitor performance: Coupons, ER probes, UT surveys, inhibitor residual analysis
6. Adjust program: Increase concentration if corrosion rate exceeds target

Metallurgy Considerations:
- Carbon steel: Acceptable for sweet service if inhibited (CO₂ partial pressure <30 psi)
- Corrosion-resistant alloys (CRAs):
  - 13Cr: Moderate CO₂ resistance, no H₂S
  - Duplex stainless (22Cr, 25Cr): High CO₂, moderate H₂S
  - Super duplex, alloy 625, 825: Severe corrosion environments
- Sour service: NACE MR0175/ISO 15156 compliance (material hardness limits to prevent SSC)

Inhibitor Squeeze Treatments (Downhole):
- Similar to scale inhibitor squeezes
- Inhibitor adsorbs onto tubing/casing, slowly released
- Provides protection for 3-12 months
- Used when surface injection is impractical or insufficient

Economic Justification:
- Inhibitor program cost: $1,000-5,000/well/month
- Tubing replacement cost: $100,000-500,000 (workover rig + tubulars)
- Production downtime: 3-10 days (NPV loss)
- HSE risk: Tubing leak can cause environmental incident or safety hazard
        """,
        key_factors=[
            "CO₂ and H₂S partial pressures in produced fluids",
            "Water cut, pH, temperature, and flow velocity",
            "Metallurgy of tubing, casing, and surface equipment",
            "Historical corrosion rates and failure history",
            "Inhibitor chemistry and injection logistics",
            "Economics of prevention vs. replacement"
        ],
        primary_authority=[
            "NACE SP0775 - Preparation, Installation, Analysis, and Interpretation of Corrosion Coupons",
            "NACE MR0175/ISO 15156 - Materials for Use in H₂S-Containing Environments in Oil and Gas Production",
            "SPE 166468 - Corrosion Inhibitor Selection and Application in Oil and Gas Production",
            "API RP 571 - Damage Mechanisms Affecting Fixed Equipment in the Refining Industry"
        ],
        burden_holder="Operator must implement corrosion monitoring program, select appropriate inhibitor chemistry, and maintain inhibitor residuals to prevent tubular failures",
        adversary_position="Corrosion inhibitors are expensive and may not be needed if no failures have occurred",
        counter_arguments=[
            "Corrosion damage is cumulative and invisible until catastrophic failure occurs",
            "Tubular replacement costs far exceed inhibitor program costs",
            "HSE incidents from leaks can result in regulatory fines and shutdowns",
            "Monitoring data guides inhibitor optimization to minimize costs while ensuring protection"
        ],
        resolution_strategy="Establish baseline corrosion rates using coupons and UT surveys, design inhibitor program to maintain <2 mils/year corrosion rate, monitor continuously and adjust based on fluid chemistry changes",
        entity_scope="Applicable to all producing wells with CO₂, H₂S, or oxygen present in produced fluids, critical for high-value wells and sour service",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard corrosion management practices codified in NACE and API standards with global regulatory acceptance",
        controlling_precedent="NACE standards and major operator integrity management practices",
        category=IssueCategory.CORROSION_CONTROL
    ),

    DoctrineBlock(
        topic="Production Surveillance - Well Testing and Allocation",
        keywords=["well test", "allocation", "test separator", "multiphase meter", "production allocation", "mass balance", "reservoir monitoring"],
        conclusion_template=[
            "Accurate well testing is essential for reservoir management, regulatory compliance, and revenue allocation.",
            "Test separators provide the most accurate measurement of oil, gas, and water rates but require production downtime.",
            "Multiphase meters and virtual metering reduce testing frequency while maintaining allocation accuracy."
        ],
        reasoning_framework="""
Well Testing Objectives:
1. Reservoir management: Monitor well performance, decline curves, reservoir pressure
2. Regulatory compliance: Report production to state/federal agencies
3. Revenue allocation: Distribute production among working interest owners, royalty owners
4. Production optimization: Identify underperforming wells, guide intervention decisions
5. Facility planning: Size separators, compressors, pipelines based on actual rates

Well Test Methods:
1. Test separator:
   - Dedicated separator for single-well testing
   - Measures oil, gas, water rates independently
   - Gold standard for accuracy (±2-5% typical)
   - Requires: Routing well to test separator, stabilization time (4-24 hours)
   - Limitations: Production downtime for other wells, requires test header and separator
2. Multiphase flow meters:
   - Inline measurement without separation
   - Technologies: Venturi + gamma densitometry, microwave, ultrasonic, cross-correlation
   - Accuracy: ±5-15% depending on flow conditions and meter type
   - Advantages: Continuous monitoring, no production interruption
   - Disadvantages: High capex ($100K-500K), requires calibration against separator tests
3. Virtual metering (soft sensors):
   - Mathematical models estimate flow rates from pressure, temperature, choke position
   - Calibrated using periodic separator tests
   - Accuracy: ±10-20%
   - Advantages: No hardware, real-time estimates
   - Disadvantages: Model drift, requires frequent recalibration

Test Frequency and Duration:
- Regulatory: Monthly to quarterly depending on jurisdiction and well status
- Operational: Weekly to monthly for active wells, quarterly for shut-in or marginal wells
- Test duration: 4-24 hours to reach stabilized rates (longer for low-rate or gassy wells)
- Offshore/remote: Less frequent testing, rely more on allocation meters and multiphase meters

Production Allocation Methods:
1. Direct measurement: Each well tested individually, allocated actual measured rates
2. Proration: Group production measured at battery, allocated to wells based on test ratios
   - Example: Well A tested 100 bopd, Well B tested 150 bopd → Battery produces 500 bopd total → Allocate 200 bopd to A, 300 bopd to B
3. Mass balance: Use separator-level measurements and inlet/outlet flows to back-calculate individual wells
4. Advanced allocation: Combine multiphase meters, virtual meters, and periodic separator tests

Test Data Quality Assurance:
- Check for meter calibration: Verify against known standards (water draw, master meter)
- Confirm stabilization: Rates should be steady for ≥1 hour before recording test
- Detect meter malfunctions: Outliers, impossible values (e.g., water cut >100%)
- Material balance checks: Total production vs. sales, gas/oil ratio consistency
- Trending: Compare to previous tests, decline curve expectations

Key Performance Indicators (KPIs):
- Oil/gas/water rates (bopd, Mscf/d, bwpd)
- Gas-oil ratio (GOR, scf/bbl)
- Water cut (%, bwpd/bfpd)
- Flowing tubing pressure (FTP), flowing casing pressure (FCP)
- Choke size and differential pressure
- Reservoir pressure (from buildup tests or permanent gauges)

Advanced Surveillance Tools:
- Permanent downhole gauges (PDG): Continuous pressure/temperature monitoring
- Distributed temperature sensing (DTS): Fiber optic cables measure temperature profile
- Production logging tools (PLT): Identify zones contributing to production in multilayer wells
- Real-time SCADA systems: Collect and visualize data from all wells and facilities

Reservoir Monitoring Integration:
- Decline curve analysis: Identify well performance trends (exponential, hyperbolic, harmonic)
- Material balance: Estimate reserves, reservoir pressure, drive mechanism
- Pressure transient analysis: Well test interpretation for permeability, skin, boundaries
- Production forecasting: Predict future rates for economic modeling and facility planning

Common Issues and Solutions:
- Infrequent testing: Wells change (water breakthrough, GOR increase), old data misleads
  Solution: Increase test frequency or install multiphase meters
- Allocation errors: Proration based on stale tests misallocates production
  Solution: Virtual metering + monthly recalibration tests
- Meter drift: Multiphase meters lose calibration over time
  Solution: Quarterly separator tests to recalibrate models
- Commingled production: Cannot allocate to specific zones or wells
  Solution: Production logging or intelligent completions with zone isolation
        """,
        key_factors=[
            "Regulatory reporting requirements and frequency",
            "Number of wells and accessibility (onshore vs. offshore)",
            "Revenue sensitivity and allocation complexity (multiple owners)",
            "Capital budget for multiphase meters or virtual metering systems",
            "Reservoir management objectives (decline monitoring, waterflood surveillance)",
            "Operational constraints (test header capacity, separator availability)"
        ],
        primary_authority=[
            "SPE 184390 - Well Testing and Production Surveillance Best Practices",
            "API MPMS Chapter 20.1 - Allocation Measurement",
            "ISO 5167 - Measurement of Fluid Flow by Means of Pressure Differential Devices",
            "SPE 166140 - Virtual Flow Metering in Oil and Gas Production"
        ],
        burden_holder="Operator must implement cost-effective surveillance program to meet regulatory requirements and provide accurate data for reservoir management",
        adversary_position="Minimize testing frequency to reduce operational costs and production downtime",
        counter_arguments=[
            "Infrequent testing results in inaccurate allocation and potential revenue disputes",
            "Poor surveillance data impairs reservoir management and results in suboptimal production",
            "Regulatory non-compliance can result in fines and production shutdowns",
            "Multiphase meters and virtual metering reduce testing costs while maintaining accuracy"
        ],
        resolution_strategy="Implement risk-based testing frequency (high-value wells tested more often), deploy multiphase meters for continuous monitoring, use virtual meters to interpolate between tests, validate with monthly/quarterly separator tests",
        entity_scope="Applicable to all producing wells and fields, especially critical for fields with complex ownership or regulatory scrutiny",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard surveillance practices aligned with API allocation standards and regulatory requirements globally",
        controlling_precedent="API MPMS and state/federal regulatory reporting requirements",
        category=IssueCategory.PRODUCTION_SURVEILLANCE
    ),

    DoctrineBlock(
        topic="Well Intervention Planning - Workover vs. Stimulation vs. Recompletion",
        keywords=["workover", "stimulation", "recompletion", "acid stimulation", "hydraulic fracturing", "intervention economics", "NPV analysis"],
        conclusion_template=[
            "Well intervention decisions require economic analysis comparing incremental production, costs, and risks of workover, stimulation, or recompletion.",
            "Acid stimulation removes near-wellbore damage and is lower cost/risk than hydraulic fracturing or recompletion.",
            "Workover and recompletion interventions are justified when production upside exceeds NPV-adjusted costs including rig time and downtime."
        ],
        reasoning_framework="""
Intervention Decision Framework:
1. Diagnose production problem:
   - Reservoir depletion (natural decline)
   - Formation damage (skin, scale, fines migration)
   - Mechanical issues (tubing leak, packer failure, lift system failure)
   - Completion issues (plugged perforations, inadequate fracture conductivity)
2. Evaluate intervention options:
   - Do nothing (accept current production)
   - Optimize existing system (adjust lift, chemical treatments)
   - Stimulation (acid, fracture)
   - Workover (repair, re-perforate, isolate water)
   - Recompletion (new zone, horizontal re-entry, multilateral)
3. Economic screening:
   - Estimate incremental production (rate and duration)
   - Calculate intervention cost (services, rig time, downtime)
   - NPV analysis: Compare options at appropriate discount rate (10-15% typical)
   - Sensitivity analysis: Vary oil price, production response, costs

Acid Stimulation:
- Purpose: Remove near-wellbore damage (drilling mud, scale, fines, asphaltenes)
- Chemistry:
  - HCl (15-28%): Carbonate formations, dissolves CaCO₃, FeS
  - Mud acid (HCl/HF 12/3 or 13.5/1.5): Sandstone, dissolves clays and silicates
  - Organic acids (acetic, formic): High-temperature applications (>250°F)
- Typical job size: 50-500 gallons/ft of pay (carbonate), 25-100 gal/ft (sandstone)
- Cost: $20,000-100,000 depending on well depth, acid volume, additives
- Production response: 1.5-3x rate increase if skin damage is primary issue
- Duration: Months to years (until damage re-accumulates)
- Risks: Formation damage from precipitation, corrosion, asphaltene/paraffin mobilization

Hydraulic Fracturing (Re-fracs):
- Purpose: Bypass damage, increase contact area, improve conductivity in tight formations
- Application: Unconventional (shale, tight sand), restimulation of depleted conventional wells
- Job size: 100,000-10,000,000 lbs proppant, 50,000-500,000 bbl fluid (varies widely)
- Cost: $200,000-5,000,000 depending on complexity and formation
- Production response: 2-10x rate increase (highly variable based on formation quality)
- Duration: Years (fracture conductivity degrades over time from proppant crushing, fines migration)
- Risks: Screenouts, formation breakdown, water production, nearby well communication

Workovers:
- Purpose: Repair mechanical issues, re-perforate, isolate water/gas, convert to injection
- Common workover operations:
  1. Tubing/packer replacement (leak repair)
  2. Re-perforation (new zone or re-shoot existing zone)
  3. Zone isolation (cement squeeze, bridge plug)
  4. Casing repair (patches, liners)
  5. Artificial lift change (ESP to rod pump, gas lift installation)
- Cost: $100,000-1,000,000+ depending on depth, complexity, rig type
- Downtime: 3-20 days (high NPV cost for high-rate wells)
- Production response: Variable (restore lost production or access new reserves)
- Risks: Stuck pipe, lost circulation, well control, formation damage

Recompletions:
- Purpose: Access new reservoir, horizontal re-entry, sidetrack, multilateral
- Types:
  1. New zone: Plug back and perforate shallower/deeper interval
  2. Horizontal re-entry: Drill horizontal lateral from existing wellbore
  3. Sidetrack: Drill around obstruction or access bypassed pay
  4. Multilateral: Add additional lateral to existing well
- Cost: $500,000-5,000,000+ (includes drilling, completion, potential sidetrack)
- Production response: Can be equivalent to drilling new well if accessing significant reserves
- Risks: High cost, geological uncertainty, mechanical complexity

Economic Analysis Example:
- Current production: 50 bopd @ $70/bbl = $3,500/day = $1.28M/year
- Acid stimulation: Cost $50K, expect 100 bopd for 2 years → Incremental $1.28M/year × 2 years = $2.56M
- NPV @ 10%: ($2.56M / 1.1 + $1.28M / 1.1²) - $50K = $2.33M + $1.06M - $50K = $3.34M (HIGHLY PROFITABLE)
- Workover: Cost $300K, expect 150 bopd for 5 years → Incremental $2.56M/year × 5 years = $12.8M
- NPV @ 10%: Sum of discounted cash flows - $300K ≈ $9.7M - $300K = $9.4M (if production holds)

Decision Rules of Thumb:
- Acid stimulation: Low cost, low risk, try first if skin damage suspected
- Hydraulic fracturing: High cost, high risk, requires significant reserves and tight formation
- Workover: Justified for mechanical repairs or high-value production restoration
- Recompletion: Only if significant unproduced reserves accessible and well economics support drilling-level investment

Monitoring and Optimization:
- Post-intervention testing: Confirm production response matches expectations
- Decline curve analysis: Track response duration, plan future interventions
- Lessons learned: Document actual vs. predicted outcomes to improve future decisions
        """,
        key_factors=[
            "Diagnosis of production decline cause (damage vs. depletion vs. mechanical)",
            "Incremental production potential and duration",
            "Intervention cost (services, rig time, downtime)",
            "Risk of failure or complications",
            "NPV analysis at appropriate discount rate",
            "Alternative uses of capital (drill new well vs. intervene existing)"
        ],
        primary_authority=[
            "SPE 158145 - Well Intervention Economics and Decision Analysis",
            "Economides, M.J. - Petroleum Production Systems",
            "SPE 177675 - Matrix Acidizing Best Practices",
            "McGuire, W.J. - Economics of Well Stimulation"
        ],
        burden_holder="Production engineer must perform rigorous economic analysis and risk assessment to justify intervention expenditures",
        adversary_position="Intervene on any well showing production decline to maximize short-term production",
        counter_arguments=[
            "Interventions on naturally declining wells may not be economic if reserves are depleted",
            "High-cost interventions (workover, refrac) may have negative NPV despite production increase",
            "Capital may be better deployed drilling new wells with higher rate of return",
            "Some production declines are not addressable through intervention (reservoir depletion)"
        ],
        resolution_strategy="Perform diagnostic testing (PLT, pressure transient analysis, well logs) to confirm intervention target, model production response, calculate NPV at appropriate discount rate, select highest NPV option",
        entity_scope="Applicable to all producing wells experiencing decline or mechanical issues, critical for mature fields with high intervention costs",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Standard petroleum economics and intervention planning methodology used globally across all operators",
        controlling_precedent="SPE economic analysis best practices and operator-specific investment hurdle rates",
        category=IssueCategory.WELL_INTERVENTION
    ),

    DoctrineBlock(
        topic="Facility Optimization - Separator Pressure and Temperature",
        keywords=["separator", "three-phase separator", "separator pressure", "flash calculation", "GOR", "API gravity", "stock tank"],
        conclusion_template=[
            "Separator pressure and temperature directly impact oil shrinkage, GOR, and stock tank API gravity through flash vaporization.",
            "Multi-stage separation (2-3 stages) maximizes liquid recovery compared to single-stage separation by reducing pressure incrementally.",
            "Optimal separator pressure balances liquid recovery, compression requirements, and sales specifications."
        ],
        reasoning_framework="""
Separator Function and Design:
- Separates wellstream into oil, gas, and water phases using gravity and residence time
- Operates at pressure below wellhead pressure but above stock tank pressure
- Temperature: Typically ambient to 100°F (no heating unless cold climate or high wax content)
- Residence time: 1-3 minutes for gas, 10-30 minutes for liquid (allows settling)

Phase Separation Mechanism:
1. Primary separation: Inlet momentum change, impingement baffles knock out large droplets
2. Secondary separation: Gravity settling (gas rises, liquid falls)
3. Mist elimination: Vane packs or mesh pads remove entrained liquid droplets from gas
4. Liquid retention: Liquid level control dumps oil/water to downstream equipment

Multi-Stage Separation Benefits:
- Reduces pressure in steps (e.g., 500 psi → 100 psi → 15 psi → 0 psig)
- At each stage, lighter components flash to gas phase
- More stages = less shrinkage = more stock tank liquid recovery
- Diminishing returns: 2-3 stages optimal (3rd stage adds <2% improvement)

Flash Calculation Fundamentals:
- Wellstream composition: C₁, C₂, C₃, C₄, C₅, C₆+ (defined by PVT analysis)
- At each separator stage: Pressure and temperature define vapor-liquid equilibrium
- K-values (equilibrium ratios): Ki = yi / xi (vapor mole fraction / liquid mole fraction)
- Flash calculation: Solve for vapor fraction (V) and compositions
- Oil shrinkage: Ratio of stock tank volume to separator volume (typically 0.75-0.95)

Separator Pressure Optimization:
- High pressure separator (HPS): 500-1,200 psi
  - Pros: Minimizes wellhead backpressure (maximizes production)
  - Cons: More gas flashes at stock tank (higher shrinkage), higher compression costs
- Low pressure separator (LPS): 50-150 psi
  - Pros: Less shrinkage (more components stay in liquid), lower API gravity
  - Cons: Higher wellhead backpressure (may reduce production)
- Optimal pressure: Depends on:
  1. Wellstream GOR and composition
  2. Wellhead flowing pressure (must be >separator pressure + pressure drop)
  3. Gas sales pressure (compression requirements)
  4. Stock tank API gravity specifications (light oil commands premium)

Typical Separator Configuration:
- Single-stage: Wellhead → 100 psi separator → stock tank (simple, low cost, high shrinkage)
- Two-stage: Wellhead → 500 psi HPS → 50 psi LPS → stock tank (industry standard)
- Three-stage: Wellhead → 800 psi HPS → 200 psi MPS → 25 psi LPS → stock tank (offshore, high shrinkage wells)

Stock Tank API Gravity Impact:
- Light ends (C₁-C₄) flash at separator → Stock tank oil is heavier (lower API)
- Higher separator pressure → More light ends flash → Heavier stock tank oil
- Example: 500 psi separator may yield 38° API, 100 psi separator may yield 42° API
- API gravity affects pricing: Light oil (>35° API) commands premium over heavy oil (<25° API)

Compression Considerations:
- Gas from separator must be compressed for sales or injection
- Higher separator pressure = lower compression ratio = lower compression cost
- Trade-off: Separator pressure that maximizes (liquid recovery × oil price - compression cost)

Separator Design Parameters:
- Diameter and length: Based on gas capacity (К-factor, settling velocity)
- Liquid retention: Volume between high and low liquid level alarms (hold time)
- Pressure vessel design: ASME Section VIII, API 12J
- Level control: Float, displacer, or differential pressure transmitter
- Pressure control: Back-pressure valve on gas outlet

Advanced Separator Technologies:
- Compact separators: Cyclonic inlets, high-efficiency internals (smaller footprint for offshore)
- Degasser: Rotating drum or vacuum to remove dissolved gas from oil (reduces stock tank flashing)
- Electrostatic coalescer: Electrical field enhances water-oil separation (tight emulsions)

Monitoring and Troubleshooting:
- Liquid level: High level = liquid carryover in gas, Low level = gas carryover in liquid
- Pressure: Increasing pressure may indicate downstream restriction or control valve failure
- Temperature: Cold temperature can cause hydrate formation in gas (requires glycol injection)
- Oil in gas: Check mist eliminator, reduce gas velocity, increase retention time
- Water in oil: Emulsion issues, increase retention time, add demulsifier chemical, consider heater-treater
        """,
        key_factors=[
            "Wellstream GOR and composition (PVT analysis)",
            "Wellhead flowing pressure and deliverability",
            "Gas sales pressure and compression costs",
            "Oil pricing differentials for API gravity",
            "Separator stages and pressure profile",
            "Liquid handling capacity and retention time"
        ],
        primary_authority=[
            "SPE 170683 - Optimization of Separator Pressure for Maximum Oil Recovery",
            "API Spec 12J - Specification for Oil and Gas Separators",
            "Arnold, K. - Surface Production Operations Vol 1: Design of Oil-Handling Systems",
            "McCain, W.D. - The Properties of Petroleum Fluids"
        ],
        burden_holder="Facility engineer must optimize separator pressure to maximize liquid recovery and oil value while meeting gas sales requirements",
        adversary_position="Operate separator at minimum pressure to maximize wellhead production regardless of shrinkage",
        counter_arguments=[
            "Excessive shrinkage from low separator pressure can lose 5-15% of oil volume",
            "Lost oil volume may exceed production gain from lower backpressure",
            "Stock tank API gravity impacts oil price, affecting total revenue",
            "Multi-stage separation requires higher capex but improves economics for high-GOR wells"
        ],
        resolution_strategy="Perform flash calculations at multiple separator pressures, calculate liquid recovery and API gravity at each stage, optimize for maximum revenue (oil volume × price - compression cost)",
        entity_scope="Applicable to all oil and gas production facilities, especially critical for high-GOR wells and facilities with compression constraints",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established thermodynamic principles and industry design standards with global application",
        controlling_precedent="API separator design standards and major operator facility design practices",
        category=IssueCategory.FACILITY_OPTIMIZATION
    ),

    DoctrineBlock(
        topic="Gas Gathering System Optimization - Compression and Pipeline Sizing",
        keywords=["gas gathering", "compression", "pipeline", "pressure drop", "Weymouth equation", "compressor", "horsepower"],
        conclusion_template=[
            "Gas gathering system capacity is limited by pipeline pressure drop and compressor horsepower.",
            "Pipeline sizing using Weymouth or Panhandle equations determines maximum throughput for given inlet/outlet pressures.",
            "Compression optimization balances number of stages, compression ratio, and horsepower to minimize fuel gas consumption and maximize throughput."
        ],
        reasoning_framework="""
Gas Gathering System Components:
1. Wellhead: Initial gas pressure (reservoir pressure minus drawdown)
2. Gathering lines: Small diameter (2"-6") flowlines from wells to manifold
3. Trunk lines: Larger diameter (6"-24") pipelines from manifold to processing plant
4. Compression: Boost pressure to overcome pipeline friction and meet sales pressure
5. Processing: Dehydration, NGL extraction, sweetening (if sour gas)

Pipeline Pressure Drop Fundamentals:
- Driving force: Pressure differential between inlet and outlet
- Opposing force: Friction between gas and pipe wall
- Pressure drop increases with: Flow rate, gas viscosity, pipeline length, pipe roughness
- Pressure drop decreases with: Pipe diameter, gas density (heavier gas = less friction)

Weymouth Equation (Typical for gathering lines):
Q = C × (Tb/Pb) × [(P₁² - P₂²) × D⁵ / (G × T × L × Z)]^0.5
Where:
- Q = Gas flow rate (Mscf/d)
- C = Constant (depending on units, typically 433.5 for U.S. customary units)
- P₁, P₂ = Inlet and outlet pressures (psia)
- D = Inside diameter (inches)
- G = Gas specific gravity (air = 1.0)
- T = Average temperature (°R)
- L = Pipeline length (miles)
- Z = Compressibility factor (typically 0.85-0.95 for gas)

Pipeline Sizing Strategy:
- Design criterion: Select diameter to limit pressure drop to 10-20% of inlet pressure
- Example: 1,000 psi inlet, allow 100-200 psi drop, 800-900 psi outlet
- Larger diameter: Lower pressure drop, higher throughput, higher capex
- Smaller diameter: Higher pressure drop, limited throughput, lower capex
- Optimize: NPV of incremental revenue vs. pipe material cost over field life

Compression Fundamentals:
- Purpose: Raise pressure to overcome gathering system pressure drop and meet sales pressure
- Compression ratio (r): Discharge pressure / suction pressure
- Typical ratios: 1.5-4.0 per stage (higher ratios reduce efficiency and increase temperature)
- Multi-stage compression: For high total compression ratios (e.g., 100 psi to 1,000 psi = 10:1, use 3 stages @ 2.15:1 each)

Compressor Horsepower Calculation:
BHP = (Q × Δh) / (6,350 × η)
Where:
- BHP = Brake horsepower
- Q = Gas flow rate (MMscf/d)
- Δh = Enthalpy rise (Btu/lb, from compression ratio and gas properties)
- η = Compressor efficiency (typically 0.70-0.85)

Simplified horsepower (for rough estimates):
BHP ≈ (Q × P₁ × r^0.286 - 1) / (229 × η)
Where r = compression ratio

Fuel Gas Consumption:
- Compressors consume 3-8% of throughput as fuel gas (depends on efficiency and compression ratio)
- Fuel cost is significant operating expense
- Optimization: Minimize compression ratio by maximizing separator pressure and gathering line diameter

Compression Station Design:
- Reciprocating compressors: Best for low flow (<50 MMscf/d), high pressure ratios, good turndown
- Centrifugal compressors: Best for high flow (>50 MMscf/d), lower pressure ratios, smooth operation
- Screw compressors: Medium flow, simple, low maintenance
- Stations typically have 2-4 units for redundancy and turndown

Gathering System Optimization Workflow:
1. Map well locations and production rates (current and forecast)
2. Design pipeline network: Minimize total length, avoid steep grades, consider rights-of-way
3. Calculate pressure drop for each line segment using Weymouth/Panhandle
4. Size lines to limit pressure drop to design criterion
5. Determine required compression (suction pressure, discharge pressure, flow rate)
6. Select compressor configuration (stages, drivers)
7. Economic analysis: Capex (pipe, compression) vs. NPV of production over field life

Common Bottlenecks and Solutions:
- Insufficient line capacity: Parallel additional line, replace with larger diameter, add compression
- Compressor limit: Add another compressor unit, upgrade drivers, increase pressure ratio (if safe)
- Hydrate formation: Install heater, inject glycol, insulate lines
- Liquid loading: Install drips/separators, increase velocity, add glycol dehydration

Advanced Optimization:
- Automated compressor control: Adjust speed/recycle to match changing production rates
- Pipeline network simulation: Model entire gathering system to optimize pressures at all nodes
- Dynamic optimization: Re-optimize as wells decline and new wells come online
        """,
        key_factors=[
            "Well locations, production rates, and reservoir pressures",
            "Sales gas delivery pressure requirement",
            "Pipeline length, diameter, elevation profile",
            "Gas properties (specific gravity, viscosity, compressibility)",
            "Compression technology and efficiency",
            "Fuel gas cost and environmental constraints"
        ],
        primary_authority=[
            "API RP 14E - Design and Installation of Offshore Production Platform Piping Systems",
            "GPSA Engineering Data Book - Gas Processors Suppliers Association",
            "SPE 180084 - Gas Gathering System Optimization",
            "Menon, E.S. - Gas Pipeline Hydraulics"
        ],
        burden_holder="Facility engineer must design gathering system to handle current and future production while minimizing capex and opex",
        adversary_position="Undersize pipelines and compression to minimize upfront capex",
        counter_arguments=[
            "Undersized systems bottleneck production, losing revenue that far exceeds capex savings",
            "Adding compression or replacing lines later is far more expensive than sizing correctly initially",
            "Production forecasts may be conservative; oversizing provides operational flexibility",
            "Pipeline pressure drop increases with production rate squared (flow² relationship)"
        ],
        resolution_strategy="Use production forecasts to size gathering system for plateau production plus 10-20% margin, perform NPV analysis comparing capex vs. revenue over field life, consider modular expansion (install oversized pipes, add compression as needed)",
        entity_scope="Applicable to all gas gathering systems from single wells to large field-wide networks, critical for unconventional plays with hundreds of wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established pipeline hydraulics and compression engineering principles with decades of field validation",
        controlling_precedent="API RP 14E and GPSA design standards",
        category=IssueCategory.GAS_GATHERING
    ),

    DoctrineBlock(
        topic="Produced Water Handling - Separation, Treatment, and Disposal",
        keywords=["produced water", "free water knockout", "FWKO", "heater-treater", "oil-water separation", "water disposal", "SWD", "API separator"],
        conclusion_template=[
            "Produced water must be separated from oil to meet sales specifications (<0.5% BS&W typical) and treated to meet disposal regulations.",
            "Free water knockouts (FWKO), heater-treaters, and chemical treatments are used to break emulsions and separate oil and water.",
            "Disposal options include saltwater disposal wells (SWD), beneficial reuse, or treatment for surface discharge (rare in oilfield)."
        ],
        reasoning_framework="""
Produced Water Characteristics:
- Total dissolved solids (TDS): 10,000-300,000+ mg/L (seawater = 35,000 mg/L)
- Oil content: 100-10,000+ ppm as produced (must reduce to <100 ppm for disposal in most jurisdictions)
- Suspended solids: Formation fines, scale, corrosion products
- Chemical additives: Corrosion inhibitors, scale inhibitors, demulsifiers
- pH: Typically 5.5-7.5 (can be acidic from CO₂ or basic from injection chemicals)

Oil-Water Emulsion Formation:
- Emulsions: Water droplets dispersed in oil (W/O) or oil droplets in water (O/W)
- Stabilized by: Asphaltenes, resins, fine solids, natural surfactants in crude
- Formation causes: Shear in pumps/chokes, pressure drop, chemical mixing
- Emulsion stability: Increases with mixing intensity, droplet size reduction, stabilizer concentration

Separation Technologies:
1. Free Water Knockout (FWKO):
   - Horizontal or vertical pressure vessel, large diameter for low velocity
   - Residence time: 10-30 minutes (allows gravity settling)
   - Removes "free water" (easily separated, large droplets >100 microns)
   - Does NOT break emulsions (requires chemical or heat)
   - Typical separation: 80-95% of water content
2. Heater-Treater:
   - Indirect-fired heater + electrostatic coalescer
   - Heat reduces oil viscosity and destabilizes emulsion (120-150°F typical)
   - Electrostatic field polarizes water droplets, causing coalescence
   - Achieves <0.5% BS&W for pipeline sales specifications
   - Capex/opex higher than FWKO, but superior water removal
3. Hydrocyclones:
   - Centrifugal separation in cone-shaped chamber
   - Compact, no moving parts, good for offshore
   - Effective for free water, less effective for tight emulsions
4. Centrifuges:
   - High-speed rotating bowl, very high G-forces
   - Can break tight emulsions, expensive, high maintenance
   - Used for difficult separations or high-value production

Chemical Demulsifiers:
- Function: Neutralize emulsion stabilizers (asphaltenes, resins), promote droplet coalescence
- Chemistry: Polyglycols, polyamines, sulfonates, resins
- Application: Inject at wellhead (10-100 ppm) or at separator
- Selection: Lab bottle tests with actual crude and water samples
- Optimization: Adjust dosage to minimize oil in water and water in oil

Water Treatment for Disposal:
- Primary treatment: FWKO or API separator (removes free oil)
- Secondary treatment: Induced gas flotation (IGF), dissolved gas flotation (DGF)
  - Gas bubbles attach to oil droplets, float to surface for skimming
  - Achieves <50 ppm oil in water
- Tertiary treatment: Filtration (walnut shell, multimedia), hydrocyclones
  - Polishing step to meet stringent discharge limits (<10-29 ppm oil)
- Chemical treatment: Coagulants, flocculants to aggregate fine oil droplets

Disposal Methods:
1. Saltwater Disposal (SWD) Wells:
   - Inject into deep disposal formations (below drinking water aquifers)
   - Regulatory permit required (UIC Class II in U.S.)
   - Injection pressure limited by formation fracture pressure
   - Typical depths: 2,000-10,000 ft
   - Cost: $0.50-3.00/bbl (includes pumping, maintenance, monitoring)
2. Beneficial Reuse:
   - Reuse for hydraulic fracturing, drilling, or enhanced oil recovery
   - Requires treatment to remove solids, bacteria, and reduce salinity if needed
   - Growing trend in water-scarce regions (Permian, DJ Basin)
3. Surface Discharge:
   - Very rare in oil and gas (requires extensive treatment to meet EPA limits)
   - Offshore: Treated water can be discharged (offshore regulations, e.g., <29 ppm oil NPDES)
   - Onshore: Typically prohibited or requires advanced treatment (reverse osmosis, evaporation)

Regulatory Considerations:
- U.S. EPA Underground Injection Control (UIC) program: Regulates SWD wells
- State regulations: Vary widely (Texas RRC, NDIC, COGCC, etc.)
- Produced water volume reporting: Monthly reports to regulatory agencies
- Seismicity concerns: Injection-induced earthquakes in some areas (Oklahoma, Kansas) → volume/pressure limits
- Beneficial reuse regulations: Emerging frameworks in most states

System Design Considerations:
- Peak water handling capacity: Size equipment for maximum anticipated water production (e.g., 90% water cut at end of field life)
- Redundancy: Install 2-3 separators/treaters to handle peak + allow maintenance
- Modular design: Add capacity as water cut increases
- Monitoring: Automated BS&W analyzers, oil-in-water monitors, flow meters
- CAPEX estimation: FWKO $50K-300K, heater-treater $200K-1M+, SWD well $500K-2M+

Water Cut Impact on Economics:
- High water cut (>90%) is common in mature fields
- Lifting costs increase with water volume (pumping, treating, disposal)
- May justify well interventions to shut off water zones (cement squeezes, mechanical isolation)
- Economic limit: Production rate where revenue = opex (lifting + disposal costs)
        """,
        key_factors=[
            "Produced water volume and water cut trend",
            "Oil-water emulsion stability and API gravity",
            "Sales specifications for BS&W content",
            "Disposal regulations and available disposal capacity",
            "Water handling and disposal costs",
            "Beneficial reuse opportunities"
        ],
        primary_authority=[
            "API Spec 12J - Oil and Gas Separators",
            "EPA UIC Program Regulations - 40 CFR Part 144-148",
            "SPE 179942 - Produced Water Management and Beneficial Reuse",
            "Arnold, K. - Surface Production Operations Vol 1: Oil and Water Separation"
        ],
        burden_holder="Operator must design water handling system to meet sales specifications and disposal regulations while minimizing costs",
        adversary_position="Minimize water treatment capex by designing only for current water cut, expand later if needed",
        counter_arguments=[
            "Water cut typically increases rapidly in mature fields, requiring frequent expansions",
            "Undersized water handling creates production bottleneck and offspec crude shipments",
            "Retrofitting water handling equipment is far more expensive than initial oversizing",
            "Disposal capacity may not be available when needed (SWD wells take 6-18 months to permit and drill)"
        ],
        resolution_strategy="Design water handling system for forecast peak water production (90-95% water cut), install modular equipment that can be expanded, secure disposal capacity early (SWD permits or beneficial reuse offtake agreements)",
        entity_scope="Applicable to all oil production with water cut >10%, critical for mature waterflood projects and unconventional wells with high water production",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard water handling and disposal practices based on API standards and decades of operational experience",
        controlling_precedent="API separator standards and EPA UIC regulations",
        category=IssueCategory.WATER_HANDLING
    ),

    DoctrineBlock(
        topic="ESG Metrics in Production Operations - Emissions, Water, and Community Impact",
        keywords=["ESG", "emissions", "methane", "flaring", "water management", "carbon intensity", "scope 1 emissions", "sustainability"],
        conclusion_template=[
            "ESG metrics are increasingly important for investor relations, regulatory compliance, and social license to operate.",
            "Scope 1 emissions (direct operational emissions) include flaring, venting, combustion, and fugitive methane leaks.",
            "Operators can reduce emissions through flare minimization, leak detection and repair (LDAR), electrification, and carbon capture."
        ],
        reasoning_framework="""
ESG Framework for Oil and Gas:
- Environmental: Emissions (GHG, methane), water use, spills, habitat impact
- Social: Community engagement, indigenous rights, workforce safety, local hiring
- Governance: Board oversight, executive compensation, transparency, anti-corruption

Scope 1, 2, 3 Emissions:
- Scope 1: Direct emissions from operations (flaring, venting, combustion, fugitives)
- Scope 2: Indirect emissions from purchased electricity/heat
- Scope 3: Value chain emissions (midstream transport, refining, end-user combustion)
- Oil and gas focus: Primarily Scope 1 (operators control these directly)

Methane Emissions Sources:
1. Venting:
   - Pneumatic devices (controllers, chemical pumps) use natural gas, vent to atmosphere
   - Tank vapor losses (flash gas from oil tanks)
   - Compressor seal leaks, blowdowns
2. Flaring:
   - Flaring converts methane to CO₂ (lower global warming potential, but still emissions)
   - Reasons: No gas sales infrastructure, safety (pressure relief), startup/shutdown
   - Efficiency: 95-98% combustion (ideal), lower if poor combustion (black smoke)
3. Fugitive leaks:
   - Valves, flanges, connectors, pump seals
   - Equipment degradation over time
   - Can be significant (0.1-2% of production in poorly maintained facilities)

Methane Intensity Calculation:
- Methane intensity = Methane emissions (Mscf) / Natural gas production (Mscf) × 100%
- Industry average: 0.2-1.0% (varies widely by operator and basin)
- Leading operators target: <0.1% (through aggressive LDAR programs)

Flare Reduction Strategies:
1. Gas capture and sales:
   - Build gathering infrastructure to monetize gas instead of flaring
   - Economic: Gas price must justify pipeline/compression capex
2. Vapor recovery units (VRU):
   - Compress tank vapors, route to sales or use as fuel gas
   - Typical installation: $100K-500K, payback <2 years if gas >$3/Mscf
3. Flare minimization:
   - Route to combustion (heaters, generators) instead of open flare
   - Use nitrogen for well unloading instead of natural gas
4. Regulation:
   - Many jurisdictions now limit routine flaring (North Dakota, Colorado, Canada)
   - Require permits for flaring beyond startup periods

Leak Detection and Repair (LDAR) Programs:
- Regulatory driver: EPA Quad Oa, NSPS OOOOa, state regulations (Colorado, Pennsylvania)
- Technologies:
  1. Optical Gas Imaging (OGI): Infrared cameras visualize methane plumes
  2. Continuous monitoring: Fixed sensors at facilities, real-time alerts
  3. Aerial surveys: Drones, aircraft, satellites (MethaneSAT)
- Frequency: Quarterly to annual surveys depending on regulation and facility size
- Repair: Tag leaking components, repair within 15-30 days (regulatory requirement)
- Cost-effectiveness: LDAR payback <1 year if gas price >$2/Mscf (captured leaks = revenue)

Electrification:
- Replace gas engines/turbines with electric motors powered by grid
- Benefits: Eliminates combustion emissions, lower maintenance, quieter
- Challenges: Grid availability (remote locations), electricity cost, reliability
- Applications: Compressors, pumps, drilling rigs (e-frac fleets)

Carbon Capture and Storage (CCS):
- Capture CO₂ from combustion or processing, inject into deep formations
- Limited application in upstream (more common in gas processing, LNG)
- Economics: Requires high carbon price or 45Q tax credits ($50-85/ton CO₂)

Water Stewardship:
- Produced water volume and disposal method (SWD vs. beneficial reuse)
- Freshwater use for drilling, hydraulic fracturing (shift to recycled produced water)
- Spill prevention and response (leak detection, secondary containment)

Community and Social Metrics:
- Local employment and contracting (% local hires, local supplier spend)
- Community investment (schools, infrastructure, health clinics)
- Indigenous consultation and free prior informed consent (FPIC)
- Accident rates (total recordable incident rate, TRIR)

Governance and Transparency:
- ESG reporting: Annual sustainability reports (GRI, SASB, TCFD frameworks)
- Board oversight: ESG committee, executive compensation tied to ESG targets
- Third-party verification: Certify emissions data, validate LDAR programs
- Transparency: Disclose hydraulic fracturing chemicals, emissions data, water use

Emerging ESG Regulations:
- SEC Climate Disclosure Rule: Require publicly traded companies to disclose Scope 1/2/3 emissions
- Methane fee (Inflation Reduction Act): $900-1,500/ton for methane emissions above threshold
- Flaring limits: North Dakota, Colorado, Canada restrict routine flaring
- ESG ratings impact: Influence investor decisions, cost of capital

Operator ESG Performance Tiers:
- Leaders: <0.1% methane intensity, zero routine flaring, >80% produced water reuse, transparent reporting
- Industry average: 0.2-0.5% methane intensity, minimal flaring, some produced water reuse
- Laggards: >1% methane intensity, routine flaring, SWD only, limited transparency

Economic Impact of ESG:
- Access to capital: ESG leaders receive better terms from banks, attract ESG-focused investors
- Social license: Community opposition can delay or block projects
- Regulatory risk: Poor ESG performance attracts regulatory scrutiny and fines
- Operational efficiency: Methane capture = revenue, electrification = lower fuel costs
        """,
        key_factors=[
            "Regulatory requirements for emissions reporting and limits",
            "Methane intensity and flaring volumes",
            "Water use and disposal practices",
            "Community engagement and social license",
            "Investor and lender ESG requirements",
            "Cost-benefit of emissions reduction technologies"
        ],
        primary_authority=[
            "EPA Greenhouse Gas Reporting Program (40 CFR Part 98)",
            "EPA Quad Oa and NSPS OOOOa (methane regulations)",
            "IPIECA - Oil and Gas Industry Guidance on Voluntary Sustainability Reporting",
            "SASB Oil & Gas Exploration & Production Standard",
            "SPE 199893 - ESG Metrics and Benchmarking in E&P Operations"
        ],
        burden_holder="Operator must measure, report, and reduce ESG impacts to meet regulatory, investor, and community expectations",
        adversary_position="ESG reporting is voluntary and adds cost without clear financial benefit",
        counter_arguments=[
            "ESG performance directly impacts cost of capital and access to investment",
            "Regulations increasingly mandate emissions reporting and reduction",
            "Methane capture programs have positive ROI (captured gas = revenue)",
            "Social license failures can halt operations (community opposition, protests)"
        ],
        resolution_strategy="Implement comprehensive ESG measurement and reporting aligned with SASB/GRI frameworks, deploy LDAR programs and flare reduction technologies, engage communities proactively, tie executive compensation to ESG targets",
        entity_scope="Applicable to all oil and gas operators, especially public companies and those seeking institutional investment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Rapidly evolving ESG standards and regulations with increasing importance for investor and regulatory compliance",
        controlling_precedent="EPA regulations, SEC disclosure requirements, and industry best practices (IPIECA, SASB)",
        category=IssueCategory.ESG_METRICS
    ),
]


# ============================================================================
# ENGINE STATE
# ============================================================================

START_TIME = time.time()
QUERY_COUNT = 0
TOTAL_LATENCY_MS = 0.0
CACHE_HITS = 0
CACHE_MISSES = 0
DOCTRINE_USAGE: Dict[str, int] = defaultdict(int)


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def normalize_query(query: str) -> str:
    """Normalize query text for deterministic processing"""
    return query.lower().strip()


def search_doctrine_cache(query: str, top_k: int = 5) -> List[DoctrineBlock]:
    """Search doctrine cache for relevant blocks"""
    query_lower = query.lower()
    query_terms = set(query_lower.split())

    scored_blocks = []
    for block in DOCTRINE_CACHE:
        score = 0.0
        # Keyword matching
        for keyword in block.keywords:
            if keyword.lower() in query_lower:
                score += 2.0
        # Topic matching
        if any(term in block.topic.lower() for term in query_terms):
            score += 3.0
        # Category matching
        if block.category.value.lower().replace("_", " ") in query_lower:
            score += 1.5

        if score > 0:
            scored_blocks.append((score, block))

    scored_blocks.sort(reverse=True, key=lambda x: x[0])
    return [block for score, block in scored_blocks[:top_k]]


def three_layer_response(query: str, mode: ResponseMode, zone: AnalysisZone) -> Tuple[str, List[DoctrineBlock], List[str], ConfidenceLevel]:
    """Three-layer response: Cache → Semantic → Deep"""
    global CACHE_HITS, CACHE_MISSES

    # Layer 1: Doctrine cache (0-200ms)
    relevant_blocks = search_doctrine_cache(query, top_k=5)

    if relevant_blocks:
        CACHE_HITS += 1
        primary_block = relevant_blocks[0]

        # Track usage
        DOCTRINE_USAGE[primary_block.topic] += 1

        # Build reasoning chain
        reasoning_chain = [
            f"Doctrine cache hit: {primary_block.topic}",
            f"Category: {primary_block.category.value}",
            f"Confidence: {primary_block.confidence.value}"
        ]

        # Generate response based on mode
        if mode == ResponseMode.FAST:
            answer = "\n".join(primary_block.conclusion_template)
            reasoning_chain.append("FAST mode: Conclusion template only")
        elif mode == ResponseMode.DEFENSE:
            answer = f"{primary_block.reasoning_framework}\n\nConclusion:\n" + "\n".join(primary_block.conclusion_template)
            reasoning_chain.append("DEFENSE mode: Full reasoning framework + conclusion")
        else:  # MEMO
            answer = f"""MEMORANDUM - Production Optimization Analysis

TOPIC: {primary_block.topic}

ISSUE:
{query}

ANALYSIS:
{primary_block.reasoning_framework}

KEY FACTORS:
{chr(10).join(f"- {factor}" for factor in primary_block.key_factors)}

AUTHORITIES:
{chr(10).join(f"- {auth}" for auth in primary_block.primary_authority)}

RESOLUTION STRATEGY:
{primary_block.resolution_strategy}

CONFIDENCE STRATIFICATION:
{primary_block.confidence_stratification}

CONCLUSION:
{chr(10).join(primary_block.conclusion_template)}

DISCLOSURE:
{primary_block.controlling_precedent}
Analysis performed under {zone.value} context with {primary_block.confidence.value} confidence level.
"""
            reasoning_chain.append("MEMO mode: Full legal memorandum format")

        return answer, relevant_blocks, reasoning_chain, primary_block.confidence

    else:
        CACHE_MISSES += 1
        # Fallback response
        reasoning_chain = [
            "No direct doctrine cache hit",
            "Generating general production optimization guidance"
        ]

        answer = f"""This query relates to production optimization but doesn't match specific doctrine blocks in the cache.

General guidance for: {query}

For production optimization questions, consider:
1. Diagnose the specific production problem (decline, mechanical, formation damage)
2. Evaluate intervention options (optimization, stimulation, workover)
3. Perform economic analysis (NPV, payback period)
4. Consider operational constraints (rig availability, downtime, HSE risk)
5. Monitor results and adjust strategy

Recommend consulting specific doctrine blocks for:
- Artificial lift selection and optimization
- Wellbore integrity monitoring
- Scale and corrosion management
- Production surveillance and well testing
- Facility and gathering system optimization

For detailed analysis, please refine query to match available expertise areas."""

        return answer, [], reasoning_chain, ConfidenceLevel.DISCLOSURE


def multi_doctrine_decomposition(query: str) -> Dict[str, Any]:
    """Decompose complex queries into multiple doctrine categories"""
    categories_mentioned = []
    for category in IssueCategory:
        if category.value.lower().replace("_", " ") in query.lower():
            categories_mentioned.append(category)

    return {
        "primary_category": categories_mentioned[0] if categories_mentioned else IssueCategory.ARTIFICIAL_LIFT,
        "related_categories": categories_mentioned[1:] if len(categories_mentioned) > 1 else [],
        "complexity": "high" if len(categories_mentioned) > 2 else "moderate" if len(categories_mentioned) > 1 else "simple"
    }


def calculate_determinism_hash(query: str, answer: str, mode: ResponseMode) -> str:
    """Calculate SHA-256 hash for determinism verification"""
    content = f"{query}|{answer}|{mode.value}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@APP.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "engine": "PROD05 - Production Optimization Engine",
        "version": "1.0.0",
        "status": "operational",
        "port": "9035"
    }


@APP.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    uptime = time.time() - START_TIME
    avg_latency = (TOTAL_LATENCY_MS / QUERY_COUNT) if QUERY_COUNT > 0 else 0.0
    cache_hit_rate = (CACHE_HITS / (CACHE_HITS + CACHE_MISSES)) if (CACHE_HITS + CACHE_MISSES) > 0 else 0.0

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        port=9035,
        doctrine_blocks=len(DOCTRINE_CACHE),
        categories=len(IssueCategory),
        uptime_seconds=uptime,
        total_queries=QUERY_COUNT,
        avg_latency_ms=avg_latency,
        cache_hit_rate=cache_hit_rate
    )


@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint - production optimization analysis"""
    global QUERY_COUNT, TOTAL_LATENCY_MS

    start_time = time.time()

    try:
        logger.info(f"Query received: {request.query[:100]}... | Mode: {request.mode} | Zone: {request.zone}")

        # Normalize query
        normalized_query = normalize_query(request.query)

        # Multi-doctrine decomposition
        decomposition = multi_doctrine_decomposition(normalized_query)

        # Three-layer response
        answer, relevant_blocks, reasoning_chain, confidence = three_layer_response(
            normalized_query, request.mode, request.zone
        )

        # Calculate determinism hash
        det_hash = calculate_determinism_hash(request.query, answer, request.mode)

        # Build response
        latency_ms = (time.time() - start_time) * 1000
        QUERY_COUNT += 1
        TOTAL_LATENCY_MS += latency_ms

        response = QueryResponse(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            answer=answer,
            confidence=confidence,
            doctrine_blocks_used=[block.topic for block in relevant_blocks],
            reasoning_chain=reasoning_chain,
            key_factors=[block.key_factors[0] if block.key_factors else "" for block in relevant_blocks[:3]],
            recommendations=[
                "Perform diagnostic testing before intervention",
                "Calculate NPV for all intervention options",
                "Monitor results and adjust strategy based on data"
            ],
            alternatives_considered=decomposition.get("related_categories", []),
            determinism_hash=det_hash,
            telemetry={
                "latency_ms": latency_ms,
                "doctrine_blocks_searched": len(DOCTRINE_CACHE),
                "doctrine_blocks_matched": len(relevant_blocks),
                "decomposition_complexity": decomposition["complexity"],
                "cache_hit": len(relevant_blocks) > 0
            },
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

        logger.info(f"Query completed: {latency_ms:.2f}ms | Confidence: {confidence.value} | Blocks: {len(relevant_blocks)}")

        return response

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@APP.get("/doctrines", response_model=Dict[str, Any])
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "total_blocks": len(DOCTRINE_CACHE),
        "categories": [cat.value for cat in IssueCategory],
        "topics": [block.topic for block in DOCTRINE_CACHE],
        "blocks": [
            {
                "topic": block.topic,
                "category": block.category.value,
                "confidence": block.confidence.value,
                "keywords": block.keywords[:5]
            }
            for block in DOCTRINE_CACHE
        ]
    }


@APP.get("/stats", response_model=Dict[str, Any])
async def get_stats():
    """Get engine statistics"""
    return {
        "total_queries": QUERY_COUNT,
        "cache_hits": CACHE_HITS,
        "cache_misses": CACHE_MISSES,
        "cache_hit_rate": (CACHE_HITS / (CACHE_HITS + CACHE_MISSES)) if (CACHE_HITS + CACHE_MISSES) > 0 else 0.0,
        "avg_latency_ms": (TOTAL_LATENCY_MS / QUERY_COUNT) if QUERY_COUNT > 0 else 0.0,
        "top_doctrines": sorted(DOCTRINE_USAGE.items(), key=lambda x: x[1], reverse=True)[:10],
        "uptime_seconds": time.time() - START_TIME
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("="*80)
    logger.info("PROD05 - Production Optimization Engine")
    logger.info("TIE Gold Standard - Production Engineering Intelligence")
    logger.info(f"Doctrine Blocks: {len(DOCTRINE_CACHE)}")
    logger.info(f"Categories: {len(IssueCategory)}")
    logger.info("="*80)

    uvicorn.run(APP, host="0.0.0.0", port=9035, log_level="info")
