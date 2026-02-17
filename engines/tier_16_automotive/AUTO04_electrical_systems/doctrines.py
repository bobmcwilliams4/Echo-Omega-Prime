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
        topic="Battery Management Systems",
        keywords=["battery", "management", "BMS", "charge", "discharge", "thermal", "safety"],
        conclusion_template="Effective battery management systems (BMS) are critical to ensure optimal charge cycles, prevent thermal runaway, and extend battery lifespan.",
        reasoning_framework=(
            "Battery Management Systems (BMS) monitor and regulate the charging and discharging of battery cells to maintain "
            "safe operating conditions. The framework involves real-time monitoring of cell voltages, temperatures, and current "
            "flows. By balancing cell charge levels and preventing overcharge or deep discharge, the BMS mitigates risks of "
            "thermal runaway and capacity degradation. The reasoning includes fault detection algorithms, state-of-charge "
            "(SOC) estimation, and state-of-health (SOH) diagnostics. The system must also interface with vehicle control units "
            "to adjust power demands based on battery status. Safety protocols embedded in the BMS ensure isolation of faulty "
            "cells and trigger protective shutdowns. The framework integrates hardware redundancy and software fail-safes to "
            "maintain operational integrity under various environmental and load conditions."
        ),
        key_factors=["cell voltage monitoring", "temperature sensing", "charge balancing", "fault detection", "thermal management"],
        primary_authority=["ISO 26262", "SAE J2464", "UL 2580"],
        burden_holder="Battery System Manufacturer",
        adversary_position="Some argue that simplified BMS designs reduce cost and complexity at the expense of safety margins.",
        counter_arguments=[
            "Simplified BMS designs increase risk of undetected faults leading to catastrophic failures.",
            "Cost savings are outweighed by potential warranty claims and safety liabilities."
        ],
        resolution_strategy="Adopt comprehensive BMS designs adhering to international safety standards with rigorous testing.",
        entity_scope="Battery Systems in Electric Vehicles",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="UL 2580 Certification Requirements for Battery Systems"
    ),
    DoctrineBlock(
        topic="Electric Motor Thermal Management",
        keywords=["electric motor", "thermal", "cooling", "heat dissipation", "efficiency", "overheating"],
        conclusion_template="Proper thermal management of electric motors is essential to maintain efficiency and prevent premature failure.",
        reasoning_framework=(
            "Electric motors generate heat due to electrical resistance and magnetic losses during operation. The thermal management "
            "framework involves designing cooling systems—air, liquid, or oil-based—to dissipate heat effectively. Thermal sensors "
            "monitor motor temperature to prevent overheating. The reasoning includes heat transfer principles, material thermal "
            "conductivity, and cooling circuit design. Overheating can degrade insulation and bearings, reducing motor lifespan. "
            "Thermal models predict temperature rise under various load cycles, informing control strategies to modulate power "
            "output or activate cooling. Integration with vehicle thermal management systems ensures coordinated temperature control."
        ),
        key_factors=["heat generation", "cooling system design", "thermal sensors", "temperature thresholds", "material properties"],
        primary_authority=["IEEE Std 841", "SAE J2954", "IEC 60034"],
        burden_holder="Electric Motor Manufacturer",
        adversary_position="Some stakeholders prioritize compact motor designs that limit cooling options to reduce weight.",
        counter_arguments=[
            "Insufficient cooling leads to thermal stress and early motor failure.",
            "Weight savings are negated by increased maintenance and replacement costs."
        ],
        resolution_strategy="Implement optimized cooling solutions balancing size, weight, and thermal performance validated by thermal simulations.",
        entity_scope="Traction Motors in Electric Vehicles",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IEEE Std 841-2009 - Specification for Petroleum and Chemical Industry Severe Duty Totally Enclosed Fan-Cooled (TEFC) Squirrel Cage Induction Motors"
    ),
    DoctrineBlock(
        topic="High Voltage Safety Protocols",
        keywords=["high voltage", "safety", "insulation", "isolation", "shock prevention", "standards"],
        conclusion_template="Adherence to stringent high voltage safety protocols is mandatory to protect personnel and equipment from electrical hazards.",
        reasoning_framework=(
            "High voltage systems in electric vehicles pose significant risks of electric shock and arc flash incidents. Safety protocols "
            "require robust insulation materials, physical barriers, and isolation monitoring to detect insulation degradation. The "
            "framework includes compliance with standards such as IEC 61851 and ISO 6469, which specify requirements for protective "
            "measures and warning signage. Personnel training and use of personal protective equipment (PPE) are integral. The reasoning "
            "also covers emergency shutdown procedures, grounding schemes, and fault current interruption mechanisms. Regular testing "
            "and maintenance ensure continued safety performance. Risk assessments guide the implementation of layered safety controls."
        ),
        key_factors=["insulation resistance", "isolation monitoring", "PPE usage", "emergency shutdown", "grounding"],
        primary_authority=["IEC 61851", "ISO 6469", "NFPA 70E"],
        burden_holder="Vehicle Manufacturer and Maintenance Personnel",
        adversary_position="Some argue that extensive safety measures increase costs and complexity without proportional risk reduction.",
        counter_arguments=[
            "Electrical hazards can cause fatal injuries and costly equipment damage.",
            "Regulatory compliance and insurance requirements mandate strict safety protocols."
        ],
        resolution_strategy="Implement comprehensive safety programs combining engineering controls, administrative procedures, and training.",
        entity_scope="High Voltage Electrical Systems in Vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="NFPA 70E Standard for Electrical Safety in the Workplace"
    ),
    DoctrineBlock(
        topic="Charging Infrastructure Interoperability",
        keywords=["charging", "infrastructure", "interoperability", "communication protocols", "standards", "EVSE"],
        conclusion_template="Ensuring interoperability of charging infrastructure with diverse electric vehicles is essential for user convenience and system scalability.",
        reasoning_framework=(
            "Charging infrastructure must support multiple vehicle types and manufacturers through standardized communication protocols such as "
            "ISO 15118 and CHAdeMO. The reasoning framework includes negotiation of charging parameters, authentication, billing, and safety "
            "checks. Interoperability reduces user confusion and infrastructure redundancy. It requires adherence to open standards and "
            "collaborative industry efforts. The system must handle varying voltage and current levels, connector types, and charging modes. "
            "Security considerations protect against cyber threats during communication. Testing and certification processes validate compliance."
        ),
        key_factors=["communication protocols", "connector standards", "authentication", "billing integration", "security"],
        primary_authority=["ISO 15118", "SAE J1772", "CHAdeMO Association"],
        burden_holder="Charging Station Operators and Manufacturers",
        adversary_position="Some operators prefer proprietary systems to lock in customers and control pricing.",
        counter_arguments=[
            "Proprietary systems limit market growth and frustrate users.",
            "Open standards foster innovation and broader adoption."
        ],
        resolution_strategy="Adopt and promote open standards with certification to guarantee interoperability and security.",
        entity_scope="Electric Vehicle Supply Equipment (EVSE)",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="ISO 15118-20 - Vehicle to Grid Communication Interface"
    ),
    DoctrineBlock(
        topic="Regenerative Braking Control Strategies",
        keywords=["regenerative braking", "energy recovery", "control algorithms", "brake blending", "efficiency"],
        conclusion_template="Optimized regenerative braking control strategies maximize energy recovery while maintaining vehicle stability and driver comfort.",
        reasoning_framework=(
            "Regenerative braking systems convert kinetic energy into electrical energy during deceleration. Control strategies must balance "
            "energy recovery with friction brake application to ensure smooth braking feel and safety. The reasoning framework involves "
            "sensor fusion from wheel speed sensors, brake pressure sensors, and vehicle dynamics control units. Algorithms predict "
            "available regenerative torque and blend it with mechanical brakes seamlessly. Constraints include battery state-of-charge, "
            "motor temperature, and road conditions. Adaptive control adjusts regeneration levels based on driver behavior and environmental factors. "
            "The framework also considers fail-safe modes to maintain braking performance in case of system faults."
        ),
        key_factors=["torque estimation", "sensor fusion", "brake blending", "battery SOC", "fail-safe operation"],
        primary_authority=["SAE J2907", "ISO 26262", "SAE J2982"],
        burden_holder="Vehicle Control System Developer",
        adversary_position="Some designs prioritize maximum regeneration at the cost of brake feel and safety margins.",
        counter_arguments=[
            "Excessive regeneration can cause instability and driver discomfort.",
            "Balanced control ensures safety without sacrificing efficiency."
        ],
        resolution_strategy="Implement adaptive control algorithms validated through extensive testing and simulation.",
        entity_scope="Electric Vehicle Brake Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2907 - Regenerative Braking System Performance"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Wiring Harness Design",
        keywords=["wiring harness", "design", "electrical distribution", "shielding", "connectors", "durability"],
        conclusion_template="Robust wiring harness design is vital for reliable electrical distribution and protection against environmental and mechanical stresses.",
        reasoning_framework=(
            "Wiring harnesses in electric vehicles distribute power and signals between components. The design framework includes selection "
            "of conductor sizes based on current ratings, insulation materials resistant to heat and chemicals, and shielding to prevent "
            "electromagnetic interference (EMI). Connector selection ensures secure, vibration-resistant connections with proper sealing. "
            "Routing strategies minimize exposure to abrasion and thermal sources. The framework also considers modularity for ease of assembly "
            "and maintenance. Durability testing simulates mechanical stresses, temperature cycles, and moisture ingress. Compliance with "
            "standards such as IPC/WHMA-A-620 guides quality requirements."
        ),
        key_factors=["conductor sizing", "insulation", "EMI shielding", "connector reliability", "environmental resistance"],
        primary_authority=["IPC/WHMA-A-620", "SAE J1128", "ISO 6722"],
        burden_holder="Wiring Harness Manufacturer",
        adversary_position="Cost pressures sometimes lead to undersized conductors or lower-grade materials.",
        counter_arguments=[
            "Substandard harnesses cause failures, recalls, and safety hazards.",
            "Investing in quality reduces lifecycle costs and improves reliability."
        ],
        resolution_strategy="Adhere to industry standards and perform rigorous validation testing.",
        entity_scope="Electric Vehicle Electrical Distribution Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="IPC/WHMA-A-620 - Requirements and Acceptance for Cable and Wire Harness Assemblies"
    ),
    DoctrineBlock(
        topic="Power Electronics Cooling Techniques",
        keywords=["power electronics", "cooling", "inverters", "thermal management", "heat sinks", "liquid cooling"],
        conclusion_template="Effective cooling techniques for power electronics ensure operational reliability and prevent thermal-induced failures.",
        reasoning_framework=(
            "Power electronics components such as inverters and converters generate significant heat during operation. The cooling framework "
            "includes passive methods like heat sinks and thermal interface materials, as well as active methods including forced air and liquid "
            "cooling. Thermal simulations guide design choices to maintain junction temperatures within safe limits. The reasoning also "
            "addresses packaging constraints, vibration resistance, and maintenance accessibility. Monitoring temperature sensors enable "
            "dynamic cooling control. The framework balances cooling efficiency, system complexity, and cost. Failure to manage heat leads "
            "to reduced efficiency, accelerated aging, and catastrophic failures."
        ),
        key_factors=["heat dissipation", "thermal interface", "coolant flow", "temperature monitoring", "packaging"],
        primary_authority=["JEDEC JESD51", "SAE J2954", "IEC 60747"],
        burden_holder="Power Electronics Manufacturer",
        adversary_position="Some designs minimize cooling to reduce size and cost, risking overheating.",
        counter_arguments=[
            "Inadequate cooling compromises reliability and safety.",
            "Proper thermal design extends component life and performance."
        ],
        resolution_strategy="Implement multi-level cooling solutions validated by thermal testing and modeling.",
        entity_scope="Electric Vehicle Power Electronics Modules",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="JEDEC JESD51 - Thermal Test Methodologies"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Grounding Schemes",
        keywords=["grounding", "earthing", "electrical safety", "fault currents", "chassis ground", "isolation monitoring"],
        conclusion_template="Proper grounding schemes are essential to ensure electrical safety and fault current management in electric vehicles.",
        reasoning_framework=(
            "Grounding schemes provide reference potentials and paths for fault currents to prevent electric shock and equipment damage. "
            "The framework includes chassis grounding, isolation monitoring to detect leakage currents, and compliance with standards such as "
            "ISO 6469. The reasoning involves analysis of fault scenarios, grounding resistance, and electromagnetic compatibility. "
            "Effective grounding reduces electromagnetic interference and ensures reliable operation of safety systems. The framework "
            "also addresses grounding conductor sizing, connection methods, and verification procedures. Fault detection systems trigger "
            "protective actions upon ground faults."
        ),
        key_factors=["ground resistance", "isolation monitoring", "fault current paths", "EMC", "verification"],
        primary_authority=["ISO 6469", "IEC 60364", "SAE J1766"],
        burden_holder="Vehicle Electrical System Designer",
        adversary_position="Some designs use minimal grounding to reduce weight and complexity.",
        counter_arguments=[
            "Insufficient grounding increases risk of shock and system malfunction.",
            "Proper grounding is mandated by safety regulations and standards."
        ],
        resolution_strategy="Design grounding schemes per international standards with regular testing and monitoring.",
        entity_scope="Electric Vehicle Electrical Systems",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="IEC 60364 - Electrical Installations of Buildings"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Communication Networks",
        keywords=["CAN bus", "Ethernet", "communication protocols", "diagnostics", "real-time data", "security"],
        conclusion_template="Robust communication networks are fundamental for real-time control, diagnostics, and security in electric vehicles.",
        reasoning_framework=(
            "Electric vehicles rely on communication networks such as CAN bus, LIN, and Automotive Ethernet to interconnect control units, sensors, "
            "and actuators. The framework encompasses protocol selection based on bandwidth, latency, and reliability requirements. "
            "Diagnostics use network data to detect faults and enable predictive maintenance. Security mechanisms protect against cyber threats "
            "including message spoofing and unauthorized access. The reasoning includes network topology design, error handling, and redundancy. "
            "Standards such as ISO 11898 and IEEE 802.3 guide implementation. Network management protocols ensure efficient bandwidth usage "
            "and fault tolerance."
        ),
        key_factors=["protocol selection", "latency", "error detection", "security", "diagnostics"],
        primary_authority=["ISO 11898", "IEEE 802.3", "SAE J1939"],
        burden_holder="Vehicle Network Architect",
        adversary_position="Some implementations neglect security, exposing vehicles to cyber risks.",
        counter_arguments=[
            "Security breaches can compromise vehicle safety and user privacy.",
            "Incorporating security is essential despite added complexity."
        ],
        resolution_strategy="Adopt secure communication protocols with encryption and authentication, combined with continuous monitoring.",
        entity_scope="Vehicle Communication Networks",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO/SAE 21434 - Road Vehicles Cybersecurity Engineering"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Thermal Runaway Prevention",
        keywords=["thermal runaway", "battery safety", "temperature control", "fault detection", "fire prevention"],
        conclusion_template="Preventing thermal runaway in battery systems is critical to ensure vehicle safety and prevent catastrophic failures.",
        reasoning_framework=(
            "Thermal runaway occurs when exothermic reactions in battery cells lead to uncontrollable temperature rise. Prevention frameworks "
            "include temperature monitoring, early fault detection, and thermal management systems. The reasoning covers chemical stability, "
            "heat dissipation, and cell design. Safety mechanisms isolate faulty cells and trigger system shutdowns. Fire suppression systems "
            "may be integrated. Standards such as UL 2580 and UN 38.3 specify testing and design requirements. Risk assessments guide "
            "material selection and system architecture to minimize propagation. The framework also considers external factors such as "
            "collision impact and environmental conditions."
        ),
        key_factors=["temperature sensors", "fault isolation", "thermal management", "material stability", "fire suppression"],
        primary_authority=["UL 2580", "UN 38.3", "SAE J2464"],
        burden_holder="Battery Pack Designer",
        adversary_position="Cost constraints sometimes lead to reduced safety features.",
        counter_arguments=[
            "Compromising safety features increases risk of fire and liability.",
            "Investment in prevention reduces long-term costs and enhances reputation."
        ],
        resolution_strategy="Implement multi-layered safety systems validated by rigorous testing and certification.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="UL 2580 - Standard for Batteries for Use in Electric Vehicles"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Energy Storage System Design",
        keywords=["energy storage", "battery pack", "capacity", "voltage", "thermal management", "safety"],
        conclusion_template="Designing energy storage systems requires balancing capacity, voltage levels, safety, and thermal management to meet performance goals.",
        reasoning_framework=(
            "Energy storage systems (ESS) in electric vehicles consist of battery cells arranged to achieve desired voltage and capacity. "
            "The design framework includes cell chemistry selection, series-parallel configurations, and mechanical packaging. "
            "Thermal management ensures temperature uniformity and prevents hotspots. Safety features include overcurrent protection, "
            "fault detection, and containment structures. The reasoning involves trade-offs between energy density, weight, cost, and "
            "reliability. Standards such as IEC 62660 and SAE J2929 guide design and testing. Integration with vehicle control systems "
            "enables optimized charging and discharging profiles."
        ),
        key_factors=["cell chemistry", "pack configuration", "thermal uniformity", "safety mechanisms", "integration"],
        primary_authority=["IEC 62660", "SAE J2929", "UL 2580"],
        burden_holder="Energy Storage System Designer",
        adversary_position="Some designs prioritize capacity over safety margins.",
        counter_arguments=[
            "Ignoring safety compromises vehicle integrity and user safety.",
            "Balanced designs optimize performance and risk mitigation."
        ],
        resolution_strategy="Follow established standards and perform comprehensive validation testing.",
        entity_scope="Electric Vehicle Battery Packs",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 62660 - Secondary Lithium-Ion Cells for the Propulsion of Electric Road Vehicles"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Onboard Charger Design",
        keywords=["onboard charger", "AC/DC conversion", "charging efficiency", "thermal management", "power factor correction"],
        conclusion_template="Onboard charger designs must optimize AC/DC conversion efficiency, thermal management, and power quality to ensure reliable charging.",
        reasoning_framework=(
            "Onboard chargers convert AC grid power to DC for battery charging. The design framework includes selection of power electronics topologies, "
            "control algorithms for power factor correction, and thermal management to dissipate heat generated during conversion. "
            "Efficiency impacts charging time and energy consumption. The reasoning also involves electromagnetic compatibility (EMC) compliance, "
            "connector compatibility, and safety features such as ground fault detection. Standards like IEC 61851 and SAE J1772 specify requirements. "
            "Thermal simulations and hardware-in-the-loop testing validate performance under various operating conditions."
        ),
        key_factors=["power electronics topology", "control algorithms", "thermal design", "EMC compliance", "safety features"],
        primary_authority=["IEC 61851", "SAE J1772", "UL 2202"],
        burden_holder="Onboard Charger Manufacturer",
        adversary_position="Some designs compromise efficiency to reduce cost and size.",
        counter_arguments=[
            "Lower efficiency increases energy costs and thermal stress.",
            "Optimized designs improve user experience and system longevity."
        ],
        resolution_strategy="Employ advanced power electronics and control strategies validated through testing and certification.",
        entity_scope="Electric Vehicle Onboard Charging Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="UL 2202 - Standard for Electric Vehicle (EV) Charging System Equipment"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Wiring Harness Shielding",
        keywords=["wiring harness", "shielding", "EMI", "electromagnetic interference", "signal integrity", "noise reduction"],
        conclusion_template="Proper shielding of wiring harnesses is essential to minimize electromagnetic interference and maintain signal integrity.",
        reasoning_framework=(
            "Electric vehicles contain numerous electronic systems sensitive to electromagnetic interference (EMI). Shielding wiring harnesses "
            "reduces EMI emissions and susceptibility. The framework involves selecting appropriate shielding materials such as braided copper, "
            "foil, or conductive polymers. Shielding effectiveness depends on coverage, grounding, and connector design. The reasoning includes "
            "analysis of EMI sources, coupling mechanisms, and frequency ranges. Proper shielding enhances communication reliability and reduces "
            "diagnostic errors. Standards like CISPR 25 and ISO 11452 guide EMI control measures. Testing includes radiated and conducted emissions "
            "measurements."
        ),
        key_factors=["shielding materials", "coverage", "grounding", "connector design", "EMI testing"],
        primary_authority=["CISPR 25", "ISO 11452", "SAE J551"],
        burden_holder="Wiring Harness Designer",
        adversary_position="Cost pressures may lead to reduced shielding, risking EMI issues.",
        counter_arguments=[
            "Insufficient shielding causes system malfunctions and warranty claims.",
            "Investing in shielding improves overall vehicle reliability."
        ],
        resolution_strategy="Design wiring harnesses with appropriate shielding validated by EMI testing.",
        entity_scope="Electric Vehicle Wiring Systems",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="CISPR 25 - Radio Disturbance Characteristics for the Protection of Receivers Used on Board Vehicles"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Safety Disconnect Systems",
        keywords=["safety disconnect", "high voltage isolation", "emergency shutdown", "contactors", "fault protection"],
        conclusion_template="Safety disconnect systems provide critical high voltage isolation and emergency shutdown capabilities to protect users and service personnel.",
        reasoning_framework=(
            "Safety disconnect systems isolate high voltage circuits during maintenance or fault conditions. The framework includes mechanical "
            "contactors, relays, and interlocks designed to interrupt current flow safely. Emergency shutdown mechanisms enable rapid de-energization "
            "in accidents. The reasoning involves electrical arc suppression, contactor reliability, and fail-safe design principles. "
            "Standards such as ISO 6469 and SAE J1766 specify requirements for disconnect systems. The framework also covers diagnostic monitoring "
            "to detect contactor status and insulation faults. Proper design prevents unintended energization and ensures compliance with safety regulations."
        ),
        key_factors=["contactor design", "interlocks", "emergency shutdown", "diagnostics", "fail-safe operation"],
        primary_authority=["ISO 6469", "SAE J1766", "UL 2231"],
        burden_holder="Vehicle Electrical System Designer",
        adversary_position="Some designs minimize disconnect features to reduce cost and complexity.",
        counter_arguments=[
            "Inadequate disconnect systems pose serious safety risks.",
            "Comprehensive disconnect designs are mandated by safety standards."
        ],
        resolution_strategy="Implement robust disconnect systems with redundant safety features and continuous monitoring.",
        entity_scope="Electric Vehicle High Voltage Systems",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="UL 2231 - Standard for Personnel Protection Systems for Electric Vehicle Supply Circuits"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery State-of-Charge Estimation",
        keywords=["state-of-charge", "SOC", "battery monitoring", "estimation algorithms", "accuracy", "battery management"],
        conclusion_template="Accurate state-of-charge (SOC) estimation is fundamental for battery management and vehicle range prediction.",
        reasoning_framework=(
            "SOC estimation algorithms integrate voltage, current, temperature, and historical usage data to provide real-time battery charge status. "
            "The framework includes coulomb counting, open-circuit voltage methods, and model-based estimations such as Kalman filtering. "
            "Accurate SOC estimation informs energy management, charging strategies, and user information systems. The reasoning considers "
            "battery aging effects, measurement noise, and environmental influences. Validation involves laboratory testing and field data analysis. "
            "The framework integrates with battery management systems to optimize performance and safety."
        ),
        key_factors=["voltage measurement", "current integration", "temperature compensation", "algorithm selection", "validation"],
        primary_authority=["SAE J2929", "IEC 62660", "UL 2580"],
        burden_holder="Battery Management System Developer",
        adversary_position="Simplified SOC methods may reduce computational load but sacrifice accuracy.",
        counter_arguments=[
            "Inaccurate SOC leads to range anxiety and potential battery damage.",
            "Advanced algorithms improve reliability and user confidence."
        ],
        resolution_strategy="Implement validated SOC estimation algorithms with adaptive calibration.",
        entity_scope="Battery Management Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="SAE J2929 - Electric Vehicle Battery State-of-Charge Estimation"
    ),
    DoctrineBlock(
        topic="Electric Vehicle High Voltage Cable Routing",
        keywords=["high voltage", "cable routing", "protection", "segregation", "mechanical stress", "thermal considerations"],
        conclusion_template="High voltage cable routing must ensure protection from mechanical damage, thermal exposure, and electromagnetic interference.",
        reasoning_framework=(
            "Routing high voltage cables requires adherence to safety and performance criteria. The framework includes physical segregation from low voltage "
            "circuits to prevent interference and shock hazards. Protection against abrasion, vibration, and impact is essential. Thermal considerations "
            "avoid proximity to heat sources that could degrade insulation. Routing paths must facilitate maintenance access and comply with vehicle packaging "
            "constraints. Standards such as SAE J1128 and ISO 6469 provide guidelines. The reasoning also involves electromagnetic compatibility and "
            "fire resistance. Validation includes mechanical testing and thermal cycling."
        ),
        key_factors=["physical segregation", "mechanical protection", "thermal exposure", "EMC", "maintenance access"],
        primary_authority=["SAE J1128", "ISO 6469", "UL 94"],
        burden_holder="Vehicle Electrical System Designer",
        adversary_position="Cost and space constraints sometimes lead to compromised routing practices.",
        counter_arguments=[
            "Poor routing increases risk of cable damage and electrical faults.",
            "Proper routing enhances safety and system longevity."
        ],
        resolution_strategy="Design routing plans per standards with thorough validation and quality control.",
        entity_scope="Electric Vehicle High Voltage Wiring",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="SAE J1128 - Low Voltage Primary Cable"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Insulation Monitoring Systems",
        keywords=["insulation monitoring", "leakage current", "fault detection", "high voltage", "safety"],
        conclusion_template="Insulation monitoring systems detect leakage currents to prevent electric shock hazards and ensure high voltage system integrity.",
        reasoning_framework=(
            "Insulation monitoring systems continuously measure insulation resistance and detect leakage currents between high voltage conductors and chassis ground. "
            "The framework includes sensor placement, measurement techniques, and alarm thresholds. Early detection of insulation faults enables preventive maintenance "
            "and reduces risk of electric shock. Standards such as ISO 6469 and IEC 61557 guide design and testing. The reasoning involves analysis of fault currents, "
            "environmental influences, and system response. Integration with vehicle control units enables protective actions upon fault detection."
        ),
        key_factors=["insulation resistance", "leakage current measurement", "sensor placement", "alarm thresholds", "system integration"],
        primary_authority=["ISO 6469", "IEC 61557", "SAE J1766"],
        burden_holder="Vehicle Electrical System Designer",
        adversary_position="Some systems omit insulation monitoring to reduce cost.",
        counter_arguments=[
            "Lack of monitoring increases risk of undetected faults and accidents.",
            "Insulation monitoring is a regulatory requirement in many jurisdictions."
        ],
        resolution_strategy="Implement continuous insulation monitoring with automatic fault response.",
        entity_scope="Electric Vehicle High Voltage Systems",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="IEC 61557 - Electrical Safety in Low Voltage Distribution Systems"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Power Distribution Architecture",
        keywords=["power distribution", "architecture", "busbars", "fuses", "contactors", "modularity"],
        conclusion_template="A modular and robust power distribution architecture enhances reliability and maintainability of electric vehicle electrical systems.",
        reasoning_framework=(
            "Power distribution architectures organize the flow of electrical energy from the battery to various subsystems. The framework includes "
            "selection of busbars, fuses, contactors, and wiring harnesses to handle current loads safely. Modularity facilitates assembly, diagnostics, "
            "and repairs. The reasoning involves fault current analysis, thermal management, and electromagnetic compatibility. Standards such as SAE J1939 "
            "and ISO 26262 influence design. Redundancy and isolation features improve fault tolerance. The architecture must accommodate future upgrades "
            "and scalability."
        ),
        key_factors=["current rating", "modularity", "fault protection", "thermal considerations", "scalability"],
        primary_authority=["SAE J1939", "ISO 26262", "UL 2231"],
        burden_holder="Vehicle Electrical System Architect",
        adversary_position="Simplified architectures may reduce cost but limit flexibility and safety.",
        counter_arguments=[
            "Robust architectures reduce downtime and improve safety.",
            "Modularity supports efficient maintenance and upgrades."
        ],
        resolution_strategy="Design architectures with modular components and comprehensive protection validated by simulations and testing.",
        entity_scope="Electric Vehicle Electrical Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ISO 26262 - Functional Safety of Electrical/Electronic Systems"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Fault Diagnosis Techniques",
        keywords=["fault diagnosis", "diagnostics", "OBD", "sensor data", "fault codes", "predictive maintenance"],
        conclusion_template="Advanced fault diagnosis techniques enable early detection and resolution of electrical system issues, improving vehicle reliability.",
        reasoning_framework=(
            "Fault diagnosis in electric vehicles utilizes onboard diagnostics (OBD), sensor data analysis, and fault code interpretation. "
            "The framework includes real-time monitoring of voltage, current, temperature, and communication signals. Diagnostic algorithms "
            "identify anomalies and isolate fault locations. Predictive maintenance leverages historical data and machine learning to anticipate "
            "failures. Standards such as SAE J1979 and ISO 14229 guide diagnostic communication protocols. The reasoning involves balancing "
            "false positives and detection sensitivity. Integration with vehicle telematics supports remote diagnostics and updates."
        ),
        key_factors=["sensor accuracy", "diagnostic algorithms", "communication protocols", "predictive analytics", "false positive management"],
        primary_authority=["SAE J1979", "ISO 14229", "ISO 26262"],
        burden_holder="Vehicle Diagnostics System Developer",
        adversary_position="Basic diagnostics may miss early fault indicators, leading to unexpected failures.",
        counter_arguments=[
            "Comprehensive diagnostics reduce downtime and repair costs.",
            "Advanced techniques improve safety and user satisfaction."
        ],
        resolution_strategy="Implement multi-layered diagnostics combining real-time monitoring and predictive analytics.",
        entity_scope="Electric Vehicle Electrical Systems",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="ISO 14229 - Unified Diagnostic Services"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Electromagnetic Compatibility (EMC)",
        keywords=["EMC", "electromagnetic interference", "emissions", "susceptibility", "shielding", "filtering"],
        conclusion_template="Ensuring electromagnetic compatibility is essential to prevent interference between vehicle electronic systems and external devices.",
        reasoning_framework=(
            "EMC involves controlling emissions and susceptibility of electronic systems to electromagnetic disturbances. The framework includes "
            "designing shielding, filtering, grounding, and layout strategies to minimize interference. Testing per CISPR and ISO standards "
            "validates compliance. The reasoning considers conducted and radiated emissions, transient immunity, and harmonic distortion. "
            "Proper EMC design prevents malfunctions, data corruption, and regulatory non-compliance. The framework integrates with wiring harness "
            "design, power electronics, and communication networks."
        ),
        key_factors=["shielding", "filtering", "grounding", "layout", "testing"],
        primary_authority=["CISPR 25", "ISO 11452", "SAE J551"],
        burden_holder="Vehicle Electrical System Designer",
        adversary_position="Neglecting EMC increases risk of system failures and regulatory penalties.",
        counter_arguments=[
            "EMC compliance is mandatory for vehicle certification.",
            "Investing in EMC design improves reliability and user experience."
        ],
        resolution_strategy="Incorporate EMC considerations early in design with iterative testing and validation.",
        entity_scope="Electric Vehicle Electronic Systems",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="CISPR 25 - Radio Disturbance Characteristics for the Protection of Receivers"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Thermal Runaway Detection",
        keywords=["thermal runaway", "detection", "temperature sensors", "fault monitoring", "early warning"],
        conclusion_template="Early detection of thermal runaway conditions is critical to initiate protective actions and prevent escalation.",
        reasoning_framework=(
            "Thermal runaway detection relies on temperature sensors, voltage monitoring, and chemical sensors to identify abnormal conditions. "
            "The framework includes threshold-based alarms, trend analysis, and integration with battery management systems. Early warning enables "
            "activation of cooling systems, isolation of affected cells, and emergency shutdown. The reasoning covers sensor placement, response "
            "time, and false alarm mitigation. Standards such as UL 2580 and SAE J2464 provide guidance. The framework also considers integration "
            "with vehicle safety systems and fire suppression."
        ),
        key_factors=["temperature monitoring", "voltage anomalies", "sensor placement", "alarm thresholds", "response protocols"],
        primary_authority=["UL 2580", "SAE J2464", "ISO 26262"],
        burden_holder="Battery Management System Developer",
        adversary_position="Limited sensor deployment may delay detection and response.",
        counter_arguments=[
            "Comprehensive detection reduces risk of catastrophic failure.",
            "Early intervention improves safety and reduces damage."
        ],
        resolution_strategy="Deploy multi-sensor arrays with intelligent monitoring algorithms and fail-safe responses.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="UL 2580 - Battery Safety Standards"
    ),
    DoctrineBlock(
        topic="Electric Vehicle High Voltage Connector Standards",
        keywords=["high voltage", "connectors", "standards", "safety", "durability", "sealing"],
        conclusion_template="Compliance with high voltage connector standards ensures safe, reliable, and durable electrical connections in electric vehicles.",
        reasoning_framework=(
            "High voltage connectors must provide secure electrical contact, insulation, and environmental sealing. The framework includes "
            "mechanical design for vibration resistance, thermal stability, and ease of assembly. Standards such as IEC 62196 and SAE J1772 "
            "specify dimensional, electrical, and safety requirements. The reasoning involves contact resistance, current rating, and ingress "
            "protection. Proper connector design prevents arcing, corrosion, and accidental disconnection. Testing includes mechanical cycling, "
            "environmental exposure, and electrical performance."
        ),
        key_factors=["contact reliability", "insulation", "sealing", "mechanical robustness", "standard compliance"],
        primary_authority=["IEC 62196", "SAE J1772", "UL 2231"],
        burden_holder="Connector Manufacturer",
        adversary_position="Non-compliant connectors risk safety and interoperability issues.",
        counter_arguments=[
            "Standards compliance is critical for vehicle certification and user safety.",
            "High-quality connectors reduce maintenance and failure rates."
        ],
        resolution_strategy="Design and test connectors per international standards with robust quality control.",
        entity_scope="Electric Vehicle High Voltage Connectors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 62196 - Plugs, Socket-Outlets, Vehicle Connectors and Vehicle Inlets"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Cell Balancing Techniques",
        keywords=["battery cell balancing", "passive balancing", "active balancing", "state-of-charge equalization", "battery longevity"],
        conclusion_template="Effective battery cell balancing techniques improve battery pack performance and extend service life.",
        reasoning_framework=(
            "Cell balancing equalizes the state-of-charge among battery cells to prevent overcharge and deep discharge of individual cells. "
            "Passive balancing dissipates excess energy as heat through resistors, while active balancing redistributes charge between cells. "
            "The framework includes monitoring cell voltages and temperatures, control algorithms, and hardware implementation. "
            "Balancing improves capacity utilization and reduces degradation. The reasoning considers energy efficiency, complexity, and cost. "
            "Standards such as IEC 62660 provide guidance. Validation includes cycle testing and performance monitoring."
        ),
        key_factors=["voltage monitoring", "balancing method", "energy efficiency", "control algorithms", "validation"],
        primary_authority=["IEC 62660", "SAE J2929", "UL 2580"],
        burden_holder="Battery Management System Developer",
        adversary_position="Passive balancing is simpler but less efficient than active methods.",
        counter_arguments=[
            "Active balancing increases complexity and cost but enhances performance.",
            "Choice depends on application requirements and cost-benefit analysis."
        ],
        resolution_strategy="Select balancing techniques appropriate to battery chemistry and application, validated by testing.",
        entity_scope="Battery Management Systems",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="IEC 62660 - Secondary Lithium-Ion Cells for Electric Vehicles"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Powertrain Control Integration",
        keywords=["powertrain", "control integration", "motor control", "battery management", "vehicle dynamics"],
        conclusion_template="Integrated powertrain control enhances vehicle performance, efficiency, and safety through coordinated management of subsystems.",
        reasoning_framework=(
            "Powertrain control integration involves synchronizing motor controllers, battery management systems, and vehicle dynamics controls. "
            "The framework includes real-time data exchange, control algorithms for torque delivery, regenerative braking, and thermal management. "
            "Integration improves energy efficiency, drivability, and fault tolerance. The reasoning covers communication protocols, control hierarchies, "
            "and safety interlocks. Standards such as ISO 26262 and SAE J1939 influence design. Validation includes hardware-in-the-loop simulation and road testing."
        ),
        key_factors=["real-time communication", "control algorithms", "fault tolerance", "thermal management", "safety interlocks"],
        primary_authority=["ISO 26262", "SAE J1939", "SAE J2907"],
        burden_holder="Vehicle Control System Integrator",
        adversary_position="Disjointed control systems reduce performance and complicate diagnostics.",
        counter_arguments=[
            "Integrated control improves efficiency and user experience.",
            "Modular yet coordinated systems balance complexity and maintainability."
        ],
        resolution_strategy="Develop integrated control architectures with standardized interfaces and rigorous validation.",
        entity_scope="Electric Vehicle Powertrain Systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO 26262 - Functional Safety"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Mechanical Design",
        keywords=["battery pack", "mechanical design", "structural integrity", "thermal management", "vibration resistance"],
        conclusion_template="Mechanical design of battery packs must ensure structural integrity, effective thermal management, and resistance to vibration and impact.",
        reasoning_framework=(
            "Battery pack mechanical design involves enclosure materials, cell mounting, and thermal interface components. The framework ensures "
            "protection against mechanical shocks, vibration, and environmental exposure. Thermal management integration includes heat sinks, cooling "
            "channels, and insulation. The reasoning considers crashworthiness, manufacturability, and serviceability. Standards such as SAE J2929 "
            "and UN ECE R100 guide design and testing. Validation includes mechanical shock, vibration, and thermal cycling tests."
        ),
        key_factors=["enclosure materials", "cell mounting", "thermal interfaces", "vibration resistance", "crashworthiness"],
        primary_authority=["SAE J2929", "UN ECE R100", "ISO 6469"],
        burden_holder="Battery Pack Mechanical Designer",
        adversary_position="Lightweight designs may compromise mechanical protection.",
        counter_arguments=[
            "Insufficient mechanical design risks cell damage and safety incidents.",
            "Balanced design optimizes weight and protection."
        ],
        resolution_strategy="Employ robust mechanical designs validated by comprehensive testing.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="UN ECE R100 - Safety Specifications for Electric Vehicle Batteries"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Fire Suppression Systems",
        keywords=["fire suppression", "battery pack", "thermal runaway", "safety systems", "extinguishing agents"],
        conclusion_template="Fire suppression systems integrated within battery packs mitigate risks of thermal runaway propagation and enhance safety.",
        reasoning_framework=(
            "Fire suppression systems detect and extinguish fires originating within battery packs. The framework includes detection sensors, "
            "extinguishing agents such as inert gases or aerosols, and activation mechanisms. The reasoning involves rapid response to thermal "
            "runaway events, containment of fire spread, and minimization of collateral damage. Integration with vehicle safety systems enables "
            "coordinated emergency responses. Standards and guidelines such as NFPA 855 influence design. Validation includes fire testing and "
            "system reliability assessments."
        ),
        key_factors=["fire detection", "extinguishing agents", "activation mechanisms", "system integration", "reliability"],
        primary_authority=["NFPA 855", "UL 9540", "SAE J2464"],
        burden_holder="Battery Pack Safety System Designer",
        adversary_position="Fire suppression adds weight and complexity, leading some to omit it.",
        counter_arguments=[
            "Omission increases risk of catastrophic fire and liability.",
            "Safety systems protect users and assets, justifying added complexity."
        ],
        resolution_strategy="Incorporate fire suppression systems designed and tested per industry standards.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NFPA 855 - Standard for the Installation of Stationary Energy Storage Systems"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Ventilation Design",
        keywords=["battery pack", "ventilation", "thermal management", "gas release", "safety"],
        conclusion_template="Battery pack ventilation design manages heat and safely vents gases generated during abnormal conditions.",
        reasoning_framework=(
            "Battery packs may release gases during thermal events or faults. Ventilation design ensures controlled release to prevent pressure buildup "
            "and accumulation of flammable gases. The framework includes vent placement, flow paths, and flame arrestors. Thermal management integrates "
            "ventilation with cooling systems. The reasoning covers chemical properties of gases, environmental exposure, and safety regulations. "
            "Standards such as UL 2580 and UN ECE R100 provide guidance. Validation includes pressure testing and gas detection."
        ),
        key_factors=["vent placement", "flow control", "flame arrestors", "thermal integration", "regulatory compliance"],
        primary_authority=["UL 2580", "UN ECE R100", "SAE J2929"],
        burden_holder="Battery Pack Mechanical Designer",
        adversary_position="Sealed designs without ventilation risk pressure buildup and explosion.",
        counter_arguments=[
            "Proper ventilation enhances safety and prevents catastrophic failures.",
            "Design must balance sealing for environmental protection with venting needs."
        ],
        resolution_strategy="Design ventilation systems per standards with rigorous testing and validation.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="UL 2580 - Battery Safety Standards"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Thermal Interface Materials",
        keywords=["thermal interface", "battery pack", "heat transfer", "materials", "thermal conductivity"],
        conclusion_template="Selection of appropriate thermal interface materials (TIM) enhances heat transfer and battery pack thermal management.",
        reasoning_framework=(
            "Thermal interface materials fill gaps between battery cells and cooling components to improve heat conduction. The framework includes "
            "material selection based on thermal conductivity, electrical insulation, mechanical compliance, and durability. The reasoning covers "
            "operating temperature ranges, chemical compatibility, and aging effects. Effective TIM reduces hotspots and improves battery performance. "
            "Standards and testing protocols evaluate thermal resistance and mechanical properties."
        ),
        key_factors=["thermal conductivity", "electrical insulation", "mechanical compliance", "durability", "aging"],
        primary_authority=["ASTM D5470", "IEC 62660", "SAE J2929"],
        burden_holder="Battery Pack Designer",
        adversary_position="Inadequate TIM selection leads to poor thermal management and reduced battery life.",
        counter_arguments=[
            "Investing in high-quality TIM improves safety and performance.",
            "Material selection must consider application-specific requirements."
        ],
        resolution_strategy="Select and validate TIM based on comprehensive thermal and mechanical testing.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="ASTM D5470 - Thermal Transmission Properties"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Monitoring Systems",
        keywords=["battery monitoring", "sensors", "data acquisition", "fault detection", "state-of-health"],
        conclusion_template="Comprehensive battery pack monitoring systems enable real-time assessment of battery condition and early fault detection.",
        reasoning_framework=(
            "Battery pack monitoring systems collect data from voltage, current, temperature, and pressure sensors. The framework includes data acquisition, "
            "signal processing, and integration with battery management systems. Monitoring enables state-of-health (SOH) estimation, fault detection, "
            "and predictive maintenance. The reasoning involves sensor accuracy, data fusion, and communication protocols. Standards such as SAE J2929 "
            "guide design. Validation includes sensor calibration and system reliability testing."
        ),
        key_factors=["sensor selection", "data accuracy", "fault detection algorithms", "SOH estimation", "system integration"],
        primary_authority=["SAE J2929", "IEC 62660", "UL 2580"],
        burden_holder="Battery Management System Developer",
        adversary_position="Limited monitoring reduces fault detection capability.",
        counter_arguments=[
            "Comprehensive monitoring improves safety and battery longevity.",
            "Investment in monitoring reduces unexpected failures."
        ],
        resolution_strategy="Implement multi-sensor monitoring with robust data processing and integration.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J2929 - Battery Monitoring Systems"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Electrical Protection",
        keywords=["electrical protection", "fuses", "circuit breakers", "current limiting", "fault isolation"],
        conclusion_template="Electrical protection devices safeguard battery packs from overcurrent and short circuit conditions to prevent damage and hazards.",
        reasoning_framework=(
            "Protection devices such as fuses and circuit breakers interrupt current flow during fault conditions. The framework includes selection "
            "based on current ratings, response times, and coordination with other protection elements. The reasoning covers fault current analysis, "
            "thermal effects, and device reliability. Proper protection prevents battery damage, fire, and system failures. Standards such as UL 248 "
            "and IEC 60269 guide device selection and testing."
        ),
        key_factors=["current rating", "response time", "coordination", "device reliability", "testing"],
        primary_authority=["UL 248", "IEC 60269", "SAE J1766"],
        burden_holder="Battery Pack Designer",
        adversary_position="Undersized protection devices risk damage and safety incidents.",
        counter_arguments=[
            "Properly sized protection devices ensure safety and compliance.",
            "Investment in protection reduces warranty and liability costs."
        ],
        resolution_strategy="Select and test protection devices per standards with system-level coordination.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="UL 248 - Fuses"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Electrical Connections",
        keywords=["electrical connections", "battery pack", "busbars", "connectors", "contact resistance", "reliability"],
        conclusion_template="Reliable electrical connections within battery packs are essential for efficient power delivery and safety.",
        reasoning_framework=(
            "Electrical connections include busbars, connectors, and terminals that link battery cells and modules. The framework involves "
            "material selection for conductivity and corrosion resistance, mechanical design for vibration resistance, and contact resistance minimization. "
            "The reasoning covers thermal effects, assembly processes, and maintenance considerations. Standards such as SAE J1128 and UL 2231 "
            "influence design. Validation includes electrical resistance measurements and mechanical cycling."
        ),
        key_factors=["material selection", "contact resistance", "mechanical robustness", "corrosion resistance", "assembly"],
        primary_authority=["SAE J1128", "UL 2231", "ISO 6469"],
        burden_holder="Battery Pack Designer",
        adversary_position="Poor connections increase losses and risk overheating.",
        counter_arguments=[
            "High-quality connections improve efficiency and safety.",
            "Proper design reduces maintenance and failure rates."
        ],
        resolution_strategy="Design and validate connections with rigorous testing and quality control.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="UL 2231 - Personnel Protection Systems"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Environmental Protection",
        keywords=["environmental protection", "battery pack", "sealing", "moisture ingress", "dust", "corrosion"],
        conclusion_template="Battery packs require robust environmental protection to prevent moisture ingress, dust contamination, and corrosion.",
        reasoning_framework=(
            "Environmental protection involves sealing enclosures against water, dust, and contaminants. The framework includes gasket design, "
            "material selection, and ingress protection ratings such as IP67. The reasoning covers thermal expansion, chemical resistance, and "
            "mechanical stresses. Protection prevents electrical faults, corrosion, and premature aging. Standards such as IEC 60529 guide ingress "
            "protection classification. Validation includes environmental testing under temperature, humidity, and vibration."
        ),
        key_factors=["sealing", "material resistance", "ingress protection rating", "thermal expansion", "testing"],
        primary_authority=["IEC 60529", "SAE J2929", "UL 2580"],
        burden_holder="Battery Pack Mechanical Designer",
        adversary_position="Cost pressures may reduce sealing quality.",
        counter_arguments=[
            "Inadequate protection leads to failures and safety risks.",
            "Proper sealing extends battery life and reliability."
        ],
        resolution_strategy="Design enclosures with appropriate sealing and validate through environmental testing.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="IEC 60529 - Degrees of Protection Provided by Enclosures"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Thermal Runaway Propagation Mitigation",
        keywords=["thermal runaway", "propagation", "mitigation", "cell separation", "fire barriers", "safety"],
        conclusion_template="Mitigation of thermal runaway propagation within battery packs is essential to limit damage and enhance safety.",
        reasoning_framework=(
            "Thermal runaway propagation occurs when heat and gases from a failing cell ignite neighboring cells. The framework includes "
            "physical barriers, cell spacing, and fire-resistant materials to prevent spread. The reasoning covers thermal conductivity, "
            "mechanical design, and chemical compatibility. Safety standards such as UL 2580 and UN ECE R100 provide guidance. Validation "
            "includes thermal propagation testing and fire resistance assessments."
        ),
        key_factors=["cell spacing", "fire barriers", "material selection", "thermal conductivity", "testing"],
        primary_authority=["UL 2580", "UN ECE R100", "SAE J2929"],
        burden_holder="Battery Pack Designer",
        adversary_position="Compact designs may reduce spacing and barriers, increasing propagation risk.",
        counter_arguments=[
            "Proper mitigation reduces fire risk and enhances occupant safety.",
            "Design must balance packaging constraints with safety requirements."
        ],
        resolution_strategy="Incorporate propagation mitigation features validated by rigorous testing.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="UL 2580 - Battery Safety Standards"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack State-of-Health Estimation",
        keywords=["state-of-health", "SOH", "battery degradation", "capacity fade", "internal resistance", "monitoring"],
        conclusion_template="Accurate state-of-health (SOH) estimation enables assessment of battery degradation and informs maintenance decisions.",
        reasoning_framework=(
            "SOH estimation uses parameters such as capacity fade, internal resistance increase, and self-discharge rates. The framework "
            "includes data collection from cycling tests, impedance spectroscopy, and model-based analysis. Accurate SOH informs warranty "
            "management and replacement scheduling. The reasoning considers environmental factors and usage patterns. Validation involves "
            "long-term testing and correlation with field data."
        ),
        key_factors=["capacity measurement", "internal resistance", "data analysis", "modeling", "validation"],
        primary_authority=["SAE J2929", "IEC 62660", "UL 2580"],
        burden_holder="Battery Management System Developer",
        adversary_position="Simplified SOH methods may misrepresent battery condition.",
        counter_arguments=[
            "Accurate SOH improves safety and cost management.",
            "Advanced methods require investment but yield better insights."
        ],
        resolution_strategy="Implement validated SOH estimation algorithms with continuous calibration.",
        entity_scope="Battery Management Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2929 - Battery SOH Estimation"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Thermal Runaway Venting",
        keywords=["thermal runaway", "venting", "pressure relief", "gas release", "safety"],
        conclusion_template="Effective venting systems manage pressure and gas release during thermal runaway events to prevent enclosure rupture and fire spread.",
        reasoning_framework=(
            "Venting systems provide controlled pathways for gases generated during thermal runaway to escape safely. The framework includes "
            "pressure relief valves, vent channels, and flame arrestors. The reasoning covers gas composition, pressure dynamics, and enclosure "
            "integrity. Proper venting reduces explosion risk and facilitates fire suppression. Standards such as UL 2580 and UN ECE R100 "
            "guide design and testing."
        ),
        key_factors=["pressure relief", "vent design", "flame arrestors", "gas composition", "testing"],
        primary_authority=["UL 2580", "UN ECE R100", "SAE J2929"],
        burden_holder="Battery Pack Mechanical Designer",
        adversary_position="Sealed packs without venting risk catastrophic failure.",
        counter_arguments=[
            "Venting enhances safety and compliance with regulations.",
            "Design must balance sealing with venting requirements."
        ],
        resolution_strategy="Incorporate venting systems validated by pressure and fire testing.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="UL 2580 - Battery Safety Standards"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Cooling System Integration",
        keywords=["battery cooling", "thermal management", "liquid cooling", "air cooling", "system integration"],
        conclusion_template="Integrating battery cooling systems with vehicle thermal management optimizes temperature control and energy efficiency.",
        reasoning_framework=(
            "Battery cooling systems use liquid or air to maintain optimal operating temperatures. Integration with vehicle HVAC and coolant circuits "
            "enhances efficiency and reduces component redundancy. The framework involves thermal modeling, coolant flow control, and sensor feedback. "
            "The reasoning includes heat exchanger design, pump control, and fault detection. Standards such as SAE J2954 influence design. Validation "
            "includes thermal cycling and system performance testing."
        ),
        key_factors=["coolant type", "flow control", "thermal modeling", "sensor integration", "fault detection"],
        primary_authority=["SAE J2954", "ISO 6469", "UL 2580"],
        burden_holder="Vehicle Thermal System Designer",
        adversary_position="Isolated cooling systems may be less efficient and increase weight.",
        counter_arguments=[
            "Integrated systems improve thermal control and reduce energy consumption.",
            "Coordination reduces complexity and maintenance."
        ],
        resolution_strategy="Design integrated cooling systems validated through simulation and testing.",
        entity_scope="Electric Vehicle Thermal Management",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2954 - Wireless Power Transfer for Electric Vehicles"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Safety Testing",
        keywords=["battery safety", "testing", "abuse tests", "thermal runaway", "mechanical impact", "electrical abuse"],
        conclusion_template="Comprehensive safety testing of battery packs ensures compliance with standards and validates design robustness.",
        reasoning_framework=(
            "Safety testing includes mechanical impact, thermal abuse, electrical overcharge, and short circuit tests. The framework follows "
            "standards such as UL 2580, UN 38.3, and SAE J2464. Testing simulates real-world abuse conditions to evaluate pack response and "
            "safety features. The reasoning covers test setup, pass/fail criteria, and data analysis. Results inform design improvements and "
            "certification."
        ),
        key_factors=["mechanical impact", "thermal abuse", "electrical abuse", "test protocols", "data analysis"],
        primary_authority=["UL 2580", "UN 38.3", "SAE J2464"],
        burden_holder="Battery Pack Manufacturer",
        adversary_position="Inadequate testing risks undetected safety issues.",
        counter_arguments=[
            "Thorough testing prevents failures and liability.",
            "Compliance is mandatory for market access."
        ],
        resolution_strategy="Conduct all required tests per standards with detailed documentation.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="UL 2580 - Battery Safety Standards"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Maintenance Procedures",
        keywords=["battery maintenance", "inspection", "cleaning", "fault detection", "serviceability"],
        conclusion_template="Regular maintenance procedures ensure battery pack reliability, safety, and longevity.",
        reasoning_framework=(
            "Maintenance includes visual inspections, cleaning of connectors, checking for corrosion, and diagnostic testing. The framework "
            "involves safety protocols for high voltage handling, use of appropriate tools, and documentation. The reasoning covers fault "
            "identification, preventive measures, and replacement criteria. Standards and manufacturer guidelines provide procedural details."
        ),
        key_factors=["inspection", "cleaning", "diagnostics", "safety protocols", "documentation"],
        primary_authority=["SAE J2929", "ISO 6469", "UL 2580"],
        burden_holder="Service Personnel",
        adversary_position="Neglecting maintenance increases failure risk and safety hazards.",
        counter_arguments=[
            "Regular maintenance reduces downtime and extends battery life.",
            "Proper training and procedures ensure safety."
        ],
        resolution_strategy="Implement scheduled maintenance programs with trained personnel and standardized procedures.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="SAE J2929 - Battery Maintenance Guidelines"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack End-of-Life Management",
        keywords=["battery end-of-life", "recycling", "disposal", "second life", "environmental impact"],
        conclusion_template="Effective end-of-life management of battery packs minimizes environmental impact and recovers valuable materials.",
        reasoning_framework=(
            "End-of-life management includes recycling, repurposing for second life applications, and safe disposal. The framework involves "
            "collection logistics, disassembly, material recovery processes, and regulatory compliance. The reasoning covers environmental "
            "impact assessments, economic viability, and safety considerations. Standards and regulations such as EU Battery Directive guide "
            "practices."
        ),
        key_factors=["collection", "disassembly", "material recovery", "regulatory compliance", "environmental impact"],
        primary_authority=["EU Battery Directive", "IEC 62933", "SAE J2929"],
        burden_holder="Battery Pack Manufacturer and Recycling Entities",
        adversary_position="Improper disposal causes environmental harm and regulatory penalties.",
        counter_arguments=[
            "Responsible management supports sustainability and regulatory compliance.",
            "Second life applications extend resource utilization."
        ],
        resolution_strategy="Develop comprehensive end-of-life programs aligned with regulations and industry best practices.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="EU Battery Directive 2006/66/EC"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Software Update Management",
        keywords=["software update", "battery management", "firmware", "security", "OTA"],
        conclusion_template="Secure and reliable software update management is essential for maintaining battery management system functionality and security.",
        reasoning_framework=(
            "Software updates for battery management systems improve functionality, fix bugs, and enhance security. The framework includes "
            "over-the-air (OTA) update mechanisms, authentication, and rollback capabilities. The reasoning covers update integrity, failure "
            "recovery, and user notification. Security protocols prevent unauthorized access and tampering. Standards such as ISO/SAE 21434 "
            "guide cybersecurity aspects."
        ),
        key_factors=["OTA mechanisms", "authentication", "rollback", "security", "user notification"],
        primary_authority=["ISO/SAE 21434", "SAE J3061", "UL 2900"],
        burden_holder="Vehicle Software Development Team",
        adversary_position="Insecure update processes expose vehicles to cyber threats.",
        counter_arguments=[
            "Robust update management protects vehicle safety and data integrity.",
            "Security measures are critical despite added complexity."
        ],
        resolution_strategy="Implement secure update frameworks with comprehensive testing and monitoring.",
        entity_scope="Battery Management Systems",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="ISO/SAE 21434 - Road Vehicles Cybersecurity"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Thermal Runaway Containment",
        keywords=["thermal runaway", "containment", "fire barriers", "enclosure design", "safety"],
        conclusion_template="Thermal runaway containment strategies limit fire spread and protect vehicle occupants and components.",
        reasoning_framework=(
            "Containment involves designing battery enclosures with fire-resistant materials and structural barriers to isolate thermal events. "
            "The framework includes material selection, compartmentalization, and integration with fire suppression systems. The reasoning covers "
            "thermal insulation, mechanical strength, and regulatory compliance. Validation includes fire testing and mechanical impact assessments."
        ),
        key_factors=["fire-resistant materials", "compartmentalization", "thermal insulation", "mechanical strength", "testing"],
        primary_authority=["UL 2580", "UN ECE R100", "NFPA 855"],
        burden_holder="Battery Pack Mechanical Designer",
        adversary_position="Compact designs may reduce containment effectiveness.",
        counter_arguments=[
            "Containment is critical for occupant safety and regulatory compliance.",
            "Design must balance packaging constraints with safety."
        ],
        resolution_strategy="Incorporate containment features validated by rigorous testing and certification.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="UL 2580 - Battery Safety Standards"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Electrical Isolation Testing",
        keywords=["electrical isolation", "high voltage testing", "insulation resistance", "safety verification"],
        conclusion_template="Electrical isolation testing verifies the integrity of insulation and safety of high voltage battery systems.",
        reasoning_framework=(
            "Isolation testing measures insulation resistance and dielectric strength to ensure no unintended current paths exist. The framework "
            "includes test voltage application, measurement techniques, and pass/fail criteria. The reasoning covers test frequency, environmental "
            "conditions, and safety protocols. Standards such as IEC 6469 and UL 2231 guide testing. Regular testing detects insulation degradation "
            "and prevents electric shock hazards."
        ),
        key_factors=["test voltage", "measurement accuracy", "environmental conditions", "pass/fail criteria", "safety protocols"],
        primary_authority=["IEC 6469", "UL 2231", "SAE J1766"],
        burden_holder="Vehicle Electrical System Tester",
        adversary_position="Skipping isolation testing risks undetected insulation failures.",
        counter_arguments=[
            "Regular testing is essential for safety and regulatory compliance.",
            "Early detection prevents accidents and costly repairs."
        ],
        resolution_strategy="Implement scheduled isolation testing with qualified personnel and calibrated equipment.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="IEC 6469 - Safety Specifications for Electric Vehicles"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Thermal Management System Redundancy",
        keywords=["thermal management", "redundancy", "fault tolerance", "cooling system", "safety"],
        conclusion_template="Redundancy in battery thermal management systems enhances fault tolerance and vehicle safety.",
        reasoning_framework=(
            "Redundant cooling circuits, sensors, and control units ensure continued thermal management in case of component failure. The framework "
            "includes fault detection, automatic switchover, and system diagnostics. The reasoning covers failure modes, reliability analysis, and "
            "safety standards such as ISO 26262. Redundancy prevents thermal runaway and extends battery life. Validation includes fault injection "
            "testing and system monitoring."
        ),
        key_factors=["redundant components", "fault detection", "automatic switchover", "diagnostics", "reliability"],
        primary_authority=["ISO 26262", "SAE J2929", "UL 2580"],
        burden_holder="Battery Thermal Management Designer",
        adversary_position="Cost constraints may limit redundancy implementation.",
        counter_arguments=[
            "Redundancy is critical for safety and regulatory compliance.",
            "Investment reduces risk of catastrophic failures."
        ],
        resolution_strategy="Design redundant thermal management systems with validated fault tolerance.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="ISO 26262 - Functional Safety"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Voltage and Current Sensing",
        keywords=["voltage sensing", "current sensing", "battery monitoring", "accuracy", "sensor placement"],
        conclusion_template="Accurate voltage and current sensing within battery packs is essential for effective battery management and safety.",
        reasoning_framework=(
            "Voltage and current sensors provide real-time data for state-of-charge estimation, fault detection, and control. The framework includes "
            "sensor selection based on accuracy, response time, and environmental robustness. Sensor placement minimizes noise and interference. "
            "The reasoning covers calibration, signal conditioning, and integration with battery management systems. Validation includes accuracy "
            "testing and environmental stress testing."
        ),
        key_factors=["sensor accuracy", "response time", "placement", "signal conditioning", "calibration"],
        primary_authority=["SAE J2929", "IEC 62660", "UL 2580"],
        burden_holder="Battery Management System Developer",
        adversary_position="Inaccurate sensing leads to poor battery management and safety risks.",
        counter_arguments=[
            "High-quality sensing improves system reliability and safety.",
            "Calibration and validation are essential for accuracy."
        ],
        resolution_strategy="Select and validate sensors with rigorous testing and integration.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="SAE J2929 - Battery Monitoring Systems"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Software Safety Requirements",
        keywords=["software safety", "battery management", "functional safety", "fault tolerance", "ISO 26262"],
        conclusion_template="Battery management software must meet functional safety requirements to ensure reliable and safe operation.",
        reasoning_framework=(
            "Software controlling battery management systems must comply with functional safety standards such as ISO 26262. The framework "
            "includes hazard analysis, risk assessment, fault detection, and fail-safe mechanisms. The reasoning covers software architecture, "
            "verification and validation, and configuration management. Safety requirements specify response to faults, data integrity, and "
            "redundancy. Validation involves static analysis, testing, and audits."
        ),
        key_factors=["hazard analysis", "risk assessment", "fault tolerance", "verification", "validation"],
        primary_authority=["ISO 26262", "SAE J3061", "UL 2900"],
        burden_holder="Battery Management Software Developer",
        adversary_position="Non-compliance risks safety incidents and regulatory penalties.",
        counter_arguments=[
            "Functional safety compliance is mandatory for market access and user safety.",
            "Rigorous processes reduce software-related failures."
        ],
        resolution_strategy="Develop software per ISO 26262 with comprehensive testing and documentation.",
        entity_scope="Battery Management Systems",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="ISO 26262 - Functional Safety"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Thermal Modeling",
        keywords=["thermal modeling", "battery pack", "simulation", "heat transfer", "temperature distribution"],
        conclusion_template="Thermal modeling of battery packs informs design decisions to optimize temperature distribution and prevent hotspots.",
        reasoning_framework=(
            "Thermal modeling uses computational methods such as finite element analysis to simulate heat generation and dissipation within battery packs. "
            "The framework includes material properties, cooling system parameters, and operating conditions. The reasoning covers transient and steady-state "
            "heat transfer, convection, conduction, and radiation. Models predict temperature gradients and identify potential hotspots. Validation involves "
            "correlation with experimental data."
        ),
        key_factors=["material properties", "cooling parameters", "heat generation", "simulation accuracy", "validation"],
        primary_authority=["SAE J2929", "UL 2580", "ISO 6469"],
        burden_holder="Battery Thermal Engineer",
        adversary_position="Neglecting thermal modeling leads to suboptimal designs and safety risks.",
        counter_arguments=[
            "Modeling reduces design iterations and improves safety.",
            "Accurate simulations guide effective thermal management."
        ],
        resolution_strategy="Develop detailed thermal models validated by experimental testing.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="SAE J2929 - Battery Thermal Modeling"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Electrical Safety Training",
        keywords=["electrical safety", "training", "high voltage", "maintenance", "procedures"],
        conclusion_template="Comprehensive electrical safety training for personnel is essential to prevent accidents during battery pack maintenance and service.",
        reasoning_framework=(
            "Training programs cover high voltage hazards, safe work practices, use of personal protective equipment, and emergency procedures. "
            "The framework includes theoretical knowledge, hands-on exercises, and certification. The reasoning covers regulatory requirements, "
            "risk assessment, and incident prevention. Regular refresher courses maintain competency."
        ),
        key_factors=["hazard awareness", "safe work practices", "PPE usage", "emergency response", "certification"],
        primary_authority=["NFPA 70E", "OSHA", "IEC 6469"],
        burden_holder="Employers and Training Providers",
        adversary_position="Inadequate training increases risk of injury and liability.",
        counter_arguments=[
            "Proper training reduces accidents and improves safety culture.",
            "Investment in training is cost-effective over time."
        ],
        resolution_strategy="Implement standardized training programs with regular assessments.",
        entity_scope="Battery Pack Maintenance Personnel",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="NFPA 70E - Electrical Safety in the Workplace"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Fire Detection Systems",
        keywords=["fire detection", "battery pack", "smoke sensors", "temperature sensors", "early warning"],
        conclusion_template="Integrated fire detection systems provide early warning of battery pack fires to enable timely response and mitigation.",
        reasoning_framework=(
            "Fire detection systems use smoke, gas, and temperature sensors to monitor battery packs. The framework includes sensor placement, "
            "alarm thresholds, and integration with vehicle safety systems. Early detection enables activation of suppression systems and "
            "emergency protocols. The reasoning covers sensor sensitivity, false alarm reduction, and system reliability. Standards such as "
            "NFPA 855 guide design."
        ),
        key_factors=["sensor selection", "placement", "alarm thresholds", "system integration", "reliability"],
        primary_authority=["NFPA 855", "UL 268", "SAE J2464"],
        burden_holder="Battery Pack Safety System Designer",
        adversary_position="Omission of detection systems delays response and increases damage.",
        counter_arguments=[
            "Early detection is critical for safety and damage limitation.",
            "Detection systems are mandated by safety standards."
        ],
        resolution_strategy="Implement multi-sensor detection systems with validated performance.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="NFPA 855 - Standard for Installation of Stationary Energy Storage Systems"
    ),
    DoctrineBlock(
        topic="Electric Vehicle Battery Pack Fault Tolerance Design",
        keywords=["fault tolerance", "battery pack", "redundancy", "failure modes", "safety"],
        conclusion_template="Designing battery packs with fault tolerance improves safety and reliability by mitigating effects of component failures.",
        reasoning_framework=(
            "Fault tolerance involves incorporating redundancy, isolation, and fail-safe mechanisms. The framework includes analysis of failure modes, "
            "effects, and criticality (FMECA). Design features such as redundant sensors, parallel cell strings, and isolation switches enhance resilience. "
            "The reasoning covers detection, containment, and recovery strategies. Standards such as ISO 26262 guide functional safety design."
        ),
        key_factors=["redundancy", "isolation", "fail-safe design", "FMECA", "recovery"],
        primary_authority=["ISO 26262", "SAE J2929", "UL 2580"],
        burden_holder="Battery Pack Designer",
        adversary_position="Cost constraints may limit fault tolerance features.",
        counter_arguments=[
            "Fault tolerance is essential for safety and compliance.",
            "Investment reduces risk of catastrophic failures."
        ],
        resolution_strategy="Incorporate fault tolerance in design validated by risk analysis and testing.",
        entity_scope="Battery Packs in Electric Vehicles",
        confidence=0.95,
        confidence_zone