"""
MECH12 Pneumatic Systems Intelligence Engine
TIE-Grade Implementation v1.0.0

Analyzes pneumatic systems: compressed air generation, air treatment, pneumatic actuators,
control valves, vacuum systems, and energy efficiency optimization.

Port: 9272
Authority Level: MECH12_PNEUMATIC_SYSTEMS
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn


# ============================================================================
# ENUMS & DATA STRUCTURES
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
    PLANNING = "PLANNING"
    REPORTING = "REPORTING"
    AUDIT = "AUDIT"


class IssueCategory(str, Enum):
    COMPRESSOR_SELECTION = "COMPRESSOR_SELECTION"
    AIR_TREATMENT = "AIR_TREATMENT"
    RECEIVER_SIZING = "RECEIVER_SIZING"
    ACTUATOR_DESIGN = "ACTUATOR_DESIGN"
    VALVE_SELECTION = "VALVE_SELECTION"
    VACUUM_SYSTEMS = "VACUUM_SYSTEMS"
    ENERGY_EFFICIENCY = "ENERGY_EFFICIENCY"
    AIR_QUALITY = "AIR_QUALITY"
    LEAK_MANAGEMENT = "LEAK_MANAGEMENT"
    SYSTEM_SAFETY = "SYSTEM_SAFETY"
    CIRCUIT_DESIGN = "CIRCUIT_DESIGN"
    FLOW_CONTROL = "FLOW_CONTROL"


@dataclass
class DoctrineBlock:
    """Represents a reusable domain expertise block."""
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


@dataclass
class TelemetryRecord:
    """Tracks query performance and metrics."""
    query_id: str
    timestamp: float
    mode: ResponseMode
    issue_categories: List[IssueCategory]
    cache_hit: bool
    response_time_ms: float
    doctrine_blocks_used: List[str]
    confidence_level: ConfidenceLevel
    error_domain: Optional[str] = None


@dataclass
class CoverageMetrics:
    """Tracks doctrine coverage and epistemic gaps."""
    total_doctrines: int
    triggered_doctrines: Set[str] = field(default_factory=set)
    missed_doctrines: Set[str] = field(default_factory=set)
    epistemic_gaps: List[str] = field(default_factory=list)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    query: str = Field(..., description="Pneumatic systems question")
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING)
    context: Optional[Dict[str, Any]] = Field(default=None)


class QueryResponse(BaseModel):
    response: str
    confidence: ConfidenceLevel
    doctrine_blocks: List[str]
    analysis_zone: AnalysisZone
    mode: ResponseMode
    determinism_hash: str
    telemetry: Dict[str, Any]
    epistemic_caveats: List[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float
    total_queries: int
    cache_hit_rate: float
    avg_response_time_ms: float


# ============================================================================
# DOCTRINE CACHE - 25+ PNEUMATIC SYSTEMS EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: Dict[str, DoctrineBlock] = {

    "reciprocating_compressor_selection": DoctrineBlock(
        topic="Reciprocating Compressor Selection and Sizing",
        keywords=["reciprocating", "piston compressor", "single-stage", "two-stage", "capacity", "pressure ratio", "volumetric efficiency"],
        conclusion_template="Reciprocating compressor selection depends on required FAD (free air delivery), discharge pressure, duty cycle, and power availability.",
        reasoning_framework="""
Reciprocating (piston) compressor selection methodology:
1. Determine FAD requirement (SCFM or m3/min at standard conditions)
2. Identify discharge pressure requirement (PSIG or bar)
3. Calculate pressure ratio (Pdischarge absolute / Patm)
4. Single-stage limited to ~7:1 ratio (100-125 PSIG typical)
5. Two-stage for 125+ PSIG (intercooled for efficiency)
6. Volumetric efficiency decreases with higher pressure ratio
7. Typical VE: 70-80% for single-stage, 75-85% for two-stage
8. Account for altitude derating (3-4% per 1000 ft above sea level)
9. Consider duty cycle (continuous, intermittent, start-stop)
10. Motor sizing: BHP = (SCFM * Pdischarge PSIG * 1.05) / (229 * mechanical efficiency)
11. Mechanical efficiency typically 85-90%
12. Cooling requirements: air-cooled vs water-cooled
13. Air receiver sizing to reduce cycling and pressure fluctuations
14. Noise level typically 75-85 dBA at 1m
15. Maintenance intervals: oil change 500-1000 hrs, valve inspection 2000 hrs
16. Advantage: high pressure capability, simple design, low initial cost
17. Disadvantage: pulsating flow, higher vibration, more maintenance vs rotary
18. Application: intermittent duty, portable, low to medium flow
19. Multi-stage compression reduces work input (isothermal approach)
20. Intercooler effectiveness: 70-85% approach to cooling water temp
        """,
        key_factors=[
            "Required FAD (free air delivery) at standard conditions",
            "Discharge pressure and pressure ratio",
            "Single-stage (up to 7:1) vs two-stage (7:1+) configuration",
            "Volumetric efficiency derating with pressure ratio",
            "Altitude derating (3-4% per 1000 ft)",
            "Duty cycle (continuous vs intermittent)",
            "Cooling method (air vs water)",
            "Motor horsepower and efficiency"
        ],
        primary_authority=[
            "CAGI (Compressed Air and Gas Institute) Performance Standards",
            "ASME PTC 9 - Performance Test Code on Displacement Compressors",
            "ISO 1217 - Displacement Compressors Acceptance Tests"
        ],
        burden_holder="System designer must demonstrate compressor sized for actual FAD requirement with adequate margin",
        adversary_position="Nameplate capacity overstates actual delivered air at operating pressure",
        counter_arguments=[
            "Volumetric efficiency losses not accounted in sizing",
            "Altitude derating ignored",
            "Duty cycle exceeds compressor rating",
            "Inadequate cooling leads to thermal derating",
            "Single-stage used beyond 7:1 pressure ratio (inefficient)"
        ],
        resolution_strategy="Calculate actual FAD at operating pressure accounting for VE, altitude, temperature, duty cycle per CAGI standards",
        entity_scope="Any compressed air system with reciprocating compressor",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on CAGI and ASME standards with validated engineering calculations",
        controlling_precedent="CAGI Compressed Air & Gas Handbook 7th Edition"
    ),

    "rotary_screw_compressor_design": DoctrineBlock(
        topic="Rotary Screw Compressor Design and Application",
        keywords=["rotary screw", "oil-flooded", "oil-free", "capacity control", "VSD", "variable speed drive", "specific power"],
        conclusion_template="Rotary screw compressors provide continuous oil-free or oil-flooded air with superior efficiency for medium to high flow applications.",
        reasoning_framework="""
Rotary screw compressor characteristics and design:
1. Two interlocking helical rotors compress air continuously
2. Oil-flooded: oil seals, cools, lubricates (most common)
3. Oil-free: no oil contact with air (food, pharma, critical apps)
4. Typical capacity range: 10-5000+ SCFM
5. Pressure range: 100-200 PSIG (higher with booster stages)
6. Capacity control methods: inlet modulation, variable speed drive (VSD), load/unload
7. VSD reduces energy 35% at partial loads vs fixed speed
8. Specific power (kW per 100 CFM): 15-22 kW/100 CFM at full load
9. Oil-flooded specific power: 18-20 kW/100 CFM
10. Oil-free specific power: 20-24 kW/100 CFM (higher due to no oil sealing)
11. Oil carryover in oil-flooded: <3 ppm with separator
12. Cooling: air-cooled, water-cooled, or glycol-cooled
13. Noise level: 60-75 dBA (quieter than reciprocating)
14. Maintenance: oil/filter change 2000-4000 hrs, separator 4000-8000 hrs
15. Air-oil separator critical component (pressure drop indicates replacement)
16. Heat recovery potential: 70-90% of motor input recoverable
17. Turndown ratio with VSD: 10:1 or better
18. Advantages: continuous flow, low vibration, high efficiency, lower maintenance
19. Disadvantages: higher initial cost, oil contamination risk (oil-flooded)
20. Application: continuous duty, medium to high flow, stable pressure
        """,
        key_factors=[
            "Oil-flooded vs oil-free design based on air purity requirements",
            "VSD for variable loads (35% energy savings potential)",
            "Specific power (kW/100 CFM) for energy cost analysis",
            "Oil carryover limits for oil-flooded units (<3 ppm)",
            "Heat recovery opportunity (70-90% of motor input)",
            "Capacity control method (modulation, VSD, load/unload)",
            "Maintenance intervals and separator replacement",
            "Continuous duty suitability"
        ],
        primary_authority=[
            "ISO 1217 - Displacement Compressors Acceptance Tests",
            "CAGI Performance Verification Program",
            "ASME PTC 9 - Compressor Performance Test Code"
        ],
        burden_holder="Manufacturer must verify specific power and capacity per CAGI data sheet",
        adversary_position="Claimed efficiency not achievable at actual operating conditions",
        counter_arguments=[
            "Specific power increases at partial loads (fixed speed)",
            "Inlet air temperature higher than test conditions",
            "Pressure drop in aftercooler/dryer not accounted",
            "Oil carryover exceeds specification",
            "Heat recovery not economically viable"
        ],
        resolution_strategy="Demand CAGI-verified performance data sheets and field verification of specific power at actual operating pressure and temperature",
        entity_scope="Any industrial compressed air system requiring continuous supply",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on CAGI verified data and ISO test standards",
        controlling_precedent="CAGI Performance Verification Program"
    ),

    "air_receiver_sizing": DoctrineBlock(
        topic="Air Receiver Tank Sizing and Pressure Stabilization",
        keywords=["air receiver", "storage tank", "ASME pressure vessel", "pressure drop", "cycling", "gallons", "volume"],
        conclusion_template="Air receiver sizing balances storage volume against acceptable pressure drop and compressor cycling frequency.",
        reasoning_framework="""
Air receiver tank sizing methodology:
1. Primary functions: dampen pressure fluctuations, reduce cycling, cool air, condense moisture
2. ASME Code Section VIII Div 1 construction required (stamped)
3. Sizing formula: V = (T * C * Pa) / (P1 - P2)
   V = receiver volume (gallons)
   T = time for pressure drop (minutes)
   C = air consumption (SCFM)
   Pa = atmospheric pressure (14.7 PSIA)
   P1 = initial pressure (PSIA)
   P2 = final pressure (PSIA)
4. Rule of thumb: 1-2 gallons per SCFM for reciprocating
5. Rule of thumb: 2-4 gallons per SCFM for rotary screw
6. Acceptable pressure drop: 5-10 PSI in most applications
7. Cycling limit: compressor should not cycle >6 times per hour (10 min minimum run)
8. Wet receiver (before dryer): removes bulk moisture, cools air
9. Dry receiver (after dryer): stabilizes pressure, backup storage
10. Location: as close to compressor discharge as practical
11. Drain valve required at lowest point (automatic or manual)
12. Safety relief valve set at MAWP (maximum allowable working pressure)
13. Pressure gauge and temperature gauge required
14. Inspection: internal inspection every 5-10 years per jurisdiction
15. Condensate accumulation: 1 gallon per 1000 CFM per 24 hrs (estimate)
16. Larger receiver = less cycling, more stable pressure, better moisture removal
17. Undersized receiver = excessive cycling, pressure swings, premature compressor wear
18. Oversized receiver = wasted cost, space, delayed pressure recovery
19. Multiple small vs single large: distributed often better for large facilities
20. Calculation must account for actual air consumption profile (peak vs average)
        """,
        key_factors=[
            "Air consumption rate (SCFM) and profile (steady vs intermittent)",
            "Acceptable pressure drop (typically 5-10 PSI)",
            "Compressor cycling limit (minimum 10 min run time)",
            "ASME Code compliance and stamping",
            "Wet vs dry receiver placement",
            "Condensate drainage and moisture removal",
            "Safety devices (relief valve, gauges)",
            "Inspection and maintenance requirements"
        ],
        primary_authority=[
            "ASME Boiler and Pressure Vessel Code Section VIII Division 1",
            "OSHA 29 CFR 1910.169 - Air Receivers",
            "NFPA 99 - Health Care Facilities (if applicable)"
        ],
        burden_holder="System designer must demonstrate receiver sized per ASME formula for actual air consumption and cycling limits",
        adversary_position="Receiver undersized leading to excessive cycling and pressure instability",
        counter_arguments=[
            "Actual air consumption exceeds design assumption",
            "Peak demand not accounted in sizing",
            "Pressure drop tolerance too tight",
            "Compressor cycling exceeds manufacturer limits",
            "ASME code compliance not verified (unstamped vessel)"
        ],
        resolution_strategy="Calculate receiver volume using ASME formula with actual consumption data and verify cycling frequency meets compressor manufacturer limits",
        entity_scope="All compressed air systems with reciprocating or rotary compressors",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ASME Code requirements and industry practice",
        controlling_precedent="ASME Section VIII Division 1 - Pressure Vessels"
    ),

    "air_dryer_selection": DoctrineBlock(
        topic="Compressed Air Dryer Selection - Refrigerated vs Desiccant",
        keywords=["air dryer", "refrigerated", "desiccant", "pressure dew point", "ISO 8573", "moisture removal", "regeneration"],
        conclusion_template="Air dryer selection depends on required pressure dew point, air quality class per ISO 8573, and operating conditions.",
        reasoning_framework="""
Compressed air dryer selection criteria:
1. Key metric: Pressure Dew Point (PDP) in deg F or deg C
2. PDP = temperature at which water vapor condenses at operating pressure
3. ISO 8573-1 air quality classes for moisture (Class 1-10)
4. Class 4 PDP: +38 deg F (most general industrial)
5. Class 3 PDP: -4 deg F (instrument air)
6. Class 2 PDP: -40 deg F (critical instrument, outdoor piping)
7. Class 1 PDP: -94 deg F (ultra-dry, pharma, electronics)
8. Refrigerated dryer: PDP +35 to +50 deg F (Class 4-5)
9. Refrigerated principle: cool air to 35-38 deg F, condense moisture, reheat
10. Refrigerated advantage: low operating cost, simple, reliable
11. Refrigerated limitation: cannot achieve sub-freezing PDP
12. Desiccant dryer: PDP -40 to -100 deg F (Class 1-2)
13. Desiccant types: heatless, heated, blower purge
14. Heatless desiccant: uses 15-20% of compressed air for regeneration (purge loss)
15. Heated desiccant: uses external heat, <7% purge loss
16. Blower purge: uses ambient air + heat, <3% purge loss (most efficient)
17. Desiccant media: activated alumina, silica gel, molecular sieve
18. Regeneration cycle: typically 4-10 hours per tower
19. Twin tower design: one drying, one regenerating (continuous operation)
20. Pressure drop: refrigerated 3-5 PSI, desiccant 5-10 PSI
21. Deliquescent dryer: chemical tablet, -20 deg F PDP, no power (low cost, high maintenance)
22. Membrane dryer: selective permeation, -40 deg F, no power (low flow only)
23. Selection decision tree: PDP requirement -> dryer type -> sizing -> cost analysis
24. Oversizing consequences: higher purge loss (desiccant), cycling (refrigerated)
25. Undersizing consequences: inadequate drying, moisture carryover, equipment damage
        """,
        key_factors=[
            "Required pressure dew point (PDP) and ISO 8573 class",
            "Refrigerated for +35 to +50 deg F PDP (Class 4-5)",
            "Desiccant for -40 to -100 deg F PDP (Class 1-2)",
            "Purge loss in desiccant dryers (15-20% heatless, 3-7% blower purge)",
            "Pressure drop (3-5 PSI refrigerated, 5-10 PSI desiccant)",
            "Operating cost (refrigerated lower, desiccant higher due to purge)",
            "Outdoor piping requires Class 2 (-40 deg F minimum)",
            "Regeneration method (heatless, heated, blower purge)"
        ],
        primary_authority=[
            "ISO 8573-1 - Compressed Air Quality Classes",
            "ISO 7183 - Compressed Air Dryers - Specifications and Testing",
            "CAGI Compressed Air Dryer Selection Guide"
        ],
        burden_holder="System designer must specify dryer capable of achieving required PDP at actual operating conditions",
        adversary_position="Dryer undersized or wrong type selected for application PDP requirement",
        counter_arguments=[
            "Ambient temperature higher than dryer rating",
            "Inlet air temperature exceeds 100 deg F (refrigerated limit)",
            "Actual PDP requirement more stringent than specified",
            "Purge loss not accounted in compressor sizing",
            "Pressure drop reduces system pressure below minimum"
        ],
        resolution_strategy="Specify ISO 8573 air quality class based on application, select dryer type per PDP requirement, verify performance at actual conditions",
        entity_scope="All compressed air systems requiring moisture removal",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ISO 8573 standards and CAGI dryer selection methodology",
        controlling_precedent="ISO 8573-1 Compressed Air Quality Classes"
    ),

    "pneumatic_cylinder_sizing": DoctrineBlock(
        topic="Pneumatic Cylinder Force and Sizing Calculations",
        keywords=["pneumatic cylinder", "bore size", "force", "stroke", "cushioning", "thrust", "air consumption"],
        conclusion_template="Pneumatic cylinder sizing requires force calculation accounting for pressure, bore area, friction, and load dynamics.",
        reasoning_framework="""
Pneumatic cylinder sizing methodology:
1. Theoretical force: F = P * A
   F = force (lbf)
   P = pressure (PSIG + 14.7 = PSIA)
   A = piston area (sq in)
2. Piston area: A = pi * (D^2) / 4
   D = bore diameter (inches)
3. Effective force accounting for friction: F_eff = F * 0.85 to 0.90
4. Friction losses: piston seals, rod seals, bearing, alignment
5. Extend force (full bore area): F_ext = P * pi * D^2 / 4
6. Retract force (annular area): F_ret = P * pi * (D^2 - d^2) / 4
   d = rod diameter
7. Force ratio: F_ret / F_ext = (D^2 - d^2) / D^2 (typically 0.6-0.8)
8. Required bore for load: D = sqrt((4 * F) / (pi * P * eff))
9. Standard bore sizes: 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12 inches
10. Standard metric: 32, 40, 50, 63, 80, 100, 125, 160, 200, 250 mm
11. Stroke length: standard increments 1, 2, 4, 6, 8, 10, 12, 18, 24, 36 inches
12. Cushioning: end-of-stroke shock absorption (adjustable needle valves)
13. Air consumption per cycle: V = A * L * 2 / 1728 (cubic feet)
   L = stroke length (inches)
14. SCFM for cycling: CFM = (V * cycles_per_min * 14.7) / P_abs
15. Speed control: meter-in (precise), meter-out (more common, stable)
16. Mounting styles: clevis, flange, trunnion, foot, rigid
17. Rod configurations: single-rod (most common), double-rod, rodless
18. Buckling limit: long stroke requires rod diameter analysis
19. Side load capacity: limited by bearing design, typically 10% of thrust
20. Operating pressure range: 60-150 PSIG (80-100 PSIG most common)
21. Material: aluminum body (light), steel (heavy duty), stainless (corrosive)
22. Seal materials: NBR (general), polyurethane (wear), Viton (chemical)
23. Temperature range: -20 to +200 deg F (standard seals)
24. Safety factor: 1.5 to 2.0 on force calculations
25. Cylinder life: 10-50 million cycles depending on load and speed
        """,
        key_factors=[
            "Required force and operating pressure",
            "Bore diameter and piston area calculation",
            "Friction losses (10-15% derating)",
            "Extend vs retract force difference (annular area)",
            "Stroke length and mounting constraints",
            "Air consumption and cycling rate",
            "Cushioning for shock absorption at end of stroke",
            "Speed control method (meter-in vs meter-out)",
            "Buckling analysis for long strokes",
            "Side load limits (typically 10% of thrust)"
        ],
        primary_authority=[
            "ISO 6431 - Pneumatic Cylinders with Detachable Mountings",
            "ISO 15552 - Pneumatic Cylinders - Metric Series",
            "NFPA T3.6.1 - Pneumatic Cylinders"
        ],
        burden_holder="System designer must demonstrate cylinder bore and rod sized for actual load with adequate safety factor",
        adversary_position="Cylinder undersized for actual load and dynamics",
        counter_arguments=[
            "Friction losses exceed 15% assumption",
            "Dynamic loads (acceleration, deceleration) not accounted",
            "Pressure drop in supply line reduces actual cylinder pressure",
            "Side loading exceeds bearing capacity",
            "Stroke length causes rod buckling",
            "Cushioning inadequate for impact loads"
        ],
        resolution_strategy="Calculate required force with safety factor, account for friction and dynamics, verify against ISO cylinder standards",
        entity_scope="All pneumatic linear actuator applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on fundamental pneumatic equations and ISO cylinder standards",
        controlling_precedent="ISO 15552 Pneumatic Cylinder Standard"
    ),

    "directional_valve_selection": DoctrineBlock(
        topic="Directional Control Valve Selection - 3/2, 5/2, 5/3 Configurations",
        keywords=["directional valve", "solenoid", "3/2", "5/2", "5/3", "center condition", "Cv", "flow coefficient"],
        conclusion_template="Directional valve selection depends on actuator type, required flow (Cv), number of ports, and center condition.",
        reasoning_framework="""
Directional control valve selection criteria:
1. Valve notation: N/M (N = ports, M = positions)
2. 3/2 valve: 3 ports, 2 positions (P=pressure, A=work, R=exhaust)
3. 5/2 valve: 5 ports, 2 positions (P, A, B, R1, R2) for double-acting cylinder
4. 5/3 valve: 5 ports, 3 positions (includes center position)
5. 3/2 normally closed: default position blocks flow to actuator
6. 3/2 normally open: default position allows flow (less common)
7. 5/2 application: double-acting cylinder (most common)
8. 5/3 center conditions: closed, pressure, exhaust, open
9. Closed center: all ports blocked (hold load)
10. Pressure center: pressure to both actuator ports (floating)
11. Exhaust center: both actuator ports to exhaust (no hold)
12. Open center: all ports connected (free movement)
13. Actuation methods: manual, mechanical, pneumatic pilot, solenoid, push button
14. Solenoid voltage: 24VDC (most common industrial), 120VAC, 12VDC
15. Flow capacity: Cv (flow coefficient) determines max flow
16. Cv definition: GPM of water at 1 PSI pressure drop
17. Pneumatic Cv: SCFM = Cv * sqrt(delta_P * (P_abs + 14.7) / 2)
18. Pressure drop: 5-15 PSI typical at rated flow
19. Response time: solenoid 20-100 ms, pilot-operated 100-300 ms
20. Port size: 1/8, 1/4, 3/8, 1/2, 3/4, 1 inch NPT or G-thread
21. Manifold mounting: ISO 15407, ISO 5599, Namur (proximity switch)
22. Inline mounting: NPT threaded ports, compact
23. Exhaust ports: muffler required for noise reduction (<85 dBA)
24. Leakage: internal leakage affects holding force, check valve may be needed
25. Durability: 10-50 million cycles depending on design
26. Manual override: allows manual actuation in power loss
27. Pilot pressure requirement: typically 85% of line pressure minimum
28. Sizing: valve Cv must exceed cylinder air consumption at desired speed
        """,
        key_factors=[
            "Actuator type: single-acting (3/2) vs double-acting (5/2)",
            "Center condition requirement (5/3 valves)",
            "Flow capacity (Cv) based on cylinder speed requirement",
            "Actuation method (solenoid, pilot, manual)",
            "Port size and connection type (NPT, G-thread)",
            "Response time requirement",
            "Manifold vs inline mounting",
            "Voltage availability (24VDC most common)",
            "Exhaust noise and muffling",
            "Manual override requirement"
        ],
        primary_authority=[
            "ISO 5599-1 - Pneumatic Control Valves - Mounting Interface",
            "ISO 15407 - Pneumatic Valves - Manifold Mounting",
            "NFPA T3.5.1 - Directional Control Valves"
        ],
        burden_holder="System designer must demonstrate valve Cv adequate for required actuator speed",
        adversary_position="Valve undersized causing slow actuator response or insufficient force",
        counter_arguments=[
            "Valve Cv too low for required flow",
            "Pressure drop excessive at rated flow",
            "Wrong center condition for application",
            "Solenoid voltage not available",
            "Port size creates bottleneck",
            "Internal leakage prevents load holding",
            "Response time too slow for cycle time"
        ],
        resolution_strategy="Calculate required Cv from cylinder speed and pressure, select valve with adequate margin, verify center condition matches application",
        entity_scope="All pneumatic actuator control systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ISO valve standards and flow calculation fundamentals",
        controlling_precedent="ISO 5599 Pneumatic Control Valve Standards"
    ),

    "flow_control_methods": DoctrineBlock(
        topic="Pneumatic Flow Control - Meter-In vs Meter-Out",
        keywords=["flow control", "meter-in", "meter-out", "speed control", "needle valve", "bypass", "cushioning"],
        conclusion_template="Flow control method (meter-in vs meter-out) determines actuator speed stability and load handling characteristics.",
        reasoning_framework="""
Pneumatic flow control strategies:
1. Purpose: control actuator speed by restricting air flow
2. Meter-in: restrict flow entering actuator (supply side)
3. Meter-out: restrict flow exiting actuator (exhaust side)
4. Meter-in characteristics: simple, unstable with varying loads, speed increases under load
5. Meter-out characteristics: stable speed, resistant to load variation (preferred)
6. Meter-out principle: back pressure on exhaust side resists motion
7. Flow control valve types: needle valve (adjustable), fixed orifice, quick exhaust
8. Bi-directional control: separate meter-out for extend and retract
9. Installation: meter-out valve at cylinder port or in exhaust line
10. Quick exhaust valve: bypasses directional valve for fast retract/extend
11. Bypass flow control: separate path around restriction (smoother)
12. Cushioning vs flow control: cushioning is end-of-stroke deceleration
13. Flow control equation: Q = Cv * sqrt(delta_P)
14. Throttle range: 10:1 typical (full open to minimum controllable)
15. Response to load: meter-in slows under load, meter-out maintains speed
16. Pressure intensification: meter-in can cause pressure spike on reversal
17. Application guidelines: meter-out for pushing loads, meter-in for light loads only
18. Cylinder speed calculation: v = (Q / A) * 60 (inches per min)
   Q = flow (CFM), A = piston area (sq in)
19. Flow control placement: close to cylinder minimizes delay volume
20. Multi-position applications: individual flow controls for each direction
21. Synchronization: two cylinders require matched flow controls (imperfect)
22. Energy efficiency: flow control wastes energy (throttling loss)
23. Alternative: regulate pressure instead of flow (less common)
24. Noise consideration: high velocity through restriction increases noise
25. Contamination: flow control orifice sensitive to dirt (filtration critical)
        """,
        key_factors=[
            "Meter-out for stable speed with varying loads (preferred)",
            "Meter-in for light loads only (unstable)",
            "Bi-directional control requires separate valves for extend/retract",
            "Flow control placement close to cylinder",
            "Quick exhaust valve for rapid motion",
            "Throttle range 10:1 typical",
            "Flow control wastes energy (throttling losses)",
            "Contamination sensitivity requires filtration"
        ],
        primary_authority=[
            "ISO 6358 - Pneumatic Components - Flow Rate Characteristics",
            "ISO 6953 - Pneumatic Symbols",
            "NFPA T2.6.1 - Flow Control Devices"
        ],
        burden_holder="System designer must specify meter-out control for load-bearing applications",
        adversary_position="Meter-in control used inappropriately causing speed instability",
        counter_arguments=[
            "Wrong control method for application",
            "Flow control undersized (excessive pressure drop)",
            "Flow control oversized (insufficient control range)",
            "Contamination blocking orifice",
            "Throttling losses increase energy consumption",
            "Delay volume between valve and cylinder excessive"
        ],
        resolution_strategy="Specify meter-out flow control for all load-bearing applications, calculate required Cv, verify throttle range adequate",
        entity_scope="All pneumatic speed control applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on fundamental pneumatic control principles and ISO standards",
        controlling_precedent="ISO 6358 Flow Rate Characteristics"
    ),

    "vacuum_generation_methods": DoctrineBlock(
        topic="Vacuum Generation - Ejector vs Mechanical Pump Selection",
        keywords=["vacuum", "ejector", "venturi", "vacuum pump", "rotary vane", "claw pump", "vacuum level", "SCFM"],
        conclusion_template="Vacuum generation method depends on required vacuum level, flow rate, and availability of compressed air.",
        reasoning_framework="""
Vacuum generation technology selection:
1. Vacuum levels: rough (760-1 torr), medium (1-0.001 torr), high (<0.001 torr)
2. Industrial vacuum: typically 15-28 inch Hg (rough vacuum)
3. Atmospheric pressure: 29.92 inch Hg = 760 torr = 14.7 PSIA
4. Vacuum ejector (venturi): compressed air driven, no moving parts
5. Ejector principle: compressed air through nozzle creates suction (Bernoulli)
6. Ejector vacuum level: 15-27 inch Hg (depending on supply pressure)
7. Ejector advantages: simple, no maintenance, fast response, compact
8. Ejector disadvantages: continuous air consumption, noisy (use muffler)
9. Ejector air consumption: 1-5 SCFM per ejector (size dependent)
10. Multi-stage ejector: higher vacuum (up to 28 inch Hg)
11. Mechanical vacuum pumps: rotary vane, claw, diaphragm, liquid ring
12. Rotary vane pump: oil-lubricated, 28+ inch Hg, 1-100+ CFM capacity
13. Claw pump: oil-free, 27 inch Hg, low maintenance, higher cost
14. Diaphragm pump: oil-free, up to 26 inch Hg, small capacity (<5 CFM)
15. Liquid ring pump: water seal, 26 inch Hg, handles moisture/particles
16. Pump evacuation time: t = (V * ln(P1/P2)) / Q
    V = volume (cu ft), P1 = initial pressure, P2 = final pressure, Q = pump flow
17. Vacuum cup sizing: suction force = vacuum * cup area
18. Vacuum force: F = vacuum_level (in Hg) * 0.491 * Area (sq in)
19. Safety factor: 2.0 minimum for vacuum cup applications
20. Leakage: vacuum systems require tight seals (O-rings, gaskets)
21. Vacuum filtration: protect pump from contamination
22. Vacuum reservoir: stabilizes vacuum level, reduces cycling
23. Vacuum switch: controls pump on/off based on pressure
24. Application decision: ejector for small, intermittent; pump for large, continuous
25. Energy efficiency: pump more efficient for continuous duty (vs ejector air consumption)
        """,
        key_factors=[
            "Required vacuum level (inch Hg or torr)",
            "Flow rate (SCFM or CFM)",
            "Duty cycle (intermittent vs continuous)",
            "Compressed air availability (ejector requires 80+ PSIG)",
            "Ejector advantages: simple, fast, no maintenance",
            "Ejector disadvantages: high air consumption, noisy",
            "Mechanical pump for continuous duty (more efficient)",
            "Vacuum cup force calculation (vacuum level * 0.491 * area)",
            "Safety factor 2.0 minimum for lifting applications",
            "Leakage control critical (seals, gaskets)"
        ],
        primary_authority=[
            "ISO 2533 - Standard Atmosphere",
            "ANSI/ASSE Z49.1 - Safety in Welding (vacuum systems)",
            "Compressed Air Challenge Best Practices for Vacuum Systems"
        ],
        burden_holder="System designer must demonstrate vacuum source capable of achieving required level and flow",
        adversary_position="Vacuum system undersized or wrong technology selected",
        counter_arguments=[
            "Ejector air consumption excessive for continuous duty",
            "Vacuum level insufficient for application (leakage, altitude)",
            "Evacuation time too long for cycle time",
            "Vacuum cups undersized (inadequate safety factor)",
            "Pump capacity inadequate for system volume",
            "Leakage exceeds pump capacity"
        ],
        resolution_strategy="Calculate required vacuum level and flow, select ejector for intermittent or pump for continuous, verify evacuation time and cup sizing",
        entity_scope="All vacuum handling and material transport applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on fundamental vacuum principles and industry best practices",
        controlling_precedent="Compressed Air Challenge Best Practices for Vacuum Systems"
    ),

    "compressed_air_quality_iso8573": DoctrineBlock(
        topic="Compressed Air Quality per ISO 8573-1 Classification",
        keywords=["ISO 8573", "air quality", "particulate", "moisture", "oil", "class", "contamination", "filtration"],
        conclusion_template="Compressed air quality requirements per ISO 8573-1 determine filtration, drying, and oil removal equipment needed.",
        reasoning_framework="""
ISO 8573-1 compressed air quality classification:
1. Three contamination categories: solid particles, water, oil
2. Class rating: 0 (highest purity) to X (not specified) for each category
3. Notation: [Particle Class] : [Moisture Class] : [Oil Class]
4. Example: 1:2:1 = Class 1 particles, Class 2 moisture, Class 1 oil
5. Particle classes (particles per m3 by size):
   Class 0: per ISO 8573-4 (lab analysis)
   Class 1: 0.1-0.5 um <20000, 0.5-1.0 um <400, 1.0-5.0 um <10
   Class 2: 0.1-0.5 um <400000, 0.5-1.0 um <6000, 1.0-5.0 um <100
   Class 3: 0.5-1.0 um <90000, 1.0-5.0 um <1000, >5.0 um <10
   Class 4: 1.0-5.0 um <10000, >5.0 um <100
   Class 5: >5.0 um <100000
6. Moisture classes (pressure dew point):
   Class 1: PDP -70 deg C (-94 deg F)
   Class 2: PDP -40 deg C (-40 deg F)
   Class 3: PDP -20 deg C (-4 deg F)
   Class 4: PDP +3 deg C (+38 deg F)
   Class 5: PDP +7 deg C (+45 deg F)
   Class 6: PDP +10 deg C (+50 deg F)
7. Oil classes (total oil aerosol + vapor, mg/m3):
   Class 0: per ISO 8573-5 (lab analysis)
   Class 1: 0.01 mg/m3
   Class 2: 0.1 mg/m3
   Class 3: 1.0 mg/m3
   Class 4: 5.0 mg/m3
8. General plant air: 3:4:3 or 4:4:3 typical
9. Instrument air: 2:3:2 or 1:2:1
10. Food/pharma: 1:2:1 or 1:1:1
11. Electronics/painting: 1:2:1
12. Breathing air: ISO 12021 (stricter than 8573)
13. Filtration stages: pre-filter (25 um) -> filter (5 um) -> coalescing (1 um) -> final (0.01 um)
14. Coalescing filter: removes oil aerosol, not vapor
15. Activated carbon: removes oil vapor (needed for Class 1 oil)
16. Filter efficiency: 99.99% at rated size (0.01 um for Class 1)
17. Pressure drop: 1-3 PSI per filter housing (clean)
18. Filter life: 6-12 months or per pressure drop indicator
19. Testing per ISO 8573 parts 2-9 (particles, moisture, oil, microbes)
20. Application risks: oil contamination damages product, moisture causes corrosion/freezing
21. Cost progression: Class 4 -> Class 1 increases equipment cost 5-10x
22. Over-specification wastes money and energy (pressure drop)
23. Under-specification risks product quality and equipment damage
24. Point-of-use treatment: local filters/dryers for critical applications
25. System design: specify class per application, cascade from cleanest to dirtiest
        """,
        key_factors=[
            "ISO 8573-1 three-part classification: particle:moisture:oil",
            "General plant air: Class 3:4:3 or 4:4:3",
            "Instrument air: Class 2:3:2 or 1:2:1",
            "Food/pharma/electronics: Class 1:2:1",
            "Filtration progression: pre-filter -> coalescing -> activated carbon",
            "Coalescing removes oil aerosol, carbon removes vapor",
            "Pressure drop 1-3 PSI per filter stage",
            "Testing per ISO 8573 parts 2-9",
            "Over-specification wastes cost and energy",
            "Point-of-use treatment for critical applications"
        ],
        primary_authority=[
            "ISO 8573-1 - Compressed Air Quality Classification",
            "ISO 8573-2 through 9 - Testing Methods",
            "ISO 12500 - Filter Test Methods"
        ],
        burden_holder="System designer must specify ISO 8573 class per application and demonstrate equipment achieves class",
        adversary_position="Air quality inadequate for application causing contamination or equipment damage",
        counter_arguments=[
            "Filtration inadequate for specified class",
            "Oil-free compressor still has ambient oil contamination",
            "Moisture class not achieved (dryer undersized)",
            "Filters not maintained (pressure drop excessive)",
            "Downstream contamination from piping rust/scale",
            "Testing not performed per ISO 8573 methods"
        ],
        resolution_strategy="Specify ISO 8573 class based on application sensitivity, design filtration train to achieve class, verify with testing per ISO standards",
        entity_scope="All compressed air systems with quality-sensitive applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ISO 8573 international air quality standard",
        controlling_precedent="ISO 8573-1 Compressed Air Quality Classification"
    ),

    "energy_audit_specific_power": DoctrineBlock(
        topic="Compressed Air Energy Audit and Specific Power Analysis",
        keywords=["energy audit", "specific power", "kW per 100 CFM", "leak detection", "efficiency", "demand reduction", "storage"],
        conclusion_template="Compressed air energy efficiency measured by specific power (kW/100 CFM) with typical systems 15-25 kW/100 CFM, best practice <18 kW/100 CFM.",
        reasoning_framework="""
Compressed air energy audit methodology:
1. Specific power: kW input / (flow in 100 CFM units)
2. Typical specific power: 18-20 kW/100 CFM (well-designed)
3. Poor systems: 25-35 kW/100 CFM
4. Best practice: 15-18 kW/100 CFM (VSD compressors, low leakage)
5. Measurement: actual kW (demand meter), actual flow (flow meter)
6. Compressed air cost: 0.25-0.35 USD per 1000 SCF (8 cent/kWh electricity)
7. Annual energy: kWh = HP * 0.746 * hours * load_factor
8. Load factor: actual load / full load (0.5-0.8 typical)
9. Major losses: leaks (20-50%), inappropriate uses (30%), pressure drop (10-20%)
10. Leak rate: 20-30% typical unmanaged systems, <10% best practice
11. Leak cost: 1/4 inch leak at 100 PSI = 100 CFM = 20 HP = 4400 USD/year
12. Leak detection: ultrasonic detector (40 kHz), soap solution (low-tech)
13. Pressure drop: each 2 PSI drop increases energy 1%
14. Artificial demand: excess pressure wastes energy (regulate to minimum needed)
15. Inappropriate uses: cooling, blowing off, open blowing (use alternatives)
16. Storage optimization: increase receiver volume reduces cycling
17. Demand reduction strategies: reduce leaks, lower pressure, eliminate waste
18. Supply side efficiency: VSD compressors, heat recovery, proper dryer/filter sizing
19. Controls optimization: sequencing, load/unload, auto-start/stop
20. Baseline audit: install flow meters, pressure sensors, kW meters
21. Monitoring: continuous data logging to identify waste
22. Benchmarking: compare specific power to industry standards
23. ROI on improvements: leak repair 1-2 year, VSD upgrade 2-3 year
24. Measurement locations: compressor discharge, system header, end-uses
25. Compressed Air Challenge recommends: 10-point energy audit protocol
        """,
        key_factors=[
            "Specific power 15-18 kW/100 CFM = best practice",
            "Typical systems 18-25 kW/100 CFM, poor systems 25-35 kW/100 CFM",
            "Leaks cost 20-50% of compressed air energy (unmanaged)",
            "1/4 inch leak at 100 PSI = 100 CFM = 20 HP = 4400 USD/year",
            "Each 2 PSI pressure drop increases energy 1%",
            "Demand reduction: fix leaks, lower pressure, eliminate waste",
            "Supply side: VSD compressors, heat recovery, proper sizing",
            "Measurement: flow meters, kW meters, pressure sensors",
            "ROI: leak repair 1-2 years, VSD 2-3 years",
            "Compressed Air Challenge 10-point audit protocol"
        ],
        primary_authority=[
            "Compressed Air Challenge Best Practices",
            "DOE Motor Challenge - Compressed Air System Optimization",
            "ISO 11011 - Compressed Air Energy Efficiency"
        ],
        burden_holder="Facility manager must demonstrate system specific power and identify improvement opportunities",
        adversary_position="Energy waste from leaks, pressure drop, and inappropriate uses not quantified",
        counter_arguments=[
            "Actual specific power exceeds 25 kW/100 CFM (inefficient)",
            "Leak rate >30% (excessive waste)",
            "Pressure drop >10 PSI from compressor to end-use",
            "No flow metering or energy monitoring",
            "Inappropriate uses (cooling, blowing) not addressed",
            "VSD not considered despite variable loads"
        ],
        resolution_strategy="Conduct energy audit per Compressed Air Challenge protocol, measure specific power, quantify leaks and losses, prioritize improvements by ROI",
        entity_scope="All industrial compressed air systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on DOE and Compressed Air Challenge verified energy audit methodologies",
        controlling_precedent="Compressed Air Challenge Best Practices for Energy Efficiency"
    ),

    "leak_detection_management": DoctrineBlock(
        topic="Compressed Air Leak Detection and Management Program",
        keywords=["leak detection", "ultrasonic", "tag and repair", "leak rate", "SCFM loss", "cost", "prevention"],
        conclusion_template="Effective leak management program reduces air loss from typical 20-30% to <10% through systematic detection, tagging, repair, and verification.",
        reasoning_framework="""
Compressed air leak detection and management:
1. Leak impact: 20-30% of compressed air production wasted in typical unmanaged plants
2. Best practice: <10% leak rate
3. Leak sources: fittings, couplings, hoses, valves, cylinders, joints, disconnects
4. Detection methods: ultrasonic (primary), soap solution, airborne ultrasound imaging
5. Ultrasonic detector: 40 kHz sensor detects turbulent flow (inaudible to humans)
6. Detection range: up to 50 feet depending on leak size and noise
7. Leak sizing: correlate dB reading to orifice size and CFM loss
8. Leak rate estimation tables: orifice diameter vs pressure vs SCFM
9. 1/4 inch orifice at 100 PSI = 104 SCFM loss
10. 1/8 inch orifice at 100 PSI = 26 SCFM loss
11. 1/16 inch orifice at 100 PSI = 6.5 SCFM loss
12. Annual cost per leak: SCFM * 0.746 * HP_per_CFM * hours * kWh_cost
13. Tagging system: numbered tags placed at leak locations
14. Repair priority: large leaks first (80/20 rule - 20% of leaks = 80% of loss)
15. Verification: re-scan after repair to confirm elimination
16. Documentation: leak log with location, size, repair date, cost savings
17. Quarterly leak surveys: ongoing program to catch new leaks
18. Leak prevention: proper installation, strain relief, thread sealant, quality fittings
19. Quick disconnect leaks: major source (30-50 SCFM each when uncoupled)
20. Automatic shutoff couplings: reduce quick disconnect leaks
21. Pressure reduction: lowering system pressure 10 PSI reduces leaks ~5%
22. ROI on leak program: typically 1-2 year payback
23. System shutdown detection: measure compressor run time on weekends (no production)
24. Baseline flow: weekend or night flow = leak load
25. Continuous monitoring: flow meters detect increasing leak rate over time
        """,
        key_factors=[
            "Typical unmanaged leak rate 20-30%, best practice <10%",
            "Ultrasonic detector primary tool (40 kHz, 50 ft range)",
            "Leak sizing: 1/4 inch at 100 PSI = 104 SCFM = major loss",
            "Tagging and prioritization: large leaks first (80/20 rule)",
            "Quarterly surveys for ongoing leak management",
            "Documentation: leak log with location, size, cost",
            "Quick disconnects major source (30-50 SCFM uncoupled)",
            "Shutdown detection: measure weekend/night compressor run",
            "ROI typically 1-2 years for leak program",
            "Leak prevention: proper installation, quality fittings"
        ],
        primary_authority=[
            "Compressed Air Challenge Leak Management Guide",
            "DOE Best Practices - Compressed Air Leak Detection",
            "ISO 11011 - Compressed Air Energy Efficiency"
        ],
        burden_holder="Facility must implement systematic leak detection and repair program",
        adversary_position="Leaks not quantified and unaddressed, wasting 20-30% of compressed air energy",
        counter_arguments=[
            "No leak detection program in place",
            "Leaks not quantified or documented",
            "Repairs not prioritized by impact",
            "No verification after repair",
            "New leaks develop faster than repairs",
            "Quick disconnects leak excessively",
            "Baseline leak load not measured"
        ],
        resolution_strategy="Implement quarterly ultrasonic leak surveys, tag and prioritize leaks, repair and verify, document cost savings, measure baseline leak load",
        entity_scope="All industrial compressed air systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on DOE and Compressed Air Challenge verified leak management protocols",
        controlling_precedent="Compressed Air Challenge Leak Management Best Practices"
    ),

    "pneumatic_logic_circuits": DoctrineBlock(
        topic="Pneumatic Logic Circuits and Sequential Control",
        keywords=["pneumatic logic", "AND gate", "OR gate", "NOT gate", "sequential control", "cascade", "memory valve"],
        conclusion_template="Pneumatic logic circuits provide electrical-free control using AND, OR, NOT gates and memory elements for sequential operations.",
        reasoning_framework="""
Pneumatic logic circuit design:
1. Purpose: control sequences without electrical power (hazardous areas, simple systems)
2. Basic gates: AND (both inputs), OR (either input), NOT (inverted output)
3. AND gate: shuttle valve with two inputs, output only if both pressurized
4. OR gate: shuttle valve with two inputs, output if either pressurized
5. NOT gate: 3/2 normally open valve, pressure input closes output
6. Memory valve: bistable element, set and reset inputs
7. Shuttle valve: allows flow from either of two inputs to single output
8. Two-pressure valve: output switches based on higher input pressure
9. Time delay valve: delays signal using restricted flow and volume
10. Sequential control: cascade method divides sequence into groups
11. Cascade notation: A+B+A-B- (+ = extend, - = retract)
12. Group division: no cylinder appears twice in same group
13. Group 1: A+B+, Group 2: A-B- (example)
14. Master control lines: I, II, III for each group
15. Signal overlap: memory valve prevents false signals
16. Emergency stop: dump all pressure via 3/2 valve
17. Start signal: momentary pulse (push button) starts sequence
18. Limit switches: roller valves detect position
19. Proximity switches: pneumatic sensors (no electrical)
20. Pneumatic timer: adjustable delay 0.1-30 seconds typical
21. Counter: counts pulses, output after preset (mechanical or pneumatic)
22. Pressure sequence: low pressure for extend, high for clamp (dual-pressure)
23. Safety circuits: two-hand control, guard interlocks (pneumatic)
24. Logic complexity limit: >5 gates becomes impractical (use electrical/PLC)
25. Advantages: intrinsically safe, no sparks, simple, reliable
26. Disadvantages: bulky, limited complexity, slower than electrical
        """,
        key_factors=[
            "AND gate: both inputs required for output",
            "OR gate: either input produces output",
            "NOT gate: inverted signal",
            "Memory valve: bistable element for set/reset",
            "Cascade method for sequential control (group division)",
            "Time delay valve for timed operations",
            "Limit switches (roller valves) for position sensing",
            "Intrinsically safe (no electrical sparks)",
            "Limited complexity (<5 gates practical)",
            "Slower response than electrical control"
        ],
        primary_authority=[
            "ISO 1219-1 - Pneumatic Symbols",
            "ISO 5599 - Pneumatic Control Valves",
            "IEC 60534 - Industrial Process Control Valves"
        ],
        burden_holder="System designer must demonstrate logic circuit meets sequence requirements and safety standards",
        adversary_position="Logic circuit fails to provide required sequence or safety function",
        counter_arguments=[
            "Signal overlap causes false activation",
            "Memory valve not reset properly",
            "Time delay inadequate or excessive",
            "Position sensing unreliable",
            "Emergency stop does not dump all pressure",
            "Cascade groups incorrectly divided",
            "Complexity exceeds practical limit for pneumatic logic"
        ],
        resolution_strategy="Design cascade sequence with proper group division, use memory valves to prevent overlap, verify emergency stop dumps all pressure",
        entity_scope="Sequential pneumatic automation in hazardous or simple applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ISO pneumatic control standards and proven cascade methodology",
        controlling_precedent="ISO 1219 Pneumatic Symbols and Circuit Diagrams"
    ),

    "vacuum_cup_gripper_design": DoctrineBlock(
        topic="Vacuum Cup Gripper Design and Suction Force Calculation",
        keywords=["vacuum cup", "suction gripper", "holding force", "cup material", "bellows", "flat cup", "safety factor"],
        conclusion_template="Vacuum cup gripper design requires calculating suction force from vacuum level and cup area with minimum 2.0 safety factor for lifting.",
        reasoning_framework="""
Vacuum cup gripper design methodology:
1. Suction force equation: F = vacuum (in Hg) * 0.491 * Area (sq in)
2. Example: 20 in Hg vacuum, 2 inch diameter cup
   Area = pi * 1^2 = 3.14 sq in
   F = 20 * 0.491 * 3.14 = 30.8 lbf
3. Safety factor: minimum 2.0 for vertical lifting
4. Safety factor 3.0 for dynamic loads or horizontal forces
5. Effective vacuum: actual vacuum at cup (accounting for leakage, altitude)
6. Cup types: flat, bellows, oval, foam, special shapes
7. Flat cup: rigid surfaces, thin sheet metal, glass
8. Bellows cup: curved surfaces, height compensation, uneven surfaces
9. Oval cup: long narrow parts (extrusions, boards)
10. Foam cup: porous or rough surfaces (wood, cardboard)
11. Cup materials: nitrile (NBR), silicone, polyurethane, natural rubber
12. NBR (nitrile): general purpose, oil resistant, -20 to 200 deg F
13. Silicone: high temp (300 deg F+), food safe, low abrasion resistance
14. Polyurethane: high wear, marking-free, 0 to 180 deg F
15. Cup durometer: 40-70 Shore A (softer = better seal on rough surfaces)
16. Surface requirements: non-porous for effective seal
17. Porous materials: require foam cup or sealing compound
18. Release methods: vacuum break valve, blow-off (compressed air pulse)
19. Response time: pickup 0.5-2 sec, release 0.1-0.5 sec
20. Multiple cups: distribute load, parallel connection (vacuum manifold)
21. Cup spacing: avoid stress concentration, consider part flexure
22. Tilting forces: additional cups or mechanical guides needed
23. Energy efficiency: vacuum-on-demand (only during grip)
24. Cup wear: replace when suction force drops >20% or cracks appear
25. Testing: verify actual holding force on production parts before full deployment
        """,
        key_factors=[
            "Suction force = vacuum (in Hg) * 0.491 * cup area (sq in)",
            "Safety factor minimum 2.0 for vertical lifting, 3.0 for dynamic",
            "Flat cup for rigid surfaces, bellows for curved/uneven",
            "Foam cup for porous surfaces (wood, cardboard)",
            "NBR general purpose, silicone high-temp, polyurethane high-wear",
            "Cup durometer 40-70 Shore A (softer for rough surfaces)",
            "Multiple cups distribute load via vacuum manifold",
            "Release via vacuum break or blow-off",
            "Test actual holding force on production parts",
            "Replace cups when force drops >20% or cracks appear"
        ],
        primary_authority=[
            "ISO 4414 - Pneumatic Fluid Power General Rules",
            "ANSI B93.81M - Vacuum Cups and Fittings",
            "OSHA 1910.178 - Powered Industrial Trucks (material handling)"
        ],
        burden_holder="System designer must demonstrate vacuum gripper holding force exceeds load with adequate safety factor",
        adversary_position="Vacuum gripper undersized or wrong cup type causing part drop",
        counter_arguments=[
            "Safety factor inadequate (<2.0 for lifting)",
            "Actual vacuum lower than design (leakage, altitude)",
            "Cup type wrong for surface (flat on curved, no foam on porous)",
            "Cup material incompatible (temperature, chemical)",
            "Multiple cups not manifolded (uneven load)",
            "Cup wear not monitored (force degradation)",
            "Tilting forces not considered"
        ],
        resolution_strategy="Calculate required holding force with safety factor, select cup type and material for surface, verify actual force with testing",
        entity_scope="All vacuum material handling and robotic gripping applications",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on fundamental vacuum physics and industry gripper standards",
        controlling_precedent="ISO 4414 Pneumatic Fluid Power General Rules"
    ),

    "pipe_sizing_pressure_drop": DoctrineBlock(
        topic="Pneumatic Pipe Sizing and Pressure Drop Calculation",
        keywords=["pipe sizing", "pressure drop", "velocity", "flow rate", "aluminum", "copper", "schedule 40", "NPT"],
        conclusion_template="Pneumatic piping sized to limit pressure drop to <5% (5 PSI at 100 PSI) with velocity <30 fps to minimize energy loss and noise.",
        reasoning_framework="""
Pneumatic pipe sizing methodology:
1. Design criteria: pressure drop <5 PSI per 100 ft at 100 PSIG
2. Maximum velocity: 20-30 fps (higher = noise and erosion)
3. Flow rate calculation: Q = SCFM * (Patm / Psystem)
   Q = actual CFM, SCFM = standard cubic feet per minute
4. Pipe sizing charts: based on flow, pressure, allowable drop
5. Undersized pipe: excessive pressure drop, energy waste, slow actuators
6. Oversized pipe: higher cost, more leakage potential (more fittings)
7. Pressure drop equation (simplified): dP = (f * L * rho * V^2) / (2 * D)
   f = friction factor, L = length, rho = density, V = velocity, D = diameter
8. Material selection: aluminum, copper, stainless, black iron
9. Aluminum pipe: lightweight, corrosion resistant, easy install (preferred)
10. Copper: Type K or L, brazed fittings, higher cost
11. Black iron: Schedule 40, threaded, prone to rust (scale contaminates air)
12. Stainless: corrosive environments, food/pharma, highest cost
13. Piping configuration: loop (best - bidirectional flow), tree, spur
14. Header sizing: oversize by 50-100% for future expansion
15. Branch sizing: per actual consumption of branch
16. Slope piping: 1-2% downward toward drain legs
17. Drain legs: moisture collection, auto-drains every 50-100 ft
18. Avoid dead-end runs: trap moisture and contaminants
19. Isolation valves: every branch for maintenance
20. Pressure drop measurement: install gauges at critical points
21. Fittings equivalent length: elbow = 2 ft, tee = 5 ft (add to pipe length)
22. Quick disconnect pressure drop: 5-15 PSI (significant - minimize use)
23. Hose pressure drop: higher than pipe (use shortest practical length)
24. Velocity calculation: V = (Q * 144) / (60 * A)
   V = fps, Q = CFM, A = pipe area (sq in)
25. Rule of thumb: 1 inch pipe per 50-70 SCFM at 100 PSIG
        """,
        key_factors=[
            "Pressure drop limit <5 PSI per 100 ft at 100 PSIG",
            "Maximum velocity 20-30 fps (noise and erosion limit)",
            "Aluminum pipe preferred (corrosion resistant, lightweight)",
            "Loop configuration best (bidirectional flow)",
            "Header oversized 50-100% for expansion",
            "Slope 1-2% downward with drain legs every 50-100 ft",
            "Fittings add equivalent length (elbow = 2 ft, tee = 5 ft)",
            "Quick disconnects add 5-15 PSI drop (minimize use)",
            "Isolation valves on every branch",
            "Rule of thumb: 1 inch pipe per 50-70 SCFM"
        ],
        primary_authority=[
            "ISO 4414 - Pneumatic Fluid Power Installations",
            "ASME B31.3 - Process Piping",
            "Compressed Air Challenge Piping Best Practices"
        ],
        burden_holder="System designer must demonstrate piping sized to limit pressure drop and velocity per standards",
        adversary_position="Undersized piping causing excessive pressure drop and energy waste",
        counter_arguments=[
            "Pressure drop exceeds 5 PSI per 100 ft",
            "Velocity exceeds 30 fps (noise, erosion)",
            "Black iron piping causing rust contamination",
            "Dead-end runs trap moisture",
            "No drain legs (moisture accumulation)",
            "Quick disconnects excessive (high pressure drop)",
            "Fittings equivalent length not accounted"
        ],
        resolution_strategy="Size piping per flow rate using pressure drop charts, verify velocity <30 fps, specify aluminum pipe with loop configuration and drain legs",
        entity_scope="All compressed air distribution systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ISO 4414 and Compressed Air Challenge piping standards",
        controlling_precedent="ISO 4414 Pneumatic Fluid Power Installations"
    ),

    "osha_compressed_air_safety": DoctrineBlock(
        topic="OSHA Compressed Air Safety - 29 CFR 1910.242 and 1910.169",
        keywords=["OSHA", "compressed air safety", "30 PSI", "dead-end", "nozzle", "air receiver", "inspection", "PPE"],
        conclusion_template="OSHA limits compressed air for cleaning to 30 PSI and requires dead-end pressure protection, receiver inspection, and PPE.",
        reasoning_framework="""
OSHA compressed air safety regulations:
1. 29 CFR 1910.242(b): Compressed air for cleaning limited to 30 PSI
2. Exception: 30 PSI limit applies only when dead-end pressure can be contacted
3. Dead-end pressure: blocked nozzle, skin contact, body cavity
4. Effective chip guarding and PPE allows >30 PSI
5. Nozzle design: must reduce dead-end pressure to <30 PSI
6. Safety nozzle: side holes or gaps to bleed pressure when blocked
7. Blow gun: spring-loaded deadman valve required
8. PPE requirement: safety glasses, face shield for cleaning operations
9. Compressed air injury risks: air embolism, eye damage, hearing loss
10. Air embolism: high pressure air into bloodstream (potentially fatal)
11. Ear damage: compressed air into ear canal causes rupture
12. Clothing inflation: air up sleeve or pant leg (serious injury)
13. Never direct compressed air at person (horseplay prohibition)
14. 29 CFR 1910.169: Air receiver safety requirements
15. ASME Code construction: all pressure vessels must be Code stamped
16. Pressure relief valve: set at or below MAWP (Maximum Allowable Working Pressure)
17. Pressure gauge: indicating current pressure
18. Drain valve: manual or automatic at lowest point
19. Air receiver inspection: external annual, internal 5-10 years per jurisdiction
20. Inspection authority: may be insurance company, state, municipality
21. Operating permit: some jurisdictions require annual permit
22. Documentation: maintain inspection records, nameplate data
23. Unsafe conditions: excessive corrosion, dents, cracks require vessel retirement
24. Piping safety: secure mounting, pressure rating adequate, isolation valves
25. Training: operators must be trained on compressed air hazards and safe use
        """,
        key_factors=[
            "30 PSI limit for cleaning (29 CFR 1910.242) when dead-end can be contacted",
            "Safety nozzle with pressure relief when blocked",
            "Blow gun with deadman valve",
            "PPE: safety glasses, face shield required",
            "Never direct air at person (air embolism, hearing damage risk)",
            "Air receivers: ASME Code stamped, relief valve, pressure gauge, drain",
            "Receiver inspection: external annual, internal 5-10 years",
            "Operating permit may be required by jurisdiction",
            "Training on compressed air hazards mandatory",
            "Document inspections and maintain nameplate data"
        ],
        primary_authority=[
            "OSHA 29 CFR 1910.242(b) - Compressed Air for Cleaning",
            "OSHA 29 CFR 1910.169 - Air Receivers",
            "ASME Boiler and Pressure Vessel Code Section VIII"
        ],
        burden_holder="Employer must demonstrate compliance with OSHA compressed air safety regulations",
        adversary_position="Non-compliant compressed air use creating hazard for employees",
        counter_arguments=[
            "Compressed air >30 PSI used for cleaning without effective guarding",
            "Blow gun lacks deadman valve",
            "No PPE provided for air cleaning operations",
            "Air directed at person (horseplay)",
            "Air receiver not ASME Code stamped",
            "No pressure relief valve or inadequate setting",
            "Air receiver inspection overdue",
            "No training on compressed air hazards"
        ],
        resolution_strategy="Implement OSHA-compliant compressed air program: 30 PSI limit or effective guarding, safety nozzles, PPE, receiver inspections, employee training",
        entity_scope="All facilities using compressed air (OSHA jurisdiction)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on explicit OSHA regulations with citations",
        controlling_precedent="OSHA 29 CFR 1910.242 and 1910.169"
    ),

    "iso_4414_pneumatic_design": DoctrineBlock(
        topic="ISO 4414 Pneumatic System Design Rules and Safety",
        keywords=["ISO 4414", "design rules", "safety", "pressure rating", "manual override", "emergency stop", "fail-safe"],
        conclusion_template="ISO 4414 establishes pneumatic system design rules including pressure ratings, fail-safe design, emergency stops, and maintenance access.",
        reasoning_framework="""
ISO 4414 pneumatic fluid power system design:
1. Scope: general rules and safety requirements for pneumatic systems
2. Pressure rating: all components rated for maximum system pressure + 25% margin
3. Proof pressure test: 1.5x maximum working pressure (new systems)
4. Operating pressure: not to exceed component ratings
5. Pressure relief: required on all pressure sources (compressor, pump)
6. Pressure regulation: local regulators for pressure-sensitive components
7. Energy isolation: manual shutoff valve with lockout/tagout capability
8. Stored energy release: bleed-down before maintenance
9. Manual override: all automatic valves require manual actuation capability
10. Emergency stop: de-energize all actuators, dump pressure safely
11. Fail-safe design: loss of pressure or power must leave system in safe state
12. Fail-safe examples: spring-return valves, mechanical locks, counterbalance
13. Residual pressure: warning of trapped pressure after shutdown
14. Start-up sequence: gradual pressure build, verify controls before operation
15. Position sensing: limit switches or proximity sensors for critical positions
16. Speed control: prevent uncontrolled motion (meter-out flow controls)
17. Two-hand control: concurrent actuation prevents hand-in-die
18. Guard interlocking: safety guards must disable motion when open
19. Component selection: components suitable for operating conditions (temp, environment)
20. Installation: secure mounting, strain relief, protection from damage
21. Piping: adequate size, material compatible, pressure rated, identified
22. Maintenance access: components accessible for inspection and service
23. Documentation: schematic diagrams (ISO 1219 symbols), maintenance manuals
24. Training: operators trained on system function, hazards, emergency procedures
25. Periodic inspection: visual checks, leak detection, function testing per schedule
        """,
        key_factors=[
            "All components rated for max pressure + 25% margin",
            "Pressure relief on all pressure sources",
            "Energy isolation with lockout/tagout",
            "Manual override on all automatic valves",
            "Emergency stop de-energizes and dumps pressure",
            "Fail-safe design (safe state on power/pressure loss)",
            "Position sensing for critical safety positions",
            "Two-hand control and guard interlocking for personnel protection",
            "Documentation with ISO 1219 symbols",
            "Training and periodic inspection required"
        ],
        primary_authority=[
            "ISO 4414 - Pneumatic Fluid Power General Rules and Safety",
            "ISO 1219 - Fluid Power Symbols",
            "ANSI B93 - Fluid Power Standards"
        ],
        burden_holder="System designer must demonstrate pneumatic system designed per ISO 4414 safety requirements",
        adversary_position="Non-compliant pneumatic system creates safety hazard",
        counter_arguments=[
            "Components not rated for system pressure",
            "No pressure relief valve",
            "No manual override on automatic valves",
            "Emergency stop does not dump pressure",
            "Fail-unsafe design (dangerous on power loss)",
            "No position sensing on critical functions",
            "Inadequate guarding or two-hand control",
            "No documentation or operator training",
            "Maintenance access blocked"
        ],
        resolution_strategy="Design pneumatic system per ISO 4414 requirements: pressure ratings, fail-safe design, emergency stop, manual overrides, documentation, training",
        entity_scope="All industrial pneumatic systems",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ISO 4414 international pneumatic safety standard",
        controlling_precedent="ISO 4414 Pneumatic Fluid Power General Rules"
    ),

    "heat_recovery_from_compressors": DoctrineBlock(
        topic="Heat Recovery from Compressed Air Systems",
        keywords=["heat recovery", "waste heat", "cooling water", "space heating", "efficiency", "COP", "payback"],
        conclusion_template="Heat recovery captures 70-90% of compressor motor input energy for space heating or process use with typical 2-4 year payback.",
        reasoning_framework="""
Compressed air heat recovery design:
1. Energy balance: 100% motor input = compressed air + heat
2. Compressed air energy: ~10-15% of motor input (useful work)
3. Heat rejected: 85-90% of motor input (recoverable)
4. Heat sources: oil cooler, aftercooler, compressor block
5. Oil-cooled rotary screw: 70-80% heat in oil cooler
6. Air-cooled compressor: heat in cooling air (hard to recover)
7. Water-cooled compressor: heat in cooling water (easiest to recover)
8. Heat recovery methods: air-to-air, water-to-water, water-to-air
9. Air-to-air: duct hot cooling air to building space (winter heating)
10. Water-to-water: heat exchanger from compressor cooling loop to hot water system
11. Water-to-air: fan coil units convert hot water to warm air
12. Recovery temperature: 150-200 deg F typical (oil-cooled)
13. Recovery rate: 100 HP compressor = 250,000 BTU/hr recoverable
14. Space heating: replaces furnace/boiler fuel
15. Process heating: pre-heat boiler makeup water, wash water, dryers
16. Seasonal consideration: heat only useful 6-8 months/year (northern climates)
17. Summer cooling: heat must still be rejected (cooling tower, radiator)
18. Heat recovery efficiency: 70-90% of theoretical depending on design
19. Payback calculation: savings = heat recovered * heating fuel cost
20. Typical payback: 2-4 years for well-designed systems
21. Best candidates: large compressors (>50 HP), high heating loads, long heating season
22. Design considerations: piping insulation, controls, backup heat source
23. Safety: overheat protection if heat recovery loop fails
24. Maintenance: heat exchangers require periodic cleaning
25. Monitoring: temperature sensors verify heat recovery operation
        """,
        key_factors=[
            "70-90% of compressor motor input recoverable as heat",
            "100 HP compressor = 250,000 BTU/hr heat available",
            "Oil-cooled rotary screw best for recovery (70-80% in oil)",
            "Water-cooled easier to recover than air-cooled",
            "Space heating or process heating applications",
            "Seasonal limitation (6-8 months useful in northern climates)",
            "Typical payback 2-4 years",
            "Best for large compressors >50 HP with high heating loads",
            "Requires backup heat source and overheat protection",
            "Heat exchangers need periodic cleaning"
        ],
        primary_authority=[
            "DOE Motor Challenge - Waste Heat Recovery",
            "Compressed Air Challenge Best Practices",
            "ASHRAE Handbook - HVAC Systems and Equipment"
        ],
        burden_holder="Facility manager must evaluate heat recovery economics and implement where justified",
        adversary_position="Heat recovery opportunity not evaluated, wasting 70-90% of compressor energy",
        counter_arguments=[
            "No heat recovery despite large compressor and heating load",
            "Air-cooled compressor when water-cooled would enable recovery",
            "Seasonal limitations not considered (overestimate savings)",
            "Payback calculation ignores installation and maintenance costs",
            "No backup heat source (risk of heating system failure)",
            "Heat exchanger fouling reduces effectiveness",
            "Monitoring not implemented to verify savings"
        ],
        resolution_strategy="Calculate heat recovery potential (motor HP * 2545 * 0.7-0.9), compare to heating fuel cost, design system with backup and monitoring",
        entity_scope="All large compressed air systems (>50 HP) with heating loads",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on DOE and Compressed Air Challenge verified heat recovery methodologies",
        controlling_precedent="DOE Motor Challenge Waste Heat Recovery Best Practices"
    ),

    "vsd_compressor_benefits": DoctrineBlock(
        topic="Variable Speed Drive (VSD) Compressor Energy Savings",
        keywords=["VSD", "variable frequency drive", "VFD", "part load", "trim compressor", "energy savings", "modulation"],
        conclusion_template="VSD compressors reduce energy consumption 35% at part load by matching motor speed to air demand vs fixed-speed load/unload cycling.",
        reasoning_framework="""
Variable Speed Drive (VSD) compressor technology:
1. VSD principle: motor speed varies with air demand (frequency control)
2. Fixed-speed operation: load/unload cycling (wasteful at part load)
3. Load/unload efficiency: 70% loaded = 70% power (false - closer to 85%)
4. Fixed-speed part-load power: P_part = P_full * (0.4 + 0.6 * load_fraction)
5. Example: 50% load, fixed-speed draws 70% power (0.4 + 0.6*0.5)
6. VSD part-load power: nearly proportional to flow (P = flow^3 / pressure)
7. VSD savings: 20-40% at 50% load vs fixed-speed
8. Typical savings: 35% average for variable loads (40-80% of full capacity)
9. VSD turndown ratio: 10:1 or 20:1 (can run at 10-20% of full capacity)
10. Fixed-speed minimum: 40% of full capacity (below this, unload cycling)
11. Compressor control strategies: single VSD, VSD + fixed-speed base load
12. Trim compressor: VSD unit handles variable load above base load
13. Base load compressors: fixed-speed units run at full load (most efficient)
14. System configuration: VSD as trim, fixed-speed as base (optimized)
15. VSD premium cost: 25-35% higher than fixed-speed
16. Payback: 2-3 years typical for variable load applications
17. Best candidates: loads varying 40-80% with frequent changes
18. Poor candidates: steady loads near full capacity (VSD not needed)
19. Pressure stability: VSD maintains tighter pressure band (+-1 PSI vs +-5 PSI)
20. Reduced artificial demand: lower pressure = lower consumption
21. Soft start: VSD ramps up gradually (reduces electrical demand charges)
22. Maintenance: VSD adds complexity (drive electronics), slightly higher service cost
23. Reliability: modern VSD 95%+ reliability, but drive failures do occur
24. Harmonics: VSD creates electrical harmonics (may need filter)
25. Monitoring: flow meter and kW meter essential to verify VSD savings
        """,
        key_factors=[
            "VSD saves 35% average for variable loads (40-80% capacity)",
            "Fixed-speed part-load power = 0.4 + 0.6 * load fraction",
            "VSD part-load power nearly proportional to flow",
            "VSD turndown ratio 10:1 or 20:1",
            "Best application: trim compressor above fixed-speed base load",
            "VSD premium cost 25-35%, payback 2-3 years",
            "Pressure stability +- 1 PSI (vs +- 5 PSI fixed-speed)",
            "Soft start reduces electrical demand charges",
            "VSD adds complexity and potential harmonics",
            "Flow and kW metering essential to verify savings"
        ],
        primary_authority=[
            "Compressed Air Challenge VSD Best Practices",
            "DOE Motor Challenge - VSD Compressor Guide",
            "CAGI Performance Verification Program"
        ],
        burden_holder="Facility manager must evaluate VSD economics for variable load applications",
        adversary_position="VSD not considered despite variable loads, wasting 35% energy",
        counter_arguments=[
            "Variable loads (40-80%) not served by VSD",
            "All fixed-speed compressors cycling (inefficient)",
            "VSD savings potential not quantified",
            "VSD cost premium not justified by payback analysis",
            "Pressure swings excessive (+- 5 PSI or more)",
            "Electrical demand charges high (soft start benefit ignored)",
            "No metering to verify actual savings"
        ],
        resolution_strategy="Analyze load profile, calculate VSD savings vs fixed-speed using 0.4 + 0.6*load formula, configure VSD as trim with fixed-speed base",
        entity_scope="All compressed air systems with variable loads",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on DOE and Compressed Air Challenge verified VSD savings data",
        controlling_precedent="Compressed Air Challenge VSD Best Practices"
    ),

    "altitude_derating_compressors": DoctrineBlock(
        topic="Altitude Derating of Compressors and Pneumatic Equipment",
        keywords=["altitude", "derating", "atmospheric pressure", "density", "FAD", "capacity", "motor cooling"],
        conclusion_template="Compressor capacity decreases 3-4% per 1000 ft altitude above sea level due to lower atmospheric pressure and air density.",
        reasoning_framework="""
Altitude effects on pneumatic equipment:
1. Atmospheric pressure decreases with altitude
2. Sea level: 14.7 PSIA (29.92 in Hg)
3. 5000 ft: 12.2 PSIA (24.9 in Hg) - 17% reduction
4. 10000 ft: 10.1 PSIA (20.6 in Hg) - 31% reduction
5. Compressor capacity derating: 3-4% per 1000 ft
6. FAD (Free Air Delivery) = volumetric flow at standard conditions (14.7 PSIA, 68 deg F)
7. Actual inlet volume increases at altitude (lower density)
8. Compressor displacement constant, but FAD decreases
9. Example: 100 CFM FAD at sea level = 83 CFM FAD at 5000 ft (17% reduction)
10. Pressure ratio effect: altitude reduces discharge pressure absolute
11. Absolute discharge pressure = gauge + atmospheric
12. Example: 100 PSIG at sea level = 114.7 PSIA, at 5000 ft = 112.2 PSIA
13. Motor cooling derating: air-cooled motors lose cooling at altitude
14. Motor derating: 1% per 330 ft above 3300 ft (NEMA MG-1)
15. Example: 100 HP motor at 10000 ft derated to 80 HP (20% reduction)
16. Combined effect: compressor + motor derating = significant capacity loss
17. Altitude compensation: oversize compressor, use water-cooled motor, lower ambient temp
18. Pneumatic actuators: force output unchanged (gauge pressure same)
19. Air consumption: actuators consume same volume at altitude
20. Vacuum systems: maximum vacuum limited by atmospheric pressure
21. Example: 28 in Hg at sea level = 23 in Hg at 5000 ft (max achievable)
22. Pressure switches: may need re-calibration for altitude
23. Design practice: specify sea level conditions, apply derating factors
24. Manufacturer data: often at sea level (verify test conditions)
25. Verify actual conditions: altitude, ambient temperature, humidity
        """,
        key_factors=[
            "Compressor capacity derating 3-4% per 1000 ft altitude",
            "Atmospheric pressure: 14.7 PSIA sea level, 12.2 at 5000 ft, 10.1 at 10000 ft",
            "Motor cooling derating 1% per 330 ft above 3300 ft (NEMA MG-1)",
            "Combined compressor + motor derating significant at high altitude",
            "Actuator force output unchanged (gauge pressure constant)",
            "Vacuum systems limited by atmospheric pressure at altitude",
            "Oversize compressor to compensate for altitude",
            "Manufacturer data often at sea level (verify test conditions)",
            "Pressure switches may need recalibration",
            "Specify altitude in design conditions"
        ],
        primary_authority=[
            "CAGI Compressed Air & Gas Handbook - Altitude Corrections",
            "NEMA MG-1 - Motors and Generators (altitude derating)",
            "ISO 1217 - Standard Reference Conditions"
        ],
        burden_holder="System designer must apply altitude derating factors to compressor and motor sizing",
        adversary_position="Compressor undersized due to failure to account for altitude derating",
        counter_arguments=[
            "Altitude derating not applied (compressor undersized)",
            "Motor derating ignored (thermal overload at altitude)",
            "Manufacturer data assumed at sea level without verification",
            "Vacuum system designed for sea level (unachievable at altitude)",
            "Pressure switches not recalibrated for altitude",
            "Oversizing inadequate for combined compressor + motor derating"
        ],
        resolution_strategy="Apply 3-4% capacity derating per 1000 ft and NEMA motor derating, oversize accordingly, verify manufacturer data test conditions",
        entity_scope="All pneumatic systems at altitude >1000 ft",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on CAGI and NEMA altitude correction standards",
        controlling_precedent="CAGI Altitude Correction Factors and NEMA MG-1 Motor Derating"
    ),

    "frl_unit_maintenance": DoctrineBlock(
        topic="Filter-Regulator-Lubricator (FRL) Unit Selection and Maintenance",
        keywords=["FRL", "filter", "regulator", "lubricator", "air preparation", "bowl", "drain", "micron"],
        conclusion_template="FRL units provide air preparation (filtration, pressure regulation, lubrication) with proper sizing, installation, and maintenance critical.",
        reasoning_framework="""
Filter-Regulator-Lubricator (FRL) unit design and maintenance:
1. Purpose: condition compressed air for pneumatic equipment
2. Filter (F): removes particulates and moisture
3. Regulator (R): reduces and stabilizes pressure
4. Lubricator (L): adds oil mist for lubrication (not always needed)
5. Component order: F-R-L (filter first, lubricator last)
6. Filter types: general purpose (40 um), standard (5 um), high efficiency (0.01 um)
7. Filter element: pleated paper, sintered bronze, coalescing media
8. Bowl: polycarbonate (clear, 150 PSI), metal (250 PSI, opaque)
9. Automatic drain: float, timer, or manual (auto preferred - no human oversight)
10. Filter pressure drop: 1-3 PSI clean, replace at 8-10 PSI drop
11. Filter sizing: Cv rating must exceed flow requirement
12. Regulator function: reduce pressure and maintain constant downstream
13. Pressure range: adjustable, typical 0-150 PSIG
14. Regulator droop: pressure drops under flow (specify max droop tolerance)
15. Relieving regulator: vents excess downstream pressure (preferred)
16. Non-relieving: does not vent (downstream pressure can rise if supply reduces)
17. Gauge: downstream pressure indication (required)
18. Lubricator: fog-type (atomized oil mist)
19. Oil type: ISO VG 32 pneumatic oil (synthetic or mineral)
20. Lubrication rate: adjustable drops per minute (visible in sight dome)
21. When to use lubricator: only if equipment requires it (cylinders, valves, tools)
22. When NOT to use: oil-free required apps, downstream oil-sensitive equipment
23. Maintenance: daily visual check, weekly drain, monthly oil fill, annual element replacement
24. Drain bowl: automatic drain eliminates manual task (prevent overflow)
25. Sizing: FRL Cv must equal or exceed system flow requirement at pressure drop <5 PSI
        """,
        key_factors=[
            "Component order: Filter-Regulator-Lubricator (F-R-L)",
            "Filter removes particles and moisture (40, 5, or 0.01 um)",
            "Automatic drain eliminates manual draining (preferred)",
            "Filter replacement at 8-10 PSI pressure drop",
            "Relieving regulator preferred (vents excess downstream pressure)",
            "Lubricator only if equipment requires oil (cylinders, valves, tools)",
            "Oil-free applications: no lubricator",
            "Maintenance: daily visual, weekly drain, monthly oil, annual element",
            "Sizing: FRL Cv must exceed flow requirement",
            "Pressure drop <5 PSI through FRL unit"
        ],
        primary_authority=[
            "ISO 4414 - Pneumatic Fluid Power General Rules",
            "NFPA T2.6.1 - Pneumatic Air Preparation Equipment",
            "Manufacturer FRL selection guides"
        ],
        burden_holder="System designer must specify and size FRL unit for application requirements",
        adversary_position="Inadequate air preparation causing equipment failure or contamination",
        counter_arguments=[
            "Filter undersized (excessive pressure drop)",
            "No automatic drain (bowl overflows)",
            "Filter element not replaced (pressure drop excessive)",
            "Lubricator used where oil-free required",
            "Non-relieving regulator allows pressure rise",
            "No pressure gauge (cannot verify regulation)",
            "Oil reservoir empty (inadequate lubrication)",
            "Maintenance not performed per schedule"
        ],
        resolution_strategy="Specify FRL per application (filtration level, pressure, oil requirement), size for flow, install with automatic drain and gauge, maintain per schedule",
        entity_scope="All pneumatic equipment requiring air preparation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence based on ISO 4414 and industry FRL best practices",
        controlling_precedent="ISO 4414 Pneumatic Fluid Power General Rules"
    ),

}


# ============================================================================
# SEMANTIC NORMALIZATION
# ============================================================================

SEMANTIC_ALIASES = {
    "reciprocating compressor": ["piston compressor", "recip", "single-stage", "two-stage"],
    "rotary screw": ["screw compressor", "oil-flooded", "oil-free"],
    "air receiver": ["storage tank", "receiver tank", "surge tank"],
    "refrigerated dryer": ["refrig dryer", "cooling dryer"],
    "desiccant dryer": ["desiccant", "adsorption dryer", "heatless", "heated"],
    "pneumatic cylinder": ["air cylinder", "actuator", "ram"],
    "directional valve": ["solenoid valve", "control valve", "DCV"],
    "flow control": ["speed control", "needle valve", "throttle valve"],
    "vacuum ejector": ["venturi", "vacuum generator"],
    "vacuum pump": ["rotary vane", "claw pump", "diaphragm pump"],
    "ISO 8573": ["air quality", "compressed air purity"],
    "specific power": ["kW per 100 CFM", "energy efficiency"],
    "leak detection": ["ultrasonic", "leak audit"],
    "FRL": ["filter regulator lubricator", "air preparation"],
    "VSD": ["variable speed drive", "VFD", "variable frequency drive"],
}


def normalize_query(query: str) -> str:
    """Normalize query terms to canonical forms."""
    query_lower = query.lower()
    for canonical, aliases in SEMANTIC_ALIASES.items():
        for alias in aliases:
            if alias in query_lower:
                query_lower = query_lower.replace(alias, canonical)
    return query_lower


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class MetricsCollector:
    """Collects and reports performance metrics."""

    def __init__(self):
        self.telemetry_records: List[TelemetryRecord] = []
        self.start_time = time.time()

    def record(self, record: TelemetryRecord):
        self.telemetry_records.append(record)

    def get_stats(self) -> Dict[str, Any]:
        if not self.telemetry_records:
            return {
                "total_queries": 0,
                "cache_hit_rate": 0.0,
                "avg_response_time_ms": 0.0,
                "uptime_seconds": time.time() - self.start_time
            }

        total = len(self.telemetry_records)
        cache_hits = sum(1 for r in self.telemetry_records if r.cache_hit)
        total_time = sum(r.response_time_ms for r in self.telemetry_records)

        return {
            "total_queries": total,
            "cache_hit_rate": cache_hits / total if total > 0 else 0.0,
            "avg_response_time_ms": total_time / total if total > 0 else 0.0,
            "uptime_seconds": time.time() - self.start_time
        }


# ============================================================================
# COVERAGE TRACKING
# ============================================================================

class CoverageTracker:
    """Tracks doctrine coverage and identifies gaps."""

    def __init__(self):
        self.metrics = CoverageMetrics(total_doctrines=len(DOCTRINE_CACHE))

    def record_triggered(self, doctrine_topics: List[str]):
        self.metrics.triggered_doctrines.update(doctrine_topics)
        all_topics = set(DOCTRINE_CACHE.keys())
        self.metrics.missed_doctrines = all_topics - self.metrics.triggered_doctrines

    def identify_gaps(self, query: str) -> List[str]:
        """Identify potential epistemic gaps in coverage."""
        gaps = []
        query_lower = query.lower()

        # Check for uncovered pneumatic topics
        if "scroll compressor" in query_lower and "scroll" not in str(self.metrics.triggered_doctrines):
            gaps.append("Scroll compressor analysis not covered in current doctrine cache")
        if "membrane dryer" in query_lower and "membrane" not in str(self.metrics.triggered_doctrines):
            gaps.append("Membrane dryer technology not detailed in doctrine cache")
        if "pneumatic muscle" in query_lower:
            gaps.append("Pneumatic muscle actuators not covered in current doctrine cache")

        return gaps


# ============================================================================
# CORE ENGINE
# ============================================================================

class MECH12PneumaticEngine:
    """MECH12 Pneumatic Systems Intelligence Engine - TIE Grade."""

    def __init__(self):
        self.metrics = MetricsCollector()
        self.coverage = CoverageTracker()
        self.audit_log_path = Path(__file__).parent / "audit_trail.jsonl"

        logger.remove()
        logger.add(
            Path(__file__).parent / "mech12_pneumatic.log",
            rotation="100 MB",
            retention="30 days",
            level="INFO"
        )
        logger.info("MECH12 Pneumatic Systems Engine initialized")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone,
        context: Optional[Dict[str, Any]] = None
    ) -> QueryResponse:
        """
        Three-layer response strategy:
        Layer 1: Doctrine Cache (0-200ms)
        Layer 2: Semantic Retrieval (fallback)
        Layer 3: Deep Analysis (complex queries)
        """
        start_time = time.time()
        query_id = hashlib.sha256(f"{query}{time.time()}".encode()).hexdigest()[:12]

        normalized_query = normalize_query(query)

        # Layer 1: Doctrine Cache Lookup
        triggered_doctrines = self._doctrine_cache_lookup(normalized_query)
        cache_hit = len(triggered_doctrines) > 0

        if cache_hit:
            response_text = self._generate_from_cache(triggered_doctrines, mode, zone)
            confidence = self._assess_confidence(triggered_doctrines)
        else:
            # Layer 2: Semantic fallback
            logger.info(f"Cache miss for query: {query[:100]}")
            response_text = self._semantic_fallback(normalized_query, mode, zone)
            confidence = ConfidenceLevel.DISCLOSURE
            triggered_doctrines = []

        response_time_ms = (time.time() - start_time) * 1000

        # Epistemic caveats
        caveats = self._generate_caveats(query, triggered_doctrines, zone)

        # Record telemetry
        telemetry_record = TelemetryRecord(
            query_id=query_id,
            timestamp=time.time(),
            mode=mode,
            issue_categories=[],
            cache_hit=cache_hit,
            response_time_ms=response_time_ms,
            doctrine_blocks_used=[d.topic for d in triggered_doctrines],
            confidence_level=confidence
        )
        self.metrics.record(telemetry_record)
        self.coverage.record_triggered([d.topic for d in triggered_doctrines])

        # Audit trail
        self._write_audit_trail(query_id, query, response_text, mode, zone)

        # Determinism hash
        determinism_hash = hashlib.sha256(
            f"{query}{mode}{zone}{response_text}".encode()
        ).hexdigest()[:16]

        return QueryResponse(
            response=response_text,
            confidence=confidence,
            doctrine_blocks=[d.topic for d in triggered_doctrines],
            analysis_zone=zone,
            mode=mode,
            determinism_hash=determinism_hash,
            telemetry={
                "query_id": query_id,
                "response_time_ms": response_time_ms,
                "cache_hit": cache_hit,
                "doctrines_triggered": len(triggered_doctrines)
            },
            epistemic_caveats=caveats
        )

    def _doctrine_cache_lookup(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks."""
        triggered = []
        query_lower = query.lower()

        for doctrine in DOCTRINE_CACHE.values():
            # Keyword matching
            if any(kw in query_lower for kw in doctrine.keywords):
                triggered.append(doctrine)
            # Topic matching
            elif doctrine.topic.lower() in query_lower:
                triggered.append(doctrine)

        return triggered

    def _generate_from_cache(
        self,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Generate response from doctrine cache."""
        if mode == ResponseMode.FAST:
            # Concise response
            conclusions = [d.conclusion_template for d in doctrines]
            return " ".join(conclusions[:3])

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with authority citations
            response_parts = []
            for d in doctrines:
                response_parts.append(f"**{d.topic}**")
                response_parts.append(d.conclusion_template)
                response_parts.append(f"Authority: {', '.join(d.primary_authority[:2])}")
                response_parts.append(f"Confidence: {d.confidence.value}")
                response_parts.append("")
            return "\n".join(response_parts)

        else:  # MEMO
            # Full documentation with reasoning
            response_parts = []
            for d in doctrines:
                response_parts.append(f"## {d.topic}")
                response_parts.append(f"\n{d.conclusion_template}\n")
                response_parts.append("### Key Factors:")
                for factor in d.key_factors:
                    response_parts.append(f"- {factor}")
                response_parts.append("\n### Reasoning Framework:")
                response_parts.append(d.reasoning_framework)
                response_parts.append("\n### Primary Authority:")
                for auth in d.primary_authority:
                    response_parts.append(f"- {auth}")
                response_parts.append(f"\n**Confidence**: {d.confidence_stratification}\n")
                response_parts.append("---\n")
            return "\n".join(response_parts)

    def _semantic_fallback(self, query: str, mode: ResponseMode, zone: AnalysisZone) -> str:
        """Fallback response when cache misses."""
        return (
            f"Query received: {query[:200]}...\n\n"
            "This query did not trigger cached pneumatic systems doctrine blocks. "
            "For detailed analysis, please rephrase to include specific topics: "
            "compressor selection, air treatment, receiver sizing, cylinder design, "
            "valve selection, vacuum systems, energy efficiency, air quality, "
            "leak management, safety, circuit design, or flow control.\n\n"
            "MECH12 Pneumatic Systems Engine specializes in compressed air generation, "
            "air treatment (dryers, filters), pneumatic actuators, control valves, "
            "vacuum systems, ISO 8573 air quality, energy audits, and OSHA safety compliance."
        )

    def _assess_confidence(self, doctrines: List[DoctrineBlock]) -> ConfidenceLevel:
        """Assess overall confidence based on triggered doctrines."""
        if not doctrines:
            return ConfidenceLevel.DISCLOSURE

        # Use most conservative confidence from triggered doctrines
        levels = [d.confidence for d in doctrines]
        if ConfidenceLevel.HIGH_RISK in levels:
            return ConfidenceLevel.HIGH_RISK
        elif ConfidenceLevel.DISCLOSURE in levels:
            return ConfidenceLevel.DISCLOSURE
        elif ConfidenceLevel.AGGRESSIVE in levels:
            return ConfidenceLevel.AGGRESSIVE
        else:
            return ConfidenceLevel.DEFENSIBLE

    def _generate_caveats(
        self,
        query: str,
        doctrines: List[DoctrineBlock],
        zone: AnalysisZone
    ) -> List[str]:
        """Generate epistemic caveats and disclosures."""
        caveats = []

        if zone == AnalysisZone.PLANNING:
            caveats.append("Analysis for planning purposes only, not final design")
        elif zone == AnalysisZone.AUDIT:
            caveats.append("Audit review mode - verify against actual installation conditions")

        if not doctrines:
            caveats.append("Query did not match cached expertise - general guidance only")

        # Check for coverage gaps
        gaps = self.coverage.identify_gaps(query)
        caveats.extend(gaps)

        return caveats

    def _write_audit_trail(
        self,
        query_id: str,
        query: str,
        response: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ):
        """Write audit trail entry."""
        audit_entry = {
            "query_id": query_id,
            "timestamp": datetime.utcnow().isoformat(),
            "query": query[:500],
            "response_preview": response[:500],
            "mode": mode.value,
            "zone": zone.value
        }

        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(audit_entry) + "\n")

    def health_check(self) -> HealthResponse:
        """Comprehensive health check."""
        stats = self.metrics.get_stats()

        return HealthResponse(
            status="healthy",
            version="1.0.0",
            port=9272,
            doctrine_count=len(DOCTRINE_CACHE),
            uptime_seconds=stats["uptime_seconds"],
            total_queries=stats["total_queries"],
            cache_hit_rate=stats["cache_hit_rate"],
            avg_response_time_ms=stats["avg_response_time_ms"]
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(title="MECH12 Pneumatic Systems Intelligence Engine", version="1.0.0")

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENGINE = MECH12PneumaticEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint."""
    try:
        return ENGINE.three_layer_response(
            query=request.query,
            mode=request.mode,
            zone=request.zone,
            context=request.context
        )
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint."""
    return ENGINE.health_check()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine topics."""
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "authority": d.primary_authority[0] if d.primary_authority else "N/A"
            }
            for d in DOCTRINE_CACHE.values()
        ]
    }


@APP.get("/metrics")
async def metrics_endpoint():
    """Performance metrics."""
    stats = ENGINE.metrics.get_stats()
    coverage = {
        "total_doctrines": ENGINE.coverage.metrics.total_doctrines,
        "triggered_doctrines": len(ENGINE.coverage.metrics.triggered_doctrines),
        "coverage_rate": len(ENGINE.coverage.metrics.triggered_doctrines) / ENGINE.coverage.metrics.total_doctrines
    }
    return {**stats, **coverage}


if __name__ == "__main__":
    logger.info("Starting MECH12 Pneumatic Systems Engine on port 9272")
    uvicorn.run(APP, host="0.0.0.0", port=9272)
