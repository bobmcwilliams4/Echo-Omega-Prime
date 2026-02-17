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
        topic="Hydraulic Pump Selection - Fixed vs Variable Displacement",
        keywords=["hydraulic pump", "fixed displacement", "variable displacement", "efficiency", "system demand"],
        conclusion_template="Select {pump_type} displacement pump based on system demand and efficiency requirements.",
        reasoning_framework=(
            "Hydraulic pump selection is governed by the system's flow and pressure requirements. "
            "Fixed displacement pumps provide constant flow regardless of system demand, making them suitable for applications "
            "with steady load profiles. Variable displacement pumps adjust flow and pressure dynamically, improving efficiency "
            "in systems with fluctuating demands. The selection process involves evaluating duty cycles, energy consumption, "
            "response time, and control complexity. Fixed pumps are generally simpler and less expensive, but may waste energy "
            "in variable load scenarios. Variable pumps offer greater control and efficiency but require more sophisticated "
            "controls and maintenance. Key standards such as ISO 4413 and manufacturer guidelines should be consulted. "
            "Consideration must also be given to compatibility with hydraulic fluid, noise levels, and heat generation. "
            "System integration, maintenance accessibility, and total cost of ownership are critical. "
            "The burden of proof lies with the designer to justify pump selection based on operational data and lifecycle analysis."
        ),
        key_factors=[
            "System flow and pressure requirements",
            "Load profile (steady vs variable)",
            "Energy efficiency",
            "Control complexity",
            "Cost and maintenance",
            "Noise and heat generation",
            "Fluid compatibility"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules and safety requirements",
            "Manufacturer technical datasheets",
            "NFPA/T2.6.1"
        ],
        burden_holder="System designer",
        adversary_position="Variable displacement pumps are unnecessarily complex for simple systems.",
        counter_arguments=[
            "Variable pumps reduce energy consumption in fluctuating load scenarios.",
            "Fixed pumps may lead to excessive heat and wasted energy."
        ],
        resolution_strategy="Conduct a lifecycle cost analysis and match pump type to application profile.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 5.2.2"
    ),
    DoctrineBlock(
        topic="Hydraulic Cylinder Sizing - Bore and Rod Diameter Selection",
        keywords=["hydraulic cylinder", "bore diameter", "rod diameter", "force calculation", "buckling"],
        conclusion_template="Specify cylinder bore and rod diameter to meet force requirements and prevent buckling.",
        reasoning_framework=(
            "Cylinder sizing is based on required force, stroke length, and operating pressure. "
            "The bore diameter determines the output force (F = P × A), where P is pressure and A is area. "
            "Rod diameter is selected to prevent buckling under compressive loads, using Euler's formula and considering "
            "stroke length and mounting configuration. Safety factors must be applied per ISO 6020/6022. "
            "Material selection, seal compatibility, and corrosion resistance are essential. "
            "Oversizing increases cost and reduces efficiency; undersizing risks failure. "
            "Designers must validate calculations with real-world load cases and consider dynamic effects such as pressure spikes. "
            "Documentation should include force calculations, buckling analysis, and reference to applicable standards."
        ),
        key_factors=[
            "Required force",
            "Operating pressure",
            "Stroke length",
            "Buckling risk",
            "Mounting configuration",
            "Material and seal selection",
            "Safety factors"
        ],
        primary_authority=[
            "ISO 6020: Hydraulic cylinders — Mounting dimensions",
            "ISO 6022: Hydraulic cylinders — Heavy-duty",
            "NFPA/T3.6.39"
        ],
        burden_holder="Design engineer",
        adversary_position="Oversized cylinders increase cost and reduce efficiency.",
        counter_arguments=[
            "Undersized cylinders risk catastrophic failure.",
            "Proper sizing ensures safety and reliability."
        ],
        resolution_strategy="Apply safety factors and validate with buckling analysis and force calculations.",
        entity_scope="MECH11 hydraulic actuators",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 6020 Section 4.1"
    ),
    DoctrineBlock(
        topic="Directional Control Valve Selection - Spool vs Poppet Design",
        keywords=["directional control valve", "spool valve", "poppet valve", "leakage", "response time"],
        conclusion_template="Choose {valve_type} valve based on leakage tolerance and response time requirements.",
        reasoning_framework=(
            "Directional control valves regulate fluid flow direction in hydraulic circuits. "
            "Spool valves offer precise control and are suitable for applications requiring frequent cycling and low leakage. "
            "Poppet valves provide fast response and minimal leakage, ideal for safety-critical and load-holding functions. "
            "Selection criteria include maximum allowable leakage, response time, pressure rating, and contamination tolerance. "
            "ISO 5598 and manufacturer specifications guide selection. "
            "Consideration must be given to valve actuation (manual, solenoid, pilot), mounting style, and compatibility with system fluid. "
            "The designer must balance performance, reliability, and cost. "
            "Maintenance requirements and ease of replacement are also relevant."
        ),
        key_factors=[
            "Leakage tolerance",
            "Response time",
            "Pressure rating",
            "Contamination tolerance",
            "Actuation method",
            "Mounting style"
        ],
        primary_authority=[
            "ISO 5598: Fluid power systems and components — Vocabulary",
            "Manufacturer valve datasheets"
        ],
        burden_holder="System integrator",
        adversary_position="Spool valves are unsuitable for load-holding due to internal leakage.",
        counter_arguments=[
            "Poppet valves may be slower in high-cycle applications.",
            "Spool valves offer finer control in proportional systems."
        ],
        resolution_strategy="Match valve design to application requirements and validate with performance testing.",
        entity_scope="MECH11 hydraulic controls",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 5598 Section 3.2"
    ),
    DoctrineBlock(
        topic="Hydraulic Fluid Selection - ISO VG Grade and Fluid Type",
        keywords=["hydraulic fluid", "ISO VG", "fluid type", "viscosity", "compatibility"],
        conclusion_template="Select hydraulic fluid with appropriate ISO VG grade and type for system compatibility and performance.",
        reasoning_framework=(
            "Hydraulic fluid selection is critical for system performance, longevity, and safety. "
            "ISO VG grade defines viscosity, which must match pump and actuator requirements for optimal lubrication and heat dissipation. "
            "Fluid type (mineral oil, synthetic, biodegradable) is chosen based on environmental regulations, compatibility with seals and materials, "
            "and operating temperature range. Manufacturer recommendations and ISO 6743-4 classification should be followed. "
            "Contamination risk, oxidation stability, and fire resistance are additional factors. "
            "Fluid selection impacts maintenance intervals and system reliability. "
            "Documentation must include fluid specification, compatibility analysis, and reference to applicable standards."
        ),
        key_factors=[
            "Viscosity (ISO VG grade)",
            "Fluid type",
            "Seal and material compatibility",
            "Operating temperature",
            "Oxidation stability",
            "Environmental regulations"
        ],
        primary_authority=[
            "ISO 6743-4: Hydraulic fluids classification",
            "Manufacturer fluid recommendations"
        ],
        burden_holder="Maintenance engineer",
        adversary_position="Mineral oils are unsuitable for environmentally sensitive applications.",
        counter_arguments=[
            "Synthetic fluids may be cost-prohibitive.",
            "Biodegradable fluids may have limited compatibility."
        ],
        resolution_strategy="Conduct compatibility and environmental impact analysis; select fluid per ISO and manufacturer guidance.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 6743-4 Section 2"
    ),
    DoctrineBlock(
        topic="Contamination Control - ISO 4406 Cleanliness Codes and Filtration",
        keywords=["contamination control", "ISO 4406", "cleanliness code", "filtration", "particle count"],
        conclusion_template="Implement filtration to achieve target ISO 4406 cleanliness code for hydraulic system reliability.",
        reasoning_framework=(
            "Contamination is the leading cause of hydraulic system failure. "
            "ISO 4406 cleanliness codes specify allowable particle counts for hydraulic fluid, guiding filter selection and maintenance intervals. "
            "Filtration strategy includes selecting filter rating (micron size), placement (pressure, return, offline), and monitoring methods. "
            "System designers must analyze contamination sources, fluid flow rates, and critical component sensitivity. "
            "Continuous monitoring (particle counters) and scheduled maintenance are required to maintain target cleanliness. "
            "Manufacturer recommendations and ISO 16889 filter testing standards apply. "
            "Documentation must include cleanliness targets, filter specifications, and maintenance procedures."
        ),
        key_factors=[
            "Target ISO 4406 code",
            "Filter rating and placement",
            "Contamination sources",
            "Monitoring methods",
            "Maintenance intervals"
        ],
        primary_authority=[
            "ISO 4406: Hydraulic fluid cleanliness",
            "ISO 16889: Filter testing",
            "Manufacturer filter datasheets"
        ],
        burden_holder="Maintenance team",
        adversary_position="High-efficiency filtration increases system cost and complexity.",
        counter_arguments=[
            "Poor filtration leads to premature component failure.",
            "High-efficiency filters reduce long-term maintenance costs."
        ],
        resolution_strategy="Balance filtration cost with reliability requirements; monitor cleanliness and adjust strategy as needed.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4406 Section 4"
    ),
    DoctrineBlock(
        topic="Hydraulic Circuit Design - Open Center vs Closed Center Systems",
        keywords=["hydraulic circuit", "open center", "closed center", "energy efficiency", "system configuration"],
        conclusion_template="Select {circuit_type} center hydraulic circuit based on energy efficiency and application requirements.",
        reasoning_framework=(
            "Hydraulic circuit configuration determines system efficiency, control complexity, and component selection. "
            "Open center systems route fluid through a continuous path, suitable for simple, low-cost applications with limited control requirements. "
            "Closed center systems isolate fluid flow, enabling simultaneous operation of multiple actuators and improved energy efficiency. "
            "Selection criteria include number of actuators, load profile, control precision, and integration with electrohydraulic controls. "
            "ISO 4413 and manufacturer guidelines provide design parameters. "
            "System designers must evaluate trade-offs in cost, complexity, and performance. "
            "Documentation should include circuit schematics, component selection rationale, and reference to standards."
        ),
        key_factors=[
            "Number of actuators",
            "Control precision",
            "Energy efficiency",
            "System complexity",
            "Cost"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer circuit design guides"
        ],
        burden_holder="System architect",
        adversary_position="Closed center systems are unnecessarily complex for simple applications.",
        counter_arguments=[
            "Open center circuits waste energy in multi-actuator systems.",
            "Closed center circuits enable advanced control and efficiency."
        ],
        resolution_strategy="Match circuit type to application profile and validate with energy efficiency analysis.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 5.3"
    ),
    DoctrineBlock(
        topic="Accumulator Sizing - Bladder and Piston Types for Energy Storage",
        keywords=["accumulator sizing", "bladder accumulator", "piston accumulator", "energy storage", "pressure fluctuations"],
        conclusion_template="Size accumulator and select type (bladder or piston) based on energy storage and pressure fluctuation requirements.",
        reasoning_framework=(
            "Accumulators store hydraulic energy and dampen pressure fluctuations. "
            "Sizing is based on required energy storage, system pressure range, and response time. "
            "Bladder accumulators offer rapid response and are suitable for pulsation damping; piston accumulators handle larger volumes and higher pressures. "
            "Selection criteria include gas pre-charge pressure, fluid compatibility, mounting orientation, and maintenance accessibility. "
            "ISO 7752 and manufacturer datasheets provide sizing formulas and guidelines. "
            "Safety considerations include pressure relief devices and compliance with local regulations. "
            "Documentation must include accumulator sizing calculations, type selection rationale, and reference to standards."
        ),
        key_factors=[
            "Required energy storage",
            "Pressure range",
            "Response time",
            "Fluid compatibility",
            "Mounting orientation",
            "Maintenance accessibility"
        ],
        primary_authority=[
            "ISO 7752: Hydraulic accumulators",
            "Manufacturer accumulator datasheets"
        ],
        burden_holder="System designer",
        adversary_position="Bladder accumulators are unsuitable for high-volume applications.",
        counter_arguments=[
            "Piston accumulators may be slower in response.",
            "Bladder accumulators offer superior pulsation damping."
        ],
        resolution_strategy="Evaluate energy storage and response requirements; select accumulator type per ISO and manufacturer guidance.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.88,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 7752 Section 3.1"
    ),
    DoctrineBlock(
        topic="Pressure Drop and Heat Generation in Hydraulic Systems",
        keywords=["pressure drop", "heat generation", "hydraulic efficiency", "fluid velocity", "component sizing"],
        conclusion_template="Minimize pressure drop and heat generation through proper component sizing and fluid velocity management.",
        reasoning_framework=(
            "Pressure drop across hydraulic components leads to heat generation, reducing system efficiency and risking component damage. "
            "Designers must calculate expected pressure losses using Darcy-Weisbach and empirical formulas, considering fluid velocity, pipe diameter, and component restrictions. "
            "Heat generation is managed by optimizing flow paths, selecting appropriate pipe sizes, and installing heat exchangers if necessary. "
            "ISO 4413 and manufacturer guidelines provide acceptable limits for pressure drop and temperature rise. "
            "Continuous monitoring and maintenance are required to prevent excessive heat buildup. "
            "Documentation must include pressure drop calculations, heat management strategies, and reference to standards."
        ),
        key_factors=[
            "Fluid velocity",
            "Pipe diameter",
            "Component restrictions",
            "Heat exchanger sizing",
            "Operating temperature limits"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer component datasheets"
        ],
        burden_holder="System designer",
        adversary_position="Oversized pipes increase cost and reduce system responsiveness.",
        counter_arguments=[
            "Undersized pipes cause excessive pressure drop and heat generation.",
            "Proper sizing balances cost and performance."
        ],
        resolution_strategy="Optimize component sizing and fluid velocity; validate with pressure drop and heat calculations.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 6.2"
    ),
    DoctrineBlock(
        topic="Electrohydraulic Motion Control - Proportional and Servo Valves",
        keywords=["electrohydraulic control", "proportional valve", "servo valve", "precision", "response time"],
        conclusion_template="Select proportional or servo valve based on required precision and response time for motion control.",
        reasoning_framework=(
            "Electrohydraulic motion control requires valves capable of precise flow and pressure regulation. "
            "Proportional valves provide variable control suitable for most industrial applications; servo valves offer higher precision and faster response, "
            "ideal for robotics and aerospace. Selection criteria include required accuracy, response time, control signal compatibility, and contamination tolerance. "
            "ISO 10770 and manufacturer datasheets guide selection. "
            "System integration with electronic controllers and feedback sensors is critical. "
            "Maintenance requirements and contamination sensitivity must be considered. "
            "Documentation should include valve selection rationale, control system integration plan, and reference to standards."
        ),
        key_factors=[
            "Required precision",
            "Response time",
            "Control signal compatibility",
            "Contamination tolerance",
            "Maintenance requirements"
        ],
        primary_authority=[
            "ISO 10770: Electrohydraulic control",
            "Manufacturer valve datasheets"
        ],
        burden_holder="Control engineer",
        adversary_position="Servo valves are unnecessarily expensive for standard applications.",
        counter_arguments=[
            "Proportional valves may lack required precision for advanced motion control.",
            "Servo valves offer unmatched accuracy and speed."
        ],
        resolution_strategy="Match valve type to application requirements; validate with performance testing and cost analysis.",
        entity_scope="MECH11 hydraulic controls",
        confidence=0.87,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 10770 Section 2"
    ),
    DoctrineBlock(
        topic="Hydraulic System Troubleshooting - Diagnostic Methodology",
        keywords=["hydraulic troubleshooting", "diagnostics", "failure analysis", "systematic approach", "root cause"],
        conclusion_template="Apply systematic diagnostic methodology to identify and resolve hydraulic system failures.",
        reasoning_framework=(
            "Troubleshooting hydraulic systems requires a structured approach to identify root causes of failures. "
            "Initial steps include reviewing system schematics, checking fluid levels and cleanliness, and inspecting for leaks. "
            "Diagnostic tools such as pressure gauges, flow meters, and particle counters are used to isolate issues. "
            "Common failure modes include pump wear, valve malfunction, contamination, and seal degradation. "
            "ISO 4413 and manufacturer troubleshooting guides provide step-by-step procedures. "
            "Documentation must include failure analysis, corrective actions, and reference to standards. "
            "Continuous improvement is achieved by tracking failure trends and updating maintenance protocols."
        ),
        key_factors=[
            "Systematic diagnostic process",
            "Use of diagnostic tools",
            "Failure mode identification",
            "Corrective action documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer troubleshooting guides"
        ],
        burden_holder="Maintenance technician",
        adversary_position="Ad-hoc troubleshooting is sufficient for minor failures.",
        counter_arguments=[
            "Structured methodology reduces downtime and prevents recurring issues.",
            "Ad-hoc approaches miss root causes."
        ],
        resolution_strategy="Implement systematic diagnostic protocols and document corrective actions.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 7.1"
    ),
    DoctrineBlock(
        topic="Predictive Maintenance - Oil Analysis and Vibration Monitoring",
        keywords=["predictive maintenance", "oil analysis", "vibration monitoring", "condition-based", "failure prevention"],
        conclusion_template="Implement predictive maintenance using oil analysis and vibration monitoring to prevent hydraulic system failures.",
        reasoning_framework=(
            "Predictive maintenance leverages condition-based monitoring to prevent hydraulic system failures. "
            "Oil analysis detects contamination, wear particles, and fluid degradation, guiding maintenance actions. "
            "Vibration monitoring identifies mechanical issues in pumps and motors before catastrophic failure. "
            "ISO 17359 and manufacturer guidelines outline best practices for implementing predictive maintenance. "
            "Data collection and trend analysis enable proactive interventions, reducing downtime and extending component life. "
            "Documentation must include monitoring protocols, analysis results, and maintenance actions."
        ),
        key_factors=[
            "Oil analysis protocols",
            "Vibration monitoring",
            "Data collection and trend analysis",
            "Proactive maintenance actions",
            "Documentation"
        ],
        primary_authority=[
            "ISO 17359: Condition monitoring and diagnostics",
            "Manufacturer maintenance guides"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Predictive maintenance is cost-prohibitive for small systems.",
        counter_arguments=[
            "Condition-based monitoring reduces long-term costs and downtime.",
            "Small systems benefit from early failure detection."
        ],
        resolution_strategy="Evaluate cost-benefit and scale predictive maintenance to system size and criticality.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 17359 Section 5"
    ),
    DoctrineBlock(
        topic="Hydraulic Hose Selection - Pressure Rating and Flexibility",
        keywords=["hydraulic hose", "pressure rating", "flexibility", "hose selection", "burst pressure"],
        conclusion_template="Select hydraulic hose with appropriate pressure rating and flexibility for system safety and performance.",
        reasoning_framework=(
            "Hydraulic hose selection is based on working pressure, burst pressure, flexibility, and compatibility with hydraulic fluid. "
            "ISO 1436 and manufacturer datasheets provide pressure rating guidelines and minimum bend radius specifications. "
            "Hose routing must avoid excessive bends and abrasion, and fittings must match hose type and pressure requirements. "
            "Safety factors are applied to prevent hose failure. "
            "Documentation must include hose specifications, routing diagrams, and reference to standards."
        ),
        key_factors=[
            "Working and burst pressure",
            "Flexibility (minimum bend radius)",
            "Fluid compatibility",
            "Abrasion resistance",
            "Fitting selection"
        ],
        primary_authority=[
            "ISO 1436: Hydraulic hose specifications",
            "Manufacturer hose datasheets"
        ],
        burden_holder="System designer",
        adversary_position="Flexible hoses are less durable than rigid piping.",
        counter_arguments=[
            "Flexible hoses enable easier routing and vibration absorption.",
            "Proper selection ensures durability."
        ],
        resolution_strategy="Apply pressure and flexibility criteria; validate with manufacturer and ISO guidelines.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 1436 Section 3"
    ),
    DoctrineBlock(
        topic="Hydraulic Reservoir Design - Volume and Contamination Management",
        keywords=["hydraulic reservoir", "volume", "contamination management", "tank design", "fluid retention"],
        conclusion_template="Design hydraulic reservoir with adequate volume and contamination management features.",
        reasoning_framework=(
            "Reservoir design ensures sufficient fluid supply, heat dissipation, and contamination management. "
            "Volume is typically 3-5 times pump flow per minute, per ISO 4413 and manufacturer recommendations. "
            "Features such as baffles, drain ports, and air breathers reduce contamination and promote fluid retention. "
            "Material selection and corrosion resistance are critical. "
            "Documentation must include reservoir sizing calculations, contamination control features, and reference to standards."
        ),
        key_factors=[
            "Reservoir volume",
            "Contamination management",
            "Heat dissipation",
            "Material selection",
            "Corrosion resistance"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer reservoir design guides"
        ],
        burden_holder="System designer",
        adversary_position="Oversized reservoirs increase cost and footprint.",
        counter_arguments=[
            "Undersized reservoirs risk fluid starvation and overheating.",
            "Proper sizing balances cost and performance."
        ],
        resolution_strategy="Apply sizing formulas and contamination management features per ISO and manufacturer guidance.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.89,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 6.3"
    ),
    DoctrineBlock(
        topic="Hydraulic Seal Selection - Material and Compatibility",
        keywords=["hydraulic seal", "material selection", "compatibility", "seal failure", "temperature range"],
        conclusion_template="Select hydraulic seals based on material compatibility and operating temperature range.",
        reasoning_framework=(
            "Seal selection is critical for preventing leaks and ensuring system longevity. "
            "Materials such as NBR, FKM, and PTFE are chosen based on fluid compatibility, temperature range, and pressure rating. "
            "ISO 3601 and manufacturer datasheets provide material selection guidelines. "
            "Seal failure modes include extrusion, chemical degradation, and wear. "
            "Documentation must include seal material specifications, compatibility analysis, and reference to standards."
        ),
        key_factors=[
            "Material compatibility",
            "Operating temperature",
            "Pressure rating",
            "Seal failure modes",
            "Manufacturer recommendations"
        ],
        primary_authority=[
            "ISO 3601: Hydraulic seals",
            "Manufacturer seal datasheets"
        ],
        burden_holder="Design engineer",
        adversary_position="Standard seals are adequate for all hydraulic fluids.",
        counter_arguments=[
            "Special fluids require compatible seal materials.",
            "High temperatures demand advanced materials."
        ],
        resolution_strategy="Conduct compatibility analysis and select seal materials per ISO and manufacturer guidance.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 3601 Section 2"
    ),
    DoctrineBlock(
        topic="Hydraulic Motor Selection - Torque and Speed Requirements",
        keywords=["hydraulic motor", "torque", "speed", "motor selection", "application requirements"],
        conclusion_template="Select hydraulic motor based on torque and speed requirements for application.",
        reasoning_framework=(
            "Hydraulic motor selection is based on required torque, speed, and duty cycle. "
            "ISO 3019 and manufacturer datasheets provide sizing formulas and performance curves. "
            "Fluid compatibility, mounting configuration, and maintenance requirements must be considered. "
            "Documentation must include motor selection rationale, sizing calculations, and reference to standards."
        ),
        key_factors=[
            "Required torque",
            "Speed",
            "Duty cycle",
            "Fluid compatibility",
            "Mounting configuration"
        ],
        primary_authority=[
            "ISO 3019: Hydraulic motors",
            "Manufacturer motor datasheets"
        ],
        burden_holder="System designer",
        adversary_position="High-torque motors are unnecessarily large for most applications.",
        counter_arguments=[
            "Undersized motors risk overload and failure.",
            "Proper sizing ensures reliability."
        ],
        resolution_strategy="Apply sizing formulas and validate with manufacturer and ISO guidelines.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 3019 Section 3"
    ),
    DoctrineBlock(
        topic="Hydraulic Pressure Relief - Valve Selection and Setting",
        keywords=["pressure relief", "valve selection", "pressure setting", "system protection", "safety"],
        conclusion_template="Select and set pressure relief valve to protect hydraulic system from overpressure.",
        reasoning_framework=(
            "Pressure relief valves protect hydraulic systems from overpressure, preventing component damage and ensuring safety. "
            "ISO 5781 and manufacturer datasheets provide selection and setting guidelines. "
            "Valve setting must be above normal operating pressure but below maximum component rating. "
            "Documentation must include valve selection rationale, pressure setting calculations, and reference to standards."
        ),
        key_factors=[
            "Operating and maximum pressure",
            "Valve selection",
            "Pressure setting",
            "System protection",
            "Safety compliance"
        ],
        primary_authority=[
            "ISO 5781: Hydraulic pressure relief valves",
            "Manufacturer valve datasheets"
        ],
        burden_holder="System designer",
        adversary_position="Pressure relief valves are unnecessary in low-pressure systems.",
        counter_arguments=[
            "Unexpected pressure spikes can damage components.",
            "Relief valves are essential for safety."
        ],
        resolution_strategy="Set relief valve per ISO and manufacturer guidelines; document selection and settings.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 5781 Section 2"
    ),
    DoctrineBlock(
        topic="Hydraulic Pump Drive - Coupling and Alignment",
        keywords=["pump drive", "coupling", "alignment", "shaft misalignment", "vibration"],
        conclusion_template="Ensure proper coupling and alignment of hydraulic pump drive to prevent vibration and shaft misalignment.",
        reasoning_framework=(
            "Proper coupling and alignment of hydraulic pump drives prevent vibration, shaft misalignment, and premature failure. "
            "ISO 10441 and manufacturer datasheets provide alignment tolerances and coupling selection guidelines. "
            "Flexible couplings accommodate minor misalignments; rigid couplings require precise alignment. "
            "Documentation must include coupling selection, alignment procedures, and reference to standards."
        ),
        key_factors=[
            "Coupling type",
            "Alignment tolerances",
            "Vibration prevention",
            "Shaft misalignment",
            "Maintenance procedures"
        ],
        primary_authority=[
            "ISO 10441: Couplings for hydraulic pumps",
            "Manufacturer coupling datasheets"
        ],
        burden_holder="Installation technician",
        adversary_position="Flexible couplings are unnecessary for precision installations.",
        counter_arguments=[
            "Minor misalignments are inevitable in real-world installations.",
            "Flexible couplings reduce maintenance."
        ],
        resolution_strategy="Select coupling and align per ISO and manufacturer guidelines; document procedures.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 10441 Section 3"
    ),
    DoctrineBlock(
        topic="Hydraulic System Startup - Commissioning Procedures",
        keywords=["system startup", "commissioning", "hydraulic procedures", "initial testing", "safety checks"],
        conclusion_template="Follow commissioning procedures for hydraulic system startup, including initial testing and safety checks.",
        reasoning_framework=(
            "Commissioning procedures ensure safe and reliable hydraulic system startup. "
            "ISO 4413 and manufacturer guidelines specify initial testing, fluid filling, air bleeding, and safety checks. "
            "Documentation must include commissioning checklist, test results, and reference to standards."
        ),
        key_factors=[
            "Commissioning checklist",
            "Initial testing",
            "Fluid filling",
            "Air bleeding",
            "Safety checks"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer commissioning guides"
        ],
        burden_holder="Commissioning engineer",
        adversary_position="Commissioning procedures are unnecessary for simple systems.",
        counter_arguments=[
            "Proper commissioning prevents startup failures.",
            "Safety checks are essential."
        ],
        resolution_strategy="Follow ISO and manufacturer commissioning procedures; document results.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 8"
    ),
    DoctrineBlock(
        topic="Hydraulic Fluid Temperature Control - Cooling and Heating",
        keywords=["fluid temperature control", "cooling", "heating", "thermal management", "operating temperature"],
        conclusion_template="Implement cooling and heating strategies to maintain hydraulic fluid within operating temperature range.",
        reasoning_framework=(
            "Fluid temperature control ensures hydraulic system performance and longevity. "
            "ISO 4413 and manufacturer guidelines specify acceptable temperature ranges and cooling/heating methods. "
            "Heat exchangers, heaters, and insulation are used to maintain fluid temperature. "
            "Documentation must include temperature control strategy, component selection, and reference to standards."
        ),
        key_factors=[
            "Operating temperature range",
            "Cooling methods",
            "Heating methods",
            "Component selection",
            "Thermal management"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer temperature control guides"
        ],
        burden_holder="System designer",
        adversary_position="Temperature control is unnecessary for moderate climates.",
        counter_arguments=[
            "Extreme temperatures degrade fluid and components.",
            "Proper control ensures reliability."
        ],
        resolution_strategy="Implement temperature control per ISO and manufacturer guidelines; document strategy.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 6.4"
    ),
    DoctrineBlock(
        topic="Hydraulic System Noise Reduction - Component Selection and Layout",
        keywords=["noise reduction", "component selection", "system layout", "vibration", "acoustic management"],
        conclusion_template="Reduce hydraulic system noise through component selection and optimized layout.",
        reasoning_framework=(
            "Noise reduction in hydraulic systems is achieved by selecting low-noise components, optimizing layout, and managing vibration. "
            "ISO 4413 and manufacturer guidelines provide noise measurement and reduction strategies. "
            "Isolation mounts, flexible hoses, and acoustic enclosures are used to minimize noise transmission. "
            "Documentation must include noise reduction strategy, component selection, and reference to standards."
        ),
        key_factors=[
            "Component noise rating",
            "System layout",
            "Vibration management",
            "Acoustic enclosures",
            "Noise measurement"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer noise reduction guides"
        ],
        burden_holder="System designer",
        adversary_position="Noise reduction measures increase cost and complexity.",
        counter_arguments=[
            "Excessive noise leads to operator fatigue and regulatory issues.",
            "Proper measures improve safety and comfort."
        ],
        resolution_strategy="Implement noise reduction per ISO and manufacturer guidelines; document strategy.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 6.5"
    ),
    DoctrineBlock(
        topic="Hydraulic System Safety - Emergency Shutdown and Interlocks",
        keywords=["system safety", "emergency shutdown", "interlocks", "fail-safe", "operator protection"],
        conclusion_template="Implement emergency shutdown and interlock systems for hydraulic system safety and operator protection.",
        reasoning_framework=(
            "Emergency shutdown and interlock systems ensure hydraulic system safety and operator protection. "
            "ISO 4413 and manufacturer guidelines specify fail-safe mechanisms, interlocks, and emergency stop procedures. "
            "Safety circuits must be tested during commissioning. "
            "Documentation must include safety system design, test results, and reference to standards."
        ),
        key_factors=[
            "Emergency shutdown",
            "Interlock design",
            "Fail-safe mechanisms",
            "Operator protection",
            "Safety circuit testing"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer safety guides"
        ],
        burden_holder="Safety engineer",
        adversary_position="Safety systems are redundant in low-risk environments.",
        counter_arguments=[
            "Unexpected failures can occur in any environment.",
            "Safety systems are essential for operator protection."
        ],
        resolution_strategy="Implement safety systems per ISO and manufacturer guidelines; document design and testing.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.97,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 9"
    ),
    DoctrineBlock(
        topic="Hydraulic System Documentation - Schematics and Maintenance Records",
        keywords=["system documentation", "schematics", "maintenance records", "traceability", "compliance"],
        conclusion_template="Maintain comprehensive schematics and maintenance records for hydraulic system traceability and compliance.",
        reasoning_framework=(
            "Comprehensive documentation ensures hydraulic system traceability, maintenance, and regulatory compliance. "
            "ISO 4413 and manufacturer guidelines specify documentation requirements, including schematics, maintenance records, and component datasheets. "
            "Documentation must be updated after modifications and accessible to maintenance personnel. "
            "Proper records support troubleshooting and audits."
        ),
        key_factors=[
            "Schematics",
            "Maintenance records",
            "Component datasheets",
            "Traceability",
            "Regulatory compliance"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer documentation guides"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Documentation is unnecessary for small systems.",
        counter_arguments=[
            "Proper records prevent errors and support troubleshooting.",
            "Documentation is required for compliance."
        ],
        resolution_strategy="Maintain documentation per ISO and manufacturer guidelines; ensure accessibility.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 10"
    ),
    DoctrineBlock(
        topic="Hydraulic System Integration - PLC and HMI Interface",
        keywords=["system integration", "PLC", "HMI", "interface", "automation"],
        conclusion_template="Integrate hydraulic system with PLC and HMI for automation and monitoring.",
        reasoning_framework=(
            "Integration with PLC and HMI enables automation and real-time monitoring of hydraulic systems. "
            "ISO 4413 and manufacturer guidelines specify interface protocols, wiring standards, and programming requirements. "
            "System designers must ensure compatibility, reliability, and cybersecurity. "
            "Documentation must include interface schematics, programming logic, and reference to standards."
        ),
        key_factors=[
            "PLC compatibility",
            "HMI interface",
            "Wiring standards",
            "Programming requirements",
            "Cybersecurity"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer integration guides"
        ],
        burden_holder="Automation engineer",
        adversary_position="Automation is unnecessary for manual systems.",
        counter_arguments=[
            "Automation improves reliability and monitoring.",
            "Manual systems lack real-time diagnostics."
        ],
        resolution_strategy="Integrate per ISO and manufacturer guidelines; document interface and logic.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 11"
    ),
    DoctrineBlock(
        topic="Hydraulic System Expansion - Modular Design and Scalability",
        keywords=["system expansion", "modular design", "scalability", "future-proof", "upgrade"],
        conclusion_template="Design hydraulic system with modularity and scalability for future expansion and upgrades.",
        reasoning_framework=(
            "Modular design and scalability enable future expansion and upgrades of hydraulic systems. "
            "ISO 4413 and manufacturer guidelines specify modular component selection and interface standards. "
            "Designers must plan for future capacity, compatibility, and ease of integration. "
            "Documentation must include expansion plan, modular component specifications, and reference to standards."
        ),
        key_factors=[
            "Modular component selection",
            "Interface standards",
            "Future capacity planning",
            "Compatibility",
            "Ease of integration"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer modular design guides"
        ],
        burden_holder="System architect",
        adversary_position="Modular design increases initial cost and complexity.",
        counter_arguments=[
            "Scalability reduces long-term upgrade costs.",
            "Modular systems enable rapid expansion."
        ],
        resolution_strategy="Design for modularity and scalability per ISO and manufacturer guidelines; document expansion plan.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 12"
    ),
    DoctrineBlock(
        topic="Hydraulic System Energy Efficiency - Variable Speed Drives",
        keywords=["energy efficiency", "variable speed drive", "pump control", "power consumption", "optimization"],
        conclusion_template="Implement variable speed drives for hydraulic pumps to optimize energy efficiency.",
        reasoning_framework=(
            "Variable speed drives (VSDs) optimize energy efficiency by matching pump speed to system demand. "
            "ISO 4413 and manufacturer guidelines specify VSD integration and control strategies. "
            "Energy consumption is reduced during low-demand periods, extending component life and reducing heat generation. "
            "Documentation must include VSD selection, control logic, and reference to standards."
        ),
        key_factors=[
            "Pump speed control",
            "Energy consumption",
            "System demand matching",
            "Component life extension",
            "Heat reduction"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer VSD guides"
        ],
        burden_holder="System designer",
        adversary_position="VSDs are unnecessary for constant demand systems.",
        counter_arguments=[
            "Variable demand benefits from VSD optimization.",
            "Energy savings justify investment."
        ],
        resolution_strategy="Implement VSDs per ISO and manufacturer guidelines; document selection and control logic.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.91,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 13"
    ),
    DoctrineBlock(
        topic="Hydraulic System Remote Monitoring - IoT Integration",
        keywords=["remote monitoring", "IoT", "integration", "data analytics", "predictive maintenance"],
        conclusion_template="Integrate IoT for remote monitoring and predictive maintenance of hydraulic systems.",
        reasoning_framework=(
            "IoT integration enables remote monitoring and predictive maintenance of hydraulic systems. "
            "ISO 4413 and manufacturer guidelines specify sensor selection, data transmission protocols, and cybersecurity measures. "
            "Data analytics support proactive maintenance and performance optimization. "
            "Documentation must include IoT integration plan, sensor specifications, and reference to standards."
        ),
        key_factors=[
            "Sensor selection",
            "Data transmission protocols",
            "Cybersecurity",
            "Data analytics",
            "Maintenance optimization"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer IoT integration guides"
        ],
        burden_holder="Automation engineer",
        adversary_position="IoT integration is unnecessary for non-critical systems.",
        counter_arguments=[
            "Remote monitoring reduces downtime and maintenance costs.",
            "IoT enables real-time diagnostics."
        ],
        resolution_strategy="Integrate IoT per ISO and manufacturer guidelines; document plan and specifications.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.90,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 14"
    ),
    DoctrineBlock(
        topic="Hydraulic System Environmental Compliance - Fluid Disposal and Spill Prevention",
        keywords=["environmental compliance", "fluid disposal", "spill prevention", "regulations", "safety"],
        conclusion_template="Ensure hydraulic system environmental compliance through proper fluid disposal and spill prevention measures.",
        reasoning_framework=(
            "Environmental compliance requires proper disposal of hydraulic fluids and implementation of spill prevention measures. "
            "ISO 14001 and manufacturer guidelines specify disposal protocols and containment strategies. "
            "Designers must ensure compliance with local regulations and document disposal and spill prevention procedures."
        ),
        key_factors=[
            "Fluid disposal protocols",
            "Spill prevention",
            "Containment strategies",
            "Regulatory compliance",
            "Documentation"
        ],
        primary_authority=[
            "ISO 14001: Environmental management",
            "Manufacturer environmental compliance guides"
        ],
        burden_holder="Safety manager",
        adversary_position="Environmental measures increase operational cost.",
        counter_arguments=[
            "Non-compliance risks fines and environmental damage.",
            "Proper measures ensure safety and sustainability."
        ],
        resolution_strategy="Implement disposal and spill prevention per ISO and manufacturer guidelines; document procedures.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14001 Section 5"
    ),
    DoctrineBlock(
        topic="Hydraulic System Redundancy - Backup Pumps and Circuits",
        keywords=["system redundancy", "backup pump", "redundant circuit", "reliability", "failover"],
        conclusion_template="Design hydraulic system with redundancy (backup pumps and circuits) for reliability and failover capability.",
        reasoning_framework=(
            "Redundancy in hydraulic systems ensures reliability and failover capability. "
            "ISO 4413 and manufacturer guidelines specify backup pump and circuit design. "
            "Critical applications require redundant systems to prevent downtime. "
            "Documentation must include redundancy plan, backup component specifications, and reference to standards."
        ),
        key_factors=[
            "Backup pump selection",
            "Redundant circuit design",
            "Reliability",
            "Failover capability",
            "Critical application assessment"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer redundancy guides"
        ],
        burden_holder="System designer",
        adversary_position="Redundancy increases cost and complexity.",
        counter_arguments=[
            "Critical systems require failover capability.",
            "Redundancy prevents costly downtime."
        ],
        resolution_strategy="Design redundancy per ISO and manufacturer guidelines; document plan and specifications.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 15"
    ),
    DoctrineBlock(
        topic="Hydraulic System Pressure Testing - Verification and Certification",
        keywords=["pressure testing", "verification", "certification", "hydrostatic test", "safety"],
        conclusion_template="Conduct pressure testing for hydraulic system verification and certification of safety.",
        reasoning_framework=(
            "Pressure testing verifies hydraulic system integrity and certifies safety. "
            "ISO 4413 and manufacturer guidelines specify hydrostatic test procedures and pressure limits. "
            "Documentation must include test results, certification records, and reference to standards."
        ),
        key_factors=[
            "Hydrostatic test procedures",
            "Pressure limits",
            "Test results",
            "Certification records",
            "Safety compliance"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer pressure testing guides"
        ],
        burden_holder="Quality engineer",
        adversary_position="Pressure testing is unnecessary for low-pressure systems.",
        counter_arguments=[
            "Unexpected pressure spikes can occur in any system.",
            "Testing ensures safety and compliance."
        ],
        resolution_strategy="Conduct testing per ISO and manufacturer guidelines; document results and certification.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 16"
    ),
    DoctrineBlock(
        topic="Hydraulic System Leak Detection - Monitoring and Response",
        keywords=["leak detection", "monitoring", "response", "fluid loss", "system integrity"],
        conclusion_template="Implement leak detection and response protocols to maintain hydraulic system integrity.",
        reasoning_framework=(
            "Leak detection and response protocols maintain hydraulic system integrity and prevent fluid loss. "
            "ISO 4413 and manufacturer guidelines specify monitoring methods and response procedures. "
            "Sensors, visual inspections, and maintenance logs are used to detect leaks. "
            "Documentation must include detection strategy, response plan, and reference to standards."
        ),
        key_factors=[
            "Monitoring methods",
            "Response procedures",
            "Sensor selection",
            "Maintenance logs",
            "System integrity"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer leak detection guides"
        ],
        burden_holder="Maintenance technician",
        adversary_position="Leak detection is unnecessary for small systems.",
        counter_arguments=[
            "Leaks cause environmental and operational issues.",
            "Early detection prevents costly repairs."
        ],
        resolution_strategy="Implement detection and response per ISO and manufacturer guidelines; document strategy.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 17"
    ),
    DoctrineBlock(
        topic="Hydraulic System Emergency Procedures - Fire and Flood Response",
        keywords=["emergency procedures", "fire response", "flood response", "safety", "contingency planning"],
        conclusion_template="Establish emergency procedures for hydraulic system fire and flood response.",
        reasoning_framework=(
            "Emergency procedures for fire and flood response ensure hydraulic system safety and contingency planning. "
            "ISO 4413 and manufacturer guidelines specify response protocols and safety measures. "
            "Documentation must include emergency plan, response protocols, and reference to standards."
        ),
        key_factors=[
            "Fire response protocols",
            "Flood response protocols",
            "Contingency planning",
            "Safety measures",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer emergency response guides"
        ],
        burden_holder="Safety manager",
        adversary_position="Emergency procedures are unnecessary for low-risk environments.",
        counter_arguments=[
            "Unexpected emergencies can occur in any environment.",
            "Proper procedures ensure safety."
        ],
        resolution_strategy="Establish procedures per ISO and manufacturer guidelines; document plan and protocols.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 18"
    ),
    DoctrineBlock(
        topic="Hydraulic System Training - Operator and Maintenance Personnel",
        keywords=["system training", "operator", "maintenance personnel", "competency", "safety"],
        conclusion_template="Provide hydraulic system training for operators and maintenance personnel to ensure competency and safety.",
        reasoning_framework=(
            "Training for operators and maintenance personnel ensures competency and hydraulic system safety. "
            "ISO 4413 and manufacturer guidelines specify training requirements and competency assessment. "
            "Documentation must include training records, competency evaluations, and reference to standards."
        ),
        key_factors=[
            "Training requirements",
            "Competency assessment",
            "Safety",
            "Documentation",
            "Continuous improvement"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer training guides"
        ],
        burden_holder="Training manager",
        adversary_position="Training is unnecessary for experienced personnel.",
        counter_arguments=[
            "Continuous training prevents errors and accidents.",
            "New technologies require updated training."
        ],
        resolution_strategy="Provide training per ISO and manufacturer guidelines; document records and evaluations.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 19"
    ),
    DoctrineBlock(
        topic="Hydraulic System Upgrade - Retrofit and Modernization",
        keywords=["system upgrade", "retrofit", "modernization", "performance improvement", "component replacement"],
        conclusion_template="Plan hydraulic system upgrade through retrofit and modernization for performance improvement.",
        reasoning_framework=(
            "Retrofit and modernization improve hydraulic system performance and extend lifespan. "
            "ISO 4413 and manufacturer guidelines specify upgrade procedures and component compatibility. "
            "Documentation must include upgrade plan, component specifications, and reference to standards."
        ),
        key_factors=[
            "Upgrade plan",
            "Component compatibility",
            "Performance improvement",
            "Documentation",
            "Lifecycle extension"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer upgrade guides"
        ],
        burden_holder="System designer",
        adversary_position="Upgrades are unnecessary for functioning systems.",
        counter_arguments=[
            "Modernization improves efficiency and reliability.",
            "Upgrades extend system life."
        ],
        resolution_strategy="Plan upgrades per ISO and manufacturer guidelines; document plan and specifications.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 20"
    ),
    DoctrineBlock(
        topic="Hydraulic System Lifecycle Management - Asset Tracking and Replacement Planning",
        keywords=["lifecycle management", "asset tracking", "replacement planning", "system longevity", "maintenance"],
        conclusion_template="Implement lifecycle management with asset tracking and replacement planning for hydraulic system longevity.",
        reasoning_framework=(
            "Lifecycle management ensures hydraulic system longevity through asset tracking and replacement planning. "
            "ISO 4413 and manufacturer guidelines specify asset management protocols and replacement criteria. "
            "Documentation must include asset records, replacement schedules, and reference to standards."
        ),
        key_factors=[
            "Asset tracking",
            "Replacement planning",
            "System longevity",
            "Maintenance",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer lifecycle management guides"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Lifecycle management is unnecessary for small systems.",
        counter_arguments=[
            "Proper management prevents unexpected failures.",
            "Asset tracking supports maintenance planning."
        ],
        resolution_strategy="Implement lifecycle management per ISO and manufacturer guidelines; document records and schedules.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 21"
    ),
    DoctrineBlock(
        topic="Hydraulic System Cybersecurity - Network and Data Protection",
        keywords=["cybersecurity", "network protection", "data protection", "automation", "remote monitoring"],
        conclusion_template="Implement cybersecurity measures for hydraulic system network and data protection.",
        reasoning_framework=(
            "Cybersecurity measures protect hydraulic system networks and data from unauthorized access and cyber threats. "
            "ISO 27001 and manufacturer guidelines specify network protection protocols and data encryption. "
            "Documentation must include cybersecurity plan, network architecture, and reference to standards."
        ),
        key_factors=[
            "Network protection",
            "Data encryption",
            "Access control",
            "Cyber threat assessment",
            "Documentation"
        ],
        primary_authority=[
            "ISO 27001: Information security management",
            "Manufacturer cybersecurity guides"
        ],
        burden_holder="IT manager",
        adversary_position="Cybersecurity is unnecessary for isolated systems.",
        counter_arguments=[
            "Remote monitoring exposes systems to cyber threats.",
            "Proper measures prevent data breaches."
        ],
        resolution_strategy="Implement cybersecurity per ISO and manufacturer guidelines; document plan and architecture.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 27001 Section 6"
    ),
    DoctrineBlock(
        topic="Hydraulic System Spare Parts Management - Inventory and Procurement",
        keywords=["spare parts management", "inventory", "procurement", "downtime prevention", "maintenance"],
        conclusion_template="Manage spare parts inventory and procurement to prevent hydraulic system downtime.",
        reasoning_framework=(
            "Spare parts management prevents hydraulic system downtime by ensuring timely availability of critical components. "
            "ISO 4413 and manufacturer guidelines specify inventory protocols and procurement procedures. "
            "Documentation must include inventory records, procurement schedules, and reference to standards."
        ),
        key_factors=[
            "Inventory management",
            "Procurement procedures",
            "Downtime prevention",
            "Critical component identification",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer spare parts guides"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Spare parts management is unnecessary for reliable systems.",
        counter_arguments=[
            "Unexpected failures require immediate replacement.",
            "Proper management reduces downtime."
        ],
        resolution_strategy="Manage inventory and procurement per ISO and manufacturer guidelines; document records and schedules.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 22"
    ),
    DoctrineBlock(
        topic="Hydraulic System Compliance Audits - Internal and External Review",
        keywords=["compliance audit", "internal review", "external review", "regulatory compliance", "documentation"],
        conclusion_template="Conduct internal and external compliance audits for hydraulic system regulatory adherence.",
        reasoning_framework=(
            "Compliance audits ensure hydraulic system regulatory adherence through internal and external review. "
            "ISO 19011 and manufacturer guidelines specify audit protocols and documentation requirements. "
            "Documentation must include audit reports, corrective actions, and reference to standards."
        ),
        key_factors=[
            "Audit protocols",
            "Internal review",
            "External review",
            "Regulatory compliance",
            "Documentation"
        ],
        primary_authority=[
            "ISO 19011: Guidelines for auditing management systems",
            "Manufacturer compliance audit guides"
        ],
        burden_holder="Compliance manager",
        adversary_position="Audits are unnecessary for compliant systems.",
        counter_arguments=[
            "Regular audits prevent regulatory violations.",
            "Audits identify improvement opportunities."
        ],
        resolution_strategy="Conduct audits per ISO and manufacturer guidelines; document reports and actions.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.95,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 19011 Section 4"
    ),
    DoctrineBlock(
        topic="Hydraulic System Failure Analysis - Root Cause Investigation",
        keywords=["failure analysis", "root cause", "investigation", "corrective action", "system reliability"],
        conclusion_template="Conduct root cause investigation for hydraulic system failures and implement corrective actions.",
        reasoning_framework=(
            "Root cause investigation improves hydraulic system reliability by identifying and correcting failure sources. "
            "ISO 4413 and manufacturer guidelines specify investigation protocols and corrective action procedures. "
            "Documentation must include investigation reports, corrective actions, and reference to standards."
        ),
        key_factors=[
            "Investigation protocols",
            "Root cause identification",
            "Corrective action",
            "System reliability",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer failure analysis guides"
        ],
        burden_holder="Reliability engineer",
        adversary_position="Root cause analysis is unnecessary for minor failures.",
        counter_arguments=[
            "Minor failures may indicate systemic issues.",
            "Proper analysis prevents recurring problems."
        ],
        resolution_strategy="Conduct investigation per ISO and manufacturer guidelines; document reports and actions.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.96,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 23"
    ),
    DoctrineBlock(
        topic="Hydraulic System Retrofit for Environmental Upgrades - Fluid and Component Replacement",
        keywords=["retrofit", "environmental upgrade", "fluid replacement", "component replacement", "compliance"],
        conclusion_template="Retrofit hydraulic system with environmentally compliant fluids and components.",
        reasoning_framework=(
            "Retrofit for environmental upgrades involves replacing hydraulic fluids and components to meet regulatory compliance. "
            "ISO 14001 and manufacturer guidelines specify fluid and component selection. "
            "Documentation must include retrofit plan, specifications, and reference to standards."
        ),
        key_factors=[
            "Fluid selection",
            "Component compatibility",
            "Regulatory compliance",
            "Retrofit plan",
            "Documentation"
        ],
        primary_authority=[
            "ISO 14001: Environmental management",
            "Manufacturer retrofit guides"
        ],
        burden_holder="System designer",
        adversary_position="Retrofit is unnecessary for non-critical applications.",
        counter_arguments=[
            "Environmental compliance is mandatory.",
            "Retrofit improves sustainability."
        ],
        resolution_strategy="Retrofit per ISO and manufacturer guidelines; document plan and specifications.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14001 Section 6"
    ),
    DoctrineBlock(
        topic="Hydraulic System Condition Monitoring - Sensor Integration and Data Analysis",
        keywords=["condition monitoring", "sensor integration", "data analysis", "performance optimization", "maintenance"],
        conclusion_template="Integrate sensors and data analysis for hydraulic system condition monitoring and performance optimization.",
        reasoning_framework=(
            "Condition monitoring improves hydraulic system performance and maintenance through sensor integration and data analysis. "
            "ISO 17359 and manufacturer guidelines specify sensor selection and data analysis protocols. "
            "Documentation must include monitoring plan, sensor specifications, and reference to standards."
        ),
        key_factors=[
            "Sensor selection",
            "Data analysis protocols",
            "Performance optimization",
            "Maintenance",
            "Documentation"
        ],
        primary_authority=[
            "ISO 17359: Condition monitoring and diagnostics",
            "Manufacturer condition monitoring guides"
        ],
        burden_holder="Maintenance engineer",
        adversary_position="Condition monitoring is unnecessary for reliable systems.",
        counter_arguments=[
            "Monitoring prevents unexpected failures.",
            "Data analysis supports proactive maintenance."
        ],
        resolution_strategy="Integrate monitoring per ISO and manufacturer guidelines; document plan and specifications.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 17359 Section 6"
    ),
    DoctrineBlock(
        topic="Hydraulic System Fluid Sampling - Protocols and Analysis",
        keywords=["fluid sampling", "protocols", "analysis", "contamination detection", "maintenance"],
        conclusion_template="Conduct hydraulic fluid sampling and analysis per protocols for contamination detection and maintenance planning.",
        reasoning_framework=(
            "Fluid sampling and analysis detect contamination and guide maintenance planning. "
            "ISO 4407 and manufacturer guidelines specify sampling protocols and analysis methods. "
            "Documentation must include sampling records, analysis results, and reference to standards."
        ),
        key_factors=[
            "Sampling protocols",
            "Analysis methods",
            "Contamination detection",
            "Maintenance planning",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4407: Hydraulic fluid analysis",
            "Manufacturer fluid sampling guides"
        ],
        burden_holder="Maintenance technician",
        adversary_position="Sampling is unnecessary for clean systems.",
        counter_arguments=[
            "Contamination can occur unexpectedly.",
            "Regular sampling prevents failures."
        ],
        resolution_strategy="Conduct sampling and analysis per ISO and manufacturer guidelines; document records and results.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4407 Section 4"
    ),
    DoctrineBlock(
        topic="Hydraulic System Component Standardization - Interchangeability and Procurement",
        keywords=["component standardization", "interchangeability", "procurement", "inventory", "maintenance"],
        conclusion_template="Standardize hydraulic system components for interchangeability and streamlined procurement.",
        reasoning_framework=(
            "Component standardization improves interchangeability and streamlines procurement and maintenance. "
            "ISO 4413 and manufacturer guidelines specify standardization protocols and component selection. "
            "Documentation must include standardization plan, component specifications, and reference to standards."
        ),
        key_factors=[
            "Standardization protocols",
            "Interchangeability",
            "Procurement",
            "Inventory management",
            "Maintenance"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer standardization guides"
        ],
        burden_holder="Procurement manager",
        adversary_position="Standardization limits design flexibility.",
        counter_arguments=[
            "Interchangeable components reduce downtime.",
            "Standardization simplifies inventory."
        ],
        resolution_strategy="Standardize components per ISO and manufacturer guidelines; document plan and specifications.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 24"
    ),
    DoctrineBlock(
        topic="Hydraulic System Warranty Management - Claims and Documentation",
        keywords=["warranty management", "claims", "documentation", "component failure", "regulatory compliance"],
        conclusion_template="Manage hydraulic system warranty claims and documentation to ensure regulatory compliance and component replacement.",
        reasoning_framework=(
            "Warranty management ensures timely claims and regulatory compliance for hydraulic system component failures. "
            "ISO 4413 and manufacturer guidelines specify warranty protocols and documentation requirements. "
            "Documentation must include claim records, replacement documentation, and reference to standards."
        ),
        key_factors=[
            "Warranty protocols",
            "Claim records",
            "Replacement documentation",
            "Regulatory compliance",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer warranty guides"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Warranty management is unnecessary for reliable systems.",
        counter_arguments=[
            "Unexpected failures require warranty claims.",
            "Proper documentation ensures compliance."
        ],
        resolution_strategy="Manage warranty per ISO and manufacturer guidelines; document claims and replacements.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 25"
    ),
    DoctrineBlock(
        topic="Hydraulic System Export Compliance - International Standards and Documentation",
        keywords=["export compliance", "international standards", "documentation", "regulatory compliance", "system certification"],
        conclusion_template="Ensure hydraulic system export compliance with international standards and documentation.",
        reasoning_framework=(
            "Export compliance requires adherence to international standards and proper documentation for hydraulic systems. "
            "ISO 9001 and manufacturer guidelines specify certification and documentation requirements. "
            "Documentation must include export records, certification documents, and reference to standards."
        ),
        key_factors=[
            "International standards",
            "Certification",
            "Export records",
            "Regulatory compliance",
            "Documentation"
        ],
        primary_authority=[
            "ISO 9001: Quality management systems",
            "Manufacturer export compliance guides"
        ],
        burden_holder="Export manager",
        adversary_position="Export compliance is unnecessary for domestic sales.",
        counter_arguments=[
            "International sales require certification and documentation.",
            "Non-compliance risks export bans."
        ],
        resolution_strategy="Ensure compliance per ISO and manufacturer guidelines; document records and certifications.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.94,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 9001 Section 8"
    ),
    DoctrineBlock(
        topic="Hydraulic System Customization - Application-Specific Design",
        keywords=["customization", "application-specific", "design", "component selection", "performance optimization"],
        conclusion_template="Customize hydraulic system design for application-specific requirements and performance optimization.",
        reasoning_framework=(
            "Application-specific customization optimizes hydraulic system performance and reliability. "
            "ISO 4413 and manufacturer guidelines specify customization protocols and component selection. "
            "Documentation must include customization plan, application requirements, and reference to standards."
        ),
        key_factors=[
            "Customization protocols",
            "Application requirements",
            "Component selection",
            "Performance optimization",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer customization guides"
        ],
        burden_holder="System designer",
        adversary_position="Customization increases cost and complexity.",
        counter_arguments=[
            "Application-specific design improves performance.",
            "Customization prevents overdesign."
        ],
        resolution_strategy="Customize per ISO and manufacturer guidelines; document plan and requirements.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 26"
    ),
    DoctrineBlock(
        topic="Hydraulic System Sustainability - Energy and Resource Optimization",
        keywords=["sustainability", "energy optimization", "resource optimization", "environmental impact", "system efficiency"],
        conclusion_template="Optimize hydraulic system for sustainability through energy and resource management.",
        reasoning_framework=(
            "Sustainability in hydraulic systems is achieved by optimizing energy and resource usage, reducing environmental impact. "
            "ISO 14001 and manufacturer guidelines specify sustainability protocols and optimization strategies. "
            "Documentation must include sustainability plan, optimization measures, and reference to standards."
        ),
        key_factors=[
            "Energy optimization",
            "Resource optimization",
            "Environmental impact",
            "Sustainability plan",
            "Documentation"
        ],
        primary_authority=[
            "ISO 14001: Environmental management",
            "Manufacturer sustainability guides"
        ],
        burden_holder="System designer",
        adversary_position="Sustainability measures increase cost and reduce performance.",
        counter_arguments=[
            "Optimization reduces long-term costs and environmental impact.",
            "Sustainability improves regulatory compliance."
        ],
        resolution_strategy="Optimize per ISO and manufacturer guidelines; document plan and measures.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.92,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 14001 Section 7"
    ),
    DoctrineBlock(
        topic="Hydraulic System Obsolescence Management - Component Replacement and Upgrade",
        keywords=["obsolescence management", "component replacement", "upgrade", "system longevity", "maintenance"],
        conclusion_template="Manage hydraulic system obsolescence through component replacement and upgrade planning.",
        reasoning_framework=(
            "Obsolescence management extends hydraulic system longevity by planning component replacement and upgrades. "
            "ISO 4413 and manufacturer guidelines specify obsolescence protocols and replacement criteria. "
            "Documentation must include obsolescence plan, replacement schedules, and reference to standards."
        ),
        key_factors=[
            "Obsolescence protocols",
            "Component replacement",
            "Upgrade planning",
            "System longevity",
            "Documentation"
        ],
        primary_authority=[
            "ISO 4413: Hydraulic fluid power — General rules",
            "Manufacturer obsolescence management guides"
        ],
        burden_holder="Maintenance manager",
        adversary_position="Obsolescence management is unnecessary for reliable systems.",
        counter_arguments=[
            "Component obsolescence risks unexpected failures.",
            "Proper management ensures system longevity."
        ],
        resolution_strategy="Manage obsolescence per ISO and manufacturer guidelines; document plan and schedules.",
        entity_scope="MECH11 hydraulic systems",
        confidence=0.93,
        confidence_zone=ConfidenceZone.HIGH.value,
        controlling_precedent="ISO 4413 Section 27"
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