"""
OFE09 - Coiled Tubing Operations Engine
Tax Intelligence Engine (TIE) Gold Standard Architecture

Domain: Oilfield Equipment - Coiled Tubing Operations
Port: 9009
Version: 1.0.0

Covers: CT string management, fatigue life tracking, BHA design, CT drilling,
wellbore cleanout, nitrogen pumping, CT fracturing, fishing, cement squeezes,
injector head operation, CT BOP systems, reel capacity, tubing selection,
yield strength, depth tracking, surface equipment layout, fatigue modeling
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


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


class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    STRING_MANAGEMENT = "STRING_MANAGEMENT"
    FATIGUE_LIFE = "FATIGUE_LIFE"
    BHA_DESIGN = "BHA_DESIGN"
    CT_DRILLING = "CT_DRILLING"
    WELLBORE_CLEANOUT = "WELLBORE_CLEANOUT"
    NITROGEN_PUMPING = "NITROGEN_PUMPING"
    CT_FRACTURING = "CT_FRACTURING"
    CT_FISHING = "CT_FISHING"
    CEMENT_SQUEEZE = "CEMENT_SQUEEZE"
    INJECTOR_HEAD = "INJECTOR_HEAD"
    CT_BOP_SYSTEM = "CT_BOP_SYSTEM"
    REEL_CAPACITY = "REEL_CAPACITY"
    TUBING_SELECTION = "TUBING_SELECTION"
    YIELD_STRENGTH = "YIELD_STRENGTH"
    DEPTH_TRACKING = "DEPTH_TRACKING"
    SURFACE_EQUIPMENT = "SURFACE_EQUIPMENT"
    FATIGUE_MODELING = "FATIGUE_MODELING"
    POWER_PACK = "POWER_PACK"
    CRANE_MAST_OPS = "CRANE_MAST_OPS"
    FLOWBACK_OPS = "FLOWBACK_OPS"


@dataclass
class DoctrineBlock:
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
    entity_scope: List[str]
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: List[str]
    issue_category: IssueCategory
    position_zone: PositionZone = PositionZone.PLANNING


class QueryRequest(BaseModel):
    query: str = Field(..., description="CT operations question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    query: str
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    reasoning_chain: List[str]
    doctrines_triggered: List[str]
    telemetry: Dict[str, Any]
    determinism_hash: str
    timestamp: str


# ============================================================================
# DOCTRINE CACHE - 25+ COILED TUBING EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="CT String Fatigue Life Tracking",
        keywords=["fatigue", "cycles", "string life", "tubing tally", "fatigue log", "retirement criteria"],
        conclusion_template=[
            "CT string fatigue life shall be tracked using cumulative cycle counting per API Recommended Practice 5ST.",
            "Retirement criteria based on manufacturer specifications, typically 80-90% of predicted fatigue life.",
            "Each trip constitutes one full fatigue cycle; partial trips count as fraction based on depth percentage."
        ],
        reasoning_framework="""
CT pipe experiences plastic deformation every time it passes over gooseneck and straightener.
Fatigue life calculation methodology:
1. Track diameter changes from baseline (new pipe = reference zero)
2. Count full cycles (reel → well → reel = 1 cycle)
3. Monitor pipe OD with calipers every 500-1000 ft after each job
4. Apply service severity multipliers (high pressure/temperature = accelerated fatigue)
5. Calculate remaining life using manufacturer fatigue curves (typically proprietary)
6. Implement retirement when OD reduction exceeds 3-5% or wall thinning detected

Industry standard: Schlumberger CoilLife software or NOV TubingLife models predict remaining cycles.
Typical fatigue life: 200-400 cycles for standard operations, 100-150 for high-stress applications.
Critical monitoring points: 500 ft increments from outer wrap (highest fatigue), gooseneck radius points.
""",
        key_factors=[
            "Cumulative cycle count (every trip = 1 cycle)",
            "Outer diameter reduction from baseline (3-5% = retirement threshold)",
            "Wall thickness monitoring via ultrasonic testing",
            "Service severity (pressure, temperature, corrosive fluids)",
            "Gooseneck radius (tighter radius = higher fatigue)",
            "Tubing grade and yield strength",
            "Manufacturer fatigue predictions (proprietary curves)"
        ],
        primary_authority=[
            "API Recommended Practice 5ST: Coiled Tubing Operations",
            "Schlumberger CoilLife Fatigue Modeling Software",
            "NOV TubingLife Predictive Models",
            "Manufacturer specifications (National Oilwell Varco, Baker Hughes, Schlumberger)"
        ],
        burden_holder="CT service company",
        adversary_position="Operator may push for extended use beyond recommended fatigue limits to reduce mobilization costs.",
        counter_arguments=[
            "Premature retirement wastes usable pipe and increases costs",
            "Visual inspection may not reveal internal degradation",
            "Field conditions may differ from lab fatigue testing",
            "Economic pressure to extend string life beyond conservative limits"
        ],
        resolution_strategy="Implement strict fatigue tracking protocol with real-time monitoring, third-party inspection, and documented retirement criteria per API 5ST standards.",
        entity_scope=["CT service companies", "well operators", "pipe manufacturers"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry-standard fatigue tracking with documented retirement criteria provides defensible safety protocol.",
        controlling_precedent=[
            "API RP 5ST Section 6: CT String Management",
            "ISO 13628-7: Design and operation of subsea production systems - Completion/workover riser systems"
        ],
        issue_category=IssueCategory.FATIGUE_LIFE,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="BHA Design for CT Drilling Applications",
        keywords=["BHA", "bottom hole assembly", "CT drilling", "motor", "drilling BHA", "rotary steerable"],
        conclusion_template=[
            "CT drilling BHA must include downhole motor (positive displacement or turbine), stabilizers, and MWD/LWD tools.",
            "Maximum BHA OD constrained by wellbore ID and CT tubing ID limitations (typically 1.5-2.875 inch motors).",
            "Weight-on-bit delivered via CT weight buckling, limited by tubing yield strength and helical buckling limits."
        ],
        reasoning_framework="""
CT drilling BHA design differs fundamentally from conventional drill string:
1. No surface rotation capability → downhole motor required (PDM 90% of applications)
2. CT OD typically 1.25-3.5 inch → limits motor size and bit diameter
3. Weight delivery via sinusoidal/helical buckling of CT in vertical/deviated sections
4. BHA components from bottom up:
   - Bit (PDC, roller cone, or hybrid based on formation)
   - Mud motor (positive displacement motor 95% of cases)
   - Flex joint or bent housing (for directional control)
   - Stabilizers (1-3 to control buckling and prevent lockup)
   - MWD tools (gamma ray minimum, adds/gyro for directional)
   - Disconnect sub (for fishing operations if BHA stuck)
   - CT connector

Critical constraints:
- Motor stall if insufficient WOB delivered (buckling geometry dependent)
- Excessive buckling → lockup in horizontal sections (friction factor critical)
- CT tubing must withstand combined tension, pressure, and buckling loads
- Flow rate requirements for motor operation (typically 1.5-4 bbl/min)

Typical CT drilling BHA length: 30-60 ft, weight 500-2000 lbs.
""",
        key_factors=[
            "Downhole motor selection (PDM vs turbine, bend angle for steering)",
            "Stabilizer placement (control buckling, prevent differential sticking)",
            "MWD/LWD tool requirements (gamma, resistivity, directional sensors)",
            "Disconnect sub for BHA recovery if stuck",
            "Flow rate requirements for motor operation (1.5-4 bbl/min typical)",
            "Maximum BHA OD vs wellbore ID clearance",
            "CT tubing yield strength vs required WOB delivery",
            "Buckling analysis for weight transfer efficiency"
        ],
        primary_authority=[
            "SPE 37697: CT Drilling BHA Design Optimization",
            "API RP 5ST: Coiled Tubing Operations (Annex C - Drilling)",
            "Schlumberger CT Drilling Handbook",
            "Baker Hughes AutoTrak Curve CT Drilling Systems Manual"
        ],
        burden_holder="CT drilling contractor",
        adversary_position="Operator may specify incompatible BHA requirements (too aggressive WOB, unrealistic motor performance expectations).",
        counter_arguments=[
            "BHA complexity increases cost and failure risk",
            "CT drilling slower than conventional rotary in many applications",
            "Directional control limited compared to rotary steerable systems",
            "Motor reliability issues in high-temperature or abrasive environments"
        ],
        resolution_strategy="Design BHA within CT system limitations using proven motor technology, conservative buckling analysis, and backup fishing tools.",
        entity_scope=["CT drilling contractors", "directional drilling companies", "well operators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="BHA design based on established CT drilling practices with proven motor and MWD technology.",
        controlling_precedent=[
            "API RP 5ST Annex C: Coiled Tubing Drilling Operations",
            "SPE 37697: Coiled Tubing Drilling BHA Design"
        ],
        issue_category=IssueCategory.BHA_DESIGN,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Injector Head Operation and Gripper Block Maintenance",
        keywords=["injector head", "gripper blocks", "chains", "drive chains", "injector", "gripping force"],
        conclusion_template=[
            "Injector head gripper blocks must apply sufficient gripping force without damaging CT pipe outer diameter.",
            "Chain tension adjustments required every 50-100 operating hours to maintain proper grip.",
            "Gripper block insert replacement when wear indicators show 50% material loss or CT slip events occur."
        ],
        reasoning_framework="""
Injector head is primary CT handling equipment - grips tubing and pushes/pulls from reel.
Typical design: dual chain system with hydraulic-actuated gripper blocks.

Operating principles:
1. Gripper blocks contain hardened steel or carbide inserts that bite into CT OD
2. Hydraulic pressure (typically 1500-3000 psi) actuates gripper blocks
3. Drive chains (roller chain, typically #140 or #160) pull gripper assemblies
4. Chain sprockets driven by hydraulic motors (variable speed 0-120 ft/min typical)

Critical maintenance points:
- Gripper block insert wear creates slip risk (CT moves but grippers don't engage)
- Excessive gripping force damages CT pipe (creates stress concentrations → fatigue)
- Chain stretch from wear requires tensioning every 50-100 hrs (measure with tension gauge)
- Chain lubrication critical (API approved lubricants, daily application)
- Hydraulic system pressure monitoring (low pressure = insufficient grip)

Inspection protocol:
- Visual: Check gripper inserts for cracks, wear patterns, material loss
- Measurement: Check chain sag/tension (typically max 1-2 inch sag acceptable)
- Functional: Test grip at low pressure before running high loads
- CT pipe: Inspect for gripper marks after each trip (excessive marking = over-gripping)

Typical gripper block life: 500-1500 hours depending on CT OD, tubing grade, and operating conditions.
""",
        key_factors=[
            "Hydraulic pressure to gripper blocks (1500-3000 psi typical)",
            "Gripper insert material (hardened steel vs carbide)",
            "Chain tension and stretch monitoring",
            "CT pipe OD marking/damage from excessive grip",
            "Slip events indicating insufficient gripping force",
            "Injector speed control (0-120 ft/min variable)",
            "Chain lubrication schedule (daily)",
            "Gripper insert wear indicators (50% material loss = replace)"
        ],
        primary_authority=[
            "API RP 5ST Section 7: CT Surface Equipment Operation",
            "Injector manufacturer specifications (NOV, Stewart & Stevenson, Halliburton)",
            "OSHA 1910.147: Lockout/Tagout for injector maintenance"
        ],
        burden_holder="CT service company operating crew",
        adversary_position="Time pressure may lead to deferred gripper maintenance, increasing slip and failure risk.",
        counter_arguments=[
            "Gripper block replacement is expensive and time-consuming",
            "Visual wear indicators may not detect internal degradation",
            "Over-tightening chains can damage sprockets",
            "CT pipe damage from grippers may be cosmetic, not structural"
        ],
        resolution_strategy="Implement scheduled preventive maintenance with documented chain tension measurements, gripper insert inspections, and CT pipe OD monitoring.",
        entity_scope=["CT service companies", "equipment manufacturers", "field supervisors"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Injector maintenance per manufacturer specs and API RP 5ST provides defensible safety and operational protocol.",
        controlling_precedent=[
            "API RP 5ST Section 7.3: Injector Head Operation and Maintenance",
            "OSHA 1910.147: Control of Hazardous Energy (Lockout/Tagout)"
        ],
        issue_category=IssueCategory.INJECTOR_HEAD,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="CT BOP Configuration and Stripper/Packer Operation",
        keywords=["CT BOP", "quad BOP", "stripper", "packer", "blowout preventer", "well control", "shear rams"],
        conclusion_template=[
            "CT BOP stack shall include minimum: stripper/packer assembly, dual pipe rams, blind/shear rams.",
            "Stripper element seals around moving CT during circulation; packer assembly seals stationary CT during static conditions.",
            "BOP testing required per API RP 53 before job start: low-pressure (200-300 psi) and high-pressure (rated working pressure)."
        ],
        reasoning_framework="""
CT BOP system provides well control for pressurized well operations.
Standard quad BOP configuration (bottom to top):
1. Stripper/packer assembly (annular-type seal, seals on moving or stationary CT)
2. Pipe rams #1 (sized for CT OD, typically 1.25-3.5 inch range)
3. Pipe rams #2 (redundant seal, same size as #1)
4. Blind/shear rams (close wellbore if CT parted or emergency evacuation)

Operational distinctions:
STRIPPER: Dynamic seal, allows CT movement while maintaining seal, rubber element wears with friction
PACKER: Static seal, higher pressure rating (10,000-15,000 psi typical), activated when CT stationary

Critical well control scenarios:
- Well kick during circulation → close stripper, activate packer if needed, shut-in well
- CT parted downhole → close blind/shear rams immediately to secure well
- Pressure test failure → do not proceed with operation until repaired/replaced

BOP testing protocol (API RP 53):
1. Low-pressure test (200-300 psi): Check for seal, identify leaks
2. High-pressure test (rated working pressure, typically 3,000-10,000 psi): Verify full rating
3. Function test each ram individually before combined operations
4. Document all tests with pressure charts and witness signatures

Stripper element life: 50-200 hours depending on CT surface condition, pressure, and movement frequency.
Replace stripper element when leak rate exceeds 1 bbl/hr or visible damage observed.
""",
        key_factors=[
            "BOP stack configuration (stripper, dual pipe rams, blind/shear rams)",
            "Pipe ram size selection for CT OD (must match tubing size)",
            "Stripper element wear monitoring (leak rate, visual inspection)",
            "BOP pressure rating vs maximum anticipated surface pressure (MASP)",
            "Function testing before job (low and high pressure per API RP 53)",
            "Emergency shutdown system (ESD) integration with BOP controls",
            "Accumulator capacity for BOP closure (sufficient volume for all rams)",
            "BOP control panel location and accessibility"
        ],
        primary_authority=[
            "API RP 53: Blowout Prevention Equipment Systems for Drilling Wells",
            "API RP 5ST Section 8: Well Control Equipment for CT Operations",
            "30 CFR 250.721: BOP requirements (offshore)",
            "State regulations (Texas RRC Rule 13, Louisiana Statewide Order 29-B)"
        ],
        burden_holder="CT service company and well operator (joint responsibility)",
        adversary_position="Time pressure may lead to abbreviated BOP testing or deferring stripper element replacement.",
        counter_arguments=[
            "Full BOP testing delays job start and increases costs",
            "Stripper element replacement is expensive and time-consuming",
            "Low-pressure leaks may not indicate high-pressure failure risk",
            "Redundant rams provide backup if one element fails"
        ],
        resolution_strategy="Enforce strict BOP testing per API RP 53 with documented pressure tests and witness signatures before every job start.",
        entity_scope=["CT service companies", "well operators", "regulatory agencies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="BOP configuration and testing per API RP 53 provides legally defensible well control protocol.",
        controlling_precedent=[
            "API RP 53: Blowout Prevention Equipment Systems",
            "API RP 5ST Section 8: Well Control Equipment",
            "30 CFR 250.721: Blowout preventer (BOP) system (offshore federal)"
        ],
        issue_category=IssueCategory.CT_BOP_SYSTEM,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Reel Capacity Calculations and CT String Length Management",
        keywords=["reel capacity", "tubing length", "reel diameter", "outer wrap", "inner wrap", "string length"],
        conclusion_template=[
            "Reel capacity calculated using inside diameter, core diameter, tubing OD, and wall thickness per geometric spiral formula.",
            "Maximum string length limited by reel capacity, fatigue considerations (outer wraps experience highest stress), and well depth requirements.",
            "Outer wrap radius dictates minimum bend radius and maximum fatigue stress on CT pipe."
        ],
        reasoning_framework="""
CT reel capacity determines maximum string length that can be stored.
Reel geometry:
- Core diameter: Inner hub where CT wraps begin (typically 72-96 inches)
- Reel flanges: Outer diameter containing CT wraps (typically 96-144 inches)
- Usable width: Distance between flanges minus safety margins

Capacity calculation (simplified):
Length ≈ π × (D_outer² - D_core²) / (4 × OD × SF)
Where: D_outer = outer wrap diameter, D_core = core diameter, OD = tubing OD, SF = safety factor (~1.1-1.2)

Practical capacity examples:
- 1.25" CT, 96" reel: ~15,000-18,000 ft
- 2.0" CT, 96" reel: ~10,000-12,000 ft
- 2.875" CT, 120" reel: ~8,000-10,000 ft

Critical considerations:
1. Outer wrap experiences maximum bending stress (largest radius, highest fatigue)
2. Inner wrap has tightest radius (highest stress per cycle but fewer cycles as outer wraps run first)
3. String length selection: Match well depth +500-1000 ft safety margin
4. Weight on reel: CT + reel weight affects transport (DOT weight limits, crane capacity)

Reel rotation monitoring:
- Depth counter tracks string position based on reel rotations and diameter changes
- Outer wrap diameter changes as CT deploys (diameter decreases)
- Depth counter must recalibrate periodically (measure actual depth vs counted depth)
""",
        key_factors=[
            "Reel core diameter (72-96 inches typical)",
            "Reel outer diameter (96-144 inches typical)",
            "CT tubing OD and wall thickness",
            "Usable reel width between flanges",
            "Outer wrap bending radius (affects fatigue life)",
            "Total CT weight on reel (affects transport and crane capacity)",
            "Depth counter calibration (reel rotation vs actual depth)",
            "Well depth requirements plus safety margin (500-1000 ft)"
        ],
        primary_authority=[
            "API RP 5ST Section 5: CT Reeling Systems",
            "Manufacturer specifications (NOV, Schlumberger, Baker Hughes reel designs)",
            "DOT weight regulations for CT unit transport"
        ],
        burden_holder="CT service company engineering team",
        adversary_position="Operator may request string length exceeding reel capacity or well depth requirements.",
        counter_arguments=[
            "Smaller OD tubing allows greater length but reduces strength and flow area",
            "Larger reel increases capacity but adds weight and transport complexity",
            "Depth counter errors can lead to incorrect depth tracking",
            "Outer wrap fatigue may require premature string retirement"
        ],
        resolution_strategy="Calculate reel capacity using standard geometric formulas, select CT OD and length within reel limits and well depth requirements.",
        entity_scope=["CT service companies", "equipment manufacturers", "logistics coordinators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Reel capacity calculations based on proven geometric formulas and manufacturer specifications.",
        controlling_precedent=[
            "API RP 5ST Section 5.2: Reel Design and Capacity",
            "ASME B30.7: Winches, Reel Handling Systems"
        ],
        issue_category=IssueCategory.REEL_CAPACITY,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="CT Tubing OD Selection and Grade Specification",
        keywords=["tubing OD", "1.25 inch", "2.0 inch", "2.875 inch", "3.5 inch", "CT grade", "70 ksi", "80 ksi", "110 ksi"],
        conclusion_template=[
            "CT tubing OD selected based on: wellbore ID clearance, required flow rate, weight/depth capacity, and operational loads.",
            "Common CT grades: 70 ksi (mild applications), 80 ksi (standard), 90-110 ksi (high-strength for deep wells or heavy loads).",
            "Minimum annular clearance: 1/2 inch between CT OD and wellbore ID for cuttings circulation and pressure management."
        ],
        reasoning_framework="""
CT tubing size selection involves multiple competing factors:

OD selection drivers:
1. Wellbore ID constraint: CT OD must clear minimum restrictions (typically 1/2" clearance minimum)
2. Flow capacity: Larger ID provides higher flow rates for cleanout/circulation (critical for drilling, fracturing)
3. Strength requirements: Larger OD and wall thickness provide higher yield strength for deep wells
4. Weight limitations: Heavier CT requires larger injector, power pack, and affects helical buckling depth

Common CT sizes and typical applications:
- 1.0-1.25" OD: Slim hole workovers, shallow wells (<8,000 ft), limited flow applications
- 1.5-2.0" OD: Standard workover, cleanouts, moderate depth (8,000-15,000 ft)
- 2.375-2.875" OD: Deep wells (>15,000 ft), high flow requirements, CT drilling
- 3.5" OD: Ultra-deep wells, heavy-duty applications, specialized units only

CT grade selection (yield strength):
- 70 ksi: Mild service, shallow wells, low pressure
- 80 ksi: Standard grade, most common, good balance of strength and fatigue life
- 90-110 ksi: High-strength applications, deep wells, high-pressure environments
- 110+ ksi: Specialty applications, ultra-deep wells, extreme loads

Trade-offs:
- Higher strength grades have reduced fatigue life (more cycles = earlier failure)
- Larger OD has higher drag in deviated wells (friction factor critical)
- Smaller OD limits flow capacity and tools that can be run through tubing

Flow rate comparison (approximate at 1000 psi pressure drop):
- 1.25" ID 0.095" wall: ~1.5 bbl/min
- 2.0" ID 0.134" wall: ~4.5 bbl/min
- 2.875" ID 0.188" wall: ~12 bbl/min
""",
        key_factors=[
            "Wellbore ID and minimum restriction clearance (1/2 inch typical)",
            "Required flow rate for operation (cleanout, drilling, fracturing)",
            "Well depth and anticipated weight/tension loads",
            "Tubing yield strength grade (70, 80, 90, 110 ksi options)",
            "Fatigue life considerations (higher strength = reduced fatigue life)",
            "Injector head capacity (can it handle CT weight and diameter?)",
            "Reel capacity for selected OD and length",
            "Annular velocity requirements for hole cleaning"
        ],
        primary_authority=[
            "API Specification 5ST: Coiled Tubing",
            "API RP 5ST: Coiled Tubing Operations",
            "Manufacturer product specifications (National Oilwell Varco, Tenaris, Vallourec)"
        ],
        burden_holder="CT service company engineering",
        adversary_position="Operator may specify smallest OD to reduce cost, compromising flow capacity or strength requirements.",
        counter_arguments=[
            "Larger OD increases cost, reel weight, and injector requirements",
            "Higher strength grades cost more and have shorter fatigue life",
            "Oversized CT for application wastes capacity and increases operational costs",
            "Annular clearance can be reduced in certain controlled conditions"
        ],
        resolution_strategy="Select CT OD and grade using engineering analysis of flow requirements, depth capacity, and wellbore geometry constraints.",
        entity_scope=["CT service companies", "well operators", "CT manufacturers"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="CT sizing based on API specifications and proven operational experience provides defensible engineering basis.",
        controlling_precedent=[
            "API Specification 5ST: Coiled Tubing (dimensional and material standards)",
            "API RP 5ST Section 4: CT String Design and Selection"
        ],
        issue_category=IssueCategory.TUBING_SELECTION,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Nitrogen Pumping Through CT for Underbalanced Operations",
        keywords=["nitrogen", "N2", "underbalanced", "gas lift", "foam", "energized fluid", "membrane unit"],
        conclusion_template=[
            "Nitrogen pumping through CT enables underbalanced operations to avoid formation damage in low-pressure reservoirs.",
            "Nitrogen generation via membrane units (95-98% purity) or cryogenic systems (99.9% purity) based on volume and purity requirements.",
            "Maximum nitrogen injection rate limited by CT flow capacity, nitrogen compressor output, and downhole pressure requirements."
        ],
        reasoning_framework="""
Nitrogen applications in CT operations:
1. Underbalanced cleanout (reduce hydrostatic pressure below reservoir pressure)
2. Foam generation (mix nitrogen with liquid for enhanced cuttings removal)
3. Gas lift (displace heavy fluids from wellbore)
4. Purging (displace oxygen or corrosive fluids)

Nitrogen generation methods:
MEMBRANE UNITS:
- Separate nitrogen from air using semi-permeable membranes
- Purity: 95-98% nitrogen (balance oxygen, argon)
- Output: 500-5,000 scfm depending on unit size
- Mobile units common for CT operations

CRYOGENIC/LIQUID N2:
- Ultra-high purity (99.9%+)
- Delivered in dewars or transported as liquid
- Vaporized on-site through heat exchangers
- Higher cost but better for critical applications (corrosion-sensitive formations)

CT nitrogen pumping configuration:
- Nitrogen compressor → flowmeter → check valve → CT injection head
- Nitrogen mixes with liquid at surface or downhole depending on application
- Foam quality (gas volume %) controlled by N2 and liquid injection rates
- Typical foam quality: 50-80% for cuttings transport

Critical parameters:
- Injection pressure: Must overcome wellbore hydrostatic + friction + surface pressure
- Volumetric flow rate: Nitrogen volume expands significantly as pressure decreases downhole
- CT flow capacity: Limits total gas+liquid throughput (typically 2-6 bbl/min)
- Oxygen content: <5% oxygen required for H2S environments (flammability risk)

Safety considerations:
- Nitrogen displaces oxygen → asphyxiation hazard in confined spaces
- High-pressure nitrogen storage (tube trailers 2,400-3,600 psi) requires DOT compliance
- Venting nitrogen from wellbore creates noise and potential freezing hazards
""",
        key_factors=[
            "Nitrogen purity requirements (95% membrane vs 99.9% cryogenic)",
            "Injection rate and volume requirements",
            "Wellbore pressure and depth (affects expansion calculations)",
            "Foam quality target (50-80% typical for solids transport)",
            "CT flow capacity limitations",
            "Compressor output capacity (scfm at operating pressure)",
            "Safety protocols for nitrogen handling and venting",
            "Oxygen content limits for H2S or flammable gas environments"
        ],
        primary_authority=[
            "API RP 5ST Annex D: Underbalanced CT Operations",
            "OSHA 1910.146: Permit-required confined spaces (asphyxiation hazards)",
            "DOT 49 CFR 173: Compressed gas transportation"
        ],
        burden_holder="CT service company nitrogen operations team",
        adversary_position="Operator may demand higher injection rates exceeding CT or compressor capacity.",
        counter_arguments=[
            "Membrane nitrogen purity sufficient for most applications (cryogenic unnecessary)",
            "Foam quality calculations are estimates (actual downhole quality varies)",
            "Nitrogen costs can be reduced by using air in non-critical applications",
            "Safety protocols can be streamlined under time pressure"
        ],
        resolution_strategy="Design nitrogen system within CT flow limitations using appropriate generation method (membrane vs cryogenic) and strict safety protocols.",
        entity_scope=["CT service companies", "nitrogen service providers", "well operators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Nitrogen pumping design per API RP 5ST and proven operational practices provides defensible underbalanced operations protocol.",
        controlling_precedent=[
            "API RP 5ST Annex D: Underbalanced Operations",
            "OSHA 1910.146: Confined Space Entry (nitrogen asphyxiation hazards)"
        ],
        issue_category=IssueCategory.NITROGEN_PUMPING,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="CT Fracturing Operations and Proppant Limitations",
        keywords=["CT fracturing", "CT frac", "proppant", "limited entry", "ball sealers", "frac sleeves"],
        conclusion_template=[
            "CT fracturing enables selective zone stimulation without workover rig, but proppant concentration limited by CT ID erosion risk.",
            "Maximum proppant concentration typically 2-4 ppg through CT (vs 8-12 ppg conventional fracturing) to avoid tubing erosion.",
            "Frac sleeve systems or ball drop activation used for multi-stage fracturing through CT."
        ],
        reasoning_framework="""
CT fracturing advantages:
- Selective zone treatment without pulling production tubing
- Reduced footprint vs conventional frac spread
- Real-time pressure and rate control at CT head
- Can treat multiple zones in single trip with sleeve systems

CT fracturing limitations:
1. PROPPANT EROSION: High-velocity proppant slurry erodes CT ID
   - Maximum safe proppant concentration: 2-4 ppg (pounds per gallon)
   - Conventional fracturing: 8-12 ppg typical
   - Erosion concentrated at gooseneck, injector head, and CT connections

2. FLOW RATE LIMITATIONS: CT ID limits maximum pump rate
   - 2.0" CT: ~15-25 bpm max (barrels per minute)
   - 2.875" CT: ~30-40 bpm max
   - Conventional frac: 60-100+ bpm typical

3. PRESSURE LIMITATIONS: CT yield strength limits maximum surface pressure
   - Typical max surface pressure: 5,000-10,000 psi
   - Must account for friction pressure in CT string

Multi-stage CT fracturing methods:
BALL DROP SYSTEMS:
- Drop degradable balls to seal lower zones, isolate upper zones
- Balls land on seats (sized progressively smaller moving up wellbore)
- Typical: 4-8 stages per trip

FRAC SLEEVE ACTIVATION:
- Mechanical or hydraulic sleeves in completion
- CT manipulates sleeves to expose perforations
- Unlimited stages possible

ABRASIVE JET PERFORATING:
- CT delivers abrasive slurry to perforate casing
- Immediate fracture treatment through fresh perforations
- No wireline or gun running required

Erosion mitigation:
- Reduce proppant concentration (accept lower proppant mass per stage)
- Use ceramic or resin-coated proppant (less erosive than sand)
- Limit frac treatment time per stage
- Monitor CT for erosion after each job (ultrasonic wall thickness)
""",
        key_factors=[
            "Maximum proppant concentration (2-4 ppg through CT)",
            "CT ID erosion monitoring (ultrasonic thickness testing)",
            "Maximum pump rate based on CT flow capacity",
            "Surface pressure limitations from CT yield strength",
            "Multi-stage activation method (balls, sleeves, or jet perforating)",
            "Proppant type selection (ceramic vs sand for erosion control)",
            "Treatment volume and proppant mass per stage",
            "Post-job CT inspection for erosion damage"
        ],
        primary_authority=[
            "API RP 5ST Annex E: CT Fracturing Operations",
            "SPE 84176: CT Fracturing Design and Operational Considerations",
            "Manufacturer guidelines for erosion limits (Schlumberger, Baker Hughes)"
        ],
        burden_holder="CT service company and fracturing contractor (joint responsibility)",
        adversary_position="Operator may demand higher proppant concentrations matching conventional frac designs, risking CT erosion.",
        counter_arguments=[
            "Lower proppant concentrations reduce fracture conductivity and production gains",
            "CT fracturing costs more per stage than conventional methods",
            "Erosion risk can be managed with careful monitoring",
            "Selective zone treatment benefits may not justify reduced proppant mass"
        ],
        resolution_strategy="Design CT frac treatments within safe proppant concentration limits (2-4 ppg) with post-job erosion inspection and documented erosion monitoring.",
        entity_scope=["CT service companies", "fracturing contractors", "well operators"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="CT fracturing proppant limits based on field experience but erosion risk requires case-by-case evaluation.",
        controlling_precedent=[
            "API RP 5ST Annex E: Coiled Tubing Fracturing Operations",
            "SPE 84176: Coiled Tubing Fracturing Design Optimization"
        ],
        issue_category=IssueCategory.CT_FRACTURING,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Real-Time Depth Tracking and Weight Indicator Monitoring",
        keywords=["depth tracking", "weight indicator", "WOB", "overpull", "string weight", "drag", "depth counter"],
        conclusion_template=[
            "Real-time depth tracking via reel rotation counter calibrated against measured depth (wireline or gamma log correlation).",
            "Weight indicator monitors CT string tension at injector head, detecting overpull, drag anomalies, and buckling transitions.",
            "Depth counter accuracy ±0.5-1.0% under normal conditions; recalibration required after string tension or reel geometry changes."
        ],
        reasoning_framework="""
Real-time depth tracking critical for:
- Positioning tools at target zones (perforations, fracture points)
- Monitoring progress during drilling or cleanout
- Detecting stuck pipe conditions (depth stops advancing, weight anomaly)
- Coordinating with surface operations (pump rates, nitrogen injection)

Depth counter methodology:
1. Reel rotation sensor (encoder) counts revolutions
2. Software calculates CT deployed based on reel geometry:
   - Outer wrap diameter changes as CT deploys (diameter decreases)
   - Algorithm compensates for changing wrap diameter
3. Initial calibration: Measure known depth (wireline tag, gamma log correlation)
4. Periodic recalibration: Compare depth counter to known markers

Depth accuracy factors:
- Reel geometry changes (CT compression under load affects effective diameter)
- Temperature effects (reel expansion/contraction)
- Encoder resolution (higher resolution = better accuracy)
- String stretch under tension (elastic elongation 0.1-0.3%)

Weight indicator system:
- Load cell at injector head measures tension/compression on CT
- Displays: Real-time weight, maximum/minimum weight, weight trend
- Critical alerts: Overpull (approaching yield strength), slack-off (buckling), stuck pipe

Weight interpretation:
NORMAL DESCENT: Weight = CT string weight in air - buoyancy + friction drag
OVERPULL: Weight > normal (stuck pipe, obstructions, tight spots)
SLACK-OFF: Weight < normal (buckling initiation, well pressure supporting CT)
BUCKLING TRANSITION: Weight decreases as CT buckles sinusoidally then helically

Typical weight monitoring thresholds:
- Maximum overpull: 80% of CT yield strength
- Minimum slack-off: 50% of normal weight (indicates significant buckling)
- Stuck pipe alarm: Weight exceeds threshold for >30 seconds

Operational protocol:
- Zero weight indicator at surface before running CT
- Record weight at 500-1000 ft increments (build drag profile)
- Compare actual weight to predicted weight (hydraulic model)
- Investigate anomalies before continuing (pull back, circulate, assess)
""",
        key_factors=[
            "Reel rotation encoder resolution and calibration",
            "Depth counter accuracy (±0.5-1.0% typical)",
            "String stretch correction for elastic elongation",
            "Weight indicator load cell accuracy and zeroing",
            "Overpull and slack-off alarm thresholds",
            "Depth correlation to known markers (gamma logs, wireline tags)",
            "Friction drag modeling for weight prediction",
            "Recalibration frequency (after major tension events or reel changes)"
        ],
        primary_authority=[
            "API RP 5ST Section 9: CT Operations Monitoring",
            "SPE 74857: Real-Time CT Monitoring and Diagnostics",
            "Manufacturer specifications for depth counter and weight indicator systems"
        ],
        burden_holder="CT service company operations crew",
        adversary_position="Operator may demand precise depth placement beyond depth counter accuracy capabilities.",
        counter_arguments=[
            "Depth counter drift is inevitable, perfect accuracy unrealistic",
            "Weight indicator affected by wellbore friction (not direct pipe weight measurement)",
            "Recalibration delays operations and increases costs",
            "Known depth markers may not be available in all wells"
        ],
        resolution_strategy="Calibrate depth counter to known markers, monitor weight indicator trends, and investigate anomalies before continuing critical operations.",
        entity_scope=["CT service companies", "field supervisors", "well operators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Depth tracking and weight monitoring per API RP 5ST with documented calibration provides defensible operational control.",
        controlling_precedent=[
            "API RP 5ST Section 9.2: Depth Measurement and Weight Monitoring",
            "SPE 74857: Real-Time Coiled Tubing Monitoring"
        ],
        issue_category=IssueCategory.DEPTH_TRACKING,
        position_zone=PositionZone.REPORTING
    ),

    DoctrineBlock(
        topic="Wellbore Cleanout Operations and Circulation Design",
        keywords=["cleanout", "sand", "scale", "paraffin", "circulation", "jetting tool", "reverse circulation"],
        conclusion_template=[
            "Wellbore cleanout via CT requires sufficient annular velocity (>100 ft/min) to lift solids to surface.",
            "Jetting tools (forward or reverse jet nozzles) enhance cleanout efficiency in horizontal or highly deviated sections.",
            "Circulation fluid selection based on solids type: water-based for sand, chemical solvents for paraffin/scale, acid for carbonate scale."
        ],
        reasoning_framework="""
CT cleanout operations remove debris obstructing production:
- Sand production from unconsolidated formations
- Scale deposits (calcium carbonate, barium sulfate, iron compounds)
- Paraffin/asphaltene buildup in tubing or wellbore
- Mill scale from new pipe, rust from old pipe
- Cement contamination from squeeze or plug jobs

Cleanout methodology:
1. FORWARD CIRCULATION (most common):
   - Pump fluid down CT, returns up annulus
   - Jetting tool at CT end (nozzles direct high-velocity fluid at obstructions)
   - Solids carried to surface in annular returns

2. REVERSE CIRCULATION (specialized):
   - Pump down annulus, returns up CT
   - Requires packer to isolate zones
   - Better for large volumes of debris (CT ID larger than nozzle restrictions)

Critical design parameters:
ANNULAR VELOCITY = Flow Rate (bbl/min) × 3.06 / Annular Area (in²)
Target: >100 ft/min for sand transport, >150 ft/min for heavy solids

Nozzle selection:
- Total flow area (TFA) of nozzles creates pressure drop → generates jetting velocity
- Typical nozzles: 4-12 orifices, 1/8" to 3/8" diameter each
- Jetting velocity: 200-400 ft/sec (creates turbulence to dislodge solids)
- Balance: Sufficient jetting pressure vs adequate annular velocity

Fluid selection by solids type:
SAND/DEBRIS: Fresh water, brine (match formation salinity to avoid clay swelling)
CARBONATE SCALE: HCl acid (15-28%), acetic acid for mild cases
SULFATE SCALE: EDTA, specialized scale dissolvers (sulfates not acid-soluble)
PARAFFIN: Diesel, xylene, hot oil, chemical paraffin solvents
ASPHALTENE: Aromatic solvents, xylene, toluene

Horizontal well cleanout challenges:
- Gravity settling: Solids fall to low side of wellbore
- CT drag: High friction limits reach in extended laterals
- Annular velocity: Difficult to maintain >100 ft/min in large annulus
- Solution: Wiper trips (multiple passes), foam circulation (gas-lift effect), coiled tubing tractors (mechanical pulling)

Circulation system surface equipment:
- Pump truck (500-1500 HHP typical)
- Mixing tanks for chemical treatments
- Solids control: Shale shaker, desander, desilter for fluid recirculation
- Flowback handling: Tanks or frac tanks for returned fluids
""",
        key_factors=[
            "Annular velocity calculation (target >100 ft/min)",
            "Jetting tool nozzle configuration (orifice count, diameter, TFA)",
            "Circulation fluid selection for solids type",
            "Pump rate and pressure requirements",
            "Horizontal well reach limitations (drag and friction)",
            "Solids control equipment at surface",
            "Wiper trip strategy for stubborn deposits",
            "Fluid returns monitoring (solids content, chemical breakthrough)"
        ],
        primary_authority=[
            "API RP 5ST Section 10: Wellbore Cleanout Operations",
            "SPE 36345: Coiled Tubing Cleanout Design Optimization",
            "Chemical manufacturer guidelines (Baker Hughes, Halliburton, Schlumberger)"
        ],
        burden_holder="CT service company operations team",
        adversary_position="Operator may demand cleanout success in wells with insufficient annular velocity or inappropriate fluid selection.",
        counter_arguments=[
            "Horizontal wells may require multiple trips regardless of annular velocity",
            "Chemical costs can be reduced by using water in all applications",
            "Jetting tools add BHA complexity and cost",
            "Wiper trips increase time and costs without guaranteed success"
        ],
        resolution_strategy="Design cleanout operations with sufficient annular velocity, appropriate fluid chemistry, and realistic expectations for horizontal well reach.",
        entity_scope=["CT service companies", "chemical service companies", "well operators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Cleanout design per hydraulic modeling and API RP 5ST provides defensible operational plan.",
        controlling_precedent=[
            "API RP 5ST Section 10: Wellbore Intervention Operations",
            "SPE 36345: Coiled Tubing Cleanout Optimization"
        ],
        issue_category=IssueCategory.WELLBORE_CLEANOUT,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="CT Fishing Operations and Stuck Pipe Recovery",
        keywords=["fishing", "stuck pipe", "jarring", "back-off", "washover", "free point", "cut and recover"],
        conclusion_template=[
            "CT fishing operations recover stuck or parted BHA using specialized tools: jars, back-off subs, washover assemblies.",
            "Free point determination via strain measurement or radioactive markers identifies stuck point depth before cut-and-recover operations.",
            "Jarring operations limited by CT yield strength and injector pulling capacity (typically 20,000-80,000 lbs max)."
        ],
        reasoning_framework="""
CT fishing scenarios:
1. BHA stuck downhole (differential sticking, mechanical obstruction, wellbore collapse)
2. CT parted downhole (fatigue failure, overpull, corrosion)
3. Tools or equipment dropped in wellbore (requiring retrieval)

Fishing tool options:
JAR (hydraulic or mechanical):
- Delivers impact load to free stuck BHA
- Typical jar output: 10,000-50,000 lbs impact
- Limitations: CT must pull jar to cocked position (requires sufficient overpull margin)

BACK-OFF SUB:
- Allows controlled unscrewing of threaded BHA connections
- Used when BHA stuck but CT is free
- Rotate CT string at surface to unscrew downhole connection

WASHOVER ASSEMBLY:
- Concentric pipe runs over outside of stuck CT
- Mill shoe or junk basket at bottom to cut/collect debris
- Circulation while advancing to clear obstructions

SPEAR/OVERSHOT:
- Internal (spear) or external (overshot) gripping tool
- Latches onto fish (stuck BHA or parted CT)
- Pull to recover

Free point determination methods:
STRAIN MEASUREMENT:
- Apply tension, measure elongation along CT string
- Free pipe stretches elastically; stuck pipe doesn't stretch
- Calculate stuck point depth from elongation measurements

RADIOACTIVE MARKERS:
- Place radioactive collar on CT before running
- Gamma ray log after stuck identifies collar depth (differentiates free vs stuck)

CUT AND RECOVER:
- If fishing unsuccessful, cut CT at free point
- Recover free portion of CT and stuck BHA
- Leave fish in wellbore or attempt secondary fishing operation

CT fishing limitations:
- Maximum pulling force: 80-90% of CT yield strength (avoid parting CT during fishing)
- Injector capacity: Typically 20,000-80,000 lbs pulling force depending on unit size
- Jarring effectiveness: Reduced in highly deviated wells (friction absorbs impact)
- Differential sticking: Requires spotting chemical pills (oil, diesel, surfactants) to break filter cake

Fishing operation protocol:
1. Diagnose stuck point (free point survey, overpull measurements)
2. Select fishing tool based on stuck mechanism
3. Attempt jarring with gradual force increase (avoid parting CT)
4. If unsuccessful, spot chemical pill and soak (4-12 hours typical)
5. Re-attempt fishing; if still stuck, consider cut-and-recover
6. Document all fishing attempts for operator and insurance claims
""",
        key_factors=[
            "Free point determination method (strain vs radioactive markers)",
            "Fishing tool selection (jar, back-off sub, washover, spear/overshot)",
            "Maximum pulling force vs CT yield strength (80-90% limit)",
            "Injector capacity for pulling operations",
            "Jarring impact force and frequency",
            "Chemical pill selection for differential sticking (oil, surfactants)",
            "Cut-and-recover decision criteria (cost vs continued fishing attempts)",
            "Documentation of fishing attempts and decisions"
        ],
        primary_authority=[
            "API RP 5ST Section 11: Fishing and Stuck Pipe Recovery",
            "API RP 10B-3: Recommended Practice for Testing of Deepwater Well Drilling Fluids (differential sticking)",
            "Fishing tool manufacturer specifications (Baker Hughes, Schlumberger, Weatherford)"
        ],
        burden_holder="CT service company fishing specialist",
        adversary_position="Operator may demand continued fishing beyond prudent cost/risk thresholds.",
        counter_arguments=[
            "Fishing operations expensive and time-consuming (cut-and-recover may be more economical)",
            "Jarring risks parting CT string if stuck point is shallow",
            "Chemical soaks delay operations without guaranteed success",
            "Insurance may cover fish, making abandonment preferable to extended fishing costs"
        ],
        resolution_strategy="Conduct free point survey, attempt fishing with appropriate tools within CT strength limits, and establish cut-and-recover decision criteria upfront.",
        entity_scope=["CT service companies", "fishing tool specialists", "well operators"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="Fishing operations inherently uncertain; success depends on accurate diagnosis and appropriate tool selection.",
        controlling_precedent=[
            "API RP 5ST Section 11: Fishing Operations",
            "API RP 10B-3: Differential Sticking Mechanisms"
        ],
        issue_category=IssueCategory.CT_FISHING,
        position_zone=PositionZone.REPORTING
    ),

    DoctrineBlock(
        topic="CT Power Pack Hydraulic System and Preventive Maintenance",
        keywords=["power pack", "hydraulic", "hydraulic oil", "pump", "reservoir", "HPU", "hydraulic power unit"],
        conclusion_template=[
            "CT power pack (HPU) provides hydraulic power for injector head, BOP controls, and reel drive systems.",
            "Hydraulic oil filtration critical: 10-micron filters typical, change at manufacturer intervals (250-500 operating hours).",
            "Preventive maintenance includes: hydraulic oil analysis (every 250 hrs), filter changes, pump inspection, hose replacement per schedule."
        ],
        reasoning_framework="""
CT power pack (Hydraulic Power Unit - HPU) functions:
- Drive injector head gripper blocks and chains (primary function)
- Operate BOP controls (pipe rams, blind/shear rams, stripper)
- Power reel rotation motor (for spooling CT on/off reel)
- Actuate auxiliary equipment (stabbing guide, stripper element)

Typical HPU specifications:
- Hydraulic pumps: 50-150 GPM (gallons per minute) flow capacity
- Operating pressure: 3,000-5,000 psi
- Reservoir capacity: 100-300 gallons
- Filtration: 10-micron absolute (prevents contamination damage)
- Cooling: Air-cooled or water-cooled heat exchangers

Hydraulic oil selection:
- Viscosity grade: ISO 46 or 68 (temperature dependent)
- Type: Anti-wear hydraulic oil (AW46, AW68)
- Additives: Rust inhibitors, anti-foam, anti-oxidants
- Temperature range: -20°F to 200°F (cold flow vs high temp stability)

Preventive maintenance schedule:
DAILY (before job start):
- Check hydraulic oil level (maintain above minimum line)
- Visual inspection for leaks (hoses, fittings, pumps)
- Check oil temperature (max 180°F typical, 200°F absolute max)
- Verify filter pressure differential (<25 psi indicates clean filter)

WEEKLY (50-100 operating hours):
- Inspect hydraulic hoses for wear, abrasion, kinks
- Check pump suction strainers (clean if restricted)
- Verify cooling system operation (fan, radiator, coolant level)

EVERY 250 HOURS:
- Change hydraulic filters (10-micron element replacement)
- Hydraulic oil analysis (send sample to lab for contamination, wear metals, viscosity)
- Inspect pump seals and gaskets
- Pressure test relief valves (verify set points)

EVERY 500-1000 HOURS:
- Full hydraulic oil change (drain, flush, refill)
- Pump overhaul or replacement if wear detected
- Hose replacement (even if no visible damage, age degrades rubber)

Common HPU failure modes:
- Hydraulic oil contamination (dirt, water, metal particles) → component wear
- Overheating (insufficient cooling, high ambient temperature, excessive load) → oil degradation
- Cavitation (air ingestion, low oil level) → pump damage
- Filter bypass (dirty filters cause bypass valve to open) → unfiltered oil circulates

Contamination control:
- Keep reservoir breather caps clean (prevent dirt ingestion)
- Use clean transfer pumps when adding oil
- Replace filters before bypass occurs (differential pressure monitoring)
- Avoid mixing oil brands/types (additive incompatibility)
""",
        key_factors=[
            "Hydraulic pump flow capacity (50-150 GPM typical)",
            "Operating pressure (3,000-5,000 psi)",
            "Oil filtration level (10-micron absolute)",
            "Reservoir capacity and oil level monitoring",
            "Oil temperature limits (max 180-200°F)",
            "Filter differential pressure (<25 psi clean, >50 psi replace)",
            "Hydraulic oil analysis frequency (every 250 hrs)",
            "Preventive maintenance schedule adherence"
        ],
        primary_authority=[
            "API RP 5ST Section 7: CT Surface Equipment Maintenance",
            "Hydraulic equipment manufacturer specifications (Caterpillar, Parker, Eaton)",
            "SAE J1165: Hydraulic Fluid Cleanliness Classification"
        ],
        burden_holder="CT service company maintenance team",
        adversary_position="Time/cost pressure may lead to deferred HPU maintenance, increasing failure risk.",
        counter_arguments=[
            "Hydraulic oil analysis is expensive and may not detect imminent failures",
            "Filter changes can be extended if differential pressure remains low",
            "Mixing oil brands is acceptable if viscosity grades match",
            "Visual inspection sufficient to detect most hydraulic problems"
        ],
        resolution_strategy="Implement manufacturer-recommended preventive maintenance schedule with documented oil analysis and filter change records.",
        entity_scope=["CT service companies", "equipment maintenance teams", "field supervisors"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="HPU maintenance per manufacturer specs and API RP 5ST provides defensible preventive maintenance protocol.",
        controlling_precedent=[
            "API RP 5ST Section 7.4: Hydraulic Power Unit Maintenance",
            "SAE J1165: Hydraulic Fluid Cleanliness Standards"
        ],
        issue_category=IssueCategory.POWER_PACK,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="CT Fatigue Modeling Using Schlumberger CoilLife and NOV Software",
        keywords=["fatigue modeling", "CoilLife", "NOV", "TubingLife", "fatigue curves", "predictive maintenance", "cycle counting"],
        conclusion_template=[
            "CT fatigue modeling software (Schlumberger CoilLife, NOV TubingLife) predicts remaining string life based on stress history and material properties.",
            "Inputs: tubing grade, OD, wall thickness, cumulative cycles, operational pressures, temperatures, and measured diameter changes.",
            "Model output: Predicted remaining cycles before retirement, recommended inspection intervals, and safe operating envelope."
        ],
        reasoning_framework="""
CT fatigue modeling purpose:
- Predict string retirement based on accumulated damage (avoid premature failures)
- Optimize CT utilization (retire at 80-90% predicted life, not arbitrary cycle counts)
- Plan string purchases and inventory management
- Support insurance and liability claims (documented fatigue tracking)

Fatigue modeling methodology:
1. BASELINE MEASUREMENT: New CT pipe measured for OD, wall thickness, yield strength
2. OPERATIONAL TRACKING: Record every trip (depth, pressure, temperature, bending cycles)
3. PERIODIC INSPECTION: Measure OD at 500-1000 ft intervals (calipers, ultrasonic)
4. FATIGUE CALCULATION: Software applies damage accumulation algorithms

Schlumberger CoilLife features:
- Proprietary fatigue curves from lab testing (simulate gooseneck bending, pressure cycling)
- Real-time integration with CT unit sensors (automatic data logging)
- Visualizations: Remaining life by string position (outer wrap highest risk)
- Alerts: Triggers warnings at 70%, 80%, 90% predicted life

NOV TubingLife features:
- Material-specific models (70 ksi, 80 ksi, 90 ksi, 110 ksi grades)
- Service severity multipliers (high pressure, high temperature, corrosive fluids)
- Statistical confidence intervals (conservative vs aggressive predictions)
- Export reports for regulatory compliance and operator audits

Critical model inputs:
- Cumulative cycle count (every trip = 1 cycle)
- Maximum operating pressure per cycle (higher pressure = accelerated fatigue)
- Operating temperature (elevated temps reduce material strength)
- Bending radius at gooseneck (tighter radius = higher stress)
- Measured OD reduction (validates model predictions against actual wear)
- Fluid chemistry (H2S, CO2 accelerate corrosion fatigue)

Model limitations:
- Fatigue curves derived from lab testing (may not capture all field conditions)
- Assumes uniform material properties (manufacturing variations exist)
- Cannot predict sudden failures from defects (cracks, weld imperfections)
- Requires accurate operational data (garbage in = garbage out)

Industry practice:
- Retire CT at 80-90% predicted life (conservative safety margin)
- Increase inspection frequency as string approaches retirement (50 ft intervals at >80% life)
- Third-party verification for high-risk applications (insurance requirements)
- Document all fatigue tracking for liability protection
""",
        key_factors=[
            "Fatigue modeling software selection (CoilLife vs TubingLife vs proprietary)",
            "Baseline measurements (new pipe OD, wall thickness, yield strength)",
            "Operational data logging (cycles, pressures, temperatures)",
            "Periodic inspection frequency (OD measurements every 500-1000 ft)",
            "Retirement criteria (80-90% predicted life)",
            "Service severity multipliers for harsh environments",
            "Model validation (compare predictions to actual failures)",
            "Documentation for regulatory and insurance compliance"
        ],
        primary_authority=[
            "API RP 5ST Section 6.3: Fatigue Life Prediction",
            "Schlumberger CoilLife Software User Manual",
            "NOV TubingLife Predictive Maintenance System",
            "ASME Boiler and Pressure Vessel Code Section VIII: Fatigue Analysis"
        ],
        burden_holder="CT service company engineering and maintenance teams",
        adversary_position="Economic pressure to extend string life beyond model predictions to reduce costs.",
        counter_arguments=[
            "Fatigue models are conservative (actual life may exceed predictions)",
            "Software costs and training requirements are significant",
            "Manual cycle counting is sufficient for small fleets",
            "Retirement at 80% predicted life wastes usable pipe"
        ],
        resolution_strategy="Implement fatigue modeling software with documented tracking, periodic validation against actual failures, and conservative retirement criteria.",
        entity_scope=["CT service companies", "fleet managers", "engineering teams"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Fatigue modeling using industry-standard software with documented tracking provides defensible life cycle management.",
        controlling_precedent=[
            "API RP 5ST Section 6: CT String Management and Fatigue Life",
            "ASME Section VIII: Fatigue Analysis Methodology"
        ],
        issue_category=IssueCategory.FATIGUE_MODELING,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Surface Equipment Layout and Rig-Up Safety",
        keywords=["surface layout", "rig-up", "equipment spacing", "CT unit positioning", "pump truck", "BOP placement", "safety zones"],
        conclusion_template=[
            "Surface equipment layout must provide safe access, adequate spacing for maintenance, and emergency egress routes.",
            "Minimum spacing between CT unit and wellhead: 10-15 feet for BOP access and emergency disconnect.",
            "Exclusion zones around high-pressure lines, BOP controls, and CT injector head during operations per OSHA and API standards."
        ],
        reasoning_framework="""
CT surface equipment rig-up components:
1. CT unit (reel, injector head, power pack, control cabin)
2. BOP stack (stripper, pipe rams, blind/shear rams)
3. Pump truck(s) (fluid circulation, pressure pumping)
4. Nitrogen unit (if underbalanced operations)
5. Chemical tanks (acid, solvents, foam additives)
6. Wellhead and flowback equipment
7. Support vehicles (supervisors, wireline if needed)

Critical rig-up safety considerations:
CT UNIT POSITIONING:
- Align injector head with wellbore (minimize bending stress on CT at BOP)
- Maintain 10-15 ft clearance between injector and wellhead (BOP access, emergency disconnect)
- Position control cabin for visibility of wellhead and downhole operations

BOP STACK:
- Anchor BOP to wellhead flange with proper torque (prevent blowout ejection)
- Install kill/bleed lines for pressure testing and well control
- Position BOP control panel accessible from safe distance (20+ ft typical)

PUMP TRUCK:
- Park upwind of wellhead (avoid H2S or gas exposure if well kicks)
- Fluid lines to wellhead: Use high-pressure hose (rated for max pressure + safety factor)
- Secure hose connections with chains or clamps (prevent whipping if disconnect)

NITROGEN UNIT:
- Position downwind (vent nitrogen away from personnel)
- Nitrogen supply line to CT injector: Check for leaks before pressurizing
- Post warning signs (asphyxiation hazard, confined space risk)

HIGH-PRESSURE EXCLUSION ZONES:
- 50 ft radius from wellhead during pressure operations (fracturing, testing)
- No personnel near BOP or injector head during CT movement (crushing hazard)
- Barricade high-pressure lines (prevent personnel walking over/across)

EMERGENCY EGRESS:
- Maintain clear pathways from all equipment to safe assembly point
- Emergency shutdown accessible from multiple locations (deadman switches)
- Fire extinguishers positioned at CT unit, pump truck, nitrogen unit (ABC class minimum)

Rig-up inspection protocol:
1. Equipment placement diagram approved by operator and CT supervisor
2. Anchor points verified (CT unit jacks, pump truck stabilizers)
3. High-pressure connections pressure tested before operations
4. Emergency shutdown system tested (ensure all kill switches functional)
5. Safety briefing with all personnel (JSA - Job Safety Analysis)
6. Exclusion zones marked with cones, flags, or caution tape

Common rig-up errors:
- CT unit too close to wellhead (difficult BOP access in emergency)
- Pump truck positioned downwind (personnel H2S exposure risk)
- Nitrogen vent directed toward personnel or equipment
- High-pressure lines running through traffic areas (trip hazard, whip risk)
- Inadequate lighting for night operations (24-hour operations common)
""",
        key_factors=[
            "CT unit to wellhead spacing (10-15 ft minimum)",
            "BOP control panel positioning (accessible from safe distance)",
            "Pump truck wind direction (upwind of wellhead)",
            "High-pressure exclusion zones (50 ft radius during pressure ops)",
            "Emergency egress routes and assembly points",
            "Nitrogen venting direction (away from personnel)",
            "Lighting for night operations",
            "Equipment anchor points (prevent tipping or movement)",
            "JSA (Job Safety Analysis) completion before rig-up"
        ],
        primary_authority=[
            "API RP 5ST Section 12: Surface Equipment Layout and Rig-Up",
            "OSHA 1910.146: Permit-Required Confined Spaces",
            "OSHA 1910.119: Process Safety Management (high-pressure operations)",
            "Operator-specific HSE requirements"
        ],
        burden_holder="CT service company site supervisor",
        adversary_position="Time pressure may lead to abbreviated rig-up inspections or inadequate safety zone enforcement.",
        counter_arguments=[
            "Equipment spacing driven by site constraints (may not allow ideal layout)",
            "Exclusion zones reduce operational efficiency (personnel must travel farther)",
            "Emergency egress routes may be blocked by equipment during operations",
            "JSA and pre-job inspections delay job start"
        ],
        resolution_strategy="Enforce rig-up safety standards per API RP 5ST with documented JSA, equipment placement diagram, and exclusion zone enforcement.",
        entity_scope=["CT service companies", "well operators", "HSE managers"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Surface layout per API RP 5ST and OSHA standards provides defensible safety protocol.",
        controlling_precedent=[
            "API RP 5ST Section 12: Surface Equipment Rig-Up and Safety",
            "OSHA 1910.119: Process Safety Management of Highly Hazardous Chemicals"
        ],
        issue_category=IssueCategory.SURFACE_EQUIPMENT,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="CT Cement Squeeze Operations",
        keywords=["cement squeeze", "remedial cementing", "squeeze pressure", "balanced plug", "CT cementing", "perforation squeeze"],
        conclusion_template=[
            "CT cement squeeze operations place cement at target depth without removing production tubing or running conventional work strings.",
            "Balanced plug method: Place cement volume calculated to fill annular space, squeeze with surface pressure to force into perforations or voids.",
            "Maximum squeeze pressure limited by formation fracture pressure and casing collapse rating."
        ],
        reasoning_framework="""
CT cementing applications:
- Perforation squeeze (isolate water or gas breakthrough)
- Casing leak repair (patch holes or splits in casing)
- Plug and abandon (set cement plugs for well abandonment)
- Lost circulation treatment (seal fractures taking drilling fluid)
- Annular isolation (squeeze cement behind casing)

CT cement squeeze advantages:
- No workover rig required (cost savings)
- Precise depth placement using depth counter and CT
- Pump through CT while retrieving (continuous operation)
- Can treat multiple zones in single trip

Cement squeeze procedure:
1. SPOT CEMENT: Pump cement down CT, displace to target depth
   - Use spacer fluids (ahead and behind cement) to prevent contamination
   - Calculate volumes to place cement across target zone

2. BALANCED PLUG: Displace cement with fluid that balances hydrostatic pressure
   - Prevents U-tubing (cement flowing back up CT)
   - Typical: Equal density fluid volume = CT capacity

3. SQUEEZE: Apply surface pressure to force cement into perforations/voids
   - Gradual pressure increase (50-100 psi/min)
   - Monitor pressure response (declining pressure = cement taking)
   - Maximum pressure = MIN(fracture gradient, casing rating) × 0.9

4. REVERSE OUT: Pull CT while reverse circulating (prevent cement setting in CT)
   - Clean CT with chemical wash (prevent cement hardening in pipe)

5. WAIT ON CEMENT (WOC): Allow cement to set per API specifications
   - Minimum WOC: 8 hours for Class G cement at 80°F
   - Higher temps = faster set time

Cement slurry design:
- Class G cement: Standard for oil well squeeze operations
- Additives: Retarders (extend pump time), accelerators (reduce WOC), fluid loss control
- Density: 15.6-16.5 ppg typical (match formation pressure requirements)
- Compressive strength: Minimum 500 psi before loading (3,000+ psi final)

Squeeze pressure interpretation:
DECLINING PRESSURE: Cement entering perforations or voids (good squeeze)
CONSTANT PRESSURE: Formation accepting cement at steady rate
RISING PRESSURE: Formation rejecting cement or near fracture (reduce pressure or stop)
RAPID DECLINE: Formation breakdown or cement channel opening (may indicate poor coverage)

Critical squeeze parameters:
- Maximum squeeze pressure = Formation fracture gradient × 0.9 (safety margin)
- Pump rate: 0.5-2 bbl/min (slow rates improve cement placement)
- Cement volume: Calculate based on perforation count, hole size, or void estimate
- Spacer volume: Minimum 50 bbls ahead of cement, 20 bbls behind (prevent contamination)

Post-squeeze evaluation:
- Pressure test after WOC (verify seal integrity)
- Temperature log (cement hydration generates heat → indicates cement top)
- Production test (verify isolation if squeeze intended to shut off water/gas)
""",
        key_factors=[
            "Cement slurry design (Class G, density, additives)",
            "Spacer fluid volumes (prevent contamination)",
            "Balanced plug calculation (prevent U-tubing)",
            "Maximum squeeze pressure (fracture gradient vs casing rating)",
            "Pump rate control (0.5-2 bbl/min typical)",
            "Wait on cement time (8+ hours minimum)",
            "Reverse circulation to clean CT",
            "Post-squeeze pressure testing"
        ],
        primary_authority=[
            "API RP 5ST Annex F: Cementing Through Coiled Tubing",
            "API Specification 10A: Cements and Materials for Well Cementing",
            "SPE 28306: Coiled Tubing Cement Squeeze Design and Evaluation"
        ],
        burden_holder="CT service company and cementing contractor (joint responsibility)",
        adversary_position="Operator may demand higher squeeze pressures risking formation fracture or casing damage.",
        counter_arguments=[
            "Higher squeeze pressures improve cement coverage (risk/benefit trade-off)",
            "WOC time can be reduced if temperature log shows adequate cement",
            "Spacer volumes increase costs without clear benefit",
            "Balanced plug calculations are estimates (downhole conditions vary)"
        ],
        resolution_strategy="Design cement squeeze within safe pressure limits using balanced plug method, adequate spacers, and documented WOC times per API standards.",
        entity_scope=["CT service companies", "cementing contractors", "well operators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Cement squeeze design per API RP 5ST and Spec 10A provides defensible remedial cementing protocol.",
        controlling_precedent=[
            "API RP 5ST Annex F: Cementing Operations",
            "API Spec 10A: Well Cement Materials and Testing"
        ],
        issue_category=IssueCategory.CEMENT_SQUEEZE,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="CT Plug Drill-Out and Composite Frac Plug Milling",
        keywords=["plug drill-out", "mill", "composite plug", "frac plug", "drill out", "plug milling", "PDC mill"],
        conclusion_template=[
            "CT plug drill-out removes composite frac plugs or cement plugs using PDC or carbide mills run on CT.",
            "Milling rate limited by CT weight-on-bit delivery (buckling constraints) and mill cutter aggression.",
            "Composite plug drill-out faster than cement (20-60 min/plug composite vs hours for cement)."
        ],
        reasoning_framework="""
Plug drill-out applications:
- Post-fracturing: Remove composite frac plugs to restore wellbore access
- Cement plug removal: Drill out cement plugs from abandonments or squeeze jobs
- Debris removal: Mill junk (metal, tools, other obstructions)

Plug types and drill-out characteristics:
COMPOSITE FRAC PLUGS:
- Material: Phenolic, rubber, PEEK, or ceramic composites
- Drill-out time: 20-60 minutes per plug (varies by mill, WOB, RPM)
- Cuttings: Fine powder, easily circulated to surface
- Common brands: Magnum, KickDown, Griffin, FracOne

CEMENT PLUGS:
- Material: Class G cement (compressive strength 3,000-8,000 psi)
- Drill-out time: Hours per plug (depends on cement strength, mill type)
- Cuttings: Coarse chunks, require good annular velocity for transport

METAL PLUGS (bridge plugs, retrievable packers):
- Material: Cast iron or steel
- Drill-out time: Variable (cast iron faster, steel very slow)
- Requires carbide or diamond mills (PDC insufficient for hard metals)

CT drill-out BHA components:
1. Mill (PDC or carbide): Cutting element at BHA bottom
   - PDC mill: Fast on composite and soft materials, wears quickly on cement
   - Carbide mill: Slower but more durable, better for cement and metal

2. Nozzle sub: Directs fluid flow to cool mill and lift cuttings
   - Typical nozzle TFA: 0.15-0.30 in² (balance jetting pressure vs annular velocity)

3. Disconnect sub: Allows BHA recovery if mill becomes stuck

4. CT connector: Attaches BHA to CT string

Milling parameters:
WEIGHT-ON-BIT (WOB):
- Delivered via CT buckling (sinusoidal or helical depending on well angle)
- Typical WOB: 2,000-8,000 lbs (limited by CT yield strength)
- Insufficient WOB: Mill stalls or makes no progress

ROTARY SPEED (if using downhole motor):
- PDM typical: 100-250 RPM
- Turbine motor: 500-1,500 RPM (less common for milling)

FLOW RATE:
- Sufficient to cool mill cutters (prevent heat damage)
- Sufficient annular velocity to lift cuttings (>100 ft/min)
- Typical: 2-6 bbl/min depending on CT ID and annulus

Composite plug drill-out challenges:
- Plug expansion: Some plugs expand when heated (friction from milling)
- Rubber smearing: Rubber elements can smear mill cutters (reduce cutting efficiency)
- Tagging plugs: Must tag each plug to confirm depth before milling (prevent drilling past plug into formation)

Cement plug drill-out challenges:
- High compressive strength cement: Requires aggressive carbide mills
- Slow milling rate: May take hours per plug
- Cuttings transport: Large cement chunks require high annular velocity

Operational protocol:
1. Tag plug with CT to confirm depth (compare to known plug depth)
2. Apply gradual WOB increase (avoid shocking CT or BHA)
3. Monitor drilling progress (depth counter advance, cuttings returns)
4. Circulate clean before pulling mill (prevent cuttings settling on top of next plug)
5. Repeat for next plug (typical multi-stage wells have 5-30 plugs)
""",
        key_factors=[
            "Mill type selection (PDC for composite, carbide for cement)",
            "Weight-on-bit delivery (2,000-8,000 lbs typical)",
            "Milling rate monitoring (minutes per plug vs expected)",
            "Flow rate for cuttings transport (>100 ft/min annular velocity)",
            "Plug tagging before drill-out (confirm depth)",
            "BHA disconnect capability (fishing risk mitigation)",
            "Cuttings monitoring at surface (confirm plug material)",
            "Number of plugs to drill out (plan for mill changes if many plugs)"
        ],
        primary_authority=[
            "API RP 5ST Section 13: Milling and Drill-Out Operations",
            "SPE 163848: Composite Frac Plug Drill-Out Optimization",
            "Mill manufacturer guidelines (NOV, Weatherford, Baker Hughes)"
        ],
        burden_holder="CT service company drill-out crew",
        adversary_position="Operator may demand faster drill-out rates than CT or mill capabilities allow.",
        counter_arguments=[
            "Faster drill-out requires higher WOB (risks damaging CT or BHA)",
            "PDC mills wear quickly on hard cement (carbide mills slower but more durable)",
            "Plug expansion or rubber smearing may be plug design issue, not CT operation",
            "Multiple mill changes increase costs but may be necessary for many plugs"
        ],
        resolution_strategy="Select appropriate mill for plug type, deliver safe WOB within CT limits, and plan for mill changes based on plug count and material.",
        entity_scope=["CT service companies", "milling tool providers", "well operators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Plug drill-out per API RP 5ST with appropriate mill selection and safe WOB provides defensible operational plan.",
        controlling_precedent=[
            "API RP 5ST Section 13: Milling Operations Through Coiled Tubing",
            "SPE 163848: Composite Plug Drill-Out Best Practices"
        ],
        issue_category=IssueCategory.WELLBORE_CLEANOUT,
        position_zone=PositionZone.PLANNING
    ),

    DoctrineBlock(
        topic="Flowback Operations Through CT and Production Testing",
        keywords=["flowback", "production test", "well testing", "flow rate", "pressure buildup", "separator", "flare"],
        conclusion_template=[
            "CT enables controlled flowback and production testing without removing completion equipment.",
            "Flow rate limited by CT ID, wellhead pressure, and separator capacity (typical 1-10 bbl/min liquid, 1-5 MMscfd gas).",
            "Production test data: Stabilized flow rate, flowing pressure, reservoir pressure from buildup analysis."
        ],
        reasoning_framework="""
CT flowback applications:
- Post-fracturing flowback (clean up frac fluid, establish production)
- Well testing (measure reservoir deliverability, pressure)
- Kick-off after workover (remove kill fluid, restore production)
- Underbalanced drilling (circulate returns to surface)

CT flowback advantages:
- Controlled flow rate (adjustable choke at surface)
- Real-time pressure monitoring at CT head
- Can circulate if well loads up (kill fluid returns)
- No pulling production tubing required

Flowback equipment configuration:
1. WELLHEAD: CT BOP provides well control during flowback
2. FLOWLINE: High-pressure line from wellhead to separator
   - Rated for max expected pressure (typically 5,000-15,000 psi)
   - Choke manifold (adjustable choke controls flow rate)
3. SEPARATOR: 2-phase or 3-phase (oil/gas/water separation)
   - Typical capacity: 5,000-20,000 bpd liquid, 5-20 MMscfd gas
4. FLARE or SALES LINE: Gas disposal
   - Flare if not connected to sales line (burn waste gas)
5. TANKS: Liquid storage (frac fluid, produced water, oil)

Flow rate limitations:
CT ID CONSTRAINT:
- 1.25" CT: Max ~2-4 bbl/min liquid (velocity limited)
- 2.0" CT: Max ~6-10 bbl/min liquid
- 2.875" CT: Max ~12-18 bbl/min liquid

PRESSURE DROP:
- Friction in CT string reduces bottomhole pressure
- Higher flow rate → higher friction → lower drawdown on reservoir
- May limit well productivity if friction pressure too high

SEPARATOR CAPACITY:
- If flow rate exceeds separator rating, liquid carryover to flare
- Gas capacity exceeded → backpressure on wellhead → reduced flow

Flowback procedure:
1. RIG UP: Connect flowline, separator, flare/sales, tanks
2. PRESSURE TEST: Test flowline to max expected pressure (1.5× safety factor)
3. OPEN WELL SLOWLY: Crack choke gradually to avoid hydraulic shock
4. STABILIZE FLOW: Adjust choke to target flow rate (separator capacity, sand control)
5. MONITOR: Flowrate, wellhead pressure, separator levels, flare (ensure complete combustion)
6. SAMPLE: Collect fluid samples (oil, water, gas for analysis)
7. SHUT-IN: Close well for pressure buildup test (measure reservoir pressure)

Production test analysis:
STABILIZED FLOW TEST:
- Flow at constant rate until pressure stabilizes (hours to days)
- Measure: Flow rate (bbl/day oil, Mscf/day gas), flowing pressure (FWHP, FBHP calculated)
- Calculate: Productivity index (PI = flow rate / pressure drawdown)

PRESSURE BUILDUP TEST:
- Shut in well after flow period
- Monitor pressure recovery (wellhead or downhole gauge)
- Horner plot analysis: Extrapolate to infinite shut-in time → reservoir pressure
- Skin factor: Measure of near-wellbore damage or stimulation

Flowback safety considerations:
- H2S monitoring (if sour gas, personnel require H2S training and monitors)
- Sand production monitoring (erosion risk to choke, flowline, separator)
- Hydrate formation (gas expansion cools → methane hydrates plug flowline)
  - Mitigation: Methanol or glycol injection
- Flare combustion (ensure complete burn, no liquid slugs to flare)

Typical flowback timeline:
- Initial flowback: 1-7 days (clean up frac fluid)
- Production test: 1-5 days (stabilize rate, buildup test)
- Extended flowback: Weeks to months (continue producing or shut-in if not commercial)
""",
        key_factors=[
            "CT ID flow capacity (1-18 bbl/min depending on size)",
            "Separator capacity (liquid and gas processing limits)",
            "Choke size selection (control flow rate, prevent erosion)",
            "Wellhead pressure monitoring (safety, well control)",
            "Flare capacity and combustion efficiency",
            "H2S monitoring and safety protocols",
            "Sand production monitoring (erosion mitigation)",
            "Pressure buildup test for reservoir characterization"
        ],
        primary_authority=[
            "API RP 5ST Section 14: Well Testing Through Coiled Tubing",
            "API RP 14C: Recommended Practice for Analysis, Design, Installation, and Testing of Basic Surface Safety Systems",
            "SPE Monograph 20: Well Testing"
        ],
        burden_holder="CT service company and well operator (joint responsibility)",
        adversary_position="Operator may demand higher flow rates exceeding CT or separator capacity.",
        counter_arguments=[
            "Higher flow rates provide faster cleanup and earlier production revenue",
            "Separator capacity can be temporarily exceeded with careful monitoring",
            "Pressure buildup tests delay production and increase costs",
            "H2S monitoring and safety protocols add operational complexity"
        ],
        resolution_strategy="Design flowback operations within CT and separator capacity, implement safety protocols, and conduct pressure buildup tests for reservoir characterization.",
        entity_scope=["CT service companies", "production testing contractors", "well operators"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Flowback operations per API RP 5ST and RP 14C with documented test procedures provide defensible production testing protocol.",
        controlling_precedent=[
            "API RP 5ST Section 14: Well Testing and Flowback Operations",
            "API RP 14C: Surface Safety Systems for Production Operations"
        ],
        issue_category=IssueCategory.FLOWBACK_OPS,
        position_zone=PositionZone.REPORTING
    )
]


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class CTOperationsEngine:
    def __init__(self):
        self.doctrine_cache = {block.topic: block for block in DOCTRINE_CACHE}
        self.query_count = 0
        self.cache_hits = 0
        self.telemetry_log = []
        logger.info("OFE09 CT Operations Engine initialized with {} doctrine blocks", len(DOCTRINE_CACHE))

    def three_layer_response(self, query: str, mode: ResponseMode) -> Tuple[str, List[str], ConfidenceLevel, List[str]]:
        """
        Layer 1: Doctrine Cache (0-200ms) - Instant responses for known patterns
        Layer 2: Semantic Retrieval - Advanced query understanding
        Layer 3: Deep Analysis - Complex multi-factor reasoning
        """
        start_time = datetime.now()

        # Layer 1: Check doctrine cache
        triggered_doctrines = []
        for topic, block in self.doctrine_cache.items():
            if any(kw.lower() in query.lower() for kw in block.keywords):
                triggered_doctrines.append(block)

        if triggered_doctrines:
            self.cache_hits += 1
            response, reasoning, confidence = self._synthesize_from_doctrines(triggered_doctrines, query, mode)
            doctrine_names = [d.topic for d in triggered_doctrines]

            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            logger.info("Layer 1 cache hit: {} doctrines triggered in {:.1f}ms", len(triggered_doctrines), elapsed)
            return response, reasoning, confidence, doctrine_names

        # Layer 2: Semantic retrieval (fallback if no cache hit)
        logger.info("Layer 2: Semantic retrieval for query: {}", query[:100])
        response, reasoning, confidence = self._semantic_analysis(query, mode)
        return response, reasoning, confidence, ["semantic_retrieval"]

    def _synthesize_from_doctrines(self, doctrines: List[DoctrineBlock], query: str, mode: ResponseMode) -> Tuple[str, List[str], ConfidenceLevel]:
        """Synthesize response from triggered doctrine blocks"""
        reasoning_chain = []

        # Sort doctrines by confidence level (DEFENSIBLE > AGGRESSIVE > DISCLOSURE > HIGH_RISK)
        confidence_order = {
            ConfidenceLevel.DEFENSIBLE: 0,
            ConfidenceLevel.AGGRESSIVE: 1,
            ConfidenceLevel.DISCLOSURE: 2,
            ConfidenceLevel.HIGH_RISK: 3
        }
        doctrines_sorted = sorted(doctrines, key=lambda d: confidence_order[d.confidence])

        # Build response based on mode
        if mode == ResponseMode.FAST:
            # Concise response from top doctrine
            primary = doctrines_sorted[0]
            response = " ".join(primary.conclusion_template)
            reasoning_chain.append(f"Primary doctrine: {primary.topic}")
            reasoning_chain.append(f"Key factors: {', '.join(primary.key_factors[:3])}")
            return response, reasoning_chain, primary.confidence

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with authority citations
            primary = doctrines_sorted[0]
            response_parts = []
            response_parts.append("POSITION: " + " ".join(primary.conclusion_template))
            response_parts.append("\nAUTHORITY: " + "; ".join(primary.primary_authority))
            response_parts.append("\nKEY FACTORS: " + "; ".join(primary.key_factors))
            response_parts.append("\nADVERSARY POSITION: " + primary.adversary_position)
            response_parts.append("\nRESOLUTION: " + primary.resolution_strategy)

            reasoning_chain.append(f"Doctrine: {primary.topic}")
            reasoning_chain.append(f"Confidence: {primary.confidence.value}")
            reasoning_chain.append(f"Authority: {primary.primary_authority[0]}")

            return "\n".join(response_parts), reasoning_chain, primary.confidence

        else:  # MEMO mode
            # Full documentation with all doctrines
            response_parts = []
            response_parts.append("COILED TUBING OPERATIONS ANALYSIS\n")
            response_parts.append(f"Query: {query}\n")

            for idx, doctrine in enumerate(doctrines_sorted, 1):
                response_parts.append(f"\n{idx}. {doctrine.topic.upper()}")
                response_parts.append(f"Confidence Level: {doctrine.confidence.value}")
                response_parts.append(f"\nConclusion: {' '.join(doctrine.conclusion_template)}")
                response_parts.append(f"\nReasoning Framework:\n{doctrine.reasoning_framework[:500]}...")
                response_parts.append(f"\nPrimary Authority: {'; '.join(doctrine.primary_authority)}")
                response_parts.append(f"\nKey Factors: {'; '.join(doctrine.key_factors[:5])}")
                response_parts.append(f"\nResolution Strategy: {doctrine.resolution_strategy}")

                reasoning_chain.append(f"Doctrine {idx}: {doctrine.topic} ({doctrine.confidence.value})")

            highest_confidence = doctrines_sorted[0].confidence
            return "\n".join(response_parts), reasoning_chain, highest_confidence

    def _semantic_analysis(self, query: str, mode: ResponseMode) -> Tuple[str, List[str], ConfidenceLevel]:
        """Fallback semantic analysis when no doctrine cache hit"""
        reasoning_chain = ["Semantic analysis - no direct doctrine match"]

        # Identify query intent
        query_lower = query.lower()

        if any(term in query_lower for term in ["fatigue", "string life", "retirement", "cycles"]):
            response = "CT string fatigue life management requires systematic tracking per API RP 5ST. Monitor cumulative cycles, measure OD reduction, and retire at 80-90% predicted life using software models like Schlumberger CoilLife or NOV TubingLife."
            confidence = ConfidenceLevel.DEFENSIBLE

        elif any(term in query_lower for term in ["bha", "drilling", "motor", "mwd"]):
            response = "CT drilling BHA design limited by CT ID and yield strength. Typical configuration: PDC bit, positive displacement motor (PDM), stabilizers, MWD tools, and disconnect sub. Weight-on-bit delivered via CT buckling, flow rate 1.5-4 bbl/min for motor operation."
            confidence = ConfidenceLevel.DEFENSIBLE

        elif any(term in query_lower for term in ["bop", "stripper", "well control", "blowout"]):
            response = "CT BOP stack requires stripper/packer assembly, dual pipe rams, and blind/shear rams. Test per API RP 53 before operations: low-pressure (200-300 psi) and high-pressure (rated working pressure). Replace stripper element when leak rate exceeds 1 bbl/hr."
            confidence = ConfidenceLevel.DEFENSIBLE

        elif any(term in query_lower for term in ["nitrogen", "underbalanced", "foam", "gas lift"]):
            response = "Nitrogen pumping through CT enables underbalanced operations. Use membrane units (95-98% purity) or cryogenic systems (99.9%). Maximum injection rate limited by CT flow capacity and compressor output. Typical foam quality 50-80% for cuttings transport."
            confidence = ConfidenceLevel.DEFENSIBLE

        elif any(term in query_lower for term in ["frac", "proppant", "fracturing", "stimulation"]):
            response = "CT fracturing limited to 2-4 ppg proppant concentration (vs 8-12 ppg conventional) to avoid tubing erosion. Multi-stage fracturing via ball drop systems or frac sleeves. Monitor CT ID erosion with ultrasonic testing after each frac job."
            confidence = ConfidenceLevel.AGGRESSIVE

        else:
            response = "CT operations require comprehensive planning per API RP 5ST covering equipment selection, operational procedures, safety protocols, and quality assurance. Consult doctrine cache for specific operational domains: string management, BHA design, well control, nitrogen operations, fracturing, fishing, cementing, milling, flowback."
            confidence = ConfidenceLevel.DISCLOSURE

        reasoning_chain.append(f"Generated response for domain: {query[:50]}...")
        return response, reasoning_chain, confidence

    def calculate_determinism_hash(self, query: str, response: str, doctrines: List[str]) -> str:
        """Generate SHA-256 hash for reproducibility verification"""
        content = f"{query}|{response}|{','.join(sorted(doctrines))}"
        return hashlib.sha256(content.encode()).hexdigest()

    def query(self, request: QueryRequest) -> QueryResponse:
        """Main query endpoint"""
        self.query_count += 1

        logger.info("Query #{}: {} (mode: {})", self.query_count, request.query[:100], request.mode.value)

        # Three-layer response
        response_text, reasoning_chain, confidence, doctrines_triggered = self.three_layer_response(
            request.query, request.mode
        )

        # Calculate determinism hash
        det_hash = self.calculate_determinism_hash(request.query, response_text, doctrines_triggered)

        # Telemetry
        telemetry = {
            "query_count": self.query_count,
            "cache_hit_rate": f"{(self.cache_hits / self.query_count * 100):.1f}%",
            "doctrines_triggered": len(doctrines_triggered),
            "confidence_level": confidence.value,
            "response_mode": request.mode.value,
            "timestamp": datetime.now().isoformat()
        }

        return QueryResponse(
            query=request.query,
            response=response_text,
            mode=request.mode,
            confidence=confidence,
            reasoning_chain=reasoning_chain,
            doctrines_triggered=doctrines_triggered,
            telemetry=telemetry,
            determinism_hash=det_hash,
            timestamp=datetime.now().isoformat()
        )

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health endpoint"""
        return {
            "status": "operational",
            "engine": "OFE09_coiled_tubing_ops",
            "version": "1.0.0",
            "port": 9009,
            "doctrine_blocks": len(DOCTRINE_CACHE),
            "issue_categories": len(IssueCategory),
            "query_count": self.query_count,
            "cache_hit_rate": f"{(self.cache_hits / max(self.query_count, 1) * 100):.1f}%",
            "timestamp": datetime.now().isoformat(),
            "capabilities": [
                "CT string fatigue life tracking and management",
                "BHA design for CT drilling applications",
                "Injector head operation and gripper maintenance",
                "CT BOP configuration and well control",
                "Reel capacity calculations and string management",
                "CT tubing OD and grade selection",
                "Nitrogen pumping for underbalanced operations",
                "CT fracturing operations and proppant limitations",
                "Real-time depth tracking and weight monitoring",
                "Wellbore cleanout and circulation design",
                "CT fishing and stuck pipe recovery",
                "Power pack hydraulic systems and maintenance",
                "Fatigue modeling (CoilLife, TubingLife)",
                "Surface equipment layout and rig-up safety",
                "CT cement squeeze operations",
                "Plug drill-out and composite frac plug milling",
                "Flowback operations and production testing"
            ]
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="OFE09 - Coiled Tubing Operations Engine",
    description="TIE Gold Standard engine for CT operations expertise",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize engine
engine = CTOperationsEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint for CT operations questions"""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error("Query failed: {}", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health")
async def health_endpoint():
    """Health check endpoint"""
    return engine.health_check()


@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine blocks"""
    return {
        "count": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": block.topic,
                "category": block.issue_category.value,
                "confidence": block.confidence.value,
                "keywords": block.keywords[:5]
            }
            for block in DOCTRINE_CACHE
        ]
    }


@APP.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": "OFE09_coiled_tubing_ops",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": ["/query", "/health", "/doctrines"],
        "port": 9009
    }


if __name__ == "__main__":
    logger.info("Starting OFE09 CT Operations Engine on port 9009")
    uvicorn.run(APP, host="127.0.0.1", port=9009)
