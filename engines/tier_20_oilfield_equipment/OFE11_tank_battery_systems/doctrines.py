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
        topic="Two-Phase Separator Design",
        keywords=["separator", "two-phase", "design", "oil", "gas", "vessel", "sizing", "residence time"],
        conclusion_template="A two-phase separator must be sized to ensure adequate residence time for oil and gas separation, considering maximum expected flow rates and fluid properties.",
        reasoning_framework="""
        The design of a two-phase separator is governed by API 12J standards and must ensure that the vessel provides sufficient volume for the separation of oil and gas under operating conditions. Key factors include the maximum anticipated flow rates, the density and viscosity of the fluids, and the presence of contaminants such as sand or water. The separator must be equipped with appropriate inlet devices to minimize turbulence, and the sizing must account for surge events and slugging. The design should also consider pressure ratings, corrosion allowances, and maintenance accessibility. Computational fluid dynamics (CFD) may be used to validate design assumptions. The separator's efficiency is directly tied to the residence time and the internal configuration, including baffles and mist eliminators. Safety and environmental compliance, such as pressure relief and vapor recovery, are mandatory.
        """,
        key_factors=[
            "Maximum flow rate",
            "Fluid properties (density, viscosity)",
            "Residence time",
            "Separator internal configuration",
            "Pressure rating",
            "Corrosion allowance",
            "Safety and environmental compliance"
        ],
        primary_authority=[
            "API 12J",
            "ASME Section VIII",
            "EPA CFR 40 Part 60 Subpart OOOOa"
        ],
        burden_holder="Design Engineer",
        adversary_position="Separator may be undersized, leading to poor separation and environmental violations.",
        counter_arguments=[
            "CFD validation supports sizing",
            "Historical performance data",
            "API 12J compliance"
        ],
        resolution_strategy="Peer review of design calculations, third-party validation, and adherence to API standards.",
        entity_scope="Tank Battery System",
        confidence=0.98,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 12J Section 4.2"
    ),
    DoctrineBlock(
        topic="Three-Phase Separator Design",
        keywords=["separator", "three-phase", "design", "oil", "water", "gas", "vessel", "emulsion"],
        conclusion_template="Three-phase separators must be designed to efficiently separate oil, water, and gas, with provisions for emulsion handling and interface control.",
        reasoning_framework="""
        Three-phase separator design requires consideration of the distinct densities and viscosities of oil, water, and gas. The vessel must provide sufficient residence time for the separation of all three phases, with interface controls to manage the oil-water boundary. Emulsion breaking devices, such as coalescers or electrostatic grids, may be necessary. The sizing must accommodate the worst-case flow scenario, including slugging and surges. Internal configurations, such as weirs and baffles, are critical for phase separation. The separator must be equipped with level control devices for each phase, and provisions for sampling and maintenance. Compliance with API 12J and ASME standards is required. Environmental controls, such as vapor recovery and water discharge treatment, must be integrated.
        """,
        key_factors=[
            "Phase densities and viscosities",
            "Residence time",
            "Emulsion handling",
            "Interface control",
            "Internal configuration",
            "Level control devices",
            "Environmental compliance"
        ],
        primary_authority=[
            "API 12J",
            "ASME Section VIII",
            "EPA NPDES"
        ],
        burden_holder="Process Engineer",
        adversary_position="Improper phase separation leads to emulsion carryover and water contamination.",
        counter_arguments=[
            "Emulsion breaking devices included",
            "API 12J-compliant sizing",
            "Level control instrumentation"
        ],
        resolution_strategy="Design review, pilot testing, and instrumentation calibration.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 12J Section 5.3"
    ),
    DoctrineBlock(
        topic="Heater Treater Emulsion Breaking",
        keywords=["heater treater", "emulsion", "breaking", "temperature", "chemical", "design"],
        conclusion_template="Heater treaters must operate at optimal temperature and chemical dosage to effectively break emulsions and separate oil and water.",
        reasoning_framework="""
        Heater treaters use heat and chemical injection to break emulsions formed between oil and water. The operating temperature must be sufficient to reduce viscosity and promote coalescence, but not so high as to cause excessive energy consumption or thermal degradation of chemicals. Chemical dosage must be optimized based on emulsion stability and water cut. The treater's internal configuration, including baffles and coalescing plates, enhances separation. API 12L provides guidance on design and operation. Monitoring of effluent quality and periodic calibration of chemical injection systems are required. Safety controls, such as pressure relief and temperature alarms, must be implemented.
        """,
        key_factors=[
            "Operating temperature",
            "Chemical dosage",
            "Emulsion stability",
            "Internal configuration",
            "Effluent quality monitoring",
            "Safety controls"
        ],
        primary_authority=[
            "API 12L",
            "EPA SPCC",
            "ASME Section VIII"
        ],
        burden_holder="Operations Supervisor",
        adversary_position="Insufficient emulsion breaking leads to water carryover and oil losses.",
        counter_arguments=[
            "Temperature and chemical optimization",
            "Effluent monitoring",
            "API 12L compliance"
        ],
        resolution_strategy="Routine performance testing and adjustment of operating parameters.",
        entity_scope="Tank Battery System",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 12L Section 3.1"
    ),
    DoctrineBlock(
        topic="Free Water Knockout (FWKO) Residence Time",
        keywords=["FWKO", "free water knockout", "residence time", "sizing", "tank", "water separation"],
        conclusion_template="FWKO tanks must be sized to provide adequate residence time for free water separation, based on anticipated flow rates and water cut.",
        reasoning_framework="""
        FWKO tanks are designed to separate free water from oil prior to further processing. The residence time is calculated based on the maximum expected flow rate and the water cut, ensuring that water droplets have sufficient time to settle. API 12D and API 12J provide sizing guidelines. The tank must be equipped with inlet diffusers to reduce turbulence and facilitate settling. Periodic inspection for sediment buildup and corrosion is required. Level control devices must be calibrated to prevent oil carryover. Environmental regulations mandate proper handling of separated water.
        """,
        key_factors=[
            "Residence time",
            "Flow rate",
            "Water cut",
            "Inlet diffuser design",
            "Level control",
            "Sediment management"
        ],
        primary_authority=[
            "API 12D",
            "API 12J",
            "EPA NPDES"
        ],
        burden_holder="Facility Designer",
        adversary_position="Insufficient residence time results in poor water separation and downstream processing issues.",
        counter_arguments=[
            "API-compliant sizing",
            "Level control calibration",
            "Sediment management plan"
        ],
        resolution_strategy="Design review and operational monitoring.",
        entity_scope="Tank Battery System",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 12D Section 2.2"
    ),
    DoctrineBlock(
        topic="Gun Barrel Wash Tank Settling Velocity",
        keywords=["gun barrel", "wash tank", "settling velocity", "water separation", "tank design"],
        conclusion_template="Gun barrel tanks must be designed to ensure that settling velocity of water droplets exceeds the upward velocity of oil, facilitating effective separation.",
        reasoning_framework="""
        Gun barrel tanks utilize gravity separation to remove water from oil. The settling velocity of water droplets is calculated using Stokes' Law, considering droplet size, density difference, and fluid viscosity. The tank's internal configuration, including inlet diffusers and baffles, is designed to minimize turbulence and maximize settling. API 12D provides guidance on tank sizing. The upward velocity of oil must not exceed the calculated settling velocity of water droplets. Regular inspection for sediment buildup and internal corrosion is necessary. Level control and sampling points must be installed for operational monitoring.
        """,
        key_factors=[
            "Settling velocity",
            "Tank configuration",
            "Inlet diffuser design",
            "Sediment management",
            "Level control"
        ],
        primary_authority=[
            "API 12D",
            "EPA NPDES",
            "ASME Section VIII"
        ],
        burden_holder="Process Engineer",
        adversary_position="Improper tank design leads to water carryover and oil losses.",
        counter_arguments=[
            "Stokes' Law calculations",
            "API 12D-compliant design",
            "Operational monitoring"
        ],
        resolution_strategy="Periodic performance testing and design validation.",
        entity_scope="Tank Battery System",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 12D Section 3.4"
    ),
    DoctrineBlock(
        topic="Stock Tank Atmospheric Storage",
        keywords=["stock tank", "atmospheric storage", "vapor loss", "tank design", "oil storage"],
        conclusion_template="Stock tanks must be designed for atmospheric storage of oil, with provisions for vapor loss mitigation and environmental compliance.",
        reasoning_framework="""
        Stock tanks store produced oil at atmospheric pressure. Design must comply with API 12B and API 650 standards, ensuring structural integrity and vapor loss mitigation. Tanks must be equipped with pressure-vacuum vents, flame arrestors, and vapor recovery systems where required. The sizing is based on anticipated production rates and surge volumes. Environmental regulations mandate secondary containment and spill prevention measures. Routine inspection for corrosion, leaks, and structural damage is required. Automatic tank gauging systems may be installed for inventory management.
        """,
        key_factors=[
            "Tank sizing",
            "Vapor loss mitigation",
            "Environmental compliance",
            "Secondary containment",
            "Inspection and maintenance"
        ],
        primary_authority=[
            "API 12B",
            "API 650",
            "EPA SPCC"
        ],
        burden_holder="Facility Manager",
        adversary_position="Improper tank design or maintenance leads to vapor emissions and environmental violations.",
        counter_arguments=[
            "API-compliant tank design",
            "Vapor recovery systems",
            "Routine inspection"
        ],
        resolution_strategy="Compliance audits and preventive maintenance.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 12B Section 2.1"
    ),
    DoctrineBlock(
        topic="LACT Lease Automatic Custody Transfer",
        keywords=["LACT", "lease automatic custody transfer", "metering", "oil sales", "measurement"],
        conclusion_template="LACT units must be designed and operated to ensure accurate custody transfer of oil, with calibrated meters and sampling systems.",
        reasoning_framework="""
        LACT units facilitate the automatic measurement and transfer of oil from lease to purchaser. The design must comply with API 21.1 and API 12F standards. Metering systems, typically Coriolis or turbine meters, must be calibrated regularly. Automatic sampling systems ensure representative BS&W measurement. Provisions for meter proving and verification are required. Security and audit trails must be maintained for custody transfer records. Environmental controls, such as spill prevention and vapor recovery, are mandatory. Periodic performance testing and calibration are essential for accuracy.
        """,
        key_factors=[
            "Meter calibration",
            "Sampling system",
            "Custody transfer records",
            "Environmental controls",
            "Performance testing"
        ],
        primary_authority=[
            "API 21.1",
            "API 12F",
            "EPA SPCC"
        ],
        burden_holder="Measurement Specialist",
        adversary_position="Inaccurate measurement leads to disputes and financial losses.",
        counter_arguments=[
            "Regular calibration",
            "Automatic sampling",
            "API-compliant records"
        ],
        resolution_strategy="Routine meter proving and audit trail maintenance.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 21.1 Section 5.2"
    ),
    DoctrineBlock(
        topic="Meter Proving (Coriolis, Turbine, PD)",
        keywords=["meter proving", "Coriolis", "turbine", "positive displacement", "accuracy", "measurement"],
        conclusion_template="Meter proving procedures must be conducted regularly for Coriolis, turbine, and PD meters to ensure measurement accuracy and compliance.",
        reasoning_framework="""
        Meter proving is essential for verifying the accuracy of flow meters used in custody transfer. Procedures must comply with API 5.6 and API 21.1 standards. Provers, such as displacement or master meters, are used to compare measured volumes. Calibration frequency is determined by regulatory requirements and operational history. Data from proving must be documented and retained for audit purposes. Environmental controls, such as spill prevention during proving, must be observed. Discrepancies must be investigated and resolved promptly.
        """,
        key_factors=[
            "Proving frequency",
            "Calibration procedures",
            "Documentation",
            "Environmental controls",
            "Discrepancy resolution"
        ],
        primary_authority=[
            "API 5.6",
            "API 21.1",
            "EPA SPCC"
        ],
        burden_holder="Measurement Specialist",
        adversary_position="Unproven meters may result in inaccurate custody transfer and regulatory violations.",
        counter_arguments=[
            "API-compliant proving procedures",
            "Audit documentation",
            "Prompt discrepancy resolution"
        ],
        resolution_strategy="Scheduled proving and regulatory audits.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 5.6 Section 4.1"
    ),
    DoctrineBlock(
        topic="BS&W Measurement",
        keywords=["BS&W", "basic sediment and water", "measurement", "sampling", "oil quality"],
        conclusion_template="BS&W measurement must be conducted using representative sampling and approved analytical methods to ensure oil quality compliance.",
        reasoning_framework="""
        BS&W (Basic Sediment and Water) measurement is critical for determining oil quality and compliance with sales contracts. Sampling must be representative, using automatic or manual methods compliant with API 8.2. Analytical methods, such as centrifuge or Karl Fischer titration, must be validated. Results must be documented and retained for audit purposes. Discrepancies in BS&W measurement can lead to disputes and financial losses. Calibration of sampling and analytical equipment is required. Environmental controls must be observed during sampling and disposal of waste.
        """,
        key_factors=[
            "Representative sampling",
            "Analytical method validation",
            "Documentation",
            "Equipment calibration",
            "Environmental controls"
        ],
        primary_authority=[
            "API 8.2",
            "API 21.1",
            "EPA SPCC"
        ],
        burden_holder="Laboratory Technician",
        adversary_position="Non-representative sampling leads to inaccurate BS&W measurement and disputes.",
        counter_arguments=[
            "API-compliant sampling",
            "Validated analytical methods",
            "Routine calibration"
        ],
        resolution_strategy="Audit of sampling and analytical procedures.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 8.2 Section 3.1"
    ),
    DoctrineBlock(
        topic="Vapor Recovery Unit (VRU) Flash Gas Compression",
        keywords=["VRU", "vapor recovery", "flash gas", "compression", "emissions", "tank battery"],
        conclusion_template="VRUs must be designed and operated to recover flash gas from tanks, minimizing emissions and maximizing gas capture efficiency.",
        reasoning_framework="""
        Vapor Recovery Units (VRUs) are used to capture flash gas emitted from stock tanks and process vessels. Design must comply with EPA CFR 40 Part 60 Subpart OOOOa and API 12B. VRUs must be sized based on anticipated gas volumes and operating pressures. Compression systems must be selected for reliability and efficiency. Controls must be installed to prevent overpressure and ensure safe operation. Routine monitoring of gas capture rates and emissions is required. Environmental compliance, including reporting and leak detection, is mandatory. Maintenance schedules must be established for compressors and associated equipment.
        """,
        key_factors=[
            "Gas volume estimation",
            "Compression system selection",
            "Emission monitoring",
            "Environmental compliance",
            "Maintenance schedule"
        ],
        primary_authority=[
            "EPA CFR 40 Part 60 Subpart OOOOa",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Specialist",
        adversary_position="Improper VRU operation leads to excessive emissions and regulatory penalties.",
        counter_arguments=[
            "EPA-compliant design",
            "Routine emission monitoring",
            "Maintenance schedule adherence"
        ],
        resolution_strategy="Environmental audits and operational reviews.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA CFR 40 Part 60 Subpart OOOOa Section 4.2"
    ),
    DoctrineBlock(
        topic="Tank Gauging (Automatic & Manual)",
        keywords=["tank gauging", "automatic", "manual", "inventory", "measurement", "stock tank"],
        conclusion_template="Tank gauging must be performed using calibrated automatic or manual systems, ensuring accurate inventory measurement and compliance.",
        reasoning_framework="""
        Tank gauging is essential for inventory management and custody transfer. Automatic gauging systems must be calibrated and maintained per API 3.1B. Manual gauging procedures must follow API 3.1A. Measurement accuracy is critical for sales and regulatory reporting. Environmental controls must be observed during manual gauging to prevent spills. Data from gauging must be documented and retained for audit purposes. Discrepancies must be investigated and resolved. Routine calibration and maintenance of gauging equipment is required.
        """,
        key_factors=[
            "Calibration of gauging systems",
            "Measurement accuracy",
            "Documentation",
            "Environmental controls",
            "Discrepancy resolution"
        ],
        primary_authority=[
            "API 3.1A",
            "API 3.1B",
            "EPA SPCC"
        ],
        burden_holder="Inventory Specialist",
        adversary_position="Inaccurate gauging leads to inventory discrepancies and financial losses.",
        counter_arguments=[
            "Routine calibration",
            "API-compliant procedures",
            "Audit documentation"
        ],
        resolution_strategy="Scheduled calibration and audit of gauging records.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 3.1B Section 2.3"
    ),
    DoctrineBlock(
        topic="Tank Battery Piping Header Manifold",
        keywords=["piping", "header", "manifold", "tank battery", "design", "flow control"],
        conclusion_template="Tank battery piping headers and manifolds must be designed for flexibility, flow control, and maintenance accessibility, complying with API and ASME standards.",
        reasoning_framework="""
        Piping headers and manifolds in tank batteries must be designed to accommodate varying flow rates and operational scenarios. API 12J and ASME B31.3 provide design standards. The layout must ensure accessibility for maintenance and minimize dead legs. Valves must be selected for reliability and compatibility with process fluids. Pressure ratings and corrosion allowances must be considered. Flow control devices, such as check valves and flow meters, must be installed. Environmental controls, such as secondary containment and leak detection, are required. Routine inspection and maintenance are essential for reliability.
        """,
        key_factors=[
            "Design flexibility",
            "Flow control",
            "Maintenance accessibility",
            "Pressure rating",
            "Corrosion allowance",
            "Environmental controls"
        ],
        primary_authority=[
            "API 12J",
            "ASME B31.3",
            "EPA SPCC"
        ],
        burden_holder="Facility Designer",
        adversary_position="Improper piping design leads to operational inefficiencies and environmental risks.",
        counter_arguments=[
            "API and ASME-compliant design",
            "Routine inspection",
            "Leak detection systems"
        ],
        resolution_strategy="Design review and preventive maintenance.",
        entity_scope="Tank Battery System",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.3 Section 5.1"
    ),
    DoctrineBlock(
        topic="Dump Valve Level Control (Pneumatic & Electric)",
        keywords=["dump valve", "level control", "pneumatic", "electric", "separator", "tank battery"],
        conclusion_template="Dump valves must be equipped with reliable level control systems, pneumatic or electric, to ensure proper operation and prevent process upsets.",
        reasoning_framework="""
        Dump valves control the discharge of separated fluids from vessels. Level control systems, pneumatic or electric, must be selected based on process requirements and reliability. API 12J and API 12L provide guidance on valve selection and control integration. Calibration and maintenance of level control devices are essential for accuracy. Redundant systems may be installed for critical applications. Environmental controls must be observed during maintenance. Operational data must be documented and reviewed periodically.
        """,
        key_factors=[
            "Level control reliability",
            "Valve selection",
            "Calibration",
            "Redundancy",
            "Environmental controls"
        ],
        primary_authority=[
            "API 12J",
            "API 12L",
            "EPA SPCC"
        ],
        burden_holder="Instrumentation Specialist",
        adversary_position="Unreliable level control leads to process upsets and environmental incidents.",
        counter_arguments=[
            "Routine calibration",
            "Redundant systems",
            "API-compliant devices"
        ],
        resolution_strategy="Scheduled maintenance and operational review.",
        entity_scope="Tank Battery System",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 12J Section 6.1"
    ),
    DoctrineBlock(
        topic="Glycol Dehydration (TEG Reboiler & Still Column)",
        keywords=["glycol dehydration", "TEG", "reboiler", "still column", "gas treatment", "water removal"],
        conclusion_template="Glycol dehydration units must be operated with optimal reboiler temperature and still column efficiency to ensure effective gas dehydration.",
        reasoning_framework="""
        Glycol dehydration units remove water vapor from natural gas using triethylene glycol (TEG). The reboiler must operate at temperatures sufficient to regenerate glycol without causing thermal degradation. The still column must efficiently strip water from glycol. API 12J and GPA 2261 provide operational guidelines. Monitoring of glycol purity and water dew point is required. Environmental controls, such as venting and spill prevention, must be implemented. Routine maintenance and calibration of instrumentation are essential for reliability.
        """,
        key_factors=[
            "Reboiler temperature",
            "Still column efficiency",
            "Glycol purity",
            "Water dew point monitoring",
            "Environmental controls"
        ],
        primary_authority=[
            "API 12J",
            "GPA 2261",
            "EPA SPCC"
        ],
        burden_holder="Process Engineer",
        adversary_position="Improper operation leads to insufficient dehydration and gas quality issues.",
        counter_arguments=[
            "Routine monitoring",
            "API and GPA-compliant operation",
            "Maintenance schedule"
        ],
        resolution_strategy="Operational review and performance testing.",
        entity_scope="Tank Battery System",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GPA 2261 Section 4.3"
    ),
    DoctrineBlock(
        topic="Amine Sweetening (H2S Removal Contact Tower)",
        keywords=["amine sweetening", "H2S removal", "contact tower", "gas treatment", "safety"],
        conclusion_template="Amine sweetening units must be operated with optimal contact tower conditions to ensure effective H2S removal and gas quality compliance.",
        reasoning_framework="""
        Amine sweetening units remove hydrogen sulfide (H2S) from natural gas using contact towers. Operating conditions, including amine concentration, temperature, and pressure, must be optimized for maximum removal efficiency. API 12J and GPA 2312 provide operational guidelines. Monitoring of H2S levels in treated gas is required. Environmental controls, such as venting and spill prevention, must be implemented. Routine maintenance and calibration of instrumentation are essential for reliability. Safety controls, including gas detection and emergency shutdown, must be installed.
        """,
        key_factors=[
            "Amine concentration",
            "Contact tower conditions",
            "H2S monitoring",
            "Environmental controls",
            "Safety controls"
        ],
        primary_authority=[
            "API 12J",
            "GPA 2312",
            "EPA SPCC"
        ],
        burden_holder="Process Engineer",
        adversary_position="Insufficient H2S removal leads to gas quality issues and safety risks.",
        counter_arguments=[
            "Routine monitoring",
            "API and GPA-compliant operation",
            "Safety controls"
        ],
        resolution_strategy="Operational review and performance testing.",
        entity_scope="Tank Battery System",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="GPA 2312 Section 5.2"
    ),
    DoctrineBlock(
        topic="Produced Water Treatment (Skim Tank & Flotation)",
        keywords=["produced water", "treatment", "skim tank", "flotation", "oil removal", "environmental"],
        conclusion_template="Produced water treatment must utilize skim tanks and flotation units to achieve regulatory oil removal standards before discharge or reuse.",
        reasoning_framework="""
        Produced water treatment involves removal of oil and solids using skim tanks and flotation units. API 12J and EPA NPDES provide regulatory standards for oil removal. Skim tanks must be designed for adequate residence time and equipped with inlet diffusers. Flotation units use gas or mechanical agitation to enhance oil removal. Monitoring of effluent quality is required. Environmental controls, such as secondary containment and spill prevention, must be implemented. Routine maintenance and calibration of instrumentation are essential for reliability.
        """,
        key_factors=[
            "Residence time",
            "Inlet diffuser design",
            "Flotation efficiency",
            "Effluent quality monitoring",
            "Environmental controls"
        ],
        primary_authority=[
            "API 12J",
            "EPA NPDES",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Specialist",
        adversary_position="Insufficient treatment leads to regulatory violations and environmental risks.",
        counter_arguments=[
            "API and EPA-compliant design",
            "Routine monitoring",
            "Maintenance schedule"
        ],
        resolution_strategy="Environmental audits and operational reviews.",
        entity_scope="Tank Battery System",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA NPDES Section 2.4"
    ),
    DoctrineBlock(
        topic="Chemical Injection Pump (Methanol & Paraffin)",
        keywords=["chemical injection", "pump", "methanol", "paraffin", "corrosion", "flow assurance"],
        conclusion_template="Chemical injection pumps must be selected and operated for reliable delivery of methanol and paraffin inhibitors, ensuring flow assurance and corrosion control.",
        reasoning_framework="""
        Chemical injection pumps deliver methanol and paraffin inhibitors to prevent hydrate formation and wax deposition. API 674 and API 675 provide pump selection and operational guidelines. Pumps must be sized for required dosage rates and compatible with injected chemicals. Calibration and maintenance are essential for reliability. Environmental controls, such as spill prevention and secondary containment, must be implemented. Monitoring of injection rates and chemical effectiveness is required. Routine inspection and documentation of pump performance are mandatory.
        """,
        key_factors=[
            "Pump sizing",
            "Chemical compatibility",
            "Injection rate monitoring",
            "Calibration",
            "Environmental controls"
        ],
        primary_authority=[
            "API 674",
            "API 675",
            "EPA SPCC"
        ],
        burden_holder="Flow Assurance Specialist",
        adversary_position="Improper injection leads to flow assurance issues and corrosion.",
        counter_arguments=[
            "API-compliant pump selection",
            "Routine calibration",
            "Injection rate monitoring"
        ],
        resolution_strategy="Scheduled maintenance and operational review.",
        entity_scope="Tank Battery System",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 675 Section 3.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Automation (RTU, SCADA, PLC)",
        keywords=["automation", "RTU", "SCADA", "PLC", "tank battery", "control system"],
        conclusion_template="Tank battery automation systems must be designed and maintained for reliable operation, data integrity, and safety compliance.",
        reasoning_framework="""
        Automation systems, including RTU, SCADA, and PLC, control tank battery operations. API 12J and ISA standards provide guidelines for system design and integration. Data integrity and cybersecurity are critical. Systems must be equipped with redundant communication and power supplies. Routine testing and calibration of sensors and actuators are required. Environmental controls, such as spill prevention and emergency shutdown, must be integrated. Documentation and audit trails must be maintained for compliance. Operator training is essential for safe and reliable operation.
        """,
        key_factors=[
            "System reliability",
            "Data integrity",
            "Cybersecurity",
            "Redundancy",
            "Environmental controls",
            "Operator training"
        ],
        primary_authority=[
            "API 12J",
            "ISA 84",
            "EPA SPCC"
        ],
        burden_holder="Automation Engineer",
        adversary_position="System failures lead to process upsets and safety risks.",
        counter_arguments=[
            "Redundant systems",
            "Routine testing",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and operational review.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 84 Section 4.1"
    ),
    DoctrineBlock(
        topic="Artificial Lift (ESP, Rod Pump, Gas Lift, Plunger)",
        keywords=["artificial lift", "ESP", "rod pump", "gas lift", "plunger", "production optimization"],
        conclusion_template="Artificial lift systems must be selected and operated based on reservoir and production characteristics to optimize oil recovery and minimize downtime.",
        reasoning_framework="""
        Artificial lift systems, including ESP, rod pump, gas lift, and plunger lift, are used to enhance oil recovery. Selection is based on reservoir properties, production rates, and well configuration. API 11B and API 11D provide guidelines for system selection and operation. Routine monitoring of lift performance and maintenance are required. Environmental controls, such as spill prevention and secondary containment, must be implemented. Operator training and documentation of lift performance are essential for reliability.
        """,
        key_factors=[
            "System selection",
            "Reservoir properties",
            "Production rates",
            "Maintenance schedule",
            "Environmental controls"
        ],
        primary_authority=[
            "API 11B",
            "API 11D",
            "EPA SPCC"
        ],
        burden_holder="Production Engineer",
        adversary_position="Improper lift selection leads to production losses and equipment failures.",
        counter_arguments=[
            "API-compliant selection",
            "Routine monitoring",
            "Maintenance schedule"
        ],
        resolution_strategy="Operational review and performance testing.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 11B Section 2.1"
    ),
    DoctrineBlock(
        topic="Wellhead Choke Bean (Fixed & Adjustable)",
        keywords=["wellhead", "choke bean", "fixed", "adjustable", "flow control", "pressure management"],
        conclusion_template="Wellhead choke beans must be selected and maintained for reliable flow control and pressure management, complying with API standards.",
        reasoning_framework="""
        Wellhead choke beans regulate flow and pressure from producing wells. Selection between fixed and adjustable chokes depends on operational requirements. API 6A provides standards for choke design and maintenance. Routine inspection and calibration are required for reliability. Environmental controls, such as spill prevention and secondary containment, must be implemented. Documentation of choke settings and performance is essential for audit purposes. Operator training is required for safe operation.
        """,
        key_factors=[
            "Choke selection",
            "Pressure management",
            "Inspection and calibration",
            "Environmental controls",
            "Operator training"
        ],
        primary_authority=[
            "API 6A",
            "EPA SPCC",
            "ASME Section VIII"
        ],
        burden_holder="Production Engineer",
        adversary_position="Improper choke selection or maintenance leads to flow control issues and safety risks.",
        counter_arguments=[
            "API-compliant selection",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and operational review.",
        entity_scope="Tank Battery System",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 6A Section 3.2"
    ),
    DoctrineBlock(
        topic="Flowline Gathering System Piping Design",
        keywords=["flowline", "gathering system", "piping", "design", "pressure", "corrosion"],
        conclusion_template="Flowline gathering system piping must be designed for anticipated flow rates, pressure, and corrosion resistance, complying with API and ASME standards.",
        reasoning_framework="""
        Flowline gathering systems transport produced fluids from wells to tank batteries. API 5L and ASME B31.4 provide standards for piping design. Sizing must accommodate maximum anticipated flow rates and pressure. Material selection must ensure corrosion resistance and compatibility with process fluids. Environmental controls, such as leak detection and secondary containment, must be implemented. Routine inspection and maintenance are required for reliability. Documentation of design and operational data is essential for compliance.
        """,
        key_factors=[
            "Flow rate",
            "Pressure rating",
            "Corrosion resistance",
            "Environmental controls",
            "Inspection and maintenance"
        ],
        primary_authority=[
            "API 5L",
            "ASME B31.4",
            "EPA SPCC"
        ],
        burden_holder="Facility Designer",
        adversary_position="Improper piping design leads to leaks, environmental risks, and operational inefficiencies.",
        counter_arguments=[
            "API and ASME-compliant design",
            "Routine inspection",
            "Leak detection systems"
        ],
        resolution_strategy="Design review and preventive maintenance.",
        entity_scope="Tank Battery System",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASME B31.4 Section 4.1"
    ),
    DoctrineBlock(
        topic="Tank Venting and Pressure Relief",
        keywords=["tank venting", "pressure relief", "stock tank", "safety", "emissions"],
        conclusion_template="Tank venting and pressure relief systems must be designed to prevent overpressure and minimize emissions, complying with API and EPA standards.",
        reasoning_framework="""
        Tank venting and pressure relief systems protect stock tanks from overpressure and minimize emissions. API 2000 provides guidance on vent sizing and relief valve selection. EPA CFR 40 Part 60 Subpart OOOOa mandates emission controls. Systems must be sized for maximum anticipated pressure and flow rates. Flame arrestors and pressure-vacuum vents must be installed. Routine inspection and maintenance are required for reliability. Documentation of venting and relief events is essential for compliance.
        """,
        key_factors=[
            "Vent sizing",
            "Relief valve selection",
            "Emission controls",
            "Inspection and maintenance",
            "Documentation"
        ],
        primary_authority=[
            "API 2000",
            "EPA CFR 40 Part 60 Subpart OOOOa",
            "ASME Section VIII"
        ],
        burden_holder="Facility Manager",
        adversary_position="Improper venting leads to overpressure, emissions, and safety risks.",
        counter_arguments=[
            "API and EPA-compliant design",
            "Routine inspection",
            "Documentation"
        ],
        resolution_strategy="Scheduled maintenance and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 2000 Section 3.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Secondary Containment Design",
        keywords=["secondary containment", "tank battery", "design", "spill prevention", "environmental"],
        conclusion_template="Secondary containment systems must be designed to capture spills and leaks from tank batteries, complying with EPA SPCC and API standards.",
        reasoning_framework="""
        Secondary containment systems, such as berms and dikes, are required to capture spills and leaks from tank batteries. EPA SPCC and API 12B provide design standards. Containment must be sized for the largest tank plus precipitation. Materials must be compatible with stored fluids and resistant to weathering. Routine inspection and maintenance are required for reliability. Documentation of containment integrity and spill events is essential for compliance. Environmental controls, such as leak detection and emergency response, must be integrated.
        """,
        key_factors=[
            "Containment sizing",
            "Material compatibility",
            "Inspection and maintenance",
            "Documentation",
            "Environmental controls"
        ],
        primary_authority=[
            "EPA SPCC",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Specialist",
        adversary_position="Insufficient containment leads to environmental violations and spill risks.",
        counter_arguments=[
            "EPA and API-compliant design",
            "Routine inspection",
            "Emergency response plan"
        ],
        resolution_strategy="Scheduled maintenance and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA SPCC Section 112.7"
    ),
    DoctrineBlock(
        topic="Tank Battery Fire Protection",
        keywords=["fire protection", "tank battery", "design", "safety", "emergency response"],
        conclusion_template="Tank battery fire protection systems must be designed and maintained for rapid response and compliance with API and NFPA standards.",
        reasoning_framework="""
        Fire protection systems, including foam, water spray, and dry chemical, are required for tank batteries. API 12B and NFPA 30 provide design and maintenance standards. Systems must be sized for anticipated fire scenarios and equipped with emergency response equipment. Routine inspection and maintenance are required for reliability. Operator training and emergency response drills are essential for preparedness. Documentation of fire protection system integrity and response events is required for compliance.
        """,
        key_factors=[
            "System sizing",
            "Emergency response equipment",
            "Inspection and maintenance",
            "Operator training",
            "Documentation"
        ],
        primary_authority=[
            "API 12B",
            "NFPA 30",
            "EPA SPCC"
        ],
        burden_holder="Safety Specialist",
        adversary_position="Insufficient fire protection leads to safety risks and regulatory violations.",
        counter_arguments=[
            "API and NFPA-compliant design",
            "Routine inspection",
            "Emergency response drills"
        ],
        resolution_strategy="Scheduled maintenance and emergency response training.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 30 Section 6.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Leak Detection and Monitoring",
        keywords=["leak detection", "monitoring", "tank battery", "environmental", "automation"],
        conclusion_template="Leak detection and monitoring systems must be installed and maintained for early identification of leaks, complying with EPA and API standards.",
        reasoning_framework="""
        Leak detection and monitoring systems, including sensors and automated alarms, are required for tank batteries. EPA SPCC and API 12B provide standards for system selection and installation. Systems must be calibrated and maintained for reliability. Routine inspection and documentation of leak detection events are required for compliance. Environmental controls, such as secondary containment and emergency response, must be integrated. Operator training is essential for rapid response.
        """,
        key_factors=[
            "System selection",
            "Calibration",
            "Inspection and maintenance",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "EPA SPCC",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Specialist",
        adversary_position="Insufficient leak detection leads to environmental violations and spill risks.",
        counter_arguments=[
            "EPA and API-compliant systems",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA SPCC Section 112.7"
    ),
    DoctrineBlock(
        topic="Tank Battery Overfill Prevention",
        keywords=["overfill prevention", "tank battery", "automation", "safety", "spill prevention"],
        conclusion_template="Overfill prevention systems must be installed and maintained to prevent spills and ensure safety, complying with API and EPA standards.",
        reasoning_framework="""
        Overfill prevention systems, including automatic shutoff valves and alarms, are required for tank batteries. API 2350 and EPA SPCC provide standards for system selection and installation. Systems must be calibrated and maintained for reliability. Routine inspection and documentation of overfill events are required for compliance. Operator training and emergency response procedures must be implemented. Environmental controls, such as secondary containment, must be integrated.
        """,
        key_factors=[
            "System selection",
            "Calibration",
            "Inspection and maintenance",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "API 2350",
            "EPA SPCC",
            "ASME Section VIII"
        ],
        burden_holder="Safety Specialist",
        adversary_position="Insufficient overfill prevention leads to spills and environmental violations.",
        counter_arguments=[
            "API and EPA-compliant systems",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 2350 Section 4.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Lightning Protection",
        keywords=["lightning protection", "tank battery", "safety", "design", "NFPA"],
        conclusion_template="Lightning protection systems must be installed and maintained for tank batteries, complying with API and NFPA standards.",
        reasoning_framework="""
        Lightning protection systems, including grounding and surge arrestors, are required for tank batteries. API 12B and NFPA 780 provide standards for system design and installation. Systems must be sized for anticipated lightning strikes and equipped with emergency response equipment. Routine inspection and maintenance are required for reliability. Documentation of lightning protection system integrity and response events is required for compliance. Operator training is essential for safety.
        """,
        key_factors=[
            "System sizing",
            "Grounding and surge arrestors",
            "Inspection and maintenance",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "API 12B",
            "NFPA 780",
            "EPA SPCC"
        ],
        burden_holder="Safety Specialist",
        adversary_position="Insufficient lightning protection leads to safety risks and regulatory violations.",
        counter_arguments=[
            "API and NFPA-compliant design",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and emergency response training.",
        entity_scope="Tank Battery System",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NFPA 780 Section 5.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Cathodic Protection",
        keywords=["cathodic protection", "tank battery", "corrosion", "design", "maintenance"],
        conclusion_template="Cathodic protection systems must be installed and maintained for tank batteries to prevent corrosion, complying with API and NACE standards.",
        reasoning_framework="""
        Cathodic protection systems, including sacrificial anodes and impressed current, are required for tank batteries. API 651 and NACE SP0169 provide standards for system design and installation. Systems must be sized for anticipated corrosion rates and equipped with monitoring devices. Routine inspection and maintenance are required for reliability. Documentation of cathodic protection system integrity and monitoring events is required for compliance. Operator training is essential for system operation.
        """,
        key_factors=[
            "System sizing",
            "Monitoring devices",
            "Inspection and maintenance",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "API 651",
            "NACE SP0169",
            "EPA SPCC"
        ],
        burden_holder="Corrosion Specialist",
        adversary_position="Insufficient cathodic protection leads to corrosion and environmental risks.",
        counter_arguments=[
            "API and NACE-compliant design",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 651 Section 3.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Insulation and Heat Tracing",
        keywords=["insulation", "heat tracing", "tank battery", "freeze protection", "design"],
        conclusion_template="Insulation and heat tracing systems must be installed and maintained for tank batteries to prevent freezing and ensure process reliability.",
        reasoning_framework="""
        Insulation and heat tracing systems are required for tank batteries in cold climates. API 12B and ASTM C680 provide standards for system design and installation. Systems must be sized for anticipated temperature drops and equipped with monitoring devices. Routine inspection and maintenance are required for reliability. Documentation of insulation and heat tracing system integrity and monitoring events is required for compliance. Operator training is essential for system operation.
        """,
        key_factors=[
            "System sizing",
            "Monitoring devices",
            "Inspection and maintenance",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "API 12B",
            "ASTM C680",
            "EPA SPCC"
        ],
        burden_holder="Facility Manager",
        adversary_position="Insufficient insulation and heat tracing leads to freezing and process upsets.",
        counter_arguments=[
            "API and ASTM-compliant design",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ASTM C680 Section 2.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Emergency Shutdown System (ESD)",
        keywords=["emergency shutdown", "ESD", "tank battery", "automation", "safety"],
        conclusion_template="Emergency shutdown systems must be installed and maintained for tank batteries to ensure rapid response and safety compliance.",
        reasoning_framework="""
        Emergency shutdown systems, including automated valves and alarms, are required for tank batteries. API 12J and ISA 84 provide standards for system design and installation. Systems must be sized for anticipated emergency scenarios and equipped with redundant power supplies. Routine inspection and maintenance are required for reliability. Documentation of ESD system integrity and response events is required for compliance. Operator training and emergency response drills are essential for preparedness.
        """,
        key_factors=[
            "System sizing",
            "Redundant power supplies",
            "Inspection and maintenance",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "API 12J",
            "ISA 84",
            "EPA SPCC"
        ],
        burden_holder="Safety Specialist",
        adversary_position="Insufficient ESD leads to safety risks and regulatory violations.",
        counter_arguments=[
            "API and ISA-compliant design",
            "Routine inspection",
            "Emergency response drills"
        ],
        resolution_strategy="Scheduled maintenance and emergency response training.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 84 Section 4.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Instrumentation Calibration",
        keywords=["instrumentation", "calibration", "tank battery", "measurement", "accuracy"],
        conclusion_template="Instrumentation used in tank batteries must be calibrated regularly to ensure measurement accuracy and compliance.",
        reasoning_framework="""
        Instrumentation, including pressure, temperature, and level sensors, must be calibrated regularly. API 21.1 and ISA standards provide guidelines for calibration procedures. Calibration frequency is determined by regulatory requirements and operational history. Documentation of calibration events is required for compliance. Routine inspection and maintenance are essential for reliability. Operator training is required for proper calibration procedures.
        """,
        key_factors=[
            "Calibration frequency",
            "Calibration procedures",
            "Documentation",
            "Inspection and maintenance",
            "Operator training"
        ],
        primary_authority=[
            "API 21.1",
            "ISA 51.1",
            "EPA SPCC"
        ],
        burden_holder="Instrumentation Specialist",
        adversary_position="Uncalibrated instrumentation leads to inaccurate measurement and regulatory violations.",
        counter_arguments=[
            "API and ISA-compliant calibration",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled calibration and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 51.1 Section 3.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Maintenance Management",
        keywords=["maintenance management", "tank battery", "preventive maintenance", "reliability", "documentation"],
        conclusion_template="Preventive maintenance management systems must be implemented for tank batteries to ensure reliability and compliance.",
        reasoning_framework="""
        Preventive maintenance management systems, including computerized maintenance management systems (CMMS), are required for tank batteries. API 12J and ISO 55000 provide standards for maintenance management. Systems must be equipped with scheduling, documentation, and reliability tracking. Routine inspection and maintenance are required for reliability. Documentation of maintenance events and reliability metrics is required for compliance. Operator training is essential for system operation.
        """,
        key_factors=[
            "Maintenance scheduling",
            "Documentation",
            "Reliability tracking",
            "Inspection and maintenance",
            "Operator training"
        ],
        primary_authority=[
            "API 12J",
            "ISO 55000",
            "EPA SPCC"
        ],
        burden_holder="Maintenance Manager",
        adversary_position="Insufficient maintenance management leads to reliability issues and regulatory violations.",
        counter_arguments=[
            "API and ISO-compliant system",
            "Routine inspection",
            "Operator training"
        ],
        resolution_strategy="Scheduled maintenance and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 55000 Section 4.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Personnel Training and Competency",
        keywords=["personnel training", "competency", "tank battery", "safety", "compliance"],
        conclusion_template="Personnel training and competency management systems must be implemented for tank batteries to ensure safety and regulatory compliance.",
        reasoning_framework="""
        Personnel training and competency management systems are required for tank batteries. API 12J and OSHA 1910 provide standards for training and competency assessment. Systems must be equipped with documentation, competency tracking, and refresher training. Routine training and assessment are required for safety and compliance. Documentation of training events and competency assessments is required for compliance. Operator training is essential for system operation and safety.
        """,
        key_factors=[
            "Training scheduling",
            "Competency assessment",
            "Documentation",
            "Refresher training",
            "Operator training"
        ],
        primary_authority=[
            "API 12J",
            "OSHA 1910",
            "EPA SPCC"
        ],
        burden_holder="Training Manager",
        adversary_position="Insufficient training leads to safety risks and regulatory violations.",
        counter_arguments=[
            "API and OSHA-compliant system",
            "Routine training",
            "Operator training"
        ],
        resolution_strategy="Scheduled training and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910 Section 4.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Incident Reporting and Investigation",
        keywords=["incident reporting", "investigation", "tank battery", "safety", "compliance"],
        conclusion_template="Incident reporting and investigation systems must be implemented for tank batteries to ensure safety and regulatory compliance.",
        reasoning_framework="""
        Incident reporting and investigation systems are required for tank batteries. API 12J and OSHA 1910 provide standards for reporting and investigation procedures. Systems must be equipped with documentation, root cause analysis, and corrective action tracking. Routine reporting and investigation are required for safety and compliance. Documentation of incident events and investigation outcomes is required for compliance. Operator training is essential for system operation and safety.
        """,
        key_factors=[
            "Reporting procedures",
            "Root cause analysis",
            "Corrective action tracking",
            "Documentation",
            "Operator training"
        ],
        primary_authority=[
            "API 12J",
            "OSHA 1910",
            "EPA SPCC"
        ],
        burden_holder="Safety Manager",
        adversary_position="Insufficient reporting and investigation leads to safety risks and regulatory violations.",
        counter_arguments=[
            "API and OSHA-compliant system",
            "Routine reporting",
            "Operator training"
        ],
        resolution_strategy="Scheduled reporting and compliance audits.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910 Section 5.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Environmental Compliance Management",
        keywords=["environmental compliance", "management", "tank battery", "EPA", "documentation"],
        conclusion_template="Environmental compliance management systems must be implemented for tank batteries to ensure regulatory compliance and minimize environmental risks.",
        reasoning_framework="""
        Environmental compliance management systems are required for tank batteries. EPA SPCC and API 12B provide standards for compliance management. Systems must be equipped with documentation, compliance tracking, and corrective action management. Routine compliance audits and documentation are required for regulatory compliance. Documentation of compliance events and corrective actions is required for compliance. Operator training is essential for system operation and environmental compliance.
        """,
        key_factors=[
            "Compliance tracking",
            "Documentation",
            "Corrective action management",
            "Compliance audits",
            "Operator training"
        ],
        primary_authority=[
            "EPA SPCC",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Manager",
        adversary_position="Insufficient compliance management leads to regulatory violations and environmental risks.",
        counter_arguments=[
            "EPA and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled compliance audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA SPCC Section 112.7"
    ),
    DoctrineBlock(
        topic="Tank Battery Process Safety Management",
        keywords=["process safety management", "tank battery", "PSM", "OSHA", "API"],
        conclusion_template="Process safety management systems must be implemented for tank batteries to ensure safety and regulatory compliance.",
        reasoning_framework="""
        Process safety management systems are required for tank batteries. OSHA 1910.119 and API 12J provide standards for PSM implementation. Systems must be equipped with hazard analysis, operating procedures, and management of change. Routine safety audits and documentation are required for regulatory compliance. Documentation of safety events and corrective actions is required for compliance. Operator training is essential for system operation and process safety.
        """,
        key_factors=[
            "Hazard analysis",
            "Operating procedures",
            "Management of change",
            "Safety audits",
            "Operator training"
        ],
        primary_authority=[
            "OSHA 1910.119",
            "API 12J",
            "EPA SPCC"
        ],
        burden_holder="Safety Manager",
        adversary_position="Insufficient PSM leads to safety risks and regulatory violations.",
        counter_arguments=[
            "OSHA and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled safety audits and management of change procedures.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="OSHA 1910.119 Section 4.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Waste Management",
        keywords=["waste management", "tank battery", "disposal", "EPA", "compliance"],
        conclusion_template="Waste management systems must be implemented for tank batteries to ensure proper disposal and regulatory compliance.",
        reasoning_framework="""
        Waste management systems are required for tank batteries. EPA RCRA and API 12B provide standards for waste disposal and management. Systems must be equipped with documentation, waste tracking, and disposal procedures. Routine waste audits and documentation are required for regulatory compliance. Documentation of waste disposal events and corrective actions is required for compliance. Operator training is essential for system operation and waste management.
        """,
        key_factors=[
            "Waste tracking",
            "Documentation",
            "Disposal procedures",
            "Waste audits",
            "Operator training"
        ],
        primary_authority=[
            "EPA RCRA",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Manager",
        adversary_position="Insufficient waste management leads to regulatory violations and environmental risks.",
        counter_arguments=[
            "EPA and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled waste audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA RCRA Section 4.2"
    ),
    DoctrineBlock(
        topic="Tank Battery Corrosion Monitoring",
        keywords=["corrosion monitoring", "tank battery", "inspection", "NACE", "API"],
        conclusion_template="Corrosion monitoring systems must be implemented for tank batteries to ensure integrity and regulatory compliance.",
        reasoning_framework="""
        Corrosion monitoring systems, including coupons and electronic sensors, are required for tank batteries. NACE SP0169 and API 651 provide standards for system selection and installation. Systems must be equipped with documentation, monitoring devices, and inspection procedures. Routine corrosion audits and documentation are required for regulatory compliance. Documentation of corrosion monitoring events and corrective actions is required for compliance. Operator training is essential for system operation and corrosion monitoring.
        """,
        key_factors=[
            "Monitoring devices",
            "Documentation",
            "Inspection procedures",
            "Corrosion audits",
            "Operator training"
        ],
        primary_authority=[
            "NACE SP0169",
            "API 651",
            "EPA SPCC"
        ],
        burden_holder="Corrosion Specialist",
        adversary_position="Insufficient corrosion monitoring leads to integrity issues and regulatory violations.",
        counter_arguments=[
            "NACE and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled corrosion audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="NACE SP0169 Section 5.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Emission Monitoring",
        keywords=["emission monitoring", "tank battery", "EPA", "compliance", "air quality"],
        conclusion_template="Emission monitoring systems must be implemented for tank batteries to ensure air quality and regulatory compliance.",
        reasoning_framework="""
        Emission monitoring systems, including sensors and automated alarms, are required for tank batteries. EPA CFR 40 Part 60 Subpart OOOOa and API 12B provide standards for system selection and installation. Systems must be equipped with documentation, monitoring devices, and inspection procedures. Routine emission audits and documentation are required for regulatory compliance. Documentation of emission monitoring events and corrective actions is required for compliance. Operator training is essential for system operation and emission monitoring.
        """,
        key_factors=[
            "Monitoring devices",
            "Documentation",
            "Inspection procedures",
            "Emission audits",
            "Operator training"
        ],
        primary_authority=[
            "EPA CFR 40 Part 60 Subpart OOOOa",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Specialist",
        adversary_position="Insufficient emission monitoring leads to air quality issues and regulatory violations.",
        counter_arguments=[
            "EPA and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled emission audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA CFR 40 Part 60 Subpart OOOOa Section 5.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Data Management and Reporting",
        keywords=["data management", "reporting", "tank battery", "compliance", "documentation"],
        conclusion_template="Data management and reporting systems must be implemented for tank batteries to ensure regulatory compliance and operational efficiency.",
        reasoning_framework="""
        Data management and reporting systems, including computerized data management systems, are required for tank batteries. API 21.1 and EPA SPCC provide standards for data management and reporting. Systems must be equipped with documentation, data tracking, and reporting procedures. Routine data audits and documentation are required for regulatory compliance. Documentation of data management events and corrective actions is required for compliance. Operator training is essential for system operation and data management.
        """,
        key_factors=[
            "Data tracking",
            "Documentation",
            "Reporting procedures",
            "Data audits",
            "Operator training"
        ],
        primary_authority=[
            "API 21.1",
            "EPA SPCC",
            "ASME Section VIII"
        ],
        burden_holder="Data Manager",
        adversary_position="Insufficient data management leads to compliance issues and operational inefficiencies.",
        counter_arguments=[
            "API and EPA-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled data audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="API 21.1 Section 6.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Process Optimization",
        keywords=["process optimization", "tank battery", "efficiency", "production", "automation"],
        conclusion_template="Process optimization systems must be implemented for tank batteries to ensure operational efficiency and maximize production.",
        reasoning_framework="""
        Process optimization systems, including automated control and monitoring, are required for tank batteries. API 12J and ISA 84 provide standards for process optimization. Systems must be equipped with documentation, optimization algorithms, and monitoring devices. Routine optimization audits and documentation are required for operational efficiency. Documentation of optimization events and corrective actions is required for compliance. Operator training is essential for system operation and process optimization.
        """,
        key_factors=[
            "Optimization algorithms",
            "Documentation",
            "Monitoring devices",
            "Optimization audits",
            "Operator training"
        ],
        primary_authority=[
            "API 12J",
            "ISA 84",
            "EPA SPCC"
        ],
        burden_holder="Process Engineer",
        adversary_position="Insufficient process optimization leads to operational inefficiencies and production losses.",
        counter_arguments=[
            "API and ISA-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled optimization audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 84 Section 5.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Water Disposal and Injection",
        keywords=["water disposal", "injection", "tank battery", "EPA", "compliance"],
        conclusion_template="Water disposal and injection systems must be implemented for tank batteries to ensure regulatory compliance and minimize environmental risks.",
        reasoning_framework="""
        Water disposal and injection systems are required for tank batteries. EPA UIC and API 12B provide standards for water disposal and injection. Systems must be equipped with documentation, injection tracking, and disposal procedures. Routine water audits and documentation are required for regulatory compliance. Documentation of water disposal and injection events and corrective actions is required for compliance. Operator training is essential for system operation and water management.
        """,
        key_factors=[
            "Injection tracking",
            "Documentation",
            "Disposal procedures",
            "Water audits",
            "Operator training"
        ],
        primary_authority=[
            "EPA UIC",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Water Management Specialist",
        adversary_position="Insufficient water disposal and injection leads to regulatory violations and environmental risks.",
        counter_arguments=[
            "EPA and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled water audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA UIC Section 4.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Chemical Management",
        keywords=["chemical management", "tank battery", "inventory", "EPA", "compliance"],
        conclusion_template="Chemical management systems must be implemented for tank batteries to ensure proper inventory and regulatory compliance.",
        reasoning_framework="""
        Chemical management systems are required for tank batteries. EPA EPCRA and API 12B provide standards for chemical inventory and management. Systems must be equipped with documentation, inventory tracking, and disposal procedures. Routine chemical audits and documentation are required for regulatory compliance. Documentation of chemical management events and corrective actions is required for compliance. Operator training is essential for system operation and chemical management.
        """,
        key_factors=[
            "Inventory tracking",
            "Documentation",
            "Disposal procedures",
            "Chemical audits",
            "Operator training"
        ],
        primary_authority=[
            "EPA EPCRA",
            "API 12B",
            "ASME Section VIII"
        ],
        burden_holder="Chemical Management Specialist",
        adversary_position="Insufficient chemical management leads to regulatory violations and environmental risks.",
        counter_arguments=[
            "EPA and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled chemical audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="EPA EPCRA Section 5.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Security Management",
        keywords=["security management", "tank battery", "access control", "API", "compliance"],
        conclusion_template="Security management systems must be implemented for tank batteries to ensure access control and regulatory compliance.",
        reasoning_framework="""
        Security management systems, including access control and surveillance, are required for tank batteries. API 12J and DHS CFATS provide standards for security management. Systems must be equipped with documentation, access tracking, and emergency response procedures. Routine security audits and documentation are required for regulatory compliance. Documentation of security management events and corrective actions is required for compliance. Operator training is essential for system operation and security management.
        """,
        key_factors=[
            "Access tracking",
            "Documentation",
            "Emergency response procedures",
            "Security audits",
            "Operator training"
        ],
        primary_authority=[
            "API 12J",
            "DHS CFATS",
            "EPA SPCC"
        ],
        burden_holder="Security Manager",
        adversary_position="Insufficient security management leads to safety risks and regulatory violations.",
        counter_arguments=[
            "API and DHS-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled security audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="DHS CFATS Section 4.1"
    ),
    DoctrineBlock(
        topic="Tank Battery Alarm Management",
        keywords=["alarm management", "tank battery", "automation", "ISA", "compliance"],
        conclusion_template="Alarm management systems must be implemented for tank batteries to ensure operational safety and regulatory compliance.",
        reasoning_framework="""
        Alarm management systems, including automated alarms and notification systems, are required for tank batteries. ISA 18.2 and API 12J provide standards for alarm management. Systems must be equipped with documentation, alarm tracking, and response procedures. Routine alarm audits and documentation are required for regulatory compliance. Documentation of alarm management events and corrective actions is required for compliance. Operator training is essential for system operation and alarm management.
        """,
        key_factors=[
            "Alarm tracking",
            "Documentation",
            "Response procedures",
            "Alarm audits",
            "Operator training"
        ],
        primary_authority=[
            "ISA 18.2",
            "API 12J",
            "EPA SPCC"
        ],
        burden_holder="Automation Engineer",
        adversary_position="Insufficient alarm management leads to safety risks and regulatory violations.",
        counter_arguments=[
            "ISA and API-compliant system",
            "Routine audits",
            "Operator training"
        ],
        resolution_strategy="Scheduled alarm audits and corrective action management.",
        entity_scope="Tank Battery System",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISA 18.2 Section 3.1"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
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