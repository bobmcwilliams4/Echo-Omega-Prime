from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from pathlib import Path

class ConfidenceZone(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

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
        topic="Diesel-Electric Prime Mover and Alternator Integration",
        keywords=["prime mover", "diesel engine", "alternator", "integration", "RAIL02"],
        conclusion_template="The integration of the diesel prime mover with the alternator in RAIL02 is achieved through direct coupling, ensuring optimal power transmission and minimal losses.",
        reasoning_framework=(
            "The diesel-electric locomotive relies on the mechanical energy produced by the prime mover (diesel engine) to drive the alternator, "
            "which converts mechanical energy into electrical energy for traction motors. Integration requires precise alignment, vibration isolation, "
            "and robust mounting to minimize mechanical losses and ensure reliability. The alternator's excitation system is tuned to match the engine's "
            "torque curve, optimizing power output across throttle notches. Key factors include engine speed regulation, alternator cooling, and load-sharing "
            "during MU operation. Industry standards (EMD, GE) specify coupling tolerances and vibration limits. EPA Tier 4 emissions impact engine design, "
            "requiring aftertreatment systems that may affect integration. FRA 49 CFR 229 mandates inspection and maintenance intervals for prime mover-alternator assemblies."
        ),
        key_factors=[
            "Engine speed regulation",
            "Alternator excitation",
            "Mechanical coupling",
            "Vibration isolation",
            "Load-sharing",
            "EPA Tier 4 compliance",
            "FRA 49 CFR 229 maintenance"
        ],
        primary_authority=[
            "EMD Locomotive Manual",
            "GE Locomotive Engineering Standards",
            "EPA Tier 4 Regulations",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive manufacturer",
        adversary_position="Integration may introduce vibration and alignment issues, impacting reliability.",
        counter_arguments=[
            "Modern coupling designs mitigate vibration.",
            "Routine maintenance ensures alignment.",
            "Aftertreatment systems are integrated with minimal impact."
        ],
        resolution_strategy="Adopt industry-standard coupling and vibration isolation methods; schedule regular inspections per FRA guidelines.",
        entity_scope="RAIL02 diesel-electric locomotives",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Integration Protocol"
    ),
    DoctrineBlock(
        topic="Traction Motor Types: DC Series vs AC Induction",
        keywords=["traction motor", "DC series", "AC induction", "RAIL02", "locomotive"],
        conclusion_template="RAIL02 utilizes AC induction traction motors for improved efficiency, reliability, and adhesion control compared to legacy DC series motors.",
        reasoning_framework=(
            "DC series motors historically dominated locomotive traction due to their high starting torque and simple control. However, AC induction motors "
            "offer superior efficiency, reduced maintenance, and enhanced adhesion control via inverter-driven variable frequency operation. AC motors withstand "
            "higher thermal loads and allow for regenerative braking. The transition to AC induction in RAIL02 aligns with industry trends and regulatory requirements. "
            "Key factors include motor cooling, inverter compatibility, maintenance intervals, and adhesion algorithms. EMD and GE specifications detail motor selection criteria. "
            "DC motors remain in legacy fleets but are phased out in new builds for Tier 4 compliance and operational efficiency."
        ),
        key_factors=[
            "Efficiency",
            "Maintenance",
            "Adhesion control",
            "Thermal tolerance",
            "Regenerative braking",
            "Inverter compatibility"
        ],
        primary_authority=[
            "EMD AC Traction Motor Specification",
            "GE AC Induction Motor Standards",
            "EPA Tier 4 Compliance"
        ],
        burden_holder="Locomotive designer",
        adversary_position="DC series motors offer higher starting torque and simpler maintenance.",
        counter_arguments=[
            "AC induction motors provide comparable torque with advanced control.",
            "Maintenance costs are lower for AC motors.",
            "Regulatory compliance favors AC induction."
        ],
        resolution_strategy="Select AC induction motors for new builds; retrofit legacy DC units as feasible.",
        entity_scope="RAIL02 traction motor systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE Evolution Series AC Motor Adoption"
    ),
    DoctrineBlock(
        topic="Power Electronics: Inverter, Rectifier, and Chopper Systems",
        keywords=["power electronics", "inverter", "rectifier", "chopper", "RAIL02"],
        conclusion_template="RAIL02 employs advanced inverter, rectifier, and chopper systems to manage power conversion and traction motor control.",
        reasoning_framework=(
            "Power electronics are central to diesel-electric locomotive operation. The rectifier converts alternator AC output to DC, which is then processed by choppers "
            "to regulate voltage and current for traction motors. Inverters convert DC back to variable-frequency AC for induction motors, enabling precise speed and torque control. "
            "RAIL02 integrates IGBT-based inverters for high efficiency and rapid switching. Chopper systems manage dynamic braking and power flow during regenerative events. "
            "Key factors include thermal management, switching frequency, harmonic mitigation, and compatibility with traction motor types. EMD and GE standards specify power electronics architecture. "
            "EPA Tier 4 regulations influence component selection for emissions and efficiency."
        ),
        key_factors=[
            "Conversion efficiency",
            "Thermal management",
            "Switching frequency",
            "Harmonic mitigation",
            "Motor compatibility",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EMD Power Electronics Manual",
            "GE Locomotive Electrical Standards",
            "EPA Tier 4 Guidelines"
        ],
        burden_holder="Electrical systems engineer",
        adversary_position="Complexity increases maintenance and failure risk.",
        counter_arguments=[
            "Modern diagnostics reduce downtime.",
            "Component reliability has improved.",
            "Efficiency gains outweigh complexity."
        ],
        resolution_strategy="Implement robust diagnostics and thermal management; adhere to industry standards.",
        entity_scope="RAIL02 power electronics",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Power Electronics Design"
    ),
    DoctrineBlock(
        topic="Dynamic Braking: Resistive and Regenerative Systems",
        keywords=["dynamic braking", "resistive", "regenerative", "RAIL02", "locomotive"],
        conclusion_template="RAIL02 supports both resistive and regenerative dynamic braking, optimizing energy recovery and heat dissipation.",
        reasoning_framework=(
            "Dynamic braking converts kinetic energy from the locomotive into electrical energy via traction motors operating as generators. Resistive braking dissipates this energy "
            "as heat through resistor grids, while regenerative braking returns energy to the power system or onboard storage. RAIL02's AC traction motors enable regenerative braking, "
            "improving fuel efficiency and reducing brake wear. Key factors include resistor grid sizing, inverter control algorithms, and compatibility with distributed power systems. "
            "Regulatory standards (FRA 49 CFR 229) require fail-safe operation and monitoring of dynamic brake performance. EMD and GE models specify resistor grid and inverter configurations."
        ),
        key_factors=[
            "Energy recovery",
            "Resistor grid sizing",
            "Inverter control",
            "Brake wear reduction",
            "Distributed power compatibility"
        ],
        primary_authority=[
            "EMD Dynamic Braking Manual",
            "GE Locomotive Braking Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Regenerative braking may be limited by grid compatibility and onboard storage.",
        counter_arguments=[
            "Resistive braking provides fallback.",
            "Distributed power systems enhance regenerative capability.",
            "Monitoring ensures safe operation."
        ],
        resolution_strategy="Integrate both braking modes; monitor performance per FRA requirements.",
        entity_scope="RAIL02 dynamic braking systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE Evolution Series Regenerative Braking"
    ),
    DoctrineBlock(
        topic="Train Resistance: Davis Equation and Grade Effects",
        keywords=["train resistance", "Davis equation", "grade", "RAIL02", "locomotive"],
        conclusion_template="Train resistance for RAIL02 is calculated using the Davis equation, with grade effects incorporated for accurate tractive effort estimation.",
        reasoning_framework=(
            "The Davis equation models train resistance as a function of speed, rolling resistance, and aerodynamic drag. Grade effects are added as a function of train weight and grade percentage. "
            "RAIL02's onboard systems use real-time data to adjust tractive effort based on calculated resistance, optimizing fuel consumption and adhesion. Key factors include train length, weight, speed, "
            "ambient conditions, and grade profile. EMD and GE software integrates Davis equation parameters for operational planning. FRA and AAR guidelines specify resistance calculation methods."
        ),
        key_factors=[
            "Speed",
            "Train weight",
            "Aerodynamic drag",
            "Rolling resistance",
            "Grade profile"
        ],
        primary_authority=[
            "AAR Train Resistance Guidelines",
            "EMD Locomotive Software",
            "GE Train Resistance Algorithms"
        ],
        burden_holder="Train dispatcher",
        adversary_position="Davis equation may not account for all real-world conditions.",
        counter_arguments=[
            "Real-time data improves accuracy.",
            "Grade effects are dynamically modeled.",
            "Software updates address new conditions."
        ],
        resolution_strategy="Use Davis equation with real-time adjustments; validate with operational data.",
        entity_scope="RAIL02 train resistance modeling",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AAR Resistance Calculation Standard"
    ),
    DoctrineBlock(
        topic="Tractive Effort and Adhesion: Wheel-Rail Friction",
        keywords=["tractive effort", "adhesion", "wheel-rail friction", "RAIL02"],
        conclusion_template="RAIL02 maximizes tractive effort through advanced adhesion control algorithms and optimized wheel-rail friction management.",
        reasoning_framework=(
            "Tractive effort is limited by the coefficient of friction between wheels and rails. RAIL02 employs real-time slip detection and adhesion control algorithms to maximize power transfer "
            "without wheel slip. Factors influencing adhesion include rail condition, weather, train weight, and speed. EMD and GE models use sanders, wheel slip sensors, and traction control software "
            "to enhance adhesion. FRA regulations require monitoring and reporting of wheel slip events. Industry standards specify minimum adhesion coefficients for safe operation."
        ),
        key_factors=[
            "Wheel-rail friction",
            "Slip detection",
            "Adhesion control",
            "Rail condition",
            "Weather effects"
        ],
        primary_authority=[
            "EMD Adhesion Control Manual",
            "GE Traction Control Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Adhesion control may be compromised by extreme weather or rail contamination.",
        counter_arguments=[
            "Sanders mitigate low adhesion.",
            "Real-time monitoring adjusts control algorithms.",
            "Maintenance addresses rail contamination."
        ],
        resolution_strategy="Implement advanced adhesion algorithms; use sanders and sensors per industry standards.",
        entity_scope="RAIL02 tractive effort systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Adhesion Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Consist, MU Operation, and Distributed Power",
        keywords=["locomotive consist", "MU operation", "distributed power", "RAIL02"],
        conclusion_template="RAIL02 supports MU and distributed power operation, enabling flexible consist management and remote locomotive control.",
        reasoning_framework=(
            "Multiple Unit (MU) operation allows locomotives to be controlled from a single cab, improving operational efficiency. Distributed power extends control to remote units within the train, "
            "reducing in-train forces and improving handling. RAIL02 integrates MU and distributed power protocols compatible with EMD and GE standards. Key factors include communication reliability, "
            "consist configuration, and remote diagnostics. FRA regulations require fail-safe operation and event recording. Industry precedents guide distributed power implementation for long trains."
        ),
        key_factors=[
            "Communication reliability",
            "Consist configuration",
            "Remote diagnostics",
            "Event recording",
            "In-train force management"
        ],
        primary_authority=[
            "EMD MU Operation Manual",
            "GE Distributed Power Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Train operator",
        adversary_position="Distributed power increases complexity and risk of communication failure.",
        counter_arguments=[
            "Redundant communication systems mitigate risk.",
            "Event recorders track operation.",
            "Industry standards ensure compatibility."
        ],
        resolution_strategy="Use industry-standard protocols; monitor communication and event recording.",
        entity_scope="RAIL02 consist and power systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE Distributed Power Implementation"
    ),
    DoctrineBlock(
        topic="Fuel Efficiency and Notch/Throttle Management",
        keywords=["fuel efficiency", "notch management", "throttle", "RAIL02"],
        conclusion_template="RAIL02 optimizes fuel efficiency through advanced notch/throttle management algorithms and real-time engine monitoring.",
        reasoning_framework=(
            "Throttle notches control engine power output, impacting fuel consumption and emissions. RAIL02 uses software algorithms to optimize notch selection based on train load, speed, and grade. "
            "Real-time monitoring adjusts engine parameters to minimize fuel use and comply with EPA Tier 4 standards. Key factors include load profile, train resistance, and operational schedule. "
            "EMD and GE models specify notch management protocols. FRA regulations require documentation of fuel efficiency improvements."
        ),
        key_factors=[
            "Throttle notch selection",
            "Engine monitoring",
            "Load profile",
            "EPA compliance",
            "Operational schedule"
        ],
        primary_authority=[
            "EMD Notch Management Manual",
            "GE Fuel Efficiency Standards",
            "EPA Tier 4 Regulations"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Manual throttle control may outperform automated algorithms in certain conditions.",
        counter_arguments=[
            "Algorithms adapt to real-time data.",
            "Manual override is available.",
            "EPA compliance requires automated management."
        ],
        resolution_strategy="Combine automated and manual control; monitor performance for continuous improvement.",
        entity_scope="RAIL02 fuel management systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Notch Optimization"
    ),
    DoctrineBlock(
        topic="EMD and GE Locomotive Model Specifications",
        keywords=["EMD", "GE", "locomotive specifications", "RAIL02"],
        conclusion_template="RAIL02 adheres to EMD and GE locomotive model specifications for mechanical, electrical, and operational standards.",
        reasoning_framework=(
            "Locomotive specifications define mechanical dimensions, electrical systems, and operational protocols. RAIL02 is designed to meet or exceed EMD and GE standards for prime mover, traction motors, "
            "power electronics, and braking systems. Key factors include model compatibility, maintenance intervals, and regulatory compliance. Industry standards ensure interoperability and safety. "
            "EPA and FRA regulations require adherence to specification for emissions and operational safety."
        ),
        key_factors=[
            "Mechanical dimensions",
            "Electrical systems",
            "Operational protocols",
            "Model compatibility",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EMD Locomotive Specification",
            "GE Locomotive Standards",
            "EPA Tier 4",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive manufacturer",
        adversary_position="Custom designs may offer improved performance over standard specifications.",
        counter_arguments=[
            "Standardization ensures interoperability.",
            "Regulatory compliance mandates specification adherence.",
            "Custom designs can be integrated within standard frameworks."
        ],
        resolution_strategy="Adhere to EMD and GE specifications; document deviations for regulatory review.",
        entity_scope="RAIL02 locomotive systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Specification Compliance"
    ),
    DoctrineBlock(
        topic="EPA Tier 4 Emissions and Locomotive Standards",
        keywords=["EPA Tier 4", "emissions", "locomotive standards", "RAIL02"],
        conclusion_template="RAIL02 complies with EPA Tier 4 emissions standards through advanced aftertreatment and engine management systems.",
        reasoning_framework=(
            "EPA Tier 4 regulations mandate strict limits on NOx, particulate matter, and hydrocarbons for locomotive engines. RAIL02 incorporates selective catalytic reduction (SCR), diesel particulate filters (DPF), "
            "and exhaust gas recirculation (EGR) to meet emissions targets. Engine management software monitors and adjusts combustion parameters in real-time. Key factors include aftertreatment system reliability, "
            "fuel quality, and maintenance intervals. EMD and GE models specify Tier 4 compliance protocols. FRA regulations require emissions testing and reporting."
        ),
        key_factors=[
            "SCR system",
            "DPF",
            "EGR",
            "Engine management",
            "Emissions testing"
        ],
        primary_authority=[
            "EPA Tier 4 Regulations",
            "EMD Emissions Compliance Manual",
            "GE Locomotive Emissions Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive manufacturer",
        adversary_position="Tier 4 systems increase complexity and maintenance costs.",
        counter_arguments=[
            "Emissions compliance is legally required.",
            "Modern systems are increasingly reliable.",
            "Maintenance intervals are optimized."
        ],
        resolution_strategy="Integrate robust aftertreatment systems; schedule maintenance per manufacturer guidelines.",
        entity_scope="RAIL02 emissions control systems",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE Tier 4 Locomotive Certification"
    ),
    DoctrineBlock(
        topic="Head End Power (HEP) and Hotel Load Management",
        keywords=["HEP", "hotel load", "power management", "RAIL02"],
        conclusion_template="RAIL02 provides reliable HEP and hotel load management through dedicated alternator and control systems.",
        reasoning_framework=(
            "Head End Power (HEP) supplies electricity for passenger train amenities, requiring stable voltage and frequency. RAIL02 uses a dedicated alternator and control system to manage hotel loads, "
            "ensuring uninterrupted power during varying operational conditions. Key factors include load balancing, alternator sizing, and emergency power protocols. EMD and GE standards specify HEP system requirements. "
            "FRA regulations mandate monitoring and fail-safe operation for passenger safety."
        ),
        key_factors=[
            "Alternator sizing",
            "Load balancing",
            "Voltage regulation",
            "Emergency protocols",
            "Passenger safety"
        ],
        primary_authority=[
            "EMD HEP System Manual",
            "GE Hotel Load Management Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive operator",
        adversary_position="HEP loads may exceed alternator capacity during peak demand.",
        counter_arguments=[
            "Load management algorithms prioritize critical systems.",
            "Emergency protocols ensure passenger safety.",
            "Alternator sizing meets peak demand requirements."
        ],
        resolution_strategy="Monitor hotel load in real-time; prioritize loads per safety guidelines.",
        entity_scope="RAIL02 HEP systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD F40PH HEP Implementation"
    ),
    DoctrineBlock(
        topic="Locomotive Maintenance and FRA 49 CFR 229 Compliance",
        keywords=["maintenance", "FRA 49 CFR 229", "compliance", "RAIL02"],
        conclusion_template="RAIL02 maintenance protocols comply with FRA 49 CFR 229, ensuring operational safety and reliability.",
        reasoning_framework=(
            "FRA 49 CFR 229 outlines mandatory inspection, maintenance, and recordkeeping requirements for locomotives. RAIL02 maintenance schedules are designed to meet or exceed these standards, "
            "covering prime mover, traction motors, power electronics, braking systems, and safety devices. Key factors include inspection intervals, documentation, and corrective action protocols. "
            "EMD and GE maintenance manuals guide procedures. Compliance is verified through FRA audits and event recorder data."
        ),
        key_factors=[
            "Inspection intervals",
            "Recordkeeping",
            "Corrective action",
            "Safety device maintenance",
            "Audit compliance"
        ],
        primary_authority=[
            "FRA 49 CFR 229",
            "EMD Maintenance Manual",
            "GE Locomotive Maintenance Standards"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Maintenance intervals may be insufficient for high-utilization fleets.",
        counter_arguments=[
            "Intervals are based on operational data.",
            "Corrective actions address unexpected failures.",
            "Event recorders provide audit trails."
        ],
        resolution_strategy="Adjust intervals based on fleet utilization; maintain comprehensive records.",
        entity_scope="RAIL02 maintenance systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA 49 CFR 229 Compliance Audit"
    ),
    DoctrineBlock(
        topic="Positive Train Control (PTC) Implementation",
        keywords=["PTC", "positive train control", "RAIL02", "safety"],
        conclusion_template="RAIL02 integrates PTC systems for enhanced safety, collision avoidance, and regulatory compliance.",
        reasoning_framework=(
            "Positive Train Control (PTC) is a federally mandated safety system designed to prevent train-to-train collisions, overspeed derailments, and unauthorized movements. RAIL02 integrates PTC hardware and software "
            "compatible with industry standards, including GPS, wireless communication, and onboard control interfaces. Key factors include system reliability, interoperability, and real-time data exchange. FRA regulations "
            "require PTC implementation and periodic testing. EMD and GE models specify PTC integration protocols."
        ),
        key_factors=[
            "System reliability",
            "Interoperability",
            "Real-time data exchange",
            "Hardware/software integration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "FRA PTC Implementation Guidelines",
            "EMD PTC Integration Manual",
            "GE PTC Standards"
        ],
        burden_holder="Railroad operator",
        adversary_position="PTC increases system complexity and may introduce interoperability challenges.",
        counter_arguments=[
            "Industry standards ensure compatibility.",
            "Periodic testing verifies reliability.",
            "Training mitigates operational risks."
        ],
        resolution_strategy="Follow FRA guidelines; conduct regular testing and training.",
        entity_scope="RAIL02 PTC systems",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA PTC Mandate"
    ),
    DoctrineBlock(
        topic="Locomotive Event Recorder and Data Management",
        keywords=["event recorder", "data management", "RAIL02", "FRA compliance"],
        conclusion_template="RAIL02 utilizes advanced event recorders and data management systems to meet FRA requirements and support operational analysis.",
        reasoning_framework=(
            "Event recorders capture operational data including speed, throttle position, brake application, and PTC events. RAIL02 integrates digital recorders with secure storage and real-time transmission capabilities. "
            "Key factors include data retention, security, and accessibility for regulatory review. FRA 49 CFR 229 mandates event recorder installation and data management protocols. EMD and GE models specify recorder specifications."
        ),
        key_factors=[
            "Data retention",
            "Security",
            "Accessibility",
            "Regulatory review",
            "Recorder specifications"
        ],
        primary_authority=[
            "FRA 49 CFR 229",
            "EMD Event Recorder Manual",
            "GE Data Management Standards"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Data management may be compromised by hardware failure or cyber threats.",
        counter_arguments=[
            "Redundant storage mitigates hardware failure.",
            "Encryption protects against cyber threats.",
            "Regular audits ensure compliance."
        ],
        resolution_strategy="Implement redundant, secure recorders; conduct periodic audits.",
        entity_scope="RAIL02 event recorder systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Event Recorder Standard"
    ),
    DoctrineBlock(
        topic="Wheel Slip Detection and Adhesion Control",
        keywords=["wheel slip", "adhesion control", "RAIL02", "traction"],
        conclusion_template="RAIL02 employs real-time wheel slip detection and advanced adhesion control to maximize tractive effort and minimize wear.",
        reasoning_framework=(
            "Wheel slip detection systems monitor traction motor speed and compare it to ground speed, identifying slip events. RAIL02 uses sensors and software algorithms to adjust power output and activate sanders as needed. "
            "Adhesion control improves safety and reduces wheel/rail wear. Key factors include sensor accuracy, algorithm responsiveness, and environmental conditions. EMD and GE models specify slip detection protocols. "
            "FRA regulations require monitoring and reporting of slip events."
        ),
        key_factors=[
            "Sensor accuracy",
            "Algorithm responsiveness",
            "Environmental conditions",
            "Sander activation",
            "Wear reduction"
        ],
        primary_authority=[
            "EMD Slip Detection Manual",
            "GE Adhesion Control Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Extreme conditions may overwhelm slip detection systems.",
        counter_arguments=[
            "Manual intervention is available.",
            "System updates improve responsiveness.",
            "Maintenance addresses sensor issues."
        ],
        resolution_strategy="Combine automated and manual control; schedule sensor maintenance.",
        entity_scope="RAIL02 slip detection systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Slip Detection Protocol"
    ),
    DoctrineBlock(
        topic="Air Brake Systems: Independent and Automatic Operation",
        keywords=["air brake", "independent brake", "automatic brake", "RAIL02"],
        conclusion_template="RAIL02 air brake systems support both independent and automatic operation, ensuring safe train handling and compliance.",
        reasoning_framework=(
            "Air brake systems are critical for train safety. Independent brakes control locomotive wheels, while automatic brakes manage the entire train consist. RAIL02 integrates both systems with electronic controls, "
            "allowing for precise application and release. Key factors include brake pipe pressure, response time, and fail-safe mechanisms. EMD and GE models specify brake system architecture. FRA regulations require "
            "periodic testing and maintenance."
        ),
        key_factors=[
            "Brake pipe pressure",
            "Response time",
            "Fail-safe mechanisms",
            "Electronic controls",
            "Testing and maintenance"
        ],
        primary_authority=[
            "EMD Brake System Manual",
            "GE Air Brake Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Train operator",
        adversary_position="Electronic controls may fail, compromising brake performance.",
        counter_arguments=[
            "Redundant systems ensure reliability.",
            "Manual override is available.",
            "Periodic testing verifies performance."
        ],
        resolution_strategy="Implement redundant controls; conduct regular testing and maintenance.",
        entity_scope="RAIL02 air brake systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Brake System Compliance"
    ),
    DoctrineBlock(
        topic="Draft Gear, Coupler Buff Forces, and Train Handling",
        keywords=["draft gear", "coupler", "buff forces", "train handling", "RAIL02"],
        conclusion_template="RAIL02 utilizes advanced draft gear and coupler designs to manage buff forces and optimize train handling.",
        reasoning_framework=(
            "Draft gear absorbs shock and buff forces during train movement, protecting equipment and cargo. RAIL02 employs high-capacity draft gear and couplers designed to industry standards. Key factors include force absorption, "
            "material durability, and compatibility with consist configuration. EMD and GE models specify draft gear and coupler requirements. FRA regulations mandate periodic inspection and testing."
        ),
        key_factors=[
            "Force absorption",
            "Material durability",
            "Consist compatibility",
            "Inspection intervals",
            "Testing protocols"
        ],
        primary_authority=[
            "EMD Draft Gear Manual",
            "GE Coupler Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Buff forces may exceed draft gear capacity during emergency braking.",
        counter_arguments=[
            "Design margins accommodate extreme forces.",
            "Periodic inspection identifies wear.",
            "Emergency protocols mitigate risk."
        ],
        resolution_strategy="Use high-capacity draft gear; inspect and test per FRA guidelines.",
        entity_scope="RAIL02 draft gear and coupler systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="AAR Draft Gear Standard"
    ),
    DoctrineBlock(
        topic="Locomotive Remote Control and Belt Pack Operation",
        keywords=["remote control", "belt pack", "RAIL02", "yard operation"],
        conclusion_template="RAIL02 supports remote control and belt pack operation for yard switching and safety.",
        reasoning_framework=(
            "Remote control and belt pack systems allow operators to control locomotives from outside the cab, improving safety and efficiency during yard operations. RAIL02 integrates wireless control protocols compatible with "
            "industry standards. Key factors include communication reliability, fail-safe operation, and operator training. FRA regulations require periodic testing and documentation. EMD and GE models specify remote control integration."
        ),
        key_factors=[
            "Communication reliability",
            "Fail-safe operation",
            "Operator training",
            "Testing and documentation",
            "Wireless protocol compatibility"
        ],
        primary_authority=[
            "EMD Remote Control Manual",
            "GE Belt Pack Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Yard operator",
        adversary_position="Wireless control may be compromised by interference or equipment failure.",
        counter_arguments=[
            "Redundant communication channels mitigate interference.",
            "Fail-safe protocols ensure safety.",
            "Training reduces operational risk."
        ],
        resolution_strategy="Use redundant wireless systems; conduct operator training and periodic testing.",
        entity_scope="RAIL02 remote control systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Remote Control Compliance"
    ),
    DoctrineBlock(
        topic="Crankcase Ventilation, Turbocharging, and Aftercooling",
        keywords=["crankcase ventilation", "turbocharging", "aftercooling", "RAIL02", "engine"],
        conclusion_template="RAIL02 engine systems utilize advanced crankcase ventilation, turbocharging, and aftercooling for emissions control and performance.",
        reasoning_framework=(
            "Crankcase ventilation removes blow-by gases, reducing emissions and preventing oil contamination. Turbocharging increases engine power and efficiency, while aftercooling reduces intake air temperature, "
            "improving combustion and lowering NOx emissions. RAIL02 integrates these systems per EPA Tier 4 requirements. Key factors include ventilation flow rate, turbocharger sizing, and aftercooler efficiency. "
            "EMD and GE models specify integration protocols. FRA regulations mandate inspection and maintenance."
        ),
        key_factors=[
            "Ventilation flow rate",
            "Turbocharger sizing",
            "Aftercooler efficiency",
            "Emissions reduction",
            "Maintenance intervals"
        ],
        primary_authority=[
            "EMD Engine Systems Manual",
            "GE Turbocharging Standards",
            "EPA Tier 4",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="System complexity increases maintenance requirements.",
        counter_arguments=[
            "Modern designs improve reliability.",
            "Maintenance intervals are optimized.",
            "Emissions compliance is mandatory."
        ],
        resolution_strategy="Integrate robust systems; schedule maintenance per manufacturer guidelines.",
        entity_scope="RAIL02 engine systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE Tier 4 Engine Integration"
    ),
    DoctrineBlock(
        topic="Locomotive Cooling System and Radiator Fan Control",
        keywords=["cooling system", "radiator fan", "control", "RAIL02"],
        conclusion_template="RAIL02 employs advanced cooling systems and radiator fan control for optimal engine temperature management.",
        reasoning_framework=(
            "Cooling systems maintain engine temperature within safe limits, preventing overheating and ensuring performance. Radiator fan control adjusts airflow based on engine load and ambient temperature. RAIL02 uses "
            "electronic fan control algorithms for efficiency. Key factors include coolant flow, fan speed, and temperature sensors. EMD and GE models specify cooling system architecture. FRA regulations require periodic inspection."
        ),
        key_factors=[
            "Coolant flow",
            "Fan speed control",
            "Temperature sensors",
            "Efficiency",
            "Inspection intervals"
        ],
        primary_authority=[
            "EMD Cooling System Manual",
            "GE Radiator Fan Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Fan control systems may fail, leading to overheating.",
        counter_arguments=[
            "Redundant sensors and manual override mitigate risk.",
            "Periodic inspection identifies issues.",
            "Electronic control improves efficiency."
        ],
        resolution_strategy="Use redundant sensors; conduct regular inspection and maintenance.",
        entity_scope="RAIL02 cooling systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Cooling Protocol"
    ),
    DoctrineBlock(
        topic="Alternator Excitation and Voltage Regulation",
        keywords=["alternator excitation", "voltage regulation", "RAIL02"],
        conclusion_template="RAIL02 alternator excitation and voltage regulation systems ensure stable power delivery to traction motors and auxiliary loads.",
        reasoning_framework=(
            "Alternator excitation controls the magnetic field strength, regulating output voltage. RAIL02 uses electronic excitation systems with real-time feedback to maintain voltage stability under varying loads. "
            "Voltage regulation is critical for traction motor performance and auxiliary systems. Key factors include excitation response time, sensor accuracy, and compatibility with power electronics. EMD and GE models "
            "specify excitation and regulation protocols. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Excitation response time",
            "Sensor accuracy",
            "Load compatibility",
            "Voltage stability",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Alternator Manual",
            "GE Voltage Regulation Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Electrical systems engineer",
        adversary_position="Rapid load changes may destabilize voltage regulation.",
        counter_arguments=[
            "Real-time feedback improves stability.",
            "Redundant sensors mitigate risk.",
            "Testing verifies performance."
        ],
        resolution_strategy="Use electronic feedback systems; conduct periodic testing.",
        entity_scope="RAIL02 alternator systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE Alternator Excitation Protocol"
    ),
    DoctrineBlock(
        topic="Distributed Power Communication Protocols",
        keywords=["distributed power", "communication protocols", "RAIL02"],
        conclusion_template="RAIL02 employs industry-standard distributed power communication protocols for reliable remote locomotive control.",
        reasoning_framework=(
            "Distributed power communication protocols enable remote control of locomotives within a train consist. RAIL02 uses wireless and wired communication systems compatible with EMD and GE standards. "
            "Key factors include signal reliability, latency, and fail-safe operation. FRA regulations require periodic testing and documentation. Industry precedents guide protocol selection for interoperability."
        ),
        key_factors=[
            "Signal reliability",
            "Latency",
            "Fail-safe operation",
            "Interoperability",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Distributed Power Manual",
            "GE Communication Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Train operator",
        adversary_position="Wireless communication may be disrupted by environmental factors.",
        counter_arguments=[
            "Redundant channels improve reliability.",
            "Periodic testing identifies issues.",
            "Industry standards ensure compatibility."
        ],
        resolution_strategy="Use redundant communication systems; conduct regular testing.",
        entity_scope="RAIL02 distributed power systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GE Distributed Power Communication Standard"
    ),
    DoctrineBlock(
        topic="Traction Motor Cooling and Thermal Management",
        keywords=["traction motor cooling", "thermal management", "RAIL02"],
        conclusion_template="RAIL02 traction motor cooling systems ensure optimal thermal management for reliability and performance.",
        reasoning_framework=(
            "Traction motors generate significant heat during operation. RAIL02 uses forced-air cooling and thermal sensors to maintain safe operating temperatures. Key factors include airflow rate, sensor placement, "
            "and maintenance intervals. EMD and GE models specify cooling system architecture. FRA regulations require periodic inspection and documentation."
        ),
        key_factors=[
            "Airflow rate",
            "Sensor placement",
            "Temperature monitoring",
            "Maintenance intervals",
            "Inspection protocols"
        ],
        primary_authority=[
            "EMD Traction Motor Cooling Manual",
            "GE Thermal Management Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Cooling system failure may lead to motor damage.",
        counter_arguments=[
            "Redundant sensors and alarms mitigate risk.",
            "Periodic maintenance identifies issues.",
            "Forced-air cooling improves reliability."
        ],
        resolution_strategy="Use redundant sensors; schedule regular maintenance and inspection.",
        entity_scope="RAIL02 traction motor systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Traction Motor Cooling Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Lighting and Safety Devices",
        keywords=["lighting", "safety devices", "RAIL02", "FRA compliance"],
        conclusion_template="RAIL02 integrates advanced lighting and safety devices to meet FRA requirements and enhance operational safety.",
        reasoning_framework=(
            "Locomotive lighting includes headlights, ditch lights, and marker lights, improving visibility and safety. Safety devices such as horn, bell, and emergency stop are integrated with electronic controls. "
            "RAIL02 meets FRA 49 CFR 229 requirements for lighting and safety device operation. Key factors include device reliability, response time, and periodic testing. EMD and GE models specify device integration protocols."
        ),
        key_factors=[
            "Device reliability",
            "Response time",
            "Electronic controls",
            "Testing intervals",
            "Regulatory compliance"
        ],
        primary_authority=[
            "EMD Lighting Manual",
            "GE Safety Device Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Electronic controls may fail, compromising safety.",
        counter_arguments=[
            "Redundant systems ensure reliability.",
            "Manual override is available.",
            "Periodic testing verifies performance."
        ],
        resolution_strategy="Implement redundant controls; conduct regular testing and maintenance.",
        entity_scope="RAIL02 lighting and safety devices",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Lighting and Safety Device Compliance"
    ),
    DoctrineBlock(
        topic="Locomotive Cab Ergonomics and Human Factors",
        keywords=["cab ergonomics", "human factors", "RAIL02"],
        conclusion_template="RAIL02 cab design prioritizes ergonomics and human factors for operator comfort and safety.",
        reasoning_framework=(
            "Cab ergonomics impact operator comfort, fatigue, and safety. RAIL02 incorporates adjustable seating, climate control, and intuitive control layouts. Key factors include visibility, accessibility, and noise reduction. "
            "EMD and GE models specify ergonomic design protocols. FRA regulations require minimum standards for cab design and safety devices."
        ),
        key_factors=[
            "Seating adjustment",
            "Climate control",
            "Control layout",
            "Visibility",
            "Noise reduction"
        ],
        primary_authority=[
            "EMD Cab Ergonomics Manual",
            "GE Human Factors Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive manufacturer",
        adversary_position="Ergonomic improvements may increase design and manufacturing costs.",
        counter_arguments=[
            "Improved ergonomics reduce operator fatigue.",
            "Safety benefits outweigh cost increases.",
            "Industry standards guide cost-effective design."
        ],
        resolution_strategy="Adhere to ergonomic standards; balance cost and safety.",
        entity_scope="RAIL02 cab systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Cab Ergonomics Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Fire Detection and Suppression",
        keywords=["fire detection", "suppression", "RAIL02", "safety"],
        conclusion_template="RAIL02 integrates fire detection and suppression systems for enhanced safety and regulatory compliance.",
        reasoning_framework=(
            "Fire detection systems monitor engine and electrical compartments for smoke and heat. Suppression systems activate automatically or manually to extinguish fires. RAIL02 uses industry-standard sensors and suppression agents. "
            "Key factors include sensor placement, response time, and maintenance intervals. FRA regulations require periodic testing and documentation. EMD and GE models specify fire system integration protocols."
        ),
        key_factors=[
            "Sensor placement",
            "Response time",
            "Suppression agent",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Fire Detection Manual",
            "GE Suppression Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="System failure may compromise safety during fire events.",
        counter_arguments=[
            "Redundant sensors improve reliability.",
            "Manual override is available.",
            "Periodic testing verifies performance."
        ],
        resolution_strategy="Use redundant sensors; conduct regular testing and maintenance.",
        entity_scope="RAIL02 fire detection and suppression systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Fire Detection Compliance"
    ),
    DoctrineBlock(
        topic="Locomotive Horn, Bell, and Audible Warning Devices",
        keywords=["horn", "bell", "audible warning", "RAIL02"],
        conclusion_template="RAIL02 integrates horn, bell, and audible warning devices per FRA standards for operational safety.",
        reasoning_framework=(
            "Audible warning devices alert personnel and the public to train movement. RAIL02 uses electronically controlled horn and bell systems with manual override. Key factors include device reliability, response time, "
            "and compliance with FRA 49 CFR 229. EMD and GE models specify device integration protocols. Periodic testing and maintenance are required."
        ),
        key_factors=[
            "Device reliability",
            "Response time",
            "Electronic controls",
            "Manual override",
            "Testing and maintenance"
        ],
        primary_authority=[
            "EMD Audible Warning Manual",
            "GE Horn and Bell Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Electronic controls may fail, compromising warning effectiveness.",
        counter_arguments=[
            "Redundant systems ensure reliability.",
            "Manual override is available.",
            "Periodic testing verifies performance."
        ],
        resolution_strategy="Implement redundant controls; conduct regular testing and maintenance.",
        entity_scope="RAIL02 warning devices",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="FRA Audible Warning Device Compliance"
    ),
    DoctrineBlock(
        topic="Locomotive Sanding System and Rail Condition Management",
        keywords=["sanding system", "rail condition", "RAIL02", "adhesion"],
        conclusion_template="RAIL02 sanding systems improve adhesion and manage rail condition for optimal tractive effort.",
        reasoning_framework=(
            "Sanding systems deposit sand on rails to increase friction during low adhesion events. RAIL02 uses electronically controlled sanders activated by slip detection algorithms. Key factors include sand quality, "
            "delivery rate, and environmental impact. EMD and GE models specify sanding system integration. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Sand quality",
            "Delivery rate",
            "Electronic control",
            "Environmental impact",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Sanding System Manual",
            "GE Rail Condition Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive operator",
        adversary_position="Excessive sanding may damage rails and increase maintenance costs.",
        counter_arguments=[
            "Algorithms optimize sanding rate.",
            "Periodic maintenance addresses rail wear.",
            "Environmental impact is monitored."
        ],
        resolution_strategy="Use optimized sanding algorithms; monitor rail condition and environmental impact.",
        entity_scope="RAIL02 sanding systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Sanding Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Battery Management and Auxiliary Power",
        keywords=["battery management", "auxiliary power", "RAIL02"],
        conclusion_template="RAIL02 battery management systems ensure reliable auxiliary power for startup and emergency operation.",
        reasoning_framework=(
            "Battery systems provide auxiliary power for engine startup, emergency lighting, and control systems. RAIL02 uses electronic battery management with real-time monitoring and charging control. Key factors include "
            "battery capacity, charge/discharge cycles, and maintenance intervals. EMD and GE models specify battery integration protocols. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Battery capacity",
            "Charge/discharge cycles",
            "Monitoring",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Battery Management Manual",
            "GE Auxiliary Power Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Battery failure may compromise auxiliary power during emergencies.",
        counter_arguments=[
            "Redundant battery systems improve reliability.",
            "Real-time monitoring identifies issues.",
            "Periodic maintenance ensures performance."
        ],
        resolution_strategy="Use redundant batteries; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 battery systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Battery Management Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Air Compressor and Pneumatic Systems",
        keywords=["air compressor", "pneumatic systems", "RAIL02"],
        conclusion_template="RAIL02 air compressor and pneumatic systems provide reliable air supply for brakes and auxiliary devices.",
        reasoning_framework=(
            "Air compressors supply pressurized air for brake systems and auxiliary devices. RAIL02 uses electronically controlled compressors with real-time monitoring. Key factors include compressor capacity, duty cycle, "
            "and maintenance intervals. EMD and GE models specify pneumatic system integration. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Compressor capacity",
            "Duty cycle",
            "Monitoring",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Air Compressor Manual",
            "GE Pneumatic Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Compressor failure may compromise brake performance.",
        counter_arguments=[
            "Redundant compressors improve reliability.",
            "Real-time monitoring identifies issues.",
            "Periodic maintenance ensures performance."
        ],
        resolution_strategy="Use redundant compressors; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 pneumatic systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Air Compressor Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Traction Control Software and Diagnostics",
        keywords=["traction control", "software", "diagnostics", "RAIL02"],
        conclusion_template="RAIL02 traction control software and diagnostics optimize performance and support predictive maintenance.",
        reasoning_framework=(
            "Traction control software manages power delivery to traction motors, maximizing efficiency and adhesion. Diagnostics monitor system health and support predictive maintenance. RAIL02 uses real-time analytics and "
            "automated alerts. Key factors include software reliability, sensor integration, and maintenance intervals. EMD and GE models specify software protocols. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Software reliability",
            "Sensor integration",
            "Analytics",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Traction Control Software Manual",
            "GE Diagnostics Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Software failure may compromise traction control.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Automated alerts identify issues.",
            "Periodic testing verifies performance."
        ],
        resolution_strategy="Use redundant software systems; conduct regular testing and maintenance.",
        entity_scope="RAIL02 traction control systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Traction Control Software Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive HVAC and Climate Control Systems",
        keywords=["HVAC", "climate control", "RAIL02"],
        conclusion_template="RAIL02 HVAC and climate control systems ensure operator comfort and equipment reliability.",
        reasoning_framework=(
            "HVAC systems regulate temperature and humidity in the locomotive cab and equipment compartments. RAIL02 uses electronically controlled HVAC with real-time monitoring. Key factors include system capacity, "
            "response time, and maintenance intervals. EMD and GE models specify HVAC integration protocols. FRA regulations require minimum standards for operator comfort."
        ),
        key_factors=[
            "System capacity",
            "Response time",
            "Monitoring",
            "Maintenance intervals",
            "Operator comfort"
        ],
        primary_authority=[
            "EMD HVAC Manual",
            "GE Climate Control Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="HVAC failure may compromise operator comfort and equipment reliability.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Real-time monitoring identifies issues.",
            "Periodic maintenance ensures performance."
        ],
        resolution_strategy="Use redundant HVAC systems; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 HVAC systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe HVAC Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Control Stand and User Interface",
        keywords=["control stand", "user interface", "RAIL02"],
        conclusion_template="RAIL02 control stand and user interface prioritize operator usability and safety.",
        reasoning_framework=(
            "Control stand and user interface design impact operator efficiency and safety. RAIL02 uses ergonomic layouts, intuitive controls, and real-time displays. Key factors include visibility, accessibility, and response time. "
            "EMD and GE models specify control stand integration protocols. FRA regulations require minimum standards for control interface design."
        ),
        key_factors=[
            "Ergonomic layout",
            "Intuitive controls",
            "Real-time displays",
            "Visibility",
            "Accessibility"
        ],
        primary_authority=[
            "EMD Control Stand Manual",
            "GE User Interface Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive manufacturer",
        adversary_position="User interface improvements may increase design and manufacturing costs.",
        counter_arguments=[
            "Improved usability reduces operator error.",
            "Safety benefits outweigh cost increases.",
            "Industry standards guide cost-effective design."
        ],
        resolution_strategy="Adhere to ergonomic standards; balance cost and safety.",
        entity_scope="RAIL02 control stand systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Control Stand Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Electrical Grounding and Fault Protection",
        keywords=["electrical grounding", "fault protection", "RAIL02"],
        conclusion_template="RAIL02 electrical grounding and fault protection systems ensure safety and reliability.",
        reasoning_framework=(
            "Electrical grounding and fault protection prevent equipment damage and ensure operator safety. RAIL02 uses industry-standard grounding protocols and circuit protection devices. Key factors include grounding integrity, "
            "fault detection, and maintenance intervals. EMD and GE models specify grounding and protection integration. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Grounding integrity",
            "Fault detection",
            "Circuit protection",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Electrical Grounding Manual",
            "GE Fault Protection Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Grounding failure may compromise safety and equipment reliability.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Periodic testing identifies issues.",
            "Industry standards ensure safety."
        ],
        resolution_strategy="Use redundant grounding systems; conduct regular testing and maintenance.",
        entity_scope="RAIL02 electrical systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Electrical Grounding Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Auxiliary Generator and Power Distribution",
        keywords=["auxiliary generator", "power distribution", "RAIL02"],
        conclusion_template="RAIL02 auxiliary generator and power distribution systems ensure reliable operation of auxiliary loads.",
        reasoning_framework=(
            "Auxiliary generators supply power to non-traction loads including lighting, HVAC, and hotel load systems. RAIL02 uses electronically controlled generators with real-time monitoring. Key factors include generator capacity, "
            "distribution architecture, and maintenance intervals. EMD and GE models specify auxiliary power integration. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Generator capacity",
            "Distribution architecture",
            "Monitoring",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Auxiliary Generator Manual",
            "GE Power Distribution Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Generator failure may compromise auxiliary load operation.",
        counter_arguments=[
            "Redundant generators improve reliability.",
            "Real-time monitoring identifies issues.",
            "Periodic maintenance ensures performance."
        ],
        resolution_strategy="Use redundant generators; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 auxiliary power systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Auxiliary Generator Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Oil Filtration and Lubrication Systems",
        keywords=["oil filtration", "lubrication", "RAIL02"],
        conclusion_template="RAIL02 oil filtration and lubrication systems ensure engine reliability and longevity.",
        reasoning_framework=(
            "Oil filtration removes contaminants, while lubrication reduces friction and wear. RAIL02 uses electronically monitored filtration and lubrication systems. Key factors include filter capacity, oil quality, and maintenance intervals. "
            "EMD and GE models specify filtration and lubrication integration. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Filter capacity",
            "Oil quality",
            "Monitoring",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Oil Filtration Manual",
            "GE Lubrication Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Filtration failure may compromise engine reliability.",
        counter_arguments=[
            "Redundant filters improve reliability.",
            "Real-time monitoring identifies issues.",
            "Periodic maintenance ensures performance."
        ],
        resolution_strategy="Use redundant filters; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 oil filtration and lubrication systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Oil Filtration Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Water System and Freeze Protection",
        keywords=["water system", "freeze protection", "RAIL02"],
        conclusion_template="RAIL02 water system and freeze protection ensure reliable operation in cold environments.",
        reasoning_framework=(
            "Water systems supply coolant and support auxiliary devices. Freeze protection prevents system damage in cold environments. RAIL02 uses electronically controlled heaters and insulation. Key factors include heater capacity, "
            "insulation quality, and maintenance intervals. EMD and GE models specify water system integration. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Heater capacity",
            "Insulation quality",
            "Monitoring",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Water System Manual",
            "GE Freeze Protection Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Freeze protection failure may compromise water system reliability.",
        counter_arguments=[
            "Redundant heaters improve reliability.",
            "Real-time monitoring identifies issues.",
            "Periodic maintenance ensures performance."
        ],
        resolution_strategy="Use redundant heaters; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 water systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Freeze Protection Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Vibration Monitoring and Mitigation",
        keywords=["vibration monitoring", "mitigation", "RAIL02"],
        conclusion_template="RAIL02 vibration monitoring and mitigation systems ensure equipment reliability and operator comfort.",
        reasoning_framework=(
            "Vibration monitoring systems detect abnormal vibration levels in engine, traction motors, and bogies. Mitigation includes isolation mounts and damping materials. RAIL02 uses real-time sensors and analytics. Key factors include sensor placement, "
            "response time, and maintenance intervals. EMD and GE models specify vibration integration protocols. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Sensor placement",
            "Response time",
            "Isolation mounts",
            "Damping materials",
            "Maintenance intervals"
        ],
        primary_authority=[
            "EMD Vibration Monitoring Manual",
            "GE Mitigation Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Mitigation failure may compromise equipment reliability.",
        counter_arguments=[
            "Redundant sensors improve reliability.",
            "Periodic maintenance identifies issues.",
            "Industry standards ensure performance."
        ],
        resolution_strategy="Use redundant sensors; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 vibration systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Vibration Monitoring Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Bogie and Suspension Systems",
        keywords=["bogie", "suspension", "RAIL02"],
        conclusion_template="RAIL02 bogie and suspension systems optimize ride quality and equipment protection.",
        reasoning_framework=(
            "Bogie and suspension systems absorb track irregularities and distribute loads. RAIL02 uses high-capacity suspension with real-time monitoring. Key factors include spring capacity, damping, and maintenance intervals. "
            "EMD and GE models specify bogie and suspension integration. FRA regulations require periodic testing and documentation."
        ),
        key_factors=[
            "Spring capacity",
            "Damping",
            "Monitoring",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Bogie Manual",
            "GE Suspension Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Suspension failure may compromise ride quality and equipment protection.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Periodic maintenance identifies issues.",
            "Industry standards ensure performance."
        ],
        resolution_strategy="Use redundant suspension systems; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 bogie and suspension systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Bogie Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Paint, Corrosion Protection, and Environmental Compliance",
        keywords=["paint", "corrosion protection", "environmental compliance", "RAIL02"],
        conclusion_template="RAIL02 paint and corrosion protection systems ensure environmental compliance and equipment longevity.",
        reasoning_framework=(
            "Paint and corrosion protection prevent environmental damage and extend equipment life. RAIL02 uses industry-standard coatings and corrosion inhibitors. Key factors include coating quality, environmental impact, and maintenance intervals. "
            "EMD and GE models specify paint and protection integration. EPA and FRA regulations require environmental compliance and periodic documentation."
        ),
        key_factors=[
            "Coating quality",
            "Corrosion inhibitors",
            "Environmental impact",
            "Maintenance intervals",
            "Testing and documentation"
        ],
        primary_authority=[
            "EMD Paint Manual",
            "GE Corrosion Protection Standards",
            "EPA Environmental Compliance",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Coating failure may compromise environmental compliance and equipment longevity.",
        counter_arguments=[
            "Redundant coatings improve reliability.",
            "Periodic maintenance identifies issues.",
            "Industry standards ensure compliance."
        ],
        resolution_strategy="Use industry-standard coatings; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 paint and corrosion protection systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Paint Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Noise and Vibration Environmental Standards",
        keywords=["noise", "vibration", "environmental standards", "RAIL02"],
        conclusion_template="RAIL02 complies with noise and vibration environmental standards for operator safety and public health.",
        reasoning_framework=(
            "Noise and vibration standards limit exposure for operators and the public. RAIL02 uses sound-damping materials and vibration isolation mounts. Key factors include measurement protocols, mitigation strategies, and maintenance intervals. "
            "EMD and GE models specify noise and vibration integration. EPA and FRA regulations require compliance and periodic documentation."
        ),
        key_factors=[
            "Sound-damping materials",
            "Isolation mounts",
            "Measurement protocols",
            "Mitigation strategies",
            "Maintenance intervals"
        ],
        primary_authority=[
            "EMD Noise Manual",
            "GE Vibration Standards",
            "EPA Environmental Compliance",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive manufacturer",
        adversary_position="Mitigation failure may compromise compliance and operator safety.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Periodic maintenance identifies issues.",
            "Industry standards ensure compliance."
        ],
        resolution_strategy="Use industry-standard mitigation; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 noise and vibration systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Noise Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Data Analytics and Predictive Maintenance",
        keywords=["data analytics", "predictive maintenance", "RAIL02"],
        conclusion_template="RAIL02 data analytics support predictive maintenance and operational optimization.",
        reasoning_framework=(
            "Data analytics monitor locomotive systems in real-time, identifying trends and predicting failures. Predictive maintenance reduces downtime and improves reliability. RAIL02 uses integrated analytics platforms compatible with EMD and GE models. "
            "Key factors include data quality, analytics algorithms, and maintenance intervals. FRA regulations require documentation and periodic review."
        ),
        key_factors=[
            "Data quality",
            "Analytics algorithms",
            "Maintenance intervals",
            "Documentation",
            "Periodic review"
        ],
        primary_authority=[
            "EMD Data Analytics Manual",
            "GE Predictive Maintenance Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Locomotive maintenance crew",
        adversary_position="Analytics failure may compromise predictive maintenance effectiveness.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Periodic review identifies issues.",
            "Industry standards ensure performance."
        ],
        resolution_strategy="Use industry-standard analytics; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 data analytics systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Data Analytics Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Fleet Management and Asset Tracking",
        keywords=["fleet management", "asset tracking", "RAIL02"],
        conclusion_template="RAIL02 fleet management and asset tracking systems optimize utilization and maintenance scheduling.",
        reasoning_framework=(
            "Fleet management systems track locomotive location, utilization, and maintenance status. Asset tracking improves operational efficiency and reduces downtime. RAIL02 uses GPS and RFID-based systems compatible with EMD and GE models. "
            "Key factors include tracking accuracy, data integration, and maintenance intervals. FRA regulations require documentation and periodic review."
        ),
        key_factors=[
            "Tracking accuracy",
            "Data integration",
            "Maintenance intervals",
            "Documentation",
            "Periodic review"
        ],
        primary_authority=[
            "EMD Fleet Management Manual",
            "GE Asset Tracking Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Railroad operator",
        adversary_position="Tracking failure may compromise fleet utilization and maintenance scheduling.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Periodic review identifies issues.",
            "Industry standards ensure performance."
        ],
        resolution_strategy="Use industry-standard tracking; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 fleet management systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Fleet Management Protocol"
    ),
    DoctrineBlock(
        topic="Locomotive Wireless Communication and Cybersecurity",
        keywords=["wireless communication", "cybersecurity", "RAIL02"],
        conclusion_template="RAIL02 wireless communication and cybersecurity systems ensure reliable operation and data protection.",
        reasoning_framework=(
            "Wireless communication systems support remote control, diagnostics, and asset tracking. Cybersecurity protocols protect against unauthorized access and data breaches. RAIL02 uses encrypted communication and redundant channels. "
            "Key factors include encryption strength, channel reliability, and maintenance intervals. FRA regulations require documentation and periodic review."
        ),
        key_factors=[
            "Encryption strength",
            "Channel reliability",
            "Maintenance intervals",
            "Documentation",
            "Periodic review"
        ],
        primary_authority=[
            "EMD Wireless Communication Manual",
            "GE Cybersecurity Standards",
            "FRA 49 CFR 229"
        ],
        burden_holder="Railroad operator",
        adversary_position="Cybersecurity failure may compromise data protection and operation.",
        counter_arguments=[
            "Redundant systems improve reliability.",
            "Periodic review identifies issues.",
            "Industry standards ensure protection."
        ],
        resolution_strategy="Use industry-standard encryption; monitor and maintain per manufacturer guidelines.",
        entity_scope="RAIL02 wireless communication systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EMD SD70ACe Cybersecurity Protocol"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(keyword: str) -> List[DoctrineBlock]:
    keyword_lower = keyword.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if keyword_lower in doctrine.topic.lower() or any(keyword_lower in k.lower() for k in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]