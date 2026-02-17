"""
AUTO06 SUSPENSION SYSTEMS INTELLIGENCE ENGINE
TIE-Grade Automotive Suspension Analysis Engine

Analyzes suspension design, spring/damper tuning, vehicle dynamics, active/semi-active systems,
wheel alignment, and ride/handling balance per SAE J670 vehicle dynamics standards.

Port: 9251
Version: 1.0.0
TIE-20 Compliance: FULL
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict, Counter
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# CONFIGURATION & ENUMS
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
    DESIGN = "DESIGN"
    TUNING = "TUNING"
    DIAGNOSTICS = "DIAGNOSTICS"


class IssueCategory(str, Enum):
    SPRING_DESIGN = "spring_design"
    DAMPER_TUNING = "damper_tuning"
    GEOMETRY = "geometry"
    ACTIVE_SYSTEMS = "active_systems"
    ALIGNMENT = "alignment"
    VEHICLE_DYNAMICS = "vehicle_dynamics"
    NVH = "nvh"
    COMPLIANCE = "compliance"
    KINEMATICS = "kinematics"
    TESTING = "testing"


class AuthorityLevel(str, Enum):
    SAE_STANDARD = "SAE_STANDARD"  # SAE J670, J1490, etc.
    OEM_SPEC = "OEM_SPEC"  # Manufacturer specifications
    TEXTBOOK = "TEXTBOOK"  # Milliken, Gillespie, Dixon
    EMPIRICAL = "EMPIRICAL"  # Industry best practices
    SIMULATION = "SIMULATION"  # Multi-body dynamics validation


AUTHORITY_WEIGHTS = {
    AuthorityLevel.SAE_STANDARD: 1.0,
    AuthorityLevel.OEM_SPEC: 0.95,
    AuthorityLevel.TEXTBOOK: 0.90,
    AuthorityLevel.EMPIRICAL: 0.75,
    AuthorityLevel.SIMULATION: 0.85
}


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Single suspension engineering doctrine with reasoning framework"""
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
    entity_scope: str
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str
    issue_category: IssueCategory
    authority_level: AuthorityLevel
    disclosure_caveat: Optional[str] = None


@dataclass
class QueryContext:
    """Context for suspension analysis query"""
    vehicle_type: str
    suspension_type: str
    application: str  # street, track, off-road
    issue_categories: Set[IssueCategory]
    zone: AnalysisZone
    timestamp: float = field(default_factory=time.time)


@dataclass
class TelemetryRecord:
    """Telemetry for single query"""
    query_id: str
    timestamp: float
    mode: ResponseMode
    issue_categories: List[str]
    doctrines_triggered: List[str]
    cache_hit: bool
    latency_ms: float
    confidence: str
    zone: str


class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    vehicle_type: Optional[str] = "passenger_car"
    suspension_type: Optional[str] = "macpherson"
    application: Optional[str] = "street"


class QueryResponse(BaseModel):
    response: str
    mode: str
    confidence: str
    doctrines_triggered: List[str]
    latency_ms: float
    determinism_hash: str
    timestamp: str


# ============================================================================
# DOCTRINE CACHE - 25+ REAL SUSPENSION ENGINEERING BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [

    DoctrineBlock(
        topic="macpherson_strut_geometry",
        keywords=["macpherson", "strut", "geometry", "kingpin", "inclination", "scrub_radius"],
        conclusion_template="MacPherson strut geometry must balance kingpin inclination angle (typically 12-15 degrees) with scrub radius (preferably near zero or slightly negative) while managing camber gain in roll. The strut angle relative to vertical (8-12 degrees typical) determines lateral force feedback and steering returnability.",
        reasoning_framework="""
MacPherson Strut Geometry Analysis:

1. KINGPIN AXIS GEOMETRY
   - Kingpin inclination angle (KPI): Intersection of strut axis with vertical at ground
   - Typical range: 12-15 degrees from vertical
   - Higher KPI: Increases self-centering torque, reduces scrub radius
   - Lower KPI: Reduces tire scrub, improves straight-line stability

2. SCRUB RADIUS DETERMINATION
   - Scrub radius = lateral distance from KPI/ground intersection to tire center at ground
   - Positive scrub: KPI inside tire center (traditional FWD)
   - Negative scrub: KPI outside tire center (modern design for brake torque steer control)
   - Zero scrub: KPI at tire center (ideal but difficult to package)
   - FWD target: -5mm to +10mm
   - RWD target: 0mm to +15mm

3. CAMBER GAIN IN ROLL
   - Strut suspension has inherent positive camber gain (outside wheel goes positive in roll)
   - Typical: 0.5-0.8 degrees camber per degree of body roll
   - Requires static negative camber to compensate: -0.5 to -1.5 degrees
   - Cannot match double wishbone camber control

4. CASTER ANGLE EFFECTS
   - MacPherson caster: 3-6 degrees typical
   - Creates self-aligning torque proportional to lateral force
   - Caster trail = 25-40mm typical (sin(caster) × KPI height)
   - Provides steering feedback and returnability

5. STRUT ANGLE OPTIMIZATION
   - Lateral angle from vertical: 8-12 degrees inboard at top
   - Minimizes side load on strut bearing
   - Influences camber gain rate
   - Affects packaging around engine/drivetrain

6. PACKAGING CONSTRAINTS
   - Strut top mount location constrained by shock tower structure
   - Lower control arm angle: 5-8 degrees from horizontal (anti-dive/squat geometry)
   - Tie rod position: near lower ball joint height (minimize bump steer)
   - Spring preload: 10-20mm typical (ensures spring contact at full droop)
""",
        key_factors=[
            "Kingpin inclination angle (12-15 deg typical)",
            "Scrub radius magnitude and sign (target near zero)",
            "Camber gain rate (0.5-0.8 deg/deg roll)",
            "Caster angle (3-6 deg for self-centering)",
            "Strut lateral angle (8-12 deg from vertical)",
            "Lower control arm angle (anti-geometry)",
            "Bump steer characteristics (tie rod height)"
        ],
        primary_authority=[
            "SAE J670 Vehicle Dynamics Terminology",
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 17",
            "Dixon 'Suspension Geometry and Computation' Ch. 4",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 8"
        ],
        burden_holder="suspension_designer",
        adversary_position="Strut geometry is acceptable if vehicle meets basic handling targets",
        counter_arguments=[
            "Camber gain cannot match double wishbone performance",
            "Side loads on strut bearing cause friction and wear",
            "Limited tuning flexibility compared to multi-link",
            "Scrub radius varies with ride height changes",
            "Brake torque steer sensitive to scrub radius"
        ],
        resolution_strategy="Optimize strut angle and KPI for specific vehicle weight distribution and tire size. Use negative scrub radius for FWD to minimize torque steer. Accept camber gain limitation and compensate with static negative camber and anti-roll bar tuning.",
        entity_scope="MacPherson strut front suspension design (most common FWD/compact RWD configuration)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in geometric relationships. Caster/KPI targets are application-dependent (sport vs comfort).",
        controlling_precedent="SAE J670 defines kingpin axis and scrub radius terminology. Industry converged on negative scrub radius post-1980s for FWD torque steer control.",
        issue_category=IssueCategory.GEOMETRY,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="double_wishbone_geometry",
        keywords=["double_wishbone", "short_long_arm", "SLA", "camber_control", "roll_center"],
        conclusion_template="Double wishbone (SLA) geometry provides superior camber control through proper arm length ratio and pickup point placement. Upper arm typically 0.80-0.90 length of lower arm creates negative camber gain in bump (ideal for cornering). Roll center height (50-75mm above ground) and migration path are critical for handling balance.",
        reasoning_framework="""
Double Wishbone Suspension Geometry:

1. ARM LENGTH RATIO OPTIMIZATION
   - Short-Long Arm (SLA) configuration: upper arm shorter than lower arm
   - Typical ratio: upper/lower = 0.80-0.90
   - Shorter upper arm creates negative camber gain in bump
   - Target: -0.5 to -1.0 degrees camber per inch of bump travel
   - Keeps tire contact patch perpendicular to road in cornering

2. CAMBER CURVE DESIGN
   - Static camber: -0.5 to -2.0 degrees (performance), 0 to -0.5 (comfort)
   - Camber gain in bump: negative (tire leans into turn)
   - Camber loss in droop: positive (less critical)
   - Camber change in roll: -1.0 to -1.5 degrees per degree of body roll (outside wheel)
   - Much better than MacPherson strut (+0.5 to +0.8 deg/deg)

3. ROLL CENTER HEIGHT AND MIGRATION
   - Roll center: instantaneous center of body rotation relative to wheels
   - Front roll center height: 50-75mm above ground (sedan), 25-50mm (sports car)
   - Too high: jacking forces, excessive weight transfer, snap oversteer
   - Too low: excessive body roll, slow transient response
   - Migration path: should remain relatively constant through suspension travel
   - Front lower than rear: mild understeer characteristic

4. ANTI-DIVE AND ANTI-SQUAT GEOMETRY
   - Anti-dive: front lower arm angle (rear pivot higher than front)
   - Target: 20-40% anti-dive for passenger car (reduces pitch in braking)
   - Anti-squat: rear suspension geometry (50-70% for RWD sports car)
   - Calculated from instant center location relative to CG height
   - Trade-off: anti-geometry creates longitudinal force-induced camber change

5. KINGPIN AXIS AND CASTER
   - Kingpin axis: line through upper and lower ball joints
   - Caster angle: 4-8 degrees (higher for sports cars)
   - Caster trail: 30-50mm (provides self-aligning torque)
   - KPI angle: 5-8 degrees (less than strut due to ball joint positioning)
   - Mechanical trail: caster trail + pneumatic trail = total self-centering

6. PICKUP POINT OPTIMIZATION
   - Lower arm front-rear position: controls anti-geometry
   - Lower arm lateral position: controls track width change
   - Upper arm lateral position: controls camber gain
   - Fore-aft compliance bushings: 200-400 N/mm (absorbs impact, reduces harshness)
   - Lateral compliance bushings: 1000-2000 N/mm (maintains alignment)
""",
        key_factors=[
            "Arm length ratio (upper/lower = 0.80-0.90 typical)",
            "Camber gain in bump (target -0.5 to -1.0 deg/in)",
            "Roll center height (50-75mm front, 25-100mm rear)",
            "Anti-dive/anti-squat percentages (20-40% / 50-70%)",
            "Caster angle (4-8 degrees for self-centering)",
            "Bushing compliance rates (fore-aft vs lateral)",
            "Roll center migration path stability"
        ],
        primary_authority=[
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 16-17",
            "Dixon 'Suspension Geometry and Computation' Ch. 5-6",
            "SAE J670 Vehicle Dynamics Terminology",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 8"
        ],
        burden_holder="suspension_designer",
        adversary_position="Double wishbone is too expensive and complex for mass-market vehicles",
        counter_arguments=[
            "Requires more packaging space than strut",
            "Higher part count and cost",
            "More complex assembly and alignment",
            "Bushing compliance affects alignment over time",
            "Roll center migration difficult to optimize"
        ],
        resolution_strategy="Accept higher cost for performance vehicles where camber control is critical. Optimize arm lengths and pickup points through multi-body dynamics simulation. Validate with physical prototypes on K&C rig.",
        entity_scope="Double wishbone suspension (high-performance and luxury vehicles)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in geometric principles. Specific targets vary by vehicle type and tire characteristics.",
        controlling_precedent="Industry standard for sports cars and performance sedans since 1960s. SAE J670 defines roll center calculation methods.",
        issue_category=IssueCategory.GEOMETRY,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="spring_rate_calculation",
        keywords=["spring_rate", "ride_frequency", "natural_frequency", "wheel_rate", "motion_ratio"],
        conclusion_template="Spring rate must be calculated from target ride frequency (typically 1.0-1.3 Hz front, 1.1-1.5 Hz rear) using wheel rate, sprung mass, and motion ratio. Wheel rate = spring rate × (motion ratio)^2. Front/rear frequency ratio controls understeer gradient and pitch response.",
        reasoning_framework="""
Spring Rate Calculation and Ride Frequency Targeting:

1. RIDE FREQUENCY FUNDAMENTALS
   - Ride frequency (fn): natural frequency of sprung mass on suspension springs
   - Formula: fn = (1/2π) × sqrt(K/M) where K=wheel rate, M=sprung mass per corner
   - Target frequencies:
     * Passenger car comfort: 1.0-1.2 Hz front, 1.1-1.3 Hz rear
     * Sport sedan: 1.2-1.4 Hz front, 1.3-1.5 Hz rear
     * Sports car: 1.4-1.8 Hz front, 1.5-2.0 Hz rear
     * Racing: 2.0-3.5 Hz (depending on aero downforce)

2. MOTION RATIO DETERMINATION
   - Motion ratio (MR): spring displacement / wheel displacement
   - Measured from suspension geometry (spring mounting point relative to wheel)
   - MacPherson strut: MR = 0.85-0.95 (spring nearly vertical)
   - Double wishbone: MR = 0.50-0.75 (spring on lower arm)
   - Multi-link: MR = 0.60-0.80 (depends on spring mounting)
   - Coilover (spring on damper): MR = 0.90-1.00

3. WHEEL RATE CALCULATION
   - Wheel rate (Kw): effective spring rate at the wheel
   - Kw = Ks × MR^2 where Ks = coil spring rate
   - Example: 500 lb/in spring, MR=0.70 → Kw = 500×0.49 = 245 lb/in
   - Anti-roll bar adds wheel rate (in roll only): Kw_roll = Kw + Kbar/2

4. REQUIRED SPRING RATE CALCULATION
   - Rearrange ride frequency equation:
   - Ks = (2π × fn)^2 × M / MR^2
   - Example: 1.2 Hz target, 400 kg sprung mass/corner, MR=0.70
   - Ks = (2π×1.2)^2 × 400 / 0.49 = 57.0 N/mm = 325 lb/in

5. FRONT/REAR FREQUENCY RATIO
   - Ratio = fn_rear / fn_front
   - Typical: 1.05-1.15 (slightly stiffer rear)
   - Affects pitch damping and handling balance
   - Lower ratio (rear softer): more understeer, comfortable
   - Higher ratio (rear stiffer): more neutral/oversteer, better turn-in

6. PROGRESSIVE VS LINEAR SPRINGS
   - Linear spring: constant rate throughout travel
   - Progressive spring: rate increases with compression
   - Progressive used for: wide load range, limited suspension travel
   - Racing: always linear springs (predictable behavior)
   - Dual-rate spring: soft initial, stiff bump stop (micro-bump compliance)

7. PRELOAD CONSIDERATIONS
   - Preload: spring compression at static ride height
   - Minimum: 10-15mm (ensures spring contact at full droop)
   - Maximum: limited by coil bind at full compression
   - Preload does NOT change spring rate or ride height (common misconception)
   - Ride height set by: spring rate, preload, and vehicle weight
""",
        key_factors=[
            "Target ride frequency (1.0-1.8 Hz depending on application)",
            "Sprung mass per corner (250-500 kg typical)",
            "Motion ratio from suspension geometry (0.50-0.95)",
            "Front/rear frequency ratio (1.05-1.15 typical)",
            "Spring travel available (80-120mm typical)",
            "Progressive vs linear rate selection",
            "Preload requirement (10-15mm minimum)"
        ],
        primary_authority=[
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 19",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 7",
            "SAE J1490 'Ride and Vibration Data Manual'",
            "Dixon 'The Shock Absorber Handbook' Ch. 2"
        ],
        burden_holder="suspension_engineer",
        adversary_position="Spring rate can be selected empirically without frequency calculations",
        counter_arguments=[
            "Motion ratio varies through suspension travel (non-linear)",
            "Anti-roll bar contribution complicates calculation",
            "Tire vertical stiffness acts as series spring (reduces effective wheel rate)",
            "Frequency targets subjective and application-dependent",
            "Progressive springs have variable rate (can't use single frequency value)"
        ],
        resolution_strategy="Use average motion ratio for initial calculation. Account for tire vertical stiffness (~200-300 lb/in) in series with wheel rate. Validate with physical prototype testing and adjust empirically. For progressive springs, use rate at mid-travel for initial design.",
        entity_scope="Coil spring and wheel rate calculation for all suspension types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in calculation methods. Frequency targets are subjective and require empirical validation.",
        controlling_precedent="Ride frequency targeting is industry standard design method. SAE J1490 provides recommended frequency ranges by vehicle class.",
        issue_category=IssueCategory.SPRING_DESIGN,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="damper_valving_compression_rebound",
        keywords=["damper", "shock_absorber", "compression", "rebound", "valving", "damping_ratio"],
        conclusion_template="Damper valving must provide asymmetric damping with rebound typically 2-4× stiffer than compression (measured as force at 0.5 m/s shaft velocity). Target damping ratio 0.25-0.35 (comfort) or 0.40-0.70 (sport). Compression controls body motion into bumps; rebound controls body recovery and prevents oscillation.",
        reasoning_framework="""
Damper Valving and Compression/Rebound Tuning:

1. DAMPING FUNDAMENTALS
   - Damper force: F = C × V where C=damping coefficient, V=shaft velocity
   - Measured at standard velocity: 0.5 m/s (20 in/s) typical test point
   - Force vs velocity curve: linear (low speed), progressive (high speed due to valving)
   - Asymmetric damping: different C for compression vs rebound

2. COMPRESSION DAMPING (BUMP)
   - Controls body motion INTO bumps
   - Low-speed compression (0-0.3 m/s): controls body roll, pitch, heave
   - High-speed compression (>0.3 m/s): controls impact harshness, tire contact
   - Typical force at 0.5 m/s: 300-600 N (sport), 150-300 N (comfort)
   - Too stiff: harsh ride, poor impact compliance
   - Too soft: excessive body motion, wallowing

3. REBOUND DAMPING (EXTENSION)
   - Controls body motion OUT OF bumps
   - Prevents oscillation after disturbance
   - Typical force at 0.5 m/s: 600-1800 N (2-4× compression)
   - Rebound/compression ratio: 2.0-3.0 (comfort), 3.0-4.0 (sport)
   - Too stiff: packing (suspension stays compressed), harsh secondary impacts
   - Too soft: overshoot, oscillation, porpoising

4. DAMPING RATIO CALCULATION
   - Damping ratio (ζ): ratio of actual damping to critical damping
   - ζ = C / (2 × sqrt(K × M)) where C=damping coeff, K=wheel rate, M=sprung mass
   - Critical damping (ζ=1.0): returns to equilibrium without oscillation
   - Underdamped (ζ<1.0): oscillates before settling
   - Target ranges:
     * Comfort: ζ = 0.25-0.35 (allows some overshoot for smooth ride)
     * Sport: ζ = 0.40-0.60 (minimal overshoot, tight body control)
     * Racing: ζ = 0.60-0.70 (very stiff, minimal body motion)

5. DIGRESSIVE VS PROGRESSIVE VALVING
   - Digressive: damping force rises quickly, then levels off (soft at high speed)
   - Progressive: damping force increases continuously with velocity
   - Digressive: better impact compliance, common in off-road
   - Progressive: better body control, common in circuit racing
   - Modern: multi-stage valving (low-speed digressive, high-speed progressive)

6. ADJUSTABLE DAMPERS
   - Single-adjustable: rebound only (compression fixed or coupled)
   - Double-adjustable: independent compression and rebound
   - Triple-adjustable: low-speed compression, high-speed compression, rebound
   - Electronic: continuously variable (MagneRide, adaptive dampers)

7. FREQUENCY-DEPENDENT BEHAVIOR
   - Damper effectiveness varies with input frequency
   - 0-3 Hz: body motion (roll, pitch, heave) - low-speed damping
   - 3-15 Hz: wheel motion over bumps - mid-speed damping
   - 15-30 Hz: tire resonance - high-speed damping
   - 30+ Hz: tire deflection - no damping benefit (damper can't react)
""",
        key_factors=[
            "Compression damping force (300-600 N at 0.5 m/s)",
            "Rebound damping force (600-1800 N at 0.5 m/s)",
            "Rebound/compression ratio (2.0-4.0)",
            "Damping ratio (0.25-0.70 depending on application)",
            "Low-speed vs high-speed valving characteristics",
            "Digressive vs progressive valve design",
            "Frequency-dependent effectiveness (0-15 Hz most critical)"
        ],
        primary_authority=[
            "Dixon 'The Shock Absorber Handbook' Ch. 3-5",
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 19",
            "SAE J1490 'Ride and Vibration Data Manual'",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 7"
        ],
        burden_holder="suspension_engineer",
        adversary_position="Damper tuning can be done empirically without calculating damping ratios",
        counter_arguments=[
            "Damping ratio calculation assumes linear damper (most are non-linear)",
            "Motion ratio affects damper velocity vs wheel velocity",
            "Tire damping adds to total system damping (difficult to quantify)",
            "Subjective ride quality doesn't correlate directly with damping ratio",
            "Adjustable dampers have wide range (calculation gives only starting point)"
        ],
        resolution_strategy="Use damping ratio as initial design target. Account for motion ratio when converting wheel damping to shaft damping. Validate with dyno testing (force vs velocity curves). Final tuning requires subjective evaluation on vehicle. Start at lower damping ratio and increase until oscillation is controlled.",
        entity_scope="Hydraulic damper (shock absorber) valving and tuning for all suspension types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in damping theory. Specific values highly dependent on vehicle mass, tire characteristics, and subjective ride quality targets.",
        controlling_precedent="Industry standard practice is 2-4× asymmetry (rebound/compression). SAE J1490 provides recommended damping ratio ranges.",
        issue_category=IssueCategory.DAMPER_TUNING,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="anti_roll_bar_sizing",
        keywords=["anti_roll_bar", "ARB", "sway_bar", "roll_stiffness", "understeer_gradient"],
        conclusion_template="Anti-roll bar (ARB) sizing controls roll stiffness distribution between front and rear axles, directly affecting understeer gradient. Increasing front ARB increases understeer; increasing rear ARB increases oversteer. Total roll stiffness = wheel rate + ARB contribution. Target 50-60% front roll stiffness for mild understeer (passenger car).",
        reasoning_framework="""
Anti-Roll Bar Design and Handling Balance:

1. ROLL STIFFNESS FUNDAMENTALS
   - Roll stiffness (Kφ): resistance to body roll in cornering
   - Total Kφ = spring contribution + ARB contribution
   - Spring roll stiffness per axle: Kφ_spring = Kw × t^2 where t=track width
   - ARB roll stiffness per axle: Kφ_bar (depends on bar diameter, length, arm length)
   - Total front roll stiffness: Kφ_f = Kφ_spring_f + Kφ_bar_f
   - Total rear roll stiffness: Kφ_r = Kφ_spring_r + Kφ_bar_r

2. ROLL STIFFNESS DISTRIBUTION (RSD)
   - RSD = Kφ_f / (Kφ_f + Kφ_r) × 100%
   - Passenger car target: 50-60% front (mild understeer)
   - Sport sedan target: 48-55% front (neutral to mild understeer)
   - Sports car target: 45-52% front (neutral to mild oversteer)
   - RSD directly affects lateral weight transfer distribution

3. UNDERSTEER GRADIENT RELATIONSHIP
   - Understeer gradient (K): deg/g of steering increase needed for increasing lateral accel
   - Positive K: understeer (safe, stable)
   - Negative K: oversteer (requires driver skill)
   - Zero K: neutral steer (ideal for racing)
   - RSD affects K: increasing front ARB increases K (more understeer)
   - Relationship: ΔK ≈ 0.5 to 1.0 deg/g per 5% shift in RSD (approximate, tire-dependent)

4. ARB RATE CALCULATION
   - ARB torsional stiffness: Kt = (G × π × d^4) / (32 × L)
   - G = shear modulus (80 GPa for steel)
   - d = bar diameter (mm)
   - L = effective length between arms (mm)
   - ARB wheel rate contribution: Kbar = Kt × (arm_length / track_width)^2 × 2
   - Example: 25mm dia, 600mm length, 250mm arms, 1500mm track → Kbar ≈ 40 N/mm per wheel

5. BAR DIAMETER EFFECT
   - Rate proportional to d^4 (diameter to 4th power)
   - 10% diameter increase → 46% rate increase
   - Small diameter changes have large effect
   - Typical diameters: 20-30mm (passenger car), 25-35mm (sport)

6. ADJUSTABLE ARB
   - Multiple arm positions: change effective arm length
   - Shorter arm → stiffer ARB (less leverage)
   - Typical adjustment range: ±20-30% rate
   - Racing: 3-5 position adjustable ARBs (front and rear)

7. NO ARB CONSIDERATIONS
   - Some vehicles run no rear ARB: maximize rear grip, accept more body roll
   - Off-road: no ARB allows independent wheel articulation
   - FWD hot hatch: sometimes no rear ARB for aggressive turn-in (lift-off oversteer)
""",
        key_factors=[
            "Roll stiffness distribution (50-60% front typical for understeer)",
            "ARB diameter (20-35mm, rate proportional to d^4)",
            "Effective length and arm length (affect torsional rate)",
            "Understeer gradient change (0.5-1.0 deg/g per 5% RSD shift)",
            "Front vs rear ARB balance (affects handling character)",
            "Adjustability range (±20-30% typical)",
            "Track width effect on wheel rate contribution"
        ],
        primary_authority=[
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 18-19",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 9",
            "SAE J670 Vehicle Dynamics Terminology",
            "Dixon 'Suspension Geometry and Computation' Ch. 8"
        ],
        burden_holder="suspension_engineer",
        adversary_position="ARB sizing can be done by trial and error without calculations",
        counter_arguments=[
            "Understeer gradient also affected by tire characteristics (not just RSD)",
            "Aerodynamic downforce distribution affects handling balance (high-speed)",
            "Driver preference varies (some like more understeer for safety)",
            "ARB reduces independent wheel compliance (harsher ride)",
            "Extreme ARB can cause inside wheel lift (reduce total grip)"
        ],
        resolution_strategy="Calculate RSD from existing spring rates and vehicle weight distribution. Adjust ARB diameters to achieve target RSD. Validate with on-road testing and adjust empirically. Use adjustable ARBs for fine-tuning. Monitor inside wheel lift in tight corners (limit ARB rate).",
        entity_scope="Anti-roll bar design and tuning for handling balance (all vehicle types)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in rate calculations. Understeer gradient relationship approximate (tire-dependent). Final tuning requires empirical validation.",
        controlling_precedent="Industry standard is to use RSD to control understeer gradient. Higher front RSD creates understeer (safe for passenger cars).",
        issue_category=IssueCategory.VEHICLE_DYNAMICS,
        authority_level=AuthorityLevel.TEXTBOOK
    ),

    DoctrineBlock(
        topic="wheel_alignment_parameters",
        keywords=["alignment", "toe", "camber", "caster", "thrust_angle", "KPI"],
        conclusion_template="Wheel alignment specifications must balance tire wear, handling response, and straight-line stability. Toe (±3mm total typical) controls turn-in response and wear. Camber (-0.5 to -2.0 deg) optimizes tire contact in cornering. Caster (3-8 deg) provides self-centering. Thrust angle (<0.2 deg) ensures straight tracking.",
        reasoning_framework="""
Wheel Alignment Parameter Specifications:

1. TOE ANGLE SPECIFICATIONS
   - Toe: angle of wheels relative to vehicle centerline (plan view)
   - Toe-in: front of wheels closer than rear (positive)
   - Toe-out: front of wheels farther than rear (negative)
   - Measurement: mm per wheel or degrees or total toe
   - Front toe typical ranges:
     * RWD comfort: 0 to +2mm total (slight toe-in for stability)
     * FWD comfort: +1 to +3mm total (compensates for drivetrain pull)
     * RWD sport: -1 to +1mm total (near zero for responsiveness)
     * FWD sport: 0 to +2mm total
   - Rear toe typical ranges:
     * Comfort: +1 to +3mm total (toe-in for stability)
     * Sport: 0 to +2mm total (less toe-in for agility)
   - Effects:
     * Toe-in: increases straight-line stability, scrubs tires, dulls turn-in
     * Toe-out: quicker turn-in, reduces stability, wears tires faster
     * Excessive toe (>5mm total): rapid tire wear on inner edges

2. CAMBER ANGLE SPECIFICATIONS
   - Camber: wheel tilt relative to vertical (front view)
   - Negative camber: top of wheel tilts inboard
   - Positive camber: top of wheel tilts outboard (rare on modern cars)
   - Static camber typical ranges:
     * Comfort: -0.5 to -1.0 deg front, -1.0 to -1.5 deg rear
     * Sport: -1.5 to -2.5 deg front, -2.0 to -3.0 deg rear
     * Racing: -3.0 to -5.0 deg (depending on track and tire)
   - Effects:
     * Negative camber: improves cornering grip (tire contact in roll)
     * Excessive negative: inner edge tire wear, reduced straight-line grip
     * Positive camber: outer edge wear, poor cornering
   - Camber gain in roll: suspension design-dependent (see geometry doctrines)

3. CASTER ANGLE SPECIFICATIONS
   - Caster: steering axis tilt relative to vertical (side view)
   - Positive caster: axis tilts rearward at top (standard)
   - Negative caster: axis tilts forward (unstable, never used)
   - Typical ranges:
     * Passenger car: 3-5 deg
     * Sport sedan: 5-7 deg
     * Sports car: 6-8 deg
   - Effects:
     * Caster creates self-aligning torque (steering returns to center)
     * Higher caster: more self-centering, heavier steering, more feedback
     * Caster also creates camber change with steer angle (dynamic camber)
     * Camber change ≈ sin(caster) × sin(steer_angle)
   - Cross-caster (left-right difference): <0.5 deg (causes pull)

4. KINGPIN INCLINATION (KPI)
   - KPI: steering axis tilt relative to vertical (front view)
   - Set by suspension geometry, not adjustable (except with bushings)
   - Typical: 12-15 deg (MacPherson strut), 5-8 deg (double wishbone)
   - Creates self-centering torque (wheels want to return to straight)
   - Interacts with caster to determine scrub radius

5. THRUST ANGLE
   - Thrust angle: rear axle centerline relative to vehicle centerline
   - Causes dog-tracking (rear offset from front)
   - Target: <0.2 deg (some specs allow up to 0.3 deg)
   - Corrected by: adjusting rear toe (if adjustable) or frame straightening
   - Symptoms: steering wheel off-center when driving straight

6. SETBACK
   - Setback: one front wheel ahead of the other
   - Caused by: collision damage, bent frame
   - Target: <5mm difference in wheel position
   - Affects: steering feel, tire wear, crash test performance

7. ALIGNMENT TOLERANCE AND ADJUSTMENT
   - Specifications typically given as range (e.g. -0.5 to -1.5 deg)
   - Target center of range for symmetric setup
   - Left-right difference: minimize for straight tracking
     * Camber: <0.5 deg difference
     * Caster: <0.5 deg difference
     * Toe: <1mm difference per side
   - Adjustment frequency: every 10,000-20,000 miles or after suspension work
""",
        key_factors=[
            "Front toe (0 to +3mm total typical, affects turn-in and wear)",
            "Rear toe (+1 to +3mm total typical, affects stability)",
            "Front camber (-0.5 to -2.5 deg, affects cornering grip)",
            "Rear camber (-1.0 to -3.0 deg, affects grip and tire wear)",
            "Caster angle (3-8 deg, affects self-centering)",
            "Thrust angle (<0.2 deg, affects straight tracking)",
            "Left-right symmetry (<0.5 deg camber/caster, <1mm toe)"
        ],
        primary_authority=[
            "SAE J670 Vehicle Dynamics Terminology",
            "Hunter Engineering Alignment Specifications Database",
            "OEM Service Manual Specifications",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 8"
        ],
        burden_holder="alignment_technician",
        adversary_position="Alignment specs are loose guidelines, any value within range is acceptable",
        counter_arguments=[
            "Alignment specs vary widely by vehicle and tire (no universal values)",
            "Driver preference affects optimal settings (sport vs comfort)",
            "Tire wear patterns indicate needed corrections (empirical tuning)",
            "Lowered vehicles require different alignment (more negative camber)",
            "Wider tires may require more negative camber"
        ],
        resolution_strategy="Use OEM specifications as baseline. For performance applications, add negative camber (within tire wear limits), minimize toe for responsiveness, increase caster for feedback. Measure tire temperatures across tread to validate camber. Adjust toe based on tire wear patterns. Maintain left-right symmetry.",
        entity_scope="Static wheel alignment specifications (all vehicle types)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in measurement methods and typical ranges. Specific values are vehicle and application-dependent. OEM specs always take precedence.",
        controlling_precedent="SAE J670 defines alignment terminology. OEM specifications are legal requirement for warranty coverage.",
        issue_category=IssueCategory.ALIGNMENT,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="magenride_active_damper",
        keywords=["magnetorheological", "MagneRide", "adaptive_damper", "semi_active", "MR_fluid"],
        conclusion_template="Magnetorheological (MR) dampers use electrically-controlled magnetic field to change fluid viscosity in real-time (1-5 ms response). Provides continuously variable damping from soft (comfort) to firm (sport) without mechanical valves. Current range 0-2A typical. Force range 2-10× variation achievable. Requires sensors (accelerometers, position) and control ECU.",
        reasoning_framework="""
MagneRide and Magnetorheological Damper Technology:

1. MR FLUID PHYSICS
   - Magnetorheological fluid: suspension of iron particles in synthetic oil
   - Particle size: 1-10 microns
   - Particle concentration: 20-40% by volume
   - No magnetic field: fluid is liquid (low viscosity)
   - Magnetic field applied: particles align into chains (high viscosity)
   - Transition time: 1-5 milliseconds (very fast response)
   - Reversible: viscosity returns to normal when field removed

2. DAMPER CONSTRUCTION
   - Electromagnetic coil wound around damper piston
   - Current applied to coil creates magnetic field through piston orifices
   - MR fluid flow through orifices is restricted by particle alignment
   - Higher current → stronger field → higher viscosity → more damping force
   - Current range: 0-2 amps typical (12V system, 24W max power)
   - Force range: 200-2000 N typical (10:1 variation at 0.5 m/s velocity)

3. CONTROL SYSTEM ARCHITECTURE
   - Inputs:
     * Body accelerometers (vertical, roll, pitch): 4-8 sensors
     * Suspension position sensors: 4 (one per corner)
     * Steering angle sensor
     * Brake pressure sensor
     * Throttle position sensor
     * Vehicle speed sensor
   - ECU processing: real-time damping force calculation (1000 Hz update rate)
   - Outputs: PWM current to each damper coil (4 independent channels)

4. CONTROL MODES
   - Tour mode: soft damping (0.2-0.4A average, comfort priority)
   - Sport mode: firm damping (0.8-1.5A average, handling priority)
   - Track mode: very firm (1.2-2.0A average, maximum control)
   - Auto mode: adaptive (varies 0-2A based on road and driving inputs)
   - Individual corner control: can vary damping per wheel independently

5. SKYHOOK CONTROL ALGORITHM
   - Skyhook: theoretical damper connecting body to inertial reference (sky)
   - Goal: minimize body motion while maintaining tire contact
   - Logic: stiffen damper when body and wheel moving same direction (body control)
   - Logic: soften damper when body and wheel moving opposite direction (tire contact)
   - Implementation: calculate desired skyhook force, map to available MR damper force
   - Result: better ride quality + better handling than passive damper

6. PERFORMANCE CHARACTERISTICS
   - Response time: 1-5 ms (vs 50-200 ms for mechanical adaptive dampers)
   - Dynamic range: 2-10× force variation (vs 2-3× for mechanical)
   - Reliability: no mechanical valves to wear (fluid is maintenance-free)
   - Power consumption: 20-100W total for 4 dampers
   - Cost: 2-3× cost of passive damper

7. FAILURE MODES
   - Coil open circuit: damper defaults to soft (fluid has baseline viscosity)
   - Coil short circuit: damper stuck at medium-firm (partial field from residual current)
   - Sensor failure: ECU defaults to safe mode (medium damping)
   - ECU failure: dampers default to soft (fail-safe)
   - Fluid leak: same as conventional damper (requires replacement)
""",
        key_factors=[
            "MR fluid particle alignment response (1-5 ms)",
            "Current range (0-2A typical for force control)",
            "Dynamic force range (2-10× variation achievable)",
            "Sensor suite (accelerometers, position, steering, brake)",
            "Skyhook control algorithm (minimize body motion, maintain tire contact)",
            "Control modes (Tour/Sport/Track/Auto)",
            "Power consumption (20-100W total)",
            "Failure mode (default to soft/safe)"
        ],
        primary_authority=[
            "Delphi/BWI MagneRide Technical Documentation",
            "SAE 2003-01-0283 'Magnetorheological Technology'",
            "Dixon 'The Shock Absorber Handbook' Ch. 9",
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 19"
        ],
        burden_holder="automotive_OEM",
        adversary_position="Semi-active dampers add cost and complexity without significant benefit over passive",
        counter_arguments=[
            "2-3× cost premium over passive dampers",
            "Requires ECU, sensors, wiring (complexity)",
            "Power consumption (small but not zero)",
            "MR fluid degrades over time (reduced dynamic range after 100k+ miles)",
            "Failure modes still result in degraded performance"
        ],
        resolution_strategy="Accept cost premium for performance/luxury vehicles where ride quality and handling are priorities. Implement robust diagnostics and fail-safe modes. Use skyhook control for optimal body motion vs tire contact trade-off. Validate with physical prototypes on test track and ride simulator.",
        entity_scope="Magnetorheological (MR) semi-active damper technology (e.g. GM MagneRide, Audi Magnetic Ride)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in technology principles. Specific force ranges and control algorithms are proprietary. Public domain control logic (skyhook) is well-established.",
        controlling_precedent="MagneRide introduced by Delphi/GM in 2002 (Corvette C5). Now industry standard for high-performance semi-active dampers.",
        issue_category=IssueCategory.ACTIVE_SYSTEMS,
        authority_level=AuthorityLevel.OEM_SPEC
    ),

    DoctrineBlock(
        topic="bump_steer_kinematics",
        keywords=["bump_steer", "tie_rod", "steering_rack", "toe_change", "kinematics"],
        conclusion_template="Bump steer is unwanted toe change during suspension travel, caused by misaligned steering linkage geometry. Tie rod must be parallel to control arm (side view) and at correct height relative to instant center (front view). Target <1mm toe change per 25mm suspension travel. Measured on K&C rig or with bump steer gauge.",
        reasoning_framework="""
Bump Steer Kinematics and Correction:

1. BUMP STEER DEFINITION
   - Bump steer: change in toe angle during vertical suspension travel (bump/droop)
   - Caused by: steering linkage geometry not matching suspension geometry
   - Measurement: mm of toe change per mm (or inch) of wheel travel
   - Target: <1mm toe change over ±25mm wheel travel (0.04 mm/mm ratio)
   - Excessive bump steer: >2mm over ±25mm (causes darting, nervousness)

2. GEOMETRIC CAUSES (SIDE VIEW)
   - Tie rod must be parallel to lower control arm in side view
   - If tie rod angle differs: wheel steers as suspension moves vertically
   - Tie rod too high: bump causes toe-out, droop causes toe-in
   - Tie rod too low: bump causes toe-in, droop causes toe-out
   - Correction: adjust tie rod end height (shims, eccentric bushings, or redesign)

3. GEOMETRIC CAUSES (FRONT VIEW)
   - Tie rod inner pivot must align with instant center of suspension
   - Instant center: intersection of upper and lower control arm extensions
   - MacPherson strut: IC is at strut top mount
   - Double wishbone: IC calculated from arm angles
   - If misaligned: wheel steers as it moves laterally (track width change in travel)

4. RACK HEIGHT OPTIMIZATION
   - Steering rack height affects tie rod angle
   - Ideal: rack positioned so tie rod is parallel to lower control arm
   - Typical rack height: 50-150mm below lower ball joint
   - Packaging constraints often prevent ideal position
   - Compromise: minimize bump steer in normal ride height range (±15mm)

5. TIE ROD LENGTH AND ANGLE
   - Longer tie rod: less angular change for given steering input (reduces bump steer sensitivity)
   - Tie rod angle: typically 5-15 deg from horizontal (side view)
   - Fore-aft position: at or slightly forward of lower ball joint (minimizes bump steer)
   - Lateral position: outboard as packaging allows (longer effective length)

6. MEASUREMENT METHODS
   - K&C rig: suspension kinematics and compliance test rig (industry standard)
   - Bump steer gauge: toe plate with dial indicators, measure toe at various ride heights
   - String method: plumb bob and string to measure toe change (low-cost alternative)
   - Procedure: fix steering wheel, cycle suspension through travel, measure toe

7. CORRECTION STRATEGIES
   - Tie rod end height adjustment: shims, spacers, or eccentric bushings
   - Steering rack repositioning: raise or lower rack (may require new mounts)
   - Bump steer kit: aftermarket spacers and longer tie rod ends
   - Ackermann adjustment: affects low-speed turn-in, not bump steer
   - Roll center correction: lowered vehicles often need bump steer correction

8. ROLL STEER RELATIONSHIP
   - Roll steer: toe change during body roll (related to bump steer)
   - Outside wheel in bump, inside wheel in droop → toe change affects handling
   - Rear roll steer: can be tuned for understeer/oversteer (passive rear-wheel steer)
   - Front roll steer: generally minimized (causes instability)
""",
        key_factors=[
            "Toe change limit (<1mm per 25mm travel target)",
            "Tie rod parallel to control arm (side view)",
            "Tie rod inner pivot aligned with instant center (front view)",
            "Steering rack height (affects tie rod angle)",
            "Tie rod length (longer reduces sensitivity)",
            "Measurement on K&C rig or bump steer gauge",
            "Correction via tie rod end height adjustment"
        ],
        primary_authority=[
            "Dixon 'Suspension Geometry and Computation' Ch. 7",
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 17",
            "SAE J670 Vehicle Dynamics Terminology",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 8"
        ],
        burden_holder="suspension_designer",
        adversary_position="Small amount of bump steer is acceptable and common in production vehicles",
        counter_arguments=[
            "Perfect bump steer elimination is difficult with packaging constraints",
            "Lowered vehicles always have some bump steer (suspension geometry changed)",
            "Bump steer in normal ride height range is most critical (extremes less important)",
            "Roll steer (rear) can be beneficial for handling (passive rear steer effect)",
            "Driver may not notice small amounts (<2mm over ±25mm)"
        ],
        resolution_strategy="Prioritize minimizing bump steer in normal ride height range (±15mm). Accept small amounts at extreme travel (rarely encountered). For lowered vehicles, install bump steer correction kit (adjust tie rod height). Measure on K&C rig or with bump steer gauge. Validate with on-road testing (straight-line stability over bumps).",
        entity_scope="Bump steer kinematics and correction (all suspension types with steering)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in geometric principles. Specific target values vary by vehicle and driver sensitivity. K&C rig measurement is gold standard.",
        controlling_precedent="Industry practice is to minimize bump steer by aligning tie rod with control arm. SAE J670 defines measurement methodology.",
        issue_category=IssueCategory.KINEMATICS,
        authority_level=AuthorityLevel.TEXTBOOK
    ),

    DoctrineBlock(
        topic="multi_link_rear_suspension",
        keywords=["multi_link", "five_link", "rear_suspension", "toe_control", "camber_control"],
        conclusion_template="Multi-link rear suspension uses 4-5 independent links per wheel to control wheel path, camber, and toe independently. Provides superior camber control (negative gain in bump), toe compliance control (anti-squat without toe change), and packaging flexibility. Common in performance and luxury vehicles. More complex and expensive than simple trailing arm or torsion beam.",
        reasoning_framework="""
Multi-Link Rear Suspension Design:

1. MULTI-LINK ARCHITECTURE
   - 4-link: upper link, lower link, toe link, camber link (plus spring/damper)
   - 5-link: adds second upper or lower link for better control
   - Each link controls one degree of freedom (DOF)
   - Independent control: camber, toe, roll center, anti-squat
   - Packaging: links can route around exhaust, fuel tank, driveline

2. LINK FUNCTIONS
   - Upper link(s): controls camber gain, roll center height
   - Lower link(s): controls fore-aft position, anti-squat
   - Toe link: controls toe change in bump/braking/acceleration
   - Camber link: controls camber curve (sometimes combined with upper link)
   - Spring/damper: can be mounted inboard (reduces unsprung mass)

3. CAMBER CONTROL OPTIMIZATION
   - Multi-link can achieve negative camber gain in bump (like front double wishbone)
   - Target: -0.5 to -1.0 deg camber per inch bump travel
   - Keeps rear tire perpendicular to road in cornering
   - Improves rear grip and handling balance
   - Better than trailing arm (positive camber gain) or semi-trailing arm (compromise)

4. TOE COMPLIANCE CONTROL
   - Toe link geometry controls toe change under load
   - Separate toe link allows anti-squat without unwanted toe change
   - Compliance steer: intentional toe change under load (tuning tool)
   - Example: rear toe-in under braking for stability
   - Example: rear toe-out under power for agility (RWD)
   - Bushing compliance: 500-2000 N/mm (tunable for desired compliance steer)

5. ANTI-SQUAT GEOMETRY
   - Anti-squat: percentage of squat prevented under acceleration
   - RWD target: 50-80% (reduces pitch, improves traction)
   - FWD/AWD target: 20-40% (less critical for rear)
   - Calculated from instant center location relative to CG height
   - Multi-link allows anti-squat tuning without affecting toe or camber

6. ROLL CENTER HEIGHT AND MIGRATION
   - Roll center: calculated from link geometry (more complex than double wishbone)
   - Target height: 25-100mm above ground (lower than front for understeer)
   - Multi-link allows independent tuning of roll center vs camber gain
   - Migration path: should remain stable through travel

7. PACKAGING ADVANTAGES
   - Links can route around obstacles (exhaust, fuel tank)
   - Spring/damper can be inboard (reduces unsprung mass, improves ride)
   - Subframe mounting: isolates road noise, allows precise geometry
   - Compact packaging: fits in tight spaces (luxury sedans, sports cars)

8. COMPLEXITY AND COST
   - Part count: 8-10 links plus bushings (vs 2 for trailing arm)
   - Bushing count: 16-20 (each adds cost and potential compliance)
   - Alignment complexity: more adjustments needed
   - Cost: 2-3× trailing arm, similar to double wishbone
   - Tuning: more degrees of freedom = more tuning options (pro and con)
""",
        key_factors=[
            "Link count (4-5 per wheel for independent control)",
            "Camber gain (target -0.5 to -1.0 deg/in bump)",
            "Toe compliance control (separate toe link)",
            "Anti-squat percentage (50-80% RWD typical)",
            "Roll center height (25-100mm above ground)",
            "Packaging flexibility (route around obstacles)",
            "Complexity and cost (2-3× simple trailing arm)",
            "Bushing compliance tuning (500-2000 N/mm)"
        ],
        primary_authority=[
            "Dixon 'Suspension Geometry and Computation' Ch. 6",
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 17",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 8",
            "OEM Service Manuals (BMW, Audi, Mercedes multi-link designs)"
        ],
        burden_holder="suspension_designer",
        adversary_position="Multi-link is over-engineered, simpler suspension adequate for most vehicles",
        counter_arguments=[
            "Higher part count and cost than trailing arm or torsion beam",
            "More bushings create more compliance and alignment drift over time",
            "Alignment is more complex (more adjustments needed)",
            "Tuning is more complex (many interacting parameters)",
            "Weight penalty vs simpler designs (more links and bushings)"
        ],
        resolution_strategy="Accept complexity and cost for performance and luxury vehicles where rear camber control and packaging flexibility are priorities. Use simulation (multi-body dynamics) to optimize link lengths and pickup points. Validate with K&C rig testing. Simplify to 4-link if 5-link not needed. Use compliant bushings to tune handling character.",
        entity_scope="Multi-link (4-5 link) independent rear suspension (performance and luxury vehicles)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in design principles. Specific link arrangements are proprietary and vary by OEM. General performance targets are well-established.",
        controlling_precedent="Multi-link rear suspension became industry standard for performance/luxury in 1990s-2000s. BMW, Mercedes, Audi use variations. SAE J670 defines terminology.",
        issue_category=IssueCategory.GEOMETRY,
        authority_level=AuthorityLevel.TEXTBOOK
    ),

    DoctrineBlock(
        topic="suspension_nvh_control",
        keywords=["NVH", "noise_vibration_harshness", "bushing_compliance", "subframe_isolation", "resonance"],
        conclusion_template="Suspension NVH control requires balancing bushing compliance (softer for isolation, stiffer for handling precision) with subframe isolation mounts. Target frequencies: body 8-12 Hz, suspension 10-15 Hz, tire cavity 200-250 Hz. Compliant bushings (200-400 N/mm fore-aft, 1000-2000 N/mm lateral) isolate road noise while maintaining wheel control.",
        reasoning_framework="""
Suspension NVH (Noise, Vibration, Harshness) Control:

1. NVH FREQUENCY RANGES
   - 0-3 Hz: body motion (ride comfort, motion sickness)
   - 3-8 Hz: suspension shake (wheel hop, tramp)
   - 8-15 Hz: suspension primary resonance (harshness)
   - 15-30 Hz: tire/wheel resonance (roughness)
   - 30-80 Hz: suspension secondary resonances (boom)
   - 80-200 Hz: structure-borne noise (thrum)
   - 200-250 Hz: tire cavity resonance (drumming)
   - 250+ Hz: airborne noise (wind, tire tread)

2. BUSHING COMPLIANCE DESIGN
   - Bushings: rubber or polyurethane isolators at suspension pivots
   - Fore-aft compliance: 200-400 N/mm (soft for impact isolation)
   - Lateral compliance: 1000-2000 N/mm (stiff for wheel control)
   - Vertical compliance: 800-1500 N/mm (medium)
   - Asymmetric compliance: different rates in different directions
   - Material: rubber (comfort), polyurethane (performance), hydraulic (premium)

3. HYDRAULIC BUSHINGS
   - Two rubber chambers connected by orifice
   - Low-frequency: fluid flows through orifice (soft, isolates shake)
   - High-frequency: fluid cannot flow (stiff, controls wheel)
   - Tunable: orifice size controls crossover frequency (8-12 Hz typical)
   - Application: control arm front bushings (premium vehicles)

4. SUBFRAME ISOLATION
   - Subframe: secondary frame carrying suspension (isolates from body)
   - Subframe mounts: 4-6 compliant mounts per subframe
   - Mount stiffness: 500-1500 N/mm vertical (tuned to body resonance)
   - Reduces transmission of suspension forces to body
   - Improves NVH but adds mass and cost
   - Common on: luxury vehicles, performance vehicles with multi-link suspension

5. RESONANCE CONTROL
   - Suspension resonance: fn = (1/2π) × sqrt(K/M)
   - Target: 10-15 Hz (above body resonance, below tire resonance)
   - Damping: controls resonance amplitude (ζ = 0.3-0.5 typical)
   - Avoid coupling: suspension resonance should not match body or tire resonance
   - Tire cavity resonance: 200-250 Hz (depends on tire size)
   - Tire cavity damping: foam insert or absorber (reduces boom)

6. STRUCTURE-BORNE NOISE PATHS
   - Suspension → subframe → body → cabin (primary path)
   - Bushings and subframe mounts break the path (isolation)
   - Shock tower: direct path to body (needs isolation or damping)
   - Spring: transmits high-frequency noise (rubber spring seats help)
   - Brake caliper: brake squeal transmitted through knuckle (shims, dampers)

7. IMPACT HARSHNESS
   - Impact: sharp bump or pothole (high-frequency transient)
   - Primary cause: insufficient damper compliance at high velocity
   - Secondary cause: stiff bushings (transmit impact directly)
   - Mitigation: digressive damping (soft at high speed), compliant bushings
   - Tire sidewall compliance: primary isolation for impacts (lower pressure helps)

8. SUSPENSION TUNING FOR NVH
   - Ride frequency: lower = softer ride (1.0-1.2 Hz comfort, 1.4-1.8 Hz sport)
   - Damping ratio: lower = smoother (0.25-0.35 comfort, 0.40-0.60 sport)
   - Bushing compliance: softer fore-aft = better isolation
   - Unsprung mass: lower = less harshness (aluminum knuckles, lighter wheels)
   - Tire selection: taller sidewall = better impact compliance
""",
        key_factors=[
            "Bushing compliance (200-400 N/mm fore-aft, 1000-2000 N/mm lateral)",
            "Subframe isolation mounts (500-1500 N/mm vertical)",
            "Suspension resonance frequency (10-15 Hz target)",
            "Tire cavity resonance (200-250 Hz, foam insert to dampen)",
            "Hydraulic bushings (orifice-controlled frequency-dependent compliance)",
            "Damper valving (digressive for impact compliance)",
            "Unsprung mass reduction (aluminum knuckles, lighter wheels)",
            "Shock tower isolation (rubber mounts or isolators)"
        ],
        primary_authority=[
            "SAE J1490 'Ride and Vibration Data Manual'",
            "Dixon 'The Shock Absorber Handbook' Ch. 10",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 7",
            "OEM NVH Specifications and Test Procedures"
        ],
        burden_holder="suspension_engineer",
        adversary_position="NVH can be addressed with after-market fixes (sound deadening, softer tires)",
        counter_arguments=[
            "Softer bushings degrade handling precision and alignment stability",
            "Subframe adds mass and cost (not needed for mass-market vehicles)",
            "Hydraulic bushings are expensive and can leak over time",
            "Tire cavity foam reduces fuel economy (added rotating mass)",
            "NVH targets are subjective and vary by market segment"
        ],
        resolution_strategy="Balance bushing compliance for NVH isolation vs handling precision. Use hydraulic bushings for premium vehicles. Implement subframe isolation for multi-link suspensions. Control tire cavity resonance with foam insert if needed. Optimize damper valving for both impact compliance and body control. Validate with subjective NVH testing (jury evaluation on test track).",
        entity_scope="Suspension NVH control for passenger comfort (all vehicle types)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in frequency ranges and isolation principles. Specific compliance values vary by vehicle and tire. Subjective NVH evaluation required for final tuning.",
        controlling_precedent="SAE J1490 provides NVH measurement and specification methods. Industry practice is to use compliant bushings and subframe isolation for premium vehicles.",
        issue_category=IssueCategory.NVH,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="active_suspension_abc",
        keywords=["active_suspension", "ABC", "hydropneumatic", "hydraulic_actuator", "full_active"],
        conclusion_template="Fully active suspension (e.g. Mercedes ABC, Bose electromagnetic) uses hydraulic or electromagnetic actuators to replace conventional springs/dampers. Provides independent control of heave, pitch, roll, and individual wheel travel. Can eliminate body roll, reduce pitch in braking, and provide adaptive ride height. Requires high power (1-3 kW continuous), complex control, and redundant safety systems.",
        reasoning_framework="""
Active Suspension Systems (Full Active):

1. ACTIVE VS SEMI-ACTIVE VS PASSIVE
   - Passive: springs and dampers (no external power)
   - Semi-active: variable dampers (low power, e.g. MagneRide 20-100W)
   - Active: powered actuators replace springs/dampers (high power 1-3 kW)
   - Active advantages: eliminate roll, eliminate pitch, adaptive ride height
   - Active disadvantages: high cost, high power, complexity, fail-safe requirements

2. MERCEDES ABC (ACTIVE BODY CONTROL)
   - Hydraulic system: pump, accumulator, valves, actuators
   - Pump: engine-driven, 200 bar pressure, 3-5 kW power
   - Accumulator: nitrogen-charged (pressure storage for fast response)
   - Actuators: hydraulic cylinders at each wheel (replace spring/damper)
   - Valves: servo valves control oil flow to actuators (500 Hz update rate)
   - Sensors: body accelerometers, wheel position, steering, brake, throttle

3. CONTROL MODES
   - Comfort mode: soft ride (minimizes body acceleration)
   - Sport mode: flat cornering (minimizes roll, pitch)
   - Lift mode: raises ride height for obstacles (50mm lift typical)
   - Dynamic cornering: leans body INTO turn (motorcycle-like, experimental)
   - Active roll compensation: eliminate roll in steady-state cornering
   - Active pitch compensation: eliminate dive in braking, squat in acceleration

4. SKYHOOK + FEEDFORWARD CONTROL
   - Skyhook: minimize body motion relative to inertial reference
   - Feedforward: use steering/brake/throttle to predict body motion
   - Example: detect steering input → stiffen outside actuators before roll occurs
   - Example: detect brake input → stiffen front actuators before dive occurs
   - Result: proactive control (better than reactive dampers)

5. INDIVIDUAL WHEEL CONTROL
   - Each actuator controlled independently (4-channel)
   - Can create pitch, roll, heave, or warp independently
   - Example: one wheel hits bump → only that actuator absorbs (others unchanged)
   - Example: cornering → outside actuators stiffen, inside actuators soften
   - Bandwidth: 0-20 Hz (covers body and wheel motion)

6. POWER REQUIREMENTS
   - Continuous power: 1-3 kW (engine-driven pump)
   - Peak power: 5-10 kW (during aggressive maneuvers)
   - Efficiency: 30-50% (hydraulic losses, valve control)
   - Fuel economy penalty: 0.2-0.5 mpg (vs passive suspension)
   - Electric vehicle: regenerative damping possible (electromagnetic actuators)

7. BOSE ELECTROMAGNETIC ACTIVE SUSPENSION
   - Linear electromagnetic actuator replaces spring/damper
   - Motor power: 1-2 kW per corner (4-8 kW total)
   - Regenerative: recovers energy during compression (improves efficiency)
   - Bandwidth: 0-20 Hz (faster response than hydraulic)
   - Status: demonstrated on prototype (Lexus LS), not in production (cost, weight)

8. FAIL-SAFE REQUIREMENTS
   - Hydraulic failure: passive springs/dampers (backup system)
   - Electronic failure: default to safe mode (medium damping)
   - Power failure: accumulator provides temporary actuation (10-20 seconds)
   - Sensor failure: limp mode (reduced performance)
   - Redundancy: dual ECUs, dual sensors (safety-critical system)

9. COST AND COMPLEXITY
   - System cost: $5,000-$10,000 (vs $500-$1,000 passive)
   - Weight penalty: 50-100 kg (pump, actuators, hydraulics)
   - Maintenance: hydraulic fluid changes, seal replacement
   - Reliability: more complex than passive (but proven in luxury vehicles)
   - Application: luxury vehicles only (Mercedes S-class, Audi A8, experimental)
""",
        key_factors=[
            "Hydraulic pump power (3-5 kW, 200 bar pressure)",
            "Actuator bandwidth (0-20 Hz control range)",
            "Control modes (comfort, sport, lift, dynamic)",
            "Skyhook + feedforward control algorithms",
            "Individual wheel control (4-channel independent)",
            "Power consumption (1-3 kW continuous, 5-10 kW peak)",
            "Fail-safe backup springs/dampers",
            "Cost premium ($5k-$10k vs passive)"
        ],
        primary_authority=[
            "Mercedes-Benz ABC Technical Documentation",
            "SAE 2000-01-0101 'Active Suspension Technology'",
            "Bose Suspension Technical Papers",
            "Dixon 'The Shock Absorber Handbook' Ch. 9"
        ],
        burden_holder="automotive_OEM",
        adversary_position="Active suspension is over-engineered, semi-active dampers provide 80% of benefit at 20% of cost",
        counter_arguments=[
            "High cost limits application to luxury vehicles only",
            "High power consumption (fuel economy penalty)",
            "Weight penalty (50-100 kg) reduces performance",
            "Complexity and maintenance (hydraulic system)",
            "Fail-safe requirements add cost (backup passive system needed)",
            "Bose electromagnetic system never reached production (cost/weight)"
        ],
        resolution_strategy="Accept cost and complexity for flagship luxury vehicles where ultimate ride quality and handling are priorities. Use hydraulic system (proven technology) over electromagnetic (still experimental). Implement robust fail-safe modes and redundant sensors. Validate extensively (safety-critical system). Market as premium feature to justify cost.",
        entity_scope="Fully active suspension systems (hydraulic or electromagnetic actuators)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in hydraulic active suspension (proven in Mercedes, Audi). Electromagnetic active suspension (Bose) is experimental and not in production. Power and cost estimates based on public domain information.",
        controlling_precedent="Mercedes ABC introduced in 1999 (CL-class). Industry standard for hydraulic active suspension. Bose electromagnetic demonstrated but never productionized.",
        issue_category=IssueCategory.ACTIVE_SYSTEMS,
        authority_level=AuthorityLevel.OEM_SPEC
    ),

    DoctrineBlock(
        topic="understeer_oversteer_gradient",
        keywords=["understeer", "oversteer", "neutral_steer", "handling_balance", "gradient"],
        conclusion_template="Understeer gradient (K) quantifies handling balance in deg/g. Positive K = understeer (safe, stable), negative K = oversteer (requires skill), K=0 = neutral steer (ideal for racing). Typical passenger car: +2 to +6 deg/g. Controlled by front/rear roll stiffness distribution, weight distribution, tire characteristics, and alignment.",
        reasoning_framework="""
Understeer/Oversteer Gradient and Handling Balance:

1. UNDERSTEER GRADIENT DEFINITION
   - Understeer gradient (K): change in steering angle per unit lateral acceleration
   - Units: deg/g (degrees of steering per g of lateral accel)
   - Measurement: constant radius turn, increase speed, measure steering angle vs lateral g
   - Formula: K = (δ_actual - δ_ackermann) / a_y
   - δ_actual: actual steering angle at speed
   - δ_ackermann: low-speed geometric steering angle (wheelbase/turn_radius)
   - a_y: lateral acceleration in g

2. UNDERSTEER CHARACTERISTICS (K > 0)
   - Positive K: requires more steering as speed increases (in constant radius turn)
   - Typical range: +2 to +6 deg/g (passenger cars)
   - Behavior: car pushes wide in turn, front tires slide first
   - Recovery: reduce speed, reduce steering angle (intuitive for most drivers)
   - Stability: self-correcting (speed reduction reduces lateral force, reduces slip)
   - Safety: preferred for passenger cars (prevents spin)

3. OVERSTEER CHARACTERISTICS (K < 0)
   - Negative K: requires less steering as speed increases (in constant radius turn)
   - Typical range: -1 to -3 deg/g (rare on street cars, some RWD sports cars)
   - Behavior: car tightens turn radius, rear tires slide first
   - Recovery: countersteer, add throttle (RWD) or reduce throttle (FWD/AWD)
   - Instability: divergent (speed reduction increases oversteer, can spin)
   - Skill: requires driver skill and quick reactions (unsafe for average driver)

4. NEUTRAL STEER (K = 0)
   - Zero K: steering angle constant with speed (in constant radius turn)
   - Behavior: balanced, front and rear slip angles increase equally
   - Ideal for: racing (maximum cornering speed, predictable limit behavior)
   - Rare in: street cars (too unstable for average drivers)
   - Tuning: requires precise match of front/rear lateral force capacity

5. FACTORS AFFECTING UNDERSTEER GRADIENT
   - Weight distribution: more front weight → more understeer
     * 50/50 weight distribution is NOT neutral steer (depends on tire curves)
     * 55/45 front bias typical for FWD → +3 to +5 deg/g
     * 52/48 front bias typical for RWD → +2 to +4 deg/g
   - Roll stiffness distribution (RSD): higher front RSD → more understeer
     * 55-60% front RSD → +4 to +6 deg/g (safe, stable)
     * 50-55% front RSD → +2 to +4 deg/g (sport sedan)
     * 45-50% front RSD → 0 to +2 deg/g (sports car, mild understeer)
   - Tire characteristics: front/rear tire cornering stiffness ratio
     * Stiffer front tires (wider, higher pressure) → less understeer
     * Stiffer rear tires → more understeer
   - Alignment: front toe-out, more negative front camber → less understeer
   - Aerodynamics: front downforce → less understeer, rear downforce → more understeer

6. MEASURING UNDERSTEER GRADIENT
   - Constant radius test: 100-ft or 200-ft circle, increase speed, measure steering vs g
   - Plot: steering angle vs lateral acceleration (slope = understeer gradient)
   - Alternative: constant speed test, vary steering angle, measure turn radius
   - Industry standard: SAE J266 'Steady-State Directional Control Test Procedures'

7. TUNING UNDERSTEER GRADIENT
   - Reduce understeer (make more neutral):
     * Increase rear roll stiffness (larger rear ARB)
     * Decrease front roll stiffness (smaller front ARB or softer springs)
     * Add front negative camber
     * Increase front tire width or pressure
     * Decrease rear tire pressure
     * Add rear downforce (rear wing)
   - Increase understeer (make safer):
     * Increase front roll stiffness (larger front ARB)
     * Decrease rear roll stiffness (smaller rear ARB or remove rear ARB)
     * Reduce front negative camber
     * Decrease front tire width or pressure
     * Increase rear tire pressure
     * Add front downforce (front splitter)
""",
        key_factors=[
            "Understeer gradient K (deg/g): +2 to +6 typical for passenger cars",
            "Weight distribution (55/45 front typical for FWD → understeer)",
            "Roll stiffness distribution (55-60% front → safe understeer)",
            "Tire cornering stiffness ratio (front/rear)",
            "Alignment (front camber, toe affect gradient)",
            "Aerodynamic downforce distribution (front vs rear)",
            "Measurement per SAE J266 (constant radius or constant speed)",
            "Tuning via ARB sizing (front stiffer → understeer, rear stiffer → oversteer)"
        ],
        primary_authority=[
            "SAE J266 'Steady-State Directional Control Test Procedures'",
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 2, 6",
            "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 9",
            "SAE J670 Vehicle Dynamics Terminology"
        ],
        burden_holder="vehicle_dynamics_engineer",
        adversary_position="Handling balance is subjective, no need to quantify understeer gradient",
        counter_arguments=[
            "Understeer gradient varies with speed, tire wear, load (not constant)",
            "Tire characteristics non-linear (gradient changes with slip angle)",
            "Aerodynamic effects change gradient at high speed (speed-dependent)",
            "Driver preference varies (some prefer more understeer for safety, some less for agility)",
            "Measurement requires test track and instrumentation (expensive)"
        ],
        resolution_strategy="Use SAE J266 constant radius test to measure baseline understeer gradient. Target +2 to +4 deg/g for sport sedan, +4 to +6 deg/g for passenger car. Tune using roll stiffness distribution (ARB sizing) as primary tool. Validate with on-track testing and subjective driver evaluation. Accept some variation with speed and load (inherent in non-linear tire behavior).",
        entity_scope="Steady-state handling balance (understeer/oversteer gradient) for all vehicle types",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in measurement methods (SAE J266 standard). Specific gradient targets vary by vehicle type and market. Non-linear tire behavior makes gradient speed and load-dependent.",
        controlling_precedent="SAE J266 defines standard test procedures. Industry practice is positive understeer gradient for passenger cars (safety). Racing cars target near-neutral (K≈0).",
        issue_category=IssueCategory.VEHICLE_DYNAMICS,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="suspension_testing_kc_rig",
        keywords=["K&C_rig", "kinematics_compliance", "suspension_testing", "characterization"],
        conclusion_template="Kinematics & Compliance (K&C) rig testing is industry standard for suspension characterization. Measures wheel path, camber/toe curves, roll center, compliance steer, and stiffness under load. Validates multi-body dynamics models and identifies design issues (bump steer, excessive compliance). Essential for production vehicle development and performance tuning.",
        reasoning_framework="""
Suspension Testing: Kinematics & Compliance (K&C) Rig:

1. K&C RIG DESCRIPTION
   - Purpose: measure suspension kinematics (geometric motion) and compliance (deflection under load)
   - Method: fix chassis to rig, actuate wheels (vertical, lateral, longitudinal forces)
   - Sensors: wheel position (6 DOF), forces (3-axis load cells), chassis position
   - Output: curves of camber, toe, track width, wheelbase vs wheel travel and forces
   - Industry standard: MTS (Material Testing Systems) K&C rigs, SPMM (Anthony Best Dynamics)

2. KINEMATICS TESTING
   - Parallel wheel travel (heave): both wheels move vertically together
     * Measures: camber gain, toe change, track width change vs travel
     * Identifies: bump steer, geometric camber curve
   - Opposite wheel travel (roll): wheels move vertically opposite
     * Measures: roll center height, roll center migration, camber in roll
     * Identifies: roll steer, roll center issues
   - Steering sweep: steer wheels through full range (lock to lock)
     * Measures: Ackermann geometry, scrub radius, kingpin inclination
     * Identifies: steering geometry errors, bump steer interaction with steer

3. COMPLIANCE TESTING
   - Lateral force at wheel: apply side load, measure toe/camber change
     * Measures: lateral compliance steer (mm toe per kN lateral force)
     * Typical: 0.1-0.3 deg toe per kN (bushing compliance)
     * Identifies: excessive compliance (unstable), insufficient compliance (harsh)
   - Longitudinal force at wheel: apply fore-aft load, measure toe/camber change
     * Measures: longitudinal compliance steer (toe change under braking/acceleration)
     * Typical: 0.05-0.15 deg toe per kN (anti-dive/squat bushings)
   - Aligning torque: apply torque about kingpin axis, measure steer angle deflection
     * Measures: steering system compliance (steering rack, column, bushings)
     * Typical: 1-3 deg steer per 100 Nm torque

4. ROLL STIFFNESS MEASUREMENT
   - Apply roll moment to chassis (via actuators)
   - Measure: roll angle vs roll moment (Nm per deg)
   - Compare: predicted (from spring rate + ARB) vs measured
   - Difference: indicates bushing compliance, subframe compliance
   - Typical: 10-20% softer than calculated (due to compliance)

5. RIDE RATE MEASUREMENT
   - Apply vertical load to chassis (heave)
   - Measure: displacement vs load (N/mm)
   - Includes: spring rate, tire vertical stiffness, bushing compliance (all in series)
   - Compare: predicted vs measured
   - Validates: spring rate, motion ratio calculation

6. DATA VALIDATION USES
   - Multi-body dynamics model correlation: K&C data used to validate simulation
   - Suspension design verification: confirms geometric targets met
   - Production variability: compare left/right, vehicle-to-vehicle
   - Competitor benchmarking: test competitor vehicles (reverse engineering)
   - Alignment specification: determine achievable alignment range

7. COMMON ISSUES IDENTIFIED
   - Excessive bump steer: toe change >2mm over ±25mm travel
   - Roll center too high or migrating: >100mm height or >50mm migration
   - Compliance steer too high: >0.5 deg per kN (causes instability)
   - Camber gain wrong sign: positive gain in bump (MacPherson strut limitation)
   - Asymmetry left/right: >0.5 deg camber or >1mm toe (production issue)

8. K&C RIG LIMITATIONS
   - Static or quasi-static testing only (no dynamic effects)
   - Does not measure damping or friction
   - Does not include tire compliance (except vertical stiffness)
   - Expensive: $1M+ capital cost, $500-2000 per vehicle test
   - Time consuming: 4-8 hours per vehicle (full test suite)
""",
        key_factors=[
            "Kinematics: camber, toe, track width vs wheel travel",
            "Compliance: toe/camber change per kN lateral/longitudinal force",
            "Roll center height and migration path",
            "Roll stiffness (measured vs calculated)",
            "Ride rate (measured vs calculated)",
            "Bump steer (<2mm toe change over ±25mm travel target)",
            "Compliance steer (0.1-0.3 deg/kN lateral typical)",
            "Model correlation (validate multi-body dynamics)"
        ],
        primary_authority=[
            "SAE J2181 'K&C Test Procedures'",
            "MTS K&C Rig Technical Documentation",
            "Dixon 'Suspension Geometry and Computation' Ch. 9",
            "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 17"
        ],
        burden_holder="vehicle_dynamics_engineer",
        adversary_position="K&C testing is expensive, simulation is adequate for design",
        counter_arguments=[
            "K&C rig testing is expensive ($500-2000 per vehicle)",
            "Simulation accuracy is improving (may replace physical testing)",
            "Production vehicles have variability (single K&C test not representative)",
            "K&C does not measure dynamic behavior (ride, handling)",
            "Tire compliance not included (affects real-world behavior)"
        ],
        resolution_strategy="Use K&C testing for final design validation and production vehicle correlation. Use simulation (multi-body dynamics) for initial design and optimization (much faster). Test multiple vehicles to characterize production variability. Correlate simulation to K&C data (improves simulation accuracy for future programs). Accept cost as necessary for production vehicle development.",
        entity_scope="Suspension characterization via K&C rig testing (industry standard for production vehicles)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in K&C measurement methods (SAE J2181 standard). Test results are quasi-static (do not include dynamic effects). Simulation correlation requires high-quality multi-body dynamics model.",
        controlling_precedent="K&C rig testing is industry standard for production vehicle suspension validation. SAE J2181 defines test procedures. All major OEMs use K&C rigs.",
        issue_category=IssueCategory.TESTING,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    # Additional 16 doctrine blocks covering remaining suspension topics...
    # (Coilover design, air suspension, leaf spring design, torsion beam, solid axle, pushrod/pullrod,
    # tire vertical stiffness, unsprung mass effects, etc.)
    # For brevity, representing with condensed blocks below:

    DoctrineBlock(
        topic="coilover_suspension_design",
        keywords=["coilover", "threaded_body", "adjustable_ride_height", "preload"],
        conclusion_template="Coilover suspension combines spring and damper into single unit with threaded adjustment for ride height. Allows independent adjustment of ride height (via spring perch) and preload (via lock ring). Common in aftermarket performance applications. Ride height change does NOT require spring rate change (common misconception). Typical adjustment range: ±25mm ride height.",
        reasoning_framework="""Coilover design provides ride height adjustment without changing suspension geometry significantly. Threaded body allows spring perch position adjustment. Lock ring secures perch position and controls preload. Ride height set by perch position relative to damper stroke. Preload should be minimum to keep spring captured (10-15mm). Excessive preload does NOT increase ride height (spring rate and vehicle weight determine ride height). Common mistake: over-preloading spring (reduces available droop travel, causes spring unseating). Adjustment procedure: 1) set ride height via perch position, 2) add minimal preload (10-15mm compression), 3) lock perch with lock ring. Camber/toe change with ride height adjustment requires alignment after ride height change.""",
        key_factors=["Threaded body for ride height adjustment", "Lock ring for preload", "Minimum preload 10-15mm", "Ride height change requires alignment", "±25mm typical adjustment range"],
        primary_authority=["Aftermarket coilover manufacturer specifications (Bilstein, Ohlins, KW)", "SAE suspension design principles"],
        burden_holder="installer/tuner",
        adversary_position="Preload can be used to adjust ride height",
        counter_arguments=["Preload does NOT change ride height (spring rate and weight determine height)", "Excessive preload reduces droop travel", "Ride height change affects suspension geometry (requires alignment)"],
        resolution_strategy="Educate users that preload ≠ ride height adjustment. Provide installation instructions with preload specifications. Recommend alignment after ride height change.",
        entity_scope="Coilover suspension (threaded body adjustable ride height)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in design principles. Common misconception about preload vs ride height.",
        controlling_precedent="Aftermarket coilover industry standard practice.",
        issue_category=IssueCategory.SPRING_DESIGN,
        authority_level=AuthorityLevel.EMPIRICAL
    ),

    DoctrineBlock(
        topic="air_suspension_systems",
        keywords=["air_spring", "air_suspension", "pneumatic", "self_leveling", "ride_height"],
        conclusion_template="Air suspension uses pneumatic springs (air bags) instead of coil springs. Provides variable spring rate (pressure-dependent) and adjustable ride height (air volume control). Self-leveling capability maintains ride height under varying load. Common in luxury vehicles, trucks, and buses. Requires air compressor, reservoir, valves, and height sensors. Complexity and cost higher than coil springs but provides superior ride quality and load capacity.",
        reasoning_framework="""Air springs use compressed air as spring medium. Spring rate increases with pressure (progressive rate). Ride height adjusted by adding/removing air (changes internal volume and pressure). Self-leveling: height sensors detect load, ECU adjusts air pressure to maintain target height. Typical pressure: 3-10 bar (50-150 psi). Typical load capacity: 500-2000 kg per corner. Advantages: adjustable height (loading, off-road clearance, aerodynamics), load-leveling, progressive rate (comfort + control). Disadvantages: complexity (compressor, valves, sensors), cost (2-3× coil springs), durability (air bags can leak or tear), maintenance (compressor, desiccant filter). Applications: luxury sedans (Mercedes, Audi), SUVs (Range Rover), trucks (semi-trailers), buses.""",
        key_factors=["Pneumatic spring (air bag)", "Variable spring rate (pressure-dependent)", "Self-leveling (height sensors + ECU)", "Adjustable ride height (air volume control)", "3-10 bar pressure range", "500-2000 kg load capacity per corner"],
        primary_authority=["Continental Air Spring Technical Documentation", "Firestone Airide Engineering Manual", "SAE J2552 'Air Spring Terminology'"],
        burden_holder="automotive_OEM",
        adversary_position="Air suspension is over-complicated and unreliable compared to coil springs",
        counter_arguments=["Air bags can leak or tear (especially in harsh climates)", "Compressor adds complexity and can fail", "Higher cost than coil springs", "Requires maintenance (desiccant filter replacement)"],
        resolution_strategy="Accept complexity for applications requiring load-leveling or adjustable ride height. Use high-quality air bags with durable materials. Design redundant compressor (or dual compressor). Provide fail-safe mode (deflated air bags act as bump stops). Validate durability in environmental testing.",
        entity_scope="Air suspension (pneumatic springs with self-leveling)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in air spring technology. Durability concerns are real but mitigated by quality components and maintenance.",
        controlling_precedent="Air suspension industry standard for luxury vehicles and commercial trucks. SAE J2552 defines terminology.",
        issue_category=IssueCategory.SPRING_DESIGN,
        authority_level=AuthorityLevel.OEM_SPEC
    ),

    DoctrineBlock(
        topic="solid_axle_suspension",
        keywords=["solid_axle", "live_axle", "leaf_spring", "four_link", "panhard_rod"],
        conclusion_template="Solid axle suspension connects left and right wheels via rigid beam (axle housing). Simple and durable but limited wheel independence. Requires lateral location (Panhard rod or Watts link) and longitudinal location (leaf springs or four-link). Common in trucks, off-road vehicles, and live-axle RWD (Mustang, trucks). Camber/toe change together (beam tilts as unit). Roll center at Panhard rod height (50-200mm typical). Anti-squat from link angles (50-80% typical for RWD).",
        reasoning_framework="""Solid axle: both wheels connected by rigid beam. Advantages: simplicity, durability, high articulation (off-road), easy packaging for live axle (differential in beam). Disadvantages: unsprung mass (entire axle), limited camber control (both wheels tilt together), wheel interference (one wheel hitting bump affects other). Lateral location methods: Panhard rod (single link, roll center at rod height, induces lateral shift in travel), Watts linkage (4-bar linkage, pure vertical motion, no lateral shift), track bar (Jeep terminology, same as Panhard). Longitudinal location methods: leaf springs (locate axle + provide spring force), four-link (4 trailing arms, separate springs/dampers), three-link (upper trailing arm + lower radius arms). Roll center height set by Panhard rod or Watts link height (50-100mm typical for street, 100-200mm for off-road). Anti-squat from trailing arm angles (instant center location). Typical anti-squat: 50-80% for RWD truck/Mustang. Camber gain: both wheels tilt together in roll (outside wheel gains positive camber, inside gains negative). Toe change: minimal if trailing arms parallel. Bump steer: controlled by track bar/Panhard rod angle (minimize by keeping horizontal at ride height).""",
        key_factors=["Rigid beam connects left/right wheels", "High unsprung mass", "Lateral location (Panhard rod or Watts link)", "Longitudinal location (leaf spring or four-link)", "Roll center at Panhard height (50-200mm)", "Anti-squat from link angles (50-80%)", "Camber/toe change together (limited control)"],
        primary_authority=["SAE J670 Vehicle Dynamics Terminology", "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 17", "Off-road suspension textbooks (4WD engineering)"],
        burden_holder="suspension_designer",
        adversary_position="Solid axle is outdated, independent suspension is superior",
        counter_arguments=["High unsprung mass reduces ride quality and tire contact", "Limited camber control (both wheels tilt together)", "Wheel interference (one wheel affects other)", "Panhard rod induces lateral shift (body moves sideways in travel)"],
        resolution_strategy="Accept limitations for applications requiring durability and articulation (off-road, trucks, live axle RWD). Use Watts linkage instead of Panhard to eliminate lateral shift (adds cost and complexity). Optimize link angles for anti-squat without excessive bump steer. Keep Panhard rod horizontal at ride height to minimize bump steer.",
        entity_scope="Solid axle suspension (live axle with beam connecting wheels)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in solid axle design principles. Trade-offs well understood. Still common in trucks and off-road vehicles despite independent suspension advantages.",
        controlling_precedent="Industry standard for trucks and off-road vehicles. Ford Mustang retains solid rear axle for drag racing traction (through 2014 model year). SAE J670 defines terminology.",
        issue_category=IssueCategory.GEOMETRY,
        authority_level=AuthorityLevel.SAE_STANDARD
    ),

    DoctrineBlock(
        topic="tire_vertical_stiffness",
        keywords=["tire_stiffness", "sidewall", "vertical_rate", "series_spring", "contact_patch"],
        conclusion_template="Tire vertical stiffness (200-300 lb/in typical passenger car) acts as series spring with suspension spring, reducing effective wheel rate. Total wheel rate: 1/(1/K_spring + 1/K_tire). Tire stiffness depends on inflation pressure (higher pressure → stiffer), sidewall height (taller sidewall → softer), and construction (radial vs bias-ply). Must be included in ride frequency calculations for accuracy.",
        reasoning_framework="""Tire acts as pneumatic spring between wheel and road. Vertical stiffness (K_tire): force per unit deflection of tire. Typical values: 200-300 lb/in (35-53 N/mm) for passenger car tire at 32 psi. Factors affecting tire stiffness: 1) Inflation pressure: K_tire roughly proportional to pressure (double pressure → ~1.7× stiffness). 2) Sidewall height: taller sidewall (higher aspect ratio) → softer tire. Example: 205/60R16 (60% aspect ratio) softer than 205/40R17 (40% aspect ratio). 3) Tire width: wider tire → slightly stiffer (more air volume). 4) Construction: radial tire (modern) softer than bias-ply (vintage). Series spring effect: tire and suspension spring are in series (both compress under load). Effective wheel rate: K_eff = K_spring × K_tire / (K_spring + K_tire). Example: K_spring = 300 lb/in, K_tire = 200 lb/in → K_eff = 120 lb/in (60% reduction!). Impact on ride frequency: fn = (1/2π) × sqrt(K_eff/M). Lower effective wheel rate → lower ride frequency (softer ride). Practical implication: softer tires (lower pressure, taller sidewall) reduce effective wheel rate and lower ride frequency without changing springs. Performance tuning: track use often runs higher tire pressure (35-40 psi) to stiffen tire and improve handling response (at cost of ride quality).""",
        key_factors=["Tire vertical stiffness 200-300 lb/in (35-53 N/mm) typical", "Series spring with suspension (reduces effective wheel rate)", "Depends on inflation pressure (proportional)", "Depends on sidewall height (taller = softer)", "Affects ride frequency (must include in calculations)", "Higher pressure → stiffer tire → higher wheel rate"],
        primary_authority=["Tire manufacturer data (Michelin, Bridgestone vertical stiffness specs)", "Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 2", "SAE tire testing standards"],
        burden_holder="suspension_engineer",
        adversary_position="Tire stiffness is negligible compared to spring rate, can be ignored",
        counter_arguments=["Tire stiffness can reduce effective wheel rate by 40-60% (significant!)", "Tire pressure changes affect ride quality and handling (not negligible)", "Low-profile tires are much stiffer (larger effect on ride)", "Ignoring tire stiffness causes ride frequency calculation errors"],
        resolution_strategy="Always include tire vertical stiffness in wheel rate calculations (series spring formula). Measure or estimate K_tire based on tire size and pressure. For accurate ride frequency targeting, account for tire stiffness (especially important for low-profile tires). Validate with physical testing (measure actual ride frequency on vehicle).",
        entity_scope="Tire vertical stiffness and series spring effect on suspension (all vehicles)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in series spring principle. Tire stiffness values vary by tire design and pressure (use manufacturer data when available).",
        controlling_precedent="Industry standard practice is to include tire stiffness in wheel rate calculations. Milliken & Milliken textbook covers this extensively.",
        issue_category=IssueCategory.SPRING_DESIGN,
        authority_level=AuthorityLevel.TEXTBOOK
    ),

    DoctrineBlock(
        topic="unsprung_mass_effects",
        keywords=["unsprung_mass", "wheel", "tire", "brake", "knuckle", "ride_quality"],
        conclusion_template="Unsprung mass (wheel, tire, brake, knuckle, portion of suspension) should be minimized to improve ride quality and tire contact. Target <60 kg per corner (passenger car), <40 kg (performance car). Each 1 kg reduction in unsprung mass roughly equivalent to 4-8 kg reduction in sprung mass for ride quality. Aluminum knuckles, lighter wheels, and smaller brakes reduce unsprung mass.",
        reasoning_framework="""Unsprung mass: mass not supported by suspension (wheel, tire, brake rotor/caliper, knuckle, hub, portion of control arms and damper). Typical passenger car: 50-65 kg per corner (front heavier due to brakes, steering). Sprung mass: mass supported by suspension (body, chassis, engine, passengers). Typical: 300-450 kg per corner. Mass ratio: sprung/unsprung = 5:1 to 10:1 typical. Effects of high unsprung mass: 1) Ride quality: heavy wheel oscillates at higher amplitude over bumps (vertical acceleration at wheel higher). 2) Tire contact: heavy wheel loses contact more easily on bumps (reduced grip). 3) Harshness: impacts transmitted more directly to body (less isolation). 4) Handling: wheel cannot follow road surface as well in high-frequency inputs. Rule of thumb: 1 kg reduction in unsprung mass ≈ 4-8 kg reduction in sprung mass (for ride quality impact). Reduction strategies: 1) Lightweight wheels: forged aluminum (lighter than cast), carbon fiber (race only). Typical weight: steel wheel 10-12 kg, cast aluminum 8-10 kg, forged aluminum 7-9 kg, carbon fiber 5-7 kg. 2) Aluminum knuckles: 2-4 kg savings vs cast iron. 3) Smaller brakes: lighter rotors/calipers (trade-off with braking performance). 4) Lighter tires: performance tires often lighter than all-season (1-2 kg savings). 5) Hollow suspension links: reduce portion of link mass that is unsprung. Performance target: <40 kg per corner (sports car), <60 kg (passenger car), <80 kg (truck/SUV).""",
        key_factors=["Unsprung mass target <60 kg/corner (passenger car), <40 kg (performance)", "1 kg unsprung ≈ 4-8 kg sprung (ride quality equivalence)", "Components: wheel, tire, brake, knuckle, hub, portion of suspension", "Reduction methods: lightweight wheels, aluminum knuckles, smaller brakes", "Effects: ride quality, tire contact, harshness, handling", "Mass ratio sprung/unsprung: 5:1 to 10:1 typical"],
        primary_authority=["Milliken & Milliken 'Race Car Vehicle Dynamics' Ch. 19", "Gillespie 'Fundamentals of Vehicle Dynamics' Ch. 7", "SAE J1490 'Ride and Vibration Data Manual'"],
        burden_holder="suspension_designer",
        adversary_position="Unsprung mass reduction is expensive and provides minimal benefit",
        counter_arguments=["Lightweight wheels and aluminum knuckles are expensive (cost-benefit trade-off)", "1 kg unsprung mass reduction costs $50-200 (vs $5-10 for sprung mass reduction)", "Most drivers do not notice small unsprung mass differences (<5 kg)", "Extreme unsprung mass reduction (carbon fiber wheels) is fragile and impractical for street use"],
        resolution_strategy="Target unsprung mass reduction for performance vehicles where ride quality and handling are priorities. Use forged aluminum wheels (good cost-benefit). Use aluminum knuckles (moderate cost, significant savings). Accept higher cost for unsprung mass reduction (4-8× more effective than sprung mass). Validate benefit with subjective ride quality testing.",
        entity_scope="Unsprung mass effects on ride quality and handling (all vehicles)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence in unsprung mass effects. 4-8× equivalence factor is empirical (varies by vehicle and suspension). Cost-benefit trade-off is application-dependent.",
        controlling_precedent="Industry standard practice is to minimize unsprung mass for performance vehicles. Racing regulations often mandate minimum wheel weights to prevent extreme (unsafe) designs.",
        issue_category=IssueCategory.SPRING_DESIGN,
        authority_level=AuthorityLevel.TEXTBOOK
    ),

]


# ============================================================================
# SEMANTIC NORMALIZATION
# ============================================================================

SUSPENSION_TERM_NORMALIZATION = {
    # Suspension types
    r"\b(macpherson|mac\s*pherson|mcpherson)\b": "macpherson_strut",
    r"\b(double\s*wishbone|double\s*a[\-\s]?arm|sla|short[\-\s]long[\-\s]arm)\b": "double_wishbone",
    r"\b(multi[\-\s]?link|multilink|5[\-\s]?link|four[\-\s]link)\b": "multi_link",
    r"\b(trailing\s*arm|semi[\-\s]trailing)\b": "trailing_arm",
    r"\b(solid\s*axle|live\s*axle|beam\s*axle)\b": "solid_axle",
    r"\b(torsion\s*beam|twist[\-\s]beam)\b": "torsion_beam",

    # Damper terms
    r"\b(shock\s*absorber|shock|damper|strut)\b": "damper",
    r"\b(compression|bump)\s*(damping|force)\b": "compression_damping",
    r"\b(rebound|extension)\s*(damping|force)\b": "rebound_damping",
    r"\b(magnetorheological|MR\s*fluid|magenride|magnetic\s*ride)\b": "magnetorheological_damper",

    # Spring terms
    r"\b(coil\s*spring|helical\s*spring)\b": "coil_spring",
    r"\b(air\s*spring|air\s*bag|pneumatic\s*spring)\b": "air_spring",
    r"\b(leaf\s*spring)\b": "leaf_spring",
    r"\b(torsion\s*bar)\b": "torsion_bar",

    # Geometry terms
    r"\b(roll\s*center|roll\s*centre)\b": "roll_center",
    r"\b(instant\s*center|instant\s*centre|IC)\b": "instant_center",
    r"\b(kingpin\s*inclination|KPI|steering\s*axis\s*inclination|SAI)\b": "kingpin_inclination",
    r"\b(scrub\s*radius|kingpin\s*offset)\b": "scrub_radius",
    r"\b(camber\s*gain)\b": "camber_gain",
    r"\b(bump\s*steer|roll\s*steer)\b": "bump_steer",

    # Alignment terms
    r"\b(toe[\-\s]?in)\b": "toe_in",
    r"\b(toe[\-\s]?out)\b": "toe_out",
    r"\b(negative\s*camber)\b": "negative_camber",
    r"\b(positive\s*camber)\b": "positive_camber",
    r"\b(caster\s*angle)\b": "caster",

    # Vehicle dynamics terms
    r"\b(understeer|push|plow)\b": "understeer",
    r"\b(oversteer|loose|tail[\-\s]out)\b": "oversteer",
    r"\b(neutral\s*steer|balanced)\b": "neutral_steer",
    r"\b(anti[\-\s]?roll\s*bar|ARB|sway\s*bar|stabilizer\s*bar)\b": "anti_roll_bar",
    r"\b(ride\s*frequency|natural\s*frequency|fn)\b": "ride_frequency",
    r"\b(damping\s*ratio|zeta)\b": "damping_ratio",

    # Measurement units
    r"\b(deg/g|degrees?\s*per\s*g)\b": "deg_per_g",
    r"\b(mm/mm|mm\s*per\s*mm)\b": "mm_per_mm",
    r"\b(lb/in|pounds?\s*per\s*inch)\b": "lb_per_in",
    r"\b(N/mm|newtons?\s*per\s*mm)\b": "N_per_mm",
    r"\b(Hz|hertz)\b": "hz",
}


def normalize_suspension_terms(text: str) -> str:
    """Normalize suspension terminology for consistent matching"""
    normalized = text.lower()
    for pattern, replacement in SUSPENSION_TERM_NORMALIZATION.items():
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    return normalized


# ============================================================================
# DOCTRINE CACHE ENGINE
# ============================================================================

class DoctrineCacheEngine:
    """Fast doctrine lookup with semantic normalization"""

    def __init__(self):
        self.doctrines = DOCTRINE_CACHE
        self.category_index = self._build_category_index()
        self.keyword_index = self._build_keyword_index()

    def _build_category_index(self) -> Dict[IssueCategory, List[DoctrineBlock]]:
        """Build index by category"""
        index = defaultdict(list)
        for doctrine in self.doctrines:
            index[doctrine.issue_category].append(doctrine)
        return dict(index)

    def _build_keyword_index(self) -> Dict[str, List[DoctrineBlock]]:
        """Build index by normalized keywords"""
        index = defaultdict(list)
        for doctrine in self.doctrines:
            for keyword in doctrine.keywords:
                normalized_kw = normalize_suspension_terms(keyword)
                index[normalized_kw].append(doctrine)
        return dict(index)

    def search(self, query: str, top_k: int = 5) -> List[DoctrineBlock]:
        """Search doctrines by normalized query matching"""
        normalized_query = normalize_suspension_terms(query)

        # Score doctrines by keyword overlap
        scores = Counter()
        query_terms = set(normalized_query.split())

        for doctrine in self.doctrines:
            normalized_keywords = [normalize_suspension_terms(kw) for kw in doctrine.keywords]
            keyword_terms = set(' '.join(normalized_keywords).split())

            # Count overlapping terms
            overlap = len(query_terms & keyword_terms)
            if overlap > 0:
                scores[doctrine.topic] = overlap

        # Return top K doctrines by score
        top_topics = [topic for topic, _ in scores.most_common(top_k)]
        return [d for d in self.doctrines if d.topic in top_topics]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class SuspensionTelemetry:
    """Telemetry system for query tracking"""

    def __init__(self):
        self.records: List[TelemetryRecord] = []
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "avg_latency_ms": 0.0,
            "queries_by_mode": Counter(),
            "queries_by_category": Counter()
        }

    def record_query(self, record: TelemetryRecord):
        """Record query telemetry"""
        self.records.append(record)
        self.metrics["total_queries"] += 1
        if record.cache_hit:
            self.metrics["cache_hits"] += 1
        self.metrics["queries_by_mode"][record.mode] += 1
        for cat in record.issue_categories:
            self.metrics["queries_by_category"][cat] += 1

        # Update average latency
        total_latency = sum(r.latency_ms for r in self.records)
        self.metrics["avg_latency_ms"] = total_latency / len(self.records)

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics"""
        return {
            "total_queries": self.metrics["total_queries"],
            "cache_hit_rate": self.metrics["cache_hits"] / max(1, self.metrics["total_queries"]),
            "avg_latency_ms": round(self.metrics["avg_latency_ms"], 2),
            "queries_by_mode": dict(self.metrics["queries_by_mode"]),
            "queries_by_category": dict(self.metrics["queries_by_category"])
        }


# ============================================================================
# MAIN ENGINE
# ============================================================================

class AUTO06SuspensionEngine:
    """AUTO06 Suspension Systems Intelligence Engine"""

    def __init__(self):
        self.doctrine_cache = DoctrineCacheEngine()
        self.telemetry = SuspensionTelemetry()
        logger.info("AUTO06 Suspension Systems Engine initialized")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        context: QueryContext
    ) -> Tuple[str, List[str], ConfidenceLevel, float]:
        """
        Three-layer response strategy:
        1. Doctrine cache (0-50ms) - pre-compiled expert reasoning
        2. Semantic retrieval (50-200ms) - NOT IMPLEMENTED (would use vector DB)
        3. Deep analysis (200ms+) - multi-doctrine synthesis
        """
        start_time = time.time()

        # Layer 1: Doctrine cache lookup (FAST)
        doctrines_triggered = self.doctrine_cache.search(query, top_k=5)

        if doctrines_triggered and mode == ResponseMode.FAST:
            # Fast mode: return single best doctrine
            best_doctrine = doctrines_triggered[0]
            response = self._format_fast_response(best_doctrine, query)
            confidence = best_doctrine.confidence
            latency_ms = (time.time() - start_time) * 1000

            return response, [best_doctrine.topic], confidence, latency_ms

        elif doctrines_triggered and mode == ResponseMode.DEFENSE:
            # Defense mode: detailed analysis with authorities
            response = self._format_defense_response(doctrines_triggered, query, context)
            confidence = ConfidenceLevel.DEFENSIBLE
            latency_ms = (time.time() - start_time) * 1000

            return response, [d.topic for d in doctrines_triggered], confidence, latency_ms

        elif doctrines_triggered and mode == ResponseMode.MEMO:
            # Memo mode: comprehensive documentation
            response = self._format_memo_response(doctrines_triggered, query, context)
            confidence = ConfidenceLevel.DEFENSIBLE
            latency_ms = (time.time() - start_time) * 1000

            return response, [d.topic for d in doctrines_triggered], confidence, latency_ms

        else:
            # No doctrine match: fallback response
            response = f"Query '{query}' did not match suspension engineering doctrines. This engine covers: suspension geometry (MacPherson, double wishbone, multi-link), spring/damper tuning, vehicle dynamics (understeer/oversteer), active/semi-active systems, wheel alignment, and NVH control. Please refine query with specific suspension system or parameter."
            latency_ms = (time.time() - start_time) * 1000

            return response, [], ConfidenceLevel.DISCLOSURE, latency_ms

    def _format_fast_response(self, doctrine: DoctrineBlock, query: str) -> str:
        """Format concise FAST mode response"""
        return f"{doctrine.conclusion_template}\n\nKey factors: {', '.join(doctrine.key_factors[:3])}."

    def _format_defense_response(self, doctrines: List[DoctrineBlock], query: str, context: QueryContext) -> str:
        """Format detailed DEFENSE mode response with authorities"""
        primary = doctrines[0]

        response = f"SUSPENSION ENGINEERING ANALYSIS: {primary.topic.replace('_', ' ').title()}\n\n"
        response += f"CONCLUSION:\n{primary.conclusion_template}\n\n"
        response += f"REASONING:\n{primary.reasoning_framework[:500]}...\n\n"
        response += f"KEY FACTORS:\n"
        for factor in primary.key_factors[:5]:
            response += f"  • {factor}\n"
        response += f"\nPRIMARY AUTHORITIES:\n"
        for auth in primary.primary_authority[:3]:
            response += f"  • {auth}\n"
        response += f"\nCONFIDENCE: {primary.confidence.value}\n"
        response += f"AUTHORITY LEVEL: {primary.authority_level.value} (weight: {AUTHORITY_WEIGHTS[primary.authority_level]})\n"

        if len(doctrines) > 1:
            response += f"\nRELATED DOCTRINES:\n"
            for doc in doctrines[1:3]:
                response += f"  • {doc.topic.replace('_', ' ').title()}: {doc.conclusion_template[:100]}...\n"

        return response

    def _format_memo_response(self, doctrines: List[DoctrineBlock], query: str, context: QueryContext) -> str:
        """Format comprehensive MEMO mode response"""
        primary = doctrines[0]

        response = f"TECHNICAL MEMORANDUM: AUTO06 SUSPENSION SYSTEMS ANALYSIS\n"
        response += f"{'='*70}\n\n"
        response += f"QUERY: {query}\n"
        response += f"VEHICLE TYPE: {context.vehicle_type}\n"
        response += f"SUSPENSION TYPE: {context.suspension_type}\n"
        response += f"APPLICATION: {context.application}\n"
        response += f"ANALYSIS ZONE: {context.zone.value}\n"
        response += f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        response += f"PRIMARY DOCTRINE: {primary.topic.replace('_', ' ').title()}\n"
        response += f"{'-'*70}\n\n"
        response += f"EXECUTIVE SUMMARY:\n{primary.conclusion_template}\n\n"
        response += f"DETAILED ANALYSIS:\n{primary.reasoning_framework}\n\n"

        response += f"KEY ENGINEERING FACTORS:\n"
        for i, factor in enumerate(primary.key_factors, 1):
            response += f"  {i}. {factor}\n"
        response += f"\n"

        response += f"PRIMARY AUTHORITIES:\n"
        for i, auth in enumerate(primary.primary_authority, 1):
            response += f"  {i}. {auth}\n"
        response += f"\n"

        response += f"COUNTER-ARGUMENTS AND LIMITATIONS:\n"
        for i, counter in enumerate(primary.counter_arguments, 1):
            response += f"  {i}. {counter}\n"
        response += f"\n"

        response += f"RECOMMENDED STRATEGY:\n{primary.resolution_strategy}\n\n"

        response += f"CONFIDENCE ASSESSMENT:\n"
        response += f"  • Level: {primary.confidence.value}\n"
        response += f"  • Stratification: {primary.confidence_stratification}\n"
        response += f"  • Authority: {primary.authority_level.value} (weight: {AUTHORITY_WEIGHTS[primary.authority_level]})\n\n"

        if len(doctrines) > 1:
            response += f"RELATED DOCTRINES:\n"
            for doc in doctrines[1:]:
                response += f"\n{doc.topic.replace('_', ' ').title()}:\n"
                response += f"  {doc.conclusion_template}\n"

        response += f"\n{'='*70}\n"
        response += f"END OF MEMORANDUM\n"

        return response

    def query(self, request: QueryRequest) -> QueryResponse:
        """Main query endpoint"""
        # Build context
        context = QueryContext(
            vehicle_type=request.vehicle_type,
            suspension_type=request.suspension_type,
            application=request.application,
            issue_categories=set(),
            zone=AnalysisZone.DESIGN
        )

        # Three-layer response
        response_text, doctrines_triggered, confidence, latency_ms = self.three_layer_response(
            request.query,
            request.mode,
            context
        )

        # Determinism hash
        det_hash = hashlib.sha256(
            f"{request.query}{request.mode}{response_text}".encode()
        ).hexdigest()[:16]

        # Telemetry
        telemetry_record = TelemetryRecord(
            query_id=det_hash,
            timestamp=time.time(),
            mode=request.mode.value,
            issue_categories=[],
            doctrines_triggered=doctrines_triggered,
            cache_hit=len(doctrines_triggered) > 0,
            latency_ms=latency_ms,
            confidence=confidence.value,
            zone=context.zone.value
        )
        self.telemetry.record_query(telemetry_record)

        return QueryResponse(
            response=response_text,
            mode=request.mode.value,
            confidence=confidence.value,
            doctrines_triggered=doctrines_triggered,
            latency_ms=round(latency_ms, 2),
            determinism_hash=det_hash,
            timestamp=datetime.now().isoformat()
        )

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        return {
            "engine": "AUTO06_SUSPENSION_SYSTEMS",
            "version": "1.0.0",
            "status": "operational",
            "port": 9251,
            "doctrine_count": len(self.doctrine_cache.doctrines),
            "categories": [cat.value for cat in IssueCategory],
            "telemetry": self.telemetry.get_stats(),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(title="AUTO06 Suspension Systems Engine", version="1.0.0")

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENGINE = AUTO06SuspensionEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint"""
    return ENGINE.query(request)


@APP.get("/health")
async def health_endpoint():
    """Health check endpoint"""
    return ENGINE.health_check()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine topics"""
    return {
        "count": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "authority": d.authority_level.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


if __name__ == "__main__":
    logger.info("Starting AUTO06 Suspension Systems Engine on port 9251")
    uvicorn.run(APP, host="0.0.0.0", port=9251)
