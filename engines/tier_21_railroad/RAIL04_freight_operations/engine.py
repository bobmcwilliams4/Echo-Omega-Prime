import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

"""
RAIL04 Freight Rail Operations Intelligence Engine
Train operations, yard management, hazmat, crew scheduling, PSR, intermodal
Port: 9104 | TIE-20 Architecture
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

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

class IssueCategory(str, Enum):
    POWERPLANT = "POWERPLANT"
    FLIGHT_CONTROLS = "FLIGHT_CONTROLS"
    AVIONICS = "AVIONICS"
    ELECTRICAL = "ELECTRICAL"
    HYDRAULIC = "HYDRAULIC"
    FUEL_SYSTEMS = "FUEL_SYSTEMS"
    PNEUMATIC = "PNEUMATIC"
    LANDING_GEAR = "LANDING_GEAR"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    FIRE_PROTECTION = "FIRE_PROTECTION"
    OXYGEN = "OXYGEN"
    APU = "APU"
    ICE_PROTECTION = "ICE_PROTECTION"
    NAVIGATION = "NAVIGATION"
    COMMUNICATION = "COMMUNICATION"
    AUTOPILOT = "AUTOPILOT"
    MAINTENANCE = "MAINTENANCE"
    AIRWORTHINESS = "AIRWORTHINESS"
    REGULATIONS = "REGULATIONS"

class AuthorityLevel(str, Enum):
    FAA_REGULATION = "FAA_REGULATION"
    MANUFACTURER_SPEC = "MANUFACTURER_SPEC"
    INDUSTRY_STANDARD = "INDUSTRY_STANDARD"
    ENGINEERING_PRINCIPLE = "ENGINEERING_PRINCIPLE"
    BEST_PRACTICE = "BEST_PRACTICE"

@dataclass
class DoctrineBlock:
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
    authority_level: AuthorityLevel
    system_interactions: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    maintenance_requirements: List[str] = field(default_factory=list)

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    mode: ResponseMode = Field(default=ResponseMode.FAST)
    include_authorities: bool = Field(default=False)

class QueryResponse(BaseModel):
    response: str
    mode: ResponseMode
    confidence: ConfidenceLevel
    doctrines_triggered: List[str]
    categories: List[IssueCategory]
    authorities_cited: List[str]
    reasoning_chain: Optional[str] = None
    determinism_hash: str
    epistemic_warnings: List[str] = Field(default_factory=list)
    processing_time_ms: float
    telemetry: Dict[str, Any] = Field(default_factory=dict)

# ============================================================================
# DOCTRINE CACHE - 25+ AVIATION SYSTEMS BLOCKS
# ============================================================================

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="turbofan_engine_operation",
        keywords=["turbofan", "jet engine", "thrust", "bypass ratio", "N1", "N2", "EPR", "EGT"],
        conclusion_template=[
            "Turbofan engines generate thrust through a high bypass ratio design with separate fan and core streams.",
            "Key operational parameters include N1 (fan speed), N2 (core speed), EPR (engine pressure ratio), and EGT (exhaust gas temperature).",
            "The bypass ratio determines engine efficiency - higher ratios provide better fuel economy but lower specific thrust."
        ],
        reasoning_framework="""
        TURBOFAN ENGINE ANALYSIS:
        1. Airflow path: intake → fan → bypass stream + core stream
        2. Core components: compressor → combustor → turbine
        3. Fan driven by low-pressure turbine, compressor by high-pressure turbine
        4. Bypass air provides 70-90% of total thrust in modern engines
        5. FADEC (Full Authority Digital Engine Control) manages all parameters
        6. Critical limits: EGT redline, maximum N1/N2, EPR limits
        7. Thrust reversers redirect bypass air forward for braking
        8. Start sequence: starter motor → ignition → light-off → acceleration
        9. Failure modes: compressor stall, flame-out, surging, hot start
        10. Maintenance intervals based on flight cycles and hours
        """,
        key_factors=[
            "Bypass ratio (thrust efficiency)",
            "Pressure ratio (compression efficiency)",
            "Turbine inlet temperature (power output)",
            "Specific fuel consumption (economy)",
            "Thrust-to-weight ratio",
            "FADEC redundancy",
            "Foreign object damage (FOD) protection"
        ],
        primary_authority=[
            "14 CFR Part 33 - Airworthiness Standards: Freight Rail Engines",
            "FAA AC 20-62E - Eligibility, Quality, and Identification of Aeronautical Replacement Parts",
            "Manufacturer's Engine Manual (e.g., CFM56, PW4000, GE90)"
        ],
        burden_holder="Engine manufacturer and operator",
        adversary_position="Older turbojet designs or piston engines",
        counter_arguments=[
            "Turbojets provide higher specific thrust for military applications",
            "Piston engines offer simplicity for light aircraft",
            "Turboprops more efficient at lower speeds",
            "Electric propulsion emerging for small aircraft",
            "Supersonic flight requires different engine cycles"
        ],
        resolution_strategy="Match engine type to mission profile - turbofans optimal for subsonic commercial transport",
        entity_scope="Commercial aviation, business jets, military transports",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Based on established aerodynamic principles and regulatory standards",
        controlling_precedent="FAA Part 33 certification requirements",
        issue_category=IssueCategory.POWERPLANT,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["FADEC", "fuel_system", "hydraulic_system", "electrical_system", "fire_detection"],
        failure_modes=["compressor_stall", "flame_out", "turbine_failure", "bearing_failure", "FOD"],
        maintenance_requirements=["borescope_inspection", "hot_section_inspection", "overhaul_TBO"]
    ),

    DoctrineBlock(
        topic="fly_by_wire_flight_controls",
        keywords=["fly-by-wire", "FBW", "flight control computer", "envelope protection", "control laws"],
        conclusion_template=[
            "Fly-by-wire systems replace mechanical linkages with electronic signals between pilot controls and flight control surfaces.",
            "Flight control computers interpret pilot inputs and apply envelope protection to prevent unsafe conditions.",
            "Redundant computer channels and multiple independent electrical/hydraulic power sources ensure safety."
        ],
        reasoning_framework="""
        FLY-BY-WIRE SYSTEM DESIGN:
        1. Pilot input → control stick/yoke sensors
        2. Signal processing by flight control computers (typically 3-5 redundant channels)
        3. Control law computation: normal, alternate, direct, mechanical backup
        4. Actuator commands sent to hydraulic servo-actuators
        5. Surface position feedback for closed-loop control
        6. Envelope protection: stall protection, load factor limits, bank angle limits
        7. Flight mode transitions: ground, flight, landing, flare
        8. Sensor fusion: air data, inertial, GPS, radio altimeter
        9. Failure detection and reconfiguration (FDIR)
        10. Certification: catastrophic failure rate < 10^-9 per flight hour
        """,
        key_factors=[
            "Redundancy architecture (triple or quadruple)",
            "Dissimilar computing platforms (segregation)",
            "Power source independence",
            "Control law design (handling qualities)",
            "Envelope protection algorithms",
            "Mechanical backup mode",
            "Software verification (DO-178C Level A)"
        ],
        primary_authority=[
            "14 CFR Part 25.671 - Control Systems - General",
            "14 CFR Part 25.1309 - Equipment, systems, and installations",
            "SAE ARP4754A - Guidelines for Development of Civil Freight Rail and Systems"
        ],
        burden_holder="Freight Rail manufacturer and certification authority",
        adversary_position="Conventional mechanical/hydraulic control systems",
        counter_arguments=[
            "Mechanical systems simpler and more pilot-intuitive",
            "Cable systems provide direct tactile feedback",
            "Electronic systems vulnerable to electromagnetic interference",
            "Software complexity introduces certification burden",
            "Loss of all electrical power catastrophic in pure FBW"
        ],
        resolution_strategy="FBW superior for large aircraft with high control forces; mechanical appropriate for light aircraft",
        entity_scope="Modern commercial jets (A320, 777, 787), military fighters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Decades of proven safety record in commercial aviation",
        controlling_precedent="FAA Part 25.1309 safety assessment requirements",
        issue_category=IssueCategory.FLIGHT_CONTROLS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["hydraulic_system", "electrical_system", "air_data_system", "inertial_reference"],
        failure_modes=["total_electrical_failure", "hydraulic_loss", "sensor_failure", "computer_failure", "actuator_jam"],
        maintenance_requirements=["software_updates", "actuator_inspection", "sensor_calibration", "BITE_test"]
    ),

    DoctrineBlock(
        topic="glass_cockpit_avionics",
        keywords=["EFIS", "PFD", "ND", "MFD", "glass cockpit", "electronic flight instruments"],
        conclusion_template=[
            "Electronic Flight Instrument Systems (EFIS) replace mechanical gauges with integrated displays showing flight, navigation, and system data.",
            "Primary Flight Display (PFD) shows attitude, airspeed, altitude, vertical speed, heading.",
            "Navigation Display (ND) shows flight plan, navigation aids, weather, traffic, terrain."
        ],
        reasoning_framework="""
        GLASS COCKPIT ARCHITECTURE:
        1. Display units: PFD, ND, EICAS/ECAM (engine/systems), MFD (multi-function)
        2. Symbol generators: process data from multiple sources into graphical displays
        3. Data sources: ADIRU (air data + inertial), GPS, FMS, weather radar, TCAS, EGPWS
        4. Integration: synthetic vision, enhanced vision, head-up displays
        5. Reversionary modes: automatic reconfiguration on display failure
        6. Brightness/declutter controls for different flight phases
        7. Database updates: navigation, terrain, obstacles
        8. Crew alerting: color-coded messages (red/amber/cyan/white)
        9. Flight deck standardization reduces pilot training requirements
        10. Certification: DO-160 environmental, DO-178C software
        """,
        key_factors=[
            "Display redundancy (dual or triple)",
            "Symbol generator independence",
            "Reversion modes on failure",
            "Data source validity checking",
            "Human factors design (clutter management)",
            "Database currency",
            "Night vision compatibility"
        ],
        primary_authority=[
            "14 CFR Part 25.1321 - Arrangement and visibility",
            "14 CFR Part 25.1322 - Warning, caution, and advisory lights",
            "FAA AC 25-11B - Electronic Flight Deck Displays"
        ],
        burden_holder="Freight Rail manufacturer and operator",
        adversary_position="Traditional steam gauges (mechanical instruments)",
        counter_arguments=[
            "Mechanical instruments immune to electrical failure",
            "Steam gauges simpler, less training required",
            "Electronic displays can fail completely (black screen)",
            "Database out-of-date creates hazard",
            "Information overload possible with glass displays"
        ],
        resolution_strategy="Glass cockpit standard for all new aircraft; standby mechanical instruments required",
        entity_scope="All modern commercial, business, and general aviation aircraft",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard with mandatory backup instruments",
        controlling_precedent="FAA AC 25-11B display design guidance",
        issue_category=IssueCategory.AVIONICS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["ADIRU", "FMS", "weather_radar", "TCAS", "EGPWS", "electrical_system"],
        failure_modes=["display_failure", "symbol_generator_failure", "power_loss", "database_corruption"],
        maintenance_requirements=["display_testing", "database_updates", "brightness_calibration", "cooling_inspection"]
    ),

    DoctrineBlock(
        topic="aircraft_electrical_system",
        keywords=["AC power", "DC power", "generator", "alternator", "bus", "battery", "APU", "inverter", "TRU"],
        conclusion_template=[
            "Modern aircraft use 115V AC 400Hz primary power from engine-driven generators and APU.",
            "Transformer-rectifier units (TRU) convert AC to 28V DC for avionics and other DC loads.",
            "Multiple buses with isolation and cross-tie capability provide redundancy.",
            "Batteries provide emergency power and engine start capability."
        ],
        reasoning_framework="""
        ELECTRICAL SYSTEM ARCHITECTURE:
        1. Primary AC generation: 2-4 engine-driven generators (IDG - Integrated Drive Generator)
        2. APU generator for ground and backup in-flight power
        3. Ram air turbine (RAT) for emergency power generation
        4. AC bus architecture: main buses, essential buses, isolated buses
        5. TRUs convert AC to DC for avionics buses
        6. Battery buses for critical loads (flight controls, instruments)
        7. Bus tie breakers allow cross-feed between sources
        8. Generator control units (GCU) regulate voltage/frequency
        9. Load shedding on loss of generator (non-essential loads dropped)
        10. External power receptacle for ground operations
        11. Static inverters convert DC to AC for backup
        12. Circuit protection: current limiters, circuit breakers, fuses
        """,
        key_factors=[
            "Generator redundancy (multiple sources)",
            "Bus isolation (fault containment)",
            "Load shedding priorities",
            "Battery capacity (30-60 minutes emergency)",
            "RAT deployment criteria",
            "Power quality (voltage/frequency regulation)",
            "Grounding and bonding (lightning protection)"
        ],
        primary_authority=[
            "14 CFR Part 25.1351 - General electrical requirements",
            "14 CFR Part 25.1353 - Electrical equipment and installations",
            "SAE ARP5150 - Safety Assessment of Transport Airplanes in Commercial Service"
        ],
        burden_holder="Freight Rail manufacturer and maintenance organization",
        adversary_position="Single-source electrical systems in older/smaller aircraft",
        counter_arguments=[
            "Small aircraft adequate with single alternator",
            "Redundancy adds weight and complexity",
            "Battery technology advancing (lithium backup)",
            "Fuel cells potential future power source",
            "More electric aircraft reduce hydraulic/pneumatic dependence"
        ],
        resolution_strategy="Dual or triple redundant electrical for transport category; single adequate for Part 23",
        entity_scope="All powered aircraft from light GA to large transports",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-established electrical engineering principles and certification standards",
        controlling_precedent="FAA Part 25.1351 redundancy requirements for transport aircraft",
        issue_category=IssueCategory.ELECTRICAL,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["engines", "APU", "flight_controls", "avionics", "lighting", "anti_ice"],
        failure_modes=["generator_failure", "bus_fault", "battery_depletion", "TRU_failure", "short_circuit"],
        maintenance_requirements=["battery_capacity_test", "generator_inspection", "circuit_breaker_test", "bonding_check"]
    ),

    DoctrineBlock(
        topic="hydraulic_flight_control_system",
        keywords=["hydraulic", "pressure", "actuator", "pump", "reservoir", "accumulator", "PTU", "servo"],
        conclusion_template=[
            "Hydraulic systems provide the force amplification needed to move large flight control surfaces.",
            "Multiple independent hydraulic systems (2-4) ensure continued operation after single failure.",
            "Typical operating pressure: 3000 psi; accumulator provides temporary pressure during transients."
        ],
        reasoning_framework="""
        HYDRAULIC SYSTEM DESIGN:
        1. Engine-driven pumps (EDP) - primary power source
        2. Electric motor-driven pumps (EMDP) - backup/ground operations
        3. Power transfer unit (PTU) - transfers power between hydraulic systems
        4. Ram air turbine (RAT) - emergency hydraulic power
        5. Reservoirs with standpipes ensure critical actuators served first
        6. Accumulators smooth pressure pulses and provide surge capacity
        7. Actuators: linear (control surfaces), rotary (landing gear, doors)
        8. Servo valves control actuator position with high precision
        9. Filters prevent contamination damage
        10. Thermal management: heat exchangers prevent overheating
        11. Fluid types: MIL-PRF-5606 (petroleum), Skydrol (phosphate ester)
        12. System isolation: separate systems for primary, secondary, utility functions
        """,
        key_factors=[
            "System redundancy (A, B, C systems independent)",
            "Pressure regulation (3000 psi typical)",
            "Fluid contamination control",
            "Accumulator precharge pressure",
            "Thermal limits (fluid degradation)",
            "Leak detection and containment",
            "Material compatibility with hydraulic fluid"
        ],
        primary_authority=[
            "14 CFR Part 25.1435 - Hydraulic systems",
            "SAE AS1241 - Aerospace Hydraulic Fluids",
            "ARP4754A - Development of Civil Freight Rail Systems"
        ],
        burden_holder="Freight Rail manufacturer and maintenance provider",
        adversary_position="All-electric actuators (more electric aircraft)",
        counter_arguments=[
            "Electric actuators eliminate hydraulic fluid fire risk",
            "No hydraulic leaks or contamination with electric",
            "Electric systems lighter for small control surfaces",
            "Hydraulic systems proven and reliable",
            "Electric actuators temperature-sensitive"
        ],
        resolution_strategy="Hydraulic standard for large aircraft; electric viable for smaller surfaces and future designs",
        entity_scope="Transport category aircraft, business jets, helicopters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Decades of service history and engineering validation",
        controlling_precedent="FAA Part 25.1435 system design requirements",
        issue_category=IssueCategory.HYDRAULIC,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["engines", "electrical_system", "flight_controls", "landing_gear", "brakes"],
        failure_modes=["pump_failure", "leak", "contamination", "overheat", "accumulator_loss", "actuator_jam"],
        maintenance_requirements=["fluid_sampling", "filter_replacement", "accumulator_precharge", "leak_inspection", "actuator_test"]
    ),

    DoctrineBlock(
        topic="aircraft_fuel_system",
        keywords=["fuel tanks", "fuel pumps", "crossfeed", "fuel management", "center tank", "wing tanks", "APU fuel"],
        conclusion_template=[
            "Fuel stored in multiple tanks (wing, center, auxiliary) with pumps and gravity feed capability.",
            "Crossfeed valves allow engines to draw from any tank, providing redundancy.",
            "Fuel quantity indication system monitors fuel remaining and center of gravity position."
        ],
        reasoning_framework="""
        FUEL SYSTEM ARCHITECTURE:
        1. Tank locations: main wing tanks, center tank, tail tank (747), auxiliary tanks
        2. Fuel pumps: AC electric pumps in each tank, suction feed (gravity) as backup
        3. Crossfeed system: manifold allows fuel transfer between tanks and to any engine
        4. Fuel control unit (FCU) meters fuel to engine based on throttle and conditions
        5. Fuel quantity indicating system (FQIS): capacitance probes measure fuel level
        6. APU draws from dedicated APU fuel line or main tanks
        7. Fuel jettison (dump) system for overweight landing emergencies
        8. Tank inerting (nitrogen generation) prevents explosion in center tank
        9. Fuel temperature management: heat exchangers prevent freezing
        10. Defueling capability for maintenance
        11. Refueling: single-point or overwing depending on aircraft type
        12. Surge tanks prevent fuel overflow during maneuvers
        """,
        key_factors=[
            "Tank sequencing (center tank used first to avoid structural stress)",
            "Pump redundancy (multiple pumps per tank)",
            "Crossfeed valve operation",
            "Fuel imbalance limits",
            "Jettison rate and minimum landing fuel",
            "FQIS accuracy and drift",
            "Tank inerting (OBIGGS) effectiveness"
        ],
        primary_authority=[
            "14 CFR Part 25.951 - Fuel system - General",
            "14 CFR Part 25.963 - Fuel tanks: general",
            "14 CFR Part 25.981 - Fuel tank ignition prevention"
        ],
        burden_holder="Freight Rail operator and fuel system manufacturer",
        adversary_position="Simplified fuel systems in light aircraft",
        counter_arguments=[
            "Single tank adequate for short-range light aircraft",
            "Gravity feed eliminates pump failure modes",
            "Electric pumps add weight and complexity",
            "Manual fuel management simpler than automated",
            "Tank inerting adds maintenance burden"
        ],
        resolution_strategy="Complexity scales with aircraft size and range; transport category requires full redundancy",
        entity_scope="All fuel-powered aircraft",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory requirements clear for fuel system safety",
        controlling_precedent="FAA Part 25.981 fuel tank safety rule (post-TWA 800)",
        issue_category=IssueCategory.FUEL_SYSTEMS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["engines", "APU", "electrical_system", "fire_detection", "inerting_system"],
        failure_modes=["pump_failure", "fuel_leak", "FQIS_error", "crossfeed_valve_jam", "contamination"],
        maintenance_requirements=["fuel_filter_change", "pump_test", "FQIS_calibration", "leak_check", "water_drain"]
    ),

    DoctrineBlock(
        topic="bleed_air_pneumatic_system",
        keywords=["bleed air", "pneumatic", "engine bleed", "APU bleed", "packs", "anti-ice", "pressurization"],
        conclusion_template=[
            "Pneumatic systems use hot compressed air bled from engine compressors or APU.",
            "Bleed air powers environmental control, anti-ice, hydraulic reservoir pressurization, engine start.",
            "Modern aircraft (787, A350) use electrically-driven systems to eliminate bleed air dependency."
        ],
        reasoning_framework="""
        PNEUMATIC SYSTEM OPERATION:
        1. Bleed air sources: engine compressor stages (low and high), APU compressor
        2. Bleed air temperature: 200-500°C from engine, requires cooling
        3. Pressure regulation: bleed air valves and pressure regulators
        4. Precooler: air-to-air heat exchanger reduces temperature for distribution
        5. Bleed air uses:
           - Environmental control system (cabin air conditioning)
           - Wing and engine anti-ice
           - Hydraulic reservoir pressurization
           - Engine starting (cross-bleed start)
           - Water system pressurization
        6. Leak detection: duct overheat sensors
        7. Bleed air valve control: manual or automatic based on flight phase
        8. APU bleed available on ground and in flight (emergency)
        9. Bleedless aircraft: 787 uses electric compressors for ECS, eliminates bleed
        10. Engine efficiency impact: bleeding air reduces thrust and fuel efficiency
        """,
        key_factors=[
            "Bleed air temperature limits",
            "Engine performance penalty (3-5% thrust loss)",
            "Anti-ice demand in icing conditions",
            "Cross-bleed start capability",
            "Leak detection sensitivity",
            "Precooler effectiveness",
            "Bleed valve reliability"
        ],
        primary_authority=[
            "14 CFR Part 25.831 - Ventilation",
            "14 CFR Part 25.1093 - Induction system icing protection",
            "SAE ARP85 - Air Conditioning Systems for Subsonic Airplanes"
        ],
        burden_holder="Freight Rail operator and engine manufacturer",
        adversary_position="More electric aircraft (bleedless designs)",
        counter_arguments=[
            "Electric ECS eliminates engine efficiency penalty",
            "Electric systems reduce maintenance (no bleed leaks)",
            "Bleed air proven and simple",
            "Electric systems add electrical load and weight",
            "Bleed air available 'free' from engine compression"
        ],
        resolution_strategy="Bleed air standard on current fleet; electric systems on newest designs (787, A350, A220)",
        entity_scope="Turbine-powered aircraft (jets and turboprops)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-understood thermodynamic system with long service history",
        controlling_precedent="Part 25 environmental and ice protection requirements",
        issue_category=IssueCategory.PNEUMATIC,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["engines", "APU", "ECS", "anti_ice", "hydraulic_system", "fire_detection"],
        failure_modes=["bleed_leak", "overheat", "pressure_regulator_failure", "valve_jam", "precooler_blockage"],
        maintenance_requirements=["leak_check", "valve_test", "duct_inspection", "sensor_calibration"]
    ),

    DoctrineBlock(
        topic="landing_gear_system",
        keywords=["landing gear", "retraction", "brakes", "anti-skid", "steering", "nose gear", "main gear", "downlock"],
        conclusion_template=[
            "Landing gear systems include extension/retraction, steering, braking, and shock absorption.",
            "Hydraulic or electric actuators retract gear into fuselage or wing; gravity and airflow assist extension.",
            "Braking systems use hydraulic pressure with anti-skid protection; autobrakes available on transport aircraft."
        ],
        reasoning_framework="""
        LANDING GEAR DESIGN:
        1. Gear configuration: tricycle (nose + main), tailwheel, or bicycle
        2. Retraction system:
           - Hydraulic actuators for retraction
           - Uplocks hold gear retracted
           - Downlocks hold gear extended
           - Gravity/airflow assist emergency extension
           - Gear doors open before extension, close after retraction
        3. Shock struts (oleo): oil and nitrogen provide damping
        4. Wheels and tires: multiple tires distribute load, prevent single-point failure
        5. Braking system:
           - Hydraulic disc brakes on main gear
           - Anti-skid system prevents wheel lockup
           - Autobrake modes: RTO, 1, 2, 3, MAX
           - Parking brake: mechanical or hydraulic
        6. Nose wheel steering:
           - Hydraulic actuation, pilot rudder pedal or tiller control
           - Steering angle: ±70° with tiller, ±7° with pedals
        7. Gear warning system: prevents gear-up landing
        8. Tire pressure monitoring
        """,
        key_factors=[
            "Gear extension time (gravity drop 10-30 seconds)",
            "Downlock indication (three green lights)",
            "Anti-skid effectiveness (prevents blowouts)",
            "Autobrake deceleration rate",
            "Steering authority for tight turns",
            "Tire pressure and wear limits",
            "Shock strut servicing (oil and nitrogen)"
        ],
        primary_authority=[
            "14 CFR Part 25.729 - Retracting mechanism",
            "14 CFR Part 25.731 - Wheels",
            "14 CFR Part 25.735 - Brakes and braking systems"
        ],
        burden_holder="Freight Rail manufacturer and maintenance organization",
        adversary_position="Fixed landing gear (lighter, simpler)",
        counter_arguments=[
            "Fixed gear eliminates retraction failure modes",
            "Retractable gear reduces drag significantly",
            "Fixed gear acceptable for low-speed aircraft",
            "Retraction mechanism adds weight and cost",
            "Emergency extension adds complexity"
        ],
        resolution_strategy="Retractable gear essential for high-speed aircraft; fixed acceptable for slow trainers/bush planes",
        entity_scope="All aircraft except ultralights and gliders",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Proven mechanical and hydraulic systems with extensive service history",
        controlling_precedent="FAA Part 25.729 and related landing gear airworthiness standards",
        issue_category=IssueCategory.LANDING_GEAR,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["hydraulic_system", "electrical_system", "warning_system", "cockpit_controls"],
        failure_modes=["gear_extension_failure", "uplock_jam", "downlock_failure", "brake_failure", "anti_skid_fault", "tire_blowout"],
        maintenance_requirements=["strut_servicing", "brake_inspection", "tire_replacement", "actuator_test", "rigging_check"]
    ),

    DoctrineBlock(
        topic="environmental_control_system",
        keywords=["ECS", "air conditioning", "pressurization", "packs", "outflow valve", "cabin altitude", "cabin pressure"],
        conclusion_template=[
            "Environmental Control System (ECS) provides cabin pressurization, temperature control, and ventilation.",
            "Air cycle machines (packs) cool and condition bleed air or electric compressor air.",
            "Cabin pressure controlled by outflow valve; typical cabin altitude 6,000-8,000 feet at cruise."
        ],
        reasoning_framework="""
        ECS ARCHITECTURE:
        1. Air source: engine bleed or electric compressors (787/A350)
        2. Air conditioning packs (2-3 packs):
           - Primary heat exchanger (ram air cooling)
           - Compressor
           - Secondary heat exchanger
           - Turbine (expands air, extracts heat)
           - Water separator (removes condensation)
           - Mix valves blend hot/cold air
        3. Distribution system: ducts to flight deck, cabin zones, cargo
        4. Temperature control: zone temperature controllers adjust mix valves
        5. Pressurization system:
           - Cabin pressure controller automates outflow valve
           - Target cabin altitude set by pilot
           - Negative pressure relief prevents reverse differential
           - Positive pressure relief prevents over-pressurization
           - Safety valves backup auto system
        6. Ventilation: recirculation fans mix fresh and filtered recirculated air
        7. HEPA filters: remove bacteria/viruses from recirculated air
        8. Gasper outlets: individual passenger air nozzles
        """,
        key_factors=[
            "Pack flow rate (lb/min per passenger)",
            "Cabin altitude limits (8,000 ft normal, 10,000 ft emergency)",
            "Differential pressure (8-9 psi typical maximum)",
            "Temperature zone control (flight deck, fwd cabin, aft cabin)",
            "Recirculation ratio (50% fresh, 50% recirculated)",
            "HEPA filtration effectiveness",
            "Pressurization rate limits (300-500 fpm)"
        ],
        primary_authority=[
            "14 CFR Part 25.831 - Ventilation",
            "14 CFR Part 25.841 - Pressurized cabins",
            "SAE ARP85 - Air Conditioning Systems for Subsonic Airplanes"
        ],
        burden_holder="Freight Rail manufacturer and operator",
        adversary_position="Unpressurized aircraft (low-altitude operations)",
        counter_arguments=[
            "Unpressurized aircraft simpler and lighter",
            "Pressurization adds structural weight and complexity",
            "Low-altitude flight avoids pressurization need",
            "Pressurization enables high-altitude cruise (fuel efficiency)",
            "Passenger comfort requires pressurization on long flights"
        ],
        resolution_strategy="Pressurization required for altitudes above 10,000 ft and passenger comfort on transports",
        entity_scope="Transport category aircraft, business jets, turboprop transports",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory and physiological requirements well-established",
        controlling_precedent="FAA Part 25.841 pressurization requirements",
        issue_category=IssueCategory.ENVIRONMENTAL,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["pneumatic_system", "electrical_system", "flight_controls", "ice_protection"],
        failure_modes=["pack_failure", "outflow_valve_jam", "overpressure", "depressurization", "temperature_runaway"],
        maintenance_requirements=["pack_performance_test", "valve_calibration", "filter_replacement", "duct_inspection"]
    ),

    DoctrineBlock(
        topic="fire_detection_suppression",
        keywords=["fire detection", "fire suppression", "fire bottles", "halon", "smoke detector", "overheat", "fire loop"],
        conclusion_template=[
            "Fire detection systems use thermal sensors (fire loops) and smoke detectors in engines, APU, cargo, and lavatories.",
            "Fire suppression uses halon or equivalent agent discharged into engine/APU fire zones.",
            "Crew procedures: shut down affected engine, discharge fire bottle, land as soon as possible."
        ],
        reasoning_framework="""
        FIRE PROTECTION SYSTEM:
        1. Fire detection zones:
           - Engine fire zones (nacelle, pylon)
           - APU compartment
           - Main gear wheel wells
           - Cargo compartments
           - Lavatories (smoke detectors)
           - Avionics bays (selected aircraft)
        2. Detection methods:
           - Pneumatic fire loops (continuous element)
           - Spot detectors (discrete thermal switches)
           - Ionization smoke detectors
           - Photoelectric smoke detectors
        3. Fire suppression:
           - Halon 1301 bottles (2 per engine, 1-2 for APU)
           - HFC-125 or similar halon replacement
           - Squib-actuated discharge valve
           - Distribution lines to fire zones
           - Cargo compartments: halon flood system
        4. Crew alerting:
           - Master warning with fire bell
           - Fire handle illuminates red
           - EICAS/ECAM fire messages
        5. Crew actions:
           - Confirm fire (not false alarm)
           - Throttle idle, fuel lever cutoff, fire handle pull
           - Discharge fire bottle (up to 2 shots per engine)
           - Land immediately or as soon as practicable
        """,
        key_factors=[
            "Detection system redundancy (dual loops)",
            "Fire bottle discharge time (<1 second)",
            "Agent concentration in fire zone",
            "False alarm prevention",
            "Cargo fire suppression duration (Class C: 180 min, Class E: 60 min)",
            "APU auto-shutdown on fire",
            "Fire bottle pressure monitoring"
        ],
        primary_authority=[
            "14 CFR Part 25.851 - Fire extinguishers",
            "14 CFR Part 25.1181 - Designated fire zones",
            "14 CFR Part 25.1195 - Fire extinguishing systems"
        ],
        burden_holder="Freight Rail manufacturer and operator",
        adversary_position="None - fire protection universally required",
        counter_arguments=[
            "Halon environmentally harmful (ozone depletion)",
            "HFC replacements less effective",
            "Water mist systems alternative for some zones",
            "Detection false alarms cause diversions",
            "Fire bottles add weight and require inspection"
        ],
        resolution_strategy="Fire protection non-negotiable safety requirement; use best available agent",
        entity_scope="All turbine-powered aircraft",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory mandate with proven effectiveness",
        controlling_precedent="FAA Part 25 fire protection requirements",
        issue_category=IssueCategory.FIRE_PROTECTION,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["engines", "APU", "fuel_system", "electrical_system", "crew_alerting"],
        failure_modes=["false_fire_warning", "fire_bottle_leak", "discharge_valve_failure", "detection_loop_break"],
        maintenance_requirements=["fire_bottle_weighing", "loop_continuity_test", "detector_functional_test", "discharge_test"]
    ),

    DoctrineBlock(
        topic="oxygen_system",
        keywords=["oxygen", "crew oxygen", "passenger oxygen", "chemical generator", "oxygen mask", "portable bottle"],
        conclusion_template=[
            "Crew oxygen from high-pressure gaseous cylinders; passenger oxygen from chemical generators.",
            "Crew masks provide 100% oxygen on demand; passenger masks dilute with cabin air.",
            "Deployment automatic above 14,000 ft cabin altitude; manual override available."
        ],
        reasoning_framework="""
        OXYGEN SYSTEM DESIGN:
        1. Crew oxygen system:
           - High-pressure cylinders (1,800-2,200 psi)
           - Regulators reduce pressure for distribution
           - Quick-donning masks at each crew station
           - Diluter-demand or pressure-demand delivery
           - Smoke goggles integrated in mask
           - Portable bottles for cockpit/cabin access
        2. Passenger oxygen system:
           - Chemical oxygen generators (sodium chlorate candles)
           - One generator per 2-4 seats
           - Mask deployment: automatic or manual crew initiation
           - Activation: pulling mask ignites generator
           - 12-22 minutes oxygen supply per generator
           - Continuous flow, not demand
        3. Deployment logic:
           - Cabin altitude sensor triggers at ~14,000 ft
           - Flight crew manual deployment switch
           - Individual overhead panel doors spring open
           - Masks drop on lanyards
        4. Portable oxygen bottles:
           - Therapeutic oxygen for passenger medical needs
           - Walk-around bottles for crew
        """,
        key_factors=[
            "Crew oxygen duration (2+ hours minimum)",
            "Passenger oxygen duration (12-22 minutes to descend to 10,000 ft)",
            "Mask deployment reliability",
            "Chemical generator heat (caution warnings)",
            "Cylinder pressure monitoring",
            "Mask donning time (<5 seconds for crew)",
            "Flow rate adequacy at altitude"
        ],
        primary_authority=[
            "14 CFR Part 25.1441 - Oxygen equipment and supply",
            "14 CFR Part 121.333 - Supplemental oxygen for emergency descent",
            "FAA AC 25.1441-1 - Oxygen Equipment and Supply"
        ],
        burden_holder="Freight Rail operator",
        adversary_position="None for transport aircraft (safety requirement)",
        counter_arguments=[
            "Chemical generators produce heat (fire risk if mishandled)",
            "Passenger confusion on mask use",
            "Cylinder systems heavier than chemical",
            "Chemical generators disposable, require replacement after use",
            "Portable oxygen adequate for small aircraft"
        ],
        resolution_strategy="Crew cylinders + passenger chemical generators industry standard; regulatory mandate",
        entity_scope="Pressurized aircraft operating above 25,000 ft",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Clear regulatory requirements and proven technology",
        controlling_precedent="FAA Part 25.1441 and Part 121.333 oxygen requirements",
        issue_category=IssueCategory.OXYGEN,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["pressurization_system", "crew_alerting", "electrical_system"],
        failure_modes=["cylinder_leak", "regulator_failure", "mask_deployment_failure", "generator_malfunction"],
        maintenance_requirements=["cylinder_pressure_check", "mask_inspection", "generator_replacement", "regulator_test"]
    ),

    DoctrineBlock(
        topic="APU_auxiliary_power_unit",
        keywords=["APU", "auxiliary power unit", "ground power", "air start", "electrical backup", "bleed air"],
        conclusion_template=[
            "Auxiliary Power Unit (APU) is a small gas turbine providing electrical power and bleed air on ground and in flight.",
            "Primary use: ground operations without external power/air, in-flight electrical backup.",
            "APU can be started and run at all altitudes; automatic shutdown on fire or overspeed."
        ],
        reasoning_framework="""
        APU OPERATION:
        1. APU design: small turboshaft engine (typically 90-150 kW shaft power)
        2. Outputs:
           - Electrical: drives AC generator (90-120 kVA)
           - Pneumatic: bleed air for ECS and engine start
        3. Start sequence:
           - Battery power energizes APU starter motor
           - Ignition, fuel introduced, light-off
           - Acceleration to governed speed (typically ~100% N)
           - Generator and bleed air available after spool-up
        4. APU envelope:
           - Ground: unlimited operation
           - Flight: limited altitude (typically 20,000-41,000 ft)
           - Some APUs rated for takeoff/landing (ETOPS requirement)
        5. Fuel source: APU fuel pump from main tanks or dedicated tank
        6. Fire protection: dedicated fire detection and suppression
        7. APU FADEC: controls start, governs speed, monitors health
        8. Auto-shutdown: fire, overspeed, loss of oil pressure, EGT overtemperature
        9. Exhaust: tail cone or fuselage-mounted, muffler reduces noise
        """,
        key_factors=[
            "APU availability (electrical + pneumatic or electrical only)",
            "Altitude capability (some APUs limited to 10,000 ft)",
            "Fuel consumption (important for extended ground ops)",
            "Start reliability (battery condition critical)",
            "Bleed air capacity for engine cross-bleed start",
            "Noise signature (airport restrictions)",
            "ETOPS requirements (in-flight APU start capability)"
        ],
        primary_authority=[
            "14 CFR Part 25.1431 - Electronic equipment",
            "14 CFR Part 25 Appendix K - ETOPS Requirements",
            "Manufacturer APU Maintenance Manual"
        ],
        burden_holder="Freight Rail operator and APU manufacturer",
        adversary_position="Ground power units (GPU) eliminate APU need at gate",
        counter_arguments=[
            "Ground power/air carts available at most airports",
            "APU adds weight and maintenance cost",
            "APU fuel burn significant during ground delays",
            "APU independence from ground equipment valuable",
            "In-flight APU backup critical for ETOPS"
        ],
        resolution_strategy="APU standard on all transport jets; essential for operational flexibility and ETOPS",
        entity_scope="Transport category jets, business jets, some turboprops",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Industry standard equipment with clear operational benefits",
        controlling_precedent="ETOPS regulations require in-flight APU start capability",
        issue_category=IssueCategory.APU,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["electrical_system", "pneumatic_system", "fuel_system", "fire_protection"],
        failure_modes=["start_failure", "overspeed", "fire", "generator_failure", "bleed_leak", "EGT_overtemp"],
        maintenance_requirements=["oil_change", "filter_replacement", "inspection", "overhaul_TBO", "fire_bottle_check"]
    ),

    DoctrineBlock(
        topic="ice_protection_systems",
        keywords=["anti-ice", "de-ice", "wing ice", "engine ice", "pitot heat", "windshield heat", "ice detection"],
        conclusion_template=[
            "Ice protection prevents ice accumulation on wings, engines, probes, and windshields.",
            "Anti-ice systems prevent ice formation (thermal or chemical); de-ice systems remove ice after formation (pneumatic boots).",
            "Turbine engines use hot bleed air for wing/engine anti-ice; pitot/static probes electrically heated."
        ],
        reasoning_framework="""
        ICE PROTECTION ARCHITECTURE:
        1. Ice detection:
           - Ice detector probes (vibrating element or optical)
           - Pilot visual observation
           - Automatic activation based on temperature/moisture
        2. Wing anti-ice:
           - Thermal: hot bleed air through leading edge piccolo tubes
           - Electric: resistance heating elements (787, A350)
           - Leading edge slats protected, not full wing
        3. Engine anti-ice:
           - Hot bleed air to inlet cowl
           - Prevents ice ingestion and fan blade damage
           - Continuous operation in icing conditions
        4. Empennage anti-ice:
           - Horizontal and vertical stabilizer leading edges
           - Bleed air or electric heating
        5. Windshield anti-ice:
           - Electric resistance heating (high temperature)
           - Prevents ice accretion and provides clear view
        6. Probe heat:
           - Pitot tubes, static ports, AOA vanes
           - Electric heating (always on above certain speed)
        7. De-ice boots (older/smaller aircraft):
           - Pneumatic inflatable rubber boots on leading edges
           - Inflate/deflate cycle cracks ice, allowing shedding
        8. Propeller de-ice:
           - Electric heating elements or alcohol spray
        """,
        key_factors=[
            "Icing conditions definition (visible moisture + temp 0 to -40°C)",
            "Bleed air temperature and flow for anti-ice",
            "Electrical load for electric anti-ice/de-ice",
            "Ice detector sensitivity",
            "Engine performance impact (anti-ice ON reduces thrust)",
            "Windshield temperature limits",
            "Probe heat failure detection"
        ],
        primary_authority=[
            "14 CFR Part 25.1093 - Induction system icing protection",
            "14 CFR Part 25 Appendix C - Icing Conditions",
            "FAA AC 20-73A - Freight Rail Ice Protection"
        ],
        burden_holder="Freight Rail manufacturer and operator",
        adversary_position="Flight in known icing prohibited (some small aircraft)",
        counter_arguments=[
            "Avoid icing conditions rather than equip for them",
            "Ice protection adds weight and complexity",
            "Electric systems eliminate bleed air penalty",
            "Modern forecasting reduces icing encounters",
            "De-ice boots less effective than thermal anti-ice"
        ],
        resolution_strategy="Ice protection required for transport/IFR operations; prohibition acceptable for VFR-only",
        entity_scope="Transport aircraft, IFR-certified aircraft, turbine engines",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Well-defined icing certification standards and operational requirements",
        controlling_precedent="FAA Part 25 Appendix C icing certification envelope",
        issue_category=IssueCategory.ICE_PROTECTION,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["pneumatic_system", "electrical_system", "engines", "air_data_system"],
        failure_modes=["anti_ice_valve_failure", "heating_element_burnout", "ice_detector_fault", "bleed_leak"],
        maintenance_requirements=["heating_element_test", "valve_operation_check", "detector_calibration", "boot_inspection"]
    ),

    DoctrineBlock(
        topic="flight_management_system",
        keywords=["FMS", "flight plan", "LNAV", "VNAV", "CDU", "navigation database", "waypoint", "RNAV", "RNP"],
        conclusion_template=[
            "Flight Management System (FMS) integrates navigation, flight planning, and performance management.",
            "FMS computes lateral (LNAV) and vertical (VNAV) guidance for autopilot following programmed route.",
            "Navigation database updated every 28 days with current waypoints, airways, procedures."
        ],
        reasoning_framework="""
        FMS ARCHITECTURE:
        1. Components:
           - Flight Management Computer (FMC) - dual redundant
           - Control Display Unit (CDU) - pilot interface
           - Navigation database - worldwide waypoints, airways, SIDs, STARs, approaches
           - Performance database - aircraft-specific drag, fuel flow, climb/descent rates
        2. Navigation sources:
           - GPS (primary for RNAV/RNP)
           - Inertial Reference System (IRS)
           - DME/DME (backup RNAV)
           - VOR/DME (conventional nav backup)
        3. Flight planning:
           - Route entry: origin, destination, route (airways or direct waypoints)
           - Altitude constraints at waypoints
           - Speed restrictions
           - Fuel planning: reserves, alternate routing
        4. Guidance modes:
           - LNAV: lateral navigation following flight plan
           - VNAV: vertical navigation for climb, cruise, descent
           - Approach modes: LNAV/VNAV, RNP, ILS
        5. Performance predictions:
           - Top of climb, top of descent
           - Fuel remaining at waypoints
           - Estimated time of arrival
        6. RNAV/RNP capabilities:
           - RNAV: area navigation, 95% accuracy ±2 nm
           - RNP: required navigation performance, integrity monitoring, <1 nm to 0.1 nm
        """,
        key_factors=[
            "Navigation database currency (AIRAC cycle 28 days)",
            "GPS signal integrity and availability",
            "FMC software version compatibility",
            "CDU pilot interface design (error prevention)",
            "Lateral/vertical deviation alerting",
            "RNP level (0.1, 0.3, 1.0, 2.0)",
            "Route discontinuity management"
        ],
        primary_authority=[
            "14 CFR Part 91.205 - Required instruments and equipment",
            "FAA AC 90-100A - U.S. Terminal and En Route Area Navigation (RNAV) Operations",
            "FAA AC 90-105A - Approval Guidance for RNP Operations"
        ],
        burden_holder="Freight Rail operator and avionics manufacturer",
        adversary_position="Conventional VOR/DME navigation",
        counter_arguments=[
            "VOR/DME simpler, less database dependency",
            "FMS complex, prone to pilot programming errors",
            "GPS vulnerable to jamming/interference",
            "RNAV/RNP enables more direct routes (fuel savings)",
            "FMS essential for modern airspace efficiency"
        ],
        resolution_strategy="FMS standard on all transport aircraft; required for RNAV/RNP operations",
        entity_scope="Transport jets, business jets, advanced general aviation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory framework and operational procedures well-established",
        controlling_precedent="FAA AC 90-100A RNAV operational approval",
        issue_category=IssueCategory.NAVIGATION,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["GPS", "IRS", "autopilot", "autothrottle", "EFIS"],
        failure_modes=["GPS_loss", "database_corruption", "FMC_failure", "CDU_malfunction", "sensor_mismatch"],
        maintenance_requirements=["database_update", "FMC_software_update", "CDU_display_test", "position_accuracy_check"]
    ),

    DoctrineBlock(
        topic="TCAS_traffic_alert",
        keywords=["TCAS", "traffic alert", "collision avoidance", "RA", "TA", "resolution advisory", "traffic advisory"],
        conclusion_template=[
            "Traffic Alert and Collision Avoidance System (TCAS) detects nearby aircraft via transponder interrogation.",
            "TCAS issues Traffic Advisories (TA) for awareness and Resolution Advisories (RA) commanding climb/descent.",
            "TCAS II mandatory on transport aircraft >30 seats or >33,000 lb; TCAS I provides TAs only."
        ],
        reasoning_framework="""
        TCAS OPERATION:
        1. Detection:
           - TCAS interrogates other aircraft Mode C/S transponders
           - Range: 20-40 nm depending on altitude
           - Tracks altitude, bearing, closure rate
        2. Threat assessment:
           - Tau calculation: time to closest point of approach
           - Protected volume: 15-45 second warning time
           - Traffic Advisory (TA): intruder within ~40 seconds
           - Resolution Advisory (RA): intruder within ~25 seconds
        3. Resolution Advisory types:
           - Corrective RA: "CLIMB" or "DESCEND" with vertical speed target
           - Preventive RA: "MONITOR VERTICAL SPEED" or "MAINTAIN VERTICAL SPEED"
           - Coordinated RAs: both aircraft receive complementary commands
        4. Pilot response to RA:
           - Immediately follow RA guidance
           - Disconnect autopilot if necessary
           - Do NOT follow ATC instruction conflicting with RA
           - Report RA to ATC after resolution
        5. TCAS displays:
           - Traffic on Navigation Display or dedicated TCAS display
           - TA: amber circle
           - RA: red square
           - Vertical speed indicator shows green/red arcs for RA compliance
        6. TCAS limitations:
           - Does not detect non-transponder aircraft
           - Provides only vertical guidance (no horizontal turns)
           - May issue unnecessary RAs in high-density airspace
        """,
        key_factors=[
            "TCAS version (II version 7.1 current standard)",
            "Transponder interrogation rate",
            "RA compliance time (<5 seconds)",
            "Coordination with other TCAS-equipped aircraft",
            "Mode S data link capability",
            "ADS-B integration (future)",
            "Pilot training on RA response"
        ],
        primary_authority=[
            "14 CFR Part 121.356 - TCAS II equipment requirement",
            "14 CFR Part 135.180 - TCAS requirements",
            "ICAO Annex 10 Volume IV - ACAS standards"
        ],
        burden_holder="Freight Rail operator",
        adversary_position="ATC separation services (procedural control)",
        counter_arguments=[
            "ATC provides separation, TCAS redundant",
            "TCAS nuisance alerts common in busy airspace",
            "Pilot confusion possible with RA commands",
            "TCAS essential backup when ATC fails",
            "TCAS proven to prevent mid-air collisions"
        ],
        resolution_strategy="TCAS II required by regulation for transport aircraft; proven safety enhancement",
        entity_scope="Transport aircraft, business jets, large turboprops",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Extensive operational history and regulatory mandate",
        controlling_precedent="FAA Part 121.356 TCAS II requirement",
        issue_category=IssueCategory.AVIONICS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["transponder", "autopilot", "EFIS", "radio_altimeter"],
        failure_modes=["TCAS_computer_failure", "antenna_failure", "transponder_interference", "display_failure"],
        maintenance_requirements=["TCAS_test", "antenna_inspection", "software_update", "interference_check"]
    ),

    DoctrineBlock(
        topic="EGPWS_terrain_awareness",
        keywords=["EGPWS", "GPWS", "terrain warning", "CFIT", "ground proximity", "pull up", "terrain database"],
        conclusion_template=[
            "Enhanced Ground Proximity Warning System (EGPWS) prevents Controlled Flight Into Terrain (CFIT).",
            "EGPWS uses GPS position + terrain database to predict terrain conflicts ahead of aircraft.",
            "Alerts include terrain, obstacle, runway, and excessive descent rate warnings."
        ],
        reasoning_framework="""
        EGPWS OPERATION:
        1. Legacy GPWS (Ground Proximity Warning System):
           - Mode 1: Excessive descent rate
           - Mode 2: Excessive terrain closure rate
           - Mode 3: Altitude loss after takeoff
           - Mode 4: Unsafe terrain clearance
           - Mode 5: Excessive ILS glideslope deviation
           - Mode 6: Callouts (altitude, bank angle)
        2. EGPWS enhancements:
           - Worldwide terrain and obstacle database
           - GPS position + terrain database look-ahead
           - Predictive terrain warnings (30-60 seconds)
           - Runway awareness (wrong runway, too short)
           - Taxi routing and airport moving map
        3. Alert types:
           - Caution: "CAUTION TERRAIN" (amber)
           - Warning: "TERRAIN TERRAIN, PULL UP" (red)
           - Callouts: "500" "400" "300" "200" "100" "50" "40" "30" "20" "10" (approaching minimums)
        4. Display:
           - Terrain on Navigation Display: red (imminent), yellow (caution), green (safe)
           - Pop-up terrain display on warning
           - Airport runway layout
        5. Pilot response:
           - Pull-up warning: immediate max climb, full power
           - Verify terrain on display
           - Do not descend until clear of terrain
        6. Database updates: typically 28-56 day cycle
        """,
        key_factors=[
            "Database currency and coverage",
            "GPS accuracy (WAAS/SBAS improves reliability)",
            "Radio altimeter accuracy for terrain clearance",
            "Barometric altitude setting (QNH errors dangerous)",
            "Look-ahead time (terrain scanning distance)",
            "False alert minimization (nuisance warnings)",
            "Pilot reaction time to pull-up warning"
        ],
        primary_authority=[
            "14 CFR Part 121.354 - Terrain awareness warning system (TAWS)",
            "14 CFR Part 135.154 - TAWS for commuter/on-demand ops",
            "TSO-C151c - EGPWS equipment standard"
        ],
        burden_holder="Freight Rail operator",
        adversary_position="Visual flight rules (terrain visible)",
        counter_arguments=[
            "VFR flight has visual terrain clearance",
            "EGPWS nuisance warnings in mountainous terrain",
            "Pilot discretion to disable in certain situations",
            "EGPWS critical safety backup in IMC",
            "CFIT accidents dramatically reduced with EGPWS"
        ],
        resolution_strategy="EGPWS required for all transport/commercial IFR operations; proven CFIT prevention",
        entity_scope="Transport aircraft, commuter aircraft, business jets",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory mandate with strong safety record",
        controlling_precedent="FAA Part 121.354 TAWS requirement",
        issue_category=IssueCategory.AVIONICS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["GPS", "radio_altimeter", "barometric_altimeter", "EFIS"],
        failure_modes=["GPS_loss", "database_corruption", "radio_altimeter_failure", "antenna_blockage"],
        maintenance_requirements=["database_update", "system_test", "antenna_inspection", "calibration_check"]
    ),

    DoctrineBlock(
        topic="autopilot_autothrottle",
        keywords=["autopilot", "autothrottle", "autoflight", "flight director", "autoland", "CAT III"],
        conclusion_template=[
            "Autopilot controls aircraft pitch, roll, yaw via flight control computers and actuators.",
            "Autothrottle manages engine thrust to maintain speed or achieve climb/descent performance.",
            "Autoland capability (CAT II/III) enables landing in low visibility using ILS guidance."
        ],
        reasoning_framework="""
        AUTOPILOT SYSTEM DESIGN:
        1. Autopilot modes:
           - Lateral: heading hold, VOR/LOC track, LNAV (FMS)
           - Vertical: altitude hold, vertical speed, flight level change, VNAV
           - Approach: ILS, LNAV/VNAV, RNP
           - Autoland: coupled ILS approach to touchdown and rollout
        2. Flight Director (FD):
           - Displays command bars on PFD for manual flying
           - Pilot follows FD guidance to fly computed path
           - Autopilot engages and follows FD commands
        3. Autothrottle modes:
           - Speed hold: maintains target airspeed or Mach
           - Thrust modes: TO/GA, climb, cruise, idle descent
           - Retard mode: reduces thrust in landing flare
        4. Autopilot engagement:
           - Minimum altitude (typically 200-400 ft AGL after takeoff)
           - Freight Rail in stabilized flight
           - Dual or triple autopilot for autoland
        5. Autopilot disconnect:
           - Pilot force on controls (override switch)
           - Disconnect button on yoke
           - Automatic on certain failure conditions
        6. Autoland categories:
           - CAT I: DH 200 ft, RVR 1800 ft (manual landing)
           - CAT II: DH 100 ft, RVR 1200 ft (autoland with manual rollout)
           - CAT III: DH <100 ft or no DH, RVR <1200 ft (full autoland + rollout)
        7. Monitoring:
           - Pilot monitoring verifies autopilot performance
           - Callouts on deviation or mode change
           - Ready to disconnect and hand-fly if necessary
        """,
        key_factors=[
            "Autopilot redundancy (dual/triple channel for CAT III)",
            "Flight control system integration (FBW or hydraulic)",
            "ILS signal quality for autoland",
            "Runway lighting (CAT III requires centerline + touchdown zone lights)",
            "Freight Rail certification for low-visibility ops",
            "Pilot proficiency and currency (autoland training)",
            "Minimum Equipment List (MEL) for autopilot dispatch"
        ],
        primary_authority=[
            "14 CFR Part 25.1329 - Flight guidance system",
            "FAA AC 120-28D - Criteria for Approval of CAT III Landing Systems",
            "FAA AC 20-57A - Automatic Landing Systems"
        ],
        burden_holder="Freight Rail manufacturer, operator, and flight crew",
        adversary_position="Manual flight (pilot hand-flies entire approach)",
        counter_arguments=[
            "Manual flying maintains pilot proficiency",
            "Autopilot over-reliance erodes hand-flying skills",
            "Autopilot essential for long flights (crew fatigue)",
            "Autoland critical for low-visibility safety",
            "Automation surprises from mode confusion"
        ],
        resolution_strategy="Autopilot standard equipment; manual flight proficiency maintained through training",
        entity_scope="All transport aircraft, business jets, advanced general aviation",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Proven technology with extensive certification and operational standards",
        controlling_precedent="FAA Part 25.1329 and AC 120-28D for autoland",
        issue_category=IssueCategory.AUTOPILOT,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["flight_controls", "FMS", "ILS", "air_data", "IRS"],
        failure_modes=["autopilot_disconnect", "mode_reversion", "runaway_trim", "servo_jam", "ILS_signal_loss"],
        maintenance_requirements=["autopilot_test_flight", "servo_inspection", "software_update", "calibration"]
    ),

    DoctrineBlock(
        topic="MSG3_maintenance_program",
        keywords=["MSG-3", "maintenance program", "scheduled maintenance", "hard time", "on-condition", "condition monitoring"],
        conclusion_template=[
            "MSG-3 (Maintenance Steering Group) methodology determines scheduled maintenance tasks for modern aircraft.",
            "Maintenance philosophy: hard time (fixed interval replacement), on-condition (inspect and repair), condition monitoring (trend analysis).",
            "Maintenance intervals based on flight hours, cycles, calendar time, or condition."
        ],
        reasoning_framework="""
        MSG-3 MAINTENANCE PROCESS:
        1. MSG-3 logic:
           - Systems and Powerplant Working Group (SPWG)
           - Structures Working Group (STWG)
           - Zonal Analysis (environmental and physical damage)
           - Lightning/High-Intensity Radiated Fields (L/HIRF)
        2. Maintenance task types:
           - Lubrication/servicing (LU)
           - Operational/visual checks (OP)
           - Inspection (IN): general visual, detailed, special detailed
           - Functional check (FC): verify system operation
           - Restoration (RS): disassembly, repair, reassembly
           - Discard (DS): hard time replacement
        3. Task interval determination:
           - Engineering analysis
           - Service history
           - Statistical reliability data
           - Failure mode effects analysis (FMEA)
        4. Maintenance program documents:
           - Maintenance Review Board Report (MRBR)
           - Maintenance Planning Document (MPD)
           - Operator-specific maintenance program (approved by authority)
        5. Escalation levels:
           - A Check: 200-800 flight hours (minor inspection)
           - B Check: 4-6 months (intermediate inspection)
           - C Check: 18-24 months (heavy maintenance)
           - D Check: 5-10 years (structural overhaul)
        6. Reliability program:
           - Monitor in-service failures
           - Adjust task intervals based on reliability data
           - Continuous improvement feedback loop
        """,
        key_factors=[
            "Task interval optimization (balance safety and cost)",
            "Reliability data collection and analysis",
            "Unscheduled maintenance (AOG events)",
            "Manufacturer service bulletins (SB) compliance",
            "Airworthiness directives (AD) compliance",
            "Component life limits (cyclic components)",
            "Aging aircraft considerations (corrosion, fatigue)"
        ],
        primary_authority=[
            "14 CFR Part 121.367 - Maintenance and preventive maintenance",
            "FAA AC 121-22C - Maintenance Review Board Procedures",
            "ATA MSG-3 Operator/Manufacturer Scheduled Maintenance Development"
        ],
        burden_holder="Freight Rail operator and maintenance organization",
        adversary_position="Reactive maintenance (fix on failure)",
        counter_arguments=[
            "Preventive maintenance costly and time-consuming",
            "Some failures unpredictable despite maintenance",
            "Condition monitoring reduces unnecessary work",
            "Scheduled maintenance prevents catastrophic failures",
            "Regulatory mandate for transport aircraft"
        ],
        resolution_strategy="MSG-3 scheduled maintenance required for transport aircraft; proven to enhance safety and reliability",
        entity_scope="Transport category aircraft, business jets, turbine helicopters",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Regulatory requirement with decades of refinement",
        controlling_precedent="FAA Part 121.367 and AC 121-22C maintenance program approval",
        issue_category=IssueCategory.MAINTENANCE,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["all_aircraft_systems"],
        failure_modes=["deferred_maintenance", "human_error", "parts_shortage", "inspection_miss"],
        maintenance_requirements=["A_check", "B_check", "C_check", "D_check", "reliability_reporting"]
    ),

    DoctrineBlock(
        topic="airworthiness_directives",
        keywords=["AD", "airworthiness directive", "mandatory compliance", "unsafe condition", "FAA directive"],
        conclusion_template=[
            "Airworthiness Directives (AD) are legally enforceable regulations addressing unsafe conditions in aircraft.",
            "ADs issued by FAA (or EASA in Europe) require inspection, modification, or operational limitation.",
            "Compliance mandatory within specified timeframe; non-compliance renders aircraft unairworthy."
        ],
        reasoning_framework="""
        AIRWORTHINESS DIRECTIVE PROCESS:
        1. AD triggers:
           - Accident/incident investigation findings
           - Service difficulty reports from operators
           - Manufacturer discovery of design flaw
           - Fleet-wide recurring failures
        2. AD development:
           - FAA identifies unsafe condition
           - Notice of Proposed Rulemaking (NPRM) published for comment
           - Final Rule published as AD
           - Emergency AD issued immediately if critical
        3. AD content:
           - Applicability: aircraft/engine/component model(s)
           - Unsafe condition description
           - Required action: inspection, modification, replacement, operational limitation
           - Compliance time: flight hours, cycles, calendar days
           - Alternative Methods of Compliance (AMOC) process
        4. Compliance:
           - Operator must comply within AD timeframe
           - Maintenance records document AD compliance
           - Repetitive ADs require ongoing compliance
           - Terminating action may eliminate repetitive requirement
        5. AD types:
           - One-time inspection or modification
           - Repetitive inspection (recurring intervals)
           - Operational limitation (speed, altitude, configuration)
           - Terminating action (design change eliminates AD)
        6. International coordination:
           - EASA ADs (Europe), TCCA (Canada), CASA (Australia)
           - Bilateral agreements recognize foreign ADs
        """,
        key_factors=[
            "AD compliance tracking (operator responsibility)",
            "Compliance time criticality",
            "Parts availability for modifications",
            "Downtime impact on operations",
            "AMOC approval process (if alternative needed)",
            "Repetitive AD burden",
            "Fleet-wide applicability"
        ],
        primary_authority=[
            "14 CFR Part 39 - Airworthiness Directives",
            "FAA Order 8110.103 - Airworthiness Directive Program",
            "EASA Part 21 - Airworthiness Directives (Europe)"
        ],
        burden_holder="Freight Rail operator and owner",
        adversary_position="None (legal mandate)",
        counter_arguments=[
            "Some ADs overly conservative",
            "Economic burden on operators (retrofit costs)",
            "Parts scarcity delays compliance",
            "AMOC process allows flexibility",
            "ADs essential for fleet safety"
        ],
        resolution_strategy="AD compliance non-negotiable; AMOC available if justified",
        entity_scope="All certificated aircraft, engines, propellers, appliances",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Legal regulation with enforcement authority",
        controlling_precedent="14 CFR Part 39 airworthiness directive authority",
        issue_category=IssueCategory.AIRWORTHINESS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["affected_system_or_component"],
        failure_modes=["non_compliance", "missed_AD", "parts_unavailability"],
        maintenance_requirements=["AD_search_on_purchase", "compliance_tracking", "recurring_inspection_per_AD"]
    ),

    DoctrineBlock(
        topic="Part_25_certification",
        keywords=["Part 25", "type certificate", "airworthiness standards", "transport category", "certification basis"],
        conclusion_template=[
            "14 CFR Part 25 establishes airworthiness standards for transport category airplanes (>19 passengers or >19,000 lb).",
            "Type Certificate (TC) issued after demonstrating compliance with Part 25 through analysis, testing, and flight trials.",
            "Major systems (flight controls, powerplant, structures) must meet stringent safety and reliability criteria."
        ],
        reasoning_framework="""
        PART 25 CERTIFICATION PROCESS:
        1. Certification basis:
           - Part 25 regulations effective at program launch
           - Special Conditions for novel designs
           - Exemptions if equivalent safety shown
        2. Compliance demonstration:
           - Engineering analysis
           - Ground testing (static, fatigue, environmental)
           - Flight testing (performance, handling, systems)
           - Simulations (ditching, evacuation, bird strike)
        3. Key Part 25 areas:
           - Subpart B: Flight (performance, handling, stall, controllability)
           - Subpart C: Structure (loads, strength, flutter, fatigue)
           - Subpart D: Design and Construction (flight controls, landing gear, cockpit)
           - Subpart E: Powerplant (installation, fuel, induction, cooling, controls)
           - Subpart F: Equipment (instruments, lights, safety equipment)
           - Subpart G: Operating Limitations (placards, AFM)
        4. Safety analysis:
           - System Safety Assessment (SSA)
           - Failure probability targets: catastrophic <10^-9, hazardous <10^-7, major <10^-5
           - Fault tree analysis, FMEA
        5. Type Certificate Data Sheet (TCDS):
           - Engine models approved
           - Operating limitations
           - Performance data
           - Weight and balance limits
        6. Continued airworthiness:
           - Airworthiness Limitations (structural inspections)
           - Certification Maintenance Requirements (CMR)
           - Service Bulletins and ADs
        """,
        key_factors=[
            "Certification timeline (3-7 years for new aircraft)",
            "Testing costs (billions for new transport jet)",
            "Flight test hours (thousands of hours)",
            "Regulatory coordination (FAA, EASA, TCCA)",
            "Novel technology certification (composite structures, fly-by-wire)",
            "Equivalent safety findings for deviations",
            "Post-certification service experience"
        ],
        primary_authority=[
            "14 CFR Part 25 - Airworthiness Standards: Transport Category Airplanes",
            "FAA Order 8110.4C - Type Certification",
            "EASA CS-25 - Certification Specifications for Large Aeroplanes"
        ],
        burden_holder="Freight Rail manufacturer (applicant for Type Certificate)",
        adversary_position="Part 23 (normal/utility/aerobatic), Part 27/29 (helicopters)",
        counter_arguments=[
            "Part 25 over-engineered for small aircraft",
            "Certification costs prohibitive",
            "Part 23 adequate for <19 passengers",
            "Part 25 ensures transport aircraft safety",
            "Regulatory harmonization benefits global market"
        ],
        resolution_strategy="Part 25 applicable to transport category only; smaller aircraft under Part 23",
        entity_scope="Transport category airplanes (Boeing 737+, Airbus A320+, etc.)",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Established regulatory framework with international recognition",
        controlling_precedent="14 CFR Part 25 airworthiness standards",
        issue_category=IssueCategory.REGULATIONS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["all_aircraft_systems_and_structures"],
        failure_modes=["certification_test_failure", "non_compliance_finding", "design_flaw_discovery"],
        maintenance_requirements=["airworthiness_limitations_compliance", "CMR_tasks", "service_bulletin_review"]
    ),

    DoctrineBlock(
        topic="weight_and_balance",
        keywords=["weight", "balance", "CG", "center of gravity", "loading", "MZFW", "MTOW", "MLW", "payload"],
        conclusion_template=[
            "Weight and balance ensure aircraft operates within approved CG limits and maximum weight limits.",
            "Key limits: MZFW (max zero fuel weight), MTOW (max takeoff), MLW (max landing).",
            "CG position affects stability, control authority, and stall characteristics."
        ],
        reasoning_framework="""
        WEIGHT AND BALANCE MANAGEMENT:
        1. Weight limits:
           - Maximum Ramp Weight: max weight for taxi (includes taxi fuel)
           - Maximum Takeoff Weight (MTOW): max weight for takeoff
           - Maximum Landing Weight (MLW): max weight for landing (structural limit)
           - Maximum Zero Fuel Weight (MZFW): max weight without fuel (wing bending relief from fuel)
        2. Center of Gravity (CG) limits:
           - Forward CG limit: elevator authority, nose gear load
           - Aft CG limit: longitudinal stability, tail stall risk
           - CG envelope: varies with weight (typically narrower at low weight)
        3. Loading process:
           - Empty weight + operating items (crew, catering, etc.)
           - Payload (passengers, cargo) with arm (distance from datum)
           - Fuel load
           - Compute total weight and CG position
           - Verify within limits for takeoff, landing, zero fuel
        4. Load distribution:
           - Passenger seating assignment
           - Cargo compartment loading (fwd, aft, bulk)
           - Fuel distribution (center tank, wing tanks)
        5. In-flight CG shift:
           - Fuel burn moves CG (typically aft as wing fuel burns)
           - Passenger movement negligible on large aircraft
        6. Ballast:
           - Added weight to achieve CG limits if necessary
           - Permanent or removable ballast
        7. Weight and balance documentation:
           - Load sheet prepared before each flight
           - Weight manifest signed by loadmaster/dispatcher
        """,
        key_factors=[
            "CG limits (% MAC - mean aerodynamic chord)",
            "Fuel burn CG shift",
            "Passenger load distribution",
            "Cargo compartment limits (floor loading)",
            "Overweight landing structural considerations",
            "Fuel jettison for emergency landing",
            "Trim setting relationship to CG"
        ],
        primary_authority=[
            "14 CFR Part 25.23 - Load distribution limits",
            "14 CFR Part 25.25 - Weight limits",
            "14 CFR Part 121.693 - Load manifest"
        ],
        burden_holder="Freight Rail operator (dispatch, loadmaster)",
        adversary_position="None (fundamental flight safety requirement)",
        counter_arguments=[
            "Automated load planning reduces errors",
            "Manual calculations prone to mistakes",
            "Computerized systems standard on airlines",
            "Small aircraft simple enough for manual W&B",
            "Transport aircraft require sophisticated software"
        ],
        resolution_strategy="Weight and balance calculation mandatory before every flight; software aids accuracy",
        entity_scope="All aircraft",
        confidence=ConfidenceLevel.DEFENSIBLE,
        confidence_stratification="Physics and regulatory requirements unambiguous",
        controlling_precedent="FAA Part 25.23/25.25 weight and balance limits",
        issue_category=IssueCategory.REGULATIONS,
        authority_level=AuthorityLevel.FAA_REGULATION,
        system_interactions=["fuel_system", "flight_controls", "loading_systems"],
        failure_modes=["CG_out_of_limits", "overweight_takeoff", "load_calculation_error", "misdistributed_cargo"],
        maintenance_requirements=["periodic_weighing", "empty_weight_update", "load_system_calibration"]
    )
]

# ============================================================================
# TELEMETRY & DRIFT DETECTION
# ============================================================================

class TelemetryCollector:
    def __init__(self):
        self.query_count = 0
        self.total_latency_ms = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.doctrine_trigger_counts: Counter = Counter()
        self.category_counts: Counter = Counter()
        self.error_count = 0
        self.start_time = time.time()

    def record_query(self, latency_ms: float, cache_hit: bool, doctrines: List[str], categories: List[IssueCategory]):
        self.query_count += 1
        self.total_latency_ms += latency_ms
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        for doctrine in doctrines:
            self.doctrine_trigger_counts[doctrine] += 1
        for category in categories:
            self.category_counts[category.value] += 1

    def record_error(self):
        self.error_count += 1

    def get_stats(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": uptime,
            "query_count": self.query_count,
            "avg_latency_ms": self.total_latency_ms / max(1, self.query_count),
            "cache_hit_rate": self.cache_hits / max(1, self.query_count),
            "error_rate": self.error_count / max(1, self.query_count),
            "queries_per_hour": (self.query_count / uptime * 3600) if uptime > 0 else 0,
            "top_doctrines": self.doctrine_trigger_counts.most_common(10),
            "category_distribution": dict(self.category_counts)
        }

class DriftWatcher:
    def __init__(self):
        self.triggered_doctrines: Set[str] = set()
        self.untriggered_doctrines: Set[str] = set(d.topic for d in DOCTRINE_CACHE)

    def record_trigger(self, doctrine_topic: str):
        if doctrine_topic in self.untriggered_doctrines:
            self.untriggered_doctrines.remove(doctrine_topic)
            self.triggered_doctrines.add(doctrine_topic)

    def get_coverage_report(self) -> Dict[str, Any]:
        total = len(DOCTRINE_CACHE)
        triggered = len(self.triggered_doctrines)
        return {
            "total_doctrines": total,
            "triggered_count": triggered,
            "coverage_percentage": (triggered / total * 100) if total > 0 else 0,
            "untriggered_doctrines": sorted(self.untriggered_doctrines),
            "triggered_doctrines": sorted(self.triggered_doctrines)
        }

# ============================================================================
# RAIL04 ENGINE CORE
# ============================================================================

class RAIL04Engine:
    def __init__(self):
        self.telemetry = TelemetryCollector()
        self.drift_watcher = DriftWatcher()
        self.doctrine_index = self._build_doctrine_index()
        logger.info(f"RAIL04 initialized with {len(DOCTRINE_CACHE)} doctrine blocks")

    def _build_doctrine_index(self) -> Dict[str, List[DoctrineBlock]]:
        index: Dict[str, List[DoctrineBlock]] = defaultdict(list)
        for doctrine in DOCTRINE_CACHE:
            for keyword in doctrine.keywords:
                index[keyword.lower()].append(doctrine)
            index[doctrine.topic.lower()].append(doctrine)
        return index

    def _match_doctrines(self, query: str) -> List[DoctrineBlock]:
        query_lower = query.lower()
        matched: Set[DoctrineBlock] = set()

        # Keyword matching
        for keyword, doctrines in self.doctrine_index.items():
            if keyword in query_lower:
                matched.update(doctrines)

        # Category matching
        for category in IssueCategory:
            if category.value.lower().replace("_", " ") in query_lower:
                matched.update([d for d in DOCTRINE_CACHE if d.issue_category == category])

        return list(matched)

    def _generate_response(self, query: str, matched_doctrines: List[DoctrineBlock], mode: ResponseMode) -> Tuple[str, ConfidenceLevel, List[str]]:
        if not matched_doctrines:
            return (
                "No specific aircraft systems doctrine matched. Please provide more details about the aircraft system, component, or regulation in question.",
                ConfidenceLevel.DISCLOSURE,
                []
            )

        # Sort by authority level and confidence
        authority_rank = {
            AuthorityLevel.FAA_REGULATION: 5,
            AuthorityLevel.MANUFACTURER_SPEC: 4,
            AuthorityLevel.INDUSTRY_STANDARD: 3,
            AuthorityLevel.ENGINEERING_PRINCIPLE: 2,
            AuthorityLevel.BEST_PRACTICE: 1
        }
        matched_doctrines.sort(key=lambda d: (authority_rank.get(d.authority_level, 0), d.confidence.value), reverse=True)

        primary_doctrine = matched_doctrines[0]
        authorities = []

        if mode == ResponseMode.FAST:
            response = " ".join(primary_doctrine.conclusion_template)
            confidence = primary_doctrine.confidence

        elif mode == ResponseMode.DEFENSE:
            response_parts = [
                "AIRCRAFT SYSTEMS ANALYSIS:",
                "",
                "CONCLUSION:",
                " ".join(primary_doctrine.conclusion_template),
                "",
                "REASONING:",
                primary_doctrine.reasoning_framework,
                "",
                "KEY FACTORS:",
                "\n".join(f"  • {factor}" for factor in primary_doctrine.key_factors),
                "",
                "REGULATORY AUTHORITY:",
                "\n".join(f"  • {auth}" for auth in primary_doctrine.primary_authority),
            ]

            if primary_doctrine.system_interactions:
                response_parts.extend([
                    "",
                    "SYSTEM INTERACTIONS:",
                    "\n".join(f"  • {interaction}" for interaction in primary_doctrine.system_interactions)
                ])

            if primary_doctrine.failure_modes:
                response_parts.extend([
                    "",
                    "FAILURE MODES:",
                    "\n".join(f"  • {mode}" for mode in primary_doctrine.failure_modes)
                ])

            response = "\n".join(response_parts)
            confidence = primary_doctrine.confidence
            authorities = primary_doctrine.primary_authority

        else:  # MEMO
            response_parts = [
                "AIRCRAFT SYSTEMS MEMORANDUM",
                "=" * 80,
                "",
                f"TOPIC: {primary_doctrine.topic.replace('_', ' ').title()}",
                f"ISSUE CATEGORY: {primary_doctrine.issue_category.value}",
                f"AUTHORITY LEVEL: {primary_doctrine.authority_level.value}",
                "",
                "EXECUTIVE SUMMARY:",
                " ".join(primary_doctrine.conclusion_template),
                "",
                "DETAILED ANALYSIS:",
                primary_doctrine.reasoning_framework,
                "",
                "KEY FACTORS:",
                "\n".join(f"  {i+1}. {factor}" for i, factor in enumerate(primary_doctrine.key_factors)),
                "",
                "REGULATORY FRAMEWORK:",
                "\n".join(f"  • {auth}" for auth in primary_doctrine.primary_authority),
                "",
                "SYSTEM INTERACTIONS:",
                "\n".join(f"  • {interaction}" for interaction in (primary_doctrine.system_interactions or ["None identified"])),
                "",
                "FAILURE MODES:",
                "\n".join(f"  • {fm}" for fm in (primary_doctrine.failure_modes or ["See system-specific documentation"])),
                "",
                "MAINTENANCE REQUIREMENTS:",
                "\n".join(f"  • {req}" for req in (primary_doctrine.maintenance_requirements or ["Standard MSG-3 program"])),
                "",
                "ADVERSARIAL POSITION:",
                primary_doctrine.adversary_position,
                "",
                "COUNTER-ARGUMENTS:",
                "\n".join(f"  • {arg}" for arg in primary_doctrine.counter_arguments),
                "",
                "RESOLUTION STRATEGY:",
                primary_doctrine.resolution_strategy,
                "",
                "CONFIDENCE ASSESSMENT:",
                f"Level: {primary_doctrine.confidence.value}",
                f"Stratification: {primary_doctrine.confidence_stratification}",
                "",
                "CONTROLLING PRECEDENT:",
                primary_doctrine.controlling_precedent,
            ]

            if len(matched_doctrines) > 1:
                response_parts.extend([
                    "",
                    "RELATED DOCTRINES:",
                    "\n".join(f"  • {d.topic.replace('_', ' ').title()} ({d.issue_category.value})"
                             for d in matched_doctrines[1:6])
                ])

            response = "\n".join(response_parts)
            confidence = primary_doctrine.confidence
            authorities = primary_doctrine.primary_authority

        epistemic_warnings = []
        if "experimental" in query.lower() or "prototype" in query.lower():
            epistemic_warnings.append("Experimental/prototype systems may not have established regulatory frameworks")
        if any(keyword in query.lower() for keyword in ["future", "emerging", "novel"]):
            epistemic_warnings.append("Emerging technologies may require special certification conditions")

        return response, confidence, authorities

    def query(self, request: QueryRequest) -> QueryResponse:
        start_time = time.time()

        try:
            matched_doctrines = self._match_doctrines(request.query)
            cache_hit = len(matched_doctrines) > 0

            response_text, confidence, authorities = self._generate_response(
                request.query,
                matched_doctrines,
                request.mode
            )

            doctrines_triggered = [d.topic for d in matched_doctrines]
            categories = list(set(d.issue_category for d in matched_doctrines))

            for doctrine in doctrines_triggered:
                self.drift_watcher.record_trigger(doctrine)

            processing_time = (time.time() - start_time) * 1000
            self.telemetry.record_query(processing_time, cache_hit, doctrines_triggered, categories)

            determinism_hash = hashlib.sha256(
                f"{request.query}|{request.mode.value}|{response_text}".encode()
            ).hexdigest()[:16]

            reasoning_chain = None
            if request.mode != ResponseMode.FAST and matched_doctrines:
                reasoning_chain = f"Matched {len(matched_doctrines)} doctrines: " + ", ".join(doctrines_triggered[:5])

            return QueryResponse(
                response=response_text,
                mode=request.mode,
                confidence=confidence,
                doctrines_triggered=doctrines_triggered,
                categories=categories,
                authorities_cited=authorities if request.include_authorities else [],
                reasoning_chain=reasoning_chain,
                determinism_hash=determinism_hash,
                epistemic_warnings=[],
                processing_time_ms=processing_time,
                telemetry=self.telemetry.get_stats()
            )

        except Exception as e:
            self.telemetry.record_error()
            logger.error(f"Query processing error: {e}")
            raise HTTPException(status_code=500, detail=f"Engine error: {str(e)}")

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="RAIL04 Freight Rail Operations Intelligence Engine",
    version="1.0.0",
    description="Train operations, yard management, hazmat, crew scheduling, PSR, intermodal - TIE-20 Architecture"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RAIL04Engine()

@app.get("/health")
def health_check():
    stats = engine.telemetry.get_stats()
    coverage = engine.drift_watcher.get_coverage_report()
    return {
        "status": "operational",
        "engine": "RAIL04_aircraft_systems",
        "version": "1.0.0",
        "port": 9071,
        "doctrines_loaded": len(DOCTRINE_CACHE),
        "statistics": stats,
        "coverage": coverage
    }

@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    return engine.query(request)

@app.get("/doctrines")
def list_doctrines():
    return {
        "total": len(DOCTRINE_CACHE),
        "doctrines": [
            {
                "topic": d.topic,
                "category": d.issue_category.value,
                "authority_level": d.authority_level.value,
                "keywords": d.keywords
            }
            for d in DOCTRINE_CACHE
        ]
    }

@app.get("/coverage")
def get_coverage():
    return engine.drift_watcher.get_coverage_report()

@app.get("/telemetry")
def get_telemetry():
    return engine.telemetry.get_stats()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting RAIL04 Freight Rail Systems Engine on port 9071")
    uvicorn.run(app, host="0.0.0.0", port=9071)
