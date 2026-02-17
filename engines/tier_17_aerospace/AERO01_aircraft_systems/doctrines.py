import enum
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

@dataclass
class DoctrineBlock:
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
    confidence: float
    confidence_zone: str
    controlling_precedent: str

DOCTRINE_CACHE: List[DoctrineBlock] = [
    DoctrineBlock(
        topic="turbofan_engine_operation",
        keywords=["turbofan", "engine", "operation", "AERO01", "thrust", "fuel", "performance"],
        conclusion_template="The AERO01 turbofan engine must be operated within certified thrust, temperature, and rotational speed limits to ensure airworthiness and compliance with Part 25.",
        reasoning_framework=(
            "1. Review EASA/FAA Part 25 certification requirements for turbofan engine operation.\n"
            "2. Analyze the AERO01 engine's certified operating envelope (N1/N2, EGT, thrust).\n"
            "3. Evaluate manufacturer limitations and published procedures in AFM/FCOM.\n"
            "4. Consider operational scenarios (takeoff, climb, cruise, descent, idle, reverse thrust).\n"
            "5. Assess risk of exceedance (overspeed, overtemp, overboost) and mitigation strategies.\n"
            "6. Examine the impact of environmental conditions (OAT, pressure altitude, humidity).\n"
            "7. Reference maintenance and monitoring requirements (trend monitoring, engine health).\n"
            "8. Synthesize findings to establish compliant operational doctrine for AERO01."
        ),
        key_factors=[
            "Certified thrust and temperature limits",
            "N1/N2 rotational speed limits",
            "AFM/FCOM procedures",
            "Environmental conditions",
            "Maintenance and monitoring requirements"
        ],
        primary_authority=[
            "14 CFR Part 25 Subpart E",
            "EASA CS-25",
            "AERO01 AFM",
            "AERO01 FCOM"
        ],
        burden_holder="Operator/Pilot-in-Command",
        adversary_position="Engine may be operated beyond certified limits for operational necessity.",
        counter_arguments=[
            "Exceeding certified limits voids airworthiness.",
            "Manufacturer prohibits such operation.",
            "Potential for catastrophic engine failure."
        ],
        resolution_strategy="Strict adherence to certified limits and manufacturer procedures; deviations require engineering authorization and post-flight inspection.",
        entity_scope="AERO01 engine installations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA Legal Interpretation 2016-02 (Engine Limit Exceedance)"
    ),
    DoctrineBlock(
        topic="fly_by_wire_flight_controls",
        keywords=["fly-by-wire", "flight controls", "electronic", "redundancy", "AERO01", "actuators"],
        conclusion_template="AERO01 fly-by-wire flight control systems must maintain triple redundancy and fail-operational capability per Part 25 and ARP4754A.",
        reasoning_framework=(
            "1. Identify regulatory requirements for fly-by-wire (FBW) systems (Part 25.671, 25.1309).\n"
            "2. Examine AERO01 FBW architecture: control computers, sensors, actuators, and data buses.\n"
            "3. Analyze redundancy levels (triple/quadruple) and failure detection/isolation mechanisms.\n"
            "4. Evaluate fail-operational and fail-safe design features.\n"
            "5. Review software assurance level (DO-178C) and hardware assurance (DO-254).\n"
            "6. Assess maintenance, dispatch, and MEL implications.\n"
            "7. Synthesize compliance with ARP4754A/4761 for system safety assessment."
        ),
        key_factors=[
            "Redundancy and segregation",
            "Failure detection and isolation",
            "Software/hardware assurance",
            "System safety assessment",
            "Dispatch and MEL policies"
        ],
        primary_authority=[
            "14 CFR Part 25.671",
            "ARP4754A",
            "DO-178C",
            "DO-254"
        ],
        burden_holder="Aircraft Manufacturer",
        adversary_position="Dual redundancy is sufficient for dispatch.",
        counter_arguments=[
            "Triple redundancy is required for fail-operational capability.",
            "Dual redundancy increases risk of loss of control.",
            "Certification basis mandates triple/quadruple redundancy."
        ],
        resolution_strategy="Design and verify triple redundancy; document compliance in system safety assessment and certification plan.",
        entity_scope="AERO01 FBW-equipped aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA Policy Statement PS-ANM-25.1309-1"
    ),
    DoctrineBlock(
        topic="glass_cockpit_avionics",
        keywords=["glass cockpit", "avionics", "EFIS", "AERO01", "display", "integration"],
        conclusion_template="AERO01 glass cockpit avionics must provide integrated, fail-safe flight and engine data display per Part 25 and DO-178C.",
        reasoning_framework=(
            "1. Review Part 25.1301/1302/1309 for avionics integration and reliability.\n"
            "2. Analyze AERO01 glass cockpit architecture: PFD, ND, EICAS/ECAM, standby instruments.\n"
            "3. Evaluate data sources (sensors, FMS, engine, navigation) and data bus integrity.\n"
            "4. Examine failure modes and reversionary capabilities.\n"
            "5. Assess software assurance (DO-178C Level A/B).\n"
            "6. Consider human factors and display readability.\n"
            "7. Synthesize doctrine for integrated, fail-safe operation."
        ),
        key_factors=[
            "Display integration",
            "Data bus reliability",
            "Software assurance",
            "Reversionary modes",
            "Human factors"
        ],
        primary_authority=[
            "14 CFR Part 25.1301",
            "DO-178C",
            "EASA AMC 25.1302"
        ],
        burden_holder="Avionics Integrator",
        adversary_position="Separate analog backup is unnecessary with modern EFIS.",
        counter_arguments=[
            "Regulations require independent standby instruments.",
            "Display failures may compromise situational awareness.",
            "Certification requires backup for critical data."
        ],
        resolution_strategy="Integrate glass cockpit with independent standby instruments and robust reversionary modes.",
        entity_scope="AERO01 glass cockpit installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1302-1"
    ),
    DoctrineBlock(
        topic="aircraft_electrical_system",
        keywords=["electrical system", "power generation", "distribution", "AERO01", "redundancy", "bus"],
        conclusion_template="The AERO01 aircraft electrical system must provide redundant AC/DC power sources and automatic load shedding per Part 25.1351.",
        reasoning_framework=(
            "1. Review Part 25.1351/1353 for electrical system requirements.\n"
            "2. Analyze AERO01 power generation (engine-driven generators, APU, batteries).\n"
            "3. Evaluate power distribution: essential, main, emergency buses.\n"
            "4. Assess redundancy and failure tolerance.\n"
            "5. Examine load shedding and automatic transfer logic.\n"
            "6. Review maintenance and dispatch requirements.\n"
            "7. Synthesize doctrine for reliable, redundant electrical power."
        ),
        key_factors=[
            "Redundant power sources",
            "Automatic load shedding",
            "Bus architecture",
            "Failure tolerance",
            "Maintenance/dispatch"
        ],
        primary_authority=[
            "14 CFR Part 25.1351",
            "EASA CS-25.1351",
            "AC 25.1353-1A"
        ],
        burden_holder="Electrical System Designer",
        adversary_position="Single generator is sufficient for dispatch.",
        counter_arguments=[
            "Redundancy is required for continued safe flight and landing.",
            "Single generator increases risk of total power loss.",
            "Certification mandates multiple independent sources."
        ],
        resolution_strategy="Design with at least two independent generators and automatic load shedding; verify compliance via system safety assessment.",
        entity_scope="AERO01 electrical system",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1353-1A"
    ),
    DoctrineBlock(
        topic="hydraulic_flight_control_system",
        keywords=["hydraulic", "flight control", "system", "AERO01", "redundancy", "actuators"],
        conclusion_template="AERO01 hydraulic flight control systems must maintain at least three independent hydraulic sources for redundancy per Part 25.671 and 25.1309.",
        reasoning_framework=(
            "1. Review Part 25.671 and 25.1309 for hydraulic system requirements.\n"
            "2. Analyze AERO01 hydraulic architecture: pumps, reservoirs, actuators, accumulators.\n"
            "3. Evaluate redundancy (three or more independent sources) and segregation.\n"
            "4. Assess failure modes and isolation capability.\n"
            "5. Examine maintenance and dispatch implications (MEL, MMEL).\n"
            "6. Synthesize doctrine for fail-operational hydraulic controls."
        ),
        key_factors=[
            "Number of independent hydraulic sources",
            "System segregation",
            "Failure isolation",
            "Maintenance/dispatch",
            "Actuator redundancy"
        ],
        primary_authority=[
            "14 CFR Part 25.671",
            "EASA CS-25.1309",
            "FAA AC 25.1309-1A"
        ],
        burden_holder="Aircraft Manufacturer",
        adversary_position="Two hydraulic sources are sufficient for dispatch.",
        counter_arguments=[
            "Three sources provide fail-operational capability.",
            "Dual redundancy increases risk of loss of control.",
            "Certification basis requires triple redundancy."
        ],
        resolution_strategy="Design and verify three independent hydraulic sources; document compliance in system safety assessment.",
        entity_scope="AERO01 hydraulic systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1309-1A"
    ),
    DoctrineBlock(
        topic="aircraft_fuel_system",
        keywords=["fuel system", "AERO01", "tanks", "pumps", "crossfeed", "contamination"],
        conclusion_template="AERO01 fuel system must ensure reliable fuel supply to all engines under all flight conditions, with crossfeed and contamination protection per Part 25.951.",
        reasoning_framework=(
            "1. Review Part 25.951/25.963 for fuel system requirements.\n"
            "2. Analyze AERO01 fuel tank arrangement, pumps, valves, and crossfeed capability.\n"
            "3. Evaluate fuel quantity measurement and low fuel warning systems.\n"
            "4. Assess fuel contamination protection (filters, water drains).\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for reliable, safe fuel supply."
        ),
        key_factors=[
            "Reliable fuel supply",
            "Crossfeed capability",
            "Contamination protection",
            "Fuel quantity measurement",
            "Warning systems"
        ],
        primary_authority=[
            "14 CFR Part 25.951",
            "EASA CS-25.963",
            "AC 25.963-1"
        ],
        burden_holder="Fuel System Designer",
        adversary_position="Crossfeed system is not required for twin-engine operation.",
        counter_arguments=[
            "Crossfeed is required for redundancy and balance.",
            "Contamination protection is critical for engine safety.",
            "Certification mandates reliable fuel supply under all conditions."
        ],
        resolution_strategy="Design with crossfeed and contamination protection; verify via system safety and compliance testing.",
        entity_scope="AERO01 fuel systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.963-1"
    ),
    DoctrineBlock(
        topic="bleed_air_pneumatic_system",
        keywords=["bleed air", "pneumatic", "AERO01", "anti-ice", "pressurization", "system"],
        conclusion_template="AERO01 bleed air system must provide regulated, monitored pneumatic supply for anti-ice, ECS, and pressurization per Part 25.831.",
        reasoning_framework=(
            "1. Review Part 25.831/25.1309 for bleed air system requirements.\n"
            "2. Analyze AERO01 bleed air sources (engine, APU), regulation, and monitoring.\n"
            "3. Evaluate distribution to anti-ice, ECS, and pressurization.\n"
            "4. Assess overpressure, overtemperature, and leak detection.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for safe, reliable pneumatic supply."
        ),
        key_factors=[
            "Regulated pneumatic supply",
            "Distribution to critical systems",
            "Overpressure/overtemp protection",
            "Leak detection",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.831",
            "EASA CS-25.831",
            "AC 25.831-1"
        ],
        burden_holder="Pneumatic System Designer",
        adversary_position="Direct engine bleed supply is sufficient without regulation.",
        counter_arguments=[
            "Regulation is required to prevent system overpressure.",
            "Monitoring is critical for safety.",
            "Certification mandates regulated, monitored supply."
        ],
        resolution_strategy="Design with regulation, monitoring, and protection; verify compliance through system testing.",
        entity_scope="AERO01 pneumatic systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.831-1"
    ),
    DoctrineBlock(
        topic="landing_gear_system",
        keywords=["landing gear", "retraction", "extension", "AERO01", "brakes", "steering"],
        conclusion_template="AERO01 landing gear system must provide reliable retraction/extension and braking under all operational conditions per Part 25.729.",
        reasoning_framework=(
            "1. Review Part 25.729 for landing gear system requirements.\n"
            "2. Analyze AERO01 gear retraction/extension mechanisms and redundancy.\n"
            "3. Evaluate braking, anti-skid, and steering systems.\n"
            "4. Assess emergency extension and failure modes.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for reliable gear operation."
        ),
        key_factors=[
            "Retraction/extension reliability",
            "Braking and anti-skid",
            "Steering capability",
            "Emergency extension",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.729",
            "EASA CS-25.729",
            "AC 25.729-1"
        ],
        burden_holder="Landing Gear System Designer",
        adversary_position="Manual extension is sufficient for all operations.",
        counter_arguments=[
            "Automatic and emergency extension are required for safety.",
            "Manual extension may not be feasible in all scenarios.",
            "Certification mandates reliable operation under all conditions."
        ],
        resolution_strategy="Design with automatic, manual, and emergency extension; verify compliance via testing.",
        entity_scope="AERO01 landing gear systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.729-1"
    ),
    DoctrineBlock(
        topic="environmental_control_system",
        keywords=["environmental control", "ECS", "AERO01", "pressurization", "air conditioning", "ventilation"],
        conclusion_template="AERO01 environmental control system must maintain cabin pressure, temperature, and ventilation within certified limits per Part 25.831.",
        reasoning_framework=(
            "1. Review Part 25.831/25.841 for ECS requirements.\n"
            "2. Analyze AERO01 ECS architecture: air sources, packs, valves, sensors.\n"
            "3. Evaluate pressurization, temperature control, and ventilation.\n"
            "4. Assess failure modes and emergency procedures.\n"
            "5. Examine maintenance and operational requirements.\n"
            "6. Synthesize doctrine for compliant ECS operation."
        ),
        key_factors=[
            "Cabin pressure control",
            "Temperature regulation",
            "Ventilation",
            "Failure modes",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.831",
            "EASA CS-25.831",
            "AC 25.831-1"
        ],
        burden_holder="ECS Designer",
        adversary_position="Natural ventilation is sufficient for all operations.",
        counter_arguments=[
            "Pressurization and temperature control are required for high altitude.",
            "Natural ventilation is inadequate above 10,000 ft.",
            "Certification mandates ECS for safety and comfort."
        ],
        resolution_strategy="Design with automated ECS and backup controls; verify compliance via testing.",
        entity_scope="AERO01 ECS installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.831-1"
    ),
    DoctrineBlock(
        topic="fire_detection_suppression",
        keywords=["fire detection", "suppression", "AERO01", "engine fire", "cargo fire", "system"],
        conclusion_template="AERO01 fire detection and suppression systems must provide rapid detection and extinguishing capability for engines, APU, and cargo per Part 25.851.",
        reasoning_framework=(
            "1. Review Part 25.851/25.857 for fire protection requirements.\n"
            "2. Analyze AERO01 fire detection sensors, suppression agents, and control logic.\n"
            "3. Evaluate coverage for engines, APU, and cargo compartments.\n"
            "4. Assess response time and reliability.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for compliant fire protection."
        ),
        key_factors=[
            "Detection coverage",
            "Suppression capability",
            "Response time",
            "Reliability",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.851",
            "EASA CS-25.851",
            "AC 25.851-1"
        ],
        burden_holder="Fire Protection System Designer",
        adversary_position="Detection only is sufficient; suppression is not required.",
        counter_arguments=[
            "Suppression is required for engines and cargo.",
            "Detection alone does not mitigate fire risk.",
            "Certification mandates both detection and suppression."
        ],
        resolution_strategy="Design with rapid detection and effective suppression; verify compliance via testing.",
        entity_scope="AERO01 fire protection systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.851-1"
    ),
    DoctrineBlock(
        topic="oxygen_system",
        keywords=["oxygen system", "crew", "passenger", "AERO01", "emergency", "supplemental"],
        conclusion_template="AERO01 oxygen systems must provide supplemental and emergency oxygen for crew and passengers per Part 25.1443.",
        reasoning_framework=(
            "1. Review Part 25.1443/25.1447 for oxygen system requirements.\n"
            "2. Analyze AERO01 oxygen supply: bottles, generators, masks, regulators.\n"
            "3. Evaluate distribution to crew and passengers.\n"
            "4. Assess duration and flow rates for emergency descent profiles.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for compliant oxygen system design."
        ),
        key_factors=[
            "Supply duration",
            "Distribution to all occupants",
            "Emergency and supplemental modes",
            "Maintenance procedures",
            "Flow rates"
        ],
        primary_authority=[
            "14 CFR Part 25.1443",
            "EASA CS-25.1443",
            "AC 25.1443-1"
        ],
        burden_holder="Oxygen System Designer",
        adversary_position="Oxygen for crew only is sufficient.",
        counter_arguments=[
            "Passengers require oxygen above 15,000 ft.",
            "Certification mandates supply for all occupants.",
            "Emergency descent may exceed crew-only supply."
        ],
        resolution_strategy="Design with adequate supply for all occupants; verify compliance via testing.",
        entity_scope="AERO01 oxygen systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1443-1"
    ),
    DoctrineBlock(
        topic="APU_auxiliary_power_unit",
        keywords=["APU", "auxiliary power", "AERO01", "electrical", "pneumatic", "start"],
        conclusion_template="AERO01 APU must provide independent electrical and pneumatic power for engine start and ground operations per Part 25.1351.",
        reasoning_framework=(
            "1. Review Part 25.1351/25.1353 for APU requirements.\n"
            "2. Analyze AERO01 APU electrical and pneumatic output capability.\n"
            "3. Evaluate integration with engine start, ECS, and electrical buses.\n"
            "4. Assess redundancy and failure modes.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for compliant APU operation."
        ),
        key_factors=[
            "Electrical and pneumatic output",
            "Integration with critical systems",
            "Redundancy",
            "Failure modes",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.1351",
            "EASA CS-25.1351",
            "AC 25.1353-1A"
        ],
        burden_holder="APU System Designer",
        adversary_position="APU is not required for dispatch.",
        counter_arguments=[
            "APU provides redundancy for engine start and ground ops.",
            "Certification may require APU for ETOPS or MEL compliance.",
            "Loss of APU limits operational flexibility."
        ],
        resolution_strategy="Design with APU capability; document MEL and dispatch policies.",
        entity_scope="AERO01 APU installations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1353-1A"
    ),
    DoctrineBlock(
        topic="ice_protection_systems",
        keywords=["ice protection", "anti-ice", "de-ice", "AERO01", "bleed air", "electrical"],
        conclusion_template="AERO01 ice protection systems must prevent hazardous ice accumulation on critical surfaces per Part 25.1419.",
        reasoning_framework=(
            "1. Review Part 25.1419 for ice protection requirements.\n"
            "2. Analyze AERO01 anti-ice and de-ice system architecture (bleed air, electrical, boots).\n"
            "3. Evaluate coverage for wings, engine inlets, and sensors.\n"
            "4. Assess performance in known icing conditions.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for compliant ice protection."
        ),
        key_factors=[
            "Coverage of critical surfaces",
            "System effectiveness",
            "Known icing performance",
            "Maintenance procedures",
            "Failure modes"
        ],
        primary_authority=[
            "14 CFR Part 25.1419",
            "EASA CS-25.1419",
            "AC 25.1419-1"
        ],
        burden_holder="Ice Protection System Designer",
        adversary_position="Ice protection is not required for VFR operations.",
        counter_arguments=[
            "Certification requires protection for all operations.",
            "Unexpected icing can occur in VFR.",
            "System must be effective in all certified conditions."
        ],
        resolution_strategy="Design for full coverage and effectiveness; verify via icing tests.",
        entity_scope="AERO01 ice protection systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1419-1"
    ),
    DoctrineBlock(
        topic="flight_management_system",
        keywords=["FMS", "flight management", "navigation", "AERO01", "performance", "integration"],
        conclusion_template="AERO01 flight management system must provide integrated navigation, performance, and guidance functions per Part 25.1301.",
        reasoning_framework=(
            "1. Review Part 25.1301/1309 for FMS requirements.\n"
            "2. Analyze AERO01 FMS architecture: navigation sensors, databases, integration with autopilot and displays.\n"
            "3. Evaluate performance calculations and guidance logic.\n"
            "4. Assess failure modes and reversionary procedures.\n"
            "5. Examine maintenance and operational requirements.\n"
            "6. Synthesize doctrine for compliant FMS operation."
        ),
        key_factors=[
            "Navigation integration",
            "Performance calculations",
            "Guidance logic",
            "Failure/reversionary modes",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.1301",
            "EASA CS-25.1301",
            "AC 20-130A"
        ],
        burden_holder="FMS Integrator",
        adversary_position="Manual navigation is sufficient for all operations.",
        counter_arguments=[
            "FMS increases situational awareness and safety.",
            "Manual navigation increases workload and error risk.",
            "Certification mandates integrated navigation for complex operations."
        ],
        resolution_strategy="Integrate FMS with navigation and autopilot; verify compliance via testing.",
        entity_scope="AERO01 FMS installations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-130A"
    ),
    DoctrineBlock(
        topic="TCAS_traffic_alert",
        keywords=["TCAS", "traffic alert", "collision avoidance", "AERO01", "transponder", "RA"],
        conclusion_template="AERO01 TCAS must provide traffic advisories and resolution advisories per TSO-C119 and Part 25.1301.",
        reasoning_framework=(
            "1. Review TSO-C119 and Part 25.1301 for TCAS requirements.\n"
            "2. Analyze AERO01 TCAS integration with transponder and displays.\n"
            "3. Evaluate traffic advisory and resolution advisory logic.\n"
            "4. Assess pilot interface and alert prioritization.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for compliant TCAS operation."
        ),
        key_factors=[
            "Traffic and resolution advisories",
            "Integration with displays",
            "Alert prioritization",
            "Maintenance procedures",
            "Pilot interface"
        ],
        primary_authority=[
            "TSO-C119",
            "14 CFR Part 25.1301",
            "AC 20-151B"
        ],
        burden_holder="TCAS Integrator",
        adversary_position="Visual separation is sufficient for collision avoidance.",
        counter_arguments=[
            "TCAS provides automated resolution advisories.",
            "Visual separation is unreliable in IMC.",
            "Certification mandates TCAS for transport aircraft."
        ],
        resolution_strategy="Integrate TCAS with displays and transponder; verify compliance via operational tests.",
        entity_scope="AERO01 TCAS installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-151B"
    ),
    DoctrineBlock(
        topic="EGPWS_terrain_awareness",
        keywords=["EGPWS", "terrain awareness", "AERO01", "TAWS", "warning", "database"],
        conclusion_template="AERO01 EGPWS must provide predictive terrain and obstacle warnings per TSO-C151 and Part 25.1301.",
        reasoning_framework=(
            "1. Review TSO-C151 and Part 25.1301 for EGPWS requirements.\n"
            "2. Analyze AERO01 EGPWS integration with navigation and terrain databases.\n"
            "3. Evaluate warning logic and pilot interface.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant EGPWS operation."
        ),
        key_factors=[
            "Predictive terrain/obstacle warnings",
            "Database integration",
            "Warning logic",
            "Maintenance procedures",
            "Pilot interface"
        ],
        primary_authority=[
            "TSO-C151",
            "14 CFR Part 25.1301",
            "AC 20-167A"
        ],
        burden_holder="EGPWS Integrator",
        adversary_position="Visual terrain avoidance is sufficient.",
        counter_arguments=[
            "EGPWS provides predictive warnings in low visibility.",
            "Visual avoidance is unreliable in IMC.",
            "Certification mandates TAWS for transport aircraft."
        ],
        resolution_strategy="Integrate EGPWS with navigation and displays; verify compliance via operational tests.",
        entity_scope="AERO01 EGPWS installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-167A"
    ),
    DoctrineBlock(
        topic="autopilot_autothrottle",
        keywords=["autopilot", "autothrottle", "AERO01", "flight director", "automation", "integration"],
        conclusion_template="AERO01 autopilot and autothrottle systems must provide integrated, fail-safe flight path and speed control per Part 25.1329.",
        reasoning_framework=(
            "1. Review Part 25.1329 for autopilot/autothrottle requirements.\n"
            "2. Analyze AERO01 system integration with flight director and FMS.\n"
            "3. Evaluate failure detection, disengagement, and reversionary modes.\n"
            "4. Assess pilot interface and alerting.\n"
            "5. Examine maintenance and operational procedures.\n"
            "6. Synthesize doctrine for compliant automation."
        ),
        key_factors=[
            "Integrated flight path/speed control",
            "Failure detection/disengagement",
            "Reversionary modes",
            "Pilot interface",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.1329",
            "EASA CS-25.1329",
            "AC 25.1329-1C"
        ],
        burden_holder="Autopilot System Integrator",
        adversary_position="Manual control is sufficient for all operations.",
        counter_arguments=[
            "Automation reduces workload and error risk.",
            "Certification mandates autopilot for complex operations.",
            "Manual control increases pilot workload."
        ],
        resolution_strategy="Integrate autopilot/autothrottle with robust disengagement and alerting; verify compliance via testing.",
        entity_scope="AERO01 autopilot/autothrottle installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1329-1C"
    ),
    DoctrineBlock(
        topic="MSG3_maintenance_program",
        keywords=["MSG-3", "maintenance", "AERO01", "scheduled", "tasks", "reliability"],
        conclusion_template="AERO01 maintenance program must be developed using MSG-3 logic to optimize reliability and safety per Part 25.1529.",
        reasoning_framework=(
            "1. Review Part 25.1529 and AC 121-22C for maintenance program requirements.\n"
            "2. Analyze MSG-3 logic for task development (hard time, on-condition, condition monitoring).\n"
            "3. Evaluate scheduled maintenance tasks for AERO01 systems.\n"
            "4. Assess reliability and safety implications.\n"
            "5. Examine operator feedback and continuous improvement.\n"
            "6. Synthesize doctrine for compliant maintenance program."
        ),
        key_factors=[
            "MSG-3 logic",
            "Task development",
            "Reliability/safety",
            "Continuous improvement",
            "Operator feedback"
        ],
        primary_authority=[
            "14 CFR Part 25.1529",
            "AC 121-22C",
            "MSG-3 Guidelines"
        ],
        burden_holder="Maintenance Program Developer",
        adversary_position="Traditional maintenance intervals are sufficient.",
        counter_arguments=[
            "MSG-3 optimizes safety and reliability.",
            "Traditional intervals may be inefficient.",
            "Certification mandates MSG-3 for new programs."
        ],
        resolution_strategy="Develop and update maintenance program using MSG-3; document compliance and continuous improvement.",
        entity_scope="AERO01 maintenance programs",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AC 121-22C"
    ),
    DoctrineBlock(
        topic="airworthiness_directives",
        keywords=["airworthiness directive", "AD", "AERO01", "compliance", "regulatory", "safety"],
        conclusion_template="AERO01 operators must comply with all applicable airworthiness directives to maintain continued airworthiness per Part 39.",
        reasoning_framework=(
            "1. Review Part 39 for airworthiness directive (AD) requirements.\n"
            "2. Analyze applicability of ADs to AERO01 engine and systems.\n"
            "3. Evaluate compliance methods and documentation.\n"
            "4. Assess impact on continued airworthiness and operational approval.\n"
            "5. Synthesize doctrine for AD compliance."
        ),
        key_factors=[
            "AD applicability",
            "Compliance methods",
            "Documentation",
            "Continued airworthiness",
            "Operational approval"
        ],
        primary_authority=[
            "14 CFR Part 39",
            "EASA Part 21.A.3B",
            "FAA Order 8110.103"
        ],
        burden_holder="Operator",
        adversary_position="ADs are advisory and not mandatory.",
        counter_arguments=[
            "ADs are legally binding.",
            "Non-compliance voids airworthiness.",
            "Certification requires AD compliance."
        ],
        resolution_strategy="Monitor and comply with all ADs; document compliance for regulatory review.",
        entity_scope="AERO01 operators",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA Order 8110.103"
    ),
    DoctrineBlock(
        topic="Part_25_certification",
        keywords=["Part 25", "certification", "AERO01", "compliance", "airworthiness", "regulatory"],
        conclusion_template="AERO01 engine and systems must demonstrate full compliance with 14 CFR Part 25 for type certification.",
        reasoning_framework=(
            "1. Review 14 CFR Part 25 for certification basis.\n"
            "2. Analyze compliance of AERO01 engine and systems with all applicable sections.\n"
            "3. Evaluate test and analysis evidence for each requirement.\n"
            "4. Assess conformity and configuration control.\n"
            "5. Synthesize doctrine for type certification compliance."
        ),
        key_factors=[
            "Certification basis",
            "Compliance evidence",
            "Test and analysis",
            "Conformity",
            "Configuration control"
        ],
        primary_authority=[
            "14 CFR Part 25",
            "EASA CS-25",
            "FAA Order 8110.4C"
        ],
        burden_holder="Applicant",
        adversary_position="Partial compliance is sufficient for certification.",
        counter_arguments=[
            "Full compliance is required for type certification.",
            "Partial compliance risks airworthiness.",
            "Regulatory authorities mandate full conformity."
        ],
        resolution_strategy="Demonstrate and document full compliance; coordinate with authorities for type certification.",
        entity_scope="AERO01 engine and systems",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="FAA Order 8110.4C"
    ),
    DoctrineBlock(
        topic="weight_and_balance",
        keywords=["weight", "balance", "AERO01", "CG", "limits", "loading"],
        conclusion_template="AERO01 aircraft must be loaded and operated within certified weight and CG limits per Part 25.23.",
        reasoning_framework=(
            "1. Review Part 25.23/25.27 for weight and balance requirements.\n"
            "2. Analyze AERO01 certified weight and CG envelope.\n"
            "3. Evaluate loading procedures and documentation.\n"
            "4. Assess operational control and monitoring.\n"
            "5. Synthesize doctrine for compliant weight and balance management."
        ),
        key_factors=[
            "Certified weight/CG limits",
            "Loading procedures",
            "Operational control",
            "Documentation",
            "Monitoring"
        ],
        primary_authority=[
            "14 CFR Part 25.23",
            "EASA CS-25.23",
            "AC 120-27F"
        ],
        burden_holder="Operator",
        adversary_position="Minor exceedances are acceptable for short flights.",
        counter_arguments=[
            "Exceeding limits voids airworthiness.",
            "Certification mandates strict compliance.",
            "Safety is compromised by out-of-envelope loading."
        ],
        resolution_strategy="Monitor and document loading; ensure operation within certified limits.",
        entity_scope="AERO01 aircraft",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AC 120-27F"
    ),
    # Additional doctrines for completeness and coverage
    DoctrineBlock(
        topic="engine_control_FADEC",
        keywords=["FADEC", "engine control", "AERO01", "automation", "thrust management"],
        conclusion_template="AERO01 engines must be controlled by dual-redundant FADEC systems to ensure precise thrust management and fault tolerance.",
        reasoning_framework=(
            "1. Review engine control requirements under Part 33 and Part 25.\n"
            "2. Analyze AERO01 FADEC architecture, redundancy, and failure detection.\n"
            "3. Evaluate integration with cockpit controls and displays.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant FADEC operation."
        ),
        key_factors=[
            "Dual-redundant FADEC",
            "Thrust management",
            "Fault detection",
            "Integration with cockpit",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 33.28",
            "EASA CS-E 50",
            "AC 33.28-1"
        ],
        burden_holder="Engine Control System Designer",
        adversary_position="Single-channel FADEC is sufficient.",
        counter_arguments=[
            "Dual-redundancy is required for fault tolerance.",
            "Single-channel increases risk of loss of control.",
            "Certification mandates dual-redundant FADEC."
        ],
        resolution_strategy="Design with dual-redundant FADEC; verify via testing and analysis.",
        entity_scope="AERO01 engine control systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 33.28-1"
    ),
    DoctrineBlock(
        topic="engine_vibration_monitoring",
        keywords=["engine vibration", "monitoring", "AERO01", "health", "maintenance"],
        conclusion_template="AERO01 engines must be equipped with vibration monitoring to detect abnormal conditions and support predictive maintenance.",
        reasoning_framework=(
            "1. Review engine health monitoring requirements under Part 33 and Part 25.\n"
            "2. Analyze AERO01 vibration sensor placement and data processing.\n"
            "3. Evaluate alerting thresholds and maintenance implications.\n"
            "4. Assess integration with cockpit displays and maintenance systems.\n"
            "5. Synthesize doctrine for compliant vibration monitoring."
        ),
        key_factors=[
            "Sensor placement",
            "Alerting thresholds",
            "Data processing",
            "Integration with cockpit",
            "Maintenance implications"
        ],
        primary_authority=[
            "14 CFR Part 33.28",
            "EASA CS-E",
            "AC 33.28-1"
        ],
        burden_holder="Engine Health Monitoring Designer",
        adversary_position="Vibration monitoring is not required for modern engines.",
        counter_arguments=[
            "Monitoring supports early fault detection.",
            "Certification and reliability standards require monitoring.",
            "Predictive maintenance reduces unscheduled events."
        ],
        resolution_strategy="Equip with vibration monitoring; integrate with cockpit and maintenance systems.",
        entity_scope="AERO01 engines",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="AC 33.28-1"
    ),
    DoctrineBlock(
        topic="engine_firewall_integrity",
        keywords=["engine firewall", "integrity", "AERO01", "fire protection", "compartmentalization"],
        conclusion_template="AERO01 engine installations must maintain firewall integrity to prevent fire propagation to critical areas per Part 25.867.",
        reasoning_framework=(
            "1. Review Part 25.867 for engine firewall requirements.\n"
            "2. Analyze AERO01 firewall materials and installation.\n"
            "3. Evaluate fireproofing and compartmentalization.\n"
            "4. Assess maintenance and inspection procedures.\n"
            "5. Synthesize doctrine for compliant firewall integrity."
        ),
        key_factors=[
            "Firewall materials",
            "Installation quality",
            "Fireproofing",
            "Compartmentalization",
            "Inspection procedures"
        ],
        primary_authority=[
            "14 CFR Part 25.867",
            "EASA CS-25.867",
            "AC 25.867-1"
        ],
        burden_holder="Engine Installation Designer",
        adversary_position="Partial firewall coverage is sufficient.",
        counter_arguments=[
            "Full coverage is required for certification.",
            "Partial coverage increases fire risk.",
            "Certification mandates full firewall integrity."
        ],
        resolution_strategy="Install full fireproof firewall; verify via inspection and testing.",
        entity_scope="AERO01 engine installations",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AC 25.867-1"
    ),
    DoctrineBlock(
        topic="engine_oil_system",
        keywords=["engine oil", "lubrication", "AERO01", "system", "monitoring"],
        conclusion_template="AERO01 engine oil systems must provide continuous lubrication and monitoring, with alerts for low pressure or high temperature.",
        reasoning_framework=(
            "1. Review engine oil system requirements under Part 33 and Part 25.\n"
            "2. Analyze AERO01 oil supply, pumps, and filtration.\n"
            "3. Evaluate monitoring and alerting for pressure and temperature.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant oil system design."
        ),
        key_factors=[
            "Continuous lubrication",
            "Monitoring and alerting",
            "Filtration",
            "Maintenance procedures",
            "System reliability"
        ],
        primary_authority=[
            "14 CFR Part 33.37",
            "EASA CS-E 510",
            "AC 33.37-1"
        ],
        burden_holder="Engine Oil System Designer",
        adversary_position="Manual checks are sufficient for oil monitoring.",
        counter_arguments=[
            "Continuous monitoring is required for safety.",
            "Manual checks may miss rapid failures.",
            "Certification mandates automatic alerting."
        ],
        resolution_strategy="Design with continuous monitoring and alerting; verify via testing.",
        entity_scope="AERO01 engine oil systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 33.37-1"
    ),
    DoctrineBlock(
        topic="engine_bird_strike_protection",
        keywords=["engine", "bird strike", "protection", "AERO01", "ingestion", "certification"],
        conclusion_template="AERO01 engines must demonstrate bird strike protection per Part 33.77 and EASA CS-E 800.",
        reasoning_framework=(
            "1. Review Part 33.77 and CS-E 800 for bird strike requirements.\n"
            "2. Analyze AERO01 engine inlet and fan blade design.\n"
            "3. Evaluate test evidence for bird ingestion tolerance.\n"
            "4. Assess maintenance and inspection procedures.\n"
            "5. Synthesize doctrine for compliant bird strike protection."
        ),
        key_factors=[
            "Inlet/fan blade design",
            "Test evidence",
            "Ingestion tolerance",
            "Inspection procedures",
            "Certification compliance"
        ],
        primary_authority=[
            "14 CFR Part 33.77",
            "EASA CS-E 800",
            "AC 33.77-1"
        ],
        burden_holder="Engine Designer",
        adversary_position="Bird strike protection is not required for all engines.",
        counter_arguments=[
            "Certification mandates protection for all transport engines.",
            "Bird strikes are a significant operational risk.",
            "Test evidence is required for compliance."
        ],
        resolution_strategy="Demonstrate protection via testing and analysis; document compliance.",
        entity_scope="AERO01 engines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AC 33.77-1"
    ),
    DoctrineBlock(
        topic="engine_overspeed_protection",
        keywords=["engine", "overspeed", "protection", "AERO01", "FADEC", "safety"],
        conclusion_template="AERO01 engines must have automatic overspeed protection to prevent catastrophic failure per Part 33.27.",
        reasoning_framework=(
            "1. Review Part 33.27 for overspeed protection requirements.\n"
            "2. Analyze AERO01 FADEC and mechanical overspeed devices.\n"
            "3. Evaluate test evidence and failure modes.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant overspeed protection."
        ),
        key_factors=[
            "Automatic overspeed protection",
            "FADEC integration",
            "Mechanical devices",
            "Test evidence",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 33.27",
            "EASA CS-E 540",
            "AC 33.27-1"
        ],
        burden_holder="Engine Designer",
        adversary_position="Pilot monitoring is sufficient for overspeed prevention.",
        counter_arguments=[
            "Automatic protection is required for certification.",
            "Pilot response may be too slow.",
            "Mechanical backup is required."
        ],
        resolution_strategy="Integrate automatic and mechanical overspeed protection; verify via testing.",
        entity_scope="AERO01 engines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AC 33.27-1"
    ),
    DoctrineBlock(
        topic="engine_emergency_shutdown",
        keywords=["engine", "emergency shutdown", "AERO01", "fire", "failure", "procedure"],
        conclusion_template="AERO01 engines must support rapid emergency shutdown from cockpit controls per Part 25.1189.",
        reasoning_framework=(
            "1. Review Part 25.1189 for emergency shutdown requirements.\n"
            "2. Analyze AERO01 shutdown controls and logic.\n"
            "3. Evaluate response time and accessibility.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant emergency shutdown."
        ),
        key_factors=[
            "Rapid shutdown capability",
            "Cockpit control accessibility",
            "Response time",
            "Maintenance procedures",
            "System reliability"
        ],
        primary_authority=[
            "14 CFR Part 25.1189",
            "EASA CS-25.1189",
            "AC 25.1189-1"
        ],
        burden_holder="Engine Installation Designer",
        adversary_position="Shutdown from outside cockpit is sufficient.",
        counter_arguments=[
            "Cockpit shutdown is required for safety.",
            "External access may be delayed.",
            "Certification mandates cockpit controls."
        ],
        resolution_strategy="Provide cockpit emergency shutdown controls; verify via testing.",
        entity_scope="AERO01 engine installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 25.1189-1"
    ),
    DoctrineBlock(
        topic="engine_start_sequence",
        keywords=["engine", "start sequence", "AERO01", "starter", "ignition", "procedure"],
        conclusion_template="AERO01 engines must follow a prescribed start sequence with starter and ignition logic to ensure safe light-off.",
        reasoning_framework=(
            "1. Review engine start requirements under Part 33 and Part 25.\n"
            "2. Analyze AERO01 starter and ignition system integration.\n"
            "3. Evaluate start sequence logic and protections.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant engine start."
        ),
        key_factors=[
            "Prescribed start sequence",
            "Starter/ignition integration",
            "Logic protections",
            "Maintenance procedures",
            "System reliability"
        ],
        primary_authority=[
            "14 CFR Part 33.7",
            "EASA CS-E 70",
            "AC 33.7-1"
        ],
        burden_holder="Engine Start System Designer",
        adversary_position="Manual start sequence is sufficient.",
        counter_arguments=[
            "Automated sequence reduces error risk.",
            "Certification mandates prescribed logic.",
            "Manual sequence may miss protections."
        ],
        resolution_strategy="Implement automated start sequence with protections; verify via testing.",
        entity_scope="AERO01 engines",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AC 33.7-1"
    ),
    DoctrineBlock(
        topic="engine_thrust_reverser",
        keywords=["engine", "thrust reverser", "AERO01", "landing", "deceleration", "system"],
        conclusion_template="AERO01 engines must be equipped with certified thrust reversers to assist in landing deceleration per Part 25.933.",
        reasoning_framework=(
            "1. Review Part 25.933 for thrust reverser requirements.\n"
            "2. Analyze AERO01 thrust reverser design and certification.\n"
            "3. Evaluate integration with cockpit controls and braking systems.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant thrust reverser operation."
        ),
        key_factors=[
            "Certified thrust reverser",
            "Integration with controls",
            "Braking system coordination",
            "Maintenance procedures",
            "System reliability"
        ],
        primary_authority=[
            "14 CFR Part 25.933",
            "EASA CS-25.933",
            "AC 25.933-1"
        ],
        burden_holder="Engine Installation Designer",
        adversary_position="Thrust reversers are not required for all runways.",
        counter_arguments=[
            "Certification mandates reversers for certain operations.",
            "Reversers improve landing safety.",
            "Some runways require reversers for compliance."
        ],
        resolution_strategy="Equip with certified thrust reversers; verify via testing.",
        entity_scope="AERO01 engines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 25.933-1"
    ),
    DoctrineBlock(
        topic="engine_exhaust_emissions",
        keywords=["engine", "exhaust", "emissions", "AERO01", "environment", "ICAO"],
        conclusion_template="AERO01 engines must comply with ICAO Annex 16 and Part 34 exhaust emissions standards.",
        reasoning_framework=(
            "1. Review ICAO Annex 16 and Part 34 for emissions requirements.\n"
            "2. Analyze AERO01 engine emissions data (NOx, CO, HC, smoke).\n"
            "3. Evaluate test evidence and certification reports.\n"
            "4. Assess operational and maintenance implications.\n"
            "5. Synthesize doctrine for compliant emissions."
        ),
        key_factors=[
            "ICAO/FAA emissions standards",
            "Test evidence",
            "Certification reports",
            "Operational implications",
            "Maintenance procedures"
        ],
        primary_authority=[
            "14 CFR Part 34",
            "ICAO Annex 16",
            "EASA CS-34"
        ],
        burden_holder="Engine Manufacturer",
        adversary_position="Emissions compliance is not required for all markets.",
        counter_arguments=[
            "Certification mandates emissions compliance.",
            "Non-compliance restricts market access.",
            "Environmental standards are legally binding."
        ],
        resolution_strategy="Demonstrate compliance via testing and reporting; maintain documentation.",
        entity_scope="AERO01 engines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ICAO Annex 16"
    ),
    DoctrineBlock(
        topic="engine_noise_compliance",
        keywords=["engine", "noise", "compliance", "AERO01", "ICAO", "Part 36"],
        conclusion_template="AERO01 engines must comply with ICAO Annex 16 Volume I and Part 36 noise certification standards.",
        reasoning_framework=(
            "1. Review ICAO Annex 16 Volume I and Part 36 for noise requirements.\n"
            "2. Analyze AERO01 engine noise data and certification tests.\n"
            "3. Evaluate operational noise abatement procedures.\n"
            "4. Assess maintenance and operational implications.\n"
            "5. Synthesize doctrine for compliant noise certification."
        ),
        key_factors=[
            "ICAO/FAA noise standards",
            "Certification tests",
            "Operational procedures",
            "Maintenance implications",
            "Documentation"
        ],
        primary_authority=[
            "14 CFR Part 36",
            "ICAO Annex 16 Volume I",
            "EASA CS-36"
        ],
        burden_holder="Engine Manufacturer",
        adversary_position="Noise compliance is not required for all airports.",
        counter_arguments=[
            "Certification mandates noise compliance.",
            "Non-compliance restricts airport access.",
            "Noise standards are legally binding."
        ],
        resolution_strategy="Demonstrate compliance via testing and reporting; maintain documentation.",
        entity_scope="AERO01 engines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="ICAO Annex 16 Volume I"
    ),
    DoctrineBlock(
        topic="engine_inlet_icing_protection",
        keywords=["engine", "inlet", "icing protection", "AERO01", "anti-ice", "bleed air"],
        conclusion_template="AERO01 engine inlets must be equipped with anti-icing systems to prevent hazardous ice formation per Part 25.1093.",
        reasoning_framework=(
            "1. Review Part 25.1093 for inlet icing protection requirements.\n"
            "2. Analyze AERO01 inlet anti-ice system design (bleed air, electrical).\n"
            "3. Evaluate effectiveness in known icing conditions.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant inlet icing protection."
        ),
        key_factors=[
            "Anti-icing system design",
            "Effectiveness in icing",
            "Maintenance procedures",
            "Operational procedures",
            "Certification compliance"
        ],
        primary_authority=[
            "14 CFR Part 25.1093",
            "EASA CS-25.1093",
            "AC 25.1093-1"
        ],
        burden_holder="Engine Installation Designer",
        adversary_position="Inlet anti-ice is not required for all operations.",
        counter_arguments=[
            "Certification mandates anti-ice for all certified conditions.",
            "Unexpected icing can occur at any time.",
            "System must be effective in all certified conditions."
        ],
        resolution_strategy="Equip with effective anti-ice; verify via icing tests.",
        entity_scope="AERO01 engine installations",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 25.1093-1"
    ),
    DoctrineBlock(
        topic="engine_fuel_filtering",
        keywords=["engine", "fuel", "filtering", "AERO01", "contamination", "system"],
        conclusion_template="AERO01 engines must be equipped with fuel filtering to prevent contamination and ensure reliable operation.",
        reasoning_framework=(
            "1. Review engine fuel system requirements under Part 33 and Part 25.\n"
            "2. Analyze AERO01 fuel filter design and placement.\n"
            "3. Evaluate effectiveness against contamination.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant fuel filtering."
        ),
        key_factors=[
            "Filter design and placement",
            "Effectiveness against contamination",
            "Maintenance procedures",
            "Operational reliability",
            "Certification compliance"
        ],
        primary_authority=[
            "14 CFR Part 33.35",
            "EASA CS-E 510",
            "AC 33.35-1"
        ],
        burden_holder="Engine Fuel System Designer",
        adversary_position="Fuel filtering is not required for all engines.",
        counter_arguments=[
            "Certification mandates fuel filtering.",
            "Contamination can cause engine failure.",
            "Maintenance intervals depend on filter effectiveness."
        ],
        resolution_strategy="Design with effective fuel filtering; verify via testing.",
        entity_scope="AERO01 engines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 33.35-1"
    ),
    DoctrineBlock(
        topic="engine_FADEC_power_supply",
        keywords=["engine", "FADEC", "power supply", "AERO01", "redundancy", "control"],
        conclusion_template="AERO01 FADEC systems must have dual-redundant power supplies to ensure continuous engine control.",
        reasoning_framework=(
            "1. Review FADEC power supply requirements under Part 33 and Part 25.\n"
            "2. Analyze AERO01 FADEC power architecture and redundancy.\n"
            "3. Evaluate failure modes and backup provisions.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant FADEC power supply."
        ),
        key_factors=[
            "Dual-redundant power supplies",
            "Failure modes",
            "Backup provisions",
            "Maintenance procedures",
            "System reliability"
        ],
        primary_authority=[
            "14 CFR Part 33.28",
            "EASA CS-E 50",
            "AC 33.28-1"
        ],
        burden_holder="FADEC System Designer",
        adversary_position="Single power supply is sufficient.",
        counter_arguments=[
            "Dual-redundancy is required for fault tolerance.",
            "Single supply increases risk of engine shutdown.",
            "Certification mandates dual-redundant power."
        ],
        resolution_strategy="Design with dual-redundant power; verify via testing.",
        entity_scope="AERO01 FADEC systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 33.28-1"
    ),
    DoctrineBlock(
        topic="engine_EICAS_integration",
        keywords=["engine", "EICAS", "integration", "AERO01", "cockpit", "display"],
        conclusion_template="AERO01 engine parameters must be fully integrated into EICAS for real-time monitoring and alerting.",
        reasoning_framework=(
            "1. Review cockpit display and alerting requirements under Part 25.\n"
            "2. Analyze AERO01 EICAS integration with engine sensors and FADEC.\n"
            "3. Evaluate display clarity and alert prioritization.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant EICAS integration."
        ),
        key_factors=[
            "Parameter integration",
            "Display clarity",
            "Alert prioritization",
            "Maintenance procedures",
            "Operational reliability"
        ],
        primary_authority=[
            "14 CFR Part 25.1322",
            "EASA CS-25.1322",
            "AC 25.1322-1"
        ],
        burden_holder="Avionics Integrator",
        adversary_position="Engine parameters can be displayed on analog gauges only.",
        counter_arguments=[
            "EICAS improves situational awareness.",
            "Certification mandates integrated alerting.",
            "Analog displays lack prioritization."
        ],
        resolution_strategy="Integrate engine data into EICAS; verify via cockpit testing.",
        entity_scope="AERO01 EICAS-equipped aircraft",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 25.1322-1"
    ),
    DoctrineBlock(
        topic="engine_maintenance_data_recording",
        keywords=["engine", "maintenance", "data recording", "AERO01", "trend monitoring"],
        conclusion_template="AERO01 engines must record maintenance and trend data for predictive maintenance and regulatory compliance.",
        reasoning_framework=(
            "1. Review maintenance data recording requirements under Part 25 and Part 121.\n"
            "2. Analyze AERO01 data acquisition and recording systems.\n"
            "3. Evaluate data retention and accessibility for maintenance personnel.\n"
            "4. Assess integration with predictive maintenance programs.\n"
            "5. Synthesize doctrine for compliant data recording."
        ),
        key_factors=[
            "Data acquisition",
            "Retention and accessibility",
            "Integration with maintenance",
            "Predictive maintenance",
            "Regulatory compliance"
        ],
        primary_authority=[
            "14 CFR Part 121.373",
            "EASA Part M",
            "AC 120-16G"
        ],
        burden_holder="Operator",
        adversary_position="Manual logbooks are sufficient for maintenance.",
        counter_arguments=[
            "Automated recording improves reliability.",
            "Certification mandates data retention.",
            "Predictive maintenance requires automated data."
        ],
        resolution_strategy="Implement automated data recording; integrate with maintenance programs.",
        entity_scope="AERO01 engines",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="AC 120-16G"
    ),
    DoctrineBlock(
        topic="engine_flight_crew_training",
        keywords=["engine", "flight crew", "training", "AERO01", "procedures"],
        conclusion_template="AERO01 flight crews must receive type-specific engine training covering normal, abnormal, and emergency procedures.",
        reasoning_framework=(
            "1. Review flight crew training requirements under Part 121 and Part 25.\n"
            "2. Analyze AERO01 engine-specific training curriculum.\n"
            "3. Evaluate coverage of normal, abnormal, and emergency procedures.\n"
            "4. Assess recurrent training and proficiency checks.\n"
            "5. Synthesize doctrine for compliant flight crew training."
        ),
        key_factors=[
            "Type-specific curriculum",
            "Normal/abnormal/emergency procedures",
            "Recurrent training",
            "Proficiency checks",
            "Regulatory compliance"
        ],
        primary_authority=[
            "14 CFR Part 121.415",
            "EASA Part ORO.FC",
            "AC 120-53B"
        ],
        burden_holder="Operator",
        adversary_position="General engine training is sufficient.",
        counter_arguments=[
            "Type-specific training improves safety.",
            "Certification mandates type-specific curriculum.",
            "General training may miss critical differences."
        ],
        resolution_strategy="Provide type-specific engine training; verify via proficiency checks.",
        entity_scope="AERO01 flight crews",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 120-53B"
    ),
    DoctrineBlock(
        topic="engine_ETOPS_compliance",
        keywords=["engine", "ETOPS", "compliance", "AERO01", "reliability", "maintenance"],
        conclusion_template="AERO01 engines must meet ETOPS reliability and maintenance requirements for extended operations.",
        reasoning_framework=(
            "1. Review ETOPS requirements under Part 25.1535 and Part 121.161.\n"
            "2. Analyze AERO01 engine reliability data and maintenance program.\n"
            "3. Evaluate compliance with ETOPS dispatch and in-flight procedures.\n"
            "4. Assess operator training and documentation.\n"
            "5. Synthesize doctrine for compliant ETOPS operation."
        ),
        key_factors=[
            "Reliability data",
            "Maintenance program",
            "Dispatch procedures",
            "Operator training",
            "Documentation"
        ],
        primary_authority=[
            "14 CFR Part 25.1535",
            "14 CFR Part 121.161",
            "AC 120-42B"
        ],
        burden_holder="Operator",
        adversary_position="ETOPS is not required for all operations.",
        counter_arguments=[
            "ETOPS is required for extended overwater/remote ops.",
            "Certification mandates ETOPS for certain routes.",
            "Reliability and maintenance are critical for ETOPS."
        ],
        resolution_strategy="Meet ETOPS requirements; document compliance and monitor reliability.",
        entity_scope="AERO01 engines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 120-42B"
    ),
    DoctrineBlock(
        topic="engine_in_flight_restart",
        keywords=["engine", "in-flight restart", "AERO01", "procedure", "reliability"],
        conclusion_template="AERO01 engines must demonstrate in-flight restart capability per Part 33.74 and provide cockpit procedures.",
        reasoning_framework=(
            "1. Review Part 33.74 for in-flight restart requirements.\n"
            "2. Analyze AERO01 engine restart envelope and procedures.\n"
            "3. Evaluate restart reliability and time.\n"
            "4. Assess cockpit indications and controls.\n"
            "5. Synthesize doctrine for compliant in-flight restart."
        ),
        key_factors=[
            "Restart envelope",
            "Reliability",
            "Cockpit procedures",
            "Indications and controls",
            "Certification compliance"
        ],
        primary_authority=[
            "14 CFR Part 33.74",
            "EASA CS-E 740",
            "AC 33.74-1"
        ],
        burden_holder="Engine Designer",
        adversary_position="In-flight restart is not required for all engines.",
        counter_arguments=[
            "Certification mandates restart capability.",
            "Restart improves safety in flameout scenarios.",
            "Cockpit procedures must be documented."
        ],
        resolution_strategy="Demonstrate restart capability; provide cockpit procedures and training.",
        entity_scope="AERO01 engines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 33.74-1"
    ),
    DoctrineBlock(
        topic="engine_hot_start_protection",
        keywords=["engine", "hot start", "protection", "AERO01", "FADEC", "start sequence"],
        conclusion_template="AERO01 engines must have hot start protection logic to prevent thermal damage during engine start.",
        reasoning_framework=(
            "1. Review engine start and thermal protection requirements under Part 33.\n"
            "2. Analyze AERO01 FADEC hot start logic and protections.\n"
            "3. Evaluate start sequence monitoring and abort criteria.\n"
            "4. Assess maintenance and operational procedures.\n"
            "5. Synthesize doctrine for compliant hot start protection."
        ),
        key_factors=[
            "Hot start logic",
            "Start sequence monitoring",
            "Abort criteria",
            "Maintenance procedures",
            "Certification compliance"
        ],
        primary_authority=[
            "14 CFR Part 33.7",
            "EASA CS-E 70",
            "AC 33.7-1"
        ],
        burden_holder="Engine Start System Designer",
        adversary_position="Pilot monitoring is sufficient for hot start prevention.",
        counter_arguments=[
            "Automatic protection reduces risk of thermal damage.",
            "Certification mandates hot start logic.",
            "Manual monitoring may be too slow."
        ],
        resolution_strategy="Implement hot start logic in FADEC; verify via testing.",
        entity_scope="AERO01 engines",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="AC 33.7-1"
    ),
    DoctrineBlock(
        topic="engine_FADEC_software_assurance",
        keywords=["engine", "FADEC", "software assurance", "AERO01", "DO-178C", "certification"],
        conclusion_template="AERO01 FADEC software must comply with DO-178C Level A assurance for engine control functions.",
        reasoning_framework=(
            "1. Review DO-178C and Part 33 for software assurance requirements.\n"
            "2. Analyze AERO01 FADEC software development and verification processes.\n"
            "3. Evaluate test evidence and configuration management.\n"
            "4. Assess integration with engine control hardware.\n"
            "5. Synthesize doctrine for compliant software assurance."
        ),
        key_factors=[
            "DO-178C Level A assurance",
            "Verification processes",
            "Test evidence",
            "Configuration management",
            "Certification compliance"
        ],
        primary_authority=[
            "DO-178C",
            "14 CFR Part 33.28",
            "EASA AMC 20-115C"
        ],
        burden_holder="FADEC Software Developer",
        adversary_position="Level B assurance is sufficient for engine control.",
        counter_arguments=[
            "Level A is required for catastrophic failure conditions.",
            "Certification mandates Level A for engine control.",
            "Level B may not meet safety objectives."
        ],
        resolution_strategy="Develop and verify FADEC software to Level A; document compliance.",
        entity_scope="AERO01 FADEC systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="DO-178C"
    ),
    DoctrineBlock(
        topic="engine_control_loss_protection",
        keywords=["engine", "control loss", "protection", "AERO01", "fail-safe", "redundancy"],
        conclusion_template="AERO01 engine control systems must be designed to prevent total loss of control through redundancy and fail-safe logic.",
        reasoning_framework=(
            "1. Review engine control system requirements under Part 33 and Part 25.\n"
            "2. Analyze AERO01 control system architecture and redundancy.\n"
            "3. Evaluate fail-safe logic and backup provisions.\n"
            "4. Assess failure modes and operational procedures.\n"
            "5. Synthesize doctrine for compliant control loss protection."
        ),
        key_factors=[
            "System redundancy",
            "Fail-safe logic",
            "Backup provisions",
            "Failure mode analysis",
            "Certification compliance"
        ],
        primary_authority=[
            "14 CFR Part 33.28",
            "EASA CS-E 50",
            "AC 33.28-1"
        ],
        burden_holder="Engine Control System Designer",
        adversary_position="Single-channel control is sufficient.",
        counter_arguments=[
            "Redundancy is required for fail-safe operation.",
            "Certification mandates backup provisions.",
            "Single-channel increases risk of total loss."
        ],
        resolution_strategy="Design with redundancy and fail-safe logic; verify via testing.",
        entity_scope="AERO01 engine control systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AC 33.28-1"
    ),
    DoctrineBlock(
        topic="engine_critical_part_tracking",
        keywords=["engine", "critical part", "tracking", "AERO01", "life-limited", "maintenance"],
        conclusion_template="AERO01 engine critical parts must be tracked for life limits and replaced per manufacturer and regulatory requirements.",
        reasoning_framework=(
            "1. Review critical part tracking requirements under Part 33 and Part 43.\n"
            "2. Analyze AERO01 critical part identification and tracking systems.\n"
            "3. Evaluate life limit documentation and replacement procedures.\n"
            "4. Assess maintenance and operational implications.\n"
            "5. Synthesize doctrine for compliant critical part tracking."
        ),
        key_factors=[
            "Part identification",
            "Life limit documentation",
            "Replacement procedures",
            "Maintenance tracking",
            "Regulatory compliance"
        ],
        primary_authority=[
            "14 CFR Part 33.70",
            "EASA CS-E 515",
            "AC 33.70-1"
        ],
        burden_holder="Operator",
        adversary_position="Critical part tracking is not required for all engines.",
        counter_arguments=[
            "Certification mandates tracking for all life-limited parts.",
            "Failure to track increases risk of catastrophic failure.",
            "Maintenance programs require accurate tracking."
        ],
        resolution_strategy="Implement tracking for all critical parts; verify compliance.",
        entity_scope="AERO01 engines",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="AC 33.70-1"
    ),
    DoctrineBlock(
        topic="engine_maintenance_manual_compliance",
        keywords=["engine", "maintenance manual", "compliance", "AERO01", "procedures"],
        conclusion_template="AERO01 engine maintenance must be performed in accordance with the approved maintenance manual to ensure continued airworthiness.",
        reasoning_framework=(
            "1. Review maintenance manual requirements under Part 43 and Part 145.\n"
            "2. Analyze AERO01 maintenance manual content and approval.\n"
            "3. Evaluate compliance monitoring and documentation.\n"
            "4. Assess maintenance personnel training.\n"
            "5. Synthesize doctrine for compliant maintenance."
        ),
        key_factors=[
            "Approved manual content",
            "Compliance monitoring",
            "Documentation",
            "Personnel training",
            "Regulatory compliance"
        ],
        primary_authority=[
            "14 CFR Part 43",
            "EASA Part M",
            "AC 43-9C"
        ],
        burden_holder="Maintenance Provider",
        adversary_position="Alternative procedures are acceptable without approval.",
        counter_arguments=[
            "Certification mandates use of approved manuals.",
            "Alternative procedures require approval.",
            "Non-compliance voids airworthiness."
        ],
        resolution_strategy="Perform maintenance per approved manual; monitor and document compliance.",
        entity_scope="AERO01 engines",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="AC 43-9C"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if (keyword_lower in doctrine.topic.lower() or
            any(keyword_lower in k.lower() for k in doctrine.keywords) or
            keyword_lower in doctrine.reasoning_framework.lower() or
            keyword_lower in doctrine.conclusion_template.lower()):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]