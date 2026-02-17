from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
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
        keywords=["turbofan", "engine", "operation", "fuel efficiency", "thrust", "maintenance"],
        conclusion_template="Turbofan engine operation must optimize thrust output while maintaining fuel efficiency and complying with regulatory maintenance intervals.",
        reasoning_framework="""
        Turbofan engines are the primary propulsion systems for freight locomotives in the RAIL04 domain. The operational doctrine requires balancing thrust output with fuel efficiency, considering environmental regulations and scheduled maintenance. Engine performance is monitored via digital sensors, and deviations from optimal parameters trigger maintenance actions. The doctrine emphasizes the importance of adhering to manufacturer specifications and FAA/EASA guidelines, especially regarding emission standards and noise abatement. Freight operations must account for varying load conditions, ensuring engines operate within safe temperature and pressure ranges. The reasoning incorporates risk assessment for engine failure, redundancy planning, and real-time diagnostics.
        """,
        key_factors=[
            "Thrust output",
            "Fuel consumption",
            "Emission standards",
            "Maintenance schedules",
            "Load variability",
            "Sensor diagnostics"
        ],
        primary_authority=[
            "FAA AC 33-1",
            "EASA CS-E",
            "Engine Manufacturer Manuals"
        ],
        burden_holder="Operator",
        adversary_position="Engine operation can prioritize thrust over efficiency, risking regulatory violations.",
        counter_arguments=[
            "Efficiency is secondary to operational demands.",
            "Maintenance can be deferred for cost savings."
        ],
        resolution_strategy="Strict adherence to regulatory and manufacturer guidelines; real-time monitoring and scheduled maintenance.",
        entity_scope="RAIL04 freight locomotives",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 33-1 Turbofan Engine Operation"
    ),
    DoctrineBlock(
        topic="fly_by_wire_flight_controls",
        keywords=["fly by wire", "flight controls", "digital", "redundancy", "safety"],
        conclusion_template="Fly-by-wire flight control systems must ensure redundancy, digital integrity, and fail-safe operation for freight locomotives.",
        reasoning_framework="""
        Fly-by-wire systems replace mechanical linkages with digital controls, increasing reliability and reducing weight. The doctrine mandates triple-redundant control channels, robust software validation, and electromagnetic interference protection. Freight operations require rapid response to control inputs, with system health monitored continuously. Failure modes are analyzed using FMEA, and backup manual controls are provided in accordance with Part 25 certification. The doctrine integrates cybersecurity measures to prevent unauthorized access and ensures compliance with RTCA DO-178C software standards. Operator training is essential for understanding digital control nuances.
        """,
        key_factors=[
            "Redundancy",
            "Software validation",
            "Electromagnetic interference",
            "Cybersecurity",
            "Operator training"
        ],
        primary_authority=[
            "FAA Part 25.671",
            "RTCA DO-178C",
            "EASA CS-25"
        ],
        burden_holder="System Integrator",
        adversary_position="Digital controls are vulnerable to software bugs and cyber threats.",
        counter_arguments=[
            "Mechanical backups are sufficient.",
            "Cybersecurity is not a primary concern."
        ],
        resolution_strategy="Implement triple redundancy, rigorous software testing, and cybersecurity protocols.",
        entity_scope="RAIL04 digital flight control systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.671 Fly-by-Wire Controls"
    ),
    DoctrineBlock(
        topic="glass_cockpit_avionics",
        keywords=["glass cockpit", "avionics", "display", "integration", "data fusion"],
        conclusion_template="Glass cockpit avionics must provide integrated, real-time data displays with intuitive interfaces for freight locomotive operators.",
        reasoning_framework="""
        Glass cockpit systems consolidate navigation, engine, and environmental data into digital displays. The doctrine requires high-resolution screens, redundant data buses, and ergonomic interface design. Freight operations prioritize situational awareness, with customizable display layouts and alert prioritization. Data fusion algorithms combine sensor inputs to reduce operator workload. System reliability is ensured through hardware redundancy and software validation. Compliance with ARINC 661 and FAA/EASA display standards is mandatory. Operator feedback is incorporated into interface updates, and training programs are developed for new display technologies.
        """,
        key_factors=[
            "Display resolution",
            "Data integration",
            "Ergonomics",
            "Redundancy",
            "Operator training"
        ],
        primary_authority=[
            "ARINC 661",
            "FAA AC 20-173",
            "EASA AMC 20-23"
        ],
        burden_holder="Avionics Supplier",
        adversary_position="Complex interfaces increase operator workload and risk misinterpretation.",
        counter_arguments=[
            "Traditional analog displays are more reliable.",
            "Data fusion may obscure critical information."
        ],
        resolution_strategy="User-centered design, rigorous testing, and operator training.",
        entity_scope="RAIL04 glass cockpit systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ARINC 661 Glass Cockpit Avionics"
    ),
    DoctrineBlock(
        topic="aircraft_electrical_system",
        keywords=["electrical", "power distribution", "redundancy", "battery", "generator"],
        conclusion_template="Electrical systems must ensure continuous power supply, redundancy, and compliance with safety standards in freight operations.",
        reasoning_framework="""
        The electrical doctrine mandates dual-generator configurations, battery backup, and intelligent power distribution. Freight locomotives require robust wiring harnesses and surge protection. System health is monitored via real-time diagnostics, and load shedding protocols are implemented during failures. Compliance with FAA Part 25.1351 and EASA CS-25.1351 is required. Maintenance intervals are based on operational hours and environmental exposure. Safety is prioritized through circuit isolation and fire protection measures. Operator training covers emergency power procedures and troubleshooting.
        """,
        key_factors=[
            "Power continuity",
            "Redundancy",
            "Surge protection",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA Part 25.1351",
            "EASA CS-25.1351",
            "IEEE 802.3"
        ],
        burden_holder="Electrical Engineer",
        adversary_position="Single-generator systems are cost-effective and sufficient.",
        counter_arguments=[
            "Redundancy increases weight and complexity.",
            "Battery backup is rarely used."
        ],
        resolution_strategy="Dual-generator design, battery backup, and compliance with safety standards.",
        entity_scope="RAIL04 electrical systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.1351 Electrical Systems"
    ),
    DoctrineBlock(
        topic="hydraulic_flight_control_system",
        keywords=["hydraulic", "flight control", "pressure", "redundancy", "maintenance"],
        conclusion_template="Hydraulic flight control systems must maintain pressure integrity, redundancy, and scheduled maintenance for safe freight operations.",
        reasoning_framework="""
        Hydraulic systems actuate control surfaces and landing gear. The doctrine requires triple-redundant hydraulic circuits, pressure monitoring, and leak detection. Freight locomotives must use high-grade hydraulic fluids and corrosion-resistant components. Maintenance schedules are based on cycle counts and fluid analysis. Compliance with FAA Part 25.1435 and EASA CS-25.1435 is mandatory. Emergency procedures include manual reversion and isolation of failed circuits. Operator training includes hydraulic system troubleshooting and emergency response.
        """,
        key_factors=[
            "Pressure integrity",
            "Redundancy",
            "Fluid quality",
            "Leak detection",
            "Maintenance"
        ],
        primary_authority=[
            "FAA Part 25.1435",
            "EASA CS-25.1435",
            "Hydraulic Manufacturer Guidelines"
        ],
        burden_holder="Maintenance Crew",
        adversary_position="Redundancy is unnecessary; single circuit suffices.",
        counter_arguments=[
            "Triple redundancy increases cost.",
            "Manual reversion is rarely needed."
        ],
        resolution_strategy="Triple-redundant design, fluid monitoring, and scheduled maintenance.",
        entity_scope="RAIL04 hydraulic systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.1435 Hydraulic Systems"
    ),
    DoctrineBlock(
        topic="aircraft_fuel_system",
        keywords=["fuel", "system", "distribution", "monitoring", "contamination"],
        conclusion_template="Fuel systems must ensure contamination-free distribution, real-time monitoring, and compliance with safety standards in freight operations.",
        reasoning_framework="""
        The fuel system doctrine emphasizes contamination prevention, real-time flow monitoring, and redundancy in fuel pumps. Freight locomotives must use certified fuel types and adhere to storage protocols. Compliance with FAA Part 25.951 and EASA CS-25.951 is required. Maintenance includes regular filter replacement and tank inspections. Emergency procedures address fuel leaks and pump failures. Operator training covers fuel management and emergency response. System health is monitored via digital sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Contamination prevention",
            "Flow monitoring",
            "Pump redundancy",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA Part 25.951",
            "EASA CS-25.951",
            "Fuel Manufacturer Guidelines"
        ],
        burden_holder="Fuel System Engineer",
        adversary_position="Contamination risk is minimal; monitoring is unnecessary.",
        counter_arguments=[
            "Redundant pumps add weight.",
            "Digital sensors are prone to failure."
        ],
        resolution_strategy="Redundant pumps, real-time monitoring, and scheduled maintenance.",
        entity_scope="RAIL04 fuel systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.951 Fuel Systems"
    ),
    DoctrineBlock(
        topic="bleed_air_pneumatic_system",
        keywords=["bleed air", "pneumatic", "pressure", "temperature", "safety"],
        conclusion_template="Bleed air pneumatic systems must regulate pressure and temperature, ensure safety, and comply with freight operation standards.",
        reasoning_framework="""
        Bleed air systems provide pneumatic power for environmental controls and anti-icing. The doctrine requires pressure regulation, temperature monitoring, and leak detection. Freight locomotives must use certified materials for ducting and valves. Compliance with FAA Part 25.1309 and EASA CS-25.1309 is mandatory. Maintenance includes regular inspection of ducts and valves. Emergency procedures address overpressure and leaks. Operator training covers system operation and emergency response. System health is monitored via digital sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Pressure regulation",
            "Temperature monitoring",
            "Leak detection",
            "Material certification",
            "Maintenance"
        ],
        primary_authority=[
            "FAA Part 25.1309",
            "EASA CS-25.1309",
            "Pneumatic Manufacturer Guidelines"
        ],
        burden_holder="Pneumatic Engineer",
        adversary_position="Pressure regulation is unnecessary; overpressure risk is minimal.",
        counter_arguments=[
            "Temperature monitoring is redundant.",
            "Leak detection adds complexity."
        ],
        resolution_strategy="Pressure regulation, temperature monitoring, and scheduled maintenance.",
        entity_scope="RAIL04 pneumatic systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.1309 Pneumatic Systems"
    ),
    DoctrineBlock(
        topic="landing_gear_system",
        keywords=["landing gear", "retraction", "extension", "braking", "safety"],
        conclusion_template="Landing gear systems must ensure reliable retraction, extension, and braking, with redundancy and compliance for freight operations.",
        reasoning_framework="""
        Landing gear doctrine mandates redundant actuation systems, robust braking mechanisms, and regular inspection. Freight locomotives require corrosion-resistant materials and hydraulic/electric actuation. Compliance with FAA Part 25.729 and EASA CS-25.729 is required. Maintenance includes cycle-based inspections and lubrication. Emergency procedures address gear extension failures and brake malfunctions. Operator training covers gear operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Redundant actuation",
            "Braking reliability",
            "Corrosion resistance",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA Part 25.729",
            "EASA CS-25.729",
            "Landing Gear Manufacturer Guidelines"
        ],
        burden_holder="Landing Gear Engineer",
        adversary_position="Redundant actuation is unnecessary; single system suffices.",
        counter_arguments=[
            "Braking reliability is overstated.",
            "Corrosion resistance adds cost."
        ],
        resolution_strategy="Redundant actuation, robust braking, and scheduled maintenance.",
        entity_scope="RAIL04 landing gear systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.729 Landing Gear Systems"
    ),
    DoctrineBlock(
        topic="environmental_control_system",
        keywords=["environmental control", "temperature", "humidity", "air quality", "safety"],
        conclusion_template="Environmental control systems must regulate temperature, humidity, and air quality, ensuring operator safety and comfort in freight operations.",
        reasoning_framework="""
        Environmental control doctrine requires real-time monitoring of temperature, humidity, and air quality. Freight locomotives must use certified HVAC components and filters. Compliance with FAA Part 25.831 and EASA CS-25.831 is mandatory. Maintenance includes regular filter replacement and system inspection. Emergency procedures address HVAC failures and air contamination. Operator training covers system operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Temperature regulation",
            "Humidity control",
            "Air quality monitoring",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA Part 25.831",
            "EASA CS-25.831",
            "HVAC Manufacturer Guidelines"
        ],
        burden_holder="Environmental Engineer",
        adversary_position="Air quality monitoring is unnecessary; comfort is secondary.",
        counter_arguments=[
            "Humidity control adds complexity.",
            "Temperature regulation is sufficient."
        ],
        resolution_strategy="Real-time monitoring, certified components, and scheduled maintenance.",
        entity_scope="RAIL04 environmental control systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.831 Environmental Control Systems"
    ),
    DoctrineBlock(
        topic="fire_detection_suppression",
        keywords=["fire detection", "suppression", "safety", "maintenance", "regulation"],
        conclusion_template="Fire detection and suppression systems must ensure rapid response, compliance, and scheduled maintenance for freight operations.",
        reasoning_framework="""
        Fire detection doctrine mandates real-time monitoring, rapid suppression, and regular system inspection. Freight locomotives must use certified fire detection sensors and suppression agents. Compliance with FAA Part 25.851 and EASA CS-25.851 is required. Maintenance includes regular inspection and agent replacement. Emergency procedures address fire outbreaks and system failures. Operator training covers fire response and suppression system operation. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Rapid detection",
            "Suppression reliability",
            "Certified agents",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA Part 25.851",
            "EASA CS-25.851",
            "Fire Suppression Manufacturer Guidelines"
        ],
        burden_holder="Safety Engineer",
        adversary_position="Rapid suppression is unnecessary; detection suffices.",
        counter_arguments=[
            "Certified agents add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Real-time monitoring, certified agents, and scheduled maintenance.",
        entity_scope="RAIL04 fire detection and suppression systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.851 Fire Detection and Suppression"
    ),
    DoctrineBlock(
        topic="oxygen_system",
        keywords=["oxygen", "system", "safety", "emergency", "maintenance"],
        conclusion_template="Oxygen systems must ensure availability, safety, and compliance for freight operations, with scheduled maintenance and emergency procedures.",
        reasoning_framework="""
        Oxygen system doctrine requires real-time monitoring, emergency availability, and regular inspection. Freight locomotives must use certified oxygen tanks and delivery systems. Compliance with FAA Part 25.1447 and EASA CS-25.1447 is mandatory. Maintenance includes regular inspection and tank replacement. Emergency procedures address oxygen depletion and system failures. Operator training covers system operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Availability",
            "Safety",
            "Certified tanks",
            "Maintenance",
            "Emergency procedures"
        ],
        primary_authority=[
            "FAA Part 25.1447",
            "EASA CS-25.1447",
            "Oxygen System Manufacturer Guidelines"
        ],
        burden_holder="Safety Engineer",
        adversary_position="Emergency oxygen is unnecessary; system failures are rare.",
        counter_arguments=[
            "Certified tanks add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Real-time monitoring, certified tanks, and scheduled maintenance.",
        entity_scope="RAIL04 oxygen systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.1447 Oxygen Systems"
    ),
    DoctrineBlock(
        topic="APU_auxiliary_power_unit",
        keywords=["APU", "auxiliary power", "backup", "maintenance", "safety"],
        conclusion_template="APU systems must provide reliable auxiliary power, backup capability, and comply with maintenance and safety standards for freight operations.",
        reasoning_framework="""
        APU doctrine mandates reliable auxiliary power, backup capability, and regular inspection. Freight locomotives must use certified APU units and adhere to operational protocols. Compliance with FAA Part 25.1309 and EASA CS-25.1309 is required. Maintenance includes regular inspection and unit replacement. Emergency procedures address APU failures and power outages. Operator training covers APU operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Auxiliary power",
            "Backup capability",
            "Certified units",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA Part 25.1309",
            "EASA CS-25.1309",
            "APU Manufacturer Guidelines"
        ],
        burden_holder="Electrical Engineer",
        adversary_position="Backup capability is unnecessary; main power is sufficient.",
        counter_arguments=[
            "Certified units add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Reliable auxiliary power, certified units, and scheduled maintenance.",
        entity_scope="RAIL04 APU systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.1309 APU Systems"
    ),
    DoctrineBlock(
        topic="ice_protection_systems",
        keywords=["ice protection", "de-icing", "anti-icing", "safety", "maintenance"],
        conclusion_template="Ice protection systems must ensure effective de-icing and anti-icing, safety, and compliance for freight operations, with scheduled maintenance.",
        reasoning_framework="""
        Ice protection doctrine requires effective de-icing and anti-icing, safety, and regular inspection. Freight locomotives must use certified ice protection systems and adhere to operational protocols. Compliance with FAA Part 25.1419 and EASA CS-25.1419 is mandatory. Maintenance includes regular inspection and system replacement. Emergency procedures address ice accumulation and system failures. Operator training covers system operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "De-icing effectiveness",
            "Anti-icing reliability",
            "Certified systems",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA Part 25.1419",
            "EASA CS-25.1419",
            "Ice Protection Manufacturer Guidelines"
        ],
        burden_holder="Safety Engineer",
        adversary_position="Ice protection is unnecessary; freight operations rarely encounter icing.",
        counter_arguments=[
            "Certified systems add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Effective de-icing, certified systems, and scheduled maintenance.",
        entity_scope="RAIL04 ice protection systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.1419 Ice Protection Systems"
    ),
    DoctrineBlock(
        topic="flight_management_system",
        keywords=["flight management", "navigation", "automation", "data integration", "safety"],
        conclusion_template="Flight management systems must provide reliable navigation, automation, and data integration for freight operations, ensuring safety and compliance.",
        reasoning_framework="""
        Flight management doctrine mandates reliable navigation, automation, and data integration. Freight locomotives must use certified FMS units and adhere to operational protocols. Compliance with FAA AC 20-130A and EASA AMC 20-13 is required. Maintenance includes regular inspection and unit replacement. Emergency procedures address navigation failures and system outages. Operator training covers FMS operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Navigation reliability",
            "Automation",
            "Data integration",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA AC 20-130A",
            "EASA AMC 20-13",
            "FMS Manufacturer Guidelines"
        ],
        burden_holder="Avionics Engineer",
        adversary_position="Automation is unnecessary; manual navigation suffices.",
        counter_arguments=[
            "Certified units add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Reliable navigation, certified units, and scheduled maintenance.",
        entity_scope="RAIL04 flight management systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-130A Flight Management Systems"
    ),
    DoctrineBlock(
        topic="TCAS_traffic_alert",
        keywords=["TCAS", "traffic alert", "collision avoidance", "safety", "automation"],
        conclusion_template="TCAS systems must provide reliable traffic alert and collision avoidance, automation, and compliance for freight operations, with scheduled maintenance.",
        reasoning_framework="""
        TCAS doctrine mandates reliable traffic alert, collision avoidance, and automation. Freight locomotives must use certified TCAS units and adhere to operational protocols. Compliance with FAA AC 20-131 and EASA AMC 20-15 is required. Maintenance includes regular inspection and unit replacement. Emergency procedures address collision threats and system failures. Operator training covers TCAS operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Traffic alert reliability",
            "Collision avoidance",
            "Automation",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA AC 20-131",
            "EASA AMC 20-15",
            "TCAS Manufacturer Guidelines"
        ],
        burden_holder="Safety Engineer",
        adversary_position="Collision avoidance is unnecessary; manual observation suffices.",
        counter_arguments=[
            "Certified units add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Reliable traffic alert, certified units, and scheduled maintenance.",
        entity_scope="RAIL04 TCAS systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-131 TCAS Systems"
    ),
    DoctrineBlock(
        topic="EGPWS_terrain_awareness",
        keywords=["EGPWS", "terrain awareness", "safety", "automation", "data integration"],
        conclusion_template="EGPWS systems must provide reliable terrain awareness, automation, and data integration for freight operations, ensuring safety and compliance.",
        reasoning_framework="""
        EGPWS doctrine mandates reliable terrain awareness, automation, and data integration. Freight locomotives must use certified EGPWS units and adhere to operational protocols. Compliance with FAA AC 20-153 and EASA AMC 20-15 is required. Maintenance includes regular inspection and unit replacement. Emergency procedures address terrain threats and system failures. Operator training covers EGPWS operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Terrain awareness reliability",
            "Automation",
            "Data integration",
            "Maintenance",
            "Safety compliance"
        ],
        primary_authority=[
            "FAA AC 20-153",
            "EASA AMC 20-15",
            "EGPWS Manufacturer Guidelines"
        ],
        burden_holder="Safety Engineer",
        adversary_position="Terrain awareness is unnecessary; manual observation suffices.",
        counter_arguments=[
            "Certified units add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Reliable terrain awareness, certified units, and scheduled maintenance.",
        entity_scope="RAIL04 EGPWS systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-153 EGPWS Systems"
    ),
    DoctrineBlock(
        topic="autopilot_autothrottle",
        keywords=["autopilot", "autothrottle", "automation", "safety", "navigation"],
        conclusion_template="Autopilot and autothrottle systems must provide reliable automation, navigation, and safety for freight operations, with scheduled maintenance.",
        reasoning_framework="""
        Autopilot and autothrottle doctrine mandates reliable automation, navigation, and safety. Freight locomotives must use certified autopilot and autothrottle units and adhere to operational protocols. Compliance with FAA AC 20-117 and EASA AMC 20-15 is required. Maintenance includes regular inspection and unit replacement. Emergency procedures address automation failures and system outages. Operator training covers autopilot and autothrottle operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Automation reliability",
            "Navigation",
            "Safety",
            "Maintenance",
            "Certified units"
        ],
        primary_authority=[
            "FAA AC 20-117",
            "EASA AMC 20-15",
            "Autopilot Manufacturer Guidelines"
        ],
        burden_holder="Avionics Engineer",
        adversary_position="Automation is unnecessary; manual control suffices.",
        counter_arguments=[
            "Certified units add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Reliable automation, certified units, and scheduled maintenance.",
        entity_scope="RAIL04 autopilot and autothrottle systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-117 Autopilot Systems"
    ),
    DoctrineBlock(
        topic="MSG3_maintenance_program",
        keywords=["MSG-3", "maintenance", "program", "safety", "compliance"],
        conclusion_template="MSG-3 maintenance programs must ensure safety, compliance, and scheduled maintenance for freight operations, with real-time monitoring.",
        reasoning_framework="""
        MSG-3 maintenance doctrine mandates scheduled maintenance, safety, and compliance. Freight locomotives must use certified MSG-3 maintenance programs and adhere to operational protocols. Compliance with FAA AC 121-22A and EASA AMC 20-20 is required. Maintenance includes regular inspection and program updates. Emergency procedures address maintenance failures and system outages. Operator training covers MSG-3 program operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Scheduled maintenance",
            "Safety",
            "Compliance",
            "Certified programs",
            "Real-time monitoring"
        ],
        primary_authority=[
            "FAA AC 121-22A",
            "EASA AMC 20-20",
            "MSG-3 Manufacturer Guidelines"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Scheduled maintenance is unnecessary; reactive maintenance suffices.",
        counter_arguments=[
            "Certified programs add cost.",
            "Real-time monitoring is redundant."
        ],
        resolution_strategy="Scheduled maintenance, certified programs, and real-time monitoring.",
        entity_scope="RAIL04 MSG-3 maintenance programs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA AC 121-22A MSG-3 Maintenance"
    ),
    DoctrineBlock(
        topic="airworthiness_directives",
        keywords=["airworthiness", "directives", "compliance", "safety", "regulation"],
        conclusion_template="Airworthiness directives must be complied with promptly, ensuring safety and regulatory adherence for freight operations.",
        reasoning_framework="""
        Airworthiness directive doctrine mandates prompt compliance, safety, and regulatory adherence. Freight locomotives must follow FAA and EASA airworthiness directives and update operational protocols accordingly. Compliance with FAA Part 39 and EASA Part M is required. Maintenance includes regular inspection and directive implementation. Emergency procedures address directive failures and system outages. Operator training covers airworthiness directive compliance and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Prompt compliance",
            "Safety",
            "Regulatory adherence",
            "Directive implementation",
            "Maintenance"
        ],
        primary_authority=[
            "FAA Part 39",
            "EASA Part M",
            "Airworthiness Directive Manufacturer Guidelines"
        ],
        burden_holder="Compliance Engineer",
        adversary_position="Directives can be delayed; operational needs take precedence.",
        counter_arguments=[
            "Prompt compliance adds cost.",
            "Directive implementation is redundant."
        ],
        resolution_strategy="Prompt compliance, directive implementation, and scheduled maintenance.",
        entity_scope="RAIL04 airworthiness directives",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA Part 39 Airworthiness Directives"
    ),
    DoctrineBlock(
        topic="Part_25_certification",
        keywords=["Part 25", "certification", "compliance", "safety", "regulation"],
        conclusion_template="Part 25 certification must be obtained and maintained, ensuring compliance and safety for freight operations.",
        reasoning_framework="""
        Part 25 certification doctrine mandates obtaining and maintaining certification, compliance, and safety. Freight locomotives must adhere to FAA Part 25 and EASA CS-25 certification requirements. Maintenance includes regular inspection and certification updates. Emergency procedures address certification failures and system outages. Operator training covers certification compliance and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Certification",
            "Compliance",
            "Safety",
            "Regulation",
            "Maintenance"
        ],
        primary_authority=[
            "FAA Part 25",
            "EASA CS-25",
            "Certification Manufacturer Guidelines"
        ],
        burden_holder="Certification Engineer",
        adversary_position="Certification can be delayed; operational needs take precedence.",
        counter_arguments=[
            "Certification adds cost.",
            "Compliance is redundant."
        ],
        resolution_strategy="Obtain and maintain certification, compliance, and scheduled maintenance.",
        entity_scope="RAIL04 certification",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA Part 25 Certification"
    ),
    DoctrineBlock(
        topic="weight_and_balance",
        keywords=["weight", "balance", "load", "compliance", "safety"],
        conclusion_template="Weight and balance must be maintained within prescribed limits, ensuring compliance and safety for freight operations.",
        reasoning_framework="""
        Weight and balance doctrine mandates maintaining prescribed limits, compliance, and safety. Freight locomotives must use certified weight and balance systems and adhere to operational protocols. Compliance with FAA Part 25.23 and EASA CS-25.23 is required. Maintenance includes regular inspection and system updates. Emergency procedures address weight and balance failures and system outages. Operator training covers weight and balance operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Prescribed limits",
            "Compliance",
            "Safety",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FAA Part 25.23",
            "EASA CS-25.23",
            "Weight and Balance Manufacturer Guidelines"
        ],
        burden_holder="Load Engineer",
        adversary_position="Prescribed limits can be exceeded; operational needs take precedence.",
        counter_arguments=[
            "Certified systems add cost.",
            "Compliance is redundant."
        ],
        resolution_strategy="Maintain prescribed limits, certified systems, and scheduled maintenance.",
        entity_scope="RAIL04 weight and balance",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.23 Weight and Balance"
    ),
    DoctrineBlock(
        topic="freight_load_distribution",
        keywords=["freight", "load", "distribution", "balance", "safety"],
        conclusion_template="Freight load distribution must ensure balanced weight, structural integrity, and compliance with operational safety standards.",
        reasoning_framework="""
        Load distribution doctrine requires careful planning of freight placement to maintain structural integrity and balance. Overloading or uneven distribution can compromise locomotive stability and violate regulatory limits. Real-time weight sensors and digital load maps are used to verify compliance. Maintenance includes periodic inspection of load sensors and structural elements. Emergency procedures address load shifts and structural failures. Operator training covers load planning and emergency response.
        """,
        key_factors=[
            "Balanced weight",
            "Structural integrity",
            "Compliance",
            "Sensor reliability",
            "Maintenance"
        ],
        primary_authority=[
            "FAA Part 25.23",
            "EASA CS-25.23",
            "Load Distribution Manufacturer Guidelines"
        ],
        burden_holder="Load Engineer",
        adversary_position="Uneven distribution is acceptable for operational flexibility.",
        counter_arguments=[
            "Sensor reliability is overstated.",
            "Structural integrity is rarely compromised."
        ],
        resolution_strategy="Balanced load planning, sensor monitoring, and scheduled maintenance.",
        entity_scope="RAIL04 freight load distribution",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA Part 25.23 Load Distribution"
    ),
    DoctrineBlock(
        topic="freight_operation_scheduling",
        keywords=["freight", "operation", "scheduling", "efficiency", "compliance"],
        conclusion_template="Freight operation scheduling must optimize efficiency, comply with regulatory limits, and ensure safety in locomotive operations.",
        reasoning_framework="""
        Operation scheduling doctrine emphasizes efficiency, regulatory compliance, and safety. Freight locomotives must adhere to scheduled maintenance and operational intervals. Real-time scheduling software integrates load, route, and maintenance data. Compliance with FRA and EASA operational standards is required. Emergency procedures address schedule disruptions and operational failures. Operator training covers scheduling software and emergency response.
        """,
        key_factors=[
            "Efficiency",
            "Compliance",
            "Safety",
            "Scheduling software",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Operational Standards",
            "EASA Operational Standards",
            "Scheduling Software Manufacturer Guidelines"
        ],
        burden_holder="Operations Manager",
        adversary_position="Efficiency can override compliance for operational needs.",
        counter_arguments=[
            "Scheduling software is unnecessary.",
            "Compliance adds complexity."
        ],
        resolution_strategy="Optimize efficiency, comply with standards, and use scheduling software.",
        entity_scope="RAIL04 freight operations",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Operational Standards"
    ),
    DoctrineBlock(
        topic="locomotive_brake_system",
        keywords=["locomotive", "brake", "system", "safety", "maintenance"],
        conclusion_template="Locomotive brake systems must ensure reliable stopping power, safety, and compliance with maintenance and operational standards.",
        reasoning_framework="""
        Brake system doctrine mandates reliable stopping power, safety, and regular maintenance. Freight locomotives must use certified brake systems and adhere to operational protocols. Compliance with FRA brake standards and EASA CS-25.735 is required. Maintenance includes regular inspection and brake replacement. Emergency procedures address brake failures and system outages. Operator training covers brake operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Stopping power",
            "Safety",
            "Certified systems",
            "Maintenance",
            "Compliance"
        ],
        primary_authority=[
            "FRA Brake Standards",
            "EASA CS-25.735",
            "Brake Manufacturer Guidelines"
        ],
        burden_holder="Brake Engineer",
        adversary_position="Certified systems are unnecessary; traditional brakes suffice.",
        counter_arguments=[
            "Maintenance intervals can be extended.",
            "Compliance adds cost."
        ],
        resolution_strategy="Reliable stopping power, certified systems, and scheduled maintenance.",
        entity_scope="RAIL04 locomotive brake systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Brake Standards"
    ),
    DoctrineBlock(
        topic="locomotive_signal_system",
        keywords=["locomotive", "signal", "system", "safety", "automation"],
        conclusion_template="Locomotive signal systems must ensure reliable communication, automation, and compliance with safety standards for freight operations.",
        reasoning_framework="""
        Signal system doctrine mandates reliable communication, automation, and safety. Freight locomotives must use certified signal systems and adhere to operational protocols. Compliance with FRA signal standards and EASA CS-25.1309 is required. Maintenance includes regular inspection and system replacement. Emergency procedures address signal failures and communication outages. Operator training covers signal system operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Communication reliability",
            "Automation",
            "Safety",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Signal Standards",
            "EASA CS-25.1309",
            "Signal Manufacturer Guidelines"
        ],
        burden_holder="Signal Engineer",
        adversary_position="Automation is unnecessary; manual communication suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Reliable communication, certified systems, and scheduled maintenance.",
        entity_scope="RAIL04 locomotive signal systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Signal Standards"
    ),
    DoctrineBlock(
        topic="locomotive_safety_management",
        keywords=["locomotive", "safety", "management", "compliance", "training"],
        conclusion_template="Safety management must ensure compliance, training, and scheduled maintenance for freight operations, with real-time monitoring.",
        reasoning_framework="""
        Safety management doctrine mandates compliance, training, and scheduled maintenance. Freight locomotives must use certified safety management systems and adhere to operational protocols. Compliance with FRA safety standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address safety failures and system outages. Operator training covers safety management operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Compliance",
            "Training",
            "Certified systems",
            "Maintenance",
            "Real-time monitoring"
        ],
        primary_authority=[
            "FRA Safety Standards",
            "EASA AMC 20-20",
            "Safety Management Manufacturer Guidelines"
        ],
        burden_holder="Safety Manager",
        adversary_position="Training is unnecessary; compliance suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Real-time monitoring is redundant."
        ],
        resolution_strategy="Compliance, training, certified systems, and real-time monitoring.",
        entity_scope="RAIL04 safety management",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FRA Safety Standards"
    ),
    DoctrineBlock(
        topic="locomotive_communication_system",
        keywords=["locomotive", "communication", "system", "safety", "automation"],
        conclusion_template="Communication systems must ensure reliable data exchange, automation, and compliance with safety standards for freight operations.",
        reasoning_framework="""
        Communication system doctrine mandates reliable data exchange, automation, and safety. Freight locomotives must use certified communication systems and adhere to operational protocols. Compliance with FRA communication standards and EASA CS-25.1309 is required. Maintenance includes regular inspection and system replacement. Emergency procedures address communication failures and data outages. Operator training covers communication system operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Data exchange reliability",
            "Automation",
            "Safety",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Communication Standards",
            "EASA CS-25.1309",
            "Communication Manufacturer Guidelines"
        ],
        burden_holder="Communication Engineer",
        adversary_position="Automation is unnecessary; manual communication suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Maintenance intervals can be extended."
        ],
        resolution_strategy="Reliable data exchange, certified systems, and scheduled maintenance.",
        entity_scope="RAIL04 communication systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FRA Communication Standards"
    ),
    DoctrineBlock(
        topic="locomotive_power_management",
        keywords=["locomotive", "power", "management", "efficiency", "safety"],
        conclusion_template="Power management must optimize efficiency, ensure safety, and comply with operational standards for freight locomotives.",
        reasoning_framework="""
        Power management doctrine emphasizes efficiency, safety, and compliance. Freight locomotives must use certified power management systems and adhere to operational protocols. Compliance with FRA power standards and EASA CS-25.1351 is required. Maintenance includes regular inspection and system updates. Emergency procedures address power failures and system outages. Operator training covers power management operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Efficiency",
            "Safety",
            "Certified systems",
            "Compliance",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Power Standards",
            "EASA CS-25.1351",
            "Power Management Manufacturer Guidelines"
        ],
        burden_holder="Power Engineer",
        adversary_position="Efficiency is secondary; safety suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Compliance is redundant."
        ],
        resolution_strategy="Optimize efficiency, ensure safety, and comply with standards.",
        entity_scope="RAIL04 power management",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Power Standards"
    ),
    DoctrineBlock(
        topic="locomotive_emergency_response",
        keywords=["locomotive", "emergency", "response", "training", "safety"],
        conclusion_template="Emergency response must ensure rapid action, training, and compliance with safety standards for freight operations.",
        reasoning_framework="""
        Emergency response doctrine mandates rapid action, training, and compliance. Freight locomotives must use certified emergency response systems and adhere to operational protocols. Compliance with FRA emergency standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address response failures and system outages. Operator training covers emergency response operation and emergency procedures. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Rapid action",
            "Training",
            "Certified systems",
            "Compliance",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Emergency Standards",
            "EASA AMC 20-20",
            "Emergency Response Manufacturer Guidelines"
        ],
        burden_holder="Emergency Manager",
        adversary_position="Training is unnecessary; compliance suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Rapid action is overstated."
        ],
        resolution_strategy="Rapid action, training, certified systems, and compliance.",
        entity_scope="RAIL04 emergency response",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Emergency Standards"
    ),
    DoctrineBlock(
        topic="locomotive_freight_tracking",
        keywords=["locomotive", "freight", "tracking", "automation", "compliance"],
        conclusion_template="Freight tracking must ensure real-time data, automation, and compliance with operational standards for freight locomotives.",
        reasoning_framework="""
        Freight tracking doctrine mandates real-time data, automation, and compliance. Freight locomotives must use certified tracking systems and adhere to operational protocols. Compliance with FRA tracking standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address tracking failures and data outages. Operator training covers tracking system operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Real-time data",
            "Automation",
            "Compliance",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Tracking Standards",
            "EASA AMC 20-20",
            "Tracking Manufacturer Guidelines"
        ],
        burden_holder="Tracking Engineer",
        adversary_position="Automation is unnecessary; manual tracking suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Real-time data is redundant."
        ],
        resolution_strategy="Real-time data, automation, certified systems, and compliance.",
        entity_scope="RAIL04 freight tracking",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Tracking Standards"
    ),
    DoctrineBlock(
        topic="locomotive_crew_management",
        keywords=["locomotive", "crew", "management", "training", "compliance"],
        conclusion_template="Crew management must ensure training, compliance, and scheduled maintenance for freight operations, with real-time monitoring.",
        reasoning_framework="""
        Crew management doctrine mandates training, compliance, and scheduled maintenance. Freight locomotives must use certified crew management systems and adhere to operational protocols. Compliance with FRA crew standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address crew failures and system outages. Operator training covers crew management operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Training",
            "Compliance",
            "Certified systems",
            "Maintenance",
            "Real-time monitoring"
        ],
        primary_authority=[
            "FRA Crew Standards",
            "EASA AMC 20-20",
            "Crew Management Manufacturer Guidelines"
        ],
        burden_holder="Crew Manager",
        adversary_position="Training is unnecessary; compliance suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Real-time monitoring is redundant."
        ],
        resolution_strategy="Training, compliance, certified systems, and real-time monitoring.",
        entity_scope="RAIL04 crew management",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Crew Standards"
    ),
    DoctrineBlock(
        topic="locomotive_route_management",
        keywords=["locomotive", "route", "management", "navigation", "compliance"],
        conclusion_template="Route management must ensure optimal navigation, compliance, and safety for freight operations, with scheduled maintenance.",
        reasoning_framework="""
        Route management doctrine mandates optimal navigation, compliance, and safety. Freight locomotives must use certified route management systems and adhere to operational protocols. Compliance with FRA route standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address route failures and navigation outages. Operator training covers route management operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Optimal navigation",
            "Compliance",
            "Safety",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Route Standards",
            "EASA AMC 20-20",
            "Route Management Manufacturer Guidelines"
        ],
        burden_holder="Route Manager",
        adversary_position="Optimal navigation is unnecessary; manual routing suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Compliance is redundant."
        ],
        resolution_strategy="Optimal navigation, compliance, certified systems, and scheduled maintenance.",
        entity_scope="RAIL04 route management",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Route Standards"
    ),
    DoctrineBlock(
        topic="locomotive_data_logging",
        keywords=["locomotive", "data", "logging", "compliance", "automation"],
        conclusion_template="Data logging must ensure reliable recording, automation, and compliance with operational standards for freight locomotives.",
        reasoning_framework="""
        Data logging doctrine mandates reliable recording, automation, and compliance. Freight locomotives must use certified data logging systems and adhere to operational protocols. Compliance with FRA data standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address logging failures and data outages. Operator training covers data logging operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Reliable recording",
            "Automation",
            "Compliance",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Data Standards",
            "EASA AMC 20-20",
            "Data Logging Manufacturer Guidelines"
        ],
        burden_holder="Data Engineer",
        adversary_position="Automation is unnecessary; manual logging suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Reliable recording is overstated."
        ],
        resolution_strategy="Reliable recording, automation, certified systems, and compliance.",
        entity_scope="RAIL04 data logging",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FRA Data Standards"
    ),
    DoctrineBlock(
        topic="locomotive_sensor_management",
        keywords=["locomotive", "sensor", "management", "automation", "compliance"],
        conclusion_template="Sensor management must ensure reliable data, automation, and compliance with operational standards for freight locomotives.",
        reasoning_framework="""
        Sensor management doctrine mandates reliable data, automation, and compliance. Freight locomotives must use certified sensor management systems and adhere to operational protocols. Compliance with FRA sensor standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address sensor failures and data outages. Operator training covers sensor management operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Reliable data",
            "Automation",
            "Compliance",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Sensor Standards",
            "EASA AMC 20-20",
            "Sensor Management Manufacturer Guidelines"
        ],
        burden_holder="Sensor Engineer",
        adversary_position="Automation is unnecessary; manual sensor management suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Reliable data is overstated."
        ],
        resolution_strategy="Reliable data, automation, certified systems, and compliance.",
        entity_scope="RAIL04 sensor management",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Sensor Standards"
    ),
    DoctrineBlock(
        topic="locomotive_maintenance_logging",
        keywords=["locomotive", "maintenance", "logging", "compliance", "automation"],
        conclusion_template="Maintenance logging must ensure reliable recording, automation, and compliance with operational standards for freight locomotives.",
        reasoning_framework="""
        Maintenance logging doctrine mandates reliable recording, automation, and compliance. Freight locomotives must use certified maintenance logging systems and adhere to operational protocols. Compliance with FRA maintenance standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address logging failures and data outages. Operator training covers maintenance logging operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Reliable recording",
            "Automation",
            "Compliance",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Maintenance Standards",
            "EASA AMC 20-20",
            "Maintenance Logging Manufacturer Guidelines"
        ],
        burden_holder="Maintenance Engineer",
        adversary_position="Automation is unnecessary; manual logging suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Reliable recording is overstated."
        ],
        resolution_strategy="Reliable recording, automation, certified systems, and compliance.",
        entity_scope="RAIL04 maintenance logging",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Maintenance Standards"
    ),
    DoctrineBlock(
        topic="locomotive_energy_efficiency",
        keywords=["locomotive", "energy", "efficiency", "compliance", "automation"],
        conclusion_template="Energy efficiency must be optimized, ensuring compliance and automation for freight operations, with scheduled maintenance.",
        reasoning_framework="""
        Energy efficiency doctrine mandates optimization, compliance, and automation. Freight locomotives must use certified energy efficiency systems and adhere to operational protocols. Compliance with FRA energy standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address efficiency failures and system outages. Operator training covers energy efficiency operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Optimization",
            "Compliance",
            "Automation",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Energy Standards",
            "EASA AMC 20-20",
            "Energy Efficiency Manufacturer Guidelines"
        ],
        burden_holder="Energy Engineer",
        adversary_position="Optimization is unnecessary; compliance suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Automation is redundant."
        ],
        resolution_strategy="Optimize energy efficiency, comply with standards, and automate systems.",
        entity_scope="RAIL04 energy efficiency",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Energy Standards"
    ),
    DoctrineBlock(
        topic="locomotive_environmental_compliance",
        keywords=["locomotive", "environmental", "compliance", "regulation", "safety"],
        conclusion_template="Environmental compliance must be ensured, adhering to regulatory standards and safety for freight operations.",
        reasoning_framework="""
        Environmental compliance doctrine mandates adherence to regulatory standards and safety. Freight locomotives must use certified environmental compliance systems and adhere to operational protocols. Compliance with FRA environmental standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address compliance failures and environmental hazards. Operator training covers environmental compliance operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Regulatory standards",
            "Safety",
            "Certified systems",
            "Compliance",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Environmental Standards",
            "EASA AMC 20-20",
            "Environmental Compliance Manufacturer Guidelines"
        ],
        burden_holder="Environmental Engineer",
        adversary_position="Regulatory standards can be delayed; operational needs take precedence.",
        counter_arguments=[
            "Certified systems add cost.",
            "Compliance is redundant."
        ],
        resolution_strategy="Ensure environmental compliance, adhere to standards, and scheduled maintenance.",
        entity_scope="RAIL04 environmental compliance",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Environmental Standards"
    ),
    DoctrineBlock(
        topic="locomotive_infrastructure_interface",
        keywords=["locomotive", "infrastructure", "interface", "compliance", "safety"],
        conclusion_template="Infrastructure interface must ensure compliance, safety, and scheduled maintenance for freight operations, with real-time monitoring.",
        reasoning_framework="""
        Infrastructure interface doctrine mandates compliance, safety, and scheduled maintenance. Freight locomotives must use certified infrastructure interface systems and adhere to operational protocols. Compliance with FRA infrastructure standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address interface failures and system outages. Operator training covers infrastructure interface operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Compliance",
            "Safety",
            "Certified systems",
            "Maintenance",
            "Real-time monitoring"
        ],
        primary_authority=[
            "FRA Infrastructure Standards",
            "EASA AMC 20-20",
            "Infrastructure Interface Manufacturer Guidelines"
        ],
        burden_holder="Infrastructure Engineer",
        adversary_position="Compliance is unnecessary; operational needs take precedence.",
        counter_arguments=[
            "Certified systems add cost.",
            "Real-time monitoring is redundant."
        ],
        resolution_strategy="Compliance, safety, certified systems, and real-time monitoring.",
        entity_scope="RAIL04 infrastructure interface",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Infrastructure Standards"
    ),
    DoctrineBlock(
        topic="locomotive_asset_management",
        keywords=["locomotive", "asset", "management", "compliance", "automation"],
        conclusion_template="Asset management must ensure compliance, automation, and scheduled maintenance for freight operations, with real-time monitoring.",
        reasoning_framework="""
        Asset management doctrine mandates compliance, automation, and scheduled maintenance. Freight locomotives must use certified asset management systems and adhere to operational protocols. Compliance with FRA asset standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address asset failures and system outages. Operator training covers asset management operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Compliance",
            "Automation",
            "Certified systems",
            "Maintenance",
            "Real-time monitoring"
        ],
        primary_authority=[
            "FRA Asset Standards",
            "EASA AMC 20-20",
            "Asset Management Manufacturer Guidelines"
        ],
        burden_holder="Asset Manager",
        adversary_position="Automation is unnecessary; manual asset management suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Real-time monitoring is redundant."
        ],
        resolution_strategy="Compliance, automation, certified systems, and real-time monitoring.",
        entity_scope="RAIL04 asset management",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Asset Standards"
    ),
    DoctrineBlock(
        topic="locomotive_risk_management",
        keywords=["locomotive", "risk", "management", "compliance", "safety"],
        conclusion_template="Risk management must ensure compliance, safety, and scheduled maintenance for freight operations, with real-time monitoring.",
        reasoning_framework="""
        Risk management doctrine mandates compliance, safety, and scheduled maintenance. Freight locomotives must use certified risk management systems and adhere to operational protocols. Compliance with FRA risk standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address risk failures and system outages. Operator training covers risk management operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Compliance",
            "Safety",
            "Certified systems",
            "Maintenance",
            "Real-time monitoring"
        ],
        primary_authority=[
            "FRA Risk Standards",
            "EASA AMC 20-20",
            "Risk Management Manufacturer Guidelines"
        ],
        burden_holder="Risk Manager",
        adversary_position="Compliance is unnecessary; operational needs take precedence.",
        counter_arguments=[
            "Certified systems add cost.",
            "Real-time monitoring is redundant."
        ],
        resolution_strategy="Compliance, safety, certified systems, and real-time monitoring.",
        entity_scope="RAIL04 risk management",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FRA Risk Standards"
    ),
    DoctrineBlock(
        topic="locomotive_performance_monitoring",
        keywords=["locomotive", "performance", "monitoring", "automation", "compliance"],
        conclusion_template="Performance monitoring must ensure reliable data, automation, and compliance with operational standards for freight locomotives.",
        reasoning_framework="""
        Performance monitoring doctrine mandates reliable data, automation, and compliance. Freight locomotives must use certified performance monitoring systems and adhere to operational protocols. Compliance with FRA performance standards and EASA AMC 20-20 is required. Maintenance includes regular inspection and system updates. Emergency procedures address monitoring failures and data outages. Operator training covers performance monitoring operation and emergency response. System health is monitored via sensors, and deviations trigger maintenance actions.
        """,
        key_factors=[
            "Reliable data",
            "Automation",
            "Compliance",
            "Certified systems",
            "Maintenance"
        ],
        primary_authority=[
            "FRA Performance Standards",
            "EASA AMC 20-20",
            "Performance Monitoring Manufacturer Guidelines"
        ],
        burden_holder="Performance Engineer",
        adversary_position="Automation is unnecessary; manual monitoring suffices.",
        counter_arguments=[
            "Certified systems add cost.",
            "Reliable data is overstated."
        ],
        resolution_strategy="Reliable data, automation, certified systems, and compliance.",
        entity_scope="RAIL04 performance monitoring",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FRA Performance Standards"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic == topic:
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    results = []
    keyword_lower = keyword.lower()
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]