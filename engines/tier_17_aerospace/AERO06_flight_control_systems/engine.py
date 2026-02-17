"""
AERO06 Flight Control Systems Intelligence Engine v1.0.0
Tax Intelligence Engine (TIE) Architecture - Aviation Specialization

Analyzes aircraft flight control systems: fly-by-wire architecture, control surface
actuators, autopilot systems, flight control laws, stability augmentation, and
redundancy management.

Port: 9201
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to sys.path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "AERO06"
ENGINE_NAME = "Flight Control Systems Intelligence Engine"
VERSION = "1.0.0"
PORT = 9201

AUDIT_LOG_PATH = Path(__file__).parent / "audit_trail.jsonl"
DRIFT_LOG_PATH = Path(__file__).parent / "doctrine_drift.jsonl"

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

class PositionZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class IssueCategory(str, Enum):
    FBW_ARCHITECTURE = "FBW_ARCHITECTURE"
    CONTROL_LAWS = "CONTROL_LAWS"
    ACTUATOR_SYSTEMS = "ACTUATOR_SYSTEMS"
    REDUNDANCY_MANAGEMENT = "REDUNDANCY_MANAGEMENT"
    AUTOPILOT_SYSTEMS = "AUTOPILOT_SYSTEMS"
    STABILITY_AUGMENTATION = "STABILITY_AUGMENTATION"
    ENVELOPE_PROTECTION = "ENVELOPE_PROTECTION"
    SOFTWARE_CERTIFICATION = "SOFTWARE_CERTIFICATION"
    SURFACE_FLUTTER = "SURFACE_FLUTTER"
    REGULATORY_COMPLIANCE = "REGULATORY_COMPLIANCE"
    FAILURE_MODES = "FAILURE_MODES"
    CONTROL_SURFACE_DESIGN = "CONTROL_SURFACE_DESIGN"

class AuthorityLevel(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    PERSUASIVE = "PERSUASIVE"
    COMMENTARY = "COMMENTARY"

# ============================================================================
# DATA MODELS
# ============================================================================

class DoctrineBlock(BaseModel):
    topic: str
    keywords: List[str]
    conclusion_template: str
    reasoning_framework: str
    key_factors: List[str]
    primary_authority: List[str]
    burden_holder: Optional[str] = None
    adversary_position: Optional[str] = None
    counter_arguments: List[str] = Field(default_factory=list)
    resolution_strategy: Optional[str] = None
    entity_scope: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.DEFENSIBLE
    controlling_precedent: Optional[str] = None
    issue_category: IssueCategory
    authority_level: AuthorityLevel = AuthorityLevel.PRIMARY

class QueryRequest(BaseModel):
    query: str
    mode: ResponseMode = ResponseMode.FAST
    zone: PositionZone = PositionZone.PLANNING
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: ResponseMode
    zone: PositionZone
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    authority_citations: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_latency_ms: float
    doctrines_loaded: int
    error_rate: float

# ============================================================================
# DOCTRINE CACHE - REAL FLIGHT CONTROL SYSTEMS EXPERTISE
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    # FBW Architecture
    DoctrineBlock(
        topic="Airbus FBW Normal Law Architecture",
        keywords=["fly-by-wire", "normal law", "flight envelope", "load factor", "alpha protection", "C* law"],
        conclusion_template="Airbus Normal Law provides comprehensive flight envelope protection through load factor limiting, angle-of-attack protection, and bank angle limiting. The system maintains C* (pitch rate command/load factor demand) control law in all flight phases except flare.",
        reasoning_framework="""
AIRBUS FBW NORMAL LAW - MULTI-LAYER PROTECTION ARCHITECTURE:

1. C* Control Law (Primary Pitch Control):
   - Below maneuvering speed: C* = nz (load factor demand)
   - Above maneuvering speed: C* = q (pitch rate demand)
   - Provides natural aircraft feel across speed range
   - Automatic transition between modes based on dynamic pressure
   - Pilot stick input generates g-load or pitch rate command

2. Angle-of-Attack Protection (Alpha Floor/Alpha Max):
   - Alpha_prot: Angle where flight control laws begin protection (typically CL_max * 0.9)
   - Alpha_max: Maximum permitted angle-of-attack (stall angle minus margin)
   - Auto-trim to maintain alpha within protected range
   - Automatic nose-down authority if alpha exceeds alpha_prot
   - Cannot stall aircraft in Normal Law even with full aft stick

3. Load Factor Limiting:
   - Clean configuration: +2.5g to -1.0g
   - With flaps/slats: +2.0g to 0g
   - Protects airframe from overstress
   - Soft stops then hard stops on sidestick
   - VFE (velocity flap extended) protection when configuration extended

4. Bank Angle Protection:
   - 67-degree bank limit in normal maneuvering
   - Auto-rollout tendency beyond 33 degrees
   - Prevents spiral divergence
   - Automatic return to wings-level if pilot releases stick beyond 45 degrees

5. Pitch Attitude Protection:
   - Nose-up limit: 30 degrees (clean), 25 degrees (config)
   - Nose-down limit: -15 degrees
   - High-speed protection: automatic pitch-up if VMO/MMO approached
   - Low-speed stability: auto-pitch authority to prevent deep stall

6. Turn Coordination:
   - Automatic rudder coordination in turns
   - Beta-target (sideslip) minimization
   - Yaw damper integrated into turn coordination
   - No Dutch roll tendency in Normal Law

7. Redundancy Architecture:
   - Five flight control computers: 3 Primary (PRIM 1/2/3) + 2 Secondary (SEC 1/2)
   - Each PRIM has command, monitor, and COM/MON voting channels
   - Dual-dual architecture: two dissimilar processors per lane
   - Automatic switching to Alternate Law if 2+ PRIMs fail
   - ARINC 429 and ARINC 629 databus communication
        """,
        key_factors=[
            "C* law provides consistent handling across speed range",
            "Alpha protection prevents stall in all configurations",
            "Load factor limits protect airframe structural integrity",
            "Bank angle limiting prevents loss of control spiral",
            "Redundant computer voting ensures fault tolerance",
            "Automatic degradation to Alternate Law on dual failure",
            "Turn coordination eliminates need for rudder input",
            "High/low speed protection maintains safe flight envelope"
        ],
        primary_authority=[
            "CS-25.143 - Controllability and Maneuverability General Requirements",
            "CS-25.145 - Longitudinal Control",
            "CS-25.147 - Directional and Lateral Control",
            "Airbus Flight Control Laws Technical Documentation A320/A330/A380 Family",
            "FAA AC 25-7C - Flight Test Guide for Certification of Transport Category Airplanes"
        ],
        issue_category=IssueCategory.FBW_ARCHITECTURE,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Airbus FBW Alternate Law Degradation",
        keywords=["alternate law", "degraded mode", "flight control degradation", "direct law", "abnormal law"],
        conclusion_template="Alternate Law is a degraded FBW mode with reduced protections, activated when multiple flight control computers fail or critical sensor inputs are lost. Aircraft handling becomes more conventional with pitch/bank limits removed but stall protection retained.",
        reasoning_framework="""
ALTERNATE LAW DEGRADATION - PROTECTION LOSS AND HANDLING CHANGES:

1. Triggering Conditions:
   - Loss of 2 or more Primary Flight Control Computers (PRIMs)
   - Dual Air Data Reference (ADR) failure
   - Dual Inertial Reference (IR) failure
   - Multiple slat/flap position sensor disagreements
   - Landing gear extended below certain altitude
   - Windshear warning activation in some phases

2. Alternate Law 1 (High-Altitude Cruise):
   - Load factor protection maintained (+2.5g / -1.0g)
   - Pitch attitude protection removed (can exceed 30 degrees)
   - Bank angle protection removed (can exceed 67 degrees)
   - High/low speed stability maintained
   - Yaw damper functional
   - No alpha protection - can stall aircraft

3. Alternate Law 2 (Low Altitude / Approach):
   - Low-speed stability reduced to conventional characteristics
   - No load factor protection
   - Reduced static stability (more tail-heavy feel)
   - Flight envelope protection removed
   - Mandatory ECAM procedures for approach in Alternate Law
   - Higher approach speeds required (typically +10-15 knots)

4. Direct Law (Severe Degradation):
   - Triggered by catastrophic FBW system failure
   - Direct mechanical/electrical link between sidestick and control surfaces
   - No computer processing of control inputs
   - Control surface deflection proportional to stick deflection
   - Trim remains available but no auto-trim
   - Aircraft feels heavy and requires significant control authority
   - Mandatory emergency descent and immediate landing

5. Mechanical Backup (Ultimate Failure):
   - Pitch Trim Wheel (manual horizontal stabilizer trim)
   - Rudder Pedals (direct mechanical linkage on some models)
   - Only available on total electrical failure
   - Extremely limited controllability
   - Emergency descent only - landing almost impossible

6. Pilot Implications:
   - Reversion message triggers ECAM alert
   - Airspeed margins increase (no alpha protection)
   - Manual pitch trim required (no auto-trim)
   - Stall warning system critical - can now stall
   - Flare technique changes (no auto-flare in Alternate Law)
   - Go-around more complex (manual thrust/pitch coordination)
        """,
        key_factors=[
            "Alternate Law removes angle-of-attack and pitch attitude limits",
            "Aircraft can now stall if mishandled - critical difference from Normal Law",
            "Load factor protection may be degraded or absent",
            "Direct Law provides only basic stick-to-surface coupling",
            "Higher approach speeds and landing distances required",
            "Auto-throttle and auto-land unavailable in degraded modes",
            "Crew workload significantly increases",
            "Emergency checklist compliance mandatory before continuing flight"
        ],
        primary_authority=[
            "EASA CS-25.1329 - Flight Guidance System",
            "Airbus FCOM (Flight Crew Operating Manual) Abnormal Procedures",
            "FAA AC 25.1309-1A - System Design and Analysis",
            "Air France 447 Accident Report BEA 2012 (Alternate Law case study)",
            "ICAO Annex 6 Part I - Operation of Aircraft"
        ],
        issue_category=IssueCategory.FBW_ARCHITECTURE,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Control Laws
    DoctrineBlock(
        topic="Boeing Control Law Philosophy vs Airbus",
        keywords=["Boeing FBW", "control augmentation", "stick feel", "control harmony", "LOES"],
        conclusion_template="Boeing FBW systems (777/787) use control augmentation philosophy preserving conventional handling, while Airbus uses full-authority flight envelope protection. Boeing maintains stick force-to-g relationship; Airbus uses load factor command law.",
        reasoning_framework="""
BOEING VS AIRBUS CONTROL LAW DESIGN PHILOSOPHY:

1. Boeing Control Augmentation System (777/787):
   - Conventional control feel with computer enhancement
   - Stick force proportional to load factor (like mechanical aircraft)
   - Pilot can overpower flight envelope protections with sufficient force
   - Control column movement visible to other pilot (tactile feedback)
   - Stall warning at natural stall speed (no alpha protection)
   - Pitch Rate Command (PRC) law in low-speed regime
   - Load Demand Command (LDC) law in cruise
   - C* (load factor/pitch rate blend) in maneuvering

2. Airbus Full-Authority Protection:
   - Sidestick generates flight parameter commands (g, pitch rate, bank)
   - Aircraft cannot stall, overspeed, or overstress in Normal Law
   - Fixed sidestick deflection produces constant load factor regardless of speed
   - No tactile feedback between pilot stations (dual input summing)
   - Aircraft automatically trims to relieve pilot workload
   - Flight envelope boundaries are hard limits

3. Control Harmony Differences:
   - Boeing: Variable stick force based on dynamic pressure (feels heavier at high speed)
   - Airbus: Constant sidestick force across all speeds
   - Boeing: Visible yoke movement provides situational awareness
   - Airbus: Sidestick position not visible to other pilot (ECAM indication only)
   - Boeing: Manual trim adjustments expected during maneuvering
   - Airbus: Auto-trim maintains zero stick force in steady state

4. LOES (Longitudinal Control) Analysis:
   - Boeing implements Level 1 flying qualities per MIL-STD-1797
   - Stick force per g: 6-12 lbs/g typical for transport category
   - Short period damping ratio: 0.3 to 2.0
   - Neutral static stability acceptable with augmentation active
   - Natural aircraft characteristics retained in degraded modes

5. Failure Mode Philosophy:
   - Boeing: Graceful degradation maintaining similar control feel
   - Airbus: Discrete mode transitions (Normal → Alternate → Direct)
   - Boeing: Fly-by-wire augments but does not replace mechanical feel
   - Airbus: Fly-by-wire completely replaces mechanical control logic

6. Regulatory Compliance Paths:
   - Boeing: Demonstrates compliance via flying qualities (MIL-STD or similar)
   - Airbus: Demonstrates compliance via envelope protection and fault tolerance
   - Both meet CS-25/FAR 25 but through different design philosophies
   - Both achieve Level 1 handling in primary mode, Level 2 in degraded
        """,
        key_factors=[
            "Boeing preserves conventional stick force gradient; Airbus uses constant force sidestick",
            "Boeing allows envelope exceedance with sufficient force; Airbus hard-limits in Normal Law",
            "Control column vs sidestick affects crew coordination and cross-checking",
            "Both philosophies meet certification standards through different means",
            "Pilot transition training critical due to handling differences",
            "Failure mode characteristics differ significantly between philosophies",
            "Tactile feedback vs flight parameter command changes pilot scanning",
            "Both systems reduce pilot workload but via different mechanisms"
        ],
        primary_authority=[
            "FAR 25.143 - Controllability and Maneuverability",
            "MIL-STD-1797A - Flying Qualities of Piloted Aircraft",
            "FAA AC 25-7C - Flight Test Guide",
            "Boeing 777/787 Flight Controls Technical Description",
            "CAST Safety Enhancement SE-004 (Control Law Design)"
        ],
        issue_category=IssueCategory.CONTROL_LAWS,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="C* Control Law Implementation",
        keywords=["C-star", "load factor command", "pitch rate", "blended law", "handling qualities"],
        conclusion_template="C* control law blends pitch rate command (low speed) and load factor command (high speed) to provide consistent handling characteristics across the flight envelope. The blending function transitions smoothly based on dynamic pressure.",
        reasoning_framework="""
C* CONTROL LAW - BLENDED COMMAND ARCHITECTURE:

1. Mathematical Definition:
   C* = nz/Vtas + k*q
   Where:
   - nz = normal load factor (g's)
   - Vtas = true airspeed
   - q = pitch rate (deg/sec)
   - k = blending coefficient (function of dynamic pressure)

2. Low-Speed Regime (Below Corner Speed):
   - k approaches 1.0 → C* ≈ q (pitch rate command)
   - Pilot stick input generates pitch rate proportional to deflection
   - Aircraft responds with constant pitch rate for fixed stick position
   - Provides natural feel for maneuvering and landing flare
   - Prevents pilot-induced oscillations during approach

3. High-Speed Regime (Above Corner Speed):
   - k approaches 0 → C* ≈ nz/Vtas (load factor command)
   - Pilot stick input generates load factor proportional to deflection
   - Aircraft maintains constant g regardless of speed changes
   - Protects against overstress at high dynamic pressure
   - Provides predictable maneuvering at cruise speeds

4. Transition Zone (Around Corner Speed):
   - Smooth blending between pitch rate and load factor response
   - Corner speed typically 1.3 * stall speed in clean configuration
   - Blending function prevents discontinuities in handling
   - Gain scheduling adjusts sensitivity with speed
   - No perceptible transition point to pilot

5. Implementation Details:
   - Requires accurate air data (Vtas, Mach, dynamic pressure)
   - Inertial reference for load factor (nz from accelerometers)
   - Rate gyros for pitch rate (q) measurement
   - Flight control computer integrates sensor inputs
   - Compensation for sensor lag and dynamics
   - Washout filters prevent long-term drift

6. Certification Considerations:
   - Must meet Level 1 flying qualities per MIL-STD-1797
   - Short period frequency and damping within acceptable range
   - Pitch attitude response to step input within bounds
   - Neal-Smith criteria for pilot compensation requirements
   - Time delay (pilot input to aircraft response) < 150 ms
   - Demonstrate handling across full weight and CG envelope
        """,
        key_factors=[
            "C* law provides consistent stick-to-response relationship across speeds",
            "Pitch rate mode prevents over-rotation during takeoff and landing",
            "Load factor mode prevents overstress during high-speed maneuvering",
            "Blending function must be smooth to avoid handling discontinuities",
            "Requires redundant air data and inertial reference sensors",
            "Gain scheduling adjusts control sensitivity with flight condition",
            "Time delay and phase lag critical for pilot-induced oscillation prevention",
            "Flying qualities must meet Level 1 in normal mode, Level 2 in degraded"
        ],
        primary_authority=[
            "MIL-STD-1797A - Flying Qualities of Piloted Aircraft",
            "FAA AC 25-7C - Flight Test Guide Section 5.2 Longitudinal Control",
            "Gibson, J.C. 'Development of the C* Flight Control Law' AIAA 1999",
            "CS-25.143(d) - Longitudinal Control Dynamic Stability",
            "Neal, T.P. and Smith, R.E. 'An In-Flight Investigation to Develop Control System Design Criteria' AFFDL-TR-70-74"
        ],
        issue_category=IssueCategory.CONTROL_LAWS,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Actuator Systems
    DoctrineBlock(
        topic="Hydraulic vs Electro-Hydrostatic Actuator Trade-offs",
        keywords=["hydraulic actuator", "EHA", "electro-hydrostatic", "power-by-wire", "failure modes"],
        conclusion_template="Hydraulic actuators provide high power density and proven reliability but require centralized hydraulic systems. Electro-Hydrostatic Actuators (EHA) eliminate hydraulic plumbing, reduce weight, and improve fault tolerance but introduce electrical load and thermal management challenges.",
        reasoning_framework="""
HYDRAULIC VS ELECTRO-HYDROSTATIC ACTUATOR COMPARISON:

1. Conventional Hydraulic Actuator Architecture:
   - Centralized hydraulic pump driven by engine or APU
   - High-pressure hydraulic fluid distribution (3000-5000 psi typical)
   - Servo valve controls fluid flow to actuator piston
   - Dual or triple redundant hydraulic systems (System A, B, C)
   - Power Control Unit (PCU) houses servo valve and actuator
   - Return lines route fluid back to reservoir

2. Hydraulic System Advantages:
   - High power-to-weight ratio (proven for large control surfaces)
   - Established certification basis and operational history
   - Inherent damping characteristics reduce flutter risk
   - Instantaneous peak power available from accumulator
   - Fire-resistant hydraulic fluid (Skydrol, MIL-PRF-83282)
   - Well-understood failure modes and maintenance procedures

3. Hydraulic System Disadvantages:
   - Heavy hydraulic lines routed throughout aircraft
   - Potential for hydraulic fluid leaks and contamination
   - Centralized failure modes (engine-driven pump loss affects multiple systems)
   - Maintenance intensive (filter changes, fluid servicing, seal replacement)
   - Hydraulic fluid flammability risk despite fire-resistant formulations
   - Environmental concerns (Skydrol toxicity, disposal)

4. Electro-Hydrostatic Actuator (EHA) Architecture:
   - Local electric motor drives hydraulic pump at each actuator
   - Closed-loop hydraulic circuit (no return lines to central reservoir)
   - Bi-directional pump provides extend/retract motion
   - Electric motor controlled by flight control computer signals
   - Self-contained unit - motor, pump, actuator in single assembly
   - No routing of high-pressure hydraulic lines

5. EHA Advantages:
   - Eliminates central hydraulic system and distribution plumbing
   - Weight reduction (787: ~1800 lbs savings vs conventional)
   - Improved fault tolerance (failure local to one actuator)
   - Reduced maintenance (no fluid contamination from central system)
   - Easier installation and retrofit (electrical instead of hydraulic routing)
   - Better thermal efficiency (power only used when actuator active)

6. EHA Challenges and Disadvantages:
   - Higher electrical system load (787 generates 1 MW electrical power)
   - Thermal management critical (motor and pump heat dissipation)
   - More complex power electronics (motor drives, controllers)
   - Limited peak power (no accumulator storage)
   - Electromagnetic interference (EMI) susceptibility
   - Higher cost per actuator unit
   - Less operational history than conventional hydraulics

7. Hybrid Approaches:
   - Electro-Backup Hydraulic Actuators (EBHA) - EHA backing up hydraulic
   - Used on A380 for critical surfaces (ailerons, elevators)
   - Primary mode: conventional hydraulic
   - Backup mode: local EHA when hydraulic system fails
   - Provides redundancy without full electrical power requirement

8. Certification Considerations:
   - EHA must demonstrate equivalent reliability to hydraulic (10^-9 failure rate)
   - DO-160 environmental testing (temperature, vibration, EMI)
   - Thermal runaway protection for electric motor
   - Jam tolerance testing (actuator hardover scenarios)
   - Power transient immunity (electrical supply interruptions)
        """,
        key_factors=[
            "Hydraulic actuators proven for high power density applications",
            "EHA eliminates hydraulic plumbing reducing weight and complexity",
            "Centralized hydraulic failure affects multiple systems; EHA failures localized",
            "EHA requires significant electrical power generation and distribution",
            "Thermal management critical for EHA motor and pump assemblies",
            "Hybrid EBHA approach combines benefits of both technologies",
            "Certification requires demonstration of jam tolerance and failure isolation",
            "Maintenance philosophy shifts from fluid servicing to electrical/electronic troubleshooting"
        ],
        primary_authority=[
            "SAE AIR5005 - Aerospace Actuation Systems Handbook",
            "Boeing 787 Systems Description - Electrical Power and Flight Controls",
            "FAA AC 25.1309-1A - System Design and Analysis (Actuator Redundancy)",
            "CS-25.671 - General (Control System Requirements)",
            "Airbus A380 Electro-Backup Hydraulic Actuator Technical Description"
        ],
        issue_category=IssueCategory.ACTUATOR_SYSTEMS,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Actuator Jam Detection and Mitigation",
        keywords=["jam tolerance", "hardover", "force fight", "disconnect mechanism", "dual tandem actuator"],
        conclusion_template="Flight control actuators must include jam detection to identify stuck or hardover conditions, and mitigation mechanisms such as force limiting, automatic disconnect, or dual-tandem architecture to prevent loss of aircraft control.",
        reasoning_framework="""
ACTUATOR JAM DETECTION AND MITIGATION STRATEGIES:

1. Jam Failure Modes:
   - Mechanical Jam: Internal bearing seizure, debris contamination, structural failure
   - Hardover: Actuator drives to full deflection and cannot be stopped
   - Runaway: Actuator moves uncommanded in one direction
   - Slow-over: Gradual drift to incorrect position
   - Oscillatory Failure: Actuator hunting or limit-cycling

2. Jam Detection Methods:
   - Position Feedback Disagreement: LVDT/RVDT sensor vs commanded position
   - Force Feedback Monitoring: Excessive servo valve current or hydraulic pressure
   - Acceleration Mismatch: Surface acceleration inconsistent with command
   - Cross-Channel Comparison: Multiple actuators on same surface disagreeing
   - Rate Limiting: Actuator velocity exceeds physical capability
   - Null Position Error: Actuator fails to center when commanded

3. Detection Threshold Tuning:
   - Must discriminate between jam and aerodynamic loads
   - Buffet, turbulence, and maneuvering loads create position variations
   - Time delay filters prevent false positives (typically 50-200 ms)
   - Threshold varies by flight phase (higher margin during turbulence)
   - Multi-fault voting (2 out of 3 sensors) prevents single-point failures

4. Force-Fight Mitigation:
   - Dual Tandem Actuators: Two actuators on same control surface
   - Force Summing Mode: Both actuators drive together in normal operation
   - Force Limiting: Healthy actuator backs off if fighting jammed actuator
   - Bypass Valve: Jammed actuator hydraulically bypassed to free-float
   - Equalization Mode: Actuators share load equally with cross-feedback

5. Automatic Disconnect Mechanisms:
   - Solenoid-Actuated Disconnect: Electrically commanded separation
   - Fuse Pin: Mechanical shear pin breaks under excessive load
   - Hydraulic Bypass: Valve opens to allow free movement of jammed actuator
   - Clutch Release: Electromagnetic or mechanical clutch disengages drive
   - Time to disconnect: < 100 ms from jam detection to full disconnect

6. Dual-Tandem Actuator Architecture (Boeing 777 Example):
   - Primary and Secondary actuators operate in parallel
   - Position summing: Both actuators must agree for full authority
   - If one jams, other continues to operate with reduced authority
   - Force fight detection via pressure differential monitoring
   - Automatic mode transition from active/active to active/damped

7. Pilot Indications and Procedures:
   - EICAS/ECAM alert: "FLT CONTROL JAM - [surface name]"
   - Control force increase may be perceptible to pilot
   - Asymmetric control forces between axes (e.g., roll jam affects turn coordination)
   - Abnormal checklist: May require reduced maneuvering, reduced speed, or immediate landing
   - Simulator training required for jam scenarios

8. Certification Requirements:
   - FAR 25.671(c): Jamming, ground, and bending loads must not impair operation
   - Must demonstrate continued safe flight and landing with single jam
   - Force fight loads must not exceed structural limits
   - Disconnect time must prevent aircraft upset
   - Multiple jam scenario analysis required for certification
        """,
        key_factors=[
            "Jam detection requires discriminating between failure and normal aerodynamic loads",
            "Dual-tandem actuators provide jam tolerance through force summing and isolation",
            "Disconnect mechanisms must activate within 100 ms to prevent aircraft upset",
            "Force fight between actuators can exceed structural limits if not mitigated",
            "Position feedback disagreement primary indicator of jam condition",
            "Certification requires demonstration of continued safe flight with single jam",
            "Pilot training essential for recognizing and responding to jam indications",
            "Multiple jam scenarios analyzed during certification (extremely low probability)"
        ],
        primary_authority=[
            "FAR 25.671(c) - Control Systems Jamming, Ground, and Bending Loads",
            "FAA AC 25.671-1 - Control Systems",
            "SAE ARP4754A - Guidelines for Development of Civil Aircraft Systems (Section 4.3.4)",
            "DO-178C - Software Considerations (for jam detection algorithms)",
            "MIL-STD-1797A Appendix B - Failure States and Handling Qualities"
        ],
        issue_category=IssueCategory.ACTUATOR_SYSTEMS,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Redundancy Management
    DoctrineBlock(
        topic="Flight Control Computer Redundancy Architecture",
        keywords=["triplex", "quadruplex", "voting logic", "dissimilar redundancy", "FCC failure"],
        conclusion_template="Modern fly-by-wire aircraft use triplex (3-channel) or quadruplex (4-channel) flight control computer redundancy with voting logic to tolerate failures. Dissimilar hardware and software in redundant lanes prevents common-mode failures.",
        reasoning_framework="""
FLIGHT CONTROL COMPUTER REDUNDANCY ARCHITECTURE:

1. Redundancy Levels:
   - Simplex: Single computer (not acceptable for fly-by-wire transport aircraft)
   - Duplex: Two computers with cross-monitoring (early FBW, military aircraft)
   - Triplex: Three computers with voting logic (Airbus A320/A330/A340)
   - Quadruplex: Four computers with voting (Boeing 777/787, Airbus A380)
   - Quintuplex: Five computers (F-16, high-performance military)

2. Voting Logic Strategies:
   - Majority Voting: 2-out-of-3 or 3-out-of-4 for triplex/quadruplex
   - Mid-Value Select: Median value selection (rejects high/low outliers)
   - Analytical Redundancy: Model-based comparison for reasonableness
   - Threshold Voting: Accept any value within tolerance band
   - Weighted Voting: Known-good channels weighted higher

3. Airbus A320 Family Triplex Architecture (PRIMs):
   - Three Primary Flight Control Computers (PRIM 1, 2, 3)
   - Each PRIM contains dual-lane: Command (COM) and Monitor (MON)
   - COM lane generates control commands; MON lane verifies COM
   - If COM and MON disagree, that PRIM is failed and isolated
   - Two healthy PRIMs sufficient for Normal Law operation
   - One healthy PRIM sufficient for Alternate Law
   - Two Secondary Computers (SEC 1, 2) provide backup for critical functions

4. Boeing 777 Quadruplex Architecture:
   - Three Primary Flight Computers (PFC) with triplex redundancy
   - One Autopilot Flight Director Computer (AFDC) provides fourth channel
   - Each PFC contains three dissimilar processing lanes
   - Actuator Control Electronics (ACE) perform final voting before surface command
   - Loss of two PFCs still maintains full flight control capability
   - Fourth channel (AFDC) enables advanced autopilot/autothrust modes

5. Dissimilar Redundancy (Common-Mode Failure Prevention):
   - Hardware: Different processor architectures (e.g., Intel vs Motorola)
   - Software: Different programming languages or development teams
   - Compiler: Different compilers to prevent compiler bugs
   - Development Environment: Separate teams with independent verification
   - Purpose: Prevent single software bug from affecting all channels
   - Example: Airbus uses different processor families in PRIM COM vs MON lanes

6. Failure Detection and Isolation:
   - Built-In Test (BIT): Continuous self-test of processor, memory, I/O
   - Cross-Channel Monitoring: Each lane monitors others for disagreement
   - Watchdog Timers: Detect processor lockup or software hang
   - Parity/ECC: Memory error detection and correction
   - Checksums/CRC: Data integrity verification on bus communication
   - ARINC 429/629/664: Fault-tolerant databusses with error detection

7. Graceful Degradation:
   - First Failure: No change to flight control laws (silent failover)
   - Second Failure: Reversion to Alternate Law with ECAM alert
   - Third Failure: Reversion to Direct Law, immediate landing required
   - Failure memory: System remembers failed lanes across power cycles
   - Dispatch with failures: MEL (Minimum Equipment List) defines acceptable degradation

8. Certification Approach (SAR 25.1309):
   - Catastrophic failures < 10^-9 per flight hour
   - Hazardous failures < 10^-7 per flight hour
   - Triplex systems meet requirements with dual-fault tolerance
   - Quadruplex provides margin for certification and dispatch flexibility
   - Fault Tree Analysis (FTA) and Markov modeling verify failure rates
   - Common Cause Analysis identifies potential common-mode failures
        """,
        key_factors=[
            "Triplex redundancy provides dual-fault tolerance for catastrophic failure protection",
            "Quadruplex architecture adds dispatch flexibility and advanced autopilot capability",
            "Voting logic must reject failed channels while maintaining flight control authority",
            "Dissimilar hardware/software prevents common-mode failures from affecting all lanes",
            "Graceful degradation maintains controllability even with multiple failures",
            "Built-in test and cross-channel monitoring detect failures before they affect control",
            "Certification requires demonstration of <10^-9 catastrophic failure rate",
            "ARINC databusses provide fault-tolerant communication between redundant computers"
        ],
        primary_authority=[
            "FAR 25.1309 - Equipment, Systems, and Installations",
            "SAE ARP4754A - Guidelines for Development of Civil Aircraft and Systems",
            "SAE ARP4761 - Guidelines and Methods for Conducting Safety Assessment Process",
            "DO-178C - Software Considerations in Airborne Systems and Equipment Certification",
            "EASA CS-25.1309 - System Design and Analysis"
        ],
        issue_category=IssueCategory.REDUNDANCY_MANAGEMENT,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Autopilot Systems
    DoctrineBlock(
        topic="Autopilot LNAV and VNAV Mode Logic",
        keywords=["LNAV", "VNAV", "flight management system", "lateral navigation", "vertical navigation", "path intercept"],
        conclusion_template="LNAV (Lateral Navigation) and VNAV (Vertical Navigation) modes enable autopilot to follow FMS-computed flight paths. LNAV controls heading/track to follow lateral route; VNAV controls altitude/speed to meet climb, cruise, and descent constraints.",
        reasoning_framework="""
AUTOPILOT LNAV AND VNAV MODE IMPLEMENTATION:

1. LNAV (Lateral Navigation) Mode:
   - Engaged when autopilot armed in NAV or LNAV mode and FMS route active
   - Computes cross-track error (XTE) from aircraft position to desired track
   - Bank angle command proportional to XTE and track angle error
   - Maximum bank angle typically limited (25 degrees typical, 30 degrees max)
   - Smoothly intercepts course using Bank Angle = K1*XTE + K2*Track_Error
   - Course anticipation (turn lead) prevents overshoot at waypoints
   - Wind correction automatically applied based on FMS wind model

2. LNAV Path Intercept Logic:
   - Initial intercept angle limited to prevent overshoot (typically 45 degrees max)
   - Intercept gain increases as aircraft approaches desired track
   - S-curve intercept profile provides smooth transition to track
   - Track angle error rate damping prevents oscillation
   - GPS or DME/DME position used for high accuracy
   - RNP (Required Navigation Performance) defines lateral accuracy requirement
   - Typical RNP values: 10.0 (enroute), 1.0 (terminal), 0.3 (approach)

3. VNAV (Vertical Navigation) Mode:
   - Vertical profile computed by FMS based on waypoint altitude constraints
   - Climb mode: Maintains climb speed (IAS or Mach) until level-off altitude
   - Cruise mode: Maintains assigned altitude (barometric or GPS altitude)
   - Descent mode: Follows computed descent path to meet altitude constraints
   - Top-of-Descent (TOD) computed based on descent gradient and wind
   - Economy descent typically 3-degree path or 1000-1500 fpm descent rate

4. VNAV Climb Logic:
   - Auto-throttle commands climb thrust (typically CLB or MCT detent)
   - Pitch mode maintains target climb speed (e.g., 250 KIAS / 0.78 Mach)
   - Altitude capture anticipation begins ~1000 feet below target altitude
   - Capture mode reduces pitch to smoothly level off at target altitude
   - Altitude hold mode engages once within ±50 feet of target
   - Thrust reduced to maintain level flight after capture

5. VNAV Descent Logic:
   - Idle thrust descent (minimum fuel consumption)
   - Pitch controls to maintain target descent speed (typically 280/.78 or economy speed)
   - Vertical path error computed as aircraft altitude - FMS altitude at current position
   - Path intercept uses proportional + rate damping control law
   - Altitude constraints at waypoints (e.g., 'cross WAYPOINT at or above 10,000 ft')
   - If constraint cannot be met, 'VNAV UNABLE' warning and reversion to V/S mode

6. VNAV Path Constraints:
   - AT (At): Aircraft must cross waypoint at exact altitude
   - AT_OR_ABOVE: Aircraft must cross at or above specified altitude (climb or level)
   - AT_OR_BELOW: Aircraft must cross at or below specified altitude (descent constraint)
   - BETWEEN: Aircraft altitude must be within specified window
   - Speed constraints similarly handled (e.g., 250 KIAS below 10,000 ft)

7. Mode Reversion and Failure Handling:
   - LNAV reverts to HDG SEL if GPS/FMS position lost
   - VNAV reverts to V/S (Vertical Speed) or ALT HOLD if FMS path invalid
   - Loss of both air data computers causes autopilot disconnect
   - Single ADR/IR failure: Autopilot continues using remaining sensors
   - Flight Director guidance remains even if autopilot disconnects

8. Advanced VNAV Features (FANS, RNP-AR):
   - RNP-AR (Required Navigation Performance - Authorization Required): 0.1-0.3 NM lateral accuracy
   - RF (Radius-to-Fix) legs: Curved paths at waypoints (reduces track miles)
   - Vertical RNP: Vertical path accuracy requirements for approaches
   - Time-of-Arrival constraints: VNAV adjusts speed to meet RTA (Required Time of Arrival)
   - Continuous Descent Operations (CDO): Idle descent from cruise to approach minimizes fuel/noise
        """,
        key_factors=[
            "LNAV maintains lateral track within RNP accuracy requirement using cross-track error feedback",
            "VNAV manages vertical profile to meet altitude and speed constraints",
            "Course anticipation and path intercept logic prevent overshoot at waypoints",
            "Auto-throttle and pitch work together to maintain target speeds in climb/descent",
            "Constraint logic handles AT, AT_OR_ABOVE, AT_OR_BELOW waypoint restrictions",
            "Mode reversions ensure safe flight even with sensor or FMS failures",
            "RNP-AR enables curved approach paths and vertical guidance for terrain clearance",
            "Economy descent uses idle thrust to minimize fuel consumption"
        ],
        primary_authority=[
            "FAA AC 90-105A - Approval Guidance for RNP Operations and Barometric VNAV",
            "RTCA DO-236C - Minimum Aviation System Performance Standards for RNP",
            "ICAO PBN Manual Doc 9613 - Performance-Based Navigation",
            "Boeing Flight Crew Training Manual - Autopilot/Flight Director",
            "Airbus FCOM - Flight Management and Guidance"
        ],
        issue_category=IssueCategory.AUTOPILOT_SYSTEMS,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Autoland System Requirements and Categories",
        keywords=["autoland", "CAT II", "CAT III", "decision height", "ILS", "fail-operational"],
        conclusion_template="Autoland systems enable autopilot-coupled approaches and landings in low visibility. CAT I requires basic autopilot; CAT II/III require redundant systems, fail-operational architecture, and specialized certification to land with decision heights down to 0 feet in CAT IIIc.",
        reasoning_framework="""
AUTOLAND SYSTEM REQUIREMENTS AND CERTIFICATION CATEGORIES:

1. ILS Category Definitions (ICAO Annex 10):
   - CAT I: Decision Height (DH) ≥ 200 ft, RVR ≥ 550 m (1800 ft)
     → Standard ILS approach, no autoland required, manual landing below DH
   - CAT II: DH 100-200 ft, RVR ≥ 300 m (1000 ft)
     → Autoland to 100 ft, manual flare and landing, or autopilot flare with manual rollout
   - CAT IIIa: DH < 100 ft or no DH, RVR ≥ 175 m (575 ft)
     → Autoland with autopilot flare and touchdown, manual rollout
   - CAT IIIb: DH < 50 ft or no DH, RVR 50-175 m (165-575 ft)
     → Autoland with autopilot flare, touchdown, and auto-rollout guidance
   - CAT IIIc: No DH, No RVR minimum (zero visibility)
     → Theoretical only, no current certifications (requires auto-taxi)

2. Autoland System Architecture (CAT II/III):
   - Dual or triple autopilot engagement required (depends on failure classification)
   - Dual ILS receivers with cross-comparison
   - Dual radio altimeters for flare initiation
   - Auto-throttle for speed and thrust control
   - Fail-operational: System continues to land safely after single failure
   - Fail-passive (CAT II): Reversion to manual after failure without hazardous deviation

3. Autoland Phases:
   - Approach Phase: Autopilot tracks ILS localizer and glideslope
   - Flare Initiation: Radio altimeter triggers flare at 40-50 ft AGL
   - Flare Phase: Pitch-up to reduce descent rate, throttle retard to idle
   - Touchdown: Main gear touchdown at 1-3 ft/sec descent rate, 130-150 KIAS typical
   - Rollout Phase (CAT IIIb): Autopilot maintains runway centerline using localizer
   - Deceleration: Auto-brake system applied, reversers deployed

4. Flare Law Design:
   - Exponential flare: h_dot = -k * h (descent rate proportional to height)
   - Typical flare constant k = 0.15 to 0.25
   - At 50 ft AGL with -700 fpm descent → flare reduces to -150 fpm at touchdown
   - Pitch attitude increases 2-5 degrees during flare
   - Auto-throttle retards to idle at flare initiation (some aircraft at 25 ft)
   - Longitudinal control authority sufficient to arrest descent without pilot input

5. Failure Monitoring and Alerting:
   - Dual/triple autopilot comparison: Localizer and glideslope error monitoring
   - If disagreement > threshold (typically 1-2 dots), autopilot disconnects with alert
   - Radio altimeter comparison: < 5 ft disagreement required for CAT III
   - ILS signal quality monitoring: Flag warnings for unreliable signals
   - Auto-disconnect below alert height if failure detected
   - Alert Height: Typically 100 ft for CAT II, 50 ft for CAT IIIa (no go-around below this)

6. Flight Crew Procedures:
   - Pre-approach briefing: Verify autoland capability, minima, runway state
   - Both pilots monitor autopilot performance during approach
   - Callouts: "Localizer alive", "Glideslope alive", "Land 2" or "Land 3" (autopilot status)
   - Decision Height callout: Crew decides to continue or go-around
   - Below Alert Height: Hands-off, monitor only (no manual intervention unless unsafe)
   - After touchdown: Disengage autopilot, manual braking and steering (or auto-rollout)

7. Aircraft and Airport Certification:
   - Aircraft must be certified for CAT II/III operations (type certificate supplement)
   - Flight crew must be trained and qualified (recurrent simulator checks)
   - Airport ILS must be certified to CAT II/III standard (signal accuracy, terrain clearance)
   - Runway lighting: High-Intensity Approach Lights (HIAL), centerline, touchdown zone
   - Runway surface: Grooved or porous friction course for contaminated runway performance

8. Limitations and Considerations:
   - Crosswind limits: CAT III typically limited to 10-15 knots crosswind
   - Contaminated runway: Standing water, snow, ice reduce autoland capability
   - Tailwind component typically limited to 10 knots
   - Turbulence and windshear may preclude autoland use
   - MEL: Autoland requires all systems serviceable (no degraded operations for CAT III)
        """,
        key_factors=[
            "CAT I allows manual landing; CAT II/III require autopilot-coupled landing capability",
            "Fail-operational architecture continues landing safely after single failure",
            "Dual ILS receivers and radio altimeters provide redundancy for approach monitoring",
            "Flare law uses exponential descent rate reduction to achieve smooth touchdown",
            "Alert height defines point below which go-around is not permitted",
            "Crew monitors autopilot performance but does not intervene below alert height unless unsafe",
            "Airport and aircraft must both be certified for CAT II/III operations",
            "Crosswind and contaminated runway conditions may preclude autoland use"
        ],
        primary_authority=[
            "ICAO Annex 10 Volume I - Aeronautical Telecommunications (ILS Standards)",
            "FAA AC 120-28D - Criteria for Approval of Category III Landing Weather Minima",
            "EASA CS-AWO - All-Weather Operations Certification Specifications",
            "FAR 91.189 - IFR Operations: Two-Way Radio Communications Failure",
            "JAA TGL No. 2 - Acceptable Means of Compliance for Autoland Systems"
        ],
        issue_category=IssueCategory.AUTOPILOT_SYSTEMS,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Stability Augmentation
    DoctrineBlock(
        topic="Yaw Damper System Design and Failure Effects",
        keywords=["yaw damper", "Dutch roll", "lateral-directional stability", "SAS", "damping ratio"],
        conclusion_template="Yaw damper augments lateral-directional stability by adding yaw rate feedback to rudder control, suppressing Dutch roll oscillations. Failure of yaw damper results in uncomfortable rolling/yawing oscillations but does not prevent safe flight if pilots recognize and compensate.",
        reasoning_framework="""
YAW DAMPER SYSTEM - DUTCH ROLL SUPPRESSION:

1. Dutch Roll Phenomenon (Unaugmented Aircraft):
   - Coupled lateral-directional oscillation: rolling and yawing motion
   - Caused by insufficient directional stability (Cnβ) relative to lateral stability (Clβ)
   - Typical period: 3-10 seconds
   - Natural damping ratio: 0.02-0.10 (lightly damped, objectionable to passengers)
   - Particularly problematic in swept-wing jet aircraft
   - Light turbulence can excite Dutch roll, creating continuous rolling motion

2. Yaw Damper Control Law (Basic):
   - Rudder command = -K * yaw_rate
   - Yaw rate sensor (rate gyro) detects yaw angular velocity
   - Gain K tuned to provide critical damping (ζ = 0.3-0.7)
   - Negative feedback: Yaw rate to right → left rudder applied
   - Washout filter prevents long-term rudder offset (high-pass filter, ~3-10 sec time constant)
   - Result: Dutch roll damping ratio improved to 0.3-0.5 (acceptable handling)

3. Advanced Yaw Damper Implementations:
   - Sideslip feedback: Rudder command also includes β (sideslip angle) term
   - Roll rate coordination: Yaw damper adjusts for roll rate to coordinate turns
   - Gain scheduling: Yaw damper gain varies with airspeed, altitude, configuration
   - Multi-loop architecture: Inner loop (yaw rate) + outer loop (sideslip)
   - Turn coordination: Automatic rudder in turns to minimize sideslip (β ≈ 0)

4. Yaw Damper Engagement and Modes:
   - Typically engaged automatically after takeoff (weight-on-wheels switch)
   - Remains engaged throughout flight unless manually disengaged or failure
   - Some aircraft: Dual yaw damper (primary and secondary channels)
   - Failure of one channel: System continues with remaining channel
   - Total yaw damper failure: EICAS/ECAM alert, flight continues safely

5. Failure Effects and Crew Response:
   - Loss of yaw damper: Dutch roll oscillations return
   - Pilot perception: Continuous gentle rolling/yawing (2-5 degrees amplitude)
   - Passenger discomfort: Motion sickness risk on long flights
   - Crew action: Reduce speed if in turbulence, avoid abrupt maneuvers
   - Manual damping: Pilot can suppress Dutch roll with small rudder inputs (tiring)
   - Landing: Approach in smooth air, increased crosswind difficulty

6. Certification Requirements:
   - FAR 25.181(a): Aircraft must have satisfactory Dutch roll characteristics
   - Level 1 requirement WITH yaw damper: ζ ≥ 0.08, ζ*ω_n ≥ 0.15 rad/sec
   - Level 2 requirement WITHOUT yaw damper: ζ ≥ 0.02, ζ*ω_n ≥ 0.05 rad/sec
   - Aircraft must be controllable with yaw damper failed (dispatch allowed per MEL)
   - Flight test demonstration of Dutch roll damping with and without yaw damper

7. Redundancy and Monitoring:
   - Single-channel yaw damper: Failure monitoring via position feedback
   - Dual-channel: Cross-comparison detects failures
   - Built-in test detects sensor, actuator, and computer failures
   - Yaw damper may share computer with autopilot or stability augmentation system
   - ARINC 429 bus provides yaw rate and sideslip data to multiple systems

8. Interaction with Autopilot and Flight Controls:
   - Yaw damper authority limited (typically ±3 degrees rudder)
   - Does not interfere with pilot rudder input (pilot has override authority)
   - Autopilot turn coordination may use same rudder actuator (summed commands)
   - Fly-by-wire aircraft: Yaw damper integrated into normal control law
   - FBW Normal Law: Turn coordination automatic, yaw damper not separate system
        """,
        key_factors=[
            "Dutch roll is lightly damped oscillation in swept-wing jets without augmentation",
            "Yaw damper uses yaw rate feedback to rudder to increase damping ratio",
            "Washout filter prevents steady-state rudder offset from long-term yaw rate bias",
            "Yaw damper failure returns aircraft to natural Dutch roll characteristics",
            "Certification requires acceptable handling with yaw damper failed",
            "Pilot can manually suppress Dutch roll but workload is high",
            "Advanced yaw dampers include sideslip and turn coordination functions",
            "Fly-by-wire aircraft integrate yaw damping into normal control law"
        ],
        primary_authority=[
            "FAR 25.181 - Dynamic Stability (Lateral-Directional)",
            "MIL-STD-1797A - Flying Qualities (Dutch Roll Requirements)",
            "FAA AC 25-7C - Flight Test Guide Section 5.4 Lateral-Directional",
            "Roskam, J. 'Airplane Flight Dynamics and Automatic Flight Controls' Part II Chapter 10",
            "CS-25.181 - Dynamic Stability"
        ],
        issue_category=IssueCategory.STABILITY_AUGMENTATION,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Envelope Protection
    DoctrineBlock(
        topic="High Angle-of-Attack Protection and Alpha Floor",
        keywords=["alpha protection", "stall prevention", "alpha floor", "TOGA", "angle of attack"],
        conclusion_template="High angle-of-attack protection prevents aircraft stall by limiting pitch authority and automatically reducing angle-of-attack when approaching stall. Alpha Floor (Airbus) provides automatic TOGA thrust if low-speed condition detected, preventing inadvertent stall entry.",
        reasoning_framework="""
HIGH ANGLE-OF-ATTACK PROTECTION SYSTEMS:

1. Angle-of-Attack (AoA) Definitions:
   - Alpha (α): Angle between aircraft longitudinal axis and relative wind
   - Alpha_prot: Protection activation angle (typically 0.9 * alpha_stall)
   - Alpha_max: Maximum permitted angle (stall angle minus safety margin)
   - Alpha_floor: Threshold for automatic TOGA thrust activation
   - Stall angle: Angle where lift coefficient peaks (typically 14-18 degrees)

2. Stall Warning System (Conventional Aircraft):
   - Stick shaker: Physical vibration of control column at alpha_warn
   - Stick pusher: Forward stick force applied at alpha > alpha_warn
   - Aural warning: "STALL STALL" voice alert
   - Visual indication: Red stall warning on PFD
   - Activation typically 5-10 knots above stall speed

3. Airbus Alpha Protection (Normal Law):
   - Alpha_prot entry: Nose-down pitch authority increases, auto-trim active
   - Flight control computer prevents exceeding alpha_max
   - Pilot can pull full aft stick → aircraft stabilizes at alpha_max (high drag, low speed)
   - Aircraft CANNOT stall in Normal Law even with full aft stick
   - Automatic pitch-down if alpha exceeds alpha_max
   - Buffet felt at alpha_prot due to airflow separation (natural cue)

4. Alpha Floor Function (Airbus):
   - Activated if alpha > alpha_floor AND throttles not already at TOGA
   - Automatic throttle advance to TOGA (takeoff/go-around thrust)
   - Both engines commanded to maximum thrust
   - Overrides autopilot throttle mode
   - Pilot can cancel by advancing throttles to TOGA detent (confirming action)
   - Prevents windshear-induced stall or inadvertent low-speed upset
   - Only active in Normal Law (not available in Alternate/Direct Law)

5. Boeing Approach: Stick Shaker and Pusher:
   - Stick shaker activates at margin above stall (typically 1.15 * V_stall)
   - Stick pusher (some models) applies forward column force
   - Pilot can overpower stick pusher if necessary (not hard-limited like Airbus alpha_max)
   - Stall protection not absolute → pilot can stall aircraft if mishandled
   - Philosophy: Provide strong cues but allow pilot override

6. Configuration and Weight Effects:
   - Alpha_prot and alpha_max vary with flap/slat configuration
   - Clean: Lower alpha limits (lower CL_max)
   - Flaps extended: Higher alpha limits (higher CL_max due to increased camber)
   - Weight affects stall speed but not alpha (AoA is geometric angle)
   - CG position affects alpha: Aft CG reduces stability, earlier stall warning

7. Sensor Architecture and Failure Modes:
   - Dual or triple AoA vanes on fuselage (left, right, standby)
   - Cross-comparison detects sensor failures
   - Single AoA failure: Reversion to Alternate Law (alpha protection lost)
   - Dual AoA failure: Reversion to Direct Law (no protections)
   - Pitot-static failure: Unreliable airspeed also triggers protection loss
   - Crew must fly manually using pitch/power/configuration tables

8. Icing Effects on AoA Protection:
   - Ice accretion on wing leading edge increases stall angle
   - AoA vane may ice over (false reading)
   - Ice protection systems (bleed air, electric heating) essential
   - Stall speed increases 20-40% in severe icing (FAR 25 Appendix C/O)
   - Alpha protection based on clean wing stall angle → inadequate if iced
   - Crew awareness: Stick shaker in icing = immediate recovery action
        """,
        key_factors=[
            "Airbus Normal Law prevents stall by hard-limiting angle-of-attack to alpha_max",
            "Alpha Floor provides automatic TOGA thrust if low-speed condition detected",
            "Boeing philosophy provides stall warning/pusher but allows pilot override",
            "AoA protection lost in Alternate/Direct Law - crew must prevent stall manually",
            "Dual AoA sensor failure causes reversion to degraded flight control modes",
            "Ice accretion increases stall speed and may render AoA protection inadequate",
            "Configuration changes (flaps/slats) affect alpha limits and stall speed",
            "Certification requires demonstration of stall characteristics in all configurations"
        ],
        primary_authority=[
            "FAR 25.201 - Stall Demonstration",
            "FAR 25.203 - Stall Characteristics",
            "EASA CS-25.201/203 - Stall Requirements",
            "Airbus FCOM - Flight Controls Normal Law Protections",
            "FAA AC 25-7C - Flight Test Guide Section 5.1.2 Stall"
        ],
        issue_category=IssueCategory.ENVELOPE_PROTECTION,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Software Certification
    DoctrineBlock(
        topic="DO-178C Software Certification for Flight Control Systems",
        keywords=["DO-178C", "DAL A", "software assurance", "verification", "MCDC", "traceability"],
        conclusion_template="DO-178C defines software development and verification standards for airborne systems. Flight control software is Design Assurance Level A (DAL-A), requiring most rigorous verification including Modified Condition/Decision Coverage (MC/DC) testing and formal methods.",
        reasoning_framework="""
DO-178C SOFTWARE CERTIFICATION PROCESS:

1. Design Assurance Levels (DAL):
   - DAL-A (Catastrophic): Failure prevents continued safe flight and landing
     → Flight control computers, engine FADEC, autopilot for CAT III
   - DAL-B (Hazardous): Failure causes serious injuries or major aircraft damage
     → Navigation displays, terrain awareness systems
   - DAL-C (Major): Failure causes passenger discomfort or workload increase
     → Weather radar, TCAS
   - DAL-D (Minor): Failure has slight impact on safety margins
     → Cabin entertainment systems
   - DAL-E (No Safety Effect): Failure has no safety impact

2. DAL-A Requirements for Flight Control Software:
   - Requirements traceability: Every line of code traced to system requirement
   - High-Level Requirements (HLR): Derived from system safety assessment
   - Low-Level Requirements (LLR): Detailed software design specifications
   - Source code: Compliant with coding standards (MISRA-C, DO-178C guidelines)
   - Structural Coverage: Modified Condition/Decision Coverage (MC/DC) = 100%
   - Verification Independence: Testing performed by team independent of developers

3. Modified Condition/Decision Coverage (MC/DC):
   - Each condition in decision independently affects outcome
   - Example: IF (A AND B) THEN action
     → Test cases: A=T,B=T (action taken), A=T,B=F (action not taken), A=F,B=T (action not taken)
   - MC/DC ensures every boolean condition tested for effect on result
   - More rigorous than statement coverage or branch coverage
   - Required for DAL-A, optional for DAL-B/C

4. Software Development Process (DO-178C Section 5):
   - Planning: Software Development Plan, Verification Plan, Configuration Management Plan
   - Requirements: High-Level and Low-Level Requirements Documents
   - Design: Software Architecture and Detailed Design
   - Coding: Source code with adherence to coding standards
   - Integration: Build process, linking, executable object code
   - Verification: Reviews, analyses, testing at each stage
   - Configuration Management: Version control, change tracking, baseline management

5. Verification Activities (DO-178C Section 6):
   - Reviews: Requirements review, design review, code review, test review
   - Analyses: Traceability analysis, timing analysis, memory usage, stack depth
   - Testing: Unit test, integration test, hardware/software integration test
   - Structural Coverage Analysis: MC/DC for DAL-A, decision coverage for DAL-B
   - Verification of Verification: Ensure test cases are correct and complete

6. Tool Qualification (DO-178C Section 12):
   - Development tools (compilers, linkers) may introduce errors
   - Tool Qualification Level (TQL-1 to TQL-5) based on tool impact
   - Compiler for DAL-A software requires qualification or extensive verification
   - Example: GCC compiler qualified per DO-178C for A380 FBW software
   - Static analysis tools (Polyspace, Coverity) often used to detect runtime errors

7. Formal Methods (DO-178C Supplement DO-333):
   - Mathematical proof of software correctness
   - Model checking: Exhaustive state space exploration
   - Theorem proving: Formal verification of properties
   - Example: Airbus A380 FBW software verified using SCADE Suite (model-based development)
   - Reduces testing burden if formal methods used correctly
   - DO-333 provides credit for formal methods in place of some testing

8. Change Impact Analysis and Regression:
   - Any software change requires re-verification
   - Impact analysis determines which requirements affected by change
   - Regression testing: Re-run all affected test cases
   - Configuration management ensures traceability of changes
   - Software Change Review Board approves all changes

9. Certification Deliverables:
   - Software Accomplishment Summary (SAS): Overview for certification authority
   - Software Configuration Index (SCI): List of all software components and versions
   - Software Life Cycle Data: Requirements, design, code, test results
   - Software Verification Results: Evidence of compliance with DO-178C objectives
   - Problem Reports: All issues found during development and resolution status

10. Ongoing Airworthiness:
    - Post-certification changes follow DO-178C process
    - Service Bulletins and Airworthiness Directives for software updates
    - Software version control critical for fleet management
    - Re-certification required for major changes
    - Lessons learned from service issues fed back to design process
        """,
        key_factors=[
            "Flight control software is DAL-A requiring highest rigor of verification",
            "MC/DC testing ensures every boolean condition tested for independent effect",
            "Requirements traceability ensures every line of code maps to safety requirement",
            "Tool qualification required for compilers and development tools",
            "Formal methods can reduce testing burden if used per DO-333 supplement",
            "Verification independence ensures unbiased testing by separate team",
            "Configuration management tracks all changes and maintains baselines",
            "Change impact analysis and regression testing required for any software modification"
        ],
        primary_authority=[
            "RTCA DO-178C - Software Considerations in Airborne Systems and Equipment Certification",
            "RTCA DO-333 - Formal Methods Supplement to DO-178C",
            "FAA AC 20-115D - Airborne Software Development Assurance Using EUROCAE ED-12 and RTCA DO-178",
            "EASA AMC 20-115D - Airborne Software Assurance",
            "SAE ARP4754A - Guidelines for Development of Civil Aircraft and Systems (Software in Context)"
        ],
        issue_category=IssueCategory.SOFTWARE_CERTIFICATION,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Control Surface Flutter
    DoctrineBlock(
        topic="Control Surface Flutter Analysis and Prevention",
        keywords=["flutter", "aeroelastic", "divergence", "damping", "frequency", "V-g diagram"],
        conclusion_template="Flutter is self-excited aeroelastic oscillation that can lead to catastrophic structural failure. Prevention requires analysis of coupled structural/aerodynamic modes, demonstration of positive damping across flight envelope, and mass balancing of control surfaces.",
        reasoning_framework="""
CONTROL SURFACE FLUTTER - AEROELASTIC INSTABILITY:

1. Flutter Mechanism (Coupled Mode Instability):
   - Structural flexibility: Wing/tail/control surface bending and torsion
   - Aerodynamic forces: Lift and moment vary with surface motion
   - Inertial coupling: Mass distribution affects modal response
   - Positive feedback: Motion generates forces that amplify motion
   - Divergence: When aerodynamic damping becomes negative, oscillations grow exponentially

2. Classical Flutter (Bending-Torsion Coupling):
   - Wing bending mode (1st mode ~2-5 Hz) couples with torsion mode (1st mode ~5-10 Hz)
   - As airspeed increases, aerodynamic forces change phase relationship
   - Below flutter speed (V_F): Oscillations damped, stable
   - At flutter speed (V_F): Zero damping, sustained oscillation
   - Above flutter speed: Negative damping, divergent oscillation → structural failure

3. Control Surface Flutter (Aileron/Elevator/Rudder):
   - Control surface rotation couples with wing/tail bending and torsion
   - Hinge moment (aerodynamic force on control surface) drives rotation
   - Free-play in control linkage can reduce flutter margin
   - Mass imbalance creates inertial coupling with surface rotation
   - Tab flutter: Trim tab oscillation couples with main surface

4. Mass Balancing for Flutter Prevention:
   - Add mass forward of hinge line to move center-of-gravity closer to hinge
   - Reduces inertial coupling between surface rotation and wing bending
   - Typical mass balance: 20-40% of control surface weight
   - Balance weight mounted in leading edge of control surface
   - Reduces flutter speed sensitivity to hinge moment variations

5. Flutter Analysis Methods:
   - V-g Method: Plot damping (g) vs airspeed (V) for each mode
   - P-K Method: Eigenvalue solution of aeroelastic equations
   - Doublet-Lattice Method: Aerodynamic influence coefficients in frequency domain
   - CFD Coupling: High-fidelity aerodynamics for complex configurations
   - Wind tunnel testing: Scaled model flutter testing (must scale stiffness correctly)

6. Flutter Clearance Flight Testing:
   - Subcritical response method: Excite structure at progressively higher airspeeds
   - Monitor damping ratio: If damping decreases with speed, approaching flutter
   - Stop test at 15% margin below predicted flutter speed
   - Envelope expansion: Gradual increase in test speed with damping monitoring
   - Instrumentation: Accelerometers on wing, tail, control surfaces
   - Real-time analysis: FFT to identify frequencies and damping ratios

7. Certification Requirements (FAR 25.629):
   - Demonstrate freedom from flutter, divergence, and control reversal
   - Up to 1.15 * V_D (design dive speed) or M_D + 0.05 Mach
   - For all aircraft configurations (fuel levels, stores, flap positions)
   - Positive damping required at all speeds below clearance envelope
   - Analysis supplemented by wind tunnel and flight test

8. Flutter Suppression Systems (Advanced):
   - Active flutter suppression: Control surface actuated to add damping
   - Sensors detect wing/tail vibration, controller commands anti-phase motion
   - Can extend flutter boundary, reduce structural weight
   - Used on flexible/high-aspect-ratio wings (e.g., B-2, Global Hawk)
   - Must be fail-safe: Flutter boundary with system failed > V_D
        """,
        key_factors=[
            "Flutter is self-excited oscillation from coupling structural and aerodynamic modes",
            "Mass balancing of control surfaces reduces inertial coupling and raises flutter speed",
            "Free-play in control linkages reduces flutter margin and must be minimized",
            "V-g diagram plots damping vs airspeed to identify flutter speed",
            "Flight testing uses subcritical response method to verify flutter clearance",
            "Certification requires positive damping up to 1.15*V_D or M_D+0.05",
            "Active flutter suppression can extend envelope but must be fail-safe",
            "Wind tunnel testing requires correct scaling of stiffness and mass distribution"
        ],
        primary_authority=[
            "FAR 25.629 - Aeroelastic Stability Requirements",
            "FAA AC 25.629-1B - Means of Compliance with §25.629 Flutter",
            "EASA CS-25.629 - Aeroelastic Stability",
            "AGARD Manual on Aeroelasticity in Axial-Flow Turbomachines Volume 1 (NATO)",
            "Bisplinghoff, R.L. 'Aeroelasticity' Dover Publications (Classic Reference)"
        ],
        issue_category=IssueCategory.SURFACE_FLUTTER,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Regulatory Compliance
    DoctrineBlock(
        topic="FAR Part 25 Flight Control System Certification Requirements",
        keywords=["FAR 25.671", "FAR 25.677", "FAR 25.1309", "flight controls", "certification"],
        conclusion_template="FAR Part 25 Subpart D establishes certification requirements for transport category aircraft flight controls. Key regulations include §25.671 (control system design), §25.677 (trim systems), and §25.1309 (system safety analysis).",
        reasoning_framework="""
FAR PART 25 FLIGHT CONTROL CERTIFICATION REQUIREMENTS:

1. FAR 25.671 - Control Systems General:
   - (a) Each control and control system must operate with ease, smoothness, and positiveness
   - (b) Each element must be designed or protected to minimize jamming, catching, or interference
   - (c) Jamming, ground, and bending loads must not impair safe operation
   - (d) Operate without excessive friction or lost motion
   - Applies to: Primary flight controls (elevator, aileron, rudder) and trim systems

2. FAR 25.677 - Trim Systems:
   - (a) Trim controls must be located to provide convenient operation
   - (b) Trim systems must be designed to prevent inadvertent operation
   - (c) Trim must not move primary controls from neutral without pilot action
   - (d) Trim indicator must show direction and magnitude of trim
   - (e) If powered trim fails, manual trim must be available
   - Airbus/Boeing: Pitch trim via horizontal stabilizer, not elevator

3. FAR 25.679 - Control System Locks:
   - (a) Control locks (gust locks) must engage and release easily
   - (b) Locks must prevent flight with controls locked
   - (c) Visual and physical indication when locks engaged
   - Modern aircraft: Weight-on-wheels logic prevents takeoff with locks engaged

4. FAR 25.685 - Control System Details:
   - (a) Cables: Minimum breaking strength with factor of safety
   - (b) Cable systems: Drums, pulleys, fairleads must prevent jamming
   - (c) Irreversible systems: No aeroelastic feedback to pilot controls
   - (d) Limit stops: Prevent control surface over-travel
   - Fly-by-wire aircraft: Electronic limit stops in flight control computer

5. FAR 25.697 - Lift and Drag Devices:
   - (a) Flaps, slats, spoilers must be controllable by pilot
   - (b) Position indication required in cockpit
   - (c) Safe operation after single failure
   - (d) Asymmetric deployment must not prevent continued safe flight
   - Example: 737 MAX stabilizer runaway → loss of control (Lion Air 610, Ethiopian 302)

6. FAR 25.1309 - Equipment, Systems, and Installations:
   - (a) Systems must be designed so single failures do not prevent continued safe flight
   - (b) Catastrophic failure conditions: Extremely improbable (<10^-9 per flight hour)
   - (c) Hazardous failure conditions: Remote (<10^-7 per flight hour)
   - (d) Major failure conditions: Probable (<10^-5 per flight hour)
   - (e) Safety assessment: Fault Tree Analysis (FTA), Failure Mode Effects Analysis (FMEA)

7. FAR 25.1309 Application to Flight Controls:
   - Loss of all flight control: Catastrophic → <10^-9 (requires triple/quadruple redundancy)
   - Loss of one axis control: Hazardous → <10^-7 (requires dual redundancy minimum)
   - Degraded control (e.g., Alternate Law): Major → <10^-5 (acceptable single failure)
   - Common Cause Analysis: Identify potential common-mode failures (fire, debris, lightning)

8. CS-25 (EASA) vs FAR 25 Differences:
   - CS-25 generally harmonized with FAR 25
   - CS-25.1309 explicitly requires Common Cause Analysis
   - CS-25 AMC (Acceptable Means of Compliance) provides detailed guidance
   - Example: AMC 25.1309 references SAE ARP4754A and ARP4761

9. Special Conditions for Novel Designs:
   - Fly-by-wire aircraft: Special conditions issued (e.g., A320, 777, 787)
   - Flight envelope protection: Demonstrate equivalence to conventional handling
   - Degraded modes: Acceptable handling qualities in failure states
   - Software: DO-178C compliance for flight-critical software (DAL-A)

10. Flight Test Demonstration (FAR 25.21):
    - Controllability and maneuverability across weight, CG, configuration envelope
    - Stall characteristics (FAR 25.201-203)
    - Static longitudinal, lateral, directional stability (FAR 25.171-181)
    - Dynamic stability: Dutch roll, spiral, phugoid modes (FAR 25.181)
    - Trim capability in all flight phases (FAR 25.161)
        """,
        key_factors=[
            "FAR 25.671 requires flight controls operate with ease, smoothness, and positiveness",
            "FAR 25.1309 establishes failure probability requirements for system safety",
            "Catastrophic failures (loss of flight control) must be <10^-9 per flight hour",
            "Trim systems must prevent inadvertent operation and provide manual backup",
            "Asymmetric deployment of flaps/slats must not prevent continued safe flight",
            "Common Cause Analysis identifies potential common-mode failures",
            "Special conditions issued for novel designs like fly-by-wire systems",
            "Flight test demonstration required across full weight and CG envelope"
        ],
        primary_authority=[
            "14 CFR Part 25 Subpart D - Design and Construction (Flight Controls)",
            "FAR 25.671 - Control Systems General",
            "FAR 25.677 - Trim Systems",
            "FAR 25.1309 - Equipment, Systems, and Installations",
            "EASA CS-25 - Certification Specifications for Large Aeroplanes"
        ],
        issue_category=IssueCategory.REGULATORY_COMPLIANCE,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    # Failure Modes
    DoctrineBlock(
        topic="Runaway Stabilizer Failure Analysis",
        keywords=["runaway trim", "stabilizer", "737 MAX", "MCAS", "emergency procedures"],
        conclusion_template="Runaway stabilizer is uncommanded movement of horizontal stabilizer trim, causing pitch-up or pitch-down. Emergency procedure is: disengage autopilot, apply control column force, deactivate electric trim (cutout switches), manually trim using trim wheel.",
        reasoning_framework="""
RUNAWAY STABILIZER - FAILURE MODE AND RECOVERY:

1. Runaway Stabilizer Definition:
   - Horizontal stabilizer moves continuously in one direction without pilot command
   - Can be caused by: Electric trim motor failure, switch malfunction, software error
   - Pitch-down runaway: Stabilizer moves toward nose-down (leading edge down)
   - Pitch-up runaway: Stabilizer moves toward nose-up (leading edge up)
   - Boeing 737: Horizontal stabilizer provides primary pitch trim (not elevator trim)

2. 737 MAX MCAS System (Maneuvering Characteristics Augmentation System):
   - Designed to improve pitch-up tendency at high AoA in manual flight
   - Single AoA sensor input (design flaw)
   - Erroneous AoA → MCAS commands nose-down stabilizer trim
   - MCAS activates repeatedly, overpowering pilot elevator authority
   - Lion Air 610 (Oct 2018) and Ethiopian 302 (Mar 2019): Loss of control due to MCAS

3. Symptoms of Runaway Stabilizer:
   - Continuous motion of stabilizer position indicator
   - Increasing column force required to maintain pitch attitude
   - Trim wheel rotating continuously (visual/audible cue)
   - Aircraft pitching up or down despite pilot input
   - Control column force may exceed pilot strength if stabilizer at extreme position

4. Emergency Procedure (Boeing Non-Normal Checklist):
   - Step 1: Disengage autopilot (if engaged) - prevents autopilot masking runaway
   - Step 2: Apply FIRM control column force opposite to trim motion
   - Step 3: Deactivate STAB TRIM CUTOUT switches (two switches on center pedestal)
   - Step 4: Manually trim using STAB TRIM wheels (physical crank handles)
   - Step 5: Do NOT re-engage electric trim (stabilizer remains manually controlled)
   - Step 6: Land as soon as practical

5. Manual Trim Operation:
   - Trim wheels: Large diameter wheels on each side of center pedestal
   - Mechanical linkage: Direct cable connection to stabilizer jackscrew
   - High forces required: If stabilizer significantly out-of-trim, may need altitude/speed relief
   - Relief technique: Adjust power and pitch to reduce column force, then trim manually
   - One full turn of trim wheel ≈ 0.5-1.0 degree stabilizer movement

6. MCAS-Specific Recovery (Post-737 MAX Accidents):
   - Recognition: Repeated nose-down trim commands at 10-second intervals
   - Airspeed: MCAS only activates above certain speed and high AoA
   - Runaway Stabilizer procedure: Cutout switches disable MCAS
   - If electric trim cutout, MCAS cannot reactivate
   - Simulator training: Pilots now trained on MCAS failure mode

7. Design Improvements (737 MAX Post-Grounding):
   - Dual AoA sensor input to MCAS (no single-point failure)
   - MCAS limited to single activation per high-AoA event (no repeated trim)
   - Increased pilot authority over MCAS (column force can override)
   - AoA disagree alert made standard (previously optional)
   - Mandatory MCAS training for all 737 MAX pilots

8. Certification Lessons Learned:
   - Single-sensor dependency for flight-critical system: Unacceptable
   - System Safety Assessment must consider pilot response time and workload
   - Novel systems require explicit pilot training (cannot assume similarity to prior models)
   - Regulators must independently verify manufacturer analysis (not delegate entirely)
   - Common Cause Analysis: Software errors must be considered in FTA/FMEA
        """,
        key_factors=[
            "Runaway stabilizer causes continuous trim motion overpowering pilot elevator authority",
            "Emergency procedure: Disengage autopilot, oppose with column force, cutout switches, manual trim",
            "737 MAX MCAS relied on single AoA sensor - design flaw leading to two fatal crashes",
            "Manual trim using trim wheels requires high physical force if stabilizer out-of-trim",
            "Speed/altitude relief may be needed to reduce column force before manual trim",
            "Post-accident improvements: Dual AoA input, limited MCAS authority, mandatory training",
            "Certification process must verify single-sensor failures for flight-critical systems",
            "Pilot recognition and immediate action critical - delayed response may be unrecoverable"
        ],
        primary_authority=[
            "Boeing 737 Flight Crew Operations Manual - Runaway Stabilizer Procedure",
            "NTSB Aircraft Accident Report AAR-19/01 (Ethiopian Airlines Flight 302)",
            "Indonesian NTSC Final Report (Lion Air Flight 610)",
            "FAA AD 2018-23-51 (737 MAX MCAS Emergency Airworthiness Directive)",
            "Congressional Hearing Report on 737 MAX Certification (2020)"
        ],
        issue_category=IssueCategory.FAILURE_MODES,
        authority_level=AuthorityLevel.PRIMARY,
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
]

# ============================================================================
# TELEMETRY AND METRICS
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.latencies: List[float] = []
        self.errors = 0
        self.start_time = datetime.now(timezone.utc)
        self.doctrine_triggers: Dict[str, int] = {}

    def record_query(self, latency_ms: float, cache_hit: bool, doctrines: List[str], error: bool = False):
        self.total_queries += 1
        self.latencies.append(latency_ms)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        if error:
            self.errors += 1
        for doctrine in doctrines:
            self.doctrine_triggers[doctrine] = self.doctrine_triggers.get(doctrine, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        cache_hit_rate = self.cache_hits / self.total_queries if self.total_queries > 0 else 0
        error_rate = self.errors / self.total_queries if self.total_queries > 0 else 0

        return {
            "uptime_seconds": uptime,
            "total_queries": self.total_queries,
            "cache_hit_rate": cache_hit_rate,
            "avg_latency_ms": avg_latency,
            "error_rate": error_rate,
            "doctrine_triggers": self.doctrine_triggers
        }

telemetry = TelemetryCollector()

# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def normalize_query(query: str) -> str:
    """Semantic normalization of query terms."""
    query_lower = query.lower()

    # Flight control term normalization
    replacements = {
        "fbw": "fly-by-wire",
        "fcc": "flight control computer",
        "pha": "power-by-wire hydraulic actuator",
        "aoa": "angle-of-attack",
        "sas": "stability augmentation system",
        "ils": "instrument landing system",
        "cat ii": "category ii",
        "cat iii": "category iii",
        "cat 2": "category ii",
        "cat 3": "category iii",
        "vnav": "vertical navigation",
        "lnav": "lateral navigation",
        "rnp": "required navigation performance",
        "mcas": "maneuvering characteristics augmentation system",
    }

    for old, new in replacements.items():
        query_lower = query_lower.replace(old, new)

    return query_lower

def calculate_doctrine_relevance(query: str, doctrine: DoctrineBlock) -> float:
    """Calculate relevance score for a doctrine block."""
    query_normalized = normalize_query(query)
    query_terms = set(query_normalized.lower().split())

    score = 0.0

    # Keyword matching
    for keyword in doctrine.keywords:
        if keyword.lower() in query_normalized:
            score += 3.0

    # Topic matching
    if doctrine.topic.lower() in query_normalized:
        score += 5.0

    # Term overlap
    doctrine_terms = set(doctrine.reasoning_framework.lower().split())
    overlap = len(query_terms.intersection(doctrine_terms))
    score += overlap * 0.1

    return score

def search_doctrines(query: str, top_k: int = 3) -> List[Tuple[DoctrineBlock, float]]:
    """Search doctrine cache for relevant blocks."""
    query_normalized = normalize_query(query)

    scored_doctrines = []
    for doctrine in DOCTRINE_CACHE:
        relevance = calculate_doctrine_relevance(query_normalized, doctrine)
        if relevance > 0:
            scored_doctrines.append((doctrine, relevance))

    scored_doctrines.sort(key=lambda x: x[1], reverse=True)
    return scored_doctrines[:top_k]

def generate_answer(query: str, doctrines: List[Tuple[DoctrineBlock, float]], mode: ResponseMode, zone: PositionZone) -> Tuple[str, ConfidenceLevel, List[str]]:
    """Generate answer based on triggered doctrines and response mode."""
    if not doctrines:
        return (
            "No relevant flight control systems doctrine found for this query. Please consult appropriate aerospace engineering references or FAA/EASA regulations.",
            ConfidenceLevel.DISCLOSURE,
            []
        )

    primary_doctrine = doctrines[0][0]
    confidence = primary_doctrine.confidence
    citations = primary_doctrine.primary_authority.copy()

    if mode == ResponseMode.FAST:
        answer = f"{primary_doctrine.conclusion_template}\n\nKey Factors:\n"
        for factor in primary_doctrine.key_factors[:3]:
            answer += f"- {factor}\n"

    elif mode == ResponseMode.DEFENSE:
        answer = f"ANALYSIS: {primary_doctrine.topic}\n\n"
        answer += f"{primary_doctrine.conclusion_template}\n\n"
        answer += "REASONING:\n"
        answer += primary_doctrine.reasoning_framework[:1000] + "...\n\n"
        answer += "KEY FACTORS:\n"
        for i, factor in enumerate(primary_doctrine.key_factors, 1):
            answer += f"{i}. {factor}\n"
        answer += "\nAUTHORITY:\n"
        for citation in primary_doctrine.primary_authority:
            answer += f"- {citation}\n"

    else:  # MEMO
        answer = f"MEMORANDUM - {primary_doctrine.topic}\n"
        answer += "=" * 70 + "\n\n"
        answer += f"ISSUE CATEGORY: {primary_doctrine.issue_category.value}\n"
        answer += f"CONFIDENCE LEVEL: {confidence.value}\n"
        answer += f"POSITION ZONE: {zone.value}\n\n"
        answer += "CONCLUSION:\n"
        answer += primary_doctrine.conclusion_template + "\n\n"
        answer += "DETAILED ANALYSIS:\n"
        answer += primary_doctrine.reasoning_framework + "\n\n"
        answer += "KEY FACTORS:\n"
        for i, factor in enumerate(primary_doctrine.key_factors, 1):
            answer += f"{i}. {factor}\n"
        answer += "\nPRIMARY AUTHORITY:\n"
        for citation in primary_doctrine.primary_authority:
            answer += f"- {citation}\n"

        if len(doctrines) > 1:
            answer += "\nRELATED DOCTRINES:\n"
            for doc, score in doctrines[1:]:
                answer += f"- {doc.topic} (relevance: {score:.1f})\n"

    return answer, confidence, citations

def compute_determinism_hash(query: str, answer: str, mode: ResponseMode) -> str:
    """Compute SHA-256 hash for determinism verification."""
    content = f"{query}|{answer}|{mode.value}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def log_audit_trail(query: str, response: QueryResponse):
    """Log query and response to JSONL audit trail."""
    audit_entry = {
        "timestamp": response.timestamp,
        "query": query,
        "mode": response.mode.value,
        "zone": response.zone.value,
        "confidence": response.confidence.value,
        "doctrines_triggered": response.doctrines_triggered,
        "determinism_hash": response.determinism_hash,
        "latency_ms": response.latency_ms
    }

    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(audit_entry) + "\n")

async def vector_search_fallback(query: str) -> str:
    """Fallback to semantic vector search if cache miss."""
    # Placeholder for actual vector DB integration
    return "Vector search not yet implemented. Please refine query or consult doctrine cache."

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=ENGINE_NAME,
    description="Flight Control Systems Intelligence Engine - TIE Architecture",
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    logger.info(f"{ENGINE_NAME} v{VERSION} starting on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    metrics = telemetry.get_metrics()

    return HealthResponse(
        status="healthy",
        engine_id=ENGINE_ID,
        version=VERSION,
        uptime_seconds=metrics["uptime_seconds"],
        total_queries=metrics["total_queries"],
        cache_hit_rate=metrics["cache_hit_rate"],
        avg_latency_ms=metrics["avg_latency_ms"],
        doctrines_loaded=len(DOCTRINE_CACHE),
        error_rate=metrics["error_rate"]
    )

@app.post("/query", response_model=QueryResponse)
async def query_engine(request: QueryRequest):
    """Main query endpoint - three-layer response architecture."""
    start_time = datetime.now(timezone.utc)

    try:
        # Layer 1: Doctrine Cache (0-200ms)
        doctrines = search_doctrines(request.query, top_k=3)
        cache_hit = len(doctrines) > 0

        # Layer 2: Semantic Retrieval (if cache miss)
        if not cache_hit:
            fallback_answer = await vector_search_fallback(request.query)
            answer = fallback_answer
            confidence = ConfidenceLevel.DISCLOSURE
            citations = []
            doctrines_triggered = []
        else:
            # Generate answer from doctrines
            answer, confidence, citations = generate_answer(
                request.query, doctrines, request.mode, request.zone
            )
            doctrines_triggered = [d[0].topic for d in doctrines]

        # Compute determinism hash
        det_hash = compute_determinism_hash(request.query, answer, request.mode)

        # Calculate latency
        latency_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

        response = QueryResponse(
            query=request.query,
            answer=answer,
            mode=request.mode,
            zone=request.zone,
            confidence=confidence,
            doctrines_triggered=doctrines_triggered,
            authority_citations=citations,
            determinism_hash=det_hash,
            latency_ms=latency_ms,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

        # Record telemetry
        telemetry.record_query(latency_ms, cache_hit, doctrines_triggered)

        # Log audit trail
        log_audit_trail(request.query, response)

        return response

    except Exception as e:
        logger.error(f"Query processing error: {e}")
        telemetry.record_query(0, False, [], error=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/metrics")
async def get_metrics():
    """Retrieve telemetry metrics."""
    return telemetry.get_metrics()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {ENGINE_NAME} v{VERSION}")
    logger.info(f"Doctrine cache: {len(DOCTRINE_CACHE)} blocks")
    logger.info(f"Port: {PORT}")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
