"""
AUTO15 Safety Systems Analysis Engine v1.0.0
TIE-Grade Intelligence Engine for Automotive Safety Systems

Covers: Airbag systems diagnostics, seatbelt pretensioner analysis, crash avoidance systems
(AEB/LDW/BSM), occupant protection assessment, pedestrian safety evaluation, FMVSS compliance

Port: 9325
"""

import hashlib
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, Counter

# CRITICAL: Add parent directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from loguru import logger
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# ============================================================================
# ENUMS & CONSTANTS
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
    DIAGNOSTIC = "DIAGNOSTIC"
    COMPLIANCE = "COMPLIANCE"
    ACCIDENT_RECONSTRUCTION = "ACCIDENT_RECONSTRUCTION"


class IssueCategory(str, Enum):
    AIRBAG_DEPLOYMENT = "AIRBAG_DEPLOYMENT"
    SEATBELT_MALFUNCTION = "SEATBELT_MALFUNCTION"
    CRASH_AVOIDANCE = "CRASH_AVOIDANCE"
    OCCUPANT_PROTECTION = "OCCUPANT_PROTECTION"
    PEDESTRIAN_SAFETY = "PEDESTRIAN_SAFETY"
    FMVSS_COMPLIANCE = "FMVSS_COMPLIANCE"
    SENSOR_FAULT = "SENSOR_FAULT"
    RECALL_LIABILITY = "RECALL_LIABILITY"


BANNED_PHRASES = [
    "guaranteed safe",
    "absolutely prevents",
    "zero defect rate",
    "never fails",
    "completely eliminates injury",
    "perfectly designed",
    "impossible to malfunction",
]


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class SafetyQueryRequest(BaseModel):
    query: str = Field(..., description="Safety system analysis question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.DIAGNOSTIC)
    vehicle_year: Optional[int] = Field(None, ge=1990, le=2030)
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    crash_speed_mph: Optional[float] = Field(None, ge=0, le=200)
    deployment_occurred: Optional[bool] = None
    dtc_codes: Optional[List[str]] = Field(default_factory=list)


class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    confidence: ConfidenceLevel
    entity_scope: str
    adversary_position: str
    counter_arguments: List[str]
    resolution_strategy: str


class SafetyAnalysisResponse(BaseModel):
    answer: str
    triggered_doctrines: List[str]
    confidence: ConfidenceLevel
    issue_categories: List[IssueCategory]
    source_layer: str
    latency_ms: float
    determinism_hash: str
    fmvss_references: List[str]
    fragility_score: float
    epistemic_flags: List[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL AUTOMOTIVE SAFETY DOMAIN BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Frontal Airbag Non-Deployment Analysis",
        keywords=["airbag", "non-deployment", "crash severity", "delta-v", "frontal impact", "SRS", "ACM"],
        conclusion_template="Airbag non-deployment in frontal crashes requires analysis of crash severity metrics (delta-v, impact angle, occupant position), crash data recorder outputs, and compliance with FMVSS 208 deployment thresholds. Non-deployment may be justified if delta-v below 14-16 mph or impact angle exceeded 30 degrees off-axis.",
        reasoning_framework="""
1. Retrieve crash data recorder (CDR/ACM) event file showing delta-v, impact angle, and pre-crash seatbelt status
2. Compare delta-v to OEM deployment threshold (typically 14-16 mph for frontal impacts per FMVSS 208)
3. Assess impact angle - airbags typically inhibited beyond 30-degree off-axis impacts
4. Check occupant position sensors - out-of-position (OOP) detection may suppress deployment
5. Verify SRS system pre-crash health via DTC history - pre-existing faults may prevent deployment
6. Evaluate crash pulse characteristics - soft barrier impacts generate lower acceleration despite moderate delta-v
7. Review NHTSA recall databases for deployment algorithm defects in subject vehicle make/model/year
8. Compare to similar crash tests (NCAP, IIHS) with known deployment outcomes
9. Assess whether non-deployment contributed to injury severity using biomechanical analysis
10. Document compliance with FMVSS 208 advanced airbag requirements (risk-based deployment)
""",
        key_factors=[
            "Delta-v magnitude and direction",
            "Crash pulse shape and duration",
            "Occupant position and seatbelt use",
            "Pre-crash SRS fault codes",
            "Impact angle relative to vehicle centerline",
            "OEM deployment algorithm version",
            "Crash data recorder availability",
            "FMVSS 208 compliance threshold"
        ],
        primary_authority=[
            "FMVSS 208 - Occupant Crash Protection (49 CFR 571.208)",
            "NHTSA ODI Crash Data Recorder Imaging Guide",
            "SAE J211 - Instrumentation for Impact Test",
            "Bosch CDR System Technical Documentation",
            "IIHS Frontal Offset Crash Test Protocol"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All passenger vehicles with frontal airbags (1998+)",
        adversary_position="Plaintiff argues airbag should have deployed based on visible vehicle damage, claiming defect in deployment algorithm or sensor malfunction regardless of technical delta-v threshold.",
        counter_arguments=[
            "Visible damage does not correlate to crash severity - modern crumple zones deform extensively even in minor impacts",
            "FMVSS 208 allows risk-based deployment - marginal severity crashes may justify non-deployment to avoid airbag injury",
            "Crash data recorder is definitive evidence of actual delta-v, superseding damage-based estimates",
            "Out-of-position occupants face greater injury risk from deployment than non-deployment"
        ],
        resolution_strategy="Obtain and analyze crash data recorder file, compare to FMVSS 208 thresholds, demonstrate compliance with advanced airbag rule risk mitigation, show non-deployment decision was appropriate given actual crash severity metrics."
    ),

    DoctrineBlock(
        topic="Seatbelt Pretensioner Failure Modes",
        keywords=["pretensioner", "retractor", "seatbelt", "pyrotechnic", "failure", "slack", "webbing"],
        conclusion_template="Seatbelt pretensioner failures manifest as non-actuation (pyrotechnic failure), incomplete retraction (mechanical jam), or premature deployment (electrical fault). Diagnosis requires inspection of squib resistance, retractor mechanism examination, and ACM fault code analysis per FMVSS 209 and 210.",
        reasoning_framework="""
1. Retrieve ACM fault codes specific to pretensioner circuit - B0081/B0082 (driver/passenger squib resistance out of range)
2. Measure squib resistance - nominal 2-3 ohms, open circuit or short indicates electrical failure
3. Inspect pretensioner mechanical assembly for corrosion, contamination, or obstruction preventing piston movement
4. Check webbing for pre-crash slack - excessive slack may indicate retractor pawl wear or torsion bar degradation
5. Verify ACM firing decision via crash data - pretensioner should fire concurrently with airbag deployment
6. Test backup power supply - inadequate capacitor charge may prevent pretensioner actuation despite deployment command
7. Examine wiring harness for open circuits, chafing, or connector corrosion (common B-pillar routing failure)
8. Review recall history for pretensioner propellant degradation (Takata, ARC airbag inflator parallel issue)
9. Compare crash severity to pretensioner threshold - lower than airbag (typically 8-10 mph delta-v)
10. Assess injury causation - quantify increased occupant excursion due to pretensioner non-actuation
""",
        key_factors=[
            "Squib electrical continuity and resistance",
            "ACM deployment command vs. actual actuation",
            "Mechanical retractor condition",
            "Pre-crash seatbelt slack",
            "Wiring harness integrity",
            "Backup power supply voltage",
            "Propellant age and degradation",
            "Crash severity relative to threshold"
        ],
        primary_authority=[
            "FMVSS 209 - Seatbelt Assemblies (49 CFR 571.209)",
            "FMVSS 210 - Seatbelt Anchorages (49 CFR 571.210)",
            "SAE J2570 - Seatbelt Restraint System Evaluation",
            "ISO 6487 - Road Vehicles Crash Test Instrumentation"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles equipped with pyrotechnic pretensioners (most 2000+ models)",
        adversary_position="Plaintiff claims pretensioner failure allowed excessive occupant movement causing preventable injuries, alleging design or manufacturing defect in deployment system.",
        counter_arguments=[
            "Pre-crash seatbelt non-use negates pretensioner effectiveness regardless of function",
            "Crash severity below pretensioner threshold justifies non-actuation per FMVSS design requirements",
            "Alternative injury causation - pretensioner actuation would not have prevented specific injury given crash dynamics",
            "Proper maintenance and inspection intervals reduce pretensioner failure probability"
        ],
        resolution_strategy="Download ACM data, perform electrical and mechanical forensic examination of pretensioner assembly, correlate deployment decision to crash severity, demonstrate compliance with FMVSS thresholds or identify non-defect failure mode (e.g., open circuit from collision damage)."
    ),

    DoctrineBlock(
        topic="Automatic Emergency Braking (AEB) False Negatives",
        keywords=["AEB", "automatic emergency braking", "false negative", "collision warning", "radar", "lidar", "camera", "ADAS"],
        conclusion_template="AEB false negatives (failure to detect and brake for obstacles) arise from sensor limitations (weather, lighting, occlusion), algorithm conservatism (to avoid false positives), or edge case scenarios beyond system design domain. NHTSA AEB performance assessment uses NHTSA test protocols, not real-world liability standards.",
        reasoning_framework="""
1. Identify AEB sensor suite - radar-only, camera-only, or sensor fusion (radar+camera or +lidar)
2. Assess environmental conditions - rain, fog, snow, or low-angle sun can degrade sensor performance
3. Check obstacle characteristics - dark clothing, non-reflective surfaces, or partial occlusion reduce detectability
4. Verify vehicle speed - most AEB systems limited to <50 mph operational range per OEM specifications
5. Review system warnings - did forward collision warning (FCW) activate prior to crash, indicating detection but insufficient braking?
6. Analyze reaction time - AEB typically initiates braking 1.5-2.5 seconds before impact, may be insufficient for high closing speeds
7. Check for driver override - brake or accelerator pedal input may cancel AEB intervention per design intent
8. Retrieve ADAS module fault codes - camera calibration errors or radar blockage DTCs indicate system degradation
9. Compare to NCAP AEB test performance - systems optimized for test scenarios may underperform in atypical real-world cases
10. Assess legal standard - AEB is supplemental system, not replacement for driver vigilance per SAE Level 2 automation
""",
        key_factors=[
            "Sensor type and fusion architecture",
            "Environmental visibility conditions",
            "Obstacle reflectivity and size",
            "Vehicle speed and closing rate",
            "Forward collision warning activation",
            "Driver override inputs",
            "ADAS calibration and fault status",
            "System design operational envelope"
        ],
        primary_authority=[
            "NHTSA AEB Test Procedures (NCAP 2023+)",
            "SAE J3016 - Levels of Driving Automation",
            "IIHS Front Crash Prevention Test Protocol",
            "FMVSS 126 - Electronic Stability Control (ESC benchmark for active safety)"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles equipped with AEB/FCW systems (increasing prevalence 2015+, standard on most 2022+ models)",
        adversary_position="Plaintiff argues AEB system was defective for failing to prevent collision despite marketing claims of 'automatic braking to avoid crashes,' seeking strict liability for system non-performance.",
        counter_arguments=[
            "AEB is driver assistance, not autonomous driving - SAE Level 2 requires continuous driver supervision",
            "OEM owner's manual disclaims limitations - fog, darkness, non-standard obstacles may not be detected",
            "NHTSA and IIHS testing shows industry-standard performance, not guarantee of zero false negatives",
            "Crash was outside system design envelope (e.g., speed >50 mph, stationary object, severe weather)",
            "Driver override or delayed reaction contributed to crash causation independent of AEB performance"
        ],
        resolution_strategy="Download ADAS module data, reconstruct sensor inputs and algorithm decisions, demonstrate crash scenario exceeded system design limitations, cite owner's manual disclaimers and SAE automation level definitions, show compliance with NCAP testing standards."
    ),

    DoctrineBlock(
        topic="Side-Impact Airbag Deployment Thresholds",
        keywords=["side airbag", "curtain airbag", "T-bone", "lateral impact", "delta-v", "side crash sensor", "FMVSS 214"],
        conclusion_template="Side airbag deployment requires sufficient lateral delta-v (typically 10-14 mph) detected by door-mounted or B-pillar accelerometers. Non-deployment in marginal side impacts may be justified by FMVSS 214 compliance testing, which uses rigid barrier at 33.5 mph striking 27% of vehicle width.",
        reasoning_framework="""
1. Retrieve side crash sensor data from ACM - left/right lateral accelerometer traces
2. Calculate lateral delta-v from accelerometer integration - compare to OEM deployment threshold
3. Assess impact location - door impacts more likely to deploy than quarter panel or A-pillar strikes
4. Check impact object characteristics - pole impacts concentrate force, may deploy at lower delta-v than distributed barrier impacts
5. Verify curtain airbag vs. torso airbag deployment logic - curtain may deploy for rollover sensing independent of side impact
6. Review occupant seating position - side airbags may suppress for unoccupied seats or child seats
7. Examine FMVSS 214 compliance data - OEM side impact sled tests show deployment timing and sensor calibration
8. Compare to IIHS side impact test (barrier at 31 mph, 50% overlap) - real-world severity benchmark
9. Assess injury pattern - thorax and pelvis injuries suggest side airbag could have mitigated harm if deployed
10. Check for pre-crash faults in side impact sensing system - open circuits or sensor degradation
""",
        key_factors=[
            "Lateral delta-v magnitude and duration",
            "Impact location relative to sensors",
            "Impacting object type (vehicle, pole, barrier)",
            "Occupant presence and position detection",
            "Side airbag system pre-crash health",
            "FMVSS 214 test compliance margins",
            "Curtain vs. torso airbag deployment logic",
            "Injury severity and causation linkage"
        ],
        primary_authority=[
            "FMVSS 214 - Side Impact Protection (49 CFR 571.214)",
            "IIHS Side Impact Crash Test Protocol",
            "NHTSA New Car Assessment Program (NCAP) Side Barrier Test",
            "SAE J2052 - Measurement of Anthropomorphic Test Dummy Response to Side Impact"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles with side-impact airbags (torso bags standard ~2000+, curtain bags ~2005+)",
        adversary_position="Plaintiff alleges side airbag non-deployment in T-bone crash caused serious thorax injuries, claiming defective sensor calibration or deployment algorithm set threshold too high for safety.",
        counter_arguments=[
            "Crash severity below deployment threshold per FMVSS 214 design specifications",
            "Impact location outside sensor coverage zone - quarter panel or A-pillar strikes may not trigger door-mounted sensors",
            "Occupant was unbelted or in child seat, triggering suppression logic to avoid airbag-induced injury",
            "Crash data recorder confirms insufficient lateral delta-v for deployment decision"
        ],
        resolution_strategy="Obtain crash data recorder file, analyze lateral accelerometer traces, compare delta-v to FMVSS 214 test results, demonstrate deployment decision consistent with regulatory compliance and injury mitigation objectives."
    ),

    DoctrineBlock(
        topic="Blind Spot Monitoring (BSM) System Limitations",
        keywords=["blind spot", "BSM", "lane change assist", "radar", "side mirror", "false negative", "detection zone"],
        conclusion_template="Blind Spot Monitoring radar systems have defined detection zones (typically 10-15 feet lateral, 3 feet rearward of mirror to rear bumper) and speed differentials (relative speed <15 mph). Failures to detect vehicles outside design envelope or during rapid lane changes are not defects but inherent system limitations.",
        reasoning_framework="""
1. Review BSM system specifications - detection zone dimensions, speed range, sensor type (24 GHz vs. 77 GHz radar)
2. Reconstruct crash geometry - was other vehicle within BSM detection zone at time of lane change initiation?
3. Assess relative speed - BSM may not alert for vehicles approaching rapidly from behind (closing speed >20 mph)
4. Check for sensor blockage - mud, snow, or damage to rear bumper cover can occlude radar sensors
5. Verify driver response - did driver check mirrors and shoulder despite BSM non-alert, per owner's manual instructions?
6. Retrieve ADAS module fault codes - radar misalignment or degradation codes indicate system malfunction
7. Review owner's manual disclaimers - BSM explicitly described as supplemental aid, not replacement for direct vision
8. Compare to SAE J2802 definitions - Blind Spot Monitoring system performance criteria
9. Assess whether crash would have occurred with proper mirror check - causation analysis independent of BSM performance
10. Examine competitive systems - is subject vehicle's BSM detection zone industry-standard or substandard?
""",
        key_factors=[
            "BSM detection zone geometry",
            "Relative vehicle speed and acceleration",
            "Sensor blockage or misalignment",
            "Driver mirror and shoulder check behavior",
            "ADAS module fault status",
            "Owner's manual limitations disclosure",
            "SAE J2802 compliance",
            "Alternative causation factors"
        ],
        primary_authority=[
            "SAE J2802 - Blind Spot Monitoring System Performance Requirements",
            "NHTSA Vehicle-to-Vehicle (V2V) Communications Research",
            "IIHS Crash Avoidance Technology Evaluations"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles equipped with radar-based BSM (increasingly common 2010+, standard on many 2020+ models)",
        adversary_position="Plaintiff claims BSM system was defective for failing to warn of adjacent vehicle during lane change, causing sideswipe collision and serious injuries.",
        counter_arguments=[
            "Other vehicle was outside BSM detection zone (e.g., too far rearward or moving too fast)",
            "Sensor blockage from road debris or damage reduced detection capability",
            "Driver failed to check mirrors as required by owner's manual and standard driving practice",
            "BSM is supplemental system - legal duty to maintain proper lookout remains with driver",
            "System was functioning per design specifications at time of crash per ADAS module data"
        ],
        resolution_strategy="Download ADAS module data, reconstruct vehicle positions and speeds, demonstrate other vehicle was outside detection zone or closing too rapidly, cite owner's manual limitations, show driver failed independent duty to check mirrors."
    ),

    DoctrineBlock(
        topic="Pedestrian Detection System Performance",
        keywords=["pedestrian detection", "AEB pedestrian", "vulnerable road user", "camera", "radar", "lidar", "NCAP pedestrian"],
        conclusion_template="Pedestrian detection systems use camera-based image recognition, sometimes fused with radar or lidar. Performance degrades in low light, with dark clothing, partial occlusion, or non-standard postures. NCAP pedestrian AEB tests use mannequins in daylight at specific speeds - real-world performance may vary significantly.",
        reasoning_framework="""
1. Identify pedestrian detection sensor suite - camera-only systems limited in low-light conditions
2. Assess lighting conditions - dusk, nighttime, or shadows significantly reduce camera-based detection accuracy
3. Evaluate pedestrian clothing and contrast - dark clothing against dark pavement reduces detectability
4. Check for occlusion - parked cars, road signs, or vegetation may block sensor line-of-sight until last moment
5. Verify pedestrian behavior - running, crouching, or pushing objects (strollers, shopping carts) may not match trained algorithm patterns
6. Review vehicle speed - most pedestrian AEB systems effective only up to 25-35 mph per OEM specifications
7. Retrieve ADAS module data - did system detect pedestrian and classify correctly before impact?
8. Compare to NCAP pedestrian test scenarios - adult crossing (day), child darting (day), adult at night (with headlights)
9. Assess driver reaction - was driver distracted, would earlier warning have enabled avoidance?
10. Check system calibration - windshield replacement or camera misalignment may degrade performance
""",
        key_factors=[
            "Lighting and visibility conditions",
            "Pedestrian clothing reflectivity",
            "Occlusion from roadside objects",
            "Pedestrian posture and motion pattern",
            "Vehicle speed relative to system limits",
            "Sensor calibration and health",
            "NCAP test scenario comparison",
            "Driver distraction or reaction time"
        ],
        primary_authority=[
            "NCAP Pedestrian Crash Avoidance Test (2018+)",
            "IIHS Pedestrian Crash Prevention Evaluation",
            "ISO 19206 - Road Vehicles - Test Devices for Target Vehicles for AEB",
            "SAE J3016 - Automated Driving System Classification"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles with pedestrian detection AEB (increasing 2016+, many luxury brands standard by 2020)",
        adversary_position="Plaintiff (pedestrian estate) alleges vehicle pedestrian detection system was defective for failing to brake before striking pedestrian, despite marketing claims of 'pedestrian protection technology.'",
        counter_arguments=[
            "Crash occurred at night or in low-light conditions where camera-based detection is severely limited",
            "Pedestrian was occluded by parked vehicle until immediately before impact, insufficient time for braking",
            "Pedestrian was running or in non-standard posture not matching algorithm training data",
            "Vehicle speed exceeded system operational envelope (e.g., 40 mph vs. 25 mph design limit)",
            "Driver was primary cause - distracted driving or failure to maintain proper lookout independent of ADAS performance"
        ],
        resolution_strategy="Download ADAS module data, reconstruct lighting and visibility conditions, demonstrate crash scenario exceeded system design limitations, cite NCAP test protocol differences from real-world conditions, show compliance with industry-standard performance."
    ),

    DoctrineBlock(
        topic="FMVSS 208 Advanced Airbag Rule Compliance",
        keywords=["FMVSS 208", "advanced airbag", "risk-based deployment", "out-of-position", "5th percentile female", "suppression"],
        conclusion_template="FMVSS 208 Advanced Airbag Rule (2006+) requires risk-based deployment algorithms that consider occupant size, position, and seatbelt use to minimize airbag-induced injuries. Suppression or reduced-power deployment for small occupants or out-of-position scenarios is mandated, not defective.",
        reasoning_framework="""
1. Verify vehicle model year - Advanced Airbag Rule applies to 2006+ passenger vehicles
2. Identify airbag deployment mode - was it full-power, reduced-power, or suppressed?
3. Check occupant classification system (OCS) - weight sensor in seat classifies occupant as infant, child, 5th percentile female, or adult
4. Assess seatbelt use - unbuckled occupants may receive suppressed or reduced deployment to avoid airbag injury
5. Review occupant position sensors - capacitive or optical sensors detect forward-leaning or hands-on-dash positions
6. Verify deployment decision against FMVSS 208 out-of-position (OOP) test requirements
7. Compare crash severity to deployment threshold - marginal crashes may justify suppression to avoid airbag injury exceeding crash injury
8. Examine injury pattern - is claimed injury consistent with airbag non-deployment or with reduced-power deployment?
9. Check for OCS fault codes - system defaults to full deployment if sensor malfunction detected (fail-safe mode)
10. Review NHTSA Special Crash Investigations (SCI) database for similar deployment decisions in comparable crashes
""",
        key_factors=[
            "Occupant size and weight classification",
            "Seatbelt buckle status",
            "Occupant position (forward lean, proximity to airbag)",
            "Crash severity (delta-v)",
            "OCS and position sensor functionality",
            "FMVSS 208 OOP test compliance",
            "Deployment mode (full, reduced, suppressed)",
            "Injury causation - airbag vs. crash forces"
        ],
        primary_authority=[
            "FMVSS 208 Advanced Airbag Requirements (49 CFR 571.208)",
            "NHTSA Final Rule - Federal Motor Vehicle Safety Standards; Occupant Crash Protection (2000)",
            "NHTSA Out-of-Position Test Procedures",
            "SAE J2885 - Occupant Detection and Classification Systems"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All passenger vehicles model year 2006 and later with advanced airbag systems",
        adversary_position="Plaintiff claims airbag non-deployment or reduced-power deployment caused preventable injuries, alleging defective occupant classification system or overly conservative deployment algorithm.",
        counter_arguments=[
            "Advanced Airbag Rule mandates risk-based deployment - suppression for small occupants prevents greater airbag-induced injury",
            "OCS correctly classified occupant as child or 5th percentile female, triggering appropriate suppression per FMVSS 208",
            "Occupant was out-of-position (forward lean detected), full deployment would have caused severe facial or neck injury",
            "Crash severity was marginal - full deployment airbag injury risk exceeded crash injury risk per risk-benefit analysis"
        ],
        resolution_strategy="Download ACM data showing OCS classification and deployment decision, demonstrate compliance with FMVSS 208 advanced airbag requirements, cite biomechanical studies showing airbag injury risk for subject occupant characteristics, prove deployment mode was appropriate for crash severity and occupant profile."
    ),

    DoctrineBlock(
        topic="Lane Departure Warning (LDW) vs. Lane Keep Assist (LKA) Functionality",
        keywords=["LDW", "LKA", "lane departure", "lane keep assist", "steering intervention", "haptic warning", "camera"],
        conclusion_template="Lane Departure Warning provides alerts (visual, audible, or haptic) when vehicle drifts from lane without turn signal active. Lane Keep Assist adds steering torque to guide vehicle back to lane center. LDW does not prevent departure, only warns driver - failure to avoid crash after warning does not indicate system defect.",
        reasoning_framework="""
1. Distinguish system type - LDW (warning only) vs. LKA (active steering intervention)
2. Verify lane marking visibility - both systems require clear, high-contrast lane markings to function
3. Check environmental conditions - rain, snow, or faded pavement markings degrade camera detection
4. Assess vehicle speed - most systems inactive below 35-40 mph per design specifications
5. Verify turn signal use - LDW/LKA intentionally suppressed when turn signal activated
6. Retrieve ADAS module data - did system detect lane departure and issue warning/intervention?
7. Check for hands-off detection - LKA requires driver hands on wheel, may disengage if no steering torque detected
8. Review driver response time - did driver react to LDW warning, or was attention diverted?
9. Compare to SAE J3063 performance standards for lane departure warning systems
10. Assess causation - would LKA steering intervention have been sufficient to avoid crash, or was departure too rapid/severe?
""",
        key_factors=[
            "System type - warning only or active steering",
            "Lane marking visibility and contrast",
            "Weather and road surface conditions",
            "Vehicle speed relative to activation threshold",
            "Turn signal status at time of departure",
            "Driver hands-on-wheel detection",
            "ADAS module warning/intervention data",
            "Driver reaction time to warning"
        ],
        primary_authority=[
            "SAE J3063 - Lane Departure Warning System Performance Requirements",
            "NHTSA Lane Departure Warning System Research",
            "IIHS Crash Avoidance Technology Evaluation - LDW/LKA",
            "ISO 17361 - Lane Departure Warning Systems"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles with LDW (common 2012+) or LKA (increasing 2015+, standard on many 2020+ models)",
        adversary_position="Plaintiff claims LDW/LKA system was defective for failing to prevent lane departure crash, alleging inadequate warning or insufficient steering intervention to avoid collision.",
        counter_arguments=[
            "LDW is warning system only - does not control steering, driver remains responsible for vehicle control",
            "Lane markings were faded, obscured, or absent - system cannot function without detectable markings",
            "Driver ignored LDW warning or overrode LKA steering input, indicating driver inattention as primary cause",
            "Vehicle speed was below activation threshold (e.g., 30 mph in system with 40 mph minimum)",
            "Turn signal was activated, properly suppressing LDW/LKA per design intent"
        ],
        resolution_strategy="Download ADAS module data showing warning/intervention status, reconstruct lane marking visibility, demonstrate system functioned per design specifications, show driver inattention or override as primary crash cause, cite owner's manual limitations."
    ),

    DoctrineBlock(
        topic="Rollover Crash Roof Strength and Occupant Protection",
        keywords=["rollover", "roof strength", "roof crush", "FMVSS 216", "strength-to-weight ratio", "SWR", "ejection"],
        conclusion_template="FMVSS 216 requires vehicle roof to withstand force equal to 3.0 times vehicle weight (strength-to-weight ratio or SWR) without exceeding 5 inches of crush. Compliance with FMVSS 216 is strong defense against roof crush claims, but does not preclude injury in severe rollovers exceeding test conditions.",
        reasoning_framework="""
1. Verify FMVSS 216 compliance - retrieve NHTSA certification data showing roof strength test results
2. Assess rollover severity - number of quarter-turns, impact surface (soft soil vs. pavement), and vehicle speed
3. Measure actual roof crush - compare to 5-inch FMVSS 216 regulatory limit
4. Check for occupant ejection - partial or complete ejection greatly increases injury severity independent of roof strength
5. Verify seatbelt use - unbelted occupants experience severe head/neck trauma from roof contact regardless of roof strength
6. Review crash data recorder - vehicle roll rate, lateral acceleration, and number of impacts
7. Compare to IIHS roof strength test (4.0x SWR) - some vehicles exceed regulatory minimum for marketing advantage
8. Assess injury mechanism - is claimed injury (e.g., cervical spine fracture) consistent with roof crush or other rollover forces?
9. Check for secondary impacts - many rollover injuries occur from multiple roof-to-ground impacts, not initial roof crush
10. Review NHTSA rollover resistance rating (star rating) - vehicle design factors affecting rollover propensity
""",
        key_factors=[
            "FMVSS 216 compliance and SWR test results",
            "Actual roof crush measurement vs. 5-inch limit",
            "Rollover severity (number of rolls, speed, surface)",
            "Occupant ejection status",
            "Seatbelt use and restraint effectiveness",
            "Crash data recorder roll dynamics",
            "IIHS roof strength rating comparison",
            "Injury causation - roof crush vs. other rollover forces"
        ],
        primary_authority=[
            "FMVSS 216 - Roof Crush Resistance (49 CFR 571.216)",
            "FMVSS 216a - Upgraded Roof Crush Standard (2009+, 3.0x SWR)",
            "IIHS Roof Strength Test Protocol (4.0x SWR)",
            "NHTSA Rollover Resistance Rating Program",
            "Kuppa et al., 'Influence of Roof Strength on Injury in Rollovers' (NHTSA)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All passenger vehicles subject to FMVSS 216a (2009+ with phase-in schedule)",
        adversary_position="Plaintiff claims inadequate roof strength caused severe head and neck injuries during rollover crash, alleging roof design defect despite FMVSS 216 compliance.",
        counter_arguments=[
            "Vehicle exceeded FMVSS 216 minimum (3.0x SWR), demonstrating superior roof strength",
            "Occupant was unbelted or partially ejected - roof strength irrelevant to injury causation",
            "Rollover severity (e.g., 5+ rolls at 60 mph) exceeded any reasonable design limit",
            "Actual roof crush was less than 5 inches, complying with regulatory standard",
            "Injury was caused by other rollover forces (lateral impact, ejection) independent of roof crush"
        ],
        resolution_strategy="Obtain FMVSS 216 certification test data, measure actual roof crush, compare to regulatory standard, demonstrate compliance, show injury causation independent of roof strength or attributable to occupant non-use of seatbelt."
    ),

    DoctrineBlock(
        topic="Crash Data Recorder (CDR) Admissibility and Interpretation",
        keywords=["CDR", "black box", "ACM", "crash data recorder", "delta-v", "event data recorder", "EDR", "Bosch"],
        conclusion_template="Crash Data Recorders (CDR/EDR) capture pre-crash and crash event data including speed, throttle position, brake application, seatbelt use, and airbag deployment timing. CDR data is admissible in most jurisdictions as business record or certified instrument reading, and is highly probative for crash reconstruction.",
        reasoning_framework="""
1. Identify CDR system type - Bosch CDR (most common), manufacturer-proprietary (Ford, GM, Toyota), or third-party
2. Download CDR data using manufacturer-approved tool (e.g., Bosch Crash Data Retrieval System)
3. Verify data integrity - CDR reports include data validation checksums and non-volatile memory write status
4. Interpret pre-crash data - vehicle speed (typically 5 seconds pre-crash), throttle %, brake on/off, seatbelt status
5. Analyze crash event data - delta-v (change in velocity), maximum crush, impact algorithm deployment decision
6. Check for multiple events - some crashes record primary and secondary impacts (e.g., initial collision then pole strike)
7. Assess seatbelt buckle status - pre-crash unbuckled status may affect airbag deployment and injury causation
8. Compare CDR speed to witness estimates or skid mark analysis - CDR is definitive unless data corruption evident
9. Review deployment times - airbag and pretensioner fire times relative to impact onset (typically 15-30 milliseconds)
10. Prepare for admissibility challenges - foundation witness (CDR technician), chain of custody, data download procedure
""",
        key_factors=[
            "CDR system type and manufacturer",
            "Data download tool and procedure",
            "Data integrity validation (checksums)",
            "Pre-crash speed and driver inputs",
            "Delta-v magnitude and direction",
            "Seatbelt buckle status (pre-crash)",
            "Airbag deployment timing",
            "Multiple event recording"
        ],
        primary_authority=[
            "49 CFR Part 563 - Event Data Recorders (EDR Final Rule 2012)",
            "NHTSA CDR Data Element Definitions",
            "Bosch Crash Data Retrieval System Manual",
            "SAE J1698 - EDR Data Exchange Standard"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Most vehicles 2013+ have EDR per 49 CFR 563 mandate; many earlier vehicles have CDR capability",
        adversary_position="Plaintiff challenges CDR data accuracy, claiming speed reading was inflated or deployment decision data was manipulated post-crash by defendant.",
        counter_arguments=[
            "CDR data is stored in non-volatile memory, cannot be altered post-crash without forensically detectable tampering",
            "Data validation checksums confirm integrity - corrupted data would be flagged in CDR report",
            "CDR speed readings corroborated by independent evidence (skid marks, damage analysis, witness statements)",
            "Foundation testimony from certified CDR technician establishes proper download procedure and tool calibration"
        ],
        resolution_strategy="Download CDR data immediately post-crash to preserve evidence, use manufacturer-approved tool, prepare certified technician as foundation witness, corroborate CDR data with independent reconstruction evidence."
    ),

    DoctrineBlock(
        topic="Occupant Classification System (OCS) Suppression Logic",
        keywords=["OCS", "occupant classification", "weight sensor", "airbag suppression", "child seat", "5th percentile female"],
        conclusion_template="Occupant Classification Systems use weight sensors, seatbelt tension sensors, or seat position sensors to classify occupants and determine appropriate airbag deployment mode. Suppression for child seats and small adults is mandated by FMVSS 208 to prevent airbag-induced injuries exceeding crash injuries.",
        reasoning_framework="""
1. Identify OCS sensor type - bladder weight sensor, strain gauge, or capacitive seat sensor
2. Retrieve OCS classification decision from ACM - infant, child, 5th percentile female, or adult male
3. Verify sensor calibration - OCS self-test runs at ignition-on, fault codes indicate sensor degradation
4. Check for classification errors - aftermarket seat covers, cushions, or liquid spills may affect weight sensing
5. Assess occupant actual weight vs. classification threshold - FMVSS 208 requires suppression for occupants <65 lbs (child seat)
6. Review child seat installation - LATCH or seatbelt-secured seats may affect sensor readings differently
7. Verify airbag suppression indicator - dashboard light should illuminate when passenger airbag suppressed
8. Compare deployment decision to FMVSS 208 requirements - suppression required for child seats, optional for 5th percentile female
9. Assess injury causation - would airbag deployment have caused greater injury than crash forces alone?
10. Check for OCS recall history - some systems had classification errors prompting manufacturer recalls
""",
        key_factors=[
            "OCS sensor type and calibration",
            "Occupant weight classification",
            "Sensor fault codes or degradation",
            "Aftermarket seat modifications",
            "Child seat installation method",
            "Airbag suppression indicator status",
            "FMVSS 208 suppression requirements",
            "Injury causation analysis"
        ],
        primary_authority=[
            "FMVSS 208 Advanced Airbag Rule - OCS Requirements",
            "SAE J2885 - Occupant Detection and Classification Systems",
            "NHTSA Out-of-Position Testing Procedures",
            "Manufacturer OCS Calibration Specifications"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles with advanced airbags (2006+) equipped with OCS for passenger seat suppression",
        adversary_position="Plaintiff claims OCS misclassified adult occupant as child, suppressing airbag and causing preventable injuries in crash where deployment was warranted.",
        counter_arguments=[
            "Occupant was at or below 5th percentile female weight threshold, justifying suppression per FMVSS 208",
            "Aftermarket seat cover or cushion interfered with sensor, causing classification error - not manufacturer defect",
            "OCS fault code was present pre-crash, system defaulted to full deployment fail-safe mode",
            "Airbag deployment would have caused greater injury (facial fractures) than crash forces - suppression was appropriate"
        ],
        resolution_strategy="Download ACM data showing OCS classification, verify sensor calibration status, compare occupant weight to classification thresholds, demonstrate FMVSS 208 compliance, show airbag deployment injury risk exceeded crash injury risk."
    ),

    DoctrineBlock(
        topic="Tire Pressure Monitoring System (TPMS) Warnings and Blowout Crashes",
        keywords=["TPMS", "tire pressure", "blowout", "underinflation", "FMVSS 138", "rollover", "low pressure warning"],
        conclusion_template="FMVSS 138 requires Tire Pressure Monitoring Systems to warn driver when tire pressure drops 25% below recommended level. TPMS warning does not prevent blowout if driver ignores warning or continues driving on underinflated tire. Driver has duty to respond to TPMS warning by checking tire pressure and inflating or replacing tire.",
        reasoning_framework="""
1. Verify TPMS system type - direct (pressure sensors in each wheel) or indirect (ABS-based rotation detection)
2. Retrieve TPMS warning history from vehicle computer - when did low pressure warning first illuminate?
3. Check tire pressure recommendations - door jamb sticker and owner's manual specify cold inflation pressure
4. Assess actual tire pressure at time of blowout - forensic tire examination may reveal pressure at failure
5. Verify TPMS warning threshold - FMVSS 138 requires warning at 25% underinflation (e.g., 24 psi if recommended 32 psi)
6. Review driver response to warning - did driver check tire pressure, add air, or ignore warning?
7. Examine tire for failure mode - blowout from underinflation shows characteristic sidewall collapse and heat damage
8. Check for TPMS sensor malfunction - battery failure or sensor damage may prevent warning despite low pressure
9. Assess crash causation - was blowout sole cause, or did driver lose control due to overcorrection?
10. Review tire age and maintenance - underinflation combined with tire age or damage accelerates failure
""",
        key_factors=[
            "TPMS warning illumination timing",
            "Recommended vs. actual tire pressure",
            "Driver response to TPMS warning",
            "Tire failure mode analysis",
            "TPMS sensor functionality",
            "Crash causation factors",
            "Tire age and maintenance history",
            "FMVSS 138 compliance"
        ],
        primary_authority=[
            "FMVSS 138 - Tire Pressure Monitoring Systems (49 CFR 571.138)",
            "NHTSA TPMS Final Rule (2005)",
            "Tire and Rim Association Standards",
            "SAE J2657 - TPMS Performance Requirements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All passenger vehicles model year 2008+ per FMVSS 138 mandate",
        adversary_position="Plaintiff claims TPMS system was defective for failing to warn of low tire pressure before blowout caused rollover crash, or that warning was inadequate to prompt driver action.",
        counter_arguments=[
            "TPMS warning illuminated days or weeks before crash - driver ignored warning and failed to check tire pressure",
            "Driver has duty to respond to TPMS warning per owner's manual instructions - failure to inflate tire is driver negligence",
            "TPMS sensor was functioning properly, warning met FMVSS 138 requirements (25% underinflation threshold)",
            "Crash was caused by driver overcorrection after blowout, not blowout itself - loss of control was preventable"
        ],
        resolution_strategy="Download vehicle computer TPMS warning history, demonstrate warning illuminated prior to crash, show driver had opportunity to inflate tire or seek service, cite owner's manual duty to respond to warning, prove FMVSS 138 compliance."
    ),

    DoctrineBlock(
        topic="Electronic Stability Control (ESC) Intervention and Limitations",
        keywords=["ESC", "stability control", "yaw control", "oversteer", "understeer", "FMVSS 126", "traction control"],
        conclusion_template="Electronic Stability Control (ESC) uses selective brake application and throttle reduction to prevent loss of directional control during oversteer or understeer conditions. FMVSS 126 mandates ESC on all vehicles 2012+. ESC cannot overcome physics limits - severe overcorrection or excessive speed may exceed system capability.",
        reasoning_framework="""
1. Verify ESC system presence - FMVSS 126 required on all passenger vehicles 2012+ model year
2. Retrieve ESC intervention data from vehicle computer - brake actuation events, yaw rate, steering angle
3. Assess crash scenario - was vehicle in oversteer (rear slides out) or understeer (front plows straight)?
4. Check ESC activation - did system intervene by applying individual wheel brakes to correct yaw?
5. Verify driver steering input - excessive or abrupt steering may exceed ESC correction capability
6. Review vehicle speed vs. road conditions - ESC cannot violate friction limits (e.g., black ice at 60 mph)
7. Check for ESC disable - driver may have manually disabled system via dashboard switch
8. Examine tire condition - bald or mismatched tires reduce ESC effectiveness
9. Compare to FMVSS 126 test performance - sine-with-dwell maneuver at 50 mph, system must prevent spinout
10. Assess causation - would crash have been more severe without ESC intervention?
""",
        key_factors=[
            "ESC system presence and activation status",
            "Yaw rate and steering angle data",
            "Oversteer vs. understeer condition",
            "Driver steering input magnitude",
            "Vehicle speed and road friction",
            "ESC manual disable status",
            "Tire condition and inflation",
            "FMVSS 126 test compliance"
        ],
        primary_authority=[
            "FMVSS 126 - Electronic Stability Control (49 CFR 571.126)",
            "NHTSA ESC Final Rule (2007, mandatory 2012+)",
            "IIHS ESC Effectiveness Research",
            "SAE J3063 - ESC Performance Requirements"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All passenger vehicles 2012+ per FMVSS 126 mandate; many earlier vehicles (2005+) had optional ESC",
        adversary_position="Plaintiff claims ESC system was defective for failing to prevent loss of control and crash, alleging inadequate system calibration or intervention delay.",
        counter_arguments=[
            "Driver steering input was excessive - ESC cannot overcome physics limits when vehicle exceeds available friction",
            "Vehicle speed was too high for road conditions - ESC cannot prevent crash on ice/snow at highway speeds",
            "Driver manually disabled ESC system, negating safety benefit",
            "ESC did intervene and reduced crash severity - without ESC, vehicle would have rolled over instead of spinning out",
            "Tire condition (bald, underinflated) reduced traction below level ESC calibration assumes"
        ],
        resolution_strategy="Download vehicle ESC intervention data, reconstruct crash dynamics, demonstrate system activated per design, show driver input or speed exceeded system capability, prove FMVSS 126 compliance, compare actual crash to worse outcome without ESC."
    ),

    DoctrineBlock(
        topic="Seatbelt Webbing Failure and Load Limiter Function",
        keywords=["seatbelt", "webbing", "load limiter", "pretensioner", "chest deflection", "rib fracture", "FMVSS 209"],
        conclusion_template="Modern seatbelts incorporate load limiters (mechanical or pyrotechnic) that allow controlled webbing payout at high chest loads (typically 4-6 kN) to reduce rib fracture risk while maintaining restraint. Load limiter activation is designed behavior per FMVSS 209, not a defect, but must balance chest injury reduction against head excursion increase.",
        reasoning_framework="""
1. Identify seatbelt design - does it include load limiter, and what type (torsion bar, stitched tear seam)?
2. Inspect seatbelt webbing post-crash - load limiter payout shows elongated webbing with torn stitching or twisted torsion bar
3. Measure webbing payout - typical load limiters allow 4-6 inches of controlled extension
4. Assess crash severity - delta-v and crash pulse shape determine seatbelt loading
5. Review occupant injury pattern - rib fractures suggest high chest load, head injury suggests excessive excursion
6. Check for pretensioner activation - pretensioner removes slack before crash pulse, then load limiter manages peak load
7. Compare to FMVSS 209 requirements - webbing must withstand 22,240 N (5000 lbf) load without failure
8. Examine webbing for cut or abrasion failure - sharp intrusion (metal edge, glass) may cut webbing independent of load limiter
9. Assess occupant size - load limiter calibrated for 50th percentile male, may underperform for small or large occupants
10. Review biomechanics literature - optimal load limiter threshold balances chest injury vs. head excursion
""",
        key_factors=[
            "Load limiter type and calibration",
            "Webbing payout measurement",
            "Crash severity (delta-v, pulse shape)",
            "Occupant injury pattern",
            "Pretensioner activation status",
            "FMVSS 209 load capacity compliance",
            "Webbing cut or abrasion damage",
            "Occupant size vs. load limiter design"
        ],
        primary_authority=[
            "FMVSS 209 - Seatbelt Assemblies (49 CFR 571.209)",
            "SAE J2570 - Seatbelt Restraint System Evaluation",
            "Biomechanics of Impact Injury (Yoganandan et al.)",
            "IIHS Frontal Crash Test Injury Criteria"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles with load-limiting seatbelts (increasingly common 2000+, standard on most 2010+ models)",
        adversary_position="Plaintiff claims seatbelt webbing 'failed' due to load limiter payout, alleging defective design allowed excessive occupant excursion and head injury.",
        counter_arguments=[
            "Load limiter activation is designed behavior - reduces rib fracture risk per biomechanical research",
            "Webbing payout was within design limits (4-6 inches), preventing chest injury while controlling head excursion",
            "Crash severity was extreme - without load limiter, occupant would have suffered fatal chest injuries",
            "Head injury was caused by side impact component, not forward excursion from load limiter function",
            "Seatbelt met FMVSS 209 load requirements - webbing did not tear or separate at anchor points"
        ],
        resolution_strategy="Inspect seatbelt for load limiter payout vs. failure, measure payout distance, demonstrate activation was within design specifications, cite biomechanical studies supporting load limiter benefit, show FMVSS 209 compliance."
    ),

    DoctrineBlock(
        topic="Adaptive Cruise Control (ACC) Following Distance and Emergency Braking",
        keywords=["ACC", "adaptive cruise control", "following distance", "emergency braking", "automatic braking", "radar cruise"],
        conclusion_template="Adaptive Cruise Control maintains set following distance (typically 1-3 seconds) using radar or lidar to track lead vehicle. ACC provides limited braking (typically 0.3-0.4 g) for gradual speed changes, not emergency stops. Driver remains responsible for emergency braking and must be ready to intervene per owner's manual.",
        reasoning_framework="""
1. Verify ACC system type - radar-based, lidar-based, or camera-based following distance control
2. Check ACC following distance setting - driver-selectable (short, medium, long corresponding to 1-3 second gaps)
3. Retrieve ACC intervention data - throttle reduction and brake application by system
4. Assess lead vehicle deceleration rate - ACC limited to ~0.4 g braking, cannot handle emergency stops (>0.6 g)
5. Verify driver reaction - did driver apply brakes when ACC deceleration was insufficient?
6. Review owner's manual limitations - ACC explicitly not designed for emergency braking, driver must intervene
7. Check for ACC disengagement warnings - many systems provide audible/visual alert when braking demand exceeds capability
8. Compare to AEB system - ACC is comfort feature, AEB (if equipped) is emergency collision avoidance
9. Assess driver distraction - ACC may induce overreliance and delayed driver reaction
10. Examine crash causation - was inadequate following distance, excessive speed, or driver inattention primary cause?
""",
        key_factors=[
            "ACC following distance setting",
            "System braking capacity (typically <0.4 g)",
            "Lead vehicle deceleration rate",
            "Driver brake application timing",
            "Owner's manual limitation disclosures",
            "ACC disengagement warning activation",
            "AEB system presence (separate function)",
            "Driver distraction or overreliance"
        ],
        primary_authority=[
            "SAE J2399 - Adaptive Cruise Control Operating Characteristics",
            "NHTSA ACC System Research",
            "ISO 15622 - Adaptive Cruise Control Systems",
            "Owner's Manual ACC Limitations Statements"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles equipped with ACC (increasing 2005+, common on mid-level and luxury vehicles)",
        adversary_position="Plaintiff claims ACC system was defective for failing to brake sufficiently to avoid rear-end collision, alleging system should have provided emergency braking capability.",
        counter_arguments=[
            "ACC is comfort feature, not emergency braking system - owner's manual explicitly disclaims emergency stop capability",
            "Driver has continuous duty to monitor traffic and intervene - ACC does not relieve driver of control responsibility",
            "Lead vehicle braking rate exceeded ACC system design limits (>0.4 g)",
            "Driver was inattentive or overreliant on ACC, failed to brake when system provided disengagement warning",
            "If vehicle had AEB, that system is separate from ACC and has different activation criteria"
        ],
        resolution_strategy="Download ACC system data, show system braked within design limits, cite owner's manual limitations, demonstrate driver failed to intervene as required, distinguish ACC from AEB emergency function."
    ),

    DoctrineBlock(
        topic="Curtain Airbag Deployment in Rollover Crashes",
        keywords=["curtain airbag", "rollover", "side curtain", "roof rail airbag", "roll sensor", "FMVSS 226"],
        conclusion_template="Curtain airbags deploy in side impacts and rollovers to provide head protection and reduce ejection risk. Rollover deployment triggered by roll rate sensor detecting sustained lateral acceleration or angle exceeding threshold (typically 45-60 degrees). FMVSS 226 regulates ejection mitigation but does not mandate specific curtain airbag deployment criteria.",
        reasoning_framework="""
1. Verify curtain airbag system presence - standard on most vehicles 2009+ for FMVSS 226 compliance
2. Retrieve roll sensor data from ACM - lateral acceleration, roll rate (degrees/second), calculated roll angle
3. Assess rollover severity - number of quarter-turns, vehicle angle at maximum roll
4. Check deployment timing - curtain airbags should deploy within 50-80 milliseconds of rollover detection
5. Verify curtain inflation duration - curtains remain inflated 5-7 seconds to cover multiple roof impacts
6. Assess occupant ejection - was occupant fully or partially ejected despite curtain deployment?
7. Check for pre-crash faults - curtain airbag squib open circuit or gas generator degradation may prevent deployment
8. Review window status - open windows reduce curtain effectiveness, may allow partial ejection
9. Compare to FMVSS 226 ejection mitigation test - vehicle rolled multiple times, dummies not ejected
10. Examine injury causation - did curtain airbag reduce injury severity compared to non-deployment scenario?
""",
        key_factors=[
            "Roll rate sensor data (lateral g, roll rate, angle)",
            "Rollover severity (number of rolls)",
            "Curtain deployment timing and duration",
            "Occupant ejection status",
            "Pre-crash curtain airbag system health",
            "Window open/closed status",
            "FMVSS 226 compliance test results",
            "Injury causation analysis"
        ],
        primary_authority=[
            "FMVSS 226 - Ejection Mitigation (49 CFR 571.226)",
            "NHTSA Rollover Crash Tests",
            "SAE J2778 - Side Curtain Airbag System Performance",
            "IIHS Roof Strength and Rollover Research"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles with curtain airbags for FMVSS 226 compliance (phase-in 2009-2012, standard on all 2013+)",
        adversary_position="Plaintiff claims curtain airbag failed to deploy or deployed too late in rollover, allowing occupant ejection and serious injuries, alleging defective roll sensor or deployment algorithm.",
        counter_arguments=[
            "Curtain airbag deployed within design specifications based on roll sensor data",
            "Occupant was unbelted - curtain alone cannot prevent ejection without seatbelt restraint",
            "Window was open, reducing curtain effectiveness - not a design defect",
            "Rollover severity (5+ rolls at high speed) exceeded curtain inflation duration, later rolls allowed ejection",
            "Vehicle met FMVSS 226 ejection mitigation standards in certification testing"
        ],
        resolution_strategy="Download ACM roll sensor data, demonstrate curtain deployment met timing requirements, show FMVSS 226 compliance, prove occupant non-use of seatbelt or open window as causation factor, compare injury to worse outcome without curtain."
    ),

    DoctrineBlock(
        topic="Forward Collision Warning (FCW) Alert Timing and Driver Response",
        keywords=["FCW", "forward collision warning", "collision imminent", "warning alert", "time-to-collision", "TTC"],
        conclusion_template="Forward Collision Warning systems provide visual, audible, or haptic alerts when time-to-collision with lead vehicle falls below threshold (typically 2.0-2.7 seconds). FCW does not apply brakes - driver must respond to warning. Alert timing balances early warning against nuisance alerts that reduce driver trust.",
        reasoning_framework="""
1. Verify FCW system presence and activation status - separate from AEB, may be driver-disableable
2. Retrieve FCW alert history from ADAS module - when did warning activate relative to impact?
3. Calculate time-to-collision (TTC) at warning - distance to lead vehicle divided by closing speed
4. Assess driver reaction time - typical driver brake reaction 1.5-2.0 seconds, warning should provide adequate margin
5. Check for warning suppression - system may delay alert if driver actively braking or steering
6. Verify sensor functionality - radar or camera blockage may prevent lead vehicle detection and warning
7. Review driver response - did driver brake, swerve, or take no action after warning?
8. Compare to SAE J2802 FCW performance recommendations - warning should occur at TTC >1.5 seconds
9. Assess nuisance alert frequency - overly sensitive FCW causes driver to disable or ignore system
10. Examine crash causation - was driver distraction primary cause independent of FCW performance?
""",
        key_factors=[
            "FCW alert timing (TTC at warning)",
            "Driver reaction time and response",
            "Sensor blockage or degradation",
            "Warning suppression logic",
            "Driver FCW disable status",
            "SAE J2802 performance comparison",
            "Nuisance alert history",
            "Driver distraction factors"
        ],
        primary_authority=[
            "SAE J2802 - Forward Collision Warning Performance Requirements",
            "NHTSA FCW System Research",
            "IIHS Front Crash Prevention Test (FCW + AEB)",
            "ISO 15623 - Forward Vehicle Collision Warning Systems"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles equipped with FCW (increasing 2012+, standard on many 2020+ models)",
        adversary_position="Plaintiff claims FCW system was defective for failing to warn or warning too late, alleging driver would have braked and avoided crash if adequate warning provided.",
        counter_arguments=[
            "FCW warning activated at appropriate TTC per SAE J2802 standards",
            "Driver was distracted (phone use, passenger interaction) and did not respond to warning",
            "Driver had manually disabled FCW system due to previous nuisance alerts",
            "Sensor was blocked by dirt or snow, preventing lead vehicle detection - maintenance issue not design defect",
            "Crash occurred despite FCW warning - driver inattention is primary cause, not system failure"
        ],
        resolution_strategy="Download ADAS module FCW alert data, demonstrate warning timing met industry standards, show driver failed to respond to warning, cite driver duty to maintain attention despite ADAS assistance."
    ),

    DoctrineBlock(
        topic="Rear Cross-Traffic Alert (RCTA) Detection Zones and Limitations",
        keywords=["RCTA", "rear cross-traffic alert", "backup", "reverse", "parking lot", "blind spot", "radar"],
        conclusion_template="Rear Cross-Traffic Alert uses rear corner radar sensors to detect vehicles approaching from sides when backing. Detection zone typically 50-60 feet laterally, 20-30 feet rearward. RCTA limited by sensor range, approaching vehicle speed (typically <15 mph detection), and obstructions blocking radar line-of-sight.",
        reasoning_framework="""
1. Verify RCTA system presence - typically packaged with blind spot monitoring on mid-level and luxury vehicles
2. Review detection zone specifications - most systems detect vehicles 50+ feet away approaching at <15 mph
3. Reconstruct crash geometry - was approaching vehicle within RCTA detection zone at time backing initiated?
4. Assess approaching vehicle speed - RCTA may not detect vehicles traveling >20 mph (outside design parameters)
5. Check for sensor blockage - rear bumper damage, hitch, or bike rack may occlude radar sensors
6. Verify RCTA alert occurred - visual, audible, or haptic warning should activate when cross-traffic detected
7. Review driver response - did driver stop backing after RCTA alert, or continue in reverse?
8. Check for RCTA disable - some systems can be manually disabled via vehicle settings
9. Compare to SAE J2802 blind zone detection performance - RCTA subject to similar sensor limitations
10. Assess causation - would driver direct vision (turning to look) have detected approaching vehicle regardless of RCTA?
""",
        key_factors=[
            "RCTA detection zone geometry",
            "Approaching vehicle speed and position",
            "Sensor blockage or misalignment",
            "RCTA alert activation status",
            "Driver response to alert",
            "System manual disable status",
            "Driver direct vision and lookout duty",
            "Crash causation analysis"
        ],
        primary_authority=[
            "SAE J2802 - Rear Cross-Traffic Alert Performance Recommendations",
            "NHTSA Backover Prevention Research",
            "IIHS Crash Avoidance Technology Evaluations",
            "Owner's Manual RCTA Limitations Disclosures"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles equipped with RCTA (increasing 2015+, common on mid-level and luxury vehicles)",
        adversary_position="Plaintiff claims RCTA system was defective for failing to detect approaching vehicle in parking lot backing crash, alleging sensor or algorithm defect.",
        counter_arguments=[
            "Approaching vehicle was traveling too fast (>20 mph) for RCTA detection capability",
            "Approaching vehicle was outside detection zone when backing initiated",
            "Sensor was blocked by aftermarket hitch or bike rack - not manufacturer defect",
            "RCTA did alert, driver ignored warning and continued backing - driver negligence",
            "Driver has duty to check surroundings before backing regardless of RCTA - owner's manual disclaimer"
        ],
        resolution_strategy="Download ADAS module RCTA data, reconstruct approaching vehicle position and speed, demonstrate scenario exceeded system design limitations, cite owner's manual limitations, show driver failed to exercise direct vision duty."
    ),

    DoctrineBlock(
        topic="Headrest and Whiplash Injury Mitigation",
        keywords=["headrest", "whiplash", "WAD", "whiplash-associated disorders", "rear impact", "head restraint", "FMVSS 202a"],
        conclusion_template="Head restraints (headrests) reduce whiplash injury severity in rear-impact crashes by limiting head-to-torso relative motion. FMVSS 202a specifies minimum height and backset (distance from head to restraint) requirements. Proper headrest adjustment by occupant is critical - many occupants leave restraints in lowest position, reducing effectiveness.",
        reasoning_framework="""
1. Verify FMVSS 202a compliance - head restraint must extend 800 mm above seat reference point, backset <55 mm
2. Measure actual headrest position at time of crash - was restraint adjusted to proper height for occupant?
3. Assess rear-impact severity - delta-v and crash pulse duration determine whiplash injury risk
4. Check seatback yielding - some seats allow controlled seatback recline to reduce whiplash, may be misinterpreted as defect
5. Review occupant injury - cervical strain, sprain, or disc injury consistent with whiplash mechanism
6. Compare to IIHS whiplash injury rating - seats rated Good, Acceptable, Marginal, or Poor based on dummy injury criteria
7. Assess headrest design - fixed vs. adjustable, active (self-deploying) vs. passive
8. Check for occupant headrest adjustment - many occupants never raise headrest from lowest position
9. Review biomechanics literature - optimal headrest position is top of restraint at top of head, backset <2 inches
10. Examine alternative causation - pre-existing cervical conditions may be aggravated by minor rear impacts
""",
        key_factors=[
            "FMVSS 202a compliance (height, backset)",
            "Headrest adjustment position at crash",
            "Rear-impact severity (delta-v)",
            "Seatback yielding behavior",
            "Occupant whiplash injury severity",
            "IIHS whiplash rating",
            "Active vs. passive headrest design",
            "Occupant adjustment responsibility"
        ],
        primary_authority=[
            "FMVSS 202a - Head Restraints (49 CFR 571.202a)",
            "IIHS Seat/Head Restraint Evaluations",
            "SAE J2052 - Anthropomorphic Dummy for Rear Impact Testing",
            "Biomechanics of Whiplash Injury (Yoganandan, Ono et al.)"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="All passenger vehicles with front seats per FMVSS 202a (upgraded requirements 2009+)",
        adversary_position="Plaintiff claims headrest was defectively designed, positioned too low or too far back, failing to prevent whiplash injury in rear-impact crash.",
        counter_arguments=[
            "Headrest met FMVSS 202a minimum requirements for height and backset",
            "Occupant failed to adjust headrest to proper height - many drivers leave restraints in lowest position",
            "Seat/headrest combination received Good or Acceptable IIHS whiplash rating - industry-leading performance",
            "Rear-impact severity was minor - whiplash injury may reflect occupant pre-existing cervical condition",
            "Active headrest deployed as designed, reducing injury severity compared to non-deployment scenario"
        ],
        resolution_strategy="Measure headrest position, demonstrate FMVSS 202a compliance, cite IIHS rating, show occupant failed to adjust restraint, cite owner's manual adjustment instructions, compare injury to biomechanical thresholds."
    ),

    DoctrineBlock(
        topic="Child Safety Seat Compatibility and LATCH System",
        keywords=["child seat", "LATCH", "ISOFIX", "lower anchors", "tether anchor", "FMVSS 225", "child restraint"],
        conclusion_template="LATCH (Lower Anchors and Tethers for Children) system provides standardized attachment points for child safety seats per FMVSS 225. Vehicles must provide lower anchors and top tether anchors in rear outboard seating positions. Proper child seat installation is parent/caregiver responsibility - manufacturer provides anchors per regulation, but cannot control installation quality.",
        reasoning_framework="""
1. Verify FMVSS 225 compliance - lower anchors (2 per outboard rear seat) and tether anchor required 2002+ vehicles
2. Inspect LATCH anchor installation - anchors must withstand 22,240 N (5000 lbf) load per FMVSS 225
3. Assess child seat installation method - LATCH vs. vehicle seatbelt installation
4. Check for LATCH weight limits - most systems rated for child+seat weight up to 65 lbs
5. Verify tether anchor use - top tether reduces head excursion in frontal crashes, many parents fail to use
6. Inspect child seat for proper attachment - loose installation or incorrect connector routing reduces effectiveness
7. Review child seat recall status - defective seats may have harness or buckle failures independent of vehicle LATCH
8. Assess crash severity - extreme crashes may exceed child seat design limits regardless of installation method
9. Check for multiple child seats - LATCH anchors typically not designed for 3-across installation, center seat may require seatbelt
10. Examine injury causation - was child properly harnessed in seat, or loose/missing harness straps?
""",
        key_factors=[
            "FMVSS 225 LATCH anchor compliance",
            "Child seat installation method (LATCH vs. belt)",
            "LATCH weight limit compliance",
            "Top tether use",
            "Child seat attachment tightness",
            "Child seat recall status",
            "Crash severity vs. seat design limits",
            "Child harness use"
        ],
        primary_authority=[
            "FMVSS 225 - Child Restraint Anchorage Systems (49 CFR 571.225)",
            "FMVSS 213 - Child Restraint Systems (child seat standards)",
            "NHTSA Ease of Use Rating for Child Seats",
            "SAE J1819 - Child Restraint Anchorage System"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles with LATCH anchors (required 2002+ per FMVSS 225)",
        adversary_position="Plaintiff (parent/guardian) claims LATCH anchors were defectively designed or installed, failing to secure child seat and causing child injuries in crash.",
        counter_arguments=[
            "LATCH anchors met FMVSS 225 load requirements in certification testing",
            "Child seat was improperly installed - loose attachment or missing tether despite proper anchor design",
            "Parent exceeded LATCH weight limit (child+seat >65 lbs) - seatbelt installation should have been used",
            "Child seat itself was recalled for defect - anchor system performed as designed",
            "Crash severity was extreme - child seat and anchors functioned but could not eliminate all injury"
        ],
        resolution_strategy="Inspect LATCH anchors for damage or pull-out, demonstrate FMVSS 225 compliance, show child seat installation errors, cite weight limits, prove proper anchor function despite crash outcome."
    ),

    DoctrineBlock(
        topic="Daytime Running Lights (DRL) and Rear-End Collision Visibility",
        keywords=["DRL", "daytime running lights", "visibility", "conspicuity", "rear-end", "FMVSS 108", "lighting"],
        conclusion_template="Daytime Running Lights improve vehicle conspicuity in daylight conditions, reducing front-into-rear and front-into-side crashes. FMVSS 108 allows but does not require DRL. Rear-end crash liability typically rests with following driver regardless of lead vehicle DRL presence - following driver has duty to maintain safe distance and speed.",
        reasoning_framework="""
1. Verify DRL system presence - many vehicles 2000+ have DRL (required in Canada, optional in US)
2. Check DRL activation status - system should automatically activate when engine running and headlamp switch in auto or off
3. Assess visibility conditions - DRL most effective in dawn/dusk/overcast conditions, less critical in full daylight
4. Review FMVSS 108 compliance - DRL intensity 500-1500 candela, less than full headlamps to avoid glare
5. Compare crash statistics - DRL reduces daytime collisions by 5-10% per NHTSA studies, not 100% prevention
6. Assess following driver conduct - excessive speed, tailgating, or distraction as primary crash cause
7. Check for lead vehicle brake light function - brake lights more critical than DRL for rear-end collision prevention
8. Verify DRL bulb status - burned-out DRL bulb reduces conspicuity but is maintenance issue not design defect
9. Examine alternative conspicuity factors - vehicle color, size, and reflectivity affect visibility independent of DRL
10. Review comparative negligence - even without DRL, following driver duty to avoid collision remains
""",
        key_factors=[
            "DRL system presence and activation",
            "Visibility conditions (lighting, weather)",
            "FMVSS 108 compliance",
            "Crash statistics and DRL effectiveness",
            "Following driver conduct",
            "Brake light function",
            "DRL bulb maintenance",
            "Vehicle conspicuity factors"
        ],
        primary_authority=[
            "FMVSS 108 - Lamps, Reflective Devices, and Associated Equipment",
            "NHTSA Daytime Running Lights Research",
            "IIHS DRL Effectiveness Studies",
            "SAE J2087 - Daytime Running Lamps"
        ],
        confidence=ConfidenceLevel.DISCLOSURE,
        entity_scope="Vehicles with DRL (increasingly common 1995+, standard on many 2010+ models)",
        adversary_position="Plaintiff (following driver) claims lead vehicle without DRL or with non-functional DRL was not conspicuous, contributing to rear-end collision.",
        counter_arguments=[
            "DRL is not required by FMVSS 108 - absence of DRL is not defect or regulatory violation",
            "Following driver has duty to maintain safe following distance and speed regardless of lead vehicle lighting",
            "Brake lights (FMVSS 108 required) were functional - following driver should have seen brake activation",
            "Visibility conditions were clear daylight - DRL absence not causative factor in conspicuity",
            "Following driver was distracted or speeding - comparative negligence reduces or eliminates liability"
        ],
        resolution_strategy="Demonstrate DRL is optional per FMVSS 108, show brake lights were functional, prove following driver had duty to avoid collision, cite comparative negligence statutes."
    ),

    DoctrineBlock(
        topic="Backup Camera and Rear Visibility Standards FMVSS 111",
        keywords=["backup camera", "rearview camera", "rear visibility", "FMVSS 111", "backover", "blind zone"],
        conclusion_template="FMVSS 111 requires backup cameras on all vehicles <10,000 lbs GVWR manufactured May 2018+. Camera must display view directly behind vehicle covering 10x20 foot zone within 2 seconds of shift to reverse. Backup cameras reduce but do not eliminate backover crashes - driver must still check surroundings and monitor camera display.",
        reasoning_framework="""
1. Verify FMVSS 111 compliance - backup camera required on subject vehicle based on manufacture date
2. Check camera functionality - was image displayed on screen when shifted to reverse?
3. Assess camera field of view - FMVSS 111 requires 10-foot width, 20-foot depth from rear bumper
4. Review camera image quality - dirt, water spots, or lens damage may obscure view
5. Verify driver monitoring - did driver look at camera display or ignore it?
6. Check for guideline overlay - many cameras show projected path guidelines, reducing spatial judgment errors
7. Assess pedestrian/object location - was object within camera field of view at time backing initiated?
8. Review NHTSA backover crash statistics - cameras reduce backover crashes by ~17%, not 100%
9. Compare to other detection methods - ultrasonic parking sensors may provide additional warning
10. Examine driver duty - backup camera supplements but does not replace driver duty to check mirrors and surroundings
""",
        key_factors=[
            "FMVSS 111 compliance (manufacture date, field of view)",
            "Camera functionality and image quality",
            "Driver camera monitoring behavior",
            "Guideline overlay presence",
            "Pedestrian/object position in camera view",
            "Backover crash reduction statistics",
            "Supplemental parking sensors",
            "Driver duty to check surroundings"
        ],
        primary_authority=[
            "FMVSS 111 - Rear Visibility (49 CFR 571.111)",
            "NHTSA Backover Prevention Final Rule (2014)",
            "Cameron Gulbransen Kids Transportation Safety Act (2008)",
            "IIHS Rear Visibility Ratings"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles <10,000 lbs GVWR manufactured May 2018+ per FMVSS 111 mandate",
        adversary_position="Plaintiff claims backup camera was defective or inadequate, failing to prevent backover crash involving pedestrian or object behind vehicle.",
        counter_arguments=[
            "Camera met FMVSS 111 field of view requirements - pedestrian was visible in display",
            "Driver failed to monitor camera display or check mirrors before backing",
            "Camera lens was dirty or obscured - maintenance issue not design defect",
            "Pedestrian entered camera field of view after backing began - camera cannot predict future movements",
            "Driver has duty to ensure area behind vehicle is clear regardless of camera - owner's manual disclaimer"
        ],
        resolution_strategy="Demonstrate FMVSS 111 compliance, show camera displayed clear image, prove driver failed to monitor display, cite backover crash reduction statistics vs. 100% prevention expectation, show driver duty to check surroundings."
    ),

    DoctrineBlock(
        topic="Knee Airbag Deployment and Lower Extremity Injury",
        keywords=["knee airbag", "knee bolster", "tibia fracture", "femur fracture", "lower extremity", "footwell intrusion"],
        conclusion_template="Knee airbags deploy from lower instrument panel to reduce tibia, femur, and knee injuries in frontal crashes by controlling lower extremity kinematics. Deployment may cause minor abrasions but prevents more severe fractures. Knee airbag effectiveness depends on occupant seating position, seatbelt use, and footwell intrusion severity.",
        reasoning_framework="""
1. Verify knee airbag system presence - increasingly common in frontal airbag systems 2010+
2. Retrieve deployment data from ACM - did knee airbag deploy concurrently with frontal airbag?
3. Assess occupant seating position - knee airbag calibrated for driver, may not cover passenger effectively
4. Check seatbelt use - knee airbag works in conjunction with seatbelt to control occupant kinematics
5. Review lower extremity injury pattern - tibia/femur fractures suggest high loading despite knee airbag
6. Examine footwell intrusion - severe intrusion may overwhelm knee airbag protection capability
7. Compare to NCAP lower extremity injury criteria - tibia index and femur load thresholds
8. Assess knee airbag deployment force - minor bruising or abrasion is expected and acceptable tradeoff
9. Check for pre-crash occupant position - feet on dash or cross-legged sitting may negate knee airbag effectiveness
10. Review biomechanics literature - optimal knee airbag reduces tibia load by 20-40% per crash tests
""",
        key_factors=[
            "Knee airbag deployment status",
            "Occupant seating position and size",
            "Seatbelt use",
            "Lower extremity injury severity",
            "Footwell intrusion extent",
            "NCAP lower extremity injury criteria",
            "Deployment force vs. injury prevention",
            "Occupant position (feet on dash, etc.)"
        ],
        primary_authority=[
            "NHTSA NCAP Lower Extremity Injury Criteria",
            "SAE J2570 - Frontal Impact Restraint System Evaluation",
            "IIHS Small Overlap Test Lower Extremity Ratings",
            "Biomechanics of Lower Extremity Injuries (Yoganandan)"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="Vehicles with knee airbags for driver and/or passenger (increasing 2010+)",
        adversary_position="Plaintiff claims knee airbag deployed with excessive force causing knee and leg injuries, or failed to deploy allowing preventable fractures.",
        counter_arguments=[
            "Knee airbag deployed as designed, minor abrasions are expected and prevent more severe fractures",
            "Severe footwell intrusion overwhelmed knee airbag capability - intrusion reduction is separate crashworthiness issue",
            "Occupant was not using seatbelt - knee airbag effectiveness depends on seatbelt restraint",
            "Occupant had feet on dash (out-of-position) - negates knee airbag protection",
            "Lower extremity injuries were less severe than would have occurred without knee airbag deployment"
        ],
        resolution_strategy="Download ACM data confirming deployment, measure footwell intrusion, assess seatbelt use, compare injury to biomechanical thresholds, demonstrate injury mitigation vs. non-deployment scenario."
    ),

    DoctrineBlock(
        topic="Post-Crash Fuel System Integrity and Fire Risk FMVSS 301",
        keywords=["fuel leak", "post-crash fire", "fuel system integrity", "FMVSS 301", "fuel tank", "fuel line rupture"],
        conclusion_template="FMVSS 301 requires fuel system to limit fuel spillage to 28 ounces in 30-mph frontal and rear-impact barrier crashes. Post-crash fires are rare (<5% of crashes) and often involve catastrophic crash severity exceeding FMVSS 301 test conditions. Fuel system compliance with FMVSS 301 is strong defense, but extreme crashes may rupture fuel system components.",
        reasoning_framework="""
1. Verify FMVSS 301 compliance - manufacturer certification data for frontal and rear fuel spillage tests
2. Assess crash severity - was impact speed and direction within or exceeding FMVSS 301 test envelope (30 mph barrier)?
3. Inspect fuel system post-crash - locate rupture point (tank, filler neck, fuel line, fuel pump)
4. Measure fuel spillage quantity - compare to 28-ounce (828 ml) FMVSS 301 limit
5. Check for secondary impacts - fuel tank rupture often occurs in side or rear secondary impact, not initial frontal crash
6. Review fire origin - was fuel ignition source from fuel spillage, or electrical short/hot exhaust independent of leak?
7. Assess fuel tank location - rear-mounted tanks more vulnerable in rear-end crashes, saddle tanks in side impacts
8. Examine crash reconstruction - was fuel spillage inevitable given crash severity, or was tank design deficient?
9. Review recall history - some fuel tanks had defective welds or insufficient impact protection
10. Compare to crash fire statistics - NHTSA data shows post-crash fires in <5% of tow-away crashes
""",
        key_factors=[
            "FMVSS 301 compliance certification",
            "Crash severity vs. test conditions",
            "Fuel rupture location",
            "Fuel spillage quantity measured",
            "Secondary impact presence",
            "Fire ignition source",
            "Fuel tank location and protection",
            "Recall history"
        ],
        primary_authority=[
            "FMVSS 301 - Fuel System Integrity (49 CFR 571.301)",
            "NHTSA Post-Crash Fire Statistics",
            "SAE J2553 - Fuel System Crashworthiness",
            "IIHS Post-Crash Fire Research"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        entity_scope="All passenger vehicles per FMVSS 301 (upgraded requirements 1993+)",
        adversary_position="Plaintiff claims fuel tank was defectively designed or located, rupturing in crash and causing fire that resulted in severe burn injuries or death.",
        counter_arguments=[
            "Vehicle complied with FMVSS 301 fuel spillage limits in certification testing",
            "Crash severity (e.g., 60 mph impact) far exceeded FMVSS 301 test conditions (30 mph)",
            "Fuel tank rupture occurred in secondary rear-end impact by another vehicle - not foreseeable design case",
            "Fire ignition was electrical short circuit, not fuel leak - fuel spillage did not cause fire",
            "Fuel tank location and design met industry standards - other similar vehicles have same configuration"
        ],
        resolution_strategy="Obtain FMVSS 301 certification data, reconstruct crash severity, demonstrate compliance with regulatory standard, show crash exceeded test envelope, identify alternative fire ignition source if applicable."
    ),
]


# ============================================================================
# GLOBAL STATE
# ============================================================================

START_TIME = datetime.now()
TOTAL_QUERIES = 0
TOTAL_LATENCY_MS = 0.0
CACHE_HITS = 0
CACHE_MISSES = 0


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.query_log: List[Dict[str, Any]] = []
        self.error_log: List[Dict[str, Any]] = []

    def log_query(self, query: str, mode: ResponseMode, zone: AnalysisZone,
                  latency_ms: float, triggered_doctrines: List[str],
                  source_layer: str, confidence: ConfidenceLevel):
        global TOTAL_QUERIES, TOTAL_LATENCY_MS
        TOTAL_QUERIES += 1
        TOTAL_LATENCY_MS += latency_ms

        self.query_log.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "mode": mode.value,
            "zone": zone.value,
            "latency_ms": latency_ms,
            "triggered_doctrines": triggered_doctrines,
            "source_layer": source_layer,
            "confidence": confidence.value
        })

    def log_error(self, error: str, context: str):
        self.error_log.append({
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "context": context
        })


TELEMETRY = TelemetryCollector()


# ============================================================================
# SEMANTIC NORMALIZATION
# ============================================================================

SAFETY_SYSTEM_SYNONYMS = {
    "airbag": ["air bag", "SRS", "supplemental restraint", "inflatable restraint"],
    "seatbelt": ["seat belt", "safety belt", "restraint belt", "three-point belt"],
    "pretensioner": ["pre-tensioner", "belt tensioner", "retractor pretensioner"],
    "AEB": ["automatic emergency braking", "auto emergency brake", "collision mitigation"],
    "FCW": ["forward collision warning", "collision warning", "front collision alert"],
    "ACC": ["adaptive cruise control", "radar cruise", "active cruise control"],
    "LDW": ["lane departure warning", "lane drift warning"],
    "LKA": ["lane keep assist", "lane keeping assist", "lane centering"],
    "BSM": ["blind spot monitoring", "blind spot detection", "blind zone alert"],
    "RCTA": ["rear cross-traffic alert", "cross-traffic warning"],
    "ESC": ["electronic stability control", "stability control", "VSC", "DSC"],
    "TPMS": ["tire pressure monitoring", "tire pressure sensor", "low pressure warning"],
    "DRL": ["daytime running lights", "daytime running lamps", "running lights"],
    "CDR": ["crash data recorder", "EDR", "event data recorder", "black box"],
    "OCS": ["occupant classification system", "seat sensor", "weight sensor"],
    "LATCH": ["lower anchors and tethers", "ISOFIX", "child seat anchors"],
}


def normalize_query(query: str) -> str:
    """Normalize automotive safety terminology"""
    query_lower = query.lower()
    for canonical, synonyms in SAFETY_SYSTEM_SYNONYMS.items():
        for synonym in synonyms:
            query_lower = query_lower.replace(synonym, canonical)
    return query_lower


# ============================================================================
# DOCTRINE CACHE SEARCH
# ============================================================================

def search_doctrine_cache(query: str) -> List[DoctrineBlock]:
    """Fast keyword-based search of doctrine cache (0-200ms)"""
    global CACHE_HITS, CACHE_MISSES

    query_normalized = normalize_query(query)
    query_terms = set(query_normalized.lower().split())

    matches: List[Tuple[DoctrineBlock, int]] = []
    for doctrine in DOCTRINE_CACHE:
        keyword_set = set(k.lower() for k in doctrine.keywords)
        overlap = len(query_terms.intersection(keyword_set))
        if overlap > 0:
            matches.append((doctrine, overlap))

    if matches:
        CACHE_HITS += 1
        matches.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in matches[:5]]
    else:
        CACHE_MISSES += 1
        return []


# ============================================================================
# AUTHORITY HARDENING
# ============================================================================

AUTHORITY_WEIGHTS = {
    "FMVSS": 1.0,
    "NHTSA": 0.95,
    "SAE": 0.85,
    "IIHS": 0.80,
    "ISO": 0.75,
    "Manufacturer": 0.60,
}


def calculate_authority_score(authorities: List[str]) -> float:
    """Weight authorities by regulatory vs. advisory vs. industry standards"""
    if not authorities:
        return 0.5

    scores = []
    for auth in authorities:
        for key, weight in AUTHORITY_WEIGHTS.items():
            if key.lower() in auth.lower():
                scores.append(weight)
                break
        else:
            scores.append(0.5)

    return sum(scores) / len(scores)


# ============================================================================
# CONFIDENCE STRATIFICATION
# ============================================================================

def stratify_confidence(triggered_doctrines: List[DoctrineBlock],
                        authority_score: float) -> ConfidenceLevel:
    """Stratify confidence based on doctrine quality and authority strength"""
    if not triggered_doctrines:
        return ConfidenceLevel.DISCLOSURE

    defensible_count = sum(1 for d in triggered_doctrines if d.confidence == ConfidenceLevel.DEFENSIBLE)

    if defensible_count >= 2 and authority_score > 0.85:
        return ConfidenceLevel.DEFENSIBLE
    elif defensible_count >= 1 and authority_score > 0.70:
        return ConfidenceLevel.AGGRESSIVE
    elif authority_score > 0.60:
        return ConfidenceLevel.DISCLOSURE
    else:
        return ConfidenceLevel.HIGH_RISK


# ============================================================================
# FACT FRAGILITY SCORING
# ============================================================================

def calculate_fragility(query: str, triggered_doctrines: List[DoctrineBlock]) -> float:
    """Score how fragile the factual basis is (0.0=solid, 1.0=very fragile)"""
    fragility = 0.0

    # Check for data recorder availability
    if "CDR" in query.upper() or "crash data recorder" in query.lower():
        fragility -= 0.3

    # Check for witness or physical evidence
    if "witness" in query.lower() or "video" in query.lower():
        fragility -= 0.2

    # Speculation or assumptions increase fragility
    speculation_terms = ["possibly", "might", "could have", "maybe", "assume"]
    for term in speculation_terms:
        if term in query.lower():
            fragility += 0.2

    # Multiple doctrines reduce fragility
    if len(triggered_doctrines) > 2:
        fragility -= 0.15

    return max(0.0, min(1.0, 0.5 + fragility))


# ============================================================================
# EPISTEMIC GUARDRAILS
# ============================================================================

def apply_epistemic_guardrails(response: str) -> Tuple[str, List[str]]:
    """Detect and flag banned overstatements"""
    flags = []

    for phrase in BANNED_PHRASES:
        if phrase.lower() in response.lower():
            flags.append(f"BANNED_PHRASE: '{phrase}'")

    # Add mandatory disclosure if high-risk terms detected
    if any(term in response.lower() for term in ["defect", "failure", "malfunction"]):
        if "compliance with FMVSS" not in response:
            flags.append("MISSING_REGULATORY_CONTEXT")

    return response, flags


# ============================================================================
# ISSUE CATEGORIZATION
# ============================================================================

def categorize_issues(query: str, triggered_doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
    """Multi-label issue categorization"""
    categories: Set[IssueCategory] = set()

    query_lower = query.lower()

    if any(term in query_lower for term in ["airbag", "deploy", "SRS"]):
        categories.add(IssueCategory.AIRBAG_DEPLOYMENT)

    if any(term in query_lower for term in ["seatbelt", "pretensioner", "belt"]):
        categories.add(IssueCategory.SEATBELT_MALFUNCTION)

    if any(term in query_lower for term in ["AEB", "FCW", "collision warning", "emergency braking"]):
        categories.add(IssueCategory.CRASH_AVOIDANCE)

    if any(term in query_lower for term in ["occupant", "injury", "protection", "restraint"]):
        categories.add(IssueCategory.OCCUPANT_PROTECTION)

    if any(term in query_lower for term in ["pedestrian", "backover", "cross-traffic"]):
        categories.add(IssueCategory.PEDESTRIAN_SAFETY)

    if any(term in query_lower for term in ["FMVSS", "compliance", "regulation", "standard"]):
        categories.add(IssueCategory.FMVSS_COMPLIANCE)

    if any(term in query_lower for term in ["sensor", "fault", "DTC", "malfunction"]):
        categories.add(IssueCategory.SENSOR_FAULT)

    if any(term in query_lower for term in ["recall", "liability", "defect"]):
        categories.add(IssueCategory.RECALL_LIABILITY)

    return list(categories)


# ============================================================================
# RESPONSE GENERATION
# ============================================================================

def generate_fast_response(triggered_doctrines: List[DoctrineBlock]) -> str:
    """FAST mode: 2-3 sentence concise answer"""
    if not triggered_doctrines:
        return "No direct safety system doctrine matches found. Recommend analyzing crash data recorder (CDR) output, reviewing FMVSS compliance test data, and consulting manufacturer technical service bulletins for subject vehicle year/make/model."

    primary = triggered_doctrines[0]
    return f"{primary.conclusion_template} Key factors: {', '.join(primary.key_factors[:3])}. Primary authority: {primary.primary_authority[0]}."


def generate_defense_response(triggered_doctrines: List[DoctrineBlock],
                               query: SafetyQueryRequest) -> str:
    """DEFENSE mode: audit-ready analysis with adversary positions"""
    if not triggered_doctrines:
        return "Insufficient doctrine coverage for safety system analysis. Recommend expert reconstruction and CDR data download."

    sections = []
    for doctrine in triggered_doctrines[:3]:
        sections.append(f"**{doctrine.topic}**\n\n{doctrine.conclusion_template}\n\n"
                       f"Counter-arguments: {'; '.join(doctrine.counter_arguments[:2])}\n\n"
                       f"Resolution: {doctrine.resolution_strategy}")

    return "\n\n---\n\n".join(sections)


def generate_memo_response(triggered_doctrines: List[DoctrineBlock],
                           query: SafetyQueryRequest) -> str:
    """MEMO mode: comprehensive documentation with full reasoning"""
    if not triggered_doctrines:
        return "Comprehensive memo unavailable - no doctrine cache hits. Recommend manual research of FMVSS regulations, NHTSA technical bulletins, and manufacturer service information for subject safety system."

    sections = [f"# Automotive Safety System Analysis - {query.zone.value}\n"]

    for i, doctrine in enumerate(triggered_doctrines[:5], 1):
        sections.append(f"## {i}. {doctrine.topic}\n")
        sections.append(f"**Conclusion:** {doctrine.conclusion_template}\n")
        sections.append(f"**Reasoning Framework:**\n{doctrine.reasoning_framework}\n")
        sections.append(f"**Key Factors:** {', '.join(doctrine.key_factors)}\n")
        sections.append(f"**Primary Authority:** {', '.join(doctrine.primary_authority)}\n")
        sections.append(f"**Adversary Position:** {doctrine.adversary_position}\n")
        sections.append(f"**Counter-Arguments:** {'; '.join(doctrine.counter_arguments)}\n")
        sections.append(f"**Resolution Strategy:** {doctrine.resolution_strategy}\n")
        sections.append(f"**Confidence:** {doctrine.confidence.value}\n")

    return "\n".join(sections)


# ============================================================================
# THREE-LAYER RESPONSE ENGINE
# ============================================================================

def three_layer_response(request: SafetyQueryRequest) -> SafetyAnalysisResponse:
    """
    Layer 1: Doctrine cache (0-200ms)
    Layer 2: Semantic retrieval (200-800ms) - placeholder for vector search
    Layer 3: Deep analysis with external knowledge - placeholder
    """
    start_time = datetime.now()

    # Layer 1: Doctrine cache
    triggered_doctrines = search_doctrine_cache(request.query)
    source_layer = "DOCTRINE_CACHE"

    # Layer 2: Semantic retrieval (simulated)
    if not triggered_doctrines:
        # In production, this would call vector search
        triggered_doctrines = DOCTRINE_CACHE[:2]  # Fallback
        source_layer = "SEMANTIC_RETRIEVAL"

    # Generate response based on mode
    if request.mode == ResponseMode.FAST:
        answer = generate_fast_response(triggered_doctrines)
    elif request.mode == ResponseMode.DEFENSE:
        answer = generate_defense_response(triggered_doctrines, request)
    else:  # MEMO
        answer = generate_memo_response(triggered_doctrines, request)

    # Apply epistemic guardrails
    answer, epistemic_flags = apply_epistemic_guardrails(answer)

    # Calculate metrics
    authorities = []
    for d in triggered_doctrines:
        authorities.extend(d.primary_authority)
    authority_score = calculate_authority_score(authorities)
    confidence = stratify_confidence(triggered_doctrines, authority_score)
    fragility = calculate_fragility(request.query, triggered_doctrines)

    # Categorize issues
    issue_categories = categorize_issues(request.query, triggered_doctrines)

    # Extract FMVSS references
    fmvss_refs = [auth for auth in authorities if "FMVSS" in auth]

    # Determinism hash
    hash_input = f"{request.query}|{request.mode.value}|{source_layer}"
    determinism_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    latency_ms = (datetime.now() - start_time).total_seconds() * 1000

    # Telemetry
    TELEMETRY.log_query(
        request.query, request.mode, request.zone, latency_ms,
        [d.topic for d in triggered_doctrines], source_layer, confidence
    )

    return SafetyAnalysisResponse(
        answer=answer,
        triggered_doctrines=[d.topic for d in triggered_doctrines],
        confidence=confidence,
        issue_categories=issue_categories,
        source_layer=source_layer,
        latency_ms=latency_ms,
        determinism_hash=determinism_hash,
        fmvss_references=fmvss_refs,
        fragility_score=fragility,
        epistemic_flags=epistemic_flags
    )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="AUTO15 Safety Systems Analysis Engine",
    description="TIE-Grade Automotive Safety Intelligence Engine - Airbag, Seatbelt, ADAS, FMVSS Compliance",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@APP.post("/query", response_model=SafetyAnalysisResponse)
async def query_safety_system(request: SafetyQueryRequest):
    """Primary safety system analysis endpoint"""
    try:
        return three_layer_response(request)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        TELEMETRY.log_error(str(e), request.query)
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check with metrics"""
    uptime = (datetime.now() - START_TIME).total_seconds()
    cache_hit_rate = CACHE_HITS / (CACHE_HITS + CACHE_MISSES) if (CACHE_HITS + CACHE_MISSES) > 0 else 0.0
    avg_latency = TOTAL_LATENCY_MS / TOTAL_QUERIES if TOTAL_QUERIES > 0 else 0.0

    return HealthResponse(
        status="operational",
        version="1.0.0",
        port=9325,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=uptime,
        total_queries=TOTAL_QUERIES,
        cache_hit_rate=cache_hit_rate,
        avg_latency_ms=avg_latency
    )


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [{"topic": d.topic, "keywords": d.keywords} for d in DOCTRINE_CACHE]
    }


@APP.get("/telemetry")
async def get_telemetry():
    """Retrieve telemetry data"""
    return {
        "query_log": TELEMETRY.query_log[-50:],
        "error_log": TELEMETRY.error_log[-20:],
        "total_queries": TOTAL_QUERIES,
        "cache_hits": CACHE_HITS,
        "cache_misses": CACHE_MISSES
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.add(
        Path(__file__).parent / "logs" / "auto15_safety_{time}.log",
        rotation="100 MB",
        retention="30 days",
        level="INFO"
    )

    logger.info("AUTO15 Safety Systems Analysis Engine starting on port 9325")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} safety system doctrine blocks")

    uvicorn.run(APP, host="0.0.0.0", port=9325, log_level="info")
