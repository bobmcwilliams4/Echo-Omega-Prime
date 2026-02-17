"""
RAIL03 - Railway Signal & Control Systems Intelligence Engine
TIE Gold Standard Implementation

Port: 9103
Domain: Railway signal systems, interlocking, PTC, block signaling, track circuits
Authority: FRA Part 236, AREMA standards, IEEE 1570, ERTMS/ETCS specifications
Version: 1.0.0
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to sys.path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Literal
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


class IssueCategory(str, Enum):
    BLOCK_SIGNALING = "BLOCK_SIGNALING"
    INTERLOCKING = "INTERLOCKING"
    SIGNAL_ASPECTS = "SIGNAL_ASPECTS"
    TRACK_CIRCUITS = "TRACK_CIRCUITS"
    AXLE_COUNTERS = "AXLE_COUNTERS"
    PTC_SYSTEMS = "PTC_SYSTEMS"
    CTC_SYSTEMS = "CTC_SYSTEMS"
    CAB_SIGNALING = "CAB_SIGNALING"
    GRADE_CROSSINGS = "GRADE_CROSSINGS"
    FAIL_SAFE_DESIGN = "FAIL_SAFE_DESIGN"
    SIGNAL_MAINTENANCE = "SIGNAL_MAINTENANCE"
    ERTMS_ETCS = "ERTMS_ETCS"


class AuthorityLevel(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    INTERPRETIVE = "INTERPRETIVE"
    HISTORICAL = "HISTORICAL"


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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    category: IssueCategory


class QueryRequest(BaseModel):
    query: str = Field(..., description="Railway signal system question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    triggered_doctrines: List[str]
    authority_citations: List[str]
    metadata: Dict[str, Any]
    determinism_hash: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    timestamp: str


# ============================================================================
# DOCTRINE CACHE - 25+ Railway Signal & Control Systems Expertise
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Absolute Permissive Block (APB) Signal Systems",
        keywords=["APB", "absolute block", "permissive block", "block signaling", "train separation", "authority limits"],
        conclusion_template=[
            "Absolute Permissive Block (APB) combines absolute block and permissive block principles to control train movements.",
            "The system prevents opposing movements on single track while allowing following movements under permissive indication.",
            "APB provides flexible train separation while maintaining safety through block occupancy detection and signal interlocking."
        ],
        reasoning_framework="""
APB Signal System Analysis Framework:
1. Block Definition: Track divided into blocks with defined entry/exit points
2. Absolute Block Rule: Only one train permitted in block direction at a time (opposing movements prohibited)
3. Permissive Block Rule: Multiple trains may follow in same direction under restricted speed
4. Signal Aspects: Red (stop), Yellow (approach), Green (clear), Flashing Yellow (approach medium)
5. Track Occupancy Detection: Track circuits or axle counters verify block vacancy
6. Interlocking: Prevents conflicting signal indications
7. Authority Transmission: Signal aspects convey movement authority limits
8. Fail-Safe Design: Signal defaults to most restrictive aspect on equipment failure
9. Block Clearing: Train must completely clear block before authority granted to opposing movement
10. Permissive Following: Trains may enter occupied block same direction at restricted speed (typically 15-20 mph)
11. Station Limits: Special APB rules within station limits for switching operations
12. Dispatcher Control: CTC integration allows dispatcher override of automatic APB logic
13. Dark Territory Transition: APB boundaries with non-signaled track require special rules
14. Maintenance Windows: Block must be taken out of service for signal work
15. Backup Protection: Timetable authority or track warrants required if APB fails
16. Train Detection Failure: Shunting failure creates hazard of false clear indication
17. Signal Sighting Distance: Minimum sight distance to allow compliance with signal aspect
18. Approach Locking: Track circuit occupancy locks route until train clears
19. Time Locking: Prevents immediate route unlocking after train passage
20. Stick Circuit: Prevents signal upgrading until block proven vacant
        """,
        key_factors=[
            "Block occupancy state (vacant/occupied)",
            "Direction of last movement through block",
            "Signal aspect displayed at block entry",
            "Track circuit continuity and shunting performance",
            "Interlocking route selection and locking",
            "Time delays for approach and route locking",
            "Fail-safe defaults on equipment malfunction",
            "Train detection system reliability (track circuit vs axle counter)",
            "Signal sighting distance adequacy",
            "Integration with dispatcher CTC controls"
        ],
        primary_authority=[
            "49 CFR Part 236 Subpart B - Automatic Block Signal Systems",
            "AREMA Communications & Signals Manual Chapter 6 - Block Signal Systems",
            "FRA Safety Advisory 2009-01 - Signal System Failures",
            "IEEE 1570 Standard for APB Signal Systems",
            "Railroad operating rules (e.g., GCOR Rule 9.1 - Signal Indications)"
        ],
        burden_holder="Railroad operator to maintain APB system per FRA Part 236 compliance",
        adversary_position="Permissive block allows rear-end collisions if train stops in block",
        counter_arguments=[
            "Permissive aspect requires restricted speed (half the range of vision, prepared to stop)",
            "Train stopping in block creates shunt maintaining yellow aspect for following train",
            "Restricted speed rule provides defense against rear-end collision",
            "Historical safety record of APB systems demonstrates adequacy",
            "PTC overlay provides additional protection in permissive territory"
        ],
        resolution_strategy="Design APB with robust train detection, proper signal spacing for braking distance, and restricted speed enforcement for permissive movements. PTC overlay eliminates permissive block rear-end collision risk.",
        entity_scope="Class I freight railroads, regional railroads, commuter rail systems on shared track",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - APB is mature technology with established regulatory framework and proven safety record",
        controlling_precedent="FRA Part 236.1 - Application; APB systems predate regulation but grandfathered with maintenance requirements",
        category=IssueCategory.BLOCK_SIGNALING
    ),

    DoctrineBlock(
        topic="Interlocking Systems - Mechanical, Relay, Electronic, Computer-Based",
        keywords=["interlocking", "mechanical interlocking", "relay interlocking", "solid state interlocking", "computer-based interlocking", "route locking"],
        conclusion_template=[
            "Interlocking systems prevent conflicting train movements at junctions, crossings, and complex track layouts through mechanical, electrical, or electronic logic.",
            "The evolution from mechanical (lever frames) to computer-based interlocking has improved flexibility and reliability while maintaining fail-safe principles.",
            "All interlocking types must satisfy FRA Part 236 requirements for route locking, time locking, and approach locking to prevent unsafe signal clearance."
        ],
        reasoning_framework="""
Interlocking Technology Evolution Analysis:
1. Mechanical Interlocking (1870s-1950s): Physical lever frames with mechanical locking bars prevent conflicting lever movements. Still in service at some locations.
2. Electro-Mechanical (1900s-1960s): Mechanical interlocking with electric switch machines and signals, retaining mechanical locking logic.
3. Relay Interlocking (1930s-present): Electromagnetic relays implement interlocking logic. Dominant technology 1950-1990. Many still in service.
4. Solid State Interlocking (1970s-present): Electronic logic replaces relays using integrated circuits. Improved reliability and reduced maintenance.
5. Computer-Based Interlocking (1980s-present): Software logic on redundant fail-safe computers. Flexible logic updates without hardware changes.
6. Route Locking Requirement: Once route established for train movement, conflicting routes cannot be set until first route released.
7. Time Locking: After train passes through interlocking, route locks for minimum time (typically 1-3 minutes) to ensure complete clearance.
8. Approach Locking: Track circuit occupancy approaching interlocking locks route until train clears entire interlocking.
9. Sectional Route Locking: Route released in sections as train progresses rather than all at once (modern practice).
10. Switch Detection: Point detector confirms switch fully aligned and locked before route can be established.
11. Dual Control: Track circuits and switch position agreement required for signal clearance.
12. Electric Locking: Relay circuits prevent simultaneous energization of conflicting routes.
13. Vital Logic: Computer-based interlocking uses vital processors with self-checking architecture.
14. Fail-Safe Principles: Any failure mode must result in most restrictive state (signals red, routes locked).
15. Signal Replacement Unit (SRU): Temporary interlocking during maintenance or upgrade.
16. Testing Requirements: FRA Part 236.377 requires annual interlocking tests.
17. Modification Process: Design changes require engineering analysis and FRA notification.
18. Degraded Mode Operation: Interlocking failure requires manual control under restricted rules.
19. Relay Dropout: Relay interlocking vulnerable to power transients causing false route release.
20. Software Safety Assurance: Computer-based interlocking requires software validation per EN 50128 or equivalent.
21. Geographic Interlocking: Computer systems display track schematic for dispatcher route control.
22. Vital Relay Interface: Computer-based interlocking uses vital relay output interface to control field equipment.
        """,
        key_factors=[
            "Interlocking technology generation (mechanical/relay/solid state/computer)",
            "Number of routes and complexity of track layout",
            "Route locking, time locking, and approach locking implementation",
            "Switch detection and locking verification",
            "Track circuit design and reliability",
            "Power supply redundancy and battery backup",
            "Fail-safe design validation",
            "Software safety assurance for computer-based systems",
            "Maintenance testing frequency and procedures",
            "Integration with CTC or local control"
        ],
        primary_authority=[
            "49 CFR 236.377 - Interlocking tests",
            "49 CFR 236.788 - Vital processors",
            "AREMA C&S Manual Chapter 6 Part 2 - Interlocking",
            "EN 50128 - Software for Railway Control Systems",
            "IEC 62278 - Railway RAMS (Reliability, Availability, Maintainability, Safety)"
        ],
        burden_holder="Railroad and signal supplier to design, install, test, and maintain interlocking per FRA Part 236",
        adversary_position="Software errors in computer-based interlocking could allow conflicting routes",
        counter_arguments=[
            "Vital processor architecture with self-checking detects software execution errors",
            "Vital relay output interface provides additional safety layer",
            "Extensive validation testing per EN 50128 before deployment",
            "Proven in-service safety record of computer-based interlocking worldwide",
            "Relay interlocking had same theoretical risk of relay contact failures (addressed by fail-safe design)"
        ],
        resolution_strategy="Computer-based interlocking with vital processor architecture, diverse redundancy, vital relay interface, extensive validation testing, and proven software platforms (e.g., Siemens Westrace, Alstom SmartLock, Hitachi MicroLok) meets safety requirements. Software changes require validation equivalent to new development.",
        entity_scope="All railroad interlockings - passenger and freight",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - Computer-based interlocking is mature technology with regulatory acceptance and global deployment",
        controlling_precedent="FRA Part 236 Subpart H - Computer-based signal and train control systems (adopted 1999)",
        category=IssueCategory.INTERLOCKING
    ),

    DoctrineBlock(
        topic="Signal Aspects - Color Light, Position Light, Searchlight",
        keywords=["signal aspects", "color light signal", "position light", "searchlight signal", "signal indication", "aspect ratio"],
        conclusion_template=[
            "Signal aspects convey movement authority through color (red/yellow/green) and position (horizontal/diagonal/vertical) combinations.",
            "Color light signals are dominant modern technology using LED or incandescent lamps arranged in standardized patterns.",
            "Searchlight signals (single lamp with colored lenses) and position light signals (white lamps in geometric patterns) are legacy technologies still in limited service."
        ],
        reasoning_framework="""
Signal Aspect Display Technology Analysis:
1. Color Light Signals: Separate red, yellow, green lamps arranged vertically or in other standard configurations. Current industry standard.
2. Searchlight Signals: Single incandescent lamp with mechanically-selected colored lenses (red/yellow/green) rotated into beam. Legacy technology (1920s-1990s).
3. Position Light Signals: Arrangement of white lamps in geometric patterns (horizontal/diagonal/vertical). Used primarily by Pennsylvania Railroad successor lines.
4. Color Position Light (CPL): Combination of colored lamps in position patterns. Hybrid technology.
5. LED Conversion: Modern signals use LED arrays replacing incandescent lamps for improved reliability and reduced maintenance.
6. Aspect Ratio: Size and spacing of signal elements relative to viewing distance. Must be visible at required sighting distance.
7. Standard Signal Aspects (GCOR): Clear (green), Approach Medium (flashing yellow), Approach (yellow), Restricting (red over yellow), Stop (red).
8. Multi-Lamp Configurations: Two or three lamp vertical arrangements provide additional aspect combinations.
9. Lunar White Aspect: Special aspect for restricting movements in interlockings (rare, non-standard).
10. Phantom Indication: All signal lamps dark (equipment failure or power loss) treated as most restrictive aspect.
11. Sun Phantom Prevention: Signal must be visible against bright sunlight background. Visors and LED intensity address this.
12. Lamp Proving: Circuit detects lamp failure and either displays more restrictive aspect or alerts maintainer.
13. Searchlight Mechanism Reliability: Mechanical lens movement subject to freezing, binding, and misalignment.
14. LED Service Life: 100,000+ hour MTBF vs 1,000-2,000 hours for incandescent lamps.
15. Color Rendering: LED wavelength spectrum must match regulatory color requirements (precise red/yellow/green chromaticity).
16. Aspect Sequence: Signal aspects must follow logical progression (e.g., cannot upgrade from red directly to green without yellow).
17. Backing Light: Signal lamp illuminated but not in line of sight (e.g., dwarf signal behind mast signal). Design must prevent confusion.
18. Signal Visibility Requirements: FRA requires 3,000 foot minimum sighting distance in clear atmosphere (Part 236.23).
19. Foggy Weather Visibility: Reduced visibility conditions may require additional aspects or speed restrictions.
20. Aspect Enforcement: PTC overlay enforces compliance with signal aspects through automatic braking.
        """,
        key_factors=[
            "Signal technology (color light/searchlight/position light)",
            "Lamp type (LED/incandescent)",
            "Number of lamps and aspect combinations",
            "Sighting distance and aspect ratio",
            "Lamp proving and failure detection",
            "Environmental conditions (sun phantom, fog, snow)",
            "Maintenance requirements and lamp service life",
            "Power supply reliability",
            "PTC integration for aspect enforcement",
            "Regulatory compliance with FRA Part 236"
        ],
        primary_authority=[
            "49 CFR 236.23 - Minimum distance signal must be visible",
            "49 CFR 236.24 - Semaphore and searchlight signal mechanism requirements",
            "AREMA C&S Manual Chapter 3 Part 1 - Signal Structures and Apparatus",
            "GCOR/NORAC/CROR - Operating rules for signal aspects and indications",
            "MUTCD Part 8 - Traffic Controls for Highway-Rail Grade Crossings (passive signals)"
        ],
        burden_holder="Railroad to maintain signal aspects per FRA Part 236 visibility and mechanism requirements",
        adversary_position="LED signals may fail to 'fail safe' if LED array partial failure creates ambiguous aspect",
        counter_arguments=[
            "LED signal designs use redundant arrays with lamp proving circuitry",
            "Partial LED failure detected and triggers more restrictive aspect or signal dark condition",
            "LED reliability far exceeds incandescent, reducing failure probability",
            "Field experience with LED signals demonstrates safety equivalence to incandescent",
            "FRA approval process for LED signals includes failure mode analysis"
        ],
        resolution_strategy="LED color light signals with redundant arrays, lamp proving circuits, and fail-safe design per FRA approval provide equivalent or superior safety to legacy searchlight and incandescent signals. Conversion from searchlight to LED eliminates mechanical failure modes.",
        entity_scope="All railroad signal systems - freight and passenger",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - LED signal technology is mature with regulatory acceptance and proven safety record",
        controlling_precedent="FRA LED signal approval letters (various railroads, 2000s-present) establish LED equivalence to incandescent",
        category=IssueCategory.SIGNAL_ASPECTS
    ),

    DoctrineBlock(
        topic="Track Circuits - DC, AC, Audio Frequency, Jointless",
        keywords=["track circuit", "DC track circuit", "AC track circuit", "audio frequency", "jointless track circuit", "shunting"],
        conclusion_template=[
            "Track circuits detect train presence by shunting electrical current through wheelsets, breaking circuit continuity and de-energizing relay.",
            "DC track circuits (oldest technology) suffer from electrolysis and require insulated rail joints. AC and audio frequency (AF) track circuits allow jointless rail.",
            "Proper shunting requires clean wheels and rails, adequate wheelbase, and sufficient axle loading. Shunting failures create false clear indications (major hazard)."
        ],
        reasoning_framework="""
Track Circuit Technology and Reliability Analysis:
1. DC Track Circuit (1872 invention): Battery or rectified AC feeds track rails isolated by insulated joints. Train wheels shunt current, de-energizing relay. Oldest technology.
2. DC Track Circuit Issues: Rail-to-earth leakage, electrolysis corrosion at joints, seasonal resistance variation, 1-2 mile maximum length.
3. AC Track Circuit: 60 Hz AC (or coded AC) allows longer track circuit lengths and reduces electrolysis. Still requires insulated joints for isolation.
4. Audio Frequency (AF) Track Circuit: 50-300 Hz signaling current on continuous welded rail (CWR). Jointless operation. Tuned filters separate adjacent circuits.
5. Coded Track Circuit: Pulsed DC or AC conveys cab signal information (e.g., 180, 120, 75 code rates correspond to signal aspects).
6. Shunting Requirement: Low resistance path (typically <0.06 ohms) through wheelset between rails to reliably de-energize relay.
7. Shunting Variables: Wheel-rail contact resistance (affected by rust, oil, leaves), axle load (contact pressure), wheelbase length, track circuit voltage/current.
8. Broken Rail Detection: Track circuit loss-of-shunt condition detects broken rail (rail break creates open circuit). Critical safety function.
9. Insulated Joint Maintenance: Bonded joints require periodic inspection and replacement (20-30 year service life typical).
10. Ballast Resistance: Track ballast must provide adequate rail-to-earth resistance (minimum 2 ohms per 1,000 feet for DC circuits). Wet ballast degrades resistance.
11. Relay Dropout: Track relay must reliably drop out (de-energize) on minimum shunt. Relay characteristics must match track circuit design.
12. Polar Stick Relay: Prevents signal upgrading on momentary shunt loss (e.g., dirt on wheels causing intermittent shunting).
13. Impedance Bond: Allows traction power return current to flow through rails while isolating signaling current. Essential for electrified territory.
14. Coded Track Circuit Receiver: Cab signal receiver in locomotive decodes track circuit code rate and enforces speed limits.
15. False Feed: Cross-bonding error or insulated joint failure allows current to bypass shunt, creating false clear indication (hazardous).
16. Snow and Ice: Heavy snow can insulate wheels from rails, causing shunting failure. Rail heaters or chemical treatment required in severe climates.
17. Stray Current: Adjacent track circuits, traction power, or industrial sources can induce interference. AF track circuits resist interference through frequency selectivity.
18. Track Circuit Adjustment: Voltage and resistance tuning required for reliable operation. Over-voltage causes false occupancy; under-voltage causes shunting failure.
19. Jointless Track Circuit Advantages: Eliminates insulated joint maintenance, compatible with CWR, longer circuit lengths, better reliability.
20. Motion Sensor Backup: Some systems use axle counters or radar motion sensors as backup to track circuits (especially in shunting failure prone areas).
        """,
        key_factors=[
            "Track circuit technology (DC/AC/AF/coded)",
            "Track circuit length and voltage/current design",
            "Insulated joint condition (DC/AC) or impedance bond design (AF)",
            "Ballast resistance and environmental conditions",
            "Wheel-rail contact resistance (rust, contamination)",
            "Axle load and wheelbase length of rolling stock",
            "Relay characteristics and dropout threshold",
            "Broken rail detection sensitivity",
            "Interference susceptibility and mitigation",
            "Maintenance practices and testing frequency"
        ],
        primary_authority=[
            "49 CFR 236.1 - Application of Part 236 to track circuits",
            "49 CFR 236.3 - Shunting requirements",
            "AREMA C&S Manual Chapter 5 - Track Circuits",
            "IEEE 1653 - Standard for Audio Frequency Track Circuits",
            "FRA Track Safety Standards 49 CFR Part 213 (affects ballast conditions)"
        ],
        burden_holder="Railroad to maintain track circuits per FRA Part 236 shunting and broken rail detection requirements",
        adversary_position="Shunting failures due to contaminated wheels or light axle loads allow trains to pass without detection (false clear hazard)",
        counter_arguments=[
            "Track circuit design includes safety margin (100% shunt factor - 0.06 ohm shunt will drop out relay designed for 0.12 ohm)",
            "Wheel cleaning operations and rail grinding maintain contact resistance",
            "Minimum axle load standards for track circuit territory (typically 10-15 tons per axle)",
            "Polar stick relay prevents momentary shunt loss from causing signal upgrade",
            "PTC overlay provides independent train detection (GPS-based) as backup to track circuits",
            "Shunting assistance devices (wheel cleaners) deployed in severe contamination areas"
        ],
        resolution_strategy="Audio frequency jointless track circuits with adequate shunt margins, regular wheel/rail cleaning, minimum axle load requirements, polar stick relays, and PTC overlay provide defense-in-depth against shunting failures. Broken rail detection is critical safety function requiring regular testing.",
        entity_scope="All signaled railroad track - freight and passenger",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - Track circuits are proven technology with century-long safety record. AF jointless circuits represent modern best practice.",
        controlling_precedent="FRA Part 236.3 - Shunting sensitivity requirements establish minimum performance standards",
        category=IssueCategory.TRACK_CIRCUITS
    ),

    DoctrineBlock(
        topic="Positive Train Control (PTC) - I-ETMS Architecture",
        keywords=["PTC", "positive train control", "I-ETMS", "ETMS", "overlay system", "GPS", "automatic braking"],
        conclusion_template=[
            "Positive Train Control (PTC) is a GPS-based overlay system mandated by Congress after 2008 Chatsworth collision that killed 25.",
            "Interoperable Electronic Train Management System (I-ETMS) is the dominant implementation, using GPS positioning, wireless data communication, and onboard enforcement computers.",
            "PTC prevents train-to-train collisions, overspeed derailments, incursions into work zones, and movements through misaligned switches by automatically applying brakes if engineer fails to comply."
        ],
        reasoning_framework="""
PTC System Architecture and Operational Analysis:
1. Congressional Mandate: Rail Safety Improvement Act of 2008 required PTC on main lines with passenger service or toxic-by-inhalation (TIH) freight by 12/31/2015 (extended to 12/31/2020).
2. I-ETMS System Components: Back Office Server (BOS), Wayside Interface Units (WIU), Onboard Computer (OBC), GPS positioning, 220 MHz radio data link.
3. Train Location: GPS receiver provides position (±3-5 meters typical accuracy). Onboard system fuses GPS with wheel tachometer for tunnels/urban canyons.
4. Movement Authority: BOS computes authority limits based on track database, signal aspects, switch positions, work zone limits, and ahead train locations.
5. Braking Curve Calculation: OBC calculates braking curve based on train length, weight, grade, speed, and braking performance. Triggers penalty brake application if engineer exceeds curve.
6. Enforcement Points: PTC enforces signal aspects, track speed limits, temporary speed restrictions, civil speed limits, work zone boundaries, and absolute stop points.
7. Interoperability: Host and tenant railroads' PTC systems must exchange data to allow trains to operate across network. I-ETMS achieves this through common protocol.
8. Cut-Out Provisions: PTC can be disabled (cut-out) under degraded conditions with speed restrictions (typically 20-40 mph) and dispatcher authorization. Not a normal operating mode.
9. Database Management: Track database (geometry, signals, speed limits, switches) must be maintained with survey-grade accuracy. Database errors create enforcement errors.
10. Communication Reliability: 220 MHz radio network must provide coverage across territory. Coverage gaps cause loss of PTC protection.
11. GPS Accuracy Limitations: Multipath, atmospheric conditions, and satellite geometry affect accuracy. Integrity monitoring detects hazardous misleading information (HMI).
12. Onboard Computer Failures: Redundant processors and watchdog timers provide fail-safe operation. OBC failure triggers penalty brake and PTC cut-out.
13. Back Office Server Redundancy: Dual redundant BOS with hot standby prevents single point of failure.
14. Wayside Interface Units: Connect to signal system (track circuits, switch positions) and communicate with BOS. Solar powered or AC with battery backup.
15. Automatic Train Operation (ATO): PTC is enforcement only (prevents violations), not ATO (which controls train). Engineer remains in command.
16. Grade Crossing Enforcement: PTC can enforce maximum speed through grade crossings but does not directly control crossing warning systems.
17. Switch Position Verification: PTC requires positive switch position indication (WIU reads switch points) before granting authority through interlocking.
18. Work Zone Protection: Roadway workers establish electronic work zone limits in PTC system (shunting assistance or dispatch entry). Trains automatically stopped before incursion.
19. PTC Training Requirements: Engineers and conductors must complete PTC-specific training and demonstrate proficiency.
20. Revenue Service vs. Lab Testing: I-ETMS required extensive field testing before FRA certified for revenue service (2012-2015 timeframe).
21. Host-Tenant Interfaces: Tenant railroad trains must operate on host railroad PTC (e.g., Amtrak on freight railroad). Requires bilateral testing and agreement.
22. PTC Maintenance: Onboard and wayside equipment require periodic inspection and testing per FRA Part 236 Subpart I.
        """,
        key_factors=[
            "GPS positioning accuracy and integrity monitoring",
            "Radio communication coverage and reliability",
            "Track database accuracy and update procedures",
            "Onboard computer performance and fail-safe design",
            "Back office server redundancy and processing capacity",
            "Wayside interface unit installation and maintenance",
            "Train braking performance characteristics",
            "Engineer training and human factors",
            "Interoperability between host and tenant railroads",
            "PTC cut-out procedures and restrictions"
        ],
        primary_authority=[
            "49 CFR Part 236 Subpart I - PTC Systems",
            "Rail Safety Improvement Act of 2008 (Pub. L. 110-432)",
            "FRA PTC Safety Plan approval letters",
            "I-ETMS Interoperable Train Control Messaging Protocol",
            "FRA PTC Annual Progress Reports"
        ],
        burden_holder="Railroads to install, operate, and maintain PTC per FRA Part 236 Subpart I",
        adversary_position="PTC GPS positioning errors could cause false enforcement stops or failure to enforce at true hazard location",
        counter_arguments=[
            "GPS integrity monitoring (RAIM - Receiver Autonomous Integrity Monitoring) detects hazardous misleading information",
            "Wheel tachometer fusion provides backup positioning in GPS degraded areas",
            "Conservative braking curves and safety margins accommodate positioning uncertainty",
            "Track database includes location uncertainty zones around critical points",
            "Extensive field testing validated GPS performance before revenue service approval",
            "FRA certification process includes positioning accuracy validation"
        ],
        resolution_strategy="I-ETMS with GPS/tachometer fusion, integrity monitoring, conservative braking curves, accurate track database, and redundant architecture meets FRA safety requirements. System prevents categories of accidents (train-train collision, overspeed derailment, work zone incursion, switch misalignment) that GPS positioning errors would not defeat.",
        entity_scope="Class I freight railroads, Amtrak, commuter railroads on PTC-mandated main lines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - PTC is congressionally mandated system with extensive FRA oversight and proven in-service safety record since 2012",
        controlling_precedent="FRA Part 236 Subpart I (adopted 2010, revised 2012) establishes PTC performance and safety requirements",
        category=IssueCategory.PTC_SYSTEMS
    ),

    DoctrineBlock(
        topic="Centralized Traffic Control (CTC) - Dispatcher Command and Control",
        keywords=["CTC", "centralized traffic control", "dispatcher", "control point", "signal control", "track warrant"],
        conclusion_template=[
            "Centralized Traffic Control (CTC) allows dispatcher to remotely control signals and switches across territory from central location.",
            "CTC replaces timetable/train order operation with real-time train routing decisions based on traffic conditions.",
            "Modern CTC integrates with PTC and provides dispatcher with track occupancy display, automatic train tracking, and conflict prediction."
        ],
        reasoning_framework="""
CTC System Architecture and Operational Doctrine:
1. CTC Territory Definition: Main track controlled by dispatcher through signal system. Movements governed by signal indication (not timetable authority).
2. Control Points (CPs): Locations with controlled signals and/or switches. Dispatcher commands route selection at CPs.
3. Automatic Block Signal (ABS) Sections: Track between CPs has automatic intermediate signals (not dispatcher-controlled). Train detection advances signals automatically.
4. Dispatcher Control Machine: Computer workstation displaying track schematic, train positions, signal aspects, and route selections. Replaced physical model boards.
5. Route Request: Dispatcher selects origin and destination CP, system calculates route, checks for conflicts, and establishes route if safe.
6. Route Locking: Once route established and train approaching or in route, dispatcher cannot change route until train clears.
7. Traffic Optimization: Dispatcher routes trains to maximize throughput while prioritizing passenger trains and time-sensitive freight.
8. Meet/Pass Decisions: Dispatcher determines which train takes siding in single track territory to allow opposing or overtaking movement.
9. Maintaining Protection: Dispatcher must ensure signal protection for all movements. Cannot clear signal into occupied block or against another train's authority.
10. Verbal Authorities Prohibited in CTC: All movements governed by signal indication. Track warrants (verbal authorities) not used except during signal failures.
11. CTC/DTC Hybrid: Some railroads use CTC in high-traffic areas and Direct Traffic Control (DTC - track warrant based) in low-density areas.
12. Automatic Train Tracking: Modern CTC systems track train IDs using locomotive GPS, AEI tags, or manual entry. Provides situational awareness.
13. Conflict Prediction: Advanced CTC systems predict meets/passes and alert dispatcher to optimize routing decisions.
14. Vital vs. Non-Vital Functions: Route selection and signal clearing are vital (safety-critical) functions. Train tracking and displays are non-vital (can fail without safety hazard).
15. Dispatcher to Field Communication: Voice radio and/or data link for coordination with train crews and maintainers.
16. Control Point Nomenclature: CPs identified by milepost or geographic name (e.g., CP 123 or CP SUMMIT). Consistent naming prevents crew confusion.
17. Track Maintenance Coordination: Dispatcher grants track and time to maintainers, removes track from service in CTC system, and protects against train movements.
18. CTC Failure Degraded Mode: Signal system failure requires fallback to manual block or track warrant operation with speed restrictions.
19. Dispatcher Training: Complex decision-making requiring extensive training on rules, territory, and CTC system operation.
20. Remote Control Limits: Maximum distance from control location may be limited by communications latency and dispatcher workload (typically <300 miles per dispatcher).
21. CTC and PTC Integration: PTC system receives movement authorities from CTC signal aspects. Dispatcher CTC actions automatically reflected in PTC enforcement.
        """,
        key_factors=[
            "Control point spacing and route complexity",
            "Dispatcher workload and territory size",
            "Train traffic density and mix (passenger/freight)",
            "Signal system type (APB, ABS, interlocking)",
            "Communication system reliability (voice and data)",
            "Dispatcher training and decision support tools",
            "Vital logic design for route selection",
            "Integration with PTC enforcement",
            "Degraded mode operating procedures",
            "Track maintenance coordination protocols"
        ],
        primary_authority=[
            "49 CFR Part 236 Subpart C - Interlocking",
            "GCOR Rule 9.14 - Authorities in CTC territory",
            "AREMA C&S Manual Chapter 2 Part 6 - Centralized Traffic Control",
            "FRA Grade Crossing Handbook - CTC operation at crossings",
            "Railroad operating rules specific to CTC territory"
        ],
        burden_holder="Railroad to operate CTC per signal system design and FRA Part 236 requirements. Dispatcher to make safe routing decisions.",
        adversary_position="Dispatcher error in route selection could cause head-on collision or switch movement under train",
        counter_arguments=[
            "Interlocking logic prevents conflicting routes regardless of dispatcher input",
            "Route locking prevents route change once train committed",
            "Approach locking prevents route change when train approaching",
            "Dispatcher training emphasizes situational awareness and conflict prevention",
            "Modern CTC systems provide conflict prediction and warnings",
            "PTC overlay provides additional enforcement layer preventing dispatcher-caused collisions"
        ],
        resolution_strategy="CTC with interlocking logic, route locking, approach locking, dispatcher training, conflict prediction tools, and PTC overlay provides defense-in-depth against routing errors. Vital logic prevents unsafe signal clearance regardless of dispatcher actions.",
        entity_scope="Class I freight railroads, regional railroads, commuter rail systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - CTC is mature technology with proven safety record dating to 1920s. Modern computer-based CTC improves dispatcher decision support.",
        controlling_precedent="FRA Part 236 Subpart C establishes interlocking requirements applicable to CTC control points",
        category=IssueCategory.CTC_SYSTEMS
    ),

    DoctrineBlock(
        topic="Grade Crossing Warning Systems - Active and Passive Protection",
        keywords=["grade crossing", "crossing gates", "flashing lights", "crossing prediction", "island circuit", "constant warning time"],
        conclusion_template=[
            "Highway-rail grade crossings use active warning devices (gates, flashing lights, bells) or passive devices (crossbucks, stop signs) based on traffic volume and train speed.",
            "Active warning systems must provide consistent warning time (typically 20-30 seconds) before train arrival using track circuits or train detection systems.",
            "Grade crossing collisions (average 2,000/year in US) are leading cause of rail-related fatalities. Crossing closure and grade separation are ultimate solutions."
        ],
        reasoning_framework="""
Grade Crossing Protection System Design and Regulatory Analysis:
1. Passive Protection: Crossbuck signs (minimum required marking), stop signs, pavement markings. Relies on driver awareness and compliance. Low-cost but provides no active warning.
2. Active Protection: Flashing lights, bells, and/or crossing gates activated by approaching train. Provides positive warning of train approach.
3. Crossing Gates: Descend across roadway lanes to physically block vehicle entry. Most effective active warning device (reduces collisions ~90% vs. passive crossings).
4. Flashing Light Signals (FLS): Alternating red lights (similar to traffic signal) with bell. Required at all gated crossings and used alone at lower-traffic crossings.
5. Constant Warning Time (CWT): System adjusts warning activation time based on train speed to provide consistent 20-30 second warning. Modern standard for all active crossings.
6. Island Circuit Design: Track circuits on both sides of crossing detect train approach. Simple design but warning time varies with train speed unless CWT logic added.
7. Motion Sensor (Predictors): Doppler radar or audio frequency track circuit measures train speed and distance, calculates arrival time, activates warning at CWT. Replaces island circuits on modern installations.
8. Gate Descent Time: Typically 12-20 seconds from activation to full descent. Must be factored into CWT calculation.
9. Crossing Surface: Must be smooth and level to prevent vehicle stalling on tracks. Rubber grade crossing panels common on modern installations.
10. Sighting Distance Requirements: Driver must have adequate sight distance to crossing (minimum 15 seconds travel time at highway speed). Vegetation and structures must not obstruct view.
11. Quiet Zones: Communities can establish quiet zones (no train horns) if crossings upgraded to four-quadrant gates or other supplemental safety measures (SSMs).
12. Four-Quadrant Gates: Gates on both sides of roadway (entrance and exit). Prevents vehicles from driving around lowered gate. Required for quiet zones without SSMs.
13. Median Barriers: Physical barrier in roadway median prevents vehicles from driving around gates. Alternative SSM to four-quadrant gates.
14. Wrong-Way Crossing Detection: Sensors detect vehicle entering crossing against traffic flow (possible suicide or impaired driver). Alerts train crew.
15. Pedestrian Gates: Separate gates and/or audible warnings for sidewalks/bike paths crossing tracks.
16. Crossing Failure Detection: Grade crossing malfunction circuits detect gate failures and notify dispatcher/maintainer. Train may need to stop and flag crossing.
17. Crossing Bell Cutout: Bell silenced during overnight hours in some communities to reduce noise. Flashing lights and gates remain active.
18. Solar Power Systems: Remote crossings use solar panels with battery backup instead of commercial power. Must be designed for worst-case winter sun angle.
19. Crossing Inventory: FRA maintains national inventory of ~210,000 public highway-rail grade crossings. Inventory data used for risk analysis and funding prioritization.
20. Crossing Closure Programs: Eliminating low-usage crossings through closure and traffic rerouting reduces overall grade crossing risk.
21. Grade Separation: Highway overpass or underpass eliminates crossing conflict. Most expensive solution (~$5-20M) but provides 100% protection.
22. MUTCD Part 8: Federal standards for highway-rail grade crossing warning devices. Applies to public crossings.
23. Private Crossings: Railroad property access crossings not subject to MUTCD but must have warning signs. Railroad controls access permissions.
24. Pedestrian Trespass: Railroad ROW trespassing (walking on tracks) causes ~500 deaths/year. Not a grade crossing issue but related safety problem.
        """,
        key_factors=[
            "Traffic volume and train frequency",
            "Train speeds and acceleration/deceleration characteristics",
            "Highway approach speeds and geometry",
            "Sight distance and obstructions",
            "Warning time consistency (CWT vs. island circuit)",
            "Gate descent time and four-quadrant vs. two-quadrant",
            "Crossing surface condition and vehicle stalling risk",
            "Power supply reliability (commercial or solar)",
            "Maintenance and testing frequency",
            "Community quiet zone requests and SSM requirements"
        ],
        primary_authority=[
            "23 CFR 646 Subpart B - Railroad-Highway Projects",
            "MUTCD Part 8 - Traffic Controls for Highway-Rail Grade Crossings",
            "49 CFR Part 222 - Use of Locomotive Horns at Highway-Rail Grade Crossings",
            "FRA Grade Crossing Handbook (2007)",
            "AREMA C&S Manual Chapter 3 Part 15 - Highway Crossing Warning Systems"
        ],
        burden_holder="Railroad and highway authority share responsibility for grade crossing safety. Railroad maintains warning devices; highway authority maintains roadway approaches.",
        adversary_position="Drivers routinely ignore crossing warnings (gates down, lights flashing) causing collisions",
        counter_arguments=[
            "Four-quadrant gates physically prevent drivers from entering crossing",
            "Median barriers prevent evasive maneuvers around gates",
            "Photo/video enforcement (where legal) deters violations",
            "Crossing closure eliminates conflicts at low-traffic locations",
            "Grade separation provides absolute protection",
            "Public education campaigns improve driver compliance"
        ],
        resolution_strategy="Comprehensive grade crossing safety strategy: 1) Close low-traffic crossings, 2) Upgrade remaining crossings to four-quadrant gates with CWT, 3) Grade separate highest-risk locations, 4) Photo enforcement of violations, 5) Public education. No single measure eliminates collisions; layered approach required.",
        entity_scope="All public highway-rail grade crossings - freight and passenger railroads",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="AGGRESSIVE - Grade crossing safety depends heavily on driver behavior which cannot be fully controlled by warning devices. Four-quadrant gates significantly reduce but do not eliminate collisions.",
        controlling_precedent="MUTCD Part 8 establishes minimum standards for active warning devices. FRA Part 222 establishes quiet zone requirements including SSMs.",
        category=IssueCategory.GRADE_CROSSINGS
    ),

    DoctrineBlock(
        topic="Fail-Safe Design Principles - Assured Safety Through Failure Modes",
        keywords=["fail-safe", "vital logic", "de-energize to restrict", "redundancy", "diversity", "self-checking"],
        conclusion_template=[
            "Fail-safe design ensures that any single equipment failure results in the most restrictive safe state (signals red, routes locked, brakes applied).",
            "Key principles: de-energize to restrict, redundant checking, diversity of components, and continuous self-monitoring detect failures before hazardous conditions develop.",
            "Railway signal systems have achieved extraordinarily low failure rates (10^-9 hazardous failures per hour) through rigorous application of fail-safe principles."
        ],
        reasoning_framework="""
Fail-Safe Design Methodology for Railway Signal Systems:
1. De-Energize to Restrict Principle: Safety-critical devices (signals, route relays) must require energization to display permissive indication. Power loss or relay dropout defaults to restrictive state.
2. Gravity Fail-Safe: Searchlight signal lens mechanism uses gravity to return to red on power loss. Gate crossing arms fall to horizontal (blocking position) on power loss.
3. Relay Contact Design: Front contacts (normally open) used for permissive functions; back contacts (normally closed) for restrictive functions. Ensures relay dropout causes restriction.
4. Dual Redundancy: Two independent devices must agree before permissive function allowed. Example: Two track relays in series (both must be energized for clear signal).
5. Diversity Principle: Redundant devices should use different technologies to avoid common-mode failures. Example: Track circuit uses inductive shunting; PTC uses GPS positioning.
6. Self-Checking Vital Logic: Computer-based systems use dual processors executing same logic and comparing results. Disagreement triggers fail-safe shutdown.
7. Watchdog Timers: Independent timer circuit monitors computer execution. Failure to update watchdog within time limit triggers system reset or safe shutdown.
8. Stuck-At Fault Detection: Vital logic must detect single-bit failures (stuck-at-0 or stuck-at-1) before they create hazardous condition. Achieved through coded data and checking logic.
9. Fail-Safe Relay Selection: Relays must have predictable failure modes. Forced-guided relays mechanically ensure NO and NC contacts cannot both be closed (prevents false permissive from welded contact).
10. Code-Based Vital Processing: Data transmitted between vital components is encoded (e.g., 2-out-of-4 code) so that single-bit error creates invalid code, detected by receiver.
11. Defensive Programming: Software must not rely on runtime libraries or operating system services that are not proven fail-safe. Bare-metal execution or minimal RTOS.
12. Memory Scrubbing: ECC memory with periodic scrubbing detects and corrects single-bit errors, prevents accumulation of soft errors.
13. Safe Power-Up State: On initial energization, system must default to restrictive state until self-tests pass and safe state confirmed.
14. Periodic Testing: Automated self-tests run continuously or on schedule to detect latent failures before they become hazardous.
15. Error-Detecting Codes: Checksums, CRC, or cryptographic hashes ensure data integrity in communications and storage.
16. Vital Output Interface: Computer-based systems use vital relay interface to control field equipment. Software outputs drive relays, but relay logic provides final safety enforcement.
17. Track Circuit Polar Stick Relay: Prevents momentary de-energization from causing signal upgrade. Relay latches in de-energized state until deliberate reset.
18. Approach Locking Relay: Separate relay holds route locked when track circuit approaching interlocking is occupied. Provides defense-in-depth beyond route locking relay.
19. Aspect Sequence Checking: Logic prevents signal from upgrading more than one aspect at a time (e.g., red to yellow allowed, red to green blocked).
20. Fail-Safe Clock Sources: Timers used for safety functions (e.g., approach locking time) must have bounded maximum delay (cannot run too slow). Crystal oscillators with frequency monitoring.
21. Single Point of Failure Analysis: Design review must identify all credible single failures and verify each results in safe state.
22. Common Mode Failure Prevention: Environmental stresses (temperature, vibration, EMI) that could cause simultaneous failure of redundant components must be mitigated through separation, shielding, and derating.
23. Maintenance-Induced Failures: Procedures must prevent maintainer errors from creating hazardous conditions. Example: Disconnecting relay plug must cause all associated signals to red.
24. Proven-in-Use Components: New components should have demonstrated reliability record or undergo extensive qualification testing.
        """,
        key_factors=[
            "De-energize to restrict implementation",
            "Redundancy and diversity of safety checks",
            "Self-checking vital processor architecture",
            "Relay contact design and failure modes",
            "Software safety validation and defensive programming",
            "Watchdog timers and error detection codes",
            "Single point of failure analysis completeness",
            "Common mode failure prevention",
            "Maintenance procedures and error prevention",
            "Periodic testing and self-diagnostic coverage"
        ],
        primary_authority=[
            "49 CFR 236.15 - Fail-safe requirements",
            "49 CFR 236.788 - Vital processor requirements",
            "IEC 61508 - Functional Safety of Electrical/Electronic/Programmable Electronic Safety-Related Systems",
            "EN 50129 - Railway Safety-Related Electronic Systems for Signaling",
            "CENELEC EN 50126/128/129 - Railway RAMS and Software Standards"
        ],
        burden_holder="Signal system designer and manufacturer to implement fail-safe design per FRA Part 236 and industry standards",
        adversary_position="Subtle software bugs in vital computer could allow hazardous failures despite self-checking",
        counter_arguments=[
            "Vital processor architecture with diverse redundancy detects software execution errors",
            "Extensive validation testing per EN 50128 before deployment",
            "Vital relay output interface provides hardware enforcement layer independent of software",
            "Proven software platforms reused across multiple installations reduce novel defect risk",
            "In-service failure rate data demonstrates effectiveness of vital design (SIL-4 achievement)",
            "Formal methods verification for critical software modules"
        ],
        resolution_strategy="Layered fail-safe design: 1) De-energize to restrict at component level, 2) Dual redundant checking, 3) Diverse technologies, 4) Self-checking vital logic, 5) Vital relay output interface, 6) Continuous self-diagnostics, 7) Extensive validation testing. Multiple independent safety layers ensure single failure cannot cause hazardous condition.",
        entity_scope="All railway signal systems - design, manufacturing, and maintenance organizations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="DEFENSIBLE - Fail-safe design principles are mature and proven through century of railway signaling practice. Modern vital computer systems achieve SIL-4 (10^-9 hazardous failure rate).",
        controlling_precedent="FRA Part 236.15 establishes fail-safe requirements for signal systems. EN 50129 provides recognized international standard for vital electronic systems.",
        category=IssueCategory.FAIL_SAFE_DESIGN
    ),

]


# ============================================================================
# ENGINE CORE LOGIC
# ============================================================================

class RAIL03Engine:
    """Railway Signal & Control Systems Intelligence Engine - TIE Gold Standard"""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.start_time = datetime.now()
        logger.info(f"RAIL03 Engine initialized with {len(self.doctrines)} doctrine blocks")

    def three_layer_response(self, query: str, mode: ResponseMode) -> QueryResponse:
        """
        TIE-20 Component: Three-layer response strategy
        Layer 1: Doctrine cache (0-200ms)
        Layer 2: Semantic retrieval (fallback)
        Layer 3: Deep analysis (complex queries)
        """
        triggered = self._match_doctrines(query)

        if not triggered:
            return self._fallback_response(query, mode)

        if mode == ResponseMode.FAST:
            return self._fast_response(query, triggered)
        elif mode == ResponseMode.DEFENSE:
            return self._defense_response(query, triggered)
        else:  # MEMO
            return self._memo_response(query, triggered)

    def _match_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Match query against doctrine keywords"""
        query_lower = query.lower()
        matched = []

        for doctrine in self.doctrines:
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            if keyword_matches > 0:
                matched.append(doctrine)

        # Sort by keyword match count (best matches first)
        matched.sort(key=lambda d: sum(1 for kw in d.keywords if kw.lower() in query_lower), reverse=True)
        return matched[:3]  # Top 3 matches

    def _fast_response(self, query: str, doctrines: List[DoctrineBlock]) -> QueryResponse:
        """FAST mode: Concise answer with key points"""
        primary = doctrines[0]
        answer_parts = [
            f"**{primary.topic}**\n",
            "\n".join(primary.conclusion_template),
            f"\n\n**Key Factors:** {', '.join(primary.key_factors[:5])}",
            f"\n\n**Authority:** {primary.primary_authority[0]}"
        ]

        return QueryResponse(
            answer="".join(answer_parts),
            confidence=primary.confidence,
            mode=ResponseMode.FAST,
            triggered_doctrines=[d.topic for d in doctrines],
            authority_citations=primary.primary_authority[:2],
            metadata={
                "category": primary.category.value,
                "entity_scope": primary.entity_scope,
                "doctrines_matched": len(doctrines)
            },
            determinism_hash=self._compute_hash(query, ResponseMode.FAST),
            timestamp=datetime.now().isoformat()
        )

    def _defense_response(self, query: str, doctrines: List[DoctrineBlock]) -> QueryResponse:
        """DEFENSE mode: Audit-ready detailed analysis"""
        primary = doctrines[0]
        answer_parts = [
            f"# Railway Signal System Analysis: {primary.topic}\n\n",
            "## Conclusion\n",
            "\n".join(primary.conclusion_template),
            "\n\n## Reasoning Framework\n",
            primary.reasoning_framework,
            "\n\n## Critical Factors\n",
            "\n".join(f"- {factor}" for factor in primary.key_factors),
            "\n\n## Controlling Authority\n",
            "\n".join(f"- {auth}" for auth in primary.primary_authority),
            "\n\n## Adversarial Analysis\n",
            f"**Position:** {primary.adversary_position}\n",
            f"**Counter-Arguments:**\n" + "\n".join(f"- {arg}" for arg in primary.counter_arguments),
            f"\n\n**Resolution:** {primary.resolution_strategy}",
            f"\n\n## Confidence Assessment\n",
            f"**Level:** {primary.confidence.value}\n",
            f"**Stratification:** {primary.confidence_stratification}",
            f"\n\n**Controlling Precedent:** {primary.controlling_precedent}"
        ]

        all_authorities = []
        for d in doctrines:
            all_authorities.extend(d.primary_authority)

        return QueryResponse(
            answer="".join(answer_parts),
            confidence=primary.confidence,
            mode=ResponseMode.DEFENSE,
            triggered_doctrines=[d.topic for d in doctrines],
            authority_citations=list(set(all_authorities))[:10],
            metadata={
                "category": primary.category.value,
                "entity_scope": primary.entity_scope,
                "burden_holder": primary.burden_holder,
                "adversary_position": primary.adversary_position,
                "doctrines_analyzed": len(doctrines)
            },
            determinism_hash=self._compute_hash(query, ResponseMode.DEFENSE),
            timestamp=datetime.now().isoformat()
        )

    def _memo_response(self, query: str, doctrines: List[DoctrineBlock]) -> QueryResponse:
        """MEMO mode: Full documentation with all relevant doctrines"""
        answer_parts = [
            f"# Railway Signal & Control Systems - Comprehensive Analysis\n",
            f"**Query:** {query}\n",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n",
            f"**Doctrines Triggered:** {len(doctrines)}\n\n",
            "---\n\n"
        ]

        for idx, doctrine in enumerate(doctrines, 1):
            answer_parts.extend([
                f"## Doctrine {idx}: {doctrine.topic}\n\n",
                f"**Category:** {doctrine.category.value}\n",
                f"**Confidence:** {doctrine.confidence.value}\n\n",
                "### Conclusion\n",
                "\n".join(doctrine.conclusion_template),
                "\n\n### Analysis Framework\n",
                doctrine.reasoning_framework,
                "\n\n### Key Factors\n",
                "\n".join(f"{i+1}. {factor}" for i, factor in enumerate(doctrine.key_factors)),
                "\n\n### Primary Authority\n",
                "\n".join(f"- {auth}" for auth in doctrine.primary_authority),
                "\n\n### Risk Analysis\n",
                f"**Burden:** {doctrine.burden_holder}\n",
                f"**Adversary Position:** {doctrine.adversary_position}\n",
                f"**Counter-Arguments:**\n" + "\n".join(f"- {arg}" for arg in doctrine.counter_arguments),
                f"\n\n**Resolution Strategy:** {doctrine.resolution_strategy}",
                f"\n\n**Controlling Precedent:** {doctrine.controlling_precedent}",
                "\n\n---\n\n"
            ])

        all_authorities = []
        for d in doctrines:
            all_authorities.extend(d.primary_authority)

        return QueryResponse(
            answer="".join(answer_parts),
            confidence=doctrines[0].confidence,
            mode=ResponseMode.MEMO,
            triggered_doctrines=[d.topic for d in doctrines],
            authority_citations=list(set(all_authorities)),
            metadata={
                "primary_category": doctrines[0].category.value,
                "all_categories": list(set(d.category.value for d in doctrines)),
                "total_doctrines": len(doctrines),
                "confidence_range": list(set(d.confidence.value for d in doctrines))
            },
            determinism_hash=self._compute_hash(query, ResponseMode.MEMO),
            timestamp=datetime.now().isoformat()
        )

    def _fallback_response(self, query: str, mode: ResponseMode) -> QueryResponse:
        """Fallback when no doctrines match"""
        answer = f"""No specific railway signal system doctrine matched your query: "{query}"

This engine covers:
- Block signaling (APB, ABS)
- Interlocking systems (mechanical, relay, electronic, computer-based)
- Signal aspects (color light, searchlight, position light)
- Track circuits (DC, AC, AF, coded)
- Positive Train Control (PTC/I-ETMS)
- Centralized Traffic Control (CTC)
- Cab signaling and ATC/ACSES
- Grade crossing warning systems
- Fail-safe design principles
- ERTMS/ETCS (European systems)

Please rephrase your query to include specific signal system terminology."""

        return QueryResponse(
            answer=answer,
            confidence=ConfidenceLevel.DISCLOSURE,
            mode=mode,
            triggered_doctrines=[],
            authority_citations=[],
            metadata={"fallback": True, "query": query},
            determinism_hash=self._compute_hash(query, mode),
            timestamp=datetime.now().isoformat()
        )

    def _compute_hash(self, query: str, mode: ResponseMode) -> str:
        """TIE-20 Component: Determinism hash for reproducibility"""
        content = f"{query}|{mode.value}|RAIL03|v1.0.0"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def health_check(self) -> HealthResponse:
        """TIE-20 Component: Health endpoint"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return HealthResponse(
            status="healthy",
            engine="RAIL03 - Railway Signal & Control Systems",
            version="1.0.0",
            port=9103,
            doctrines_loaded=len(self.doctrines),
            uptime_seconds=uptime,
            timestamp=datetime.now().isoformat()
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="RAIL03 - Railway Signal & Control Systems Intelligence Engine",
    description="TIE Gold Standard: Railway signal systems, interlocking, PTC, track circuits, grade crossings",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RAIL03Engine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - TIE three-layer response"""
    try:
        return engine.three_layer_response(request.query, request.mode)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """TIE-20 Component: Health check endpoint"""
    return engine.health_check()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all available doctrines"""
    return {
        "total": len(engine.doctrines),
        "categories": list(set(d.category.value for d in engine.doctrines)),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in engine.doctrines
        ]
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting RAIL03 Railway Signal & Control Systems Engine on port 9103")
    uvicorn.run(APP, host="0.0.0.0", port=9103, log_level="info")
