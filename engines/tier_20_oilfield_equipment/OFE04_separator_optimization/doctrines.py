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
        topic="Two-Phase vs Three-Phase Separator Selection",
        keywords=["separator", "two-phase", "three-phase", "oil", "water", "gas", "selection", "process"],
        conclusion_template="Select a three-phase separator when water cut exceeds 5% and gas production is significant; otherwise, two-phase is sufficient.",
        reasoning_framework=(
            "Separator selection is based on the composition of the inlet stream. If the produced fluids contain significant water "
            "(>5% by volume) and gas, a three-phase separator is required to efficiently separate oil, water, and gas. For streams "
            "with negligible water, a two-phase separator suffices. Consider operational flexibility, future water cut increase, "
            "and downstream requirements. Evaluate capital and operating costs, maintenance complexity, and space constraints. "
            "Assess regulatory requirements for water disposal and gas emissions. Three-phase separators provide better water "
            "removal and reduce downstream treatment load. Two-phase separators are simpler and less costly. The decision should "
            "be validated by process simulation and material balance calculations."
        ),
        key_factors=[
            "Inlet stream composition",
            "Water cut percentage",
            "Gas production rate",
            "Operational flexibility",
            "Capital and operating costs",
            "Space constraints",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE Guidelines"
        ],
        burden_holder="Process Engineer",
        adversary_position="Three-phase separators are unnecessarily complex for low water cut applications.",
        counter_arguments=[
            "Future water cut may increase, requiring three-phase separation.",
            "Regulatory requirements may mandate water removal.",
            "Operational flexibility is enhanced with three-phase units."
        ],
        resolution_strategy="Perform material balance and process simulation; review regulatory requirements; consider future production profiles.",
        entity_scope="Separator Selection for Oilfield Facilities",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 3.2"
    ),
    DoctrineBlock(
        topic="Horizontal vs Vertical Separator Configuration",
        keywords=["separator", "horizontal", "vertical", "configuration", "design", "selection"],
        conclusion_template="Horizontal separators are preferred for high liquid rates and three-phase separation; vertical separators are optimal for low liquid rates and space-constrained sites.",
        reasoning_framework=(
            "The configuration of separators is determined by process requirements and site constraints. Horizontal separators offer "
            "greater surface area for liquid-gas separation, making them ideal for high liquid rates and three-phase applications. "
            "Vertical separators are more compact and suitable for low liquid rates, limited footprint, and where sand or solids "
            "settling is a concern. Evaluate inlet stream characteristics, site layout, maintenance access, and safety considerations. "
            "Horizontal units are easier to clean and maintain, while vertical units may be preferred in offshore or space-limited "
            "installations. Consider vessel diameter, length-to-diameter ratio, and internal design features."
        ),
        key_factors=[
            "Liquid rate",
            "Gas rate",
            "Site footprint",
            "Solids handling",
            "Maintenance access",
            "Safety considerations"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Vertical separators are more versatile and require less space.",
        counter_arguments=[
            "Horizontal separators provide better liquid-gas separation for high flow rates.",
            "Maintenance is easier in horizontal vessels.",
            "Three-phase separation is more efficient in horizontal units."
        ],
        resolution_strategy="Compare process simulations, evaluate site constraints, and review maintenance records.",
        entity_scope="Separator Configuration Selection",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 4.1"
    ),
    DoctrineBlock(
        topic="Oil-Water Retention Time Calculation (Stokes Law)",
        keywords=["oil", "water", "retention time", "stokes law", "separator", "design"],
        conclusion_template="Calculate oil-water retention time using Stokes Law, adjusting for emulsion stability and temperature.",
        reasoning_framework=(
            "Retention time is critical for effective oil-water separation. Stokes Law provides the theoretical settling velocity of "
            "water droplets in oil, assuming spherical droplets and laminar flow. Adjust calculations for emulsion stability, droplet "
            "size distribution, and temperature effects. Use laboratory data for droplet size and viscosity. Increase retention time "
            "for stable emulsions or high viscosity fluids. Validate with pilot testing or field performance data. Ensure compliance "
            "with regulatory discharge limits and downstream process requirements."
        ),
        key_factors=[
            "Droplet size distribution",
            "Fluid viscosity",
            "Temperature",
            "Emulsion stability",
            "Regulatory discharge limits"
        ],
        primary_authority=[
            "API RP 12J",
            "SPE 169978",
            "ASME Section VIII"
        ],
        burden_holder="Process Designer",
        adversary_position="Stokes Law is not valid for turbulent flow or non-spherical droplets.",
        counter_arguments=[
            "Adjust calculations for turbulence and non-ideal conditions.",
            "Use empirical data to validate theoretical results.",
            "Pilot testing can confirm retention time requirements."
        ],
        resolution_strategy="Combine theoretical calculations with empirical and pilot data; adjust design as needed.",
        entity_scope="Separator Design Calculations",
        confidence=0.85,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 12J Section 5.3"
    ),
    DoctrineBlock(
        topic="Gas-Liquid Retention Time (Vapor Dropout)",
        keywords=["gas", "liquid", "retention time", "vapor dropout", "separator", "design"],
        conclusion_template="Set gas-liquid retention time based on vapor dropout curves and process simulation; typically 1-3 minutes for oilfield separators.",
        reasoning_framework=(
            "Gas-liquid retention time is determined by the time required for vapor to disengage from the liquid phase. Use vapor "
            "dropout curves and process simulation to estimate required retention time. Consider gas rate, liquid rate, temperature, "
            "pressure, and separator internals. Short retention times may lead to carryover; excessive times increase vessel size "
            "and cost. Validate with field data and adjust for separator configuration (horizontal vs vertical). Ensure compliance "
            "with gas emission regulations and downstream process requirements."
        ),
        key_factors=[
            "Gas rate",
            "Liquid rate",
            "Temperature",
            "Pressure",
            "Separator internals",
            "Regulatory requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Short retention times are sufficient due to high efficiency internals.",
        counter_arguments=[
            "High efficiency internals may not perform as expected under all conditions.",
            "Field data shows carryover at short retention times.",
            "Regulatory requirements may mandate minimum retention times."
        ],
        resolution_strategy="Review process simulation, field data, and regulatory requirements; adjust design accordingly.",
        entity_scope="Separator Design for Gas-Liquid Separation",
        confidence=0.83,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 12J Section 5.4"
    ),
    DoctrineBlock(
        topic="Heater Treater Design and Operation",
        keywords=["heater treater", "design", "operation", "oil", "water", "emulsion", "temperature"],
        conclusion_template="Design heater treaters for optimal emulsion breaking at target temperature; operate within manufacturer's guidelines for safety and efficiency.",
        reasoning_framework=(
            "Heater treaters use heat to break oil-water emulsions, enhancing separation. Design must consider inlet stream composition, "
            "emulsion stability, target temperature, and heat exchanger efficiency. Select heating elements based on fuel availability "
            "and safety requirements. Operate within manufacturer's guidelines to prevent overheating, fire hazards, and excessive "
            "energy consumption. Monitor temperature, pressure, and level controls. Validate design with pilot testing and adjust for "
            "field conditions. Ensure compliance with safety and environmental regulations."
        ),
        key_factors=[
            "Inlet stream composition",
            "Emulsion stability",
            "Target temperature",
            "Heating element selection",
            "Safety requirements",
            "Energy efficiency"
        ],
        primary_authority=[
            "API RP 12L",
            "ASME Section VIII",
            "NFPA 30"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Heater treaters are unnecessary with advanced chemical demulsifiers.",
        counter_arguments=[
            "Chemical demulsifiers may not be effective for all emulsions.",
            "Heat enhances separation and reduces chemical usage.",
            "Heater treaters provide operational flexibility."
        ],
        resolution_strategy="Evaluate emulsion stability, pilot test chemical and heat treatment, select optimal approach.",
        entity_scope="Heater Treater Design and Operation",
        confidence=0.87,
        confidence_zone="High",
        controlling_precedent="API RP 12L Section 2.1"
    ),
    DoctrineBlock(
        topic="Free Water Knockout (FWKO) Sizing",
        keywords=["fwko", "free water knockout", "sizing", "separator", "oil", "water"],
        conclusion_template="Size FWKO vessels based on water cut, oil rate, retention time, and solids handling requirements.",
        reasoning_framework=(
            "FWKO vessels are designed to remove free water from oil prior to further processing. Sizing is based on inlet oil and "
            "water rates, required retention time (typically 5-30 minutes), and solids handling requirements. Consider emulsion stability, "
            "temperature, and separator configuration. Provide adequate space for solids settling and removal. Validate design with "
            "process simulation and field data. Ensure compliance with regulatory discharge limits and downstream process requirements."
        ),
        key_factors=[
            "Oil rate",
            "Water cut",
            "Retention time",
            "Solids handling",
            "Emulsion stability",
            "Temperature"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Designer",
        adversary_position="FWKO vessels are redundant with modern three-phase separators.",
        counter_arguments=[
            "FWKO provides additional water removal and solids settling.",
            "Reduces load on downstream separators.",
            "Enhances overall process efficiency."
        ],
        resolution_strategy="Evaluate process simulation, field data, and operational requirements; select optimal vessel configuration.",
        entity_scope="FWKO Design and Sizing",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 6.1"
    ),
    DoctrineBlock(
        topic="Mist Extractor Selection (Vane vs Mesh Pad)",
        keywords=["mist extractor", "vane", "mesh pad", "separator", "selection", "design"],
        conclusion_template="Select vane-type mist extractors for high gas rates and mesh pads for lower gas rates or finer mist removal.",
        reasoning_framework=(
            "Mist extractors remove liquid droplets from gas streams in separators. Vane-type extractors are preferred for high gas "
            "rates and larger droplets, offering low pressure drop and high capacity. Mesh pads are effective for lower gas rates and "
            "finer mist removal but may plug with solids or emulsions. Evaluate gas rate, droplet size, solids content, and maintenance "
            "requirements. Consider pressure drop, efficiency, and operational reliability. Validate selection with process simulation "
            "and field data. Ensure compliance with emission regulations and downstream equipment protection."
        ),
        key_factors=[
            "Gas rate",
            "Droplet size",
            "Solids content",
            "Pressure drop",
            "Efficiency",
            "Maintenance requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Mesh pads provide higher efficiency for all applications.",
        counter_arguments=[
            "Mesh pads may plug with solids and emulsions.",
            "Vane-type extractors are more reliable for high gas rates.",
            "Pressure drop is lower with vane-type extractors."
        ],
        resolution_strategy="Evaluate process simulation, field data, and maintenance records; select optimal extractor type.",
        entity_scope="Mist Extractor Selection",
        confidence=0.84,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 12J Section 7.2"
    ),
    DoctrineBlock(
        topic="Dump Valve Sizing and Control (Level Control)",
        keywords=["dump valve", "sizing", "control", "level", "separator", "design"],
        conclusion_template="Size dump valves based on maximum liquid rate and select control schemes to maintain stable separator levels.",
        reasoning_framework=(
            "Dump valves control liquid level in separators, preventing overflow or dry-out. Size valves based on maximum liquid rate, "
            "pressure differential, and solids content. Select control schemes (manual, pneumatic, electronic) to maintain stable levels. "
            "Consider response time, reliability, and maintenance requirements. Validate sizing with process simulation and field data. "
            "Ensure compliance with safety and environmental regulations. Provide redundancy and fail-safe features for critical applications."
        ),
        key_factors=[
            "Maximum liquid rate",
            "Pressure differential",
            "Solids content",
            "Control scheme",
            "Response time",
            "Reliability"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "ISA 75.01"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Manual control is sufficient for most separator applications.",
        counter_arguments=[
            "Automatic control enhances reliability and reduces operator workload.",
            "Manual control may lead to unstable levels and process upsets.",
            "Electronic control provides better accuracy and response."
        ],
        resolution_strategy="Evaluate process simulation, field data, and operational requirements; select optimal valve and control scheme.",
        entity_scope="Separator Level Control",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 8.1"
    ),
    DoctrineBlock(
        topic="Separator Vessel Design per ASME Section VIII",
        keywords=["separator", "vessel", "design", "asme", "section viii", "pressure", "code"],
        conclusion_template="Design separator vessels per ASME Section VIII, ensuring compliance with pressure, material, and fabrication requirements.",
        reasoning_framework=(
            "Separator vessel design must comply with ASME Section VIII for pressure vessels. Specify design pressure, temperature, "
            "material selection, corrosion allowance, and fabrication requirements. Perform stress analysis, hydrostatic testing, "
            "and non-destructive examination. Ensure compliance with welding, inspection, and documentation standards. Validate design "
            "with process simulation and field data. Provide certification and registration as required by local regulations."
        ),
        key_factors=[
            "Design pressure",
            "Design temperature",
            "Material selection",
            "Corrosion allowance",
            "Fabrication requirements",
            "Inspection and testing"
        ],
        primary_authority=[
            "ASME Section VIII",
            "API RP 12J",
            "National Board Inspection Code"
        ],
        burden_holder="Design Engineer",
        adversary_position="API standards are sufficient for separator vessel design.",
        counter_arguments=[
            "ASME Section VIII is mandatory for pressure vessels in most jurisdictions.",
            "API standards provide supplemental guidance but do not replace ASME requirements.",
            "Regulatory compliance requires ASME certification."
        ],
        resolution_strategy="Design per ASME Section VIII; supplement with API guidance; ensure certification and documentation.",
        entity_scope="Separator Vessel Design",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Sand Jet and Sand Drain Systems",
        keywords=["sand jet", "sand drain", "separator", "solids", "removal", "design"],
        conclusion_template="Include sand jet and drain systems in separators handling high solids to prevent accumulation and maintain performance.",
        reasoning_framework=(
            "Sand jet and drain systems remove accumulated solids from separator vessels, preventing performance degradation and "
            "maintenance issues. Design systems based on solids rate, particle size, and separator configuration. Provide adequate "
            "drainage and flushing capacity. Validate design with field data and pilot testing. Ensure compliance with safety and "
            "environmental regulations. Provide redundancy and fail-safe features for critical applications. Monitor solids removal "
            "and adjust operation as needed."
        ),
        key_factors=[
            "Solids rate",
            "Particle size",
            "Separator configuration",
            "Drainage capacity",
            "Flushing system",
            "Safety requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Sand jet systems are unnecessary with proper upstream solids removal.",
        counter_arguments=[
            "Upstream removal may not capture all solids.",
            "Sand accumulation degrades separator performance.",
            "Sand jet systems reduce maintenance and downtime."
        ],
        resolution_strategy="Evaluate solids rate, field data, and operational requirements; include sand jet systems as needed.",
        entity_scope="Separator Solids Removal",
        confidence=0.82,
        confidence_zone="Moderate-High",
        controlling_precedent="API RP 12J Section 9.2"
    ),
    DoctrineBlock(
        topic="H2S Service and Sour Gas Considerations",
        keywords=["h2s", "sour gas", "separator", "design", "corrosion", "safety"],
        conclusion_template="Design separators for H2S service with corrosion-resistant materials, enhanced safety features, and compliance with relevant standards.",
        reasoning_framework=(
            "H2S service requires special design considerations for separators. Use corrosion-resistant materials (e.g., stainless steel, "
            "clad steel) and enhanced safety features (e.g., gas detection, emergency shutdown systems). Ensure compliance with NACE MR0175, "
            "API RP 12J, and ASME Section VIII. Provide adequate ventilation, monitoring, and emergency response plans. Validate design with "
            "process simulation and field data. Ensure operator training and regular inspection. Consider environmental and regulatory requirements."
        ),
        key_factors=[
            "Corrosion resistance",
            "Safety features",
            "Material selection",
            "Regulatory compliance",
            "Emergency response",
            "Operator training"
        ],
        primary_authority=[
            "NACE MR0175",
            "API RP 12J",
            "ASME Section VIII"
        ],
        burden_holder="Design Engineer",
        adversary_position="Standard separator design is sufficient for low H2S concentrations.",
        counter_arguments=[
            "Low concentrations may increase over time.",
            "Regulatory requirements mandate enhanced design for any H2S presence.",
            "Safety risks are significant even at low concentrations."
        ],
        resolution_strategy="Design per NACE MR0175 and API RP 12J; monitor H2S levels; upgrade as needed.",
        entity_scope="Separator Design for Sour Gas",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 2.1"
    ),
    DoctrineBlock(
        topic="LACT Unit Design and Custody Transfer",
        keywords=["lact", "unit", "design", "custody transfer", "separator", "measurement"],
        conclusion_template="Design LACT units for accurate custody transfer, ensuring compliance with API standards and metering requirements.",
        reasoning_framework=(
            "LACT (Lease Automatic Custody Transfer) units provide accurate measurement and transfer of oil from production facilities to "
            "pipelines or storage. Design must comply with API standards (API MPMS), ensuring accurate metering, sampling, and control. "
            "Select meters based on flow rate, fluid properties, and regulatory requirements. Provide calibration and verification procedures. "
            "Ensure compliance with custody transfer agreements and local regulations. Validate design with process simulation and field data."
        ),
        key_factors=[
            "Meter selection",
            "Flow rate",
            "Fluid properties",
            "Calibration procedures",
            "Regulatory compliance",
            "Custody transfer agreements"
        ],
        primary_authority=[
            "API MPMS",
            "API RP 12J",
            "ASME Section VIII"
        ],
        burden_holder="Measurement Engineer",
        adversary_position="Standard production meters are sufficient for custody transfer.",
        counter_arguments=[
            "Custody transfer requires higher accuracy and compliance.",
            "API standards mandate specific design and calibration procedures.",
            "Disputes may arise without proper LACT unit design."
        ],
        resolution_strategy="Design per API MPMS; validate with calibration and verification; ensure compliance with agreements.",
        entity_scope="Custody Transfer Measurement",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API MPMS Chapter 4"
    ),
    DoctrineBlock(
        topic="Pressure Control and Back Pressure Regulation",
        keywords=["pressure control", "back pressure", "separator", "regulation", "design"],
        conclusion_template="Implement pressure control and back pressure regulation to maintain separator performance and protect downstream equipment.",
        reasoning_framework=(
            "Pressure control and back pressure regulation are essential for separator performance and protection of downstream equipment. "
            "Design systems based on separator operating pressure, downstream requirements, and safety considerations. Select control valves, "
            "pressure relief devices, and instrumentation. Validate design with process simulation and field data. Ensure compliance with "
            "safety and environmental regulations. Provide redundancy and fail-safe features for critical applications."
        ),
        key_factors=[
            "Operating pressure",
            "Downstream requirements",
            "Control valve selection",
            "Pressure relief devices",
            "Instrumentation",
            "Safety requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "ISA 75.01"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Pressure control is unnecessary for separators operating at atmospheric pressure.",
        counter_arguments=[
            "Atmospheric pressure may fluctuate, affecting separator performance.",
            "Downstream equipment may require stable pressure.",
            "Safety risks exist without proper pressure control."
        ],
        resolution_strategy="Evaluate process simulation, field data, and operational requirements; implement pressure control as needed.",
        entity_scope="Separator Pressure Regulation",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 10.1"
    ),
    DoctrineBlock(
        topic="Separator Internals Selection and Optimization",
        keywords=["separator", "internals", "selection", "optimization", "design", "vane", "mesh", "baffle"],
        conclusion_template="Optimize separator internals for process efficiency, selecting vane, mesh, or baffle types based on fluid properties and flow rates.",
        reasoning_framework=(
            "Separator internals enhance phase separation by controlling flow patterns and increasing droplet coalescence. Select internals "
            "based on fluid properties, flow rates, and separator configuration. Vane packs are suitable for high gas rates, mesh pads for fine "
            "mist removal, and baffles for controlling turbulence. Evaluate efficiency, pressure drop, and maintenance requirements. Validate "
            "selection with process simulation and field data. Ensure compliance with emission regulations and downstream equipment protection."
        ),
        key_factors=[
            "Fluid properties",
            "Flow rates",
            "Separator configuration",
            "Efficiency",
            "Pressure drop",
            "Maintenance requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard internals are sufficient for most applications.",
        counter_arguments=[
            "Optimized internals enhance separation efficiency.",
            "Pressure drop can be minimized with proper selection.",
            "Maintenance requirements vary with internal type."
        ],
        resolution_strategy="Evaluate process simulation, field data, and operational requirements; optimize internals selection.",
        entity_scope="Separator Internals Optimization",
        confidence=0.88,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.1"
    ),
    DoctrineBlock(
        topic="Emulsion Stability and Demulsifier Selection",
        keywords=["emulsion", "stability", "demulsifier", "separator", "design", "chemical"],
        conclusion_template="Select demulsifiers based on emulsion stability, fluid properties, and separator design; validate effectiveness with pilot testing.",
        reasoning_framework=(
            "Emulsion stability affects separator performance and chemical requirements. Select demulsifiers based on laboratory testing, "
            "fluid properties, and separator design. Evaluate effectiveness with pilot testing and field data. Adjust dosage based on emulsion "
            "type, temperature, and separator configuration. Monitor separation efficiency and adjust chemical program as needed. Ensure compliance "
            "with environmental regulations and downstream process requirements."
        ),
        key_factors=[
            "Emulsion stability",
            "Fluid properties",
            "Separator design",
            "Demulsifier effectiveness",
            "Dosage",
            "Environmental compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Mechanical separation is sufficient without chemicals.",
        counter_arguments=[
            "Stable emulsions require chemical treatment for efficient separation.",
            "Demulsifiers reduce water and solids carryover.",
            "Pilot testing confirms chemical effectiveness."
        ],
        resolution_strategy="Evaluate laboratory and pilot testing; adjust chemical program as needed.",
        entity_scope="Separator Chemical Optimization",
        confidence=0.86,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 11.2"
    ),
    DoctrineBlock(
        topic="Separator Startup and Shutdown Procedures",
        keywords=["separator", "startup", "shutdown", "procedure", "operation", "safety"],
        conclusion_template="Follow standardized startup and shutdown procedures to ensure safety, prevent equipment damage, and maintain process integrity.",
        reasoning_framework=(
            "Startup and shutdown procedures are critical for separator safety and performance. Follow standardized procedures, including "
            "equipment checks, pressure and level monitoring, and gradual ramp-up or ramp-down of flow rates. Ensure compliance with safety "
            "regulations and manufacturer guidelines. Provide operator training and documentation. Monitor process parameters and adjust as needed. "
            "Validate procedures with field data and incident records. Provide emergency shutdown protocols and fail-safe features."
        ),
        key_factors=[
            "Safety requirements",
            "Equipment checks",
            "Process monitoring",
            "Operator training",
            "Documentation",
            "Emergency protocols"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "NFPA 30"
        ],
        burden_holder="Operations Supervisor",
        adversary_position="Informal procedures are sufficient for experienced operators.",
        counter_arguments=[
            "Standardized procedures reduce risk and improve reliability.",
            "Documentation ensures compliance and training.",
            "Emergency protocols are critical for safety."
        ],
        resolution_strategy="Develop and implement standardized procedures; provide training and documentation.",
        entity_scope="Separator Operation",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="API RP 12J Section 12.1"
    ),
    DoctrineBlock(
        topic="Separator Maintenance and Inspection",
        keywords=["separator", "maintenance", "inspection", "operation", "safety", "reliability"],
        conclusion_template="Implement regular maintenance and inspection programs to ensure separator reliability, safety, and compliance.",
        reasoning_framework=(
            "Regular maintenance and inspection are essential for separator reliability and safety. Develop programs based on manufacturer "
            "guidelines, regulatory requirements, and field data. Include routine checks, cleaning, and testing of internals, valves, and instrumentation. "
            "Monitor performance and adjust maintenance frequency as needed. Provide documentation and training. Validate program effectiveness with "
            "incident records and operational data. Ensure compliance with safety and environmental regulations."
        ),
        key_factors=[
            "Manufacturer guidelines",
            "Regulatory requirements",
            "Field data",
            "Maintenance frequency",
            "Documentation",
            "Training"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "National Board Inspection Code"
        ],
        burden_holder="Maintenance Supervisor",
        adversary_position="Reactive maintenance is sufficient for separator reliability.",
        counter_arguments=[
            "Preventive maintenance reduces downtime and risk.",
            "Inspection programs improve safety and compliance.",
            "Documentation and training enhance reliability."
        ],
        resolution_strategy="Develop preventive maintenance and inspection programs; provide training and documentation.",
        entity_scope="Separator Maintenance",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 13.1"
    ),
    DoctrineBlock(
        topic="Separator Debottlenecking and Capacity Optimization",
        keywords=["separator", "debottlenecking", "capacity", "optimization", "process", "design"],
        conclusion_template="Optimize separator capacity by debottlenecking process constraints, upgrading internals, and adjusting operating parameters.",
        reasoning_framework=(
            "Separator debottlenecking involves identifying and addressing process constraints to increase capacity and efficiency. Upgrade internals, "
            "adjust operating parameters, and modify vessel configuration as needed. Use process simulation and field data to identify bottlenecks. "
            "Validate improvements with pilot testing and operational data. Ensure compliance with safety and environmental regulations. Provide "
            "documentation and training for operators."
        ),
        key_factors=[
            "Process constraints",
            "Internals upgrade",
            "Operating parameters",
            "Vessel configuration",
            "Simulation and field data",
            "Safety requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Existing separator design is sufficient for current production rates.",
        counter_arguments=[
            "Production rates may increase over time.",
            "Process constraints reduce efficiency and reliability.",
            "Debottlenecking enhances capacity and performance."
        ],
        resolution_strategy="Identify bottlenecks with simulation and field data; implement upgrades and adjustments.",
        entity_scope="Separator Capacity Optimization",
        confidence=0.89,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 14.1"
    ),
    DoctrineBlock(
        topic="Separator Safety Systems and Emergency Shutdown",
        keywords=["separator", "safety", "emergency shutdown", "system", "operation"],
        conclusion_template="Implement safety systems and emergency shutdown protocols to protect personnel, equipment, and environment.",
        reasoning_framework=(
            "Safety systems and emergency shutdown protocols are critical for separator operation. Implement gas detection, pressure relief, "
            "emergency shutdown valves, and alarm systems. Develop standardized procedures and provide operator training. Validate systems with "
            "field data and incident records. Ensure compliance with safety and environmental regulations. Provide redundancy and fail-safe features "
            "for critical applications."
        ),
        key_factors=[
            "Safety systems",
            "Emergency shutdown protocols",
            "Operator training",
            "Incident records",
            "Regulatory compliance",
            "Redundancy"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "NFPA 30"
        ],
        burden_holder="Safety Engineer",
        adversary_position="Basic safety systems are sufficient for separator operation.",
        counter_arguments=[
            "Enhanced safety systems reduce risk and improve reliability.",
            "Emergency shutdown protocols are critical for safety.",
            "Regulatory requirements mandate advanced safety features."
        ],
        resolution_strategy="Develop and implement safety systems and protocols; provide training and documentation.",
        entity_scope="Separator Safety",
        confidence=0.96,
        confidence_zone="Very High",
        controlling_precedent="API RP 12J Section 15.1"
    ),
    DoctrineBlock(
        topic="Separator Instrumentation and Automation",
        keywords=["separator", "instrumentation", "automation", "control", "operation"],
        conclusion_template="Implement advanced instrumentation and automation for separator control, monitoring, and optimization.",
        reasoning_framework=(
            "Advanced instrumentation and automation enhance separator control, monitoring, and optimization. Select instruments based on process "
            "requirements, accuracy, and reliability. Implement automated control systems for level, pressure, and flow regulation. Validate systems "
            "with process simulation and field data. Provide operator training and documentation. Ensure compliance with safety and environmental regulations."
        ),
        key_factors=[
            "Instrumentation selection",
            "Automation systems",
            "Process requirements",
            "Accuracy",
            "Reliability",
            "Training"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "ISA 75.01"
        ],
        burden_holder="Automation Engineer",
        adversary_position="Manual control is sufficient for separator operation.",
        counter_arguments=[
            "Automation enhances reliability and reduces operator workload.",
            "Advanced instrumentation improves accuracy and process optimization.",
            "Regulatory requirements may mandate automation."
        ],
        resolution_strategy="Implement advanced instrumentation and automation; provide training and documentation.",
        entity_scope="Separator Automation",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 16.1"
    ),
    DoctrineBlock(
        topic="Separator Environmental Compliance and Emissions Control",
        keywords=["separator", "environmental", "compliance", "emissions", "control", "regulation"],
        conclusion_template="Design separators to minimize emissions and ensure environmental compliance with relevant regulations.",
        reasoning_framework=(
            "Environmental compliance and emissions control are critical for separator design and operation. Minimize emissions of hydrocarbons, H2S, "
            "and other pollutants by optimizing separator internals, implementing vapor recovery systems, and monitoring emissions. Ensure compliance with "
            "local, state, and federal regulations. Provide documentation and reporting as required. Validate compliance with field data and regulatory audits."
        ),
        key_factors=[
            "Emissions minimization",
            "Vapor recovery systems",
            "Regulatory compliance",
            "Monitoring",
            "Documentation",
            "Reporting"
        ],
        primary_authority=[
            "EPA CFR 40",
            "API RP 12J",
            "ASME Section VIII"
        ],
        burden_holder="Environmental Engineer",
        adversary_position="Emissions control is unnecessary for low production rates.",
        counter_arguments=[
            "Regulatory requirements mandate emissions control for all facilities.",
            "Emissions may increase over time.",
            "Environmental compliance reduces risk and liability."
        ],
        resolution_strategy="Design for emissions minimization; implement monitoring and reporting; ensure compliance with regulations.",
        entity_scope="Separator Environmental Compliance",
        confidence=0.94,
        confidence_zone="Very High",
        controlling_precedent="EPA CFR 40 Part 60"
    ),
    DoctrineBlock(
        topic="Separator Design for High Pressure Applications",
        keywords=["separator", "design", "high pressure", "application", "asme", "section viii"],
        conclusion_template="Design separators for high pressure applications per ASME Section VIII, using appropriate materials and safety features.",
        reasoning_framework=(
            "High pressure separator design requires compliance with ASME Section VIII, selection of appropriate materials, and enhanced safety features. "
            "Specify design pressure, temperature, and material properties. Perform stress analysis, hydrostatic testing, and non-destructive examination. "
            "Provide pressure relief devices and emergency shutdown systems. Validate design with process simulation and field data. Ensure compliance with "
            "regulatory requirements and provide certification and documentation."
        ),
        key_factors=[
            "Design pressure",
            "Material selection",
            "Safety features",
            "Stress analysis",
            "Testing",
            "Certification"
        ],
        primary_authority=[
            "ASME Section VIII",
            "API RP 12J",
            "National Board Inspection Code"
        ],
        burden_holder="Design Engineer",
        adversary_position="Standard separator design is sufficient for moderate pressures.",
        counter_arguments=[
            "High pressure requires enhanced design and materials.",
            "Regulatory requirements mandate ASME compliance.",
            "Safety risks are significant at high pressure."
        ],
        resolution_strategy="Design per ASME Section VIII; validate with testing and certification; ensure compliance.",
        entity_scope="Separator High Pressure Design",
        confidence=0.95,
        confidence_zone="Very High",
        controlling_precedent="ASME Section VIII Division 2"
    ),
    DoctrineBlock(
        topic="Separator Design for Low Temperature Applications",
        keywords=["separator", "design", "low temperature", "application", "material", "asme"],
        conclusion_template="Design separators for low temperature applications using materials with adequate toughness and compliance with ASME Section VIII.",
        reasoning_framework=(
            "Low temperature separator design requires selection of materials with adequate toughness to prevent brittle fracture. Comply with ASME Section VIII "
            "and specify design temperature, material properties, and testing requirements. Provide insulation and heating as needed. Validate design with process "
            "simulation and field data. Ensure compliance with regulatory requirements and provide certification and documentation."
        ),
        key_factors=[
            "Design temperature",
            "Material toughness",
            "Insulation",
            "Heating",
            "Testing",
            "Certification"
        ],
        primary_authority=[
            "ASME Section VIII",
            "API RP 12J",
            "National Board Inspection Code"
        ],
        burden_holder="Design Engineer",
        adversary_position="Standard materials are sufficient for low temperature applications.",
        counter_arguments=[
            "Low temperature increases risk of brittle fracture.",
            "ASME Section VIII mandates material toughness requirements.",
            "Insulation and heating enhance reliability."
        ],
        resolution_strategy="Select materials with adequate toughness; provide insulation and heating; ensure compliance.",
        entity_scope="Separator Low Temperature Design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Separator Design for High Solids Applications",
        keywords=["separator", "design", "high solids", "application", "sand", "drain", "jet"],
        conclusion_template="Design separators for high solids applications with enhanced sand jet and drain systems, and increased maintenance frequency.",
        reasoning_framework=(
            "High solids separator design requires enhanced sand jet and drain systems to prevent accumulation and maintain performance. Increase maintenance "
            "frequency and provide redundancy for critical applications. Validate design with field data and pilot testing. Ensure compliance with safety and "
            "environmental regulations. Provide documentation and training for operators."
        ),
        key_factors=[
            "Solids rate",
            "Sand jet and drain systems",
            "Maintenance frequency",
            "Redundancy",
            "Field data",
            "Safety requirements"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Standard separator design is sufficient for solids removal.",
        counter_arguments=[
            "High solids increase risk of accumulation and performance degradation.",
            "Enhanced systems reduce maintenance and downtime.",
            "Field data confirms need for increased maintenance."
        ],
        resolution_strategy="Design with enhanced sand jet and drain systems; increase maintenance frequency; provide training.",
        entity_scope="Separator High Solids Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 9.3"
    ),
    DoctrineBlock(
        topic="Separator Design for High Water Cut Applications",
        keywords=["separator", "design", "high water cut", "application", "three-phase", "fwko"],
        conclusion_template="Design separators for high water cut applications with three-phase separation and FWKO vessels for enhanced water removal.",
        reasoning_framework=(
            "High water cut separator design requires three-phase separation and FWKO vessels for enhanced water removal. Specify retention time, separator "
            "configuration, and internals based on water cut and fluid properties. Validate design with process simulation and field data. Ensure compliance "
            "with regulatory discharge limits and downstream process requirements. Provide documentation and training for operators."
        ),
        key_factors=[
            "Water cut",
            "Three-phase separation",
            "FWKO vessels",
            "Retention time",
            "Separator configuration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard two-phase separators are sufficient for high water cut applications.",
        counter_arguments=[
            "Three-phase separation enhances water removal and process efficiency.",
            "FWKO vessels reduce load on downstream separators.",
            "Regulatory requirements mandate water removal."
        ],
        resolution_strategy="Design with three-phase separation and FWKO vessels; validate with simulation and field data.",
        entity_scope="Separator High Water Cut Design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 6.2"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas Rate Applications",
        keywords=["separator", "design", "high gas rate", "application", "mist extractor", "vane"],
        conclusion_template="Design separators for high gas rate applications with vane-type mist extractors and optimized internals for gas-liquid separation.",
        reasoning_framework=(
            "High gas rate separator design requires vane-type mist extractors and optimized internals for gas-liquid separation. Specify retention time, separator "
            "configuration, and internals based on gas rate and fluid properties. Validate design with process simulation and field data. Ensure compliance with "
            "emission regulations and downstream equipment protection. Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Vane-type mist extractors",
            "Internals optimization",
            "Retention time",
            "Separator configuration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Mesh pads are sufficient for high gas rate applications.",
        counter_arguments=[
            "Vane-type extractors provide higher capacity and reliability.",
            "Optimized internals enhance gas-liquid separation.",
            "Emission regulations mandate efficient mist removal."
        ],
        resolution_strategy="Design with vane-type mist extractors and optimized internals; validate with simulation and field data.",
        entity_scope="Separator High Gas Rate Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.3"
    ),
    DoctrineBlock(
        topic="Separator Design for Offshore Applications",
        keywords=["separator", "design", "offshore", "application", "vertical", "compact"],
        conclusion_template="Design separators for offshore applications with vertical configuration, compact footprint, and enhanced safety features.",
        reasoning_framework=(
            "Offshore separator design requires vertical configuration, compact footprint, and enhanced safety features. Specify retention time, separator "
            "configuration, and internals based on space constraints and fluid properties. Validate design with process simulation and field data. Ensure "
            "compliance with safety and environmental regulations. Provide documentation and training for operators."
        ),
        key_factors=[
            "Vertical configuration",
            "Compact footprint",
            "Safety features",
            "Retention time",
            "Separator internals",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Horizontal separators are sufficient for offshore applications.",
        counter_arguments=[
            "Vertical configuration reduces footprint and enhances safety.",
            "Space constraints mandate compact design.",
            "Regulatory requirements mandate enhanced safety features."
        ],
        resolution_strategy="Design with vertical configuration and compact footprint; validate with simulation and field data.",
        entity_scope="Separator Offshore Design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 4.2"
    ),
    DoctrineBlock(
        topic="Separator Design for Onshore Applications",
        keywords=["separator", "design", "onshore", "application", "horizontal", "maintenance"],
        conclusion_template="Design separators for onshore applications with horizontal configuration, enhanced maintenance access, and optimized internals.",
        reasoning_framework=(
            "Onshore separator design requires horizontal configuration, enhanced maintenance access, and optimized internals. Specify retention time, separator "
            "configuration, and internals based on fluid properties and site layout. Validate design with process simulation and field data. Ensure compliance "
            "with safety and environmental regulations. Provide documentation and training for operators."
        ),
        key_factors=[
            "Horizontal configuration",
            "Maintenance access",
            "Internals optimization",
            "Retention time",
            "Separator configuration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Facilities Engineer",
        adversary_position="Vertical separators are sufficient for onshore applications.",
        counter_arguments=[
            "Horizontal configuration enhances maintenance access and separation efficiency.",
            "Site layout allows for larger footprint.",
            "Regulatory requirements mandate optimized internals."
        ],
        resolution_strategy="Design with horizontal configuration and enhanced maintenance access; validate with simulation and field data.",
        entity_scope="Separator Onshore Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 4.3"
    ),
    DoctrineBlock(
        topic="Separator Design for Remote Monitoring and Control",
        keywords=["separator", "design", "remote monitoring", "control", "automation", "instrumentation"],
        conclusion_template="Design separators with remote monitoring and control capabilities, implementing advanced automation and communication systems.",
        reasoning_framework=(
            "Remote monitoring and control enhance separator operation and reliability. Implement advanced automation and communication systems for level, pressure, "
            "and flow regulation. Select instruments based on process requirements, accuracy, and reliability. Provide operator training and documentation. Validate "
            "systems with process simulation and field data. Ensure compliance with safety and environmental regulations."
        ),
        key_factors=[
            "Remote monitoring",
            "Automation systems",
            "Communication",
            "Instrumentation selection",
            "Accuracy",
            "Reliability"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "ISA 75.01"
        ],
        burden_holder="Automation Engineer",
        adversary_position="Manual control is sufficient for separator operation.",
        counter_arguments=[
            "Remote monitoring enhances reliability and reduces operator workload.",
            "Advanced automation improves accuracy and process optimization.",
            "Regulatory requirements may mandate remote monitoring."
        ],
        resolution_strategy="Design with remote monitoring and control capabilities; provide training and documentation.",
        entity_scope="Separator Remote Monitoring",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 16.2"
    ),
    DoctrineBlock(
        topic="Separator Design for Enhanced Oil Recovery (EOR) Applications",
        keywords=["separator", "design", "eor", "enhanced oil recovery", "process", "optimization"],
        conclusion_template="Design separators for EOR applications with optimized internals, three-phase separation, and enhanced chemical treatment.",
        reasoning_framework=(
            "EOR applications require separators with optimized internals, three-phase separation, and enhanced chemical treatment. Specify retention time, separator "
            "configuration, and internals based on EOR process and fluid properties. Validate design with process simulation and field data. Ensure compliance with "
            "regulatory requirements and provide documentation and training for operators."
        ),
        key_factors=[
            "EOR process",
            "Three-phase separation",
            "Internals optimization",
            "Chemical treatment",
            "Retention time",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for EOR applications.",
        counter_arguments=[
            "EOR increases water and solids production, requiring enhanced separation.",
            "Optimized internals and chemical treatment enhance efficiency.",
            "Regulatory requirements mandate enhanced design."
        ],
        resolution_strategy="Design with optimized internals, three-phase separation, and enhanced chemical treatment; validate with simulation and field data.",
        entity_scope="Separator EOR Design",
        confidence=0.90,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 17.1"
    ),
    DoctrineBlock(
        topic="Separator Design for High Viscosity Oil Applications",
        keywords=["separator", "design", "high viscosity", "oil", "application", "retention time"],
        conclusion_template="Design separators for high viscosity oil applications with increased retention time, optimized internals, and enhanced heating.",
        reasoning_framework=(
            "High viscosity oil separator design requires increased retention time, optimized internals, and enhanced heating to improve separation efficiency. Specify "
            "retention time, separator configuration, and internals based on viscosity and fluid properties. Validate design with process simulation and field data. "
            "Ensure compliance with safety and environmental regulations. Provide documentation and training for operators."
        ),
        key_factors=[
            "Oil viscosity",
            "Retention time",
            "Internals optimization",
            "Heating",
            "Separator configuration",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high viscosity oil applications.",
        counter_arguments=[
            "High viscosity reduces separation efficiency, requiring increased retention time.",
            "Enhanced heating improves separation.",
            "Optimized internals enhance performance."
        ],
        resolution_strategy="Design with increased retention time, optimized internals, and enhanced heating; validate with simulation and field data.",
        entity_scope="Separator High Viscosity Oil Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 5.5"
    ),
    DoctrineBlock(
        topic="Separator Design for High Temperature Applications",
        keywords=["separator", "design", "high temperature", "application", "material", "asme"],
        conclusion_template="Design separators for high temperature applications with materials rated for elevated temperatures and compliance with ASME Section VIII.",
        reasoning_framework=(
            "High temperature separator design requires materials rated for elevated temperatures and compliance with ASME Section VIII. Specify design temperature, "
            "material properties, and insulation requirements. Perform stress analysis and testing. Validate design with process simulation and field data. Ensure "
            "compliance with regulatory requirements and provide certification and documentation."
        ),
        key_factors=[
            "Design temperature",
            "Material selection",
            "Insulation",
            "Stress analysis",
            "Testing",
            "Certification"
        ],
        primary_authority=[
            "ASME Section VIII",
            "API RP 12J",
            "National Board Inspection Code"
        ],
        burden_holder="Design Engineer",
        adversary_position="Standard materials are sufficient for high temperature applications.",
        counter_arguments=[
            "High temperature increases risk of material degradation.",
            "ASME Section VIII mandates material requirements.",
            "Insulation enhances reliability and safety."
        ],
        resolution_strategy="Select materials rated for high temperature; provide insulation; ensure compliance.",
        entity_scope="Separator High Temperature Design",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="ASME Section VIII Division 1"
    ),
    DoctrineBlock(
        topic="Separator Design for High Corrosivity Applications",
        keywords=["separator", "design", "high corrosivity", "application", "material", "nace"],
        conclusion_template="Design separators for high corrosivity applications with corrosion-resistant materials and compliance with NACE MR0175.",
        reasoning_framework=(
            "High corrosivity separator design requires corrosion-resistant materials and compliance with NACE MR0175. Specify material selection, corrosion allowance, "
            "and testing requirements. Validate design with process simulation and field data. Ensure compliance with regulatory requirements and provide certification "
            "and documentation."
        ),
        key_factors=[
            "Corrosivity",
            "Material selection",
            "Corrosion allowance",
            "Testing",
            "Certification",
            "Regulatory compliance"
        ],
        primary_authority=[
            "NACE MR0175",
            "API RP 12J",
            "ASME Section VIII"
        ],
        burden_holder="Design Engineer",
        adversary_position="Standard materials are sufficient for high corrosivity applications.",
        counter_arguments=[
            "High corrosivity increases risk of material degradation.",
            "NACE MR0175 mandates material requirements.",
            "Corrosion-resistant materials enhance reliability."
        ],
        resolution_strategy="Select corrosion-resistant materials; provide corrosion allowance; ensure compliance.",
        entity_scope="Separator High Corrosivity Design",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="NACE MR0175 Section 2.2"
    ),
    DoctrineBlock(
        topic="Separator Design for High Solids and Water Cut Applications",
        keywords=["separator", "design", "high solids", "high water cut", "application", "three-phase", "fwko"],
        conclusion_template="Design separators for high solids and water cut applications with three-phase separation, FWKO vessels, and enhanced sand jet systems.",
        reasoning_framework=(
            "High solids and water cut separator design requires three-phase separation, FWKO vessels, and enhanced sand jet systems. Specify retention time, separator "
            "configuration, and internals based on solids and water cut. Validate design with process simulation and field data. Ensure compliance with regulatory "
            "discharge limits and downstream process requirements. Provide documentation and training for operators."
        ),
        key_factors=[
            "Solids rate",
            "Water cut",
            "Three-phase separation",
            "FWKO vessels",
            "Sand jet systems",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high solids and water cut applications.",
        counter_arguments=[
            "Three-phase separation and FWKO vessels enhance water and solids removal.",
            "Enhanced sand jet systems reduce maintenance and downtime.",
            "Regulatory requirements mandate enhanced design."
        ],
        resolution_strategy="Design with three-phase separation, FWKO vessels, and enhanced sand jet systems; validate with simulation and field data.",
        entity_scope="Separator High Solids and Water Cut Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 6.3"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas and Water Cut Applications",
        keywords=["separator", "design", "high gas", "high water cut", "application", "three-phase", "mist extractor"],
        conclusion_template="Design separators for high gas and water cut applications with three-phase separation, vane-type mist extractors, and optimized internals.",
        reasoning_framework=(
            "High gas and water cut separator design requires three-phase separation, vane-type mist extractors, and optimized internals. Specify retention time, separator "
            "configuration, and internals based on gas and water cut. Validate design with process simulation and field data. Ensure compliance with emission regulations "
            "and downstream equipment protection. Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Water cut",
            "Three-phase separation",
            "Vane-type mist extractors",
            "Internals optimization",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high gas and water cut applications.",
        counter_arguments=[
            "Three-phase separation and vane-type mist extractors enhance gas and water removal.",
            "Optimized internals improve efficiency.",
            "Emission regulations mandate enhanced design."
        ],
        resolution_strategy="Design with three-phase separation, vane-type mist extractors, and optimized internals; validate with simulation and field data.",
        entity_scope="Separator High Gas and Water Cut Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.4"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas and Solids Applications",
        keywords=["separator", "design", "high gas", "high solids", "application", "vane", "sand jet"],
        conclusion_template="Design separators for high gas and solids applications with vane-type mist extractors, enhanced sand jet systems, and increased maintenance frequency.",
        reasoning_framework=(
            "High gas and solids separator design requires vane-type mist extractors, enhanced sand jet systems, and increased maintenance frequency. Specify retention time, "
            "separator configuration, and internals based on gas and solids rate. Validate design with process simulation and field data. Ensure compliance with emission and "
            "safety regulations. Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Solids rate",
            "Vane-type mist extractors",
            "Sand jet systems",
            "Maintenance frequency",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high gas and solids applications.",
        counter_arguments=[
            "Vane-type mist extractors and sand jet systems enhance gas and solids removal.",
            "Increased maintenance frequency reduces downtime.",
            "Emission and safety regulations mandate enhanced design."
        ],
        resolution_strategy="Design with vane-type mist extractors, enhanced sand jet systems, and increased maintenance frequency; validate with simulation and field data.",
        entity_scope="Separator High Gas and Solids Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.5"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas, Water, and Solids Applications",
        keywords=["separator", "design", "high gas", "high water cut", "high solids", "application", "three-phase", "vane", "sand jet"],
        conclusion_template="Design separators for high gas, water, and solids applications with three-phase separation, vane-type mist extractors, FWKO vessels, and enhanced sand jet systems.",
        reasoning_framework=(
            "High gas, water, and solids separator design requires three-phase separation, vane-type mist extractors, FWKO vessels, and enhanced sand jet systems. Specify retention time, "
            "separator configuration, and internals based on gas, water, and solids rate. Validate design with process simulation and field data. Ensure compliance with emission, safety, and "
            "regulatory requirements. Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Water cut",
            "Solids rate",
            "Three-phase separation",
            "Vane-type mist extractors",
            "FWKO vessels",
            "Sand jet systems",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high gas, water, and solids applications.",
        counter_arguments=[
            "Three-phase separation, vane-type mist extractors, FWKO vessels, and sand jet systems enhance gas, water, and solids removal.",
            "Regulatory requirements mandate enhanced design.",
            "Field data confirms need for enhanced systems."
        ],
        resolution_strategy="Design with three-phase separation, vane-type mist extractors, FWKO vessels, and enhanced sand jet systems; validate with simulation and field data.",
        entity_scope="Separator High Gas, Water, and Solids Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.6"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas, Water, Solids, and Corrosivity Applications",
        keywords=["separator", "design", "high gas", "high water cut", "high solids", "high corrosivity", "application", "three-phase", "vane", "sand jet", "nace"],
        conclusion_template="Design separators for high gas, water, solids, and corrosivity applications with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, and corrosion-resistant materials.",
        reasoning_framework=(
            "High gas, water, solids, and corrosivity separator design requires three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, and corrosion-resistant materials. "
            "Specify retention time, separator configuration, and internals based on gas, water, solids, and corrosivity. Validate design with process simulation and field data. Ensure compliance with emission, safety, and regulatory requirements. "
            "Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Water cut",
            "Solids rate",
            "Corrosivity",
            "Three-phase separation",
            "Vane-type mist extractors",
            "FWKO vessels",
            "Sand jet systems",
            "Corrosion-resistant materials",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "NACE MR0175",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high gas, water, solids, and corrosivity applications.",
        counter_arguments=[
            "Three-phase separation, vane-type mist extractors, FWKO vessels, sand jet systems, and corrosion-resistant materials enhance gas, water, solids, and corrosivity handling.",
            "Regulatory requirements mandate enhanced design.",
            "Field data confirms need for enhanced systems."
        ],
        resolution_strategy="Design with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, and corrosion-resistant materials; validate with simulation and field data.",
        entity_scope="Separator High Gas, Water, Solids, and Corrosivity Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.7"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas, Water, Solids, Corrosivity, and Temperature Applications",
        keywords=["separator", "design", "high gas", "high water cut", "high solids", "high corrosivity", "high temperature", "application", "three-phase", "vane", "sand jet", "nace", "asme"],
        conclusion_template="Design separators for high gas, water, solids, corrosivity, and temperature applications with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials.",
        reasoning_framework=(
            "High gas, water, solids, corrosivity, and temperature separator design requires three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials. "
            "Specify retention time, separator configuration, and internals based on gas, water, solids, corrosivity, and temperature. Validate design with process simulation and field data. Ensure compliance with emission, safety, and regulatory requirements. "
            "Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Water cut",
            "Solids rate",
            "Corrosivity",
            "Temperature",
            "Three-phase separation",
            "Vane-type mist extractors",
            "FWKO vessels",
            "Sand jet systems",
            "Corrosion-resistant and high-temperature materials",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "NACE MR0175",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high gas, water, solids, corrosivity, and temperature applications.",
        counter_arguments=[
            "Three-phase separation, vane-type mist extractors, FWKO vessels, sand jet systems, and corrosion-resistant and high-temperature materials enhance gas, water, solids, corrosivity, and temperature handling.",
            "Regulatory requirements mandate enhanced design.",
            "Field data confirms need for enhanced systems."
        ],
        resolution_strategy="Design with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials; validate with simulation and field data.",
        entity_scope="Separator High Gas, Water, Solids, Corrosivity, and Temperature Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.8"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas, Water, Solids, Corrosivity, Temperature, and Pressure Applications",
        keywords=["separator", "design", "high gas", "high water cut", "high solids", "high corrosivity", "high temperature", "high pressure", "application", "three-phase", "vane", "sand jet", "nace", "asme"],
        conclusion_template="Design separators for high gas, water, solids, corrosivity, temperature, and pressure applications with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials, and compliance with ASME Section VIII.",
        reasoning_framework=(
            "High gas, water, solids, corrosivity, temperature, and pressure separator design requires three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials, and compliance with ASME Section VIII. "
            "Specify retention time, separator configuration, and internals based on gas, water, solids, corrosivity, temperature, and pressure. Validate design with process simulation and field data. Ensure compliance with emission, safety, and regulatory requirements. "
            "Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Water cut",
            "Solids rate",
            "Corrosivity",
            "Temperature",
            "Pressure",
            "Three-phase separation",
            "Vane-type mist extractors",
            "FWKO vessels",
            "Sand jet systems",
            "Corrosion-resistant and high-temperature materials",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "NACE MR0175",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high gas, water, solids, corrosivity, temperature, and pressure applications.",
        counter_arguments=[
            "Three-phase separation, vane-type mist extractors, FWKO vessels, sand jet systems, and corrosion-resistant and high-temperature materials enhance gas, water, solids, corrosivity, temperature, and pressure handling.",
            "Regulatory requirements mandate enhanced design.",
            "Field data confirms need for enhanced systems."
        ],
        resolution_strategy="Design with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials, and compliance with ASME Section VIII; validate with simulation and field data.",
        entity_scope="Separator High Gas, Water, Solids, Corrosivity, Temperature, and Pressure Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.9"
    ),
    DoctrineBlock(
        topic="Separator Design for High Gas, Water, Solids, Corrosivity, Temperature, Pressure, and EOR Applications",
        keywords=["separator", "design", "high gas", "high water cut", "high solids", "high corrosivity", "high temperature", "high pressure", "eor", "application", "three-phase", "vane", "sand jet", "nace", "asme"],
        conclusion_template="Design separators for high gas, water, solids, corrosivity, temperature, pressure, and EOR applications with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials, and compliance with ASME Section VIII and EOR process requirements.",
        reasoning_framework=(
            "High gas, water, solids, corrosivity, temperature, pressure, and EOR separator design requires three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials, compliance with ASME Section VIII, and EOR process requirements. "
            "Specify retention time, separator configuration, and internals based on gas, water, solids, corrosivity, temperature, pressure, and EOR process. Validate design with process simulation and field data. Ensure compliance with emission, safety, and regulatory requirements. "
            "Provide documentation and training for operators."
        ),
        key_factors=[
            "Gas rate",
            "Water cut",
            "Solids rate",
            "Corrosivity",
            "Temperature",
            "Pressure",
            "EOR process",
            "Three-phase separation",
            "Vane-type mist extractors",
            "FWKO vessels",
            "Sand jet systems",
            "Corrosion-resistant and high-temperature materials",
            "Regulatory compliance"
        ],
        primary_authority=[
            "API RP 12J",
            "ASME Section VIII",
            "NACE MR0175",
            "SPE 169978"
        ],
        burden_holder="Process Engineer",
        adversary_position="Standard separator design is sufficient for high gas, water, solids, corrosivity, temperature, pressure, and EOR applications.",
        counter_arguments=[
            "Three-phase separation, vane-type mist extractors, FWKO vessels, sand jet systems, and corrosion-resistant and high-temperature materials enhance gas, water, solids, corrosivity, temperature, pressure, and EOR handling.",
            "Regulatory requirements mandate enhanced design.",
            "Field data confirms need for enhanced systems."
        ],
        resolution_strategy="Design with three-phase separation, vane-type mist extractors, FWKO vessels, enhanced sand jet systems, corrosion-resistant and high-temperature materials, compliance with ASME Section VIII, and EOR process requirements; validate with simulation and field data.",
        entity_scope="Separator High Gas, Water, Solids, Corrosivity, Temperature, Pressure, and EOR Design",
        confidence=0.91,
        confidence_zone="High",
        controlling_precedent="API RP 12J Section 7.10"
    ),
]

def get_doctrine_by_topic(topic: str) -> Optional[DoctrineBlock]:
    for doctrine in DOCTRINE_CACHE:
        if doctrine.topic.lower() == topic.lower():
            return doctrine
    return None

def search_doctrines(query: str) -> List[DoctrineBlock]:
    query_lower = query.lower()
    results = []
    for doctrine in DOCTRINE_CACHE:
        if query_lower in doctrine.topic.lower() or any(query_lower in kw.lower() for kw in doctrine.keywords):
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]