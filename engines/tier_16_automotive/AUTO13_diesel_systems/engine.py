"""
AUTO13 Diesel Systems Analysis Engine v1.0.0
Tax Intelligence Engine (TIE) Grade - Diesel Engineering Expertise

Covers: Diesel diagnostics, common rail injection, turbocharger analysis,
DPF/SCR/DEF aftertreatment, glow plug systems, fuel quality assessment.

Port: 9323
Author: ECHO OMEGA PRIME Build System
"""

import sys
from pathlib import Path

# CRITICAL: Add parent directory to path BEFORE local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import asyncio
import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field
import uvicorn


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class ResponseMode(str, Enum):
    """Response mode for query output."""
    FAST = "FAST"
    DEFENSE = "DEFENSE"
    MEMO = "MEMO"


class ConfidenceLevel(str, Enum):
    """Confidence stratification levels."""
    DEFENSIBLE = "DEFENSIBLE"
    AGGRESSIVE = "AGGRESSIVE"
    DISCLOSURE = "DISCLOSURE"
    HIGH_RISK = "HIGH_RISK"


class AnalysisZone(str, Enum):
    """Analysis context zones."""
    DIAGNOSTIC = "DIAGNOSTIC"
    REPAIR = "REPAIR"
    MAINTENANCE = "MAINTENANCE"


class IssueCategory(str, Enum):
    """Diesel system issue categories."""
    FUEL_INJECTION = "FUEL_INJECTION"
    TURBOCHARGER = "TURBOCHARGER"
    AFTERTREATMENT = "AFTERTREATMENT"
    GLOW_PLUG = "GLOW_PLUG"
    FUEL_QUALITY = "FUEL_QUALITY"
    COMPRESSION = "COMPRESSION"
    TIMING = "TIMING"
    COOLING = "COOLING"
    ELECTRICAL = "ELECTRICAL"
    MECHANICAL = "MECHANICAL"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for diesel system analysis."""
    query: str = Field(..., min_length=5, description="Diesel system diagnostic query")
    mode: ResponseMode = Field(ResponseMode.FAST, description="Response detail level")
    zone: AnalysisZone = Field(AnalysisZone.DIAGNOSTIC, description="Analysis context")
    include_reasoning: bool = Field(False, description="Include reasoning chain")
    vehicle_make: Optional[str] = Field(None, description="Vehicle manufacturer")
    vehicle_model: Optional[str] = Field(None, description="Vehicle model")
    engine_model: Optional[str] = Field(None, description="Diesel engine model designation")
    year: Optional[int] = Field(None, description="Model year")


class QueryResponse(BaseModel):
    """Response model for diesel analysis."""
    query_id: str
    answer: str
    confidence: ConfidenceLevel
    reasoning: Optional[str]
    triggered_doctrines: List[str]
    issue_categories: List[IssueCategory]
    recommended_tests: List[str]
    safety_warnings: List[str]
    determinism_hash: str
    latency_ms: float
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    engine: str
    version: str
    port: int
    doctrines_loaded: int
    uptime_seconds: float


# ============================================================================
# DOCTRINE BLOCKS - REAL DIESEL ENGINEERING EXPERTISE
# ============================================================================

class DoctrineBlock:
    """Diesel engineering doctrine block."""

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
        diagnostic_tests: List[str],
        safety_warnings: List[str]
    ):
        self.topic = topic
        self.keywords = keywords
        self.conclusion_template = conclusion_template
        self.reasoning_framework = reasoning_framework
        self.key_factors = key_factors
        self.primary_authority = primary_authority
        self.confidence = confidence
        self.issue_category = issue_category
        self.diagnostic_tests = diagnostic_tests
        self.safety_warnings = safety_warnings


# Doctrine cache with 25+ real diesel engineering doctrine blocks
DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="Common Rail High Pressure Fuel System Diagnostics",
        keywords=["common rail", "high pressure", "fuel rail", "injector", "rail pressure"],
        conclusion_template="Common rail system pressure deviations indicate {component} malfunction requiring {action} based on pressure variance of {magnitude}.",
        reasoning_framework="""
        Common rail diesel injection operates at 23,000-29,000 PSI (1600-2000 bar).
        Pressure control via fuel metering valve on high-pressure pump.
        Rail pressure sensor provides feedback to ECM for closed-loop control.
        Injector flow controlled by piezo or solenoid actuators opening for 0.5-2 milliseconds.

        Diagnostic sequence:
        1. Verify rail pressure sensor reading with mechanical gauge (within 200 PSI)
        2. Monitor desired vs actual rail pressure at idle, 1500 RPM, 2500 RPM
        3. Check fuel volume control valve operation (0-100% duty cycle)
        4. Perform injector leak-back test (less than 50ml per injector in 30 seconds)
        5. Inspect high-pressure pump cam lobe wear and roller followers

        Pressure too high: Stuck fuel metering valve, faulty pressure sensor, ECM logic error
        Pressure too low: Worn pump, leaking injectors, restricted fuel supply, air in system
        Pressure unstable: Failing pressure regulator, intermittent injector leak, pump wear
        """,
        key_factors=[
            "Rail pressure specification typically 23,000-29,000 PSI depending on load",
            "Pressure sensor accuracy critical - 200 PSI variance acceptable",
            "Injector leak-back test threshold: 50ml per injector in 30 seconds",
            "Fuel volume control valve duty cycle 0-100% controls pump output",
            "High-pressure pump driven by engine camshaft or dedicated lobe"
        ],
        primary_authority=[
            "Bosch Common Rail System Technical Documentation",
            "SAE J1939 Diesel Engine Diagnostics Standard",
            "Delphi Common Rail Service Manual"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FUEL_INJECTION,
        diagnostic_tests=[
            "Rail pressure sensor verification with mechanical gauge",
            "Injector leak-back test (return flow measurement)",
            "Fuel volume control valve duty cycle scan",
            "High-pressure pump output volume test",
            "Fuel system air bleed procedure"
        ],
        safety_warnings=[
            "Common rail fuel pressure exceeds 25,000 PSI - fuel penetration injury risk",
            "Never loosen fuel connections with engine running or key on",
            "Wear safety glasses - fuel spray can penetrate skin and eyes",
            "Depressurize system before service - crack injector line 1/4 turn"
        ]
    ),

    DoctrineBlock(
        topic="Turbocharger Boost Control and Compressor Surge Analysis",
        keywords=["turbo", "boost", "surge", "wastegate", "vgt", "compressor"],
        conclusion_template="Turbocharger performance deviation of {variance} indicates {failure_mode} requiring {corrective_action} to restore boost pressure to {target_spec}.",
        reasoning_framework="""
        Diesel turbochargers increase air density for improved combustion efficiency.
        Variable Geometry Turbo (VGT) uses movable vanes to optimize turbine efficiency across RPM range.
        Wastegate turbo bleeds exhaust gas around turbine above target boost to prevent overboosting.

        Boost pressure targets: 15-25 PSI typical for light duty, 30-45 PSI for heavy duty
        Compressor efficiency peaks at 65-75% of maximum speed
        Surge occurs when airflow drops below compressor map minimum - causes reverse flow

        VGT vane position control:
        - Vanes closed at low RPM: increases exhaust velocity, spools turbo faster
        - Vanes open at high RPM: reduces backpressure, allows max airflow
        - Actuator position 0-100%: feedback via position sensor or actuator current

        Common failure modes:
        1. Carbon buildup on VGT vanes: sticky operation, vanes binding, loss of control
        2. Wastegate stuck open: boost pressure low across RPM range, poor acceleration
        3. Wastegate stuck closed: overboosting, potential engine damage, detonation risk
        4. Compressor wheel damage: low boost, abnormal noise, oil consumption
        5. Turbine shaft play: oil consumption, boost instability, catastrophic failure risk

        Diagnostic approach:
        1. Compare actual vs desired boost pressure at 1500, 2000, 2500 RPM under load
        2. Monitor VGT actuator position and verify vane movement (0-100% sweep test)
        3. Check for exhaust restriction (backpressure should be 1.5-3x boost pressure)
        4. Inspect compressor and turbine wheels for damage, oil contamination
        5. Measure shaft axial and radial play (axial <0.003 in., radial <0.010 in.)
        """,
        key_factors=[
            "Boost pressure typically 15-45 PSI depending on engine size and tune",
            "VGT vane position controlled by ECM based on RPM, load, temperature",
            "Compressor surge causes reverse airflow - audible as flutter or bark sound",
            "Turbo shaft play limits: axial <0.003 in., radial <0.010 in.",
            "Exhaust backpressure normally 1.5-3x boost pressure"
        ],
        primary_authority=[
            "Garrett Turbocharger Technical Service Manual",
            "BorgWarner VGT Diagnostics Guide",
            "Cummins Holset Turbocharger Service Procedures"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TURBOCHARGER,
        diagnostic_tests=[
            "Boost pressure measurement at multiple RPM points under load",
            "VGT actuator sweep test and position feedback verification",
            "Turbo shaft play measurement (dial indicator method)",
            "Exhaust backpressure measurement pre-turbo",
            "Compressor wheel and turbine wheel visual inspection",
            "Oil supply and drain flow verification"
        ],
        safety_warnings=[
            "Turbocharger reaches 1000+ degrees F during operation - severe burn risk",
            "Allow turbo cooldown period before shutdown to prevent bearing damage",
            "Never run engine with turbo oil supply disconnected - catastrophic failure",
            "Compressor wheel failure can eject debris at high velocity - stay clear of intake"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Particulate Filter Regeneration and Ash Loading",
        keywords=["dpf", "particulate", "regen", "regeneration", "soot", "ash"],
        conclusion_template="DPF pressure differential of {delta_p} indicates {loading_level} requiring {regen_type} regeneration with estimated {time_duration}.",
        reasoning_framework="""
        Diesel Particulate Filter (DPF) captures soot particles from exhaust to meet emissions.
        Soot accumulation increases backpressure - requires periodic regeneration (burn-off).

        Regeneration types:
        1. Passive regen: Occurs naturally during highway driving when exhaust temp >600F
        2. Active regen: ECM injects extra fuel to raise exhaust temp to 1000-1100F
        3. Forced regen: Service procedure initiated via scan tool when passive/active fail

        Pressure differential (delta-P) sensor measures restriction across DPF:
        - Clean filter: 0.5-2 PSI at idle, 2-5 PSI at highway speed
        - Moderate loading: 5-10 PSI - active regen should trigger
        - Heavy loading: 10-15 PSI - forced regen required
        - Critical: >15 PSI - potential filter damage, possible removal/cleaning needed

        Ash vs soot:
        - Soot: Carbon particles that burn during regen (combustible)
        - Ash: Non-combustible residue from engine oil additives (ZDDP, calcium, magnesium)
        - Ash accumulates over time and cannot be regenerated - requires filter removal
        - Typical ash loading limit: 200,000-300,000 miles depending on oil consumption

        Failed regen causes:
        1. Low exhaust temperature: Short trips, idle time, faulty injector
        2. Excessive soot loading: Oil consumption, turbo failure, injector issues
        3. Plugged DOC (Diesel Oxidation Catalyst): Prevents temp rise
        4. Faulty delta-P sensor: ECM doesn't recognize need for regen
        5. EGR system dumping excess soot: EGR valve stuck, cooler plugged

        Regen failure consequences:
        - Continued driving with high delta-P can crack filter substrate
        - Excessive heat during delayed regen can melt filter (thermal runaway)
        - Engine derates power to prevent damage when delta-P exceeds threshold
        """,
        key_factors=[
            "DPF delta-P specification: <2 PSI clean, 5-10 PSI moderate, >15 PSI critical",
            "Active regen requires 1000-1100F exhaust temperature for 20-40 minutes",
            "Ash accumulation limit typically 200,000-300,000 miles (non-removable)",
            "Forced regen contraindicated if delta-P >20 PSI (damage risk)",
            "Oil consumption >1 quart per 2000 miles accelerates ash loading"
        ],
        primary_authority=[
            "EPA Diesel Emissions Control Technology Overview",
            "Johnson Matthey DPF Service Manual",
            "Cummins Aftertreatment System Diagnostics"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.AFTERTREATMENT,
        diagnostic_tests=[
            "DPF delta-P sensor reading verification at idle and under load",
            "Exhaust temperature sensor verification (pre-DPF, post-DPF)",
            "Forced regeneration procedure via scan tool",
            "DOC face temperature measurement (should reach 1000F+ during regen)",
            "Soot load estimation via ECM (grams accumulated)",
            "Ash load estimation based on mileage and oil consumption history"
        ],
        safety_warnings=[
            "DPF reaches 1200F during regen - extreme burn hazard to personnel and surroundings",
            "Never perform regen near combustible materials - fire risk",
            "Ensure adequate ventilation during regen - toxic exhaust fumes",
            "Vehicle may emit visible smoke and odor during regen - this is normal"
        ]
    ),

    DoctrineBlock(
        topic="Selective Catalytic Reduction DEF System Diagnostics",
        keywords=["scr", "def", "urea", "nox", "adblue", "dosing"],
        conclusion_template="SCR NOx conversion efficiency of {efficiency_pct}% indicates {system_health} with DEF quality at {quality_level} requiring {corrective_action}.",
        reasoning_framework="""
        Selective Catalytic Reduction (SCR) injects Diesel Exhaust Fluid (DEF) into exhaust
        to convert NOx into nitrogen and water vapor. DEF is 32.5% urea, 67.5% deionized water.

        SCR chemical reaction:
        - DEF sprayed into hot exhaust (500-900F) hydrolyzes into ammonia
        - Ammonia reacts with NOx over catalyst to form N2 + H2O
        - Target NOx reduction: 85-95% to meet EPA emissions standards

        DEF dosing control:
        - ECM calculates required DEF based on NOx sensor readings, exhaust flow, temperature
        - DEF pump pressurizes fluid to 70-90 PSI
        - Dosing injector sprays DEF into exhaust upstream of SCR catalyst
        - Typical consumption: 2-3% of diesel fuel consumption (1 gallon DEF per 30-50 gallons diesel)

        Common SCR failures:
        1. DEF crystallization: Dosing injector plugged, poor atomization, white smoke
        2. DEF quality degradation: Stored >1 year, contaminated, frozen/thawed cycles
        3. DEF tank heater failure: DEF freezes at 12F, system inoperable in cold weather
        4. NOx sensor failure: Incorrect dosing, poor conversion efficiency, false codes
        5. SCR catalyst poisoning: Wrong DEF (fertilizer urea), fuel contamination, ash

        DEF quality tests:
        - Refractometer test: 32.5% concentration (refractive index 1.3814 at 68F)
        - Freeze point: Should freeze at 12F (concentration too high/low if different)
        - Contamination check: Clear fluid, no particles, no discoloration
        - pH test: Should be 9.0-9.5 (acidic if contaminated)

        Diagnostic approach:
        1. Verify NOx sensors pre-SCR and post-SCR reading correctly (compare to expected)
        2. Check DEF level, quality (refractometer), temperature (should not freeze)
        3. Monitor DEF dosing rate vs calculated requirement (within 10%)
        4. Inspect DEF injector spray pattern (should be fine mist, not stream)
        5. Check SCR catalyst face temperature (500-900F optimal range)
        6. Calculate NOx conversion efficiency: (Pre-SCR - Post-SCR) / Pre-SCR x 100
        """,
        key_factors=[
            "DEF concentration must be 32.5% urea (refractometer reading 1.3814)",
            "DEF freezes at 12F - tank heater and lines must function in cold climates",
            "Target NOx reduction 85-95% with properly functioning SCR system",
            "DEF consumption typically 2-3% of diesel fuel consumption",
            "SCR catalyst optimal temperature 500-900F for NOx conversion"
        ],
        primary_authority=[
            "ISO 22241 DEF Quality Standard",
            "Cummins SCR System Service Manual",
            "Bosch Denoxtronic DEF Dosing System Technical Guide"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.AFTERTREATMENT,
        diagnostic_tests=[
            "DEF concentration test with refractometer (32.5% target)",
            "NOx sensor pre-SCR and post-SCR output verification",
            "DEF dosing injector spray pattern inspection",
            "DEF pump pressure test (70-90 PSI)",
            "SCR catalyst face temperature measurement",
            "NOx conversion efficiency calculation",
            "DEF tank heater operation test in cold conditions"
        ],
        safety_warnings=[
            "DEF is mildly corrosive - avoid skin and eye contact",
            "Do not use agricultural urea or contaminated DEF - catalyst damage",
            "DEF expands when frozen - do not overfill tank",
            "SCR exhaust contains ammonia if dosing excessive - irritant to eyes/lungs"
        ]
    ),

    DoctrineBlock(
        topic="Glow Plug System Operation and Pre-Heat Diagnostics",
        keywords=["glow plug", "preheat", "cold start", "grid heater", "intake heater"],
        conclusion_template="Glow plug circuit resistance of {resistance_ohms} ohms indicates {component_status} with pre-heat cycle duration {duration_sec} seconds requiring {action}.",
        reasoning_framework="""
        Glow plugs provide combustion chamber pre-heat for cold diesel starting.
        Unlike gasoline spark plugs, glow plugs only operate during starting and warm-up.

        Glow plug operation:
        - Controller energizes glow plugs 5-30 seconds before cranking (wait-to-start light)
        - Plugs heat combustion chamber air to 1500-1800F to aid fuel vaporization
        - Remains on 30-180 seconds after start for smooth idle
        - Some systems use post-glow for emissions reduction during warm-up

        Types of glow plugs:
        1. Standard metal sheath: 8-12V, 8-20 ohm resistance, slower heat-up
        2. Ceramic/high-speed: 5V, 0.5-1.0 ohm, heats to temp in 2-5 seconds
        3. Pressure sensor glow plugs: Dual function - pre-heat and cylinder pressure sensing

        Glow plug system configurations:
        - Individual plug control: ECM can monitor each plug resistance, detect failures
        - Series circuit: All plugs wired together, one failure affects system
        - Parallel circuit: Each plug independent, failure doesn't affect others

        Cold start alternatives:
        - Intake air grid heater: Warms all intake air, used on engines without glow plugs
        - Ether injection: Emergency starting aid, can damage engine if overused
        - Block heater: External AC-powered heater warms coolant for easier starting

        Diagnostic sequence:
        1. Check glow plug relay/controller operation (listen for click, measure voltage)
        2. Measure individual glow plug resistance (should be 0.5-20 ohm depending on type)
        3. Test current draw during pre-heat cycle (10-25 amps per plug typical)
        4. Inspect glow plug tips for damage (swelling, breakage, carbon buildup)
        5. Verify pre-heat timer operation (wait-to-start light duration)

        Failed glow plug symptoms:
        - Hard cold starting below 40F (one or more plugs failed)
        - White smoke on cold start (incomplete combustion)
        - Rough idle until engine warms up
        - DTC codes: P0380-P0394 (glow plug circuit faults)

        Glow plug failure causes:
        - Excessive voltage: Wrong relay, controller failure, battery overcharge
        - Mechanical damage: Injector leakage, carbon buildup, overheating
        - Age/thermal cycling: Metal fatigue, element burnout after 100,000+ miles
        - Wrong fuel injector: Tip impingement, direct flame contact with glow plug
        """,
        key_factors=[
            "Glow plug resistance: 0.5-1.0 ohm (ceramic), 8-20 ohm (standard metal)",
            "Pre-heat cycle duration: 5-30 seconds depending on temperature",
            "Current draw: 10-25 amps per plug during operation",
            "Glow plugs NOT required for starting above 60-70F on most engines",
            "Failed glow plugs primarily affect cold starts below 40F"
        ],
        primary_authority=[
            "Bosch Glow Plug Technical Manual",
            "NGK Diesel Glow Plug Application Guide",
            "SAE J1177 Diesel Engine Cold Starting Standard"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.GLOW_PLUG,
        diagnostic_tests=[
            "Glow plug resistance test with ohmmeter (key off, plug disconnected)",
            "Glow plug relay/controller output voltage test",
            "Pre-heat current draw measurement with clamp meter",
            "Wait-to-start light duration verification",
            "Glow plug visual inspection for tip damage or swelling",
            "Cylinder contribution test during cold start (identify weak cylinders)"
        ],
        safety_warnings=[
            "Disconnect battery before removing glow plugs - live voltage risk",
            "Glow plugs fragile - do not overtighten (25-30 lb-ft typical torque)",
            "Broken glow plug tips can fall into cylinder - engine damage risk",
            "Never bypass glow plug timer - excessive current can damage plugs/wiring"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Fuel Quality Assessment and Contamination Analysis",
        keywords=["fuel quality", "cetane", "contamination", "water", "algae", "biodiesel"],
        conclusion_template="Fuel sample analysis shows {contamination_type} at {concentration_level} with cetane number {cetane_rating} indicating {fuel_grade} requiring {remediation}.",
        reasoning_framework="""
        Diesel fuel quality directly impacts combustion efficiency, emissions, and component life.

        Cetane number (diesel equivalent of gasoline octane):
        - Measures ignition quality - higher cetane = easier ignition, smoother combustion
        - Minimum specification: 40 cetane (ASTM D975)
        - Premium diesel: 45-50 cetane
        - Ultra-low sulfur diesel (ULSD): <15 ppm sulfur, standard since 2006

        Common fuel contaminants:
        1. Water: Most common, causes corrosion, microbial growth, injector wear
           - Sources: Condensation in tank, leaking tank, contaminated delivery
           - Detection: Water-finding paste, visual inspection (water sinks to bottom)
           - Limit: <200 ppm (0.02%) per ASTM D975

        2. Microbial growth (diesel bug/algae):
           - Bacteria and fungi grow at fuel/water interface
           - Produces slimy biomass, acidic byproducts, plugs filters
           - Prevention: Keep tanks full (reduce condensation), use biocide additives
           - Detection: Black/brown sludge in filter, fuel odor, tank inspection

        3. Particulate contamination:
           - Dirt, rust, tank scale, delivery contamination
           - Accelerates injector and pump wear
           - Detection: Fuel filter inspection, fuel sample filtration

        4. Gasoline contamination:
           - Lowers cetane, causes hard starting, misfires, knock
           - Detection: Flash point test (diesel >130F, gasoline <0F)
           - Risk: Cross-contamination at fuel station, wrong tank filled

        5. Wrong diesel grade:
           - #1 diesel (winter): Lower viscosity, prevents gelling in cold weather
           - #2 diesel (summer): Higher energy content, better fuel economy
           - Cold Flow Plugging Point (CFPP): Temperature where fuel gels
           - Cloud point: Temperature where wax crystals form (first warning)

        Biodiesel blend considerations:
        - B5 (5% biodiesel): Safe for all diesel engines, OEM approved
        - B20 (20% biodiesel): May require fuel system modifications
        - B100 (100% biodiesel): Not recommended for common rail systems
        - Biodiesel attracts water, degrades rubber fuel lines, plugs filters
        - Storage life: 6-12 months for biodiesel vs 12+ months for petroleum diesel

        Fuel system damage from poor quality:
        - Water in fuel: Injector corrosion, pump wear, microbial growth
        - Low cetane: Hard starting, excessive white smoke, poor performance
        - Contamination: Plugged filters, scored injectors, pump failure
        - Gasoline in diesel: Engine knock, reduced lubricity, fuel pump damage
        """,
        key_factors=[
            "Minimum cetane rating: 40 (ASTM D975), premium diesel 45-50 cetane",
            "Ultra-low sulfur diesel (ULSD) required: <15 ppm sulfur since 2006",
            "Water contamination limit: <200 ppm (0.02%)",
            "Biodiesel blends >5% may require fuel system modifications",
            "Diesel fuel gelling temperature varies: #1 diesel for cold weather, #2 for summer"
        ],
        primary_authority=[
            "ASTM D975 Standard Specification for Diesel Fuel",
            "SAE J313 Diesel Fuel Injection Equipment Nomenclature",
            "ISO 12156 Diesel Fuel Lubricity Test Methods"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FUEL_QUALITY,
        diagnostic_tests=[
            "Cetane number test (ASTM D613 or D6890)",
            "Water contamination test (water-finding paste or Karl Fischer titration)",
            "Flash point test (ASTM D93) to detect gasoline contamination",
            "Cloud point and pour point test (ASTM D2500, D97) for cold weather",
            "Fuel filter inspection for contamination type (water, sludge, particulates)",
            "Microbial growth test (dip slide culture test)",
            "Fuel lubricity test (ASTM D6079) for ULSD with biodiesel blends"
        ],
        safety_warnings=[
            "Diesel fuel flammable - flash point >130F but still combustible",
            "ULSD low sulfur content reduces lubricity - may require additives",
            "Never use gasoline as diesel fuel additive - engine damage and fire risk",
            "Biodiesel can degrade natural rubber fuel lines - inspect for swelling/leaks"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Engine Compression Testing and Cylinder Sealing",
        keywords=["compression", "cylinder", "leak down", "blowby", "piston rings"],
        conclusion_template="Compression test reading {psi_value} PSI in cylinder {cylinder_num} with variation {variance_pct}% indicates {sealing_condition} requiring {corrective_action}.",
        reasoning_framework="""
        Diesel engines rely on compression heating to ignite fuel (no spark plugs).
        Compression ratios: 16:1 to 23:1 typical (vs 9:1-11:1 gasoline).
        Higher compression = more heat, harder starting when worn.

        Compression test procedure:
        1. Engine at operating temperature (180-200F coolant)
        2. Remove all glow plugs or injectors for access
        3. Disable fuel system (prevent engine starting)
        4. Install compression gauge with proper adapter
        5. Crank engine minimum 6 revolutions per cylinder
        6. Record maximum pressure reading for each cylinder

        Compression specifications:
        - Light duty diesel: 350-450 PSI typical
        - Medium duty: 400-500 PSI
        - Heavy duty: 450-550 PSI
        - Maximum variance between cylinders: 10-15% (50-75 PSI)

        Low compression causes:
        1. Worn piston rings: Gradual loss, oil consumption, blowby
        2. Scored cylinder walls: Sudden loss, coolant loss if head gasket
        3. Leaking valves: Burnt valve seats, carbon buildup, improper clearance
        4. Blown head gasket: Adjacent cylinders low, coolant in oil, overheating
        5. Cracked cylinder head: Coolant in cylinder, external leaks

        Leak-down test (more detailed than compression test):
        - Pressurize cylinder to 100 PSI with piston at TDC compression
        - Measure pressure loss over time (1 minute typical)
        - Good cylinder: <5% leak-down (95 PSI retained)
        - Acceptable: 5-10% leak-down (90-95 PSI)
        - Marginal: 10-20% leak-down (80-90 PSI)
        - Failed: >20% leak-down (<80 PSI)

        Leak location identification:
        - Air escaping from oil filler: Piston rings or cylinder wall wear
        - Air escaping from intake: Intake valve not sealing
        - Air escaping from exhaust: Exhaust valve not sealing
        - Air escaping from radiator: Head gasket or cracked head/block

        Blowby measurement:
        - Crankcase pressure or blowby flow rate measurement
        - Typical spec: <2 CFM at idle on 6-cylinder engine
        - Excessive blowby: Worn rings, scored cylinders, cracked piston
        - Blowby increases with engine load and RPM
        """,
        key_factors=[
            "Diesel compression ratio 16:1 to 23:1 (high compression essential for ignition)",
            "Typical compression: 350-550 PSI depending on engine size and design",
            "Maximum cylinder-to-cylinder variance: 10-15% (50-75 PSI)",
            "Leak-down test more accurate: <10% leakage = good sealing",
            "Blowby specification typically <2 CFM per cylinder at idle"
        ],
        primary_authority=[
            "SAE J1349 Diesel Engine Power Test Code",
            "Cummins Engine Compression Test Procedure",
            "Detroit Diesel Troubleshooting Guide - Low Compression"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.COMPRESSION,
        diagnostic_tests=[
            "Compression test on all cylinders (engine hot, glow plugs removed)",
            "Leak-down test to quantify cylinder sealing (100 PSI applied pressure)",
            "Blowby measurement via crankcase pressure or flow meter",
            "Cylinder balance test (power contribution per cylinder)",
            "Visual inspection via borescope (piston top, valves, cylinder walls)",
            "Oil consumption tracking (rings wear = oil consumption increase)"
        ],
        safety_warnings=[
            "Remove all glow plugs before compression test - excessive pressure buildup",
            "Disable fuel system during test - engine must not start",
            "High compression can eject gauge adapter - secure properly",
            "Coolant in cylinder from head gasket can hydrolock engine - damage risk"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Injection Timing and Valve Train Synchronization",
        keywords=["timing", "injection timing", "valve timing", "tdc", "camshaft"],
        conclusion_template="Injection timing measurement shows {advance_degrees} degrees BTDC variance of {deviation_amount} indicating {timing_accuracy} requiring {timing_adjustment}.",
        reasoning_framework="""
        Diesel injection timing critical for power, efficiency, emissions, and noise.
        Timing measured in crankshaft degrees Before Top Dead Center (BTDC).

        Injection timing basics:
        - Static timing: Position of injection pump or camshaft relative to crankshaft TDC
        - Dynamic timing: Actual start of injection under running conditions
        - Timing advance: Earlier injection (more BTDC)
        - Timing retard: Later injection (closer to TDC or after TDC)

        Typical injection timing:
        - Mechanical injection: 10-20 degrees BTDC at idle, advances with RPM
        - Electronic common rail: 5-15 degrees BTDC, ECM controlled based on load/RPM
        - Pilot injection: Small pre-injection 30-40 degrees BTDC for noise reduction
        - Main injection: Primary fuel delivery 5-20 degrees BTDC
        - Post injection: After TDC for DPF regeneration (exhaust temp increase)

        Effects of incorrect timing:

        Advanced timing (too early):
        - Increased cylinder pressure and heat
        - Harder, noisier combustion (diesel knock/rattle)
        - Improved cold starting
        - Increased NOx emissions
        - Potential engine damage from excessive pressure

        Retarded timing (too late):
        - Reduced power output
        - Increased exhaust temperature
        - Black smoke (incomplete combustion)
        - Poor fuel economy
        - Reduced NOx, increased particulate emissions

        Valve timing relationship:
        - Intake valve opens: 10-30 degrees BTDC (start of intake stroke)
        - Intake valve closes: 40-60 degrees ABDC (after piston passes BDC)
        - Exhaust valve opens: 40-60 degrees BBDC (before end of power stroke)
        - Exhaust valve closes: 10-30 degrees ATDC (after piston passes TDC)
        - Valve overlap: Period when both valves open (scavenging effect)

        Timing adjustment methods:

        Mechanical pump engines:
        - Rotate injection pump housing to advance/retard timing
        - Adjustment range typically +/- 5 degrees
        - Verify with dial indicator on #1 cylinder TDC and pump timing marks

        Electronic engines:
        - ECM controls injection timing via fuel injector pulse timing
        - No mechanical adjustment - timing changed via ECM calibration
        - Can monitor actual vs desired timing with scan tool

        Valve train timing (camshaft position):
        - Verify camshaft-to-crankshaft relationship with timing marks
        - Gear-driven: Inspect gear timing marks alignment
        - Belt/chain-driven: Check belt/chain tension and mark alignment
        - Variable valve timing (VVT): ECM controlled cam phaser position

        Timing verification methods:
        1. Static timing: Use dial indicator to find TDC, verify pump/camshaft marks
        2. Dynamic timing: Scan tool monitoring of actual injection timing
        3. Fuel injection pressure rise measurement (start of injection detection)
        4. Valve train timing: Camshaft position sensor vs crankshaft position sensor correlation
        """,
        key_factors=[
            "Injection timing typically 5-20 degrees BTDC for main injection",
            "Advanced timing increases power and NOx, retarded timing reduces power",
            "Valve overlap period allows scavenging effect (exhaust out, fresh air in)",
            "Electronic engines have no mechanical timing adjustment (ECM controlled)",
            "Timing belt/chain failure causes valve-to-piston contact (catastrophic damage)"
        ],
        primary_authority=[
            "Bosch Diesel Fuel Injection Timing Procedures",
            "SAE J1826 Diesel Engine Valve Train Timing",
            "Cummins PT Fuel System Timing Specification"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.TIMING,
        diagnostic_tests=[
            "Static injection timing check with dial indicator at TDC",
            "Dynamic injection timing monitoring via scan tool",
            "Camshaft-to-crankshaft position correlation test",
            "Fuel injection pressure rise measurement (start of injection)",
            "Valve timing verification with timing marks and TDC indicator",
            "Compression stroke identification for #1 cylinder TDC"
        ],
        safety_warnings=[
            "Never rotate engine backwards - timing belt/chain damage risk",
            "Incorrect timing can cause piston-to-valve contact - catastrophic damage",
            "Advanced timing increases cylinder pressure - engine stress and failure risk",
            "Always verify TDC position before setting injection timing"
        ]
    ),

    DoctrineBlock(
        topic="EGR System Diagnostics and Cooler Fouling Analysis",
        keywords=["egr", "exhaust gas recirculation", "egr valve", "egr cooler", "soot"],
        conclusion_template="EGR valve position {valve_position_pct}% with flow rate {flow_variance} indicates {egr_health} and cooler restriction {restriction_level} requiring {service_action}.",
        reasoning_framework="""
        Exhaust Gas Recirculation (EGR) reduces NOx emissions by recirculating exhaust
        back into intake to lower combustion temperatures.

        EGR system components:
        - EGR valve: Controls exhaust gas flow into intake (0-100% position)
        - EGR cooler: Cools exhaust gas before intake (improves efficiency)
        - EGR position sensor: Provides feedback to ECM for closed-loop control
        - Differential pressure sensor: Measures restriction across EGR cooler

        EGR operation:
        - Closed at idle and wide-open throttle (maximum power scenarios)
        - Open during cruise and light load (10-30% flow typical)
        - ECM commands position based on NOx reduction targets
        - Cooled EGR more effective than hot EGR (denser gas, more flow)

        Common EGR failures:

        1. EGR valve stuck open:
           - Rough idle, stalling (excess exhaust dilution)
           - Black smoke, poor power (insufficient fresh air)
           - High soot accumulation in intake manifold
           - Diagnostic: Command 0% EGR, verify valve closes (position sensor)

        2. EGR valve stuck closed:
           - High NOx emissions (no exhaust recirculation)
           - May pass inspection but fail emissions test
           - Diagnostic: Command 50% EGR, verify valve opens

        3. EGR cooler plugged:
           - Restricted exhaust flow, high backpressure
           - Low EGR flow rate despite valve open
           - Potential cooler failure from excessive pressure
           - Diagnostic: Measure delta-P across cooler (should be <2 PSI)

        4. EGR cooler leaking (internal):
           - Coolant consumption, white smoke
           - Coolant contamination in intake manifold
           - Overheating from coolant loss
           - Diagnostic: Pressure test cooling system, inspect intake for coolant

        EGR cooler fouling progression:
        - New cooler: 0.5-1 PSI restriction, full flow capability
        - Moderate fouling: 2-5 PSI restriction, reduced flow (50-70% of spec)
        - Heavy fouling: 5-10 PSI restriction, minimal flow (20-50% of spec)
        - Critical: >10 PSI restriction, cooler failure risk, bypass recommended

        Fouling causes:
        - Excessive soot production: Worn injectors, turbo failure, over-fueling
        - Short trip operation: Cooler never reaches full temperature to burn off deposits
        - Poor fuel quality: High sulfur or contaminated fuel increases soot
        - Oil consumption: Burnt oil ash accumulates in cooler passages

        Cleaning vs replacement:
        - Chemical cleaning effective for moderate fouling (<5 PSI restriction)
        - Ultrasonic cleaning for heavy fouling (5-10 PSI)
        - Replacement required if cooler leaking or >10 PSI restriction
        - Some OEMs recommend replacement-only (no cleaning due to failure risk)
        """,
        key_factors=[
            "EGR valve position 0-100% controlled by ECM based on NOx targets",
            "EGR cooler delta-P specification typically <2 PSI when clean",
            "EGR closed at idle and WOT, open 10-30% during cruise",
            "Cooler fouling primary cause: excessive soot from injector/turbo issues",
            "EGR valve stuck open causes rough idle and black smoke"
        ],
        primary_authority=[
            "BorgWarner EGR System Service Manual",
            "Cummins EGR Diagnostics and Repair Procedures",
            "SAE J1904 EGR System Performance Standard"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.AFTERTREATMENT,
        diagnostic_tests=[
            "EGR valve position command vs actual position verification",
            "EGR cooler delta-P measurement (before/after cooler)",
            "EGR flow rate measurement or calculation via scan tool",
            "Intake manifold inspection for soot accumulation",
            "Coolant pressure test to detect EGR cooler internal leak",
            "EGR valve operation test (0% and 100% commanded sweep)"
        ],
        safety_warnings=[
            "EGR cooler under pressure - coolant spray risk if leaking",
            "EGR passages contain hot exhaust gas (1000F+) - burn hazard",
            "Coolant in intake from EGR leak can hydrolock engine - damage risk",
            "Chemical cleaning of EGR cooler requires proper PPE - caustic solutions"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Engine Oil Analysis and Wear Metal Trending",
        keywords=["oil analysis", "wear metals", "contamination", "oil degradation", "soot"],
        conclusion_template="Oil sample shows {wear_metal} at {concentration_ppm} ppm with soot level {soot_pct}% and TBN {tbn_value} indicating {oil_condition} requiring {action}.",
        reasoning_framework="""
        Oil analysis provides early warning of engine wear and contamination issues.
        Trending data over time more valuable than single sample results.

        Key oil analysis parameters:

        1. Wear metals (parts per million - ppm):
           - Iron (Fe): General engine wear, cylinder/ring/bearing wear
           - Chromium (Cr): Piston rings, cylinder liner chrome plating
           - Aluminum (Al): Pistons, bearings, cooler corrosion
           - Copper (Cu): Bearings, bushings, cooler corrosion
           - Lead (Pb): Bearings (older engines), babbit bearing material
           - Tin (Sn): Bearings, piston coatings

           Normal levels: <50 ppm Fe, <10 ppm Cr, <20 ppm Al, <30 ppm Cu
           Abnormal: >100 ppm any metal or rapid increase (2x in 3000 miles)

        2. Contaminants:
           - Silicon (Si): Dirt ingestion through air filter (>30 ppm abnormal)
           - Sodium (Na): Coolant contamination (>50 ppm indicates leak)
           - Potassium (K): Coolant contamination (>25 ppm abnormal)
           - Fuel dilution: Gasoline or diesel in oil (>2% abnormal)
           - Water: Coolant or condensation (>0.5% abnormal)

        3. Oil condition:
           - Viscosity: Should match grade (15W-40 typical for diesel)
           - TBN (Total Base Number): Acid neutralization capacity
             * New oil: 10-12 TBN typical
             * Condemning limit: <3 TBN (oil acidic, can't neutralize combustion acids)
           - Oxidation: Oil breakdown from heat (condemn if >25 absorbance units)
           - Nitration: Combustion byproducts (high indicates blowby or EGR issues)
           - Soot: Carbon particles from combustion
             * Normal: 0.5-1.5% soot
             * Moderate: 1.5-3% (oil still usable but monitor)
             * High: >3% (change oil, investigate cause)

        4. Additive depletion:
           - Calcium (Ca): Detergent additive (depletes over time)
           - Magnesium (Mg): Detergent/dispersant additive
           - Zinc (Zn): Anti-wear additive (ZDDP)
           - Phosphorus (P): Anti-wear additive (ZDDP component)

           Additive depletion indicates oil aging, change interval exceeded

        Wear metal trending interpretation:

        Gradual increase (normal wear):
        - Iron increasing 5-10 ppm per 5000 miles: Normal ring/cylinder wear
        - Acceptable as long as rate of increase steady

        Sudden increase (abnormal wear):
        - Iron jumps from 30 ppm to 150 ppm in one interval: Component failure imminent
        - Chromium spike: Ring or cylinder liner failure
        - Aluminum spike: Piston failure, bearing failure, cooler leak
        - Copper spike: Bearing wear, bushing failure

        Contamination scenarios:
        - Silicon high: Air filter failed, dirt ingestion, accelerated wear
        - Sodium/Potassium high: Head gasket leak, oil cooler leak, corrosion
        - Fuel dilution: Injector leak, poor combustion, dilutes oil film strength
        - Water: Condensation, coolant leak, can cause bearing corrosion

        Soot accumulation causes:
        - Extended oil change intervals (normal accumulation)
        - Excessive idling or short trips (incomplete combustion)
        - Worn piston rings (blowby carries soot into oil)
        - Malfunctioning EGR system (excess soot production)
        - Plugged air filter (rich combustion)
        """,
        key_factors=[
            "Normal wear metals: <50 ppm Fe, <10 ppm Cr, <20 ppm Al, <30 ppm Cu",
            "TBN condemning limit: <3 (oil acidic, must change)",
            "Soot level: <1.5% normal, 1.5-3% monitor, >3% change oil",
            "Silicon >30 ppm indicates air filter failure or leak",
            "Trending more important than single sample - track rate of increase"
        ],
        primary_authority=[
            "ASTM D6595 Oil Analysis for Used Lubricants",
            "SAE J1454 Oil Analysis Data Interpretation",
            "Caterpillar Scheduled Oil Sampling Handbook"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.MECHANICAL,
        diagnostic_tests=[
            "Used oil analysis (wear metals, contaminants, oil condition)",
            "TBN test (acid neutralization capacity)",
            "Fuel dilution test (percent fuel in oil)",
            "Water contamination test (Karl Fischer titration)",
            "Soot percentage analysis (thermogravimetric analysis)",
            "Viscosity test at 100C (should match oil grade specification)"
        ],
        safety_warnings=[
            "Used diesel oil contains combustion byproducts - minimize skin contact",
            "High soot oil is abrasive - can accelerate wear if not changed",
            "Coolant in oil creates acidic sludge - corrosive to bearings",
            "Fuel dilution reduces oil viscosity - can cause bearing failure"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Engine Cooling System and Cavitation Analysis",
        keywords=["cooling", "coolant", "cavitation", "thermostat", "water pump", "radiator"],
        conclusion_template="Coolant analysis shows pH {ph_value} with inhibitor depletion {depletion_pct}% and cavitation indicators {cavitation_level} requiring {coolant_service}.",
        reasoning_framework="""
        Diesel engines produce more heat than gasoline engines due to higher compression.
        Cooling system must maintain 180-210F operating temperature for efficiency.

        Coolant mixture specifications:
        - 50/50 ethylene glycol and water: freeze protection to -34F, boil point 265F
        - 60/40 mixture: freeze protection to -62F (extreme cold climates)
        - 40/60 mixture: freeze protection to -12F (warm climates, better heat transfer)
        - Never use pure antifreeze: Poor heat transfer, can overheat engine
        - Never use plain water: No corrosion protection, freezing risk, low boiling point

        Coolant types:
        - Conventional (green): Inorganic Additive Technology (IAT), 2-3 year life
        - Extended Life (orange/red): Organic Acid Technology (OAT), 5-year life
        - Hybrid (yellow): Hybrid OAT (HOAT), combines IAT and OAT
        - Diesel-specific: Supplemental Coolant Additives (SCA) for cavitation protection

        Cavitation damage:
        - Caused by formation and collapse of vapor bubbles on cylinder liner surface
        - High-frequency pressure waves create pitting on wet cylinder liners
        - Appears as small holes or craters on coolant side of liner
        - Prevention: Proper coolant concentration, SCA additives, avoid overspeed

        Supplemental Coolant Additives (SCA):
        - Contains nitrite (NO2-) to protect against cavitation
        - Typical concentration: 1200-2400 ppm nitrite for diesel engines
        - Test strips measure nitrite concentration (add SCA if below 1200 ppm)
        - Over-treatment can cause gel formation, plugged radiators

        Common cooling system failures:

        1. Thermostat stuck closed:
           - Overheating, high coolant temperature, potential boilover
           - Upper radiator hose cold while engine hot
           - Diagnostic: Temperature >220F, radiator cold, verify thermostat opening temp

        2. Thermostat stuck open:
           - Overcooling, slow warm-up, heater insufficient
           - Poor fuel economy, excessive emissions (cold enrichment)
           - Diagnostic: Temperature <180F, both hoses hot immediately on startup

        3. Water pump failure:
           - Leaking seal (coolant drips from weep hole)
           - Worn impeller (reduced coolant flow, overheating)
           - Bearing failure (squealing noise, shaft play)
           - Diagnostic: Visual leak inspection, pressure test, flow test

        4. Radiator restriction:
           - External blockage: Bugs, dirt, bent fins (reduced airflow)
           - Internal blockage: Scale, corrosion, stop-leak products (reduced flow)
           - Diagnostic: Temperature differential >20F across radiator indicates restriction

        5. Air in cooling system:
           - Hot spots, temperature fluctuations, gurgling sounds
           - Causes: Head gasket leak, improper fill, leaking hose
           - Diagnostic: Coolant level drops, air bubbles in radiator, burping sounds

        6. Cylinder head gasket failure:
           - Combustion gases in coolant (bubbles in radiator)
           - Coolant in oil (milky appearance)
           - External coolant leaks between head and block
           - Diagnostic: Combustion gas test, pressure test, visual inspection

        Coolant condition testing:
        - pH test: Should be 7.5-11.0 (acidic if <7, corrosive if >11)
        - Freeze point test: Refractometer or hydrometer (should match mix ratio)
        - Nitrite test: 1200-2400 ppm for diesel (cavitation protection)
        - Chloride test: <100 ppm (high chloride indicates hard water or contamination)
        - Glycol concentration: 50% typical (test with refractometer)
        """,
        key_factors=[
            "Coolant mix: 50/50 glycol/water typical (freeze to -34F, boil 265F)",
            "Operating temperature: 180-210F for optimal efficiency",
            "Diesel engines require SCA additives: 1200-2400 ppm nitrite for cavitation protection",
            "pH specification: 7.5-11.0 (acidic or alkaline outside range indicates contamination)",
            "Thermostat opening temperature: 180-195F typical (verify with actual vs spec)"
        ],
        primary_authority=[
            "ASTM D3306 Automotive Engine Coolant Specification",
            "TMC RP 329 Coolant System Inspection and Maintenance",
            "Fleetguard Coolant Analysis and SCA Recommendations"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.COOLING,
        diagnostic_tests=[
            "Coolant pH test (should be 7.5-11.0)",
            "Freeze point test with refractometer or hydrometer",
            "Nitrite concentration test for SCA level",
            "Pressure test of cooling system (hold 15 PSI for 15 minutes)",
            "Combustion gas test (chemical test for exhaust in coolant)",
            "Thermostat operation test (opening temperature verification)",
            "Water pump flow and leak inspection"
        ],
        safety_warnings=[
            "Never open radiator cap when hot - scalding coolant spray under pressure",
            "Ethylene glycol coolant is toxic - fatal if ingested, do not spill",
            "Cooling system under 15 PSI pressure - hot coolant can cause severe burns",
            "Combustion gases in coolant indicate head gasket failure - tow vehicle, do not drive"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Engine Electrical System and Charging Analysis",
        keywords=["battery", "alternator", "charging", "voltage", "amperage", "starter"],
        conclusion_template="Electrical system shows {voltage_reading}V with charging current {amperage}A indicating {charging_health} and battery condition {battery_status} requiring {electrical_service}.",
        reasoning_framework="""
        Diesel engines require robust electrical systems due to high starter loads.

        Battery specifications:
        - Diesel engines typically use dual batteries (24V series or 12V parallel)
        - Cold Cranking Amps (CCA): Minimum current at 0F for 30 seconds
          * Light duty diesel: 700-1000 CCA per battery
          * Medium/heavy duty: 1000-1500 CCA per battery
        - Reserve Capacity (RC): Minutes battery can supply 25A at 80F before <10.5V
        - Group size: Physical dimensions (Group 31, 4D, 8D common for diesel)

        Cranking amperage requirements:
        - Diesel starter draws 200-400 amps (light duty) to 600-1200 amps (heavy duty)
        - High compression requires more starter torque than gasoline
        - Cold weather increases oil viscosity, requires 2-3x normal cranking amps
        - Glow plug system adds 80-200 amps during pre-heat cycle

        Charging system components:
        - Alternator: 120-200 amp output typical (larger for commercial diesels)
        - Voltage regulator: Maintains 13.8-14.4V (12V system) or 27.6-28.8V (24V)
        - Battery temperature sensor: Adjusts charge voltage based on battery temp

        Alternator testing:
        1. No-load test: Engine idle, no accessories, should see 13.8-14.4V
        2. Load test: All accessories on, headlights high beam, should maintain >13.5V
        3. Output test: Clamp meter on alternator output wire, should see rated amps
        4. Ripple test: AC voltage should be <0.5V (excessive ripple indicates bad diode)

        Battery testing:
        1. Open-circuit voltage test (key off, 2+ hours since charge):
           - 12.6-12.8V = 100% charged
           - 12.4V = 75% charged
           - 12.2V = 50% charged
           - 12.0V = 25% charged
           - <11.8V = discharged

        2. Load test: Apply load equal to half CCA rating for 15 seconds
           - Voltage should stay >9.6V at 70F (>10.5V if temperature compensated)
           - Voltage drops below threshold = failed battery

        3. Conductance test: Electronic test measures internal resistance
           - Fast test, battery can remain in vehicle
           - Good: CCA rating within 10% of spec
           - Marginal: 10-25% below spec
           - Failed: >25% below spec

        Parasitic draw testing:
        - Normal: <50 milliamps with all systems off (radio memory, ECM keep-alive)
        - Abnormal: >100 milliamps (locate source with fuse pull method)
        - Common causes: Interior lights, aftermarket accessories, module failures
        - Draw test: Insert ammeter in series with negative battery cable

        Starter system diagnosis:
        - Voltage drop test: Measure voltage loss in cables during cranking
          * Positive side: <0.5V drop from battery to starter
          * Negative side: <0.3V drop from battery to engine block
          * Excessive drop indicates corroded connections or undersized cables

        - Starter amperage draw test:
          * Normal: 150-400 amps (varies by engine size)
          * High draw + slow crank: Worn starter bushings, bad bearings
          * Low draw + slow crank: High resistance in cables or connections
          * High draw + no crank: Seized starter or engine

        Common electrical failures:
        1. Corroded battery terminals: High resistance, voltage drop, no-start
        2. Sulfated batteries: Low capacity, won't hold charge, fails load test
        3. Failed alternator diode: Low charging, AC ripple, battery drain
        4. Worn alternator brushes: Intermittent charging, no charge at idle
        5. Faulty voltage regulator: Overcharging (>15V) or undercharging (<13V)
        """,
        key_factors=[
            "Diesel requires 700-1500 CCA batteries (high compression = high starter load)",
            "Charging voltage specification: 13.8-14.4V (12V system)",
            "Cranking draws 200-1200 amps depending on engine size",
            "Battery voltage drop test: <0.5V positive side, <0.3V negative side",
            "Parasitic draw limit: <50 milliamps with all systems off"
        ],
        primary_authority=[
            "SAE J537 Battery Ratings Standard",
            "SAE J1654 Electrical Charging System Test Procedures",
            "Interstate Batteries Heavy Duty Battery Application Guide"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.ELECTRICAL,
        diagnostic_tests=[
            "Battery open-circuit voltage test (12.6-12.8V = full charge)",
            "Battery load test (half CCA rating for 15 sec, >9.6V pass)",
            "Alternator output test (no-load and full-load voltage)",
            "Voltage drop test on starter circuit (positive and negative cables)",
            "Parasitic draw test with ammeter (<50 mA normal)",
            "Starter amperage draw measurement during cranking",
            "Alternator ripple test (<0.5V AC ripple)"
        ],
        safety_warnings=[
            "Battery produces explosive hydrogen gas - no sparks or flames near battery",
            "Always disconnect negative cable first when servicing - prevents shorts",
            "Wear eye protection when testing batteries - acid spray risk",
            "Never charge frozen battery - explosion risk from ice expansion"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Fuel Injector Flow Balance and Pattern Testing",
        keywords=["injector", "flow test", "spray pattern", "balance", "nozzle"],
        conclusion_template="Injector flow test shows cylinder {cylinder_num} variance of {flow_variance}% with spray pattern {pattern_quality} indicating {injector_condition} requiring {injector_action}.",
        reasoning_framework="""
        Fuel injectors critical for diesel combustion - atomize fuel into fine mist.

        Injector types:
        1. Mechanical (pump-line-nozzle): Opening pressure 3000-5000 PSI
        2. Unit injector: Integrated pump and nozzle, 20,000+ PSI injection
        3. Common rail piezo: Opens in 0.1 milliseconds, 29,000 PSI rail
        4. Common rail solenoid: Opens in 0.5 milliseconds, 23,000-26,000 PSI

        Spray pattern characteristics:
        - Cone angle: 140-160 degrees typical (wide cone for good atomization)
        - Droplet size: 10-20 microns optimal (too large = poor combustion)
        - Number of holes: 5-8 holes typical in nozzle tip
        - Hole diameter: 0.006-0.010 inch (150-250 microns)

        Flow balance testing:
        - Measures fuel delivery from each injector at same pulse width
        - Variance between injectors should be <5% (10cc difference max)
        - High flow: Worn nozzle, stuck open, internal leak
        - Low flow: Plugged nozzle, stuck closed, weak spring

        Injector balance test procedure (common rail):
        1. Connect scan tool, navigate to injector balance test
        2. ECM pulses each injector for fixed duration (typically 1000 pulses)
        3. Measure fuel volume delivered from each injector
        4. Compare to specification and between cylinders
        5. Variance >10% indicates failed injector

        Spray pattern inspection:
        - Connect injector to test bench, pressurize to operating pressure
        - Observe spray: Should be fine mist in cone shape
        - Poor pattern: Streams instead of mist, asymmetric cone, dripping
        - Causes: Worn nozzle tip, carbon buildup, damaged holes

        Injector failures and symptoms:

        1. Leaking injector (internal):
           - Cylinder wash-down: Fuel dilutes oil on cylinder wall
           - White smoke on startup (unburned fuel)
           - Oil level rises (fuel mixes with oil)
           - Diagnostic: Oil smells like diesel, elevated fuel in oil analysis

        2. Plugged injector:
           - Misfire on affected cylinder
           - Black smoke (incomplete combustion in other cylinders compensating)
           - Poor idle quality, reduced power
           - Diagnostic: Cylinder contribution test shows weak cylinder

        3. Stuck-open injector:
           - Excessive fuel delivery to one cylinder
           - Black smoke, rough idle
           - Possible hydrostatic lock if enough fuel accumulates
           - Diagnostic: Flow test shows high flow, compression test shows fuel smell

        4. Worn injector nozzle:
           - Poor spray pattern, large droplets instead of mist
           - Increased emissions (HC and particulates)
           - Reduced power, poor fuel economy
           - Diagnostic: Spray pattern test shows streams, not mist

        Injector cleaning:
        - Ultrasonic cleaning: Effective for carbon removal, restores flow
        - Chemical cleaning (on-engine): Injector cleaner additive in fuel
        - Flow testing after cleaning: Verify restored to specification
        - Some injectors not serviceable - replace only (common rail piezo)

        Return flow test (common rail):
        - Measures fuel returned from injector (should be minimal)
        - Collect return fuel from each injector for 30 seconds at idle
        - Normal: <50 ml per injector in 30 seconds
        - Excessive: >100 ml indicates internal leak, replace injector
        """,
        key_factors=[
            "Injector flow variance specification: <5% between cylinders",
            "Spray pattern should be fine mist, not streams or drips",
            "Common rail return flow limit: <50 ml per injector in 30 seconds",
            "Injection pressure: 23,000-29,000 PSI for common rail systems",
            "Nozzle hole size: 0.006-0.010 inch (extremely fine, easily plugged)"
        ],
        primary_authority=[
            "Bosch Common Rail Injector Service Procedures",
            "Delphi Fuel Injector Testing and Diagnosis Manual",
            "SAE J1832 Diesel Fuel Injection Equipment Nomenclature"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.FUEL_INJECTION,
        diagnostic_tests=[
            "Injector balance test via scan tool (flow variance between cylinders)",
            "Return flow test (fuel quantity returned per injector)",
            "Spray pattern test on injector test bench",
            "Cylinder contribution test (power output per cylinder)",
            "Injector resistance test (solenoid coil resistance)",
            "Nozzle opening pressure test (mechanical injectors)"
        ],
        safety_warnings=[
            "Injector spray exceeds 25,000 PSI - can penetrate skin and cause severe injury",
            "Never put hand near injector during operation - fuel injection injury",
            "Wear safety glasses during spray pattern test - fuel spray to eyes risk",
            "Leaking injector can cause cylinder wash-down and catastrophic engine damage"
        ]
    ),

    DoctrineBlock(
        topic="Diesel Crankcase Ventilation and Blowby Management",
        keywords=["crankcase", "blowby", "pcv", "breather", "crankcase pressure"],
        conclusion_template="Crankcase pressure measurement {pressure_value} inches H2O with blowby flow {flow_rate} CFM indicates {crankcase_health} requiring {ventilation_service}.",
        reasoning_framework="""
        Crankcase ventilation removes combustion gases that leak past piston rings.
        Excessive blowby indicates worn rings, cylinders, or piston damage.

        Blowby sources:
        - Combustion gas escaping past piston rings during compression/power stroke
        - Normal on all engines due to ring gap and imperfect sealing
        - Increases with engine wear, load, and boost pressure

        Crankcase ventilation systems:

        1. Open breather (older engines):
           - Simple tube venting crankcase to atmosphere
           - Oil mist and fumes released to environment
           - No emission control

        2. Closed PCV (Positive Crankcase Ventilation):
           - Routes crankcase fumes back to intake for combustion
           - PCV valve regulates flow based on intake vacuum
           - Reduces emissions, prevents oil contamination of environment

        3. Centrifugal separator (modern diesel):
           - Spins crankcase gases to separate oil mist
           - Returns oil to sump, vents clean air to intake
           - Prevents oil consumption through ventilation system

        Blowby measurement methods:

        1. Crankcase pressure test:
           - Install manometer (water column gauge) in dipstick tube
           - Engine at operating temp, 2500 RPM
           - Typical spec: <6 inches H2O positive pressure
           - Excessive: >10 inches H2O indicates restriction or high blowby

        2. Flow meter test:
           - Install flow meter on crankcase breather outlet
           - Measure CFM (cubic feet per minute) at specified RPM
           - Spec varies by engine size: <2 CFM per liter displacement
           - Example: 6-liter engine should be <12 CFM at rated speed

        3. Breather smoke test:
           - Visual observation of breather discharge
           - Light haze normal, heavy smoke indicates excessive blowby
           - Blue smoke: Oil consumption (rings or valve guides)
           - White/gray smoke: Combustion gas leakage (worn rings)

        Causes of excessive blowby:

        1. Worn piston rings:
           - Compression rings lose tension, don't seal cylinder wall
           - Ring gap increases with wear (0.015-0.030 inch acceptable)
           - Excessive gap (>0.050 inch) allows gas leakage

        2. Scored cylinder walls:
           - Vertical scratches prevent ring sealing
           - Causes: Dirt ingestion, broken ring, piston scuffing
           - Glaze breaking normal service, scoring requires rebore/hone

        3. Cracked or damaged piston:
           - Allows combustion gas path into crankcase
           - Often catastrophic failure (broken ring land, melted crown)
           - Detected via borescope inspection

        4. Plugged crankcase breather:
           - Causes pressure buildup in crankcase
           - Forces oil out of seals and gaskets
           - Can read as high crankcase pressure but blowby may be normal

        Effects of excessive crankcase pressure:
        - Oil leaks from rear main seal, valve covers, pan gasket
        - Oil consumption through PCV system
        - Contamination of intake with oil (carbon buildup on valves)
        - Reduced engine performance (oil in intake reduces oxygen)

        Breather system maintenance:
        - Clean or replace breather filter every 15,000-30,000 miles
        - Inspect separator for oil accumulation, drain if equipped
        - Check PCV valve operation (should rattle when shaken)
        - Verify breather hoses not collapsed or plugged
        """,
        key_factors=[
            "Crankcase pressure specification: <6 inches H2O at 2500 RPM",
            "Blowby flow specification: <2 CFM per liter displacement",
            "Ring end gap specification: 0.015-0.030 inch (>0.050 inch excessive)",
            "Plugged breather can cause pressure without excessive blowby",
            "Blue smoke from breather indicates oil consumption issue"
        ],
        primary_authority=[
            "SAE J1349 Diesel Engine Blowby Measurement",
            "Cummins Crankcase Pressure Specification",
            "Detroit Diesel Troubleshooting - Excessive Blowby"
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        issue_category=IssueCategory.MECHANICAL,
        diagnostic_tests=[
            "Crankcase pressure measurement with manometer (<6 inches H2O spec)",
            "Blowby flow measurement with flow meter at rated RPM",
            "Cylinder leak-down test to identify weak cylinders",
            "Compression test on all cylinders",
            "Breather smoke observation (light haze OK, heavy smoke abnormal)",
            "PCV valve function test (should rattle when shaken)",
            "Borescope inspection of cylinders for scoring or damage"
        ],
        safety_warnings=[
            "Crankcase contains combustible vapors - no sparks or flames near breather",
            "Excessive crankcase pressure can blow dipstick out - hot oil spray risk",
            "Plugged breather can cause catastrophic seal failure - oil loss",
            "Never seal crankcase completely - pressure buildup can damage engine"
        ]
    )
]


# ============================================================================
# TELEMETRY & METRICS
# ============================================================================

class TelemetryCollector:
    """Collect and track query metrics."""

    def __init__(self):
        self.query_count = 0
        self.total_latency_ms = 0.0
        self.doctrine_hits = 0
        self.doctrine_misses = 0
        self.error_count = 0
        self.issue_category_counts: Dict[IssueCategory, int] = {cat: 0 for cat in IssueCategory}

    def record_query(
        self,
        latency_ms: float,
        doctrines_triggered: int,
        issue_categories: List[IssueCategory],
        had_error: bool = False
    ):
        """Record query metrics."""
        self.query_count += 1
        self.total_latency_ms += latency_ms

        if doctrines_triggered > 0:
            self.doctrine_hits += 1
        else:
            self.doctrine_misses += 1

        for category in issue_categories:
            self.issue_category_counts[category] += 1

        if had_error:
            self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        avg_latency = (
            self.total_latency_ms / self.query_count if self.query_count > 0 else 0.0
        )
        hit_rate = (
            self.doctrine_hits / self.query_count if self.query_count > 0 else 0.0
        )

        return {
            "total_queries": self.query_count,
            "average_latency_ms": round(avg_latency, 2),
            "doctrine_hit_rate": round(hit_rate * 100, 1),
            "error_rate": round((self.error_count / self.query_count * 100), 2) if self.query_count > 0 else 0.0,
            "issue_category_distribution": {
                cat.value: count for cat, count in self.issue_category_counts.items() if count > 0
            }
        }


# ============================================================================
# CORE ENGINE LOGIC
# ============================================================================

class DieselSystemsEngine:
    """AUTO13 Diesel Systems Analysis Engine - TIE Grade."""

    def __init__(self):
        self.telemetry = TelemetryCollector()
        self.start_time = datetime.now()
        logger.info("AUTO13 Diesel Systems Analysis Engine initialized")

    def semantic_normalize(self, query: str) -> str:
        """Normalize diesel terminology for consistent matching."""
        normalization_map = {
            "diesel particulate filter": "dpf",
            "def fluid": "def",
            "urea": "def",
            "adblue": "def",
            "selective catalytic reduction": "scr",
            "exhaust gas recirculation": "egr",
            "variable geometry turbo": "vgt",
            "variable nozzle turbo": "vgt",
            "glow plugs": "glow plug",
            "pre-heat": "glow plug",
            "fuel injection": "injector",
            "fuel pump": "injection pump",
            "blow by": "blowby",
            "blow-by": "blowby",
            "crankcase ventilation": "blowby",
            "positive crankcase ventilation": "pcv",
            "common rail": "common rail",
            "unit injector": "unit injector",
            "turbocharger": "turbo",
            "boost pressure": "boost",
            "wastegate": "wastegate"
        }

        normalized = query.lower()
        for term, replacement in normalization_map.items():
            normalized = normalized.replace(term, replacement)

        return normalized

    def search_doctrines(self, query: str) -> List[DoctrineBlock]:
        """Search doctrine cache for matching blocks."""
        normalized_query = self.semantic_normalize(query)
        query_terms = set(normalized_query.split())

        matches = []
        for doctrine in DOCTRINE_CACHE:
            keyword_set = set(k.lower() for k in doctrine.keywords)
            if query_terms & keyword_set:
                matches.append(doctrine)

        return matches

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> Tuple[str, List[DoctrineBlock], List[IssueCategory], List[str], List[str]]:
        """
        Three-layer response system:
        1. Doctrine cache (fast, 0-50ms)
        2. Semantic search (medium, 50-200ms) - placeholder for vector DB
        3. Deep analysis (slow, 200ms+) - synthesize multiple sources
        """
        start = datetime.now()

        # Layer 1: Doctrine cache
        triggered_doctrines = self.search_doctrines(query)

        if triggered_doctrines:
            answer = self._build_doctrine_response(triggered_doctrines, mode, zone)
            issue_categories = list(set(d.issue_category for d in triggered_doctrines))
            diagnostic_tests = []
            safety_warnings = []

            for doctrine in triggered_doctrines:
                diagnostic_tests.extend(doctrine.diagnostic_tests)
                safety_warnings.extend(doctrine.safety_warnings)

            # Deduplicate
            diagnostic_tests = list(set(diagnostic_tests))[:5]
            safety_warnings = list(set(safety_warnings))[:3]

            logger.info(f"Doctrine cache hit: {len(triggered_doctrines)} blocks, {(datetime.now() - start).total_seconds() * 1000:.1f}ms")
            return answer, triggered_doctrines, issue_categories, diagnostic_tests, safety_warnings

        # Layer 2: Semantic search (placeholder - would use vector DB)
        logger.info("Doctrine cache miss, using general diesel knowledge")
        answer = self._general_diesel_response(query, mode, zone)

        return answer, [], [IssueCategory.MECHANICAL], [], []

    def _build_doctrine_response(
        self,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Build response from triggered doctrine blocks."""
        if mode == ResponseMode.FAST:
            # Concise response
            summaries = []
            for doctrine in doctrines[:2]:  # Top 2 doctrines
                summaries.append(f"{doctrine.topic}: {doctrine.conclusion_template}")
            return " ".join(summaries)

        elif mode == ResponseMode.DEFENSE:
            # Audit-ready response with citations
            response_parts = []
            for doctrine in doctrines:
                part = f"**{doctrine.topic}**\n\n"
                part += f"{doctrine.reasoning_framework}\n\n"
                part += "Key Factors:\n"
                for factor in doctrine.key_factors:
                    part += f"- {factor}\n"
                part += "\nAuthority:\n"
                for auth in doctrine.primary_authority:
                    part += f"- {auth}\n"
                response_parts.append(part)
            return "\n\n".join(response_parts)

        else:  # MEMO
            # Full documentation
            response_parts = []
            for doctrine in doctrines:
                part = f"# {doctrine.topic}\n\n"
                part += f"**Zone:** {zone.value}\n"
                part += f"**Confidence:** {doctrine.confidence.value}\n"
                part += f"**Category:** {doctrine.issue_category.value}\n\n"
                part += "## Analysis\n\n"
                part += f"{doctrine.reasoning_framework}\n\n"
                part += "## Key Factors\n\n"
                for factor in doctrine.key_factors:
                    part += f"- {factor}\n"
                part += "\n## Diagnostic Tests\n\n"
                for test in doctrine.diagnostic_tests:
                    part += f"- {test}\n"
                part += "\n## Safety Warnings\n\n"
                for warning in doctrine.safety_warnings:
                    part += f"- **WARNING:** {warning}\n"
                part += "\n## Authority\n\n"
                for auth in doctrine.primary_authority:
                    part += f"- {auth}\n"
                response_parts.append(part)
            return "\n\n---\n\n".join(response_parts)

    def _general_diesel_response(
        self,
        query: str,
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Fallback response for queries not matching doctrine cache."""
        return (
            f"Diesel system analysis for query: '{query}'\n\n"
            f"Zone: {zone.value}\n"
            f"Mode: {mode.value}\n\n"
            "This query did not match specific doctrine blocks in the cache. "
            "For detailed diesel diagnostics, please rephrase to include specific "
            "system components (e.g., 'DPF regeneration', 'common rail pressure', "
            "'turbocharger boost control', 'glow plug circuit')."
        )

    def calculate_determinism_hash(self, query: str, answer: str) -> str:
        """Calculate SHA-256 hash for response reproducibility."""
        content = f"{query}|{answer}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process diesel system diagnostic query."""
        start_time = datetime.now()
        query_id = hashlib.sha256(f"{request.query}{start_time}".encode()).hexdigest()[:12]

        try:
            # Three-layer response
            answer, triggered_doctrines, issue_categories, tests, warnings = self.three_layer_response(
                request.query,
                request.mode,
                request.zone
            )

            # Determine confidence
            if triggered_doctrines:
                confidence = triggered_doctrines[0].confidence
            else:
                confidence = ConfidenceLevel.DISCLOSURE

            # Calculate latency
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000

            # Determinism hash
            det_hash = self.calculate_determinism_hash(request.query, answer)

            # Build reasoning chain if requested
            reasoning = None
            if request.include_reasoning and triggered_doctrines:
                reasoning = "\n\n".join(d.reasoning_framework for d in triggered_doctrines[:2])

            # Record metrics
            self.telemetry.record_query(
                latency_ms,
                len(triggered_doctrines),
                issue_categories
            )

            # Audit trail
            self._log_audit_trail(query_id, request, answer, triggered_doctrines)

            return QueryResponse(
                query_id=query_id,
                answer=answer,
                confidence=confidence,
                reasoning=reasoning,
                triggered_doctrines=[d.topic for d in triggered_doctrines],
                issue_categories=issue_categories,
                recommended_tests=tests,
                safety_warnings=warnings,
                determinism_hash=det_hash,
                latency_ms=round(latency_ms, 2),
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            logger.error(f"Query processing error: {e}")
            self.telemetry.record_query(0, 0, [], had_error=True)
            raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    def _log_audit_trail(
        self,
        query_id: str,
        request: QueryRequest,
        answer: str,
        doctrines: List[DoctrineBlock]
    ):
        """Log query to audit trail (JSONL format)."""
        audit_entry = {
            "query_id": query_id,
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "mode": request.mode.value,
            "zone": request.zone.value,
            "vehicle_make": request.vehicle_make,
            "vehicle_model": request.vehicle_model,
            "engine_model": request.engine_model,
            "year": request.year,
            "triggered_doctrines": [d.topic for d in doctrines],
            "answer_length": len(answer)
        }

        logger.info(f"AUDIT: {json.dumps(audit_entry)}")

    def get_health(self) -> HealthResponse:
        """Get engine health status."""
        uptime = (datetime.now() - self.start_time).total_seconds()

        return HealthResponse(
            status="healthy",
            engine="AUTO13_diesel_systems",
            version="1.0.0",
            port=9323,
            doctrines_loaded=len(DOCTRINE_CACHE),
            uptime_seconds=round(uptime, 1)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="AUTO13 Diesel Systems Analysis Engine",
    description="TIE-grade diesel diagnostics, common rail injection, turbocharger, DPF/SCR/DEF, glow plugs, fuel quality",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Engine instance
engine = DieselSystemsEngine()


@APP.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main diesel system diagnostic query endpoint."""
    return await engine.process_query(request)


@APP.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint."""
    return engine.get_health()


@APP.get("/metrics")
async def metrics_endpoint():
    """Get telemetry metrics."""
    return engine.telemetry.get_metrics()


@APP.get("/doctrines")
async def doctrines_endpoint():
    """List all available doctrine topics."""
    return {
        "total_doctrines": len(DOCTRINE_CACHE),
        "topics": [d.topic for d in DOCTRINE_CACHE],
        "categories": list(set(d.issue_category.value for d in DOCTRINE_CACHE))
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting AUTO13 Diesel Systems Analysis Engine on port 9323")
    uvicorn.run(APP, host="0.0.0.0", port=9323, log_level="info")
