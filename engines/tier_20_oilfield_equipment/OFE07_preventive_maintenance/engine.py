"""
OFE07 - Preventive Maintenance Scheduling Engine
TIE Gold Standard Intelligence Engine for Oilfield Equipment Maintenance Management

Provides expert analysis of preventive maintenance scheduling, inspection intervals,
condition monitoring, and reliability-centered maintenance for oilfield equipment.

Port: 9007
Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Set
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    Path(__file__).parent / "logs" / "ofe07_{time:YYYY-MM-DD}.log",
    rotation="100 MB",
    retention="90 days",
    level="DEBUG"
)


# ============================================================================
# ENUMS & DATA MODELS
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


class EquipmentCategory(str, Enum):
    DRILLING_RIG = "DRILLING_RIG"
    MUD_PUMP = "MUD_PUMP"
    PRIME_MOVER = "PRIME_MOVER"
    GENERATOR = "GENERATOR"
    BOP_SYSTEM = "BOP_SYSTEM"
    CRANE = "CRANE"
    PRESSURE_VESSEL = "PRESSURE_VESSEL"
    PIPING_SYSTEM = "PIPING_SYSTEM"
    STORAGE_TANK = "STORAGE_TANK"
    ROTATING_EQUIPMENT = "ROTATING_EQUIPMENT"


class MaintenanceStrategy(str, Enum):
    TIME_BASED = "TIME_BASED"
    CONDITION_BASED = "CONDITION_BASED"
    RCM = "RCM"
    RUN_TO_FAILURE = "RUN_TO_FAILURE"
    PREDICTIVE = "PREDICTIVE"


@dataclass
class DoctrineBlock:
    """Core reasoning block for maintenance scheduling doctrine"""
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
    equipment_scope: List[EquipmentCategory]
    confidence: ConfidenceLevel
    confidence_stratification: str
    controlling_precedent: str


@dataclass
class TelemetryEntry:
    """Telemetry tracking for query analysis"""
    query_id: str
    timestamp: datetime
    response_mode: ResponseMode
    doctrines_triggered: List[str]
    cache_hit: bool
    latency_ms: float
    equipment_categories: List[str]
    confidence_level: str
    zone: AnalysisZone


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class MaintenanceQueryRequest(BaseModel):
    query: str = Field(..., description="Maintenance scheduling question or analysis request")
    mode: ResponseMode = Field(default=ResponseMode.FAST, description="Response detail level")
    equipment_type: Optional[EquipmentCategory] = Field(None, description="Specific equipment category")
    zone: AnalysisZone = Field(default=AnalysisZone.PLANNING, description="Analysis context zone")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class MaintenanceQueryResponse(BaseModel):
    query_id: str
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_applied: List[str]
    authorities_cited: List[str]
    equipment_categories: List[str]
    latency_ms: float
    determinism_hash: str
    timestamp: str
    disclosure: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    port: int
    doctrines_loaded: int
    cache_size: int
    uptime_seconds: float
    total_queries: int
    avg_latency_ms: float


# ============================================================================
# DOCTRINE CACHE - 25+ REAL MAINTENANCE EXPERTISE BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="API_RP_53_BOP_MAINTENANCE",
        keywords=["BOP", "blowout preventer", "API RP 53", "function test", "pressure test", "ram", "annular"],
        conclusion_template=[
            "BOP systems require comprehensive maintenance per API RP 53 including weekly function tests, bi-weekly pressure tests, and component rebuilds every 3-5 years or 1000 closures.",
            "Critical components (ram blocks, annular elements, control pods) must be inspected at intervals not exceeding manufacturer recommendations.",
            "All BOP maintenance must be documented with pressure test charts, function test logs, and component serial number tracking."
        ],
        reasoning_framework="""
API RP 53 Fourth Edition establishes prescriptive maintenance intervals for BOP systems:
- Weekly function tests of all rams, annular, choke/kill valves (when not drilling)
- Bi-weekly pressure test to rated working pressure (documented with chart recorder)
- Quarterly control system component inspection (hydraulic fluid analysis, accumulator pre-charge)
- Annual tear-down inspection of one ram cavity (rotating between positions)
- 3-year complete disassembly or 1000 closures (whichever comes first) for ram preventers
- 5-year annular element replacement maximum, sooner if elastomer degradation observed

High-risk failure modes include: ram seal leakage causing well control loss, annular element
tearing during stripping operations, control pod internal leakage preventing closure, accumulator
bottle pre-charge loss causing insufficient closing force.

Condition monitoring indicators: pressure decay rate during test, closure time trending,
hydraulic fluid contamination (ISO code), elastomer durometer hardness measurements.

IADC guidance adds that equipment operating in H2S environments requires 50% reduction in
service intervals due to accelerated elastomer degradation.
        """,
        key_factors=[
            "API RP 53 Fourth Edition prescriptive intervals",
            "1000-closure or 3-year ram rebuild limit (whichever first)",
            "5-year maximum annular element service life",
            "Bi-weekly pressure test to rated working pressure with chart documentation",
            "H2S service requires 50% interval reduction",
            "Pressure decay rate trending for seal condition assessment",
            "Component serial number tracking for life-limited parts"
        ],
        primary_authority=[
            "API RP 53 Fourth Edition - Blowout Prevention Equipment Systems for Drilling Wells",
            "IADC HSE Reference Guide Section 4.3 - BOP Maintenance Management",
            "30 CFR 250.442 - BOP Inspection and Testing Requirements (offshore)"
        ],
        burden_holder="Drilling contractor and operator share maintenance responsibility per drilling contract terms",
        adversary_position="Generic time-based maintenance without condition monitoring misses developing failures; over-maintenance increases handling damage risk",
        counter_arguments=[
            "Vibration monitoring and fluid analysis can extend intervals with data justification",
            "OEM technical bulletins may supersede API intervals for specific models",
            "Risk assessment can justify interval extension if redundant barriers exist"
        ],
        resolution_strategy="Implement API baseline intervals with condition-based adjustments supported by trending data; document technical justification for any deviations",
        equipment_scope=[EquipmentCategory.BOP_SYSTEM],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for API intervals; moderate for condition-based extensions requiring engineering analysis",
        controlling_precedent="API RP 53 is industry standard referenced in regulatory requirements and drilling contracts"
    ),

    DoctrineBlock(
        topic="MUD_PUMP_FLUID_END_MAINTENANCE",
        keywords=["mud pump", "fluid end", "expendables", "liner", "piston", "valve", "seat", "3000 hours"],
        conclusion_template=[
            "Triplex mud pump fluid ends require expendable replacement every 500-3000 hours depending on abrasive content and operating pressure.",
            "Liners and pistons typically fail between 1000-2000 hours in abrasive drilling fluid; valves/seats every 500-1000 hours.",
            "Vibration monitoring and discharge pressure pulsation analysis enable condition-based replacement, avoiding premature failures."
        ],
        reasoning_framework="""
National Oilwell Varco (NOV) and Gardner Denver (GD) OEM recommendations establish baseline
intervals, but actual service life varies dramatically with operating conditions:

Liner/Piston Life Factors:
- Clean water-based mud: 2500-3000 hours
- Moderate sand content (<2%): 1500-2000 hours
- High abrasive loading (barite, drilled solids): 800-1200 hours
- Operating pressure impact: 3000 psi vs 5000 psi reduces life 30-40%

Valve/Seat Life Factors:
- Intake valve seats fail faster than discharge (suction erosion)
- Elastomer valve pod life: 500-1000 hours (temperature dependent)
- Metal-to-metal seats: 1500-2500 hours with proper filtration

Condition Monitoring Approach:
- Vibration trending (ISO 10816): >7mm/s indicates liner wear
- Discharge pressure pulsation analysis: >5% variance indicates valve leakage
- Volumetric efficiency decline: >8% indicates internal leakage
- Fluid end temperature differential: >20°F indicates friction increase

Preventive replacement intervals should be 80% of observed failure distribution to minimize
catastrophic failures while avoiding unnecessary expendable consumption. A 2000-hour baseline
for medium-duty service provides 95% reliability.
        """,
        key_factors=[
            "Abrasive content drives expendable life (2% sand content halves liner life)",
            "Operating pressure directly impacts fatigue life (higher pressure = shorter life)",
            "Vibration trending provides 200-400 hour failure warning window",
            "Volumetric efficiency monitoring detects internal leakage before catastrophic failure",
            "OEM baselines: 3000 hours clean fluid, 1000 hours abrasive service",
            "Temperature monitoring identifies friction/alignment issues"
        ],
        primary_authority=[
            "NOV Mission Magnum Technical Manual Section 8 - Fluid End Maintenance",
            "Gardner Denver PZ-11 Maintenance Manual Chapter 4 - Expendables Replacement",
            "SPE 184562 - Predictive Maintenance for Mud Pumps Using Vibration Analysis"
        ],
        burden_holder="Drilling contractor responsible for pump maintenance and expendable inventory",
        adversary_position="Fixed 500-hour intervals waste expendables and increase costs; run-to-failure risks NPT from catastrophic liner failure",
        counter_arguments=[
            "Condition monitoring requires investment in sensors and trending software",
            "Highly variable drilling conditions make predictive intervals unreliable",
            "Catastrophic failure risk justifies conservative replacement intervals"
        ],
        resolution_strategy="Implement baseline 1500-hour intervals with condition monitoring for interval extension; maintain critical spares inventory for rapid replacement",
        equipment_scope=[EquipmentCategory.MUD_PUMP],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for baseline intervals; moderate for predictive extensions requiring vibration trending validation",
        controlling_precedent="OEM technical manuals and SPE industry studies establish maintenance best practices"
    ),

    DoctrineBlock(
        topic="DRAWWORKS_BRAKE_INSPECTION",
        keywords=["drawworks", "brake", "band", "disc", "auxiliary", "electromagnetic", "eddy current", "IADC"],
        conclusion_template=[
            "Drawworks brake systems require daily visual inspection, monthly thickness measurements, and complete overhaul every 24 months or 8000 operating hours.",
            "Auxiliary brake (electromagnetic/eddy current) requires annual inspection with disc/magnet gap verification and cooling system maintenance.",
            "Brake band thickness below 50% of new warrants replacement; disc warpage beyond 0.015 inches requires resurfacing or replacement."
        ],
        reasoning_framework="""
IADC Drilling Manual Chapter 7 and OEM specifications (Drillmec, NOV, Gefco) establish
comprehensive brake maintenance protocols:

Mechanical Brake Bands (Primary):
- Daily visual inspection for oil contamination, band alignment, even wear
- Monthly thickness measurements at 6 positions around circumference
- Replace when any measurement <50% of new thickness (typically 0.625" new, replace at 0.312")
- Uneven wear >0.125" indicates misalignment requiring band adjustment
- Band surface temperature >400°F indicates insufficient cooling or dragging

Auxiliary Brake (Electromagnetic Eddy Current):
- Annual inspection of disc/magnet air gap (maintain 0.010"-0.015" per OEM spec)
- Cooling water flow verification (minimum 10 GPM for adequate heat dissipation)
- Disc runout measurement (<0.020" TIR acceptable)
- Magnet coil resistance testing (deviation >10% from baseline indicates winding degradation)
- Disc thickness measurement (replace when <0.875" remaining from 1.00" new)

Hydraulic Disc Brakes (if equipped):
- Quarterly hydraulic fluid analysis (ISO 18/16/13 cleanliness maximum)
- Annual caliper seal replacement (prevents sudden pressure loss)
- Disc thickness measurement every 6 months (minimum 1.25" for 1.50" new discs)
- Rotor surface finish inspection (deep scoring >0.030" requires resurfacing)

Critical failure modes: brake band fracture during heavy load, auxiliary brake overheating
causing loss of retarding force, hydraulic leak causing brake failure. All require immediate
shutdown and replacement before resuming operations.

Load testing verification: 150% of maximum static hook load with emergency stop test annually.
        """,
        key_factors=[
            "IADC recommendation: 24-month complete brake overhaul cycle",
            "Daily visual inspection prevents catastrophic band failure",
            "50% remaining thickness replacement criterion prevents fracture risk",
            "Auxiliary brake gap maintenance critical for proper retarding force",
            "Uneven wear indicates alignment issues requiring immediate correction",
            "Annual load test to 150% max static hook load",
            "Temperature monitoring prevents thermal degradation"
        ],
        primary_authority=[
            "IADC Drilling Manual 12th Edition Chapter 7 - Hoisting Systems Maintenance",
            "API Spec 8C - Drilling and Production Hoisting Equipment",
            "NOV Cyber Drawworks Maintenance Manual Section 6",
            "29 CFR 1910.179 - Overhead and Gantry Cranes (applicable provisions)"
        ],
        burden_holder="Drilling contractor responsible for drawworks maintenance and inspection documentation",
        adversary_position="Extending intervals beyond 24 months to reduce costs risks catastrophic brake failure and personnel injury",
        counter_arguments=[
            "Light-duty operations with low cycle counts may justify extended intervals",
            "Continuous monitoring systems can provide earlier failure warning",
            "Some modern hydraulic disc systems have longer service intervals"
        ],
        resolution_strategy="Maintain IADC baseline intervals for brake bands; implement temperature and thickness monitoring for auxiliary systems; never extend intervals beyond OEM maximums",
        equipment_scope=[EquipmentCategory.DRILLING_RIG],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for mechanical brake intervals; moderate for auxiliary brake extensions with monitoring data",
        controlling_precedent="IADC standards are industry baseline; API Spec 8C provides minimum requirements referenced in regulations"
    ),

    DoctrineBlock(
        topic="CATERPILLAR_3512_3516_ENGINE_MAINTENANCE",
        keywords=["CAT 3512", "CAT 3516", "diesel engine", "oil analysis", "valve adjustment", "injector", "turbo"],
        conclusion_template=[
            "Caterpillar 3512/3516 engines require oil and filter changes every 500 hours, valve lash adjustment every 2000 hours, and injector replacement every 12,000 hours.",
            "Oil analysis at 250-hour intervals enables condition-based interval extensions with documented trending data.",
            "Major overhaul (in-frame rebuild) typically at 24,000-30,000 hours depending on operating severity and maintenance quality."
        ],
        reasoning_framework="""
Caterpillar Operation and Maintenance Manual for 3512/3516 engines establishes comprehensive
service intervals, with adjustments based on fuel quality and operating load:

Lubrication System Maintenance:
- Oil and filter change: 500 hours (250 hours for high-sulfur fuel >0.5%)
- Oil analysis sampling: every oil change (track TBN, viscosity, metals, soot)
- TBN depletion to 50% of new oil warrants oil change regardless of hours
- Iron >100 ppm indicates ring/liner wear; copper >50 ppm bearing wear; silicon >20 ppm air filter failure

Fuel System Maintenance:
- Fuel filter change: 500 hours or when differential pressure >25 psi
- Injector testing: every 6000 hours (spray pattern, opening pressure, leakback volume)
- Injector replacement: 12,000 hours or when leakback exceeds spec (>60 mL/min @ idle)
- Fuel pump timing verification: every 4000 hours

Valve Train Maintenance:
- Valve lash adjustment: every 2000 hours (critical for maintaining compression and preventing valve impact)
- Intake lash: 0.015" cold; exhaust lash: 0.030" cold (tighter clearance indicates wear)
- Valve stem seals: replace at 12,000 hours or with excessive oil consumption (>1 qt/100 hrs)

Turbocharger Maintenance:
- Inspection every 2000 hours (bearing play, wheel damage, seal leakage)
- Overhaul or replacement: 12,000-15,000 hours (compressor efficiency <70% indicates degradation)
- Boost pressure monitoring: >10% decline from baseline indicates turbo degradation

Cooling System:
- Coolant analysis every 1000 hours (check pH, inhibitor concentration, contamination)
- Extended Life Coolant (ELC) change: 12,000 hours or 6 years
- Conventional coolant: 3000 hours or annually
- Radiator core cleaning: every 4000 hours or when temperature differential >15°F

Major Overhaul Triggers:
- Cylinder pressure variation >10% between cylinders
- Oil consumption >1 quart per 50 hours
- Compression ratio decline >15% from new
- 24,000-30,000 hours in severe service; 30,000-40,000 hours in light duty
        """,
        key_factors=[
            "500-hour oil change baseline; 250 hours for high-sulfur fuel",
            "Oil analysis TBN trending enables interval extensions with data justification",
            "2000-hour valve lash adjustment prevents valve train damage",
            "12,000-hour injector replacement prevents fuel system failures",
            "Turbo efficiency monitoring detects degradation before catastrophic failure",
            "24,000-30,000 hour overhaul interval for severe service applications",
            "Coolant pH and inhibitor monitoring prevents corrosion failures"
        ],
        primary_authority=[
            "Caterpillar 3512/3516 Operation and Maintenance Manual SEBU6250",
            "CAT Dealer Service Bulletins (SEBF8229 for oil analysis interpretation)",
            "ISO 4406 - Hydraulic Fluid Contamination Analysis Methods",
            "SAE J1939 - Heavy-Duty Vehicle Diagnostic Codes (for electronic diagnostics)"
        ],
        burden_holder="Equipment owner/operator responsible for following OEM maintenance schedules; deviation voids warranty",
        adversary_position="Extended oil change intervals beyond 500 hours without analysis increases wear and reduces engine life",
        counter_arguments=[
            "Synthetic oil and improved filtration can justify 750-1000 hour intervals with trending data",
            "Low-load standby generator service may warrant longer intervals than drilling rig continuous duty",
            "Some operators successfully run 1000-hour oil changes with comprehensive analysis programs"
        ],
        resolution_strategy="Follow CAT baseline 500-hour intervals initially; extend to 750 hours only with 3-cycle oil analysis trending showing stable TBN and metals; never exceed OEM maximum intervals",
        equipment_scope=[EquipmentCategory.PRIME_MOVER, EquipmentCategory.GENERATOR],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for OEM baseline intervals; moderate for extensions requiring documented oil analysis trending",
        controlling_precedent="CAT Operation and Maintenance Manual is contractual requirement for warranty coverage; deviation requires technical justification"
    ),

    DoctrineBlock(
        topic="API_2C_CRANE_INSPECTION",
        keywords=["crane", "API 2C", "wire rope", "hoist", "boom", "inspection", "certification", "load test"],
        conclusion_template=[
            "Offshore pedestal cranes require daily pre-shift inspection, monthly detailed inspection, annual certification inspection per API 2C, and load testing every 4 years.",
            "Wire rope replacement required when: 6 broken wires in one lay, 1/3 diameter reduction, kinking, bird-caging, or core protrusion observed.",
            "Third-party inspection and certification required annually for cranes >5 ton capacity in oilfield service."
        ],
        reasoning_framework="""
API Specification 2C Seventh Edition establishes comprehensive inspection and maintenance
requirements for offshore pedestal cranes used in oilfield operations:

Inspection Frequency Hierarchy:
1. Pre-shift inspection (daily before use):
   - Visual inspection of wire rope (broken wires, wear, corrosion, kinks)
   - Hook latch operation and throat opening
   - Brake function test (holding and dynamic)
   - Control operation (smooth function, no binding)
   - Boom angle indicator and anti-two-block system functional
   - Hydraulic system leak check

2. Monthly detailed inspection (documented):
   - Wire rope measurement (diameter at multiple points)
   - Hook magnetic particle inspection (cracks in high-stress areas)
   - Sheave/drum groove wear measurement (>10% wear warrants replacement)
   - Structural crack inspection (boom heel, pedestal base, A-frame)
   - Hydraulic hose condition (abraded cover, exposed wire braid)
   - Load moment indicator calibration verification

3. Annual certification inspection (third-party):
   - Complete structural NDT (MT or PT on welded joints)
   - Hydraulic system pressure test (1.25x rated working pressure)
   - Load chart verification
   - Safety device functional testing (overload, anti-two-block, boom angle)
   - Wire rope destructive testing (sample submitted to lab for tensile test)
   - Documentation review (maintenance logs, previous inspection reports)

4. Quadrennial load test (every 4 years):
   - Static load test to 110% of rated capacity at minimum radius
   - Dynamic operational test at 100% rated load
   - Structural deflection measurement (must return to baseline after load removal)
   - Certification issued by competent person or third-party inspector

Wire Rope Rejection Criteria (API 2C Section 9.3):
- 6 broken wires in one rope lay (6 x diameter length)
- 3 broken wires in one strand in one lay
- Diameter reduction >1/3 of nominal (wear or internal corrosion)
- Kinking, bird-caging, core protrusion, or strand displacement
- Heat damage (blue discoloration indicating >400°F exposure)
- Severe corrosion (pitting visible, diameter reduction)

Common failure modes requiring immediate removal from service:
- Boom structural cracks (propagate rapidly under cyclic loading)
- Hydraulic hose burst (sudden loss of control)
- Wire rope parting (catastrophic load drop)
- Anti-two-block failure (boom collapse risk)

Maintenance documentation must be retained for 5 years minimum, available for regulatory
inspection (BSEE for offshore, OSHA for onshore).
        """,
        key_factors=[
            "API 2C establishes four-tier inspection hierarchy (daily/monthly/annual/4-year)",
            "Third-party annual certification required for >5 ton capacity offshore cranes",
            "Wire rope rejection: 6 broken wires in one lay OR 1/3 diameter reduction",
            "Load test every 4 years to 110% rated capacity with deflection measurement",
            "Magnetic particle inspection of hook annually (crack detection)",
            "Documentation retention 5 years minimum for regulatory compliance",
            "Anti-two-block and load moment indicator must be functional before operation"
        ],
        primary_authority=[
            "API Specification 2C Seventh Edition - Offshore Pedestal Mounted Cranes",
            "ASME B30.8 - Floating Cranes and Derricks (complementary standard)",
            "30 CFR 250.107 - BSEE Inspection Requirements for Offshore Cranes",
            "OSHA 1910.179 - Overhead and Gantry Cranes (general industry)"
        ],
        burden_holder="Equipment owner responsible for inspection documentation; operator responsible for pre-shift checks; third-party inspector certifies annually",
        adversary_position="Extending annual inspection intervals to reduce costs violates API 2C and regulatory requirements; creates liability exposure",
        counter_arguments=[
            "Low-utilization cranes (standby service) may justify risk assessment for interval extension",
            "Continuous monitoring systems (load/deflection/vibration) could supplement inspection",
            "Some jurisdictions allow 18-month intervals with engineering analysis"
        ],
        resolution_strategy="Strict adherence to API 2C inspection intervals; no deviations without formal engineering analysis and regulatory approval; maintain robust documentation",
        equipment_scope=[EquipmentCategory.CRANE],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - API 2C is prescriptive standard referenced in regulations; no discretion for interval extension without formal approval",
        controlling_precedent="API 2C incorporated by reference in 30 CFR 250 for offshore operations; OSHA General Duty Clause for onshore"
    ),

    DoctrineBlock(
        topic="PRESSURE_VESSEL_INSPECTION_NB23_API510",
        keywords=["pressure vessel", "boiler", "NB-23", "API 510", "thickness", "CML", "RBI", "hydrostatic test"],
        conclusion_template=[
            "Unfired pressure vessels require external inspection annually, internal inspection every 5-10 years, and thickness measurements at corrosion monitoring locations (CMLs) per API 510.",
            "ASME National Board NB-23 requires hydrostatic testing every 5 years for vessels without internal inspection access.",
            "Risk-based inspection (RBI) per API 580/581 can justify extended intervals with documented probability of failure analysis."
        ],
        reasoning_framework="""
API 510 Pressure Vessel Inspection Code and ASME National Board NB-23 establish minimum
inspection requirements for oilfield pressure vessels (separators, heater-treaters, scrubbers):

Inspection Interval Hierarchy:
1. External Visual Inspection (annually):
   - Corrosion, coating degradation, mechanical damage
   - Support/foundation settling or degradation
   - Insulation condition (CUI risk areas)
   - Relief valve discharge piping condition
   - Nameplate legibility and attachment

2. Thickness Measurements (frequency based on corrosion rate):
   - CML (Corrosion Monitoring Location) mapping per API 510 Appendix B
   - Minimum 4 CMLs per vessel (more for complex geometries)
   - Ultrasonic thickness (UT) measurement at each CML
   - Inspection interval = (Current Thickness - Retirement Thickness) / Corrosion Rate × 0.5
   - Example: 0.500" current, 0.250" retirement, 0.020"/year rate = 6.25 years × 0.5 = 3.1 year interval

3. Internal Inspection (5-10 year baseline):
   - Full internal access and cleaning required
   - Visual inspection of all surfaces (general corrosion, pitting, cracking)
   - CML thickness verification
   - Nozzle and attachment weld inspection (MT or PT)
   - Internals condition (mist eliminators, baffles, supports)
   - Interval may be extended to 15 years with RBI analysis and favorable service history

4. Hydrostatic Pressure Test (5-year NB-23 requirement):
   - Required for vessels without internal inspection access
   - Test pressure = 1.5 × MAWP (Maximum Allowable Working Pressure)
   - Hold time: minimum 30 minutes with no visible leakage
   - Exemption: internal inspection resets hydrostatic test requirement

Risk-Based Inspection (API 580/581) Methodology:
- Probability of Failure (POF) assessment: corrosion rate, inspection history, damage mechanisms
- Consequence of Failure (COF) assessment: fluid inventory, toxicity, flammability, proximity to personnel
- Risk matrix determines inspection interval (high risk = more frequent)
- RBI can justify 15-year internal inspection intervals for low-risk vessels

Corrosion Under Insulation (CUI) Considerations:
- Vessels operating 250-350°F at highest CUI risk (water condensation in insulation)
- CUI inspection intervals: 5 years minimum, 10 years maximum with RBI
- Removal of insulation sections for visual inspection required

Retirement Criteria:
- Minimum thickness = (MAWP × R) / (S × E - 0.6 × MAWP) + Corrosion Allowance
  Where: R = inside radius, S = allowable stress, E = joint efficiency
- Typical retirement thickness 0.250" for 1/2" design thickness vessels

Documentation Requirements (API 510 Section 6):
- Inspection report with thickness readings, photos, findings
- Calculations for remaining life and next inspection due date
- Authorized Inspector signature (API 510 certified)
- Records retained for vessel life plus 3 years after retirement
        """,
        key_factors=[
            "API 510 establishes risk-based inspection intervals (5-15 years typical)",
            "NB-23 hydrostatic test every 5 years OR internal inspection resets requirement",
            "Corrosion rate determines thickness measurement frequency via formula",
            "RBI analysis per API 580/581 can justify extended intervals with documentation",
            "CUI high-risk zone 250-350°F requires enhanced inspection attention",
            "Authorized Inspector (API 510 certified) must review and sign reports",
            "Thickness measurements at CMLs required at defined intervals"
        ],
        primary_authority=[
            "API 510 Pressure Vessel Inspection Code Tenth Edition",
            "ASME National Board NB-23 National Board Inspection Code",
            "API 580 Risk-Based Inspection (RBI) Standard",
            "API 581 Risk-Based Inspection Methodology",
            "ASME Boiler and Pressure Vessel Code Section VIII Division 1"
        ],
        burden_holder="Vessel owner responsible for inspection program; Authorized Inspector certifies inspections meet API 510 requirements",
        adversary_position="Fixed 10-year internal inspection intervals ignore actual corrosion rates and may be either too conservative or too aggressive",
        counter_arguments=[
            "RBI requires significant engineering resources and software tools",
            "Unknown or variable corrosion rates make interval calculation uncertain",
            "Regulatory jurisdictions may not accept RBI-based interval extensions"
        ],
        resolution_strategy="Implement baseline 10-year internal inspection intervals; develop RBI program for high-value or critical vessels; always maintain thickness trending at CMLs",
        equipment_scope=[EquipmentCategory.PRESSURE_VESSEL],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for baseline intervals; moderate for RBI extensions requiring detailed analysis and regulatory acceptance",
        controlling_precedent="API 510 is recognized standard; many jurisdictions require Authorized Inspector certification for vessel inspections"
    ),

    DoctrineBlock(
        topic="PIPING_INSPECTION_API570",
        keywords=["piping", "API 570", "thickness", "CML", "erosion", "corrosion", "circuits", "RBI"],
        conclusion_template=[
            "Process piping requires external inspection every 5 years, thickness measurements at CMLs based on corrosion rates, and internal inspection when thickness approaches minimum.",
            "API 570 circuit-based inspection grouping allows similar piping to share inspection intervals based on highest corrosion rate in circuit.",
            "High-energy piping (>600 psig or >400°F) requires enhanced inspection frequency and methodology per owner risk tolerance."
        ],
        reasoning_framework="""
API 570 Piping Inspection Code Third Edition establishes circuit-based inspection methodology
for process piping in oilfield facilities (flow lines, gathering systems, processing plant piping):

Circuit Classification System:
- Circuit: group of piping with similar operating conditions, materials, corrosion environment
- Each circuit assigned inspection interval based on maximum corrosion rate within circuit
- Allows efficient resource allocation (inspect representative locations, extrapolate to circuit)

Inspection Interval Calculation (API 570 Section 6.3):
Interval = (Current Thickness - Minimum Required Thickness) / Corrosion Rate × 0.5

Example calculation:
- Flow line: 0.500" wall thickness, 0.280" minimum required, 0.030"/year corrosion rate
- Interval = (0.500 - 0.280) / 0.030 × 0.5 = 3.67 years → round to 3 years

Maximum Intervals (API 570 Table 6-1):
- Low corrosion rate (<0.005"/yr): 10 years maximum
- Moderate corrosion rate (0.005-0.025"/yr): 5-10 years
- High corrosion rate (>0.025"/yr): <5 years
- Unknown corrosion environment: 5 years maximum until data established

Corrosion Monitoring Location (CML) Selection:
- Elbows, tees (erosion/corrosion prone areas)
- Downstream of control valves (high velocity erosion)
- Low points (water accumulation and bottom-side corrosion)
- Injection points (chemical corrosion)
- Minimum 4 CMLs per circuit; more for complex geometry

Inspection Methods by Access:
1. External (cladding/insulation removed):
   - Ultrasonic thickness (UT) at CMLs
   - Visual inspection for external corrosion, coating failure, mechanical damage
   - Profile radiography for inaccessible areas (under pipe supports)

2. Internal (if feasible):
   - Smart pig (ILI - In-Line Inspection) for long pipelines
   - Visual inspection during shutdown/turnaround
   - Removal of sample spools for metallurgical analysis

High-Energy Piping Considerations (>600 psig or >400°F):
- Consequence of failure higher due to stored energy
- Require more frequent inspection (50% reduction in calculated interval)
- Enhanced NDE methods (radiography, phased array UT)
- Critical areas: deadlegs (corrosion under stagnant conditions), small-bore connections (fatigue)

Damage Mechanisms Requiring Specific Inspection Plans:
- Erosion-corrosion: downstream of control valves, high-velocity areas (annual inspection)
- Flow-accelerated corrosion (FAC): carbon steel in wet CO2 service (every 2-3 years)
- Sulfide stress cracking (SSC): H2S service >50 ppm (baseline 5 years, can't extend)
- External corrosion under insulation (CUI): 250-350°F range (5-year inspection)

Risk-Based Inspection (RBI) Application (API 580/581):
- POF assessment: corrosion rate trending, historical failures, damage mechanism activity
- COF assessment: fluid toxicity/flammability, inventory, proximity to personnel/environment
- Risk matrix determines inspection scope and interval
- High-risk circuits: more CMLs, shorter intervals, enhanced NDE
- Low-risk circuits: interval extensions to 15 years with documented justification

Minimum Required Thickness Calculation:
t_min = (P × D) / (2 × S × E × W) + Corrosion Allowance
Where: P = pressure, D = diameter, S = allowable stress, E = weld joint efficiency, W = weld strength reduction factor

Retirement and Repair Decisions:
- Thickness <minimum required: repair or replace
- Extensive pitting: pressure test or fitness-for-service analysis (API 579)
- Localized thin areas: evaluate per ASME B31G for remaining strength
        """,
        key_factors=[
            "Circuit-based grouping enables efficient inspection resource allocation",
            "Interval formula: (Current - Minimum) / Rate × 0.5 (safety factor built in)",
            "Maximum 10-year interval for low corrosion rate; 5-year unknown environment",
            "High-energy piping requires 50% interval reduction for higher consequence",
            "CML selection critical: elbows, tees, low points, injection points",
            "RBI methodology can justify interval extensions with risk documentation",
            "Smart pig (ILI) provides comprehensive data for long pipelines"
        ],
        primary_authority=[
            "API 570 Piping Inspection Code Third Edition",
            "ASME B31.3 Process Piping Design Code",
            "API 580/581 Risk-Based Inspection Standards",
            "ASME B31G Manual for Determining Remaining Strength of Corroded Pipe",
            "NACE SP0206 - Internal Corrosion Direct Assessment for Pipelines"
        ],
        burden_holder="Piping owner/operator responsible for inspection program development and execution; API 570 Inspector certifies compliance",
        adversary_position="Fixed 10-year inspection intervals ignore actual corrosion rates and process changes; risk-based approach optimizes safety and cost",
        counter_arguments=[
            "RBI programs require significant engineering resources and specialized software",
            "Unknown corrosion mechanisms may not be captured by limited CML sampling",
            "Regulatory authorities may not accept RBI-based interval extensions"
        ],
        resolution_strategy="Implement circuit-based inspection with calculated intervals; develop RBI program for large piping inventories; always trend thickness data at CMLs for interval validation",
        equipment_scope=[EquipmentCategory.PIPING_SYSTEM],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for calculated intervals with corrosion rate data; moderate for RBI extensions requiring engineering analysis",
        controlling_precedent="API 570 widely adopted industry standard; many facilities require API 570 Inspector certification for piping inspection programs"
    ),

    DoctrineBlock(
        topic="STORAGE_TANK_INSPECTION_API653",
        keywords=["storage tank", "API 653", "bottom", "shell", "roof", "internal inspection", "MFL", "vacuum box"],
        conclusion_template=[
            "Aboveground storage tanks require external inspection every 5 years, internal inspection every 10-20 years based on corrosion rate and service, and bottom thickness surveys per API 653.",
            "Tank bottom inspection can use MFL (Magnetic Flux Leakage) in lieu of full excavation for tanks in non-corrosive service with cathodic protection.",
            "Floating roof tanks require roof inspection every 5 years with detailed seal and pontoon inspection."
        ],
        reasoning_framework="""
API 653 Tank Inspection, Repair, Alteration, and Reconstruction Fourth Edition establishes
comprehensive inspection requirements for field-erected aboveground storage tanks:

External Inspection Interval (API 653 Section 6.3.1):
- Maximum 5 years (except special cases with extended interval justification)
- External visual inspection: shell corrosion, coating condition, foundation settlement
- Leak detection: staining at shell-to-bottom joint, product pooling around tank
- Settlement monitoring: tank out-of-plumbness (max 1/100 of tank height per API 653)
- Roof condition: coating, structural integrity, vents/hatches functional

Internal Inspection Interval (API 653 Section 6.4):
Base calculation: Interval = (Current Thickness - Retirement Thickness) / Corrosion Rate × 0.5
- Maximum interval: 20 years (even for very low corrosion service)
- Minimum interval: 5 years (unknown corrosion or aggressive service)
- First internal inspection: 10 years for new construction (establish baseline)

Floating Roof Inspection (every 5 years per API 653 Section 6.4.3):
- Roof structure: pontoons, buoyancy compartments (water intrusion check)
- Seals: primary and secondary seal wear, contact pressure with shell
- Rim vents: proper function (prevent vacuum on drain-down)
- Deck coating: condition, degradation requiring maintenance
- Drain system: operational test (deck drains must not plug)

Tank Bottom Inspection Methods:
1. Internal Visual (gold standard):
   - Complete drainage and cleaning required
   - Visual inspection of entire bottom surface
   - Thickness measurements at grid pattern (10-foot spacing typical)
   - Weld inspection (especially annular plate to shell weld)
   - Settlement evaluation (bottom profile survey)

2. MFL (Magnetic Flux Leakage) - In-Service Inspection:
   - Robotic scanner on tank bottom interior (product remains in tank)
   - Detects bottom pitting and thickness loss without full drainage
   - Requires compatible product (non-conductive, non-corrosive to sensor)
   - Accuracy ±0.020" thickness (not suitable for thin bottoms <0.200")
   - Supplemental to internal inspection, not complete replacement

3. Vacuum Box Testing (weld integrity):
   - Applied to bottom-side of annular plate and critical welds
   - Low-pressure vacuum applied to soaped surface (leak detection)
   - Required for bottom repairs and new construction verification

Corrosion Rate Determination (API 653 Appendix B):
- Requires minimum 2 internal inspections to establish reliable rate
- Calculate using: Rate = (Thickness₁ - Thickness₂) / Time Interval
- Apply statistical methods if multiple measurement points (average, min, max)
- Account for measurement uncertainty (±0.005" typical for UT)

Settlement Monitoring Requirements:
- Tank out-of-level tolerance: 1/100 of tank diameter (48-foot tank = 5.76" max)
- Foundation settlement causes shell stress and potential bottom buckling
- Measure at 8 or more points around circumference
- Trending required if settlement >50% of allowable

Retirement Thickness Criteria:
- Tank bottom: 0.100" minimum (thinner requires engineering analysis)
- Shell courses: varies by course stress (bottom course thickest requirement)
- Formula: t_min = (2.6 × D × H × G) / S (for bottom course)
  Where: D = diameter, H = liquid height, G = specific gravity, S = allowable stress

Cathodic Protection Integration:
- Tanks with CP systems can justify extended internal inspection intervals
- Requires annual CP effectiveness testing (voltage survey)
- Soil-side corrosion prevented by CP (extends bottom life)
- Product-side corrosion still requires monitoring (CP does not protect internal)

Special Inspection Requirements for Heated Tanks:
- Tanks >140°F require enhanced inspection for thermal cycling effects
- Roof-to-shell joint inspection critical (thermal expansion differential)
- Foundation inspection for heater equipment corrosion and leaks
        """,
        key_factors=[
            "External inspection every 5 years; internal every 10-20 years per corrosion rate",
            "MFL robotic inspection enables in-service bottom assessment (supplement to internal)",
            "Floating roof inspection every 5 years for seals, pontoons, deck coating",
            "Settlement monitoring critical: max 1/100 of diameter out-of-level tolerance",
            "Cathodic protection can justify extended intervals with annual effectiveness testing",
            "Minimum bottom thickness 0.100 inches before engineering analysis required",
            "First internal inspection at 10 years to establish corrosion baseline"
        ],
        primary_authority=[
            "API 653 Tank Inspection, Repair, Alteration, and Reconstruction Fourth Edition",
            "API Standard 650 Welded Tanks for Oil Storage Twelfth Edition (design standard)",
            "API RP 651 Cathodic Protection of Aboveground Petroleum Storage Tanks",
            "NACE SP0169 Control of External Corrosion on Underground or Submerged Metallic Piping Systems"
        ],
        burden_holder="Tank owner responsible for inspection program and documented interval justification; API 653 Inspector certifies inspections",
        adversary_position="Fixed intervals ignore actual tank condition and service severity; RBI approach optimizes inspection frequency",
        counter_arguments=[
            "MFL technology enables more frequent inspection without full drainage costs",
            "Some jurisdictions require fixed intervals regardless of condition assessment",
            "Uncertainty in corrosion rate justifies conservative intervals"
        ],
        resolution_strategy="Implement calculated intervals per API 653 formula; use MFL for interim assessments between internal inspections; always maintain settlement and thickness trending",
        equipment_scope=[EquipmentCategory.STORAGE_TANK],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for API 653 baseline intervals; moderate for extensions requiring corrosion rate data and engineering justification",
        controlling_precedent="API 653 universally adopted for storage tank inspection programs; many facilities require API 653 Inspector certification"
    ),

    DoctrineBlock(
        topic="WIRE_ROPE_REPLACEMENT_CRITERIA",
        keywords=["wire rope", "cable", "broken wires", "kink", "bird cage", "diameter", "ASME B30", "discard"],
        conclusion_template=[
            "Wire rope must be removed from service when: 6 broken wires in one lay, 1/3 diameter reduction, kinking, bird-caging, core protrusion, or heat damage observed.",
            "Running rope (dynamic service) requires more conservative criteria than standing rope (static service) due to fatigue loading.",
            "Monthly documented inspection with diameter measurements and broken wire counts required per ASME B30.5 for running ropes."
        ],
        reasoning_framework="""
ASME B30.5 Mobile and Locomotive Cranes establishes wire rope discard criteria applicable to
oilfield hoisting equipment (drawworks, cranes, wireline units):

Wire Rope Construction Understanding:
- Rope lay: one complete spiral of strands (6-8 strands typical)
- Lay length: ~6-8 times rope diameter (6x19 IWRC = 6 strands, 19 wires/strand, independent wire rope core)
- Running rope: moves over sheaves/drums (dynamic bending fatigue)
- Standing rope: guy lines, static loads (primarily tensile loading)

Broken Wire Discard Criteria (ASME B30.5 Table 5-1.4.3-1):
Running Ropes:
- 6 broken wires in one rope lay OR
- 3 broken wires in one strand in one rope lay

Standing Ropes:
- More than 2 broken wires in one rope lay (adjacent to end connections)
- More than 4 broken wires in one rope lay (elsewhere in rope)

Rationale: Running ropes experience reverse-bend fatigue over sheaves; broken wires indicate
fatigue damage and reduced safety factor. Conservative criteria prevents catastrophic failure.

Diameter Reduction Criteria:
- >1/3 reduction from nominal diameter warrants discard
- Measurement at multiple points (not just at terminations where sockets swell rope)
- Causes: wear from sheave/drum abrasion, internal corrosion, core deterioration
- Example: 1-1/8" nominal rope, discard at <0.750" (1/3 × 1.125 = 0.375" reduction)

Geometric Distortions (Immediate Discard):
1. Kinking: sharp localized bend (wire rope bent around itself under tension)
   - Permanently damages core and wires
   - Occurs from improper spooling, slack line under load
   - No repair possible; discard entire section

2. Bird-caging: strands unwound/separated forming "cage" shape
   - Caused by sudden release of tension on pre-loaded rope
   - Core damage and strand wire breakage present
   - Indicates overload or shock loading event

3. Core Protrusion: wire rope core protruding between strands
   - Indicates internal corrosion or severe compression damage
   - Reduces rope cross-section and load capacity
   - Often hidden until advanced stage

Heat Damage (Discard Immediately):
- Blue/brown discoloration indicates >400°F exposure (annealing of wires)
- Loss of tensile strength (can be 50% reduction with no visible damage)
- Occurs from friction heating (slipping on drum), torch work nearby, exhaust exposure
- Magnetic particle inspection can detect metallurgical changes

Corrosion (Engineering Judgment Required):
- External corrosion: surface rust, broken wire fragments, diameter reduction
- Internal corrosion: most insidious, requires rope dissection to detect
- Corrosion pits reduce cross-section and create stress risers
- Severe external corrosion (heavy scale, pitting): discard
- Moderate corrosion: increase inspection frequency, evaluate with broken wire counts

Wear (Measure Diameter Reduction):
- External wear: flattening of outer wires from sheave/drum contact
- Crown wear: loss of rope roundness (oval cross-section)
- Acceptable: light polishing, minor outer wire wear
- Unacceptable: >1/3 diameter reduction, individual wire breakage at wear points

Inspection Frequency (ASME B30.5 Section 5-2.4.2):
- Frequent inspection: daily or before each shift (visual by operator)
- Periodic inspection: monthly (documented by designated person)
- Includes diameter measurement, broken wire count, lubrication condition

Lubrication Requirements:
- Wire rope must be lubricated to prevent internal corrosion and reduce friction
- Visible lubricant on surface; penetrating type for core lubrication
- Frequency: every 6 months or more often in corrosive environment
- Lack of lubrication accelerates wear and internal corrosion

Service Life Considerations:
- Typical service life: 1-3 years for running rope in drilling service (high cycles)
- Crane pendants: 3-5 years (lower cycle, less bending fatigue)
- Guy lines: 5-10 years (static load, primarily tensile)
- Retirement based on condition, not time; well-maintained rope can exceed typical life
        """,
        key_factors=[
            "Running rope discard: 6 broken wires in one lay OR 3 in one strand",
            "Diameter reduction >1/3 of nominal requires discard (wear or internal corrosion)",
            "Kinking, bird-caging, core protrusion = immediate discard (no repair possible)",
            "Heat damage (blue discoloration >400°F) causes tensile strength loss",
            "Monthly documented inspection with diameter and broken wire count required",
            "Standing rope has less conservative criteria than running rope",
            "Lubrication every 6 months prevents internal corrosion"
        ],
        primary_authority=[
            "ASME B30.5 Mobile and Locomotive Cranes Section 5-2.4 Rope Inspection",
            "ASME B30.7 Base Mounted Drum Hoists (similar criteria)",
            "Wire Rope Users Manual Fourth Edition (Wire Rope Technical Board)",
            "API RP 9B Application, Care, and Use of Wire Rope for Oilfield Service"
        ],
        burden_holder="Equipment operator responsible for daily visual inspection; maintenance supervisor responsible for monthly documented inspection and discard decisions",
        adversary_position="Extending rope life beyond discard criteria to reduce costs creates catastrophic failure risk and liability exposure",
        counter_arguments=[
            "Some broken wires are acceptable depending on type and location (not adjacent)",
            "Engineering analysis can justify continued service for minor exceedances",
            "Rope condition highly dependent on application and maintenance quality"
        ],
        resolution_strategy="Strict adherence to ASME B30.5 discard criteria; err on conservative side for critical applications; maintain documented inspection records",
        equipment_scope=[EquipmentCategory.CRANE, EquipmentCategory.DRILLING_RIG],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence - ASME B30.5 criteria are prescriptive and regulatory-referenced; no discretion for extensions",
        controlling_precedent="ASME B30.5 incorporated by reference in OSHA 1910.180; API RP 9B provides oilfield-specific guidance"
    ),

    DoctrineBlock(
        topic="TORQUE_WRENCH_CALIBRATION",
        keywords=["torque wrench", "calibration", "accuracy", "ISO 6789", "certificate", "traceability", "NIST"],
        conclusion_template=[
            "Torque wrenches require calibration every 12 months or 5000 cycles (whichever first) per ISO 6789 to maintain ±4% accuracy for critical bolting.",
            "Calibration must be traceable to NIST or equivalent national standards with certificate documenting as-found and as-left values at 5 torque points.",
            "Wrenches dropped, overloaded, or showing erratic readings require immediate re-calibration before further use."
        ],
        reasoning_framework="""
ISO 6789 Assembly Tools for Screws and Nuts - Hand Torque Tools establishes calibration
requirements for torque wrenches used in critical bolting applications (flanges, pressure
equipment, structural connections):

Calibration Frequency Requirements:
- Time-based: every 12 months maximum
- Usage-based: every 5000 cycles (or per manufacturer spec if lower)
- Condition-based: immediately if dropped, overloaded, or erratic readings observed
- First calibration: new tools should be calibrated before first use to establish baseline

Calibration Procedure (ISO 6789-2:2017):
1. Pre-load cycling: minimum 3 cycles to 100% of range before testing (settles mechanism)
2. Test points: minimum 5 points across working range (20%, 40%, 60%, 80%, 100%)
3. Measurements per point: 3 readings at each test point (statistical validation)
4. Accuracy tolerance:
   - Class A tools: ±4% of indicated value (critical applications)
   - Class B tools: ±6% of indicated value (general purpose)
   - Class C tools: ±10% of indicated value (low-criticality)

5. As-found / As-left documentation:
   - As-found: tool accuracy before adjustment
   - As-left: tool accuracy after calibration adjustment
   - Out-of-tolerance findings trigger investigation of work performed with that tool

Traceability Requirements:
- Calibration equipment must be traceable to NIST (USA) or equivalent (NPL, PTB, etc.)
- Deadweight torque standard or torque transducer with 0.25% accuracy (4:1 TUR minimum)
- Calibration certificate must include:
  * Tool serial number and description
  * Calibration date and next due date
  * Standard equipment used (serial numbers and last calibration)
  * As-found and as-left data at all test points
  * Technician signature and facility accreditation (ISO/IEC 17025)

Wrench Type-Specific Considerations:

1. Click-Type Wrenches (most common):
   - Mechanical cam-over mechanism
   - Accuracy degrades with use (spring relaxation)
   - Typical service life: 5-10 years before excessive drift
   - Storage: set to lowest scale value to relieve spring tension

2. Beam-Type Wrenches:
   - Mechanical pointer deflection
   - More stable over time (no spring degradation)
   - Requires visual interpolation (operator error risk)
   - Less affected by dropping (no precision mechanism to damage)

3. Digital Electronic Wrenches:
   - Strain gauge or load cell measurement
   - Battery condition affects accuracy
   - Require more frequent calibration (every 6-12 months)
   - Temperature compensation required for outdoor use

4. Hydraulic Torque Wrenches:
   - Torque = pressure × wrench factor
   - Calibrate complete system (pump + wrench together)
   - Pressure gauge accuracy critical (calibrate gauge separately)
   - Require annual calibration minimum

Usage Conditions Affecting Accuracy:
- Temperature: calibrated at 20°C ±2°C; use outside this range affects accuracy
- Humidity/moisture: can affect electronic tools and corrode mechanical tools
- Vibration during use: can cause premature click in click-type wrenches
- Side-loading: applying force off-axis reduces accuracy (keep perpendicular to handle)

Critical Bolting Applications Requiring Calibrated Tools:
- ASME B16.5 flange bolting (pressure-retaining connections)
- ASME Section VIII pressure vessel closure bolting
- Structural steel connections (AISC requirements for slip-critical joints)
- Turbomachinery casing bolts (gas turbines, compressors)
- Critical equipment foundation bolts

Acceptance Criteria for Out-of-Tolerance Findings:
- Minor exceedance (<1% beyond tolerance): adjust and return to service
- Moderate exceedance (1-3% beyond tolerance): investigate recent work, may require re-torquing
- Major exceedance (>3% beyond tolerance): quarantine tool, evaluate all work since last calibration

Calibration Record Management:
- Maintain calibration certificates for tool life + 3 years after retirement
- Identify tools clearly with calibration sticker (next due date)
- Implement recall system 30 days before due date
- Track wrench usage cycles if possible (some tools have counters)

Cost-Benefit Considerations:
- Calibration cost: $50-$150 per wrench (external lab)
- In-house capability: $10,000-$25,000 for deadweight system and training
- Breakeven: ~100-200 wrenches justifies in-house calibration lab
- Critical application failures far exceed calibration costs (justifies conservative intervals)
        """,
        key_factors=[
            "ISO 6789 requires calibration every 12 months or 5000 cycles (whichever first)",
            "±4% accuracy tolerance for Class A tools (critical bolting applications)",
            "5-point calibration across working range with 3 readings per point",
            "NIST traceability required with as-found and as-left documentation",
            "Dropped or overloaded wrenches require immediate re-calibration",
            "Storage at lowest scale value prevents spring relaxation in click-type wrenches",
            "Out-of-tolerance findings may require investigation of recent work"
        ],
        primary_authority=[
            "ISO 6789-1:2017 Assembly Tools - Hand Torque Tools - Requirements and Test Methods",
            "ASME PCC-1 Guidelines for Pressure Boundary Bolted Flange Joint Assembly",
            "ASTM E2428 Standard Practice for Calibration and Verification of Torque Tools",
            "ISO/IEC 17025 General Requirements for Competence of Testing and Calibration Laboratories"
        ],
        burden_holder="Tool owner responsible for calibration program; maintenance personnel responsible for identifying out-of-tolerance conditions",
        adversary_position="Annual calibration is arbitrary; condition-based approach with spot-checking more efficient",
        counter_arguments=[
            "Low-use tools may not need annual calibration if cycle count tracked",
            "Some manufacturers specify longer intervals for specific models",
            "Non-critical applications can use less frequent calibration with risk acceptance"
        ],
        resolution_strategy="Implement 12-month baseline for all critical-use tools; track cycles where possible; immediate calibration for damage/drop events; maintain robust traceability documentation",
        equipment_scope=[EquipmentCategory.PRESSURE_VESSEL, EquipmentCategory.PIPING_SYSTEM, EquipmentCategory.DRILLING_RIG],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for critical applications requiring ISO 6789 compliance; moderate for general-purpose tools where risk tolerance higher",
        controlling_precedent="ISO 6789 is internationally recognized standard; ASME PCC-1 references calibrated tools for pressure equipment bolting"
    ),

    DoctrineBlock(
        topic="NDT_METHODS_SELECTION",
        keywords=["NDT", "ultrasonic", "magnetic particle", "dye penetrant", "radiography", "UT", "MT", "PT", "RT"],
        conclusion_template=[
            "NDT method selection depends on material, defect type, access, and acceptance criteria: MT for surface/near-surface in ferromagnetic materials, PT for non-magnetic, UT for volumetric, RT for permanent records.",
            "ASME Section V establishes minimum requirements for each method; inspector certification per SNT-TC-1A or ISO 9712 required.",
            "Multiple methods often required: MT or PT for surface, plus UT or RT for volumetric examination of critical welds."
        ],
        reasoning_framework="""
ASME Boiler and Pressure Vessel Code Section V Nondestructive Examination establishes
standardized procedures for NDT methods used in oilfield equipment inspection:

Method Selection Matrix:

1. Magnetic Particle Testing (MT) - ASME V Article 7:
   Best for: Surface and near-surface defects in ferromagnetic materials
   Materials: Carbon steel, low-alloy steel (NOT stainless, aluminum, titanium)
   Detects: Cracks, laps, seams, inclusions (within ~0.125" of surface)
   Sensitivity: Can detect cracks <0.001" wide if surface-breaking
   Limitations: Requires clean surface, demagnetization after testing, geometry constraints

   Applications in oilfield:
   - BOP ram cavity crack detection
   - Crane hook annual inspection
   - Pressure vessel nozzle welds
   - Drawworks drum shaft crack inspection
   - Drill pipe tool joint inspection

   Procedure: Apply magnetic field (yoke, coil, prod method) + ferromagnetic particles
             Surface cracks disrupt field, particles accumulate at discontinuity
             Wet fluorescent method most sensitive (UV light inspection)

2. Liquid Penetrant Testing (PT) - ASME V Article 6:
   Best for: Surface-breaking defects in non-ferromagnetic materials
   Materials: Stainless steel, aluminum, titanium, plastics (any non-porous material)
   Detects: Cracks, porosity, laps, seams (ONLY surface-breaking)
   Sensitivity: Can detect defects 0.0001" wide (very sensitive to tight cracks)
   Limitations: Surface-breaking only, requires very clean surface, false indications common

   Applications in oilfield:
   - Stainless steel piping welds
   - Aluminum helicopter deck crack inspection
   - Titanium pressure housing inspection
   - Cast iron component crack detection

   Procedure: Clean surface → apply penetrant (dwell 10-30 min) → remove excess →
             apply developer → inspect for penetrant bleeding out of defects
             Visible dye or fluorescent penetrant options

3. Ultrasonic Testing (UT) - ASME V Article 4, Article 5:
   Best for: Volumetric examination, thickness measurement, internal defects
   Materials: Metals, plastics, composites (anything that propagates sound waves)
   Detects: Internal cracks, lack of fusion, inclusions, porosity, thickness loss
   Sensitivity: Can detect defects >1/4 wavelength (0.020" typical for 5 MHz)
   Limitations: Requires coupling medium (gel/water), operator skill-dependent, geometry challenges

   Applications in oilfield:
   - Pressure vessel shell/head thickness measurement (corrosion monitoring)
   - Piping CML thickness trending
   - Weld volumetric examination (alternative to radiography)
   - Bolt load monitoring (bolt stretch measurement)
   - Dissimilar metal weld inspection (austenitic/ferritic interface)

   Techniques:
   - Straight beam: thickness measurement, lamination detection
   - Angle beam: weld inspection (shear wave for crack detection)
   - Phased array: complex geometries, improved crack sizing
   - TOFD (Time of Flight Diffraction): accurate crack height sizing

   Procedure: Couple transducer to surface → transmit ultrasound pulse → receive echo →
             analyze time and amplitude (A-scan, B-scan, C-scan displays)

4. Radiographic Testing (RT) - ASME V Article 2, Article 3:
   Best for: Permanent volumetric record, complex geometries, final acceptance
   Materials: All materials (penetration depends on thickness and density)
   Detects: Porosity, inclusions, lack of fusion, cracks (if oriented correctly)
   Sensitivity: 2% of thickness typical (0.020" defect in 1" thick material)
   Limitations: Expensive, radiation safety requirements, crack orientation-dependent

   Applications in oilfield:
   - Pressure vessel construction code welds (ASME Section VIII)
   - Piping construction welds (ASME B31.3 Category M fluid service)
   - Repair weld acceptance testing
   - Casting quality verification

   Sources:
   - X-ray: portable, lower penetration (up to 3" steel), instant imaging (digital)
   - Gamma (Ir-192): high penetration (up to 6" steel), isotope decay (replacement schedule)

   Procedure: Position source → place film or digital detector opposite side → expose →
             develop film or process digital image → interpret per acceptance criteria

Inspector Qualification Requirements:
- SNT-TC-1A (USA): employer-based certification program (Level I, II, III)
- ASNT Central Certification Program (ACCP): third-party national certification
- ISO 9712 (International): equivalent to ACCP, widely recognized outside USA
- Level II minimum required for independent inspection and acceptance decisions
- Level III required for procedure development and Level I/II certification

Acceptance Criteria Sources:
- ASME Section VIII Division 1: pressure vessel construction welds
- ASME B31.3: process piping welds (normal, Category M fluid)
- AWS D1.1: structural steel welds (statically loaded, dynamically loaded)
- API 1104: pipeline girth welds
- Client specifications: often more stringent than code minimums

Multi-Method Approach for Critical Welds:
- Typical: MT or PT (surface) + UT or RT (volumetric)
- Rationale: Surface methods detect tight cracks UT/RT might miss; volumetric finds internal defects
- Example: Pressure vessel nozzle weld: PT after welding + UT for volumetric + final RT
- Repair welds: MT/PT between passes + final volumetric UT or RT

Method Cost Comparison (relative):
- PT: Low cost, fast, portable (baseline = 1×)
- MT: Low-moderate cost, fast for ferromagnetic materials (1.2×)
- UT: Moderate cost, equipment investment, operator training required (2-3×)
- RT: High cost, safety/licensing requirements, film processing time (5-10×)

Emerging Technologies:
- Phased Array UT (PAUT): replaces conventional UT, better crack sizing, faster inspection
- Full Matrix Capture (FMC): advanced UT, improved resolution
- Digital radiography: replaces film, instant results, lower dose
- Eddy current array: rapid corrosion mapping (piping, tank bottoms)
        """,
        key_factors=[
            "MT best for surface/near-surface defects in ferromagnetic materials (carbon steel)",
            "PT for surface defects in non-magnetic materials (stainless, aluminum, titanium)",
            "UT for volumetric examination and thickness measurement (internal defects)",
            "RT for permanent record and code-required final acceptance (most expensive)",
            "Multi-method approach: surface (MT/PT) + volumetric (UT/RT) for critical welds",
            "Inspector certification Level II minimum per SNT-TC-1A or ISO 9712",
            "ASME Section V establishes standardized procedures for all methods"
        ],
        primary_authority=[
            "ASME BPVC Section V Nondestructive Examination",
            "SNT-TC-1A Personnel Qualification and Certification in NDT (ASNT)",
            "ISO 9712 Non-Destructive Testing - Qualification and Certification of NDT Personnel",
            "ASTM E709 Magnetic Particle Testing Standard",
            "ASTM E1417 Liquid Penetrant Testing Standard",
            "ASTM E114 Ultrasonic Pulse-Echo Testing Standard"
        ],
        burden_holder="Equipment owner specifies required methods and acceptance criteria; qualified inspector performs and interprets testing",
        adversary_position="Single-method inspection (PT only or UT only) may miss defects detectable by complementary methods",
        counter_arguments=[
            "Cost-benefit analysis may justify single method for low-risk applications",
            "Some defect types not relevant to service (e.g., porosity in low-stress areas)",
            "Over-inspection can lead to rejection of serviceable equipment"
        ],
        resolution_strategy="Select methods based on material, defect type, and criticality; use multi-method for pressure-retaining and structural welds; always use qualified inspectors",
        equipment_scope=[
            EquipmentCategory.PRESSURE_VESSEL,
            EquipmentCategory.PIPING_SYSTEM,
            EquipmentCategory.STORAGE_TANK,
            EquipmentCategory.DRILLING_RIG,
            EquipmentCategory.CRANE
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for ASME Section V procedures and inspector qualification requirements; method selection requires engineering judgment for specific applications",
        controlling_precedent="ASME Section V universally adopted for NDT procedures; inspector certification programs (SNT-TC-1A, ISO 9712) industry standard"
    ),

    DoctrineBlock(
        topic="VIBRATION_ANALYSIS_ISO10816",
        keywords=["vibration", "ISO 10816", "velocity", "displacement", "acceleration", "bearing", "imbalance", "misalignment"],
        conclusion_template=[
            "Machinery vibration monitoring per ISO 10816 uses velocity (mm/s RMS) severity zones: Zone A (new), Zone B (acceptable), Zone C (marginal), Zone D (unacceptable).",
            "Trending vibration data detects developing faults 4-8 weeks before failure: imbalance, misalignment, bearing defects, looseness.",
            "Critical rotating equipment (mud pumps, prime movers, generators) requires monthly vibration surveys with trending software for predictive maintenance."
        ],
        reasoning_framework="""
ISO 10816 Mechanical Vibration - Evaluation of Machine Vibration by Measurements on
Non-Rotating Parts establishes vibration severity criteria for condition-based maintenance:

Vibration Severity Zones (ISO 10816-1):
Zone A: Newly commissioned machines (vibration very low, <2.8 mm/s typical)
Zone B: Acceptable for unrestricted long-term operation (<4.5 mm/s rigid foundation)
Zone C: Unsatisfactory for continuous long-term operation; corrective action advised (4.5-11.2 mm/s)
Zone D: Damage imminent; immediate corrective action required (>11.2 mm/s)

Values vary by machine type and foundation:
- Small machines (<15 kW): lower thresholds (Zone C begins at 2.8 mm/s)
- Large machines (>300 kW): higher thresholds (Zone C begins at 7.1 mm/s)
- Rigid foundation: lower tolerance than flexible foundation

Measurement Parameters:
1. Velocity (mm/s or in/sec RMS):
   - Overall indicator: 10 Hz - 1000 Hz frequency range
   - Most common metric for rotating machinery condition assessment
   - RMS (Root Mean Square) value used for severity comparison

2. Displacement (mils or μm peak-to-peak):
   - Low-frequency faults: imbalance, misalignment (typically <300 Hz)
   - Shaft position relative to bearing
   - Critical for low-speed equipment (<600 RPM)

3. Acceleration (g or m/s² peak):
   - High-frequency faults: bearing defects, gear mesh (>1000 Hz)
   - Early detection of bearing failures (captures impact pulses)
   - Envelope analysis for bearing diagnostics

Fault Frequency Analysis:

1. Imbalance:
   - Signature: 1× running speed (fundamental frequency) dominates spectrum
   - Causes: material buildup, missing balance weight, thermal distortion
   - Phase relationship: in-phase vibration in horizontal and vertical directions
   - Correction: balance rotor (static or dynamic balancing)

2. Misalignment:
   - Signature: 2× running speed (second harmonic) elevated, may have 3×
   - Causes: improper coupling installation, thermal growth, foundation settling
   - Axial vibration component significant (thrust in axial direction)
   - Correction: precision shaft alignment (laser alignment within 0.002" TIR)

3. Bearing Defects:
   - Signatures: Ball Pass Frequency Outer Race (BPFO), Ball Pass Frequency Inner Race (BPFI),
                Ball Spin Frequency (BSF), Fundamental Train Frequency (FTF)
   - Calculation: depends on bearing geometry (number of balls, pitch diameter, contact angle)
   - Early detection: envelope analysis (demodulation) reveals bearing fault frequencies
   - Progression: Stage 1 (ultrasonic), Stage 2 (high frequency), Stage 3 (broadband increase),
                  Stage 4 (low frequency dominance = catastrophic failure imminent)

4. Mechanical Looseness:
   - Signature: multiple harmonics (2×, 3×, 4× running speed), non-synchronous peaks
   - Causes: loose bolts, worn bearings, excessive bearing clearance
   - Time waveform: "clipping" or truncated peaks (impact events)
   - Correction: tighten bolts, replace worn components, reduce clearances

Monitoring Strategy:

Baseline Establishment:
- Collect vibration data on new or newly-repaired equipment (Zone A reference)
- Measure at consistent locations: bearing housings, pedestal, motor body
- Three directions: horizontal, vertical, axial (full machine condition picture)
- Record operating conditions: load, speed, temperature

Trending and Alarm Limits:
- Monthly surveys for critical equipment (mud pumps, prime movers, generators)
- Quarterly for non-critical rotating equipment (cooling fans, small pumps)
- Alert alarm: 50% increase from baseline OR enter Zone C
- Danger alarm: 100% increase from baseline OR enter Zone D
- Trending software: track overall levels, spectrum changes, bearing fault energy

Predictive Maintenance Benefits:
- Early fault detection: 4-8 weeks warning before catastrophic failure
- Planned repairs: order parts, schedule downtime during planned outage (avoid NPT)
- Root cause analysis: spectrum and phase data identify specific fault type
- Cost avoidance: prevent secondary damage (bearing failure → shaft damage)

Oilfield Equipment-Specific Considerations:

Mud Pumps:
- High cyclic loading (300-120 SPM piston reciprocation)
- Bearing defects common (thrust bearing, crankshaft main bearings)
- Fluid end vibration: monitor for liner/piston wear (increased clearance = looseness signature)
- Alert: >7 mm/s velocity overall (Zone C entry for large pump)

Prime Movers (CAT 3512/3516, Cummins QSK):
- Torsional vibration in crankshaft (not detectable with accelerometers on block)
- Turbocharger bearing failures common (high-speed 20,000+ RPM)
- Monitor at turbo bearing housing: alert >4.5 mm/s for turbo-specific issues
- Engine mounts: check for looseness (multiple harmonics indicate mount degradation)

Generators:
- Electrical signature: 2× line frequency (120 Hz for 60 Hz systems) indicates electrical fault
- Rotor bars: broken bars create sidebands around running speed
- Coupling misalignment to engine: common cause of elevated 2× running speed

Centrifugal Compressors/Pumps:
- Impeller imbalance: 1× running speed dominant
- Cavitation: broadband high-frequency energy (2000-5000 Hz)
- Surge: low-frequency pulsation (<10 Hz), destructive to seals and bearings

Portable Analyzer vs. Continuous Monitoring:
- Portable: handheld data collector, route-based surveys, lower cost
- Continuous: permanently installed sensors, real-time alarms, higher cost
- Critical equipment justifies continuous (mud pumps, main power generation)
- General equipment suitable for portable route monitoring (monthly surveys)
        """,
        key_factors=[
            "ISO 10816 severity zones: A (new), B (acceptable), C (marginal), D (unacceptable)",
            "Velocity (mm/s RMS) primary metric for overall machine condition (10-1000 Hz)",
            "Fault signatures: 1× imbalance, 2× misalignment, bearing frequencies for defects",
            "Monthly trending detects faults 4-8 weeks before catastrophic failure",
            "Alert alarm at 50% increase from baseline or Zone C entry",
            "Critical equipment (pumps, engines, generators) requires monthly vibration surveys",
            "Envelope analysis for early bearing fault detection (high-frequency impacts)"
        ],
        primary_authority=[
            "ISO 10816-1 Mechanical Vibration - General Guidelines",
            "ISO 10816-3 Industrial Machines with Nominal Power Above 15 kW",
            "ISO 20816 (replacement series for ISO 10816)",
            "Mobius Institute Category II-IV Vibration Analysis Certification Standards",
            "API 670 Machinery Protection Systems (continuous monitoring)"
        ],
        burden_holder="Maintenance organization responsible for establishing monitoring program; vibration analyst interprets data and recommends actions",
        adversary_position="Vibration monitoring is expensive overhead; run-to-failure cheaper for non-critical equipment",
        counter_arguments=[
            "Critical equipment failure causes NPT far exceeding monitoring costs",
            "Secondary damage from catastrophic failures increases repair costs 3-10×",
            "Portable route monitoring cost-effective for large equipment populations"
        ],
        resolution_strategy="Implement tiered monitoring: continuous for critical (pumps, engines), monthly portable for important, quarterly for general; always trend and set alarms",
        equipment_scope=[
            EquipmentCategory.MUD_PUMP,
            EquipmentCategory.PRIME_MOVER,
            EquipmentCategory.GENERATOR,
            EquipmentCategory.ROTATING_EQUIPMENT
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for ISO 10816 severity criteria and fault frequency analysis; monitoring interval requires risk assessment per equipment criticality",
        controlling_precedent="ISO 10816 internationally recognized standard for machinery vibration limits; API 670 for continuous monitoring on critical equipment"
    ),

    DoctrineBlock(
        topic="OIL_ANALYSIS_PROGRAMS",
        keywords=["oil analysis", "wear metals", "TBN", "viscosity", "contamination", "ISO 4406", "trending"],
        conclusion_template=[
            "Oil analysis programs track wear metals (Fe, Cu, Cr, Al), contamination (Si, water), and oil condition (TBN, viscosity, oxidation) to detect developing failures and extend drain intervals.",
            "Sampling frequency: every oil change initially, then every 250-500 hours for engines and hydraulic systems in severe service.",
            "Trending data enables predictive maintenance and interval extensions: stable metals + TBN >50% of new oil = safe to extend drain."
        ],
        reasoning_framework="""
Oil analysis is the most cost-effective condition monitoring technique for lubricated equipment,
providing early warning of developing failures and enabling data-driven oil change intervals:

Critical Test Parameters:

1. Wear Metals (ICP or RDE spectrometry):
   Iron (Fe):
   - Sources: cylinder liners, piston rings, gears, bearings (ferrous components)
   - Normal: <50 ppm for engines, <100 ppm for gearboxes
   - Alert: >100 ppm or 50% increase from baseline
   - Abnormal: >200 ppm indicates severe wear or component failure imminent

   Copper (Cu):
   - Sources: bearings (bronze/brass), bushings, cooler tubes
   - Normal: <20 ppm for engines, <50 ppm for gearboxes
   - Alert: >50 ppm or doubling from baseline
   - Abnormal: >100 ppm indicates bearing wear or corrosion

   Chromium (Cr):
   - Sources: piston rings, cylinder liners (hard chrome plating)
   - Normal: <5 ppm
   - Alert: >10 ppm indicates ring/liner wear
   - Often increases with iron (both from cylinder wear)

   Aluminum (Al):
   - Sources: pistons, thrust washers, dirt contamination
   - Normal: <10 ppm
   - Alert: >20 ppm from pistons, >30 ppm may be dirt (Si correlation)

   Lead (Pb):
   - Sources: bearing overlays (babbitt), solder, fuel additives (legacy)
   - Normal: <20 ppm
   - Alert: >50 ppm indicates bearing wear

   Tin (Sn):
   - Sources: bearing overlays (babbitt)
   - Normal: <10 ppm
   - Alert: >20 ppm indicates bearing wear (often correlates with Cu and Pb)

2. Contaminants:
   Silicon (Si):
   - Sources: dirt ingestion (silica/sand), antifreeze (silicate-based), silicone sealers
   - Normal: <15 ppm
   - Alert: >30 ppm indicates air filtration failure or coolant leak
   - Trend: sudden increase = air filter element failure; gradual = poor sealing

   Water (Karl Fischer method):
   - Normal: <200 ppm (0.02%) for engines, <500 ppm for hydraulics
   - Alert: >500 ppm accelerates oxidation and bearing corrosion
   - Sources: coolant leak, condensation, water ingress through breathers
   - Emulsified water most damaging (can't settle out)

   Fuel Dilution (flashpoint or IR):
   - Normal: <1% for diesel engines
   - Alert: >2% reduces viscosity and lubricating film strength
   - Sources: injector leakage, incomplete combustion, excessive idling
   - Detection: flashpoint depression (lower flashpoint = fuel present)

3. Oil Condition:
   Total Base Number (TBN):
   - Measures alkaline reserve (neutralizes combustion acids)
   - New oil: 8-12 TBN for diesel engines, 6-8 for gasoline
   - Change oil when: TBN <50% of new oil (depletion indicates end of useful life)
   - High-sulfur fuel (>0.5% S) depletes TBN faster

   Viscosity (@ 40°C or 100°C):
   - Critical parameter: must stay within ±10% of new oil spec
   - Increase: oxidation, soot, contamination (thickening)
   - Decrease: fuel dilution, shear breakdown (polymer viscosity improvers)
   - Out-of-spec viscosity = immediate oil change required

   Oxidation (IR spectroscopy):
   - Measures carbonyl compounds from oil degradation
   - Increases with temperature and time
   - Alert: >25 abs/cm indicates significant oxidation
   - Leads to viscosity increase, deposits, acid formation

   Nitration (IR spectroscopy):
   - Measures nitration products (combustion byproducts in engines)
   - Increases in high-temperature engines
   - Alert: >20 abs/cm
   - Correlates with soot loading and TBN depletion

   Soot (IR spectroscopy):
   - Measures carbon particulates from incomplete combustion
   - Normal: <2% for diesel engines
   - Alert: >3% causes viscosity increase and abrasive wear
   - High soot: check air/fuel ratio, injector spray pattern

4. Particle Count (ISO 4406 code):
   Measures contamination by particle size: >4μm, >6μm, >14μm
   ISO cleanliness code: 18/16/13 typical target for hydraulics
   Example: 20/18/15 = >100,000 particles >4μm (unacceptable for servo valves)

   Target cleanliness by system type:
   - Servo hydraulics: 16/14/11 (very clean)
   - General hydraulics: 18/16/13
   - Gearboxes: 20/18/15
   - Engines: not typically specified (blow-by contamination inherent)

Sampling Best Practices:
- Sample port location: mid-stream flow during operation (not bottom of sump)
- Avoid sampling from drain plug (captures settled debris, not representative)
- Sampling interval: every oil change until baseline established
- Severe service: every 250 hours (engines), every 500 hours (hydraulics)
- Light service: every 500-1000 hours
- Always sample same location for trending consistency

Trending and Diagnostics:
- Single sample = limited value; trend analysis = predictive power
- Establish baseline: 3-5 samples at normal intervals
- Statistical limits: ±2 standard deviations from mean = normal variation
- Sudden change: >50% increase in any parameter = investigate immediately
- Gradual change: linear increase within limits = acceptable wear pattern

Interval Extension Strategy:
Phase 1: Follow OEM intervals with oil analysis at every change
Phase 2: If results favorable (metals stable, TBN >50%, viscosity in-spec), extend 25%
Phase 3: Continue extensions until limits reached or analysis shows degradation
Phase 4: Optimize interval = maximum safe extension (typically 50-100% OEM interval)

Example: CAT 3512 engine
- OEM interval: 500 hours
- Phase 1: 500 hours × 5 samples (establish baseline)
- Phase 2: extend to 625 hours if all parameters acceptable
- Phase 3: extend to 750 hours if still acceptable
- Phase 4: settle at 750 hours or back off to 625 if limits approached

Cost-Benefit Analysis:
- Oil analysis cost: $25-$50 per sample
- Engine oil change cost: $500-$1500 (oil + filter + labor)
- Avoided failure cost: $5,000-$50,000 (engine rebuild or replacement)
- Interval extension savings: 25-50% reduction in oil change costs
- ROI: 10:1 to 50:1 (analysis cost vs failure avoidance + interval extension)

Diagnostic Case Studies:

Case 1: Bearing Failure Warning
- Sample: Cu 15 ppm → 30 ppm → 65 ppm → 120 ppm over 4 samples
- Pb and Sn also increasing (bearing overlay metals)
- Action: Inspect bearings at next scheduled maintenance (found spalling)
- Avoided catastrophic failure and secondary damage

Case 2: Coolant Leak Detection
- Sample: Si suddenly increases from 10 ppm to 85 ppm
- Glycol test positive (silicate-based antifreeze)
- Action: Pressure test cooling system, found leaking head gasket
- Avoided oil emulsification and bearing damage

Case 3: Air Filter Failure
- Sample: Si gradual increase from 8 ppm → 20 ppm → 45 ppm
- Al also increasing (dirt ingestion)
- Action: Inspect air filtration, found torn filter element
- Replaced filter, Si returned to normal within 2 oil changes

Case 4: Interval Extension Success
- Engine: stable Fe <30 ppm, Cu <10 ppm, TBN declining 1.5 units per 500 hours
- Starting TBN 10 → 8.5 @ 500 hrs → 7.0 @ 1000 hrs
- Extended interval to 750 hours (TBN still >5.0, metals stable)
- Saved 1 oil change per 3000 hours operation (33% reduction)
        """,
        key_factors=[
            "Trending wear metals (Fe, Cu, Cr, Al) detects developing failures 1000+ hours early",
            "TBN depletion to 50% of new oil indicates oil change needed (acid neutralization capacity)",
            "Viscosity must remain within ±10% of specification (lubricating film integrity)",
            "Silicon trending detects air filtration failures (dirt ingestion)",
            "Oil analysis every 250-500 hours in severe service for predictive maintenance",
            "Interval extensions justified with stable metals + adequate TBN + in-spec viscosity",
            "Cost-benefit: $25-50 analysis vs $500-1500 oil change vs $5000-50000 failure"
        ],
        primary_authority=[
            "ASTM D6224 Standard Practice for In-Service Monitoring of Lubricating Oil",
            "ASTM D7720 Standard Practice for Stationary Hydraulic Fluid Analysis",
            "ISO 4406 Hydraulic Fluid Cleanliness Code",
            "SAE J300 Engine Oil Viscosity Classification",
            "Caterpillar SOS Services Technical Bulletins (SEBF8229)"
        ],
        burden_holder="Equipment owner responsible for establishing oil analysis program; lab provides test results and recommendations; maintenance decides actions",
        adversary_position="Oil analysis is unnecessary expense; follow fixed OEM intervals regardless of condition",
        counter_arguments=[
            "Oil analysis cost $25-50/sample justified by single avoided failure ($5000-50000)",
            "Interval extensions from analysis data reduce oil consumption and disposal costs",
            "Trending data provides forensic evidence for warranty claims and failure investigations"
        ],
        resolution_strategy="Implement oil analysis on all critical equipment (engines, hydraulics, gearboxes); sample every oil change initially; extend intervals with favorable trending data; maintain consistent sampling",
        equipment_scope=[
            EquipmentCategory.PRIME_MOVER,
            EquipmentCategory.GENERATOR,
            EquipmentCategory.MUD_PUMP,
            EquipmentCategory.ROTATING_EQUIPMENT,
            EquipmentCategory.DRILLING_RIG
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for wear metal interpretation and TBN trending; interval extensions require equipment-specific validation with data",
        controlling_precedent="ASTM standards establish test methods and interpretation; OEM technical bulletins provide equipment-specific limits and trending guidance"
    ),

    DoctrineBlock(
        topic="RCM_RELIABILITY_CENTERED_MAINTENANCE",
        keywords=["RCM", "reliability", "FMEA", "criticality", "failure modes", "MSG-3", "preventive", "predictive"],
        conclusion_template=[
            "Reliability-Centered Maintenance (RCM) optimizes maintenance strategies by analyzing failure modes, criticality, and task effectiveness rather than applying fixed intervals.",
            "RCM methodology: identify functions, functional failures, failure modes, failure effects, criticality ranking, and select optimal maintenance tasks.",
            "Results in multi-strategy approach: time-based for age-related failures, condition-based for detectable degradation, run-to-failure for low-criticality non-safety items."
        ],
        reasoning_framework="""
RCM is a systematic approach for determining optimal maintenance requirements based on
equipment functions, failure modes, and consequences. Developed for aviation (MSG-3),
widely adopted in oil & gas, power generation, and process industries.

RCM Methodology (SAE JA1011 Standard):

Phase 1: Equipment/System Selection
- Identify critical equipment for RCM analysis (high-value, safety-critical, high-failure-cost)
- Not all equipment justifies full RCM (cost-benefit analysis)
- Typical candidates: drilling rigs (BOP, drawworks, top drive), production facilities (compressors,
  separators), power generation (prime movers, generators)

Phase 2: Functional Analysis
Define what the equipment is supposed to do:
- Primary functions: design intent (BOP isolates wellbore annulus, drawworks hoists drill string)
- Secondary functions: safety, environmental, comfort (BOP control panel monitoring, acoustic alarms)
- Performance standards: quantify acceptable function (BOP holds 15,000 psi for 30 min)

Phase 3: Functional Failure Analysis
Identify ways each function can fail:
- Total failure: complete inability to perform function (BOP won't close)
- Partial failure: degraded performance (BOP closes slowly, leaks during test)
- Example: BOP primary function = "Isolate wellbore to rated pressure"
  - Functional failures: won't close, won't hold pressure, leaks through seals, closes partially

Phase 4: Failure Mode and Effects Analysis (FMEA)
For each functional failure, identify specific failure modes:
- Failure mode: specific way the functional failure occurs (ram seal degradation, hydraulic leak,
  control pod solenoid failure, accumulator pre-charge loss, ram block cracking)
- Failure cause: root cause of the failure mode (seal hardening from heat, vibration fatigue,
  contaminated hydraulic fluid, nitrogen leak, stress corrosion cracking)
- Failure effect: consequences if failure mode occurs (loss of well control, personnel injury,
  environmental release, NPT, equipment damage)

Phase 5: Criticality Ranking (Consequence Assessment)
Rate failure modes by consequences (SAE JA1011 categories):

1. Hidden failures (H):
   - Not evident to operators during normal operation
   - Protective devices, backup systems, redundant components
   - Example: BOP backup control pod failure (primary pod still functional)
   - Highest priority for periodic inspection/testing

2. Safety consequences (S):
   - Could cause injury or death
   - Example: BOP ram seal failure under pressure (sudden release, well control loss)
   - Second priority after hidden failures

3. Environmental consequences (E):
   - Could cause environmental damage or regulatory violation
   - Example: hydraulic fluid spill from BOP power unit leak
   - Third priority

4. Operational consequences (O):
   - Directly impacts production, availability, or operating costs
   - Example: BOP test failure causes NPT (delay drilling operations)
   - Fourth priority

5. Non-operational consequences (N):
   - Only involves cost of repair (no safety, environmental, or operational impact)
   - Example: BOP control panel cosmetic damage
   - Lowest priority

Phase 6: Maintenance Task Selection
For each failure mode, select the most effective and economical task:

Task Categories (in order of preference):

1. Condition-Directed (On-Condition):
   - Monitor for detectable degradation (vibration, oil analysis, thermography, thickness)
   - Intervene when condition reaches defined limit (before functional failure)
   - Applicable when: degradation detectable, sufficient P-F interval (time from detection to failure)
   - Example: BOP hydraulic fluid analysis for contamination trending

2. Time-Directed (Preventive):
   - Scheduled restoration or discard at defined interval
   - Applicable when: age-related failure pattern exists, defined useful life known
   - Example: BOP ram seal replacement every 5 years (elastomer aging regardless of cycles)

3. Failure-Finding (Hidden Function Testing):
   - Periodic inspection or test to detect hidden failures
   - Applicable when: failure mode is hidden, no condition monitoring feasible
   - Example: BOP backup control pod function test every 2 weeks

4. Run-to-Failure (No Scheduled Maintenance):
   - Allow failure to occur, then repair
   - Applicable when: failure consequence acceptable (non-operational), PM not effective or cost-justified
   - Example: BOP control panel indicator light (replace when burned out, no PM needed)

5. One-Time Change (Design Improvement):
   - Modify equipment to eliminate or reduce failure mode
   - Example: Upgrade BOP seals to higher temperature rating (eliminate heat degradation)

RCM Task Effectiveness Criteria:

Applicable: Must address the failure mode (reduce probability or consequence)
Effective: Must actually prevent or detect the failure (proven track record or engineering analysis)
Cost-effective: Must be economically justified compared to consequences and alternative tasks

Example RCM Analysis - BOP Ram Preventers:

| Failure Mode | Consequence | Task Type | Task | Interval | Justification |
|--------------|-------------|-----------|------|----------|---------------|
| Ram seal leak | S (safety) | Time-Directed | Replace ram seals | 5 years or 1000 closures | Elastomer aging curve |
| Control pod solenoid fail | H (hidden) | Failure-Finding | Function test all pods | Bi-weekly | Detect hidden failures |
| Hydraulic fluid contamination | O (operational) | Condition-Directed | Fluid analysis | Quarterly | Trend ISO code, moisture |
| Accumulator pre-charge loss | H (hidden) | Failure-Finding | Pressure check all bottles | Weekly | Detect slow nitrogen leaks |
| Ram block cracking | S (safety) | Failure-Finding | MT inspection ram cavity | Annual tear-down | Detect fatigue cracks early |
| Annular element tear | S (safety) | Time-Directed | Replace element | 5 years max | Erosion/degradation |
| Pressure gauge inaccuracy | N (non-op) | Condition-Directed | Calibration check | Annual | Maintain accuracy for tests |

Benefits of RCM Approach:

1. Optimal Resource Allocation:
   - Focus intensive PM on high-criticality failure modes (safety, hidden)
   - Reduce or eliminate PM on low-consequence modes (run-to-failure acceptable)
   - Example: Deep analysis on BOP (safety-critical) vs. minimal PM on paint condition (cosmetic)

2. Evidence-Based Decision Making:
   - Maintenance tasks selected based on failure mode analysis, not tradition or OEM generic recommendations
   - Justification for deviations from OEM intervals (if RCM analysis supports)
   - Example: Extend oil change from 500 to 750 hours based on oil analysis trending (condition-directed)

3. Living Program:
   - RCM analysis updated with operating experience and failure data
   - Adjust tasks/intervals as failure patterns emerge
   - Example: If BOP ram seals consistently fail at 800 closures, reduce interval from 1000 to 600

4. Multi-Strategy Integration:
   - Combines time-based, condition-based, run-to-failure, and failure-finding in optimal mix
   - Not "one size fits all" - tailored to each failure mode
   - Example: Same BOP system uses all four strategies for different failure modes

Implementation Challenges:

1. Resource Intensive:
   - Full RCM analysis requires cross-functional team (operations, maintenance, engineering)
   - Time requirement: 40-80 hours per major equipment system
   - Specialized training required (RCM facilitators, FMEA expertise)

2. Data Requirements:
   - Requires failure history data to identify patterns (may not exist for new equipment)
   - Condition monitoring infrastructure needed (sensors, trending software, analysis capability)

3. Organizational Resistance:
   - "We've always done it this way" mentality
   - Requires cultural shift from reactive to proactive maintenance
   - Management commitment essential (resource allocation for analysis and implementation)

RCM-Derived Maintenance Strategies (Typical Oilfield Equipment):

Drilling Rig:
- BOP: Multi-strategy (time-based seals, condition-based fluid, failure-finding tests, run-to-failure cosmetics)
- Drawworks: Time-based brake bands, condition-based vibration, failure-finding load tests
- Top Drive: Condition-based bearing vibration, time-based gearbox oil change with analysis extensions
- Mud Pumps: Condition-based fluid end (vibration/efficiency trending), time-based expendables with adjustments

Production Facility:
- Compressors: Condition-based (vibration, oil analysis, thermography), time-based valve overhauls
- Separators: Time-based internal inspection with RBI extensions, failure-finding relief valve tests
- Pumps: Condition-based (vibration, seal leakage, performance trending)

Power Generation:
- Prime Movers: Condition-based oil analysis with interval extensions, time-based valve adjustments
- Generators: Condition-based vibration and electrical testing, time-based winding insulation tests

RCM Simplification (Streamlined RCM for smaller equipment):
- Focus on critical few failure modes (Pareto principle: 20% of modes cause 80% of consequences)
- Use standardized templates for similar equipment (fleet analysis vs. individual units)
- Risk-based prioritization (analyze high-risk equipment first)
        """,
        key_factors=[
            "RCM optimizes maintenance by analyzing failure modes and consequences, not applying generic intervals",
            "Five task types: condition-directed (preferred), time-directed, failure-finding, run-to-failure, design-out",
            "Consequence categories: Hidden (H), Safety (S), Environmental (E), Operational (O), Non-operational (N)",
            "Multi-strategy results: time-based for age-related, condition-based for detectable, run-to-failure for acceptable consequences",
            "Living program: update tasks and intervals based on operating experience and failure data",
            "Resource intensive: 40-80 hours analysis per major system, requires cross-functional team",
            "Streamlined RCM for smaller equipment: focus on critical few failure modes, use templates"
        ],
        primary_authority=[
            "SAE JA1011 Evaluation Criteria for Reliability-Centered Maintenance (RCM) Processes",
            "SAE JA1012 Guide to the Reliability-Centered Maintenance (RCM) Standard",
            "MSG-3 Operator/Manufacturer Scheduled Maintenance Development (aviation origin)",
            "MIL-STD-2173 Reliability-Centered Maintenance Requirements for Naval Aircraft",
            "ISO 14224 Petroleum, Petrochemical and Natural Gas Industries - Collection and Exchange of Reliability Data"
        ],
        burden_holder="Equipment owner/operator responsible for RCM analysis and implementation; maintenance organization executes derived tasks; engineering validates effectiveness",
        adversary_position="RCM is academic exercise; traditional time-based PM simpler and adequate for most equipment",
        counter_arguments=[
            "RCM resource investment justified by improved reliability and reduced total maintenance cost",
            "Critical equipment failures in oilfield operations far exceed RCM analysis costs",
            "Hybrid approach: full RCM for critical, streamlined RCM for important, traditional PM for general equipment"
        ],
        resolution_strategy="Implement tiered RCM: full analysis for safety-critical and high-value equipment (BOP, top drive, prime movers); streamlined for important equipment (pumps, compressors); traditional PM for low-criticality items",
        equipment_scope=[
            EquipmentCategory.BOP_SYSTEM,
            EquipmentCategory.DRILLING_RIG,
            EquipmentCategory.MUD_PUMP,
            EquipmentCategory.PRIME_MOVER,
            EquipmentCategory.GENERATOR,
            EquipmentCategory.PRESSURE_VESSEL,
            EquipmentCategory.ROTATING_EQUIPMENT
        ],
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="High confidence for RCM methodology and task selection logic; implementation requires equipment-specific analysis and organizational commitment",
        controlling_precedent="SAE JA1011/JA1012 define RCM standard methodology; MSG-3 established in aviation, adopted across industries for safety-critical equipment"
    ),
]


# ============================================================================
# ENGINE CORE LOGIC
# ============================================================================

class OFE07MaintenanceEngine:
    """OFE07 Preventive Maintenance Scheduling Intelligence Engine"""

    def __init__(self):
        self.version = "1.0.0"
        self.port = 9007
        self.doctrine_cache = DOCTRINE_CACHE
        self.telemetry: List[TelemetryEntry] = []
        self.start_time = datetime.now()

        logger.info(f"OFE07 Preventive Maintenance Engine v{self.version} initialized")
        logger.info(f"Loaded {len(self.doctrine_cache)} doctrine blocks")

    def three_layer_response(
        self,
        query: str,
        mode: ResponseMode,
        equipment_type: Optional[EquipmentCategory],
        zone: AnalysisZone
    ) -> MaintenanceQueryResponse:
        """
        Three-layer response architecture:
        Layer 1: Doctrine Cache (0-200ms) - Pre-compiled expert blocks
        Layer 2: Semantic Retrieval (200-2000ms) - Vector search (if implemented)
        Layer 3: Deep Analysis (2000ms+) - Multi-source synthesis
        """
        start_time = datetime.now()
        query_id = hashlib.sha256(f"{query}{start_time.isoformat()}".encode()).hexdigest()[:16]

        # Layer 1: Doctrine Cache Lookup
        triggered_doctrines = self._search_doctrine_cache(query, equipment_type)

        if triggered_doctrines:
            # Cache hit - fast response
            response = self._compile_doctrine_response(triggered_doctrines, mode, zone)
            cache_hit = True
            logger.info(f"Cache hit: {len(triggered_doctrines)} doctrines triggered")
        else:
            # Cache miss - generate analysis
            response = self._generate_analysis(query, mode, equipment_type, zone)
            cache_hit = False
            logger.warning(f"Cache miss for query: {query[:100]}")

        latency_ms = (datetime.now() - start_time).total_seconds() * 1000

        # Extract applied doctrines and authorities
        doctrines_applied = [d.topic for d in triggered_doctrines] if triggered_doctrines else []
        authorities = self._extract_authorities(triggered_doctrines) if triggered_doctrines else []
        equipment_categories = self._extract_equipment_categories(triggered_doctrines) if triggered_doctrines else []

        # Determine confidence level
        confidence = triggered_doctrines[0].confidence if triggered_doctrines else ConfidenceLevel.DISCLOSURE

        # Generate determinism hash
        determinism_hash = hashlib.sha256(
            f"{query}{mode}{equipment_type}{zone}{response}".encode()
        ).hexdigest()[:16]

        # Record telemetry
        self._record_telemetry(
            query_id=query_id,
            response_mode=mode,
            doctrines_triggered=doctrines_applied,
            cache_hit=cache_hit,
            latency_ms=latency_ms,
            equipment_categories=equipment_categories,
            confidence_level=confidence.value,
            zone=zone
        )

        return MaintenanceQueryResponse(
            query_id=query_id,
            response=response,
            mode=mode,
            confidence=confidence,
            doctrines_applied=doctrines_applied,
            authorities_cited=authorities,
            equipment_categories=equipment_categories,
            latency_ms=round(latency_ms, 2),
            determinism_hash=determinism_hash,
            timestamp=datetime.now().isoformat(),
            disclosure=self._generate_disclosure(confidence, zone) if zone == AnalysisZone.AUDIT else None
        )

    def _search_doctrine_cache(
        self,
        query: str,
        equipment_type: Optional[EquipmentCategory]
    ) -> List[DoctrineBlock]:
        """Search doctrine cache for relevant blocks"""
        query_lower = query.lower()
        matched_doctrines = []

        for doctrine in self.doctrine_cache:
            # Check equipment type match if specified
            if equipment_type and equipment_type not in doctrine.equipment_scope:
                continue

            # Check keyword match
            keyword_matches = sum(1 for kw in doctrine.keywords if kw.lower() in query_lower)
            if keyword_matches > 0:
                matched_doctrines.append((doctrine, keyword_matches))

        # Sort by match score and return top matches
        matched_doctrines.sort(key=lambda x: x[1], reverse=True)
        return [d[0] for d in matched_doctrines[:3]]  # Top 3 most relevant

    def _compile_doctrine_response(
        self,
        doctrines: List[DoctrineBlock],
        mode: ResponseMode,
        zone: AnalysisZone
    ) -> str:
        """Compile response from triggered doctrine blocks"""
        if mode == ResponseMode.FAST:
            # Concise response - just conclusions
            conclusions = []
            for doctrine in doctrines:
                conclusions.extend(doctrine.conclusion_template)
            return " ".join(conclusions[:3])  # Top 3 conclusions

        elif mode == ResponseMode.DEFENSE:
            # Detailed response with authorities
            sections = []
            for doctrine in doctrines:
                section = f"**{doctrine.topic}**\n\n"
                section += "\n".join(doctrine.conclusion_template) + "\n\n"
                section += f"**Key Factors:**\n" + "\n".join(f"- {kf}" for kf in doctrine.key_factors[:5]) + "\n\n"
                section += f"**Authorities:** {', '.join(doctrine.primary_authority)}\n"
                sections.append(section)
            return "\n\n".join(sections)

        else:  # MEMO mode
            # Full documentation with reasoning
            sections = []
            for doctrine in doctrines:
                section = f"# {doctrine.topic}\n\n"
                section += "## Conclusion\n" + "\n".join(doctrine.conclusion_template) + "\n\n"
                section += f"## Reasoning Framework\n{doctrine.reasoning_framework}\n\n"
                section += f"## Key Factors\n" + "\n".join(f"- {kf}" for kf in doctrine.key_factors) + "\n\n"
                section += f"## Primary Authority\n" + "\n".join(f"- {auth}" for auth in doctrine.primary_authority) + "\n\n"
                section += f"## Resolution Strategy\n{doctrine.resolution_strategy}\n"
                sections.append(section)
            return "\n\n---\n\n".join(sections)

    def _generate_analysis(
        self,
        query: str,
        mode: ResponseMode,
        equipment_type: Optional[EquipmentCategory],
        zone: AnalysisZone
    ) -> str:
        """Generate analysis when no doctrine cache hit"""
        # Fallback response when cache misses
        return (
            f"Analysis for: {query}\n\n"
            f"This query did not match pre-compiled maintenance doctrines. "
            f"For equipment-specific maintenance scheduling guidance, please provide:\n"
            f"- Equipment type (rig component, pump, engine, vessel, etc.)\n"
            f"- Specific maintenance concern (intervals, methods, acceptance criteria)\n"
            f"- Operating conditions and service severity\n\n"
            f"The OFE07 engine specializes in preventive maintenance scheduling per API, "
            f"ASME, ISO, and OEM standards for oilfield equipment."
        )

    def _extract_authorities(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract unique authorities from doctrines"""
        authorities = set()
        for doctrine in doctrines:
            authorities.update(doctrine.primary_authority)
        return sorted(list(authorities))

    def _extract_equipment_categories(self, doctrines: List[DoctrineBlock]) -> List[str]:
        """Extract equipment categories from doctrines"""
        categories = set()
        for doctrine in doctrines:
            categories.update([eq.value for eq in doctrine.equipment_scope])
        return sorted(list(categories))

    def _generate_disclosure(self, confidence: ConfidenceLevel, zone: AnalysisZone) -> str:
        """Generate disclosure statement based on confidence and zone"""
        if confidence == ConfidenceLevel.HIGH_RISK or zone == AnalysisZone.AUDIT:
            return (
                "DISCLOSURE: This analysis is for informational purposes only and does not "
                "constitute professional engineering advice. Maintenance intervals and methods "
                "must be validated by qualified personnel considering specific operating conditions, "
                "regulatory requirements, and manufacturer recommendations. Always consult with "
                "certified inspectors and licensed engineers for critical equipment maintenance decisions."
            )
        return None

    def _record_telemetry(
        self,
        query_id: str,
        response_mode: ResponseMode,
        doctrines_triggered: List[str],
        cache_hit: bool,
        latency_ms: float,
        equipment_categories: List[str],
        confidence_level: str,
        zone: AnalysisZone
    ):
        """Record telemetry entry"""
        entry = TelemetryEntry(
            query_id=query_id,
            timestamp=datetime.now(),
            response_mode=response_mode,
            doctrines_triggered=doctrines_triggered,
            cache_hit=cache_hit,
            latency_ms=latency_ms,
            equipment_categories=equipment_categories,
            confidence_level=confidence_level,
            zone=zone
        )
        self.telemetry.append(entry)

        # Keep only last 1000 entries
        if len(self.telemetry) > 1000:
            self.telemetry = self.telemetry[-1000:]

    def get_health(self) -> HealthResponse:
        """Comprehensive health check"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        total_queries = len(self.telemetry)
        avg_latency = (
            sum(t.latency_ms for t in self.telemetry) / total_queries
            if total_queries > 0 else 0.0
        )

        return HealthResponse(
            status="healthy",
            version=self.version,
            port=self.port,
            doctrines_loaded=len(self.doctrine_cache),
            cache_size=len(self.doctrine_cache),
            uptime_seconds=round(uptime, 2),
            total_queries=total_queries,
            avg_latency_ms=round(avg_latency, 2)
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

APP = FastAPI(
    title="OFE07 - Preventive Maintenance Scheduling Engine",
    description="TIE Gold Standard Intelligence Engine for Oilfield Equipment Maintenance Management",
    version="1.0.0"
)

APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = OFE07MaintenanceEngine()


@APP.post("/query", response_model=MaintenanceQueryResponse)
async def query_maintenance(request: MaintenanceQueryRequest):
    """Process preventive maintenance scheduling query"""
    try:
        logger.info(f"Query received: {request.query[:100]}")
        response = engine.three_layer_response(
            query=request.query,
            mode=request.mode,
            equipment_type=request.equipment_type,
            zone=request.zone
        )
        return response
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@APP.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return engine.get_health()


@APP.get("/doctrines")
async def list_doctrines():
    """List all available doctrine topics"""
    return {
        "total_doctrines": len(engine.doctrine_cache),
        "doctrines": [
            {
                "topic": d.topic,
                "keywords": d.keywords,
                "equipment_scope": [eq.value for eq in d.equipment_scope],
                "confidence": d.confidence.value
            }
            for d in engine.doctrine_cache
        ]
    }


@APP.get("/")
async def root():
    """Root endpoint"""
    return {
        "engine": "OFE07 - Preventive Maintenance Scheduling Engine",
        "version": "1.0.0",
        "status": "operational",
        "doctrines_loaded": len(engine.doctrine_cache),
        "endpoints": ["/query", "/health", "/doctrines"]
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 80)
    logger.info("OFE07 - PREVENTIVE MAINTENANCE SCHEDULING ENGINE")
    logger.info("TIE Gold Standard - Oilfield Equipment Maintenance Intelligence")
    logger.info("=" * 80)
    logger.info(f"Version: 1.0.0")
    logger.info(f"Port: 9007")
    logger.info(f"Doctrines Loaded: {len(DOCTRINE_CACHE)}")
    logger.info("=" * 80)

    uvicorn.run(APP, host="0.0.0.0", port=9007, log_level="info")
