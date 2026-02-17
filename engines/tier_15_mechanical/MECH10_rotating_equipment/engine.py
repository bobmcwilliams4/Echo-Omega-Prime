"""
MECH10 - Rotating Equipment Reliability Engine
TIE Gold Standard Implementation

Mechanical Engineering expertise for rotating machinery - motors, pumps, compressors,
turbines, gear drives, couplings, seals, alignment, condition monitoring.

Port: 9050
Version: 1.0.0
"""

import sys
from pathlib import Path

# CRITICAL: Add parent to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "mech10_rotating_equipment.log",
    rotation="100 MB",
    retention="30 days",
    level="DEBUG"
)


# ============================================================================
# ENUMS & MODELS
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
    MOTOR_SELECTION = "MOTOR_SELECTION"
    VFD_APPLICATION = "VFD_APPLICATION"
    GEAR_DRIVES = "GEAR_DRIVES"
    COUPLING_SELECTION = "COUPLING_SELECTION"
    SHAFT_ALIGNMENT = "SHAFT_ALIGNMENT"
    MECHANICAL_SEALS = "MECHANICAL_SEALS"
    SHAFT_DESIGN = "SHAFT_DESIGN"
    VIBRATION_ANALYSIS = "VIBRATION_ANALYSIS"
    API_STANDARDS = "API_STANDARDS"
    CONDITION_MONITORING = "CONDITION_MONITORING"
    FAILURE_ANALYSIS = "FAILURE_ANALYSIS"
    SPARE_PARTS = "SPARE_PARTS"


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=10, description="Rotating equipment question")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    categories: List[IssueCategory]
    authorities: List[str]
    reasoning_chain: List[str]
    mode: ResponseMode
    determinism_hash: str
    query_time_ms: float


class HealthResponse(BaseModel):
    status: str
    engine: str
    version: str
    port: int
    doctrine_count: int
    uptime_seconds: float


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
    entity_scope: str
    confidence: ConfidenceLevel
    controlling_precedent: Optional[str] = None


# ============================================================================
# DOCTRINE CACHE - 25+ ROTATING EQUIPMENT EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="electric_motor_nema_frame_sizing",
        keywords=["NEMA frame", "motor frame size", "shaft height", "foot mounting", "T-frame", "U-frame"],
        conclusion_template=[
            "NEMA frame size determines mounting dimensions and shaft dimensions standardized across manufacturers.",
            "Two-digit frames (48, 56) specify shaft height centerline in 1/16 inch increments.",
            "Three-digit frames (140T-580) use first two digits for D-dimension (distance bolt holes) in quarter-inches."
        ],
        reasoning_framework="""NEMA MG 1 establishes standardized frame dimensions ensuring interchangeability.
        Frame 56 = 3.5 inch shaft height (56/16). Frame 143T = 14/4 = 3.5 inch D-dimension, T suffix indicates standard shaft diameter/length.
        C-face motors have pilot/bolt circle for direct flange mounting to gearboxes/pumps.
        Older U-frame motors (1952-1964) are non-interchangeable with modern T-frames despite similar numbers.
        Oversized frames allow better cooling, lower temperature rise, longer insulation life.""",
        key_factors=[
            "Shaft height centerline must match driven equipment or base plate design",
            "T-frame standardization vs legacy U-frame compatibility issues",
            "C-face vs foot-mounted applications",
            "Horsepower and speed determine minimum frame size",
            "Thermal capacity increases with larger frames at same HP"
        ],
        primary_authority=[
            "NEMA MG 1-2021 Motors and Generators",
            "IEC 60072 Dimensions and output series for rotating electrical machines",
            "IEEE 841-2009 Standard for Petroleum and Chemical Industry - Severe Duty Totally Enclosed Motors"
        ],
        burden_holder="equipment_specifier",
        adversary_position="Any frame that meets horsepower rating is acceptable",
        counter_arguments=[
            "Larger frames improve reliability through lower temperature rise",
            "Base plate modifications expensive if wrong frame specified",
            "Shaft height mismatch causes misalignment and coupling issues",
            "C-face dimensions critical for direct-coupled applications",
            "Inventory standardization reduces spare parts complexity"
        ],
        resolution_strategy="Specify exact NEMA frame per mounting constraints, verify T-frame vs U-frame for replacements, consider next larger frame for severe duty",
        entity_scope="industrial_facilities",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="motor_efficiency_classes_ie_standards",
        keywords=["motor efficiency", "IE1", "IE2", "IE3", "IE4", "premium efficiency", "NEMA Premium"],
        conclusion_template=[
            "International efficiency classes (IE1-IE5) define minimum motor efficiency per IEC 60034-30-1.",
            "IE3 (Premium Efficiency) is mandatory in US/EU for most applications, IE4 (Super Premium) emerging.",
            "Higher efficiency motors reduce energy cost but have higher purchase price and efficiency penalties at partial load."
        ],
        reasoning_framework="""Motor efficiency directly impacts operating cost over 15-20 year life.
        IE1 (Standard) ~88%, IE2 (High) ~91%, IE3 (Premium) ~93.6%, IE4 (Super Premium) ~95% at 50 HP.
        Energy cost typically 10-20x motor purchase price over lifetime.
        NEMA Premium = IE3 equivalent. DOE 2016 rule mandates IE3 for most motors 1-500 HP.
        VFD operation reduces efficiency ~2-5% due to harmonic losses.
        Efficiency peaks at 75-100% load, drops significantly below 50% load.""",
        key_factors=[
            "Life cycle cost analysis: purchase + energy over 20 years",
            "Load profile - constant vs variable, full vs partial load",
            "VFD application reduces effective efficiency",
            "Payback period typically 1-3 years for IE3 vs IE1",
            "Utility rebates available for premium efficiency motors"
        ],
        primary_authority=[
            "IEC 60034-30-1 Efficiency classes of line-operated AC motors",
            "NEMA MG 1 Table 12-12 Nominal Full-Load Efficiencies",
            "DOE 10 CFR 431 Energy Conservation Standards for Electric Motors",
            "IEEE 112 Standard Test Procedure for Polyphase Induction Motors"
        ],
        burden_holder="facility_owner",
        adversary_position="Standard efficiency acceptable if purchase price critical",
        counter_arguments=[
            "Energy cost dominates total cost of ownership",
            "IE3 motors generate less waste heat, reduce HVAC load",
            "Premium efficiency mandatory for most new installations",
            "Rebates and incentives offset higher purchase cost",
            "Improved power factor reduces demand charges"
        ],
        resolution_strategy="Default to IE3 minimum, IE4 for continuous high-load operation, perform LCC analysis for motors >25 HP",
        entity_scope="industrial_commercial",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="motor_service_factor_thermal_margin",
        keywords=["service factor", "SF", "1.15 service factor", "thermal margin", "overload capacity"],
        conclusion_template=[
            "Service factor is multiplier indicating motor can operate continuously above nameplate HP without damage.",
            "1.15 SF means motor can run at 115% nameplate HP at rated voltage/frequency with reduced life expectancy.",
            "Service factor operation increases temperature rise, reduces insulation life per Arrhenius equation."
        ],
        reasoning_framework="""Service factor provides thermal margin for adverse conditions (high ambient, poor ventilation, voltage imbalance).
        NEMA Design B motors typically 1.15 SF, European IEC motors typically 1.0 SF.
        Operating at SF reduces motor life - every 10°C rise halves insulation life.
        SF should not be used for normal continuous operation, only temporary overload.
        VFD operation typically voids service factor above base speed.
        Premium efficiency motors may have lower SF (1.0) due to optimized thermal design.""",
        key_factors=[
            "Service factor is safety margin, not continuous operating range",
            "Insulation life degradation accelerates exponentially with temperature",
            "Altitude, ambient temperature, ventilation affect effective SF",
            "VFD operation typically requires derating or voids SF",
            "1.0 SF motors require more accurate load calculation"
        ],
        primary_authority=[
            "NEMA MG 1 Part 12 Service Factors",
            "IEEE 841 Section 5.2 Service Factor Requirements",
            "ANSI/NEMA MG 1 Part 30 Application Considerations"
        ],
        burden_holder="application_engineer",
        adversary_position="Service factor provides free extra capacity",
        counter_arguments=[
            "SF operation reduces motor life, increases failure risk",
            "High ambient or altitude already consume SF margin",
            "Should size motor for actual load, not rely on SF",
            "Warranty may be void if operated continuously at SF",
            "Better to specify next frame size for sustained overload"
        ],
        resolution_strategy="Size motor for maximum continuous load without using SF, reserve SF for abnormal conditions or derating factors",
        entity_scope="industrial_applications",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="vfd_harmonics_mitigation",
        keywords=["VFD harmonics", "PWM", "drive harmonics", "THD", "5th harmonic", "7th harmonic", "line reactor", "isolation transformer"],
        conclusion_template=[
            "6-pulse VFDs generate characteristic harmonics (5th, 7th, 11th, 13th) causing voltage distortion and motor heating.",
            "IEEE 519 limits total harmonic distortion (THD) to 5% voltage, 15-20% current depending on system.",
            "Mitigation: line/load reactors (3-5% impedance), isolation transformers, active harmonic filters, or 18-pulse drives."
        ],
        reasoning_framework="""PWM switching creates non-sinusoidal current waveform with harmonic content.
        6-pulse VFD: 5th harmonic (-20%), 7th (+14%), 11th (-9%), 13th (+7%) relative to fundamental.
        Harmonics cause: motor heating (2-5°C rise), nuisance breaker trips, capacitor bank failures, transformer overheating.
        Line reactor (3%) reduces input current THD from ~35% to ~25%, load reactor protects motor insulation.
        18-pulse drive eliminates 5th/7th harmonics, reduces THD to ~10%.
        Active harmonic filter can achieve <5% THD across wide load range.""",
        key_factors=[
            "System short circuit ratio determines harmonic distortion impact",
            "Notching on voltage waveform vs current harmonics",
            "Motor derating required if THD >5% - typically 1.5% per 1% THD",
            "Reflected wave phenomenon for long motor cables (>50ft) requires load reactor/dV/dt filter",
            "Multiple VFDs create harmonic cancellation or amplification"
        ],
        primary_authority=[
            "IEEE 519-2014 Harmonic Control in Electrical Power Systems",
            "IEC 61800-3 Adjustable Speed Drives - EMC Requirements",
            "NEMA MG 1 Part 31 Definite Purpose Inverter-Fed Motors",
            "IEEE 1159 Recommended Practice for Monitoring Electric Power Quality"
        ],
        burden_holder="electrical_designer",
        adversary_position="VFD built-in features adequate for harmonic control",
        counter_arguments=[
            "IEEE 519 compliance often requires external mitigation",
            "Motor bearing currents from common mode voltage cause premature failure",
            "Transformer K-factor rating needed for harmonic heating",
            "3% line reactor increases DC bus ripple, may reduce drive rating",
            "Cable length >50ft creates voltage reflection, insulation stress"
        ],
        resolution_strategy="3-5% line reactor for most applications, 18-pulse or active filter for sensitive systems, load reactor if cable >50ft or common mode current issue",
        entity_scope="vfd_installations",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="gear_drive_types_selection",
        keywords=["parallel shaft gearbox", "right angle gearbox", "worm gear", "bevel gear", "planetary gear", "epicyclic"],
        conclusion_template=[
            "Parallel shaft (helical) gears offer highest efficiency (96-98%) for speed reduction <6:1, compact inline design.",
            "Right angle (bevel/spiral bevel) gears change shaft orientation 90°, efficiency 94-96%, ratios to 5:1 per stage.",
            "Planetary/epicyclic gears provide high ratios (5:1 to 100:1) in compact envelope, coaxial shafts, efficiency 94-97%."
        ],
        reasoning_framework="""Gear type selection driven by: ratio, efficiency, orientation, footprint, cost.
        Helical parallel shaft: smooth/quiet, high capacity, requires thrust bearings for helix angle.
        Worm gears: high ratio (10:1 to 60:1) single stage, self-locking possible, low efficiency (50-90%), high sliding wear.
        Bevel gears: intersecting shafts, limited to lower ratios/speeds vs helical.
        Planetary: sun-planet-ring arrangement, load shared across multiple planets (3-6), very compact.
        Double reduction helical: two stages achieve ratio to 40:1, larger footprint.""",
        key_factors=[
            "Service factor: AGMA 2001/6010 sizing for shock loads, duty cycle",
            "Lubrication method: splash (to 5000 fpm PV) vs forced (higher speeds/loads)",
            "Backlash requirements for positioning applications",
            "Noise limits favor helical over spur, planetary over parallel shaft",
            "Overhung load capacity on input/output shafts"
        ],
        primary_authority=[
            "AGMA 2001-D04 Fundamental Rating Factors for Involute Spur and Helical Gear Teeth",
            "AGMA 6010-F97 Standard for Spur, Helical, Herringbone and Bevel Enclosed Drives",
            "API 613 5th Edition Special Purpose Gear Units",
            "API 677 General Purpose Gear Units",
            "ISO 6336 Calculation of Load Capacity of Spur and Helical Gears"
        ],
        burden_holder="mechanical_designer",
        adversary_position="Lowest cost gearbox meeting ratio requirement acceptable",
        counter_arguments=[
            "Efficiency loss compounds over 20+ year life, energy cost significant",
            "AGMA service factor critical for reliability - 1.5 minimum for industrial",
            "Thermal rating limits continuous power, must verify oil temperature rise",
            "Bearing life calculation per ISO 281 ensures 100,000 hour L10 life",
            "Seal type affects maintenance - contact vs non-contact, shaft speed limits"
        ],
        resolution_strategy="Helical parallel shaft for efficiency-critical <6:1, planetary for compactness/high ratio, right angle only if space dictates, avoid worm except low speed/high ratio",
        entity_scope="power_transmission",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="coupling_selection_flexible_vs_rigid",
        keywords=["flexible coupling", "rigid coupling", "disc coupling", "gear coupling", "elastomeric coupling", "misalignment compensation"],
        conclusion_template=[
            "Flexible couplings accommodate misalignment (angular, parallel, axial) and dampen torsional vibration.",
            "Disc couplings (metallic) handle highest misalignment with no backlash, no lubrication, 0.5° angular/0.03in parallel typical.",
            "Gear couplings transmit highest torque, require lubrication, allow 1° angular/0.05in parallel, introduce backlash."
        ],
        reasoning_framework="""Coupling selection balances: torque capacity, misalignment tolerance, torsional stiffness, maintenance.
        Rigid couplings (compression, flanged) require precision alignment (<0.002in TIR), used only for very stiff systems.
        Elastomeric (jaw, tire, donut): absorb shock, electrically insulating, limited temperature (200-250°F), wear element.
        Disc coupling: all-metal (stainless), no maintenance, fail-safe (gradual), high temperature, high speed.
        Diaphragm coupling: similar to disc, more flexible, lower axial stiffness, used in turbomachinery.
        Grid coupling: high torque density, damping, needs lubrication, backlash present.""",
        key_factors=[
            "Service factor per AGMA 9001 or coupling manufacturer - 1.5 to 3.0 based on shock load",
            "Torsional natural frequency - avoid resonance with running speed or 2x/3x",
            "Misalignment limits - installation vs thermal growth vs foundation settlement",
            "Lubrication maintenance access and interval",
            "Fail-safe behavior - gradual degradation vs catastrophic"
        ],
        primary_authority=[
            "API 671 Special Purpose Couplings for Petroleum, Chemical and Gas Industry Services",
            "AGMA 9001-B97 Flexible Couplings - Lubricated and Non-Lubricated Types",
            "ISO 14691 Couplings - Lubricated flexible couplings",
            "API 610 Annex I Couplings and Guards for Centrifugal Pumps"
        ],
        burden_holder="mechanical_designer",
        adversary_position="Lowest cost coupling meeting torque rating adequate",
        counter_arguments=[
            "Undersized coupling causes premature failure, shaft damage, downtime cost >>coupling cost",
            "Misalignment tolerance essential for field installation reality vs perfect CAD model",
            "Torsional analysis required for variable speed, reciprocating loads",
            "Balance quality per ISO 1940 critical for high speed (>3600 RPM)",
            "Spacer vs close-coupled affects pump removal without disturbing driver"
        ],
        resolution_strategy="Disc coupling for high reliability/low maintenance, gear coupling for extreme torque, elastomeric for small HP/misalignment, rigid coupling only for calibrated precision systems",
        entity_scope="rotating_equipment",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="shaft_alignment_methods_precision",
        keywords=["shaft alignment", "dial indicator", "reverse dial", "laser alignment", "rim and face", "soft foot"],
        conclusion_template=[
            "Reverse dial indicator method measures coupling sag compensation, achieves ±0.001in if executed properly.",
            "Laser alignment systems provide real-time alignment values, tolerance bands per machine type, faster than dial indicators.",
            "Acceptable misalignment: API 610 pumps ±0.002in offset/0.0005in/in angularity, general industrial ±0.005in."
        ],
        reasoning_framework="""Misalignment causes: premature bearing failure (50% of bearing failures), coupling wear, seal leakage, shaft fatigue, vibration.
        Reverse dial indicator: mount indicators on coupling hubs, rotate 360°, record TIR (total indicated runout), calculate shim changes.
        Laser alignment: transmitter-receiver units measure angularity/offset in two planes, software calculates shim corrections, accounts for thermal growth.
        Soft foot check critical - unequal bolt torque distorts machine frame, introduces misalignment. Must correct before alignment.
        Thermal growth: drivers typically grow upward (motor) or toward coupling (turbine), must pre-offset cold alignment.
        Pipe strain: check coupling opening/closing with piping connected vs disconnected, indicates unacceptable pipe load.""",
        key_factors=[
            "Foundation/grout integrity - voids under feet invalidate alignment",
            "Thermal growth compensation - cold offset to achieve hot alignment",
            "Piping strain - API 686 limits force/moment on pump nozzles",
            "Coupling type affects allowable misalignment",
            "Documentation - record as-found, as-left alignment for trend analysis"
        ],
        primary_authority=[
            "API 686 Machinery Installation and Installation Design",
            "ISO 10816 Mechanical Vibration - Evaluation of Machine Vibration",
            "API 610 Centrifugal Pumps Section 6.8 Alignment",
            "ANSI/HI 9.6.4 Centrifugal and Vertical Pumps for Allowable Nozzle Loads"
        ],
        burden_holder="millwright_contractor",
        adversary_position="Visual alignment or straight edge adequate for industrial equipment",
        counter_arguments=[
            "Precision alignment extends bearing life 3-5x, eliminates 50% of vibration issues",
            "Laser systems pay for themselves in labor savings after 10-20 alignments",
            "API equipment contractually requires documented precision alignment",
            "Thermal growth if ignored causes hot misalignment worse than cold",
            "Soft foot >0.002in distorts casing, binding/clearance issues"
        ],
        resolution_strategy="Laser alignment for all critical equipment (API pumps/compressors), reverse dial for general purpose, verify soft foot <0.002in, account for thermal growth per OEM",
        entity_scope="machinery_installation",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="mechanical_seal_api_682_plans",
        keywords=["mechanical seal", "API 682", "Plan 11", "Plan 23", "Plan 32", "Plan 52", "Plan 53", "flush plan", "dual seal"],
        conclusion_template=[
            "API 682 defines piping plans providing cooling/lubrication/pressure control for mechanical seals.",
            "Plan 11 (internal recirculation) simplest for clean liquids <300°F, no external system required.",
            "Plan 53A/B/C dual pressurized seal with barrier fluid protects against process leakage for hazardous/flammable fluids."
        ],
        reasoning_framework="""Mechanical seal selection driven by: fluid compatibility, temperature, pressure, toxicity, abrasiveness.
        Single seals: one seal face, process fluid lubricates, leakage to atmosphere if failed.
        Dual seals: two faces in series, barrier/buffer fluid between, inner seal contains process, outer seal backup.
        Plan 11: simplest, internal circulation from pump discharge through seal chamber, clean liquids only.
        Plan 23: external reservoir above seal for thermal siphon cooling, dirty liquids, solids settlement.
        Plan 32: external flush from clean source, dilute/cool process fluid, used for slurries/crystallizing fluids.
        Plan 52: pressurized barrier fluid for dual seals, bladder accumulator maintains pressure >process.
        Plan 53A: unpressurized reservoir, 53B: floating reservoir, 53C: pressurized reservoir - all for dual seals.""",
        key_factors=[
            "Emission regulations (EPA LDAR, VOC limits) often mandate dual seals",
            "Seal face material compatibility: SiC vs tungsten carbide vs carbon graphite",
            "Temperature limits: elastomers (300-400°F), PTFE (450°F), metal bellows (600°F+)",
            "PV limit (pressure × velocity) per seal design, typically 300,000-500,000",
            "Flush rate calculation: 1-2 GPM per inch diameter minimum for cooling"
        ],
        primary_authority=[
            "API 682 4th Edition Pumps - Shaft Sealing Systems for Centrifugal and Rotary Pumps",
            "API 610 12th Edition Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries",
            "ISO 21049 Pumps - Shaft Sealing Systems for Centrifugal and Rotary Pumps",
            "ASME B73.1 Specification for Horizontal End Suction Centrifugal Pumps"
        ],
        burden_holder="process_engineer",
        adversary_position="Standard packing adequate for most services, seals too complex",
        counter_arguments=[
            "Mechanical seals eliminate packing leakage (1-60 drops/min per ring), reduce emissions",
            "Seal life 3-5 years vs packing adjustment every 3-6 months",
            "Dual seals required for toxic/flammable per OSHA/EPA regulations",
            "Incorrect plan causes seal failure - Plan 32 for slurry NOT Plan 11",
            "Barrier fluid selection critical - compatible with process if inner seal leaks"
        ],
        resolution_strategy="Plan 11 for clean <300°F, Plan 23 for dirty/hot, Plan 32 for slurries, Plan 52/53 dual seal for hazardous/toxic, consult API 682 compatibility matrix",
        entity_scope="centrifugal_pumps",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="packing_vs_mechanical_seal_selection",
        keywords=["packing", "mechanical seal", "compression packing", "braided packing", "PTFE packing", "graphite packing"],
        conclusion_template=[
            "Compression packing allows controlled leakage (5-60 drops/min), requires periodic adjustment, lower cost than seals.",
            "Mechanical seals provide near-zero leakage, require no adjustment, mandatory for toxic/VOC services.",
            "Packing suitable for: abrasive slurries, <300°F, non-hazardous, outdoor/accessible applications."
        ],
        reasoning_framework="""Packing vs seal decision driven by: leakage tolerance, emissions, maintenance access, cost, fluid properties.
        Packing: braided rings (graphite/PTFE/aramid) compressed in stuffing box, require leakage for cooling.
        Zero leakage packing sets exist (die-formed) but require perfect installation, limited life.
        Mechanical seals: rotating/stationary face (SiC/carbon) with elastomer secondary seal, springs maintain contact pressure.
        Packing advantages: lower cost, abrasive tolerance, simple replacement, no auxiliary systems.
        Seal advantages: no leakage (environmental), no adjustment, longer life, higher pressure/speed capability.
        Emissions regulations (EPA NSPS, LDAR) often prohibit packing for VOC services.""",
        key_factors=[
            "Leakage rate: packing 5-60 drops/min, seals <1 drop/hour or zero visible",
            "Shaft/sleeve wear: packing causes wear groove, seals minimal if aligned properly",
            "Power consumption: packing friction 1-5 HP loss, seals negligible",
            "Temperature: graphite packing to 650°F, PTFE to 500°F, seal elastomers limit ~400°F",
            "Solids content: >5% solids favors packing, Plan 32 flush can enable seals"
        ],
        primary_authority=[
            "EPA 40 CFR Part 60 Subpart VV Standards of Performance for Equipment Leaks of VOC",
            "API 682 Section 2.2.1 Seal Selection Criteria",
            "FSA (Fluid Sealing Association) Packing Technical Manual",
            "ASME PCC-1 Guidelines for Pressure Boundary Bolted Flange Joint Assembly"
        ],
        burden_holder="reliability_engineer",
        adversary_position="Packing cheaper initial cost, easier to maintain in field",
        counter_arguments=[
            "Seal total cost of ownership lower: no adjustment labor, no leakage cleanup, longer life",
            "Environmental/safety regulations mandate seals for many services",
            "Shaft wear from packing requires machining/sleeve replacement, costly downtime",
            "Water services: seal eliminates bearing contamination from packing leakage",
            "High speed (>3000 FPM): packing excessive heat generation, seal required"
        ],
        resolution_strategy="Mechanical seal default for toxic/VOC/high speed, packing acceptable for abrasive slurries/low value fluids/outdoor non-critical, verify regulatory compliance",
        entity_scope="pump_sealing",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="shaft_design_keyway_stress_analysis",
        keywords=["shaft design", "keyway", "stress concentration", "torsional stress", "bending stress", "fatigue", "Kt factor"],
        conclusion_template=[
            "Keyways introduce stress concentration factor Kt=2.0-3.0, reducing shaft fatigue strength 50%.",
            "Combined torsion and bending requires von Mises or Tresca equivalent stress calculation per ANSI B106.1M.",
            "Shaft diameter calculation:Account for stress concentration, fatigue endurance limit, surface finish, size effect."
        ],
        reasoning_framework="""Shaft failure modes: torsional yielding (ductile), fatigue (cyclic bending), brittle fracture (impact/stress concentration).
        Torsional shear stress τ = 16T/(πd³), bending stress σ = 32M/(πd³), maximum occurs at keyway/shoulder/hole.
        Stress concentration: keyway Kt ~2.5, shoulder fillet Kt=1.5-2.5 (depends on r/d ratio), press fit Kt=2-3.
        Fatigue analysis: Goodman/Soderberg/Gerber diagram, modified endurance limit Se' = ka·kb·kc·kd·Se.
        Surface factor ka (machined ~0.8, ground ~0.9), size factor kb (d>2in penalized), reliability factor kc.
        Keyway depth per ANSI B17.1: square key width = d/4, depth = width/2, weakens shaft significantly.""",
        key_factors=[
            "Material selection: 4140/4340 alloy steel for high stress, 1045 for moderate, 304SS for corrosion",
            "Surface finish: turned 125 RMS vs ground 32 RMS affects fatigue limit 15-20%",
            "Fillet radius: r/d ratio >0.1 reduces Kt from 2.5 to 1.5",
            "Press fit interference: 0.001in/in diametral creates high hoop stress, Kt=2-3",
            "Axial loads: thrust bearings, belt/gear loads create combined stress"
        ],
        primary_authority=[
            "ANSI B106.1M-1985 Design of Transmission Shafting",
            "ANSI/AGMA 6001-E08 Design and Selection of Components for Enclosed Gear Drives",
            "ASME BTH-1 Design of Below-the-Hook Lifting Devices Shafting Section",
            "Shigley's Mechanical Engineering Design (textbook standard reference)"
        ],
        burden_holder="mechanical_designer",
        adversary_position="Rule of thumb sizing (d³=16T/τ) adequate without detailed analysis",
        counter_arguments=[
            "Fatigue failures occur at stress concentrations ignored by simple formulas",
            "Keyway stress concentration reduces strength 50%, must be accounted for",
            "Spline or interference fit eliminates keyway, increases fatigue life",
            "Shot peening or cold rolling increases surface compressive stress, improves fatigue 20-40%",
            "FEA analysis required for complex loading, non-circular sections"
        ],
        resolution_strategy="Calculate combined stress with stress concentration factors, verify fatigue safety factor >1.5, eliminate keyways where possible (spline/interference), fillet all shoulders r/d>0.1",
        entity_scope="shaft_design",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="torsional_critical_speed_analysis",
        keywords=["torsional vibration", "torsional critical", "resonance", "Campbell diagram", "excitation frequency", "damping"],
        conclusion_template=[
            "Torsional natural frequencies occur where system torsional stiffness resonates with inertia distribution.",
            "Excitation from: gear mesh frequency, motor slip frequency, VFD switching, reciprocating loads.",
            "Avoid running speeds within ±20% of torsional critical, verify stress amplification factor <2.0."
        ],
        reasoning_framework="""Torsional system: series springs (shafts, couplings) and masses (rotors, gears, flywheels).
        Natural frequency fn = (1/2π)√(K/I) where K=torsional stiffness, I=moment of inertia.
        Multi-mass system: multiple modes, lowest mode typically critical (all masses in phase).
        Excitation sources: 2-pole motor 2× slip frequency (~3-5 Hz), gear mesh Ngears × RPM/60, VFD switching 2× line frequency.
        Resonance amplification: stress σ = σstatic × Q where Q=1/(2ζ), damping ζ typically 0.01-0.05 for steel shafts.
        Campbell diagram: plot natural frequencies vs excitation orders, identify interference.
        Shaft failure at keyway or coupling hub if torsional stress exceeds fatigue limit.""",
        key_factors=[
            "Long slender shafts between large inertias most susceptible",
            "VFD startup sweep through critical - limit accel/decel rate",
            "Gear drives introduce mesh frequency excitation N × RPM",
            "Reciprocating compressors: firing frequency 2× for single acting, 4× for double",
            "Damping very low for all-metal systems, viscous coupling/elastomer adds damping"
        ],
        primary_authority=[
            "API 684 Tutorial on the API Standard Paragraphs Covering Rotor Dynamics and Balancing",
            "API 617 Axial and Centrifugal Compressors Section 6.9 Torsional Analysis",
            "API 612 Special Purpose Steam Turbines Section 5.9",
            "AGMA 6011-I03 Specification for High Speed Helical Gear Units Torsional Vibrations"
        ],
        burden_holder="dynamics_engineer",
        adversary_position="Torsional analysis only needed for high-speed turbomachinery",
        counter_arguments=[
            "VFD drives make torsional issues common even on moderate speed equipment",
            "Gearbox failures often torsional fatigue from resonant operation",
            "Long shafts (>20:1 L/D) susceptible even at low speed",
            "Startup transient through critical can cause failure even if operating speed safe",
            "Coupling manufacturer requires torsional analysis for warranty"
        ],
        resolution_strategy="Torsional analysis mandatory for: VFD >100 HP, geared systems, L/D >15, API equipment. Use vendor software or FEA, verify margin to excitation >20%",
        entity_scope="rotating_machinery",
        confidence=ConfidenceLevel.AGGRESSIVE
    ),

    DoctrineBlock(
        topic="lateral_critical_speed_bearing_stiffness",
        keywords=["lateral critical speed", "rotor dynamics", "bearing stiffness", "first critical", "Campbell diagram", "unbalance response"],
        conclusion_template=[
            "Lateral critical speed is shaft bending natural frequency, depends on rotor mass distribution and bearing stiffness.",
            "First critical typically occurs 0.7-0.9× operating speed for rigid-bearing systems, must separate >20% from running speed.",
            "API 610/617 require lateral analysis, separation margin ±15% for pumps, ±20% for compressors."
        ],
        reasoning_framework="""Lateral vibration: shaft bends in transverse direction, supported by bearings.
        Critical speed fc = (λ/2π)√(EI/mL³) where EI=bending stiffness, m=mass/length, L=span, λ=mode constant.
        Bearing stiffness modifies equation - rigid bearings increase fc, soft bearings decrease fc.
        Flexible rotor: operates above first critical, requires careful unbalance control, bearing damping critical.
        Rigid rotor: operates below first critical, simpler but speed limited.
        Unbalance excitation at 1× running speed - if coincides with critical, amplification factor Q=1/(2ζ) produces high vibration.
        API separates criticality: 20% for flexible rotors, 15% for rigid, to avoid resonant operation.""",
        key_factors=[
            "Bearing type: ball bearing K=1-5×10⁶ lb/in, sleeve bearing K=5-50×10⁵ lb/in (depends on speed)",
            "Overhung rotors (pumps): first mode lower than between-bearing designs",
            "Disk inertia polar moment affects critical via gyroscopic effects",
            "Foundation stiffness: soft foundation lowers critical by 5-15%",
            "Balance quality per ISO 1940 G2.5 standard for rigid, G1.0 for flexible"
        ],
        primary_authority=[
            "API 610 12th Edition Section 6.9 Rotor Dynamics",
            "API 684 Rotor Dynamics and Balancing Tutorial",
            "ISO 1940-1 Balance Quality Requirements for Rotors",
            "ISO 21940-11 Rotodynamic Balance - Procedures and Tolerances"
        ],
        burden_holder="OEM_manufacturer",
        adversary_position="Design well below critical speed, analysis unnecessary",
        counter_arguments=[
            "High speed equipment often flexible rotor, must operate above first critical",
            "VFD allows variable speed - must verify no critical in operating range",
            "Foundation or piping changes alter bearing stiffness, shift critical",
            "Unbalance from fouling, erosion, or mechanical damage excites critical",
            "Startup transient passes through critical - must control acceleration"
        ],
        resolution_strategy="Lateral analysis for all speeds >3600 RPM, API equipment, or VFD variable speed. Verify 15-20% margin, specify balance grade, damped bearings if operating near critical",
        entity_scope="high_speed_machinery",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="api_610_centrifugal_pump_standard",
        keywords=["API 610", "centrifugal pump", "BB1", "BB2", "OH2", "VS1", "radial split", "axial split", "minimum flow"],
        conclusion_template=[
            "API 610 12th edition defines design/materials/testing for petroleum/chemical centrifugal pumps.",
            "Pump types: OH (overhung), BB (between bearings), VS (vertical), each with subtypes for mounting/splitting.",
            "Key requirements: casing pressure test 1.5× design, hydrostatic test 1.5×, mechanical run test, NPSH margin, spares."
        ],
        reasoning_framework="""API 610 ensures reliability for critical/hazardous services: refining, petrochemical, LNG.
        OH2 (overhung, centerline mounted) most common for moderate head/flow, single stage, easy maintenance.
        BB2 (axial split, radially supported): high pressure/temperature, multi-stage, heavier duty than OH.
        Minimum continuous flow required to prevent recirculation/cavitation damage - typically 40-60% BEP.
        NPSH margin: 1.0 m (3 ft) above NPSH3% or 1.15× NPSHR, prevents cavitation erosion.
        Casing design pressure: 25 psi above maximum expected, or 1.25× design pressure, whichever greater.
        Mechanical seal per API 682, alignment per API 686.""",
        key_factors=[
            "Reliability critical - shutdowns cost $100K-1M+/day for refinery",
            "Materials: 316SS minimum for wetted parts, duplex/super duplex for corrosive/chlorides",
            "Baseplate design: fabricated steel with grouting pocket, precision machined faces",
            "Auxiliary systems: seal flush, cooling water, warmup/venting connections",
            "Vibration limits per API 610 Table 13: unfiltered 0.12 in/s for <3600 RPM"
        ],
        primary_authority=[
            "API 610 12th Edition Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries",
            "API 682 4th Edition Shaft Sealing Systems",
            "API 686 2nd Edition Machinery Installation and Installation Design",
            "ISO 13709 Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (ISO version of API 610)"
        ],
        burden_holder="EPC_contractor",
        adversary_position="ANSI/ASME B73.1 chemical pumps adequate, API 610 over-specified",
        counter_arguments=[
            "API 610 uptime/reliability vastly superior - 3-5 year MTBR vs 1-2 year ANSI",
            "Lifecycle cost favors API 610: fewer failures, less maintenance, interchangeable spares",
            "Hazardous services require rugged design, testing, documentation per API",
            "Seal chamber design per API 682 prevents premature seal failures",
            "Vendor performance test witnesses verify contractual compliance"
        ],
        resolution_strategy="API 610 for critical/hazardous services, high temperature/pressure, continuous operation >90% runtime. ANSI pumps acceptable for non-critical, clean water, intermittent duty",
        entity_scope="process_plants",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="api_617_centrifugal_compressor_standard",
        keywords=["API 617", "centrifugal compressor", "axial compressor", "magnetic bearings", "dry gas seal", "surge control"],
        conclusion_template=[
            "API 617 8th edition covers axial/centrifugal compressors for petroleum/chemical gas services.",
            "Key requirements: rotordynamic analysis (lateral/torsional), dry gas seals, surge control system, performance test.",
            "Separation margins: 15% from lateral critical, 10% from torsional critical, 10% from surge line."
        ],
        reasoning_framework="""Centrifugal compressors: critical for gas processing, refrigeration, air separation, hydrogen.
        Impeller types: open (low head), closed (high head), 3D (complex geometry), inducer (anti-surge).
        Bearing types: tilting pad (high stability, temperature tolerance), magnetic (no oil, high speed, expensive).
        Dry gas seals: non-contacting, pressurized gas film, <1 scfh leakage, 95%+ reliability.
        Surge: flow reversal when pressure rise exceeds impeller capability, causes violent vibration, thrust reversal.
        Anti-surge control: recycle valve bypasses flow to prevent surge, controlled by δP/flow map.
        Testing: mechanical run test, full-load test, surge test to verify control system.""",
        key_factors=[
            "Polytropic efficiency >78% typical for modern designs, >82% for high-efficiency",
            "Thrust bearing design critical - magnetic thrust or tilting pad with high load capacity",
            "Intercoolers reduce power consumption 15-25% for multi-stage compression",
            "Variable inlet guide vanes (IGV) provide turndown without surge, improve part-load efficiency",
            "Acoustic analysis required for high flow velocity (>Mach 0.7) to prevent noise/fatigue"
        ],
        primary_authority=[
            "API 617 8th Edition Axial and Centrifugal Compressors for Petroleum, Chemical and Gas Industry Services",
            "API 684 Rotordynamic Tutorial",
            "API 614 Lubrication, Shaft-Sealing, and Oil-Control Systems for Special Purpose Applications",
            "ASME PTC 10 Performance Test Code for Compressors and Exhausters"
        ],
        burden_holder="compressor_OEM",
        adversary_position="Industrial blowers/fans adequate, API 617 over-specified for most applications",
        counter_arguments=[
            "API 617 compressors operate at extreme conditions - 10,000+ PSI, 500°F+, 15,000+ RPM",
            "Failure causes plant shutdown, safety incident, environmental release",
            "Rotordynamic analysis prevents catastrophic bearing/seal failure",
            "Dry gas seals eliminate oil contamination of process gas, reduce maintenance",
            "Surge control prevents $1M+ damage from uncontrolled surge event"
        ],
        resolution_strategy="API 617 mandatory for critical gas compression, high pressure/temperature, continuous operation. Industrial fans acceptable for low pressure air, non-critical",
        entity_scope="gas_processing",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="api_670_machinery_protection_systems",
        keywords=["API 670", "machinery protection", "vibration monitoring", "proximity probe", "accelerometer", "trip setpoint", "Bently Nevada"],
        conclusion_template=[
            "API 670 5th edition defines machinery protection systems (MPS) for critical turbomachinery monitoring.",
            "Minimum sensors: 2 radial vibration probes per bearing (XY), 1 axial position probe (thrust), 1 speed probe (keyphasor).",
            "Alarm/trip setpoints: vibration alarm 6 mils, trip 7.5 mils (displacement) OR alarm 0.3 in/s, trip 0.5 in/s (velocity)."
        ],
        reasoning_framework="""MPS protects against catastrophic machinery failure by detecting abnormal conditions and initiating shutdown.
        Proximity probes (eddy current): measure shaft displacement 0-200 mils, DC-10kHz response, for journal bearings <3000 RPM.
        Accelerometers (piezoelectric): measure casing vibration 10-10,000 Hz, for rolling element bearings, high frequency detection.
        Vibration monitoring: detects unbalance, misalignment, rubs, bearing wear, looseness, resonance.
        Axial position: thrust bearing wear, rotor thermal growth, hydraulic forces.
        Speed monitoring: overspeed, underspeed, loss of speed signal.
        Trip logic: 2oo3 voting (2 out of 3 sensors) for critical machines, prevents spurious trips.""",
        key_factors=[
            "Sensor installation critical - probe gap 40-80 mils, perpendicular to shaft, non-magnetic area",
            "Cable length limits: extension cables every 300 ft max for proximity probes",
            "Transducer electronic modules (TEM): -24 VDC output, 200 mV/mil sensitivity typical",
            "Data recording: continuous trending for predictive maintenance, event capture for failure analysis",
            "Integration with DCS/SCADA for plant-wide monitoring, automated permissives"
        ],
        primary_authority=[
            "API 670 5th Edition Machinery Protection Systems",
            "ISO 20816 (formerly ISO 10816) Mechanical Vibration - Measurement and Evaluation",
            "API 610/617/611/612 machinery standards reference API 670 for monitoring",
            "IEC 61508 Functional Safety of Electrical/Electronic/Programmable Electronic Safety Systems"
        ],
        burden_holder="instrumentation_engineer",
        adversary_position="Simple vibration switch adequate, full MPS over-designed for most equipment",
        counter_arguments=[
            "API 670 MPS prevents catastrophic failures - compressor explosion, turbine blade liberation",
            "Downtime cost justifies MPS investment - 24-48 hour outage = $500K-2M lost production",
            "Predictive maintenance from trending reduces unplanned shutdowns 40-60%",
            "Regulatory requirements (PSM, RMP) require protection systems for critical equipment",
            "2oo3 voting eliminates spurious trips while maintaining safety integrity level (SIL 2)"
        ],
        resolution_strategy="API 670 MPS for critical rotating equipment per API 610/617/611/612, drivers >500 HP, hazardous services. Simple switches acceptable for non-critical <100 HP",
        entity_scope="critical_machinery",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="vibration_analysis_fault_diagnosis",
        keywords=["vibration analysis", "FFT", "spectrum", "unbalance", "misalignment", "bearing defects", "1X", "2X", "harmonics"],
        conclusion_template=[
            "FFT (Fast Fourier Transform) spectrum analysis decomposes vibration waveform into frequency components identifying fault types.",
            "Unbalance: high 1× RPM radial vibration, in-phase in horizontal/vertical directions.",
            "Misalignment: high 2× RPM (angular) or 1×/2×/3× (parallel), 180° phase shift across coupling."
        ],
        reasoning_framework="""Vibration signature analysis: each fault type produces characteristic frequency pattern.
        Unbalance (mass eccentricity): 1× running speed dominant, radial direction, in-phase both bearings.
        Angular misalignment: 2× running speed dominant, axial vibration significant.
        Parallel misalignment: 1× dominant but also 2×/3× harmonics, high radial vibration.
        Bearing defects: BPFO (ball pass frequency outer race), BPFI (inner race), BSF (ball spin), FTF (cage).
        Resonance: amplified vibration at natural frequency, phase shift through resonance.
        Looseness: multiple harmonics (1×, 2×, 3×, 4×+), non-integer harmonics indicate looseness.
        ISO 20816 severity zones: A=good, B=acceptable, C=unsatisfactory, D=unacceptable per machine type/speed.""",
        key_factors=[
            "Data collection: triaxial accelerometers, 1-10 kHz bandwidth for bearing analysis",
            "Fmax selection: 3× highest frequency of interest (bearing defects require 10-50× RPM)",
            "Time waveform analysis: impacts/shocks visible in time domain, periodic for bearing faults",
            "Phase analysis: timing relationship between measurements identifies fault type",
            "Trending: track vibration over time, detect gradual deterioration before failure"
        ],
        primary_authority=[
            "ISO 20816-1 Mechanical Vibration - Measurement and Evaluation (replaces ISO 10816)",
            "ISO 18436-2 Condition Monitoring and Diagnostics of Machines - Vibration Analysis",
            "API 610/617 vibration limits for specific machinery types",
            "SKF/Emerson/Pruftechnik vibration diagnostic guides"
        ],
        burden_holder="predictive_maintenance_technician",
        adversary_position="Overall vibration level adequate, spectrum analysis unnecessary complexity",
        counter_arguments=[
            "Overall vibration misses early-stage faults - bearing defects 10-50× running speed",
            "Spectrum analysis differentiates root cause - unbalance vs misalignment vs bearing",
            "Trending prevents catastrophic failure - bearing defects detectable 3-6 months before failure",
            "Phase analysis critical for balancing/alignment - amplitude alone insufficient",
            "Automated diagnostics (AI/ML) requires frequency domain data for pattern recognition"
        ],
        resolution_strategy="FFT spectrum analysis for all critical rotating equipment, quarterly baseline, monthly trending, phase analysis for high 1×/2× vibration, envelope analysis for bearing faults",
        entity_scope="predictive_maintenance",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="condition_monitoring_program_development",
        keywords=["condition monitoring", "predictive maintenance", "PdM", "vibration route", "thermography", "oil analysis", "ultrasound"],
        conclusion_template=[
            "Comprehensive condition monitoring combines multiple technologies: vibration, oil analysis, thermography, ultrasound, motor current.",
            "Criticality-based monitoring: critical equipment monthly, essential quarterly, general semi-annually.",
            "ROI typical 5:1 to 10:1 - maintenance cost savings plus avoided downtime justify program cost."
        ],
        reasoning_framework="""Condition-based maintenance replaces time-based (PM) or run-to-failure (reactive) strategies.
        Vibration analysis: rotating equipment (pumps, motors, gearboxes, fans), detects mechanical faults.
        Oil analysis: wear metals (Fe, Cu, Cr, Al), contamination (water, fuel, dirt), oxidation, viscosity - indicates bearing/gear wear.
        Thermography (IR imaging): electrical connections, motor windings, insulation, steam traps - finds hot spots.
        Ultrasound: bearing lubrication, steam leaks, compressed air leaks, electrical corona/tracking.
        Motor current signature analysis (MCSA): rotor bar defects, eccentricity, load variations.
        Equipment criticality matrix: production impact × failure consequence → monitoring frequency/technology.""",
        key_factors=[
            "Criticality ranking: safety, environmental, production, cost to classify A/B/C equipment",
            "Technology selection based on failure mode: vibration for mechanical, oil for lubricated, IR for thermal/electrical",
            "Route optimization: handheld data collector, measurement points, route time <4 hours",
            "Alarm limits: ALERT (investigate), ALARM (schedule repair), FAULT (immediate shutdown)",
            "CMMS integration: work order generation, history tracking, spare parts trigger"
        ],
        primary_authority=[
            "ISO 17359 Condition Monitoring and Diagnostics of Machines - General Guidelines",
            "ISO 13374 Condition Monitoring and Diagnostics - Data Processing, Communication and Presentation",
            "ASTM D6224 Standard Practice for In-Service Monitoring of Lubricating Oil for Auxiliary Power Plant Equipment",
            "ISO 18434 Condition Monitoring and Diagnostics - Thermography"
        ],
        burden_holder="reliability_manager",
        adversary_position="PM (time-based) maintenance adequate, condition monitoring too expensive",
        counter_arguments=[
            "PdM reduces maintenance cost 25-30% vs PM, eliminates unnecessary overhauls",
            "Unplanned downtime 5-10× more costly than planned maintenance window",
            "Early fault detection prevents secondary damage (bearing failure → shaft damage → seal failure)",
            "Regulatory compliance (PSM, OSHA) requires documented mechanical integrity program",
            "Remote monitoring (IIoT sensors) provides continuous surveillance vs monthly routes"
        ],
        resolution_strategy="Implement multi-technology PdM program, start with critical equipment (A-list), vibration + oil analysis baseline, expand to thermography/ultrasound, integrate with CMMS",
        entity_scope="industrial_plants",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="root_cause_analysis_machinery_failures",
        keywords=["RCA", "root cause analysis", "5 whys", "fishbone diagram", "failure mode", "FMEA", "fault tree"],
        conclusion_template=[
            "RCA systematically identifies underlying causes of machinery failures to prevent recurrence.",
            "Common root causes: inadequate lubrication (40%), misalignment (30%), contamination (15%), overload (10%).",
            "Effective RCA: physical evidence collection, timeline reconstruction, causal factor tree, corrective action verification."
        ],
        reasoning_framework="""Machinery failures have proximate cause (immediate trigger) vs root cause (underlying systemic issue).
        Example: Bearing failure (proximate) ← inadequate lubrication (intermediate) ← missing PM schedule (root).
        5 Whys technique: iteratively ask "why" to drill down to root cause, typically 3-5 levels deep.
        Fishbone (Ishikawa) diagram: categorize causes - Man, Machine, Method, Material, Measurement, Environment.
        Physical evidence: failed components, oil samples, vibration data, operating logs - preserve for analysis.
        Failure modes: fatigue (cyclic stress), wear (adhesive, abrasive, corrosive), overload (ductile, brittle), corrosion.
        RCA deliverable: report with timeline, evidence, causal tree, action items, ownership, verification.""",
        key_factors=[
            "Assemble cross-functional team: operations, maintenance, engineering, reliability",
            "Evidence preservation: photograph failed parts, measure clearances, save oil/wear debris",
            "Metallurgical analysis: SEM (scanning electron microscope) reveals fatigue striations, crack origin",
            "Operating data review: vibration trends, temperature, pressure leading to failure",
            "Verification: implement corrective actions, monitor to confirm recurrence prevented"
        ],
        primary_authority=[
            "NASA RCA Guide (NASA-STD-8739.19) - comprehensive methodology",
            "API RP 584 Integrity Operating Windows - process safety applications",
            "MIL-STD-1629A Procedures for Performing FMEA",
            "ISO 14224 Collection and Exchange of Reliability and Maintenance Data for Equipment"
        ],
        burden_holder="reliability_engineer",
        adversary_position="Replace failed component, return to service, detailed RCA unnecessary cost",
        counter_arguments=[
            "Repeat failures cost 5-10× single failure (parts + downtime + lost production)",
            "Systemic issues affect multiple equipment - fix root cause prevents fleet-wide failures",
            "RCA identifies latent design/process flaws requiring engineering change",
            "Regulatory requirements (PSM, OSHA) mandate investigation of mechanical integrity failures",
            "Knowledge capture - RCA documents lessons learned for organization"
        ],
        resolution_strategy="Mandatory RCA for: unplanned shutdowns, safety incidents, repeat failures (3+ in 12 months), high-cost failures (>$50K), critical equipment. Use structured methodology (5 Whys + Fishbone), verify corrective actions",
        entity_scope="industrial_reliability",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="spare_parts_strategy_insurance_vs_consumable",
        keywords=["spare parts", "insurance spares", "consumable spares", "critical spares", "lead time", "obsolescence", "inventory optimization"],
        conclusion_template=[
            "Insurance spares: low failure rate, long lead time, high consequence items (spare rotor, casing) - stock based on criticality.",
            "Consumable spares: high usage rate, short lead time items (seals, bearings, filters) - stock based on consumption rate + lead time.",
            "Optimal strategy: criticality matrix (failure probability × consequence) determines stock level, consignment for expensive items."
        ],
        reasoning_framework="""Spare parts inventory balances carrying cost vs stockout cost (downtime + expedite fees).
        Insurance spares: purchased at equipment procurement, may never be used, high carrying cost, prevents long outage.
        Examples: complete spare pump, gearbox, motor, compressor rotor, turbine blades.
        Consumable spares: regular replacement during PM, predictable usage, economic order quantity (EOQ) optimization.
        Examples: mechanical seals, bearings, couplings, oil filters, V-belts, gaskets.
        Criticality classification: A (critical, stock immediately), B (essential, stock or fast-track), C (general, order as needed).
        Lead time: domestic 2-8 weeks, international 12-26 weeks, engineered-to-order 26-52 weeks.
        Obsolescence risk: technology change, OEM discontinuation, interchangeability issues.""",
        key_factors=[
            "Criticality analysis: production impact, safety, environmental, redundancy, repair time",
            "Failure rate data: MTBF from OEM, industry standards (OREDA, IEEE 493), plant history",
            "Vendor-managed inventory (VMI): supplier stocks consignment parts on-site, pay on use",
            "Interchangeability: standardize on common frame sizes, bearing types, seal designs",
            "Repairable vs replace: cost threshold - repair if <70% replacement cost"
        ],
        primary_authority=[
            "ISO 55000 Asset Management - Overview, Principles and Terminology",
            "API 686 Annex C Recommended Spare Parts List for Pumps",
            "API 614 Annex A Recommended Spare Parts for Lubrication Systems",
            "SMRP (Society for Maintenance & Reliability Professionals) Best Practices"
        ],
        burden_holder="materials_manager",
        adversary_position="Just-in-time procurement eliminates inventory cost, spares on demand",
        counter_arguments=[
            "Critical equipment downtime cost $10K-100K/hour - spare parts cost negligible vs lost production",
            "Lead times for engineered equipment (compressor rotor, special alloy pump) 6-18 months",
            "Expedite fees 50-200% premium plus air freight for emergency procurement",
            "Obsolescence risk - equipment life 20-30 years, OEM support may end after 10-15 years",
            "Multiple identical units justify pooled spares - 10 pumps may need 2-3 spare rotors"
        ],
        resolution_strategy="Stock insurance spares for critical equipment with lead time >12 weeks, consumable spares per EOQ analysis, VMI for high-value/low-turnover items, standardize equipment to reduce SKU count",
        entity_scope="industrial_asset_management",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="motor_enclosure_types_nema_ratings",
        keywords=["motor enclosure", "TEFC", "ODP", "TENV", "explosion proof", "NEMA 1", "NEMA 4X", "IP rating"],
        conclusion_template=[
            "TEFC (Totally Enclosed Fan Cooled) prevents entry of external air, external fan cools, suitable for dusty/wet environments.",
            "ODP (Open Drip Proof) allows air circulation through motor, lowest cost, clean dry indoor locations only.",
            "Explosion proof (Class I Div 1/2) contains internal arc, prevents ignition of external atmosphere, hazardous locations."
        ],
        reasoning_framework="""Enclosure selection driven by: environment (dust, moisture, corrosive), hazardous area classification, temperature/altitude.
        ODP: openings prevent vertically falling liquids/solids >15° from vertical, cheapest, best cooling, clean environments only.
        TEFC: no openings, external cooling fan on shaft, prevents dust/moisture ingress, slightly derated vs ODP.
        TENV (Totally Enclosed Non-Ventilated): no fan, convection cooling only, low HP (<5 HP) or low duty cycle.
        Explosion proof (XP): UL 1004/674, CSA C22.2, contains explosion, flame paths prevent propagation, hazloc Div 1.
        NEMA ratings: 1 (indoor general), 3R (outdoor rain), 4 (hosedown), 4X (corrosion resistant), 12 (dust tight).
        IP ratings: IP54 (dust protected, splash), IP55 (dust tight, water jet), IP56 (dust tight, powerful water jet).""",
        key_factors=[
            "Hazardous area classification per NEC Article 500/505: Class (material type), Division (likelihood), Group (ignition energy)",
            "Altitude derating: >3300 ft reduce motor rating 1% per 330 ft or install larger frame",
            "Ambient temperature: standard 40°C, special 60°C insulation for hot environments",
            "Corrosion protection: stainless hardware, epoxy paint, sealed conduit entries for chemical plants",
            "Mounting: foot mount (NEMA 143T-580), C-face flange, D-flange, rigid base vs resilient"
        ],
        primary_authority=[
            "NEMA MG 1 Part 4 Enclosures and Mounting Arrangements",
            "NEC Article 500 Hazardous (Classified) Locations - Classes, Divisions, Groups",
            "UL 1004-1 Rotating Electrical Machines - General Requirements",
            "IEC 60034-5 Degrees of Protection Provided by Integral Enclosures (IP Code)",
            "IEEE 841 Petroleum and Chemical Industry - Severe Duty Motors"
        ],
        burden_holder="electrical_engineer",
        adversary_position="ODP lowest cost, use unless environment requires enclosed",
        counter_arguments=[
            "TEFC prevents moisture condensation in windings, extends motor life 2-3×",
            "Washdown environments (food, pharmaceutical) require NEMA 4/4X or IP66",
            "Hazardous locations legally require explosion proof or purged/pressurized enclosures",
            "Outdoor applications: TEFC minimum, ODP corrodes from rain/humidity",
            "Chemical plants: severe duty TEFC per IEEE 841 - stainless hardware, sealed conduits, epoxy coating"
        ],
        resolution_strategy="ODP only for indoor climate-controlled clean environments, TEFC for general industrial/outdoor, XP for hazloc Div 1, specify IP rating for international projects, IEEE 841 severe duty for chemical plants",
        entity_scope="motor_selection",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="gearbox_lubrication_oil_vs_grease",
        keywords=["gear lubrication", "gear oil", "ISO VG", "EP additive", "splash lubrication", "forced lubrication", "grease lubrication"],
        conclusion_template=[
            "Oil lubrication (splash or forced) required for continuous duty, speeds >1000 RPM, power >5 HP.",
            "ISO VG 220-320 common for industrial gearboxes, EP (extreme pressure) additives for high load.",
            "Grease lubrication limited to low speed (<500 RPM), intermittent duty, sealed-for-life small gearboxes."
        ],
        reasoning_framework="""Gear tooth lubrication: forms EHL (elastohydrodynamic) film separating metal surfaces under high pressure.
        Lubrication regime: boundary (thin film, metal contact, wear), mixed (partial contact), full film (no contact, ideal).
        Oil viscosity critical: too thin → insufficient film, too thick → churning losses, poor cold start.
        ISO VG grade: viscosity at 40°C in centistokes - VG 150/220/320/460 common for gears.
        AGMA lubricant numbers: 2EP, 3EP, 4EP, 5EP, 6EP, 7EP (higher number = higher viscosity).
        EP additives (sulfur-phosphorus compounds): react under pressure to form protective layer, prevent scuffing/scoring.
        Splash lubrication: gears dip in oil sump, throw oil onto upper gears/bearings, to ~5000 fpm pitch line velocity.
        Forced lubrication: pump delivers oil to spray nozzles on mesh/bearings, required >5000 fpm or high power.""",
        key_factors=[
            "Load intensity: Hertzian contact stress 150-300 ksi typical, EP required >200 ksi",
            "Operating temperature: oil degradation accelerates above 200°F, synthetic extends to 300°F",
            "Contamination: filtration 10-25 micron absolute for forced lube systems",
            "Oil change interval: mineral 2000-6000 hours, synthetic 8000-12000 hours, oil analysis guides",
            "Synthetic vs mineral: synthetics superior extreme temp/load, 3-5× cost, 2-4× life"
        ],
        primary_authority=[
            "AGMA 9005-F16 Industrial Gear Lubrication",
            "ISO 12925-1 Lubricants, Industrial Oils and Related Products - Classification - Part 1: Family C (Gears)",
            "API 613 Section 5 Lubrication System Requirements for Special Purpose Gear Units",
            "DIN 51517 Lubricants - Lubricating Oils for Gears"
        ],
        burden_holder="lubrication_engineer",
        adversary_position="Any gear oil adequate if meets viscosity grade, EP unnecessary",
        counter_arguments=[
            "Wrong viscosity causes 30-40% of gear failures - too thin → scuffing, too thick → overheating",
            "Non-EP oil fails under boundary lubrication conditions, scoring/pitting/spalling damage",
            "Synthetic oils justify cost in severe service: high temp, high load, extended drain, low temp start",
            "Oil analysis (wear metals, viscosity, TAN, water) detects degradation before failure",
            "Forced lube required for high speed - splash lubrication inadequate cooling/distribution"
        ],
        resolution_strategy="Specify ISO VG grade per AGMA 9005 based on ambient temp + speed + load, EP additives mandatory for industrial gears, forced lube >5000 fpm or >100 HP, synthetic for severe duty",
        entity_scope="gear_drives",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="api_611_steam_turbine_applications",
        keywords=["API 611", "steam turbine", "extraction turbine", "condensing turbine", "back pressure turbine", "governing system"],
        conclusion_template=[
            "API 611 covers general purpose steam turbines for mechanical drive (pumps, compressors, generators) in petroleum/chemical.",
            "Turbine types: condensing (maximum power extraction), back pressure (process steam use), extraction (combined power + process steam).",
            "Governing: mechanical (speed droop 3-5%), electronic (isochronous or droop), overspeed trip 110% rated speed."
        ],
        reasoning_framework="""Steam turbines convert thermal energy to mechanical work via expansion across nozzles/blades.
        Condensing turbine: exhaust to vacuum condenser (~1-4 psia), maximizes power output, requires cooling water.
        Back pressure (non-condensing): exhaust at process pressure (50-200 psig), lower power but provides process steam.
        Extraction turbine: bleeds steam at intermediate pressure for process, balance to condenser or back pressure.
        Governing system: controls steam admission to maintain speed under varying load.
        Mechanical governor: centrifugal flyweights move valve via linkage, 3-5% speed droop inherent.
        Electronic governor: speed sensor + controller + servo valve, can achieve isochronous (0% droop) for grid-tied generators.
        Overspeed trip: mechanical bolt-type or electronic, independent of governor, trips at 110% speed.""",
        key_factors=[
            "Steam conditions: pressure (600-1500 psig typical), temperature (750-950°F), superheat >100°F prevents moisture erosion",
            "Expansion ratio: condensing 50-100:1, back pressure 5-20:1, affects stage count (1-15 stages)",
            "Efficiency: mechanical drive 50-70%, extraction ~60%, condensing 70-80% for large units",
            "Rotor dynamics: lateral critical speed analysis, avoid 1× operating speed ±20%",
            "Blade erosion: moisture >10% causes erosion, solid particle erosion from boiler carryover"
        ],
        primary_authority=[
            "API 611 5th Edition General Purpose Steam Turbines for Petroleum, Chemical and Gas Industry Services",
            "API 612 Special Purpose Steam Turbines (for critical services)",
            "ASME PTC 6 Steam Turbines Performance Test Code",
            "NEMA SM 24 Steam Turbines for Mechanical Drive Service"
        ],
        burden_holder="turbine_manufacturer",
        adversary_position="Electric motor drive simpler/cheaper than steam turbine, avoid complexity",
        counter_arguments=[
            "Steam turbine utilizes waste heat (cogeneration), efficiency 70-80% vs 40% Rankine cycle",
            "Eliminates electric power cost for large drives (>1000 HP), payback 2-5 years",
            "Variable speed without VFD (harmonics, motor heating issues)",
            "Reliability: 20-30 year life, 3-5 year overhaul interval, proven technology",
            "Essential for sites with steam surplus (cogeneration, process steam letdown)"
        ],
        resolution_strategy="Steam turbine economical for sites with steam availability + large continuous loads >500 HP, back pressure if process steam needed, condensing for maximum power, extraction for flexible operation",
        entity_scope="process_plants",
        confidence=ConfidenceLevel.AGGRESSIVE
    ),

    DoctrineBlock(
        topic="coupling_balance_and_alignment_runout",
        keywords=["coupling balance", "balance grade", "G2.5", "runout", "TIR", "coupling hub runout", "field balancing"],
        conclusion_template=[
            "Coupling balance quality per ISO 1940 G2.5 for general machinery, G1.0 for precision, G6.3 for pumps/fans.",
            "Coupling hub runout: radial TIR <0.005in, face TIR <0.003in, excessive runout causes vibration even with perfect alignment.",
            "Field balancing required after coupling installation if 1× vibration >0.15 in/s, balance to <0.10 in/s or G2.5 equivalent."
        ],
        reasoning_framework="""Coupling contributes to rotor unbalance if: mass imbalance, runout (eccentricity), bent hub, asymmetric design.
        Balance quality G = eω where e=eccentricity (mm), ω=angular velocity (rad/s), G in mm/s.
        G2.5: eccentricity = 2.5/(ω) → 3600 RPM (377 rad/s): e = 0.0066 mm = 0.00026 in.
        Runout vs balance: runout is geometric error (coupling hub not concentric/perpendicular), balance is mass distribution.
        High runout creates variable radius → centrifugal force varies → vibration even if mass balanced.
        Coupling hub TIR spec: API 610 <0.002in for pumps, API 617 <0.001in for compressors, general industrial 0.005in.
        Field balancing: single-plane for disc rotors, two-plane for long rotors, influence coefficient method.""",
        key_factors=[
            "Measure runout before and after coupling installation - detects bent shaft, poor fit",
            "Coupling half balance: balance hubs separately before assembly, mark orientation",
            "High speed (>3600 RPM): G1.0 balance, precision runout <0.002in critical",
            "Trim balance: balance coupling-shaft assembly in-situ if vibration excessive",
            "Coupling guard: must not contact guard, guard balance not required if no contact"
        ],
        primary_authority=[
            "ISO 1940-1 Mechanical Vibration - Balance Quality Requirements for Rotors in a Constant State",
            "ISO 21940-11 Rotodynamic Balance - Procedures and Tolerances for Rotors with Rigid Behavior - Part 11: Procedures",
            "API 610 Section 6.8.4 Coupling Installation and Balance",
            "API 684 Tutorial on Balancing of Turbomachinery Rotors"
        ],
        burden_holder="field_service_technician",
        adversary_position="Coupling manufacturer balances adequately, field check unnecessary",
        counter_arguments=[
            "Coupling unbalance common cause of high 1× vibration after maintenance",
            "Runout from poor press fit, damaged taper, or bent shaft invisible without dial indicator check",
            "Field balancing eliminates trial weights, achieves target in 1-2 runs with influence coefficients",
            "High vibration accelerates bearing wear, coupling wear, seal leakage - costs >>balance cost",
            "API equipment contractually requires balance verification, documented runout check"
        ],
        resolution_strategy="Measure coupling hub runout during installation, balance per ISO 1940 for equipment class, trim balance if 1× vibration >0.15 in/s, verify balance quality with vibration analyzer",
        entity_scope="rotating_equipment_installation",
        confidence=ConfidenceLevel.DEFENSIBLE
    )
]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    """Tracks query performance, hit rates, error domains"""

    def __init__(self):
        self.queries_total = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors_by_category: Dict[str, int] = {}
        self.latency_samples: List[float] = []
        self.start_time = time.time()

    def record_query(self, hit: bool, latency_ms: float, categories: List[IssueCategory]):
        self.queries_total += 1
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        self.latency_samples.append(latency_ms)
        for cat in categories:
            self.errors_by_category[cat.value] = self.errors_by_category.get(cat.value, 0) + 1

    def get_metrics(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        avg_latency = sum(self.latency_samples) / len(self.latency_samples) if self.latency_samples else 0
        return {
            "uptime_seconds": uptime,
            "queries_total": self.queries_total,
            "cache_hit_rate": self.cache_hits / self.queries_total if self.queries_total > 0 else 0,
            "avg_latency_ms": avg_latency,
            "error_domains": self.errors_by_category
        }


telemetry = TelemetryCollector()


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

def normalize_query(question: str) -> str:
    """Semantic normalization for rotating equipment queries"""
    q = question.lower().strip()

    # Motor terminology normalization
    q = q.replace("electric motor", "motor").replace("induction motor", "motor")
    q = q.replace("variable frequency drive", "vfd").replace("variable speed drive", "vfd")
    q = q.replace("nema premium", "ie3").replace("premium efficiency", "ie3")

    # Gear terminology
    q = q.replace("gearbox", "gear drive").replace("speed reducer", "gear drive")
    q = q.replace("right-angle", "right angle").replace("bevel gear", "right angle")

    # Coupling terminology
    q = q.replace("flexible coupling", "coupling").replace("disc-pack", "disc coupling")

    # Seal terminology
    q = q.replace("mechanical seal", "seal").replace("seal flush", "seal plan")
    q = q.replace("plan 11", "plan11").replace("plan 23", "plan23")

    # Vibration terminology
    q = q.replace("vibration analysis", "vibration").replace("spectrum analysis", "fft")
    q = q.replace("predictive maintenance", "pdm").replace("condition monitoring", "cbm")

    return q


def search_doctrine_cache(question: str) -> Tuple[List[DoctrineBlock], bool]:
    """Search doctrine cache for matching blocks"""
    normalized = normalize_query(question)
    tokens = set(normalized.split())

    matches = []
    for doctrine in DOCTRINE_CACHE:
        keyword_set = set(k.lower() for k in doctrine.keywords)
        overlap = len(tokens & keyword_set)
        if overlap >= 2:  # Require at least 2 keyword matches
            matches.append((overlap, doctrine))

    matches.sort(key=lambda x: x[0], reverse=True)
    top_matches = [d for _, d in matches[:5]]

    cache_hit = len(top_matches) >= 1
    return top_matches, cache_hit


def categorize_issue(question: str, doctrines: List[DoctrineBlock]) -> List[IssueCategory]:
    """Determine issue categories from question and matched doctrines"""
    categories = set()
    q_lower = question.lower()

    # Keyword-based categorization
    if any(word in q_lower for word in ["motor", "nema", "efficiency", "enclosure", "service factor"]):
        categories.add(IssueCategory.MOTOR_SELECTION)
    if any(word in q_lower for word in ["vfd", "drive", "harmonic", "pwm", "inverter"]):
        categories.add(IssueCategory.VFD_APPLICATION)
    if any(word in q_lower for word in ["gear", "gearbox", "reducer", "planetary", "helical"]):
        categories.add(IssueCategory.GEAR_DRIVES)
    if any(word in q_lower for word in ["coupling", "disc", "gear coupling", "elastomeric", "flexible"]):
        categories.add(IssueCategory.COUPLING_SELECTION)
    if any(word in q_lower for word in ["alignment", "laser", "dial indicator", "misalignment", "soft foot"]):
        categories.add(IssueCategory.SHAFT_ALIGNMENT)
    if any(word in q_lower for word in ["seal", "mechanical seal", "api 682", "plan", "packing"]):
        categories.add(IssueCategory.MECHANICAL_SEALS)
    if any(word in q_lower for word in ["shaft", "keyway", "torsion", "stress concentration", "fatigue"]):
        categories.add(IssueCategory.SHAFT_DESIGN)
    if any(word in q_lower for word in ["vibration", "fft", "spectrum", "unbalance", "bearing defect"]):
        categories.add(IssueCategory.VIBRATION_ANALYSIS)
    if any(word in q_lower for word in ["api 610", "api 617", "api 670", "api 611", "api 682"]):
        categories.add(IssueCategory.API_STANDARDS)
    if any(word in q_lower for word in ["condition monitoring", "pdm", "predictive", "oil analysis", "thermography"]):
        categories.add(IssueCategory.CONDITION_MONITORING)
    if any(word in q_lower for word in ["failure", "rca", "root cause", "failure analysis"]):
        categories.add(IssueCategory.FAILURE_ANALYSIS)
    if any(word in q_lower for word in ["spare", "inventory", "stock", "consignment"]):
        categories.add(IssueCategory.SPARE_PARTS)

    # Add categories from matched doctrines
    for doctrine in doctrines:
        if "motor" in doctrine.topic or "efficiency" in doctrine.topic or "enclosure" in doctrine.topic:
            categories.add(IssueCategory.MOTOR_SELECTION)
        if "vfd" in doctrine.topic or "harmonic" in doctrine.topic:
            categories.add(IssueCategory.VFD_APPLICATION)
        if "gear" in doctrine.topic:
            categories.add(IssueCategory.GEAR_DRIVES)
        if "coupling" in doctrine.topic:
            categories.add(IssueCategory.COUPLING_SELECTION)
        if "alignment" in doctrine.topic:
            categories.add(IssueCategory.SHAFT_ALIGNMENT)
        if "seal" in doctrine.topic or "packing" in doctrine.topic:
            categories.add(IssueCategory.MECHANICAL_SEALS)
        if "shaft" in doctrine.topic or "torsional" in doctrine.topic or "lateral" in doctrine.topic:
            categories.add(IssueCategory.SHAFT_DESIGN)
        if "vibration" in doctrine.topic or "critical" in doctrine.topic:
            categories.add(IssueCategory.VIBRATION_ANALYSIS)
        if "api" in doctrine.topic:
            categories.add(IssueCategory.API_STANDARDS)
        if "monitoring" in doctrine.topic or "condition" in doctrine.topic:
            categories.add(IssueCategory.CONDITION_MONITORING)
        if "failure" in doctrine.topic or "rca" in doctrine.topic:
            categories.add(IssueCategory.FAILURE_ANALYSIS)
        if "spare" in doctrine.topic:
            categories.add(IssueCategory.SPARE_PARTS)

    return list(categories) if categories else [IssueCategory.VIBRATION_ANALYSIS]


def build_answer(
    question: str,
    doctrines: List[DoctrineBlock],
    mode: ResponseMode,
    categories: List[IssueCategory]
) -> Tuple[str, List[str], List[str]]:
    """Construct answer from doctrine blocks"""

    if not doctrines:
        return (
            "No specific rotating equipment doctrine matched this query. Please provide more details about the equipment type (motor, pump, gearbox, coupling, etc.) and the specific technical question.",
            [],
            ["General rotating equipment analysis attempted"]
        )

    primary = doctrines[0]
    authorities = list(primary.primary_authority)
    reasoning_chain = [
        f"Matched doctrine: {primary.topic}",
        f"Confidence level: {primary.confidence.value}",
        f"Key factors: {', '.join(primary.key_factors[:3])}"
    ]

    if mode == ResponseMode.FAST:
        answer = " ".join(primary.conclusion_template)
        reasoning_chain.append("Fast mode: conclusion template only")

    elif mode == ResponseMode.DEFENSE:
        answer_parts = [
            "ROTATING EQUIPMENT ANALYSIS:",
            "",
            "CONCLUSION:",
            " ".join(primary.conclusion_template),
            "",
            "TECHNICAL REASONING:",
            primary.reasoning_framework,
            "",
            "CRITICAL FACTORS:",
        ]
        for i, factor in enumerate(primary.key_factors, 1):
            answer_parts.append(f"{i}. {factor}")

        answer_parts.extend([
            "",
            "AUTHORITATIVE REFERENCES:",
        ])
        for i, auth in enumerate(primary.primary_authority, 1):
            answer_parts.append(f"{i}. {auth}")

        if len(doctrines) > 1:
            answer_parts.extend([
                "",
                "RELATED CONSIDERATIONS:",
            ])
            for doc in doctrines[1:3]:
                answer_parts.append(f"- {doc.topic}: {doc.conclusion_template[0]}")
                authorities.extend(doc.primary_authority)

        answer = "\n".join(answer_parts)
        reasoning_chain.append("Defense mode: full technical analysis with authorities")

    else:  # MEMO mode
        answer_parts = [
            f"TECHNICAL MEMORANDUM: {primary.topic.replace('_', ' ').title()}",
            "=" * 80,
            "",
            "EXECUTIVE SUMMARY:",
            " ".join(primary.conclusion_template),
            "",
            "TECHNICAL ANALYSIS:",
            primary.reasoning_framework,
            "",
            "KEY ENGINEERING FACTORS:",
        ]
        for i, factor in enumerate(primary.key_factors, 1):
            answer_parts.append(f"{i}. {factor}")

        answer_parts.extend([
            "",
            "INDUSTRY STANDARDS & REFERENCES:",
        ])
        for i, auth in enumerate(primary.primary_authority, 1):
            answer_parts.append(f"{i}. {auth}")

        answer_parts.extend([
            "",
            f"BURDEN OF PROOF: {primary.burden_holder.replace('_', ' ').title()}",
            "",
            "ADVERSARIAL POSITION:",
            primary.adversary_position,
            "",
            "COUNTER-ARGUMENTS:",
        ])
        for i, counter in enumerate(primary.counter_arguments, 1):
            answer_parts.append(f"{i}. {counter}")

        answer_parts.extend([
            "",
            "RECOMMENDED STRATEGY:",
            primary.resolution_strategy,
            "",
            "CONTROLLING PRECEDENT:",
            primary.controlling_precedent or "Industry best practices and engineering standards govern",
        ])

        if len(doctrines) > 1:
            answer_parts.extend([
                "",
                "RELATED TECHNICAL DOMAINS:",
            ])
            for doc in doctrines[1:4]:
                answer_parts.append(f"\n{doc.topic.replace('_', ' ').title()}:")
                answer_parts.append(" ".join(doc.conclusion_template))
                authorities.extend(doc.primary_authority)

        answer_parts.extend([
            "",
            "=" * 80,
            f"Categories: {', '.join(c.value for c in categories)}",
            f"Confidence: {primary.confidence.value}",
        ])

        answer = "\n".join(answer_parts)
        reasoning_chain.append("Memo mode: comprehensive technical documentation")

    # Deduplicate authorities
    authorities = list(dict.fromkeys(authorities))

    return answer, authorities, reasoning_chain


def calculate_determinism_hash(question: str, answer: str, mode: ResponseMode) -> str:
    """SHA-256 hash for reproducibility verification"""
    content = f"{question}|{answer}|{mode.value}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def three_layer_response(request: QueryRequest) -> QueryResponse:
    """TIE-20 three-layer response: cache → semantic → deep"""
    start_time = time.time()

    logger.info(f"Query received: {request.question[:100]}")

    # Layer 1: Doctrine cache (0-50ms)
    doctrines, cache_hit = search_doctrine_cache(request.question)
    categories = categorize_issue(request.question, doctrines)

    # Layer 2: Would do semantic search if cache miss (not implemented - TIE pattern)
    # Layer 3: Would do deep LLM analysis if semantic insufficient (not implemented - TIE pattern)

    # Build answer
    answer, authorities, reasoning_chain = build_answer(
        request.question,
        doctrines,
        request.mode,
        categories
    )

    # Determine confidence
    if doctrines:
        confidence = doctrines[0].confidence
    else:
        confidence = ConfidenceLevel.DISCLOSURE

    # Calculate metrics
    query_time = (time.time() - start_time) * 1000
    determinism_hash = calculate_determinism_hash(request.question, answer, request.mode)

    # Record telemetry
    telemetry.record_query(cache_hit, query_time, categories)

    logger.info(f"Query completed in {query_time:.2f}ms, cache_hit={cache_hit}")

    return QueryResponse(
        answer=answer,
        confidence=confidence,
        categories=categories,
        authorities=authorities,
        reasoning_chain=reasoning_chain,
        mode=request.mode,
        determinism_hash=determinism_hash,
        query_time_ms=query_time
    )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="MECH10 - Rotating Equipment Reliability Engine",
    description="TIE Gold Standard mechanical engineering expertise for rotating machinery",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - three-layer TIE response"""
    try:
        return three_layer_response(request)
    except Exception as e:
        logger.error(f"Query error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check with engine metrics"""
    uptime = time.time() - START_TIME
    return HealthResponse(
        status="healthy",
        engine="MECH10_rotating_equipment",
        version="1.0.0",
        port=9050,
        doctrine_count=len(DOCTRINE_CACHE),
        uptime_seconds=uptime
    )


@APP.get("/metrics")
async def metrics_endpoint():
    """Telemetry metrics endpoint"""
    return telemetry.get_metrics()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all doctrine topics"""
    return {
        "total": len(DOCTRINE_CACHE),
        "topics": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value
            }
            for d in DOCTRINE_CACHE
        ]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting MECH10 Rotating Equipment Reliability Engine on port 9050")
    uvicorn.run(APP, host="0.0.0.0", port=9050)
