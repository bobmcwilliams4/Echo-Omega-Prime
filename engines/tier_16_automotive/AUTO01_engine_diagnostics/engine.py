import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
AUTO01 - Automotive Engine Diagnostics Intelligence Engine
===========================================================

COMPREHENSIVE AUTOMOTIVE DIAGNOSTIC KNOWLEDGE ENGINE

Domain Coverage:
- OBD-II diagnostic trouble codes (P0xxx, B0xxx, C0xxx, U0xxx)
- Engine management systems (ECU, PCM, TCM)
- Fuel injection systems (port, GDI, diesel common rail)
- Ignition systems (coil-on-plug, distributorless)
- Emission control systems (catalytic converter, EGR, DPF, SCR)
- Engine mechanical diagnostics
- Cooling system diagnostics
- Turbocharger/supercharger systems
- Variable valve timing (VVT, VTEC, VarioCam)
- Engine sensors and interpretation
- Scan tool data analysis
- Misfire and no-start diagnostics
- Hybrid/EV powertrain basics

Port: 9061
Version: 1.0.0
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGINE_ID = "AUTO01"
ENGINE_NAME = "Automotive Engine Diagnostics Intelligence"
VERSION = "1.0.0"
PORT = 9061

# ============================================================================
# PYDANTIC MODELS
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


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Diagnostic question or symptom description")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Vehicle/diagnostic context")


class QueryResponse(BaseModel):
    engine_id: str
    query: str
    mode: str
    response: str
    confidence: str
    sources: List[str]
    triggered_doctrines: List[str]
    analysis_path: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    engine_id: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float


# ============================================================================
# DOCTRINE BLOCKS
# ============================================================================

@dataclass
class DoctrineBlock:
    """Atomic unit of automotive diagnostic knowledge"""
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
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# DOCTRINE CACHE - 25+ AUTOMOTIVE DIAGNOSTIC EXPERT BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="OBD-II P0xxx Powertrain Codes",
        keywords=["P0", "powertrain", "DTC", "engine code", "transmission code", "OBD-II"],
        conclusion_template=[
            "P0xxx codes indicate powertrain-related faults (engine, transmission, emissions)",
            "First two digits after P0 indicate the subsystem (P00xx=fuel/air, P01xx=fuel/air, P02xx=fuel/air, P03xx=ignition, P04xx=emissions)",
            "Generic codes (P0xxx) are standardized across manufacturers; manufacturer-specific codes start with P1xxx"
        ],
        reasoning_framework="""
        OBD-II P0 codes follow SAE J2012 standard:

        P0xxx Structure:
        - P = Powertrain
        - 0 = Generic (SAE standard), 1/2/3 = Manufacturer-specific
        - First digit after P0 = System (0/1/2=fuel/air metering, 3=ignition, 4=emissions, 5=speed/idle, 6=computer/output, 7/8=transmission)
        - Last two digits = Specific fault

        Common P0 Code Categories:
        P0100-P0199: Air/fuel metering (MAF, MAP, throttle position)
        P0200-P0299: Fuel system (injectors, fuel pressure)
        P0300-P0399: Ignition system (misfires, coils)
        P0400-P0499: Emissions (EGR, EVAP, catalytic converter)
        P0500-P0599: Speed/idle control (VSS, idle control)
        P0600-P0699: Computer/output circuits (ECU internal)
        P0700-P0799: Transmission control (TCM codes)

        Diagnostic Priority:
        1. Retrieve freeze frame data (conditions when code set)
        2. Check for pending/history codes (intermittent vs permanent)
        3. Verify with Mode 6 data (component test results)
        4. Clear codes and verify return (permanent fault vs transient)
        5. Inspect related components (sensors, wiring, connectors)
        """,
        key_factors=[
            "Code persistence (current, pending, or history)",
            "Freeze frame conditions (RPM, load, coolant temp when code set)",
            "Related codes (cascade failures vs root cause)",
            "Mode 6 test data for failing component",
            "Vehicle mileage and maintenance history"
        ],
        primary_authority=[
            "SAE J2012 (OBD-II DTC definitions)",
            "SAE J1979 (OBD-II diagnostic test modes)",
            "ISO 15031 (OBD-II communication standard)"
        ],
        burden_holder="Technician to diagnose root cause, not just clear code",
        adversary_position="Code reader shows code = bad part (incorrect assumption)",
        counter_arguments=[
            "Codes indicate symptoms, not always failed components",
            "P0171 (system too lean) could be vacuum leak, MAF fault, fuel pressure, or injector issue",
            "P0300 (random misfire) could be fuel, ignition, mechanical, or computer issue",
            "Multiple codes often share common root cause",
            "Intermittent codes require drive cycle monitoring"
        ],
        resolution_strategy="Use systematic diagnosis: verify code conditions, test components per TSB/FSM, confirm repair with drive cycle",
        entity_scope="All OBD-II compliant vehicles (1996+ US, 2001+ EU)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Engine Misfire Diagnosis (P030x Codes)",
        keywords=["misfire", "P0300", "P0301", "P0302", "rough idle", "shaking", "CEL flashing"],
        conclusion_template=[
            "Misfires have four primary causes: fuel delivery, ignition, compression, or engine management",
            "Random misfire (P0300) suggests common failure (fuel pressure, vacuum leak); cylinder-specific (P0301-P0312) suggests local fault",
            "Flashing check engine light indicates severe misfire risking catalytic converter damage (stop driving immediately)"
        ],
        reasoning_framework="""
        Misfire Diagnostic Decision Tree:

        1. CODE TYPE:
           - P0300 (Random/Multiple Cylinders): Common cause (fuel system, MAF, vacuum leak, bad gas)
           - P030x (Specific Cylinder): Local fault (spark plug, coil, injector, valve, compression)

        2. FUEL DELIVERY CHECK:
           - Fuel pressure test (spec typically 35-65 PSI port injection, 2000+ PSI GDI)
           - Injector flow test (spray pattern, balance, resistance)
           - Fuel quality (water contamination, octane, age)

        3. IGNITION SYSTEM CHECK:
           - Spark plug condition (gap, fouling, heat range)
           - Coil primary/secondary resistance
           - Ignition timing (base timing, advance curve)
           - Spark intensity test (30+ kV typical)

        4. COMPRESSION/MECHANICAL:
           - Compression test (should be within 10% cylinder-to-cylinder)
           - Leak-down test (locate leak: intake valve, exhaust valve, rings, head gasket)
           - Valve adjustment (overhead cam engines)
           - Timing chain/belt condition

        5. ENGINE MANAGEMENT:
           - MAF/MAP sensor readings vs expected
           - O2 sensor short/long-term fuel trims
           - Crankshaft/camshaft position sensor correlation
           - VVT operation (if equipped)

        Pattern Analysis:
        - Cold-start only: Enrichment issue, leaking injector
        - Hot-running only: Ignition coil thermal breakdown
        - Under load: Fuel pressure, ignition breakdown, EGR
        - Idle only: Vacuum leak, dirty throttle body, idle control
        """,
        key_factors=[
            "Misfire frequency (constant, intermittent, condition-specific)",
            "Cylinder pattern (random, specific, bank-specific)",
            "Driving conditions when occurs (idle, acceleration, cruise, deceleration)",
            "Engine temperature (cold, hot, both)",
            "Recent maintenance (spark plugs, coils, fuel filter)"
        ],
        primary_authority=[
            "SAE J1979 Mode 6 misfire counters",
            "OEM service manual diagnostic procedures",
            "ASE Certification Test L1 (Advanced Engine Performance)"
        ],
        burden_holder="Technician to isolate root cause through systematic testing",
        adversary_position="Replace spark plugs/coils first without diagnosis",
        counter_arguments=[
            "Spark plugs may look fine but still misfire under load",
            "Coils can test good cold but fail when hot",
            "Fuel injector flow may be in spec but spray pattern poor",
            "Compression test good but leak-down reveals valve issue",
            "Carbon buildup on GDI valves causes misfires despite good compression"
        ],
        resolution_strategy="Follow decision tree: scan tool data → swap test suspected components → verify with drive cycle",
        entity_scope="All spark-ignition gasoline engines",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Gasoline Direct Injection (GDI) Systems",
        keywords=["GDI", "direct injection", "FSI", "TFSI", "carbon buildup", "high pressure fuel"],
        conclusion_template=[
            "GDI systems inject fuel directly into combustion chamber at 2000-3000 PSI (vs 40-60 PSI port injection)",
            "GDI engines prone to intake valve carbon buildup (no fuel wash) causing rough idle, misfires, reduced power",
            "GDI requires high-pressure fuel pump (mechanical, driven by camshaft) and low-pressure pump (in-tank electric)"
        ],
        reasoning_framework="""
        GDI System Architecture:

        FUEL DELIVERY PATH:
        1. Low-pressure pump (in-tank, 60-100 PSI) → fuel filter → low-pressure line
        2. High-pressure pump (engine-driven, camshaft lobe) boosts to 2000-3000 PSI
        3. Fuel rail (high-pressure) → direct injectors → combustion chamber

        CRITICAL COMPONENTS:
        - High-pressure fuel pump (HPFP): Cam-driven, lubricated by fuel
        - Fuel pressure sensor: Monitors rail pressure for ECU control
        - Direct injectors: Piezo or solenoid, faster response than port injectors
        - Fuel pressure regulator: Mechanical or ECU-controlled

        COMMON FAILURES:
        1. HPFP failure: Metal shavings in fuel system, loss of high pressure
           Symptoms: Hard start, loss of power, P0087 low fuel pressure
           Cause: Manufacturing defect (early GDI), contaminated fuel, wear

        2. Intake valve carbon buildup: No fuel wash on back of valves
           Symptoms: Rough idle, misfires (P030x), reduced power, poor fuel economy
           Cause: Oil vapor from PCV, EGR gases deposit on valve face
           Solution: Walnut blasting (media blast), chemical cleaning, catch can install

        3. Injector failure: Carbon buildup on tip, electrical fault
           Symptoms: Hard start, misfire, P0300/P030x, black smoke
           Diagnosis: Injector flow test, spray pattern check

        4. Low-pressure pump failure: Inadequate feed to HPFP
           Symptoms: Intermittent stalling, P0087, starving HPFP

        DIAGNOSTIC APPROACH:
        - Monitor fuel rail pressure (scan tool PID): Should hit 2000+ PSI
        - Low-pressure fuel pressure test: 60-100 PSI typical
        - High-pressure fuel volume test: Varies by manufacturer
        - Injector balance test: Flow rate cylinder-to-cylinder
        - Borescope inspection: Check for carbon on intake valves (every 50K-80K miles)
        """,
        key_factors=[
            "Fuel quality (contamination damages HPFP)",
            "PCV system condition (oil vapor causes carbon)",
            "EGR operation (exhaust gases contribute to carbon)",
            "Fuel pressure sensor accuracy",
            "Injector spray pattern (tight cone vs atomization)"
        ],
        primary_authority=[
            "SAE 2010-01-1510 (GDI combustion analysis)",
            "OEM TSBs on HPFP failures (VW, BMW, GM)",
            "ASE L1 Advanced Engine Performance"
        ],
        burden_holder="Technician to differentiate low vs high pressure fuel system faults",
        adversary_position="GDI same as port injection, just different location",
        counter_arguments=[
            "GDI fuel pressure 50x higher than port injection",
            "GDI requires additional high-pressure pump (failure point)",
            "Carbon buildup unique to GDI (port injection washes valves)",
            "GDI injectors more expensive ($200-500 vs $50-150 port)",
            "GDI fuel contamination more critical (metal shavings from HPFP)"
        ],
        resolution_strategy="Separate low-pressure (in-tank pump, filter) from high-pressure (HPFP, rail, injectors) diagnosis",
        entity_scope="GDI gasoline engines (VW TSI/FSI, GM Ecotec, Ford EcoBoost, BMW N54/N55, etc.)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Catalytic Converter Diagnostics",
        keywords=["catalytic converter", "cat", "P0420", "P0430", "O2 sensor", "emissions"],
        conclusion_template=[
            "P0420/P0430 indicate catalytic converter efficiency below threshold (Bank 1/Bank 2)",
            "Upstream O2 sensor (pre-cat) oscillates; downstream (post-cat) should be steady if converter working",
            "Failed cats caused by: oil/coolant contamination, overheating from misfires, age/mileage, impact damage"
        ],
        reasoning_framework="""
        Catalytic Converter Operation & Diagnosis:

        CONVERTER FUNCTION:
        - Oxidizes HC (hydrocarbons) and CO (carbon monoxide) to CO2 and H2O
        - Reduces NOx (nitrogen oxides) to N2 and O2
        - Three-way catalyst: handles all three reactions
        - Operating temp: 400-800°F (efficiency peak ~750°F)

        O2 SENSOR MONITORING:
        Upstream O2 (pre-cat):
        - Rapid oscillation (0.1-0.9V, 1-2 Hz) = healthy closed-loop operation
        - Monitors air/fuel ratio, provides feedback to ECU

        Downstream O2 (post-cat):
        - Should be steady (0.6-0.8V, slow response) if converter working
        - Mimics upstream signal = converter not processing exhaust = P0420/P0430
        - ECU compares upstream/downstream switch counts

        DIAGNOSTIC CRITERIA:
        P0420/P0430 Set When:
        - Downstream O2 sensor switches too frequently (>threshold over drive cycle)
        - Indicates converter not storing oxygen (catalyst substrate degraded)

        VERIFY BEFORE REPLACING CONVERTER:
        1. Check for air leaks between upstream/downstream O2 (false air causes code)
        2. Test upstream O2 sensor function (must oscillate properly)
        3. Test downstream O2 sensor (may be faulty, reporting incorrect data)
        4. Check for oil/coolant consumption (contaminates catalyst)
        5. Verify no recent misfires (unburned fuel damages substrate)

        BACKPRESSURE TEST:
        - Remove upstream O2 sensor, install pressure gauge
        - Idle: <2 PSI | 2000 RPM: <3 PSI | Blocked cat: >6-8 PSI
        - Alternative: temperature test (upstream vs downstream should be 100°F+ hotter)

        FAILURE MODES:
        - Substrate melted/broken: Misfires, oil burning, coolant leak
        - Poisoning: Leaded fuel, silicone (RTV), phosphorus (oil)
        - Physical damage: Impact, road debris, rust-through
        - Aging: 150K+ miles, gradual efficiency loss
        """,
        key_factors=[
            "Mileage and age (cats degrade over time)",
            "Oil/coolant consumption history",
            "Recent misfire codes (P0300-P0312)",
            "Exhaust smell (rotten egg = sulfur, working cat)",
            "Upstream vs downstream O2 sensor correlation"
        ],
        primary_authority=[
            "EPA Mobile Source Emission Standards",
            "SAE J2008 (Oxygen Sensor Performance)",
            "California ARB catalyst certification"
        ],
        burden_holder="Technician to verify converter failure, not O2 sensor or air leak",
        adversary_position="P0420 = bad cat, replace immediately",
        counter_arguments=[
            "Downstream O2 sensor failure mimics bad converter",
            "Exhaust leak between sensors causes false P0420",
            "Recent engine repair (coolant leak, oil change) may clear on its own",
            "Aftermarket cats may not last as long as OEM",
            "Some converters can be cleaned (Cataclean additive, Italian tuneup)"
        ],
        resolution_strategy="Verify O2 sensors working, check for leaks, backpressure test, then replace cat if confirmed failed",
        entity_scope="All gasoline vehicles with catalytic converters (1975+ US)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Mass Airflow (MAF) Sensor Diagnosis",
        keywords=["MAF", "mass airflow", "air meter", "P0100", "P0101", "P0102", "hot wire"],
        conclusion_template=[
            "MAF sensor measures actual mass of air entering engine (grams/second) for precise fuel calculation",
            "Contaminated MAF causes: rough idle, stalling, poor acceleration, P0171/P0174 lean codes, P0100-P0104 MAF codes",
            "Clean with MAF-specific cleaner (NOT carb cleaner or brake cleaner, damages hot wire element)"
        ],
        reasoning_framework="""
        MAF Sensor Technology & Diagnosis:

        HOT-WIRE MAF (most common):
        - Heated wire (platinum, nichrome) in airstream
        - ECU maintains wire at constant temp (100-200°C above ambient)
        - Airflow cools wire, ECU increases current to maintain temp
        - Current draw = airflow mass (more flow = more cooling = more current)
        - Output: Voltage or frequency signal (0-5V typical, or 0-10kHz)

        HOT-FILM MAF (alternative):
        - Similar principle, heated film instead of wire
        - More robust, less contamination-sensitive

        COMMON FAILURES:
        1. Contamination: Oil (from over-oiled air filter), dirt, carbon
           - Deposits on hot wire change heat transfer
           - Causes under-reading (ECU thinks less air = lean condition)
           - Symptoms: P0171/P0174, hesitation, poor fuel economy

        2. Electrical fault: Broken wire, connector corrosion
           - P0100 (circuit malfunction), P0102 (low input), P0103 (high input)

        3. Air leak after MAF: Unmetered air enters
           - MAF reads correct, but actual air higher
           - Causes lean condition (P0171/P0174)

        DIAGNOSTIC TESTS:
        Scan Tool Data (live):
        - Idle: 2-7 g/s (4-cylinder), 4-10 g/s (V6), 6-12 g/s (V8)
        - 2000 RPM: 15-25 g/s (varies by displacement)
        - WOT: 150-300 g/s (depends on engine size, boost)
        - Compare to known-good values for same engine

        Voltage Test (key on, engine off):
        - Typical: 0.5-1.0V at rest (hot-wire MAF)
        - Should increase smoothly with airflow (blow on sensor)

        Resistance Test (MAF unplugged):
        - Hot-wire element: 2-6 ohms typical
        - Check OEM spec (varies by manufacturer)

        TAP TEST:
        - Engine running, tap MAF housing gently
        - RPM should not change (loose wire if RPM fluctuates)

        CLEANING PROCEDURE:
        - Remove MAF sensor
        - Spray MAF cleaner (CRC MAF Cleaner) on hot wire element
        - Let dry completely (alcohol evaporates quickly)
        - DO NOT touch element (skin oils contaminate)
        - DO NOT use compressed air (may damage wire)
        """,
        key_factors=[
            "Air filter condition (over-oiled K&N filters damage MAF)",
            "Intake air leaks after MAF sensor",
            "PCV system condition (oil vapor contaminates MAF)",
            "Fuel trim values (STFT/LTFT negative = MAF over-reading)",
            "Scan tool MAF g/s vs calculated load correlation"
        ],
        primary_authority=[
            "SAE J2008 (Air Flow Sensors)",
            "Bosch MAF sensor technical documentation",
            "OEM service manual MAF specifications"
        ],
        burden_holder="Technician to verify MAF fault vs intake leak or fuel system issue",
        adversary_position="P0171 lean code = bad O2 sensor",
        counter_arguments=[
            "P0171 (system lean) often caused by MAF under-reading or intake leak",
            "O2 sensor reports lean (correct), MAF is root cause (incorrect reading)",
            "Cleaning MAF may restore function (avoid replacement cost)",
            "Aftermarket MAF sensors often lower quality than OEM",
            "Intake leak after MAF causes lean without MAF code"
        ],
        resolution_strategy="Check MAF g/s data, clean sensor, smoke test for intake leaks, verify fuel trims",
        entity_scope="Vehicles with MAF-based engine management (vs MAP-based)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Turbocharger Diagnostics",
        keywords=["turbo", "turbocharger", "boost", "wastegate", "P0234", "P0299", "overboost", "underboost"],
        conclusion_template=[
            "Turbochargers use exhaust gas energy to compress intake air (boost pressure), increasing power density",
            "P0299 (turbo underboost) caused by: boost leak, wastegate stuck open, turbo oil seal failure, VGT actuator fault",
            "P0234 (turbo overboost) caused by: wastegate stuck closed, boost control solenoid failure, ECU overboost protection"
        ],
        reasoning_framework="""
        Turbocharger System Operation & Diagnosis:

        TURBO COMPONENTS:
        - Turbine side: Exhaust gases spin turbine wheel (600°F-1800°F)
        - Compressor side: Turbine shaft spins compressor wheel (pressurizes intake air)
        - Center bearing: Oil-cooled/lubricated (10K-20K RPM typical, up to 150K+ RPM)
        - Wastegate: Bypasses exhaust around turbine to control boost (prevents overboost)
        - Intercooler: Cools compressed air (denser charge = more power)

        WASTEGATE TYPES:
        Internal wastegate:
        - Valve inside turbine housing
        - Spring-loaded, vacuum/boost actuated
        - Common on factory turbos

        External wastegate:
        - Separate valve in exhaust manifold
        - More precise boost control
        - Common on aftermarket/performance turbos

        BOOST CONTROL:
        Mechanical (older):
        - Spring pressure sets max boost
        - Boost pressure overcomes spring, opens wastegate

        Electronic (modern):
        - ECU controls wastegate solenoid valve
        - Modulates vacuum/boost signal to wastegate actuator
        - Allows variable boost by RPM/load/gear

        VARIABLE GEOMETRY TURBO (VGT):
        - Movable vanes in turbine housing
        - Change effective A/R ratio (aspect ratio)
        - Low RPM: Vanes closed (high velocity, quick spool)
        - High RPM: Vanes open (high flow, prevent overboost)
        - Common on diesels, rare on gas engines (heat issues)

        DIAGNOSTIC TESTS:
        P0299 (Underboost) Diagnosis:
        1. Check boost pressure (scan tool PID or mechanical gauge)
           - Should hit target boost (varies: 5-25 PSI typical)
        2. Boost leak test: Pressurize intake (compressed air), listen/spray soapy water
           - Common leaks: intercooler piping, clamps, intake manifold gasket
        3. Wastegate inspection: Manually check actuator arm moves freely
           - Stuck open = no boost (exhaust bypasses turbine)
        4. Turbo shaft play: Push/pull compressor wheel
           - Radial play: <0.005" typical (excessive = bearing wear)
           - Axial play: <0.003" typical
        5. Compressor wheel damage: Look for blade damage (FOD = foreign object damage)
        6. Oil supply: Check oil feed line (clogged restrictor causes bearing failure)

        P0234 (Overboost) Diagnosis:
        1. Wastegate stuck closed: Check actuator arm, linkage binding
        2. Boost control solenoid: Test electrical operation (clicking, resistance)
        3. Vacuum/boost line routing: Verify correct hose connections
        4. ECU boost target: Check for tune/calibration issue (aftermarket ECU)

        TURBO FAILURE MODES:
        Bearing failure:
        - Symptoms: Loud whine, smoke (blue/white), oil consumption
        - Causes: Oil starvation, contamination, overspeed, coking
        - Prevention: Warm-up/cool-down, clean oil, avoid lugging

        Compressor surge:
        - Symptoms: Fluttering/chattering under throttle lift
        - Causes: Throttle closed with boost present
        - Prevention: Blow-off valve (BOV) or bypass valve (BPV)

        Shaft/wheel damage:
        - Symptoms: Grinding, vibration, loss of boost
        - Causes: FOD (debris ingestion), overspeed, imbalance
        """,
        key_factors=[
            "Boost pressure actual vs target (scan tool comparison)",
            "Wastegate actuator arm movement (manual check)",
            "Turbo shaft play (radial and axial)",
            "Oil condition and supply (clean oil, proper pressure)",
            "Intercooler piping integrity (boost leaks)"
        ],
        primary_authority=[
            "SAE J1826 (Turbocharger nomenclature)",
            "Garrett turbocharger technical bulletins",
            "BorgWarner turbo service manuals"
        ],
        burden_holder="Technician to isolate boost control vs turbo mechanical failure",
        adversary_position="Turbo spinning = turbo good",
        counter_arguments=[
            "Turbo may spin but not build boost (wastegate stuck open)",
            "Boost leak causes underboost without turbo failure",
            "Wastegate actuator can fail (stuck open/closed)",
            "Compressor wheel damage reduces efficiency (still spins)",
            "Oil seal failure causes smoke but turbo still works (temporarily)"
        ],
        resolution_strategy="Measure boost pressure, leak test system, inspect wastegate, check turbo shaft play",
        entity_scope="Turbocharged gasoline and diesel engines",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Variable Valve Timing (VVT) Systems",
        keywords=["VVT", "VTEC", "VVT-i", "VarioCam", "P0010", "P0011", "P0020", "P0021", "cam phaser"],
        conclusion_template=[
            "VVT adjusts camshaft timing relative to crankshaft for optimal performance/efficiency across RPM range",
            "P0010-P0014 codes indicate VVT actuator solenoid circuit faults; P0011/P0021 indicate over-advanced camshaft position",
            "Common VVT failures: oil sludge blocking solenoid, worn cam phaser, timing chain stretch, solenoid screen clogged"
        ],
        reasoning_framework="""
        Variable Valve Timing Systems:

        VVT PRINCIPLES:
        Why VVT?
        - Low RPM: Need high torque (retarded cam = better low-end)
        - High RPM: Need high HP (advanced cam = better breathing)
        - Fixed cam timing = compromise (good at one RPM range, poor elsewhere)
        - VVT = dynamic adjustment (optimize for all conditions)

        SYSTEM TYPES:
        1. Cam Phasing (most common):
           - Oil-actuated vane-type phaser on camshaft
           - ECU controls oil flow via solenoid valve
           - Advances or retards cam timing 15-60° (varies by system)
           - Examples: GM VVT, Ford Ti-VCT, Toyota VVT-i, Nissan CVTC

        2. VTEC (Honda):
           - Two cam lobe profiles (low-RPM and high-RPM)
           - Oil pressure activates locking pin at high RPM
           - Switches from mild cam to aggressive cam
           - Dramatic change at switchover (~5000-6000 RPM)

        3. VarioCam (Porsche):
           - Combines cam phasing + variable valve lift
           - Hydraulic chain tensioner adjusts cam position
           - More complex, higher cost

        4. Valvetronic (BMW):
           - Fully variable valve lift (no throttle plate)
           - Eccentric shaft adjusts rocker arm ratio
           - Extremely complex, expensive to repair

        COMMON VVT CODES:
        P0010, P0013: VVT solenoid circuit (Bank 1/2 intake)
        P0011, P0021: Camshaft position over-advanced (Bank 1/2 intake)
        P0012, P0022: Camshaft position over-retarded (Bank 1/2 intake)
        P0014, P0024: VVT solenoid circuit (Bank 1/2 exhaust)

        DIAGNOSIS:
        Over-Advanced (P0011/P0021):
        - Solenoid stuck open (oil continuously flows to phaser)
        - Cam phaser locked in advanced position
        - Timing chain stretched (cam appears advanced)

        Over-Retarded (P0012/P0022):
        - Solenoid stuck closed (no oil flow to phaser)
        - Oil pressure low (worn engine, diluted oil)
        - Cam phaser internal failure (vane stuck)

        Circuit Fault (P0010/P0013/P0014/P0024):
        - Solenoid wiring open/short
        - Solenoid coil failed (check resistance: typically 6-12 ohms)
        - ECU driver circuit failure

        TESTING PROCEDURE:
        1. Check oil level and condition:
           - VVT requires clean oil, proper viscosity
           - Sludge blocks solenoid passages
           - Low oil = insufficient pressure for phaser

        2. Test solenoid:
           - Resistance check (6-12 ohms typical)
           - Function test: Apply 12V, should click
           - Remove and inspect filter screen (often clogged)

        3. Check cam timing (scan tool):
           - Monitor camshaft position sensor (actual)
           - Compare to ECU target position
           - Should move smoothly when commanded

        4. Oil pressure test:
           - Minimum 15-20 PSI at idle (varies by engine)
           - Low pressure = phaser won't actuate

        5. Timing chain inspection:
           - Stretched chain causes incorrect cam timing
           - Check for codes + rattle on cold start

        FAILURE CAUSES:
        - Oil neglect: Sludge blocks solenoid, phaser passages
        - Wrong oil viscosity: Too thick (won't flow), too thin (leaks past phaser)
        - Timing chain wear: Appears as cam timing fault
        - Solenoid screen clogged: Restricts oil flow
        - Phaser internal failure: Vanes stuck, seals worn
        """,
        key_factors=[
            "Oil change interval compliance (VVT sensitive to oil quality)",
            "Oil viscosity specification (wrong weight causes VVT issues)",
            "Timing chain condition (stretch mimics VVT fault)",
            "Cam/crank sensor correlation (timing verification)",
            "Solenoid screen condition (remove and inspect)"
        ],
        primary_authority=[
            "SAE J1979 Mode 6 VVT tests",
            "OEM service bulletins (GM, Ford, Toyota VVT TSBs)",
            "ASE A8 Engine Performance certification"
        ],
        burden_holder="Technician to verify VVT fault vs oil quality or timing chain issue",
        adversary_position="P0011 code = replace VVT solenoid",
        counter_arguments=[
            "Over-advanced code may be timing chain stretch, not solenoid",
            "Clogged solenoid screen causes fault (clean vs replace)",
            "Low oil pressure prevents VVT operation (not solenoid fault)",
            "Sludged engine needs flush + oil changes before VVT parts",
            "Some phasers can be cleaned/rebuilt (avoid full replacement)"
        ],
        resolution_strategy="Check oil first, test solenoid, verify timing chain condition, replace phaser if confirmed failed",
        entity_scope="Engines with variable valve timing (1990s+ common)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Diesel Engine Diagnostics",
        keywords=["diesel", "compression ignition", "glow plug", "DPF", "DEF", "SCR", "EGR cooler"],
        conclusion_template=[
            "Diesel engines use compression ignition (no spark plugs), glow plugs for cold-start assist only",
            "Modern diesels require DPF (diesel particulate filter) regeneration and DEF (diesel exhaust fluid) for SCR (NOx reduction)",
            "Common diesel failures: glow plug failure (hard cold start), injector imbalance (smoke, rough idle), DPF clogged (regen cycle), EGR cooler leak"
        ],
        reasoning_framework="""
        Diesel Engine Diagnostics:

        DIESEL VS GASOLINE:
        - Compression ratio: 14:1-25:1 (diesel) vs 8:1-12:1 (gasoline)
        - Ignition: Compression heat (diesel) vs spark plug (gasoline)
        - Fuel injection: High pressure (15,000-30,000 PSI diesel) vs low pressure (gasoline port) or 2000 PSI (GDI)
        - Air intake: Unthrottled (diesel) vs throttled (gasoline)

        GLOW PLUG SYSTEM:
        Purpose: Pre-heat combustion chamber for cold starting
        - Not used for running (diesel compression creates ignition heat)
        - Glow time: 5-30 seconds depending on temp
        - Types: Conventional (1V drop), rapid-heat (4-6V drop)

        Glow Plug Diagnosis:
        - Hard cold start (hot start OK) = bad glow plugs
        - White smoke on cold start = incomplete combustion (glow plug issue)
        - Test: Measure resistance (0.5-2 ohms typical, check spec)
        - Test: Current draw (15-20A per plug typical)

        DIESEL FUEL INJECTION:
        Common Rail (modern):
        - High-pressure pump (15,000-30,000 PSI)
        - Rail stores fuel at constant high pressure
        - Injectors electronically controlled (piezo or solenoid)
        - Multiple injection events per cycle (pilot, main, post)

        Rotary Pump (older):
        - Bosch VE pump, mechanical distribution
        - Lower pressure (2000-5000 PSI)
        - Timing advance mechanical (weights/springs)

        Injector Failures:
        - Leaking injector: Diesel in oil (dilution), hard start
        - Clogged injector: Power loss, smoke, rough idle
        - Imbalance: Contribution test (cylinder cut-out) shows weak cylinder

        DIESEL EMISSIONS SYSTEMS:
        DPF (Diesel Particulate Filter):
        - Traps soot (PM) from exhaust
        - Requires regeneration (burn off soot)
        - Passive regen: High exhaust temp (highway driving)
        - Active regen: ECU injects fuel, raises temp to 1100°F
        - Ash accumulation: Non-burnable residue (oil ash)

        DPF Issues:
        - Clogged DPF: Loss of power, poor fuel economy, regen cycles
        - Failed regen: Check for codes, verify exhaust temp sensor
        - Cracked substrate: Regen overtemp, thermal shock

        SCR (Selective Catalytic Reduction):
        - Injects DEF (diesel exhaust fluid, 32.5% urea solution) into exhaust
        - NOx + DEF → N2 + H2O (reduces NOx emissions)
        - DEF tank, pump, injector, heater (prevents freezing)

        SCR Issues:
        - Low DEF level: Engine derate (reduced power)
        - DEF quality: Contaminated DEF (coolant, diesel) damages system
        - DEF crystallization: Heater failure, injector clogged
        - NOx sensor fault: P20E8, P20EE codes

        EGR (Exhaust Gas Recirculation):
        - Diesel EGR recirculates 10-30% exhaust (lowers NOx)
        - EGR cooler: Cools exhaust before intake (coolant-cooled)

        EGR Issues:
        - Clogged EGR valve: Carbon buildup, sticking
        - EGR cooler failure: Leak (exhaust to coolant or vice versa)
           Symptoms: Coolant loss, white smoke, overheating
        - EGR delete (illegal): Removes EGR, emissions non-compliant

        DIESEL DIAGNOSTIC TESTS:
        Compression Test:
        - Diesel requires high compression (350-450 PSI typical)
        - Worn rings/valves cause low compression = hard start, smoke

        Cylinder Contribution Test:
        - Disable injector one at a time (scan tool)
        - Measure RPM drop (weak cylinder has less drop)
        - Identifies injector imbalance

        Fuel Pressure Test:
        - Low-pressure side: 10-15 PSI (lift pump)
        - High-pressure side: 15,000-30,000 PSI (common rail)
        - Low pressure = hard start, power loss

        Smoke Analysis:
        - Black smoke: Too much fuel (overfueling, boost leak)
        - White smoke: Unburned fuel (low compression, bad injector, glow plug)
        - Blue smoke: Oil burning (rings, turbo seal)
        """,
        key_factors=[
            "Glow plug condition (cold start performance)",
            "Fuel quality (diesel contamination, water)",
            "DPF regen cycle completion (passive vs active)",
            "DEF level and quality (SCR operation)",
            "EGR system condition (carbon buildup, cooler integrity)"
        ],
        primary_authority=[
            "SAE J1979 OBD-II for diesel",
            "Bosch diesel fuel injection systems",
            "EPA Tier 3/4 diesel emission standards"
        ],
        burden_holder="Technician to diagnose diesel-specific failures (glow plug, DPF, DEF, EGR)",
        adversary_position="Diesel same as gas, just different fuel",
        counter_arguments=[
            "Diesel compression ignition (no spark plugs)",
            "Diesel fuel pressure 10x higher than gasoline",
            "DPF and SCR systems unique to diesel (complex emissions)",
            "Glow plugs required for cold start (not continuous operation)",
            "Diesel fuel contamination (water, algae) more critical"
        ],
        resolution_strategy="Verify glow plug operation, test fuel pressure, monitor DPF regen, check DEF quality, inspect EGR system",
        entity_scope="Compression-ignition diesel engines",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Engine Cooling System Diagnostics",
        keywords=["cooling", "overheating", "thermostat", "water pump", "radiator", "head gasket"],
        conclusion_template=[
            "Cooling system failures cause overheating: thermostat stuck (closed = overheat, open = never warms up), water pump failure (no coolant flow), head gasket leak (combustion gases in coolant)",
            "Head gasket failure symptoms: White smoke (coolant burning), coolant loss (no external leak), bubbles in radiator, oil milky (coolant mixing)",
            "Cooling system requires periodic maintenance: flush every 50K miles, pressure test annually, replace coolant per spec (not just water)"
        ],
        reasoning_framework="""
        Cooling System Operation & Diagnosis:

        SYSTEM COMPONENTS:
        - Radiator: Heat exchanger (coolant to air)
        - Water pump: Circulates coolant (belt or timing chain driven)
        - Thermostat: Controls coolant flow (closed until engine warm)
        - Coolant: 50/50 mix (ethylene glycol + water, anti-freeze + anti-boil)
        - Expansion tank/overflow: Accommodates thermal expansion
        - Heater core: Cabin heat (mini radiator inside dash)

        THERMOSTAT OPERATION:
        Closed (cold engine):
        - Blocks coolant flow to radiator
        - Coolant circulates through engine block only
        - Engine warms up quickly

        Open (hot engine):
        - Opens at rated temp (180-195°F typical)
        - Coolant flows to radiator for cooling
        - Maintains operating temp

        Thermostat Failures:
        - Stuck closed: Overheating (no coolant to radiator)
        - Stuck open: Never warms up (poor heater, high emissions, reduced efficiency)
        - Test: Feel upper radiator hose (should warm up after thermostat opens)

        WATER PUMP DIAGNOSIS:
        Function: Belt or chain-driven impeller circulates coolant
        - Flow rate: 5-10 GPM typical (varies by engine size)

        Water Pump Failures:
        - Bearing failure: Noise (grinding, whirring), wobble, leaking seal
        - Impeller erosion/corrosion: Reduced flow, overheating
        - Seal leak: Coolant drips from weep hole (normal small seepage OK)

        Tests:
        - Visual: Check for leaks, bearing play (wiggle pulley)
        - Squeeze upper radiator hose (engine running): Should feel pressure pulses
        - Temperature differential: Inlet vs outlet radiator hose temp difference

        HEAD GASKET FAILURE:
        Gasket seals: Combustion chamber, coolant passages, oil passages

        Failure Modes:
        1. Combustion to coolant:
           - Exhaust gases enter cooling system
           - Symptoms: Bubbles in radiator, pressurized overflow tank
           - Test: Block test (chemical turns yellow if combustion gases present)

        2. Coolant to combustion:
           - Coolant burns in cylinder
           - Symptoms: White smoke, coolant loss (no external leak), rough idle
           - Test: Compression test (coolant in cylinder = low compression)

        3. Coolant to oil:
           - Coolant mixes with oil
           - Symptoms: Milky oil (chocolate milk appearance), oil level rises
           - Test: Oil analysis (coolant contamination)

        4. External leak:
           - Coolant leaks externally
           - Symptoms: Coolant puddle, overheating, white smoke on startup

        HEAD GASKET TESTS:
        Block test (chemical):
        - Blue fluid turns yellow if combustion gases in coolant
        - Most reliable test (HC detection)

        Compression test:
        - Low compression in adjacent cylinders = head gasket
        - Add coolant to cylinder, re-test: compression rises = gasket leak

        Leak-down test:
        - Pressurize cylinder, listen for air escaping
        - Bubbles in radiator = head gasket leak

        Cylinder leak-down test:
        - Pressurize cooling system (pressure tester)
        - System should hold 15 PSI (small drop OK)
        - Rapid pressure loss = leak (external, head gasket, or cracked head/block)

        OVERHEATING DIAGNOSIS:
        Immediate overheat:
        - Thermostat stuck closed
        - Water pump failure
        - Coolant level low (air pocket)
        - Radiator cap failure (won't hold pressure)

        Gradual overheat:
        - Clogged radiator (external: bugs/dirt, internal: scale/rust)
        - Radiator fan failure (electric fan not running)
        - Head gasket leak (combustion gases pressurize system)
        - Restricted coolant flow (clogged heater core, hoses)

        COOLANT SPECIFICATIONS:
        Types:
        - Green (traditional): Ethylene glycol, silicate additives
        - Orange (Dex-Cool): OAT (organic acid technology), long-life
        - Pink/Red (Asian): Hybrid organic acid technology (HOAT)
        - DO NOT MIX: Different types react, form sludge

        Concentration:
        - 50/50 mix: -34°F freeze, 265°F boil (with pressure cap)
        - Too much antifreeze: Reduced heat transfer (worse cooling)
        - Too much water: Freezing risk, corrosion, lower boiling point
        """,
        key_factors=[
            "Coolant level and condition (50/50 mix, no contamination)",
            "Thermostat opening temperature (test in boiling water)",
            "Water pump operation (check for leaks, bearing noise)",
            "Radiator cap pressure rating (typically 13-16 PSI)",
            "Head gasket integrity (block test, compression test)"
        ],
        primary_authority=[
            "SAE J814 (Engine Coolant Concentrate)",
            "ASTM D3306 (Ethylene glycol coolant)",
            "OEM cooling system service procedures"
        ],
        burden_holder="Technician to isolate cooling system fault (thermostat, pump, gasket, radiator)",
        adversary_position="Overheating = bad thermostat, replace it",
        counter_arguments=[
            "Overheating can be water pump, radiator, fan, or head gasket",
            "Thermostat stuck open causes poor warm-up, not overheating",
            "Head gasket failure mimics other cooling issues (bubbles, loss)",
            "Clogged radiator (internal corrosion) common on neglected systems",
            "Radiator cap failure prevents proper pressurization (lower boiling point)"
        ],
        resolution_strategy="Check coolant level, pressure test system, verify thermostat/pump operation, block test for head gasket",
        entity_scope="All liquid-cooled internal combustion engines",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Hybrid Vehicle Powertrain Basics",
        keywords=["hybrid", "HEV", "PHEV", "electric motor", "regenerative braking", "traction battery", "P0A80"],
        conclusion_template=[
            "Hybrid vehicles combine gasoline engine + electric motor for improved efficiency (30-50% better MPG than conventional)",
            "Types: Parallel hybrid (engine + motor both drive wheels), series hybrid (engine charges battery, motor drives wheels), series-parallel (combination)",
            "High-voltage system (200-300V typical) requires special training and PPE (insulated gloves, voltage detector) for service"
        ],
        reasoning_framework="""
        Hybrid Electric Vehicle (HEV) Diagnostics:

        HYBRID ARCHITECTURES:
        1. Parallel Hybrid (Honda IMA, Hyundai Hybrid):
           - Engine and motor both mechanically coupled to transmission
           - Motor assists engine (electric boost)
           - Smaller motor, smaller battery
           - Simpler, lower cost

        2. Series Hybrid (Chevy Volt, BMW i3 REX):
           - Engine powers generator (not mechanically connected to wheels)
           - Electric motor drives wheels exclusively
           - Acts as EV with range extender
           - Larger motor, larger battery

        3. Series-Parallel Hybrid (Toyota Prius, Ford Fusion Hybrid):
           - Power-split device (planetary gearset)
           - Engine can drive wheels OR charge battery (or both)
           - Two motor/generators (MG1 for starting/charging, MG2 for propulsion)
           - Most complex, most efficient

        HIGH-VOLTAGE SYSTEM:
        Components:
        - Traction battery: NiMH (older) or Li-ion (newer), 200-300V nominal
        - Inverter: Converts DC (battery) to AC (motor)
        - Motor/generator: Permanent magnet synchronous motor (PMSM) or AC induction
        - DC/DC converter: Steps down HV to 12V for accessories
        - High-voltage cables: Orange color-coded

        SAFETY PROCEDURES:
        CRITICAL: High voltage can KILL. Follow safety protocol:
        1. Disconnect 12V battery (disables HV contactors)
        2. Remove service plug (disconnects HV battery from system)
        3. Wait 5-10 minutes (capacitors discharge)
        4. Verify zero voltage (HV voltage detector, not multimeter)
        5. Wear PPE: Class 0 insulated gloves (1000V rating), safety glasses

        COMMON HV CODES:
        P0A80: Hybrid battery pack replaced
        P0A7F: Hybrid battery pack deterioration
        P3000-P3004: Battery module faults
        P0A1F: Electric motor/generator communication error
        P0AA6: Hybrid battery positive contactor stuck

        TRACTION BATTERY DIAGNOSIS:
        Battery Management System (BMS):
        - Monitors individual cell voltages
        - Balances charge across modules
        - Thermal management (cooling fan, liquid cooling)

        Battery Health Indicators:
        - State of Charge (SOC): 20-80% typical (avoid full charge/discharge)
        - State of Health (SOH): Capacity vs new (80%+ = good, <70% = replacement)
        - Cell voltage balance: All cells within 0.05V (imbalance = weak cell/module)
        - Internal resistance: Increases with age (high resistance = reduced power)

        Battery Failure Modes:
        - Module failure: Single module (multiple cells in series) fails
           Symptoms: P3000-P3004 codes, reduced power, battery light
        - Thermal management failure: Cooling fan/pump failure
           Symptoms: Overheating, reduced battery capacity
        - Contactor failure: HV relay stuck open/closed
           Symptoms: No HV, P0AA6 code, no EV mode

        REGENERATIVE BRAKING:
        Operation:
        - Motor acts as generator during deceleration
        - Converts kinetic energy to electrical (charges battery)
        - Blends with friction brakes (seamless transition)

        Diagnosis:
        - Poor regen: Battery fully charged (nowhere to store energy)
        - No regen: Motor/inverter fault, brake system fault
        - Harsh transition: Brake actuator/accumulator issue

        12V BATTERY ISSUES:
        Unique to Hybrid:
        - 12V battery charged by DC/DC converter (not alternator)
        - Weak 12V battery prevents HV system activation
        - Symptoms: No start (HV contactors won't close), dash warnings
        - Common failure: 12V battery weak (4-5 years typical lifespan)

        HYBRID-SPECIFIC DIAGNOSTICS:
        Scan Tool Data:
        - HV battery voltage, current, temperature
        - Individual module voltages
        - Motor/generator RPM, torque request
        - Inverter temperature
        - SOC, SOH

        Health Check:
        - Dr. Prius app (Toyota/Lexus): Cell voltage monitoring
        - FORScan (Ford): Hybrid system status
        - Torque Pro + HybridReporter plugin: Generic HV monitoring

        MAINTENANCE DIFFERENCES:
        - Engine oil changes: Less frequent (engine runs less)
        - Brake pads: Last longer (regen braking reduces friction brake use)
        - Transaxle fluid: Hybrid-specific ATF (do not substitute)
        - Coolant: Two systems (engine coolant + inverter coolant)
        - Cabin air filter: Critical (battery cooling air path)
        """,
        key_factors=[
            "High-voltage safety procedures (service plug, PPE)",
            "Battery state of health (SOH percentage)",
            "Cell voltage balance (weak module detection)",
            "12V battery condition (enables HV system)",
            "Inverter and motor temperature (thermal management)"
        ],
        primary_authority=[
            "SAE J1772 (EV/HEV charging standard)",
            "SAE J2344 (HEV safety guidelines)",
            "OEM hybrid service training (manufacturer-specific)"
        ],
        burden_holder="Certified hybrid technician (high-voltage trained)",
        adversary_position="Hybrid = regular car with battery",
        counter_arguments=[
            "High-voltage system (200-300V) lethal if contacted",
            "Special PPE and procedures required (not standard automotive)",
            "Traction battery failure expensive ($2K-$6K replacement)",
            "Complex diagnostics (requires hybrid scan tool)",
            "12V battery critical (weak 12V prevents HV operation)"
        ],
        resolution_strategy="Follow HV safety protocol, verify 12V battery, scan HV system codes, check battery SOH/balance",
        entity_scope="Hybrid electric vehicles (HEV, PHEV)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="No-Start Diagnosis Decision Tree",
        keywords=["no start", "crank no start", "no crank", "starter", "fuel", "spark", "compression"],
        conclusion_template=[
            "No-start diagnosis follows decision tree: Crank? (yes = fuel/spark/compression, no = starter/battery/immobilizer)",
            "Crank-no-start: Verify fuel pressure, spark, compression, and timing (any missing = no start)",
            "No-crank: Check battery voltage (>12.4V), starter current draw (<200A), and security system (immobilizer active)"
        ],
        reasoning_framework="""
        No-Start Diagnostic Decision Tree:

        LEVEL 1: DOES ENGINE CRANK?

        NO CRANK:
        1. Battery Test:
           - Voltage: >12.4V resting, >9.6V cranking
           - Load test: 1/2 CCA for 15 sec, >9.6V = good
           - Hydrometer: All cells 1.265+ = good

        2. Starter System:
           - Starter current draw: 80-200A typical (>300A = bad starter)
           - Voltage drop test: <0.5V drop on positive side, <0.3V on ground
           - Solenoid click: Yes = starter bad, No = solenoid/wiring bad

        3. Security System:
           - Immobilizer active: Theft light flashing = key not recognized
           - Passlock/VATS: Relearn procedure required
           - Aftermarket alarm: May prevent crank signal

        4. Neutral Safety Switch (automatic):
           - Test: Shift to neutral and retry (park switch may be faulty)
           - Bypass: Jumper switch to verify fault

        5. Clutch Switch (manual):
           - Test: Clutch pedal position switch
           - Bypass: Jumper switch to verify fault

        CRANK-NO-START (engine turns but doesn't fire):
        Need: Fuel, Spark, Compression, Timing (all four)

        1. FUEL TEST:
           - Fuel pressure: 30-60 PSI (port injection), 2000+ PSI (GDI), 5-15 PSI (carb)
           - Fuel volume: >1 pint in 30 seconds
           - Injector pulse: Noid light or scan tool (should pulse during crank)
           - Fuel quality: Check for contamination (water, wrong fuel)

        2. SPARK TEST:
           - Remove spark plug, ground to engine, crank (should see blue spark)
           - Spark tester: Adjustable gap (30kV minimum)
           - Timing light: Verify spark occurring at correct time
           - Coil test: Primary resistance (0.5-2 ohms), secondary (6K-15K ohms)

        3. COMPRESSION TEST:
           - Minimum: 100 PSI (will run poorly), 120+ PSI (acceptable), 150+ PSI (good)
           - Variation: Within 10% cylinder-to-cylinder
           - Wet test: Add oil to cylinder, re-test (compression rises = rings, same = valves)

        4. TIMING VERIFICATION:
           - Timing mark alignment: TDC mark on harmonic balancer vs pointer
           - Timing chain/belt: Cam position sensor vs crank sensor (should correlate)
           - Jumped timing: Engine cranks faster than normal (valves not opening)
           - Broken timing belt: Engine cranks very fast (no compression, valves not moving)

        QUICK TESTS:
        Starter Fluid Test:
        - Spray starter fluid (ether) into intake
        - Engine fires briefly = fuel problem
        - No change = spark, compression, or timing problem

        Fuel Pump Relay Jumper:
        - Bypass fuel pump relay (supply 12V directly to pump)
        - Fuel pump runs = relay bad
        - No run = pump bad or wiring issue

        COMMON NO-START CAUSES:
        Fuel-related:
        - Fuel pump failure (listen for hum in tank when key on)
        - Clogged fuel filter
        - Bad fuel pressure regulator (pressure too low/high)
        - No injector pulse (ECU, wiring, crank sensor)

        Spark-related:
        - Ignition coil failure (no spark)
        - Crank position sensor (ECU doesn't know when to fire)
        - Cam position sensor (sequential injection systems)
        - Ignition module failure
        - Distributor cap/rotor (older vehicles)

        Compression-related:
        - Broken timing belt (interference engine = bent valves)
        - Jumped timing chain (worn guides, tensioner)
        - Blown head gasket (low compression multiple cylinders)
        - Severely worn rings (low compression all cylinders)

        INTERMITTENT NO-START:
        Heat-soak no-start:
        - Engine starts cold, won't restart hot
        - Common: Ignition coil thermal failure, fuel vapor lock

        Cold no-start:
        - Engine won't start cold, starts fine hot
        - Common: Coolant temp sensor, enrichment system, glow plugs (diesel)

        Random no-start:
        - Sometimes starts, sometimes doesn't
        - Common: Crank sensor intermittent, fuel pump relay, loose connection
        """,
        key_factors=[
            "Engine cranks or not (narrows to starter system vs fuel/spark/compression)",
            "Fuel pressure present during crank (pump working, injectors pulsing)",
            "Spark present at plugs (coil function, timing signal)",
            "Compression adequate (120+ PSI minimum)",
            "Timing correct (cam/crank correlation, timing marks aligned)"
        ],
        primary_authority=[
            "ASE A8 Engine Performance Specialist",
            "SAE J1930 (Diagnostic terminology)",
            "OEM service manual no-start flowcharts"
        ],
        burden_holder="Technician to systematically verify fuel, spark, compression, timing",
        adversary_position="No start = bad starter (assumption without testing)",
        counter_arguments=[
            "No-crank vs crank-no-start are different diagnostic paths",
            "Crank-no-start requires fuel AND spark AND compression AND timing",
            "Starter may be fine (battery, security, neutral switch)",
            "Fuel pressure good doesn't mean injectors pulsing",
            "Spark at coil doesn't mean spark at plug (bad wires, distributor)"
        ],
        resolution_strategy="Follow decision tree: crank? → fuel/spark/compression/timing tests → isolate failed component",
        entity_scope="All internal combustion engines",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
]

# Add 15 more doctrine blocks to reach 25+ total
DOCTRINE_CACHE.extend([
    DoctrineBlock(
        topic="Oxygen Sensor Operation and Diagnosis",
        keywords=["O2 sensor", "lambda sensor", "P0130", "P0134", "P0171", "fuel trim"],
        conclusion_template=[
            "O2 sensors report air/fuel ratio to ECU for closed-loop fuel control (target 14.7:1 stoichiometric)",
            "Narrow-band O2 switches 0.1-0.9V (lean-rich), wide-band reports exact A/F ratio (used in performance tuning)",
            "Failed O2 causes: P0130-P0167 codes, poor fuel economy, failed emissions, rough idle"
        ],
        reasoning_framework="""
        Oxygen Sensor Technology:

        NARROW-BAND O2 (standard):
        - Zirconia element (generates voltage based on O2 differential)
        - Lean exhaust (excess O2): Low voltage (0.1-0.3V)
        - Rich exhaust (low O2): High voltage (0.7-0.9V)
        - Stoichiometric (14.7:1): 0.45V
        - Switches rapidly in closed loop (1-2 Hz)

        WIDE-BAND O2 (AFR sensor):
        - Planar zirconia with pump cell
        - Reports exact A/F ratio (not just lean/rich)
        - Output: Linear voltage or current
        - Used: Upstream (Bank 1/2 Sensor 1) on modern vehicles

        HEATED O2 SENSOR:
        - Internal heater element (reaches operating temp faster)
        - Typical: 400°C (750°F) operating temp
        - Heater resistance: 5-20 ohms
        - Allows closed-loop operation sooner after start

        FUEL TRIM OPERATION:
        Short-Term Fuel Trim (STFT):
        - Immediate adjustment based on O2 sensor
        - Range: -10% to +10% (0% = perfect)
        - Negative = ECU reducing fuel (O2 reads rich)
        - Positive = ECU adding fuel (O2 reads lean)

        Long-Term Fuel Trim (LTFT):
        - Learned adjustment over time
        - Compensates for wear, deposits, altitude
        - Range: -20% to +20% typically
        - High LTFT = underlying problem (intake leak, MAF fault, injector issue)

        DIAGNOSTIC CODES:
        P0130-P0167: O2 sensor circuit faults
        P0171, P0174: System lean (Bank 1/2)
        P0172, P0175: System rich (Bank 1/2)

        O2 SENSOR TESTING:
        Scan Tool (live data):
        - Voltage should oscillate 0.1-0.9V (1-2 Hz)
        - Snap throttle: Should go rich (>0.7V) then recover
        - Propane enrichment: Voltage should go high (>0.8V)
        - Vacuum leak: Voltage should stay low (<0.3V)

        Response Time Test:
        - Create rich condition (propane in intake)
        - Measure time to switch lean→rich (<100ms good)
        - Slow response = aged sensor (lazy)

        Heater Circuit Test:
        - Resistance: 5-20 ohms typical (check spec)
        - Current draw: 0.5-1.5A typical
        - Voltage supply: Battery voltage when running
        """,
        key_factors=[
            "O2 sensor switching frequency (1-2 Hz = healthy)",
            "Fuel trim values (STFT + LTFT within ±10% = good)",
            "Heater circuit operation (sensor reaches temp)",
            "Sensor age and mileage (replace every 100K miles)",
            "Exhaust leaks before sensor (false lean reading)"
        ],
        primary_authority=["SAE J2008", "Bosch O2 sensor documentation"],
        burden_holder="Technician to verify O2 sensor fault vs intake leak or MAF issue",
        adversary_position="P0171 lean code = bad O2 sensor",
        counter_arguments=[
            "Lean code often caused by intake leak or MAF, not O2 sensor",
            "O2 sensor reports lean (correct), root cause elsewhere",
            "Fuel trims reveal whether ECU compensating (leak) or sensor bad"
        ],
        resolution_strategy="Check fuel trims, smoke test for leaks, verify MAF data, test O2 response",
        entity_scope="All gasoline engines with O2 sensors",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="EGR System Diagnosis",
        keywords=["EGR", "exhaust gas recirculation", "P0400", "P0401", "carbon buildup"],
        conclusion_template=[
            "EGR recirculates exhaust into intake to lower NOx emissions (reduces combustion temp)",
            "P0400-P0409 codes indicate EGR flow issues (insufficient, excessive, or no flow)",
            "Common failures: carbon buildup (valve stuck), EGR valve diaphragm, vacuum leak, electrical fault"
        ],
        reasoning_framework="""
        EGR System Operation:

        PURPOSE:
        - Recirculate 5-15% exhaust gas into intake
        - Inert gas (CO2, N2) lowers combustion temp
        - Lower temp = less NOx formation

        EGR VALVE TYPES:
        Vacuum-operated (older):
        - Vacuum diaphragm opens valve
        - Ported vacuum or EGR solenoid controlled

        Electronic (modern):
        - Stepper motor or duty-cycle solenoid
        - ECU controls position (closed at idle/WOT, open cruise)

        COMMON CODES:
        P0400: EGR flow malfunction
        P0401: EGR flow insufficient
        P0402: EGR flow excessive
        P0403-P0409: EGR circuit faults

        DIAGNOSIS:
        EGR valve inspection:
        - Remove and inspect for carbon buildup
        - Valve should move freely (stuck = carbon)

        Vacuum test (vacuum EGR):
        - Apply vacuum to EGR valve (engine idling)
        - Engine should stumble/stall (exhaust entering intake)
        - No change = valve stuck closed or passages blocked

        Scan tool command (electronic EGR):
        - Command EGR open (idle)
        - Monitor MAP sensor (should decrease = EGR flow)
        - RPM should drop (diluting intake charge)

        Backpressure test:
        - Install pressure gauge in EGR passage
        - Should see exhaust pulses (flow path open)
        - No pressure = clogged passages
        """,
        key_factors=[
            "EGR valve movement (stuck from carbon)",
            "Intake manifold EGR passages (carbon clogged)",
            "DPFE sensor accuracy (measures EGR flow)",
            "Vacuum supply (vacuum-operated EGR)",
            "Electrical circuit (electronic EGR)"
        ],
        primary_authority=["SAE emissions standards", "OEM EGR service procedures"],
        burden_holder="Technician to verify EGR flow issue vs sensor/circuit fault",
        adversary_position="P0401 = replace EGR valve",
        counter_arguments=[
            "Clogged passages cause code (valve may be fine)",
            "DPFE sensor failure mimics EGR flow fault",
            "Carbon cleaning may restore function (avoid replacement)"
        ],
        resolution_strategy="Inspect valve, test flow (vacuum or scan tool), clean passages, verify sensor operation",
        entity_scope="Gasoline engines with EGR (1970s+)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="EVAP System Diagnosis",
        keywords=["EVAP", "evaporative emissions", "P0440", "P0442", "P0455", "purge valve", "charcoal canister"],
        conclusion_template=[
            "EVAP system captures fuel vapors from tank/carburetor, stores in charcoal canister, purges to intake during operation",
            "P0440-P0457 codes indicate EVAP leaks or purge flow issues (large leak P0455, small leak P0442)",
            "Common failures: loose/missing gas cap (P0457), purge valve stuck, vent valve failure, cracked hoses"
        ],
        reasoning_framework="""
        EVAP System Components:
        - Fuel tank with rollover valve
        - Charcoal canister (stores fuel vapors)
        - Purge valve: ECU-controlled, opens to purge vapors into intake
        - Vent valve: Normally open, closes during leak test
        - Fuel tank pressure sensor: Monitors vacuum/pressure
        - Gas cap: Seals system

        OPERATION:
        Engine off:
        - Vapors collect in canister
        - Vent valve open (vents to atmosphere through canister)

        Engine running:
        - ECU opens purge valve (controlled duty cycle)
        - Intake vacuum draws vapors from canister
        - Fresh air enters through vent valve (purges canister)

        Leak Test:
        - ECU closes vent valve, opens purge valve
        - Creates vacuum in system (MAP sensor pulls air out)
        - Monitors fuel tank pressure sensor
        - Leak present: vacuum decays (P0442 small, P0455 large)

        COMMON CODES:
        P0440: EVAP system malfunction
        P0442: Small leak detected
        P0455: Large leak detected
        P0457: Loose/missing gas cap

        DIAGNOSIS:
        Gas cap test:
        - Inspect cap seal (cracked, missing)
        - Tighten cap, clear code, drive cycle

        Smoke test:
        - Introduce smoke into EVAP system
        - Locate leak (hoses, canister, tank)

        Purge valve test:
        - Remove valve, blow through (should be closed key off)
        - Apply 12V (should open, allow airflow)
        - Check duty cycle scan tool (0-100%)

        Vent valve test:
        - Normally open (check with vacuum/pressure)
        - Should close when commanded (scan tool)
        """,
        key_factors=[
            "Gas cap condition (most common leak source)",
            "Purge valve operation (stuck open/closed)",
            "Vent valve function (normally open, closes for test)",
            "Hose integrity (cracked, disconnected)",
            "Canister condition (saturated, damaged)"
        ],
        primary_authority=["EPA Tier 2/3 emission standards", "SAE J1979 EVAP test modes"],
        burden_holder="Technician to locate leak (gas cap to fuel tank)",
        adversary_position="EVAP code = replace purge valve",
        counter_arguments=[
            "70% of EVAP codes = loose gas cap (free fix)",
            "Smoke test identifies exact leak location",
            "Purge valve may be fine (leak elsewhere in system)"
        ],
        resolution_strategy="Check gas cap first, smoke test system, test purge/vent valves, inspect hoses",
        entity_scope="All gasoline vehicles (1996+ US OBD-II)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Crankshaft and Camshaft Position Sensors",
        keywords=["crank sensor", "cam sensor", "CKP", "CMP", "P0335", "P0340", "no start", "Hall effect"],
        conclusion_template=[
            "Crank position sensor tells ECU engine speed and TDC position (essential for fuel injection timing and spark)",
            "Cam position sensor identifies which cylinder is on compression stroke (allows sequential fuel injection)",
            "Failed crank sensor = no start (no signal = ECU won't fire injectors/coils); failed cam sensor = starts but rough (batch fire mode)"
        ],
        reasoning_framework="""
        Position Sensor Technology:

        CRANK POSITION SENSOR (CKP):
        Function:
        - Monitors crankshaft rotation (RPM)
        - Identifies piston position (TDC)
        - Required for fuel injection and ignition timing

        Types:
        - Hall-effect: 5V or 12V square wave signal
        - Inductive (magnetic): AC voltage signal (amplitude increases with RPM)
        - Optical (rare): LED/photodiode in distributor

        Trigger wheel:
        - Reluctor wheel with teeth (36-1, 60-2 common)
        - Missing tooth = TDC reference
        - ECU counts teeth to determine crank angle

        CAMSHAFT POSITION SENSOR (CMP):
        Function:
        - Identifies which cylinder (cylinder 1 cam lobe)
        - Allows sequential fuel injection (each injector fires individually)
        - Allows sequential ignition (coil-on-plug timing)

        Correlation:
        - ECU compares crank and cam signals
        - Verifies valve timing correct
        - P0016-P0019: Cam/crank correlation fault (timing chain jumped)

        COMMON CODES:
        P0335: Crank position sensor circuit
        P0336: Crank position sensor range/performance
        P0340: Cam position sensor circuit
        P0341: Cam position sensor range/performance
        P0016-P0019: Cam/crank correlation fault

        DIAGNOSIS:
        No-start (crank sensor):
        - Scan tool: No RPM signal while cranking = bad crank sensor
        - Voltage test: Sensor output should pulse (AC or square wave)
        - Resistance test (inductive): 500-1500 ohms typical
        - Air gap: 0.020-0.050" typical (too large = weak signal)

        Rough idle (cam sensor):
        - Engine starts but runs poorly (batch fire mode)
        - Scan tool: No cam signal or erratic
        - Check correlation: Cam and crank should be in sync

        Intermittent stall:
        - Crank sensor fails when hot (thermal breakdown)
        - Test: Heat sensor with heat gun, monitor signal

        Trigger wheel inspection:
        - Check for missing/damaged teeth
        - Check for debris/metal shavings (magnetic sensors attract)
        """,
        key_factors=[
            "Sensor signal present (scan tool RPM reading)",
            "Sensor air gap (excessive gap = weak signal)",
            "Trigger wheel condition (teeth damaged, debris)",
            "Cam/crank correlation (timing chain verification)",
            "Wiring integrity (connector corrosion, chafed wire)"
        ],
        primary_authority=["SAE J1930 sensor terminology", "OEM sensor specifications"],
        burden_holder="Technician to verify sensor failure vs wiring or trigger wheel issue",
        adversary_position="No-start = bad starter (ignoring sensor diagnosis)",
        counter_arguments=[
            "Crank sensor failure prevents start (no RPM signal to ECU)",
            "Cam sensor failure allows start but rough operation",
            "Correlation codes indicate timing chain/belt issue (not sensor)",
            "Intermittent failures common (heat-related)"
        ],
        resolution_strategy="Check scan tool for RPM/cam signal, test sensor output, verify air gap, inspect trigger wheel",
        entity_scope="All modern fuel-injected engines (1985+)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),

    DoctrineBlock(
        topic="Ignition Coil Diagnosis (Coil-on-Plug)",
        keywords=["ignition coil", "coil-on-plug", "COP", "P0351", "P0352", "misfire", "spark"],
        conclusion_template=[
            "Coil-on-plug (COP) systems have individual coil per cylinder (no distributor or plug wires)",
            "P0351-P0362 codes indicate coil primary circuit faults; misfires (P030x) may indicate coil failure under load",
            "Common failures: coil thermal breakdown (hot restart), oil contamination (leaking valve cover), carbon tracking"
        ],
        reasoning_framework="""
        Coil-on-Plug Ignition System:

        ADVANTAGES:
        - No distributor (eliminates mechanical wear)
        - No spark plug wires (eliminates crossfire, EMI)
        - Hotter spark (shorter path, less resistance)
        - ECU can control dwell per cylinder

        COIL OPERATION:
        Primary circuit:
        - ECU grounds coil negative (12V applied to positive)
        - Current flows through primary winding (induces magnetic field)
        - ECU opens ground (field collapses)

        Secondary circuit:
        - Collapsing field induces high voltage in secondary winding
        - Voltage steps up (12V → 30,000-50,000V)
        - High voltage jumps spark plug gap (ionizes air/fuel)

        COMMON CODES:
        P0351-P0362: Coil primary circuit (Cyl 1-12)
        P030x: Misfire (may be coil failure under load)

        DIAGNOSIS:
        Coil swap test:
        - Misfire on Cyl 2 (P0302)
        - Swap Cyl 2 coil with Cyl 3
        - Misfire moves to Cyl 3 = bad coil
        - Misfire stays Cyl 2 = plug, compression, fuel

        Resistance test (key off):
        - Primary: 0.5-2 ohms typical
        - Secondary: 5,000-15,000 ohms typical
        - Out of spec = replace coil

        Current draw test:
        - Clamp meter on coil power wire
        - Crank engine, measure current
        - 5-8A typical (varies by coil design)

        Spark intensity test:
        - Remove coil, attach spark tester (30kV+ gap)
        - Crank engine, observe spark
        - Weak/no spark = bad coil

        FAILURE MODES:
        Thermal breakdown:
        - Coil fails when hot (OK when cold)
        - Symptom: Hot-restart misfire, cold-start OK
        - Test: Heat coil with heat gun, monitor operation

        Oil contamination:
        - Valve cover leak allows oil into coil boot
        - Oil tracks spark (shorts coil)
        - Symptom: Misfire, coil damaged
        - Fix: Replace valve cover gasket, coils, spark plugs

        Carbon tracking:
        - High voltage finds path to ground (not through plug)
        - Visible carbon track on coil/boot
        - Symptom: Misfire, erratic spark
        - Fix: Replace coil, plug, inspect boots

        Coil driver fault (ECU):
        - ECU transistor fails (can't ground coil)
        - Symptom: P035x code, no spark that cylinder
        - Rare, usually coil failure not ECU
        """,
        key_factors=[
            "Misfire pattern (constant, heat-related, load-related)",
            "Coil swap test result (misfire follows coil = coil bad)",
            "Oil contamination (valve cover gasket leak)",
            "Coil boot condition (carbon tracking, oil)",
            "Spark plug condition (fouled plug may damage coil)"
        ],
        primary_authority=["SAE ignition system standards", "OEM coil specifications"],
        burden_holder="Technician to verify coil failure vs plug, compression, or fuel issue",
        adversary_position="Misfire = replace spark plugs",
        counter_arguments=[
            "Coil failure common on high-mileage engines (100K+ miles)",
            "Swap test isolates coil vs other causes",
            "Thermal breakdown won't show on resistance test (must test hot)",
            "Oil contamination damages coils and plugs (both need replacement)"
        ],
        resolution_strategy="Swap test to isolate coil, check for oil contamination, test spark intensity, replace coil if confirmed",
        entity_scope="Engines with coil-on-plug ignition (1990s+)",
        confidence=ConfidenceLevel.DEFENSIBLE
    ),
])

# ============================================================================
# ENGINE LOGIC
# ============================================================================

class AUTO01Engine:
    """Automotive Engine Diagnostics Intelligence Engine"""

    def __init__(self):
        self.start_time = time.time()
        self.query_count = 0
        self.total_latency = 0.0
        self.doctrine_hits: Dict[str, int] = defaultdict(int)
        self.recent_queries: deque = deque(maxlen=100)

        logger.info(f"{ENGINE_ID} initialized | Doctrines: {len(DOCTRINE_CACHE)}")

    def query(self, query_text: str, mode: ResponseMode, context: Optional[Dict] = None) -> QueryResponse:
        """Process diagnostic query through doctrine cache"""
        start = time.time()
        self.query_count += 1

        # Normalize query
        query_lower = query_text.lower()

        # Find matching doctrines
        matches = self._match_doctrines(query_lower)

        # Generate response based on mode
        if mode == ResponseMode.FAST:
            response = self._fast_response(query_text, matches, context)
        elif mode == ResponseMode.DEFENSE:
            response = self._defense_response(query_text, matches, context)
        else:  # MEMO
            response = self._memo_response(query_text, matches, context)

        # Track metrics
        latency = (time.time() - start) * 1000
        self.total_latency += latency

        # Build response
        triggered = [m.topic for m in matches[:5]]
        sources = list(set([auth for m in matches[:3] for auth in m.primary_authority]))

        result = QueryResponse(
            engine_id=ENGINE_ID,
            query=query_text,
            mode=mode.value,
            response=response,
            confidence=matches[0].confidence.value if matches else ConfidenceLevel.DISCLOSURE.value,
            sources=sources[:5],
            triggered_doctrines=triggered,
            analysis_path=self._build_analysis_path(matches),
            determinism_hash=self._compute_hash(query_text, response),
            latency_ms=round(latency, 2),
            timestamp=datetime.utcnow().isoformat()
        )

        self.recent_queries.append({
            "query": query_text,
            "mode": mode.value,
            "latency_ms": latency,
            "doctrines": len(matches)
        })

        return result

    def _match_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Find doctrines matching query keywords"""
        scored = []

        for doctrine in DOCTRINE_CACHE:
            score = 0
            # Check keywords
            for keyword in doctrine.keywords:
                if keyword.lower() in query:
                    score += 10
            # Check topic
            if any(word in query for word in doctrine.topic.lower().split()):
                score += 5

            if score > 0:
                scored.append((score, doctrine))
                self.doctrine_hits[doctrine.topic] += 1

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored]

    def _fast_response(self, query: str, matches: List[DoctrineBlock], context: Optional[Dict]) -> str:
        """Concise diagnostic guidance (FAST mode)"""
        if not matches:
            return f"No specific automotive diagnostic doctrine found for: {query}. Recommend systematic diagnosis: verify symptoms, check codes, test components per service manual."

        top = matches[0]
        response_parts = []

        # Primary conclusion
        response_parts.append("**Primary Diagnosis:**")
        response_parts.extend([f"- {c}" for c in top.conclusion_template])

        # Quick diagnostic steps
        response_parts.append("\n**Quick Diagnostic Steps:**")
        for i, factor in enumerate(top.key_factors[:3], 1):
            response_parts.append(f"{i}. {factor}")

        # Related concerns
        if len(matches) > 1:
            related = [m.topic for m in matches[1:4]]
            response_parts.append(f"\n**Related Diagnostics:** {', '.join(related)}")

        return "\n".join(response_parts)

    def _defense_response(self, query: str, matches: List[DoctrineBlock], context: Optional[Dict]) -> str:
        """Detailed diagnostic analysis (DEFENSE mode)"""
        if not matches:
            return self._fast_response(query, matches, context)

        top = matches[0]
        response_parts = []

        # Header
        response_parts.append(f"# {top.topic} - Diagnostic Analysis\n")

        # Conclusions
        response_parts.append("## Diagnostic Conclusions:")
        response_parts.extend([f"- {c}" for c in top.conclusion_template])

        # Reasoning framework
        response_parts.append("\n## Diagnostic Reasoning:")
        response_parts.append(top.reasoning_framework.strip())

        # Key factors
        response_parts.append("\n## Critical Diagnostic Factors:")
        for i, factor in enumerate(top.key_factors, 1):
            response_parts.append(f"{i}. {factor}")

        # Authority sources
        response_parts.append("\n## Technical Authority:")
        for auth in top.primary_authority:
            response_parts.append(f"- {auth}")

        # Counter-arguments (common misconceptions)
        response_parts.append("\n## Common Diagnostic Errors to Avoid:")
        for arg in top.counter_arguments[:5]:
            response_parts.append(f"- {arg}")

        # Resolution strategy
        response_parts.append(f"\n## Recommended Diagnostic Approach:")
        response_parts.append(top.resolution_strategy)

        # Related doctrines
        if len(matches) > 1:
            response_parts.append("\n## Related Diagnostic Areas:")
            for m in matches[1:4]:
                response_parts.append(f"- **{m.topic}**: {m.conclusion_template[0]}")

        return "\n".join(response_parts)

    def _memo_response(self, query: str, matches: List[DoctrineBlock], context: Optional[Dict]) -> str:
        """Comprehensive diagnostic documentation (MEMO mode)"""
        response_parts = []

        # Title
        response_parts.append("# AUTOMOTIVE DIAGNOSTIC MEMORANDUM\n")
        response_parts.append(f"**Query:** {query}")
        response_parts.append(f"**Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        response_parts.append(f"**Engine:** {ENGINE_ID} v{VERSION}\n")

        if not matches:
            response_parts.append("## Analysis:")
            response_parts.append("No specific automotive diagnostic doctrine identified for this query.")
            response_parts.append("Recommend consulting factory service manual and following systematic diagnostic procedures.")
            return "\n".join(response_parts)

        # Executive Summary
        response_parts.append("## Executive Summary\n")
        top = matches[0]
        for conclusion in top.conclusion_template:
            response_parts.append(f"- {conclusion}")

        # Primary Diagnostic Analysis
        response_parts.append(f"\n## Primary Diagnostic Analysis: {top.topic}\n")
        response_parts.append("### Diagnostic Framework:")
        response_parts.append(top.reasoning_framework.strip())

        response_parts.append("\n### Critical Diagnostic Factors:")
        for i, factor in enumerate(top.key_factors, 1):
            response_parts.append(f"{i}. {factor}")

        response_parts.append("\n### Technical Authority and Standards:")
        for auth in top.primary_authority:
            response_parts.append(f"- {auth}")

        response_parts.append(f"\n### Diagnostic Approach:")
        response_parts.append(top.resolution_strategy)

        # Common Diagnostic Errors
        response_parts.append("\n### Common Diagnostic Errors and Misconceptions:")
        response_parts.append(f"**Incorrect Assumption:** {top.adversary_position}")
        response_parts.append("\n**Why This is Wrong:**")
        for arg in top.counter_arguments:
            response_parts.append(f"- {arg}")

        # Related Diagnostics
        if len(matches) > 1:
            response_parts.append("\n## Related Diagnostic Considerations\n")
            for i, match in enumerate(matches[1:4], 1):
                response_parts.append(f"### {i}. {match.topic}")
                response_parts.append(f"- {match.conclusion_template[0]}")
                response_parts.append(f"- Key factors: {', '.join(match.key_factors[:3])}")

        # Diagnostic Confidence Assessment
        response_parts.append(f"\n## Confidence Assessment\n")
        response_parts.append(f"**Confidence Level:** {top.confidence.value}")
        response_parts.append(f"**Applicable Scope:** {top.entity_scope}")
        response_parts.append(f"**Diagnostic Burden:** {top.burden_holder}")

        # Recommendations
        response_parts.append("\n## Diagnostic Recommendations\n")
        response_parts.append("1. Follow systematic diagnostic approach outlined above")
        response_parts.append("2. Verify all test results against OEM specifications")
        response_parts.append("3. Document all findings for warranty/customer records")
        response_parts.append("4. Consider TSBs (Technical Service Bulletins) for known issues")
        response_parts.append("5. Use OEM scan tool when available for enhanced diagnostics")

        return "\n".join(response_parts)

    def _build_analysis_path(self, matches: List[DoctrineBlock]) -> List[str]:
        """Build analysis path for transparency"""
        path = [f"Matched {len(matches)} doctrines"]
        if matches:
            path.append(f"Primary: {matches[0].topic}")
            if len(matches) > 1:
                path.append(f"Secondary: {', '.join([m.topic for m in matches[1:4]])}")
        return path

    def _compute_hash(self, query: str, response: str) -> str:
        """Compute determinism hash (SHA-256)"""
        content = f"{query}|{response}|{VERSION}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_health(self) -> Dict[str, Any]:
        """Return engine health metrics"""
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / self.query_count if self.query_count > 0 else 0

        return {
            "status": "healthy",
            "engine_id": ENGINE_ID,
            "version": VERSION,
            "port": PORT,
            "doctrines_loaded": len(DOCTRINE_CACHE),
            "uptime_seconds": round(uptime, 2),
            "total_queries": self.query_count,
            "avg_latency_ms": round(avg_latency, 2),
            "top_doctrines": dict(sorted(self.doctrine_hits.items(), key=lambda x: x[1], reverse=True)[:5]),
            "recent_queries": list(self.recent_queries)[-5:]
        }


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title=ENGINE_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AUTO01Engine()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Engine health check endpoint"""
    health_data = engine.get_health()
    return HealthResponse(**health_data)


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main diagnostic query endpoint"""
    try:
        result = engine.query(request.query, request.mode, request.context)
        return result
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/doctrines")
async def list_doctrines():
    """List all available doctrines"""
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "confidence": d.confidence.value,
                "scope": d.entity_scope
            }
            for d in DOCTRINE_CACHE
        ]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.add(
        f"logs/{ENGINE_ID}_{{time}}.log",
        rotation="100 MB",
        retention="30 days",
        level="INFO"
    )

    logger.info(f"Starting {ENGINE_NAME} v{VERSION} on port {PORT}")
    logger.info(f"Loaded {len(DOCTRINE_CACHE)} doctrine blocks")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
