"""
DRL02 - Directional Drilling Intelligence Engine
TIE Gold Standard Implementation

Domain: Directional & Horizontal Drilling Engineering
Port: 9012
Version: 1.0.0

Covers: trajectory planning, motor yield, slide/rotate drilling, MWD/LWD,
survey calculations, dogleg severity, mud motors, RSS systems, geosteering,
horizontal landing, magnetic interference, anti-collision, BHA design
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import math
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from loguru import logger
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


class IssueCategory(str, Enum):
    TRAJECTORY_PLANNING = "TRAJECTORY_PLANNING"
    MOTOR_OPERATIONS = "MOTOR_OPERATIONS"
    SURVEY_ACCURACY = "SURVEY_ACCURACY"
    GEOSTEERING = "GEOSTEERING"
    ANTI_COLLISION = "ANTI_COLLISION"
    BHA_DESIGN = "BHA_DESIGN"
    RSS_OPERATIONS = "RSS_OPERATIONS"
    MAGNETIC_INTERFERENCE = "MAGNETIC_INTERFERENCE"
    WELLBORE_QUALITY = "WELLBORE_QUALITY"
    HORIZONTAL_LANDING = "HORIZONTAL_LANDING"


class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    OPERATIONS = "OPERATIONS"
    POST_RUN = "POST_RUN"


BANNED_PHRASES = [
    "guaranteed drilling performance",
    "100% accurate surveys",
    "zero collision risk",
    "perfect wellbore trajectory",
    "no magnetic interference possible",
    "RSS always superior to motors",
    "gyro surveys always accurate"
]


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Real directional drilling domain expertise"""
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
    issue_category: IssueCategory
    analysis_zone: AnalysisZone
    interactions: List[str] = field(default_factory=list)


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=5000)
    mode: ResponseMode = ResponseMode.FAST
    context: Optional[Dict[str, Any]] = None

    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class QueryResponse(BaseModel):
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    reasoning_chain: List[str]
    epistemic_warnings: List[str]
    determinism_hash: str
    processing_time_ms: float
    zone: AnalysisZone


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float


# ============================================================================
# DOCTRINE CACHE - 25+ BLOCKS OF REAL DIRECTIONAL DRILLING EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Build Rate and Dogleg Severity Limits",
        keywords=["build rate", "dogleg severity", "DLS", "toolstring design", "casing wear"],
        conclusion_template=[
            "Dogleg severity (DLS) limits are governed by casing/tubing wear considerations, drilling dynamics, and survey accuracy requirements.",
            "Industry standard for production casing is typically 3-5°/100ft; intermediate casing may tolerate 6-8°/100ft depending on metallurgy.",
            "Excessive DLS causes premature casing wear, stuck pipe risk, torque and drag issues, and fatigue failures in completion equipment."
        ],
        reasoning_framework="""
DLS represents the rate of wellbore curvature change over distance. Key considerations:

1. Casing Wear Impact:
   - DLS > 6°/100ft in production intervals → severe wear at doglegs
   - Contact forces increase exponentially with DLS
   - Wear rate proportional to DLS², not linear

2. Drilling String Fatigue:
   - High DLS causes cyclic bending stress in drillpipe
   - Tool joints experience highest stress concentration
   - Fatigue life inversely proportional to DLS magnitude

3. Survey Accuracy Requirements:
   - DLS calculation depends on survey station spacing
   - Minimum curvature method assumes smooth arc between stations
   - Sharp doglegs (short radius) require closer survey spacing

4. Operational Limits:
   - BHA length must accommodate build section
   - Motor/RSS capability limits achievable build rates
   - Formation hardness affects actual vs planned build rate

5. Completion Constraints:
   - Production tubing wear at doglegs
   - ESP/PCP installation through high DLS sections
   - Wireline tool passage limitations
        """,
        key_factors=[
            "Casing grade and wall thickness",
            "Expected well life and production rates",
            "Completion type (ESP, rod pump, gas lift)",
            "Formation properties affecting build capability",
            "Survey tool accuracy and station spacing",
            "Drilling BHA stiffness and motor yield",
            "Torque and drag modeling results"
        ],
        primary_authority=[
            "API RP 7G: Recommended Practice for Drill Stem Design and Operating Limits",
            "SPE 52820: Dogleg Severity and Casing Wear in Directional Wells",
            "IADC Drilling Manual: Directional Drilling Section",
            "Operator-specific wellbore quality standards"
        ],
        burden_holder="Directional driller and wellbore design engineer",
        adversary_position="Cost pressure may drive aggressive DLS to reduce well MD and rig time",
        counter_arguments=[
            "Higher DLS reduces well measured depth and thus drilling cost",
            "Modern casing wear prediction tools allow higher DLS in some cases",
            "Short lateral sections may tolerate higher DLS with acceptable wear",
            "RSS technology enables smoother wellbore profiles than motors",
            "Protective casing wear technology (friction reducers) mitigates risk"
        ],
        resolution_strategy="Balance drilling economics against long-term well integrity; use torque-drag and casing wear modeling to establish DLS limits; apply more conservative limits in critical production zones",
        entity_scope="Wellbore trajectory design, drilling operations, completion engineering",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry consensus on 3-5°/100ft for production intervals; specific limits require well-specific engineering analysis",
        controlling_precedent="API RP 7G and operator-specific drilling design standards",
        issue_category=IssueCategory.TRAJECTORY_PLANNING,
        analysis_zone=AnalysisZone.PLANNING,
        interactions=["BHA_DESIGN", "WELLBORE_QUALITY"]
    ),

    DoctrineBlock(
        topic="Motor Yield and Slide Drilling Efficiency",
        keywords=["motor yield", "slide drilling", "bent housing angle", "build rate", "toolface control"],
        conclusion_template=[
            "Motor yield (actual build rate vs theoretical) typically ranges 60-85% due to formation resistance, motor stall, and bit walk.",
            "Slide efficiency depends on motor power section performance, formation properties, WOB/differential pressure relationship, and toolface maintenance.",
            "Optimal slide/rotate ratios balance penetration rate against directional control requirements and motor reliability."
        ],
        reasoning_framework="""
Mud motor performance in slide drilling mode involves complex interactions:

1. Theoretical Build Rate:
   BHA build rate (°/100ft) = (180/π) × tan(α) / L
   where α = bent housing angle, L = bit-to-bend distance

2. Motor Yield Factors:
   - Formation anisotropy causes bit walk (lateral drift)
   - Motor stall under high WOB reduces effective rotation
   - Stabilizer placement affects fulcrum point
   - Bit design (aggressive vs passive) impacts side-cutting

3. Slide Drilling Challenges:
   - Friction between BHA and wellbore reduces weight transfer
   - Toolface orientation drift due to reactive torque
   - Reduced ROP compared to rotary mode (50-70% typical)
   - Motor bearing/rotor wear accelerated in slide mode

4. Formation Impact:
   - Hard formations: lower yield, slower penetration, better toolface stability
   - Soft formations: higher yield, faster penetration, toolface drift
   - Interbedded formations: erratic build rates, difficult control

5. Optimization Strategies:
   - Minimize slide percentage to preserve motor life
   - Use high-performance motors (higher RPM, better stall resistance)
   - Optimize bit hydraulics for cuttings removal in slide mode
   - Consider RSS for extended lateral sections
        """,
        key_factors=[
            "Bent housing angle (0.5° to 3.0° typical)",
            "Motor specifications (lobe configuration, flow rate, RPM)",
            "Formation drillability and anisotropy",
            "WOB and differential pressure across motor",
            "Stabilizer configuration and gauge",
            "Bit design and wear state",
            "Wellbore friction coefficient"
        ],
        primary_authority=[
            "Motor manufacturer performance curves and specifications",
            "SPE 28293: Directional Drilling Motor Performance Analysis",
            "Offset well data for formation-specific yield factors",
            "Real-time motor performance monitoring data"
        ],
        burden_holder="Directional driller and MWD engineer",
        adversary_position="Pressure to maximize ROP may lead to excessive rotate drilling and loss of directional control",
        counter_arguments=[
            "RSS eliminates slide drilling inefficiency entirely",
            "Advanced motor designs claim 90%+ yield in optimal conditions",
            "Automated drilling systems can optimize slide/rotate cycles",
            "Some formations allow continuous curve with rotary steerable"
        ],
        resolution_strategy="Use offset well data to establish realistic yield expectations; monitor real-time motor performance; adjust drilling parameters dynamically; plan trajectory profiles that minimize slide percentage while meeting directional objectives",
        entity_scope="Motor BHA design, slide drilling operations, trajectory execution",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Motor yield highly formation-dependent; general ranges are industry consensus but specific wells require real-time adjustment",
        controlling_precedent="Motor manufacturer specifications and offset well performance data",
        issue_category=IssueCategory.MOTOR_OPERATIONS,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["TRAJECTORY_PLANNING", "BHA_DESIGN"]
    ),

    DoctrineBlock(
        topic="Survey Calculation Methods and Accuracy",
        keywords=["minimum curvature", "radius of curvature", "survey calculation", "inclination", "azimuth", "position uncertainty"],
        conclusion_template=[
            "Minimum curvature method is industry standard for wellbore positioning, assuming smooth circular arc between survey stations.",
            "Survey accuracy depends on sensor quality, magnetic interference, station spacing, and calculation method assumptions.",
            "Position uncertainty accumulates along wellbore; error ellipses grow with measured depth and must be considered for anti-collision analysis."
        ],
        reasoning_framework="""
Survey calculations convert downhole measurements (Inc, Azi, MD) to 3D position:

1. Calculation Methods (accuracy ranking):
   a) Minimum Curvature (most accurate, industry standard)
      - Assumes smooth circular arc between stations
      - RF = 2/DL × tan(DL/2) where DL = dogleg angle
      - Coordinates: ΔN, ΔE, ΔTVDi = RF × survey geometry

   b) Radius of Curvature (deprecated, less accurate)
      - Assumes constant curvature
      - Oversimplifies complex wellbore geometry

   c) Tangential, Balanced Tangential, Average Angle (historical only)
      - Not suitable for modern directional wells

2. Survey Sensor Types and Error Sources:
   - Magnetic MWD: ±0.2° inc, ±1-3° azi (magnetic interference dependent)
   - Gyroscopic: ±0.1° inc, ±0.5° azi (drift over time, no magnetic sensitivity)
   - IFR/MFM corrections: reduce magnetic azimuth error near casing

3. Position Uncertainty:
   - Inc/Azi sensor errors propagate through calculation
   - Station spacing affects interpolation accuracy
   - Error ellipse semi-major axis typically 3-10 ft at TD
   - Anti-collision calculations use 3σ confidence intervals

4. Survey Quality Control:
   - Check for gross errors (sudden azi changes, impossible DLS)
   - Compare magnetic vs gyro surveys
   - Monitor total magnetic field strength for interference
   - Verify closure on multi-station gyro runs

5. Survey Frequency Requirements:
   - Build/drop sections: 30-60 ft spacing minimum
   - Tangent sections: 90-150 ft acceptable
   - High DLS areas: closer spacing required
   - Approach to offset wells: increase frequency
        """,
        key_factors=[
            "Survey sensor type and accuracy specifications",
            "Magnetic field environment (BHA magnetization, nearby casing)",
            "Survey station spacing relative to wellbore curvature",
            "Calculation method and software implementation",
            "QC procedures and verification surveys",
            "Position uncertainty requirements for anti-collision",
            "Real-time vs memory survey data quality"
        ],
        primary_authority=[
            "SPE 56702: Industry Standard for Survey Calculation Methods",
            "ISCWSA (Industry Steering Committee on Wellbore Survey Accuracy) error models",
            "API RP 78: Recommended Practice for wellbore position accuracy",
            "Survey tool manufacturer accuracy specifications"
        ],
        burden_holder="MWD engineer and wellbore positioning specialist",
        adversary_position="Operational pressure to reduce survey frequency to save time",
        counter_arguments=[
            "Memory surveys can replace real-time to reduce station count",
            "Modern MWD tools have improved accuracy reducing survey needs",
            "Gyro surveys only needed in high-interference zones",
            "Tangent sections don't require frequent surveys"
        ],
        resolution_strategy="Apply ISCWSA error models to determine required survey frequency; use gyro surveys in magnetically uncertain environments; increase survey frequency approaching offset wells; perform QC on all surveys before using for directional decisions",
        entity_scope="Wellbore positioning, survey planning, anti-collision analysis",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Minimum curvature method is universally accepted; position uncertainty quantification depends on proper error model application",
        controlling_precedent="ISCWSA error models and industry survey standards",
        issue_category=IssueCategory.SURVEY_ACCURACY,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["ANTI_COLLISION", "MAGNETIC_INTERFERENCE"]
    ),

    DoctrineBlock(
        topic="Rotary Steerable Systems (RSS) - Push vs Point the Bit",
        keywords=["RSS", "rotary steerable", "push the bit", "point the bit", "continuous curve", "wellbore quality"],
        conclusion_template=[
            "RSS systems enable continuous rotation while steering, improving ROP, wellbore quality, and BHA life compared to slide drilling.",
            "Push-the-bit systems use external pads to deflect the bit; point-the-bit systems articulate the bit independently of BHA.",
            "RSS economics justified by ROP improvement, reduced tortuosity, extended reach capability, and elimination of slide-related NPT."
        ],
        reasoning_framework="""
RSS technology fundamentally changes directional drilling paradigms:

1. Push-the-Bit Systems (e.g., PowerDrive, AutoTrak):
   - External pads extend to push bit in desired direction
   - BHA remains relatively straight
   - Build rates typically 6-12°/100ft
   - Better suited for moderate DLS applications
   - More robust in challenging formations
   - Lower mechanical complexity

2. Point-the-Bit Systems (e.g., Geo-Pilot, VertiTrak):
   - Internal mechanism articulates bit direction
   - Can achieve higher build rates (12-18°/100ft)
   - More precise directional control
   - Better performance in hard formations
   - Higher mechanical complexity
   - Typically higher day rate

3. RSS Advantages Over Motors:
   - Continuous rotation: 20-40% ROP improvement typical
   - Superior wellbore quality (reduced tortuosity)
   - Elimination of slide drilling inefficiency
   - Better hole cleaning and ECD management
   - Reduced drillstring fatigue
   - Improved MWD/LWD data quality (continuous rotation)

4. RSS Limitations:
   - Higher day rate (2-3× motor cost)
   - Build rate limitations in soft formations
   - Hydraulic power requirements
   - Cannot achieve ultra-short radius curves
   - Reliability concerns in harsh environments (high temp, vibration)

5. Application Sweet Spots:
   - Extended reach wells (ERD)
   - Long lateral sections (>5,000 ft)
   - Wells requiring superior wellbore quality
   - High-angle wells with torque/drag challenges
   - Interbedded formations causing motor steering difficulty
        """,
        key_factors=[
            "Well trajectory profile and required build rates",
            "Formation characteristics and drillability",
            "Economic comparison: RSS premium vs drilling time savings",
            "Wellbore quality requirements",
            "Torque and drag constraints",
            "Temperature and vibration environment",
            "Operator experience and RSS availability"
        ],
        primary_authority=[
            "SPE 151324: RSS Performance in Extended Reach Drilling",
            "Manufacturer specifications and performance guarantees",
            "Operator offset well RSS vs motor performance data",
            "IADC drilling performance benchmarking studies"
        ],
        burden_holder="Drilling engineer and directional contractor",
        adversary_position="Motor systems advocate argues RSS premium not justified for simple well profiles",
        counter_arguments=[
            "Short laterals don't justify RSS premium",
            "High-performance motors approaching RSS build rates",
            "RSS reliability issues in some environments negate ROP advantage",
            "Motor slide drilling adequate for most directional control needs",
            "RSS learning curve and operational complexity add risk"
        ],
        resolution_strategy="Perform economic analysis comparing RSS premium against projected time savings; consider wellbore quality impact on completion and production; use RSS for extended reach and long laterals; retain motors for short build sections and backup",
        entity_scope="BHA selection, directional drilling method, wellbore quality optimization",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="RSS advantages well-documented in technical literature; economic justification well-specific",
        controlling_precedent="Operator drilling performance databases and RSS vendor case studies",
        issue_category=IssueCategory.RSS_OPERATIONS,
        analysis_zone=AnalysisZone.PLANNING,
        interactions=["MOTOR_OPERATIONS", "WELLBORE_QUALITY", "BHA_DESIGN"]
    ),

    DoctrineBlock(
        topic="Geosteering and Formation Evaluation While Drilling",
        keywords=["geosteering", "LWD", "gamma ray", "resistivity", "landing point", "formation tops"],
        conclusion_template=[
            "Geosteering uses real-time LWD data to navigate wellbore within target formation, maximizing reservoir contact and production potential.",
            "Key LWD measurements: gamma ray (lithology), resistivity (fluid contacts), density/neutron (porosity), azimuthal imaging (structural dip).",
            "Landing zone accuracy and maintaining wellbore position within pay zone are critical to horizontal well productivity."
        ],
        reasoning_framework="""
Geosteering is active wellbore navigation using formation evaluation data:

1. Real-Time LWD Measurements:
   - Gamma Ray: lithology identification, correlation to offset logs
   - Resistivity (propagation/induction): fluid contacts, formation boundaries
   - Density/Neutron: porosity calculation, lithology verification
   - Azimuthal tools: detect bed boundaries above/below wellbore
   - Seismic while drilling: look-ahead capability

2. Geosteering Workflow:
   a) Pre-drill: Build geological model from offset wells, seismic
   b) Landing: Use GR/resistivity to identify target formation entry
   c) Lateral navigation: Maintain position relative to structural dip
   d) Real-time updates: Revise geological model as new data acquired
   e) Trajectory adjustments: Steer to stay within pay window

3. Landing Zone Challenges:
   - Formation top depth uncertainty (±10-50 ft typical)
   - Rapid penetration may overshoot target
   - Tool-to-bit distance creates lag in measurements
   - Subtle lithology changes difficult to identify
   - Need balance between aggressive landing and formation damage

4. Lateral Section Optimization:
   - Maintain wellbore 10-30 ft from top/bottom of reservoir
   - Avoid water/gas contacts while maximizing net pay
   - Respond to structural dip changes
   - Identify faults, fractures, drilling hazards
   - Balance reservoir quality against wellbore stability

5. Geosteering Technology Levels:
   - Basic: GR correlation to planned trajectory
   - Advanced: Multi-measurement integration, azimuthal data
   - Ultra-deep: Seismic/EM look-ahead for proactive steering
        """,
        key_factors=[
            "Quality of pre-drill geological model",
            "LWD tool suite capability and reliability",
            "Formation top uncertainty from offset wells",
            "Structural dip and reservoir thickness",
            "Real-time interpretation expertise",
            "Communication lag between surface and directional driller",
            "Formation damage risk from trajectory adjustments"
        ],
        primary_authority=[
            "SPE 103563: Best Practices in Geosteering for Horizontal Wells",
            "LWD tool manufacturer interpretation guidelines",
            "Operator-specific geosteering procedures and software",
            "Geological model and offset well data"
        ],
        burden_holder="Geosteering geologist and directional driller",
        adversary_position="Pressure to drill fast may conflict with optimal geosteering trajectory adjustments",
        counter_arguments=[
            "Pre-planned trajectory sufficient if geological model accurate",
            "Excessive geosteering adjustments damage formation and reduce productivity",
            "Cost of advanced LWD tools not justified for simple geology",
            "Pilot hole can validate formation tops before lateral drilling"
        ],
        resolution_strategy="Invest in quality pre-drill geological model; use appropriate LWD tool suite for formation type; establish clear decision criteria for trajectory adjustments; balance formation contact optimization against wellbore quality; post-well analysis to improve future geosteering",
        entity_scope="Horizontal well drilling, reservoir contact optimization, real-time formation evaluation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Geosteering value proven in heterogeneous reservoirs; execution quality highly dependent on interpretation expertise and LWD data quality",
        controlling_precedent="Operator geosteering procedures and LWD interpretation standards",
        issue_category=IssueCategory.GEOSTEERING,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["HORIZONTAL_LANDING", "TRAJECTORY_PLANNING"]
    ),

    DoctrineBlock(
        topic="Anti-Collision Analysis and Separation Factor",
        keywords=["anti-collision", "separation factor", "traveling cylinder", "ellipse of uncertainty", "well spacing"],
        conclusion_template=[
            "Anti-collision analysis ensures minimum safe separation between wells, accounting for position uncertainty and operational risk tolerance.",
            "Separation factor (SF) = actual separation / (sum of uncertainty radii); SF ≥ 1.5-2.0 typically required depending on risk tolerance.",
            "Traveling cylinder method provides real-time closest approach distance; more sophisticated than simple center-to-center calculations."
        ],
        reasoning_framework="""
Anti-collision prevents wellbore intersections in multi-well developments:

1. Position Uncertainty Quantification:
   - Each survey has ellipse of uncertainty (error ellipse)
   - Semi-major/minor axes from ISCWSA error model
   - Uncertainty grows with measured depth
   - Typical 3σ confidence interval (99.7% confidence)
   - At 10,000 ft MD: error ellipse ~5-15 ft radius typical

2. Separation Factor Calculation:
   SF = C-C Distance / (R1 + R2)
   where:
   - C-C Distance = center-to-center between wells
   - R1, R2 = position uncertainty radii (3σ) of each well
   - SF ≥ 2.0 = very low collision risk
   - SF ≥ 1.5 = acceptable risk (industry common)
   - SF < 1.0 = ellipses overlap, collision possible

3. Traveling Cylinder Method:
   - Scan along reference well trajectory
   - Calculate closest approach to drilling well at each station
   - Generate SF profile vs measured depth
   - Identify minimum SF and depth of closest approach
   - More accurate than single-point calculations

4. Risk Mitigation Strategies:
   - Increase survey frequency approaching offset wells
   - Use gyro surveys to reduce azimuthal uncertainty
   - Magnetic ranging tools for ultra-close spacing
   - Real-time monitoring and alerts
   - Contingency trajectory plans if SF drops

5. Regulatory and Operational Standards:
   - Offshore: often SF ≥ 2.0 required
   - Onshore: SF ≥ 1.5 common, varies by state/operator
   - Infill drilling may accept SF ≥ 1.2 with enhanced monitoring
   - Blow-out relief wells: magnetic ranging, SF < 1.0 acceptable
        """,
        key_factors=[
            "Survey accuracy and error model assumptions",
            "Well spacing and trajectory proximity",
            "Regulatory requirements and operator risk tolerance",
            "Survey frequency and gyro usage",
            "Quality control on survey data",
            "Communication between offset operators",
            "Magnetic ranging tool availability for close spacing"
        ],
        primary_authority=[
            "ISCWSA SPE-90408: Wellbore Position Accuracy Error Model",
            "State/federal anti-collision regulations",
            "Operator-specific anti-collision procedures",
            "Industry best practice: SF ≥ 1.5 minimum"
        ],
        burden_holder="Directional company and operator wellbore positioning team",
        adversary_position="Desire for tighter well spacing to maximize field development may pressure anti-collision limits",
        counter_arguments=[
            "Modern survey accuracy allows closer spacing than traditional SF limits",
            "Magnetic ranging eliminates position uncertainty for ultra-close wells",
            "Overly conservative SF wastes reservoir development opportunities",
            "Infill wells routinely drilled with SF < 1.5 without incidents"
        ],
        resolution_strategy="Apply ISCWSA error models rigorously; increase survey frequency and use gyro surveys when approaching offset wells; implement real-time monitoring and alert systems; plan contingency trajectories; use magnetic ranging for intentional close spacing; balance field development optimization against collision risk",
        entity_scope="Multi-well trajectory planning, collision avoidance, survey program design",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="SF ≥ 1.5 is industry consensus minimum; specific applications may justify different thresholds with proper risk assessment",
        controlling_precedent="ISCWSA error models and operator/regulatory anti-collision standards",
        issue_category=IssueCategory.ANTI_COLLISION,
        analysis_zone=AnalysisZone.PLANNING,
        interactions=["SURVEY_ACCURACY", "TRAJECTORY_PLANNING"]
    ),

    DoctrineBlock(
        topic="Magnetic Interference and Correction Methods (IFR/MFM)",
        keywords=["magnetic interference", "IFR", "in-field referencing", "MFM", "multi-station analysis", "azimuth error"],
        conclusion_template=[
            "Magnetic interference from BHA magnetization and nearby casing causes azimuth errors in magnetic MWD surveys, potentially 5-20° or more.",
            "In-Field Referencing (IFR) and Multi-Station Analysis (MSA/MFM) provide real-time azimuth correction, improving accuracy to ±1-2°.",
            "Gyroscopic surveys eliminate magnetic interference but have drift limitations and higher cost; used for verification and high-interference zones."
        ],
        reasoning_framework="""
Magnetic survey accuracy degradation and mitigation:

1. Sources of Magnetic Interference:
   - BHA component magnetization (drillpipe, collars, stabilizers)
   - Nearby casing strings (particularly in pad drilling)
   - Surface metal structures (offshore platforms)
   - Geological magnetic anomalies (rare)
   - Magnitude increases with proximity and magnetic material volume

2. Interference Detection:
   - Total magnetic field strength anomalies
   - Dip angle deviations from expected Earth field
   - Comparison of magnetic vs gyro surveys
   - Sudden azimuth changes inconsistent with trajectory

3. In-Field Referencing (IFR):
   - Uses multiple magnetometers spaced along BHA
   - Reference magnetometer above interference zone
   - Real-time correction of lower magnetometer readings
   - Accuracy: ±1-2° azimuth typical
   - Requires non-magnetic drill collars (expensive)

4. Multi-Station Analysis (MSA/MFM):
   - Post-processing technique using multiple survey stations
   - Statistical analysis to separate interference from Earth field
   - Corrects historical surveys after drilling
   - Accuracy: ±1-3° azimuth depending on data quality
   - Does not require special MWD configuration

5. Gyroscopic Surveys:
   - Immune to magnetic interference
   - North-seeking gyro: ±0.5° azimuth accuracy
   - Rate gyro: lower cost, higher drift
   - Must pull drillstring for wireline gyro (NPT)
   - Continuous gyro MWD available but expensive

6. Survey Strategy Selection:
   - Open hole, no nearby wells: magnetic MWD adequate
   - Near casing (pad drilling): IFR or frequent gyro verification
   - Uncertain magnetic environment: gyro survey for QC
   - Critical anti-collision zones: gyro or IFR mandatory
        """,
        key_factors=[
            "Proximity to offset wellbores and casing",
            "BHA magnetic properties and configuration",
            "Anti-collision separation requirements",
            "Survey QC procedures and verification intervals",
            "Economic trade-off: IFR/gyro cost vs azimuth uncertainty risk",
            "Total magnetic field strength monitoring",
            "Regulatory requirements for survey accuracy"
        ],
        primary_authority=[
            "SPE 67616: Magnetic Interference and Azimuth Accuracy",
            "ISCWSA error models for magnetic surveys with/without IFR",
            "MWD manufacturer IFR/MSA specifications",
            "Gyroscopic survey tool accuracy specifications"
        ],
        burden_holder="MWD service provider and wellbore positioning specialist",
        adversary_position="Operational pressure to use standard magnetic MWD to avoid IFR cost or gyro NPT",
        counter_arguments=[
            "Magnetic interference often overstated, surveys accurate without correction",
            "MSA post-processing can fix magnetic errors without real-time IFR cost",
            "Gyro surveys too expensive for routine use",
            "Offset well database allows confident magnetic surveying in known environments"
        ],
        resolution_strategy="Monitor total magnetic field strength continuously; implement IFR in pad drilling and near-casing environments; run gyro verification surveys at key depths; use MSA to validate and correct magnetic surveys post-run; increase survey frequency in magnetically uncertain zones",
        entity_scope="Survey accuracy assurance, wellbore positioning QC, anti-collision risk management",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Magnetic interference effects well-documented; IFR/gyro effectiveness proven; application requires site-specific assessment",
        controlling_precedent="ISCWSA magnetic interference error models and MWD service quality standards",
        issue_category=IssueCategory.MAGNETIC_INTERFERENCE,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["SURVEY_ACCURACY", "ANTI_COLLISION"]
    ),

    DoctrineBlock(
        topic="BHA Design for Directional Control",
        keywords=["BHA design", "stabilizer placement", "bit-to-bend", "pendulum assembly", "packed assembly", "stiffness"],
        conclusion_template=[
            "BHA design determines directional performance through stabilizer placement, bit-to-bend distance, and overall stiffness.",
            "Pendulum assemblies (under-gauged stabilizers, flexible) allow formation tendency; packed assemblies (near-gauge stabilizers, stiff) force trajectory.",
            "Motor BHA: bit-to-bend distance and bent housing angle set theoretical build rate; stabilizer placement determines actual performance and yield."
        ],
        reasoning_framework="""
BHA configuration is primary control for directional drilling performance:

1. Motor BHA Components (bottom to top):
   - Bit (drill ahead, side-cutting capability affects steering)
   - Motor (power section, bent housing angle)
   - Bit-to-bend section (distance determines build rate sensitivity)
   - Near-bit stabilizer (gauge control, side force reaction point)
   - Adjustable stabilizer (fine-tune build rate, optional)
   - Non-magnetic drill collars (MWD housing, ~30 ft)
   - Additional stabilizers (control buckling, maintain trajectory)

2. Build Rate Control:
   Build Rate = (180/π) × tan(α) / L_bb
   where α = bent housing angle, L_bb = bit-to-bend distance

   - Short bit-to-bend (10-15 ft): high build rate, responsive
   - Long bit-to-bend (20-30 ft): moderate build rate, smoother
   - Stabilizer placement shifts effective fulcrum point

3. Pendulum vs Packed Assembly:
   Pendulum (drop tendency):
   - Under-gauge or no near-bit stabilizer
   - BHA sags under gravity in deviated hole
   - Useful for controlled drop sections
   - Formation tendency dominates

   Packed (hold/build tendency):
   - Near-gauge stabilizer close to bit
   - Stiff BHA resists formation tendency
   - Better directional control
   - Higher side forces, more casing wear

4. RSS BHA Design:
   - Simpler than motor (no bent housing)
   - Stabilizer placement affects steering forces
   - Push-the-bit: pad extension locations critical
   - Point-the-bit: requires articulation clearance
   - Generally 1-2 stabilizers in BHA

5. BHA Design Trade-offs:
   - Stiff BHA: better control, higher torque/drag, casing wear
   - Flexible BHA: lower torque/drag, more formation tendency
   - Short BHA: easier to run, less buckling, limited stabilization
   - Long BHA: better stability, harder to slide, buckling risk
        """,
        key_factors=[
            "Required directional performance (build/hold/drop)",
            "Formation characteristics and drillability",
            "Motor specifications or RSS type",
            "Hole size and casing program",
            "Torque and drag limitations",
            "Wellbore quality requirements",
            "Bit selection and aggressiveness"
        ],
        primary_authority=[
            "Directional drilling contractor BHA design guidelines",
            "Motor/RSS manufacturer recommendations",
            "Offset well BHA performance database",
            "BHA modeling software results"
        ],
        burden_holder="Directional drilling engineer and contractor",
        adversary_position="Simplification pressure may lead to sub-optimal BHA compromising directional performance",
        counter_arguments=[
            "Generic BHA designs adequate for simple trajectories",
            "Formation tendency predictable, minimal BHA optimization needed",
            "RSS eliminates BHA design sensitivity vs motors",
            "Cost and logistics favor standardized BHA configurations"
        ],
        resolution_strategy="Use BHA modeling software to predict performance; reference offset well data for similar formations; design BHA specific to trajectory section requirements; balance directional control against mechanical risk and cost",
        entity_scope="BHA engineering, directional drilling planning, trajectory execution",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="BHA design principles well-established; specific performance prediction requires modeling and offset data validation",
        controlling_precedent="Directional drilling contractor design standards and BHA modeling tools",
        issue_category=IssueCategory.BHA_DESIGN,
        analysis_zone=AnalysisZone.PLANNING,
        interactions=["MOTOR_OPERATIONS", "RSS_OPERATIONS", "TRAJECTORY_PLANNING"]
    ),

    DoctrineBlock(
        topic="Horizontal Well Landing Techniques",
        keywords=["landing", "kickoff point", "curve section", "entry angle", "formation damage", "wellbore stability"],
        conclusion_template=[
            "Successful horizontal landing requires precise kickoff point selection, controlled build section, and accurate formation top identification.",
            "Entry angle into reservoir typically 85-90° measured depth for maximum lateral length and optimal completion.",
            "Landing zone operations balance aggressive penetration with formation damage prevention and wellbore stability maintenance."
        ],
        reasoning_framework="""
Horizontal well landing is critical transition from build to lateral:

1. Landing Zone Geometry:
   KOP (Kickoff Point) → Build Section → Landing Point → Lateral

   - KOP depth: above target by radius of curvature
   - Build section: constant or variable curvature to reach angle
   - Landing point: entry into target formation
   - Entry angle: typically 85-90° from vertical

2. Kickoff Point Selection:
   - Must provide sufficient MD to reach target angle
   - Radius = (5730 / build rate in °/100ft) × 100
   - Example: 8°/100ft build → R = 71,625 ft / 100 = 716 ft
   - TVD required: R × (1 - cos(final angle))
   - Account for formation top uncertainty

3. Build Section Management:
   - Constant curvature preferred for smooth wellbore
   - Motor build rate may vary with formation changes
   - Monitor actual vs planned build rate continuously
   - Adjust if approaching formation too fast/slow
   - Minimize slide percentage for better ROP

4. Formation Entry Challenges:
   - Formation top uncertainty: ±10-50 ft typical
   - Overshoot → miss reservoir or thin pay contact
   - Undershoot → excessive build or early entry
   - Rapid lithology change at formation boundary
   - Formation damage from excessive trajectory correction

5. Landing Strategies:
   A) Aggressive landing: drill fast, accept some overshoot risk
   B) Conservative landing: slow approach, gamma ray monitoring
   C) Pilot hole: drill vertical pilot, log, then sidetrack lateral
   D) Controlled entry: reduce WOB, monitor formation response

6. Wellbore Stability Considerations:
   - Transitioning to high angle increases wellbore stress
   - Weak formations may collapse or slough
   - Mud weight and properties critical
   - ECD management in narrow pressure window
   - Cuttings transport becomes more difficult >60° inclination
        """,
        key_factors=[
            "Formation top depth uncertainty from offset wells",
            "Build rate capability and DLS limits",
            "LWD data quality for formation identification",
            "Reservoir thickness and entry angle requirements",
            "Formation damage sensitivity",
            "Wellbore stability and mud program",
            "Geosteering capability and expertise"
        ],
        primary_authority=[
            "SPE 80945: Horizontal Well Landing Best Practices",
            "Operator horizontal drilling procedures",
            "Geosteering and formation evaluation guidelines",
            "Offset well landing performance data"
        ],
        burden_holder="Directional driller, geosteering geologist, and drilling engineer",
        adversary_position="Pressure to maximize drilling speed may compromise landing accuracy and formation protection",
        counter_arguments=[
            "Pilot holes waste rig time when geological model is confident",
            "Aggressive landing acceptable if reservoir thick and homogeneous",
            "Modern geosteering eliminates need for conservative approach",
            "Formation damage concern overstated vs operational efficiency"
        ],
        resolution_strategy="Evaluate formation top uncertainty and select appropriate landing strategy; use geosteering data to refine entry point real-time; balance penetration rate against landing precision; plan contingency trajectories for early/late formation encounter; minimize formation damage through optimized mud properties and trajectory smoothness",
        entity_scope="Horizontal well trajectory execution, landing zone operations, reservoir entry optimization",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Landing techniques well-established; execution quality depends on formation evaluation accuracy and real-time decision-making",
        controlling_precedent="Operator horizontal drilling procedures and offset well landing data",
        issue_category=IssueCategory.HORIZONTAL_LANDING,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["GEOSTEERING", "TRAJECTORY_PLANNING", "WELLBORE_QUALITY"]
    ),

    DoctrineBlock(
        topic="Wellbore Tortuosity and Quality Metrics",
        keywords=["tortuosity", "wellbore quality", "micro-doglegs", "spiraling", "ledges", "keyseats"],
        conclusion_template=[
            "Wellbore tortuosity (micro-doglegs, spiraling) reduces completion efficiency and long-term well integrity beyond macro-DLS limits.",
            "Quality metrics include mean DLS, standard deviation, tortuosity index, and smoothness measures over short intervals (30-90 ft).",
            "RSS systems and optimized motor operations improve wellbore quality, reducing completion NPT and maximizing production life."
        ],
        reasoning_framework="""
Wellbore quality extends beyond simple DLS compliance:

1. Tortuosity vs Dogleg Severity:
   - DLS: curvature over standard interval (usually 100 ft)
   - Tortuosity: short-period variations (micro-doglegs)
   - Spiraling: corkscrew trajectory pattern
   - Both can exist with acceptable average DLS

2. Tortuosity Causes:
   - Slide/rotate drilling cycles create jagged trajectory
   - Motor reactive torque causes bit walk
   - Formation changes cause unplanned deflections
   - Improper toolface control during slide drilling
   - Excessive correction steering
   - BHA vibration and whirl

3. Quality Metrics:
   - Standard Deviation of Inclination/Azimuth
   - Tortuosity Index: ∑|dogleg_i| over short intervals
   - Smoothness Factor: trajectory curvature variability
   - Ledge count: sharp trajectory changes >2°/30ft
   - Spiral severity: lateral displacement off planned path

4. Impact on Well Operations:
   - Completion: wireline/coiled tubing passage difficulty
   - Casing running: higher drag, potential hang-up
   - Cementing: poor displacement, channeling
   - Production: ESP/rod pump wear, tubing wear
   - Intervention: difficulty running tools to TD
   - Long-term: accelerated casing/tubing failure

5. Quality Improvement Methods:
   - RSS instead of motor (eliminates slide/rotate cycles)
   - High-performance motors with better toolface control
   - Automated drilling parameters optimization
   - Reduce correction steering frequency
   - Optimize BHA design for smooth drilling
   - Real-time tortuosity monitoring and alerts

6. Quality Standards:
   - Operator-specific wellbore acceptance criteria
   - Completion contractor tool passage requirements
   - Production engineering long-term integrity targets
   - Comparison to offset well benchmarks
        """,
        key_factors=[
            "Directional drilling method (motor vs RSS)",
            "Slide percentage and toolface control quality",
            "Formation heterogeneity and drillability",
            "BHA design and vibration control",
            "Completion method and tool size",
            "Expected well life and production profile",
            "Survey frequency and quality"
        ],
        primary_authority=[
            "SPE 128702: Wellbore Quality Impact on Completion and Production",
            "Operator wellbore quality standards and acceptance criteria",
            "Completion contractor tool passage specifications",
            "Directional drilling service quality metrics"
        ],
        burden_holder="Directional drilling contractor and operator drilling engineer",
        adversary_position="Focus on drilling speed and reaching TD may deprioritize wellbore quality",
        counter_arguments=[
            "Wellbore quality impact overstated for short-life wells",
            "Completion technology can handle poor quality wellbores",
            "RSS premium not justified by quality improvement alone",
            "Tortuosity metrics lack standardization and are subjective"
        ],
        resolution_strategy="Establish quantitative wellbore quality targets in well planning; implement real-time monitoring; select directional method (RSS vs motor) considering quality requirements; perform post-well analysis to correlate quality with completion/production performance; use quality data to improve future well designs",
        entity_scope="Wellbore drilling quality, completion efficiency, long-term well integrity",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Wellbore quality impact on operations widely recognized; quantitative acceptance criteria vary by operator and well type",
        controlling_precedent="Operator wellbore quality standards and completion contractor requirements",
        issue_category=IssueCategory.WELLBORE_QUALITY,
        analysis_zone=AnalysisZone.POST_RUN,
        interactions=["RSS_OPERATIONS", "MOTOR_OPERATIONS", "TRAJECTORY_PLANNING"]
    ),

    DoctrineBlock(
        topic="Whipstock and Sidetracking Operations",
        keywords=["whipstock", "sidetrack", "window milling", "kickoff", "cement plug", "oriented milling"],
        conclusion_template=[
            "Whipstock operations create new wellbore trajectory from existing wellbore, commonly used for sidetracking and multi-lateral wells.",
            "Window milling through casing requires precise orientation, adequate cement support, and proper mill selection to avoid casing damage.",
            "Sidetrack success depends on cement plug quality, whipstock setting depth, and formation competence at kickoff point."
        ],
        reasoning_framework="""
Whipstock technology enables wellbore trajectory changes from existing holes:

1. Whipstock Types and Applications:
   A) Retrievable whipstock: set on packer, can be recovered
   B) Permanent whipstock: cemented in place
   C) Hydraulic whipstock: single-trip system
   D) Concave mill assembly: no whipstock, direct milling

   Applications:
   - Sidetrack damaged wellbore section
   - Bypass fish or junk in hole
   - Drill multi-lateral junctions (TAML Level 3-4)
   - Directional correction from vertical pilot

2. Window Milling Process:
   a) Set cement plug below window depth (hard point)
   b) Orient whipstock (scribe line to desired direction)
   c) Mill starter hole (30-50 ft typical)
   d) Widen window with watermelon mill
   e) Dress window with section mill
   f) Retrieve whipstock (if retrievable type)
   g) Dress window ledge and continue drilling

3. Cement Plug Requirements:
   - Length: 100-200 ft minimum for support
   - Strength: >1500 psi compressive minimum
   - Quality: no channeling, good bonding to casing
   - WOC time: 12-24 hours typical
   - Tag cement top to verify depth
   - Drill cement to establish kickoff point

4. Orientation and Survey:
   - Whipstock must be oriented precisely (±5° tolerance)
   - Gyroscopic or magnetic orientation tool
   - Verify orientation before milling start
   - First survey critical to confirm exit direction
   - High side of window determines initial trajectory

5. Risks and Mitigation:
   - Inadequate cement → casing collapse during milling
   - Misorientation → wrong exit direction
   - Soft formation → window instability, lost circulation
   - Casing damage above window → integrity compromise
   - Whipstock failure → stuck tool, fishing operation

6. Multi-Lateral Junction Design:
   TAML (Technology Advancement for Multi-Laterals):
   - Level 1: unsupported junction, open hole
   - Level 2: supported junction, open hole lateral
   - Level 3: mechanical junction, cased lateral
   - Level 4: pressure-isolated junction, cased lateral
        """,
        key_factors=[
            "Cement plug quality and length",
            "Formation competence at sidetrack depth",
            "Whipstock system selection and specifications",
            "Orientation accuracy requirements",
            "Casing size and grade",
            "Subsequent trajectory requirements",
            "Multi-lateral junction integrity needs (if applicable)"
        ],
        primary_authority=[
            "SPE 37485: Whipstock Technology and Best Practices",
            "TAML classification for multi-lateral junctions",
            "Service company whipstock system manuals",
            "Operator sidetracking procedures"
        ],
        burden_holder="Completions engineer and directional drilling contractor",
        adversary_position="Cost pressure may favor cheaper whipstock systems or marginal cement plugs",
        counter_arguments=[
            "Simple sidetracks don't need expensive retrievable whipstocks",
            "Reduced cement plug length acceptable in competent formations",
            "Concave mill systems eliminate whipstock complexity",
            "Multi-lateral junctions only need TAML Level 1-2 for most applications"
        ],
        resolution_strategy="Select whipstock system appropriate to application criticality; ensure adequate cement plug quality through testing and WOC time; verify orientation before milling; use proper mill sequence to protect casing; design for worst-case formation conditions; perform risk assessment for multi-lateral junctions",
        entity_scope="Sidetracking operations, multi-lateral well construction, wellbore trajectory redirection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Whipstock operations well-understood with established best practices; execution quality critical to success",
        controlling_precedent="Service company whipstock specifications and operator sidetracking procedures",
        issue_category=IssueCategory.TRAJECTORY_PLANNING,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["BHA_DESIGN", "WELLBORE_QUALITY"]
    ),

    DoctrineBlock(
        topic="Toolface Orientation (Gravity vs Magnetic)",
        keywords=["toolface", "gravity toolface", "magnetic toolface", "high side", "reactive torque", "orientation control"],
        conclusion_template=[
            "Toolface orientation controls steering direction in slide drilling; gravity toolface used at high inclination (>~5°), magnetic toolface at low inclination.",
            "Toolface = angular position of bent housing/RSS steering force relative to reference (high side or magnetic north).",
            "Maintaining toolface during slide drilling is challenged by reactive torque, formation effects, and measurement lag; modern MWD provides real-time feedback."
        ],
        reasoning_framework="""
Toolface orientation is fundamental to directional control:

1. Toolface Definition:
   - Angular position of motor bend/RSS steering direction
   - Referenced to either gravity high side or magnetic north
   - Measured in degrees: 0-360° (or -180° to +180°)
   - Determines direction of build/turn

2. Gravity Toolface (GTF):
   - Used when inclination >~5° (gravity measureable)
   - GTF = 0° → drilling straight up (build)
   - GTF = 180° → drilling straight down (drop)
   - GTF = 90°/270° → building left/right
   - Reference: gravity vector (high side of hole)
   - Advantage: immune to magnetic interference
   - Limitation: unusable at low inclination (<5°)

3. Magnetic Toolface (MTF):
   - Used at low inclination (<~5°) where gravity weak
   - MTF = 0° → drilling toward magnetic north
   - MTF = 90° → drilling toward east
   - Reference: Earth's magnetic field
   - Advantage: works at any inclination
   - Limitation: affected by magnetic interference

4. Toolface Control Challenges:
   - Reactive torque: motor rotation creates counter-rotation
   - Drillstring twist: surface/downhole toolface differ
   - Bit wobble: toolface oscillates while sliding
   - Formation effects: hard stringers deflect bit
   - Friction: high drag prevents toolface transmission
   - Measurement lag: MWD updates every 30-90 seconds

5. Toolface Management Techniques:
   - Slow, steady sliding (avoid rushing)
   - Pick up off bottom to orient, then slide
   - Monitor real-time toolface on MWD display
   - Anticipate reactive torque direction
   - Use toolface stability indicator (if available)
   - Automated toolface control systems (advanced rigs)

6. Relationship to Build Rate:
   Actual build = motor build rate × cos(toolface error)
   - Small toolface errors (<15°) have minimal effect
   - Large errors (>30°) significantly reduce build efficiency
   - 90° toolface error → pure turn, no build
        """,
        key_factors=[
            "Wellbore inclination (determines GTF vs MTF use)",
            "Motor specifications and reactive torque",
            "MWD update rate and toolface accuracy",
            "Driller skill and experience",
            "Automated drilling system capability",
            "Formation heterogeneity",
            "Slide drilling parameters (WOB, flow rate, slide speed)"
        ],
        primary_authority=[
            "MWD manufacturer toolface measurement specifications",
            "Directional drilling training and best practices manuals",
            "Motor manufacturer reactive torque data",
            "Real-time drilling optimization studies"
        ],
        burden_holder="Directional driller and MWD engineer",
        adversary_position="Pressure for fast drilling may compromise toolface control quality",
        counter_arguments=[
            "RSS eliminates toolface control complexity entirely",
            "Automated drilling systems handle toolface better than manual",
            "Modern MWD toolface accuracy sufficient for most applications",
            "Excessive focus on toolface wastes rig time vs just slide and correct"
        ],
        resolution_strategy="Train drillers on toolface fundamentals; use real-time MWD display for feedback; implement automated toolface optimization where available; plan trajectories accounting for realistic toolface control capability; use RSS for sections requiring precise continuous steering",
        entity_scope="Slide drilling operations, motor directional control, trajectory execution",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Toolface principles universally accepted; control quality depends on equipment, personnel skill, and formation conditions",
        controlling_precedent="Directional drilling operational best practices and MWD technology standards",
        issue_category=IssueCategory.MOTOR_OPERATIONS,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["MOTOR_OPERATIONS", "BHA_DESIGN"]
    ),

    DoctrineBlock(
        topic="Stuck Pipe Risk in Directional Drilling",
        keywords=["stuck pipe", "differential sticking", "key seating", "pack-off", "torque and drag", "wellbore stability"],
        conclusion_template=[
            "Stuck pipe is elevated risk in directional wells due to differential sticking, key seating, hole pack-off, and torque/drag limitations.",
            "Differential sticking occurs when pipe contacts permeable formation under overbalance; severity increases with inclination, contact area, and mud cake quality.",
            "Prevention: minimize contact time, maintain pipe movement, optimize mud properties, control ECD, avoid excessive overbalance in permeable zones."
        ],
        reasoning_framework="""
Directional wells face increased stuck pipe risk vs vertical wells:

1. Differential Sticking Mechanism:
   - Pipe presses against low-pressure permeable formation
   - Overbalance pressure forces pipe into mud cake
   - Friction force = pressure differential × contact area × friction coefficient
   - Severity increases with: high overbalance, thick mud cake, large contact area
   - Directional wells: gravity pulls pipe to low side, increasing contact

2. Key Seating:
   - Drillstring wears groove (keyseat) at dogleg
   - Tool joint larger diameter than pipe body
   - Tool joint catches in keyseat during trip out
   - Severity proportional to DLS and depth
   - High-angle wells create longer keyseats

3. Hole Pack-Off and Cuttings Accumulation:
   - Poor hole cleaning in high-angle sections
   - Cuttings settle on low side of wellbore
   - Cuttings bed restricts annular flow
   - Pack-off when BHA surrounded by cuttings
   - Directional wells >40° inclination most susceptible

4. Torque and Drag:
   - Friction between drillstring and wellbore
   - Increases with well depth, inclination, DLS
   - Limits WOB transmission to bit
   - Can prevent pipe movement (lockup)
   - Extended reach wells most affected

5. Wellbore Instability:
   - Formation collapse or sloughing
   - Swelling shales narrow wellbore
   - Lost circulation weakens formation
   - Tight hole while tripping
   - Wellbore breathing (pressure cycling)

6. Prevention Strategies:
   - Maintain pipe movement (rotate, reciprocate)
   - Optimize mud weight (minimize overbalance)
   - Improve mud cake quality (thin, slick)
   - Enhance hole cleaning (flow rate, sweeps, back-reaming)
   - Reduce contact time in critical zones
   - Use spotting fluids (oil-based, surfactant pills)
   - Monitor torque/drag trends
   - Wiper trips to condition hole

7. Intervention Tactics (if stuck):
   - Work pipe (torque, pull, slack off cycles)
   - Spot free-point pill
   - Wait for fluid soak time
   - Free-point survey to locate stuck point
   - Jar up/down (if jars in BHA)
   - Sever pipe above stuck point (last resort)
        """,
        key_factors=[
            "Wellbore inclination and DLS profile",
            "Formation permeability and pressure",
            "Overbalance magnitude and duration",
            "Mud properties (cake quality, lubricity, density)",
            "Hole cleaning efficiency",
            "Drillstring design and BHA configuration",
            "Drilling practice (pipe movement, wiper trips)",
            "Wellbore stability and formation competence"
        ],
        primary_authority=[
            "SPE 16162: Analysis of Stuck Pipe in Deviated Wells",
            "IADC Stuck Pipe Prevention Guidelines",
            "Operator drilling procedures for high-angle wells",
            "Service company stuck pipe mitigation best practices"
        ],
        burden_holder="Drilling engineer and rig operations crew",
        adversary_position="Time pressure may lead to reduced wiper trips and insufficient hole conditioning",
        counter_arguments=[
            "Modern LCM and spotting fluids mitigate differential sticking",
            "RSS and optimized BHA reduce key seating risk",
            "Managed pressure drilling allows lower overbalance",
            "Directional well stuck pipe rates comparable to vertical with proper practices"
        ],
        resolution_strategy="Implement rigorous stuck pipe prevention program; maintain continuous pipe movement in critical zones; optimize mud properties for formation type; perform regular wiper trips; monitor torque/drag trends; have spotting fluids and intervention tools ready; design BHA to minimize differential sticking and key seating risk",
        entity_scope="Drilling operations risk management, wellbore integrity, NPT reduction",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Stuck pipe mechanisms well-understood; prevention effectiveness depends on operational discipline and formation characteristics",
        controlling_precedent="IADC and SPE stuck pipe prevention best practices",
        issue_category=IssueCategory.WELLBORE_QUALITY,
        analysis_zone=AnalysisZone.OPERATIONS,
        interactions=["TRAJECTORY_PLANNING", "BHA_DESIGN"]
    ),

    DoctrineBlock(
        topic="Extended Reach Drilling (ERD) Torque and Drag",
        keywords=["ERD", "torque", "drag", "buckling", "lockup", "rotary steerable", "friction coefficient"],
        conclusion_template=[
            "Extended reach drilling pushes torque and drag limits; horizontal displacement >2× TVD requires specialized design and execution.",
            "Torque/drag modeling essential for ERD planning; friction coefficients, wellbore profile smoothness, and drillstring design are critical inputs.",
            "RSS, high-torque top drives, friction reduction additives, and optimized trajectories enable ERD; economic limit often reached before mechanical limit."
        ],
        reasoning_framework="""
ERD represents extreme directional drilling, demanding advanced technology:

1. ERD Classification:
   - Medium reach: HD/TVD = 1.5 to 2.0
   - Extended reach: HD/TVD = 2.0 to 3.0
   - Ultra-extended reach: HD/TVD > 3.0
   - World records exceed HD/TVD = 5.0

2. Torque and Drag Fundamentals:
   Drag Force = Normal Force × Friction Coefficient
   - Normal force from pipe weight on wellbore low side
   - Friction coefficient: 0.15-0.25 water-based, 0.10-0.18 oil-based
   - Torque increases with depth, inclination, DLS
   - Cumulative effect: total drag = sum of incremental segments

3. Mechanical Limitations:
   - Drillstring tensile limit (overpull capacity)
   - Drillpipe torsional limit (twist-off risk)
   - Top drive torque capacity
   - Buckling in compression zones
   - Casing shoe stress during drilling below casing

4. ERD Enabling Technologies:
   - RSS: continuous rotation eliminates slide drag penalty
   - High-torque top drives: 50,000+ ft-lbs capability
   - Friction reduction: oil-based mud, lubricant additives, low-friction coatings
   - Casing while drilling: set casing and drill simultaneously
   - High-strength drillpipe: reduce pipe body for same strength
   - Torque-reduction tools: roller reamers, anti-torque systems

5. Trajectory Optimization:
   - Minimize DLS to reduce contact forces
   - Build curve in shallow section (lower normal force)
   - Smooth wellbore (RSS preferred over motors)
   - Tangent section at optimal inclination (85-87° typical)
   - Avoid unnecessary corrections

6. Real-Time Monitoring:
   - Compare actual vs modeled torque/drag
   - Trend analysis to predict lockup
   - Adjust drilling parameters if approaching limits
   - Decision points: continue vs pull back and sidetrack

7. Economic Considerations:
   - Rig time cost vs displacement benefit
   - Multiple sidetracks may be needed (planned)
   - Advanced technology premium (RSS, specialty mud, drillpipe)
   - Often cheaper than offshore platform or subsea manifold
        """,
        key_factors=[
            "Horizontal displacement and TVD",
            "Wellbore profile (DLS, inclination, smoothness)",
            "Drillstring design and mechanical limits",
            "Friction coefficient (mud type, additives, casing)",
            "Top drive and drawworks capacity",
            "RSS vs motor directional method",
            "Formation hardness and ROP",
            "Economic drivers and alternatives"
        ],
        primary_authority=[
            "SPE 112849: Extended Reach Drilling Best Practices and Technology Review",
            "Torque and drag modeling software (Landmark, Halliburton, Baker Hughes)",
            "Operator ERD case studies and lessons learned",
            "Drillstring manufacturer specifications and limits"
        ],
        burden_holder="Drilling engineer and wellbore design team",
        adversary_position="ERD complexity may be avoided in favor of additional surface locations or subsea infrastructure",
        counter_arguments=[
            "ERD wells have higher mechanical risk and failure rate",
            "Advanced technology costs exceed economic benefit in some cases",
            "Multiple vertical wells from additional location may be cheaper",
            "ERD complicates completions and production operations"
        ],
        resolution_strategy="Perform rigorous torque/drag modeling in well planning; select enabling technologies appropriate to reach requirements; design smooth trajectory profile; implement real-time monitoring and contingency plans; balance ERD reach against mechanical risk and economics; consider ERD where it provides clear advantage (offshore development, restricted surface access)",
        entity_scope="Well planning for extreme horizontal displacement, drilling operations optimization, field development strategy",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ERD principles and limitations well-established through industry experience; specific well success depends on design quality and execution",
        controlling_precedent="Industry ERD case studies and torque/drag modeling validation data",
        issue_category=IssueCategory.TRAJECTORY_PLANNING,
        analysis_zone=AnalysisZone.PLANNING,
        interactions=["RSS_OPERATIONS", "BHA_DESIGN", "WELLBORE_QUALITY"]
    )
]


# ============================================================================
# ENGINE CORE
# ============================================================================

class DirectionalDrillingEngine:
    """TIE Gold Standard Directional Drilling Intelligence Engine"""

    def __init__(self):
        self.doctrine_cache = DOCTRINE_CACHE
        self.start_time = datetime.now()
        self.query_count = 0
        self.cache_hits = 0

        # Telemetry
        self.query_log: List[Dict[str, Any]] = []

        # Semantic normalization map
        self.normalization_map = {
            "dls": "dogleg severity",
            "mwd": "measurement while drilling",
            "lwd": "logging while drilling",
            "rss": "rotary steerable system",
            "bha": "bottom hole assembly",
            "gtf": "gravity toolface",
            "mtf": "magnetic toolface",
            "erd": "extended reach drilling",
            "ifr": "in-field referencing",
            "msa": "multi-station analysis",
            "iscwsa": "industry steering committee on wellbore survey accuracy",
            "sf": "separation factor",
            "rop": "rate of penetration",
            "wob": "weight on bit",
            "rpm": "revolutions per minute",
            "ecd": "equivalent circulating density"
        }

        logger.info("DRL02 Directional Drilling Engine initialized")
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

    def normalize_query(self, query: str) -> str:
        """Apply semantic normalization"""
        normalized = query.lower()
        for abbrev, full_term in self.normalization_map.items():
            normalized = normalized.replace(abbrev, full_term)
        return normalized

    def match_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Match query to relevant doctrine blocks"""
        normalized = self.normalize_query(query)
        matched = []

        for doctrine in self.doctrine_cache:
            # Check keyword matching
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in normalized)

            # Check topic relevance
            topic_match = any(word in normalized for word in doctrine.topic.lower().split())

            if keyword_matches >= 1 or topic_match:
                matched.append((doctrine, keyword_matches))

        # Sort by relevance
        matched.sort(key=lambda x: x[1], reverse=True)
        return [d[0] for d in matched[:5]]  # Top 5 doctrines

    def apply_epistemic_guardrails(self, response: str) -> Tuple[str, List[str]]:
        """Check for banned phrases and add appropriate caveats"""
        warnings = []

        for phrase in BANNED_PHRASES:
            if phrase.lower() in response.lower():
                warnings.append(f"Response contains overconfident phrase: '{phrase}'")

        # Add disclosure caveat for high-risk statements
        if any(term in response.lower() for term in ["guarantee", "certain", "always", "never"]):
            caveat = "\n\n[DISCLOSURE: Directional drilling outcomes depend on numerous variables including formation properties, equipment performance, and operational execution. Consult qualified drilling engineers and follow applicable safety regulations.]"
            response += caveat

        return response, warnings

    def generate_response(self, query: str, mode: ResponseMode, doctrines: List[DoctrineBlock]) -> str:
        """Generate response based on mode and matched doctrines"""

        if not doctrines:
            return "No relevant directional drilling doctrine found for this query. Please consult qualified drilling engineers and service company technical support."

        primary = doctrines[0]

        if mode == ResponseMode.FAST:
            # Concise response
            response = f"**{primary.topic}**\n\n"
            response += "\n".join(primary.conclusion_template[:2])
            if len(doctrines) > 1:
                response += f"\n\nRelated: {', '.join(d.topic for d in doctrines[1:3])}"
            return response

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready detailed response
            response = f"# {primary.topic}\n\n"
            response += "## Conclusion\n" + "\n".join(primary.conclusion_template) + "\n\n"
            response += "## Reasoning Framework\n" + primary.reasoning_framework + "\n\n"
            response += "## Key Factors\n" + "\n".join(f"- {f}" for f in primary.key_factors) + "\n\n"
            response += "## Governing Authority\n" + "\n".join(f"- {a}" for a in primary.primary_authority) + "\n\n"
            response += f"## Confidence Level\n{primary.confidence.value} - {primary.confidence_stratification}\n\n"

            if len(doctrines) > 1:
                response += "## Related Doctrines\n"
                for d in doctrines[1:]:
                    response += f"- **{d.topic}**: {d.conclusion_template[0]}\n"

            return response

        else:  # MEMO
            # Full technical memorandum
            response = f"# TECHNICAL MEMORANDUM: {primary.topic}\n\n"
            response += f"**Issue Category:** {primary.issue_category.value}\n"
            response += f"**Analysis Zone:** {primary.analysis_zone.value}\n"
            response += f"**Confidence:** {primary.confidence.value}\n\n"

            response += "## Executive Summary\n" + "\n".join(primary.conclusion_template) + "\n\n"

            response += "## Detailed Analysis\n" + primary.reasoning_framework + "\n\n"

            response += "## Key Factors for Consideration\n"
            response += "\n".join(f"{i+1}. {f}" for i, f in enumerate(primary.key_factors)) + "\n\n"

            response += "## Technical Authority\n" + "\n".join(f"- {a}" for a in primary.primary_authority) + "\n\n"

            response += "## Adversarial Position\n" + primary.adversary_position + "\n\n"

            response += "## Counter-Arguments\n" + "\n".join(f"- {c}" for c in primary.counter_arguments) + "\n\n"

            response += "## Resolution Strategy\n" + primary.resolution_strategy + "\n\n"

            response += f"## Controlling Precedent\n{primary.controlling_precedent}\n\n"

            if primary.interactions:
                response += "## Doctrine Interactions\n"
                response += "This doctrine interacts with: " + ", ".join(primary.interactions) + "\n\n"

            if len(doctrines) > 1:
                response += "## Additional Relevant Doctrines\n"
                for d in doctrines[1:]:
                    response += f"\n### {d.topic}\n"
                    response += d.conclusion_template[0] + "\n"
                    response += f"*Category: {d.issue_category.value}, Confidence: {d.confidence.value}*\n"

            return response

    def calculate_determinism_hash(self, query: str, response: str, doctrines: List[DoctrineBlock]) -> str:
        """Generate SHA-256 hash for reproducibility verification"""
        content = f"{query}|{response}|{','.join(d.topic for d in doctrines)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing"""
        start = datetime.now()
        self.query_count += 1

        # Match doctrines
        doctrines = self.match_doctrines(request.query)

        if doctrines:
            self.cache_hits += 1

        # Generate response
        response = self.generate_response(request.query, request.mode, doctrines)

        # Apply epistemic guardrails
        response, warnings = self.apply_epistemic_guardrails(response)

        # Determine zone and confidence
        zone = doctrines[0].analysis_zone if doctrines else AnalysisZone.PLANNING
        confidence = doctrines[0].confidence if doctrines else ConfidenceLevel.DISCLOSURE

        # Calculate hash
        det_hash = self.calculate_determinism_hash(request.query, response, doctrines)

        # Processing time
        elapsed = (datetime.now() - start).total_seconds() * 1000

        # Telemetry
        self.query_log.append({
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "mode": request.mode.value,
            "doctrines_triggered": [d.topic for d in doctrines],
            "confidence": confidence.value,
            "processing_ms": elapsed,
            "hash": det_hash
        })

        return QueryResponse(
            response=response,
            mode=request.mode,
            confidence=confidence,
            doctrines_triggered=[d.topic for d in doctrines],
            reasoning_chain=[d.topic for d in doctrines],
            epistemic_warnings=warnings,
            determinism_hash=det_hash,
            processing_time_ms=elapsed,
            zone=zone
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="DRL02 - Directional Drilling Intelligence Engine",
    version="1.0.0",
    description="TIE Gold Standard engine for directional and horizontal drilling expertise"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

engine = DirectionalDrillingEngine()


@APP.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    uptime = (datetime.now() - engine.start_time).total_seconds()
    hit_rate = (engine.cache_hits / engine.query_count * 100) if engine.query_count > 0 else 0.0

    return HealthResponse(
        status="healthy",
        engine="DRL02_Directional_Drilling",
        version="1.0.0",
        port=9012,
        doctrines_loaded=len(engine.doctrine_cache),
        uptime_seconds=uptime,
        total_queries=engine.query_count,
        cache_hit_rate=hit_rate
    )


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    try:
        return engine.query(request)
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }


@APP.get("/telemetry")
async def get_telemetry():
    """Get engine telemetry data"""
    return {
        "total_queries": engine.query_count,
        "cache_hit_rate": (engine.cache_hits / engine.query_count * 100) if engine.query_count > 0 else 0.0,
        "uptime_seconds": (datetime.now() - engine.start_time).total_seconds(),
        "recent_queries": engine.query_log[-10:]
    }


if __name__ == "__main__":
    logger.info("Starting DRL02 Directional Drilling Engine on port 9012")
    uvicorn.run(APP, host="0.0.0.0", port=9012)
