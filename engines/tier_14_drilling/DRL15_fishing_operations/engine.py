"""
DRL15 Fishing Operations Intelligence Engine v1.0.0
Comprehensive drilling fishing operations analysis and decision support.

Domain Coverage:
- Stuck pipe analysis and free point determination
- Jarring operations and tool selection
- Fishing tool selection (overshots, spears, washover pipe)
- Milling operations (junk mills, section mills, pilot mills)
- Wireline fishing tools and techniques
- Backoff procedures and string shots
- Sidetrack decision criteria and economics
- Fishing job planning and risk assessment
- Stuck pipe prevention strategies

Port: 9265
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to path BEFORE any local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger


# ============================================================================
# ENUMS AND DATA MODELS
# ============================================================================

class ResponseMode(str, Enum):
    """Response detail modes."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class IssueCategory(str, Enum):
    """Fishing operation issue categories."""
    STUCK_PIPE_DIAGNOSIS = "stuck_pipe_diagnosis"
    JARRING_OPERATIONS = "jarring_operations"
    FISHING_TOOL_SELECTION = "fishing_tool_selection"
    MILLING_OPERATIONS = "milling_operations"
    WIRELINE_FISHING = "wireline_fishing"
    BACKOFF_PROCEDURES = "backoff_procedures"
    SIDETRACK_DECISION = "sidetrack_decision"
    FISHING_ECONOMICS = "fishing_economics"
    PREVENTION_STRATEGY = "prevention_strategy"
    FREE_POINT_ANALYSIS = "free_point_analysis"
    WASHOVER_OPERATIONS = "washover_operations"
    FISHING_JOB_PLANNING = "fishing_job_planning"


class AnalysisZone(str, Enum):
    """Position zones for analysis."""
    PLANNING = "PLANNING"
    OPERATIONAL = "OPERATIONAL"
    AUDIT = "AUDIT"


@dataclass
class DoctrineBlock:
    """Structured fishing operations expertise block."""
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
    confidence: ConfidenceLevel
    category: IssueCategory
    zone_applicability: List[AnalysisZone] = field(default_factory=lambda: [AnalysisZone.PLANNING, AnalysisZone.OPERATIONAL])

    def triggered_by(self, query: str) -> bool:
        """Check if doctrine applies to query."""
        query_lower = query.lower()
        return any(kw.lower() in query_lower for kw in self.keywords)


class QueryRequest(BaseModel):
    """Fishing operations query request."""
    query: str = Field(..., description="Fishing operations question or scenario")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.OPERATIONAL, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional operational context")


class QueryResponse(BaseModel):
    """Fishing operations analysis response."""
    query: str
    response: str
    mode: ResponseMode
    zone: AnalysisZone
    confidence: ConfidenceLevel
    triggered_doctrines: List[str]
    source_layer: str
    latency_ms: float
    determinism_hash: str
    timestamp: str


# ============================================================================
# DOCTRINE CACHE - 19 FISHING OPERATIONS EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    # Stuck Pipe Diagnosis
    DoctrineBlock(
        topic="Differential Sticking Mechanism",
        keywords=["differential sticking", "differential stuck", "filter cake", "overbalance pressure", "permeable formation", "pipe embedded"],
        conclusion_template="Differential sticking occurs when drill pipe becomes embedded in filter cake against permeable formation under overbalance pressure. Diagnosis requires correlation of drilling parameters, formation permeability, and pressure differentials.",
        reasoning_framework="""
Primary mechanism: Differential pressure between wellbore and formation presses pipe into filter cake on permeable zone wall. Contact area and pressure differential create holding force exceeding rig pulling capacity.

Diagnostic indicators:
1. Stuck while stationary (not rotating or moving)
2. Occurred in permeable formation (sand, sandstone)
3. High overbalance (ECD >> formation pressure)
4. Thick filter cake from high solids mud
5. Free point near permeable zone contact
6. No circulation loss (wellbore integrity intact)
7. Torque and drag normal before stuck event
8. Rapid onset after stopping motion

Physics: Holding force F = A × ΔP × μ
- A = contact area (pipe OD × length embedded)
- ΔP = pressure differential (overbalance)
- μ = coefficient of friction (filter cake to steel)

Critical factors:
- Contact area increases with time stationary
- Pressure differential from mud weight excess
- Filter cake thickness and composition
- Formation permeability and pressure
- Pipe metallurgy and coating condition

Differential vs mechanical distinction:
- Differential: stuck while static, normal parameters before
- Mechanical: progressive torque/drag increase, motion-related
- Key seating: specific geometry, rotation possible
- Packoff: circulation restricted, cuttings correlation

Free point determination essential: stretch calculation method or electronic free point indicator reveals stuck interval for jar placement and fishing tool selection.

Industry practice: Spot oil-based pill to break filter cake seal, reduce overbalance if safe, apply slow steady pull (not jarring initially), consider backoff above free point if pull unsuccessful.
""",
        key_factors=[
            "Permeable formation presence",
            "Overbalance pressure magnitude",
            "Filter cake quality and thickness",
            "Stationary time duration",
            "Contact area geometry",
            "Mud solids content",
            "Formation pressure regime"
        ],
        primary_authority=[
            "API RP 7G: Recommended Practice for Drill Stem Design and Operating Limits",
            "IADC Drilling Manual: Stuck Pipe Prevention and Fishing Operations",
            "SPE 67707: Analysis of Stuck Pipe in Deviated Boreholes"
        ],
        burden_holder="Operator - prove differential mechanism through parameter correlation",
        adversary_position="Contractor may argue mechanical sticking or hole condition issues",
        counter_arguments=[
            "Torque and drag data shows no progressive increase",
            "Circulation maintained rules out packoff",
            "Free point correlation with permeable zone",
            "No wellbore collapse or key seat geometry"
        ],
        resolution_strategy="Free point determination, spot pill, backoff if necessary",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STUCK_PIPE_DIAGNOSIS
    ),

    DoctrineBlock(
        topic="Mechanical Pipe Sticking Diagnosis",
        keywords=["mechanical sticking", "key seating", "ledge", "dogleg", "hole deviation", "packoff", "cuttings accumulation"],
        conclusion_template="Mechanical sticking results from physical restriction of pipe movement by wellbore geometry or cuttings accumulation. Diagnosis requires analysis of torque and drag trends, hole geometry, and circulation parameters.",
        reasoning_framework="""
Mechanical sticking mechanisms:
1. Key seating: pipe groove worn in dogleg, prevents upward movement
2. Ledge/shoulder: formation irregularity catches tool joint or BHA component
3. Packoff: cuttings accumulation around BHA restricts annular flow
4. Wellbore collapse: shale sloughing or unconsolidated formation failure
5. Undergauge hole: bit size reduction from formation squeeze

Diagnostic differentiation:
Key seating:
- Occurs in doglegs (typically >3 deg/100 ft)
- Pipe rotates freely but won't pull up
- Can often continue drilling down
- Gradual onset as groove deepens

Packoff:
- Circulation pressure increases
- Pump pressure spikes
- Cuttings returns degraded
- Cannot reciprocate up or down

Ledge/shoulder:
- Sudden stop during tripping
- Specific depth correlation
- May feel jar impact at ledge
- Weight indicator shows contact

Key seat prevention: maintain low dogleg severity, ream while tripping, use spiral drill collars in deviated sections, avoid excessive WOB creating groove wear.

Industry approach:
- Key seat: work pipe up/down while rotating, wash and ream, consider string shot backoff
- Packoff: pump sweeps, work pipe, increase annular velocity
- Ledge: jarring down to break ledge, wash and ream past obstruction
- Collapse: stabilize with weighted mud, consider sidetrack if severe

Critical: Do not jar upward on key seat - worsens situation by tightening groove. Jar down or backoff and fish with rotary shoe or section mill.
""",
        key_factors=[
            "Dogleg severity and location",
            "Torque and drag trend analysis",
            "Circulation pressure changes",
            "Cuttings removal efficiency",
            "Hole cleaning parameters",
            "Directional survey data",
            "Formation stability characteristics"
        ],
        primary_authority=[
            "API RP 7G: Drill Stem Design and Operating Limits",
            "SPE 21999: Key Seating - Causes and Prevention",
            "IADC Stuck Pipe Guidelines and Best Practices"
        ],
        burden_holder="Operator - document wellbore conditions and mechanical indicators",
        adversary_position="May argue inadequate hole cleaning or BHA design",
        counter_arguments=[
            "Directional survey confirms dogleg location",
            "Torque trend shows progressive increase",
            "Circulation data proves packoff vs differential",
            "Free point analysis confirms restriction zone"
        ],
        resolution_strategy="Mechanism-specific remediation: backoff, jar, wash/ream, or sidetrack",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STUCK_PIPE_DIAGNOSIS
    ),

    DoctrineBlock(
        topic="Free Point Determination Methods",
        keywords=["free point", "stretch calculation", "free point indicator", "electronic free point", "stuck point", "overpull measurement"],
        conclusion_template="Free point determination identifies the depth where pipe is stuck, essential for jar placement and fishing tool selection. Methods include stretch calculation and electronic free point indicators.",
        reasoning_framework="""
Stretch calculation method:
ΔL = (F × L) / (A × E)
Where:
- ΔL = pipe stretch (inches)
- F = applied tension (lbs)
- L = free pipe length (feet)
- A = pipe cross-sectional area (sq in)
- E = modulus of elasticity (30 × 10^6 psi for steel)

Procedure:
1. Record pipe weight in slips
2. Apply known overpull (e.g., 50,000 lbs)
3. Measure surface stretch at kelly or top drive
4. Calculate free length using formula
5. Stuck point = total depth - free length

Accuracy factors:
- Weight indicator calibration critical
- Account for buoyancy factor
- Consider drill collar vs drill pipe sections
- Temperature effects on E modulus
- Measurement precision at surface

Electronic free point indicator:
- Wireline tool measures pipe elongation downhole
- More accurate than stretch calculation
- Can pinpoint within 10-50 feet typically
- Requires pipe ID clearance for tool passage
- Measures magnetic properties under tension

Tool operation:
1. Lower wireline tool to suspect zone
2. Apply surface tension
3. Tool detects elongation change
4. Free pipe stretches, stuck pipe does not
5. Transition point = stuck point

Applications:
- Jar placement: position 1-2 joints above stuck point
- Backoff location: determine string shot depth
- Fishing tool selection: overshot length calculation
- Economics: determine fish length for recovery value

Industry practice: Use both methods when possible - stretch calculation for initial estimate, electronic tool for confirmation before backoff or fishing operations. Critical for multi-million dollar fishing jobs.
""",
        key_factors=[
            "Overpull magnitude applied",
            "Pipe weight and cross-section accuracy",
            "Buoyancy factor for mud weight",
            "Measurement instrument calibration",
            "Mixed string complications (DP and DC)",
            "Temperature correction factors",
            "Electronic tool selection and operation"
        ],
        primary_authority=[
            "API RP 7G: Recommended Practice for Drill Stem Design",
            "SPE 27490: Free Point Determination and Backoff Operations",
            "Schlumberger Wireline Services Manual: Free Point Tools"
        ],
        burden_holder="Operator - accurate measurements and calculations required",
        adversary_position="Contractor may dispute calculations if backoff fails",
        counter_arguments=[
            "Electronic tool confirmation of calculation",
            "Multiple measurement cross-validation",
            "Instrument calibration records",
            "Successful backoff confirms accuracy"
        ],
        resolution_strategy="Use both methods, document thoroughly, confirm before irreversible operations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FREE_POINT_ANALYSIS
    ),

    # Jarring Operations
    DoctrineBlock(
        topic="Hydraulic vs Mechanical Jar Selection",
        keywords=["hydraulic jar", "mechanical jar", "jar selection", "jarring force", "jar placement", "bumper sub"],
        conclusion_template="Jar type selection depends on stuck mechanism, hole conditions, and required impact force. Hydraulic jars provide controlled force; mechanical jars deliver rapid impact.",
        reasoning_framework="""
Hydraulic jar characteristics:
- Oil or mud-filled chamber with metering system
- Controlled time delay (typically 3-60 seconds)
- Consistent impact force delivery
- Up and down jarring capability
- Force rating: 100,000-500,000 lbs typical
- Suitable for differential sticking, light mechanical stuck

Mechanical jar characteristics:
- Spring-loaded or telescoping mechanical linkage
- Instantaneous release (no time delay)
- Higher peak impact force
- Primarily upward jarring
- Simpler mechanism, more robust
- Better for severe mechanical restrictions

Selection criteria:

For differential sticking:
- Hydraulic jar preferred
- Jarring upward with controlled force
- Time delay allows cuttings to settle
- Place 1-2 joints above stuck point
- Combine with spotting pill

For key seating:
- DO NOT jar upward (worsens key seat)
- Jar downward if attempted
- Consider backoff instead
- Mechanical jar acceptable

For packoff:
- Hydraulic jar with pumping
- Jar downward to break bridge
- Mechanical jar for severe bridges
- Work pipe while circulating

Jar placement calculation:
- Position above stuck point per free point
- Allow drill collar stretch for stroke
- Typical stroke: 2-5 feet
- Need bumper sub or sufficient DC length

Jarring procedure:
1. Slack off to jar
2. Pick up to set desired overpull
3. Continue pulling to cock jar
4. Jar fires when threshold reached
5. Repeat with increasing overpull if needed
6. Maximum attempts: typically 10-15 before alternative

Force calculations:
Static force < Jar impact < Pipe yield strength
Typical: Apply 80% of jar rating maximum

Industry practice: Start with low overpull (50,000-100,000 lbs), increase gradually, monitor for pipe damage, combine jarring with chemical treatment for differential sticking, consider backoff if jarring unsuccessful after 15 attempts.
""",
        key_factors=[
            "Stuck mechanism type",
            "Required impact force magnitude",
            "Hole deviation and geometry",
            "Drill string configuration",
            "Jar stroke length required",
            "Time delay preference",
            "Environmental conditions"
        ],
        primary_authority=[
            "API Spec 7: Specification for Rotary Drill Stem Elements",
            "IADC Fishing and Stuck Pipe Manual",
            "SPE 16661: Jarring Effectiveness in Stuck Pipe Recovery"
        ],
        burden_holder="Operator - proper jar selection and placement engineering",
        adversary_position="May argue inadequate jar specifications if unsuccessful",
        counter_arguments=[
            "Engineering calculations justify jar selection",
            "Placement based on free point analysis",
            "Force ratings appropriate for conditions",
            "Procedure followed industry standards"
        ],
        resolution_strategy="Select jar type for mechanism, calculate placement, follow graduated force protocol",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.JARRING_OPERATIONS
    ),

    DoctrineBlock(
        topic="Jar Placement Engineering",
        keywords=["jar placement", "stroke length", "drill collar stretch", "neutral point", "jar position calculation"],
        conclusion_template="Proper jar placement requires calculating drill collar stretch to achieve required stroke length above the stuck point for effective impact delivery.",
        reasoning_framework="""
Jar placement physics:
The jar must be positioned such that drill collar stretch equals jar stroke length when overpull is applied. This positions the jar's hammer section adjacent to its anvil section just above the stuck point.

Stretch formula:
ΔL = (F × L) / (A × E)
Where:
- ΔL = desired stroke (feet converted to inches)
- F = applied overpull (lbs)
- L = free drill collar length needed (feet)
- A = drill collar cross-section area (sq in)
- E = 30 × 10^6 psi for steel

Rearranged for placement:
L = (ΔL × A × E) / F

Example calculation:
- Desired stroke: 4 feet = 48 inches
- Overpull planned: 100,000 lbs
- 6.5 inch OD × 2.75 inch ID drill collar
- A = π/4 × (6.5^2 - 2.75^2) = 27.23 sq in
- L = (48 × 27.23 × 30×10^6) / 100,000 = 392 feet

Therefore, place jar 392 feet above stuck point.

Practical considerations:
1. Free point determination accuracy critical
2. Account for drill pipe stretch if in string above jar
3. Buoyancy factor reduces effective weight
4. Add safety margin (1-2 joints) above calculated depth
5. Ensure sufficient heavy drill collars below jar

Neutral point consideration:
Above neutral point: pipe in tension (normal)
Below neutral point: pipe in compression (buckling risk)
Jar must be above neutral point to function properly.

Neutral point depth from bit:
NP = (Buoyed weight on bit) / (Buoyed weight per foot of DC)

Common errors:
- Ignoring buoyancy (overstates stretch)
- Using total depth instead of free point
- Insufficient drill collar weight to compress jar
- Forgetting drill pipe section stretch contribution

Industry practice: Calculate placement mathematically, confirm with free point indicator, position jar 1-2 joints higher than calculation for safety margin, ensure adequate heavy weight below jar for compression stroke.
""",
        key_factors=[
            "Free point accuracy",
            "Drill collar dimensions and weight",
            "Planned overpull magnitude",
            "Stroke length requirement",
            "Buoyancy factor for mud weight",
            "Neutral point location",
            "Safety margin considerations"
        ],
        primary_authority=[
            "API RP 7G: Drill Stem Design and Operating Limits",
            "SPE 16191: Optimizing Jar Placement in Fishing Operations",
            "Baker Hughes Drilling Engineering Manual: Jarring Operations"
        ],
        burden_holder="Operator - engineering calculations and jar placement design",
        adversary_position="May claim improper placement if jarring fails",
        counter_arguments=[
            "Detailed calculations using accurate parameters",
            "Free point confirmation before placement",
            "Industry-standard formulas applied",
            "Safety margins incorporated"
        ],
        resolution_strategy="Calculate placement using stretch formula, verify free point, add safety margin",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.JARRING_OPERATIONS
    ),

    # Fishing Tool Selection
    DoctrineBlock(
        topic="Overshot vs Spear Selection Criteria",
        keywords=["overshot", "spear", "fishing tool selection", "external catch", "internal catch", "pipe recovery"],
        conclusion_template="Overshot is preferred for pipe with accessible external diameter; spear for internal catch when pipe end is open and accessible. Selection depends on fish condition and geometry.",
        reasoning_framework="""
Overshot characteristics:
- Engages outside diameter of pipe (external catch)
- Grapple or basket design grips pipe OD
- Requires fish top to be relatively round and clean
- Can engage damaged pipe if OD intact
- Available in slip-type or spiral grapple designs
- Typical catches: drill pipe, drill collars, casing

Overshot advantages:
1. Does not require entry into pipe bore
2. Can catch collapsed or plugged pipe
3. Easier engagement than spear
4. Less risk of fish damage during catch
5. Higher pull capacity than equivalent spear

Overshot limitations:
- Requires clearance around fish OD
- Cannot catch if fish expanded or welded to casing
- Needs relatively smooth OD surface
- May slip on heavily corroded pipe

Spear characteristics:
- Engages inside diameter of pipe (internal catch)
- Expanding basket or slip mechanism grips ID
- Requires open pipe end for entry
- Available in poor-boy (releasing) or catch-type designs
- Used when overshot cannot fit or engage

Spear advantages:
1. Can catch fish in tight annulus
2. Works when OD damaged or inaccessible
3. Smaller tool OD for restricted holes
4. Can mill fish ID if needed for entry

Spear limitations:
- Requires open pipe end
- Lower pull capacity than overshot (limited by ID)
- Risk of damaging fish wall during expansion
- May not grip corroded or swollen ID

Selection decision tree:

Is fish OD accessible in open hole? → Overshot
Is fish OD collapsed or heavily damaged? → Spear
Is annular clearance insufficient for overshot? → Spear
Is pipe end open and ID accessible? → Spear possible
Is maximum pull capacity required? → Overshot preferred
Is fish in casing with minimal annulus? → Spear

Combined operations:
- Washover pipe over fish, then overshot on clean section
- Mill fish OD, then overshot on milled diameter
- Mill fish ID, then releasing spear for internal catch

Industry practice: Overshot is first choice if geometry permits - higher success rate and pull capacity. Spear when overshot physically cannot work or when fish is in very tight spot. Consider sequential attempts: overshot first, spear if unsuccessful, washover or milling if both fail.
""",
        key_factors=[
            "Fish OD accessibility and condition",
            "Annular clearance around fish",
            "Pipe end condition (open vs closed)",
            "Required pull capacity",
            "Fish ID condition if spear used",
            "Wellbore geometry restrictions",
            "Previous fishing attempt results"
        ],
        primary_authority=[
            "API Spec 7: Rotary Drill Stem Elements (fishing tools)",
            "IADC Drilling Manual: Fishing Tool Selection Guidelines",
            "Weatherford Fishing Services Manual"
        ],
        burden_holder="Operator - proper tool selection for fish configuration",
        adversary_position="Contractor may argue tool inappropriate for conditions",
        counter_arguments=[
            "Fish measurements confirmed tool selection",
            "Industry practice followed",
            "Tool specifications matched requirements",
            "Alternative methods evaluated"
        ],
        resolution_strategy="Select based on fish geometry, attempt overshot first if possible, escalate to spear or milling",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FISHING_TOOL_SELECTION
    ),

    DoctrineBlock(
        topic="Washover Pipe Operations",
        keywords=["washover pipe", "washpipe", "wash over stuck fish", "external cutting", "rotary shoe", "concentric cut"],
        conclusion_template="Washover pipe cuts and removes formation, cement, or junk around stuck fish exterior, enabling recovery by exposing clean fish section for overshot engagement.",
        reasoning_framework="""
Washover pipe system components:
1. Washpipe: heavy wall pipe with ID > fish OD
2. Rotary shoe: cutting shoe on washpipe bottom
3. Circulating head: top of washpipe for circulation
4. Drive mechanism: rotary table or top drive

Operating principle:
Washpipe is rotated and advanced over stuck fish while circulating. Rotary shoe cuts formation, cement, junk, or scale on fish exterior. Cuttings are circulated up the washpipe annulus and out.

Rotary shoe types:
- Mill tooth: for soft formations
- Tungsten carbide insert: for hard rock
- Diamond impregnated: for very hard formations
- Concave profile: helps center on fish

Washover applications:
1. Fish stuck in unconsolidated formation (sand, gravel)
2. Fish cemented in place (bad cement job, squeeze)
3. Parted fish with junk accumulation around it
4. Corroded fish requiring cleaning before overshot
5. Key seated fish requiring groove excavation

Procedure:
1. Run washpipe on drill pipe with jar above
2. Circulate and rotate while advancing slowly
3. Monitor torque and weight (avoid excessive force)
4. Typical ROP: 1-10 feet per hour depending on conditions
5. Wash over sufficient length for overshot engagement
6. Pull washpipe and run overshot inside washpipe
7. Engage fish and recover together with washpipe

Critical parameters:
- Weight on shoe: 5,000-20,000 lbs typical
- Rotary speed: 40-100 RPM
- Circulation rate: maximum practical for hole cleaning
- Washpipe/fish clearance: typically 0.5-1.0 inch minimum

Risks and mitigation:
Risk: Washpipe stuck on fish exterior
Mitigation: Monitor torque, jar in string, avoid excessive WOB

Risk: Fish damage from excessive force
Mitigation: Gradual advancement, monitor parameters

Risk: Shoe damage in hard formations
Mitigation: Proper shoe selection, replace when worn

Industry practice: Use washover as secondary operation after simpler methods fail (jarring, spotting pills). Calculate clearances carefully - too tight risks differential sticking of washpipe, too loose reduces cutting efficiency. Always include jar in washpipe string for recovery if washpipe becomes stuck.
""",
        key_factors=[
            "Fish OD and washpipe ID clearance",
            "Formation or cement hardness",
            "Washover length required",
            "Rotary shoe type selection",
            "Circulation system capacity",
            "Torque and drag limitations",
            "Junk or scale composition"
        ],
        primary_authority=[
            "API Spec 7: Specification for Rotary Drill Stem Elements",
            "SPE 37623: Washover Operations in Challenging Environments",
            "Weatherford Washover Systems Technical Manual"
        ],
        burden_holder="Operator - engineering washover design and execution",
        adversary_position="May argue improper execution if washpipe stuck",
        counter_arguments=[
            "Clearance calculations proper",
            "Parameters within safe limits",
            "Shoe selection appropriate",
            "Industry procedures followed"
        ],
        resolution_strategy="Calculate clearances, select proper shoe, monitor parameters, jar in string for contingency",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.WASHOVER_OPERATIONS
    ),

    # Milling Operations
    DoctrineBlock(
        topic="Junk Mill vs Section Mill Selection",
        keywords=["junk mill", "section mill", "taper mill", "pilot mill", "milling operations", "mill selection"],
        conclusion_template="Junk mills pulverize small debris; section mills cut large tubulars; taper mills start cuts; pilot mills guide milling. Selection depends on fish size, composition, and desired outcome.",
        reasoning_framework="""
Junk mill characteristics and applications:
- Flat or concave bottom with hard-faced matrix
- Tungsten carbide or diamond impregnated cutting surface
- Grinds junk into small particles for circulation
- Used for: bit cones, bearing races, hand tools, small fish debris
- Flat bottom style for soft junk (rubber, aluminum)
- Concave style for hard junk (steel, carbide)
- Typical sizes: 4.75 inch to 26 inch diameter

Junk mill operation:
1. Low weight on mill (5,000-15,000 lbs)
2. High RPM (60-120) for grinding action
3. High circulation rate to remove cuttings
4. Slow advancement as junk is pulverized
5. Monitor for mill wear by cuttings change

Section mill characteristics:
- Cylindrical body with spiral cutting blades
- Designed to cut tubular fish (pipe, casing, collar)
- Creates "window" in fish wall
- Available in:
  * Straight section mill: parallel cut
  * Taper section mill: angled entry
  * Pilot mill: smaller diameter for starting cut

Section mill operation:
1. Start with pilot mill or taper mill for entry
2. Progress to full-size section mill
3. Weight on mill: 10,000-30,000 lbs
4. RPM: 40-80 (slower than junk mill)
5. Milling rate: 1-6 feet per hour typically
6. Mill sufficient length for fishing tool catch

Taper mill application:
- Start milling operation on fish top
- Angled cutting surface eases entry
- Prevents mill from "walking off" fish
- Critical when fish top is irregular or beveled
- Transition to section mill after entry established

Pilot mill application:
- Small diameter mill runs inside larger mill
- Guides larger mill to proper location
- Prevents deflection in directional holes
- Used in staged milling (pilot → section)

Selection criteria:

Small junk (< 2 inch): Junk mill
Large fish requiring window: Section mill
Starting cut on irregular top: Taper mill
Directional hole guidance: Pilot mill
Extremely hard junk (carbide): Diamond junk mill

Milling economics:
- Mills expensive ($5,000-50,000+ each)
- Milling time costly (rig rates $20,000-100,000/day)
- Calculate: mill cost + rig time vs fish value + sidetrack cost
- Typical decision point: 24-48 hours milling maximum

Industry practice: Use junk mill for unidentified debris or small junk. Use section mill when fish is known pipe and recovery desired. Start section milling with taper or pilot mill. Monitor mill condition by cuttings - fresh sharp cuttings indicate good mill, fine dust indicates mill worn out. Replace mills proactively to maintain efficiency.
""",
        key_factors=[
            "Fish size and composition",
            "Junk identification and quantity",
            "Desired outcome (pulverize vs cut window)",
            "Wellbore geometry and deviation",
            "Economic comparison to alternatives",
            "Mill availability and specifications",
            "Anticipated milling time"
        ],
        primary_authority=[
            "API Spec 7: Rotary Drill Stem Elements",
            "SPE 84237: Milling Operations Optimization",
            "Baker Hughes Milling Services Handbook"
        ],
        burden_holder="Operator - proper mill selection and operation",
        adversary_position="May argue excessive milling time or cost",
        counter_arguments=[
            "Mill selection appropriate for fish type",
            "Parameters within industry standards",
            "Progress monitored and documented",
            "Economic analysis justified continuation"
        ],
        resolution_strategy="Select mill for fish type, use taper/pilot for starting, monitor progress, economic cutoff decision",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MILLING_OPERATIONS
    ),

    DoctrineBlock(
        topic="Milling Parameters Optimization",
        keywords=["milling parameters", "weight on mill", "mill RPM", "circulation rate", "milling efficiency", "mill wear"],
        conclusion_template="Optimal milling parameters balance cutting efficiency against mill wear and hole cleaning. Weight, RPM, and circulation must match mill type, fish hardness, and hole conditions.",
        reasoning_framework="""
Weight on mill guidelines:

Junk mills:
- Soft junk (rubber, aluminum): 5,000-10,000 lbs
- Hard junk (steel, carbide): 10,000-20,000 lbs
- Excessive weight: premature mill wear
- Insufficient weight: poor cutting efficiency

Section mills:
- Pilot mills: 8,000-15,000 lbs
- Taper mills: 10,000-20,000 lbs
- Full section mills: 15,000-35,000 lbs
- Thicker fish walls: higher weight required

RPM optimization:

Junk mills: 60-120 RPM
- Higher RPM for grinding action
- Creates heat - monitor circulation for cooling
- Very hard junk may need lower RPM

Section mills: 40-80 RPM
- Lower RPM for cutting vs grinding
- Harder fish materials: reduce RPM
- Prevent mill overheating

Circulation rate:
- Primary purpose: cuttings removal
- Secondary: mill cooling
- Minimum: 300 GPM typical for 8.5 inch hole
- Maximum practical rate without erosion
- Annular velocity target: 120-200 ft/min
- Insufficient circulation: mill loading, recut cuttings
- Excessive circulation: erosion of mill and fish

Monitoring mill condition:

Cuttings analysis:
- Fresh, large chips: mill cutting efficiently
- Fine dust: mill dulled, needs replacement
- Metallic sheen: cutting fish (good)
- Formation cuttings only: mill not contacting fish

Performance indicators:
- Milling rate (ft/hr): should be relatively consistent
- Torque: steady torque normal, erratic indicates problems
- Weight: sudden decrease may indicate mill breakthrough
- Pump pressure: increase suggests cuttings loading

Mill failure modes:
1. Cutting structure wear: gradual efficiency loss
2. Body washout: erosion from circulation
3. Connection failure: torque overload
4. Breakage: excessive WOB or hidden fish hardness

Optimization procedure:
1. Start conservative: low WOB, moderate RPM
2. Monitor initial performance (15-30 minutes)
3. Incrementally increase WOB if cutting poorly
4. Adjust RPM based on torque response
5. Maximize circulation within safe limits
6. Document cuttings and ROP throughout
7. Replace mill when efficiency drops 50%

Economic consideration:
Milling time cost = rig rate × hours
Typical rig rate: $20,000-100,000/day
Mill cost: $5,000-50,000
Optimization saves hours = major cost impact

Industry practice: Start with manufacturer recommendations, adjust based on real-time feedback, prioritize consistent progress over maximum rate (prevents mill damage), maintain detailed logs for future operations, replace mills proactively before complete failure to avoid losing efficiency.
""",
        key_factors=[
            "Mill type and specifications",
            "Fish material hardness",
            "Hole size and annular clearance",
            "Circulation system capacity",
            "Cuttings removal effectiveness",
            "Economic time constraints",
            "Mill condition monitoring"
        ],
        primary_authority=[
            "API RP 7G: Recommended Practice for Drill Stem Design",
            "SPE 28323: Optimization of Downhole Milling Operations",
            "Halliburton Milling Services Best Practices Guide"
        ],
        burden_holder="Operator - optimize parameters for efficiency and cost",
        adversary_position="May claim improper parameters caused excessive time or failure",
        counter_arguments=[
            "Parameters within manufacturer specifications",
            "Real-time adjustments based on performance",
            "Detailed logs document optimization efforts",
            "Industry best practices followed"
        ],
        resolution_strategy="Start conservative, adjust based on performance monitoring, document thoroughly, replace mills proactively",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MILLING_OPERATIONS
    ),

    # Wireline Fishing
    DoctrineBlock(
        topic="Wireline Fishing Tools and Techniques",
        keywords=["wireline fishing", "grab tool", "spear", "cutting tool", "wireline recovery", "fishing magnet"],
        conclusion_template="Wireline fishing tools recover wireline, slickline, or small fish from wellbore. Selection depends on fish type, condition, and whether cutting or gripping is required.",
        reasoning_framework="""
Wireline fishing tool categories:

Grab tools (gripping):
- Wireline spear: grips wireline rope
- Rope socket: attaches to severed wireline end
- Fishing magnet: retrieves magnetic debris
- Boot basket: catches small junk

Cutting tools:
- Severing tool: cuts wireline under tension
- Cable cutter: mechanical shear for wireline
- Chemical cutter: acid severs cable
- String shot: explosive backoff

Grab tool operation - wireline spear:
1. Lower spear to fish depth
2. Engage fish by rotating or jarring
3. Basket or fingers grip wireline strands
4. Pull slowly to avoid slippage
5. May require multiple attempts for solid catch

Fishing magnet application:
- Recovers steel debris (bit cones, hand tools)
- Does not work on non-magnetic items (monel, stainless, aluminum)
- Limited pull capacity (typically < 500 lbs)
- Used in conjunction with boot basket
- Multiple runs may be required

Boot basket application:
- Catches small junk by circulation
- Fluid flow directs junk into basket
- Check valve retains junk during retrieval
- Effective for: nuts, bolts, hand tools, rock samples
- Limited to items that fit through basket throat

Cutting tool selection:

Wireline severing for stuck conditions:
- String shot: explosive charge severs under tension
- Mechanical cutter: shear blades activated by jarring
- Chemical cutter: acid eats through cable (slowest)

Severing procedure:
1. Determine cut depth (free point if possible)
2. Select appropriate tool for cable type
3. Run tool to cut depth
4. Activate cutting mechanism
5. Verify separation (weight loss at surface)
6. Retrieve upper section
7. Fish or mill lower section

Common wireline fish scenarios:

Stuck perforating gun:
- Attempt to jar free with cable
- If unsuccessful, severe cable and pull upper section
- Mill gun if critical to well completion
- Sidetrack if gun can be abandoned

Stuck logging tool:
- Pull to cable yield limit (typically 15,000-25,000 lbs)
- Severe cable if stuck solid
- Consider fishing tool value vs sidetrack cost

Parted cable with fish in hole:
- Run wireline spear to engage fish top
- If fish inaccessible, run fishing magnet
- Last resort: junk mill to pulverize

Industry practice: Wireline fishing relatively low cost compared to drillstring fishing - attempt multiple times before escalating to coiled tubing or drillstring fishing. Document cable pull tests before severing. Calculate tool value vs fishing cost - many wireline tools cost $50,000-500,000, justifying extensive fishing efforts.
""",
        key_factors=[
            "Fish type and composition",
            "Fish depth and accessibility",
            "Wellbore conditions",
            "Tool value economics",
            "Wireline cable condition",
            "Magnetic properties of fish",
            "Available fishing tool inventory"
        ],
        primary_authority=[
            "API RP 7G: Recommended Practice for Drill Stem Design",
            "Schlumberger Wireline Fishing Manual",
            "SPE 84508: Wireline Fishing Operations Best Practices"
        ],
        burden_holder="Operator - cost-effective wireline fish recovery",
        adversary_position="Service company may claim fish unrecoverable",
        counter_arguments=[
            "Multiple fishing attempts documented",
            "Tool value justifies effort",
            "Industry standard methods applied",
            "Economic decision properly analyzed"
        ],
        resolution_strategy="Attempt gripping tools first, cut and fish if stuck, mill or abandon based on economics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.WIRELINE_FISHING
    ),

    # Backoff Operations
    DoctrineBlock(
        topic="String Shot Backoff Procedures",
        keywords=["backoff", "string shot", "explosive backoff", "reverse thread", "backoff sub", "pipe separation"],
        conclusion_template="Backoff operations separate drillstring at desired depth using explosive string shot or mechanical backoff subs, enabling recovery of upper section and fishing of lower section.",
        reasoning_framework="""
Backoff applications:
1. Recover upper free section of stuck pipe
2. Separate twisted-off pipe at weak point
3. Position fish top for overshot engagement
4. Abandon lower section if uneconomic to fish

String shot method:
- Primacord explosive charge wrapped around pipe ID
- Detonated electrically or mechanically
- Explosion unthreads connection under tension

String shot procedure:
1. Free point determination (critical for depth selection)
2. Apply right-hand torque to pipe (pretension connection)
3. Lower string shot assembly to backoff depth
4. Position charge at connection (not pipe body)
5. Apply surface tension (typically 20,000-50,000 lbs overpull)
6. Detonate charge
7. Monitor weight indicator for sudden drop (confirms backoff)
8. Pull upper section

Connection selection for backoff:
- Choose connection 1-2 joints above stuck point
- Avoid backing off at tool joint (leaves pin in hole)
- Prefer connection in lighter pipe (easier unthread)
- Right-hand threads: apply right-hand torque
- Left-hand threads: apply left-hand torque

Backoff tension calculation:
Optimal tension = makeup torque × leverage factor
Too low: connection won't unthread
Too high: may part pipe instead of unthread

Typical tensions:
- 4.5 inch drill pipe: 30,000-40,000 lbs
- 5.0 inch drill pipe: 40,000-60,000 lbs
- Drill collars: 60,000-100,000 lbs

Alternative: Mechanical backoff subs
- Installed in drillstring during initial run
- No explosives required
- Activated by rotation or jarring
- More predictable than string shot
- Higher cost, requires planning

Backoff verification:
- Weight indicator shows sudden decrease (weight of lower section)
- Can rotate pipe freely (no torque transmission)
- Can pull upper section without resistance
- Free point run confirms separation depth

Risks and mitigation:

Risk: Backoff at wrong depth
Mitigation: Accurate free point determination, double-check depth

Risk: Pipe parts instead of unthreads
Mitigation: Proper tension, good connection condition

Risk: Charge damages pipe above backoff
Mitigation: Correct charge size, proper placement

Post-backoff operations:
1. Retrieve upper section
2. Run overshot or spear on lower fish
3. If fishing unsuccessful, consider:
   - Washover and re-attempt
   - Section milling
   - Sidetrack

Industry practice: Backoff operations are point of no return - verify free point thoroughly before proceeding. Use minimum charge necessary (avoid pipe damage). Apply tension before detonation. Document weight before and after to confirm separation. If backoff fails, do not re-attempt at same depth (connection damaged) - select different connection.
""",
        key_factors=[
            "Free point accuracy",
            "Connection type and condition",
            "Applied tension magnitude",
            "Charge size and placement",
            "Pipe grade and weight",
            "Torque direction (RH vs LH threads)",
            "Economic value of lower section"
        ],
        primary_authority=[
            "API RP 7G: Drill Stem Design and Operating Limits",
            "SPE 27490: Backoff Operations in Fishing Jobs",
            "Halliburton Backoff Services Manual"
        ],
        burden_holder="Operator - proper backoff engineering and execution",
        adversary_position="May claim improper backoff caused additional problems",
        counter_arguments=[
            "Free point determination documented",
            "Calculations per industry standards",
            "Proper tension applied and recorded",
            "Backoff confirmed by weight drop"
        ],
        resolution_strategy="Accurate free point first, calculate tension, verify separation, fish lower section or sidetrack",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BACKOFF_PROCEDURES
    ),

    # Sidetrack Decision
    DoctrineBlock(
        topic="Fish vs Sidetrack Economics",
        keywords=["sidetrack decision", "fishing economics", "probability of success", "sidetrack cost", "fish value", "NPV analysis"],
        conclusion_template="Sidetrack decision requires economic analysis comparing fishing costs and success probability against sidetrack costs and delays. Net present value comparison drives the decision.",
        reasoning_framework="""
Economic decision framework:

Fish value calculation:
FV = Salvage value + Avoided sidetrack cost - Fishing cost

Where:
Salvage value = Material cost + time saved if recovered
Avoided sidetrack cost = Whipstock + milling + directional + cement + time
Fishing cost = Tools + personnel + rig time

Probability-weighted expected value:
EV(Fish) = P(success) × (FV - FC) - P(failure) × FC
EV(Sidetrack) = -SC (certain cost)

Decision: Fish if EV(Fish) > EV(Sidetrack)

Detailed cost components:

Fishing costs:
- Fishing tools: $50,000-500,000+ (overshot, jars, mills)
- Fishing service personnel: $5,000-15,000/day
- Rig time: $20,000-100,000/day
- Mud and consumables: $10,000-50,000
- Typical fishing job: 3-14 days = $300,000-2,000,000+

Sidetrack costs:
- Whipstock assembly: $100,000-300,000
- Window milling: 2-5 days rig time
- Directional drilling: premium rates, $50,000-200,000
- Cement plug: $20,000-100,000
- Lost hole section value
- Delayed production: NPV impact
- Typical sidetrack: $500,000-3,000,000+

Fish value:
- Drill collars: $500-2,000/foot
- Drill pipe: $100-300/foot
- MWD/LWD tools: $500,000-2,000,000
- Downhole motors: $200,000-500,000
- Casing: $50-200/foot

Probability of success estimation:

High probability (70-90%):
- Simple mechanical stuck, free point clear
- Jarring or chemical treatment likely effective
- Fish in good condition, accessible

Medium probability (30-70%):
- Differential sticking in moderate conditions
- Fish requires milling or washover
- Some uncertainty in fish condition

Low probability (10-30%):
- Severely stuck, multiple mechanisms
- Fish damaged or in very difficult location
- Previous fishing attempts failed

Time value consideration:
NPV of delayed production critical in high-value wells
Example: $50,000/day production revenue
14-day fishing delay = $700,000 lost production
Add to fishing cost for comparison

Decision matrix examples:

Scenario 1: MWD stuck in 10,000 ft vertical hole
Fish value: $1M tool + $200K avoided sidetrack = $1.2M
Fishing cost estimate: $400K (5 days)
Success probability: 80%
EV(Fish) = 0.8 × ($1.2M - $400K) - 0.2 × $400K = $560K
Sidetrack cost: $600K
Decision: Fish (EV positive and better than sidetrack)

Scenario 2: Drill pipe stuck in 18,000 ft directional hole
Fish value: $100K pipe + $1.5M avoided sidetrack = $1.6M
Fishing cost estimate: $1.2M (12 days)
Success probability: 40%
Lost production: $600K (12 days × $50K/day)
EV(Fish) = 0.4 × ($1.6M - $1.8M) - 0.6 × $1.8M = -$1.16M
Sidetrack cost: $2M + $200K lost production = $2.2M
Decision: Fish (both negative, fishing less bad)

Industry practice: Conduct formal economic analysis with sensitivity to probability estimates. Set time limit for fishing (typically 7-14 days maximum). Re-evaluate decision if fishing extends beyond initial estimate. Sidetrack becomes more favorable if: fishing attempts unsuccessful, unexpected difficulties arise, success probability drops, well production value very high (time critical).
""",
        key_factors=[
            "Fish material value",
            "Fishing tool and service costs",
            "Rig day rate",
            "Sidetrack cost estimate",
            "Success probability assessment",
            "Well production value (NPV)",
            "Fishing time estimate",
            "Previous attempt results"
        ],
        primary_authority=[
            "SPE 84323: Economic Analysis of Fishing vs Sidetrack Decisions",
            "IADC Fishing Operations Manual: Decision Criteria",
            "API RP 7G: Drill Stem Design (fishing considerations)"
        ],
        burden_holder="Operator - sound economic analysis and decision documentation",
        adversary_position="Partners or AFE holders may challenge decision basis",
        counter_arguments=[
            "Detailed NPV analysis with sensitivity cases",
            "Industry-standard probability assessment methods",
            "Market-rate cost estimates",
            "Re-evaluation at decision milestones"
        ],
        resolution_strategy="Calculate EV for both options, set time limits, re-evaluate if circumstances change",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FISHING_ECONOMICS
    ),

    DoctrineBlock(
        topic="Whipstock Sidetrack Operations",
        keywords=["whipstock", "window milling", "sidetrack", "kickoff point", "oriented sidetrack", "openhole whipstock"],
        conclusion_template="Whipstock sidetrack creates new wellbore from existing hole using oriented deflection assembly and window milling. Success requires proper setting depth, orientation, and window milling execution.",
        reasoning_framework="""
Whipstock sidetrack applications:
1. Bypass stuck fish that cannot be recovered economically
2. Bypass damaged casing or collapsed hole section
3. Directional correction in vertical wells
4. Multi-lateral well construction

Whipstock assembly components:
- Whipstock body: tapered face deflects bit laterally
- Anchor: mechanical or hydraulic setting mechanism
- Orientation sub: aligns whipstock face direction
- Mill: typically section mill or taper mill
- Guide shoe: prevents mill from sliding off whipstock

Setting procedure:
1. Run whipstock assembly on drillstring or wireline
2. Orient whipstock face to desired azimuth
3. Set anchor (mechanical slips or hydraulic expansion)
4. Verify setting with weight and torque indicators
5. If drillstring-set, release and POOH
6. If permanent, mill through whipstock guide shoe

Openhole vs cased hole whipstock:

Openhole whipstock:
- Used when fish is in openhole section
- Anchor relies on mechanical force against formation
- Less secure than cased hole anchor
- Requires competent formation for stability

Cased hole whipstock:
- Anchor grips casing ID
- More secure setting
- Requires window milling through casing
- Typical for bypassing casing damage or stuck casing fish

Window milling procedure:
1. Run taper mill or section mill
2. Mill first window section (typically 10-30 feet)
3. Circulate cuttings to surface
4. POOH and inspect mill condition
5. Run full-size section mill if taper mill used first
6. Continue milling to planned window depth
7. Total window length: typically 30-100 feet

Milling parameters for casing window:
- Weight on mill: 10,000-30,000 lbs depending on casing size
- RPM: 40-80 typical
- Circulation: maximum rate for cuttings removal
- Milling rate: 2-10 feet/hour depending on casing grade

Kickoff angle development:
- Whipstock angle: typically 2-4 degrees/foot
- Build rate depends on whipstock length and angle
- Typical build rates: 8-20 degrees/100 feet
- First survey typically 30-50 feet above whipstock

Directional drilling after window:
1. Complete window mill
2. Run BHA with motor or RSS
3. Drill pilot hole with directional control
4. Monitor surveys to stay on desired trajectory
5. Transition to rotary drilling when stable

Risks and mitigation:

Risk: Whipstock orientation incorrect
Mitigation: Verify orientation before setting, use MWD/gyro

Risk: Inadequate window length
Mitigation: Mill full planned length, confirm clearance

Risk: Window collapse during directional drilling
Mitigation: Stabilize with mud weight, adequate window length

Risk: Intersecting original wellbore
Mitigation: Build angle aggressively, monitor surveys closely

Post-sidetrack options for fish:
- Abandon permanently (cement plug)
- Abandon temporarily (may return to fish later)
- Continue sidetrack as primary wellbore

Industry practice: Whipstock sidetrack is major operation - requires detailed planning, directional drilling expertise, and significant cost ($500K-2M+). Used when fishing attempts unsuccessful or economics clearly favor sidetrack. Permanent whipstock preferred over retrievable for critical sidetracks. Window must be milled completely before directional drilling to prevent window collapse and loss of trajectory control.
""",
        key_factors=[
            "Kickoff point depth selection",
            "Whipstock orientation accuracy",
            "Window milling length adequacy",
            "Casing grade and condition",
            "Formation stability for openhole anchor",
            "Directional trajectory planning",
            "Economic justification vs fishing"
        ],
        primary_authority=[
            "API RP 7G: Drill Stem Design and Operating Limits",
            "SPE 39312: Sidetracking Operations Best Practices",
            "Baker Hughes Whipstock Services Manual"
        ],
        burden_holder="Operator - proper sidetrack engineering and execution",
        adversary_position="May claim sidetrack unnecessary or poorly executed",
        counter_arguments=[
            "Economic analysis justified sidetrack vs fishing",
            "Engineering design per industry standards",
            "Orientation and setting verified",
            "Successful trajectory achieved"
        ],
        resolution_strategy="Plan thoroughly, orient accurately, mill complete window, execute directional drilling",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SIDETRACK_DECISION
    ),

    # Stuck Pipe Prevention
    DoctrineBlock(
        topic="Differential Sticking Prevention",
        keywords=["stuck pipe prevention", "differential sticking prevention", "mud properties", "pipe movement", "minimize contact time"],
        conclusion_template="Differential sticking prevention requires managing overbalance, mud properties, and operational practices to minimize filter cake contact and contact time.",
        reasoning_framework="""
Prevention strategies - mud system:

Minimize overbalance:
- Use lowest safe mud weight for pore pressure control
- Consider managed pressure drilling for narrow margin wells
- Typical target: 0.3-0.5 ppg overbalance minimum
- Excessive overbalance increases differential force

Optimize mud properties:
- Minimize HPHT fluid loss (< 15 mL API typical)
- Thin filter cake formation
- Use lubricants (oil-based mud, synthetic, or additives)
- Reduce mud solids content
- Use properly sized bridging materials

Oil-based mud advantages:
- Superior lubricity vs water-based mud
- Thinner, more stable filter cake
- Lower coefficient of friction
- Typical reduction: 50-70% vs WBM in differential risk

Synthetic-based mud (SBM):
- Environmental advantages over OBM
- Similar lubricity and filtration properties
- Increasingly preferred for offshore operations

Prevention strategies - operational:

Minimize static time:
- Avoid prolonged stationary periods in permeable zones
- Typical rule: move pipe every 5-10 minutes
- Reciprocate or rotate when circulating connections
- Differential force increases with contact time

Maintain pipe movement:
- Rotate drill pipe when conditions allow
- Reciprocate pipe during connections
- Use power slips or top drive for continuous rotation
- Movement prevents filter cake bonding

Drilling practices:
- Minimize trips through permeable zones
- Ream tight spots immediately
- Circulate bottoms up before tripping
- Use wiper trips in high-risk sections

String design:
- Use spiral drill collars in deviated wells (reduce contact area)
- Maximize standoff in permeable zones
- Avoid unnecessary stabilizers in permeable sections
- Consider reduced-OD pipe for high-risk zones

Operational monitoring:

Leading indicators of differential risk:
1. High filtration rates (HPHT fluid loss test)
2. Thick filter cake (>3/32 inch)
3. Increasing overbalance
4. Extended static time in permeable zones
5. High-permeability formations on logs

Real-time monitoring:
- Torque and drag trends
- Hookload changes when picking up
- Free rotating weight decrease
- ECD monitoring (PWD tools)

Emergency response if indications present:
1. Immediately start moving pipe
2. Reduce mud weight if safely possible
3. Spot oil-based or synthetic pill
4. Prepare jarring assembly for future runs
5. Plan to minimize future static time

High-risk scenarios:

Depleted reservoirs:
- High overbalance unavoidable
- Enhanced prevention measures critical
- Consider MPD or UBD techniques

Deep wells with narrow margin:
- Overbalance required for deeper zones
- Sticky zones at shallower depth
- Careful mud weight management

Horizontal wells in permeable reservoirs:
- Long contact length with permeable zone
- Spiral drill collars essential
- Continuous rotation preferred

Industry practice: Prevention far cheaper than fishing - implement multi-layered strategy. OBM or SBM preferred for high differential risk wells. Never remain stationary >10 minutes in permeable zones. If differential sticking occurs despite prevention, immediate action critical - every minute increases holding force. Spot pill immediately, apply slow steady pull, prepare for jarring if simple pulling fails.
""",
        key_factors=[
            "Overbalance magnitude management",
            "Mud filtration control (HPHT fluid loss)",
            "Filter cake quality and thickness",
            "Pipe movement frequency",
            "Static time minimization",
            "Formation permeability characterization",
            "Mud system selection (WBM vs OBM vs SBM)"
        ],
        primary_authority=[
            "API RP 7G: Drill Stem Design and Operating Limits",
            "SPE 67707: Analysis and Prevention of Differential Sticking",
            "IADC Stuck Pipe Prevention Guidelines"
        ],
        burden_holder="Operator - implement prevention best practices",
        adversary_position="Contractor may argue prevention measures inadequate",
        counter_arguments=[
            "Mud properties within specifications",
            "Operational practices followed industry standards",
            "Real-time monitoring documented",
            "Prevention measures appropriate for well risk"
        ],
        resolution_strategy="Multi-layer prevention: mud system, operational practices, BHA design, real-time monitoring",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PREVENTION_STRATEGY
    ),

    DoctrineBlock(
        topic="Key Seat Prevention Strategies",
        keywords=["key seat prevention", "dogleg severity", "spiral collars", "reaming", "BHA design"],
        conclusion_template="Key seat prevention requires managing dogleg severity, using appropriate BHA components, and proper drilling practices to avoid groove formation in doglegs.",
        reasoning_framework="""
Key seat formation mechanism:
- Drill pipe wears groove in dogleg during rotation
- Groove conforms to pipe OD
- Groove prevents upward pipe movement
- Tool joints or collars larger than groove diameter catch

Prevention strategy 1: Minimize dogleg severity

Directional well planning:
- Design minimum curvature for target reach
- Typical safe dogleg: <3 degrees/100 feet
- Higher doglegs in deviated wells increase key seat risk
- Build/drop/turn sections highest risk

Survey frequency:
- Frequent surveys to detect unintended doglegs
- Correct trajectory deviations early
- Typical survey interval: 30-90 feet in build sections

Prevention strategy 2: BHA design for deviated wells

Spiral drill collars:
- Helical grooves machined on collar OD
- Prevents collar from wearing single groove in formation
- Distributes contact area around circumference
- Standard practice for dogleg >2 degrees/100 feet

String reamers:
- Cutting structure on collar OD
- Reams hole to larger diameter than pipe OD
- Prevents groove formation or widens existing grooves
- Position in string near expected dogleg zones

Roller reamers:
- Rolling cutters on stabilizer body
- Less aggressive than string reamers
- Maintains hole gauge
- Reduces torque vs fixed blade reamers

Prevention strategy 3: Operational practices

Ream while tripping:
- Rotate and circulate while pulling out of hole
- Reams any tight spots or grooves
- Essential in deviated wells with doglegs
- Typical: ream every 5-10 stands during trip out

Wiper trips:
- POOH to casing/liner top, then run back in hole
- Identifies and reams restrictions before final trip
- Standard practice before running casing in deviated wells
- Can prevent key seat by widening grooves before trip

Backreaming:
- Ream while pulling out of dogleg section
- Use rotary table or top drive
- Removes formation groove before tool joints pass through
- Critical in wells with known key seat risk

Minimize WOB in doglegs:
- Excessive WOB accelerates groove cutting
- Use lowest WOB consistent with acceptable ROP
- Particularly important in soft formations

Prevention strategy 4: Formation considerations

Soft formations highest risk:
- Sandstone, limestone, soft shale
- Groove cuts quickly in soft rock
- Hard formations (granite, hard limestone) resist grooving

Unconsolidated zones:
- May slough into dogleg, creating restriction
- Stabilize with mud weight and chemistry
- Consider casing off if severe

Monitoring and early detection:

Indicators of key seat formation:
1. Increasing torque in dogleg section
2. Drag when pulling through dogleg
3. Decreased ROP in dogleg (WOB absorbed by contact)
4. Tight spot at consistent depth during trips

Action if indicators present:
- Increase reaming frequency
- Run string reamer if not already in BHA
- Consider trip and change BHA to add prevention tools
- Wiper trip before final trip to TD

Industry practice: Key seats are highly preventable with proper planning and execution. Directional wells >45 degrees should always use spiral collars in build and turn sections. Ream while tripping is non-negotiable in deviated wells. If key seat does form, DO NOT jar upward - worsens the situation. Backoff above key seat and fish with rotary shoe or section mill to cut through groove.
""",
        key_factors=[
            "Dogleg severity management",
            "Spiral collar use in deviated sections",
            "Reaming while tripping compliance",
            "WOB control in doglegs",
            "Formation softness assessment",
            "Survey frequency and accuracy",
            "BHA component selection"
        ],
        primary_authority=[
            "SPE 21999: Key Seating - Causes, Prevention, and Remediation",
            "API RP 7G: Drill Stem Design and Operating Limits",
            "IADC Directional Drilling Best Practices Manual"
        ],
        burden_holder="Operator - engineering and operational prevention",
        adversary_position="Contractor may argue BHA inadequate or procedures not followed",
        counter_arguments=[
            "BHA design appropriate for dogleg severity",
            "Operational procedures documented and followed",
            "Survey data shows dogleg within design parameters",
            "Industry best practices implemented"
        ],
        resolution_strategy="Design for doglegs, use spiral collars and reamers, ream while tripping, monitor indicators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PREVENTION_STRATEGY
    ),

    # Fishing Job Planning
    DoctrineBlock(
        topic="Fishing Job Risk Assessment and Planning",
        keywords=["fishing job planning", "risk assessment", "contingency planning", "fishing tools inventory", "fishing procedure"],
        conclusion_template="Comprehensive fishing job planning includes risk assessment, tool selection, contingency scenarios, economic analysis, and detailed operational procedures to maximize success probability.",
        reasoning_framework="""
Pre-fishing assessment:

Fish characterization:
- Type: drill pipe, drill collar, BHA component, casing, wireline
- Condition: intact, parted, twisted, corroded, damaged
- Length: total length stuck vs total fish length
- Location: depth, deviation, formation type
- Value: material cost, time to replace, strategic importance

Stuck mechanism analysis:
- Differential: permeable zone, overbalance, static time
- Mechanical: key seat, packoff, ledge, collapse
- Junk: cuttings, cement, lost circulation material
- Unknown: requires diagnostic operations first

Free point determination:
- Stretch calculation method
- Electronic free point indicator
- Accuracy critical for all planning decisions

Wellbore condition assessment:
- Hole size and gauge
- Deviation and dogleg severity
- Formation stability and lithology
- Mud properties and hole cleaning
- Restrictions or tight spots

Tool selection matrix:

Primary fishing tool options:
1. Overshot with jar (differential or light mechanical stuck)
2. Spear with jar (internal catch, tight annulus)
3. Washover pipe (fish in junk or cement)
4. Section mill (cut window for catch or sidetrack)
5. Junk mill (small debris, unidentified junk)

Jar selection:
- Hydraulic jar for differential or controlled jarring
- Mechanical jar for severe mechanical restrictions
- Jar placement calculation based on free point

Support equipment:
- Reverse circulation tool (cuttings bypass)
- Bumper sub (jar stroke control)
- Safety joint (allows disconnect if fishing tools stuck)
- Accelerator (increase jar impact)

Contingency planning:

Sequential escalation:
1. Primary plan: simplest/cheapest method first
2. Contingency 1: next complexity level if primary fails
3. Contingency 2: more aggressive approach
4. Contingency 3: sidetrack decision point

Example escalation for differential stuck drill pipe:
Primary: Spot oil pill, jar with hydraulic jar, 10 attempts
Contingency 1: Washover pipe 3 joints, re-attempt jarring
Contingency 2: Backoff above stuck point, run overshot
Contingency 3: Section mill and sidetrack if fish value < $500K

Tool inventory verification:
- Confirm availability before starting operation
- Order long-lead items immediately
- Have backup tools on standby
- Know delivery time for specialty tools

Economic analysis:

Cost estimation:
- Fishing tools rental/purchase: itemized list
- Service personnel: rates and estimated days
- Rig time: day rate × estimated duration
- Consumables: mud, chemicals, fuel
- Contingency factor: typically 25-50%

Time estimation:
- Optimistic: everything works first attempt (20th percentile)
- Most likely: typical operation duration (50th percentile)
- Pessimistic: multiple attempts or escalation (80th percentile)

Expected value calculation:
EV = P(success) × (Fish value - Cost) - P(failure) × Cost
Compare to sidetrack EV

Decision criteria:
- Proceed if EV(fish) > EV(sidetrack)
- Set maximum time limit (typically 7-14 days)
- Set maximum cost limit
- Define decision points for re-evaluation

Operational procedure development:

Detailed step-by-step plan:
1. Current well status and BHA configuration
2. POOH procedure if needed
3. Fishing assembly makeup and inspection
4. RIH procedure with special precautions
5. Fishing tool engagement procedure
6. Primary recovery attempt procedure
7. Success criteria and verification
8. Failure criteria and contingency trigger
9. POOH procedure with fish if successful
10. Handover to contingency plan if unsuccessful

Safety considerations:
- Tension limits for pipe and connections
- Jarring force limits vs pipe yield
- Differential pressure limits for stuck pipe
- Personnel qualifications and supervision

Real-time monitoring plan:
- Key parameters to track
- Decision points for plan modification
- Communication protocol for updates
- Authority for contingency activation

Industry practice: Comprehensive planning before starting fishing operation is critical - hasty or improvised fishing often fails and wastes time/money. Assemble full fishing team (operator rep, fishing service engineer, directional driller if needed) for planning session. Document plan in detail with decision trees. Have all tools on location before starting. Set clear decision criteria and authority. Re-evaluate plan if circumstances change. Know when to abandon fishing and sidetrack - sunk cost fallacy leads to wasting millions on unrecoverable fish.
""",
        key_factors=[
            "Fish characterization accuracy",
            "Stuck mechanism diagnosis",
            "Free point determination",
            "Tool availability and lead time",
            "Economic analysis thoroughness",
            "Contingency scenarios defined",
            "Decision criteria clarity",
            "Time and cost limits set"
        ],
        primary_authority=[
            "API RP 7G: Drill Stem Design and Operating Limits",
            "SPE 84323: Economic and Technical Decision Making in Fishing Operations",
            "IADC Fishing Operations Manual: Planning and Execution"
        ],
        burden_holder="Operator - comprehensive planning and economic justification",
        adversary_position="Partners may challenge fishing decision or execution quality",
        counter_arguments=[
            "Detailed risk assessment conducted",
            "Economic analysis with sensitivity cases",
            "Contingency plans for all scenarios",
            "Industry expert consultation documented",
            "Decision criteria pre-established and followed"
        ],
        resolution_strategy="Thorough assessment, detailed planning, economic justification, contingencies, decision criteria",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FISHING_JOB_PLANNING
    ),

    # Additional critical doctrines
    DoctrineBlock(
        topic="Fishing Tool Safety Joint Application",
        keywords=["safety joint", "disconnect", "fishing string protection", "left-hand safety joint", "fishing assembly"],
        conclusion_template="Safety joints in fishing assemblies allow intentional disconnect if fishing tools become stuck, protecting the fishing string from becoming additional fish.",
        reasoning_framework="""
Safety joint purpose:
If fishing tools become stuck during recovery attempt, safety joint allows disconnect of fishing string above stuck tools. This prevents compounding the problem by sticking the entire fishing assembly.

Safety joint types:
1. Mechanical safety joint: threaded connection with reduced strength
2. Hydraulic release joint: pressure-activated disconnect
3. Left-hand safety joint: reverse rotation to disconnect

Placement in fishing string:
Typical position: 1-2 joints above fishing tool (overshot or spear)
Above jar but below drill pipe/heavy weight pipe
Allows recovery of jar and most of fishing assembly

Left-hand safety joint operation:
- Body has left-hand threads (opposite normal drill pipe)
- Assembled by turning left (CCW from above)
- Disconnects by turning right (CW from above)
- Used when fish may need to be released after engagement

Release procedure:
1. Engage fish with fishing tool
2. Attempt recovery with jarring/pulling
3. If fishing string becomes stuck
4. Apply torque to operate safety joint (or pressure if hydraulic)
5. Disconnect and recover fishing string above safety joint
6. Fish is now original fish + stuck fishing tools below safety joint

When to use safety joint:

High-risk fishing operations:
- Uncertain fish condition (may be heavily damaged)
- First fishing attempt in difficult conditions
- Tight clearances (high risk of sticking fishing tools)
- Unknown junk in hole around fish

When NOT to use safety joint:
- Simple, low-risk fishing (unnecessary complication)
- When releasing fish after catch is unacceptable
- When fishing string very short (safety joint adds length)

Alternative: shear sub
- Similar concept but designed to part under tension
- Shear pins release at predetermined load
- Simpler than threaded safety joint
- One-time use (pins shear permanently)

Industry practice: Safety joint is insurance policy - hope not to use it, but critical if fishing goes wrong. Standard in first fishing attempt on difficult fish. Omitted in simple, low-risk operations to reduce trip time and complexity. Always inspect and function test before running. Know activation procedure (torque direction, pressure, etc.) before emergency need arises.
""",
        key_factors=[
            "Fishing operation risk level",
            "Fish condition uncertainty",
            "Wellbore geometry constraints",
            "Safety joint type selection",
            "Placement in fishing string",
            "Activation procedure clarity"
        ],
        primary_authority=[
            "API Spec 7: Rotary Drill Stem Elements",
            "IADC Fishing Operations Manual",
            "Weatherford Fishing Tools Catalog"
        ],
        burden_holder="Operator - risk assessment and safety joint decision",
        adversary_position="May argue safety joint unnecessary or improperly placed",
        counter_arguments=[
            "Risk assessment justified safety joint use",
            "Industry practice for this fish type",
            "Prevented compounding stuck situation",
            "Cost justified by risk mitigation"
        ],
        resolution_strategy="Include safety joint in high-risk fishing, proper placement, know activation procedure",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FISHING_TOOL_SELECTION
    ),

    DoctrineBlock(
        topic="Stuck Pipe Spotting Fluids",
        keywords=["spotting fluid", "pipe-free pill", "diesel pill", "oil-based pill", "surfactant pill", "stuck pipe treatment"],
        conclusion_template="Spotting fluids reduce friction, break filter cake seal, or lubricate stuck pipe contact points. Selection depends on stuck mechanism and mud system compatibility.",
        reasoning_framework="""
Spotting fluid mechanisms:

Oil-based pills for differential sticking:
- Penetrate filter cake with low-viscosity oil
- Reduce filter cake/pipe friction coefficient
- Break capillary bond between cake and pipe
- Most effective for differential sticking

Composition:
- Base: diesel, mineral oil, or synthetic oil
- Surfactants: reduce surface tension, enhance penetration
- Viscosifiers: suspend solids, prevent settling
- Additives: lubricants, wetting agents

Surfactant pills:
- Reduce surface tension at pipe/formation interface
- Emulsify filter cake
- Penetrate narrow spaces
- Can be water-based (compatible with WBM systems)

Acid pills (for carbonate formations):
- Dissolve carbonate cement or scale on pipe
- HCl typical (15-28%)
- Use with corrosion inhibitors
- Risk: formation damage if uncontrolled

Lubricant pills:
- Graphite, glass beads, or synthetic lubricants
- Reduce friction coefficient
- Can be added to any mud system
- Less effective than oil-based for differential

Spotting procedure:

Volume calculation:
Calculate annular volume around stuck zone
Typical: spot 50-100% excess to ensure coverage
Account for mud displacement as pill pumped

Placement:
1. Calculate pill volume for stuck zone coverage
2. Pump pill down drillstring
3. Displace with mud to position pill at stuck point
4. Allow soak time (typically 4-12 hours)
5. Attempt to work pipe (jarring, rotation, reciprocation)
6. Circulate out if unsuccessful, re-spot if needed

Soak time:
Minimum: 4 hours for oil-based pills
Typical: 8-12 hours for maximum effect
Longer soak may help but diminishing returns
Monitor temperature (higher temp = faster action)

Working pipe during treatment:
Some methods recommend slow pipe movement during soak
Others recommend static soak followed by movement
Industry divided on best practice

Pill selection for stuck mechanism:

Differential sticking:
Primary: Oil-based pill (diesel or synthetic)
Secondary: Surfactant pill
Rationale: penetrate filter cake, reduce friction

Mechanical sticking (key seat, packoff):
Primary: High-lubricity pill (graphite, synthetic)
Secondary: Surfactant to loosen debris
Rationale: reduce friction, aid debris removal

Cement/scale:
Primary: Acid pill (HCl for carbonate cement)
Secondary: Solvent pill for organic residues
Rationale: dissolve bonding material

Mud system compatibility:

Water-based mud system:
- Oil-based pills create emulsion (may damage mud)
- Use surfactant or water-based lubricant pills
- If oil pill required, may need mud replacement cost

Oil-based mud system:
- Oil pills fully compatible
- Can use higher concentrations
- Typically more effective than in WBM

Synthetic-based mud system:
- Synthetic oil pills compatible
- Similar effectiveness to OBM
- Environmental advantage over diesel

Cost considerations:
- Oil-based pills: $50-200 per barrel
- Typical volume: 20-100 barrels
- Total pill cost: $1,000-20,000
- Cheap compared to fishing or rig time
- Almost always worth attempting before escalation

Effectiveness:
Success rate for differential sticking: 30-70%
Lower success for mechanical sticking: 10-30%
Combined with jarring: improved success rates
Multiple applications may be needed

Industry practice: Spot pill as first response to stuck pipe - low cost, non-destructive, can work while planning next steps. Oil-based pills most effective for differential sticking even in WBM wells (accept mud contamination cost). Allow adequate soak time - rushing reduces effectiveness. Combine pill with jarring for maximum effectiveness. If pill unsuccessful after 2-3 attempts, escalate to backoff, washover, or other mechanical methods.
""",
        key_factors=[
            "Stuck mechanism diagnosis",
            "Mud system type",
            "Spotting fluid selection",
            "Volume and placement calculation",
            "Soak time allowed",
            "Mud compatibility impact",
            "Economic cost vs benefit"
        ],
        primary_authority=[
            "SPE 67707: Stuck Pipe Prevention and Remediation",
            "API RP 13C: Recommended Practice on Drilling Fluid Processing Systems",
            "M-I SWACO Stuck Pipe Handbook"
        ],
        burden_holder="Operator - proper pill selection and application",
        adversary_position="May argue pill unnecessary or improperly selected",
        counter_arguments=[
            "Stuck mechanism diagnosis justified pill type",
            "Industry-standard pill formulation",
            "Adequate soak time provided",
            "Combined with mechanical methods for best chance"
        ],
        resolution_strategy="Select pill for mechanism, calculate volume, allow soak time, combine with jarring",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.STUCK_PIPE_DIAGNOSIS
    ),

    DoctrineBlock(
        topic="Fishing Assembly Design and Makeup",
        keywords=["fishing assembly", "BHA design", "jar placement", "fishing string", "torque and makeup", "fishing connection"],
        conclusion_template="Fishing assembly design requires engineering for tension loads, jar placement, and connection integrity. Proper makeup and inspection critical to prevent fishing string failure.",
        reasoning_framework="""
Fishing assembly components (bottom to top):

1. Fishing tool (overshot, spear, mill)
2. Jar (hydraulic or mechanical)
3. Drill collars (heavy weight for jar compression)
4. Crossover sub (if needed for connection change)
5. Heavy weight drill pipe or drill collars
6. Drill pipe (main working string)
7. Kelly or top drive

Critical design considerations:

Tension rating:
Every component must exceed maximum anticipated load
Max load = Fish weight + Overpull + Jar impact force
Add safety factor: typically 1.25-1.5

Example:
Fish weight: 100,000 lbs
Maximum overpull: 150,000 lbs
Jar impact: 200,000 lbs
Peak load: 450,000 lbs
Minimum component rating: 562,500 lbs (1.25 SF)

Compression rating:
Components below neutral point in compression
Drill collars must not buckle under compression load
Neutral point must be above jar for proper function

Torque rating:
Connections must withstand makeup torque plus operational torque
Fishing operations often require high torque for milling or rotation

Jar placement engineering:
Position based on free point and desired stroke length
Requires sufficient drill collar weight below jar
See separate doctrine on jar placement calculations

Connection selection:

Premium connections preferred:
- API IF (internal flush) for drill pipe
- API FH (full hole) for drill collars
- NC38, NC40, NC46, NC50 for various sizes
- Rotary shouldered connections for high loads

Torque specifications:
Must makeup to proper torque for connection type
Under-torque: risk of connection failure, washout
Over-torque: risk of galling, thread damage

Connection inspection before makeup:
1. Visual inspection for damage, wear, corrosion
2. Thread gauge to verify dimensions in spec
3. Magnetic particle inspection for cracks (critical components)
4. Clean threads thoroughly before makeup
5. Apply appropriate thread compound

Makeup procedure:

Field makeup (rotary table):
1. Stab connection and hand-tighten
2. Pickup pipe to engage threads fully
3. Apply rotary table torque to reach shoulder
4. Final torque with tong wrench to specification
5. Mark connection with paint for torque verification

Top drive makeup:
1. Stab connection in rotary table
2. Pick up with top drive engaged
3. Torque to specification using top drive's torque control
4. Verify final torque with hydraulic torque wrench if critical

Premium connection makeup:
1. Clean and inspect threads meticulously
2. Apply makeup compound per manufacturer spec
3. Makeup to specified torque (often higher than API)
4. Use calibrated torque wrench
5. Document torque values

Special considerations for fishing:

New vs used connections:
- New connections preferred for critical fishing
- Used connections acceptable if inspected and within spec
- Worn connections risk failure under high loads

Safety joint integration:
- Include if warranted by risk assessment
- Verify safety joint activation procedure
- Position properly in string (above fishing tool, below drill pipe)

Handling and stabbing:
- Use proper elevators and slips for component weights
- Avoid side loading or dropping connections
- Support fishing tools properly during makeup

Quality control:

Inspection points:
- Before makeup: thread inspection, gauging
- During makeup: torque monitoring, alignment
- After makeup: visual verification, torque marks
- Before RIH: final assembly verification

Documentation:
- Component serial numbers and ratings
- Torque values achieved for each connection
- Inspection results and acceptance
- Assembly sequence and configuration

Failure modes and prevention:

Connection washout:
- Caused by under-torque or thread damage
- Prevention: proper makeup torque, inspection

Connection parting:
- Caused by over-tension or fatigue
- Prevention: proper component rating, inspection for cracks

Thread galling:
- Caused by over-torque or contamination
- Prevention: clean threads, proper compound, torque control

Industry practice: Fishing assembly failure is catastrophic - creates additional fish of expensive fishing tools. Inspect every component and connection carefully. Use new or like-new connections for critical fishing. Makeup to exact torque specifications using calibrated equipment. Document everything. Never rush assembly - time spent on proper makeup is cheap compared to consequences of failure. If any component or connection is questionable, replace it - false economy to save $5,000 on connection and lose $500,000 fishing job.
""",
        key_factors=[
            "Component tension ratings vs loads",
            "Jar placement calculations",
            "Connection type selection",
            "Torque specification compliance",
            "Thread inspection thoroughness",
            "Makeup procedure adherence",
            "Documentation completeness"
        ],
        primary_authority=[
            "API RP 7G: Drill Stem Design and Operating Limits",
            "API RP 7: Recommended Practice for Rotary Drill Stem Elements",
            "DS-1 Drill String Design and Inspection Standard"
        ],
        burden_holder="Operator - proper engineering and quality control",
        adversary_position="May claim inadequate design or makeup if failure occurs",
        counter_arguments=[
            "Engineering calculations documented",
            "Inspection records complete",
            "Torque values recorded and verified",
            "Industry standards followed",
            "Component ratings exceed loads"
        ],
        resolution_strategy="Engineer properly, inspect thoroughly, makeup correctly, document everything",
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FISHING_JOB_PLANNING
    )
]


# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

class TelemetryCollector:
    """Comprehensive operation telemetry tracking."""

    def __init__(self):
        self.query_count = 0
        self.doctrine_hits = Counter()
        self.response_times = []
        self.mode_usage = Counter()
        self.zone_usage = Counter()
        self.category_distribution = Counter()
        self.error_domains = Counter()

    def record_query(self, query: str, mode: ResponseMode, zone: AnalysisZone,
                    triggered: List[str], latency_ms: float, category: Optional[IssueCategory] = None):
        """Record query metrics."""
        self.query_count += 1
        self.response_times.append(latency_ms)
        self.mode_usage[mode.value] += 1
        self.zone_usage[zone.value] += 1
        if category:
            self.category_distribution[category.value] += 1
        for doctrine in triggered:
            self.doctrine_hits[doctrine] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics."""
        return {
            "total_queries": self.query_count,
            "avg_latency_ms": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            "p95_latency_ms": sorted(self.response_times)[int(len(self.response_times) * 0.95)] if self.response_times else 0,
            "doctrine_hit_rate": len([d for d in self.doctrine_hits.values() if d > 0]) / len(DOCTRINE_CACHE),
            "top_doctrines": self.doctrine_hits.most_common(10),
            "mode_distribution": dict(self.mode_usage),
            "zone_distribution": dict(self.zone_usage),
            "category_distribution": dict(self.category_distribution)
        }


class DriftWatcher:
    """Monitor for doctrine drift and coverage gaps."""

    def __init__(self):
        self.missed_queries = []
        self.low_confidence_queries = []

    def record_miss(self, query: str, triggered_count: int):
        """Record query with no/few doctrine hits."""
        if triggered_count == 0:
            self.missed_queries.append(query)

    def record_low_confidence(self, query: str, confidence: ConfidenceLevel):
        """Record high-risk confidence queries."""
        if confidence == ConfidenceLevel.HIGH_RISK:
            self.low_confidence_queries.append(query)

    def get_gaps(self) -> Dict[str, Any]:
        """Identify coverage gaps."""
        return {
            "total_misses": len(self.missed_queries),
            "recent_misses": self.missed_queries[-10:],
            "high_risk_queries": len(self.low_confidence_queries),
            "recent_high_risk": self.low_confidence_queries[-10:]
        }


# ============================================================================
# CORE ENGINE
# ============================================================================

class FishingOperationsEngine:
    """DRL15 Fishing Operations Intelligence Engine."""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.startup_time = datetime.now()
        logger.info(f"DRL15 Fishing Operations Engine initialized with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> tuple[str, List[str], ConfidenceLevel, str]:
        """
        Three-layer response architecture:
        Layer 1: Doctrine cache (0-50ms)
        Layer 2: Semantic retrieval (fallback)
        Layer 3: Deep analysis (complex queries)
        """
        start_time = time.time()

        # Layer 1: Check doctrine cache
        triggered = self._check_doctrine_cache(query, zone)

        if triggered:
            response = self._synthesize_doctrine_response(query, triggered, mode)
            confidence = self._assess_confidence(triggered)
            latency_ms = (time.time() - start_time) * 1000
            return response, [d.topic for d in triggered], confidence, "doctrine_cache"

        # Layer 2: Semantic search (if implemented)
        # For now, fall through to Layer 3

        # Layer 3: Deep analysis
        response = self._deep_analysis(query, mode)
        latency_ms = (time.time() - start_time) * 1000
        return response, [], ConfidenceLevel.DISCLOSURE, "deep_analysis"

    def _check_doctrine_cache(self, query: str, zone: AnalysisZone) -> List[DoctrineBlock]:
        """Check doctrine cache for relevant blocks."""
        triggered = []
        for doctrine in self.doctrines:
            if doctrine.triggered_by(query) and zone in doctrine.zone_applicability:
                triggered.append(doctrine)
        return triggered

    def _synthesize_doctrine_response(self, query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
        """Synthesize response from triggered doctrines."""
        if mode == ResponseMode.FAST:
            # Concise response
            primary = doctrines[0]
            return f"{primary.conclusion_template}\n\nKey factors: {', '.join(primary.key_factors[:3])}"

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready comprehensive response
            sections = []
            for doctrine in doctrines[:3]:  # Top 3 most relevant
                sections.append(f"**{doctrine.topic}**\n\n{doctrine.reasoning_framework}\n\n" +
                              f"Primary authority: {'; '.join(doctrine.primary_authority)}")
            return "\n\n---\n\n".join(sections)

        else:  # MEMO
            # Full documentation
            sections = [f"# Fishing Operations Analysis: {query}\n"]
            for i, doctrine in enumerate(doctrines, 1):
                sections.append(f"## {i}. {doctrine.topic}\n\n" +
                              f"**Conclusion:** {doctrine.conclusion_template}\n\n" +
                              f"**Analysis:**\n{doctrine.reasoning_framework}\n\n" +
                              f"**Key Factors:**\n" + "\n".join(f"- {f}" for f in doctrine.key_factors) + "\n\n" +
                              f"**Authorities:**\n" + "\n".join(f"- {a}" for a in doctrine.primary_authority) + "\n\n" +
                              f"**Resolution Strategy:** {doctrine.resolution_strategy}\n\n" +
                              f"**Confidence Level:** {doctrine.confidence.value}")
            return "\n".join(sections)

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence from triggered doctrines."""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Return most conservative confidence level
        levels = [d.confidence for d in doctrines]
        if ConfidenceLevel.HIGH_RISK in levels:
            return ConfidenceLevel.HIGH_RISK
        elif ConfidenceLevel.DISCLOSURE in levels:
            return ConfidenceLevel.DISCLOSURE
        elif ConfidenceLevel.AGGRESSIVE in levels:
            return ConfidenceLevel.AGGRESSIVE
        else:
            return ConfidenceLevel.DEFENSIBLE

    def _deep_analysis(self, query: str, mode: ResponseMode) -> str:
        """Deep analysis for queries not covered by doctrine cache."""
        # Fallback response for uncached queries
        return (f"Query received: {query}\n\n" +
                f"This query does not trigger specific doctrine blocks. " +
                f"For fishing operations analysis, consider:\n" +
                f"1. Fish characterization and free point determination\n" +
                f"2. Stuck mechanism diagnosis (differential vs mechanical)\n" +
                f"3. Fishing tool selection (overshot vs spear vs mill)\n" +
                f"4. Economic analysis (fish vs sidetrack)\n" +
                f"5. Prevention strategies for future operations\n\n" +
                f"Please provide more specific details for targeted analysis.")

    def determinism_hash(self, query: str, response: str) -> str:
        """Generate SHA-256 hash for response determinism verification."""
        content = f"{query}::{response}".encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check."""
        return {
            "status": "healthy",
            "uptime_seconds": (datetime.now() - self.startup_time).total_seconds(),
            "doctrine_count": len(self.doctrines),
            "metrics": self.telemetry.get_metrics(),
            "coverage_gaps": self.drift_watcher.get_gaps(),
            "categories": [c.value for c in IssueCategory],
            "version": "1.0.0"
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title="DRL15 Fishing Operations Intelligence Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = FishingOperationsEngine()


@app.post("/query", response_model=QueryResponse)
async def query_fishing_operations(request: QueryRequest):
    """
    Analyze fishing operations query with TIE-grade intelligence.

    Supports three response modes:
    - FAST: Concise tactical guidance
    - DEFENSE: Audit-ready comprehensive analysis
    - MEMO: Full documentation with authorities
    """
    start_time = time.time()

    try:
        response_text, triggered_topics, confidence, source_layer = engine.three_layer_response(
            request.query, request.mode, request.zone
        )

        latency_ms = (time.time() - start_time) * 1000

        # Determine category from triggered doctrines
        category = None
        if triggered_topics:
            for doctrine in engine.doctrines:
                if doctrine.topic in triggered_topics:
                    category = doctrine.category
                    break

        # Record telemetry
        engine.telemetry.record_query(
            request.query, request.mode, request.zone,
            triggered_topics, latency_ms, category
        )

        # Track coverage
        if not triggered_topics:
            engine.drift_watcher.record_miss(request.query, 0)
        if confidence == ConfidenceLevel.HIGH_RISK:
            engine.drift_watcher.record_low_confidence(request.query, confidence)

        det_hash = engine.determinism_hash(request.query, response_text)

        return QueryResponse(
            query=request.query,
            response=response_text,
            mode=request.mode,
            zone=request.zone,
            confidence=confidence,
            triggered_doctrines=triggered_topics,
            source_layer=source_layer,
            latency_ms=round(latency_ms, 2),
            determinism_hash=det_hash,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Comprehensive health check endpoint."""
    return engine.health_check()


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine blocks."""
    return {
        "count": len(engine.doctrines),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "zones": [z.value for z in d.zone_applicability]
            }
            for d in engine.doctrines
        ]
    }


@app.get("/metrics")
async def get_metrics():
    """Retrieve operational metrics and telemetry."""
    return engine.telemetry.get_metrics()


@app.get("/")
async def root():
    """Engine information and capabilities."""
    return {
        "engine": "DRL15 Fishing Operations Intelligence Engine",
        "version": "1.0.0",
        "port": 9265,
        "capabilities": [
            "Stuck pipe diagnosis (differential vs mechanical)",
            "Free point determination methods",
            "Jarring operations and jar selection",
            "Fishing tool selection (overshot, spear, washover)",
            "Milling operations (junk mill, section mill)",
            "Wireline fishing techniques",
            "Backoff procedures and string shots",
            "Sidetrack decision economics",
            "Stuck pipe prevention strategies",
            "Fishing job planning and risk assessment"
        ],
        "categories": [c.value for c in IssueCategory],
        "response_modes": [m.value for m in ResponseMode],
        "analysis_zones": [z.value for z in AnalysisZone],
        "doctrine_count": len(engine.doctrines)
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DRL15 Fishing Operations Intelligence Engine on port 9265")
    uvicorn.run(app, host="0.0.0.0", port=9265)
