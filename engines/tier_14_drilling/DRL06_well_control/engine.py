"""
DRL06 - Well Control & Kick Management Intelligence Engine
TIE Gold Standard - Real Domain Expertise

Port: 9016
Domain: Well control procedures, kick detection, shut-in operations, kill methods,
        BOP operations, gas behavior, barrier philosophy, emergency response

Authority: API RP 53, API RP 59, IADC WellCAP, IWCF guidelines, NORSOK D-010
"""

import asyncio
import hashlib
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# CRITICAL: Add parent dir to sys.path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "DRL06"
ENGINE_NAME = "Well Control & Kick Management"
VERSION = "1.0.0"
PORT = 9016

# ============================================================================
# ENUMS
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
    KICK_DETECTION = "KICK_DETECTION"
    SHUT_IN_PROCEDURES = "SHUT_IN_PROCEDURES"
    KILL_METHODS = "KILL_METHODS"
    KILL_CALCULATIONS = "KILL_CALCULATIONS"
    GAS_BEHAVIOR = "GAS_BEHAVIOR"
    BOP_OPERATIONS = "BOP_OPERATIONS"
    ACCUMULATOR_SYSTEMS = "ACCUMULATOR_SYSTEMS"
    SPECIAL_SITUATIONS = "SPECIAL_SITUATIONS"
    BARRIER_PHILOSOPHY = "BARRIER_PHILOSOPHY"
    EMERGENCY_RESPONSE = "EMERGENCY_RESPONSE"
    TRAINING_CERTIFICATION = "TRAINING_CERTIFICATION"
    OFFSHORE_OPERATIONS = "OFFSHORE_OPERATIONS"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None
    well_depth: Optional[float] = None
    mud_weight: Optional[float] = None
    formation_pressure: Optional[float] = None

class DoctrineMatch(BaseModel):
    topic: str
    confidence: float
    reasoning: str
    authorities: List[str]

class EngineResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrine_matches: List[DoctrineMatch]
    reasoning_chain: List[str]
    authorities: List[str]
    warnings: List[str]
    determinism_hash: str
    response_time_ms: float
    mode: ResponseMode

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    doctrine_count: int
    uptime_seconds: float

# ============================================================================
# DOCTRINE BLOCKS
# ============================================================================

class DoctrineBlock:
    """Real well control expertise encoded as doctrine"""

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
        counter_arguments: Optional[List[str]] = None,
        calculation_method: Optional[str] = None,
        safety_critical: bool = False
    ):
        self.topic = topic
        self.keywords = [k.lower() for k in keywords]
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.category = category
        self.counter_arguments = counter_arguments or []
        self.calculation_method = calculation_method
        self.safety_critical = safety_critical

# ============================================================================
# DOCTRINE CACHE - 25+ REAL WELL CONTROL DOCTRINE BLOCKS
# ============================================================================

DOCTRINE_CACHE = [
    DoctrineBlock(
        topic="Kick Detection - Pit Gain Method",
        keywords=["kick detection", "pit gain", "flow increase", "trip tank", "early warning"],
        conclusion_template="Primary kick detection relies on continuous pit level monitoring with a gain threshold indicating formation fluid influx requiring immediate shut-in procedures per API RP 59.",
        reasoning_framework="Pit gain is the most reliable kick indicator. Trip tank increases of 1-2 bbl warrant investigation. Active pit gains of 5-10 bbl require shut-in preparation. Gains of 10+ bbl demand immediate well shut-in. Any gain with pumps off confirms a kick. Correlation with flow meters and other indicators is essential.",
        key_factors=[
            "Continuous pit monitoring via PVT system",
            "Trip tank sensitivity (1-2 bbl warning level)",
            "Active pit gain threshold (5-10 bbl action level)",
            "Correlation with flow meter readings",
            "Flow check confirmation if uncertain"
        ],
        primary_authority=[
            "API RP 59 - Well Control Operations",
            "IADC WellCAP - Drilling Well Control",
            "NORSOK D-010 Well Integrity Standard"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KICK_DETECTION,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Flow Check Procedure",
        keywords=["flow check", "pumps off", "confirm kick", "static conditions"],
        conclusion_template="A proper flow check requires stopping all pumps, observing for 5-10 minutes, confirming whether flow continues, with any positive flow indicating a kick requiring immediate shut-in.",
        reasoning_framework="Flow check is the definitive test. Stop pumps and rotary, observe flow for 5-10 minutes minimum. Longer for gas kicks. If flow continues or pits gain, shut in immediately. If no flow and stable pits, resume drilling. Clear rig floor and have BOP ready during procedure.",
        key_factors=[
            "Stop all pumps and observe 5-10 minutes",
            "Monitor flow line and pit levels simultaneously",
            "Any positive flow confirms kick",
            "Longer observation for gas kicks",
            "BOP stack ready before flow check",
            "When in doubt, shut in"
        ],
        primary_authority=[
            "API RP 59 Section 6.3 - Flow Checks",
            "IADC WellCAP Lesson 3 - Kick Detection",
            "IWCF Well Control Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KICK_DETECTION,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Hard Shut-In vs Soft Shut-In",
        keywords=["hard shut in", "soft shut in", "choke first", "rams first", "formation strength"],
        conclusion_template="Hard shut-in (close BOP first, then choke) is the industry standard providing fastest kick control, unless weak formations require soft shut-in (choke first) to limit surface pressure spikes.",
        reasoning_framework="Hard shut-in: Close annular/rams, open HCR valve, close choke, record pressures. Fastest method, minimizes influx. Soft shut-in: Close choke, close BOP, slowly open choke to read pressures. Used only for known weak formations. API RP 59 recommends hard shut-in as standard.",
        key_factors=[
            "Hard shut-in closes BOP first (fastest)",
            "Soft shut-in closes choke first (lower spike)",
            "Hard shut-in is API RP 59 standard",
            "Soft shut-in only for weak formations",
            "Speed critical for gas kicks",
            "Pre-drill planning specifies method"
        ],
        primary_authority=[
            "API RP 59 Section 7.2 - Shut-in Procedures",
            "IADC WellCAP - Hard vs Soft Shut-in",
            "SPE 179191 - Shut-in Method Comparison"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SHUT_IN_PROCEDURES,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="SIDPP and SICP Interpretation",
        keywords=["sidpp", "sicp", "shut in drill pipe pressure", "shut in casing pressure"],
        conclusion_template="SIDPP represents formation pressure minus hydrostatic pressure, while SICP indicates kick fluid type and volume, with SICP greater than SIDPP confirming gas influx.",
        reasoning_framework="SIDPP read at standpipe gauge, stabilizes quickly, equals formation pressure minus mud hydrostatic. SICP read at casing gauge, may rise over time from gas migration. Large SICP-SIDPP difference indicates gas kick. Equal pressures suggest saltwater kick. Rising SICP requires pressure bleed-off to maintain constant BHP.",
        key_factors=[
            "SIDPP = formation pressure minus mud hydrostatic",
            "SICP reflects kick fluid density",
            "SICP > SIDPP indicates gas kick",
            "SICP - SIDPP quantifies kick fluid weight",
            "Rising SICP over time indicates gas migration",
            "Record pressures every 5-15 minutes",
            "Both pressures needed for kill sheet"
        ],
        primary_authority=[
            "API RP 59 Section 7.3 - Pressure Interpretation",
            "IADC WellCAP Lesson 5 - Kill Sheet Calculations",
            "Grace Well Control Manual Chapter 4"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_CALCULATIONS
    ),

    DoctrineBlock(
        topic="Driller's Method - Two Circulation Kill",
        keywords=["drillers method", "two circulation", "first circulation", "second circulation"],
        conclusion_template="The Driller's Method uses two circulations: first to remove kick with original mud weight, second to kill well with weighted mud, providing simplicity and time to prepare kill mud.",
        reasoning_framework="First circulation: ICP equals SIDPP plus SCR, maintain constant drill pipe pressure, circulate kick out. Second circulation: start at SIDPP, reduce linearly to FCP as kill mud enters pipe, maintain FCP from bit to surface. Advantages: simple, time to prepare kill mud, clear indication kick is removed. Industry standard method.",
        key_factors=[
            "First circulation removes kick at original mud weight",
            "ICP = SIDPP + SCR maintains constant BHP",
            "Second circulation displaces to kill mud weight",
            "FCP = SCR times (OMW divided by KMW)",
            "Provides time to prepare kill mud",
            "Simplest method, lowest error risk",
            "Industry standard for most situations"
        ],
        primary_authority=[
            "API RP 59 Section 8.2 - Driller's Method",
            "IADC WellCAP Lesson 6 - Kill Methods",
            "IWCF Surface BOP Operations Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_METHODS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Wait and Weight Method",
        keywords=["wait and weight", "concurrent method", "single circulation", "kill mud ready"],
        conclusion_template="The Wait and Weight method circulates kill-weight mud in one circulation, reducing formation exposure time and casing pressure cycles, but requires kill mud ready before starting.",
        reasoning_framework="Prerequisites: kill mud mixed and ready. Calculate ICP and FCP. Start pump at ICP, begin pumping kill mud, reduce drill pipe pressure linearly from ICP to FCP over drill pipe volume. Maintain FCP from bit to surface. Faster than Driller's Method, lower formation pressure exposure, but requires skilled choke operator.",
        key_factors=[
            "Single circulation with kill-weight mud",
            "Kill mud must be ready before starting",
            "Linear pressure reduction from ICP to FCP",
            "Faster than Driller's Method",
            "Lower formation pressure exposure",
            "Requires skilled choke operator",
            "Preferred for weak formations"
        ],
        primary_authority=[
            "API RP 59 Section 8.3 - Wait and Weight Method",
            "IADC WellCAP Lesson 6 - Kill Methods",
            "SPE 13047 - Kill Method Comparison"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_METHODS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Kill Mud Weight Calculation",
        keywords=["kill mud weight", "kmw", "safety factor", "trip margin"],
        conclusion_template="Kill mud weight equals formation pressure gradient plus safety factor (typically 0.5 to 1.0 ppg), ensuring sufficient overbalance without exceeding fracture gradient.",
        reasoning_framework="KMW equals (Formation Pressure divided by 0.052 divided by TVD) plus Safety Factor. Formation pressure from SIDPP plus current mud hydrostatic. Typical safety factor 0.5 ppg for normal operations, 0.75 ppg for high-pressure wells, 1.0 ppg for H2S or critical wells. Must not exceed fracture gradient, casing burst, or pump ratings.",
        key_factors=[
            "KMW = (Formation Pressure / 0.052 / TVD) + Safety Factor",
            "Typical safety factor 0.5 to 1.0 ppg",
            "Must not exceed fracture gradient",
            "Formation pressure from SIDPP plus hydrostatic",
            "Verify against casing and pump ratings",
            "Round to practical mixing increment",
            "Check barite inventory before committing"
        ],
        primary_authority=[
            "API RP 59 Section 8.1 - Kill Mud Weight",
            "IADC WellCAP Lesson 5 - Kill Sheet Calculations",
            "SPE Drilling Engineering Textbook Chapter 6"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_CALCULATIONS
    ),

    DoctrineBlock(
        topic="Initial and Final Circulating Pressure",
        keywords=["icp", "fcp", "circulating pressure", "slow circulating rate", "scr"],
        conclusion_template="Initial Circulating Pressure (ICP = SIDPP + SCR) maintains formation pressure during kill, while Final Circulating Pressure (FCP = SCR times OMW divided by KMW) confirms kill mud at bit.",
        reasoning_framework="SCR measured daily at slow pump rate (20-40 SPM). ICP equals SIDPP plus SCR provides pressure to circulate while balanced. FCP equals SCR times density ratio accounts for kill mud heavier than original. ICP held constant in Driller's Method first circulation. Linear reduction ICP to FCP in Wait and Weight. Final pressure should match FCP when killed.",
        key_factors=[
            "ICP = SIDPP + SCR maintains constant BHP",
            "FCP = SCR times (OMW / KMW) confirms kill mud at bit",
            "SCR measured daily at slow pump rate",
            "Lower SCR means gentler well control",
            "ICP held constant in Driller's first circulation",
            "Linear reduction ICP to FCP in Wait and Weight",
            "Final pressure should match FCP when killed"
        ],
        primary_authority=[
            "API RP 59 Section 8.1.3 - Kill Pressures",
            "IADC WellCAP Kill Sheet Calculations",
            "IWCF Pressure Control Manual Section 7"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_CALCULATIONS
    ),

    DoctrineBlock(
        topic="Gas Behavior - Boyle's Law and Migration",
        keywords=["boyles law", "gas expansion", "gas migration", "volume increase"],
        conclusion_template="Gas kick volume expands inversely with pressure per Boyle's Law, causing rapid SICP increase as gas rises, requiring continuous pressure bleed-off to prevent uncontrolled expansion.",
        reasoning_framework="Boyle's Law: P1 times V1 equals P2 times V2. Gas expands 2-5 times from TD to surface. Migration causes SICP to rise continuously. Must bleed pressure to prevent casing damage. SIDPP should stay constant if BHP maintained. Volumetric method for severe migration. Gas lubrication can cause drill string to fall.",
        key_factors=[
            "Boyle's Law: P1V1 = P2V2 (volume increases as pressure drops)",
            "Gas expands 2-5 times from TD to surface",
            "Migration causes SICP to rise continuously",
            "Must bleed pressure to prevent casing damage",
            "SIDPP should stay constant if BHP maintained",
            "Volumetric method for severe migration",
            "Gas lubrication can cause drill string to fall"
        ],
        primary_authority=[
            "API RP 59 Section 9 - Gas Kick Behavior",
            "IADC WellCAP Lesson 7 - Gas Migration",
            "SPE 36582 - Gas Kick Migration Modeling"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.GAS_BEHAVIOR,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="BOP Stack Components and Function",
        keywords=["bop", "blowout preventer", "annular", "pipe rams", "blind rams", "shear rams"],
        conclusion_template="BOP stack includes annular preventer, pipe rams, blind/shear rams, and choke/kill lines, each serving specific functions per API Spec 16A with rated working pressures.",
        reasoning_framework="Annular closes on any diameter, fastest, lower pressure rating (2000-5000 psi). Pipe rams for specific OD, higher pressure (5000-15000 psi), used for kill operations. Blind rams for open hole only. Shear rams cut pipe in emergency. Test every 14 days per API RP 53. Close annular first, transfer to rams for kill.",
        key_factors=[
            "Annular closes on any size, fastest, lower pressure rating",
            "Pipe rams for specific OD, higher pressure, kill operations",
            "Blind rams for open hole only",
            "Shear rams cut pipe in emergency",
            "Choke/kill lines for circulation",
            "Test every 14 days per API RP 53",
            "Close annular first, transfer to rams for kill"
        ],
        primary_authority=[
            "API Spec 16A - BOP Equipment Specification",
            "API RP 53 - BOP Testing and Maintenance",
            "IADC WellCAP Lesson 2 - BOP Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BOP_OPERATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Accumulator System Requirements",
        keywords=["accumulator", "closing unit", "volume requirement", "precharge", "nitrogen"],
        conclusion_template="API RP 53 requires accumulator capacity sufficient to close all BOP components with pressure remaining above 1200 psi (deepwater 1500 psi), typically 1.5 times required volume.",
        reasoning_framework="Minimum volume for full annular closure, one pipe ram closure, HCR valve opening, plus 50 percent margin. Final pressure must exceed 1200 psi (land) or 1500 psi (deepwater). Nitrogen precharge at 60-80 percent of minimum operating pressure. Operating pressure typically 3000 psi. Daily pressure checks required.",
        key_factors=[
            "Capacity for all closures plus 50 percent margin",
            "Minimum 1200 psi remaining (land), 1500 psi (deepwater)",
            "Nitrogen precharge 60-80 percent of min operating pressure",
            "Typical operating pressure 3000 psi",
            "Daily pressure checks required",
            "Multiple bottles for redundancy",
            "Ideal gas law accounts for pressure drop"
        ],
        primary_authority=[
            "API RP 53 Section 5 - Accumulator Requirements",
            "API RP 16Q - BOP Control Systems",
            "IADC WellCAP Lesson 2 - Accumulator Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ACCUMULATOR_SYSTEMS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Underground Blowout",
        keywords=["underground blowout", "crossflow", "lost circulation", "formation fracture"],
        conclusion_template="Underground blowout occurs when formation fluid flows into weaker formation downhole rather than to surface, indicated by total lost returns with stable/rising SIDPP, requiring cementing or relief well.",
        reasoning_framework="Formation fractures during kill attempt, kick fluid flows into fractured formation instead of surface. Total lost returns with stable or rising SIDPP distinguishes from simple lost circulation. Stop circulation immediately. Treatment: LCM pills, cement plugs, or relief well as last resort. Cannot kill with conventional methods. Prevention: know fracture gradient and kick tolerance.",
        key_factors=[
            "Flow between formations, not to surface",
            "Total lost returns with stable/rising SIDPP",
            "Caused by fracturing weak formation during kill",
            "Cementing is most common solution",
            "Cannot kill with conventional methods",
            "May require relief well if severe",
            "Prevention: know fracture gradient and kick tolerance"
        ],
        primary_authority=[
            "API RP 59 Section 11 - Special Situations",
            "IADC WellCAP Lesson 9 - Underground Blowout",
            "SPE 170368 - Underground Blowout Case Studies"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.SPECIAL_SITUATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Volumetric Method for Gas Kicks",
        keywords=["volumetric method", "gas migration", "kick tolerance", "limited circulation"],
        conclusion_template="Volumetric method controls gas kicks by bleeding calculated volumes at depth intervals to maintain constant bottomhole pressure while allowing gas to migrate upward, used when circulation would exceed formation limits.",
        reasoning_framework="Required when kick volume exceeds kick tolerance or circulating would fracture formation. Allow gas to migrate upward, calculate volume increase per Boyle's Law, bleed exact volume to maintain constant BHP. Repeat until gas reaches surface. Do not circulate with pumps. MAASP determines maximum pressure without fracture. Slow process, may take days, requires continuous monitoring.",
        key_factors=[
            "Used when circulation would fracture formation",
            "Allow gas to migrate, bleed calculated volumes",
            "Maintain BHP constant without pumps",
            "Calculate volume increase per Boyle's Law",
            "MAASP equals max pressure without fracture",
            "Slow process, may take days",
            "Requires continuous monitoring"
        ],
        primary_authority=[
            "API RP 59 Section 10 - Volumetric Method",
            "IADC WellCAP Lesson 8 - Special Kill Methods",
            "SPE 36582 - Volumetric Method Field Applications"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.SPECIAL_SITUATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Well Control During Tripping",
        keywords=["trip margin", "trip tank", "fill up volume", "swab", "surge"],
        conclusion_template="Tripping operations require continuous hole fill monitoring, trip margin on mud weight, controlled tripping speeds to prevent swab/surge, and immediate shut-in if trip tank shows gain.",
        reasoning_framework="Trip margin 0.2 to 0.5 ppg above balance. Monitor trip tank for every stand. Fill volume should match pipe displacement. Trip tank gain indicates potential kick, shut in immediately. Control tripping speed to prevent swab/surge. Typical speed 60-90 ft/min pulling, 90-120 running. Stripping with BOP closed is last resort.",
        key_factors=[
            "Use trip margin (0.2-0.5 ppg) above balance",
            "Monitor trip tank for every stand",
            "Fill volume should match pipe displacement",
            "Trip tank gain equals potential kick, shut in immediately",
            "Control tripping speed to prevent swab/surge",
            "Typical speed 60-90 ft/min pulling, 90-120 running",
            "Stripping with BOP closed is last resort"
        ],
        primary_authority=[
            "API RP 59 Section 12 - Well Control During Tripping",
            "IADC WellCAP Lesson 10 - Trip Procedures",
            "IADC Drilling Manual Chapter 7 - Tripping Operations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.SPECIAL_SITUATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Floating Rig Well Control",
        keywords=["floating rig", "riser", "riser disconnect", "subsea bop", "heave"],
        conclusion_template="Floating rig well control requires managing riser gas handling, potential emergency disconnect, subsea BOP operations, and vessel motion effects, with modified shut-in to prevent riser over-pressure.",
        reasoning_framework="Riser filled with 8.6 ppg seawater. Gas in riser expands rapidly, over-pressure risk. Modified shut-in: close subsea BOP, vent riser first. Emergency disconnect if drive-off or severe weather. Subsea BOP has slower response time. Heave and dynamic positioning affect operations. Shallow gas can bypass BOP subsea.",
        key_factors=[
            "Riser filled with 8.6 ppg seawater, not mud",
            "Gas in riser expands rapidly, over-pressure risk",
            "Modified shut-in: close subsea BOP, vent riser first",
            "Emergency disconnect if drive-off or severe weather",
            "Subsea BOP has slower response time",
            "Heave and DP motion affect operations",
            "Shallow gas can bypass BOP subsea"
        ],
        primary_authority=[
            "API RP 59 Appendix B - Floating Operations",
            "IADC WellCAP Deepwater Module",
            "NORSOK D-010 Well Control for Floating Units"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.OFFSHORE_OPERATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="H2S Well Control Considerations",
        keywords=["h2s", "sour gas", "hydrogen sulfide", "scavenger", "evacuation"],
        conclusion_template="H2S well control requires continuous gas detection, specialized PPE, higher kill mud safety factors (1.0+ ppg), scavenger chemicals, and emergency evacuation plans per API RP 49.",
        reasoning_framework="H2S is highly toxic (500 ppm fatal). Continuous gas detection required. SCBA and training for all personnel. Higher kill mud safety factor (1.0+ ppg). H2S scavengers in mud system. Remote choke operation downwind. Evacuation plan and regular drills mandatory.",
        key_factors=[
            "H2S is highly toxic (500 ppm fatal)",
            "Continuous gas detection required",
            "SCBA and training for all personnel",
            "Higher kill mud safety factor (1.0+ ppg)",
            "H2S scavengers in mud system",
            "Remote choke operation downwind",
            "Evacuation plan and regular drills mandatory"
        ],
        primary_authority=[
            "API RP 49 - Safe Drilling of Wells Containing H2S",
            "IADC HSE Reference Guide - H2S",
            "OSHA 29 CFR 1910.1000 - Hydrogen Sulfide"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.EMERGENCY_RESPONSE,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Barrier Philosophy and Well Integrity",
        keywords=["barrier", "primary barrier", "secondary barrier", "well integrity", "two barrier"],
        conclusion_template="Well integrity requires maintaining two independent barriers to flow at all times per NORSOK D-010 and API RP 96, with primary barrier (mud column) and secondary barrier (casing plus BOP or cement).",
        reasoning_framework="Two independent barriers required at all times. Primary barrier: mud column during drilling. Secondary barrier: BOP plus casing plus cement. Each barrier must be tested and verified. Loss of one barrier requires immediate action. Cannot operate with single barrier. NORSOK D-010 and API RP 96 define requirements.",
        key_factors=[
            "Two independent barriers required at all times",
            "Primary barrier: mud column during drilling",
            "Secondary barrier: BOP plus casing plus cement",
            "Each barrier must be tested and verified",
            "Loss of one barrier requires immediate action",
            "Cannot operate with single barrier",
            "NORSOK D-010 and API RP 96 define requirements"
        ],
        primary_authority=[
            "NORSOK D-010 Well Integrity Standard",
            "API RP 96 Deepwater Well Control",
            "ISO 16530 Well Integrity Parts 1-2"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.BARRIER_PHILOSOPHY
    ),

    DoctrineBlock(
        topic="WellCAP and IWCF Certification",
        keywords=["wellcap", "iwcf", "iadc", "certification", "training", "driller certification"],
        conclusion_template="Industry requires well control certification through IADC WellCAP or IWCF programs, with supervisory personnel requiring Level 4 certification renewed every 2 years.",
        reasoning_framework="IADC WellCAP or IWCF certification required. Level 4 for supervisory personnel (drillers, tool pushers). Valid for 2 years, must renew. Written exam plus practical simulator plus calculations. 3-5 days training plus exam. Regulatory requirement in many jurisdictions. Rig drills required in addition to certification.",
        key_factors=[
            "IADC WellCAP or IWCF certification required",
            "Level 4 for supervisory personnel (drillers, tool pushers)",
            "Valid for 2 years, must renew",
            "Written exam plus practical simulator plus calculations",
            "3-5 days training plus exam",
            "Regulatory requirement in many jurisdictions",
            "Rig drills required in addition to certification"
        ],
        primary_authority=[
            "IADC WellCAP Program Standards",
            "IWCF Scheme Document",
            "BSEE 30 CFR 250 Subpart O (US Offshore)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.TRAINING_CERTIFICATION
    ),

    DoctrineBlock(
        topic="MAASP - Maximum Allowable Annular Surface Pressure",
        keywords=["maasp", "maximum allowable", "fracture pressure", "casing shoe", "kick tolerance"],
        conclusion_template="MAASP is the maximum surface pressure that can be applied to annulus without fracturing weakest formation, calculated as fracture pressure minus mud hydrostatic, limiting kick size and kill method selection.",
        reasoning_framework="MAASP equals (Frac Gradient minus Mud Gradient) times 0.052 times Shoe TVD. Limits kick tolerance and kill methods. Determined by LOT or FIT at casing shoe. Low MAASP requires volumetric method. Must be posted and monitored continuously. Drives casing setting depth decisions.",
        key_factors=[
            "MAASP equals max surface pressure without fracture",
            "Formula: (Frac Grad - Mud Grad) times 0.052 times Shoe TVD",
            "Limits kick tolerance and kill methods",
            "Determined by LOT or FIT at casing shoe",
            "Low MAASP requires volumetric method",
            "Must be posted and monitored continuously",
            "Drives casing setting depth decisions"
        ],
        primary_authority=[
            "API RP 59 Section 6.5 - MAASP",
            "IADC WellCAP Lesson 5 - Kick Tolerance",
            "SPE Textbook - Casing Design and MAASP"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_CALCULATIONS
    ),

    DoctrineBlock(
        topic="Relief Well Planning",
        keywords=["relief well", "directional drilling", "ranging", "magnetic ranging", "intersection"],
        conclusion_template="Relief wells are drilled to intersect and kill blowout wells, requiring precise directional drilling, electromagnetic ranging for final approach, typically costing 20-100 million dollars and taking 3-6 months.",
        reasoning_framework="Last resort for uncontrolled blowouts. Requires 3-6 months to drill and intersect. Cost 20-100M or more. Electromagnetic ranging for final approach. Intersection accuracy critical (within feet). Kill with heavy mud or cement. Success rate high but very expensive.",
        key_factors=[
            "Last resort for uncontrolled blowouts",
            "Requires 3-6 months to drill and intersect",
            "Cost 20-100M or more",
            "Electromagnetic ranging for final approach",
            "Intersection accuracy critical (within feet)",
            "Kill with heavy mud or cement",
            "Success rate high but very expensive"
        ],
        primary_authority=[
            "API RP 59 Section 14 - Relief Wells",
            "SPE 121781 - Relief Well Planning and Execution",
            "Macondo Investigation Report - Relief Well Operations"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.EMERGENCY_RESPONSE,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Shallow Gas Hazards",
        keywords=["shallow gas", "biogenic gas", "conductor casing", "diverter", "surface flow"],
        conclusion_template="Shallow gas (above 1000-1500 ft) presents extreme hazard due to low confining pressure, inability to use BOP, and potential for rapid broaching to surface, requiring diverter system and specialized procedures.",
        reasoning_framework="Shallow gas above surface casing depth (less than 1500 ft). Cannot use BOP, only diverter available. Low confining pressure, easy to fracture. DO NOT shut in - will cause broaching. Divert flow overboard/away from rig. May need to lighten mud weight. Pre-drill planning critical.",
        key_factors=[
            "Shallow gas above surface casing depth (less than 1500 ft)",
            "Cannot use BOP, only diverter available",
            "Low confining pressure, easy to fracture",
            "DO NOT shut in - will cause broaching",
            "Divert flow overboard/away from rig",
            "May need to lighten mud weight",
            "Pre-drill planning critical"
        ],
        primary_authority=[
            "API RP 96 Section 7 - Shallow Hazards",
            "IADC Deepwater Well Control Guidelines",
            "NORSOK D-010 Appendix G - Shallow Gas"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.SPECIAL_SITUATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Choke Management During Kill",
        keywords=["choke", "choke operator", "adjustable choke", "maintain pressure", "pressure control"],
        conclusion_template="Choke operator maintains constant drill pipe pressure during kill operations by adjusting choke opening to compensate for changing annular density, requiring continuous monitoring and skilled operation.",
        reasoning_framework="Choke operator critical role during well control. Maintain ICP on drill pipe during first circulation. Reduce from ICP to FCP during second circulation or Wait and Weight. Choke adjustments every few seconds. Open choke as gas expands. Close choke as kill mud enters annulus. Remote operation for H2S wells. Manual backup for hydraulic failure.",
        key_factors=[
            "Maintain constant drill pipe pressure via choke adjustments",
            "Open choke as gas expands and rises",
            "Close choke as kill mud weight increases annular density",
            "Continuous monitoring of pressure gauges",
            "Smooth adjustments to prevent pressure spikes",
            "Remote operation for H2S or high-risk wells",
            "Manual backup choke required"
        ],
        primary_authority=[
            "API RP 59 Section 8.4 - Choke Operations",
            "IADC WellCAP Lesson 6 - Kill Procedures",
            "IWCF Choke Operator Training"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_METHODS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Well Control During Connections",
        keywords=["connection", "kelly down", "make connection", "flow check", "pressure check"],
        conclusion_template="Well control during connections requires flow checking and pressure monitoring after each connection, with annular or pipe rams closed if kick is suspected, per API RP 59 connection procedures.",
        reasoning_framework="Stop pumps for connection. Observe for flow. If no flow, make connection normally. If flow observed, shut in well before breaking connection. If uncertain, close annular and make connection with BOP closed (slow, wears BOP). Record SIDPP and SICP after each connection during kill operations to verify constant BHP. Connection gas (recycled gas from previous circulation) may cause brief flow - distinguish from new kick.",
        key_factors=[
            "Flow check before breaking connection if kick suspected",
            "Shut in well if flow observed during connection",
            "Monitor SIDPP and SICP during kill connections",
            "Connection gas may cause brief flow (not new kick)",
            "Can make connection with annular closed if necessary",
            "Verify constant BHP between connections",
            "Do not circulate bottoms up through connections during kill"
        ],
        primary_authority=[
            "API RP 59 Section 8.5 - Connections During Kill",
            "IADC WellCAP Connection Procedures",
            "IWCF Well Control Manual Section 8"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.KILL_METHODS
    ),

    DoctrineBlock(
        topic="Bullheading Kill Method",
        keywords=["bullheading", "dynamic kill", "reverse circulation", "force kill", "pump down annulus"],
        conclusion_template="Bullheading pumps kill mud down the annulus at high rate to force formation fluids back into reservoir, used when conventional circulation is impossible, requiring high pump pressures and careful monitoring for fracture.",
        reasoning_framework="Bullheading used when: pipe stuck, bit plugged, cannot circulate normally, surface blowout. Pump kill mud down annulus (choke line or annulus). Force fluids back into formation. High pump pressure required (may exceed formation pressure). Risk of fracturing formation. Monitor for underground blowout. May require cement to seal formation. Last resort before relief well.",
        key_factors=[
            "Used when conventional circulation impossible",
            "Pump kill mud down annulus at high rate",
            "Force formation fluids back into reservoir",
            "High pump pressure required",
            "Risk of fracturing formation",
            "Monitor for underground blowout or losses",
            "May require cement to seal formation"
        ],
        primary_authority=[
            "API RP 59 Section 11.3 - Bullheading",
            "IADC WellCAP Lesson 9 - Special Kill Methods",
            "SPE 120379 - Dynamic Kill Analysis"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.KILL_METHODS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Snubbing and Stripping Operations",
        keywords=["snubbing", "stripping", "running in hole shut in", "hydraulic workover", "force pipe"],
        conclusion_template="Snubbing forces pipe into pressurized well against wellbore pressure using hydraulic rams, while stripping pulls pipe through closed annular preventer, both used during well control when pipe movement is required with well shut in.",
        reasoning_framework="Stripping: pull pipe through closed annular BOP. Bleed volume equal to pipe displacement. Monitor pressures continuously. Slow process, wears annular element. Used to pull out during well control. Snubbing: force pipe into well against pressure. Requires snubbing unit (hydraulic). Used to run pipe or tools into flowing well. Both operations high-risk, require specialized equipment and trained crews.",
        key_factors=[
            "Stripping pulls pipe through closed annular",
            "Bleed pipe displacement volume during stripping",
            "Snubbing forces pipe into pressurized well",
            "Requires specialized equipment (snubbing unit)",
            "Both operations high-risk",
            "Trained crew required",
            "Monitor pressures continuously"
        ],
        primary_authority=[
            "API RP 59 Section 12.4 - Stripping Operations",
            "IADC WellCAP Snubbing Procedures",
            "Snubbing Units Manufacturers Association (SUMA) Guidelines"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.SPECIAL_SITUATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Kick During Casing Operations",
        keywords=["kick while running casing", "casing shut in", "float collar", "casing head", "stage collar"],
        conclusion_template="Kick during casing running requires immediate shut-in at casing head if float equipment is functional, or at BOP if float has failed, followed by kill operations or cement squeeze per API RP 59.",
        reasoning_framework="If float collar holds: shut in at casing head, pressure test float, bullhead kill mud down annulus, displace casing to kill mud if needed. If float leaks: shut in on casing with BOP, higher risk of casing collapse, may need to pull casing. If casing landed but not cemented: squeeze cement through stage collar or perforations. Prevention: test float before running, maintain overbalance, run casing quickly.",
        key_factors=[
            "Shut in at casing head if float holds",
            "Shut in at BOP if float leaks",
            "Test float equipment before running casing",
            "Bullhead kill mud down annulus outside casing",
            "May need cement squeeze if casing landed",
            "Risk of casing collapse if high pressure",
            "Run casing quickly to minimize time at balance"
        ],
        primary_authority=[
            "API RP 59 Section 13 - Casing Operations",
            "IADC WellCAP Casing Well Control",
            "API RP 10B-2 Casing Cementing Practices"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.SPECIAL_SITUATIONS,
        safety_critical=True
    ),

    DoctrineBlock(
        topic="Bit Nozzle Plugging During Kill",
        keywords=["plugged bit", "nozzle plugged", "barite sag", "LCM", "pressure increase"],
        conclusion_template="Bit nozzle plugging during kill operations causes sudden pump pressure increase with constant flow rate, requiring immediate response to prevent losing circulation or formation fracture, typically cleared by working pipe or pumping sweep.",
        reasoning_framework="Symptoms: pump pressure increases, flow rate constant, SIDPP unchanged. Causes: barite sag in heavy kill mud, LCM bridging nozzles, cuttings. Response: do NOT increase pump rate (will fracture formation). Work pipe up and down to clear. Pump low-solids sweep. Reduce pump rate if necessary. If cannot clear: may need to pull bit, use bullheading, or spot acid. Prevention: condition kill mud, limit LCM concentration, avoid long static periods.",
        key_factors=[
            "Symptom: pump pressure increases with constant flow rate",
            "Do NOT increase pump rate (fracture risk)",
            "Work pipe up and down to clear nozzles",
            "Pump low-solids sweep to dislodge plug",
            "Reduce pump rate if pressure excessive",
            "May need to pull bit if cannot clear",
            "Prevention: condition kill mud, limit LCM, avoid stagnation"
        ],
        primary_authority=[
            "API RP 59 Section 8.7 - Plugged Bit",
            "IADC WellCAP Troubleshooting Kill Operations",
            "SPE 24577 - Bit Plugging During Well Control"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.KILL_METHODS
    ),

    DoctrineBlock(
        topic="Simultaneous Operations (SIMOPS) Well Control",
        keywords=["simops", "simultaneous operations", "adjacent well", "multi-well platform", "interference"],
        conclusion_template="Simultaneous operations on adjacent wells require formal risk assessment and barrier verification for each well, ensuring one well's operations cannot compromise another's barriers per NORSOK D-010 SIMOPS guidelines.",
        reasoning_framework="SIMOPS: drilling and completion, drilling and production, multiple drilling operations. Each well must maintain two independent barriers. One well's operation cannot compromise another. Formal risk assessment required. Communication protocols between operations. Shut-in procedures if interference detected. Pressure testing schedules coordinated. Dedicated supervisors for each operation. Common hazards: mud gas entering adjacent well, pressure communication through formation, lost circulation affecting offset.",
        key_factors=[
            "Each well maintains two independent barriers",
            "Formal SIMOPS risk assessment required",
            "One operation cannot compromise another's barriers",
            "Communication protocols between operations",
            "Coordinated pressure testing schedules",
            "Dedicated supervisor for each operation",
            "Shut-in procedures if interference detected"
        ],
        primary_authority=[
            "NORSOK D-010 Section 8 - SIMOPS",
            "API RP 96 Appendix C - SIMOPS Guidelines",
            "UK HSE SIMOPS Guidance Notes"
        ],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.BARRIER_PHILOSOPHY
    ),
]

# ============================================================================
# TELEMETRY
# ============================================================================

class Telemetry:
    def __init__(self):
        self.queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_response_time = 0.0
        self.start_time = datetime.now()

    def record_query(self, response_time: float, cache_hit: bool):
        self.queries += 1
        self.total_response_time += response_time
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def get_stats(self) -> Dict[str, Any]:
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_response = self.total_response_time / self.queries if self.queries > 0 else 0

        return {
            "queries": self.queries,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": self.cache_hits / self.queries if self.queries > 0 else 0,
            "avg_response_time_ms": avg_response,
            "uptime_seconds": uptime
        }

# ============================================================================
# ENGINE CORE
# ============================================================================

class WellControlEngine:
    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.telemetry = Telemetry()
        logger.info(f"{ENGINE_NAME} initialized with {len(self.doctrines)} doctrine blocks")

    def _match_doctrines(self, question: str, context: Optional[Dict] = None) -> List[DoctrineBlock]:
        """Match question to relevant doctrines"""
        question_lower = question.lower()
        matches = []

        for doctrine in self.doctrines:
            score = 0.0

            # Keyword matching
            for keyword in doctrine.keywords:
                if keyword in question_lower:
                    score += 1.0

            # Category bonus if context provides category
            if context and context.get("category") == doctrine.category:
                score += 0.5

            # Safety critical bonus
            if doctrine.safety_critical and any(word in question_lower for word in ["emergency", "critical", "danger", "fatal"]):
                score += 0.3

            if score > 0:
                matches.append((score, doctrine))

        # Sort by score descending
        matches.sort(key=lambda x: x[0], reverse=True)

        # Return top matches
        return [d for _, d in matches[:5]]

    def _generate_response(
        self,
        question: str,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        context: Optional[Dict]
    ) -> str:
        """Generate response based on mode and matched doctrines"""

        if not doctrines:
            return "No relevant well control doctrine found for this query. Please provide more specific well control terminology or context."

        primary = doctrines[0]

        if mode == ResponseMode.FAST:
            # Concise answer
            return primary.conclusion_template

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready detailed answer
            answer_parts = [
                f"WELL CONTROL ANALYSIS - {primary.topic}",
                "",
                "CONCLUSION:",
                primary.conclusion_template,
                "",
                "TECHNICAL FRAMEWORK:",
                primary.reasoning_framework[:800],
                "",
                "KEY OPERATIONAL FACTORS:",
            ]
            for factor in primary.key_factors:
                answer_parts.append(f"  - {factor}")

            answer_parts.append("")
            answer_parts.append("AUTHORITATIVE SOURCES:")
            for auth in primary.primary_authority:
                answer_parts.append(f"  - {auth}")

            if primary.counter_arguments:
                answer_parts.append("")
                answer_parts.append("ALTERNATIVE CONSIDERATIONS:")
                for arg in primary.counter_arguments:
                    answer_parts.append(f"  - {arg}")

            return "\n".join(answer_parts)

        else:  # MEMO
            # Full documentation with all matched doctrines
            answer_parts = [
                f"COMPREHENSIVE WELL CONTROL MEMORANDUM",
                f"Re: {question}",
                f"Date: {datetime.now().strftime('%Y-%m-%d')}",
                "",
                "EXECUTIVE SUMMARY:",
                primary.conclusion_template,
                "",
                "DETAILED ANALYSIS:",
                ""
            ]

            for i, doctrine in enumerate(doctrines[:3], 1):
                answer_parts.extend([
                    f"{i}. {doctrine.topic}",
                    "",
                    doctrine.reasoning_framework,
                    "",
                    "Key Factors:",
                ])
                for factor in doctrine.key_factors:
                    answer_parts.append(f"  - {factor}")

                answer_parts.append("")
                answer_parts.append("Authorities:")
                for auth in doctrine.primary_authority:
                    answer_parts.append(f"  - {auth}")

                answer_parts.append("")

            return "\n".join(answer_parts)

    def _calculate_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Determine confidence based on doctrine matches"""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        primary = doctrines[0]

        # If primary doctrine is safety critical and high confidence, maintain that
        if primary.safety_critical and primary.confidence == ConfidenceLevel.DEFENSIBLE:
            return ConfidenceLevel.DEFENSIBLE

        # If multiple strong matches, defensible
        if len(doctrines) >= 3:
            return ConfidenceLevel.DEFENSIBLE

        return primary.confidence

    def _determinism_hash(self, question: str, mode: str) -> str:
        """Generate SHA-256 hash for reproducibility"""
        content = f"{question}|{mode}|{VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def query(self, request: QueryRequest) -> EngineResponse:
        """Main query endpoint"""
        start = datetime.now()

        # Match doctrines
        matched = self._match_doctrines(request.question, request.context)
        cache_hit = len(matched) > 0

        # Generate response
        answer = self._generate_response(
            request.question,
            matched,
            request.mode,
            request.context
        )

        # Build doctrine matches
        doctrine_matches = [
            DoctrineMatch(
                topic=d.topic,
                confidence=0.9 if i == 0 else 0.7,
                reasoning=d.reasoning_framework[:200] + "...",
                authorities=d.primary_authority
            )
            for i, d in enumerate(matched[:3])
        ]

        # Calculate confidence
        confidence = self._calculate_confidence(matched)

        # Build reasoning chain
        reasoning_chain = [
            f"Matched {len(matched)} doctrine blocks",
            f"Primary doctrine: {matched[0].topic}" if matched else "No strong match",
            f"Confidence level: {confidence.value}",
            f"Response mode: {request.mode.value}"
        ]

        # Aggregate authorities
        authorities = []
        for d in matched[:3]:
            authorities.extend(d.primary_authority)
        authorities = list(set(authorities))[:5]

        # Warnings
        warnings = []
        if any(d.safety_critical for d in matched):
            warnings.append("SAFETY CRITICAL: This involves life-safety operations requiring trained personnel")
        if confidence == ConfidenceLevel.HIGH_RISK:
            warnings.append("HIGH RISK: Consult qualified well control engineer before proceeding")

        # Calculate response time
        response_time = (datetime.now() - start).total_seconds() * 1000

        # Record telemetry
        self.telemetry.record_query(response_time, cache_hit)

        return EngineResponse(
            answer=answer,
            confidence=confidence,
            doctrine_matches=doctrine_matches,
            reasoning_chain=reasoning_chain,
            authorities=authorities,
            warnings=warnings,
            determinism_hash=self._determinism_hash(request.question, request.mode.value),
            response_time_ms=response_time,
            mode=request.mode
        )

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title=f"{ENGINE_ID} - {ENGINE_NAME}",
    version=VERSION,
    description="TIE Gold Standard - Well Control & Kick Management Intelligence"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = WellControlEngine()
start_time = datetime.now()

@APP.post("/query", response_model=EngineResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    try:
        return await engine.query(request)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint"""
    uptime = (datetime.now() - start_time).total_seconds()
    return HealthResponse(
        status="operational",
        engine_id=ENGINE_ID,
        version=VERSION,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=uptime
    )

@APP.get("/stats")
async def stats_endpoint():
    """Telemetry stats endpoint"""
    return engine.telemetry.get_stats()

@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "safety_critical": d.safety_critical
            }
            for d in DOCTRINE_CACHE
        ]
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Doctrine blocks loaded: {len(DOCTRINE_CACHE)}")

    uvicorn.run(
        APP,
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
