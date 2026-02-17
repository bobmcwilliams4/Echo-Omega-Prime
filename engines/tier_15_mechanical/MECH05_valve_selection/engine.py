"""
MECH05 - Valve Selection & Sizing Intelligence Engine
Mechanical Engineering - Control & Isolation Valves

TIE Gold Standard Implementation
Port: 9045
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

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
    CONTROL_VALVE_SIZING = "CONTROL_VALVE_SIZING"
    VALVE_TYPE_SELECTION = "VALVE_TYPE_SELECTION"
    ACTUATOR_SELECTION = "ACTUATOR_SELECTION"
    SAFETY_RELIEF_SIZING = "SAFETY_RELIEF_SIZING"
    MATERIAL_SELECTION = "MATERIAL_SELECTION"
    VALVE_NOISE = "VALVE_NOISE"
    CAVITATION_FLASHING = "CAVITATION_FLASHING"
    FUGITIVE_EMISSIONS = "FUGITIVE_EMISSIONS"
    FIRE_SAFE_DESIGN = "FIRE_SAFE_DESIGN"
    WELLHEAD_VALVES = "WELLHEAD_VALVES"
    MAINTENANCE_TESTING = "MAINTENANCE_TESTING"
    PRESSURE_REGULATION = "PRESSURE_REGULATION"

class AnalysisZone(str, Enum):
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"

class QueryRequest(BaseModel):
    query: str = Field(..., description="Valve engineering question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    mode: ResponseMode
    doctrine_topics: List[str]
    issue_categories: List[str]
    determinism_hash: str
    latency_ms: float
    zone: AnalysisZone

class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    issue_categories: int
    uptime_seconds: float

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════

class DoctrineBlock:
    """Valve engineering expertise block"""
    def __init__(
        self,
        topic: str,
        keywords: List[str],
        conclusion_template: List[str],
        reasoning_framework: str,
        key_factors: List[str],
        primary_authority: List[str],
        burden_holder: str,
        adversary_position: str,
        counter_arguments: List[str],
        resolution_strategy: str,
        entity_scope: str,
        confidence: ConfidenceLevel,
        confidence_stratification: str,
        controlling_precedent: str,
        zone: AnalysisZone = AnalysisZone.PLANNING
    ):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.burden_holder = burden_holder
        self.adversary_position = adversary_position
        self.counter_arguments = counter_arguments
        self.resolution_strategy = resolution_strategy
        self.entity_scope = entity_scope
        self.confidence = confidence
        self.confidence_stratification = confidence_stratification
        self.controlling_precedent = controlling_precedent
        self.zone = zone
        self.access_count = 0
        self.last_accessed: Optional[datetime] = None

# ═══════════════════════════════════════════════════════════════════════════
# DOCTRINE CACHE - 25+ REAL VALVE ENGINEERING BLOCKS
# ═══════════════════════════════════════════════════════════════════════════

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Control Valve Cv Sizing per ISA-75.01.01",
        keywords=["cv", "control valve", "sizing", "flow coefficient", "ISA", "IEC 60534"],
        conclusion_template=[
            "For {fluid_type} at {flow_rate} {units}, pressure drop {delta_p} psi, the required Cv is {cv_value}.",
            "Valve should be sized to operate at {percent_open}% open at normal flow to allow control range.",
            "Use ISA-75.01.01 equation: Cv = Q × sqrt(SG / ΔP) for liquids, Cv = Q × sqrt((SG × T) / (ΔP × P1)) for gases."
        ],
        reasoning_framework="""
        ISA-75.01.01 and IEC 60534 define standard sizing equations:
        - Liquids (non-choked): Cv = Q × sqrt(SG / ΔP) where Q=gpm, SG=specific gravity, ΔP=psi
        - Gases (subsonic): Cv = Q × sqrt((SG × T) / (520 × ΔP × P1)) where Q=scfh, T=°R, P1=psia upstream
        - Choked flow: occurs when ΔP exceeds FL²(P1 - FF×Pv) for liquids or pressure ratio exceeds Fγ×xt
        - Normal operating point should be 60-80% of full Cv to allow turndown and control
        - Oversizing causes instability, undersizing limits capacity
        - Account for piping reducers with Fp factor
        """,
        key_factors=[
            "Fluid type and properties (SG, viscosity, vapor pressure)",
            "Flow rate (normal, max, min) and units",
            "Upstream and downstream pressures",
            "Temperature effects on gas density",
            "Choked flow conditions (cavitation for liquids, sonic velocity for gases)",
            "Required rangeability and turndown ratio",
            "Piping geometry factor (Fp) for reducers"
        ],
        primary_authority=[
            "ISA-75.01.01 (ANSI/ISA-75.01.01-2012) - Flow Equations for Sizing Control Valves",
            "IEC 60534-2-1 - Industrial-process control valves - Flow capacity - Sizing equations for fluid flow",
            "NFPA 99 - Health Care Facilities Code (medical gas valve sizing)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may suggest oversized valve for wider product range applicability",
        counter_arguments=[
            "Oversized valves operate near seat, causing instability and wear",
            "Undersized valves cannot pass required flow at low differential",
            "Ignoring choked flow leads to noise, vibration, and damage",
            "Failing to account for turndown causes poor control at low flows",
            "Incorrect specific gravity for mixtures or varying compositions"
        ],
        resolution_strategy="Calculate Cv at normal, max, and min flow conditions. Select valve with Cv such that normal flow is 70% of rated Cv. Verify no choked flow at max ΔP. Check turndown ratio meets process requirements (typical 50:1 for good control valves).",
        entity_scope="All fluid services requiring throttling control",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ISA and IEC standards are consensus-based and universally accepted in industry",
        controlling_precedent="ISA-75.01.01-2012 Clause 3.2 Liquid Flow Equations",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Globe Valve vs Butterfly Valve Selection",
        keywords=["globe", "butterfly", "valve type", "selection", "shutoff", "throttling"],
        conclusion_template=[
            "For {service} service with {pressure_class} pressure and {size} line size, {valve_type} valve is recommended.",
            "Globe valves provide tighter shutoff (Class IV-VI) and better throttling control.",
            "Butterfly valves offer lower cost and pressure drop but limited shutoff (Class III-IV) and flow characteristics."
        ],
        reasoning_framework="""
        Globe valves:
        - Excellent throttling control with linear or equal percentage characteristics
        - Tight shutoff: ANSI Class IV (0.01% of Cv), Class V (5×10⁻⁵ ml/min/in), Class VI (bubbles)
        - High pressure drop (useful for pressure reduction)
        - Higher cost, larger actuator force required
        - Preferred for: critical control, high pressure drop, tight shutoff

        Butterfly valves (per API 609):
        - Low cost, compact, lightweight
        - Low pressure drop (Cv/D² ratio ~20-30 vs globe ~10)
        - Limited shutoff: typically Class III-IV (0.1% leakage)
        - Nonlinear flow characteristic (high gain near closed position)
        - Torque increases rapidly at high differential pressures
        - Preferred for: on/off service, large lines (>6 inch), low ΔP systems
        """,
        key_factors=[
            "Required shutoff class per ANSI/FCI 70-2",
            "Control precision vs on/off service",
            "Pressure drop budget",
            "Line size and cost sensitivity",
            "Actuator size and force requirements",
            "Flow characteristic linearity needs"
        ],
        primary_authority=[
            "ANSI/FCI 70-2 - Control Valve Seat Leakage",
            "API 609 - Butterfly Valves: Double Flanged, Lug- and Wafer-Type",
            "ISA-75.25.01 - Control Valve Diagnostic Data Acquisition"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor prefers butterfly valves for higher margins in large sizes",
        counter_arguments=[
            "Butterfly valves cannot achieve Class V/VI shutoff",
            "Globe valves have higher installed cost (valve + larger actuator)",
            "Butterfly high-gain near-closed causes control instability",
            "Globe valves create excessive pressure drop in low-ΔP systems",
            "Butterfly disc in flow path causes wear and failure in dirty service"
        ],
        resolution_strategy="Use globe for: control loops requiring <1% error, shutoff Class V+, erosive service. Use butterfly for: on/off isolation, low-pressure systems, large diameter (>12 inch), clean service. For 6-12 inch control, evaluate Cv/cost tradeoff.",
        entity_scope="General process control and isolation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API and ANSI standards clearly define performance classes and applications",
        controlling_precedent="API 609 Section 6.2 Seat Tightness",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Safety Relief Valve Sizing per API 520",
        keywords=["PRV", "safety", "relief", "API 520", "overpressure", "set pressure", "ASME"],
        conclusion_template=[
            "For {scenario} overpressure scenario, required relief area is {area} in² at {set_pressure} psig set pressure.",
            "Use API 520 Part I equation with {correction_factor} correction and {backpressure}% backpressure.",
            "ASME VIII allows {accumulation}% accumulation for {service} service (10% fire, 16% single contingency, 21% multiple)."
        ],
        reasoning_framework="""
        API 520 Part I sizing procedure:
        1. Determine relieving scenarios: fire, blocked outlet, cooling failure, tube rupture, runaway reaction
        2. Calculate required relieving rate (mass or volume flow)
        3. Select set pressure: typically MAWP or slightly below (95-98% MAWP)
        4. Determine allowable accumulation: 10% (fire), 16% (single contingency), 21% (multiple devices)
        5. Calculate relieving pressure = set + accumulation + overpressure
        6. Size orifice area using API 520 equations with correction factors (Kb, Kc, Kd, Kv, Kw)
        7. Select standard orifice per API 526 (D through T)
        8. Verify backpressure does not exceed 10% (conventional) or allowable (balanced bellows)
        9. Check inlet pressure drop <3% of set pressure
        10. Calculate reaction force on discharge piping

        Critical corrections:
        - Kb (backpressure correction for balanced bellows PRVs)
        - Kc (combination correction for pilot-operated)
        - Kw (backpressure correction for rupture disk upstream)
        - Kd (discharge coefficient, typically 0.975 for gas, 0.65 for liquid)
        """,
        key_factors=[
            "Overpressure scenario (fire, blocked outlet, etc.)",
            "Fluid properties at relieving conditions (MW, Z, k, Cp/Cv)",
            "Set pressure relative to MAWP",
            "Allowable accumulation per ASME VIII",
            "Backpressure (built-up + superimposed)",
            "Inlet pressure drop",
            "PRV type (conventional, balanced bellows, pilot-operated)",
            "Rupture disk upstream presence"
        ],
        primary_authority=[
            "API 520 Part I - Sizing, Selection, and Installation of Pressure-relieving Devices (Fire and Vapor)",
            "API 521 - Pressure-relieving and Depressuring Systems",
            "ASME BPVC Section VIII Div 1 - Pressure Vessels (overpressure limits)",
            "API 526 - Flanged Steel Pressure-relief Valves (standard orifice sizes)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may suggest oversized PRV for conservative margin, causing chattering",
        counter_arguments=[
            "Undersizing leads to overpressure beyond Code limits",
            "Oversizing causes chattering and premature failure",
            "Ignoring backpressure causes PRV to not fully open",
            "Incorrect relieving temperature affects gas density/viscosity",
            "Failing to account for two-phase flow in liquid service"
        ],
        resolution_strategy="Calculate required area for each credible scenario. Select smallest orifice that covers worst case with <10% margin. Verify backpressure, inlet drop, reaction forces. For fire case, use API 521 heat input (21,000 BTU/hr/ft² for insulated vessels). Document basis in relief device datasheet.",
        entity_scope="Pressure vessels, piping systems, storage tanks per ASME VIII",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 520/521 and ASME VIII are legal Code requirements for pressure relief",
        controlling_precedent="API 520 Part I Section 3.6 Required Capacity Determination",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Equal Percentage vs Linear Control Valve Characteristics",
        keywords=["equal percentage", "linear", "quick opening", "inherent characteristic", "installed characteristic"],
        conclusion_template=[
            "For {process_type} with {pressure_drop_variation}, use {characteristic_type} characteristic.",
            "Equal percentage compensates for varying pressure drop in liquid level and flow control.",
            "Linear characteristic suitable for constant ΔP applications like pressure control."
        ],
        reasoning_framework="""
        Inherent valve characteristics (constant ΔP across valve):

        1. Equal Percentage (log):
           - Flow increases exponentially with stroke
           - Equation: Q/Qmax = R^((L-1)) where R=rangeability (20-50), L=stroke fraction
           - Small changes at low flows, large changes at high flows
           - Compensates for ΔP variation as valve opens (ΔPvalve decreases, system ΔP increases)
           - Preferred for: liquid level control, flow control, most processes where ΔPvalve >> system ΔP at closed

        2. Linear:
           - Flow proportional to stroke: Q = Qmax × L
           - Equal incremental flow change per stroke increment
           - Preferred for: pressure control (ΔP constant), bypass control, split-range applications

        3. Quick Opening:
           - Maximum flow change near closed position
           - Used for on/off service, not modulating control

        Installed characteristic differs from inherent due to:
        - System pressure drop in series with valve
        - If ΔPvalve @ full open << total system ΔP, equal percentage becomes more linear
        - If ΔPvalve @ full open >> system ΔP, linear becomes more equal percentage
        """,
        key_factors=[
            "Process type (level, flow, pressure, temperature)",
            "Pressure drop split: valve vs system",
            "Rangeability requirement",
            "System dynamics and lag time",
            "Control loop gain variation acceptable",
            "Interaction with controller tuning"
        ],
        primary_authority=[
            "ISA-75.01.01 - Control Valve Sizing Equations (Appendix B Characteristics)",
            "IEC 60534-2-3 - Flow capacity - Test procedures (characteristic curves)",
            "Valve Handbook by Skousen (industry reference)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor stocks linear cages and may push for simplicity",
        counter_arguments=[
            "Equal percentage in constant-ΔP systems causes nonlinear installed characteristic",
            "Linear in varying-ΔP systems causes high loop gain at low flow",
            "Ignoring installed characteristic leads to unstable control",
            "Wrong characteristic requires detuning controller, reducing performance"
        ],
        resolution_strategy="Calculate valve ΔP at full open and compare to system ΔP. If ratio <0.3 (valve drop is <30% of total), equal percentage approaches linear installed. For typical liquid level/flow control where ratio >0.5, use equal percentage. For pressure control where ratio <0.2, use linear.",
        entity_scope="All modulating control valves",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ISA and IEC standards define characteristic curves; application guidelines are consensus-based",
        controlling_precedent="ISA-75.01.01 Appendix B Flow Characteristics",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Pneumatic vs Electric Actuator Selection",
        keywords=["actuator", "pneumatic", "electric", "fail-safe", "stroking time", "MOV"],
        conclusion_template=[
            "For {valve_size} valve in {location} requiring {fail_mode}, use {actuator_type} actuator.",
            "Pneumatic actuators provide fail-safe action and fast stroking for ESD valves.",
            "Electric actuators offer precise positioning and no air supply requirement for remote locations."
        ],
        reasoning_framework="""
        Pneumatic actuators:
        - Intrinsically fail-safe (spring return to fail position on air loss)
        - Fast stroking (1-3 seconds typical for ESD valves)
        - Simple, rugged, proven technology
        - Require instrument air supply (clean, dry, 40-80 psig)
        - Lower initial cost for small/medium valves
        - Torque/thrust proportional to air pressure (positioners modulate)
        - Ideal for: emergency shutdown (ESD), fire-safe areas, fail-safe critical

        Electric actuators (MOV - Motor Operated Valve):
        - Precise positioning (0.1% repeatability with digital controllers)
        - No air supply required (ideal for remote locations)
        - Fail-in-place or battery backup for fail-safe (adds cost)
        - Slower stroking (10-60 seconds typical)
        - Higher torque capacity for large valves (>12 inch)
        - Lower lifecycle cost (no air compressor/dryer maintenance)
        - Diagnostic capability (torque profiling, partial stroke testing)
        - Ideal for: remote sites, precise control, large valves, no air available

        Hydraulic actuators (rare):
        - Very high force for large high-pressure valves
        - Used in subsea and special applications
        """,
        key_factors=[
            "Fail-safe requirement (fail-closed, fail-open, fail-in-place)",
            "Stroking time requirement (ESD valves need <5 seconds)",
            "Instrument air availability and quality",
            "Valve size and required torque/thrust",
            "Hazardous area classification (pneumatic is simpler for Class I Div 1)",
            "Positioning accuracy requirement",
            "Location remoteness (no air for offshore/desert)",
            "Lifecycle cost (air system vs electrical maintenance)"
        ],
        primary_authority=[
            "ISA-75.25.01 - Control Valve Diagnostic Data (actuator diagnostics)",
            "API 6D - Pipeline Valves (actuator requirements)",
            "IEC 60534-6 - Mounting details for attachment of positioners to control valves"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor prefers electric for higher margin and add-on diagnostics",
        counter_arguments=[
            "Pneumatic requires air compressor, dryer, and distribution (capex + maintenance)",
            "Electric fail-safe requires battery/UPS (single point of failure)",
            "Pneumatic lacks precise positioning for tight control",
            "Electric is too slow for emergency shutdown applications",
            "Hydraulic systems are complex and leak-prone"
        ],
        resolution_strategy="For ESD/safety valves in plants with air systems: use pneumatic spring-return. For remote locations without air: use electric with battery backup if fail-safe needed. For large throttling valves (>12 inch): evaluate electric for torque capacity. For precise control loops: electric or pneumatic with digital positioner.",
        entity_scope="All automated valves requiring actuators",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry consensus based on decades of experience; API and ISA standards provide guidance",
        controlling_precedent="API 6D Section 6.4 Actuator Requirements",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="NACE MR0175 Material Selection for Sour Service",
        keywords=["sour service", "H2S", "NACE", "MR0175", "ISO 15156", "sulfide stress cracking"],
        conclusion_template=[
            "For sour service with {h2s_partial_pressure} psia H2S, use materials per NACE MR0175/ISO 15156.",
            "Valve body and trim must meet Severity Level {level} requirements.",
            "Carbon steel limited to <22 HRC hardness; austenitic stainless or nickel alloys preferred for trim."
        ],
        reasoning_framework="""
        NACE MR0175/ISO 15156 covers materials for H2S-containing environments to prevent sulfide stress cracking (SSC).

        Severity levels based on H2S partial pressure and pH:
        - Level 0: <0.05 psia H2S (sweet service, no special requirements)
        - Level I: 0.05-1.5 psia H2S
        - Level II: 1.5-30 psia H2S
        - Level III: >30 psia H2S or pH <4

        Acceptable materials:
        - Carbon steel: limited to <22 HRC (Rockwell C) hardness, annealed/normalized condition
        - Low alloy steel: specific grades per MR0175 Table A.2 (e.g., F22 Cl.3 <22 HRC)
        - Austenitic stainless (316, 317, 6Mo): acceptable for most sour service (22-28 HRC max)
        - Duplex stainless (2205, 2507): acceptable with restrictions on hardness and temperature
        - Nickel alloys (625, 825, C-276): preferred for severe sour and high chloride
        - Trim materials: avoid martensitic stainless (hardness >22 HRC); use stellite, tungsten carbide, or ceramic

        Special considerations:
        - Hardness testing required on trim and body (critical for SSC resistance)
        - Electroplating and hard-facing acceptable if per MR0175 requirements
        - Elastomers: HNBR, FFKM acceptable; nitrile NBR generally not
        """,
        key_factors=[
            "H2S partial pressure (psia)",
            "Total pressure and temperature",
            "pH and chloride content",
            "Hardness of body and trim materials (<22 HRC critical)",
            "Valve trim type and hardness",
            "Elastomer compatibility",
            "Welding and heat treatment effects on hardness"
        ],
        primary_authority=[
            "NACE MR0175/ISO 15156 - Materials for Use in H2S-Containing Environments in Oil and Gas Production",
            "API 6A - Wellhead and Christmas Tree Equipment (sour service requirements)",
            "ASME B16.34 - Valves-Flanged, Threaded, and Welding End (material standards)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may offer non-compliant materials to reduce cost or lead time",
        counter_arguments=[
            "Carbon steel >22 HRC will crack in sour service (catastrophic failure)",
            "Electroless nickel plating can be acceptable if per MR0175 (hardness <22 HRC equivalent)",
            "Duplex stainless has temperature limits (avoid >450°F in sour service)",
            "Ignoring pH can lead to cracking even at low H2S",
            "Non-compliant elastomers swell and fail in sour service"
        ],
        resolution_strategy="Calculate H2S partial pressure from mol% and total pressure. Determine severity level. Select body material per MR0175 Table A.2 (carbon steel <22 HRC, or stainless/nickel alloy). Select trim material (stellite, tungsten carbide, or austenitic stainless <28 HRC). Specify hardness testing on MTRs. Verify elastomers are NACE-compliant (HNBR, FFKM).",
        entity_scope="Oil and gas production valves exposed to H2S",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="NACE MR0175/ISO 15156 is legal requirement in oil and gas industry; violations lead to failures and liability",
        controlling_precedent="NACE MR0175/ISO 15156-1 Section 5 Material Requirements",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="API 6A Wellhead and Christmas Tree Valve Requirements",
        keywords=["API 6A", "wellhead", "christmas tree", "oilfield", "PSL", "PR", "temperature class"],
        conclusion_template=[
            "For wellhead service at {pressure} psi and {temp}°F, use API 6A PSL {psl} rated valves.",
            "Pressure rating PR{pr} with temperature class U (-75 to +250°F) or higher required.",
            "Gate valves must meet API 6A pressure testing and material requirements."
        ],
        reasoning_framework="""
        API 6A defines wellhead and Christmas tree equipment for oil and gas wells.

        Product Specification Level (PSL):
        - PSL 1: basic quality, minimal testing
        - PSL 2: intermediate quality, additional NDE
        - PSL 3: highest quality, full NDE, material traceability (critical sour service)
        - PSL 3G: PSL 3 with gas testing instead of hydrostatic

        Pressure Rating (PR):
        - PR1 = 2,000 psi, PR2 = 3,000 psi, PR3 = 5,000 psi, PR4 = 10,000 psi
        - PR5 = 15,000 psi, PR6 = 20,000 psi

        Temperature Classes:
        - Class K: -60°F to 180°F
        - Class L: -75°F to 180°F
        - Class N: 0°F to 250°F
        - Class P: -15°F to 250°F
        - Class S: -60°F to 250°F
        - Class T: -75°F to 250°F
        - Class U: -75°F to 350°F (most common)

        Material Classes:
        - AA, BB, CC, DD, EE, FF (different metallurgy for sour/sweet service)

        Testing requirements:
        - Body pressure test: 1.5 × rated pressure
        - Seat leakage test: rated pressure (gas or liquid)
        - PSL 3 requires NDE (RT or UT) on critical pressure boundaries
        """,
        key_factors=[
            "Wellhead pressure (maximum anticipated surface pressure)",
            "Temperature range (min/max operating)",
            "Sour service (H2S content determines PSL and material class)",
            "Product Specification Level (PSL 1/2/3/3G)",
            "Valve type (gate, ball, check)",
            "End connections (flanged, threaded, welded)",
            "Testing requirements (pressure, NDE)"
        ],
        primary_authority=[
            "API 6A - Wellhead and Christmas Tree Equipment",
            "API 6AV1 - Validation of API 6A Standard",
            "ASME BPVC Section VIII - Pressure Vessels (design principles apply)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may offer lower PSL or PR to reduce cost",
        counter_arguments=[
            "PSL 1 lacks NDE and traceability (unacceptable for critical wells)",
            "Undersized PR leads to overpressure and failure",
            "Wrong temperature class causes brittle fracture (low temp) or creep (high temp)",
            "Sour service without PSL 3 and proper material class leads to SSC",
            "Ignoring API 6A testing leads to seat leakage and well control issues"
        ],
        resolution_strategy="Determine maximum wellhead pressure (reservoir pressure × safety factor, typically 1.1-1.25). Select PR equal or next higher. Determine temperature range (wellbore temp, ambient extremes). Select temp class. For sour service (H2S >0.05 psia): specify PSL 3, material class EE/FF, NACE MR0175 compliance. For sweet service: PSL 2 acceptable, material class AA/BB.",
        entity_scope="Wellhead and Christmas tree valves for oil and gas wells",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 6A is legal standard for wellhead equipment; violations cause well control incidents",
        controlling_precedent="API 6A Section 4 Design Requirements",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Valve Noise Prediction per IEC 60534-8-3",
        keywords=["noise", "aerodynamic", "IEC 60534", "sound pressure", "dBA", "cavitation noise"],
        conclusion_template=[
            "For {fluid_type} at {delta_p} psi pressure drop, predicted valve noise is {noise_level} dBA at 1 meter.",
            "Exceeds {limit} dBA limit; use multi-stage trim or silencer to reduce noise to acceptable level.",
            "IEC 60534-8-3 Method B predicts noise from flow velocity and turbulence."
        ],
        reasoning_framework="""
        IEC 60534-8-3 provides methods for predicting valve aerodynamic noise:

        Method A (Simplified):
        - Based on pressure drop ratio and flow coefficient
        - Accuracy ±5 dBA
        - Equation: SPL = 10 × log10(Pv × ΔP × Cv) + C1 + C2

        Method B (Detailed):
        - Accounts for valve geometry, trim type, and flow regime
        - Accuracy ±3 dBA
        - Requires vendor data on Fp, xt, FL factors

        Noise generation mechanisms:
        - Turbulence (predominant): pressure drop converts to kinetic energy, then turbulent dissipation
        - Sonic velocity (choked flow): shock waves when ΔP exceeds critical
        - Cavitation (liquids): bubble collapse creates shock waves (can exceed 100 dBA)

        Noise limits:
        - OSHA: 90 dBA for 8-hour exposure, 85 dBA preferred
        - ISO 3746: environmental limits 55-75 dBA depending on area
        - Typical plant: target <85 dBA at 1 meter from valve

        Noise reduction methods:
        - Multi-stage trim: divides ΔP into multiple stages (10-15 dBA reduction per stage)
        - Cage trim with tortuous path: increases throttling stages
        - Downstream diffusers and silencers: absorb sound energy (10-20 dBA reduction)
        - Heavy-wall body: increases transmission loss (5-10 dBA reduction)
        - Low-noise valve types: labyrinth, stacked-disk designs
        """,
        key_factors=[
            "Pressure drop and flow rate",
            "Fluid type (gas noise is dominant issue)",
            "Valve style and trim type",
            "Downstream pipe diameter and length",
            "Distance to nearest personnel",
            "Acceptable noise limit (regulatory and operational)",
            "Cavitation presence (for liquids)"
        ],
        primary_authority=[
            "IEC 60534-8-3 - Industrial-process control valves - Noise considerations - Control valve aerodynamic noise prediction method",
            "IEC 60534-8-4 - Prediction of noise generated by hydrodynamic flow (cavitation)",
            "OSHA 1910.95 - Occupational Noise Exposure"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may underpredict noise to sell standard trim instead of expensive multi-stage",
        counter_arguments=[
            "Underpredicted noise leads to OSHA violations and hearing damage",
            "Cavitation noise can exceed 110 dBA (causes valve and piping damage, not just hearing risk)",
            "Ignoring downstream piping length affects noise (longer pipe = more attenuation)",
            "Multi-stage trim costs 2-4× standard but may be only solution for high-ΔP gas",
            "Silencers add pressure drop (must account for in system design)"
        ],
        resolution_strategy="Calculate noise using IEC 60534-8-3 Method B (or vendor software). If >85 dBA: specify multi-stage trim (2-stage for 85-95 dBA, 3-stage for 95-105 dBA, 4+ stages for >105 dBA). For extreme cases (>110 dBA), add downstream silencer. Verify with vendor acoustic calculation per IEC standard. Document in valve datasheet.",
        entity_scope="All control valves with significant pressure drop, especially gas service",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="IEC 60534-8-3 is internationally recognized prediction method; OSHA noise limits are legal requirements",
        controlling_precedent="IEC 60534-8-3 Section 3 Prediction Method",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Cavitation and Flashing in Control Valves",
        keywords=["cavitation", "flashing", "vapor pressure", "FL", "FF", "choked flow", "erosion"],
        conclusion_template=[
            "For {liquid} at {pressure} psia and {temp}°F, {phenomenon} occurs when ΔP exceeds {threshold} psi.",
            "Cavitation causes noise, vibration, and erosive damage to valve trim and body.",
            "Use multi-stage trim or increase downstream pressure to suppress cavitation."
        ],
        reasoning_framework="""
        Cavitation vs Flashing in liquids:

        Cavitation:
        - Pressure in vena contracta drops below vapor pressure (Pv)
        - Vapor bubbles form, then collapse when pressure recovers downstream
        - Collapse creates shock waves (noise >100 dBA, vibration, erosion)
        - Damage typically at valve seat and downstream body
        - Occurs when: ΔP > FL²(P1 - FF×Pv) and P2 > Pv

        Flashing:
        - Pressure drops below vapor pressure and stays below
        - Liquid converts to vapor permanently (two-phase flow)
        - High velocity, erosion, but no bubble collapse noise
        - Occurs when: P2 < Pv

        Predicting cavitation:
        - Cavitation index σ = (P2 - Pv) / ΔP
        - Incipient cavitation: σ < σi (typically 1.5-3.0)
        - Constant cavitation: σi < σ < σc (noise increases)
        - Choked cavitation: σ > σc (maximum noise, erosion)
        - Use ISA-75.01.01 FL and FF factors (vendor-supplied)

        Mitigation strategies:
        1. Increase P2 (downstream pressure): most effective
        2. Multi-stage trim: divide ΔP into stages, keep local pressure >Pv
        3. Use hardened trim materials: stellite, tungsten carbide (resist erosion)
        4. Avoid high recovery valves (low FL): globe preferred over ball/butterfly
        5. Limit velocity <100 ft/s in vena contracta
        """,
        key_factors=[
            "Liquid vapor pressure at operating temperature",
            "Upstream pressure P1 and downstream pressure P2",
            "Pressure drop ΔP",
            "Valve recovery factor FL (globe ~0.9, ball ~0.6)",
            "Piping geometry factor FF",
            "Trim hardness and material",
            "Velocity in vena contracta"
        ],
        primary_authority=[
            "ISA-75.01.01 - Flow Equations for Sizing Control Valves (cavitation criteria)",
            "IEC 60534-8-4 - Prediction of noise generated by hydrodynamic flow",
            "ANSI/ISA-75.02 - Control Valve Capacity Test Procedures (FL determination)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may claim standard trim is adequate to avoid expensive multi-stage trim",
        counter_arguments=[
            "Cavitation damage can destroy valve in days/weeks",
            "Noise from cavitation exceeds 100 dBA (OSHA violation, personnel risk)",
            "Flashing causes two-phase flow instability and control loop oscillation",
            "Standard trim (stainless) erodes rapidly; hardened trim essential",
            "Ignoring cavitation leads to unscheduled shutdowns and safety incidents"
        ],
        resolution_strategy="Calculate cavitation index σ. If σ <2.0, cavitation is likely. Options: (1) Increase P2 by raising control valve outlet pressure (add backpressure valve or redesign system). (2) Use multi-stage trim (anti-cavitation cage). (3) Use hardened trim (stellite 6 or tungsten carbide). (4) For unavoidable flashing, design for two-phase flow and use erosion-resistant materials. Document in valve datasheet.",
        entity_scope="All liquid control valves with high pressure drop",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ISA and IEC standards define cavitation criteria; physics of bubble collapse is well-understood",
        controlling_precedent="ISA-75.01.01 Section 3.3.3 Pressure Drop Limitation (cavitation)",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Fugitive Emissions Standards for Valve Packing",
        keywords=["fugitive emissions", "packing", "ISO 15848", "API 622", "API 624", "methane", "VOC"],
        conclusion_template=[
            "For {service} service, valve packing must meet {standard} leakage rate of <{rate} ppm.",
            "Use graphite or PTFE packing with live-loading for low-emission performance.",
            "Test per ISO 15848 or API 624 to verify <100 ppm leakage (Class A)."
        ],
        reasoning_framework="""
        Fugitive emissions regulations (EPA LDAR, EU VOC Directive) require low-emission packing:

        Standards:
        - ISO 15848-1: Fugitive Emissions from Valves - Measurement, test, and qualification (most stringent)
        - API 622: Type Testing of Process Valve Packing for Fugitive Emissions
        - API 624: Type Testing of Rising Stem Valves Equipped with Graphite Packing for Fugitive Emissions
        - EPA Method 21: Determination of VOC leaks (≥10,000 ppm = leak)

        Classification (ISO 15848):
        - Class A: <100 ppm (most stringent)
        - Class B: 100-500 ppm
        - Class C: >500 ppm
        - Endurance: CO1 (500 cycles), CO2 (2500 cycles), CO3 (10,000 cycles)

        Low-emission packing types:
        - Braided graphite: most common, temperature to 1200°F, chemical resistant
        - PTFE (Teflon): low friction, temperature to 500°F, good for low-torque valves
        - Graphite/PTFE composite: combines benefits
        - Live-loading (spring-energized): maintains packing compression as graphite creeps

        Design features:
        - Minimum 5 packing rings (prefer 7)
        - Lantern ring for injection of sealant (optional)
        - Extended bonnet for cryogenic service (keeps packing warm)
        - Live-loading springs to compensate for packing relaxation
        """,
        key_factors=[
            "Fluid toxicity and volatility (determines Class A/B/C requirement)",
            "Operating temperature and pressure",
            "Stem movement frequency (cycling affects packing wear)",
            "Regulatory requirement (EPA, EU, company policy)",
            "Packing type and arrangement",
            "Live-loading presence",
            "Testing and certification to ISO 15848 or API 622/624"
        ],
        primary_authority=[
            "ISO 15848-1 - Industrial valves - Measurement, test and qualification procedures for fugitive emissions - Part 1: Classification system and qualification procedures for type testing of valves",
            "API 622 - Type Testing of Process Valve Packing for Fugitive Emissions",
            "API 624 - Type Testing of Rising Stem Valves Equipped with Graphite Packing for Fugitive Emissions",
            "EPA Method 21 - Determination of Volatile Organic Compound Leaks"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may offer standard packing without low-emission certification to reduce cost",
        counter_arguments=[
            "Standard PTFE packing leaks >1000 ppm (EPA violation)",
            "Graphite without live-loading relaxes over time (leakage increases)",
            "Insufficient packing rings (less than 5) cannot seal reliably",
            "Uncertified packing has no performance guarantee",
            "Regulatory fines for fugitive emissions exceed cost of low-emission packing"
        ],
        resolution_strategy="For VOC or toxic services: specify ISO 15848 Class A (<100 ppm) or API 622/624 certified packing. Use braided graphite with live-loading (7 rings minimum). For non-toxic, non-regulated services: standard PTFE or graphite acceptable. Verify vendor provides test certificate per ISO or API standard. Include packing specification in valve datasheet.",
        entity_scope="All process valves in chemical plants, refineries, gas plants with emissions regulations",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ISO 15848 and API 622/624 are internationally recognized standards; EPA Method 21 is legal requirement",
        controlling_precedent="ISO 15848-1 Section 5 Classification System",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Fire-Safe Valve Design per API 607",
        keywords=["fire safe", "API 607", "fire test", "seat leakage", "soft seat", "metal seat"],
        conclusion_template=[
            "For fire-safe requirement, valve must pass API 607 fire test with <{leakage} cc/min/in seat leakage.",
            "Use metal-seated or graphite-sealed design that maintains integrity at {test_temp}°F.",
            "Soft-seated valves fail in fire; specify metal seats for critical isolation."
        ],
        reasoning_framework="""
        API 607 defines fire testing for soft-seated quarter-turn valves (ball, butterfly):

        Fire test procedure:
        1. Cycle valve 310 times at ambient to verify initial tightness
        2. Subject valve to 1550°F flame for 30 minutes (simulates pool fire)
        3. Cool with water spray
        4. Test seat leakage (gas or liquid) at rated pressure
        5. Acceptable leakage: varies by size (e.g., <40 cc/min for 2-inch, <400 cc/min for 12-inch)

        Design requirements:
        - Soft seats (PTFE, Nylon) burn away in fire → must have secondary metal seat
        - Metal seats: 316SS, stellite, or tungsten carbide seating surface
        - Body-to-bonnet seal: graphite spiral-wound gasket (survives fire; PTFE does not)
        - Stem seal: graphite packing (PTFE burns away)
        - Body-to-ball/disc seal: graphite or metal C-ring
        - Fire-safe certification required for each valve size and pressure class

        Applications requiring fire-safe:
        - Hydrocarbon isolation valves in process areas
        - Emergency shutdown (ESD) valves in fire zones
        - Tank farm isolation valves
        - Offshore platforms (high fire risk)

        Non-fire-safe alternatives:
        - Soft-seated valves acceptable in non-fire areas (lower cost, better shutoff)
        - Double block and bleed (DBB) with one fire-safe valve provides redundancy
        """,
        key_factors=[
            "Fire risk in installation area",
            "Fluid hazard (flammable, toxic)",
            "Isolation criticality (ESD vs normal)",
            "Valve type (ball, butterfly, gate)",
            "Seat type (soft or metal)",
            "Body-to-bonnet and stem seal materials",
            "API 607 certification from manufacturer"
        ],
        primary_authority=[
            "API 607 - Fire Test for Quarter-Turn Valves and Valves Equipped with Nonmetallic Seats",
            "API 6FA - Fire Test for Valves (alternative standard)",
            "BS 6755 - Specification for testing of valves - Part 2: Fire type-testing requirements"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may offer soft-seated valve (lower cost) without fire-safe certification",
        counter_arguments=[
            "Soft-seated valves fail catastrophically in fire (seat burns, massive leakage)",
            "API 607 testing is expensive; vendor may skip to reduce cost",
            "Metal seats have higher leakage at ambient (Class III-IV vs Class VI for soft)",
            "Fire-safe design adds cost (graphite seals, metal seats)",
            "False sense of security if not all sealing elements are fire-rated (e.g., PTFE bonnet gasket)"
        ],
        resolution_strategy="For hydrocarbon isolation in fire zones: specify API 607 fire-tested valve with metal seats and graphite seals. For non-fire areas: soft-seated acceptable (better shutoff, lower cost). For critical ESD: require API 607 certificate for exact valve size and class. Verify all sealing elements (seats, gaskets, packing) are rated for fire exposure.",
        entity_scope="Isolation valves in hydrocarbon and chemical plants with fire risk",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 607 is industry-standard fire test; insurance and regulations often require fire-safe valves in hazardous areas",
        controlling_precedent="API 607 Section 5 Fire Test Procedure",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Choke Valve Sizing for Oilfield Production",
        keywords=["choke", "oilfield", "multiphase", "flow bean", "erosion", "API 14B"],
        conclusion_template=[
            "For {flow_rate} BPD oil + {gor} GOR at {upstream_pressure} psi, choke size is {choke_size} inch.",
            "Use tungsten carbide trim to resist erosive multiphase flow.",
            "Calculate using multiphase flow correlation (API 14B or proprietary)."
        ],
        reasoning_framework="""
        Oilfield choke valves control wellhead pressure and flow rate:

        Flow regimes:
        - Single-phase liquid: use standard Cv equation
        - Single-phase gas: use ISA gas equation with critical flow factor
        - Multiphase (oil + gas + water): empirical correlations required

        Multiphase sizing methods:
        - API 14B: provides correlations for oil/gas/water mixtures (limited accuracy)
        - Sachdeva correlation: widely used in industry software
        - Perkins correlation: simplified for high GOR wells
        - Vendor software (e.g., Emerson, Cameron): proprietary multiphase models

        Critical flow (choked):
        - Occurs when downstream pressure <0.5 × upstream pressure (approximate)
        - Flow rate becomes independent of downstream pressure
        - Sonic velocity reached in choke throat

        Choke types:
        - Fixed choke (flow bean): replaceable orifice, sizes 1/4" to 2"
        - Adjustable choke: variable orifice, remote or manual actuation
        - Positive choke: cage-style with multiple flow paths

        Erosion considerations:
        - Sand production requires tungsten carbide or ceramic trim (not stainless)
        - Velocity in throat <300 ft/s to limit erosion (API 14E guideline)
        - Avoid sharp edges (use streamlined flow paths)
        - Replaceable trim for high-wear service
        """,
        key_factors=[
            "Oil, gas, water flow rates",
            "Gas-oil ratio (GOR) and water cut",
            "Upstream and downstream pressures",
            "Fluid properties (density, viscosity, compressibility)",
            "Sand production (erosion risk)",
            "Fixed vs adjustable choke requirement",
            "Trim material (stainless, stellite, tungsten carbide, ceramic)"
        ],
        primary_authority=[
            "API 14B - Recommended Practice for Design, Installation, and Operation of Subsurface Safety Valve Systems (choke sizing)",
            "API 14E - Recommended Practice for Design and Installation of Offshore Production Platform Piping Systems (erosion velocity)",
            "ISO 10423 - Petroleum and natural gas industries - Drilling and production equipment - Wellhead and christmas tree equipment"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may suggest stainless steel trim (lower cost) instead of tungsten carbide",
        counter_arguments=[
            "Multiphase flow is complex; single-phase equations underpredict pressure drop",
            "Undersized choke causes excessive backpressure on well (reduces production)",
            "Oversized choke loses control of well (safety risk)",
            "Stainless steel erodes in weeks with sand production; tungsten carbide lasts years",
            "Ignoring critical flow leads to unstable control and slugging"
        ],
        resolution_strategy="Use multiphase flow software (or API 14B correlations) to calculate required choke size for operating conditions. Select next larger standard size. For sand production >0.1% by weight: specify tungsten carbide or ceramic trim. For critical wells (high H2S, high pressure): use adjustable choke with remote actuation. Verify throat velocity <300 ft/s per API 14E.",
        entity_scope="Wellhead chokes in oil and gas production",
        confidence=ConfidenceLevel.AGGRESSIVE,
        confidence_stratification="API 14B correlations have ±20% accuracy; proprietary multiphase models are better but not standardized",
        controlling_precedent="API 14B Section 3 Flow Performance Calculations",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Pressure Regulating Valve Selection and Sizing",
        keywords=["pressure regulator", "PRV", "pilot operated", "direct acting", "self-actuated", "dome loaded"],
        conclusion_template=[
            "For {application} with inlet {p1} psi and setpoint {p2} psi, use {regulator_type} pressure regulator.",
            "Direct-acting suitable for low flow and <2:1 pressure ratio; pilot-operated for high flow and accuracy.",
            "Size for {flow_rate} at {pressure_drop} psi drop with {droop}% droop acceptable."
        ],
        reasoning_framework="""
        Pressure regulators (self-actuated control valves) maintain downstream pressure:

        Types:
        1. Direct-acting (spring-loaded):
           - Spring opposes diaphragm actuated by downstream pressure
           - Simple, no external power required
           - Limited accuracy (±10% droop typical)
           - Pressure ratio limited to 2:1 or 3:1
           - Flow capacity limited by diaphragm area
           - Applications: low flow, non-critical pressure control

        2. Pilot-operated (dome-loaded):
           - External pilot senses downstream pressure and loads dome above main diaphragm
           - High accuracy (±1% droop possible)
           - High pressure ratio (10:1 or higher)
           - Large flow capacity (up to 10,000 scfm or more)
           - Applications: gas pressure regulation, critical control

        3. Back-pressure regulator:
           - Maintains upstream pressure (reverses direct-acting design)
           - Used for vapor recovery, tank blanketing

        Sizing considerations:
        - Droop: pressure decreases as flow increases (inherent to self-actuated)
           Droop % = (Pset @ no flow - Pactual @ max flow) / Pset × 100
        - Lock-up: pressure rises above setpoint when flow stops (spring compression)
        - Capacity: size for maximum flow at minimum inlet pressure
        - Turndown: ratio of max to min controllable flow (typically 10:1 to 100:1)

        Applications:
        - Natural gas distribution: pilot-operated for accurate pressure control
        - Building gas supply: direct-acting acceptable
        - Instrument air: pilot-operated for precision
        - Fuel gas to burners: direct-acting or pilot-operated depending on criticality
        """,
        key_factors=[
            "Required downstream pressure setpoint and tolerance",
            "Inlet pressure range (min and max)",
            "Flow rate range (min, normal, max)",
            "Acceptable droop and lock-up",
            "Pressure ratio (P1/P2)",
            "Fluid type (gas, liquid, steam)",
            "Accuracy requirement",
            "Relief capacity (for overpressure protection)"
        ],
        primary_authority=[
            "ASME B16.44 - Manually Operated Metallic Gas Valves for Use in Above Ground Piping Systems up to 125 psig",
            "API 14H - Recommended Practice for Installation, Maintenance, and Repair of Surface Safety Valves and Underwater Safety Valves Offshore"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may oversell pilot-operated (higher margin) when direct-acting is adequate",
        counter_arguments=[
            "Direct-acting has excessive droop for tight tolerance applications",
            "Pilot-operated is overkill for low-flow, non-critical service",
            "Undersized regulator causes downstream pressure droop and process upset",
            "Oversized regulator operates near-closed (instability, hunting)",
            "Failing to account for lock-up can overpressure downstream equipment"
        ],
        resolution_strategy="Calculate required capacity at maximum flow and minimum inlet pressure. Determine acceptable droop (±1% for critical, ±10% for non-critical). Select direct-acting for: low flow (<1000 scfm gas), pressure ratio <3:1, droop <10% acceptable. Select pilot-operated for: high flow, pressure ratio >3:1, droop <2% required. Size per vendor curves with 10-20% margin. Verify lock-up pressure does not exceed downstream equipment rating.",
        entity_scope="Gas distribution, instrument air, fuel gas, liquid pressure control",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard practice; regulator performance is well-characterized by manufacturers",
        controlling_precedent="Manufacturer capacity curves and droop specifications",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Gate Valve vs Ball Valve for Isolation Service",
        keywords=["gate valve", "ball valve", "isolation", "API 6D", "API 600", "bidirectional", "full bore"],
        conclusion_template=[
            "For {service} isolation in {size} line, {valve_type} valve is recommended.",
            "Gate valves provide low pressure drop and bidirectional flow; ball valves offer faster actuation and tighter shutoff.",
            "API 6D pipeline valves meet {pressure_class} and fire-safe requirements."
        ],
        reasoning_framework="""
        Gate valves (API 600, API 602, API 6D):
        - Rising or non-rising stem
        - Full-bore (no flow restriction when open)
        - Low pressure drop (Cv/D² ~25-30)
        - Slow actuation (many turns to open/close)
        - Excellent for large sizes (>12 inch, up to 60+ inch)
        - Bidirectional flow capability
        - Wedge or parallel slide gates
        - Prone to galling and seizure if cycled frequently
        - Applications: main line isolation, infrequent operation

        Ball valves (API 6D, API 608):
        - Quarter-turn (90° rotation to open/close)
        - Full-bore or reduced-bore (reduced-bore has lower Cv)
        - Fast actuation (ideal for ESD)
        - Tight shutoff (Class VI possible with soft seats)
        - Fire-safe designs available (metal seats per API 607)
        - Higher torque required (especially at high differential pressure)
        - Limited to ~48 inch (larger sizes are rare and expensive)
        - Trunnion-mounted (for large sizes/high pressure) or floating ball (small sizes)
        - Applications: ESD valves, frequent on/off cycling, tight shutoff

        Comparison for pipeline isolation:
        - Gate valve: traditional choice for large pipelines, low cost, proven reliability
        - Ball valve: modern preference for faster actuation, better shutoff, reduced maintenance
        - API 6D covers both types for pipeline service
        """,
        key_factors=[
            "Line size (gate preferred >24 inch)",
            "Cycling frequency (ball for frequent, gate for infrequent)",
            "Shutoff tightness requirement (ball tighter)",
            "Actuation speed requirement (ball faster)",
            "Pressure drop budget (both are low-drop)",
            "Fire-safe requirement (both available)",
            "Cost (gate cheaper for large sizes)"
        ],
        primary_authority=[
            "API 6D - Pipeline Valves (gate and ball valves)",
            "API 600 - Steel Gate Valves - Flanged and Butt-welding Ends, Bolted Bonnets",
            "API 608 - Metal Ball Valves - Flanged, Threaded, and Welding Ends"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor prefers ball valves for higher margin; gate valves are commodity",
        counter_arguments=[
            "Gate valves seize if not exercised regularly (stem/wedge galling)",
            "Ball valves have higher torque (larger actuators required)",
            "Soft-seated ball valves fail in fire (need metal seats for fire-safe)",
            "Reduced-bore ball valves increase velocity and erosion",
            "Gate valves are slower to close (not suitable for ESD)"
        ],
        resolution_strategy="For main pipeline isolation (infrequent operation, >24 inch): use API 6D gate valve. For ESD or frequent cycling: use API 6D ball valve (full-bore, trunnion-mounted for >6 inch). For fire-safe requirement: specify API 607 certified ball valve or gate valve with appropriate seals. For <6 inch: ball valve is cost-competitive and offers better shutoff.",
        entity_scope="Pipeline isolation, process isolation, on/off service",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 6D, 600, and 608 are well-established standards with decades of field experience",
        controlling_precedent="API 6D Section 6 Design Requirements",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Check Valve Selection and Slam Prevention",
        keywords=["check valve", "non-return", "slam", "API 594", "swing check", "wafer check", "dual plate"],
        conclusion_template=[
            "For {application} at {flow_rate} and {pressure} psi, use {check_type} check valve.",
            "Swing check has low pressure drop but risks slam; spring-loaded or dual-plate check prevents slam.",
            "Calculate deceleration time to verify slam risk per API 594."
        ],
        reasoning_framework="""
        Check valve types (per API 594):

        1. Swing check:
           - Disc swings on hinge pin
           - Full-bore, very low pressure drop (Cv/D² ~20)
           - Prone to slam if flow decelerates rapidly (water hammer)
           - Large sizes (up to 60 inch)
           - Applications: pump discharge (with slow-closing feature), gravity flow

        2. Tilting disc:
           - Similar to swing but disc tilts at center pivot
           - Faster closing, less slam tendency
           - Moderate pressure drop

        3. Dual plate (wafer):
           - Two semicircular discs spring-loaded to close
           - Fast closing, minimal slam
           - Compact (wafer style fits between flanges)
           - Moderate pressure drop
           - Sizes 2-72 inch
           - Applications: pump discharge, compressor discharge, general non-return

        4. Lift check (piston):
           - Disc lifts vertically (like globe valve)
           - High pressure drop (like globe valve)
           - Positive seating, good for high-pressure steam
           - Must be installed vertically (flow upward)

        5. Spring-loaded check:
           - Any of above with spring to assist closing
           - Prevents slam by closing before flow reversal
           - Higher cracking pressure (reduces efficiency)

        Slam (water hammer):
        - Occurs when check valve closes too slowly during flow reversal
        - Reverse flow accelerates, then disc slams shut → pressure surge
        - Pressure spike can exceed 10× normal (causes pipe and valve failure)
        - Calculate deceleration time: Δt = (2 × L × V) / (a × g) where L=pipe length, V=velocity, a=wave speed
        - If Δt < closing time, slam will occur

        Slam prevention:
        - Use spring-loaded check (closes before reverse flow)
        - Use dual-plate wafer check (fast closing)
        - Use slow-closing swing check (dampened closing)
        - Install check valve close to pump (short deceleration column)
        """,
        key_factors=[
            "Flow rate and velocity",
            "Pressure and pressure drop budget",
            "Pump/compressor discharge (high slam risk) vs gravity flow",
            "Pipe length and deceleration time",
            "Cracking pressure (spring-loaded checks require higher pressure to open)",
            "Installation orientation (horizontal vs vertical)",
            "Size and cost"
        ],
        primary_authority=[
            "API 594 - Check Valves: Flanged, Lug, Wafer and Butt-welding",
            "ASME B16.34 - Valves-Flanged, Threaded, and Welding End (pressure-temperature ratings)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may sell swing check (lowest cost) without analyzing slam risk",
        counter_arguments=[
            "Swing check slam can destroy valve and pipe in single event",
            "Spring-loaded checks reduce pump efficiency (higher cracking pressure)",
            "Dual-plate checks cost 2-3× swing check",
            "Lift checks have high pressure drop (unacceptable in low-head systems)",
            "Ignoring slam analysis leads to catastrophic failures and safety incidents"
        ],
        resolution_strategy="For pump discharge: calculate deceleration time. If <1 second, use spring-loaded or dual-plate check. For long pipelines (>1000 ft): swing check may slam; use dual-plate or slow-closing swing check. For vertical flow (upward): lift check is acceptable. For low pressure drop critical: swing check with slam analysis. Install check valve within 10 pipe diameters of pump discharge to minimize deceleration column.",
        entity_scope="All piping systems requiring backflow prevention",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 594 is industry standard; slam analysis is well-established fluid mechanics",
        controlling_precedent="API 594 Section 6 Backflow Prevention Requirements",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Valve Body Material Selection for Temperature Service",
        keywords=["body material", "ASTM", "low temperature", "high temperature", "carbon steel", "stainless steel", "impact testing"],
        conclusion_template=[
            "For {service} at {temperature}°F, use {material} body material per ASME B16.34.",
            "Low-temperature service below {mdmt}°F requires impact testing per ASME B31.3.",
            "High-temperature service above 800°F requires creep-resistant alloy steel."
        ],
        reasoning_framework="""
        Valve body material selection per ASME B16.34 and ASTM standards:

        Temperature ranges:
        - Cryogenic (<-50°F): stainless steel (304, 316, 304L, 316L) or nickel alloys
        - Low temp (-50 to 100°F): carbon steel with impact testing, or stainless steel
        - Ambient (100-400°F): carbon steel (WCB, LCB, WCC)
        - Elevated (400-800°F): carbon steel or low-alloy steel (WC6, WC9)
        - High temp (800-1100°F): chrome-moly steel (C5, C12, F11, F22)
        - Very high (>1100°F): austenitic stainless (F304, F316, F321, F347)

        Low-temperature considerations:
        - Carbon steel becomes brittle below MDMT (Minimum Design Metal Temperature)
        - MDMT depends on material and thickness (thinner = lower MDMT)
        - Impact testing (Charpy V-notch) required per ASME B31.3 to verify toughness
        - Exemptions from impact testing per B31.3 Fig 323.2.2A (based on thickness and temperature)
        - Stainless steel (austenitic) has excellent low-temp toughness (no MDMT limit)

        High-temperature considerations:
        - Carbon steel loses strength above 800°F (creep becomes significant)
        - Chrome-moly alloys resist creep (1Cr-0.5Mo, 2.25Cr-1Mo, etc.)
        - Austenitic stainless for >1100°F but requires thermal expansion allowances
        - Avoid mixed materials (carbon + stainless) due to differential expansion

        Common materials (ASTM):
        - A216 WCB: carbon steel, -20 to 800°F
        - A216 LCC: carbon steel, -50 to 650°F (low-temp)
        - A352 LCB: carbon steel, -50 to 650°F (low-temp, impact tested)
        - A217 WC6: 1.25Cr-0.5Mo, -20 to 1000°F
        - A217 WC9: 2.25Cr-1Mo, -20 to 1100°F
        - A351 CF8M: 316 stainless, -425 to 1500°F
        """,
        key_factors=[
            "Operating temperature (min and max)",
            "Pressure rating (impacts wall thickness, affects MDMT)",
            "Corrosion environment (may require stainless or alloy)",
            "Thermal cycling (affects creep and fatigue)",
            "Impact testing requirement and exemptions",
            "Cost (carbon steel cheapest, stainless/alloy expensive)"
        ],
        primary_authority=[
            "ASME B16.34 - Valves-Flanged, Threaded, and Welding End (material selection)",
            "ASME B31.3 - Process Piping (impact testing requirements, MDMT)",
            "ASTM A216 - Standard Specification for Steel Castings, Carbon, Suitable for Fusion Welding, for High-Temperature Service"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may offer carbon steel without verifying low-temp impact testing requirement",
        counter_arguments=[
            "Carbon steel at low temp without impact testing risks brittle fracture",
            "Stainless steel costs 3-5× carbon steel (may be unnecessary)",
            "High-temp carbon steel creeps and fails (must use chrome-moly)",
            "Ignoring thermal expansion in mixed materials causes leakage and cracking",
            "Wrong material leads to premature failure and safety incidents"
        ],
        resolution_strategy="Determine min and max operating temperatures. For <-20°F: use stainless steel or impact-test carbon steel per B31.3. For -20 to 800°F: carbon steel WCB. For 800-1100°F: chrome-moly WC9 (2.25Cr-1Mo). For >1100°F: austenitic stainless CF8M. Verify MDMT on material test report. For corrosive service, upgrade to stainless or alloy regardless of temperature.",
        entity_scope="All valve body material selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ASME B16.34 and B31.3 are legal Code requirements; ASTM material standards are consensus-based",
        controlling_precedent="ASME B16.34 Table 1 Material Grouping and Temperature Limits",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Valve End Connection Selection: Flanged vs Threaded vs Welded",
        keywords=["end connection", "flanged", "threaded", "butt weld", "socket weld", "ASME B16.5", "ASME B16.11"],
        conclusion_template=[
            "For {size} valve at {pressure_class} in {service}, use {end_connection} end connections.",
            "Flanged connections allow disassembly; welded connections provide leak-tight permanent joint.",
            "Threaded connections limited to ≤2 inch and ≤600 psig per ASME B31.3."
        ],
        reasoning_framework="""
        End connection types:

        1. Flanged (ASME B16.5, B16.47):
           - Removable (maintenance, replacement)
           - Gasket seal (potential leak path)
           - Flange classes: 150, 300, 600, 900, 1500, 2500 (pressure-temperature rated)
           - Available in all sizes (1/2" to 60"+)
           - Higher cost (valve + flanges + bolts + gasket)
           - Applications: general process, where disassembly expected

        2. Butt-weld (ASME B16.25):
           - Permanent, leak-tight (no gasket)
           - Requires welding (qualified welder, weld procedure)
           - Full penetration weld (high integrity)
           - Must cut pipe to remove valve (maintenance downtime)
           - Lower cost (no flanges)
           - Applications: critical service, high pressure/temp, underground, no disassembly

        3. Socket-weld (ASME B16.11):
           - Similar to butt-weld but socket joint (easier fit-up)
           - Limited to ≤4 inch and ≤Class 3000
           - Fillet weld (lower integrity than butt-weld)
           - Crevice corrosion risk (gap behind socket)
           - Applications: small bore, high pressure, where butt-weld is difficult

        4. Threaded (ASME B1.20.1 NPT):
           - Removable with thread sealant/tape
           - Limited to ≤2 inch and ≤600 psig per ASME B31.3
           - Leak risk (threads are tapered, rely on sealant)
           - Stress concentration at threads (vibration/fatigue risk)
           - No welding required (easy installation)
           - Applications: low-pressure, small-bore, temporary, non-critical

        Selection guidelines:
        - >2 inch: flanged or welded (not threaded)
        - Critical service (fire, toxic, flammable): welded preferred
        - High vibration: welded (threaded can leak)
        - High pressure (>600 psig): flanged or welded
        - Underground/buried: welded (no leak path)
        - Maintenance frequency: flanged if frequent, welded if infrequent
        """,
        key_factors=[
            "Valve size",
            "Pressure and temperature rating",
            "Fluid hazard (flammable, toxic)",
            "Maintenance frequency (disassembly need)",
            "Installation location (underground, overhead)",
            "Vibration and fatigue",
            "Cost and schedule (welding time vs flange cost)"
        ],
        primary_authority=[
            "ASME B16.5 - Pipe Flanges and Flanged Fittings",
            "ASME B16.11 - Forged Fittings, Socket-Welding and Threaded",
            "ASME B16.25 - Buttwelding Ends",
            "ASME B31.3 - Process Piping (limitations on threaded connections)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor prefers flanged (higher selling price with flanges included)",
        counter_arguments=[
            "Flanged connections leak (gasket degradation, bolt relaxation)",
            "Welded connections require cutting for maintenance (downtime)",
            "Threaded connections leak under vibration and thermal cycling",
            "Socket-weld has crevice corrosion risk (not suitable for corrosive service)",
            "Butt-weld requires qualified welders (higher labor cost)"
        ],
        resolution_strategy="For ≤2 inch non-critical: threaded acceptable if low vibration and <600 psig. For 2-4 inch: flanged (if maintenance access needed) or socket-weld (if permanent). For >4 inch: flanged (if disassembly expected) or butt-weld (if critical/permanent). For underground/high-hazard: butt-weld. For offshore/high-vibration: welded or special flange (RTJ gasket).",
        entity_scope="All valve installations requiring end connection selection",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ASME B16 and B31.3 standards define connection types and limitations; decades of field experience",
        controlling_precedent="ASME B31.3 Section 314.2.1 Threaded Joint Limitations",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Valve Stem Sealing: Packing vs Bellows Seal",
        keywords=["stem seal", "packing", "bellows", "hermetic", "leak-tight", "fugitive emissions", "zero leakage"],
        conclusion_template=[
            "For {service} with {emission_requirement}, use {seal_type} stem seal.",
            "Bellows seal valves provide hermetic seal (zero leakage) but are expensive and limited in size.",
            "Packing seals require maintenance but are cost-effective for most services."
        ],
        reasoning_framework="""
        Stem sealing methods:

        1. Packing seal (conventional):
           - Braided packing rings compressed in stuffing box
           - Requires periodic adjustment (packing wears and relaxes)
           - Leakage: 100-1000 ppm (standard packing), <100 ppm (low-emission packing)
           - Low cost, proven technology
           - All sizes available
           - Live-loading optional (spring maintains compression)
           - Applications: general process, where <500 ppm leakage acceptable

        2. Bellows seal (hermetic):
           - Metal bellows (welded to stem and bonnet) forms pressure boundary
           - Zero leakage (hermetic seal, no dynamic seal)
           - Backup packing for bellows failure protection
           - High cost (2-4× conventional valve)
           - Limited sizes (typically ≤4 inch, up to 12 inch special)
           - Limited stroke (bellows has finite extension cycles, typically 10,000-50,000)
           - Pressure and temperature limits (bellows material and fatigue)
           - Applications: toxic, radioactive, ultra-pure (semiconductor, pharma), vacuum

        3. Diaphragm seal:
           - Flexible diaphragm seals stem (no packing)
           - Zero leakage on stem (but limited stroke and pressure)
           - Diaphragm is wear item (replace periodically)
           - Limited to low pressure (<300 psi) and small stroke
           - Applications: corrosive service, slurries, where packing contamination is unacceptable

        Selection guidelines:
        - Toxic/radioactive: bellows seal (zero leakage)
        - Fugitive emissions <100 ppm: low-emission packing (ISO 15848 Class A)
        - High cycling (>10,000 cycles): packing (bellows fatigue limit)
        - Large valves (>12 inch): packing only (bellows unavailable)
        - High temperature (>800°F): packing (bellows limited to ~650°F)
        - Cost-sensitive: packing
        """,
        key_factors=[
            "Fluid toxicity and emissions regulations",
            "Leakage tolerance (ppm)",
            "Valve size and stroke length",
            "Operating temperature and pressure",
            "Cycling frequency (bellows fatigue)",
            "Maintenance capability (packing adjustment)",
            "Cost budget"
        ],
        primary_authority=[
            "ISO 15848-1 - Fugitive Emissions from Valves (packing leakage classification)",
            "ASME B16.34 - Valves-Flanged, Threaded, and Welding End (design standards)"
        ],
        burden_holder="Engineer",
        adversary_position="Vendor may push bellows seal (higher margin) when packing is adequate",
        counter_arguments=[
            "Bellows seal eliminates packing maintenance (lifecycle cost advantage)",
            "Packing requires periodic adjustment (maintenance cost, potential leakage between adjustments)",
            "Bellows can fail (fatigue, corrosion) and leak catastrophically",
            "Low-emission packing achieves <100 ppm (meets most regulations at lower cost)",
            "Bellows valves are unavailable for large sizes or high temperatures"
        ],
        resolution_strategy="For highly toxic/radioactive fluids: specify bellows seal valve. For emissions-regulated services (VOC, methane): specify ISO 15848 Class A low-emission packing with live-loading. For general process: conventional graphite packing. For high-cycling applications: packing (bellows will fatigue). For >12 inch or >650°F: packing only (bellows unavailable). Document selection in valve datasheet.",
        entity_scope="All rising-stem valves (globe, gate, etc.)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ISO 15848 defines packing performance; bellows seal technology is well-established for critical applications",
        controlling_precedent="ISO 15848-1 Section 5 Classification of Leakage",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Valve Testing Requirements per API and ASME Standards",
        keywords=["valve testing", "hydrostatic", "pneumatic", "seat leakage", "API 598", "MSS SP-61"],
        conclusion_template=[
            "For {valve_type} valve in {pressure_class}, perform {test_type} testing per {standard}.",
            "Shell test at {shell_pressure} psi and seat test at {seat_pressure} psi required.",
            "Acceptance criteria: {leakage_class} leakage per ANSI/FCI 70-2."
        ],
        reasoning_framework="""
        Valve testing standards:

        API 598 - Valve Inspection and Testing (general industrial valves):
        - Shell test (body strength): 1.5 × rated pressure, no leakage permitted
        - Seat test (shutoff tightness): 1.1 × rated pressure (or rated pressure for >38 inch)
        - Test medium: water (hydrostatic) or air/nitrogen (pneumatic) for valves that cannot be wet
        - Duration: shell 2+ minutes, seat 2+ minutes
        - Leakage acceptance: zero visible leakage (liquid), bubble count (gas)

        MSS SP-61 - Pressure Testing of Steel Valves (alternative to API 598):
        - Similar requirements to API 598
        - Used for valves not covered by API standards

        API 6D - Pipeline Valves:
        - More stringent than API 598
        - Shell test: 1.5 × rated pressure
        - Seat test: 1.1 × rated pressure, both directions (bidirectional seat)
        - Gas test option (seat test with air/nitrogen to verify bubble-tight)

        ANSI/FCI 70-2 - Control Valve Seat Leakage:
        - Defines leakage classes for control valves:
          * Class II: 0.5% of Cv (loose shutoff)
          * Class III: 0.1% of Cv
          * Class IV: 0.01% of Cv (standard control valve)
          * Class V: 5×10⁻⁴ ml/min per inch of port diameter
          * Class VI: bubble-tight (1-4 bubbles/min depending on size)

        Special tests:
        - Fire test: API 607 or API 6FA (valves in fire zones)
        - Cryogenic test: BS 6364 (valves for LNG, liquid nitrogen, etc.)
        - Fugitive emissions test: ISO 15848, API 622, API 624
        - Extended body test: for cryogenic valves (stem seal at ambient while body at cryogenic)
        """,
        key_factors=[
            "Valve type and application (pipeline, process, control)",
            "Applicable standard (API 598, API 6D, MSS SP-61)",
            "Pressure rating and size",
            "Required seat leakage class (ANSI/FCI 70-2)",
            "Test medium (water, air, nitrogen)",
            "Unidirectional vs bidirectional seat test",
            "Special testing (fire, cryogenic, fugitive emissions)"
        ],
        primary_authority=[
            "API 598 - Valve Inspection and Testing",
            "API 6D - Pipeline Valves (testing requirements)",
            "MSS SP-61 - Pressure Testing of Steel Valves",
            "ANSI/FCI 70-2 - Control Valve Seat Leakage"
        ],
        burden_holder="Manufacturer (testing) and Engineer (specifying acceptance criteria)",
        adversary_position="Manufacturer may perform minimal testing to reduce cost; buyer may accept without verification",
        counter_arguments=[
            "Shell test at <1.5× pressure does not verify strength adequately",
            "Seat test at rated pressure (not 1.1×) may miss marginal seats",
            "Pneumatic test is less sensitive than hydrostatic (small leaks not visible)",
            "Not testing both seat directions misses leakage in one direction",
            "Skipping special tests (fire, emissions) leads to field failures"
        ],
        resolution_strategy="Specify testing per applicable standard in purchase order: API 598 for general valves, API 6D for pipeline valves, MSS SP-61 for specialty valves. For control valves: specify seat leakage class (Class IV minimum for tight shutoff, Class VI for critical). For fire zones: add API 607 fire test. For emissions-critical: add ISO 15848 fugitive emissions test. Require test certificates with results.",
        entity_scope="All valves requiring factory acceptance testing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API and MSS standards are consensus-based and legally referenced in codes; decades of industry use",
        controlling_precedent="API 598 Section 4 Test Procedures",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Valve Maintenance and Testing Schedules",
        keywords=["maintenance", "testing", "PST", "partial stroke test", "preventive maintenance", "overhaul"],
        conclusion_template=[
            "For {valve_type} in {service}, perform {maintenance_type} every {interval}.",
            "Partial stroke testing (PST) required for ESD valves per ISA-84/IEC 61511 to verify SIL.",
            "Predictive maintenance (torque trending, signature analysis) extends life and prevents failures."
        ],
        reasoning_framework="""
        Valve maintenance strategies:

        1. Run-to-failure:
           - No preventive maintenance (repair only when fails)
           - Acceptable for non-critical, redundant valves
           - Risk: unplanned downtime, potential safety incident

        2. Preventive maintenance (time-based):
           - Scheduled inspections and rebuilds (e.g., every 2 years)
           - Typical tasks: packing adjustment, seat inspection, actuator service
           - Over-maintains (replacing parts with remaining life) but reduces failures
           - Interval based on manufacturer recommendation and operating experience

        3. Predictive maintenance (condition-based):
           - Monitor valve condition (torque, vibration, leakage, stroke time)
           - Maintain only when degradation detected
           - Requires instrumentation (smart positioners, vibration sensors, leak detectors)
           - Optimizes maintenance cost and maximizes valve life

        Testing requirements:

        - Partial Stroke Testing (PST) for ESD valves:
          * ISA-84/IEC 61511 requires periodic testing to verify SIF (Safety Instrumented Function)
          * PST moves valve 10-20% of stroke, verifies movement, returns to operating position
          * Frequency: monthly or quarterly (determines Safety Integrity Level proof test interval)
          * Detects: stuck valve, actuator failure, control system failure
          * Does NOT verify full seat leakage (requires full stroke or shutdown for full test)

        - Full stroke testing:
          * Required annually or per SIL calculation (proof test)
          * Valve stroked fully closed, leakage verified, returned to service
          * May require process shutdown or bypass

        - Seat leakage monitoring:
          * Online leak detection (acoustic, thermal imaging, pressure monitoring downstream)
          * Detects degrading seat before catastrophic failure

        Maintenance intervals (typical):
        - Control valves (throttling): packing adjustment every 6-12 months, trim inspection every 2-4 years
        - Isolation valves (infrequent operation): exercise (stroke) every 3-6 months, overhaul every 5-10 years
        - ESD valves (safety-critical): PST monthly, full stroke test annually, overhaul every 5 years
        - Check valves: inspection every 2-5 years (or per API 570 RBI)
        - PRVs: bench test every 3-5 years (or per API 510/576)
        """,
        key_factors=[
            "Valve criticality (ESD, control, isolation)",
            "Service severity (erosive, corrosive, high-cycling)",
            "Safety integrity level (SIL) requirement",
            "Operating experience (failure history)",
            "Manufacturer recommendations",
            "Regulatory requirements (PSM, API 570, API 510)",
            "Maintenance strategy (preventive vs predictive)",
            "Downtime impact and bypass availability"
        ],
        primary_authority=[
            "ISA-84/IEC 61511 - Functional Safety - Safety Instrumented Systems for the Process Industry Sector (PST requirements)",
            "API 576 - Inspection of Pressure-Relieving Devices",
            "API 570 - Piping Inspection Code (valve inspection)",
            "Manufacturer maintenance manuals"
        ],
        burden_holder="Owner/Operator",
        adversary_position="Operations may defer maintenance to avoid downtime; vendor may push short intervals to sell parts",
        counter_arguments=[
            "Deferred maintenance leads to stuck valves and ESD failures (safety incidents)",
            "Excessive maintenance wastes resources and introduces infant mortality (reassembly errors)",
            "PST without full stroke testing misses seat leakage degradation",
            "Ignoring predictive data (torque trends) misses early failure warnings",
            "Not exercising infrequent valves leads to seized stems and failed operation"
        ],
        resolution_strategy="For ESD valves: implement PST per ISA-84 (monthly or quarterly), full stroke test annually. For control valves: adjust packing 6-12 months, inspect trim 2-4 years, or implement predictive maintenance (torque trending). For isolation valves: exercise every 3-6 months (stroke fully), overhaul every 5-10 years. For PRVs: bench test every 3-5 years per API 576. Document in maintenance management system (CMMS) with failure tracking.",
        entity_scope="All valves requiring ongoing maintenance and testing",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="ISA-84/IEC 61511 is legal requirement for safety instrumented systems; API standards are consensus-based",
        controlling_precedent="ISA-84 Section 11.8 Proof Testing",
        zone=AnalysisZone.PLANNING
    ),

    DoctrineBlock(
        topic="Double Block and Bleed (DBB) Valve Configuration",
        keywords=["double block", "bleed", "DBB", "DIB", "isolation", "blind positive", "API 6D"],
        conclusion_template=[
            "For {isolation_requirement}, use {configuration} configuration to achieve positive isolation.",
            "DBB provides two independent seals plus bleed/vent between seals to verify zero leakage.",
            "API 6D Annex F defines DBB valve design and testing requirements."
        ],
        reasoning_framework="""
        Isolation configurations:

        1. Single Block (SB):
           - One valve
           - Leakage possible if seat fails
           - Not acceptable for maintenance isolation (potential exposure)
           - Applications: general isolation, low-hazard fluids

        2. Double Block and Bleed (DBB):
           - Two independent seals (two valves or one DBB valve) plus vent/bleed between
           - Vent/bleed allows verification of isolation (open vent, no flow = both seats tight)
           - Positive isolation (even if one seat leaks, second seat holds)
           - Required for: maintenance on pressurized systems, toxic/flammable fluids, custody transfer metering
           - Can be: two separate valves + bleed valve, or single DBB valve (integral design)

        3. Double Isolation and Bleed (DIB):
           - Similar to DBB but both seals are in one valve body
           - Single DBB valve (ball, gate, or plug) with two seats
           - More compact and lower cost than two separate valves
           - API 6D Annex F covers DBB ball valves

        4. Blind Positive Isolation:
           - Physical barrier (blind flange, spectacle blind) in addition to valve(s)
           - Absolute isolation (no reliance on valve seats)
           - Required for: entry into vessels, critical maintenance, when one failure is unacceptable

        DBB valve types:
        - DBB ball valve: two seats (upstream and downstream) with cavity relief and vent
        - DBB gate valve: double gate with bleed between gates
        - Separate valves: two valves (gate, ball, globe) with bleed valve between

        Testing:
        - Seat test: verify each seat independently (pressurize one side, bleed between, verify no leakage on other seat)
        - API 6D Annex F specifies DBB ball valve testing procedure
        - Field verification: close both valves, open bleed, verify no flow (proves isolation)
        """,
        key_factors=[
            "Fluid hazard (toxic, flammable, high pressure)",
            "Isolation purpose (maintenance, custody transfer, emergency)",
            "Regulatory requirements (OSHA PSM, EPA RMP)",
            "Space constraints (two valves + bleed vs single DBB valve)",
            "Cost (separate valves vs DBB valve)",
            "Testing and verification capability",
            "Company isolation procedures and standards"
        ],
        primary_authority=[
            "API 6D Annex F - Double Block and Bleed (DBB) Single Valves",
            "OSHA 1910.147 - Control of Hazardous Energy (Lockout/Tagout)",
            "API 2201 - Safe Hot Tapping Practices in the Petroleum and Petrochemical Industries"
        ],
        burden_holder="Engineer and Operations",
        adversary_position="Vendor may sell single valve (lower cost) when DBB is required for safety",
        counter_arguments=[
            "Single block does not provide positive isolation (seat leakage risk)",
            "DBB valve costs 2-3× single valve (but less than two valves + bleed valve + piping)",
            "Failing to verify isolation before maintenance leads to exposure incidents",
            "Bleed valve can plug or be left closed (defeats DBB protection)",
            "Separate valves provide redundancy (if one valve fails, second still provides isolation)"
        ],
        resolution_strategy="For toxic or flammable fluids: specify DBB configuration (two valves + bleed, or DBB valve). For maintenance isolation: DBB minimum (unless blind flange can be easily installed). For custody transfer metering: DBB to isolate meter for calibration. For critical isolation (vessel entry, hot work): use blind flange in addition to DBB. Verify bleed valve operation during commissioning. Train operators on DBB verification procedure (bleed and verify no flow).",
        entity_scope="All critical isolation points in process plants",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="API 6D Annex F defines DBB design; OSHA lockout/tagout requires positive isolation",
        controlling_precedent="API 6D Annex F Section F.3 Design Requirements for DBB Valves",
        zone=AnalysisZone.PLANNING
    )
]

# ═══════════════════════════════════════════════════════════════════════════
# ENGINE CORE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

class MECH05Engine:
    """Valve Selection & Sizing Intelligence Engine"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9045
        self.start_time = time.time()
        self.query_count = 0
        self.doctrine_access_log: List[Dict] = []

        logger.add(
            Path(__file__).parent / "logs" / "mech05_{time}.log",
            rotation="100 MB",
            retention="30 days",
            level="INFO"
        )
        logger.info(f"MECH05 Valve Selection Engine v{self.version} initialized on port {self.port}")

    def normalize_query(self, query: str) -> str:
        """Semantic normalization for valve engineering terms"""
        query_lower = query.lower()

        # Normalize valve type synonyms
        query_lower = re.sub(r'\bPRV\b', 'safety relief valve', query_lower)
        query_lower = re.sub(r'\bESD\b', 'emergency shutdown', query_lower)
        query_lower = re.sub(r'\bMOV\b', 'motor operated valve', query_lower)
        query_lower = re.sub(r'\bDBB\b', 'double block and bleed', query_lower)

        # Normalize standards
        query_lower = re.sub(r'\bISA.?75', 'ISA-75', query_lower)
        query_lower = re.sub(r'\bIEC.?60534', 'IEC 60534', query_lower)
        query_lower = re.sub(r'\bAPI.?520', 'API 520', query_lower)
        query_lower = re.sub(r'\bAPI.?6[AD]', lambda m: m.group(0).replace('.', ' '), query_lower)

        return query_lower

    def search_doctrine_cache(self, query: str) -> List[Tuple[DoctrineBlock, float]]:
        """Search doctrine cache with keyword matching and scoring"""
        normalized = self.normalize_query(query)
        matches: List[Tuple[DoctrineBlock, float]] = []

        for block in DOCTRINE_CACHE:
            score = 0.0
            for keyword in block.keywords:
                if keyword.lower() in normalized:
                    score += 2.0

            # Topic match
            if any(word in normalized for word in block.topic.lower().split()):
                score += 1.0

            # Authority match
            for auth in block.primary_authority:
                if any(word in normalized for word in auth.lower().split()):
                    score += 0.5

            if score > 0:
                matches.append((block, score))
                block.access_count += 1
                block.last_accessed = datetime.now()

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:5]

    def generate_response(
        self,
        query: str,
        mode: ResponseMode,
        matches: List[Tuple[DoctrineBlock, float]]
    ) -> str:
        """Generate response based on mode and doctrine matches"""

        if not matches:
            return "No relevant valve engineering doctrine found for this query. Please provide more context about the valve application, service conditions, or standards involved."

        primary = matches[0][0]

        if mode == ResponseMode.FAST:
            # Concise answer from conclusion template
            conclusion = " ".join(primary.conclusion_template[:2])
            return f"{conclusion} (per {primary.primary_authority[0]})"

        elif mode == ResponseMode.DEFENSE:
            # Detailed answer with reasoning and authority
            response_parts = [
                "VALVE ENGINEERING ANALYSIS:",
                "",
                f"Issue: {primary.topic}",
                "",
                "Conclusion:",
                " ".join(primary.conclusion_template),
                "",
                "Technical Basis:",
                primary.reasoning_framework[:500] + "..." if len(primary.reasoning_framework) > 500 else primary.reasoning_framework,
                "",
                "Key Factors:",
                *[f"• {factor}" for factor in primary.key_factors[:5]],
                "",
                "Applicable Standards:",
                *[f"• {auth}" for auth in primary.primary_authority],
                "",
                f"Confidence Level: {primary.confidence.value}",
                f"Stratification: {primary.confidence_stratification}"
            ]
            return "\n".join(response_parts)

        else:  # MEMO mode
            # Full documentation-grade response
            response_parts = [
                f"VALVE ENGINEERING MEMORANDUM: {primary.topic}",
                "=" * 80,
                "",
                "EXECUTIVE SUMMARY:",
                " ".join(primary.conclusion_template),
                "",
                "TECHNICAL ANALYSIS:",
                primary.reasoning_framework,
                "",
                "CRITICAL FACTORS:",
                *[f"{i+1}. {factor}" for i, factor in enumerate(primary.key_factors)],
                "",
                "APPLICABLE CODES AND STANDARDS:",
                *[f"• {auth}" for auth in primary.primary_authority],
                "",
                "ALTERNATIVE POSITIONS:",
                f"Adversary Position: {primary.adversary_position}",
                "",
                "Counter-Arguments to Address:",
                *[f"• {arg}" for arg in primary.counter_arguments],
                "",
                "RECOMMENDED APPROACH:",
                primary.resolution_strategy,
                "",
                "CONFIDENCE ASSESSMENT:",
                f"Level: {primary.confidence.value}",
                f"Basis: {primary.confidence_stratification}",
                "",
                "CONTROLLING PRECEDENT:",
                primary.controlling_precedent,
                "",
                "ENTITY SCOPE:",
                primary.entity_scope,
                "",
                "RELATED TOPICS:",
            ]

            # Add related doctrine blocks
            for match, score in matches[1:4]:
                response_parts.append(f"• {match.topic} (relevance: {score:.1f})")

            return "\n".join(response_parts)

    def classify_issue(self, query: str) -> List[IssueCategory]:
        """Classify query into issue categories"""
        categories = []
        query_lower = query.lower()

        category_keywords = {
            IssueCategory.CONTROL_VALVE_SIZING: ["cv", "sizing", "flow coefficient", "ISA"],
            IssueCategory.VALVE_TYPE_SELECTION: ["globe", "butterfly", "ball", "gate", "valve type"],
            IssueCategory.ACTUATOR_SELECTION: ["actuator", "pneumatic", "electric", "MOV"],
            IssueCategory.SAFETY_RELIEF_SIZING: ["PRV", "relief", "safety", "API 520", "overpressure"],
            IssueCategory.MATERIAL_SELECTION: ["material", "NACE", "sour", "stainless", "carbon steel"],
            IssueCategory.VALVE_NOISE: ["noise", "dBA", "IEC 60534", "aerodynamic"],
            IssueCategory.CAVITATION_FLASHING: ["cavitation", "flashing", "vapor pressure"],
            IssueCategory.FUGITIVE_EMISSIONS: ["fugitive", "emissions", "packing", "ISO 15848"],
            IssueCategory.FIRE_SAFE_DESIGN: ["fire safe", "API 607", "fire test"],
            IssueCategory.WELLHEAD_VALVES: ["wellhead", "API 6A", "christmas tree"],
            IssueCategory.MAINTENANCE_TESTING: ["maintenance", "testing", "PST", "partial stroke"],
            IssueCategory.PRESSURE_REGULATION: ["regulator", "pressure control", "pilot operated"]
        }

        for category, keywords in category_keywords.items():
            if any(kw in query_lower for kw in keywords):
                categories.append(category)

        return categories if categories else [IssueCategory.VALVE_TYPE_SELECTION]

    def calculate_determinism_hash(self, query: str, response: str) -> str:
        """Generate SHA-256 hash for reproducibility"""
        content = f"{query}|{response}|{self.version}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def process_query(self, request: QueryRequest) -> QueryResponse:
        """Main query processing pipeline (TIE three-layer response)"""
        start = time.time()
        self.query_count += 1

        logger.info(f"Query #{self.query_count}: {request.query[:100]}")

        # Layer 1: Doctrine Cache (fast retrieval)
        matches = self.search_doctrine_cache(request.query)

        # Layer 2: Generate response based on mode
        answer = self.generate_response(request.query, request.mode, matches)

        # Layer 3: Metadata and telemetry
        categories = self.classify_issue(request.query)
        confidence = matches[0][0].confidence if matches else ConfidenceLevel.DISCLOSURE
        topics = [m[0].topic for m in matches]

        latency_ms = (time.time() - start) * 1000

        response = QueryResponse(
            answer=answer,
            confidence=confidence,
            mode=request.mode,
            doctrine_topics=topics,
            issue_categories=[c.value for c in categories],
            determinism_hash=self.calculate_determinism_hash(request.query, answer),
            latency_ms=round(latency_ms, 2),
            zone=AnalysisZone.PLANNING
        )

        logger.info(f"Response generated in {latency_ms:.2f}ms, {len(topics)} doctrines matched")

        return response

    def health_check(self) -> HealthResponse:
        """System health and metrics"""
        uptime = time.time() - self.start_time
        return HealthResponse(
            status="operational",
            version=self.version,
            port=self.port,
            doctrine_count=len(DOCTRINE_CACHE),
            issue_categories=len(IssueCategory),
            uptime_seconds=round(uptime, 2)
        )

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

APP = FastAPI(
    title="MECH05 - Valve Selection & Sizing Engine",
    version="1.0.0",
    description="TIE Gold Standard: Mechanical Engineering - Control & Isolation Valves"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

engine = MECH05Engine()

@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with three-layer TIE response"""
    try:
        return engine.process_query(request)
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check and system metrics"""
    return engine.health_check()

@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine topics with access counts"""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": block.topic,
                "keywords": block.keywords,
                "confidence": block.confidence.value,
                "access_count": block.access_count,
                "last_accessed": block.last_accessed.isoformat() if block.last_accessed else None
            }
            for block in DOCTRINE_CACHE
        ]
    }

@APP.get("/")
async def root():
    """Root endpoint with engine information"""
    return {
        "engine": "MECH05 - Valve Selection & Sizing Intelligence Engine",
        "version": engine.version,
        "port": engine.port,
        "status": "operational",
        "doctrine_count": len(DOCTRINE_CACHE),
        "endpoints": {
            "query": "POST /query",
            "health": "GET /health",
            "doctrines": "GET /doctrines"
        }
    }

# ═══════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("MECH05 - Valve Selection & Sizing Intelligence Engine")
    logger.info(f"Version: {engine.version} | Port: {engine.port}")
    logger.info(f"Doctrines loaded: {len(DOCTRINE_CACHE)}")
    logger.info(f"Issue categories: {len(IssueCategory)}")
    logger.info("TIE-20 Gold Standard: COMPLETE")
    logger.info("=" * 80)

    uvicorn.run(
        APP,
        host="0.0.0.0",
        port=engine.port,
        log_level="info"
    )
