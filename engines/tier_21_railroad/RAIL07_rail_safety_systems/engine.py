"""
RAIL07 Rail Safety Systems Intelligence Engine
Port: 9213
Version: 1.0.0

Railroad safety analysis: PTC, grade crossings, derailment prevention, hazmat transport,
accident investigation, FRA compliance.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_NAME = "RAIL07_rail_safety_systems"
VERSION = "1.0.0"
PORT = 9213

logger.add(
    f"logs/{ENGINE_NAME}.log",
    rotation="100 MB",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)

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
    PTC_SYSTEMS = "PTC_SYSTEMS"
    GRADE_CROSSINGS = "GRADE_CROSSINGS"
    TRACK_SAFETY = "TRACK_SAFETY"
    DERAILMENT_PREVENTION = "DERAILMENT_PREVENTION"
    HAZMAT_TRANSPORT = "HAZMAT_TRANSPORT"
    SIGNAL_SYSTEMS = "SIGNAL_SYSTEMS"
    ACCIDENT_INVESTIGATION = "ACCIDENT_INVESTIGATION"
    LOCOMOTIVE_SAFETY = "LOCOMOTIVE_SAFETY"
    CREW_ALERTNESS = "CREW_ALERTNESS"
    EOT_DEVICES = "EOT_DEVICES"
    TRACK_GEOMETRY = "TRACK_GEOMETRY"
    BROKEN_RAIL_DETECTION = "BROKEN_RAIL_DETECTION"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    mode: ResponseMode = ResponseMode.FAST
    zone: AnalysisZone = AnalysisZone.REPORTING
    context: Optional[Dict[str, Any]] = None

class DoctrineMatch(BaseModel):
    topic: str
    confidence: float
    reasoning: str
    authority: List[str]

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    reasoning_chain: List[str]
    authorities: List[str]
    warnings: List[str]
    mode: ResponseMode
    zone: AnalysisZone
    determinism_hash: str
    latency_ms: float

class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float

# ============================================================================
# DOCTRINE BLOCK STRUCTURE
# ============================================================================

class DoctrineBlock:
    def __init__(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: str,
        reasoning_framework: str,
        key_factors: List[str],
        primary_authority: List[str],
        confidence: ConfidenceLevel,
        issue_category: IssueCategory,
        fragility_score: float = 0.5
    ):
        self.topic = topic
        self.keywords = [k.lower() for k in keywords]
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.issue_category = issue_category
        self.fragility_score = fragility_score
        self.triggered_count = 0
        self.last_triggered = None

    def matches(self, question: str) -> float:
        q_lower = question.lower()
        matches = sum(1 for kw in self.keywords if kw in q_lower)
        return matches / len(self.keywords) if self.keywords else 0.0

# ============================================================================
# DOCTRINE CACHE - 25+ REAL RAILROAD SAFETY EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="PTC Implementation Requirements",
        keywords=["ptc", "positive train control", "i-etms", "acses", "e-atc", "interoperability"],
        conclusion_template="PTC system implementation must meet FRA interoperability and safety requirements.",
        reasoning_framework="""
Positive Train Control (PTC) analysis framework:
1. System Architecture Assessment:
   - I-ETMS (Interoperable Electronic Train Management System) for freight
   - ACSES (Advanced Civil Speed Enforcement System) for passenger
   - E-ATC (Enhanced Automatic Train Control) for commuter rail
   - Back office server (BOS) integration requirements
   - Onboard systems (OBE) certification status

2. Interoperability Requirements (49 CFR 236.1015):
   - PTC systems of different railroads must interoperate
   - Tenant railroad operations on host railroad territory
   - System interface specifications compliance
   - Communication protocols (220 MHz radio spectrum)

3. Safety Critical Functions:
   - Prevention of train-to-train collisions
   - Enforcement of speed restrictions (permanent and temporary)
   - Protection of roadway workers in work zones
   - Prevention of train movement through switches left in wrong position

4. Implementation Challenges:
   - Back office server redundancy and failover
   - Wayside interface unit (WIU) installation and maintenance
   - Onboard equipment installation and testing
   - Spectrum allocation and radio coverage gaps
   - Software version control across multi-railroad operations

5. Testing and Certification:
   - FRA Type Approval process
   - Field testing on revenue service track
   - Interoperability testing with connecting carriers
   - Cut-over procedures from legacy signaling

6. Operational Considerations:
   - Dark territory (non-signaled) PTC overlay
   - Temporary speed restrictions (TSR) entry and enforcement
   - PTC-equipped locomotive availability
   - Crew training and qualification requirements

7. Failure Mode Analysis:
   - Loss of communication (revert to restricted speed)
   - GPS signal degradation or loss
   - Onboard equipment failure (PTC cut-out procedures)
   - Back office server unavailability
        """,
        key_factors=[
            "FRA Type Approval status",
            "Interoperability testing completion",
            "220 MHz radio spectrum coverage",
            "Back office server redundancy",
            "Onboard equipment certification",
            "Crew training and qualification",
            "TSR enforcement capability"
        ],
        primary_authority=[
            "49 CFR Part 236 Subpart I - Positive Train Control Systems",
            "49 CFR 236.1015 - PTC System Interoperability",
            "FRA PTC Implementation Status Reports"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.PTC_SYSTEMS,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Grade Crossing Warning Systems",
        keywords=["grade crossing", "crossing protection", "gates", "flashers", "quiet zone", "crossing warning"],
        conclusion_template="Grade crossing protection adequacy depends on traffic volume, train speed, and FRA risk assessment.",
        reasoning_framework="""
Grade crossing warning system analysis:
1. Crossing Classification (USDOT Crossing Inventory):
   - Public vs. private crossings
   - Highway classification (interstate, arterial, local road)
   - Annual average daily traffic (AADT) counts
   - Train movements per day
   - Maximum timetable speed

2. Warning Device Types (23 CFR 646):
   - Passive devices: crossbucks, stop signs, pavement markings
   - Active automatic: flashing lights, gates, constant warning time
   - Active advanced: four-quadrant gates, median barriers
   - Predictive systems for variable train speeds

3. Constant Warning Time (CWT) Requirements:
   - 20-30 second advance warning before train arrival
   - Motion detectors vs. fixed island circuits
   - Approach circuit design for varying train speeds
   - Predictor algorithms for acceleration/deceleration

4. Quiet Zone Establishment (49 CFR Part 222):
   - Supplemental Safety Measures (SSMs) required
   - Four-quadrant gates or median barriers
   - Photo enforcement or one-way streets with gates
   - Risk index analysis must show no increase in risk
   - New Quiet Zones require SSMs at all crossings
   - Pre-existing Quiet Zones (pre-2005) may continue with risk analysis

5. Sight Distance Requirements:
   - Stopping sight distance calculation
   - Clear zone vegetation and obstacle management
   - Horizontal and vertical alignment impact
   - Driver decision time and vehicle acceleration

6. Diagnostic Team Reviews:
   - FRA-led field reviews for high-incident crossings
   - State Highway-Rail Grade Crossing Action Plans
   - Engineering, enforcement, education (3E) approach
   - Crossing closure vs. upgrade cost-benefit analysis

7. Maintenance and Testing (49 CFR 234):
   - Monthly inspections of active warning devices
   - Battery backup testing
   - Gate timing and constant warning time verification
   - Signal maintainer qualifications
        """,
        key_factors=[
            "AADT and train movement volumes",
            "Maximum train speed",
            "Warning device type and condition",
            "Constant warning time accuracy",
            "Quiet zone SSM compliance",
            "Sight distance adequacy",
            "Maintenance and testing records"
        ],
        primary_authority=[
            "49 CFR Part 222 - Use of Locomotive Horns at Highway-Rail Grade Crossings",
            "49 CFR Part 234 - Grade Crossing Safety",
            "23 CFR 646 Subpart B - Railroad-Highway Projects"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.GRADE_CROSSINGS,
        fragility_score=0.4
    ),

    DoctrineBlock(
        topic="FRA Track Safety Standards",
        keywords=["track safety", "fra part 213", "track geometry", "track class", "rail defects"],
        conclusion_template="Track safety compliance requires adherence to FRA Part 213 geometry limits and inspection frequencies.",
        reasoning_framework="""
FRA Part 213 Track Safety Standards framework:
1. Track Classification and Speed Limits (49 CFR 213.9):
   - Class 1: Freight 10 mph, Passenger 15 mph
   - Class 2: Freight 25 mph, Passenger 30 mph
   - Class 3: Freight 40 mph, Passenger 60 mph
   - Class 4: Freight 60 mph, Passenger 80 mph
   - Class 5: Freight 80 mph, Passenger 90 mph
   - Class 6-9: Higher speed passenger service (up to 200 mph Class 9)

2. Track Geometry Limits (49 CFR 213.55, 213.63):
   - Gage: 56.5 inches standard, 57 inches max for Class 1-2
   - Alignment: Deviation from straight line (0.5 in. to 3 in. depending on class)
   - Surface (profile): Vertical deviation in 31 or 62 ft chord
   - Cross level: Difference in elevation of rail tops (Class 5: 0.75 in. max)
   - Warp: Twist over 62 ft distance

3. Rail Inspection Requirements (49 CFR 213.233-237):
   - Visual inspection frequencies by track class
   - Ultrasonic testing for internal defects
   - 29 types of rail defects requiring remedial action
   - Joint bar inspection (bolt tightness, broken bars)
   - Continuous welded rail (CWR) stress management

4. Rail Defect Types Requiring Immediate Action:
   - Transverse defects (detail fractures, bolt hole cracks)
   - Engine burn fractures
   - Vertical split heads
   - Horizontal split heads
   - Compound fissures
   - Crushed heads or ends

5. Crossties and Track Structure (49 CFR 213.109):
   - Defective crosstie criteria (split, broken, decay)
   - Crosstie distribution requirements
   - Ballast depth and shoulder width
   - Track modulus and support conditions

6. Continuous Welded Rail (CWR) Requirements (49 CFR 213.119):
   - Rail temperature monitoring and neutral temperature
   - Buckling prevention in hot weather
   - Pull-apart prevention in cold weather
   - Destressing procedures after rail work
   - Slow orders during extreme temperatures

7. Track Geometry Measurement:
   - Automated track geometry cars (TGC)
   - Gage restraint measurement systems (GRMS)
   - Exception reporting and prioritization
   - Geometry degradation trending
        """,
        key_factors=[
            "Track class and authorized speeds",
            "Geometry measurements vs. FRA limits",
            "Rail defect inspection frequency",
            "Crosstie condition and distribution",
            "CWR neutral temperature management",
            "Ballast condition and drainage",
            "Inspection qualification and records"
        ],
        primary_authority=[
            "49 CFR Part 213 - Track Safety Standards",
            "49 CFR 213.233 - Automated Inspection",
            "FRA Track Inspector Field Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRACK_SAFETY,
        fragility_score=0.2
    ),

    DoctrineBlock(
        topic="Derailment Causation Analysis",
        keywords=["derailment", "wheel climb", "l/v ratio", "track geometry", "hunting", "rail rollover"],
        conclusion_template="Derailment analysis requires examination of wheel-rail interface forces and track geometry conditions.",
        reasoning_framework="""
Derailment prevention and investigation framework:
1. Wheel Climb Derailment Mechanics:
   - L/V ratio (lateral to vertical force ratio)
   - Nadal's criterion: L/V > tan(flange angle - friction angle)
   - Typical flange angle 70 degrees, friction coefficient 0.3-0.5
   - Critical L/V ratio approximately 0.8 to 1.2

2. Track Geometry Defects Leading to Derailment:
   - Wide gage allowing wheel drop between rails
   - Alignment deviation causing excessive lateral forces
   - Cross level defects causing unequal wheel loading
   - Surface (profile) defects causing dynamic wheel unloading
   - Gage restraint loss in curves

3. Rolling Stock Defects:
   - Wheel tread defects (flat spots, shells, shelling)
   - Hollow worn wheels reducing wheel-rail contact
   - Truck hunting (lateral oscillation) due to worn suspension
   - Center plate wear allowing excessive truck rotation
   - Broken or worn springs causing uneven load distribution

4. Operational Factors:
   - Excessive speed in curves (centrifugal force)
   - Emergency braking causing longitudinal forces
   - Slack run-in/run-out in train (buff and draft forces)
   - Improper train handling (power application in curves)

5. Broken Rail Derailments:
   - Track circuit shunting may detect break
   - Rail anchoring conditions
   - Joint bar integrity at bolted joints
   - CWR gap formation in cold weather

6. Load Shift and Securement:
   - Lading shift in loaded cars
   - Center of gravity height and lateral stability
   - Improper loading or securement
   - Liquids sloshing in tank cars

7. NTSB Investigation Methodology:
   - Event recorder data analysis
   - Locomotive speed and braking application
   - Track geometry measurement at derailment site
   - Rolling stock mechanical inspection
   - Metallurgical analysis of failed components
   - Human factors analysis (crew actions, fatigue)
        """,
        key_factors=[
            "L/V ratio and wheel climb potential",
            "Track geometry condition at derailment site",
            "Wheel and truck condition",
            "Train speed vs. authorized limit",
            "Event recorder data analysis",
            "Broken rail or track structure failure",
            "Load distribution and securement"
        ],
        primary_authority=[
            "49 CFR Part 213 - Track Safety Standards",
            "49 CFR Part 215 - Railroad Freight Car Safety Standards",
            "NTSB Railroad Accident Investigation Reports"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.DERAILMENT_PREVENTION,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Hazmat Rail Transport Regulations",
        keywords=["hazmat", "hazardous materials", "dot classification", "placarding", "tank car", "phmsa"],
        conclusion_template="Hazmat rail transport requires DOT classification, proper placarding, and routing per FRA Part 174.",
        reasoning_framework="""
Hazardous materials rail transport safety framework:
1. DOT Hazard Classification (49 CFR Part 172):
   - Class 1: Explosives (divisions 1.1 to 1.6)
   - Class 2: Gases (flammable, non-flammable, poison)
   - Class 3: Flammable liquids
   - Class 4: Flammable solids
   - Class 5: Oxidizers and organic peroxides
   - Class 6: Toxic substances and infectious substances
   - Class 7: Radioactive materials
   - Class 8: Corrosive materials
   - Class 9: Miscellaneous hazardous materials

2. Tank Car Specifications (49 CFR Part 179):
   - DOT-111 (legacy general service tank car)
   - DOT-117 (enhanced tank car for flammable liquids)
   - Pressure tank cars for gases (DOT-105, 112, 114)
   - Thickness of tank shell
   - Head shield protection
   - Jacket and thermal protection
   - Top and bottom fittings protection

3. Placarding Requirements (49 CFR 172.504):
   - Four placards minimum (one on each side and end)
   - Placard specifications (10.75 inch square)
   - Proper hazard class and division
   - UN identification numbers on orange panels or placards

4. Rail Routing and Security (49 CFR Part 172 Subpart I):
   - High-hazard flammable trains (HHFT) definition
   - 20+ consecutive or 35+ total loads of Class 3 flammable liquids
   - Route analysis considering population density
   - Alternative route feasibility
   - Security plans for toxic inhalation hazard (TIH) materials

5. FRA Part 174 Specific Requirements:
   - Carload-to-train limits for certain materials
   - Separation and segregation requirements
   - Position in train restrictions (away from locomotives, occupied caboose)
   - Handling and storage requirements

6. Emergency Response Information (49 CFR 172.602):
   - Emergency Response Guidebook (ERG) compliance
   - Shipping papers with 24-hour emergency contact
   - Train crew hazmat training and certification
   - First responder notification procedures

7. Crude Oil and Ethanol Transport (Post-Lac-Mégantic):
   - Enhanced tank car standards (DOT-117)
   - Electronically controlled pneumatic (ECP) brakes (delayed)
   - Speed restrictions through high-threat urban areas
   - Risk-based route selection
        """,
        key_factors=[
            "Proper DOT hazard classification",
            "Tank car specification compliance",
            "Placard accuracy and visibility",
            "Route analysis and selection",
            "Train positioning of hazmat cars",
            "Emergency response information availability",
            "Crew hazmat training certification"
        ],
        primary_authority=[
            "49 CFR Part 174 - Carriage by Rail",
            "49 CFR Part 172 - Hazardous Materials Table and Communications",
            "49 CFR Part 179 - Specifications for Tank Cars"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.HAZMAT_TRANSPORT,
        fragility_score=0.2
    ),

    DoctrineBlock(
        topic="Locomotive Event Recorder Analysis",
        keywords=["event recorder", "locomotive data", "speed recording", "brake application", "black box"],
        conclusion_template="Event recorder data provides critical evidence of train handling and equipment performance during incidents.",
        reasoning_framework="""
Locomotive event recorder analysis framework:
1. Regulatory Requirements (49 CFR 229.135):
   - All locomotives in lead position must have event recorder
   - Minimum data elements: time, train speed, distance, direction
   - Throttle position, brake applications, dynamic brake
   - Head end and rear end brake pipe pressure
   - Data retention minimum 48 hours, overwritten basis

2. Recorded Data Parameters:
   - GPS position and speed (0.1 mph resolution)
   - Throttle position (notch 0-8 or continuous)
   - Independent brake position
   - Automatic brake position (release, service, emergency)
   - Dynamic brake effort
   - Brake pipe pressure (head end)
   - Brake cylinder pressure
   - Main reservoir pressure
   - PTC system status and interventions

3. Accident Investigation Use:
   - Train speed at impact or derailment
   - Brake application timing and magnitude
   - Emergency brake application point
   - Distance traveled during braking
   - Throttle position (power applied or idle)
   - PTC penalty brake application

4. Train Handling Analysis:
   - Excessive speed for conditions
   - Improper brake handling (plugged brakes, graduations)
   - Slack action management
   - Grade descent speed control
   - Emergency brake application response

5. Equipment Performance Verification:
   - Brake system response time
   - Emergency brake propagation through train
   - Dynamic brake effectiveness
   - Brake pipe leakage rates
   - PTC system enforcement actions

6. Data Download and Preservation:
   - FRA Form F 6180.81 - Event Recorder Download
   - Chain of custody procedures
   - Data analysis software (ATDAS, proprietary tools)
   - Graphical plots of speed, brake, throttle over time

7. Correlation with Other Data Sources:
   - Wayside detector data (hotbox, dragging equipment)
   - Signal system event logs
   - PTC back office server logs
   - Crew statements and radio transmissions
        """,
        key_factors=[
            "Event recorder functionality and data completeness",
            "Train speed vs. authorized limits",
            "Brake application timing and magnitude",
            "Throttle position during incident",
            "PTC system status and interventions",
            "Data correlation with other sources",
            "Chain of custody for data download"
        ],
        primary_authority=[
            "49 CFR 229.135 - Event Recorders",
            "FRA Guide for Preparing Accident/Incident Reports",
            "NTSB Railroad Investigation Procedures"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ACCIDENT_INVESTIGATION,
        fragility_score=0.2
    ),

    DoctrineBlock(
        topic="Locomotive Alerter and Vigilance Systems",
        keywords=["alerter", "vigilance", "dead man", "crew alertness", "locomotive control"],
        conclusion_template="Locomotive alerter systems ensure crew vigilance by requiring periodic acknowledgment of alertness.",
        reasoning_framework="""
Locomotive alerter and crew vigilance framework:
1. Regulatory Requirements (49 CFR 229.140):
   - Alerter or automatic train stop/control required
   - System must actuate after predetermined time without crew action
   - Audible alarm before penalty brake application
   - Reset by operating locomotive controls or dedicated reset button

2. Alerter System Operation:
   - Time interval typically 30-60 seconds without throttle, brake, or horn
   - Visual and audible alarm stage (warning)
   - If not acknowledged, penalty brake application
   - Penalty brake is full service application, not emergency
   - Requires reset before train can proceed

3. Control Stand Actions That Reset Alerter:
   - Throttle movement
   - Automatic brake valve movement
   - Independent brake movement
   - Horn actuation
   - Dedicated alerter reset button
   - Bell activation (on some systems)

4. PTC Integration:
   - PTC status display interaction
   - Combined alerter/PTC acknowledgment
   - PTC penalty vs. alerter penalty differentiation
   - Loss of PTC enforcement capability

5. Crew Fatigue and Alertness:
   - Hours of Service Act (49 USC 21103) limits
   - Maximum 12 hours on duty for train crew
   - Minimum 10 hours off duty between tours
   - Cumulative fatigue considerations
   - Dispatcher assignment practices

6. Human Factors in Alerter Effectiveness:
   - Habituation to repetitive alarm
   - "Beating the system" by rocking throttle
   - Automation complacency with PTC
   - Circadian rhythm disruption (night operations)
   - Sleep apnea and other medical conditions

7. Accident Investigation Considerations:
   - Alerter alarm and penalty brake events in recorder data
   - Pattern of alerter acknowledgments (regular vs. delayed)
   - Crew interviews about fatigue and alertness
   - Medical records and medication use
   - Prior discipline or incidents involving same crew
        """,
        key_factors=[
            "Alerter system functionality and testing",
            "Time interval and alarm settings",
            "Event recorder evidence of alerter events",
            "Crew hours of service compliance",
            "Pattern of alerter acknowledgments",
            "PTC system integration and status",
            "Crew fatigue assessment"
        ],
        primary_authority=[
            "49 CFR 229.140 - Alerter",
            "49 USC 21103 - Limitations on Duty Hours of Train Employees",
            "FRA Hours of Service Regulations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.CREW_ALERTNESS,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="End-of-Train Device (EOT) Requirements",
        keywords=["eot", "end of train", "rear end device", "telemetry", "emergency brake", "marker"],
        conclusion_template="End-of-train devices provide rear brake pipe monitoring and emergency brake initiation capability.",
        reasoning_framework="""
End-of-train device (EOT) regulatory and operational framework:
1. Regulatory Requirements (49 CFR Part 232):
   - Required on freight trains without caboose or occupied cab car
   - One-way or two-way telemetry type
   - Rear brake pipe pressure monitoring
   - Emergency brake application capability (two-way EOT)
   - Marker light (flashing rear-facing)

2. EOT Device Types:
   - One-way (rear to head end): Pressure monitoring and marker only
   - Two-way: Adds emergency brake application from head end
   - Sense and Braking Unit (SBU) on rear car
   - Head of Train (HOT) unit in locomotive cab

3. Transmitted Data (Two-Way EOT):
   - Rear brake pipe pressure (PSI)
   - Battery voltage/condition
   - Motion sensor status
   - Air flow sensor (brake application/release)
   - Communication link quality

4. Emergency Brake Application:
   - Conductor can initiate from HOT unit
   - Vents brake pipe at rear of train
   - Faster emergency propagation than head-end only
   - Used for emergency stops, runaways, breaking in two

5. Testing and Inspection Requirements (49 CFR 232.213):
   - Class I brake test includes EOT functional test
   - Communication link verification
   - Pressure reading comparison (within 5 PSI of head end)
   - Marker light operation verification
   - Emergency brake application test (two-way EOT)

6. Breaking in Two Detection:
   - Sudden drop in rear brake pipe pressure
   - Loss of communication link
   - Motion sensor indicates stopped while train still moving
   - Automatic emergency application on some systems

7. Operational Considerations:
   - Radio frequency (typically 457 MHz)
   - Antenna placement and orientation
   - Tunnels and terrain blocking signal
   - Battery life and replacement intervals
   - Cold weather battery performance
        """,
        key_factors=[
            "EOT device type (one-way or two-way)",
            "Brake pipe pressure monitoring accuracy",
            "Communication link reliability",
            "Emergency brake application functionality",
            "Marker light operation",
            "Battery condition and voltage",
            "Testing and inspection compliance"
        ],
        primary_authority=[
            "49 CFR Part 232 Subpart E - End-of-Train Devices",
            "49 CFR 232.213 - Extended Haul Trains",
            "AAR Manual of Standards and Recommended Practices Section M"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.EOT_DEVICES,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Broken Rail Detection Technologies",
        keywords=["broken rail", "track circuit", "rail integrity", "joint bar", "rail fracture", "detection"],
        conclusion_template="Broken rail detection relies on track circuits, joint bar inspection, and ultrasonic testing programs.",
        reasoning_framework="""
Broken rail detection and prevention framework:
1. Track Circuit Detection:
   - Rail serves as electrical conductor
   - Train shunt detects occupied track
   - Broken rail creates open circuit
   - Signal system indicates occupied (red signal aspect)
   - Limitations: Non-signaled (dark) territory has no circuits

2. Audio Frequency Track Circuits (AFTC):
   - More sensitive to rail breaks than DC circuits
   - Detects higher resistance breaks (partial fractures)
   - Joint bond condition critical
   - Ballast resistance affects performance

3. Broken Rail Defect Types:
   - Transverse defects (detail fractures)
   - Bolt hole cracks at joints
   - Engine burn fractures
   - Vertical split heads
   - Horizontal split heads
   - Web fractures

4. Ultrasonic Rail Testing:
   - Detection of internal rail defects before failure
   - Testing frequencies by track class (49 CFR 213.237)
   - Class 4-5 track: annually or tonnage-based
   - Class 6-9 track: more frequent intervals
   - Defect sizing and growth monitoring

5. Joint Bar Inspection (Bolted Joints):
   - Broken or cracked joint bars
   - Loose or missing bolts
   - Battered bolt holes
   - Joint bar bending or crushing
   - Thermite welding to eliminate joints

6. Continuous Welded Rail (CWR) Considerations:
   - Fewer joints eliminate common failure points
   - Rail neutral temperature management prevents pull-aparts
   - Destressing procedures after rail work
   - Cold weather gap formation
   - Broken rail emergency orders (slow orders)

7. Non-Signaled Territory Challenges:
   - No automatic broken rail detection
   - Reliance on visual inspection and train crew reports
   - Wayside detectors (wheel impact load detectors - WILD)
   - Geometry car detection of sudden changes
   - Risk-based inspection prioritization
        """,
        key_factors=[
            "Track circuit type and sensitivity",
            "Ultrasonic testing frequency and results",
            "Joint bar condition and bolt tightness",
            "Rail defect history and trending",
            "CWR neutral temperature maintenance",
            "Signal system functionality",
            "Non-signaled territory inspection practices"
        ],
        primary_authority=[
            "49 CFR 213.233 - Automated Inspection",
            "49 CFR 213.237 - Inspection of Rail",
            "49 CFR 213.119 - Continuous Welded Rail"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.BROKEN_RAIL_DETECTION,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Track Geometry Degradation Analysis",
        keywords=["track geometry", "geometry car", "degradation", "maintenance planning", "exception"],
        conclusion_template="Track geometry degradation trending enables predictive maintenance before FRA limits are exceeded.",
        reasoning_framework="""
Track geometry measurement and degradation framework:
1. Automated Track Geometry Measurement:
   - High-speed geometry cars (up to track speed)
   - Laser-based measurement systems
   - Inertial measurement units (IMU)
   - GPS positioning for exception location
   - Data collection at 0.1 ft to 1 ft intervals

2. Key Geometry Parameters Measured:
   - Gage (distance between rail heads)
   - Alignment (lateral deviation from straight line)
   - Profile/Surface (vertical deviation)
   - Cross level (superelevation difference)
   - Warp (twist over 62 ft base)
   - Curvature and superelevation

3. Exception Reporting:
   - Level 1: Informational, trending toward limits
   - Level 2: Action required, approaching FRA limits
   - Level 3: FRA limit exceeded, immediate remedial action
   - Priority ranking based on safety impact

4. Degradation Rate Analysis:
   - Comparison of successive geometry runs
   - Tons of traffic between measurements
   - Seasonal variation (frost heave, heat expansion)
   - Maintenance effectiveness assessment
   - Predictive models for future degradation

5. Root Cause Analysis:
   - Subgrade or drainage problems
   - Insufficient ballast depth or fouling
   - Crosstie condition and distribution
   - Rail wear patterns (corrugation, wheel burns)
   - Lateral loads in curves (gage widening)

6. Maintenance Prioritization:
   - Safety-critical vs. ride quality issues
   - Traffic volume and train speed
   - Degradation rate and time to FRA limit
   - Maintenance window availability
   - Resource allocation (materials, equipment, crews)

7. Gage Restraint Measurement Systems (GRMS):
   - Measures lateral resistance to gage widening
   - Identifies weak spots before geometry degrades
   - Particularly important in curves
   - Correlates with crosstie condition and ballast support
        """,
        key_factors=[
            "Geometry car measurement frequency",
            "Exception severity and quantity",
            "Degradation rate analysis",
            "Tons of traffic between measurements",
            "Maintenance response timeliness",
            "Root cause identification",
            "GRMS data correlation"
        ],
        primary_authority=[
            "49 CFR 213.233 - Automated Inspection",
            "FRA Track Inspector Field Manual",
            "AREMA Manual for Railway Engineering - Chapter 4"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRACK_GEOMETRY,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Signal System Types and Operations",
        keywords=["signal system", "absolute block", "cab signal", "automatic block", "interlocking"],
        conclusion_template="Railroad signal systems provide collision protection through block occupancy detection and signal aspects.",
        reasoning_framework="""
Railroad signal system framework:
1. Automatic Block Signal (ABS) System:
   - Track divided into blocks by signals
   - Train occupancy detected by track circuits
   - Following train held at red signal (stop)
   - Approach signal (yellow) warns of red ahead
   - Clear signal (green) indicates open blocks ahead

2. Signal Aspects and Indications:
   - Red: Stop (absolute or block occupied)
   - Yellow: Approach (prepare to stop at next signal)
   - Green: Clear (proceed at authorized speed)
   - Flashing yellow: Advance approach
   - Lunar white: Call-on or restricting (yard signals)

3. Centralized Traffic Control (CTC):
   - Dispatcher controls switches and signals remotely
   - Interlocking prevents conflicting routes
   - Track warrant not required in CTC territory
   - Dispatcher authorization for movements

4. Cab Signal Systems:
   - Signal aspects displayed in locomotive cab
   - Supplements or replaces wayside signals
   - Continuous speed enforcement
   - ACSES overlays cab signals for PTC

5. Interlocking Plants:
   - Protect crossing or converging routes
   - Mechanical or electrical locking prevents conflicts
   - Approach locking prevents route change with train approaching
   - Time locking on conflicting routes

6. Dark Territory (Non-Signaled):
   - Track warrant control or direct traffic control
   - No automatic block signals
   - Authority limits and meets specified by dispatcher
   - No automatic broken rail detection

7. Signal System Failures and Procedures:
   - Signal showing most restrictive aspect on failure
   - Dispatcher authority to pass red signal
   - Restricted speed rules in failed signal territory
   - Signal maintainer call-out procedures
        """,
        key_factors=[
            "Signal system type (ABS, CTC, dark territory)",
            "Signal aspect indication and crew understanding",
            "Interlocking logic and route locking",
            "Cab signal operation and enforcement",
            "Signal system maintenance and testing",
            "Dispatcher authorization procedures",
            "Failure mode and safety backup"
        ],
        primary_authority=[
            "49 CFR Part 236 - Rules, Standards, and Instructions Governing Installation, Inspection, Maintenance, and Repair of Signal and Train Control Systems",
            "NORAC Operating Rules (Northeast Operating Rules Advisory Committee)",
            "GCOR - General Code of Operating Rules"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.SIGNAL_SYSTEMS,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="NTSB Railroad Investigation Procedures",
        keywords=["ntsb", "investigation", "accident investigation", "probable cause", "safety recommendation"],
        conclusion_template="NTSB conducts independent investigations to determine probable cause and issue safety recommendations.",
        reasoning_framework="""
NTSB railroad accident investigation framework:
1. NTSB Jurisdiction and Authority:
   - Independent federal agency (not part of DOT or FRA)
   - Investigates significant railroad accidents
   - Highway-rail grade crossing accidents with fatalities
   - Hazmat releases during rail transport
   - Certain passenger train accidents

2. Go-Team Deployment:
   - Rapid response to major accidents
   - Multidisciplinary team (operations, signals, human factors, survival factors)
   - On-scene investigation leadership
   - Evidence preservation and documentation

3. Investigative Groups:
   - Operations Group: Train handling, crew qualifications
   - Signal and Train Control Group: Signal system operation, PTC status
   - Track Group: Track geometry, rail defects, maintenance
   - Mechanical Group: Rolling stock condition, wheel-rail interface
   - Human Performance Group: Crew fatigue, medical factors, training
   - Survival Factors Group: Crashworthiness, evacuation, injuries

4. Evidence Collection and Preservation:
   - Event recorder download and analysis
   - Track geometry measurement at accident site
   - Rolling stock mechanical examination
   - Signal system event logs
   - PTC back office server data
   - Crew interviews and statements
   - Toxicology testing

5. Laboratory Analysis:
   - Metallurgical examination of failed components
   - Rail defect analysis
   - Wheel and axle examination
   - Event recorder data validation

6. Probable Cause Determination:
   - Factual findings from investigation groups
   - Analysis of causal and contributing factors
   - Public hearing for major accidents
   - Board meeting to adopt probable cause
   - Accident report publication

7. Safety Recommendations:
   - Issued to FRA, railroads, labor organizations
   - Address systemic safety issues
   - Track recommendation status (open, closed acceptable, closed unacceptable)
   - Most Wanted List of recurring safety issues
        """,
        key_factors=[
            "NTSB jurisdiction and investigation authority",
            "Evidence collection and preservation",
            "Investigative group factual findings",
            "Probable cause analysis methodology",
            "Safety recommendation issuance and tracking",
            "Independence from regulatory agencies",
            "Public reporting and transparency"
        ],
        primary_authority=[
            "49 USC Chapter 11 - National Transportation Safety Board",
            "NTSB Regulations 49 CFR Part 800-850",
            "NTSB Major Investigation Reports"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ACCIDENT_INVESTIGATION,
        fragility_score=0.2
    ),

    DoctrineBlock(
        topic="Railroad Bridge Inspection and Safety",
        keywords=["bridge", "structure", "inspection", "bridge safety", "load rating", "clearance"],
        conclusion_template="Railroad bridge safety requires regular inspection, load rating verification, and clearance maintenance.",
        reasoning_framework="""
Railroad bridge inspection and safety framework:
1. Bridge Inspection Requirements (49 CFR 237):
   - Annual inspection of all railroad bridges
   - Qualified bridge inspectors
   - Written inspection reports
   - Defect remediation tracking
   - Bridge management programs

2. Bridge Load Rating:
   - Cooper E rating system (E40, E60, E80)
   - Gross rail load (GRL) for heavier cars
   - Axle load limits
   - Speed restrictions for heavy loads
   - Special movement permits

3. Bridge Types and Inspection Focus:
   - Steel truss bridges (member condition, connections)
   - Steel girder bridges (flanges, webs, bearings)
   - Concrete bridges (cracking, spalling, rebar corrosion)
   - Timber bridges (decay, crushing, insect damage)
   - Movable bridges (operating machinery, electrical systems)

4. Critical Inspection Areas:
   - Bearings and expansion devices
   - Deck and track support
   - Substructure (piers, abutments)
   - Waterway scour around piers
   - Fracture-critical members

5. Vertical and Horizontal Clearances:
   - Overhead clearance for double-stack trains (20 ft 2 in. minimum)
   - Horizontal clearance (side clearance to structures)
   - Clearance diagrams (AAR Plate designations)
   - Clearance verification after track work

6. Bridge Management Systems:
   - Inventory of all bridges
   - Inspection history and defect tracking
   - Planned maintenance and capital programs
   - Risk-based prioritization
   - Regulatory compliance tracking

7. Scour Critical Bridges:
   - Bridges over waterways subject to scour
   - Underwater inspection requirements
   - Scour monitoring during floods
   - Action plans for scour critical conditions
        """,
        key_factors=[
            "Bridge inspection frequency and qualification",
            "Load rating vs. current traffic",
            "Defect identification and remediation",
            "Clearance adequacy for equipment",
            "Scour susceptibility and monitoring",
            "Fracture-critical member inspection",
            "Bridge management program effectiveness"
        ],
        primary_authority=[
            "49 CFR Part 237 - Bridge Safety Standards",
            "AREMA Manual Chapter 15 - Steel Structures",
            "AREMA Manual Chapter 8 - Concrete Structures and Foundations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRACK_SAFETY,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Freight Car Brake System Requirements",
        keywords=["air brake", "brake system", "freight car", "brake inspection", "brake test"],
        conclusion_template="Freight car brake systems require regular inspection, testing, and compliance with FRA Part 232.",
        reasoning_framework="""
Freight car brake system regulatory framework:
1. Brake System Components (49 CFR Part 232):
   - Brake pipe (train line)
   - Auxiliary reservoir
   - Emergency reservoir
   - Control valve (AB, ABD, DB types)
   - Brake cylinder
   - Brake rigging and levers
   - Brake shoes and wheels

2. Brake Test Types:
   - Class I (Initial Terminal): Full inspection and test
   - Class IA: 1,000-mile or 24-hour inspection
   - Class II: Intermediate test for added/removed cars
   - Class III: Transfer train test
   - Continuity test: Minimum brake test

3. Class I Brake Test Requirements:
   - Visual inspection of all brake equipment
   - Leakage test (brake pipe reduction and holding)
   - Application and release test
   - Brake cylinder piston travel inspection
   - Angle cock and air hose inspection
   - Retaining valve position

4. Piston Travel Standards:
   - Hand brake applied: 6 to 9 inches typical
   - Excessive piston travel indicates adjustment needed
   - Insufficient piston travel indicates brake binding
   - Adjustment procedures by car type

5. Single Car Test (FRA Part 232 Appendix D):
   - Pre-departure inspection for certain cars
   - Hazmat cars, passenger equipment
   - Cars out of interchange for repairs
   - Brake application and release verification
   - Piston travel and rigging condition

6. Empty/Load Brake Systems:
   - Variable load valve adjusts braking force
   - Empty position: reduced brake cylinder pressure
   - Load position: full brake cylinder pressure
   - Proper setting critical for train handling

7. Defective Brake Conditions:
   - Brakes failed to apply or release
   - Excessive piston travel (out of adjustment)
   - Air leaks (brake pipe, reservoirs, cylinder)
   - Broken or binding rigging
   - Worn brake shoes (less than 1/2 inch thickness)
        """,
        key_factors=[
            "Brake test type and frequency compliance",
            "Piston travel within specifications",
            "Brake pipe leakage rate",
            "Component condition and functionality",
            "Empty/load setting accuracy",
            "Brake shoe thickness adequacy",
            "Qualified brake inspector certification"
        ],
        primary_authority=[
            "49 CFR Part 232 - Brake System Safety Standards for Freight and Other Non-Passenger Trains",
            "AAR Field Manual of the AAR Interchange Rules",
            "FRA Brake System Inspection Guide"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.LOCOMOTIVE_SAFETY,
        fragility_score=0.2
    ),

    DoctrineBlock(
        topic="Railroad Worker Safety and Roadway Worker Protection",
        keywords=["roadway worker", "worker safety", "iws", "on-track safety", "lookout", "foul time"],
        conclusion_template="Roadway worker protection requires on-track safety procedures per 49 CFR Part 214.",
        reasoning_framework="""
Roadway worker protection framework (49 CFR Part 214):
1. Roadway Worker Definition:
   - Any employee whose duties require fouling a track
   - Fouling: being within 4 feet of field side of rail
   - Includes track maintainers, signal personnel, bridge inspectors

2. On-Track Safety Methods:
   - Working Limits (exclusive track occupancy)
   - Inaccessible Track (physical barriers prevent train entry)
   - Foul Time (dispatcher authority for specific time period)
   - Train Approach Warning (lookout with communication)
   - Definite Train Location (visual sight of train)

3. Individual Worker Safety (IWS):
   - Single worker qualification
   - Train approach detection responsibility
   - Clear of track 15 seconds before train arrival
   - Audible train approach alert (horn, bell)

4. Lone Worker Requirements:
   - IWS qualification and annual training
   - Ability to hear and see approaching trains
   - No headphones or devices that impair hearing
   - Alternative protection if hearing/sight impaired

5. Working Limits Establishment:
   - Dispatcher grants exclusive authority
   - Physical markers at limits (flags, signs)
   - Red zone authority form
   - Release procedures when work complete

6. Lookout Procedures:
   - Dedicated employee watching for trains
   - Positioned with adequate sight distance
   - Reliable communication to workers (radio, hand signals)
   - Cannot perform other duties while serving as lookout

7. Roadway Maintenance Machines (RMM):
   - Movement authority on track
   - On-track safety for machine operators
   - Blue signal protection for maintenance
   - Machine clearances and visibility
        """,
        key_factors=[
            "On-track safety method appropriateness",
            "Worker qualification and training",
            "Communication reliability",
            "Sight distance adequacy",
            "Authority establishment and release",
            "Lookout positioning and attention",
            "IWS lone worker procedures"
        ],
        primary_authority=[
            "49 CFR Part 214 - Railroad Workplace Safety",
            "49 CFR 214.329 - Working Limits",
            "FRA Guide to Roadway Worker Protection"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ACCIDENT_INVESTIGATION,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Tank Car Thermal Protection Requirements",
        keywords=["tank car", "thermal protection", "fire", "safety vent", "jacket", "insulation"],
        conclusion_template="Tank car thermal protection prevents BLEVE during fire exposure through insulation and pressure relief.",
        reasoning_framework="""
Tank car thermal protection framework:
1. BLEVE Risk (Boiling Liquid Expanding Vapor Explosion):
   - Fire exposure heats tank contents
   - Liquid vaporization increases tank pressure
   - Tank metal weakens at elevated temperature
   - Catastrophic rupture if pressure exceeds weakened tank strength
   - Fireball and projectile hazards

2. Thermal Protection Types (49 CFR Part 179):
   - Spray-on insulation (thermal barrier)
   - Jacket with insulation (metal jacket over insulation)
   - Thickness requirements by hazard class
   - Thermal resistance rating (typically 0.5 to 2 hour)

3. Pressure Relief Devices:
   - Safety relief valves (SRV) on pressure cars
   - Pressure relief valves (PRV) on non-pressure cars
   - Set pressure vs. tank test pressure
   - Capacity requirements for fire exposure
   - Reclosing vs. non-reclosing types

4. Tank Car Construction Standards:
   - Shell thickness for hazard class
   - Head shield protection (1/2 inch minimum)
   - Top fittings protection (jacket or housing)
   - Bottom outlet valve protection
   - Coupler vertical restraint (to prevent disengagement)

5. DOT-117 Enhanced Standards (for flammable liquids):
   - 9/16 inch minimum shell thickness
   - 11-gauge jacket (1/8 inch)
   - Thermal protection to 0.3 hour
   - Full-height head shields
   - Pressure relief device capacity for fire exposure

6. Fire Exposure Testing:
   - Pool fire or jet fire simulation
   - Tank pressure and temperature monitoring
   - PRD actuation timing
   - Thermal protection effectiveness
   - Post-fire tank integrity

7. Emergency Response Considerations:
   - Firefighter approach hazards (BLEVE radius)
   - Water cooling effectiveness
   - Foam application for flammable liquids
   - Evacuation distance recommendations (ERG)
   - Tank car orientation and valve accessibility
        """,
        key_factors=[
            "Thermal protection type and thickness",
            "Pressure relief device capacity and setting",
            "Tank car specification compliance",
            "Fire exposure duration and intensity",
            "Tank contents and hazard classification",
            "Emergency response procedures",
            "Historical tank car accident data"
        ],
        primary_authority=[
            "49 CFR Part 179 - Specifications for Tank Cars",
            "NTSB Special Investigation Report - Hazardous Materials Rail Tank Car Safety",
            "FRA Emergency Order 28 (Crude Oil Transport)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.HAZMAT_TRANSPORT,
        fragility_score=0.2
    ),

    DoctrineBlock(
        topic="Railroad Dispatching and Train Authority",
        keywords=["dispatcher", "train authority", "track warrant", "train order", "ctc", "dispatching"],
        conclusion_template="Train movement authority prevents collisions through exclusive track occupancy or signal indication.",
        reasoning_framework="""
Railroad dispatching and authority framework:
1. Authority Types:
   - Signal Indication (CTC, ABS): Signal aspect authorizes movement
   - Track Warrant: Written authority for specific track limits
   - Track and Time: Authority for specific time period
   - Direct Traffic Control (DTC): Verbal authority with documentation
   - Yard Limits: Restricted authority within yard boundaries

2. Track Warrant System:
   - Dispatcher issues written authority (Form EC-1 or equivalent)
   - Specific main track limits (milepost to milepost)
   - Crew copies and reads back warrant verbatim
   - Dispatcher confirms correct readback
   - Release procedures when movement complete

3. Centralized Traffic Control (CTC):
   - Dispatcher controls signals and switches remotely
   - Signal aspect provides authority
   - No additional track warrant needed in CTC territory
   - Conflicting routes prevented by interlocking logic

4. Meet and Pass Coordination:
   - Opposing trains on single track
   - One train takes siding, other proceeds on main
   - Authority limits prevent overlap
   - Radio communication confirms clearance

5. Dispatcher Workload and Error Risk:
   - Multiple subdivisions under single dispatcher
   - Fatigue and distraction factors
   - Error-likely situations (complex meets, detours)
   - Computer-aided dispatching (CAD) systems

6. Dark Territory Operations:
   - No automatic block signals
   - Complete reliance on dispatcher authority
   - Crew must protect against opposing movements
   - Restricted speed when authority limits uncertain

7. Emergency Authority Revocation:
   - Dispatcher discovers error in issued authority
   - Immediate contact with affected train
   - Emergency broadcast on all channels
   - Stop indication on all signals if CTC
        """,
        key_factors=[
            "Authority type and specificity",
            "Crew understanding and readback accuracy",
            "Dispatcher workload and fatigue",
            "Communication system reliability",
            "CAD system use and effectiveness",
            "Interlocking logic in CTC territory",
            "Emergency procedures and crew training"
        ],
        primary_authority=[
            "GCOR Rule 9 - Train Dispatchers Authority",
            "NORAC Rule 241 - Track Warrants",
            "49 CFR Part 236 - Train Control Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.SIGNAL_SYSTEMS,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Wheel Impact Load Detection (WILD)",
        keywords=["wild", "wheel impact", "detector", "flat wheel", "wayside detector", "impact load"],
        conclusion_template="Wheel impact load detectors identify defective wheels causing high impact forces before failure.",
        reasoning_framework="""
Wheel impact load detection framework:
1. WILD System Operation:
   - Strain gages installed in rail
   - Measure vertical wheel load at rail
   - High-impact loads indicate wheel defects
   - Real-time data transmission to dispatcher

2. Wheel Defects Detected:
   - Flat spots (wheel slides on rail)
   - Shells and shelling (surface cracks)
   - Out-of-round wheels
   - Loose wheels on axle
   - Built-up tread metal

3. Impact Load Thresholds:
   - Low impact: 90,000 to 120,000 lbs
   - Medium impact: 120,000 to 150,000 lbs
   - High impact: 150,000 to 200,000 lbs
   - Critical impact: Over 200,000 lbs (immediate train stop)

4. AAR Interchange Rules:
   - Wheel condemned for flat spot 2.5 inches or longer
   - Shelled or spalled tread surface
   - Thermal damage (slide damage)
   - Hollow worn wheels (tread thickness)

5. Dispatcher Response Procedures:
   - Low impact: Advisory message to crew
   - Medium impact: Inspection at next forward location
   - High impact: Stop and inspect immediately
   - Critical impact: Emergency stop, do not move until repaired

6. Flat Spot Formation:
   - Emergency brake application with wheels locked
   - Defective brake releasing (stuck brakes)
   - Low adhesion conditions (wet rail, leaves)
   - Length of slide determines flat spot size

7. WILD System Limitations:
   - Point measurement (not continuous)
   - Seasonal variations in ambient temperature
   - Rail condition affects baseline readings
   - Calibration drift over time
        """,
        key_factors=[
            "Impact load magnitude vs. thresholds",
            "Wheel defect type and severity",
            "Dispatcher response timeliness",
            "Train speed and tonnage",
            "WILD system calibration accuracy",
            "Inspection and repair procedures",
            "AAR interchange rule compliance"
        ],
        primary_authority=[
            "AAR Field Manual of AAR Interchange Rules - Rule 41",
            "49 CFR Part 215 - Railroad Freight Car Safety Standards",
            "WILD System Installation and Operating Guidelines"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.DERAILMENT_PREVENTION,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Passenger Rail Crashworthiness Standards",
        keywords=["crashworthiness", "passenger", "collision", "car strength", "crush zone", "compartmentalization"],
        conclusion_template="Passenger rail crashworthiness standards protect occupants through structural integrity and energy absorption.",
        reasoning_framework="""
Passenger rail crashworthiness framework:
1. Regulatory Standards (49 CFR Part 238):
   - Buff strength: 800,000 lbs minimum (Tier I)
   - Collision posts and corner posts strength
   - Anti-climbing mechanisms between cars
   - Glazing retention and breakage characteristics
   - Interior furnishing flammability

2. Crashworthiness Design Principles:
   - Compartmentalization (preserve occupant space)
   - Structural integrity (prevent car telescoping)
   - Energy absorption (crush zones at car ends)
   - Occupant protection (seat strength, interior padding)

3. Collision Post Requirements:
   - Vertical posts at car ends
   - Resist 300,000 lb lateral load
   - Prevent override and telescoping
   - Corner post reinforcement

4. Anti-Climber Design:
   - Interlocking couplers or end sills
   - Prevent one car from riding over another
   - Alignment maintained during collision
   - Tested under buff load conditions

5. Glazing (Window) Standards:
   - Laminated or tempered glass
   - Retention in frames during collision
   - Breakage pattern (granular vs. sharp edges)
   - Emergency egress window marking and operation

6. Seat Strength and Attachment:
   - Forward-facing seat back strength
   - Withstand occupant loading in collision
   - Attachment to car structure
   - Padding and energy absorption

7. Post-Collision Survivability:
   - Emergency egress routes and marking
   - Rescue access (doors, windows)
   - Fire safety (interior materials, suppression)
   - Communications (passenger to crew, crew to dispatch)
        """,
        key_factors=[
            "Car structural design and testing",
            "Buff strength and collision post adequacy",
            "Anti-climber effectiveness",
            "Glazing retention and breakage",
            "Seat strength and attachment",
            "Emergency egress accessibility",
            "Post-collision fire safety"
        ],
        primary_authority=[
            "49 CFR Part 238 - Passenger Equipment Safety Standards",
            "FRA Passenger Equipment Safety Standards Final Rule",
            "NTSB Passenger Rail Crashworthiness Reports"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.LOCOMOTIVE_SAFETY,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Railroad Crossing Sight Distance Requirements",
        keywords=["sight distance", "crossing", "stopping", "decision", "visibility", "obstruction"],
        conclusion_template="Adequate sight distance at grade crossings allows drivers to detect trains and stop safely.",
        reasoning_framework="""
Grade crossing sight distance framework:
1. Stopping Sight Distance (SSD):
   - Distance required for driver to stop vehicle
   - Components: perception time, reaction time, braking distance
   - Perception-reaction time typically 2.5 seconds
   - Braking distance varies by speed and road conditions

2. Decision Sight Distance (DSD):
   - Greater than SSD to allow decision-making
   - Driver must detect train, judge speed, decide to stop
   - AASHTO guidelines for DSD by approach speed
   - More critical at complex or unusual crossings

3. Sight Triangle Requirements:
   - Clear zone along track and approach road
   - Measured from driver eye position (3.5 ft above road)
   - To train detection point (15 ft above track centerline)
   - Vegetation, structures, terrain must not obstruct

4. Train Detection Distance:
   - Distance along track where driver can see approaching train
   - Function of train speed and vehicle approach speed
   - Minimum sight distance to allow safe crossing
   - MUTCD formula: d = 1.47 * V * t
     (d = distance in ft, V = train speed mph, t = time in seconds)

5. Sight Distance Calculation:
   - Vehicle approach speed determines time needed
   - Train speed determines distance traveled during approach
   - Crossing angle affects sight triangle geometry
   - Distance from track to stop line (storage distance)

6. Obstructions and Mitigation:
   - Buildings, vegetation, stored equipment
   - Terrain (hills, cuts, curves)
   - Parked vehicles or seasonal crops
   - Mitigation: vegetation removal, advance warning signs, signal upgrades

7. Diagnostic Reviews for Inadequate Sight Distance:
   - FRA-led field reviews
   - State DOT participation
   - Recommendation: active warning devices if SSD cannot be achieved
   - Crossing closure as alternative
        """,
        key_factors=[
            "Vehicle approach speed",
            "Train speed and frequency",
            "Crossing angle geometry",
            "Obstruction identification and removal",
            "Stopping sight distance adequacy",
            "Active warning device presence",
            "Diagnostic team review recommendations"
        ],
        primary_authority=[
            "MUTCD (Manual on Uniform Traffic Control Devices) Part 8",
            "AASHTO Policy on Geometric Design of Highways and Streets",
            "23 CFR 646 - Railroad-Highway Grade Crossings"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.GRADE_CROSSINGS,
        fragility_score=0.4
    ),

    DoctrineBlock(
        topic="Locomotive Fuel System Safety",
        keywords=["fuel", "diesel", "fuel tank", "fuel leak", "fire", "locomotive fuel"],
        conclusion_template="Locomotive fuel system integrity prevents fires through leak prevention and crashworthy design.",
        reasoning_framework="""
Locomotive fuel system safety framework:
1. Regulatory Requirements (49 CFR Part 229):
   - Fuel tank securement and protection
   - Fuel line routing and protection
   - Fuel shutoff capability
   - Fire detection and suppression

2. Fuel Tank Design:
   - Capacity typically 3,000 to 5,000 gallons
   - Mounting on locomotive underframe
   - Collision protection (anticlimbers, end sills)
   - Venting to prevent pressure buildup

3. Fuel System Components:
   - Main fuel tank
   - Fuel lines (supply and return)
   - Fuel pumps and filters
   - Fuel injectors or fuel nozzles (diesel engine)
   - Overflow and vent lines

4. Fuel Leak Hazards:
   - Fire ignition from hot engine surfaces
   - Smoke and fumes in cab or engine room
   - Slip hazard on walkways
   - Environmental contamination

5. Collision Fuel Release Prevention:
   - Crashworthy fuel tank design
   - Fuel line breakaway fittings
   - Automatic fuel shutoff valves
   - Tank mounting to resist separation in collision

6. Fire Detection and Suppression:
   - Engine room fire detectors (heat and smoke)
   - Automatic CO2 or Halon suppression systems
   - Manual pull stations for crew activation
   - Fuel shutoff integration with fire suppression

7. Fuel Spill Response:
   - Crew procedures for fuel leak detection
   - Engine shutdown and fuel shutoff
   - Fire extinguisher availability
   - Environmental reporting requirements (EPA, state agencies)
        """,
        key_factors=[
            "Fuel tank condition and mounting",
            "Fuel line integrity and routing",
            "Fire detection system functionality",
            "Suppression system charge and readiness",
            "Fuel shutoff valve operation",
            "Collision protection adequacy",
            "Crew training on fuel leak procedures"
        ],
        primary_authority=[
            "49 CFR Part 229 - Railroad Locomotive Safety Standards",
            "AAR Locomotive Crashworthiness Requirements",
            "FRA Locomotive Fire Safety Guidance"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.LOCOMOTIVE_SAFETY,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Railroad Trespasser Prevention Measures",
        keywords=["trespasser", "intrusion", "fencing", "pedestrian", "right of way", "trespassing"],
        conclusion_template="Trespasser prevention combines physical barriers, signage, education, and enforcement to reduce intrusions.",
        reasoning_framework="""
Railroad trespasser prevention framework:
1. Trespasser Statistics and Risk:
   - Leading cause of rail-related deaths (approximately 500 annually)
   - Pedestrians struck by trains on tracks
   - High-risk locations: urban areas, adjacent to homeless camps, shortcuts
   - Time of day: evening and night hours

2. Physical Barriers:
   - Right-of-way fencing (chain link, barbed wire)
   - Fence height (6 to 8 feet typical)
   - Gates at access points
   - Vegetation management for visibility

3. Signage and Warnings:
   - "No Trespassing" signs at intervals
   - "Danger - Railroad Tracks" warnings
   - Multilingual signs in diverse communities
   - Emergency contact information (Operation Lifesaver)

4. Education and Outreach:
   - Operation Lifesaver public awareness programs
   - School presentations on railroad safety
   - Community engagement in high-risk areas
   - Social media and advertising campaigns

5. Law Enforcement Collaboration:
   - Trespassing is violation of state law (misdemeanor or felony)
   - Railroad police patrols in high-incidence areas
   - Citations and arrests for repeat offenders
   - Video surveillance and detection systems

6. High-Risk Location Mitigation:
   - Pedestrian underpasses or overpasses
   - Lighting in areas with pedestrian activity
   - Fence repairs and breach closure
   - Removal of attractants (homeless encampments with social services)

7. Intrusion Detection Technology:
   - Thermal cameras at key locations
   - Motion sensors along right-of-way
   - Alert systems to dispatch and train crews
   - Video analytics for automated detection
        """,
        key_factors=[
            "Fence condition and coverage",
            "Signage visibility and adequacy",
            "Law enforcement presence and activity",
            "Community education program reach",
            "High-risk location identification",
            "Intrusion detection system deployment",
            "Trespasser incident trending"
        ],
        primary_authority=[
            "State Trespassing Laws (varies by state)",
            "FRA Trespasser Prevention Guidance",
            "Operation Lifesaver Educational Materials"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ACCIDENT_INVESTIGATION,
        fragility_score=0.4
    ),

    DoctrineBlock(
        topic="Rail Fatigue and Defect Growth",
        keywords=["rail fatigue", "defect growth", "crack", "fracture mechanics", "stress", "cycles"],
        conclusion_template="Rail fatigue defects grow over repeated load cycles, requiring detection before critical size.",
        reasoning_framework="""
Rail fatigue and defect growth framework:
1. Fatigue Crack Initiation:
   - Stress concentration at rail surface or internal defects
   - Repeated wheel loading (millions of cycles)
   - Manufacturing defects (inclusions, pipe, seams)
   - Corrosion pits or wear concentrating stress

2. Defect Growth Mechanisms:
   - Paris Law: crack growth per cycle vs. stress intensity
   - Growth rate accelerates as crack size increases
   - Critical crack size leads to sudden fracture
   - Environmental factors (corrosion, temperature)

3. Common Rail Defect Types:
   - Detail fractures (transverse defects from bolt holes)
   - Horizontal split heads (longitudinal internal cracks)
   - Vertical split heads (vertical plane cracks)
   - Engine burn fractures (thermal damage and cracking)
   - Bolt hole cracks (stress concentration at joints)

4. Ultrasonic Testing for Defect Detection:
   - Angle beam probes for transverse defects
   - Straight beam probes for horizontal defects
   - Testing frequencies based on tonnage (49 CFR 213.237)
   - Defect sizing and growth monitoring between tests

5. Factors Affecting Fatigue Life:
   - Rail steel metallurgy (carbon content, microstructure)
   - Rail profile and contact stress distribution
   - Axle loads and traffic tonnage
   - Track curvature and lateral forces
   - Residual stresses from manufacturing or grinding

6. Rail Grinding for Fatigue Mitigation:
   - Remove surface cracks before penetration
   - Restore optimal rail profile
   - Reduce contact stress concentrations
   - Introduce compressive residual stress

7. Critical Defect Response:
   - Immediate speed restriction or track closure
   - Rail replacement before train operations resume
   - Analysis of adjacent rail for similar defects
   - Review of inspection and testing intervals
        """,
        key_factors=[
            "Cumulative tonnage and load cycles",
            "Ultrasonic testing frequency and results",
            "Defect growth rate between inspections",
            "Rail grinding effectiveness",
            "Stress concentration locations",
            "Rail metallurgy and manufacturing quality",
            "Critical defect size for fracture"
        ],
        primary_authority=[
            "49 CFR 213.237 - Inspection of Rail",
            "AREMA Manual Chapter 4 - Rail",
            "Fracture Mechanics Research (Transportation Technology Center)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRACK_SAFETY,
        fragility_score=0.2
    ),

    DoctrineBlock(
        topic="Passenger Train Emergency Evacuation",
        keywords=["evacuation", "emergency", "egress", "passenger", "train evacuation", "emergency exits"],
        conclusion_template="Passenger train emergency evacuation requires accessible exits, crew training, and passenger awareness.",
        reasoning_framework="""
Passenger train emergency evacuation framework:
1. Regulatory Requirements (49 CFR Part 238):
   - Emergency exit windows marked and operational
   - Exit instructions visible to passengers
   - Crew emergency evacuation training
   - Emergency lighting and communication

2. Emergency Exit Types:
   - Side doors (primary exits)
   - End doors between cars
   - Emergency exit windows (breakable or removable)
   - Roof hatches (older equipment)

3. Emergency Window Requirements:
   - Marked with reflective "Emergency Exit" label
   - Instructions for operation (kick out, pull handle)
   - Minimum dimensions for passage (26 inches wide)
   - Distribution along car length

4. Evacuation Scenarios:
   - Fire or smoke in car
   - Collision with car damage blocking doors
   - Derailment with car on side or overturned
   - Water or environmental hazard

5. Crew Responsibilities:
   - Assess situation and determine evacuation need
   - Open exits and assist passengers
   - Direct passengers away from hazard
   - Account for passengers after evacuation
   - Communicate with dispatcher and emergency responders

6. Passenger Awareness:
   - Safety briefing announcements
   - Emergency instruction cards in seat backs
   - Exit location identification before emergency
   - Assistance for mobility-impaired passengers

7. Challenges in Emergency Evacuation:
   - High platforms vs. ballast level (fall hazard)
   - Adjacent track with train movements
   - Third rail or catenary electrical hazards
   - Night or low visibility conditions
   - Passenger panic and crowding at exits
        """,
        key_factors=[
            "Emergency exit availability and condition",
            "Crew training and qualification",
            "Passenger awareness and instructions",
            "Exit accessibility in accident conditions",
            "Emergency lighting functionality",
            "Communication system operation",
            "Evacuation route hazards (tracks, electrical)"
        ],
        primary_authority=[
            "49 CFR Part 238 Subpart D - Inspection and Testing Requirements",
            "FRA Passenger Train Emergency Preparedness Final Rule",
            "NTSB Passenger Evacuation Recommendations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.LOCOMOTIVE_SAFETY,
        fragility_score=0.3
    ),

    DoctrineBlock(
        topic="Superelevation and Curve Maintenance",
        keywords=["superelevation", "curve", "cant", "equilibrium", "underbalance", "rail rollover"],
        conclusion_template="Proper superelevation balances lateral forces in curves, preventing rail rollover and passenger discomfort.",
        reasoning_framework="""
Superelevation and curve maintenance framework:
1. Superelevation Principles:
   - Outer rail elevated above inner rail
   - Balances centrifugal force on train in curve
   - Equilibrium speed: lateral force equals gravitational component
   - Underbalance: speed above equilibrium (outward force)
   - Overbalance: speed below equilibrium (inward force, rare)

2. Superelevation Calculation:
   - E = 0.0007 * D * V^2 (E in inches, D = degree of curve, V = speed mph)
   - Actual superelevation = equilibrium elevation minus underbalance
   - FRA limits: 6 inches maximum for freight, 8 inches for passenger

3. Underbalance Limits (49 CFR 213.57):
   - Unbalanced superelevation (Eu) = actual centrifugal force
   - Class 1-5: 3 inches max underbalance
   - Class 6-9: up to 6 inches for passenger with qualification testing
   - Prevents excessive lateral force on outer rail

4. Rail Rollover Risk:
   - High lateral forces in curves can rotate outer rail
   - Rail anchors and tie plates resist lateral movement
   - Gage restraint critical (crosstie condition, ballast support)
   - Low rail (inner rail) can also roll under certain conditions

5. Spirals (Transition Curves):
   - Gradual increase in curvature entering main curve
   - Gradual increase in superelevation (runoff)
   - Prevents sudden lateral force change
   - Length of spiral based on speed and superelevation change

6. Superelevation Maintenance:
   - Surfacing and lining operations to restore design superelevation
   - Measurement by track geometry car
   - Cross level (difference in rail elevation) vs. design
   - Degradation from ballast settlement and lateral forces

7. Speed vs. Superelevation Mismatches:
   - Overspeed in curve exceeds safe underbalance
   - PTC enforcement of permanent speed restrictions
   - Temporary speed restrictions for degraded superelevation
   - Passenger discomfort at excessive underbalance or overbalance
        """,
        key_factors=[
            "Actual superelevation vs. design",
            "Train speed vs. equilibrium speed",
            "Underbalance magnitude and FRA limits",
            "Gage restraint and rail rollover risk",
            "Spiral length and superelevation runoff",
            "Track geometry degradation rate",
            "Speed restriction enforcement"
        ],
        primary_authority=[
            "49 CFR 213.57 - Curves; elevation and speed limitations",
            "AREMA Manual Chapter 5 - Track Geometry",
            "FRA Track Safety Standards Compliance Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TRACK_GEOMETRY,
        fragility_score=0.3
    )
]

# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.query_count = 0
        self.total_latency_ms = 0.0
        self.errors: List[Dict[str, Any]] = []
        self.doctrine_hits: Counter = Counter()
        self.start_time = datetime.now(timezone.utc)

    def record_query(self, latency_ms: float, doctrines: List[str], error: Optional[str] = None):
        self.query_count += 1
        self.total_latency_ms += latency_ms
        for doctrine in doctrines:
            self.doctrine_hits[doctrine] += 1
        if error:
            self.errors.append({"timestamp": datetime.now(timezone.utc).isoformat(), "error": error})

    def get_metrics(self) -> Dict[str, Any]:
        uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        avg_latency = self.total_latency_ms / self.query_count if self.query_count > 0 else 0.0
        return {
            "total_queries": self.query_count,
            "avg_latency_ms": round(avg_latency, 2),
            "uptime_seconds": round(uptime, 2),
            "error_count": len(self.errors),
            "top_doctrines": dict(self.doctrine_hits.most_common(10))
        }

telemetry = TelemetryCollector()

# ============================================================================
# SEMANTIC NORMALIZATION
# ============================================================================

RAIL_SAFETY_TERM_MAP = {
    "positive train control": ["ptc", "i-etms", "acses", "e-atc", "train control"],
    "grade crossing": ["highway rail crossing", "level crossing", "road crossing"],
    "derailment": ["train wreck", "off track", "wheel climb"],
    "hazmat": ["hazardous materials", "dangerous goods", "toxic inhalation hazard"],
    "event recorder": ["black box", "locomotive data recorder", "edr"],
    "alerter": ["dead man", "vigilance device", "crew alertness"],
    "end of train": ["eot", "rear end device", "telemetry device"],
    "broken rail": ["rail fracture", "rail break", "track break"],
    "track geometry": ["alignment", "surface", "gage", "cross level"],
    "signal system": ["automatic block", "abs", "ctc", "cab signal"],
    "wheel impact": ["wild", "flat wheel", "wheel defect"],
    "superelevation": ["cant", "banking", "curve elevation"]
}

def normalize_query(question: str) -> str:
    q_lower = question.lower()
    for canonical, variants in RAIL_SAFETY_TERM_MAP.items():
        for variant in variants:
            if variant in q_lower and canonical not in q_lower:
                q_lower = q_lower.replace(variant, canonical)
    return q_lower

# ============================================================================
# DOCTRINE MATCHING ENGINE
# ============================================================================

def find_matching_doctrines(question: str, top_n: int = 5) -> List[Tuple[DoctrineBlock, float]]:
    normalized = normalize_query(question)
    matches = []
    for doctrine in DOCTRINE_CACHE:
        score = doctrine.matches(normalized)
        if score > 0:
            matches.append((doctrine, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:top_n]

# ============================================================================
# THREE-LAYER RESPONSE ENGINE
# ============================================================================

async def three_layer_response(
    question: str,
    mode: ResponseMode,
    zone: AnalysisZone,
    context: Optional[Dict[str, Any]]
) -> QueryResponse:
    start_time = datetime.now(timezone.utc)

    # Layer 1: Doctrine Cache (0-200ms target)
    matched_doctrines = find_matching_doctrines(question, top_n=5)

    if not matched_doctrines:
        logger.warning(f"No doctrine matches for question: {question[:100]}")
        return QueryResponse(
            answer="No specific rail safety doctrine matches found. Please refine your question with more specific technical terms.",
            confidence=ConfidenceLevel.DISCLOSURE,
            doctrines_triggered=[],
            reasoning_chain=["No matching doctrines in cache"],
            authorities=[],
            warnings=["Question may be outside rail safety scope"],
            mode=mode,
            zone=zone,
            determinism_hash=compute_hash(question, mode, zone),
            latency_ms=0.0
        )

    # Build response from top doctrines
    triggered_doctrines = []
    reasoning_chain = []
    authorities_cited = []
    warnings = []

    for doctrine, score in matched_doctrines[:3]:
        triggered_doctrines.append(doctrine.topic)
        reasoning_chain.append(f"[{doctrine.topic}] Match score: {score:.2f}")
        authorities_cited.extend(doctrine.primary_authority)
        doctrine.triggered_count += 1
        doctrine.last_triggered = datetime.now(timezone.utc)

    # Generate answer based on mode
    primary_doctrine = matched_doctrines[0][0]

    if mode == ResponseMode.FAST:
        answer = f"{primary_doctrine.conclusion_template}\n\nKey factors: {', '.join(primary_doctrine.key_factors[:5])}"
    elif mode == ResponseMode.DEFENSE:
        answer = f"{primary_doctrine.conclusion_template}\n\n{primary_doctrine.reasoning_framework[:500]}...\n\nPrimary Authority:\n"
        answer += "\n".join(f"- {auth}" for auth in primary_doctrine.primary_authority)
    else:  # MEMO
        answer = f"RAIL SAFETY ANALYSIS MEMORANDUM\n\nISSUE: {question}\n\n"
        answer += f"CONCLUSION:\n{primary_doctrine.conclusion_template}\n\n"
        answer += f"ANALYSIS:\n{primary_doctrine.reasoning_framework[:1000]}\n\n"
        answer += f"KEY FACTORS:\n" + "\n".join(f"{i+1}. {factor}" for i, factor in enumerate(primary_doctrine.key_factors))
        answer += f"\n\nAUTHORITY:\n" + "\n".join(f"- {auth}" for auth in primary_doctrine.primary_authority)

    # Apply epistemic guardrails
    if primary_doctrine.fragility_score > 0.6:
        warnings.append("HIGH FRAGILITY: Analysis based on interpretive guidance. Regulatory compliance review recommended.")

    if zone == AnalysisZone.AUDIT:
        warnings.append("AUDIT ZONE: This analysis should be verified by qualified railroad safety professionals.")

    # Confidence stratification
    confidence = primary_doctrine.confidence
    if len(matched_doctrines) < 2:
        confidence = ConfidenceLevel.DISCLOSURE

    elapsed_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

    telemetry.record_query(elapsed_ms, triggered_doctrines)

    return QueryResponse(
        answer=answer,
        confidence=confidence,
        doctrines_triggered=triggered_doctrines,
        reasoning_chain=reasoning_chain,
        authorities=list(set(authorities_cited)),
        warnings=warnings,
        mode=mode,
        zone=zone,
        determinism_hash=compute_hash(question, mode, zone),
        latency_ms=round(elapsed_ms, 2)
    )

# ============================================================================
# DETERMINISM HASH
# ============================================================================

def compute_hash(question: str, mode: ResponseMode, zone: AnalysisZone) -> str:
    content = f"{question}|{mode.value}|{zone.value}|{VERSION}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title=f"{ENGINE_NAME} v{VERSION}", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        logger.info(f"Query received: {request.question[:100]} | Mode: {request.mode} | Zone: {request.zone}")
        response = await three_layer_response(
            request.question,
            request.mode,
            request.zone,
            request.context
        )
        return response
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        telemetry.record_query(0.0, [], error=str(e))
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    metrics = telemetry.get_metrics()
    return HealthResponse(
        status="healthy",
        engine=ENGINE_NAME,
        version=VERSION,
        port=PORT,
        doctrines_loaded=len(DOCTRINE_CACHE),
        uptime_seconds=metrics["uptime_seconds"],
        total_queries=metrics["total_queries"],
        avg_latency_ms=metrics["avg_latency_ms"]
    )

@app.get("/doctrines")
async def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "triggered_count": d.triggered_count,
                "last_triggered": d.last_triggered.isoformat() if d.last_triggered else None
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/metrics")
async def get_metrics():
    return telemetry.get_metrics()

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} rail safety doctrine blocks")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
