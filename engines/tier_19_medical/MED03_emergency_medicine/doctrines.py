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
        keywords=["turbofan", "engine", "operation", "thrust", "fuel efficiency", "maintenance"],
        conclusion_template="Turbofan engine operation must ensure optimal thrust generation, fuel efficiency, and compliance with airworthiness standards.",
        reasoning_framework="""
        Turbofan engines are the primary propulsion units for modern commercial aircraft. Their operation involves careful management of airflow, fuel injection, and combustion to maximize thrust while minimizing fuel consumption and emissions. Key operational parameters include N1/N2 speeds, EGT, and fuel flow. Maintenance schedules must adhere to MSG-3 guidelines, and any deviations in performance require immediate troubleshooting. Regulatory oversight from FAA/EASA mandates compliance with Part 25 certification standards, and operators must ensure engines are maintained per manufacturer recommendations. Reliability and safety are paramount, with regular borescope inspections and trend monitoring. Engine health monitoring systems provide real-time diagnostics, enabling predictive maintenance and reducing unscheduled removals. The doctrine emphasizes proactive risk management and adherence to controlling precedents in engine operation and maintenance.
        """,
        key_factors=[
            "Thrust output",
            "Fuel efficiency",
            "Emission standards",
            "Maintenance intervals",
            "Regulatory compliance",
            "Engine health monitoring"
        ],
        primary_authority=[
            "FAA Part 25",
            "EASA CS-25",
            "Engine manufacturer manuals",
            "MSG-3 maintenance guidelines"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Engine operation can be compromised by inadequate maintenance or non-compliance with regulatory standards.",
        counter_arguments=[
            "Modern turbofan engines are equipped with advanced health monitoring systems.",
            "Strict regulatory oversight ensures compliance.",
            "Manufacturer support mitigates operational risks."
        ],
        resolution_strategy="Implement robust maintenance programs, utilize predictive diagnostics, and ensure regulatory compliance.",
        entity_scope="Commercial aircraft propulsion systems",
        confidence=0.98,
        confidence_zone="High",
        controlling_precedent="FAA AC 33.70-1, EASA AMC 20-23"
    ),
    DoctrineBlock(
        topic="fly_by_wire_flight_controls",
        keywords=["fly-by-wire", "flight controls", "electronic", "redundancy", "safety"],
        conclusion_template="Fly-by-wire flight control systems must provide reliable, redundant, and precise control of aircraft surfaces, ensuring safety and compliance.",
        reasoning_framework="""
        Fly-by-wire (FBW) systems replace mechanical linkages with electronic signals, offering improved reliability, weight reduction, and flight envelope protection. The doctrine requires multiple redundant channels to mitigate single-point failures, and software must be certified to DO-178C Level A standards. FBW systems integrate with autopilot and flight management systems, enabling advanced control laws and protections against pilot-induced errors. Maintenance protocols include regular software updates, hardware inspections, and system self-tests. Regulatory authorities mandate rigorous testing and certification, with failure mode and effects analysis (FMEA) guiding design and operational procedures. Operators must ensure crew training on FBW nuances, and any anomalies must be reported under mandatory occurrence reporting frameworks.
        """,
        key_factors=[
            "Redundancy",
            "Software certification",
            "Hardware integrity",
            "Flight envelope protection",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.671",
            "EASA CS-25.671",
            "RTCA DO-178C",
            "Aircraft manufacturer documentation"
        ],
        burden_holder="Aircraft Manufacturer/Operator",
        adversary_position="Electronic flight controls may be susceptible to software bugs or hardware failures.",
        counter_arguments=[
            "Redundant architectures mitigate risks.",
            "Rigorous certification standards ensure reliability.",
            "Continuous crew training addresses operational challenges."
        ],
        resolution_strategy="Adopt multi-channel redundancy, maintain software certification, and enforce comprehensive crew training.",
        entity_scope="Aircraft flight control systems",
        confidence=0.97,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1309-1A, EASA AMC 25.1309"
    ),
    DoctrineBlock(
        topic="glass_cockpit_avionics",
        keywords=["glass cockpit", "avionics", "display", "integration", "situational awareness"],
        conclusion_template="Glass cockpit avionics must deliver integrated, reliable, and intuitive information to enhance situational awareness and flight safety.",
        reasoning_framework="""
        Glass cockpit avionics consolidate flight, navigation, and engine data into digital displays, replacing analog instruments. The doctrine emphasizes integration of primary flight displays (PFD), multi-function displays (MFD), and engine indication and crew alerting systems (EICAS). Avionics must comply with DO-178C and DO-254 standards, ensuring software and hardware reliability. Crew interface design prioritizes clarity, minimal workload, and rapid access to critical information. Regular software updates and hardware checks are mandated, with built-in test equipment (BITE) facilitating diagnostics. Regulatory bodies require thorough certification and operational testing, and operators must ensure crew proficiency in glass cockpit operations. System redundancy and failover mechanisms are essential for safety.
        """,
        key_factors=[
            "Display integration",
            "Software/hardware reliability",
            "Crew interface",
            "Redundancy",
            "Certification"
        ],
        primary_authority=[
            "FAA Part 25.1302",
            "EASA CS-25.1302",
            "RTCA DO-178C",
            "RTCA DO-254"
        ],
        burden_holder="Avionics Manufacturer/Operator",
        adversary_position="Digital displays may fail or mislead pilots due to software/hardware errors.",
        counter_arguments=[
            "Redundant systems ensure continued operation.",
            "Rigorous certification and testing mitigate risks.",
            "Crew training addresses interface challenges."
        ],
        resolution_strategy="Maintain software/hardware certification, implement redundancy, and enforce crew training.",
        entity_scope="Aircraft avionics systems",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-173, EASA AMC 20-115"
    ),
    DoctrineBlock(
        topic="aircraft_electrical_system",
        keywords=["electrical", "power distribution", "generator", "bus", "failure management"],
        conclusion_template="Aircraft electrical systems must provide reliable power distribution, redundancy, and failure management to ensure operational safety.",
        reasoning_framework="""
        Aircraft electrical systems distribute power from generators, batteries, and auxiliary power units (APU) to critical and non-critical loads. The doctrine mandates multiple power sources and bus architectures to ensure redundancy and continuity of supply. Failure management protocols include automatic load shedding, bus isolation, and emergency power switching. Maintenance involves regular checks of generators, batteries, wiring, and circuit protection devices. Regulatory standards require compliance with Part 25.1351 and associated guidance. Operators must ensure crew proficiency in electrical failure procedures and maintain up-to-date system diagrams and troubleshooting guides. System upgrades must be certified and documented.
        """,
        key_factors=[
            "Power source redundancy",
            "Bus architecture",
            "Failure management",
            "Maintenance protocols",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1351",
            "EASA CS-25.1351",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Electrical failures can lead to loss of critical systems and flight safety risks.",
        counter_arguments=[
            "Redundant power sources mitigate risks.",
            "Automatic failure management protocols ensure continuity.",
            "Regular maintenance reduces failure likelihood."
        ],
        resolution_strategy="Implement robust redundancy, maintain failure management protocols, and enforce crew training.",
        entity_scope="Aircraft electrical systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1351-1"
    ),
    DoctrineBlock(
        topic="hydraulic_flight_control_system",
        keywords=["hydraulic", "flight control", "pressure", "actuator", "failure modes"],
        conclusion_template="Hydraulic flight control systems must ensure reliable actuation, redundancy, and effective failure management.",
        reasoning_framework="""
        Hydraulic systems power flight control actuators, landing gear, brakes, and other critical functions. The doctrine requires multiple independent hydraulic circuits to prevent loss of control from single-point failures. Pressure monitoring, leak detection, and accumulator maintenance are essential. Regulatory standards mandate compliance with Part 25.1435, and operators must adhere to manufacturer maintenance schedules. Crew must be trained in hydraulic failure procedures, including manual reversion and alternate systems. System upgrades and repairs must be certified, and all hydraulic fluid types and compatibility must be documented.
        """,
        key_factors=[
            "Circuit redundancy",
            "Pressure monitoring",
            "Leak detection",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1435",
            "EASA CS-25.1435",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Hydraulic failures may result in loss of flight control or landing gear operation.",
        counter_arguments=[
            "Multiple hydraulic circuits provide redundancy.",
            "Regular maintenance and monitoring reduce risk.",
            "Crew training ensures effective response."
        ],
        resolution_strategy="Maintain circuit redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft hydraulic systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1435-1"
    ),
    DoctrineBlock(
        topic="aircraft_fuel_system",
        keywords=["fuel system", "tank", "pump", "distribution", "contamination"],
        conclusion_template="Aircraft fuel systems must ensure safe storage, distribution, and contamination prevention for reliable engine operation.",
        reasoning_framework="""
        Aircraft fuel systems store and distribute fuel to engines and APUs. The doctrine emphasizes tank integrity, pump reliability, and contamination prevention. Regular fuel sampling and filter replacement are required. System redundancy ensures continued operation in case of pump or valve failures. Regulatory standards mandate compliance with Part 25.963 and associated guidance. Operators must maintain up-to-date fuel system diagrams and ensure crew proficiency in fuel management and emergency procedures. Maintenance schedules must be strictly followed, and any modifications must be certified.
        """,
        key_factors=[
            "Tank integrity",
            "Pump reliability",
            "Contamination prevention",
            "System redundancy",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.963",
            "EASA CS-25.963",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Fuel system failures or contamination can lead to engine shutdown or fire.",
        counter_arguments=[
            "Redundant pumps and valves mitigate risks.",
            "Regular sampling and maintenance prevent contamination.",
            "Crew training ensures effective response."
        ],
        resolution_strategy="Maintain system redundancy, enforce contamination prevention, and ensure crew proficiency.",
        entity_scope="Aircraft fuel systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.963-1"
    ),
    DoctrineBlock(
        topic="bleed_air_pneumatic_system",
        keywords=["bleed air", "pneumatic", "pressure", "temperature", "system integrity"],
        conclusion_template="Bleed air pneumatic systems must provide reliable pressure and temperature control for environmental and engine functions.",
        reasoning_framework="""
        Bleed air systems extract compressed air from engines for cabin pressurization, environmental control, and anti-ice functions. The doctrine requires robust pressure and temperature regulation, leak detection, and system integrity checks. Regulatory standards mandate compliance with Part 25.841 and associated guidance. Maintenance includes regular inspection of ducts, valves, and sensors. Crew must be trained in bleed air failure procedures, including isolation and alternate sources. System modifications must be certified, and all operational parameters documented.
        """,
        key_factors=[
            "Pressure regulation",
            "Temperature control",
            "Leak detection",
            "System integrity",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.841",
            "EASA CS-25.841",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Bleed air failures may compromise cabin pressurization or anti-ice functions.",
        counter_arguments=[
            "Robust regulation and monitoring mitigate risks.",
            "Regular maintenance ensures system integrity.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain regulation systems, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft pneumatic systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.841-1"
    ),
    DoctrineBlock(
        topic="landing_gear_system",
        keywords=["landing gear", "retraction", "extension", "brakes", "steering"],
        conclusion_template="Landing gear systems must ensure reliable retraction, extension, braking, and steering under all operational conditions.",
        reasoning_framework="""
        Landing gear systems provide support during takeoff, landing, and ground operations. The doctrine requires robust retraction/extension mechanisms, brake reliability, and steering control. Redundant hydraulic/electric actuators are mandated to prevent gear-up landings. Maintenance protocols include regular inspection of gear components, lubrication, and brake system checks. Regulatory standards require compliance with Part 25.729 and associated guidance. Crew must be trained in gear failure procedures, including manual extension and alternate braking. System modifications must be certified and documented.
        """,
        key_factors=[
            "Retraction/extension reliability",
            "Brake performance",
            "Steering control",
            "Redundancy",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.729",
            "EASA CS-25.729",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Landing gear failures may result in unsafe landings or ground operations.",
        counter_arguments=[
            "Redundant actuators and systems mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft landing gear systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.729-1"
    ),
    DoctrineBlock(
        topic="environmental_control_system",
        keywords=["environmental control", "cabin pressure", "temperature", "air quality", "ventilation"],
        conclusion_template="Environmental control systems must ensure cabin pressure, temperature, and air quality for passenger and crew safety.",
        reasoning_framework="""
        Environmental control systems regulate cabin pressure, temperature, and air quality. The doctrine requires robust sensors, actuators, and control algorithms to maintain optimal conditions. Redundant systems are mandated to prevent loss of pressurization or temperature control. Maintenance includes regular inspection of valves, sensors, and filters. Regulatory standards require compliance with Part 25.831 and associated guidance. Crew must be trained in environmental system failure procedures, including manual override and alternate sources. System modifications must be certified and documented.
        """,
        key_factors=[
            "Pressure regulation",
            "Temperature control",
            "Air quality",
            "Redundancy",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.831",
            "EASA CS-25.831",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Environmental system failures may compromise passenger and crew safety.",
        counter_arguments=[
            "Redundant systems mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft environmental control systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.831-1"
    ),
    DoctrineBlock(
        topic="fire_detection_suppression",
        keywords=["fire detection", "suppression", "smoke", "alarm", "extinguisher"],
        conclusion_template="Fire detection and suppression systems must provide rapid detection and effective suppression to ensure aircraft safety.",
        reasoning_framework="""
        Fire detection systems utilize sensors and alarms to identify smoke or fire in engines, cargo, and cabin areas. Suppression systems deploy extinguishing agents to mitigate fire risks. The doctrine requires multiple detection zones, redundant sensors, and reliable suppression mechanisms. Maintenance protocols include regular sensor checks, extinguisher inspections, and system tests. Regulatory standards mandate compliance with Part 25.851 and associated guidance. Crew must be trained in fire response procedures, including manual suppression and evacuation. System modifications must be certified and documented.
        """,
        key_factors=[
            "Detection reliability",
            "Suppression effectiveness",
            "Redundancy",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.851",
            "EASA CS-25.851",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Fire detection or suppression failures may lead to catastrophic outcomes.",
        counter_arguments=[
            "Redundant sensors and suppression systems mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft fire detection and suppression systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.851-1"
    ),
    DoctrineBlock(
        topic="oxygen_system",
        keywords=["oxygen", "crew", "passenger", "emergency", "mask"],
        conclusion_template="Oxygen systems must provide reliable supply for crew and passengers during emergencies and high-altitude operations.",
        reasoning_framework="""
        Oxygen systems supply breathable air to crew and passengers during emergencies, decompression, or high-altitude flight. The doctrine requires reliable storage, distribution, and mask deployment mechanisms. Maintenance protocols include regular cylinder inspections, pressure checks, and mask functionality tests. Regulatory standards mandate compliance with Part 25.1447 and associated guidance. Crew must be trained in oxygen system operation and emergency procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Supply reliability",
            "Distribution integrity",
            "Mask deployment",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1447",
            "EASA CS-25.1447",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Oxygen system failures may compromise crew and passenger safety.",
        counter_arguments=[
            "Redundant supply and distribution systems mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft oxygen systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1447-1"
    ),
    DoctrineBlock(
        topic="APU_auxiliary_power_unit",
        keywords=["APU", "auxiliary power", "engine start", "electrical", "bleed air"],
        conclusion_template="Auxiliary Power Units must provide reliable electrical and pneumatic power for engine start and ground operations.",
        reasoning_framework="""
        APUs supply electrical and pneumatic power for engine start, environmental control, and ground operations. The doctrine requires reliable start-up, power output, and integration with main systems. Maintenance protocols include regular inspections, performance checks, and troubleshooting. Regulatory standards mandate compliance with Part 25.1309 and associated guidance. Crew must be trained in APU operation and emergency procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Start-up reliability",
            "Power output",
            "Integration",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1309",
            "EASA CS-25.1309",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="APU failures may compromise engine start or ground operations.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft auxiliary power units",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1309-1A"
    ),
    DoctrineBlock(
        topic="ice_protection_systems",
        keywords=["ice protection", "de-icing", "anti-icing", "wing", "engine"],
        conclusion_template="Ice protection systems must ensure effective de-icing and anti-icing for critical surfaces and engine components.",
        reasoning_framework="""
        Ice protection systems prevent accumulation on wings, tail, engine inlets, and sensors. The doctrine requires reliable detection, activation, and distribution of anti-icing/de-icing agents. Maintenance protocols include regular inspection of heating elements, valves, and sensors. Regulatory standards mandate compliance with Part 25.1419 and associated guidance. Crew must be trained in ice protection operation and emergency procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Detection reliability",
            "Activation effectiveness",
            "Distribution integrity",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1419",
            "EASA CS-25.1419",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Ice protection failures may compromise flight safety.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft ice protection systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1419-1"
    ),
    DoctrineBlock(
        topic="flight_management_system",
        keywords=["flight management", "navigation", "performance", "autopilot", "integration"],
        conclusion_template="Flight Management Systems must provide reliable navigation, performance optimization, and integration with autopilot and avionics.",
        reasoning_framework="""
        Flight Management Systems (FMS) automate navigation, performance calculations, and integration with autopilot and avionics. The doctrine requires reliable software, hardware, and database updates. Maintenance protocols include regular software updates, hardware checks, and database validation. Regulatory standards mandate compliance with Part 25.1302 and associated guidance. Crew must be trained in FMS operation and troubleshooting. System modifications must be certified and documented.
        """,
        key_factors=[
            "Navigation reliability",
            "Performance optimization",
            "Integration",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1302",
            "EASA CS-25.1302",
            "RTCA DO-178C",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="FMS failures may compromise navigation and performance optimization.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft flight management systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-173"
    ),
    DoctrineBlock(
        topic="TCAS_traffic_alert",
        keywords=["TCAS", "traffic alert", "collision avoidance", "transponder", "resolution advisory"],
        conclusion_template="TCAS systems must provide reliable traffic alerts and resolution advisories to prevent mid-air collisions.",
        reasoning_framework="""
        Traffic Collision Avoidance Systems (TCAS) monitor nearby aircraft and provide alerts and resolution advisories. The doctrine requires reliable transponder interrogation, alert generation, and crew response protocols. Maintenance protocols include regular system tests, transponder checks, and software updates. Regulatory standards mandate compliance with Part 25.1322 and associated guidance. Crew must be trained in TCAS operation and advisory response. System modifications must be certified and documented.
        """,
        key_factors=[
            "Alert reliability",
            "Resolution advisory effectiveness",
            "Transponder integrity",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1322",
            "EASA CS-25.1322",
            "RTCA DO-185B",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="TCAS failures may compromise collision avoidance.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft collision avoidance systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-131A"
    ),
    DoctrineBlock(
        topic="EGPWS_terrain_awareness",
        keywords=["EGPWS", "terrain awareness", "warning", "database", "crew response"],
        conclusion_template="EGPWS systems must provide reliable terrain awareness and warning to prevent controlled flight into terrain.",
        reasoning_framework="""
        Enhanced Ground Proximity Warning Systems (EGPWS) utilize terrain databases and aircraft position to provide warnings. The doctrine requires reliable database updates, alert generation, and crew response protocols. Maintenance protocols include regular system tests, database validation, and software updates. Regulatory standards mandate compliance with Part 25.1302 and associated guidance. Crew must be trained in EGPWS operation and warning response. System modifications must be certified and documented.
        """,
        key_factors=[
            "Warning reliability",
            "Database integrity",
            "Alert effectiveness",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1302",
            "EASA CS-25.1302",
            "RTCA DO-309",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="EGPWS failures may compromise terrain awareness.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft terrain awareness systems",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="FAA AC 20-153"
    ),
    DoctrineBlock(
        topic="autopilot_autothrottle",
        keywords=["autopilot", "autothrottle", "flight control", "automation", "crew monitoring"],
        conclusion_template="Autopilot and autothrottle systems must provide reliable automation and maintain crew situational awareness.",
        reasoning_framework="""
        Autopilot and autothrottle systems automate flight control and engine power management. The doctrine requires reliable software, hardware, and integration with flight management systems. Maintenance protocols include regular system tests, software updates, and hardware checks. Regulatory standards mandate compliance with Part 25.1329 and associated guidance. Crew must be trained in automation operation and monitoring. System modifications must be certified and documented.
        """,
        key_factors=[
            "Automation reliability",
            "Integration",
            "Crew monitoring",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1329",
            "EASA CS-25.1329",
            "RTCA DO-178C",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Automation failures may compromise flight control or situational awareness.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft automation systems",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1329-1"
    ),
    DoctrineBlock(
        topic="MSG3_maintenance_program",
        keywords=["MSG-3", "maintenance", "program", "scheduled", "unscheduled"],
        conclusion_template="MSG-3 maintenance programs must optimize scheduled and unscheduled maintenance for reliability and safety.",
        reasoning_framework="""
        MSG-3 maintenance programs utilize reliability-centered maintenance to optimize scheduled and unscheduled tasks. The doctrine requires regular data analysis, task revision, and compliance with manufacturer recommendations. Maintenance protocols include interval checks, task effectiveness reviews, and documentation. Regulatory standards mandate compliance with Part 25.1529 and associated guidance. Operators must ensure maintenance personnel are trained in MSG-3 principles and reporting. Program modifications must be certified and documented.
        """,
        key_factors=[
            "Task optimization",
            "Interval compliance",
            "Data analysis",
            "Personnel training",
            "Documentation"
        ],
        primary_authority=[
            "FAA Part 25.1529",
            "EASA CS-25.1529",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Maintenance programs may fail to address reliability or safety concerns.",
        counter_arguments=[
            "Reliability-centered maintenance optimizes tasks.",
            "Regular data analysis ensures effectiveness.",
            "Personnel training addresses operational challenges."
        ],
        resolution_strategy="Maintain optimization, enforce interval compliance, and ensure personnel proficiency.",
        entity_scope="Aircraft maintenance programs",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="FAA AC 121-22A"
    ),
    DoctrineBlock(
        topic="airworthiness_directives",
        keywords=["airworthiness", "directive", "compliance", "regulatory", "safety"],
        conclusion_template="Airworthiness directives must be complied with promptly to ensure continued safety and regulatory compliance.",
        reasoning_framework="""
        Airworthiness directives (ADs) are mandatory instructions issued by regulatory authorities to address safety concerns. The doctrine requires prompt compliance, documentation, and reporting. Maintenance protocols include task scheduling, completion verification, and record keeping. Regulatory standards mandate compliance with Part 39 and associated guidance. Operators must ensure personnel are trained in AD management and reporting. Modifications must be certified and documented.
        """,
        key_factors=[
            "Prompt compliance",
            "Documentation",
            "Reporting",
            "Personnel training",
            "Record keeping"
        ],
        primary_authority=[
            "FAA Part 39",
            "EASA Part 21",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Failure to comply with ADs may compromise safety and regulatory status.",
        counter_arguments=[
            "Mandatory compliance ensures safety.",
            "Documentation and reporting mitigate risks.",
            "Personnel training addresses operational challenges."
        ],
        resolution_strategy="Maintain prompt compliance, enforce documentation, and ensure personnel proficiency.",
        entity_scope="Aircraft regulatory compliance",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="FAA AC 39-7"
    ),
    DoctrineBlock(
        topic="Part_25_certification",
        keywords=["Part 25", "certification", "airworthiness", "design", "compliance"],
        conclusion_template="Part 25 certification must ensure airworthiness, design compliance, and operational safety for transport category aircraft.",
        reasoning_framework="""
        Part 25 certification governs airworthiness standards for transport category aircraft. The doctrine requires comprehensive design review, compliance demonstration, and operational testing. Regulatory standards mandate adherence to Part 25 and associated guidance. Operators and manufacturers must document compliance, maintain records, and ensure personnel are trained in certification requirements. Modifications must be certified and documented.
        """,
        key_factors=[
            "Design compliance",
            "Operational safety",
            "Documentation",
            "Personnel training",
            "Record keeping"
        ],
        primary_authority=[
            "FAA Part 25",
            "EASA CS-25",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Aircraft Manufacturer/Operator",
        adversary_position="Failure to comply with certification standards may compromise airworthiness.",
        counter_arguments=[
            "Comprehensive review ensures compliance.",
            "Documentation and training mitigate risks.",
            "Regulatory oversight addresses operational challenges."
        ],
        resolution_strategy="Maintain compliance, enforce documentation, and ensure personnel proficiency.",
        entity_scope="Aircraft certification",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.2"
    ),
    DoctrineBlock(
        topic="weight_and_balance",
        keywords=["weight", "balance", "center of gravity", "loading", "performance"],
        conclusion_template="Weight and balance must be managed to ensure safe aircraft performance and compliance with operational limits.",
        reasoning_framework="""
        Weight and balance management ensures aircraft performance and safety. The doctrine requires accurate calculation of loading, center of gravity, and compliance with operational limits. Maintenance protocols include regular weighing, record keeping, and crew training. Regulatory standards mandate compliance with Part 25.23 and associated guidance. Operators must ensure personnel are trained in weight and balance principles and reporting. Modifications must be certified and documented.
        """,
        key_factors=[
            "Loading accuracy",
            "Center of gravity management",
            "Operational limits",
            "Record keeping",
            "Personnel training"
        ],
        primary_authority=[
            "FAA Part 25.23",
            "EASA CS-25.23",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Improper weight and balance may compromise safety and performance.",
        counter_arguments=[
            "Accurate calculation ensures compliance.",
            "Record keeping and training mitigate risks.",
            "Regulatory oversight addresses operational challenges."
        ],
        resolution_strategy="Maintain accuracy, enforce record keeping, and ensure personnel proficiency.",
        entity_scope="Aircraft weight and balance",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-27E"
    ),
    # Additional doctrine blocks for comprehensive coverage
    DoctrineBlock(
        topic="emergency_power_management",
        keywords=["emergency power", "battery", "generator", "load shedding", "continuity"],
        conclusion_template="Emergency power management must ensure continuity of critical systems during generator or main power failures.",
        reasoning_framework="""
        Emergency power systems provide backup energy to critical avionics, flight controls, and communication systems. The doctrine requires robust battery capacity, automatic generator switching, and load shedding protocols. Maintenance includes regular battery checks, generator tests, and system diagnostics. Regulatory standards mandate compliance with Part 25.1351 and associated guidance. Crew must be trained in emergency power procedures and troubleshooting. System modifications must be certified and documented.
        """,
        key_factors=[
            "Battery capacity",
            "Generator switching",
            "Load shedding",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1351",
            "EASA CS-25.1351",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Emergency power failures may compromise critical systems.",
        counter_arguments=[
            "Redundant batteries and generators mitigate risks.",
            "Automatic switching ensures continuity.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft emergency power systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1351-1"
    ),
    DoctrineBlock(
        topic="engine_fire_protection",
        keywords=["engine fire", "detection", "suppression", "alarm", "response"],
        conclusion_template="Engine fire protection systems must provide rapid detection and effective suppression to prevent catastrophic failure.",
        reasoning_framework="""
        Engine fire protection systems utilize sensors and suppression agents to detect and extinguish fires. The doctrine requires multiple detection zones, redundant sensors, and reliable suppression mechanisms. Maintenance includes regular sensor checks, extinguisher inspections, and system tests. Regulatory standards mandate compliance with Part 25.1182 and associated guidance. Crew must be trained in engine fire response procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Detection reliability",
            "Suppression effectiveness",
            "Redundancy",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1182",
            "EASA CS-25.1182",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Engine fire protection failures may lead to catastrophic outcomes.",
        counter_arguments=[
            "Redundant sensors and suppression systems mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft engine fire protection systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1182-1"
    ),
    DoctrineBlock(
        topic="cabin_smoke_detection",
        keywords=["cabin", "smoke detection", "alarm", "evacuation", "crew response"],
        conclusion_template="Cabin smoke detection systems must provide rapid alerts and enable effective crew response and evacuation.",
        reasoning_framework="""
        Cabin smoke detection systems utilize sensors and alarms to identify smoke and initiate evacuation procedures. The doctrine requires reliable detection, alarm activation, and crew response protocols. Maintenance includes regular sensor checks, alarm tests, and system diagnostics. Regulatory standards mandate compliance with Part 25.851 and associated guidance. Crew must be trained in smoke detection response and evacuation procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Detection reliability",
            "Alarm activation",
            "Crew response",
            "Maintenance intervals",
            "Evacuation procedures"
        ],
        primary_authority=[
            "FAA Part 25.851",
            "EASA CS-25.851",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Smoke detection failures may compromise evacuation and safety.",
        counter_arguments=[
            "Redundant sensors and alarms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft cabin smoke detection systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.851-1"
    ),
    DoctrineBlock(
        topic="crew_alerting_systems",
        keywords=["crew alerting", "EICAS", "alarms", "warnings", "response"],
        conclusion_template="Crew alerting systems must provide timely and accurate alarms and warnings to enable effective response.",
        reasoning_framework="""
        Crew alerting systems consolidate alarms, warnings, and advisories for rapid crew response. The doctrine requires reliable integration, prioritization, and display clarity. Maintenance includes regular system tests, software updates, and hardware checks. Regulatory standards mandate compliance with Part 25.1322 and associated guidance. Crew must be trained in alerting system operation and response. System modifications must be certified and documented.
        """,
        key_factors=[
            "Integration reliability",
            "Prioritization",
            "Display clarity",
            "Maintenance intervals",
            "Crew training"
        ],
        primary_authority=[
            "FAA Part 25.1322",
            "EASA CS-25.1322",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Alerting system failures may compromise crew response.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain integration, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft crew alerting systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1322-1"
    ),
    DoctrineBlock(
        topic="emergency_lighting_system",
        keywords=["emergency lighting", "evacuation", "battery", "visibility", "maintenance"],
        conclusion_template="Emergency lighting systems must ensure visibility and enable safe evacuation during power failures.",
        reasoning_framework="""
        Emergency lighting systems provide illumination during power failures to facilitate evacuation. The doctrine requires reliable battery backup, automatic activation, and regular maintenance. Regulatory standards mandate compliance with Part 25.812 and associated guidance. Crew must be trained in emergency lighting operation and evacuation procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Battery backup",
            "Automatic activation",
            "Visibility",
            "Maintenance intervals",
            "Evacuation procedures"
        ],
        primary_authority=[
            "FAA Part 25.812",
            "EASA CS-25.812",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Lighting failures may compromise evacuation safety.",
        counter_arguments=[
            "Redundant batteries and automatic activation mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain battery backup, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft emergency lighting systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.812-1"
    ),
    DoctrineBlock(
        topic="emergency_evacuation_system",
        keywords=["emergency evacuation", "slide", "door", "crew training", "maintenance"],
        conclusion_template="Emergency evacuation systems must enable rapid and safe evacuation of passengers and crew.",
        reasoning_framework="""
        Emergency evacuation systems include slides, doors, and crew protocols for rapid evacuation. The doctrine requires reliable slide deployment, door operation, and crew training. Maintenance includes regular slide inspections, door tests, and system diagnostics. Regulatory standards mandate compliance with Part 25.809 and associated guidance. Crew must be trained in evacuation procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Slide deployment",
            "Door operation",
            "Crew training",
            "Maintenance intervals",
            "Evacuation protocols"
        ],
        primary_authority=[
            "FAA Part 25.809",
            "EASA CS-25.809",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Evacuation system failures may compromise passenger safety.",
        counter_arguments=[
            "Redundant slides and doors mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft emergency evacuation systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.809-1"
    ),
    DoctrineBlock(
        topic="emergency_communication_system",
        keywords=["emergency communication", "PA", "intercom", "radio", "crew training"],
        conclusion_template="Emergency communication systems must enable reliable crew and passenger communication during emergencies.",
        reasoning_framework="""
        Emergency communication systems include PA, intercom, and radio for crew and passenger coordination. The doctrine requires reliable operation, redundancy, and crew training. Maintenance includes regular system tests, hardware checks, and software updates. Regulatory standards mandate compliance with Part 25.1307 and associated guidance. Crew must be trained in emergency communication procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Operation reliability",
            "Redundancy",
            "Crew training",
            "Maintenance intervals",
            "Communication protocols"
        ],
        primary_authority=[
            "FAA Part 25.1307",
            "EASA CS-25.1307",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Communication system failures may compromise emergency coordination.",
        counter_arguments=[
            "Redundant systems and backup procedures mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain redundancy, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft emergency communication systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1307-1"
    ),
    DoctrineBlock(
        topic="emergency_medical_equipment",
        keywords=["emergency medical", "first aid", "AED", "crew training", "maintenance"],
        conclusion_template="Emergency medical equipment must be available, functional, and crew must be trained in its use.",
        reasoning_framework="""
        Emergency medical equipment includes first aid kits, AEDs, and crew protocols for medical emergencies. The doctrine requires reliable equipment availability, regular maintenance, and crew training. Maintenance includes regular equipment checks, expiration monitoring, and system diagnostics. Regulatory standards mandate compliance with Part 121.803 and associated guidance. Crew must be trained in medical emergency procedures. Equipment modifications must be certified and documented.
        """,
        key_factors=[
            "Equipment availability",
            "Functionality",
            "Crew training",
            "Maintenance intervals",
            "Medical protocols"
        ],
        primary_authority=[
            "FAA Part 121.803",
            "EASA OPS 1.745",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Medical equipment failures may compromise passenger safety.",
        counter_arguments=[
            "Regular equipment checks mitigate risks.",
            "Crew training ensures effective response.",
            "Regulatory oversight addresses operational challenges."
        ],
        resolution_strategy="Maintain equipment availability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft emergency medical systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 121-33"
    ),
    DoctrineBlock(
        topic="emergency_water_landings",
        keywords=["water landing", "life vest", "raft", "crew training", "maintenance"],
        conclusion_template="Emergency water landing systems must ensure availability and functionality of life vests and rafts, and crew must be trained in their use.",
        reasoning_framework="""
        Emergency water landing systems include life vests, rafts, and crew protocols for water evacuation. The doctrine requires reliable equipment availability, regular maintenance, and crew training. Maintenance includes regular equipment checks, expiration monitoring, and system diagnostics. Regulatory standards mandate compliance with Part 25.1411 and associated guidance. Crew must be trained in water landing procedures. Equipment modifications must be certified and documented.
        """,
        key_factors=[
            "Equipment availability",
            "Functionality",
            "Crew training",
            "Maintenance intervals",
            "Water landing protocols"
        ],
        primary_authority=[
            "FAA Part 25.1411",
            "EASA CS-25.1411",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Water landing equipment failures may compromise passenger safety.",
        counter_arguments=[
            "Regular equipment checks mitigate risks.",
            "Crew training ensures effective response.",
            "Regulatory oversight addresses operational challenges."
        ],
        resolution_strategy="Maintain equipment availability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft water landing systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1411-1"
    ),
    DoctrineBlock(
        topic="emergency_decompression_management",
        keywords=["decompression", "oxygen", "crew training", "maintenance", "response"],
        conclusion_template="Emergency decompression management must ensure rapid oxygen supply and crew response to maintain safety.",
        reasoning_framework="""
        Emergency decompression management includes oxygen supply, crew protocols, and passenger coordination. The doctrine requires reliable oxygen system operation, regular maintenance, and crew training. Maintenance includes regular oxygen system checks, mask tests, and system diagnostics. Regulatory standards mandate compliance with Part 25.1447 and associated guidance. Crew must be trained in decompression response procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Oxygen supply reliability",
            "Crew training",
            "Maintenance intervals",
            "Decompression protocols",
            "Passenger coordination"
        ],
        primary_authority=[
            "FAA Part 25.1447",
            "EASA CS-25.1447",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Decompression management failures may compromise safety.",
        counter_arguments=[
            "Redundant oxygen systems mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain oxygen supply, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft decompression management systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1447-1"
    ),
    DoctrineBlock(
        topic="emergency_flight_control_reversion",
        keywords=["flight control reversion", "manual", "hydraulic", "crew training", "maintenance"],
        conclusion_template="Emergency flight control reversion systems must enable safe manual control in case of hydraulic or electronic failures.",
        reasoning_framework="""
        Emergency flight control reversion includes manual control protocols, hydraulic backup, and crew training. The doctrine requires reliable reversion mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, hydraulic tests, and diagnostics. Regulatory standards mandate compliance with Part 25.671 and associated guidance. Crew must be trained in flight control reversion procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Reversion reliability",
            "Manual control protocols",
            "Hydraulic backup",
            "Crew training",
            "Maintenance intervals"
        ],
        primary_authority=[
            "FAA Part 25.671",
            "EASA CS-25.671",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Flight control reversion failures may compromise safety.",
        counter_arguments=[
            "Redundant reversion mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain reversion reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft flight control reversion systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.671-1"
    ),
    DoctrineBlock(
        topic="emergency_engine_shutdown",
        keywords=["engine shutdown", "crew training", "maintenance", "response", "safety"],
        conclusion_template="Emergency engine shutdown procedures must enable rapid and safe response to engine failures or fires.",
        reasoning_framework="""
        Emergency engine shutdown includes crew protocols, system integration, and maintenance. The doctrine requires reliable shutdown mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, shutdown tests, and diagnostics. Regulatory standards mandate compliance with Part 25.1182 and associated guidance. Crew must be trained in engine shutdown procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Shutdown reliability",
            "Crew training",
            "Maintenance intervals",
            "Shutdown protocols",
            "Safety"
        ],
        primary_authority=[
            "FAA Part 25.1182",
            "EASA CS-25.1182",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Engine shutdown failures may compromise safety.",
        counter_arguments=[
            "Redundant shutdown mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain shutdown reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft engine shutdown systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1182-1"
    ),
    DoctrineBlock(
        topic="emergency_landing_gear_extension",
        keywords=["landing gear extension", "manual", "hydraulic", "crew training", "maintenance"],
        conclusion_template="Emergency landing gear extension systems must enable safe manual deployment in case of hydraulic or electronic failures.",
        reasoning_framework="""
        Emergency landing gear extension includes manual protocols, hydraulic backup, and crew training. The doctrine requires reliable extension mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, hydraulic tests, and diagnostics. Regulatory standards mandate compliance with Part 25.729 and associated guidance. Crew must be trained in landing gear extension procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Extension reliability",
            "Manual protocols",
            "Hydraulic backup",
            "Crew training",
            "Maintenance intervals"
        ],
        primary_authority=[
            "FAA Part 25.729",
            "EASA CS-25.729",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Landing gear extension failures may compromise safety.",
        counter_arguments=[
            "Redundant extension mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain extension reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft landing gear extension systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.729-1"
    ),
    DoctrineBlock(
        topic="emergency_fuel_shutoff",
        keywords=["fuel shutoff", "crew training", "maintenance", "response", "safety"],
        conclusion_template="Emergency fuel shutoff systems must enable rapid and safe response to fuel leaks or fires.",
        reasoning_framework="""
        Emergency fuel shutoff includes crew protocols, system integration, and maintenance. The doctrine requires reliable shutoff mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, shutoff tests, and diagnostics. Regulatory standards mandate compliance with Part 25.963 and associated guidance. Crew must be trained in fuel shutoff procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Shutoff reliability",
            "Crew training",
            "Maintenance intervals",
            "Shutoff protocols",
            "Safety"
        ],
        primary_authority=[
            "FAA Part 25.963",
            "EASA CS-25.963",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Fuel shutoff failures may compromise safety.",
        counter_arguments=[
            "Redundant shutoff mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain shutoff reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft fuel shutoff systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.963-1"
    ),
    DoctrineBlock(
        topic="emergency_bleed_air_isolation",
        keywords=["bleed air isolation", "manual", "crew training", "maintenance", "response"],
        conclusion_template="Emergency bleed air isolation systems must enable safe manual isolation in case of leaks or failures.",
        reasoning_framework="""
        Emergency bleed air isolation includes manual protocols, system integration, and crew training. The doctrine requires reliable isolation mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, isolation tests, and diagnostics. Regulatory standards mandate compliance with Part 25.841 and associated guidance. Crew must be trained in bleed air isolation procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Isolation reliability",
            "Manual protocols",
            "Crew training",
            "Maintenance intervals",
            "Response"
        ],
        primary_authority=[
            "FAA Part 25.841",
            "EASA CS-25.841",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Bleed air isolation failures may compromise safety.",
        counter_arguments=[
            "Redundant isolation mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain isolation reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft bleed air isolation systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.841-1"
    ),
    DoctrineBlock(
        topic="emergency_hydraulic_system_isolation",
        keywords=["hydraulic system isolation", "manual", "crew training", "maintenance", "response"],
        conclusion_template="Emergency hydraulic system isolation must enable safe manual isolation in case of leaks or failures.",
        reasoning_framework="""
        Emergency hydraulic system isolation includes manual protocols, system integration, and crew training. The doctrine requires reliable isolation mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, isolation tests, and diagnostics. Regulatory standards mandate compliance with Part 25.1435 and associated guidance. Crew must be trained in hydraulic system isolation procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Isolation reliability",
            "Manual protocols",
            "Crew training",
            "Maintenance intervals",
            "Response"
        ],
        primary_authority=[
            "FAA Part 25.1435",
            "EASA CS-25.1435",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Hydraulic system isolation failures may compromise safety.",
        counter_arguments=[
            "Redundant isolation mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain isolation reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft hydraulic system isolation",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1435-1"
    ),
    DoctrineBlock(
        topic="emergency_electrical_bus_isolation",
        keywords=["electrical bus isolation", "manual", "crew training", "maintenance", "response"],
        conclusion_template="Emergency electrical bus isolation must enable safe manual isolation in case of faults or failures.",
        reasoning_framework="""
        Emergency electrical bus isolation includes manual protocols, system integration, and crew training. The doctrine requires reliable isolation mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, isolation tests, and diagnostics. Regulatory standards mandate compliance with Part 25.1351 and associated guidance. Crew must be trained in electrical bus isolation procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Isolation reliability",
            "Manual protocols",
            "Crew training",
            "Maintenance intervals",
            "Response"
        ],
        primary_authority=[
            "FAA Part 25.1351",
            "EASA CS-25.1351",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Electrical bus isolation failures may compromise safety.",
        counter_arguments=[
            "Redundant isolation mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain isolation reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft electrical bus isolation",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1351-1"
    ),
    DoctrineBlock(
        topic="emergency_avionics_backup",
        keywords=["avionics backup", "manual", "crew training", "maintenance", "response"],
        conclusion_template="Emergency avionics backup systems must enable safe manual operation in case of primary system failures.",
        reasoning_framework="""
        Emergency avionics backup includes manual protocols, system integration, and crew training. The doctrine requires reliable backup mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, backup tests, and diagnostics. Regulatory standards mandate compliance with Part 25.1302 and associated guidance. Crew must be trained in avionics backup procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Backup reliability",
            "Manual protocols",
            "Crew training",
            "Maintenance intervals",
            "Response"
        ],
        primary_authority=[
            "FAA Part 25.1302",
            "EASA CS-25.1302",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Avionics backup failures may compromise safety.",
        counter_arguments=[
            "Redundant backup mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain backup reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft avionics backup systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1302-1"
    ),
    DoctrineBlock(
        topic="emergency_autopilot_disengagement",
        keywords=["autopilot disengagement", "manual", "crew training", "maintenance", "response"],
        conclusion_template="Emergency autopilot disengagement must enable safe manual control in case of automation failures.",
        reasoning_framework="""
        Emergency autopilot disengagement includes manual protocols, system integration, and crew training. The doctrine requires reliable disengagement mechanisms, regular maintenance, and crew training. Maintenance includes regular system checks, disengagement tests, and diagnostics. Regulatory standards mandate compliance with Part 25.1329 and associated guidance. Crew must be trained in autopilot disengagement procedures. System modifications must be certified and documented.
        """,
        key_factors=[
            "Disengagement reliability",
            "Manual protocols",
            "Crew training",
            "Maintenance intervals",
            "Response"
        ],
        primary_authority=[
            "FAA Part 25.1329",
            "EASA CS-25.1329",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Autopilot disengagement failures may compromise safety.",
        counter_arguments=[
            "Redundant disengagement mechanisms mitigate risks.",
            "Regular maintenance ensures reliability.",
            "Crew training addresses operational challenges."
        ],
        resolution_strategy="Maintain disengagement reliability, enforce maintenance, and ensure crew proficiency.",
        entity_scope="Aircraft autopilot disengagement systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 25.1329-1"
    ),
    DoctrineBlock(
        topic="emergency_maintenance_reporting",
        keywords=["maintenance reporting", "emergency", "crew training", "documentation", "regulatory"],
        conclusion_template="Emergency maintenance reporting must ensure prompt documentation and regulatory compliance.",
        reasoning_framework="""
        Emergency maintenance reporting includes crew protocols, documentation, and regulatory compliance. The doctrine requires prompt reporting, accurate documentation, and crew training. Maintenance includes regular review of reporting procedures and record keeping. Regulatory standards mandate compliance with Part 121.703 and associated guidance. Crew must be trained in maintenance reporting procedures. Modifications must be certified and documented.
        """,
        key_factors=[
            "Prompt reporting",
            "Documentation",
            "Regulatory compliance",
            "Crew training",
            "Record keeping"
        ],
        primary_authority=[
            "FAA Part 121.703",
            "EASA Part M",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Maintenance reporting failures may compromise safety and regulatory status.",
        counter_arguments=[
            "Prompt reporting ensures compliance.",
            "Documentation and training mitigate risks.",
            "Regulatory oversight addresses operational challenges."
        ],
        resolution_strategy="Maintain prompt reporting, enforce documentation, and ensure crew proficiency.",
        entity_scope="Aircraft emergency maintenance reporting",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 121-22A"
    ),
    DoctrineBlock(
        topic="emergency_airworthiness_directive_compliance",
        keywords=["airworthiness directive", "emergency", "compliance", "crew training", "documentation"],
        conclusion_template="Emergency airworthiness directive compliance must ensure prompt action and regulatory documentation.",
        reasoning_framework="""
        Emergency airworthiness directive compliance includes crew protocols, documentation, and regulatory compliance. The doctrine requires prompt compliance, accurate documentation, and crew training. Maintenance includes regular review of directive procedures and record keeping. Regulatory standards mandate compliance with Part 39 and associated guidance. Crew must be trained in directive compliance procedures. Modifications must be certified and documented.
        """,
        key_factors=[
            "Prompt compliance",
            "Documentation",
            "Regulatory compliance",
            "Crew training",
            "Record keeping"
        ],
        primary_authority=[
            "FAA Part 39",
            "EASA Part 21",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Directive compliance failures may compromise safety and regulatory status.",
        counter_arguments=[
            "Prompt compliance ensures safety.",
            "Documentation and training mitigate risks.",
            "Regulatory oversight addresses operational challenges."
        ],
        resolution_strategy="Maintain prompt compliance, enforce documentation, and ensure crew proficiency.",
        entity_scope="Aircraft emergency directive compliance",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 39-7"
    ),
    DoctrineBlock(
        topic="emergency_weight_and_balance_management",
        keywords=["weight and balance", "emergency", "crew training", "documentation", "regulatory"],
        conclusion_template="Emergency weight and balance management must ensure safe aircraft performance and compliance during abnormal operations.",
        reasoning_framework="""
        Emergency weight and balance management includes crew protocols, documentation, and regulatory compliance. The doctrine requires accurate calculation, prompt reporting, and crew training. Maintenance includes regular review of weight and balance procedures and record keeping. Regulatory standards mandate compliance with Part 25.23 and associated guidance. Crew must be trained in emergency weight and balance procedures. Modifications must be certified and documented.
        """,
        key_factors=[
            "Accurate calculation",
            "Prompt reporting",
            "Regulatory compliance",
            "Crew training",
            "Record keeping"
        ],
        primary_authority=[
            "FAA Part 25.23",
            "EASA CS-25.23",
            "Aircraft manufacturer manuals"
        ],
        burden_holder="Operator/Maintenance Organization",
        adversary_position="Weight and balance management failures may compromise safety and performance.",
        counter_arguments=[
            "Accurate calculation ensures compliance.",
            "Documentation and training mitigate risks.",
            "Regulatory oversight addresses operational challenges."
        ],
        resolution_strategy="Maintain accuracy, enforce documentation, and ensure crew proficiency.",
        entity_scope="Aircraft emergency weight and balance management",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="FAA AC 120-27E"
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