"""
AUTO14 Steering Systems Analysis Engine
TIE-Grade Intelligence Engine for Automotive Steering Technology

Covers: Power steering diagnostics, EPS analysis, rack and pinion systems,
steering geometry, steer-by-wire, steering column assessment, alignment theory,
hydraulic power steering, electronic control systems, torque sensors, and failure analysis.

Port: 9324
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
import uvicorn


# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class ResponseMode(str, Enum):
    """Response modes for different use cases"""
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
    """Steering system issue categories"""
    POWER_STEERING_HYDRAULIC = "POWER_STEERING_HYDRAULIC"
    ELECTRIC_POWER_STEERING = "ELECTRIC_POWER_STEERING"
    RACK_AND_PINION = "RACK_AND_PINION"
    STEERING_GEOMETRY = "STEERING_GEOMETRY"
    STEER_BY_WIRE = "STEER_BY_WIRE"
    STEERING_COLUMN = "STEERING_COLUMN"
    ALIGNMENT_THEORY = "ALIGNMENT_THEORY"
    TORQUE_SENSORS = "TORQUE_SENSORS"
    CONTROL_MODULES = "CONTROL_MODULES"
    FAILURE_MODES = "FAILURE_MODES"
    DIAGNOSTIC_PROCEDURES = "DIAGNOSTIC_PROCEDURES"
    SAFETY_SYSTEMS = "SAFETY_SYSTEMS"


class AuthorityLevel(str, Enum):
    """Authority hierarchy for steering engineering"""
    SAE_STANDARD = "SAE_STANDARD"
    OEM_SPECIFICATION = "OEM_SPECIFICATION"
    ENGINEERING_TEXTBOOK = "ENGINEERING_TEXTBOOK"
    FIELD_DATA = "FIELD_DATA"
    EXPERT_OPINION = "EXPERT_OPINION"


AUTHORITY_WEIGHTS = {
    AuthorityLevel.SAE_STANDARD: 1.0,
    AuthorityLevel.OEM_SPECIFICATION: 0.95,
    AuthorityLevel.ENGINEERING_TEXTBOOK: 0.85,
    AuthorityLevel.FIELD_DATA: 0.75,
    AuthorityLevel.EXPERT_OPINION: 0.60,
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Input model for steering system queries"""
    query: str = Field(..., description="Steering system question or scenario")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    vehicle_info: Optional[Dict[str, str]] = Field(default=None, description="Vehicle make/model/year")


class DoctrineMatch(BaseModel):
    """Matched doctrine block"""
    topic: str
    confidence: float
    conclusion: str
    authority: AuthorityLevel
    reasoning_preview: str


class QueryResponse(BaseModel):
    """Output model for steering analysis"""
    query_id: str
    conclusion: str
    confidence: ConfidenceLevel
    matched_doctrines: List[DoctrineMatch]
    reasoning: Optional[str] = None
    safety_warnings: List[str] = Field(default_factory=list)
    technical_details: Optional[Dict[str, Any]] = None
    determinism_hash: str
    latency_ms: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float


# ============================================================================
# DOCTRINE BLOCK STRUCTURE
# ============================================================================

@dataclass
class DoctrineBlock:
    """Core doctrine knowledge block"""
    topic: str
    keywords: Set[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: AuthorityLevel
    controlling_precedent: List[str]
    confidence: ConfidenceLevel
    issue_category: IssueCategory
    safety_critical: bool = False
    counter_arguments: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)


# ============================================================================
# DOCTRINE CACHE - 25+ EXPERT BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Hydraulic Power Steering Fluid Contamination",
        keywords={"fluid", "contamination", "hydraulic", "power steering", "dirty", "metal", "particles"},
        conclusion_template="Contaminated power steering fluid indicates wear, seal failure, or pump degradation. Flush system, replace filter, inspect for source.",
        reasoning_framework="""
1. Fluid analysis reveals contaminant type (metal particles = pump wear, black = seal degradation, milky = water ingress)
2. Metal particles suggest internal pump wear or rack seal failure
3. Water contamination indicates seal breach or reservoir cap failure
4. Color change to dark brown/black indicates oxidized fluid from overheating
5. Immediate flush required to prevent accelerated wear
6. Source identification critical: pump, rack, hoses, or reservoir
7. Filter inspection shows contamination rate and particle size
8. System pressure test post-flush validates repair
        """,
        key_factors=[
            "Fluid color and clarity",
            "Presence of metal particles",
            "Water contamination indicators",
            "System operating temperature",
            "Pump noise correlation",
            "Rack seal condition",
            "Filter element inspection"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2658 - Power Steering Fluid Requirements",
            "OEM fluid specification compliance",
            "Hydraulic system contamination standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.POWER_STEERING_HYDRAULIC,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Electric Power Steering Torque Sensor Drift",
        keywords={"EPS", "torque sensor", "drift", "calibration", "offset", "electric power steering"},
        conclusion_template="Torque sensor drift causes steering assist errors. Recalibrate using OEM scan tool, validate with road test under varying loads.",
        reasoning_framework="""
1. EPS torque sensor measures driver input to calculate assist level
2. Sensor drift causes over-assist or under-assist conditions
3. Temperature-dependent drift suggests sensor aging
4. Calibration procedure requires wheels straight, engine running
5. Zero-point offset critical for proper assist curve
6. Post-calibration validation tests light/heavy steering inputs
7. Persistent drift after calibration indicates sensor replacement needed
8. Module adaptation may require drive cycle completion
        """,
        key_factors=[
            "Torque sensor offset value",
            "Assist level correlation",
            "Temperature coefficient",
            "Calibration success rate",
            "DTC presence (C0460, C0461)",
            "Steering angle sensor agreement",
            "Driver complaint specificity"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "ISO 26262 functional safety for EPS",
            "OEM calibration procedures",
            "Torque sensor specification tolerances"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TORQUE_SENSORS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Rack and Pinion Inner Tie Rod Wear",
        keywords={"inner tie rod", "rack", "pinion", "play", "clunk", "wear", "looseness"},
        conclusion_template="Inner tie rod wear produces clunking during direction changes. Replace both sides, perform alignment, verify no rack damage.",
        reasoning_framework="""
1. Inner tie rod connects rack to outer tie rod via threaded socket
2. Wear occurs at ball joint interface and rack threads
3. Clunking heard during steering direction reversal
4. Dry park test reveals play: rock wheel while feeling tie rod
5. Both sides replaced regardless of individual condition (paired wear)
6. Rack housing threads inspected for damage
5. Torque specification critical: 40-74 ft-lbs typical, varies by vehicle
6. Alignment mandatory post-replacement (toe affected)
7. Boot integrity checked to prevent future contamination
        """,
        key_factors=[
            "Clunk timing relative to steering input",
            "Amount of play measured in inches",
            "Boot condition and grease presence",
            "Rack thread condition",
            "Outer tie rod condition",
            "Wheel bearing noise differentiation",
            "Steering angle sensor response"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J490 - Tie Rod Socket Assemblies",
            "OEM torque specifications",
            "Alignment angle tolerances"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.RACK_AND_PINION
    ),

    DoctrineBlock(
        topic="Ackermann Steering Geometry Principles",
        keywords={"ackermann", "geometry", "toe curve", "steering angle", "kingpin", "scrub radius"},
        conclusion_template="Ackermann geometry ensures inner wheel turns sharper than outer during cornering. Deviations cause tire scrub and uneven wear.",
        reasoning_framework="""
1. Ackermann principle: inner wheel must trace smaller radius than outer
2. Achieved via angled steering arms pointing toward rear axle centerline
3. Perfect Ackermann rarely used; parallel or reverse Ackermann common
4. Toe curve measured: difference in wheel angles at full lock
5. 100% Ackermann: lines from steering arms intersect at rear axle center
6. Parallel steering: equal angles both wheels (oval track racing)
7. Reverse Ackermann: outer wheel turns more (high-speed stability)
8. Scrub radius affects steering feel and return-to-center
        """,
        key_factors=[
            "Steering arm angle relative to chassis",
            "Toe curve measurement at lock",
            "Kingpin inclination angle",
            "Scrub radius positive/negative",
            "Tire wear pattern correlation",
            "Vehicle application (street vs race)",
            "Suspension geometry interaction"
        ],
        primary_authority=AuthorityLevel.ENGINEERING_TEXTBOOK,
        controlling_precedent=[
            "Milliken & Milliken - Race Car Vehicle Dynamics",
            "SAE J670 - Vehicle Dynamics Terminology",
            "OEM suspension geometry specifications"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.STEERING_GEOMETRY
    ),

    DoctrineBlock(
        topic="Steer-by-Wire Redundancy Architecture",
        keywords={"steer by wire", "redundancy", "fail safe", "electronic", "backup", "SbW"},
        conclusion_template="Steer-by-wire requires dual or triple redundant systems per ISO 26262 ASIL-D. Mechanical backup or independent ECU paths mandatory.",
        reasoning_framework="""
1. No mechanical connection between steering wheel and wheels
2. ISO 26262 ASIL-D required for safety-critical steering function
3. Dual ECU architecture: primary and monitor ECU cross-check commands
4. Triple motor winding design allows two-winding operation on failure
5. Dual power supplies prevent single-point electrical failure
6. Mechanical fallback clutch engages on total system failure (some designs)
7. Continuous self-diagnostics with fail-operational capability
8. Steering angle sensors redundant: resolver + Hall effect typical
        """,
        key_factors=[
            "ECU redundancy level (dual/triple)",
            "Motor winding configuration",
            "Power supply independence",
            "Mechanical backup presence",
            "Sensor redundancy architecture",
            "Fail-operational vs fail-safe mode",
            "Diagnostic coverage percentage",
            "Mean time between failures (MTBF)"
        ],
        primary_authority=AuthorityLevel.SAE_STANDARD,
        controlling_precedent=[
            "ISO 26262 - Functional Safety for Road Vehicles",
            "SAE J3016 - Levels of Driving Automation",
            "OEM steer-by-wire system specifications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.STEER_BY_WIRE,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Steering Column Intermediate Shaft U-Joint Failure",
        keywords={"intermediate shaft", "u-joint", "clunk", "steering column", "coupler", "spline"},
        conclusion_template="Intermediate shaft U-joint wear causes clunking over bumps or during turns. Replace shaft assembly, lubricate splines, verify column alignment.",
        reasoning_framework="""
1. Intermediate shaft connects column to rack pinion via universal joints
2. U-joint wear produces clunk when torque direction changes
3. Spline wear at slip joint causes axial play and noise
4. Rubber coupler deterioration (older vehicles) allows vibration transfer
5. Column misalignment accelerates U-joint wear
6. Grease loss from torn boots causes accelerated wear
7. Replacement requires shaft assembly (U-joints not serviceable)
8. Alignment check ensures column-to-rack angle within spec
        """,
        key_factors=[
            "Clunk timing: turning vs over bumps",
            "U-joint visual wear assessment",
            "Spline play measurement",
            "Boot condition and grease presence",
            "Column-to-rack angle measurement",
            "Coupler condition (if equipped)",
            "Steering wheel return-to-center quality"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2492 - Steering Column Assemblies",
            "OEM service procedures",
            "U-joint angle specifications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.STEERING_COLUMN
    ),

    DoctrineBlock(
        topic="Power Steering Pump Flow and Pressure Testing",
        keywords={"pump", "flow", "pressure", "hydraulic", "psi", "gpm", "relief valve"},
        conclusion_template="Pump flow and pressure tests diagnose assist level issues. Spec: 1000-1500 psi relief, 2-3 GPM flow typical. Low flow indicates pump wear.",
        reasoning_framework="""
1. Pressure test: install gauge in high-pressure line, engine at idle
2. Normal pressure: 80-150 psi at idle, 1000-1500 psi at relief
3. Relief valve test: close valve fully, pressure should hit relief spec
4. Flow test requires flow meter: 2-3 GPM typical at 1500 RPM
5. Low pressure at relief indicates worn pump vanes or housing
6. Excessive pressure suggests restricted lines or stuck relief valve
7. Flow below spec confirms pump replacement needed
8. Cavitation noise indicates aerated fluid or inlet restriction
        """,
        key_factors=[
            "Idle pressure reading",
            "Relief pressure value",
            "Flow rate in GPM",
            "Fluid temperature during test",
            "Pump noise characteristics",
            "Reservoir fluid level stability",
            "Hose condition and routing"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2658 - Power Steering Pumps",
            "OEM pressure and flow specifications",
            "Hydraulic system testing standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.POWER_STEERING_HYDRAULIC
    ),

    DoctrineBlock(
        topic="Electric Power Steering Motor Current Draw Analysis",
        keywords={"EPS motor", "current", "amperage", "assist", "electric", "overcurrent", "resistance"},
        conclusion_template="EPS motor current analysis reveals mechanical binding or electrical faults. Normal: 5-40A depending on assist level. Overcurrent trips module protection.",
        reasoning_framework="""
1. EPS motor current proportional to assist torque required
2. Baseline current: 2-5A at idle, 10-40A during parking maneuvers
3. Overcurrent condition: >60A triggers module protection shutdown
4. High current with low assist suggests mechanical binding (rack, column)
5. Low current with assist complaint indicates motor or module fault
6. Temperature-dependent current rise normal up to 150°F motor temp
7. Current signature analysis reveals commutation faults or winding shorts
8. Scan tool PID monitoring shows real-time current vs commanded assist
        """,
        key_factors=[
            "Peak current during parking maneuver",
            "Baseline current at idle",
            "Current vs assist level correlation",
            "Temperature coefficient",
            "DTC for overcurrent (C0550, C0551)",
            "Motor resistance measured",
            "Module power supply voltage"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "ISO 26262 EPS functional safety",
            "OEM motor current specifications",
            "Electric motor testing standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ELECTRIC_POWER_STEERING,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Toe Angle and Tire Wear Correlation",
        keywords={"toe", "alignment", "tire wear", "feathering", "inside edge", "outside edge"},
        conclusion_template="Toe misalignment causes rapid tire wear. Toe-in wears outside edges, toe-out wears inside edges. Feathering confirms toe issue.",
        reasoning_framework="""
1. Toe: angle of wheels relative to vehicle centerline (top view)
2. Toe-in: front of tires closer than rear (positive toe)
3. Toe-out: front of tires farther apart (negative toe)
4. Toe-in wears outside tire edges due to scrubbing outward
5. Toe-out wears inside edges due to inward scrub
6. Feathering: smooth one side, sharp other side of tread blocks
7. Specification typically 0 degrees +/- 0.1 degrees total toe
8. Adjustment via tie rod length: turn to change toe setting
        """,
        key_factors=[
            "Total toe measurement (degrees or inches)",
            "Individual wheel toe values",
            "Tire wear pattern location",
            "Feathering direction",
            "Steering wheel centering",
            "Recent suspension work",
            "Tie rod adjustment range"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J1100 - Motor Vehicle Dimensions",
            "OEM alignment specifications",
            "Tire wear pattern diagnostic standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ALIGNMENT_THEORY
    ),

    DoctrineBlock(
        topic="Rack and Pinion Hydraulic Seal Leak Diagnosis",
        keywords={"rack seal", "leak", "fluid", "boot", "inner", "outer", "seepage"},
        conclusion_template="Rack seal leaks appear at inner tie rod boots or rack ends. Inner seal leak requires rack replacement; outer seal may be serviceable depending on design.",
        reasoning_framework="""
1. Rack contains three seal locations: inner left, inner right, outer pinion
2. Inner seals prevent fluid loss into tie rod boots
3. Fluid in tie rod boot confirms inner seal failure
4. Outer pinion seal leaks at input shaft (visible externally)
5. Most racks non-rebuildable: seal failure requires rack replacement
6. Some commercial vehicle racks have serviceable seals
7. Leak rate assessment: drips vs seepage affects urgency
8. Fluid loss causes assist degradation and pump damage if ignored
        """,
        key_factors=[
            "Leak location (inner boot vs pinion shaft)",
            "Leak rate severity",
            "Boot fluid contamination",
            "Rack rebuildability per OEM",
            "System fluid level trend",
            "Pump condition correlation",
            "Vehicle mileage and rack age"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2657 - Rack and Pinion Assemblies",
            "OEM rack serviceability specifications",
            "Hydraulic seal failure analysis"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.RACK_AND_PINION,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Steering Angle Sensor Calibration Procedures",
        keywords={"steering angle sensor", "SAS", "calibration", "centering", "ESP", "ABS"},
        conclusion_template="Steering angle sensor requires calibration after alignment or steering component replacement. Procedure: wheels straight, ignition on, scan tool calibration command.",
        reasoning_framework="""
1. SAS provides steering wheel position to ESC, ABS, and EPS systems
2. Calibration zeros sensor with wheels straight ahead
3. Required after: alignment, tie rod replacement, rack replacement, or wheel removal
4. Uncalibrated SAS causes ESC/ABS malfunction and warning lights
5. Procedure varies by OEM: some auto-calibrate via drive cycle
6. Manual calibration via scan tool: wheels straight, ignition on, execute command
7. Validation: turn wheel lock-to-lock, verify sensor reading returns to zero
8. ESC system learns new zero point for stability control calculations
        """,
        key_factors=[
            "DTC presence (C0710, C0800 typical)",
            "ESC/ABS warning lights",
            "Recent steering or suspension work",
            "Wheel alignment status",
            "Calibration success confirmation",
            "Sensor signal quality",
            "Drive cycle completion if auto-learn"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2564 - Steering Angle Sensor",
            "OEM calibration procedures",
            "ESC system integration requirements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.CONTROL_MODULES,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Variable Ratio Steering Analysis",
        keywords={"variable ratio", "progressive", "steering ratio", "rack", "VGS", "speed sensitive"},
        conclusion_template="Variable ratio steering provides quick response at center, slower at lock. Achieved via non-linear rack tooth spacing or active systems (VGS).",
        reasoning_framework="""
1. Constant ratio: same steering wheel degrees per wheel degree throughout
2. Variable ratio: ratio changes with wheel angle (faster on-center)
3. Passive variable ratio: rack tooth spacing varies (mechanical)
4. Active variable ratio (VGS): planetary gear set changes ratio electronically
5. Typical ratios: 12:1 on-center, 18:1 at lock for passive systems
6. VGS systems adjust ratio based on speed: quick at low speed, slower at high speed
7. Diagnostic challenge: VGS module failure causes default fixed ratio
8. Benefit: parking maneuverability with highway stability
        """,
        key_factors=[
            "Steering ratio specification",
            "Ratio change profile",
            "Active vs passive system",
            "VGS module DTCs if equipped",
            "Speed sensor input correlation",
            "Driver complaint specificity",
            "Rack tooth inspection for passive systems"
        ],
        primary_authority=AuthorityLevel.ENGINEERING_TEXTBOOK,
        controlling_precedent=[
            "SAE J670 - Vehicle Dynamics Terminology",
            "OEM variable ratio specifications",
            "VGS system design documentation"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.RACK_AND_PINION
    ),

    DoctrineBlock(
        topic="Power Steering Hose Pressure Rating and Failure",
        keywords={"hose", "pressure line", "burst", "leak", "crimp", "hydraulic line"},
        conclusion_template="Power steering hoses rated 1500-2000 psi. Failure at crimp fittings or age-related cracking. Replace with OEM-spec hose; generic hoses may not meet pressure rating.",
        reasoning_framework="""
1. High-pressure hose: pump to rack, rated 1500-2000 psi
2. Low-pressure hose: rack to reservoir, rated 50-100 psi
3. Failure modes: crimp separation, hose burst, age cracking
4. Crimp fittings most common failure point under pressure cycling
5. Generic hoses may use lower pressure rating or incorrect crimp spec
6. Hose routing critical: heat exposure accelerates degradation
7. Fluid type compatibility required (ATF, synthetic, etc.)
8. Leak location determines if high or low pressure side affected
        """,
        key_factors=[
            "Leak location (crimp vs hose body)",
            "Hose age and exposure to heat",
            "Pressure side vs return side",
            "Hose pressure rating specification",
            "Crimp fitting type and quality",
            "Routing interference or chafing",
            "Fluid type compatibility"
        ],
        primary_authority=AuthorityLevel.SAE_STANDARD,
        controlling_precedent=[
            "SAE J188 - Hydraulic Hose and Hose Assemblies",
            "OEM hose specifications",
            "DOT brake hose standards (similar pressure applications)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.POWER_STEERING_HYDRAULIC
    ),

    DoctrineBlock(
        topic="EPS Motor Position Sensor Hall Effect Failure",
        keywords={"Hall effect", "position sensor", "motor", "EPS", "rotor position", "commutation"},
        conclusion_template="EPS motor Hall sensors provide rotor position for commutation. Sensor failure causes assist loss or erratic assist. Replace motor assembly; sensors not serviceable separately.",
        reasoning_framework="""
1. Brushless DC motor requires rotor position for electronic commutation
2. Three Hall effect sensors spaced 120 degrees detect magnetic pole position
3. Sensor failure causes incorrect commutation timing and torque ripple
4. Complete sensor failure results in no assist (fail-safe mode)
5. Intermittent sensor causes erratic assist and assist loss at specific angles
6. DTCs: C0899 (motor position sensor), C0550 (motor circuit)
7. Oscilloscope waveform analysis shows missing or corrupted Hall signals
8. Motor assembly replacement required; Hall sensors embedded in stator
        """,
        key_factors=[
            "DTC codes present",
            "Assist loss pattern (constant vs angle-dependent)",
            "Hall sensor signal quality on scope",
            "Motor resistance measurement",
            "Connector and wiring integrity",
            "Module power and ground circuits",
            "Temperature correlation (heat-related failure)"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "ISO 26262 EPS safety requirements",
            "OEM motor assembly specifications",
            "Brushless DC motor design standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ELECTRIC_POWER_STEERING,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Kingpin Inclination and Scrub Radius Effects",
        keywords={"kingpin", "KPI", "scrub radius", "SAI", "steering axis inclination", "offset"},
        conclusion_template="Kingpin inclination (SAI) and scrub radius affect steering feel and stability. Positive scrub radius causes pull under braking; negative scrub improves straight-line stability.",
        reasoning_framework="""
1. Kingpin inclination (KPI/SAI): inward tilt of steering axis from vertical
2. Scrub radius: distance between tire contact patch center and steering axis ground intersection
3. Positive scrub radius: steering axis inside contact patch (traditional FWD)
4. Negative scrub radius: steering axis outside contact patch (modern safety design)
5. Negative scrub reduces torque steer and brake pull effects
6. Excessive positive scrub causes steering wheel pull during braking
7. KPI creates camber change during steering (wheel lifts chassis slightly)
8. Scrub radius affected by wheel offset and tire width changes
        """,
        key_factors=[
            "KPI angle measurement (degrees)",
            "Scrub radius measurement (mm or inches)",
            "Wheel offset change from stock",
            "Tire width variance from OEM",
            "Brake pull complaints",
            "Torque steer severity",
            "Steering return-to-center quality"
        ],
        primary_authority=AuthorityLevel.ENGINEERING_TEXTBOOK,
        controlling_precedent=[
            "SAE J670 - Vehicle Dynamics Terminology",
            "Milliken - Race Car Vehicle Dynamics Chapter 17",
            "OEM suspension geometry specifications"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.STEERING_GEOMETRY
    ),

    DoctrineBlock(
        topic="Steering Column Tilt and Telescoping Mechanism Failure",
        keywords={"tilt", "telescope", "column adjustment", "lock", "lever", "stuck"},
        conclusion_template="Tilt/telescope mechanism uses lever-actuated locks or electric motors. Stuck positions indicate bent shafts, worn detents, or motor failure. Inspect for crash damage.",
        reasoning_framework="""
1. Manual tilt: lever releases cam locks, spring pressure allows adjustment
2. Power tilt/telescope: electric motors drive screw or cable mechanisms
3. Failure modes: bent shaft from crash, worn lock detents, broken lever linkage
4. Power systems: motor failure, broken cables, position sensor faults
5. Post-crash inspection critical: column designed to collapse in frontal impact
6. Binding during adjustment suggests bent shaft or misaligned components
7. DTCs for power systems: B1000-B1999 range (body control modules)
8. Replacement may require full column assembly to maintain crash compliance
        """,
        key_factors=[
            "Manual vs power adjustment system",
            "Failure mode (stuck locked vs stuck unlocked)",
            "Recent crash history",
            "Binding or grinding noise during adjustment",
            "Power system DTCs",
            "Position sensor feedback",
            "Lever/switch operation"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "FMVSS 204 - Steering Control Rearward Displacement",
            "SAE J2492 - Steering Column Assemblies",
            "OEM service procedures and crash compliance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.STEERING_COLUMN,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Active Return-to-Center Steering Analysis",
        keywords={"return to center", "self centering", "caster", "active steering", "pull"},
        conclusion_template="Proper return-to-center requires positive caster, aligned steering geometry, and functional assist system. Poor return suggests low caster, binding, or EPS calibration issue.",
        reasoning_framework="""
1. Return-to-center primarily driven by positive caster angle
2. Caster creates self-aligning torque through mechanical trail
3. Low or unequal caster causes poor return and steering pull
4. Binding components (column, rack, ball joints) resist return
5. EPS systems use active return-to-center logic based on speed and angle
6. EPS calibration error causes over-return or under-return
7. Hydraulic systems rely purely on mechanical geometry for return
8. Steering angle sensor input critical for EPS return-to-center algorithm
        """,
        key_factors=[
            "Caster angle measurement (left vs right)",
            "Binding test during manual steering input",
            "EPS vs hydraulic system type",
            "Return-to-center speed and consistency",
            "Steering angle sensor calibration",
            "Ball joint and tie rod condition",
            "Tire pressure and size variance"
        ],
        primary_authority=AuthorityLevel.ENGINEERING_TEXTBOOK,
        controlling_precedent=[
            "SAE J670 - Vehicle Dynamics Terminology",
            "OEM alignment specifications",
            "EPS control algorithm documentation"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.STEERING_GEOMETRY
    ),

    DoctrineBlock(
        topic="Rack and Pinion Mounting Bushing Wear",
        keywords={"rack bushings", "mounting", "clunk", "shimmy", "steering rack", "subframe"},
        conclusion_template="Rack mounting bushing wear allows rack movement, causing clunk and shimmy. Replace bushings, verify subframe torque, check for rack housing damage.",
        reasoning_framework="""
1. Rack mounts to subframe or crossmember via rubber bushings
2. Bushing wear allows rack to shift laterally during cornering or braking
3. Symptoms: clunk over bumps, steering shimmy, vague steering feel
4. Dry park test: rock steering wheel while observing rack movement
5. Torn or collapsed bushings visible during inspection
6. Subframe bolt torque critical: loose bolts mimic bushing wear
7. Aftermarket polyurethane bushings reduce movement but increase NVH
8. Rack housing cracks may develop if bushings failed long ago
        """,
        key_factors=[
            "Bushing visual condition (torn, collapsed, oil-soaked)",
            "Rack lateral movement measurement",
            "Subframe mounting bolt torque",
            "Clunk timing relative to input",
            "Rack housing crack inspection",
            "Steering feel quality (vague vs tight)",
            "Recent pothole or curb impact"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2657 - Rack and Pinion Assemblies",
            "OEM bushing specifications and torque values",
            "Subframe mounting standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.RACK_AND_PINION
    ),

    DoctrineBlock(
        topic="EPS Column-Assist vs Rack-Assist Architecture",
        keywords={"column assist", "rack assist", "EPS", "motor location", "C-EPS", "R-EPS"},
        conclusion_template="Column-assist EPS (C-EPS) mounts motor on column; rack-assist (R-EPS) mounts on rack. C-EPS: lower cost, less assist force. R-EPS: higher assist, better for heavy vehicles.",
        reasoning_framework="""
1. Column-assist (C-EPS): motor and gear reduction on steering column
2. Rack-assist (R-EPS): motor drives rack directly via pinion or ball screw
3. Pinion-assist (P-EPS): motor on rack pinion, mid-range cost/performance
4. C-EPS advantages: lower cost, easier packaging, lighter weight
5. C-EPS disadvantages: limited assist force (mechanical reduction limits)
6. R-EPS advantages: high assist force, better road feel isolation
7. R-EPS disadvantages: higher cost, complex integration, heavier
8. Application: C-EPS for compact cars, R-EPS for trucks/SUVs
        """,
        key_factors=[
            "Motor mounting location",
            "Vehicle weight and application",
            "Assist force requirement",
            "Cost and complexity targets",
            "Packaging space constraints",
            "NVH isolation needs",
            "Road feel quality priorities"
        ],
        primary_authority=AuthorityLevel.ENGINEERING_TEXTBOOK,
        controlling_precedent=[
            "SAE J2564 - Electric Power Steering Systems",
            "OEM EPS architecture design specifications",
            "Automotive engineering textbooks on steering systems"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.ELECTRIC_POWER_STEERING
    ),

    DoctrineBlock(
        topic="Hydraulic Power Steering Pump Belt Failure Effects",
        keywords={"belt", "pump", "serpentine", "squealing", "loss of assist", "hydraulic"},
        conclusion_template="Power steering pump belt failure causes immediate total assist loss. Squealing indicates slip; inspect belt condition, tensioner, and pump bearing. Replace belt and address root cause.",
        reasoning_framework="""
1. Serpentine belt drives power steering pump (and alternator, A/C, water pump)
2. Belt slip causes squealing and reduced pump speed (low assist)
3. Total belt failure causes immediate complete assist loss (heavy steering)
4. Belt condition: cracks, glazing, rib wear indicate replacement needed
5. Tensioner failure allows belt slip: measure tension with gauge
6. Seized pump bearing causes belt overload and rapid wear
7. Pulley misalignment accelerates belt edge wear
8. Emergency operation possible with failed belt but requires high steering effort
        """,
        key_factors=[
            "Belt condition (cracks, glazing, fraying)",
            "Tensioner function and spring tension",
            "Pump bearing noise or roughness",
            "Pulley alignment measurement",
            "Belt width and rib count specification",
            "Pump rotation resistance",
            "Recent belt replacement history"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J1459 - V-Ribbed Belts and Pulleys",
            "OEM belt tension specifications",
            "Accessory drive system standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.POWER_STEERING_HYDRAULIC,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Steering Wheel Vibration Diagnosis (Shimmy vs Shake)",
        keywords={"vibration", "shimmy", "shake", "steering wheel", "wobble", "frequency"},
        conclusion_template="Shimmy: oscillating side-to-side (15-30 Hz) from tire/wheel imbalance or worn steering parts. Shake: vertical vibration from brake or suspension. Frequency analysis differentiates sources.",
        reasoning_framework="""
1. Shimmy: side-to-side oscillation felt in steering wheel (15-30 Hz typical)
2. Shake: vertical or fore-aft vibration (lower frequency, 5-15 Hz)
3. Shimmy sources: tire imbalance, bent wheel, worn tie rods, loose rack bushings
4. Shake sources: brake rotor runout, wheel bearing wear, suspension bushings
5. Speed correlation: tire imbalance worse at specific speed (60-70 mph typical)
6. Acceleration/deceleration correlation: brake rotor runout worse during braking
7. Road test with hands-off steering isolates tire/wheel issues
8. Frequency measurement via stethoscope or vibration analyzer confirms source
        """,
        key_factors=[
            "Vibration type (shimmy vs shake)",
            "Speed range where vibration occurs",
            "Brake application correlation",
            "Tire balance and condition",
            "Wheel runout measurement",
            "Steering component play",
            "Vibration frequency measurement"
        ],
        primary_authority=AuthorityLevel.FIELD_DATA,
        controlling_precedent=[
            "SAE J2002 - Vehicle Vibration Testing",
            "OEM vibration diagnostic procedures",
            "Tire and wheel serviceability standards"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.DIAGNOSTIC_PROCEDURES
    ),

    DoctrineBlock(
        topic="Active Front Steering (AFS) Planetary Gear System",
        keywords={"active front steering", "AFS", "planetary gear", "variable ratio", "lane keeping"},
        conclusion_template="Active Front Steering uses planetary gear set to vary steering ratio electronically. System adds or subtracts angle to driver input. Module failure causes fixed ratio fallback.",
        reasoning_framework="""
1. Planetary gear set sits between column and rack pinion
2. Electric motor rotates ring gear to add/subtract steering angle
3. Low speed: motor adds angle for quick parking maneuvers (10:1 ratio)
4. High speed: motor subtracts angle for stability (20:1 ratio)
5. Lane keeping assist uses AFS to apply corrective steering inputs
6. Self-park systems command AFS motor for autonomous steering
7. Module failure: system defaults to fixed 1:1 ratio (mechanical passthrough)
8. Calibration required after module replacement or steering component service
        """,
        key_factors=[
            "AFS module DTCs",
            "Steering ratio behavior at low vs high speed",
            "Lane keeping or self-park function",
            "Module power and ground circuits",
            "Steering angle sensor calibration",
            "Motor current draw during operation",
            "Planetary gear mechanical condition"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "ISO 26262 functional safety for active steering",
            "SAE J3016 - Driving Automation Levels",
            "OEM AFS system specifications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.CONTROL_MODULES,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Steering Gear Ratio Calculation and Effects",
        keywords={"steering ratio", "gear ratio", "lock to lock", "turns", "quick ratio"},
        conclusion_template="Steering ratio: degrees of steering wheel rotation per degree of wheel turn. Typical: 12:1 to 20:1. Lower ratio (quick steering) requires fewer turns lock-to-lock but increases effort.",
        reasoning_framework="""
1. Steering ratio = steering wheel degrees / road wheel degrees
2. Fast ratio: 12:1 to 14:1, 2.5-3.0 turns lock-to-lock (sports cars)
3. Slow ratio: 18:1 to 22:1, 4.0-5.0 turns lock-to-lock (trucks, older cars)
4. Lower ratio increases steering effort (mechanical disadvantage)
5. Power assist compensates for low ratio effort increase
6. Ratio determined by rack pinion diameter and steering arm length
7. Lock-to-lock turns = total wheel travel / (360 / ratio)
8. Quick ratio racks available as performance upgrade for many vehicles
        """,
        key_factors=[
            "Turns lock-to-lock measurement",
            "Steering ratio specification",
            "Power assist presence and type",
            "Driver effort required at low speed",
            "Rack pinion diameter",
            "Steering arm length",
            "Vehicle application (street, race, truck)"
        ],
        primary_authority=AuthorityLevel.ENGINEERING_TEXTBOOK,
        controlling_precedent=[
            "SAE J670 - Vehicle Dynamics Terminology",
            "OEM steering ratio specifications",
            "Milliken - Race Car Vehicle Dynamics"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.STEERING_GEOMETRY
    ),

    DoctrineBlock(
        topic="EPS Thermal Management and Overheating Protection",
        keywords={"EPS", "overheating", "thermal", "temperature", "assist reduction", "duty cycle"},
        conclusion_template="EPS systems reduce assist when motor temperature exceeds threshold (typically 150°F). Prolonged parking maneuvers trigger thermal protection. Allow cool-down period before full assist returns.",
        reasoning_framework="""
1. EPS motor generates heat during high-current assist (parking maneuvers)
2. Temperature sensor in motor or module monitors thermal state
3. Thermal protection algorithm reduces assist at 140-160°F motor temp
4. Complete assist cutoff at 180-200°F to prevent motor damage
5. Cool-down period required: 5-10 minutes for full assist restoration
6. Frequent thermal events suggest mechanical binding or module fault
7. Duty cycle limits protect system: 30 seconds on, 10 seconds off typical
8. Ambient temperature affects thermal margin: hot climates reduce headroom
        """,
        key_factors=[
            "Motor temperature sensor reading",
            "Assist reduction severity and timing",
            "Recent parking or low-speed maneuvering",
            "Ambient temperature conditions",
            "Mechanical binding inspection",
            "Module cooling airflow",
            "DTC for overtemperature (C0899, C0460)"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "ISO 26262 thermal protection requirements",
            "OEM EPS thermal specifications",
            "Electric motor thermal management standards"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ELECTRIC_POWER_STEERING,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Four-Wheel Steering (4WS) Rear Steering Control",
        keywords={"four wheel steering", "4WS", "rear steering", "all wheel steering", "AWS"},
        conclusion_template="Four-wheel steering turns rear wheels to reduce turning radius (low speed, same direction) or improve stability (high speed, opposite direction). Rear actuator failure causes 4WS disable and handling change.",
        reasoning_framework="""
1. Low-speed 4WS: rear wheels steer same direction as front (tighter turns)
2. High-speed 4WS: rear wheels steer opposite direction (stability, lane change)
3. Transition speed typically 30-50 mph depending on system
4. Rear steering angle: 2-5 degrees typical (much less than front)
5. Electric actuators or hydraulic rams control rear toe change
6. System failure: rear wheels lock to zero toe, 4WS light illuminates
7. Handling change on failure: understeer increases, turning radius widens
8. Calibration required after rear suspension or alignment work
        """,
        key_factors=[
            "4WS system type (electric vs hydraulic)",
            "Speed-dependent steering behavior",
            "Rear steering angle sensor readings",
            "4WS warning light status",
            "Rear actuator DTCs",
            "Handling change description",
            "Recent rear alignment or suspension service"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2564 - Rear Steering Systems",
            "OEM 4WS system specifications",
            "Vehicle dynamics engineering references"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.CONTROL_MODULES,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Steering Column Bearing Noise Diagnosis",
        keywords={"column bearing", "noise", "grinding", "steering column", "bearing wear"},
        conclusion_template="Steering column bearing wear causes grinding or growling noise during steering input. Noise source: upper or lower column bearing. Requires column disassembly; bearings not separately serviceable in most designs.",
        reasoning_framework="""
1. Column contains two main bearings: upper (near steering wheel) and lower (firewall area)
2. Bearing wear produces grinding, growling, or clicking during rotation
3. Noise frequency correlates with steering wheel rotation speed
4. Load-dependent noise: worse under torque (parking) suggests bearing wear
5. Stethoscope isolation: touch column at bearing locations to pinpoint source
6. Some columns have serviceable bearings; most require column assembly replacement
7. Post-crash inspection: impact can damage bearings even if column appears intact
8. Grease loss from torn seals accelerates bearing wear
        """,
        key_factors=[
            "Noise type and frequency",
            "Load dependency (torque applied vs free rotation)",
            "Noise location along column length",
            "Recent crash history",
            "Column bearing serviceability per OEM",
            "Grease presence at bearing seals",
            "Steering shaft endplay measurement"
        ],
        primary_authority=AuthorityLevel.OEM_SPECIFICATION,
        controlling_precedent=[
            "SAE J2492 - Steering Column Assemblies",
            "OEM column bearing specifications",
            "Crash compliance post-repair requirements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.STEERING_COLUMN
    ),

    DoctrineBlock(
        topic="Bump Steer Analysis and Correction",
        keywords={"bump steer", "tie rod", "suspension", "geometry", "roll center", "toe change"},
        conclusion_template="Bump steer: unintended toe change during suspension travel. Caused by non-parallel tie rod and control arm geometry. Correct via tie rod height adjustment or suspension geometry modification.",
        reasoning_framework="""
1. Bump steer: toe change as suspension compresses or extends
2. Ideal: tie rod and lower control arm parallel in side view (no toe change)
3. Tie rod above or below ideal plane causes toe-in or toe-out during bump
4. Test procedure: jack up wheel, measure toe change through suspension travel
5. Acceptable: less than 0.05 degrees toe change per inch of travel
6. Correction: adjustable tie rod ends change tie rod height at rack
7. Lowered vehicles especially prone: suspension geometry altered from stock
8. Severe bump steer causes darting, instability over bumps
        """,
        key_factors=[
            "Toe change per inch of suspension travel",
            "Tie rod angle relative to control arm",
            "Suspension ride height vs stock",
            "Tie rod end adjustability",
            "Driver complaint (darting, tramlining)",
            "Recent suspension modification",
            "Roll center height change from stock"
        ],
        primary_authority=AuthorityLevel.ENGINEERING_TEXTBOOK,
        controlling_precedent=[
            "Milliken - Race Car Vehicle Dynamics Chapter 18",
            "SAE J670 - Vehicle Dynamics Terminology",
            "Suspension geometry design references"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        issue_category=IssueCategory.STEERING_GEOMETRY
    )
]


# ============================================================================
# ENGINE CORE LOGIC
# ============================================================================

class SteeringSystemsEngine:
    """AUTO14 Steering Systems Analysis Engine"""

    def __init__(self):
        self.start_time = datetime.now()
        self.query_count = 0
        self.cache_hits = 0
        self.total_latency_ms = 0.0

        logger.info(f"AUTO14 Steering Systems Engine initialized with {len(DOCTRINE_CACHE)} doctrines")

    def three_layer_response(self, query: str, mode: ResponseMode, context: Optional[Dict] = None) -> QueryResponse:
        """
        Three-layer response architecture:
        1. Doctrine Cache (0-50ms)
        2. Semantic Retrieval (50-200ms) - simulated
        3. Deep Analysis (200-1000ms) - for MEMO mode
        """
        start = datetime.now()
        query_id = str(uuid.uuid4())
        self.query_count += 1

        # Layer 1: Doctrine Cache
        matched = self._search_doctrine_cache(query)

        if matched:
            self.cache_hits += 1
            response = self._build_response_from_cache(query_id, query, matched, mode, context)
        else:
            # Layer 2/3: Would invoke semantic search or deep analysis
            response = self._build_fallback_response(query_id, query, mode)

        latency = (datetime.now() - start).total_seconds() * 1000
        self.total_latency_ms += latency
        response.latency_ms = latency

        # Add determinism hash
        response.determinism_hash = self._compute_determinism_hash(response)

        # Audit trail
        self._log_to_audit_trail(query_id, query, response)

        return response

    def _search_doctrine_cache(self, query: str) -> List[Tuple[DoctrineBlock, float]]:
        """Search doctrine cache for keyword matches"""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        matches = []
        for doctrine in DOCTRINE_CACHE:
            # Calculate keyword overlap
            overlap = len(query_terms & doctrine.keywords)
            if overlap > 0:
                confidence = min(overlap / len(doctrine.keywords), 1.0)
                matches.append((doctrine, confidence))

        # Sort by confidence, return top 5
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:5]

    def _build_response_from_cache(
        self,
        query_id: str,
        query: str,
        matches: List[Tuple[DoctrineBlock, float]],
        mode: ResponseMode,
        context: Optional[Dict]
    ) -> QueryResponse:
        """Build response from matched doctrines"""
        top_match = matches[0][0]

        # Build conclusion
        conclusion = top_match.conclusion_template

        # Add vehicle-specific context if provided
        if context and "vehicle_info" in context:
            vehicle = context["vehicle_info"]
            conclusion = f"[{vehicle.get('year', 'N/A')} {vehicle.get('make', 'N/A')} {vehicle.get('model', 'N/A')}] {conclusion}"

        # Matched doctrines
        doctrine_matches = []
        for doctrine, conf in matches:
            doctrine_matches.append(DoctrineMatch(
                topic=doctrine.topic,
                confidence=conf,
                conclusion=doctrine.conclusion_template,
                authority=doctrine.primary_authority,
                reasoning_preview=doctrine.reasoning_framework[:200] + "..."
            ))

        # Safety warnings
        safety_warnings = []
        for doctrine, _ in matches:
            if doctrine.safety_critical:
                safety_warnings.append(f"SAFETY CRITICAL: {doctrine.topic} - Follow OEM procedures exactly")

        # Mode-dependent reasoning
        reasoning = None
        technical_details = None

        if mode == ResponseMode.DEFENSE or mode == ResponseMode.MEMO:
            reasoning = self._build_detailed_reasoning(matches)
            technical_details = self._extract_technical_details(matches)

        return QueryResponse(
            query_id=query_id,
            conclusion=conclusion,
            confidence=top_match.confidence,
            matched_doctrines=doctrine_matches,
            reasoning=reasoning,
            safety_warnings=safety_warnings,
            technical_details=technical_details,
            determinism_hash="",  # Set later
            latency_ms=0.0,  # Set later
            metadata={
                "mode": mode,
                "cache_hit": True,
                "doctrine_count": len(matches)
            }
        )

    def _build_detailed_reasoning(self, matches: List[Tuple[DoctrineBlock, float]]) -> str:
        """Build detailed reasoning for DEFENSE/MEMO modes"""
        parts = ["DETAILED REASONING:\n"]

        for i, (doctrine, conf) in enumerate(matches, 1):
            parts.append(f"\n{i}. {doctrine.topic} (Confidence: {conf:.2%})")
            parts.append(f"   Authority: {doctrine.primary_authority.value}")
            parts.append(f"   Framework: {doctrine.reasoning_framework[:300]}...")
            parts.append(f"   Key Factors: {', '.join(doctrine.key_factors[:5])}")

        return "\n".join(parts)

    def _extract_technical_details(self, matches: List[Tuple[DoctrineBlock, float]]) -> Dict[str, Any]:
        """Extract technical specifications and measurements"""
        details = {
            "primary_category": matches[0][0].issue_category.value,
            "authority_level": matches[0][0].primary_authority.value,
            "safety_critical": matches[0][0].safety_critical,
            "related_topics": matches[0][0].related_topics,
            "key_factors": matches[0][0].key_factors,
            "controlling_precedent": matches[0][0].controlling_precedent
        }
        return details

    def _build_fallback_response(self, query_id: str, query: str, mode: ResponseMode) -> QueryResponse:
        """Fallback response when no doctrines match"""
        return QueryResponse(
            query_id=query_id,
            conclusion="No specific doctrine matched. General steering system principles apply: inspect components for wear, verify alignment, check fluid levels (hydraulic), scan for DTCs (EPS).",
            confidence=ConfidenceLevel.DISCLOSURE,
            matched_doctrines=[],
            reasoning="No direct doctrine cache hit. Recommend detailed diagnostic procedure based on symptom description." if mode != ResponseMode.FAST else None,
            safety_warnings=["General steering system work requires trained technician and proper tools"],
            determinism_hash="",
            latency_ms=0.0,
            metadata={"mode": mode, "cache_hit": False}
        )

    def _compute_determinism_hash(self, response: QueryResponse) -> str:
        """Compute SHA-256 determinism hash"""
        content = f"{response.query_id}|{response.conclusion}|{response.confidence}|{len(response.matched_doctrines)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _log_to_audit_trail(self, query_id: str, query: str, response: QueryResponse) -> None:
        """Log query to JSONL audit trail"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_id": query_id,
            "query": query,
            "conclusion": response.conclusion,
            "confidence": response.confidence,
            "doctrines_matched": len(response.matched_doctrines),
            "latency_ms": response.latency_ms,
            "determinism_hash": response.determinism_hash
        }
        logger.info(f"AUDIT: {json.dumps(audit_entry)}")

    def get_health(self) -> HealthResponse:
        """Health check endpoint"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        cache_hit_rate = self.cache_hits / self.query_count if self.query_count > 0 else 0.0
        avg_latency = self.total_latency_ms / self.query_count if self.query_count > 0 else 0.0

        return HealthResponse(
            status="healthy",
            engine="AUTO14_steering_systems",
            version="1.0.0",
            port=9324,
            doctrines_loaded=len(DOCTRINE_CACHE),
            uptime_seconds=uptime,
            total_queries=self.query_count,
            cache_hit_rate=cache_hit_rate,
            avg_latency_ms=avg_latency
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="AUTO14 Steering Systems Analysis Engine",
    description="TIE-Grade intelligence for automotive steering diagnostics and analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SteeringSystemsEngine()


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    """Main query endpoint for steering system analysis"""
    try:
        context = request.context or {}
        if request.vehicle_info:
            context["vehicle_info"] = request.vehicle_info

        response = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            context=context
        )
        return response
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_endpoint() -> HealthResponse:
    """Health check endpoint"""
    return engine.get_health()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrines"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "authority": d.primary_authority.value,
                "safety_critical": d.safety_critical
            }
            for d in DOCTRINE_CACHE
        ]
    }


@app.get("/categories")
async def list_categories():
    """List all issue categories"""
    category_counts = {}
    for doctrine in DOCTRINE_CACHE:
        cat = doctrine.issue_category.value
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "categories": [cat.value for cat in IssueCategory],
        "doctrine_distribution": category_counts
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting AUTO14 Steering Systems Analysis Engine on port 9324")
    uvicorn.run(app, host="0.0.0.0", port=9324)
