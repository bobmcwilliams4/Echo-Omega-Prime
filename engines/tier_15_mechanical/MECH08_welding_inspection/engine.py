"""
MECH08 - Welding & Inspection Intelligence Engine
TIE Gold Standard - Mechanical Engineering Domain

Comprehensive welding technology and quality assurance/quality control expertise.
Covers welding processes, code compliance, NDT methods, and inspection protocols.

Port: 9048
Version: 1.0.0
"""

import asyncio
import hashlib
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

# CRITICAL: Set sys.path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ════════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & LOGGING
# ════════════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="MECH08 Welding & Inspection Engine",
    version="1.0.0",
    description="TIE Gold Standard welding technology and NDT intelligence"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "mech08_welding.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)

# ════════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ════════════════════════════════════════════════════════════════════════════════

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
    WELDING_PROCESS = "welding_process"
    CODE_COMPLIANCE = "code_compliance"
    NDT_METHOD = "ndt_method"
    WELD_DEFECT = "weld_defect"
    PROCEDURE_QUALIFICATION = "procedure_qualification"
    WELDER_QUALIFICATION = "welder_qualification"
    MATERIAL_SPECIFICATION = "material_specification"
    HEAT_TREATMENT = "heat_treatment"
    JOINT_DESIGN = "joint_design"
    FILLER_METAL = "filler_metal"
    INSPECTION_PLANNING = "inspection_planning"
    REPAIR_WELDING = "repair_welding"
    DOCUMENTATION = "documentation"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    EXECUTION = "EXECUTION"
    INSPECTION = "INSPECTION"

BANNED_PHRASES = [
    "This is legal advice",
    "This is engineering certification",
    "guaranteed to pass inspection",
    "no defects possible",
    "code compliance guaranteed",
    "certified weld procedure",
    "approved for all applications"
]

# ════════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ════════════════════════════════════════════════════════════════════════════════

class WeldingQuery(BaseModel):
    question: str = Field(..., description="Welding or inspection question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    project_details: Optional[Dict[str, str]] = Field(default=None, description="Project-specific information")

class WeldingResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    categories: List[IssueCategory]
    authorities_cited: List[str]
    telemetry: Dict[str, Any]
    determinism_hash: str
    timestamp: str
    epistemic_disclosure: Optional[str] = None
    zones_analyzed: List[AnalysisZone]

@dataclass
class DoctrineBlock:
    """Welding expertise doctrine block"""
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
    issue_categories: List[IssueCategory] = field(default_factory=list)
    zones: List[AnalysisZone] = field(default_factory=list)

@dataclass
class TelemetryData:
    """Query telemetry tracking"""
    query_id: str
    start_time: float
    end_time: float
    cache_hit: bool
    doctrines_triggered: List[str]
    semantic_fallback: bool
    error_domain: Optional[str]
    confidence: ConfidenceLevel
    response_mode: ResponseMode

# ════════════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ WELDING EXPERTISE BLOCKS
# ════════════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="SMAW Stick Welding Process Selection",
        keywords=["smaw", "stick welding", "shielded metal arc", "electrode", "e6010", "e7018", "outdoor welding", "field welding"],
        conclusion_template=[
            "SMAW is preferred for {application} due to wind resistance and portability.",
            "Electrode selection depends on base metal composition, position, and current type.",
            "E6010 provides deep penetration for root passes; E7018 offers superior mechanical properties for fill/cap."
        ],
        reasoning_framework="""
        SMAW (Shielded Metal Arc Welding) selection analysis:
        1. Evaluate environmental conditions (wind, rain, outdoor vs indoor)
        2. Assess base metal type, thickness, and carbon equivalent
        3. Determine welding position requirements (flat, horizontal, vertical, overhead)
        4. Select electrode classification based on AWS A5.1/A5.5 specifications
        5. Consider current type (AC vs DC) and polarity (DCEP, DCEN)
        6. Verify preheat requirements per ASME Section IX or AWS D1.1
        7. Establish amperage range based on electrode diameter and position
        8. Plan for slag removal between passes
        9. Confirm operator qualification for selected electrode classification
        10. Document WPS parameters including travel speed and interpass temperature

        E6010: DC+ only, deep penetration, all position, excellent for root passes, minimal slag
        E6011: AC or DC+, similar to E6010, better for rusty/dirty materials
        E7018: AC or DC+, low hydrogen, high strength, smooth bead, requires dry storage
        E7024: AC or DC either, heavy slag, flat/horizontal fillet only, high deposition

        Critical: Low hydrogen electrodes (E7018, E7016) must be stored at 250-300°F
        to prevent moisture absorption and hydrogen-induced cracking (HIC).
        """,
        key_factors=[
            "Environmental exposure (wind negates gas-shielded processes)",
            "Base metal chemistry and carbon equivalent (CE > 0.45 requires preheat)",
            "Welding position dictates electrode selection",
            "Low hydrogen requirements for high strength or thick materials",
            "Portability needs (SMAW requires only electrode holder and ground)",
            "Operator skill level and certification",
            "Material cleanliness (rust, mill scale, paint)"
        ],
        primary_authority=[
            "AWS A5.1 Carbon Steel Electrodes",
            "AWS A5.5 Low-Alloy Steel Electrodes",
            "ASME Section IX Welding Procedure Qualification",
            "AWS D1.1 Structural Welding Code - Steel"
        ],
        burden_holder="Engineer/WPS author to justify electrode selection based on service conditions",
        adversary_position="Client may prefer faster processes (GMAW/FCAW) to reduce labor cost",
        counter_arguments=[
            "SMAW has lower deposition rates than wire-feed processes",
            "Requires frequent electrode changes",
            "Slag must be removed between passes (additional labor)",
            "Sensitive to wind with gas-shielded alternatives",
            "Limited to ~350A maximum (lower than SAW/FCAW)"
        ],
        resolution_strategy="Demonstrate total project economics including equipment cost, setup time, rework risk, and environmental adaptability",
        entity_scope="Applicable to structural steel, pipeline, pressure vessel, and field repair welding",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="SMAW process selection is code-compliant and field-proven across industries",
        controlling_precedent="AWS D1.1 and ASME B31 codes explicitly permit SMAW for most applications",
        issue_categories=[IssueCategory.WELDING_PROCESS, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING]
    ),

    DoctrineBlock(
        topic="GMAW/MIG Welding Process Parameters",
        keywords=["gmaw", "mig", "gas metal arc", "short circuit", "spray transfer", "pulse", "shielding gas", "wire feed speed"],
        conclusion_template=[
            "GMAW transfer mode depends on amperage, voltage, and shielding gas composition.",
            "Short circuit transfer is optimal for thin materials and out-of-position welding.",
            "Spray transfer provides high deposition rates for thick sections in flat/horizontal positions."
        ],
        reasoning_framework="""
        GMAW process parameter selection:
        1. Determine base metal thickness and composition
        2. Select transfer mode: short circuit (< 200A), globular (200-250A), spray (> 250A), pulsed
        3. Choose shielding gas: 75/25 Ar/CO2 (short circuit), 90/10 Ar/CO2 (spray), 98/2 Ar/O2 (stainless)
        4. Set wire feed speed (WFS) based on amperage demand
        5. Adjust voltage for desired bead profile and penetration
        6. Confirm wire diameter matches application (0.030", 0.035", 0.045", 1/16")
        7. Set contact tip-to-work distance (CTWD): 3/8" - 3/4 inch typical
        8. Verify travel speed for specified heat input (per WPS)
        9. Monitor spatter generation and adjust voltage/inductance
        10. Document all parameters on PQR

        Transfer Modes:
        - Short Circuit: 50-200A, thin gauge, all position, low heat input, higher spatter
        - Globular: 200-250A, transition zone, irregular transfer, not recommended
        - Spray: > 250A, argon-rich gas required, smooth transfer, flat/horizontal only
        - Pulsed Spray: Spray benefits at lower average current, all position capable

        Critical: Shielding gas selection affects arc stability, penetration, and mechanical properties.
        CO2-only produces deeper penetration but more spatter; argon-rich gives smoother arc.
        """,
        key_factors=[
            "Material thickness dictates amperage and transfer mode",
            "Welding position limits spray transfer to flat/horizontal",
            "Shielding gas composition affects bead profile and spatter",
            "Wire diameter influences deposition rate and penetration",
            "Travel speed controls heat input and dilution",
            "Contact tip condition (wear increases resistance and arc instability)",
            "Gas flow rate (35-50 CFH typical; excessive flow creates turbulence)"
        ],
        primary_authority=[
            "AWS D1.1 Structural Welding Code",
            "AWS A5.18 Carbon Steel Electrodes and Rods for GMAW",
            "ASME Section IX QW-250 Welding Variables",
            "API 1104 Pipeline Welding Standard"
        ],
        burden_holder="Welding engineer to qualify procedure with specified parameters via PQR",
        adversary_position="Production may push for faster travel speeds, risking lack of fusion or undercut",
        counter_arguments=[
            "GMAW requires clean base metal (oil, rust, mill scale cause porosity)",
            "Wind sensitivity limits outdoor use without windscreens",
            "Equipment cost higher than SMAW",
            "Requires wire feeder and gas cylinder (portability issues)",
            "Spatter cleanup adds post-weld labor"
        ],
        resolution_strategy="Balance productivity gains against quality risk; use pulsed GMAW for versatility",
        entity_scope="Suitable for automotive, structural steel, general fabrication, and robotic welding",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="GMAW parameters are well-established in AWS and ASME codes",
        controlling_precedent="AWS D1.1 Table 3.7 provides prequalified GMAW joint details",
        issue_categories=[IssueCategory.WELDING_PROCESS, IssueCategory.PROCEDURE_QUALIFICATION],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION]
    ),

    DoctrineBlock(
        topic="GTAW/TIG Welding for Critical Applications",
        keywords=["gtaw", "tig", "gas tungsten arc", "tungsten electrode", "filler rod", "root pass", "stainless steel", "exotic alloys"],
        conclusion_template=[
            "GTAW provides superior weld quality and cleanliness for critical root passes.",
            "Tungsten electrode selection (pure, 2% thoriated, 2% lanthanated, 2% ceriated) affects arc stability.",
            "GTAW is mandatory for exotic alloys (Inconel, Hastelloy, titanium) due to contamination sensitivity."
        ],
        reasoning_framework="""
        GTAW process application and parameter selection:
        1. Identify material sensitivity to contamination (stainless, nickel alloys, titanium, aluminum)
        2. Select tungsten electrode type and diameter per AWS A5.12
        3. Determine current type: DCEN (steel/stainless), AC (aluminum/magnesium)
        4. Choose shielding gas: argon (most metals), helium blend (aluminum), argon + hydrogen (austenitic stainless)
        5. Set amperage based on material thickness and tungsten diameter
        6. Grind tungsten to proper taper angle (15-30° for DCEN, balled tip for AC)
        7. Use filler rod matching base metal composition (AWS A5.9 for stainless, A5.14 for Ni alloys)
        8. Employ trailing shield or purge gas for reactive metals
        9. Control interpass temperature to prevent grain growth
        10. Verify operator dexterity and certification for manual GTAW

        Tungsten Electrode Selection:
        - Pure Tungsten (green): AC only, aluminum/magnesium, rounded ball tip
        - 2% Thoriated (red): DCEN, excellent arc starts, radioactive (being phased out)
        - 2% Lanthanated (blue): AC/DC, thorium replacement, better longevity
        - 2% Ceriated (orange): AC/DC, low amperage applications, aerospace

        Critical: GTAW root passes in pipe welding (ASME B31.3, API 1104) provide clean, porosity-free
        starts critical for subsequent fill passes. Backing gas (argon purge) prevents oxidation.
        """,
        key_factors=[
            "Material oxidation sensitivity (titanium oxidizes instantly without purge)",
            "Joint access and fit-up quality (GTAW is unforgiving of gaps)",
            "Amperage precision requirements (pulsed GTAW for thin sections)",
            "Filler metal compatibility with base metal",
            "Shielding gas purity (99.995% minimum for reactive metals)",
            "Tungsten contamination (dipping tungsten into weld pool ruins electrode)",
            "Welder skill level (GTAW has steep learning curve)"
        ],
        primary_authority=[
            "AWS A5.12 Tungsten and Tungsten Alloy Electrodes",
            "AWS D17.1 Fusion Welding for Aerospace Applications",
            "ASME Section IX QW-200 Welding Procedure Specifications",
            "AWS B2.1 Welding Procedure and Performance Qualification"
        ],
        burden_holder="Welding engineer to justify GTAW cost premium for critical applications",
        adversary_position="Contractor may prefer faster GMAW/FCAW to reduce labor hours",
        counter_arguments=[
            "GTAW has lowest deposition rate of all arc welding processes",
            "Requires highly skilled operators",
            "Equipment cost (high-frequency start, foot pedal control)",
            "Slow travel speed limits production throughput",
            "Tungsten inclusion defects if electrode contacts molten pool"
        ],
        resolution_strategy="Demonstrate superior quality, lower rework rate, and code compliance for critical piping/pressure vessels",
        entity_scope="Mandatory for nuclear, aerospace, pharmaceutical, and high-purity applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="GTAW is code-required for many ASME Section III and aerospace applications",
        controlling_precedent="ASME B31.3 permits GTAW for all piping materials without additional qualification testing",
        issue_categories=[IssueCategory.WELDING_PROCESS, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION]
    ),

    DoctrineBlock(
        topic="Welding Procedure Specification (WPS) per ASME Section IX",
        keywords=["wps", "welding procedure", "asme section ix", "essential variables", "pqr", "procedure qualification"],
        conclusion_template=[
            "WPS must be supported by a qualified PQR demonstrating acceptable mechanical properties.",
            "Essential variables (base metal P-number, filler metal F-number, PWHT) require requalification if changed.",
            "Prequalified WPS per AWS D1.1 eliminates need for mechanical testing within specified limits."
        ],
        reasoning_framework="""
        WPS development and qualification per ASME Section IX:
        1. Identify base metal P-Number (QW-420) grouping similar materials
        2. Select filler metal F-Number (QW-432) classification
        3. Determine welding process(es) to be used
        4. Establish joint design and weld preparation (groove angle, root opening, land)
        5. Specify essential variables: amperage range, voltage range, travel speed, preheat, interpass temp
        6. Define supplementary essential variables if impact testing required
        7. List nonessential variables for information only
        8. Create supporting PQR via actual welding and mechanical testing
        9. Extract tensile, bend (side, face, root), and impact specimens per QW-150
        10. Document PQR results; if acceptable, WPS is qualified

        Essential Variables (requalification required if exceeded):
        - Base metal P-Number change
        - Filler metal F-Number change
        - Welding process addition/deletion
        - Electrode diameter or filler wire size (outside qualified range)
        - Current or polarity change
        - Preheat/interpass temperature (decrease > 100°F)
        - PWHT deletion or time/temperature change

        Critical: ASME Section IX QW-200 series defines WPS format and required content.
        A single PQR can support multiple WPSs if variables remain within qualified range.
        """,
        key_factors=[
            "Code of construction dictates qualification requirements (ASME vs AWS vs API)",
            "Material grouping (P-Numbers) determines procedure transferability",
            "Joint configuration affects bending specimen orientation",
            "Impact testing requirements add cost (CVN testing at low temperature)",
            "Preheat reduces cracking risk but adds field labor",
            "PWHT affects hardness and requires furnace access",
            "Welder/operator qualification separate from procedure qualification"
        ],
        primary_authority=[
            "ASME Section IX Welding and Brazing Qualifications",
            "AWS B2.1 Standard for Welding Procedure and Performance Qualification",
            "API 1104 Welding of Pipelines and Related Facilities",
            "AWS D1.1 Structural Welding Code - Steel (prequalified WPS Table 3.7)"
        ],
        burden_holder="Contractor to produce qualified WPS and supporting PQR before production welding",
        adversary_position="Client may question cost of qualification testing and request prequalified procedures",
        counter_arguments=[
            "Mechanical testing (tensile, bend, impact) is expensive and time-consuming",
            "Prequalified WPS (AWS D1.1) available only for limited joint configurations",
            "Each essential variable change requires new PQR",
            "PWHT adds significant cost for field welds",
            "Impact testing may require subzero conditioning chamber"
        ],
        resolution_strategy="Leverage existing qualified procedures from similar projects; use prequalified WPS where code permits",
        entity_scope="Mandatory for ASME pressure vessels, piping, nuclear, and many pipeline applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ASME Section IX is universally recognized and legally enforceable code",
        controlling_precedent="ASME Section IX has been incorporated by reference in OSHA, DOT, and state regulations",
        issue_categories=[IssueCategory.PROCEDURE_QUALIFICATION, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING]
    ),

    DoctrineBlock(
        topic="Welder Performance Qualification per ASME Section IX",
        keywords=["welder qualification", "performance qualification", "wpq", "continuity", "6g position", "asme section ix qw-300"],
        conclusion_template=[
            "Welder must qualify by welding a test coupon in accordance with WPS and achieving acceptable bend test results.",
            "Qualification in 6G position (pipe at 45° fixed) qualifies welder for all positions.",
            "Welder qualification expires if welder does not weld with qualified process for 6 months."
        ],
        reasoning_framework="""
        Welder performance qualification (ASME Section IX QW-300):
        1. Select qualified WPS for test coupon welding
        2. Determine test position(s) required for production work (1G, 2G, 5G, 6G for pipe)
        3. Prepare test coupon per WPS joint geometry
        4. Welder completes coupon under supervision without assistance
        5. Visual inspection confirms acceptance criteria (no cracks, complete fusion, proper contour)
        6. Extract bend specimens per QW-452 (side, face, or root bends depending on thickness)
        7. Perform bend test per QW-160 (guided bend jig or wrap-around mandrel)
        8. Acceptance: < 1/8 inch discontinuity in any direction after bending
        9. Document results on Welder Performance Qualification Record (WPQR)
        10. Establish continuity requirements (weld every 6 months to maintain qualification)

        Essential Variables for Welder Qualification:
        - Welding process change
        - Material thickness change (outside qualified range per QW-451)
        - Weld progression (uphill vs downhill change)
        - Filler metal diameter change
        - Pipe diameter change (< 2-7/8 inch vs >= 2-7/8")

        Critical: 6G position (pipe at 45° angle, welded without rotating) is most difficult and
        qualifies welder for all pipe positions. 6GR adds restriction ring to simulate tight access.
        """,
        key_factors=[
            "Test position selection determines scope of qualification",
            "Material thickness tested establishes qualified thickness range",
            "Pipe diameter tested (small bore qualifies for larger, not vice versa)",
            "Weld deposit thickness (groove vs fillet qualification)",
            "Continuity maintenance (welding every 6 months with each process)",
            "Multiple process qualification (SMAW, GMAW, GTAW require separate tests)",
            "Visual inspection before destructive testing (reject obvious defects early)"
        ],
        primary_authority=[
            "ASME Section IX QW-300 Performance Qualifications",
            "AWS D1.1 Section 4 Qualification",
            "API 1104 Section 6 Welder Qualification",
            "AWS B2.1 Welding Procedure and Performance Qualification"
        ],
        burden_holder="Employer to ensure welders are qualified and maintain continuity",
        adversary_position="Welders may resist frequent re-qualification testing if continuity lapses",
        counter_arguments=[
            "Qualification testing is destructive (scrap cost)",
            "Downtime for testing reduces billable hours",
            "6-month continuity rule is strict for seasonal workers",
            "Each process/position combination requires separate qualification",
            "Radiography or UT can't substitute for bend testing (per code)"
        ],
        resolution_strategy="Schedule qualification tests during equipment maintenance; track continuity proactively",
        entity_scope="Required for pressure vessel, piping, structural steel, and pipeline welding",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Welder qualification is legally mandated by ASME, API, and AWS codes",
        controlling_precedent="OSHA 29 CFR 1910.254 and DOT 49 CFR Part 192/195 require welder qualification",
        issue_categories=[IssueCategory.WELDER_QUALIFICATION, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING]
    ),

    DoctrineBlock(
        topic="Preheat and Interpass Temperature Requirements",
        keywords=["preheat", "interpass temperature", "carbon equivalent", "hydrogen cracking", "haz", "heat affected zone"],
        conclusion_template=[
            "Preheat reduces cooling rate and prevents hydrogen-induced cracking in HAZ.",
            "Minimum preheat temperature increases with carbon equivalent and section thickness.",
            "Interpass temperature maximum prevents grain coarsening and loss of toughness."
        ],
        reasoning_framework="""
        Preheat and interpass temperature determination:
        1. Calculate carbon equivalent (CE) of base metal: CE = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15
        2. Determine material thickness at weld joint
        3. Consult preheat tables (AWS D1.1 Table 3.2, ASME Section IX QW-406.1)
        4. For CE > 0.45, minimum preheat often 200-400°F depending on thickness
        5. Verify hydrogen content of filler metal (low hydrogen electrodes reduce cracking risk)
        6. Measure preheat temperature 3 inch from weld joint on both sides using temp sticks or pyrometer
        7. Maintain interpass temperature between minimum (equal to preheat) and maximum (often 500-550°F)
        8. Monitor and record temperatures during welding (per WPS requirements)
        9. For quenched and tempered steels, interpass max may be lower to preserve temper
        10. Consider post-weld heat treatment (PWHT) as alternative to extreme preheat

        Material-Specific Preheat:
        - Low carbon steel (< 0.25% C, thin section): Often no preheat required
        - Medium carbon (0.25-0.50% C) or thick section (> 1"): 200-400°F typical
        - High strength low alloy (HSLA): 150-300°F depending on CE and restraint
        - Cr-Mo alloys (P5, P9, P11, P22): 300-500°F minimum per ASME Section VIII
        - Cast iron: 500-1200°F slow preheat, slow cooling to avoid cracking

        Critical: Hydrogen-induced cracking (HIC) occurs in HAZ when three factors converge:
        hydrogen presence, susceptible microstructure (martensite), and residual stress.
        Preheat slows cooling rate, preventing martensite formation.
        """,
        key_factors=[
            "Base metal carbon equivalent (higher CE = higher preheat)",
            "Section thickness (mass increases heat sink effect)",
            "Joint restraint (fixed vs free to move)",
            "Hydrogen content of filler metal (low-H electrodes reduce cracking)",
            "Ambient temperature (cold weather increases preheat needs)",
            "Material heat treatment condition (QT, normalized, annealed)",
            "Prior weld repair history (re-heat-affected zones are more susceptible)"
        ],
        primary_authority=[
            "AWS D1.1 Table 3.2 Preheat and Interpass Temperature",
            "ASME Section VIII Division 1 UW-30 Preheat Requirements",
            "API 1104 Section 5.6 Preheat and Heat Treatment",
            "AWS D1.8 Seismic Supplement (higher preheat for seismic applications)"
        ],
        burden_holder="Welding engineer to specify preheat in WPS based on material properties",
        adversary_position="Production may view preheat as productivity loss and request elimination",
        counter_arguments=[
            "Preheat adds significant labor time (heating, temperature verification)",
            "Requires propane torches, induction heaters, or resistance blankets (equipment cost)",
            "High preheat uncomfortable for welders in hot weather",
            "Interpass temperature monitoring requires frequent interruptions",
            "Over-conservative preheat wastes fuel and time"
        ],
        resolution_strategy="Demonstrate cracking risk via Graville diagram; consider low-H consumables to reduce preheat",
        entity_scope="Applies to all structural, pressure vessel, and pipeline welding codes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Preheat requirements are empirically derived and code-mandated",
        controlling_precedent="AWS D1.1 and ASME Section VIII preheat tables are minimum requirements, not optional",
        issue_categories=[IssueCategory.HEAT_TREATMENT, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION]
    ),

    DoctrineBlock(
        topic="Post-Weld Heat Treatment (PWHT) Requirements",
        keywords=["pwht", "post weld heat treatment", "stress relief", "hardness reduction", "asme section viii", "tempering"],
        conclusion_template=[
            "PWHT reduces residual stresses and tempers martensite in HAZ to acceptable hardness levels.",
            "ASME Section VIII mandates PWHT for P-No. 3/4/5 materials over specified thickness.",
            "Furnace PWHT provides uniform heating; local PWHT requires thermal gradient control."
        ],
        reasoning_framework="""
        PWHT application and requirements:
        1. Identify code of construction (ASME Section VIII, B31.3, API 650, etc.)
        2. Determine base metal P-Number and thickness
        3. Consult code tables for mandatory PWHT (e.g., ASME VIII-1 UW-40)
        4. Establish PWHT temperature and time at temperature per code
        5. Define heating rate (< 400°F/hr typical for thick sections to avoid thermal shock)
        6. Maintain soak temperature uniformly across weld zone
        7. Define cooling rate (< 500°F/hr typical to avoid re-hardening)
        8. Use thermocouples to monitor actual temperature during cycle
        9. Document PWHT chart (time-temperature curve) for QA records
        10. Verify hardness after PWHT (HRC < 22 typical for pressure vessels per ASME Section VIII)

        PWHT Temperature Ranges (typical):
        - Carbon steel: 1100-1200°F for 1 hr per inch thickness (minimum 30 min)
        - 1-1/4 Cr - 1/2 Mo (P4): 1250-1400°F
        - 2-1/4 Cr - 1 Mo (P5A): 1300-1400°F
        - 5 Cr - 1/2 Mo (P5B): 1300-1450°F
        - 9 Cr - 1 Mo (P5C): 1350-1450°F
        - Stainless steels: Often no PWHT (solution anneal or stabilizing anneal if required)

        Critical: Local PWHT (resistance bands, induction) requires thermal gradient control
        per ASME Section VIII UW-40(g) — heated band width minimum 2x thickness, maximum
        temperature gradient 100°F per inch radially from weld.
        """,
        key_factors=[
            "Material P-Number and thickness trigger mandatory PWHT",
            "Residual stress level (highly restrained joints need PWHT)",
            "Hardness acceptance criteria (HRC < 22 for sour service per NACE MR0175)",
            "Furnace availability and size (local PWHT if component too large)",
            "Thermal gradient control for local PWHT (avoid cracking from differential expansion)",
            "Impact on material properties (over-tempering reduces strength)",
            "Code exemptions (small bore piping, non-pressure parts may be exempt)"
        ],
        primary_authority=[
            "ASME Section VIII Division 1 UW-40 Post-Weld Heat Treatment",
            "ASME B31.3 Process Piping Section 331 PWHT Requirements",
            "API 650 Storage Tank PWHT (Appendix R for low-temperature service)",
            "NACE MR0175/ISO 15156 Hardness Requirements for Sour Service"
        ],
        burden_holder="Fabricator to perform PWHT per code and provide documented heat treatment records",
        adversary_position="Owner may request PWHT exemption to reduce cost and schedule impact",
        counter_arguments=[
            "PWHT requires expensive furnace or local heating equipment",
            "Furnace PWHT may require disassembly/transportation of large components",
            "Adds significant schedule time (heating, soak, cooling cycle may take days)",
            "Local PWHT has higher risk of thermal gradient-induced cracking",
            "Some materials (austenitic stainless) don't benefit from PWHT and may sensitize"
        ],
        resolution_strategy="Evaluate code exemptions (impact tested, reduced thickness); consider alternative materials not requiring PWHT",
        entity_scope="Mandatory for most pressure vessels, high-pressure piping, and refinery equipment",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PWHT requirements are code-mandated and supported by decades of service experience",
        controlling_precedent="ASME Section VIII and B31.3 PWHT rules are legally binding per jurisdictional regulations",
        issue_categories=[IssueCategory.HEAT_TREATMENT, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION]
    ),

    DoctrineBlock(
        topic="Filler Metal Selection and AWS Classification",
        keywords=["filler metal", "electrode", "aws classification", "e7018", "er70s-6", "tensile strength", "low hydrogen"],
        conclusion_template=[
            "AWS filler metal classification designates tensile strength, welding position, and coating/flux type.",
            "Match filler metal tensile strength to base metal or exceed by one grade.",
            "Low hydrogen designations (suffix H4, H8, H16) critical for high strength steels and thick sections."
        ],
        reasoning_framework="""
        AWS filler metal classification and selection:
        1. Identify base metal minimum tensile strength (e.g., A36 = 58 ksi, A572 Gr50 = 65 ksi)
        2. Select filler metal with equal or greater strength (e.g., E70XX for 50-70 ksi base metals)
        3. Determine welding position requirements (all-position vs flat/horizontal only)
        4. Evaluate coating/flux type for electrode (rutile for smooth bead, low-H for crack resistance)
        5. For wire processes (GMAW/SAW), select electrode-flux/gas combination per AWS A5.X
        6. Consider impact toughness requirements (some classifications have CVN minimums)
        7. Verify compatibility with base metal chemistry (austenitic filler for stainless, etc.)
        8. Review moisture sensitivity (low-H electrodes require 250-300°F storage)
        9. Confirm availability and cost (exotic filler metals have long lead times)
        10. Document filler metal specification on WPS

        AWS SMAW Electrode Classification (e.g., E7018):
        - E: Electrode
        - 70: Tensile strength (70,000 psi minimum)
        - 1: Welding positions (0=flat/horizontal, 1=all, 2=flat/horizontal fillet, 4=downhill)
        - 8: Coating type and current (low-H iron powder, AC/DC+)

        AWS GMAW Wire Classification (e.g., ER70S-6):
        - ER: Electrode or Rod
        - 70: Tensile strength (70 ksi)
        - S: Solid wire
        - 6: Chemical composition (deoxidizer level)

        Critical: Hydrogen content classification (SMAW):
        H16 = <= 16 ml H2 per 100g weld metal
        H8 = <= 8 ml H2 per 100g (more stringent)
        H4 = <= 4 ml H2 per 100g (most stringent, offshore/subsea)
        """,
        key_factors=[
            "Base metal strength matching (undermatching causes weld failure)",
            "Notch toughness requirements (CVN testing at design temperature)",
            "Hydrogen cracking susceptibility (high strength steels require low-H)",
            "Welding position (overhead requires different coating than flat)",
            "Shielding gas compatibility for GMAW/FCAW wires",
            "Moisture exposure (low-H electrodes absorb moisture from air)",
            "Dilution considerations (first pass has ~50% dilution from base metal)"
        ],
        primary_authority=[
            "AWS A5.1 Carbon Steel Electrodes for SMAW",
            "AWS A5.18 Carbon Steel Filler Metals for GMAW/GTAW",
            "AWS A5.20 Carbon Steel Electrodes for FCAW",
            "AWS A5.28 Low-Alloy Filler Metals for GMAW/GTAW"
        ],
        burden_holder="Welding engineer to specify compatible filler metal on WPS",
        adversary_position="Purchasing may substitute cheaper filler metal without consulting engineering",
        counter_arguments=[
            "Premium filler metals (low-H, high-toughness) cost 2-3x standard grades",
            "Specialized storage ovens required for low-H electrodes (energy cost)",
            "Matching base metal strength may require exotic filler (long lead time)",
            "Some applications over-specify filler metal (E7018 when E6010 sufficient)",
            "Multiple filler metal types complicate inventory management"
        ],
        resolution_strategy="Standardize on versatile grades (E7018, ER70S-6) to reduce SKUs; qualify alternatives as backups",
        entity_scope="Applicable to all arc welding processes and material combinations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="AWS filler metal specifications are industry standard and code-referenced",
        controlling_precedent="ASME Section II Part C includes AWS filler metal specifications by reference",
        issue_categories=[IssueCategory.FILLER_METAL, IssueCategory.MATERIAL_SPECIFICATION],
        zones=[AnalysisZone.PLANNING]
    ),

    DoctrineBlock(
        topic="Weld Joint Design and Preparation",
        keywords=["joint design", "groove angle", "root opening", "land", "bevel", "j-groove", "u-groove", "backing strip"],
        conclusion_template=[
            "Joint preparation affects weld accessibility, fusion quality, and filler metal consumption.",
            "Groove angle too narrow causes lack of fusion on sidewalls; too wide wastes filler metal.",
            "Root opening and land dimensions control penetration and prevent burn-through."
        ],
        reasoning_framework="""
        Weld joint design considerations:
        1. Select joint type based on material thickness and loading (butt, corner, tee, lap, edge)
        2. Determine groove geometry for butt joints (V, bevel, J, U, double-V, double-U)
        3. Specify groove angle (60° total for V-groove typical; 45° for J-groove)
        4. Define root opening (gap between members): 1/16" - 1/8 inch typical for SMAW/GTAW root pass
        5. Establish root face (land) dimension: 1/16 inch typical to prevent burn-through
        6. Consider backing (consumable insert, backing strip, or open root)
        7. Evaluate bevel preparation method (flame cutting, machining, grinding)
        8. Calculate weld volume and filler metal required (cost estimation)
        9. Verify joint configuration is prequalified (AWS D1.1 Figure 3.3) or requires testing
        10. Document joint detail on WPS with dimensioned sketch

        Joint Type Selection by Thickness:
        - Thin (< 3/16"): Square groove butt (no bevel) or lap/fillet
        - Medium (3/16" - 3/4"): Single-V or single-bevel groove
        - Thick (3/4" - 1-1/2"): Single-V with backing or double-V (no backing)
        - Very thick (> 1-1/2"): Double-U or J-groove (reduced filler metal vs V-groove)

        Critical: J-groove and U-groove reduce weld volume by ~30% vs V-groove for thick sections,
        saving filler metal and reducing distortion. However, J/U require machining (higher prep cost).
        """,
        key_factors=[
            "Material thickness dictates groove type and angle",
            "Welding process affects root opening tolerance (GTAW needs tight fit-up)",
            "Access to both sides of joint (single-side access requires backing or skilled open root)",
            "Distortion control (double-V/U grooves balance shrinkage)",
            "Filler metal cost vs preparation cost trade-off",
            "Code prequalification status (prequalified joints avoid procedure testing)",
            "Fit-up tolerance in field (production joints rarely perfect)"
        ],
        primary_authority=[
            "AWS D1.1 Figure 3.3 Prequalified Joint Details",
            "ASME Section IX QW-402 Welding Positions",
            "API 1104 Figure 3 Welding Positions for Pipe",
            "AWS A3.0 Welding Terms and Definitions"
        ],
        burden_holder="Design engineer to specify joint geometry on fabrication drawings",
        adversary_position="Fabricator may prefer simpler joint (V-groove) even if U-groove saves filler metal long-term",
        counter_arguments=[
            "Complex grooves (J, U) require machining (vs thermal cutting for V-groove)",
            "Tight fit-up difficult to achieve in field conditions",
            "Backing strips may be prohibited (crevice corrosion, fatigue concerns)",
            "Double-sided prep requires flipping heavy components",
            "Excessive root opening causes excessive reinforcement or lack of fusion"
        ],
        resolution_strategy="Use AWS D1.1 prequalified joints to avoid qualification testing; balance prep cost vs filler cost",
        entity_scope="Applies to all welded joints in structural, pressure vessel, and piping applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Joint design principles are empirically proven and code-defined",
        controlling_precedent="AWS D1.1 prequalified joint details widely accepted by building codes and inspection authorities",
        issue_categories=[IssueCategory.JOINT_DESIGN, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING]
    ),

    DoctrineBlock(
        topic="Weld Defects - Porosity",
        keywords=["porosity", "gas pocket", "wormhole", "piping porosity", "hydrogen porosity", "nitrogen", "shielding gas"],
        conclusion_template=[
            "Porosity results from gas entrapment during weld solidification (hydrogen, nitrogen, CO).",
            "Causes include contaminated base metal, moisture, inadequate shielding gas coverage, or excessive travel speed.",
            "Acceptance criteria per AWS D1.1: scattered porosity 3/32 inch diameter max, uniformly distributed porosity 1/8 inch cumulative max in any linear inch."
        ],
        reasoning_framework="""
        Porosity defect analysis and prevention:
        1. Identify porosity type: uniformly distributed, clustered, linear (piping), or surface breaking
        2. Determine gas source: moisture (H2), air contamination (N2), base metal outgassing (C+O->CO)
        3. Evaluate shielding effectiveness: gas flow rate, nozzle cleanliness, wind interference
        4. Inspect base metal cleanliness: oil, grease, paint, rust, mill scale
        5. Check filler metal storage: low-H electrodes exposed to moisture produce porosity
        6. Review travel speed: excessive speed traps gas before it escapes to surface
        7. Verify arc length: long arc allows atmospheric contamination
        8. Consider base metal chemistry: high sulfur or phosphorus increases porosity susceptibility
        9. Apply acceptance criteria per code (AWS D1.1 Section 6.12, ASME Section VIII Appendix 7)
        10. Repair if rejectable: grind out, clean, re-weld per qualified repair procedure

        Common Porosity Causes by Process:
        - SMAW: Damp electrodes, long arc, contaminated base metal
        - GMAW: Insufficient gas flow, spatter in nozzle, wind drafts, rusty wire
        - GTAW: Inadequate argon purge, tungsten contamination, base metal outgassing
        - FCAW: Moisture in flux core, excessive voltage (gas expansion)

        Critical: Piping porosity (elongated gas tunnels) is more detrimental than scattered porosity
        due to stress concentration. Often caused by contamination or crater cracking at arc stop.
        """,
        key_factors=[
            "Shielding gas purity and flow rate (35-50 CFH typical for GMAW)",
            "Base metal surface preparation (solvent clean, wire brush, grind if needed)",
            "Filler metal storage conditions (low-H electrodes, wire free of rust)",
            "Welding technique (travel speed, arc length, work angle)",
            "Environmental conditions (wind, humidity, temperature)",
            "Material chemistry (deoxidized killed steel resists porosity better than rimmed)",
            "Joint design (deep narrow grooves trap gas)"
        ],
        primary_authority=[
            "AWS D1.1 Section 6.12 Porosity Acceptance Criteria",
            "ASME Section VIII Appendix 7 Porosity Charts",
            "API 1104 Section 9.3 Defect Acceptance Standards",
            "AWS B1.10 Guide for the Nondestructive Examination of Welds"
        ],
        burden_holder="Welder/operator to maintain proper technique and base metal cleanliness",
        adversary_position="Inspector may reject scattered porosity that meets code acceptance criteria",
        counter_arguments=[
            "Some porosity is cosmetic and doesn't affect structural integrity",
            "Rework cost often exceeds risk of minor porosity in non-critical welds",
            "Acceptance criteria vary by code (AWS more lenient than ASME)",
            "RT may reveal subsurface porosity not visible on surface",
            "Complete porosity elimination unrealistic in production welding"
        ],
        resolution_strategy="Document acceptance criteria in project specification; train inspectors on code requirements",
        entity_scope="Porosity is evaluated in all welding codes and NDT methods",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Porosity acceptance criteria are quantified and code-defined",
        controlling_precedent="AWS D1.1 and ASME Section VIII provide clear acceptance/rejection limits",
        issue_categories=[IssueCategory.WELD_DEFECT, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Weld Defects - Lack of Fusion and Incomplete Penetration",
        keywords=["lack of fusion", "lof", "incomplete penetration", "lack of sidewall fusion", "cold lap", "root penetration"],
        conclusion_template=[
            "Lack of fusion (LOF) is failure of weld metal to fuse with base metal or previous weld pass.",
            "Incomplete penetration occurs when weld fails to extend through full joint thickness.",
            "Both defects are planar and crack-like, therefore rejectable under all major welding codes."
        ],
        reasoning_framework="""
        Lack of fusion and incomplete penetration analysis:
        1. Distinguish LOF (sidewall, inter-bead) from incomplete penetration (root)
        2. Identify cause: insufficient heat input, improper travel angle, contaminated surfaces
        3. Evaluate joint design: narrow groove angle limits electrode access to sidewalls
        4. Review welding parameters: amperage too low reduces penetration and fusion
        5. Inspect electrode/wire positioning: improper work angle causes LOF on one side
        6. Consider travel speed: excessive speed prevents adequate fusion time
        7. Check for mill scale, rust, or slag preventing fusion
        8. For root penetration, verify root opening, land, and backing (if used)
        9. Apply rejection criteria: LOF and IP are always rejectable per AWS D1.1 Section 6.9
        10. Repair: gouge out defect to sound metal, re-weld with adequate heat input

        Common Causes by Defect Location:
        - Sidewall LOF: Narrow groove, improper work angle, low amperage, fast travel
        - Inter-bead LOF: Slag not removed between passes, convex bead shape (undercut valley)
        - Incomplete root penetration: Insufficient root opening, land too thick, low amperage
        - Root LOF (lack of root fusion): Backing bar interference, root pass too small

        Critical: LOF and IP are planar defects oriented perpendicular to principal stress,
        making them highly susceptible to crack initiation and propagation. Zero tolerance.
        """,
        key_factors=[
            "Heat input (amperage x voltage / travel speed) must be sufficient",
            "Electrode manipulation technique (weave, pause at sidewalls)",
            "Joint geometry (groove angle adequate for electrode access)",
            "Surface cleanliness (slag, mill scale, rust prevent fusion)",
            "Root preparation (opening and land dimensions)",
            "Welding position (overhead position increases LOF risk)",
            "Filler metal fluidity (some filler metals wet sidewalls better)"
        ],
        primary_authority=[
            "AWS D1.1 Section 6.9 Lack of Fusion/Penetration - Not Permitted",
            "ASME Section VIII Appendix 7 - Planar Defects Unacceptable",
            "API 1104 Section 9.3.3 - Incomplete Fusion Rejectable",
            "AWS B1.10 Guide for Nondestructive Examination"
        ],
        burden_holder="Welder to maintain proper technique; inspector to detect via UT or RT",
        adversary_position="Some argue minor LOF in non-critical welds is acceptable if stress is low",
        counter_arguments=[
            "LOF detection requires UT or RT (visual inspection cannot detect subsurface LOF)",
            "Repair is costly (gouging, NDE re-inspection, possible re-PWHT)",
            "In low-stress applications, engineering analysis may justify acceptance",
            "Complete elimination requires slower travel speeds (productivity impact)",
            "Some codes (e.g., AWS D1.1 Annex A seismic) have zero tolerance"
        ],
        resolution_strategy="Emphasize crack-like nature of planar defects; demonstrate fracture mechanics analysis if acceptance considered",
        entity_scope="LOF and IP are rejectable in all structural, pressure vessel, and piping codes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="LOF and IP rejection is universally accepted across all welding codes",
        controlling_precedent="Planar defects have caused catastrophic failures (Liberty ships, offshore platforms, pipelines)",
        issue_categories=[IssueCategory.WELD_DEFECT, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Weld Defects - Cracks (Hot Cracks and Cold Cracks)",
        keywords=["cracking", "hot crack", "cold crack", "hydrogen cracking", "solidification cracking", "liquation cracking", "lamellar tearing"],
        conclusion_template=[
            "Hot cracks occur during solidification due to low-melting segregates or excessive restraint.",
            "Cold cracks (hydrogen-induced) form after cooling due to hydrogen, hard microstructure, and residual stress.",
            "All cracks are rejectable under every major welding code; no acceptance criteria exist."
        ],
        reasoning_framework="""
        Crack defect analysis and prevention:
        1. Classify crack type: hot (solidification, liquation, crater) or cold (HAZ, underbead, toe)
        2. Hot crack causes: high sulfur/phosphorus, excessive dilution, center-line shrinkage, restraint
        3. Cold crack causes: hydrogen + martensite + residual stress (three factors required)
        4. Evaluate material chemistry: CE > 0.45 increases cold crack susceptibility
        5. Review filler metal selection: matching vs overmatching strength affects crack resistance
        6. Assess restraint level: highly restrained joints concentrate stress at weld
        7. Verify preheat and PWHT: slow cooling prevents martensite, PWHT diffuses hydrogen
        8. Inspect for crater cracks: improper arc termination leaves shrinkage cavity
        9. Check for lamellar tearing: through-thickness stress on laminated plate (steel directionality)
        10. Rejection and repair: grind out crack plus 1 inch margin, NDE to verify removal, re-weld

        Hot Crack Prevention:
        - Reduce dilution (smaller weld beads, lower heat input)
        - Select low-sulfur base metal (S < 0.035%)
        - Use crack-resistant filler (austenitic stainless for duplex solidification)
        - Minimize restraint (reduce weld length, sequence to control shrinkage)
        - Avoid crater cracks (fill crater before breaking arc, use run-off tabs)

        Cold Crack Prevention:
        - Preheat to slow cooling rate (prevent martensite formation in HAZ)
        - Use low-hydrogen filler metal (H4 or H8 classification)
        - PWHT to diffuse hydrogen and temper HAZ
        - Delay inspection 48-72 hours (cold cracks form slowly as hydrogen diffuses to high-stress areas)

        Critical: Hydrogen cracking can occur days or weeks after welding as hydrogen migrates
        to high-stress regions. Common locations: HAZ toe, root, weld centerline (underbead).
        """,
        key_factors=[
            "Material carbon equivalent and hardenability",
            "Hydrogen content of filler metal and base metal moisture",
            "Cooling rate (fast cooling forms martensite)",
            "Residual stress magnitude (restraint level)",
            "Sulfur and phosphorus content (promote hot cracking)",
            "Weld bead shape (convex beads concentrate stress at toes)",
            "Delayed inspection timing (wait 48+ hours for hydrogen cracks to develop)"
        ],
        primary_authority=[
            "AWS D1.1 Section 6.10 Cracks - Not Permitted",
            "ASME Section VIII UW-35 Repairs of Weld Defects",
            "API 1104 Section 9.3.1 Cracks - Rejectable",
            "AWS D1.8 Seismic Supplement (enhanced crack prevention measures)"
        ],
        burden_holder="Welding engineer to specify preheat, low-H filler, and PWHT to prevent cracking",
        adversary_position="No adversary accepts cracks; all parties agree cracks are rejectable",
        counter_arguments=[
            "Micro-cracks < 1/16 inch sometimes argued as non-detrimental (still rejectable by code)",
            "Destructive testing required to confirm crack depth and extent",
            "Repair may introduce new crack risk if not properly executed",
            "Some surface indications are not cracks (undercut, toe geometry)",
            "Thermal stress relief during repair may cause distortion"
        ],
        resolution_strategy="Zero tolerance for cracks; focus on prevention via proper WPS and execution",
        entity_scope="Crack prohibition is universal across all welding codes and applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Crack rejection is absolute and non-negotiable in all welding standards",
        controlling_precedent="Cracking has caused catastrophic failures in every industry (bridges, ships, platforms, pipelines)",
        issue_categories=[IssueCategory.WELD_DEFECT, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Ultrasonic Testing (UT) for Weld Inspection",
        keywords=["ultrasonic testing", "ut", "phased array", "paut", "tofd", "shear wave", "longitudinal wave", "asme section v"],
        conclusion_template=[
            "UT uses high-frequency sound waves to detect internal discontinuities without destroying the weld.",
            "Shear wave angle beam technique (45° or 60°) is standard for weld inspection.",
            "Phased array UT (PAUT) provides sectorial scanning and improved defect characterization vs conventional UT."
        ],
        reasoning_framework="""
        Ultrasonic testing application and technique:
        1. Select UT method: conventional angle beam, PAUT, or TOFD (Time of Flight Diffraction)
        2. Determine frequency: 2-5 MHz typical (higher frequency = better resolution, less penetration)
        3. Choose probe angle: 45° for thin sections, 60° or 70° for thick sections
        4. Calibrate on reference block (IIW or AWS block) per ASME Section V Article 5
        5. Establish DAC (Distance Amplitude Correction) curve for sizing
        6. Perform scanning: longitudinal for laminations, shear wave for volumetric defects
        7. Identify reflectors: amplitude, location, extent, orientation
        8. Size defects using 6 dB drop method or TOFD diffraction signals
        9. Record indications and apply acceptance criteria (ASME Section VIII Appendix 12, AWS D1.1)
        10. Verify critical indications with second method (RT, MT, or destructive sectioning)

        UT Advantages:
        - No radiation safety concerns (vs RT)
        - Detects planar defects (LOF, cracks) better than RT
        - Provides depth information (through-thickness location)
        - Portable equipment (battery-powered units)
        - Immediate results (vs RT film processing delay)

        UT Limitations:
        - Requires skilled operator (Level II or III per SNT-TC-1A)
        - Surface condition critical (rough surface scatters sound)
        - Complex geometry difficult to scan
        - Coarse-grained materials (stainless steel castings) attenuate sound
        - Porosity difficult to size accurately (small spherical reflectors)

        Critical: PAUT (phased array) uses multi-element probe to electronically steer beam,
        providing S-scan (sectorial) or linear scan images. AWS D1.5 Bridge Welding Code
        permits PAUT as alternative to RT for fracture-critical welds.
        """,
        key_factors=[
            "Material thickness and grain structure (affects frequency selection)",
            "Weld geometry (probe placement and angle beam path)",
            "Surface condition (grinding smooth may be required for coupling)",
            "Defect orientation (UT detects perpendicular reflectors best)",
            "Operator certification level (Level II minimum, Level III for procedure write-up)",
            "Couplant type (gel, glycerin, or water depending on temperature and orientation)",
            "Acceptance criteria (ASME Appendix 12 vs AWS D1.1 Section 6 vs API 1104 Appendix A)"
        ],
        primary_authority=[
            "ASME Section V Article 5 Ultrasonic Examination Methods",
            "AWS D1.1 Section 6 Inspection (UT alternative to RT)",
            "AWS D1.5 Bridge Welding Code (PAUT for fracture-critical)",
            "API 1104 Appendix A Ultrasonic Inspection Alternative to Radiography"
        ],
        burden_holder="Inspection contractor to provide certified UT operators and calibrated equipment",
        adversary_position="Some clients prefer RT for permanent film record despite UT advantages",
        counter_arguments=[
            "UT requires operator interpretation (subjective vs RT film objectivity)",
            "UT procedures must be qualified per ASME Section V Appendix I or AWS",
            "PAUT equipment cost significantly higher than conventional UT",
            "Surface preparation adds labor cost (grinding weld cap and sides)",
            "UT indications require amplitude-based acceptance (false calls possible)"
        ],
        resolution_strategy="Demonstrate UT superior crack detection vs RT; use PAUT for complex geometries and data archiving",
        entity_scope="UT applicable to all weld types in pressure vessels, piping, structural steel, and pipelines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="UT methods are code-qualified and widely accepted as RT alternative",
        controlling_precedent="ASME Section V Article 5 and AWS D1.1 establish UT as primary NDE method",
        issue_categories=[IssueCategory.NDT_METHOD, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Radiographic Testing (RT) for Weld Inspection",
        keywords=["radiography", "rt", "x-ray", "gamma ray", "film", "digital radiography", "iridium-192", "asme section v"],
        conclusion_template=[
            "RT produces permanent image of weld internal discontinuities via radiation attenuation.",
            "Film radiography provides archival record; digital RT (CR/DR) offers faster results and no chemical processing.",
            "RT excels at detecting volumetric defects (porosity, slag) but less effective for planar defects (cracks, LOF) than UT."
        ],
        reasoning_framework="""
        Radiographic testing application and technique:
        1. Select radiation source: X-ray (portable or stationary) or gamma (Ir-192, Co-60, Se-75)
        2. Determine film type and speed: D4, D5, D7 per ASTM E1742 (higher speed = less exposure time)
        3. Calculate exposure parameters: source-to-film distance (SFD), exposure time, activity
        4. Position source and film: single-wall single-image (SWSI) or double-wall techniques
        5. Use penetrameters (IQI) to verify image quality: hole-type (ASME) or wire-type (EN)
        6. Expose film, process in darkroom (or use digital detector for CR/DR)
        7. Interpret radiograph on illuminator per ASME Section V Article 2 / AWS B1.11
        8. Identify defects: porosity (round dark spots), slag (elongated irregular), cracks (sharp linear)
        9. Apply acceptance criteria: ASME Section VIII Appendix 7, AWS D1.1 Section 6, API 1104 Section 9
        10. Archive film per code requirements (often 5 years minimum retention)

        RT Technique Selection:
        - SWSI (single-wall single-image): Film inside pipe, source outside (best image quality)
        - SWDI (single-wall double-image): Film outside, source inside (two wall images superimposed)
        - DWSI (double-wall single-image): Film outside pipe, source outside opposite side (offshore/subsea)
        - Tangential: For nozzle welds, branch connections (oblique angle to capture weld profile)

        Critical: RT exposes film to radiation passing through weld. Thicker or denser material
        attenuates more radiation (appears lighter on film). Defects attenuate less (appear darker).
        IQI (Image Quality Indicator) confirms sufficient contrast sensitivity to detect code-size defects.
        """,
        key_factors=[
            "Material thickness and density (determines radiation energy and exposure time)",
            "Source type selection (X-ray portable for field, gamma for remote areas)",
            "Film sensitivity and grain size (D7 finest grain, slowest speed)",
            "Image quality indicator (penetrameter) demonstrates sensitivity",
            "Radiation safety (10 CFR Part 20, state licensing, dosimetry, exclusion zones)",
            "Film processing quality (developer temperature, agitation, fixing time)",
            "Viewing conditions (illuminator brightness, ambient light, reader certification)"
        ],
        primary_authority=[
            "ASME Section V Article 2 Radiographic Examination",
            "AWS B1.11 Guide for the Visual Examination of Welds",
            "ASTM E1742 Standard Practice for Radiographic Examination",
            "API 1104 Section 8 Radiographic Inspection"
        ],
        burden_holder="Radiography contractor to provide licensed operators, calibrated equipment, and film interpretation",
        adversary_position="Owner may prefer UT to avoid radiation safety exclusion zones and film processing delays",
        counter_arguments=[
            "RT requires radiation safety program (licensing, dosimetry, training, barriers)",
            "Film processing 24-48 hour delay (vs UT immediate results)",
            "Digital RT equipment cost very high (CR systems ~$50K, DR systems ~$200K+)",
            "RT misses tight cracks and LOF oriented parallel to beam",
            "Gamma sources decay over time (Ir-192 half-life 74 days, requires frequent replacement)"
        ],
        resolution_strategy="RT remains gold standard for porosity/slag detection and provides archival record; combine with UT for comprehensive NDE",
        entity_scope="RT applicable to all material types and thicknesses, limited only by radiation penetration",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="RT is ASME Section VIII mandatory examination method for many pressure vessel welds",
        controlling_precedent="ASME Section VIII UW-51 requires RT or UT for full penetration butt welds in many applications",
        issue_categories=[IssueCategory.NDT_METHOD, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Magnetic Particle Testing (MT) for Surface Crack Detection",
        keywords=["magnetic particle", "mt", "wet fluorescent", "dry powder", "yoke", "prod", "surface cracks", "asme section v"],
        conclusion_template=[
            "MT detects surface and near-surface discontinuities in ferromagnetic materials via magnetic flux leakage.",
            "Wet fluorescent MT provides highest sensitivity; dry powder MT suitable for field applications.",
            "MT is mandatory for detecting surface cracks after weld repairs and stress relief."
        ],
        reasoning_framework="""
        Magnetic particle testing application and technique:
        1. Verify material is ferromagnetic (carbon steel, low alloy; not stainless 300-series or aluminum)
        2. Select magnetization method: yoke (easiest, portable), prods (high amperage, burn risk), coil (circumferential)
        3. Choose particle type: wet fluorescent (highest sensitivity), dry powder (field use, no UV light needed)
        4. Clean surface: remove oil, grease, weld spatter, loose scale
        5. Apply magnetizing current: AC (surface cracks), DC (subsurface), half-wave DC (compromise)
        6. Orient magnetic field perpendicular to expected defect (requires two shots 90° apart for unknown orientation)
        7. Apply magnetic particles while current is on (continuous method) or immediately after (residual method)
        8. Inspect under UV-A light (365 nm, 1000 µW/cm² minimum) for fluorescent particles
        9. Record indications: linear (crack), rounded (porosity), non-relevant (magnetic write, edge effect)
        10. Demagnetize after inspection if part will undergo machining or welding (residual magnetism affects arc blow)

        MT Sensitivity by Particle Type:
        - Wet fluorescent: Detects cracks < 0.001 inch opening under UV light (highest sensitivity)
        - Dry powder: Detects cracks > 0.003 inch opening in visible light (field portable)
        - Magnetic rubber: Permanent record of indication (rarely used except for training)

        Critical: MT only works on ferromagnetic materials. Austenitic stainless steel (304, 316)
        is non-magnetic and requires PT (penetrant testing) instead. Welds must be ground smooth
        for MT to avoid false indications from surface roughness. Arc strikes create magnetic
        write patterns that look like cracks (demagnetize to confirm).
        """,
        key_factors=[
            "Material magnetic permeability (carbon steel ideal, austenitic stainless unsuitable)",
            "Surface condition (rough as-welded surface causes particle accumulation)",
            "Magnetization direction (must be perpendicular to defect for detection)",
            "Particle suspension concentration (wet method requires bath concentration check)",
            "UV light intensity (verify with UV meter before inspection)",
            "Prod burn risk (high amperage can arc to part, creating craters)",
            "Demagnetization after inspection (prevent arc blow in subsequent welding)"
        ],
        primary_authority=[
            "ASME Section V Article 7 Magnetic Particle Examination",
            "ASTM E1444 Standard Practice for Magnetic Particle Testing",
            "AWS D1.1 Section 6.11 MT Acceptance Criteria",
            "API 1104 Section 8.3 Magnetic Particle Examination"
        ],
        burden_holder="Inspector to apply proper magnetization technique and interpret indications",
        adversary_position="Some argue PT (penetrant) is equivalent to MT for surface cracks (MT is more sensitive)",
        counter_arguments=[
            "MT requires ferromagnetic material (limits applicability)",
            "Surface preparation (grinding) adds labor cost",
            "Wet fluorescent method requires darkened area and UV light (difficult in bright sunlight)",
            "Prods can burn surface if held in one place (creates repair requirement)",
            "Non-relevant indications (magnetic write, scratch marks) require interpretation skill"
        ],
        resolution_strategy="MT is code-required for post-PWHT crack detection; wet fluorescent is most sensitive surface NDE method",
        entity_scope="MT applicable to carbon steel, low alloy steel welds after repair or stress relief",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="MT is ASME Section VIII mandatory examination for welds after thermal stress relief",
        controlling_precedent="ASME Section VIII UW-51(b) requires MT after weld repairs and PWHT",
        issue_categories=[IssueCategory.NDT_METHOD, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Liquid Penetrant Testing (PT) for Non-Magnetic Materials",
        keywords=["penetrant testing", "pt", "dye penetrant", "fluorescent penetrant", "developer", "dwell time", "stainless steel"],
        conclusion_template=[
            "PT detects surface-breaking discontinuities in any non-porous material regardless of magnetic properties.",
            "Fluorescent penetrant provides higher sensitivity than visible dye penetrant.",
            "PT is the only practical surface crack detection method for austenitic stainless steel and aluminum."
        ],
        reasoning_framework="""
        Liquid penetrant testing application and technique:
        1. Select penetrant type: fluorescent (Type 1) or visible dye (Type 2), sensitivity level (1/2/3/4)
        2. Clean surface thoroughly: solvent clean, water rinse, dry (critical step; contamination prevents penetration)
        3. Apply penetrant by spray, brush, or immersion; ensure complete coverage
        4. Dwell time: minimum 10 minutes (Type 1-A fluorescent post-emulsifiable) up to 60 minutes for deep/tight cracks
        5. Remove excess penetrant: water wash (water-washable), emulsifier (post-emulsifiable), or solvent wipe (solvent-removable)
        6. Dry surface completely (forced air or oven, temperature < 125°F to avoid over-drying)
        7. Apply developer: dry powder, non-aqueous wet, or aqueous wet (draws penetrant back to surface via blotting action)
        8. Develop indications: 7-30 minutes development time before inspection
        9. Inspect under UV-A light (fluorescent) or white light (visible dye) for indications
        10. Record indications: linear (crack), rounded (porosity), non-relevant (scratches, tool marks)

        PT Penetrant Systems (Sensitivity):
        - Type 1 Method A (fluorescent post-emulsifiable): Highest sensitivity, best for aerospace/nuclear
        - Type 1 Method C (fluorescent solvent-removable): High sensitivity, portable field use
        - Type 2 Method C (visible dye solvent-removable): Lower sensitivity, no UV light needed, low cost

        Critical: PT developer is NOT paint — it's a porous medium (talc, silica) that wicks penetrant
        from defect back to surface via capillary action, making indication visible. Excessive developer
        thickness obscures indications. Surface must be bone-dry before developer application.
        """,
        key_factors=[
            "Surface cleanliness (oil, grease, water prevent penetrant entry into defects)",
            "Penetrant dwell time (deep tight cracks need longer dwell)",
            "Removal technique (over-washing removes penetrant from defects; under-washing leaves background)",
            "Developer application (uniform thin coat, not thick paint-like layer)",
            "Temperature (penetrant freezes < 40°F, loses sensitivity > 125°F)",
            "UV light intensity (fluorescent PT requires 1000 µW/cm² minimum)",
            "Indication interpretation (distinguish cracks from non-relevant indications)"
        ],
        primary_authority=[
            "ASME Section V Article 6 Liquid Penetrant Examination",
            "ASTM E1417 Standard Practice for Liquid Penetrant Testing",
            "AWS D1.6 Structural Welding Code - Stainless Steel (PT for surface examination)",
            "AMS 2644 Aerospace Material Specification for Penetrant Inspection"
        ],
        burden_holder="Inspector to follow proper PT procedure and interpret indications",
        adversary_position="Some argue PT is too sensitive and detects irrelevant surface roughness",
        counter_arguments=[
            "PT requires very clean surface (time-consuming preparation)",
            "Fluorescent PT requires UV light and darkened area (field logistics)",
            "PT detects only surface-breaking defects (not subsurface)",
            "Consumable cost (penetrant, remover, developer) for large surface areas",
            "Non-relevant indications (grinding marks, etch marks) require experience to dismiss"
        ],
        resolution_strategy="PT is only option for austenitic stainless and aluminum surface crack detection; lower sensitivity acceptable for non-critical welds",
        entity_scope="PT applicable to all non-porous materials: stainless, aluminum, titanium, nickel alloys, even plastics/ceramics",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="PT is ASME and AWS code-approved method for non-ferromagnetic materials",
        controlling_precedent="ASME Section V Article 6 and AWS D1.6 establish PT as primary surface NDE for stainless steel",
        issue_categories=[IssueCategory.NDT_METHOD, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Visual Inspection (VT) and Acceptance Criteria",
        keywords=["visual inspection", "vt", "weld profile", "undercut", "overlap", "reinforcement", "acceptance criteria", "aws d1.1"],
        conclusion_template=[
            "Visual inspection is the primary and most cost-effective NDE method, performed on 100% of welds.",
            "VT detects surface discontinuities (cracks, undercut, overlap, insufficient reinforcement) and dimensional non-conformance.",
            "AWS D1.1 and ASME Section VIII provide specific acceptance limits for undercut depth, reinforcement height, and profile."
        ],
        reasoning_framework="""
        Visual inspection technique and acceptance criteria:
        1. Inspect during welding (inter-pass): verify slag removal, no cracks between passes
        2. Inspect after welding completion: overall weld profile, reinforcement, undercut, overlap
        3. Use proper lighting: 100 foot-candles minimum (1000 lux) on inspection surface
        4. Employ magnification if needed: 10x magnifier for crack detection
        5. Measure weld size: fillet leg length with weld gauge, reinforcement height with machinist rule
        6. Check undercut depth: < 1/32 inch typically acceptable (AWS D1.1), 0.01 inch maximum (ASME Section VIII)
        7. Verify no overlap (cold lap): weld face must transition smoothly to base metal
        8. Confirm reinforcement within limits: <= 1/8 inch for <= 1 inch thick base metal (AWS D1.1 Table 6.1)
        9. Inspect for surface cracks: none permitted (may require MT or PT to confirm)
        10. Document results on inspection report with accept/reject disposition per code

        AWS D1.1 Visual Acceptance Criteria (Section 6.9):
        - Cracks: None permitted
        - Fusion: Complete fusion required (no LOF visible on surface)
        - Craters: Filled to full cross-section (no shrinkage cavities)
        - Weld profiles: Uniform with gradual transitions
        - Undercut: <= 1/32 inch for non-cyclically loaded, <= 0.01 inch for cyclically loaded
        - Reinforcement: <= 1/8 inch for t <= 1", <= 3/16 inch for t > 1"
        - Overlap: None permitted

        Critical: Visual inspection is performed by Certified Welding Inspector (CWI) per AWS QC1.
        Inspector must have near vision acuity (Jaeger J2 or equivalent) verified annually.
        VT cannot detect subsurface defects; supplemented by UT or RT per code requirements.
        """,
        key_factors=[
            "Lighting adequacy (100 fc minimum, shadow-free illumination)",
            "Inspector vision acuity (near vision chart, color vision for PT/MT)",
            "Weld accessibility (confined space, overhead position limit inspection quality)",
            "Surface condition (slag, spatter must be removed before VT)",
            "Code of construction (AWS D1.1 vs ASME Section VIII criteria differ)",
            "Cyclically loaded vs static (fatigue-critical welds have tighter undercut limits)",
            "Dimensional conformance (weld size, length, location per drawing)"
        ],
        primary_authority=[
            "AWS D1.1 Section 6 Inspection",
            "ASME Section VIII UW-35 Requirements for Welds",
            "AWS QC1 Standard for AWS Certification of Welding Inspectors",
            "API 1104 Section 8.2 Visual Inspection"
        ],
        burden_holder="Certified Welding Inspector (CWI) to perform VT and apply code acceptance criteria",
        adversary_position="Welders may argue minor undercut or reinforcement excess is cosmetic and doesn't affect strength",
        counter_arguments=[
            "VT is subjective (inspector judgment on borderline conditions)",
            "Undercut acceptance limits vary by code (AWS D1.1 vs ASME Section VIII)",
            "Some defects visible on surface require NDE confirmation (cracks vs tool marks)",
            "Reinforcement grinding to meet criteria adds labor cost",
            "Inspector certification requirements vary (CWI, CAWI, SCWI levels)"
        ],
        resolution_strategy="VT is foundation of weld QC; supplement with volumetric NDE (UT/RT) for critical applications",
        entity_scope="VT is mandatory first step for all welded construction across all codes",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="VT acceptance criteria are quantified and code-defined with minimal ambiguity",
        controlling_precedent="AWS D1.1 and ASME Section VIII visual acceptance criteria are industry standard",
        issue_categories=[IssueCategory.NDT_METHOD, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="API 1104 Pipeline Welding Standard",
        keywords=["api 1104", "pipeline welding", "5g position", "stovepipe", "tie-in weld", "cap pass", "pipeline inspection"],
        conclusion_template=[
            "API 1104 is the welding standard for oil and gas transmission pipelines.",
            "5G position (horizontal fixed pipe) is most common field position for mainline pipeline welding.",
            "API 1104 permits both radiographic and ultrasonic inspection with defined acceptance criteria."
        ],
        reasoning_framework="""
        API 1104 pipeline welding requirements:
        1. Qualify WPS per API 1104 Section 5 (alternative to ASME Section IX for pipelines)
        2. Determine joint design: V-bevel or J-bevel with or without backing
        3. Select filler metal: E6010 root, E7018 or E8018-C3 fill/cap for manual; ER70S-X for semi-automatic
        4. Establish preheat per Section 5.6 based on carbon equivalent and temperature
        5. Define welding parameters: amperage, voltage, travel speed ranges per WPS
        6. Perform root pass (stringer bead, no weave) for penetration and tie-in
        7. Execute fill passes (hot pass to burn out contaminants, then fill to flush)
        8. Apply cap pass(es) with proper reinforcement (1/16 inch to 3/32 inch typical)
        9. Inspect per Section 8: visual for 100%, RT or UT for percentage per project spec (often 10-100%)
        10. Repair defects per Section 7: grind out, re-weld, re-inspect (maximum 2 repairs per joint)

        API 1104 Welder Qualification (Section 6):
        - Test positions: 5G (horizontal fixed), 2G (vertical fixed), 6G (45° fixed)
        - Pipe diameters: < 2.375 inch (small bore), 2.375" - 12.75 inch (common), > 12.75 inch (large diameter)
        - Welding processes: SMAW, GMAW, FCAW, GTAW (root), SAW, combinations
        - Test coupons: 4 bend specimens (2 root, 2 face) plus optional tensile/nick-break

        Critical: API 1104 tie-in welds (field girth welds connecting pipe sections) are typically
        5G position welded from bottom (6 o'clock) upward on both sides to 12 o'clock (top).
        Stovepipe (vertical uphill progression) welds large-diameter pipe in 2G position.
        """,
        key_factors=[
            "Base metal grade (X42, X52, X60, X70, X80, X100 designate yield strength)",
            "Pipe diameter and wall thickness (affects heat input and cooling rate)",
            "Environmental conditions (temperature, wind, precipitation)",
            "Production welding rate (mainline vs tie-in vs station piping)",
            "Inspection percentage (100% RT for sour service, 10% random for sweet service typical)",
            "Defect acceptance criteria (API 1104 Table 9.3.2 for RT, Appendix A for UT)",
            "Repair limits (2 repairs maximum before pipe section rejection)"
        ],
        primary_authority=[
            "API 1104 Welding of Pipelines and Related Facilities",
            "ASME B31.4 Pipeline Transportation Systems for Liquid Hydrocarbons",
            "ASME B31.8 Gas Transmission and Distribution Piping Systems",
            "DOT 49 CFR Part 192 (gas) and Part 195 (liquid) Pipeline Safety Regulations"
        ],
        burden_holder="Pipeline contractor to provide qualified welders and inspection per API 1104",
        adversary_position="Owner may request 100% inspection to reduce failure risk (contractor argues 10% is code-compliant)",
        counter_arguments=[
            "100% RT on long pipelines is very expensive (miles of film)",
            "UT alternative faster and safer but requires operator certification",
            "Production welding rates vary widely (mechanized GMAW 200+ joints/day, manual SMAW 10-20 joints/day)",
            "Repair rate affects schedule (2% typical, 10% unacceptable productivity)",
            "Cold weather preheat requirements slow production"
        ],
        resolution_strategy="Balance inspection percentage against risk of failure; use UT for speed, RT for permanent record on critical segments",
        entity_scope="API 1104 applicable to all onshore and offshore oil/gas transmission pipelines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 1104 is DOT-recognized standard and legally enforceable for interstate pipelines",
        controlling_precedent="49 CFR Part 192/195 incorporates API 1104 by reference for pipeline construction",
        issue_categories=[IssueCategory.CODE_COMPLIANCE, IssueCategory.WELDING_PROCESS],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION, AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="AWS D1.1 Structural Welding Code - Steel",
        keywords=["aws d1.1", "structural steel", "prequalified wps", "certified welding inspector", "cwi", "fillet weld"],
        conclusion_template=[
            "AWS D1.1 is the primary structural steel welding code for buildings and bridges.",
            "Prequalified WPS (Table 3.7) eliminates need for procedure qualification testing within specified limits.",
            "Certified Welding Inspector (CWI) per AWS QC1 is industry standard for inspection personnel qualification."
        ],
        reasoning_framework="""
        AWS D1.1 structural welding code application:
        1. Determine if project is statically loaded or cyclically loaded (affects acceptance criteria)
        2. Select prequalified joint detail from Figure 3.3 or develop qualified WPS per Clause 4
        3. Verify base metal is weldable grade (ASTM A36, A572, A992, A500 common)
        4. Establish preheat per Table 3.2 based on thickness and lowest anticipated temperature
        5. Define fillet weld size (minimum per Table 2.4, maximum = base metal thickness)
        6. Specify complete joint penetration (CJP) or partial joint penetration (PJP) groove welds
        7. Qualify welders per Clause 4 (visual+bend testing, or visual-only for fillet welds)
        8. Inspect per Clause 6: visual 100%, UT or RT per engineer requirement
        9. Apply acceptance criteria: Table 6.1 for visual, Clause 6.12 for UT/RT
        10. Repair rejectable welds per Clause 5.26 (gouge, grind, re-weld, re-inspect)

        AWS D1.1 Prequalified WPS Benefits:
        - No mechanical testing required (tensile, bend tests waived)
        - Applies to complete joint penetration groove welds in Table 3.7 configurations
        - Fillet welds automatically prequalified (no procedure qualification needed)
        - Essential variables defined in Table 3.1 (stay within range to maintain prequalification)

        Critical: AWS D1.1 permits two welder qualification paths:
        1. Visual inspection + guided bend testing (qualifies all weld types and positions tested)
        2. Visual inspection only for fillet welds (unlimited thickness/size qualification)
        Groove weld qualification requires destructive bend testing.
        """,
        key_factors=[
            "Building vs bridge application (D1.1 vs D1.5 for fracture-critical bridges)",
            "Statically vs cyclically loaded (undercut limits tighter for cyclically loaded)",
            "Seismic application (D1.8 Seismic Supplement adds requirements)",
            "Base metal thickness and grade (affects preheat and filler metal selection)",
            "Joint accessibility (tight fit-up tolerances for prequalified joints)",
            "Welder certification continuity (6-month rule for maintaining qualification)",
            "Inspector certification (CWI required for most structural steel projects)"
        ],
        primary_authority=[
            "AWS D1.1 Structural Welding Code - Steel",
            "AWS D1.8 Seismic Supplement",
            "AISC 360 Specification for Structural Steel Buildings (references D1.1)",
            "IBC International Building Code (adopts AWS D1.1 by reference)"
        ],
        burden_holder="Contractor to follow AWS D1.1 WPS and employ qualified welders/inspectors",
        adversary_position="Some jurisdictions require specific inspection percentage (e.g., 100% CJP welds); D1.1 doesn't mandate",
        counter_arguments=[
            "Prequalified WPS limits joint configurations (custom joints require qualification testing)",
            "D1.1 fillet weld visual-only qualification may be inadequate for critical connections",
            "Preheat tables conservative (may add unnecessary cost in warm climates)",
            "CWI certification expensive ($2K+ including prep course and exam)",
            "Cyclically loaded acceptance criteria difficult to achieve (undercut <= 0.01 inch very tight)"
        ],
        resolution_strategy="Leverage prequalified WPS to avoid testing; use D1.8 Seismic Supplement for high-importance structures",
        entity_scope="AWS D1.1 covers all structural steel welding except bridges (D1.5) and rebar (D1.4)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="AWS D1.1 is legally adopted by IBC and most state/local building codes",
        controlling_precedent="AISC 360 and IBC mandate compliance with AWS D1.1 for structural welding",
        issue_categories=[IssueCategory.CODE_COMPLIANCE, IssueCategory.PROCEDURE_QUALIFICATION],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION, AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="NACE MR0175/ISO 15156 Sour Service Welding Requirements",
        keywords=["nace mr0175", "iso 15156", "sour service", "h2s", "hardness testing", "hrc 22", "sulfide stress cracking", "ssc"],
        conclusion_template=[
            "NACE MR0175/ISO 15156 limits material hardness to prevent sulfide stress cracking (SSC) in H2S environments.",
            "Maximum hardness HRC 22 (approximately HB 250) applies to base metal, weld metal, and HAZ.",
            "PWHT is often mandatory to reduce HAZ hardness below HRC 22 limit."
        ],
        reasoning_framework="""
        NACE MR0175/ISO 15156 sour service welding requirements:
        1. Identify H2S partial pressure and pH to determine if MR0175 applies (typically > 0.05 psia H2S)
        2. Select materials from MR0175 approved list (carbon steel, low alloy, CRA)
        3. Verify base metal hardness <= HRC 22 (or material-specific limit per MR0175-2 Table A.2)
        4. Select filler metal producing weld metal hardness <= HRC 22 (typically ER80S-D2 or similar)
        5. Qualify WPS with hardness testing: base metal, HAZ (1mm, 3mm, 5mm from fusion line), weld metal
        6. Establish preheat and interpass temperature to control HAZ cooling rate (slow cooling reduces hardness)
        7. Perform PWHT if required to temper HAZ to <= HRC 22 (often mandatory for >0.5 inch thickness or CE>0.45)
        8. Test hardness after PWHT at HAZ locations using HRC or HB tester (convert to HRC if needed)
        9. Document hardness results on PQR; all readings must be <= HRC 22
        10. Perform production hardness testing per project specification (random sampling or 100%)

        MR0175 Hardness Testing Locations:
        - Base metal: 6mm from weld fusion line (unaffected by welding)
        - HAZ: 1mm, 3mm, 5mm from weld fusion line (critical zone for SSC)
        - Weld metal: mid-thickness of weld deposit
        - All locations on both sides of weld

        Critical: Sulfide stress cracking (SSC) occurs when three factors combine: H2S presence,
        tensile stress (residual or applied), and susceptible material (hardness > HRC 22).
        Hard HAZ is most susceptible location. PWHT is most reliable mitigation.
        """,
        key_factors=[
            "H2S partial pressure and environment pH (determines MR0175 applicability)",
            "Material carbon equivalent (high CE increases hardness after welding)",
            "Weld cooling rate (faster cooling produces harder HAZ)",
            "PWHT temperature and time (must be sufficient to temper martensite)",
            "Filler metal chemistry (matching vs undermatching affects weld metal hardness)",
            "Production hardness testing frequency (statistical sampling vs 100% test)",
            "Hardness tester calibration (verify on test block before use)"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156 Petroleum and Natural Gas Industries - Materials for Use in H2S Environments",
            "ASME Section VIII Division 1 UHT Hardness Testing Requirements",
            "API 6A Wellhead and Christmas Tree Equipment (references MR0175)",
            "ASTM E92 Test Method for Vickers Hardness"
        ],
        burden_holder="Fabricator to perform PWHT and hardness testing per MR0175 requirements",
        adversary_position="Some argue HRC 22 limit is too conservative for low H2S concentrations",
        counter_arguments=[
            "Hardness testing 100% of production welds is very time-consuming",
            "PWHT adds significant cost for field welds (local PWHT equipment rental)",
            "HRC 22 limit difficult to achieve without PWHT for high-strength steels",
            "MR0175 applicability threshold (0.05 psia H2S) is debated (some say 0.3 psia more realistic)",
            "Portable hardness testers less accurate than lab benchtop testers"
        ],
        resolution_strategy="Follow MR0175 strictly for sour service applications; document hardness test results for liability protection",
        entity_scope="NACE MR0175 mandatory for oil/gas production equipment exposed to H2S",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="MR0175 is industry standard and legally incorporated into operator purchase specifications",
        controlling_precedent="API 6A, 17D, and operator company specifications mandate MR0175 compliance",
        issue_categories=[IssueCategory.CODE_COMPLIANCE, IssueCategory.MATERIAL_SPECIFICATION],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION, AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Repair Welding Procedures and Limitations",
        keywords=["weld repair", "excavation", "gouge", "grind", "repair limit", "preheat for repair", "nde after repair"],
        conclusion_template=[
            "Weld repairs require removal of defective material and re-welding per qualified repair procedure.",
            "Most codes limit number of repairs (often 2 maximum before component rejection).",
            "NDE after repair must demonstrate defect removal and acceptable re-weld quality."
        ],
        reasoning_framework="""
        Weld repair procedure and execution:
        1. Identify defect type, location, and extent via NDE (UT, RT, MT, PT, or VT)
        2. Mark defect boundaries with soapstone or marker (add 1 inch margin beyond defect extent)
        3. Remove defective weld metal via grinding, arc gouging, or machining
        4. Verify complete defect removal via re-NDE (MT or PT for surface, UT for volumetric)
        5. Prepare excavation for re-welding: smooth contour, proper groove angle if deep
        6. Apply preheat per WPS (often higher than original weld due to restraint and prior heat cycles)
        7. Re-weld using same WPS as original weld (or qualified repair procedure if different)
        8. Perform PWHT if required (local PWHT if original weld was PWHT'd)
        9. Perform final NDE (same method as original inspection) to verify acceptability
        10. Document repair on weld map and in QC records (location, size, NDE results, welder ID)

        Repair Limitations by Code:
        - AWS D1.1: 2 repairs maximum per CJP groove weld; unlimited repairs on fillet welds
        - ASME Section VIII: No specific limit, but engineering review required after 2 repairs
        - API 1104: 2 repairs maximum per girth weld; pipe section rejected after 2 failures
        - Nuclear (ASME Section III): Engineering analysis and NDE documentation for all repairs

        Critical: Each repair cycle work-hardens the HAZ and increases cracking susceptibility.
        After 2 repairs, base metal may be embrittled. Some critical applications (nuclear, aerospace)
        require engineering disposition for any repair. Repair welds in PWHT'd components require
        re-PWHT to avoid hard zones (localized hardness > HRC 22 in sour service is rejectable).
        """,
        key_factors=[
            "Defect type and severity (cracks require 100% removal; porosity may be excavated partially)",
            "Component criticality (pressure vessels have stricter repair limits than structural steel)",
            "Number of prior repairs (multiple repairs increase risk of cracking)",
            "Accessibility for excavation and re-welding (internal defects may require entry permit)",
            "PWHT requirements (local PWHT after repair if original weld was PWHT'd)",
            "NDE re-inspection method (same or more sensitive than original NDE)",
            "Code-specific repair limits and documentation requirements"
        ],
        primary_authority=[
            "ASME Section VIII UW-35 Requirements for Repair of Weld Defects",
            "AWS D1.1 Clause 5.26 Technique - Repair of Unacceptable Welds",
            "API 1104 Section 7 Repair of Welds",
            "ASME Section XI Rules for Inservice Inspection (repair of operating equipment)"
        ],
        burden_holder="Contractor to perform repairs per code requirements and document all repair activities",
        adversary_position="Owner may demand unlimited repairs to avoid scrapping expensive components",
        counter_arguments=[
            "Excessive repairs risk cracking due to cumulative heat cycles",
            "Each repair adds cost (excavation, NDE, re-weld, PWHT, re-NDE)",
            "Repair quality often lower than original weld (accessibility, fit-up issues)",
            "Code limits (2 repairs) are conservative; some repairs exceed limits successfully",
            "Repair documentation requirements add administrative burden"
        ],
        resolution_strategy="Follow code repair limits strictly; consider component replacement if chronic weld quality issues",
        entity_scope="Repair procedures apply to all codes and all weld types (groove, fillet, corner, edge)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Repair limits are code-defined to prevent cumulative damage from excessive rework",
        controlling_precedent="ASME Section VIII and API 1104 repair limits are minimum requirements for safety",
        issue_categories=[IssueCategory.REPAIR_WELDING, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.EXECUTION, AnalysisZone.INSPECTION]
    ),

    DoctrineBlock(
        topic="Weld Documentation and Traceability",
        keywords=["weld map", "material test report", "mtr", "mill certificate", "pqr", "wpq", "traveler", "data book"],
        conclusion_template=[
            "Weld documentation provides traceability from material procurement through final inspection.",
            "MTRs (Material Test Reports) verify chemistry and mechanical properties of base metal and filler metal.",
            "Weld maps, PQRs, WPQRs, and NDE reports comprise the permanent quality record."
        ],
        reasoning_framework="""
        Weld documentation system and traceability:
        1. Procurement: MTRs (mill certificates) for base metal and filler metal showing chemistry, tensile, CVN
        2. Procedure Qualification: PQRs documenting mechanical test results supporting each WPS
        3. Welder Qualification: WPQRs showing bend test or RT results for each qualified welder
        4. Production Welding: Weld maps or ISO drawings showing weld joint locations and IDs
        5. Inspection: NDE reports (RT films, UT scan data, MT/PT reports) for each weld joint
        6. Repairs: Repair log documenting location, defect type, excavation depth, re-weld details
        7. Heat Treatment: PWHT charts (time-temperature curves) with thermocouple locations
        8. Hardness Testing: HRC/HB hardness survey results for sour service applications
        9. Traceability: Weld joint ID -> welder ID -> WPS -> PQR -> filler metal heat -> base metal heat
        10. Data Book Assembly: Compile all records into indexed data book for client delivery

        Essential Documentation Elements:
        - Material Test Reports (MTRs): C, Mn, Si, S, P, Cr, Mo, Ni, Cu, yield, tensile, elongation, CVN
        - PQR: Actual welding parameters used, mechanical test results (tensile, bend, impact, hardness)
        - WPS: Parameter ranges (amperage, voltage, travel speed, preheat, interpass, PWHT)
        - WPQR: Welder name, test position, test date, bend test results, RT results (if used)
        - Weld Map: Isometric or plan drawing showing joint locations, joint IDs, weld sizes

        Critical: ASME Code stamp requires Authorized Inspector (AI) to review documentation
        and witness testing. AI signs off on data book as part of Code certification process.
        Material traceability prevents use of non-compliant materials (wrong grade, no impact testing, etc.).
        Heat numbers stamped on materials allow tracking from steel mill through fabrication.
        """,
        key_factors=[
            "Material heat traceability (heat numbers low-stress stamped or stenciled on materials)",
            "Filler metal lot tracking (electrode boxes, wire spool labels)",
            "Welder identification on weld map (stamp or ID tag on each joint)",
            "NDE report correlation to weld joint ID on map",
            "Data book organization (indexed by drawing, weld joint, or inspection type)",
            "Electronic document management (scanned PDFs vs paper records)",
            "Client-specific documentation requirements (beyond code minimums)"
        ],
        primary_authority=[
            "ASME Section VIII UG-93 Preparation of Reports and Nameplates",
            "AWS QC1 Standard for AWS Certification of Welding Inspectors (Section 8 - Documentation)",
            "API 6A Annex J Documentation Requirements for Wellhead Equipment",
            "ISO 3834 Quality Requirements for Fusion Welding of Metallic Materials"
        ],
        burden_holder="Fabricator to generate, compile, and deliver complete welding data book per code and contract",
        adversary_position="Client may request excessive documentation beyond code requirements (cost and schedule impact)",
        counter_arguments=[
            "Comprehensive documentation is time-consuming (engineering admin cost)",
            "MTR verification for every stick of steel impractical for large projects",
            "Electronic records acceptable per ASME but some clients still require paper originals",
            "Data book assembly after project completion delays final invoicing",
            "Traceability to individual filler metal lot rarely useful (batch testing sufficient)"
        ],
        resolution_strategy="Define documentation requirements in contract; use electronic document management to reduce paper handling",
        entity_scope="Documentation requirements apply to all code construction (ASME, API, AWS) and most client specifications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Documentation is code-mandated and essential for regulatory compliance and liability protection",
        controlling_precedent="ASME Code stamp cannot be applied without Authorized Inspector sign-off on documentation",
        issue_categories=[IssueCategory.DOCUMENTATION, IssueCategory.CODE_COMPLIANCE],
        zones=[AnalysisZone.PLANNING, AnalysisZone.EXECUTION, AnalysisZone.INSPECTION]
    ),
]

# ════════════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ════════════════════════════════════════════════════════════════════════════════

class MECH08Engine:
    """MECH08 Welding & Inspection Intelligence Engine"""

    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry_log: List[TelemetryData] = []
        self.query_count = 0

    def three_layer_response(
        self,
        question: str,
        mode: ResponseMode,
        context: Optional[Dict[str, Any]] = None
    ) -> WeldingResponse:
        """Three-layer response: Doctrine Cache -> Semantic Retrieval -> Deep Analysis"""

        start_time = datetime.now().timestamp()
        self.query_count += 1
        query_id = f"MECH08-{self.query_count}-{int(start_time)}"

        # Layer 1: Doctrine Cache (0-200ms)
        cache_result = self._search_doctrine_cache(question, context)

        if cache_result["hit"]:
            answer = self._format_cached_response(cache_result["doctrines"], question, mode)
            categories = self._extract_categories(cache_result["doctrines"])
            authorities = self._extract_authorities(cache_result["doctrines"])
            zones = self._extract_zones(cache_result["doctrines"])
            confidence = self._calculate_confidence(cache_result["doctrines"])

            telemetry = TelemetryData(
                query_id=query_id,
                start_time=start_time,
                end_time=datetime.now().timestamp(),
                cache_hit=True,
                doctrines_triggered=[d.topic for d in cache_result["doctrines"]],
                semantic_fallback=False,
                error_domain=None,
                confidence=confidence,
                response_mode=mode
            )
            self.telemetry_log.append(telemetry)

            return WeldingResponse(
                answer=answer,
                confidence=confidence,
                mode=mode,
                categories=categories,
                authorities_cited=authorities,
                telemetry=self._telemetry_to_dict(telemetry),
                determinism_hash=self._compute_hash(answer),
                timestamp=datetime.now().isoformat(),
                epistemic_disclosure=self._apply_epistemic_guardrails(answer),
                zones_analyzed=zones
            )

        # Layer 2: Semantic Retrieval (fallback - not implemented in this standalone version)
        # Layer 3: Deep Analysis (synthesize from multiple doctrines)
        answer = self._deep_analysis(question, mode, context)
        categories = [IssueCategory.WELDING_PROCESS]  # Default
        authorities = ["ASME Section IX", "AWS D1.1"]
        zones = [AnalysisZone.PLANNING]
        confidence = ConfidenceLevel.DISCLOSURE

        telemetry = TelemetryData(
            query_id=query_id,
            start_time=start_time,
            end_time=datetime.now().timestamp(),
            cache_hit=False,
            doctrines_triggered=[],
            semantic_fallback=True,
            error_domain=None,
            confidence=confidence,
            response_mode=mode
        )
        self.telemetry_log.append(telemetry)

        return WeldingResponse(
            answer=answer,
            confidence=confidence,
            mode=mode,
            categories=categories,
            authorities_cited=authorities,
            telemetry=self._telemetry_to_dict(telemetry),
            determinism_hash=self._compute_hash(answer),
            timestamp=datetime.now().isoformat(),
            epistemic_disclosure=self._apply_epistemic_guardrails(answer),
            zones_analyzed=zones
        )

    def _search_doctrine_cache(
        self,
        question: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Search doctrine cache for matching expertise blocks"""
        question_lower = question.lower()
        matched_doctrines = []

        for doctrine in self.doctrine_cache:
            # Keyword matching
            keyword_match = any(kw in question_lower for kw in doctrine.keywords)
            topic_match = any(word in question_lower for word in doctrine.topic.lower().split())

            if keyword_match or topic_match:
                matched_doctrines.append(doctrine)

        return {
            "hit": len(matched_doctrines) > 0,
            "doctrines": matched_doctrines[:5]  # Top 5 matches
        }

    def _format_cached_response(
        self,
        doctrines: List[DoctrineBlock],
        question: str,
        mode: ResponseMode
    ) -> str:
        """Format response from cached doctrine blocks"""
        if mode == ResponseMode.FAST:
            # Concise response
            primary = doctrines[0]
            conclusion = " ".join(primary.conclusion_template)
            return f"{conclusion}\n\nAuthority: {', '.join(primary.primary_authority[:2])}"

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with full reasoning
            sections = []
            for doctrine in doctrines[:2]:
                sections.append(f"## {doctrine.topic}\n")
                sections.append(f"**Conclusion:** {' '.join(doctrine.conclusion_template)}\n")
                sections.append(f"**Reasoning:** {doctrine.reasoning_framework[:500]}...\n")
                sections.append(f"**Key Factors:** {', '.join(doctrine.key_factors[:5])}\n")
                sections.append(f"**Authority:** {', '.join(doctrine.primary_authority)}\n")
            return "\n".join(sections)

        else:  # MEMO
            # Full documentation response
            sections = []
            for doctrine in doctrines:
                sections.append(f"# {doctrine.topic}\n")
                sections.append(f"**Conclusion:** {' '.join(doctrine.conclusion_template)}\n")
                sections.append(f"**Detailed Reasoning:**\n{doctrine.reasoning_framework}\n")
                sections.append(f"**Key Factors:**\n" + "\n".join(f"- {factor}" for factor in doctrine.key_factors))
                sections.append(f"\n**Primary Authority:**\n" + "\n".join(f"- {auth}" for auth in doctrine.primary_authority))
                sections.append(f"\n**Confidence:** {doctrine.confidence.value}")
                sections.append(f"**Controlling Precedent:** {doctrine.controlling_precedent}\n")
            return "\n\n".join(sections)

    def _deep_analysis(
        self,
        question: str,
        mode: ResponseMode,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Deep analysis when cache miss occurs"""
        return (
            f"Analysis of '{question}' requires synthesis of multiple welding and inspection principles. "
            f"For comprehensive guidance, consult ASME Section IX (welding procedure qualification), "
            f"AWS D1.1 (structural welding), API 1104 (pipeline welding), and ASME Section V (NDE methods). "
            f"Specific recommendations depend on material type, code of construction, service conditions, "
            f"and inspection requirements. This response is general guidance only and should be verified "
            f"against applicable codes and project specifications."
        )

    def _extract_categories(self, doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
        """Extract issue categories from doctrines"""
        categories = set()
        for doctrine in doctrines:
            categories.update(doctrine.issue_categories)
        return list(categories)

    def _extract_authorities(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract cited authorities from doctrines"""
        authorities = set()
        for doctrine in doctrines:
            authorities.update(doctrine.primary_authority)
        return list(authorities)

    def _extract_zones(self, doctrines: List[DoctrineBlock]) -> List[AnalysisZone]:
        """Extract analysis zones from doctrines"""
        zones = set()
        for doctrine in doctrines:
            zones.update(doctrine.zones)
        return list(zones)

    def _calculate_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Calculate confidence level from matched doctrines"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence from matched doctrines
        confidence_levels = [d.confidence for d in doctrines]
        if ConfidenceLevel.HIGH_RISK in confidence_levels:
            return ConfidenceLevel.HIGH_RISK
        elif ConfidenceLevel.DISCLOSURE in confidence_levels:
            return ConfidenceLevel.DISCLOSURE
        elif ConfidenceLevel.AGGRESSIVE in confidence_levels:
            return ConfidenceLevel.AGGRESSIVE
        else:
            return ConfidenceLevel.DEFENSIBLE

    def _apply_epistemic_guardrails(self, answer: str) -> Optional[str]:
        """Apply epistemic guardrails to prevent overconfident claims"""
        for phrase in BANNED_PHRASES:
            if phrase.lower() in answer.lower():
                return (
                    f"EPISTEMIC DISCLOSURE: This analysis is based on welding codes and industry standards "
                    f"but does not constitute engineering certification or code compliance guarantee. "
                    f"All welding procedures must be qualified per applicable codes, and all welders must "
                    f"be certified. Final inspection and acceptance is the responsibility of the Authorized "
                    f"Inspector or Certified Welding Inspector."
                )
        return None

    def _telemetry_to_dict(self, telemetry: TelemetryData) -> Dict[str, Any]:
        """Convert telemetry to dictionary"""
        return {
            "query_id": telemetry.query_id,
            "latency_ms": (telemetry.end_time - telemetry.start_time) * 1000,
            "cache_hit": telemetry.cache_hit,
            "doctrines_triggered": telemetry.doctrines_triggered,
            "semantic_fallback": telemetry.semantic_fallback,
            "confidence": telemetry.confidence.value,
            "response_mode": telemetry.response_mode.value
        }

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 determinism hash"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

# ════════════════════════════════════════════════════════════════════════════════
# FASTAPI ENDPOINTS
# ════════════════════════════════════════════════════════════════════════════════

engine = MECH08Engine()

@APP.post("/query", response_model=WeldingResponse)
async def query_welding_engine(query: WeldingQuery):
    """Main query endpoint for welding and inspection intelligence"""
    try:
        logger.info(f"Query received: {query.question[:100]}... | Mode: {query.mode}")
        response = engine.three_layer_response(
            question=query.question,
            mode=query.mode,
            context=query.context
        )
        logger.info(f"Query completed | Confidence: {response.confidence} | Hash: {response.determinism_hash}")
        return response
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "operational",
        "engine": "MECH08 Welding & Inspection",
        "version": "1.0.0",
        "port": 9048,
        "doctrine_blocks": len(engine.doctrine_cache),
        "total_queries": engine.query_count,
        "telemetry_entries": len(engine.telemetry_log)
    }

@APP.get("/doctrines")
async def list_doctrines():
    """List all doctrine block topics"""
    return {
        "total_doctrines": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords[:5],
                "categories": [cat.value for cat in d.issue_categories],
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }

@APP.get("/telemetry")
async def get_telemetry():
    """Retrieve telemetry data"""
    return {
        "total_queries": engine.query_count,
        "recent_telemetry": [
            engine._telemetry_to_dict(t)
            for t in engine.telemetry_log[-20:]
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting MECH08 Welding & Inspection Engine on port 9048")
    uvicorn.run(APP, host="0.0.0.0", port=9048)
