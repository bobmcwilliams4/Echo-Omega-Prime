import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

# ═══════════════════════════════════════════════════════════════════════════
# AUTO02 - AUTOMOTIVE TRANSMISSION SYSTEMS INTELLIGENCE ENGINE
# ═══════════════════════════════════════════════════════════════════════════
# TIE-20 Gold Standard Engine
# Domain: Automotive transmission design, diagnosis, repair, and analysis
# Port: 9062
# Version: 1.0.0
# ═══════════════════════════════════════════════════════════════════════════

APP = FastAPI(title="AUTO02 Transmission Systems Engine", version="1.0.0")
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add(
    Path(__file__).parent / "logs" / "auto02_{time}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO"
)


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS & MODELS
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
    MANUAL_TRANSMISSION = "MANUAL_TRANSMISSION"
    AUTOMATIC_TRANSMISSION = "AUTOMATIC_TRANSMISSION"
    CVT_SYSTEMS = "CVT_SYSTEMS"
    DCT_SYSTEMS = "DCT_SYSTEMS"
    TRANSFER_CASES = "TRANSFER_CASES"
    DIFFERENTIALS = "DIFFERENTIALS"
    FLUID_ANALYSIS = "FLUID_ANALYSIS"
    CLUTCH_SYSTEMS = "CLUTCH_SYSTEMS"
    DIAGNOSTICS = "DIAGNOSTICS"
    ELECTRONIC_CONTROL = "ELECTRONIC_CONTROL"
    HYBRID_TRANSMISSIONS = "HYBRID_TRANSMISSIONS"
    REBUILD_PROCEDURES = "REBUILD_PROCEDURES"
    DRIVETRAIN_NVH = "DRIVETRAIN_NVH"
    PERFORMANCE_TUNING = "PERFORMANCE_TUNING"


class DoctrineBlock(BaseModel):
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
    category: IssueCategory
    controlling_precedent: Optional[str] = None


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    category_hint: Optional[IssueCategory] = None


class QueryResponse(BaseModel):
    query: str
    mode: ResponseMode
    response: str
    doctrine_blocks_triggered: List[str]
    confidence: ConfidenceLevel
    categories: List[IssueCategory]
    reasoning_chain: List[str]
    determinism_hash: str
    telemetry: Dict[str, Any]


# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Manual Transmission Synchronizer Design",
        keywords=["synchronizer", "synchro", "brass ring", "cone clutch", "blocking ring", "shift fork", "manual transmission"],
        conclusion_template=[
            "Synchronizer assemblies enable smooth gear engagement by matching shaft speeds before locking.",
            "Cone clutch friction synchronizes rotational speeds, brass/carbon blocking rings prevent premature engagement.",
            "Worn synchronizers manifest as grinding during shifts, difficulty engaging gears, or jumping out of gear."
        ],
        reasoning_framework="""
        Synchronizer mechanism fundamentals:
        - Hub splined to output shaft, sleeve slides on hub via shift fork
        - Blocking ring has internal cone surface matching gear cone
        - Friction torque brings gear to shaft speed before sleeve teeth engage
        - Strut-type or pin-type detents hold sleeve in neutral or engaged
        - Double-cone synchronizers provide higher torque capacity
        - Carbon-lined rings offer better friction characteristics than brass

        Failure modes:
        - Cone surface wear reduces friction capacity → incomplete synchronization
        - Blocking ring groove wear allows premature lockout
        - Hub spline wear causes backlash and noise
        - Detent spring fatigue leads to gear pop-out
        - Shift fork wear creates misalignment

        Diagnostic indicators:
        - 2nd gear grind = most common (highest torque multiplication)
        - Cold operation grind = fluid viscosity masking synchronizer wear
        - Downshift grind = excessive speed differential overwhelming synchro
        - Reverse grind normal = no synchronizer on reverse gear (most designs)
        """,
        key_factors=[
            "Cone angle (typically 7-8 degrees for optimal friction)",
            "Blocking ring material (brass, carbon-composite, molybdenum)",
            "Synchro mesh clearances (0.05-0.15mm typical)",
            "Shift effort and cable/linkage condition",
            "Transmission fluid condition and specification",
            "Dual-cone vs single-cone design for torque capacity"
        ],
        primary_authority=[
            "SAE J2879 - Manual Transmission Synchronizer Testing",
            "OEM service manual synchronizer wear limits",
            "Borg-Warner synchronizer design patents and technical papers"
        ],
        burden_holder="Technician diagnosing shift quality issues",
        adversary_position="Misdiagnosis as clutch problem or shifter cable issue",
        counter_arguments=[
            "Clutch not releasing fully can mimic synchronizer wear",
            "Linkage bushings worn can create false grind sensation",
            "Incorrect fluid viscosity affects shift quality",
            "Pilot bearing failure loads input shaft affecting synchro operation"
        ],
        resolution_strategy="Inspect synchronizer assemblies for cone wear, measure blocking ring gap, check for brass debris in fluid, verify clutch release clearance, test in multiple gears to isolate affected synchro.",
        entity_scope=["Manual transmission assemblies", "5-speed and 6-speed gearboxes", "Performance and OEM applications"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.MANUAL_TRANSMISSION
    ),

    DoctrineBlock(
        topic="Automatic Transmission Planetary Gear Set Design",
        keywords=["planetary", "sun gear", "ring gear", "planet carrier", "Simpson gear set", "Ravigneaux", "automatic transmission"],
        conclusion_template=[
            "Planetary gear sets provide multiple gear ratios through selective holding and driving of sun, carrier, and ring elements.",
            "Simpson compound planetary (common design) achieves 4 forward ratios and reverse with two simple planetaries.",
            "Holding one element and driving another produces different ratios; holding two elements locks the set for direct drive."
        ],
        reasoning_framework="""
        Planetary gear fundamentals:
        - Simple planetary: sun gear (center), planet gears on carrier, ring gear (outer)
        - Ratio calculation: (Ring teeth) / (Sun teeth) when carrier held, sun input, ring output
        - Three elements allow six possible operational modes
        - Simpson set: shares common sun gear between two planetaries
        - Ravigneaux: combines long and short planets, one carrier, two sun gears

        Operational modes:
        - Overdrive: Ring held, carrier input, sun output (ratio < 1.0)
        - Reduction: Sun input, carrier output, ring held (ratio > 1.0)
        - Direct drive: Any two elements locked (ratio = 1.0)
        - Reverse: Sun input, ring output, carrier held (reverses rotation)
        - Neutral: No elements held (freewheels)

        Common ratios in 4-speed automatic:
        - 1st: 2.4-2.8:1 (sun input, carrier output, ring held)
        - 2nd: 1.5-1.6:1 (different element combination)
        - 3rd: 1.0:1 (direct drive, two elements locked)
        - 4th (OD): 0.7-0.75:1 (carrier input, sun output, ring held)
        - Reverse: -2.0 to -2.4:1 (sun input, ring output, carrier held)
        """,
        key_factors=[
            "Gear tooth count and ratio calculations",
            "Clutch pack and band application timing (overlap vs gap)",
            "One-way clutch (sprag/roller) operation in 1st and 2nd",
            "Thrust bearing loading and end play specifications",
            "Planet carrier pinion bearing condition",
            "Ring gear internal spline wear"
        ],
        primary_authority=[
            "Transmission Bench Overhaul Manuals by OEM",
            "SAE J2807 - Planetary Gear Design Standards",
            "ATSG (Automatic Transmission Service Group) Technical Manuals"
        ],
        burden_holder="Transmission rebuilder or diagnostician",
        adversary_position="Electronic/hydraulic control blamed for mechanical planetary failure",
        counter_arguments=[
            "Wrong gear ratio can be pressure regulator or solenoid issue",
            "Slipping can be clutch pack instead of planetary damage",
            "Noise can be pump, torque converter, or differential",
            "Incorrect diagnosis wastes teardown labor"
        ],
        resolution_strategy="Perform stall test to check holding ability, use pressure gauges to verify clutch application, listen for planetary whine under load, inspect for metal in pan indicating gear tooth damage, measure end play during teardown.",
        entity_scope=["4-speed, 5-speed, 6-speed automatics", "RWD and FWD transaxles", "Light truck and passenger car"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.AUTOMATIC_TRANSMISSION
    ),

    DoctrineBlock(
        topic="Torque Converter Operation and Diagnosis",
        keywords=["torque converter", "stator", "impeller", "turbine", "lockup clutch", "TCC", "stall speed", "converter shudder"],
        conclusion_template=[
            "Torque converter multiplies engine torque through fluid coupling between impeller and turbine, with stator redirecting flow.",
            "Lockup clutch mechanically couples turbine to impeller above ~45 mph to eliminate slip losses and improve fuel economy.",
            "Converter shudder indicates lockup clutch facing degradation; stall speed diagnosis reveals internal damage or engine issues."
        ],
        reasoning_framework="""
        Torque converter operation:
        - Impeller (pump) driven by engine, throws fluid outward
        - Turbine receives fluid energy, drives transmission input shaft
        - Stator between impeller and turbine redirects fluid for torque multiplication
        - One-way clutch on stator allows it to freewheel at coupling point (~0.9 speed ratio)
        - Torque multiplication factor typically 2.0-2.5:1 at stall
        - Lockup clutch eliminates 2-5% slip loss for efficiency

        Stall speed testing:
        - Normal stall: 2000-2600 RPM (engine and converter specific)
        - High stall: weak engine (low power) or transmission slipping (not holding)
        - Low stall: restricted exhaust, engine timing issue, or stator one-way clutch failed (locked both directions)
        - Stall test should be brief (5 seconds max) to avoid overheating

        Lockup clutch (TCC) issues:
        - Shudder at 40-50 mph = clutch facing material degraded, fluid contaminated
        - No lockup = solenoid failure, wiring issue, valve body problem
        - Harsh engagement = PID control issue, worn damper springs
        - Slipping lockup = facing wear, pressure regulation fault

        Failure modes:
        - Hub weld failure (catastrophic, lots of metal in pan)
        - Stator one-way clutch failure (freewheels both ways = no multiplication, or locks both ways = no coupling)
        - Turbine blade damage (impact from hard part failure)
        - Lockup clutch friction material delamination
        """,
        key_factors=[
            "Stall speed specification vs actual measurement",
            "Fluid condition (contamination indicates internal damage)",
            "TCC duty cycle percentage from scan tool",
            "Temperature rise during operation",
            "Vibration frequency (12-15 Hz typical for shudder)",
            "Presence of metal debris in pan"
        ],
        primary_authority=[
            "OEM stall speed specifications",
            "SAE J1967 - Torque Converter Performance Testing",
            "ATSG torque converter diagnostic procedures"
        ],
        burden_holder="Transmission technician diagnosing converter-related issues",
        adversary_position="Misdiagnosis as transmission slip when converter is cause",
        counter_arguments=[
            "Slipping transmission and converter slip feel similar to driver",
            "Shudder can be misdiagnosed as engine misfire or U-joint issue",
            "Low stall can be mistaken for weak engine rather than stator failure",
            "Expensive replacement part creates pressure to misdiagnose as fluid/filter issue"
        ],
        resolution_strategy="Perform stall test in drive and reverse (compare), scan for TCC duty cycle and slip RPM, fluid analysis for friction material, temperature measurement during lockup, road test for shudder frequency.",
        entity_scope=["All automatic transmissions with fluid coupling", "Conventional and lockup torque converters", "Variable stator converters"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.AUTOMATIC_TRANSMISSION
    ),

    DoctrineBlock(
        topic="CVT Belt/Chain System Design and Failure",
        keywords=["CVT", "continuously variable", "steel belt", "push belt", "chain CVT", "pulley", "ratio control", "judder"],
        conclusion_template=[
            "CVT systems use steel belt or chain running between variable-width pulleys to provide infinite ratio adjustment.",
            "Pulley clamping force must match torque load; insufficient pressure causes belt slip and rapid wear.",
            "CVT fluid condition is critical - contamination causes belt slip, judder, and ratio control failure."
        ],
        reasoning_framework="""
        CVT operating principles:
        - Two pulleys: primary (input, driven by engine) and secondary (output, to final drive)
        - Each pulley has movable sheave controlled by hydraulic pressure
        - Ratio change: squeeze one pulley (belt rides higher), release other (belt rides lower)
        - Steel belt (Van Doorne type) or chain (LUK, Jatco) connects pulleys
        - Belt is not V-belt friction drive; it's compression loaded (segments push on each other)

        Ratio control:
        - Low ratio (launch): primary pulley open (wide), secondary closed (narrow) - belt rides low on primary, high on secondary
        - High ratio (overdrive): primary closed, secondary open - belt rides high on primary, low on secondary
        - Steptronic/manual mode: TCM holds ratio at predefined points

        Common failures:
        - Belt slip: insufficient clamping pressure, worn belt surface, contaminated fluid
        - Judder: stick-slip phenomenon, usually fluid degradation or pressure modulation issue
        - Whining noise: belt edge wear, misalignment, bearing issues
        - Stuck ratio: stepper motor failure, valve body contamination
        - Shudder on launch: torque converter lockup or pressure modulation fault

        Fluid requirements:
        - CVT fluid is NOT interchangeable with ATF
        - Specific friction modifiers prevent belt slip
        - NS-2, NS-3 (Nissan), CVT-F (Toyota), CVTF (Honda) - NOT universal
        - Fluid breakdown causes loss of friction, leading to belt slip and overheating
        """,
        key_factors=[
            "Fluid condition and correct specification (NS-2, NS-3, etc.)",
            "Pulley surface condition and cleanliness",
            "Belt or chain wear limits and stretch measurement",
            "Hydraulic pressure readings (primary and secondary circuits)",
            "Stepper motor operation and calibration",
            "TCM adaptation values and learning status"
        ],
        primary_authority=[
            "OEM CVT service manuals (Nissan, Honda, Toyota, Subaru)",
            "Van Doorne and LUK CVT technical publications",
            "JATCO CVT overhaul procedures"
        ],
        burden_holder="CVT specialist technician (dealer or transmission shop)",
        adversary_position="Misdiagnosis as torque converter or engine power issue",
        counter_arguments=[
            "Shudder can be engine misfire, torque converter, or CVT - difficult to isolate",
            "Ratio control issues can mimic throttle position sensor faults",
            "CVT whine can be confused with differential or wheel bearing noise",
            "Expensive CVT replacement creates incentive to blame external components"
        ],
        resolution_strategy="Scan for ratio deviation codes, pressure test primary/secondary circuits, fluid analysis for metal content, visual inspection of belt/chain for glazing or edge wear, stepper motor voltage/resistance testing, road test for slip under load.",
        entity_scope=["Nissan/Jatco CVT7/8", "Honda CVT", "Toyota K310/K311", "Subaru Lineartronic", "Audi Multitronic"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CVT_SYSTEMS
    ),

    DoctrineBlock(
        topic="Dual Clutch Transmission (DCT) Operation",
        keywords=["dual clutch", "DCT", "DSG", "Powershift", "PDK", "mechatronic", "dry clutch", "wet clutch"],
        conclusion_template=[
            "DCT uses two clutches and two input shafts (odd/even gears) to pre-select next gear for near-instantaneous shifts.",
            "Wet clutch designs (VW DSG6/7) handle higher torque but require fluid service; dry clutch (Ford, VW DQ200) lighter but wear-sensitive.",
            "Mechatronic unit integrates valve body, TCM, and sensors - expensive assembly, often replaced as unit."
        ],
        reasoning_framework="""
        DCT architecture:
        - Two clutches: one for odd gears (1-3-5-R), one for even gears (2-4-6)
        - Two input shafts: outer hollow shaft (one clutch), inner solid shaft (other clutch)
        - Pre-selection: while driving in 3rd (odd clutch engaged), 4th gear is already engaged on even shaft
        - Upshift: release odd clutch, engage even clutch - effectively two manual transmissions working together
        - Clutch actuation: hydraulic (VW DSG) or electromechanical (Ford Powershift, BMW DCT)

        Wet vs Dry clutch:
        - Wet (DSG DQ250, DQ500): multi-plate clutches in oil, higher torque capacity, require fluid changes every 40-60k mi
        - Dry (DSG DQ200, Ford): single-plate clutch in bell housing, lower parasitic loss, but subject to wear like manual clutch
        - Dry clutch limited to ~250 lb-ft torque, wet clutch up to 400+ lb-ft

        Common failures:
        - Mechatronic unit: valve body contamination, solenoid failure, TCM corruption
        - Clutch wear (dry clutch DCT): judder, slip, smell - similar to manual clutch
        - Dual-mass flywheel failure (wet clutch DCT): rattling at idle, vibration
        - Clutch fork/release bearing (dry clutch): noise, inconsistent engagement
        - Fluid degradation (wet clutch): shift quality, pressure regulation issues

        Diagnostic challenges:
        - Launch shudder: can be clutch wear, flywheel, or pressure modulation
        - Harsh shifts: software calibration, clutch bite point adaptation, or mechanical wear
        - Neutral at stops: clutch overheating protection mode - not a fault, but symptom of abuse or wear
        """,
        key_factors=[
            "Clutch adaptation values and bite point learning status",
            "Mechatronic unit software version and updates",
            "Fluid condition and level (wet clutch designs)",
            "Dual-mass flywheel condition (wet clutch designs)",
            "Clutch disc friction material remaining (dry clutch)",
            "Launch strategy adaptation (creep, hill hold, manual mode)"
        ],
        primary_authority=[
            "VW/Audi DSG Technical Service Bulletins",
            "Ford Powershift Service Manual and TSBs",
            "Porsche PDK Technical Training Materials",
            "SAE papers on dual-clutch transmission control strategies"
        ],
        burden_holder="Dealer technician with factory scan tool and software access",
        adversary_position="Independent shop lacking adaptation/programming capability",
        counter_arguments=[
            "Some DCT issues require software updates not available to independents",
            "Clutch adaptation procedure requires specific scan tool functions",
            "Mechatronic unit replacement expensive - pressure to misdiagnose as clutch wear",
            "Judder can be flywheel, motor mounts, or clutch - difficult to isolate without disassembly"
        ],
        resolution_strategy="Scan for clutch adaptation values and compare to specifications, monitor clutch slip under load, check software version against TSB database, fluid analysis for contamination (wet clutch), measure dual-mass flywheel free-play, test launch quality in manual mode.",
        entity_scope=["VW DSG (DQ250, DQ500, DQ200)", "Ford Powershift", "Porsche PDK", "BMW DCT (M-series)", "Hyundai/Kia DCT"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DCT_SYSTEMS
    ),

    DoctrineBlock(
        topic="Transfer Case Design - Part-Time vs Full-Time 4WD",
        keywords=["transfer case", "4WD", "AWD", "part-time", "full-time", "NP231", "NP241", "viscous coupling", "chain drive"],
        conclusion_template=[
            "Part-time 4WD locks front and rear driveshafts together (1:1 ratio) via sliding collar - must not be used on dry pavement.",
            "Full-time 4WD uses center differential or viscous coupling to allow front/rear speed differentiation for on-road use.",
            "Chain-drive transfer cases (common in IFS trucks) are lighter but less durable than gear-driven designs for severe off-road use."
        ],
        reasoning_framework="""
        Part-time 4WD operation:
        - 2WD mode: power to rear axle only, front axle freewheeling
        - 4WD mode: sliding collar locks front and rear outputs together
        - No speed differentiation allowed - front/rear axles turn at same speed
        - Dry pavement binding: turning causes front axle to travel further than rear (different radii), inducing driveline wind-up
        - Use only on slippery surfaces (snow, mud, loose gravel) where tire slip relieves wind-up
        - Examples: NP231, NP241, BW1354, manual locking hubs on older trucks

        Full-time 4WD/AWD operation:
        - Center differential allows front/rear speed differentiation (like rear diff allows left/right wheel speed difference)
        - Open center diff: can drive on pavement, but loses all traction if one axle lifts (power takes path of least resistance)
        - Locking center diff: driver can lock for off-road, creating part-time 4WD behavior
        - Viscous coupling: silicone fluid creates progressive lockup under speed difference - no driver input needed
        - Examples: NP242 (Selec-Trac), Quadra-Trac, Mercedes 4Matic, Audi Quattro (Torsen center diff)

        Chain vs gear drive:
        - Chain drive: lighter, quieter, cheaper, used in most IFS trucks (NP231, NP241, BW4405)
        - Gear-driven: heavier, more durable, used in severe-duty trucks (NP205, NP208, Atlas II)
        - Chain stretch and wear common after 150k+ miles, especially with larger tires
        - Chain slap noise on decel indicates wear or low fluid level

        Common failures:
        - Mode fork/slider wear causing incomplete engagement
        - Chain stretch causing slap, whine, or jumps out of 4WD
        - Viscous coupling lockup (shudders turning) or failure (no torque transfer)
        - Encoder motor/actuator failure on electronic shift systems
        - Leaking seals causing fluid loss and chain wear
        """,
        key_factors=[
            "Tire size and gear ratio matching front/rear",
            "Fluid level and condition (ATF or gear oil depending on design)",
            "Chain stretch measurement during inspection",
            "Mode fork engagement travel and wear",
            "Encoder motor position sensor accuracy",
            "Viscous coupling shear strength (if equipped)"
        ],
        primary_authority=[
            "NP (New Process/Magna) Transfer Case Service Manuals",
            "BorgWarner Transfer Case Technical Publications",
            "OEM 4WD system diagnostic procedures"
        ],
        burden_holder="4WD/truck specialist technician",
        adversary_position="Misdiagnosis as axle or differential problem",
        counter_arguments=[
            "Transfer case noise can mimic rear differential noise - difficult to isolate",
            "Binding on pavement can be blamed on limited-slip rear diff instead of 4WD engagement",
            "Electronic shift issues can be wiring/switch rather than internal transfer case fault",
            "Fluid leak location can be confused with transmission output seal"
        ],
        resolution_strategy="Test 4WD engagement with wheels off ground (observe front driveshaft rotation), fluid analysis for metal content indicating chain wear, scan for encoder position vs commanded position, on-road test for binding or shudder, inspection for leaks at all seal locations.",
        entity_scope=["NP231, NP241, NP241OR, NP263", "BW4405, BW4410", "Mercedes, Audi, BMW AWD systems", "Truck and SUV applications"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.TRANSFER_CASES
    ),

    DoctrineBlock(
        topic="Differential Types and Limited-Slip Operation",
        keywords=["differential", "limited slip", "LSD", "posi", "locking differential", "Torsen", "clutch pack", "open differential"],
        conclusion_template=[
            "Open differential allows wheel speed differentiation but sends all torque to the wheel with least traction (unloaded wheel).",
            "Clutch-type limited-slip uses friction discs preloaded by springs to bias torque toward wheel with traction.",
            "Torsen (torque-sensing) differential uses worm gears to provide automatic torque biasing without clutches or electronics."
        ],
        reasoning_framework="""
        Open differential operation:
        - Ring gear drives carrier, spider gears (pinions) mesh with side gears
        - Turning: inside wheel slows down, outside speeds up - pinions walk around side gears
        - Straight line: pinions don't rotate, both wheels driven equally
        - Traction loss: pinion rotates freely sending torque to unloaded wheel (path of least resistance)
        - One wheel on ice: spinning wheel gets 100% torque, wheel with traction gets 0%

        Clutch-type limited-slip (posi):
        - Clutch packs between side gears and carrier
        - Preload springs apply constant clamping force (~50-100 lb-ft breakaway torque)
        - Side gear tries to rotate relative to carrier, clutch resists, biasing torque to other wheel
        - Friction modifier additive in gear oil prevents chatter
        - Wear: clutch discs wear reducing breakaway torque - eventually behaves like open diff
        - GM Eaton G80 (Gov-Lok): flyweight actuated, engages when speed difference detected

        Torsen differential:
        - Worm gears (side gears) meshed with spur gears (pinions) in perpendicular orientation
        - Worm gear high friction (can't be back-driven easily) creates torque multiplication
        - Torque bias ratio (TBR): 2.5:1 to 5:1 typical - wheel with traction gets 2.5-5x more torque than slipping wheel
        - No clutches to wear, no maintenance, fully mechanical
        - Limitation: still needs some traction both wheels - can't transfer 100% to one wheel
        - Used in Audi Quattro, Toyota trucks (rear diff), GM Hummer H3

        Locking differentials:
        - ARB Air Locker: compressed air actuates locking collar, making diff 100% locked (spool)
        - Detroit Locker: automatic mechanical lock, ratchets on turns (clunking normal)
        - E-locker (electric): solenoid actuates locking mechanism
        - Use: off-road only (except Detroit which auto-unlocks), binding on pavement when locked
        """,
        key_factors=[
            "Breakaway torque measurement (clutch-type LSD)",
            "Friction modifier additive in gear oil (clutch LSD only)",
            "Torque bias ratio specification (Torsen)",
            "Chatter on turns indicates clutch wear or wrong fluid",
            "Air pressure and seal integrity (ARB locker)",
            "Electrical connector and wiring (E-locker)"
        ],
        primary_authority=[
            "Eaton Posi Limited-Slip Service Manual",
            "Torsen Differential Technical Publications",
            "ARB Air Locker Installation and Service Guide",
            "OEM axle service procedures"
        ],
        burden_holder="Technician diagnosing traction or noise issues",
        adversary_position="Misdiagnosis as axle bearing, U-joint, or driveshaft problem",
        counter_arguments=[
            "Chatter can be misdiagnosed as CV joint or wheel bearing",
            "LSD clutch wear causes loss of traction similar to open diff - may not be obvious without testing",
            "Locker electrical issues can be blamed on axle mechanical failure",
            "Noise from Detroit Locker is normal operation but often mistaken for failure"
        ],
        resolution_strategy="Perform breakaway torque test (coast clutch test for clutch LSD), verify correct gear oil and friction modifier, test traction with one wheel on rollers (or ice), inspect for fluid leaks (air locker), scan for locker engagement signal (E-locker).",
        entity_scope=["Eaton, Auburn, Detroit limited-slip", "Torsen T-1, T-2, T-3", "ARB, OX, E-locker locking diffs", "Truck, SUV, performance car axles"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DIFFERENTIALS
    ),

    DoctrineBlock(
        topic="Transmission Fluid Analysis and Specification",
        keywords=["ATF", "transmission fluid", "Dexron", "Mercon", "CVT fluid", "friction modifier", "fluid analysis", "contamination"],
        conclusion_template=[
            "Transmission fluid specifications are NOT universal - using incorrect fluid causes shift quality issues, clutch slip, and seal degradation.",
            "Fluid analysis reveals internal component wear through metal particulate identification before catastrophic failure.",
            "CVT fluid is NOT interchangeable with ATF - different friction characteristics required for steel belt operation."
        ],
        reasoning_framework="""
        Fluid specification importance:
        - ATF properties: friction characteristics, viscosity, oxidation resistance, seal compatibility
        - Dexron VI: backward compatible with Dexron III, not forward compatible (Dex III in Dex VI system = shift issues)
        - Mercon V vs Mercon LV: LV is lower viscosity, not interchangeable despite similar name
        - Honda DW-1/Z1: specific friction modifiers, NOT compatible with Dexron
        - Ford Type F: high friction (no friction modifiers) for older transmissions with bands
        - CVT fluid (NS-2, NS-3, CVT-F): prevents steel belt slip, NOT compatible with ATF

        Fluid analysis indicators:
        - Copper: bearing and bushing wear (normal wear metal in small quantities)
        - Iron: gear tooth wear, planetary damage (high levels indicate severe wear)
        - Aluminum: pump housing wear, valve body wear, planetary carrier
        - Lead: bearing overlay material, thrust washer wear
        - Friction material (particles): clutch disc wear, band lining material
        - Silver: coating on some bushings and thrust washers
        - Viscosity change: oxidation breakdown (increased viscosity) or fuel dilution (decreased)
        - Color: dark brown/black = oxidized/burnt, pink = normal, milky = coolant contamination

        Fluid contamination consequences:
        - Coolant contamination: destroys friction material, causes foaming, seal swell
        - Fuel contamination: reduces viscosity, causes clutch slip
        - Metal particulate: acts as abrasive, accelerates wear, clogs filter
        - Oxidation: varnish formation, valve body sticking, clutch glazing
        - Water intrusion: corrosion, loss of lubrication, foaming

        Change intervals:
        - Conventional ATF: 30-60k miles (severe duty) to 100k+ (normal duty)
        - CVT fluid: 30-60k miles (critical, cannot tolerate degradation)
        - DCT wet clutch: 40-60k miles
        - Lifetime fill myth: fluid degrades, "lifetime" means warranty period, not vehicle life
        """,
        key_factors=[
            "Exact fluid specification per OEM (not generic equivalent)",
            "Fluid level at operating temperature (overfill causes foaming, underfill causes starvation)",
            "Color and smell (burnt odor indicates overheating)",
            "Presence of metal particles or friction material debris",
            "Viscosity measurement vs specification",
            "Coolant contamination test (milky appearance)"
        ],
        primary_authority=[
            "OEM transmission fluid specifications",
            "ASTM D7450 - Automatic Transmission Fluid Testing",
            "Lubricant analysis lab reports (Blackstone, Polaris)",
            "SAE J2527 - Performance Requirements for Automatic Transmission Fluids"
        ],
        burden_holder="Technician selecting correct fluid and diagnosing fluid-related issues",
        adversary_position="Misdiagnosis of transmission failure when fluid degradation is root cause",
        counter_arguments=[
            "Using wrong fluid can mimic internal transmission failure (slip, harsh shifts)",
            "Fluid degradation slow and progressive - hard to pinpoint when problem started",
            "Generic 'universal ATF' claims vs OEM-specific requirements",
            "Cost pressure to use cheaper fluid instead of OEM specification"
        ],
        resolution_strategy="Verify exact fluid specification from OEM service information, fluid analysis for metal content and viscosity, drain and refill with correct fluid if wrong type suspected, monitor shift quality after fluid service, use dipstick or scan tool to verify correct level.",
        entity_scope=["All automatic transmissions, CVTs, DCTs", "Passenger cars, trucks, performance vehicles"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.FLUID_ANALYSIS
    ),

    DoctrineBlock(
        topic="Clutch Hydraulic System Operation and Diagnosis",
        keywords=["clutch master cylinder", "slave cylinder", "hydraulic clutch", "CSC", "concentric slave cylinder", "clutch pedal", "bleeding"],
        conclusion_template=[
            "Hydraulic clutch system uses master cylinder (pedal) and slave cylinder (release bearing actuation) connected by hydraulic line.",
            "Concentric slave cylinder (CSC) integrates slave and release bearing in one unit inside bellhousing - common failure point.",
            "Air in system or fluid contamination causes soft pedal, incomplete disengagement, and difficult shifting."
        ],
        reasoning_framework="""
        Hydraulic clutch operation:
        - Master cylinder: piston actuated by clutch pedal, generates hydraulic pressure
        - Slave cylinder: receives pressure, pushes clutch fork or release bearing
        - External slave: mounted outside bellhousing, pushes fork through pivot
        - Concentric slave (CSC): mounted on transmission input shaft, directly pushes release bearing
        - Fluid: DOT 3/4 brake fluid (hygroscopic, absorbs moisture over time)

        CSC advantages and failures:
        - Advantages: no clutch fork, less pedal effort, self-adjusting, compact
        - Failures: internal seals fail (leak fluid into bellhousing), bearing wears, plastic housing cracks
        - Failure symptoms: soft pedal, clutch not releasing, transmission removal required for replacement
        - Common in: GM trucks (2007+), Ford (2011+ Mustang, F-series), many European cars
        - Preventive replacement: when doing clutch job, replace CSC (labor already invested)

        Master cylinder failures:
        - Internal seal leak: pedal slowly sinks to floor when depressed, clutch won't disengage fully
        - External leak: fluid on firewall or carpet, reservoir level drops
        - Pushrod misalignment: hard pedal, incomplete actuation

        Slave cylinder failures:
        - External leak: visible fluid at cylinder or line connection
        - Internal leak (CSC): no visible leak, but soft pedal and incomplete disengagement
        - Pushrod extension incorrect: clutch won't release or over-releases (causing premature bearing wear)

        Bleeding procedure:
        - Gravity bleed: open bleeder, let fluid drip until no bubbles (slow but effective)
        - Vacuum bleed: vacuum pump on bleeder, draws fluid through system
        - Pressure bleed: pressurize reservoir, forces fluid through system (fastest)
        - Bench bleed master cylinder before installation (critical for new units)
        """,
        key_factors=[
            "Fluid level in reservoir and evidence of leaks",
            "Pedal feel (firm vs soft/spongy)",
            "Clutch release travel (measure at fork or pedal)",
            "Air in system (spongy pedal, inconsistent engagement point)",
            "Fluid contamination (moisture causes reduced boiling point)",
            "CSC bearing noise (grinding/whining when pedal depressed)"
        ],
        primary_authority=[
            "OEM clutch hydraulic system service procedures",
            "LUK Clutch Technical Training Materials",
            "SAE J1703 - Hydraulic Brake Fluid Standards (applies to clutch fluid)"
        ],
        burden_holder="Technician diagnosing clutch release issues",
        adversary_position="Misdiagnosis as clutch disc or pressure plate failure when hydraulic system is cause",
        counter_arguments=[
            "Incomplete clutch release can be hydraulic, clutch disc, or pilot bearing - all have similar symptoms",
            "Soft pedal can be air in system, master cylinder leak, or slave cylinder leak",
            "CSC failure requires transmission removal - expensive, creates pressure to misdiagnose",
            "Pilot bearing failure can mimic clutch not releasing (transmission hard to shift)"
        ],
        resolution_strategy="Check fluid level and inspect for leaks, test pedal firmness and travel, measure clutch fork travel at bellhousing, bleed system and retest, pressure test hydraulic circuit if soft pedal persists, scan for throwout bearing noise with pedal depressed.",
        entity_scope=["Manual transmissions with hydraulic clutch actuation", "GM, Ford, import cars and trucks", "CSC and external slave designs"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.CLUTCH_SYSTEMS
    ),

    DoctrineBlock(
        topic="Automatic Transmission Pressure Testing and Diagnosis",
        keywords=["line pressure", "clutch pressure", "solenoid", "valve body", "pressure regulator", "pressure test", "transmission diagnosis"],
        conclusion_template=[
            "Line pressure is main regulated pressure (150-250 psi typical), varies with throttle position and gear selection.",
            "Individual clutch/band pressure testing isolates hydraulic vs electronic faults in specific circuits.",
            "Low pressure indicates pump wear, regulator malfunction, or internal leak; high pressure indicates stuck regulator valve."
        ],
        reasoning_framework="""
        Hydraulic pressure fundamentals:
        - Pump generates pressure (front pump driven by torque converter)
        - Pressure regulator valve controls line pressure based on throttle position (TV cable/sensor) and load
        - Line pressure feeds: clutch packs, bands, torque converter, lubrication circuit
        - Solenoids modulate line pressure to individual clutch circuits for ratio control
        - Governor pressure (older transmissions) or vehicle speed sensor provides shift timing reference

        Line pressure specifications:
        - Idle in park: 50-90 psi (minimal demand)
        - Idle in drive: 90-150 psi (forward clutch applied)
        - Part throttle: 120-180 psi
        - Wide open throttle (WOT): 180-250+ psi (maximum holding force for performance)
        - Reverse: typically higher than drive (150-200 psi at idle)

        Pressure test points:
        - Line pressure port: usually on side of case or valve body
        - Governor pressure port (older transmissions): indicates VSS circuit operation
        - Individual clutch circuit ports (rebuild diagnosis): pinpoints which circuit leaking

        Diagnostic patterns:
        - Low pressure all conditions: pump wear, regulator stuck open, major internal leak, filter clogged
        - Low pressure one gear only: specific clutch circuit leak, piston seal failure, ball check valve
        - High pressure all conditions: regulator stuck closed, TV cable/sensor fault (thinks throttle wide open)
        - Fluctuating pressure: pump cavitation (low fluid level), aeration, regulator valve sticking
        - Normal pressure but slips: clutch pack wear, not hydraulic fault

        Solenoid testing:
        - Measure resistance (typically 10-30 ohms)
        - Command on/off with scan tool, verify pressure change
        - Pressure should drop when normally-open solenoid energized (or rise if normally-closed)
        - Stuck solenoid: pressure doesn't change with command
        - Shorted solenoid: 0 ohms or infinite ohms, blown fuse
        """,
        key_factors=[
            "Line pressure specification vs measured (idle, part throttle, WOT)",
            "Clutch circuit pressure in specific gears",
            "Solenoid duty cycle percentage from scan tool",
            "Fluid level (low level causes pump cavitation and low pressure)",
            "Filter condition (restriction causes pressure drop)",
            "Pump clearances and wear (measure during teardown)"
        ],
        primary_authority=[
            "OEM transmission service manual pressure specifications",
            "ATSG transmission repair manuals with pressure charts",
            "Transmission pressure test equipment manuals"
        ],
        burden_holder="Transmission diagnostician with pressure test equipment",
        adversary_position="Misdiagnosis as internal clutch failure when pressure regulation is cause",
        counter_arguments=[
            "Slipping can be low pressure OR clutch wear - both have similar symptoms",
            "Harsh shifts can be high pressure OR shift timing issue",
            "No specific gear can be pressure, clutch, or band - need pressure test to confirm",
            "Pressure testing requires drill/tap of case if no factory ports - invasive"
        ],
        resolution_strategy="Install pressure gauge at line pressure port, test at idle/part throttle/WOT in park and drive, test in all gears, compare to specifications, command solenoids on/off with scan tool and observe pressure change, fluid level verification.",
        entity_scope=["All automatic transmissions with hydraulic control", "RWD and FWD applications", "Electronic and conventional valve bodies"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DIAGNOSTICS
    ),

    DoctrineBlock(
        topic="Transmission Control Module (TCM) Adaptive Learning",
        keywords=["TCM", "adaptive learning", "shift adaptation", "clutch volume index", "CVI", "quick learn", "transmission programming"],
        conclusion_template=[
            "TCM adaptive learning compensates for clutch pack wear by adjusting shift pressures and timing over vehicle life.",
            "Clutch Volume Index (CVI) values indicate fluid volume required to apply each clutch - increasing values = wear.",
            "After transmission repair or fluid service, adaptive values must be cleared and re-learned for optimal shift quality."
        ],
        reasoning_framework="""
        Adaptive learning operation:
        - TCM monitors turbine speed, output speed, and input speed during shifts
        - Measures shift time (time from shift command to ratio change completion)
        - Target: smooth shift in 0.3-0.8 seconds (depending on shift type and load)
        - Too fast: harsh shift (bump) - TCM reduces pressure/overlap on next attempt
        - Too slow: slip (flare) - TCM increases pressure/overlap on next attempt
        - Adaptation range: typically ±30% from base calibration

        Clutch Volume Index (CVI):
        - Measures fluid volume (in mL or counts) required to stroke clutch piston and take up clearance
        - New clutch: low CVI (minimal volume to apply)
        - Worn clutch: high CVI (more volume needed to compress worn friction discs)
        - CVI reaches limit: TCM can't compensate further, slipping begins
        - Example values: new = 5-15 counts, worn = 40-60 counts, limit = 80 counts

        Reset/relearn procedures:
        - After rebuild: clear adaptations (old values don't match new clutches)
        - After fluid change: may need clear/relearn depending on system
        - Quick learn procedure: specific drive cycle (idle, drive, reverse, specific shifts) to accelerate learning
        - Cold learn: performed at cold temperatures for initial baseline
        - Full learn: 50-100 miles of varied driving for all shift types and conditions

        Failure to relearn consequences:
        - Old adaptation values cause harsh or slipping shifts with new clutches
        - TCM tries to apply old pressure/timing to new components
        - Can cause premature clutch wear if adaptations far from optimal
        - Customer complaint: "transmission worse after service"
        """,
        key_factors=[
            "CVI values per clutch (compare to specifications and limits)",
            "Adaptation values (pressure trim, timing offset) within range",
            "Shift time measurement vs target (too fast = harsh, too slow = slip)",
            "Number of learning cycles completed",
            "Fault codes for adaptation failures or sensor issues",
            "Scan tool capability to clear/reset adaptations and perform quick learn"
        ],
        primary_authority=[
            "OEM TCM adaptation procedures and specifications",
            "Factory scan tool quick learn drive cycles",
            "Transmission control system training materials"
        ],
        burden_holder="Technician with factory-level scan tool and adaptation capability",
        adversary_position="Independent shop without adaptation reset capability",
        counter_arguments=[
            "Some adaptations require dealer-only scan tool functions",
            "Relearn procedures vary by manufacturer and model year",
            "Failure to reset after service can be misdiagnosed as poor rebuild quality",
            "Customer may need to drive 50+ miles for full relearn - not instant fix"
        ],
        resolution_strategy="Scan for CVI values and compare to limits, check adaptation values against acceptable range, clear adaptations after service (if capable), perform quick learn procedure, road test for shift quality, monitor shift times with scan tool during test drive.",
        entity_scope=["All electronically controlled transmissions", "GM, Ford, Chrysler, import TCM systems", "6-speed, 8-speed, 10-speed modern automatics"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.ELECTRONIC_CONTROL
    ),

    DoctrineBlock(
        topic="Toyota Hybrid Transaxle (eCVT) Operation",
        keywords=["hybrid transaxle", "eCVT", "power split device", "planetary CVT", "MG1", "MG2", "Prius", "electric CVT"],
        conclusion_template=[
            "Toyota hybrid eCVT uses planetary gear set to blend engine and electric motor power without conventional transmission clutches or belts.",
            "MG1 (motor-generator 1) controls engine RPM via planetary sun gear; MG2 (motor-generator 2) provides propulsion via ring gear.",
            "No transmission fluid changes required (sealed system), but transaxle fluid separate from engine oil and coolant."
        ],
        reasoning_framework="""
        eCVT power-split device:
        - Simple planetary gear set: sun gear (MG1), carrier (engine), ring gear (MG2 + final drive)
        - Engine always connected to carrier - no clutch to disconnect
        - MG1 spins freely on sun gear, acts as generator or motor depending on load
        - MG2 spins ring gear, provides propulsion torque to wheels
        - Ratio control: vary MG1 speed to change effective ratio between engine and wheels

        Operating modes:
        - EV mode: engine off, MG2 drives wheels, MG1 freewheeling (sun gear spins freely)
        - Engine start: MG1 spins sun gear to crank engine via planetary carrier
        - Normal driving: engine drives carrier, MG1 controls engine RPM (generator or motor), MG2 assists or generates
        - High speed: MG1 spins backward to allow engine to rev higher than wheel speed (overdrive effect)
        - Regenerative braking: MG2 acts as generator, MG1 may spin engine for compression braking
        - Reverse: engine off, MG2 spins ring gear backward, carrier held stationary

        Advantages:
        - No belt or chain CVT wear issues (purely mechanical and electrical)
        - No clutches to slip or wear (no friction material)
        - Infinite ratio variability (MG1 speed control)
        - Smooth operation (no shift points)

        Service considerations:
        - Transaxle fluid: specific hybrid vehicle ATF (not conventional ATF)
        - Fluid change interval: none specified (lifetime fill per Toyota), but some recommend 100k mi
        - Separate cooling system for hybrid components (electric inverter coolant)
        - MG1/MG2 resolver sensors critical for operation (no Hall effect backup)
        - Park lock mechanism mechanical (pawl engages ring gear)

        Common issues:
        - Transaxle fluid leak at seals (coolant and ATF separated by seal)
        - MG1/MG2 bearing noise (whine or growl, not related to vehicle speed)
        - Inverter coolant pump failure (not transmission issue, but related system)
        - Hybrid battery degradation affects performance but not transaxle
        """,
        key_factors=[
            "Transaxle fluid level and condition (pink/red, not discolored)",
            "MG1/MG2 resolver sensor signals (scan tool monitoring)",
            "Inverter operation and fault codes",
            "Coolant system for inverter (separate from engine coolant)",
            "Park pawl engagement (P light on dash)",
            "Noise during EV mode (isolates transaxle noise from engine noise)"
        ],
        primary_authority=[
            "Toyota Hybrid System Training Materials",
            "Prius Repair Manual (Generation 2, 3, 4, 5)",
            "SAE papers on power-split hybrid transmissions"
        ],
        burden_holder="Hybrid-certified technician with HV safety training",
        adversary_position="Conventional transmission technician unfamiliar with eCVT operation",
        counter_arguments=[
            "eCVT noise can be misdiagnosed as conventional CVT belt issue",
            "Fluid leak can be misdiagnosed as engine or coolant leak (separate systems close together)",
            "MG resolver failure can mimic inverter or battery issue (all cause no-start or limp mode)",
            "No conventional transmission expertise applies - completely different design"
        ],
        resolution_strategy="Scan for hybrid system codes (P0A00-P3FFF range), monitor MG1/MG2 RPM and torque on scan tool, listen for noise during EV mode (engine off), verify transaxle fluid level and color, check for coolant contamination of transaxle fluid (milky appearance).",
        entity_scope=["Toyota Prius (all generations)", "Toyota Camry Hybrid", "Lexus hybrids (RX, ES, NX)", "RAV4 Hybrid", "Highlander Hybrid"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.HYBRID_TRANSMISSIONS
    ),

    DoctrineBlock(
        topic="Transmission Rebuild Quality Gates and Inspection",
        keywords=["rebuild", "overhaul", "hard parts", "soft parts", "clearances", "end play", "torque specs", "transmission rebuild"],
        conclusion_template=[
            "Transmission rebuild requires measurement of all clearances, end play, and selective fit components to factory specifications.",
            "Hard parts (shafts, cases, drums) must be inspected for wear, cracks, and spline damage; replace if beyond service limits.",
            "Soft parts (seals, gaskets, clutches, bands) always replaced during rebuild; filter and fluid are maintenance items."
        ],
        reasoning_framework="""
        Rebuild quality fundamentals:
        - Measure everything: end play, gear backlash, bushing clearances, clutch pack clearance
        - Replace soft parts: all seals, gaskets, O-rings, clutch friction discs, steel plates (if grooved), bands
        - Inspect hard parts: input/output shafts, planetary carriers, sun gears, ring gears, drums, cases
        - Selective fit: use correct thickness snap ring or shim to achieve specified clearance
        - Torque specifications: all fasteners to spec with proper thread locker where specified

        End play measurement:
        - Measures axial shaft movement within case
        - Too tight: bearings preloaded, early failure, hard shifting
        - Too loose: excessive axial movement, noise, potential clutch hub disengagement
        - Typical specification: 0.010-0.040 inches (varies by transmission)
        - Adjusted with selective thrust washers or shims

        Clutch pack clearance:
        - Measures total clearance between all friction and steel plates when released
        - Too tight: clutch drags when released, heat buildup, premature wear
        - Too loose: excessive apply time (slip), soft engagement, burnt clutches
        - Typical specification: 0.030-0.090 inches (varies by clutch pack)
        - Adjusted with selective snap ring or additional steel plate

        Hard part inspection:
        - Bushing wear: measure ID, compare to specification, replace if worn beyond limit
        - Spline wear: check for rounded edges, excessive play, replace if damaged
        - Drum cracks: magnaflux or dye penetrant test on high-stress areas (apply piston bore)
        - Bearing condition: rough rotation, pitting, discoloration = replace
        - Case porosity: check for cracks, stripped threads, repair or replace

        Assembly best practices:
        - Clean all parts thoroughly (solvent wash, air dry)
        - Pre-lube all friction surfaces with ATF
        - Install seals with proper seal installation tool (no damage to seal lip)
        - Air check all clutch packs (apply shop air to circuit, verify clutch applies)
        - Rotate components during assembly to verify smooth operation
        - Pressure test valve body circuits before installation
        """,
        key_factors=[
            "End play specification and measurement method",
            "Clutch pack clearance per pack (multiple packs in transmission)",
            "Bushing clearances (input shaft, output shaft, stator support)",
            "Torque converter inspection (hub, stator one-way clutch, lockup clutch)",
            "Valve body inspection (wear, cracks, bore scoring)",
            "Case inspection (porosity, cracks, thread damage)"
        ],
        primary_authority=[
            "OEM transmission overhaul manual and specifications",
            "ATSG rebuild procedures and clearance specifications",
            "Sonnax technical bulletins (upgrade parts and common failures)"
        ],
        burden_holder="Transmission rebuilder with experience and precision measurement tools",
        adversary_position="Low-quality rebuild with incorrect clearances or reused worn parts",
        counter_arguments=[
            "Incorrect clearances cause repeat failures - customer blames entire repair",
            "Reusing hard parts beyond service limit saves money short-term but causes early failure",
            "Skipping air checks or pressure tests allows assembly errors to go undetected",
            "Inadequate cleaning leaves debris that damages new clutches"
        ],
        resolution_strategy="Follow OEM or ATSG rebuild procedure step-by-step, measure all clearances and record on worksheet, replace all soft parts and worn hard parts, air check every clutch pack, pressure test valve body, verify torque converter condition, final end play check before case closure.",
        entity_scope=["All automatic transmissions requiring rebuild", "RWD and FWD transaxles", "4-speed through 10-speed designs"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.REBUILD_PROCEDURES
    ),

    DoctrineBlock(
        topic="Drivetrain NVH (Noise, Vibration, Harshness) Diagnosis",
        keywords=["NVH", "vibration", "driveline vibration", "U-joint", "CV joint", "driveshaft", "carrier bearing", "harmonics"],
        conclusion_template=[
            "Drivetrain vibration frequency correlates to component RPM - driveshaft vibration typically 3x-4x wheel speed vibration.",
            "U-joint wear causes vibration that intensifies with throttle application; CV joint wear causes clicking on turns and vibration when accelerating.",
            "Driveshaft phasing and balance critical - incorrect angle or out-of-balance shaft causes harmonic vibration at specific speeds."
        ],
        reasoning_framework="""
        Vibration frequency analysis:
        - Wheel/tire imbalance: 1x vehicle speed (1st order), felt in steering wheel
        - Driveshaft imbalance: 3-4x vehicle speed, felt in floor/seat
        - Engine/transmission imbalance: RPM-dependent, not speed-dependent
        - Exhaust contact: random, intermittent, often at specific engine load
        - Differential issue: constant whine or rhythmic clicking correlated to wheel speed

        U-joint diagnosis:
        - Clunk on throttle application or deceleration: worn U-joint with excessive play
        - Vibration that changes with throttle: U-joint binding (not worn but tight)
        - Test: grab driveshaft and attempt to rotate - excessive play indicates wear
        - Greased vs non-greased: non-greased (Spicer SPL) sealed for life, fail without warning
        - Phasing: U-joints on same driveshaft must be in-phase (yokes parallel) to avoid vibration

        CV joint diagnosis:
        - Clicking on turns: outer CV joint worn (balls worn, races pitted)
        - Vibration on acceleration: inner CV joint worn (tripod or plunge joint)
        - Torn boot: allows grease loss and contamination, accelerates wear
        - Clunk on engagement: excessive play in inner joint or axle spline

        Driveshaft angle and phasing:
        - Operating angle: 1-3 degrees ideal, >3 degrees causes U-joint wear
        - Pinion angle: must be within 1 degree of driveshaft angle for optimal life
        - Lift kits and lowering: change driveshaft angle, require correction (shims, adjustable control arms)
        - Two-piece driveshaft: front and rear sections must have equal and opposite angles at carrier bearing

        Carrier bearing failure:
        - Worn bearing: vibration at specific speed range (resonance of driveshaft)
        - Rubber mount deterioration: allows driveshaft to contact tunnel, causes vibration and noise
        - Test: listen for bearing noise during coast (no load), compare to acceleration

        Driveshaft balance:
        - Factory balanced as assembly (driveshaft + yokes + U-joints)
        - Replacing U-joint or yoke can shift balance
        - Balance weights: weld-on or hose-clamp type, positioned by balancing machine
        - High-speed balance required for 90+ mph capable vehicles
        """,
        key_factors=[
            "Vibration frequency relative to vehicle speed or engine RPM",
            "Change in vibration with throttle application (load)",
            "Noise on turns (CV joint) or straight line (U-joint, driveshaft)",
            "Visual inspection of boots, U-joints, and carrier bearing",
            "Driveshaft angle and pinion angle measurement",
            "Wheel speed vs driveshaft speed correlation"
        ],
        primary_authority=[
            "SAE J1937 - Driveshaft Balance Standards",
            "Spicer U-Joint Service Manual",
            "OEM driveline angle specifications"
        ],
        burden_holder="Technician diagnosing vibration complaint",
        adversary_position="Misdiagnosis as tire balance or alignment when driveline is cause",
        counter_arguments=[
            "Tire imbalance and driveshaft vibration can both cause vibration - difficult to isolate",
            "Exhaust contact can mimic driveline vibration - must inspect for clearance",
            "Transmission mount failure allows driveline angle change, causing vibration",
            "Customer may describe vibration at 'highway speed' without specific MPH - need exact speed for frequency calc"
        ],
        resolution_strategy="Test drive at various speeds and note exact speed of vibration, calculate frequency (RPM or Hz) and correlate to component, inspect U-joints for play and binding, check CV boots for tears, measure driveshaft angles, inspect carrier bearing for play or noise, balance driveshaft if no other cause found.",
        entity_scope=["RWD and AWD vehicles", "Truck and SUV driveshafts", "FWD CV axles", "Two-piece and single-piece driveshafts"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DRIVETRAIN_NVH
    ),

    DoctrineBlock(
        topic="Performance Transmission Tuning and Modifications",
        keywords=["performance", "shift kit", "valve body", "torque converter", "stall speed", "shift points", "transmission cooler", "line pressure"],
        conclusion_template=[
            "Shift kits modify valve body to increase line pressure and reduce shift time for firmer, faster shifts under performance driving.",
            "Higher stall speed torque converter allows engine to build boost (turbo) or reach power band before vehicle movement.",
            "Transmission cooler mandatory for towing and performance - ATF temp above 250°F rapidly degrades fluid and causes clutch failure."
        ],
        reasoning_framework="""
        Shift kit modifications:
        - Increase line pressure: stronger clutch clamping force, reduces slip during shift
        - Reduce shift time: faster clutch apply = less friction material wear during shift transition
        - Modify accumulator: reduce cushion for firmer shift feel (performance) or increase for smoother shift (towing)
        - Recalibrate valve springs: change shift points and shift firmness
        - Block off circuits: eliminate unwanted clutch overlap or slip

        Stall speed torque converter:
        - Stock stall: 1200-1800 RPM (allows idle creep, smooth launch)
        - Performance stall: 2200-3500 RPM (allows engine to build power before launch)
        - Too high stall: excessive heat generation, poor fuel economy, reduced low-speed drivability
        - Too low stall: bog on launch, can't build boost (turbo applications)
        - Stall speed testing: brake torque in drive, measure peak RPM before wheels break free (dangerous, brief test only)

        Torque converter selection:
        - Match stall to engine power band: peak torque RPM - 500 RPM = ideal stall
        - Turbo applications: higher stall to build boost pressure before launch
        - Naturally aspirated: moderate stall (2200-2600 RPM)
        - Lockup vs non-lockup: lockup for street (fuel economy), non-lockup for drag racing (shock absorption)

        Transmission cooling:
        - Factory cooler: adequate for normal driving, marginal for towing
        - Aftermarket cooler: plate-and-fin or tube-and-fin, 20,000+ BTU/hr capacity
        - Temp monitoring: 180-200°F normal, 220°F warning, 240°F+ damage zone
        - Cooler placement: in front of radiator (max airflow) or stacked (not as effective)
        - Thermostat: allows fluid to warm up quickly, bypasses cooler when cold

        Line pressure modification:
        - Factory pressure: 150-180 psi (balance between shift quality and clutch life)
        - Performance pressure: 200-250 psi (firmer shifts, better holding under power)
        - Boost-referenced pressure: increases line pressure with turbo boost (diesel and turbo gas applications)
        - Manual valve body: removes automatic shifting, driver controls all shifts (drag racing)

        Fluid and filter upgrades:
        - Synthetic ATF: better thermal stability, oxidation resistance
        - Deep pan: increases fluid capacity (2-4 quarts), improves cooling
        - High-flow filter: reduces restriction, maintains pressure under high flow demand
        """,
        key_factors=[
            "Stall speed matched to engine power band and application",
            "Shift kit calibration appropriate for use (street vs strip)",
            "Transmission cooler capacity and placement",
            "ATF temperature monitoring (gauge mandatory for performance/towing)",
            "Line pressure specification vs modified pressure",
            "Fluid capacity increase with deep pan or external reservoir"
        ],
        primary_authority=[
            "Transmission specialty companies (TCI, B&M, Hughes, Precision Industries)",
            "Shift kit installation instructions (TransGo, Superior, Sonnax)",
            "Dyno testing results and track performance data"
        ],
        burden_holder="Performance transmission builder or tuner",
        adversary_position="Stock transmission with performance modifications fails prematurely",
        counter_arguments=[
            "Excessive line pressure causes harsh shifts and can damage hard parts",
            "Too high stall speed hurts drivability and fuel economy on street",
            "Shift kit without cooler upgrade leads to overheating and failure",
            "Manual valve body eliminates all safety features (no park safety, no failsafe)"
        ],
        resolution_strategy="Match torque converter stall to engine dyno curve, install shift kit appropriate for application (street, towing, racing), add transmission cooler with thermostat, monitor ATF temp during use, adjust line pressure based on performance testing and shift quality.",
        entity_scope=["Performance cars and trucks", "Towing applications", "Drag racing and road racing", "Turbo and supercharged applications"],
        confidence=ConfidenceLevel.AGGRESSIVE,
        category=IssueCategory.PERFORMANCE_TUNING
    ),

    DoctrineBlock(
        topic="Final Drive Ratio Selection and Gear Ratio Calculations",
        keywords=["final drive", "gear ratio", "axle ratio", "differential ratio", "ring and pinion", "overall ratio", "RPM calculation"],
        conclusion_template=[
            "Final drive ratio (ring gear teeth ÷ pinion gear teeth) determines engine RPM at given vehicle speed and affects acceleration vs fuel economy.",
            "Numerically higher ratio (4.10 vs 3.55) provides better acceleration and towing but higher highway RPM and worse fuel economy.",
            "Overall ratio = transmission gear ratio × final drive ratio; affects wheel torque and vehicle performance characteristics."
        ],
        reasoning_framework="""
        Gear ratio fundamentals:
        - Final drive ratio: ring gear teeth / pinion gear teeth (example: 41/10 = 4.10:1)
        - Numerically higher: 4.10, 4.56, 5.13 (more torque multiplication, lower top speed)
        - Numerically lower: 3.08, 3.23, 3.55 (less torque, higher top speed, better fuel economy)
        - Common truck ratios: 3.55, 3.73, 4.10 (balanced for towing and highway)
        - Common performance car ratios: 3.73, 4.10, 4.56 (acceleration priority)

        Overall ratio calculation:
        - 1st gear overall = transmission 1st ratio × final drive
        - Example: 2.84 (1st gear) × 4.10 (axle) = 11.64:1 overall
        - Higher overall ratio = more wheel torque, better acceleration
        - Top gear overall: transmission OD ratio × final drive (lower number)
        - Example: 0.70 (OD) × 3.55 (axle) = 2.49:1 overall

        RPM calculation at speed:
        - RPM = (MPH × final drive ratio × transmission ratio × 336) / tire diameter (inches)
        - Example: 70 MPH, 3.73 axle, 0.70 OD, 30" tire = (70 × 3.73 × 0.70 × 336) / 30 = 2,043 RPM
        - Tire size change affects effective ratio: taller tire = lower effective ratio (acts like numerically lower axle)
        - 33" tire with 3.73 axle = effective 3.39 ratio compared to stock 30" tire

        Ratio selection criteria:
        - Towing heavy loads: numerically higher (4.10, 4.56) for torque multiplication
        - Highway cruising: numerically lower (3.08, 3.23) for lower RPM and better MPG
        - Performance/drag racing: numerically higher (4.10, 4.56+) for acceleration
        - Off-road: numerically higher (4.56, 5.13, 5.38) for crawl speed and torque
        - Large tires: numerically higher to compensate for tire size increase

        Matching transmission and axle ratios:
        - Wide ratio transmission (large gap between 1st and OD): can use numerically lower axle
        - Close ratio transmission (small gaps): may need numerically higher axle for launch
        - Example: 4L80E (2.48 1st, 0.75 OD) pairs well with 3.73 axle
        - Example: 4L60E (3.06 1st, 0.70 OD) may need 4.10 axle for similar performance

        Speedometer/odometer correction:
        - Changing axle ratio or tire size requires speedometer recalibration
        - Electronic: reprogram PCM/TCM with new ratio and tire size
        - Mechanical: change speedometer gear in transmission or transfer case
        - GPS speedometer: unaffected by drivetrain changes
        """,
        key_factors=[
            "Vehicle use case (towing, highway, off-road, performance)",
            "Tire size and weight (larger/heavier tires need numerically higher ratio)",
            "Engine torque curve (diesel and high-torque engines can use lower ratio)",
            "Transmission ratios (wide vs close ratio affects axle selection)",
            "Desired highway cruising RPM (lower RPM = better economy, less noise)",
            "Towing capacity and trailer weight"
        ],
        primary_authority=[
            "OEM axle ratio specifications and towing guides",
            "Gear ratio calculators and performance modeling tools",
            "Drivetrain engineering references (SAE papers)"
        ],
        burden_holder="Customer selecting axle ratio for truck order or enthusiast upgrading ring and pinion",
        adversary_position="Incorrect ratio selection causing poor performance or excessive fuel consumption",
        counter_arguments=[
            "Too high ratio causes excessive highway RPM, noise, and fuel consumption",
            "Too low ratio causes sluggish acceleration and poor towing performance",
            "Tire size change without ratio adjustment causes speedometer error and poor performance",
            "Automatic transmission shift points affected by ratio change - may need recalibration"
        ],
        resolution_strategy="Calculate current overall ratios (1st and OD), determine desired RPM at cruise speed, calculate required final drive ratio for target RPM, consider towing and acceleration needs, verify transmission ratios complement axle selection, plan for speedometer recalibration.",
        entity_scope=["Truck and SUV axle selection", "Performance car ring and pinion upgrades", "Off-road vehicles with large tires"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.PERFORMANCE_TUNING
    ),

    DoctrineBlock(
        topic="Fleet Transmission Maintenance and Predictive Monitoring",
        keywords=["fleet", "preventive maintenance", "fluid analysis", "telemetry", "transmission failure prediction", "downtime reduction", "TCO"],
        conclusion_template=[
            "Fleet transmission maintenance programs reduce total cost of ownership by preventing catastrophic failures through fluid analysis and telemetry.",
            "Predictive monitoring using CVI values, shift quality metrics, and temperature data identifies failing transmissions before roadside breakdown.",
            "Scheduled fluid service intervals based on duty cycle (severe vs normal) extend transmission life and reduce unscheduled repairs."
        ],
        reasoning_framework="""
        Fleet maintenance strategies:
        - Preventive: scheduled fluid changes, inspections at mileage intervals
        - Predictive: monitor telemetry data, fluid analysis, identify failures before occurrence
        - Reactive: repair after failure (highest cost, most downtime)
        - Proactive: design vehicle spec for duty cycle (correct ratio, cooler, etc.)

        Fluid analysis program:
        - Sample interval: every 25-50k miles for severe duty, 50-100k for normal duty
        - Metal trends: increasing copper/iron indicates wear acceleration
        - Viscosity change: indicates oxidation or fuel dilution
        - Particle count: ISO cleanliness code, higher count = contamination
        - Predictive window: 10-30k miles of warning before failure (catch bearing wear before it damages gears)

        Telemetry monitoring (heavy trucks with J1939 or telematics):
        - Clutch Volume Index (CVI): track over time, approaching limit = schedule replacement
        - Transmission temperature: repeated high temp events indicate cooler inadequacy or abuse
        - Shift quality metrics: harsh shift count, slip events, failed shift attempts
        - Fault code history: recurring codes indicate systemic issue
        - Idle time and PTO usage: high idle affects transmission fluid life

        Duty cycle classification:
        - Severe: towing, frequent stop-and-go, high ambient temp, dusty environment, PTO use
        - Normal: highway cruising, minimal towing, moderate climate
        - Severe duty requires 50% reduction in service intervals

        Scheduled service intervals:
        - Normal duty: 60-100k miles for fluid/filter
        - Severe duty: 30-50k miles for fluid/filter
        - CVT: 30-60k miles (critical, shorter interval than automatic)
        - DCT wet clutch: 40-60k miles
        - Transfer case: 50-75k miles
        - Differential: 50-100k miles (gear oil)

        Failure cost analysis:
        - Preventive fluid service: $200-400 per vehicle
        - Roadside transmission failure: $500 tow + $2,000-5,000 repair + 3-7 days downtime
        - Fleet downtime cost: $500-1,500 per day (lost revenue)
        - Total cost of ownership (TCO): preventive maintenance reduces TCO by 20-40%

        Fleet specification best practices:
        - Specify transmission for worst-case duty (max GCWR, max grade)
        - Order transmission cooler upgrade (especially for towing fleets)
        - Specify correct axle ratio for loaded weight and route profile
        - Implement driver training program (reduce abuse, extend component life)
        """,
        key_factors=[
            "Duty cycle classification and service interval adjustment",
            "Fluid analysis trending (not one-time snapshot)",
            "Telemetry data capture and analysis capability",
            "Driver behavior monitoring and training",
            "Vehicle specification matched to duty cycle",
            "Total cost of ownership calculation (preventive vs reactive)"
        ],
        primary_authority=[
            "OEM fleet maintenance guides",
            "TMC (Technology & Maintenance Council) Recommended Practices",
            "ASTM D7450 - Fluid Analysis for Automatic Transmissions",
            "Fleet management software providers (Fleetio, Samsara, Geotab)"
        ],
        burden_holder="Fleet manager balancing maintenance cost vs downtime risk",
        adversary_position="Deferred maintenance to reduce short-term costs, increasing long-term failures",
        counter_arguments=[
            "Preventive maintenance cost is visible and immediate, failure cost is future and uncertain",
            "Pressure to extend intervals to save money in short term",
            "Driver abuse hard to detect without telemetry, may be blamed on vehicle spec",
            "Fluid analysis cost ($30-50 per sample) vs benefit requires long-term tracking to prove ROI"
        ],
        resolution_strategy="Implement fluid analysis program with trending, install telematics to monitor transmission health, classify vehicles by duty cycle and adjust service intervals, specify vehicles correctly for duty cycle, track total cost of ownership (preventive vs reactive repair costs).",
        entity_scope=["Commercial truck fleets", "Delivery van fleets", "Municipal vehicle fleets", "Rental car fleets"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DIAGNOSTICS
    ),

    DoctrineBlock(
        topic="Transmission Temperature Management and Cooling Systems",
        keywords=["transmission temperature", "ATF temp", "cooler", "overheating", "towing", "temp sensor", "thermal management"],
        conclusion_template=[
            "Transmission fluid operating temperature should remain 180-220°F; temps above 240°F cause rapid fluid degradation and clutch failure.",
            "Factory coolers adequate for normal driving but marginal for towing - aftermarket cooler mandatory for heavy towing or performance use.",
            "Temp sensor and gauge essential for early detection of cooling system failure before catastrophic transmission damage."
        ],
        reasoning_framework="""
        ATF temperature effects:
        - 180-200°F: optimal operating range, fluid viscosity correct, good clutch friction
        - 220-240°F: elevated but acceptable for brief periods (climbing grade while towing)
        - 240-260°F: fluid life reduced by 50%, clutch material begins to glaze
        - 260-280°F: fluid life reduced by 75%, seals begin to fail, varnish formation accelerates
        - 280°F+: catastrophic damage zone, clutches slip and burn, fluid breaks down rapidly

        Heat generation sources:
        - Torque converter slip: largest heat source (2-5% slip = significant heat)
        - Clutch pack friction during shifts: each shift generates heat pulse
        - Hydraulic pump friction: constant parasitic load
        - Towing uphill: converter slip + high load = maximum heat generation
        - Stop-and-go driving: frequent shifts, limited airflow over cooler

        Cooling system design:
        - In-radiator cooler: transmission lines to heat exchanger inside radiator tank
        - Advantage: quick warm-up, integrated packaging
        - Disadvantage: limited capacity, shared cooling with engine, cooler failure can cross-contaminate ATF and coolant
        - External cooler: dedicated transmission cooler in front of radiator
        - Plate-and-fin design: higher capacity, better for towing and performance
        - Tube-and-fin design: cheaper, adequate for light duty
        - Stacked coolers: external cooler + in-radiator cooler in series for maximum capacity

        Cooler sizing:
        - Light duty (no towing): 10,000-15,000 BTU/hr
        - Medium duty (occasional towing): 15,000-20,000 BTU/hr
        - Heavy duty (frequent towing, large trailers): 25,000-40,000 BTU/hr
        - GVW and GCWR affect sizing: heavier loads need more capacity

        Thermostat operation:
        - Allows fluid to warm up quickly to operating temp (important for clutch friction and efficiency)
        - Bypasses cooler when fluid below 180°F
        - Opens to route fluid through cooler when above 180°F
        - Prevents overcooling in winter (fluid too cold = harsh shifts)

        Temperature monitoring:
        - Factory temp sensor (if equipped): scan tool can display ATF temp
        - Aftermarket gauge: capillary tube sensor in cooler line, analog or digital readout
        - Installation location: cooler return line (after cooler, before transmission)
        - Warning threshold: 240°F = reduce load or stop, 260°F = stop immediately

        Cooling system failures:
        - Radiator cooler failure: ATF and coolant mix, milky fluid, transmission and cooling system both contaminated
        - External cooler leak: ATF drips from cooler, low fluid level, overheating
        - Restricted cooler: corrosion, debris, reduces flow and cooling capacity
        - Thermostat stuck closed: prevents cooling, fluid overheats
        - Thermostat stuck open: overcooling, harsh shifts when cold
        """,
        key_factors=[
            "ATF temperature during towing or high-load operation",
            "Cooler capacity matched to vehicle duty cycle (GVW, GCWR)",
            "Thermostat operation and opening temperature",
            "Cooler line routing and potential for damage/restriction",
            "Radiator cooler integrity (check for coolant in ATF or ATF in coolant)",
            "Airflow to external cooler (blockage by debris reduces cooling)"
        ],
        primary_authority=[
            "OEM towing guides and transmission temperature specifications",
            "Aftermarket cooler manufacturers (B&M, Hayden, Derale) capacity charts",
            "SAE J2807 - Towing Ratings and Performance Standards"
        ],
        burden_holder="Technician diagnosing overheating or vehicle owner towing heavy loads",
        adversary_position="Misdiagnosis as transmission internal failure when cooling system is inadequate",
        counter_arguments=[
            "Overheating damage can mimic clutch wear, slipping, or pressure issues",
            "Intermittent overheating (only while towing) hard to diagnose if not monitored",
            "Factory cooler adequate for light use but fails under towing load - not obvious from vehicle spec",
            "Coolant contamination of ATF requires complete transmission flush and rebuild"
        ],
        resolution_strategy="Install aftermarket temp gauge to monitor during towing, verify cooler capacity for towing duty, inspect cooler and lines for leaks/restrictions, check for coolant contamination (milky fluid), consider external cooler upgrade for heavy towing, install thermostat if not equipped.",
        entity_scope=["Towing applications", "Performance vehicles", "Commercial trucks", "RVs and heavy trailers"],
        confidence=ConfidenceLevel.DEFENSIBLE,
        category=IssueCategory.DIAGNOSTICS
    )
]


# ═══════════════════════════════════════════════════════════════════════════
# TELEMETRY & COVERAGE TRACKING
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryCollector:
    def __init__(self):
        self.query_count = 0
        self.doctrine_triggers: Dict[str, int] = {}
        self.category_distribution: Dict[str, int] = {}
        self.response_times: List[float] = []

    def record_query(self, triggered_topics: List[str], categories: List[IssueCategory], response_time: float):
        self.query_count += 1
        self.response_times.append(response_time)

        for topic in triggered_topics:
            self.doctrine_triggers[topic] = self.doctrine_triggers.get(topic, 0) + 1

        for category in categories:
            cat_str = category.value
            self.category_distribution[cat_str] = self.category_distribution.get(cat_str, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        return {
            "total_queries": self.query_count,
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "doctrine_triggers": self.doctrine_triggers,
            "category_distribution": self.category_distribution,
            "total_doctrines": len(DOCTRINE_CACHE)
        }


TELEMETRY = TelemetryCollector()


# ═══════════════════════════════════════════════════════════════════════════
# CORE ENGINE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def match_doctrines(query: str, category_hint: Optional[IssueCategory] = None) -> List[DoctrineBlock]:
    """Match query against doctrine cache using keyword matching."""
    query_lower = query.lower()
    matched = []

    for doctrine in DOCTRINE_CACHE:
        if category_hint and doctrine.category != category_hint:
            continue

        keyword_match = any(kw.lower() in query_lower for kw in doctrine.keywords)
        topic_match = doctrine.topic.lower() in query_lower

        if keyword_match or topic_match:
            matched.append(doctrine)

    return matched[:5]  # Top 5 matches


def generate_response(query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
    """Generate response based on mode and matched doctrines."""
    if not doctrines:
        return "No specific transmission system doctrine matched. Please provide more details about the transmission type, symptoms, or specific component."

    if mode == ResponseMode.FAST:
        # Concise response with key conclusions
        primary = doctrines[0]
        response = f"**{primary.topic}**\n\n"
        response += "\n".join(f"• {conclusion}" for conclusion in primary.conclusion_template)

        if len(doctrines) > 1:
            response += "\n\n**Related considerations:**\n"
            response += "\n".join(f"• {d.topic}" for d in doctrines[1:3])

        return response

    elif mode == ResponseMode.DEFENSE:
        # Comprehensive analysis with reasoning
        response = f"**TRANSMISSION SYSTEMS ANALYSIS**\n\n"
        response += f"**Query:** {query}\n\n"

        for i, doctrine in enumerate(doctrines[:3], 1):
            response += f"**{i}. {doctrine.topic}**\n\n"
            response += "**Conclusions:**\n"
            response += "\n".join(f"• {conclusion}" for conclusion in doctrine.conclusion_template)
            response += "\n\n**Key Factors:**\n"
            response += "\n".join(f"• {factor}" for factor in doctrine.key_factors[:5])
            response += "\n\n**Diagnostic Strategy:**\n"
            response += doctrine.resolution_strategy
            response += f"\n\n**Confidence Level:** {doctrine.confidence.value}\n\n"
            response += "---\n\n"

        return response.strip()

    else:  # MEMO mode
        # Full technical memorandum
        primary = doctrines[0]
        response = f"**TECHNICAL MEMORANDUM: {primary.topic.upper()}**\n\n"
        response += f"**Subject:** {query}\n"
        response += f"**Category:** {primary.category.value}\n"
        response += f"**Confidence Level:** {primary.confidence.value}\n\n"

        response += "**EXECUTIVE SUMMARY**\n\n"
        response += "\n".join(f"{i}. {conclusion}" for i, conclusion in enumerate(primary.conclusion_template, 1))

        response += "\n\n**TECHNICAL ANALYSIS**\n\n"
        response += primary.reasoning_framework

        response += "\n\n**KEY FACTORS**\n\n"
        response += "\n".join(f"• {factor}" for factor in primary.key_factors)

        response += "\n\n**DIAGNOSTIC RESOLUTION STRATEGY**\n\n"
        response += primary.resolution_strategy

        response += "\n\n**PRIMARY AUTHORITY**\n\n"
        response += "\n".join(f"• {auth}" for auth in primary.primary_authority)

        response += f"\n\n**BURDEN HOLDER:** {primary.burden_holder}\n"
        response += f"\n**ADVERSARY POSITION:** {primary.adversary_position}\n"

        response += "\n\n**COUNTER-ARGUMENTS**\n\n"
        response += "\n".join(f"• {arg}" for arg in primary.counter_arguments)

        if len(doctrines) > 1:
            response += "\n\n**RELATED DOCTRINES**\n\n"
            for doctrine in doctrines[1:]:
                response += f"• **{doctrine.topic}** ({doctrine.category.value})\n"

        return response


def compute_determinism_hash(query: str, doctrines: List[DoctrineBlock], mode: ResponseMode) -> str:
    """Generate SHA-256 hash for determinism verification."""
    content = f"{query}|{mode.value}|"
    content += "|".join(d.topic for d in doctrines)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@APP.get("/health")
async def health_check():
    """Health check endpoint with system metrics."""
    return {
        "status": "operational",
        "engine": "AUTO02_transmission_systems",
        "version": "1.0.0",
        "port": 9062,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "categories": [cat.value for cat in IssueCategory],
        "telemetry": TELEMETRY.get_metrics()
    }


@APP.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint for transmission systems analysis."""
    start_time = datetime.now()

    logger.info(f"Query received: {request.query[:100]}... | Mode: {request.mode.value}")

    # Match doctrines
    matched_doctrines = match_doctrines(request.query, request.category_hint)

    if not matched_doctrines:
        logger.warning(f"No doctrines matched for query: {request.query[:50]}")

    # Generate response
    response_text = generate_response(request.query, matched_doctrines, request.mode)

    # Extract metadata
    triggered_topics = [d.topic for d in matched_doctrines]
    categories = list(set(d.category for d in matched_doctrines))
    confidence = matched_doctrines[0].confidence if matched_doctrines else ConfidenceLevel.DISCLOSURE

    # Build reasoning chain
    reasoning_chain = []
    for doctrine in matched_doctrines[:3]:
        reasoning_chain.append(f"{doctrine.topic}: {doctrine.resolution_strategy[:100]}...")

    # Compute hash
    det_hash = compute_determinism_hash(request.query, matched_doctrines, request.mode)

    # Calculate response time
    response_time = (datetime.now() - start_time).total_seconds()

    # Record telemetry
    TELEMETRY.record_query(triggered_topics, categories, response_time)

    # Build telemetry
    telemetry = {
        "response_time_ms": round(response_time * 1000, 2),
        "doctrines_matched": len(matched_doctrines),
        "timestamp": datetime.now().isoformat()
    }

    logger.info(f"Query processed in {response_time*1000:.2f}ms | Doctrines: {len(matched_doctrines)}")

    return QueryResponse(
        query=request.query,
        mode=request.mode,
        response=response_text,
        doctrine_blocks_triggered=triggered_topics,
        confidence=confidence,
        categories=categories,
        reasoning_chain=reasoning_chain,
        determinism_hash=det_hash,
        telemetry=telemetry
    )


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("AUTO02 TRANSMISSION SYSTEMS ENGINE STARTING")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")
    logger.info(f"Categories: {len(IssueCategory)}")
    logger.info(f"Port: 9062")
    logger.info("=" * 80)

    uvicorn.run(APP, host="127.0.0.1", port=9062, log_level="info")
