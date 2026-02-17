from dataclasses import dataclass, field
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
        topic="reciprocating_compressor_clearance_volume",
        keywords=["reciprocating compressor", "clearance volume", "volumetric efficiency", "capacity"],
        conclusion_template="Minimizing clearance volume is essential to maximize volumetric efficiency in reciprocating compressors.",
        reasoning_framework=(
            "Clearance volume in reciprocating compressors is the volume remaining in the cylinder when the piston is at top dead center. "
            "This volume cannot be compressed further and contains residual gas that expands during the suction stroke, reducing the amount of fresh gas drawn in. "
            "The volumetric efficiency is inversely related to clearance volume; higher clearance leads to lower efficiency. "
            "Designs must balance mechanical constraints (e.g., valve operation, thermal expansion) with the need to minimize clearance. "
            "Clearance pockets may be used for capacity control but should be minimized during normal operation. "
            "API 618 provides guidelines for acceptable clearance volumes. "
            "Careful calculation and verification during commissioning and maintenance are necessary to ensure optimal performance."
        ),
        key_factors=[
            "Cylinder geometry",
            "Valve design",
            "Operating pressure and temperature",
            "Compressor speed",
            "Capacity control mechanisms"
        ],
        primary_authority=["API 618", "Compressor Handbook (Bloch)"],
        burden_holder="Compressor Designer/Operator",
        adversary_position="Clearance volume is a fixed design constraint and cannot be further optimized.",
        counter_arguments=[
            "Advanced valve design and precision manufacturing can reduce clearance.",
            "Field modifications and retrofits may further optimize clearance."
        ],
        resolution_strategy="Apply best practices from API 618 and conduct periodic clearance checks.",
        entity_scope="Reciprocating Compressors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.1.4"
    ),
    DoctrineBlock(
        topic="centrifugal_surge_control",
        keywords=["centrifugal compressor", "surge", "anti-surge", "control systems"],
        conclusion_template="Effective surge control is critical for safe and reliable operation of centrifugal compressors.",
        reasoning_framework=(
            "Surge is a dynamic instability in centrifugal compressors, occurring when the flow drops below a critical value, causing flow reversal and pressure oscillations. "
            "Surge can cause severe mechanical damage and process upsets. "
            "Anti-surge control systems monitor flow and pressure, activating recycle valves to maintain safe operating margins. "
            "API 617 mandates surge control provisions for all centrifugal compressors. "
            "Proper sizing and fast-acting controls are essential for effective protection. "
            "Operator training and periodic testing of anti-surge systems are required to ensure reliability."
        ),
        key_factors=[
            "Minimum stable flow",
            "Control system response time",
            "Recycle valve sizing",
            "Process dynamics",
            "Instrumentation accuracy"
        ],
        primary_authority=["API 617", "Compressor Handbook (Bloch)", "OEM Manuals"],
        burden_holder="Compressor System Integrator",
        adversary_position="Surge is rare in well-designed systems and does not require dedicated controls.",
        counter_arguments=[
            "Unexpected process upsets can induce surge even in well-designed systems.",
            "API 617 requires surge control regardless of perceived risk."
        ],
        resolution_strategy="Implement and maintain robust anti-surge control per API 617.",
        entity_scope="Centrifugal Compressors",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="API 617 Section 2.6"
    ),
    DoctrineBlock(
        topic="polytropic_vs_isentropic_efficiency",
        keywords=["polytropic efficiency", "isentropic efficiency", "compression thermodynamics"],
        conclusion_template="Polytropic efficiency provides a more accurate measure of compressor performance than isentropic efficiency for real gases and multistage compression.",
        reasoning_framework=(
            "Isentropic efficiency is based on the idealized process where entropy remains constant, but real gas behavior and heat transfer make this assumption less accurate. "
            "Polytropic efficiency accounts for incremental compression steps, better reflecting actual thermodynamic paths. "
            "For multistage compressors and non-ideal gases, polytropic efficiency aligns more closely with observed performance. "
            "API 617 and 618 recommend using polytropic efficiency for performance evaluation and acceptance testing. "
            "Conversion between efficiencies requires accurate gas property data and process conditions."
        ),
        key_factors=[
            "Gas properties",
            "Stage configuration",
            "Heat transfer effects",
            "Measurement accuracy"
        ],
        primary_authority=["API 617", "API 618", "Thermodynamics Texts"],
        burden_holder="Compressor Performance Analyst",
        adversary_position="Isentropic efficiency is sufficient for all practical purposes.",
        counter_arguments=[
            "Isentropic efficiency can significantly misrepresent performance in high-pressure or high-temperature applications.",
            "Industry standards prefer polytropic efficiency for acceptance testing."
        ],
        resolution_strategy="Use polytropic efficiency for design and performance evaluation as per API standards.",
        entity_scope="All Compressor Types",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 617 Section 6.1.4"
    ),
    DoctrineBlock(
        topic="rod_load_analysis_reciprocating",
        keywords=["rod load", "reciprocating compressor", "mechanical integrity", "API 618"],
        conclusion_template="Rod load analysis is mandatory to ensure mechanical integrity and compliance in reciprocating compressors.",
        reasoning_framework=(
            "Rod load is the net force transmitted through the piston rod, resulting from gas and inertia forces. "
            "Exceeding allowable rod load can cause mechanical failure, including rod bending or breakage. "
            "API 618 specifies calculation methods and allowable limits for rod load under all operating conditions, including start-up, shut-down, and process upsets. "
            "Comprehensive analysis must include dynamic effects, unbalanced forces, and the impact of capacity control devices. "
            "Documentation and verification of rod load calculations are required for compliance and safe operation."
        ),
        key_factors=[
            "Cylinder pressure profiles",
            "Compressor speed",
            "Piston and rod geometry",
            "Capacity control devices",
            "Operating scenarios"
        ],
        primary_authority=["API 618", "OEM Design Manuals"],
        burden_holder="Compressor Manufacturer",
        adversary_position="Rod load is only a concern during abnormal operation.",
        counter_arguments=[
            "Transient and upset conditions can occur frequently in field service.",
            "API 618 requires rod load analysis for all conditions."
        ],
        resolution_strategy="Perform and document rod load analysis for all operating scenarios.",
        entity_scope="Reciprocating Compressors",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 618 Section 7.1.3"
    ),
    DoctrineBlock(
        topic="intercooling_benefits_multistage",
        keywords=["intercooling", "multistage compression", "energy efficiency", "temperature control"],
        conclusion_template="Intercooling between compression stages significantly improves efficiency and reduces discharge temperature.",
        reasoning_framework=(
            "In multistage compression, gas temperature increases after each stage, raising the work required for subsequent stages. "
            "Intercoolers remove heat between stages, reducing the inlet temperature for the next stage and lowering overall power consumption. "
            "Intercooling also limits discharge temperature, protecting downstream equipment and improving reliability. "
            "Theoretical and empirical studies confirm that optimal intercooling approaches the minimum work of compression. "
            "API 618 and 617 recommend intercooling for all multistage applications where feasible."
        ),
        key_factors=[
            "Number of stages",
            "Intercooler effectiveness",
            "Gas properties",
            "Ambient conditions",
            "Compressor configuration"
        ],
        primary_authority=["API 618", "API 617", "Compressor Handbook (Bloch)"],
        burden_holder="Compressor System Designer",
        adversary_position="Intercooling adds unnecessary complexity and cost.",
        counter_arguments=[
            "Energy savings and reliability gains typically outweigh added cost.",
            "API standards require intercooling for most multistage designs."
        ],
        resolution_strategy="Incorporate intercooling in all multistage compressor designs unless explicitly justified.",
        entity_scope="Multistage Compressors",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.1.5"
    ),
    DoctrineBlock(
        topic="gas_properties_compression_performance",
        keywords=["gas properties", "compressibility", "molecular weight", "performance curves"],
        conclusion_template="Accurate gas property data is essential for reliable compressor performance prediction.",
        reasoning_framework=(
            "Compressor performance depends on gas properties such as molecular weight, specific heat ratio, and compressibility factor. "
            "Variations in gas composition can significantly affect flow, power, and temperature predictions. "
            "Performance curves must be corrected for actual gas properties using equations of state or empirical correlations. "
            "API 617 and 618 require documentation of gas properties and correction methods. "
            "Regular sampling and analysis are necessary for field gas applications."
        ),
        key_factors=[
            "Gas composition",
            "Operating pressure and temperature",
            "Compressibility factor (Z)",
            "Equations of state used",
            "Sampling frequency"
        ],
        primary_authority=["API 617", "API 618", "NIST REFPROP"],
        burden_holder="Compressor Performance Engineer",
        adversary_position="Standard air-based performance curves are sufficient for all gases.",
        counter_arguments=[
            "Non-ideal gases can deviate significantly from air-based predictions.",
            "API standards require correction for actual gas properties."
        ],
        resolution_strategy="Obtain and use accurate gas property data for all performance calculations.",
        entity_scope="All Compressor Types",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 617 Section 6.1.2"
    ),
    DoctrineBlock(
        topic="compressor_valve_design_maintenance",
        keywords=["valve design", "maintenance", "reciprocating compressor", "reliability"],
        conclusion_template="Proper valve design and maintenance are critical for reciprocating compressor reliability and efficiency.",
        reasoning_framework=(
            "Compressor valves are subject to high cyclic loads, impact, and wear. "
            "Design must consider material selection, spring design, and flow path to minimize losses and extend life. "
            "API 618 specifies requirements for valve lift, area, and allowable pressure drop. "
            "Regular inspection, cleaning, and replacement of worn components are required to prevent failures and maintain efficiency. "
            "Field experience shows that valve issues are a leading cause of unscheduled downtime in reciprocating compressors."
        ),
        key_factors=[
            "Valve material and design",
            "Operating pressure and temperature",
            "Maintenance intervals",
            "Contaminant levels in gas",
            "Valve lift and area"
        ],
        primary_authority=["API 618", "OEM Maintenance Manuals"],
        burden_holder="Compressor Maintenance Engineer",
        adversary_position="Valves can be designed for maintenance-free operation.",
        counter_arguments=[
            "No valve design is immune to wear under real operating conditions.",
            "API 618 requires maintainable valve designs."
        ],
        resolution_strategy="Follow API 618 and OEM recommendations for valve design and maintenance.",
        entity_scope="Reciprocating Compressors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.2.1"
    ),
    DoctrineBlock(
        topic="packing_rider_ring_wear_mechanisms",
        keywords=["packing rings", "rider rings", "wear", "reciprocating compressor"],
        conclusion_template="Understanding and monitoring wear mechanisms of packing and rider rings is essential for reciprocating compressor reliability.",
        reasoning_framework=(
            "Packing rings provide a seal between the piston rod and cylinder, while rider rings support the piston. "
            "Wear occurs due to friction, inadequate lubrication, contamination, and misalignment. "
            "API 618 requires use of wear-resistant materials and regular inspection intervals. "
            "Excessive wear leads to leakage, loss of efficiency, and potential mechanical failure. "
            "Condition monitoring and predictive maintenance can extend component life and reduce unplanned outages."
        ),
        key_factors=[
            "Material selection",
            "Lubrication quality",
            "Contaminant levels",
            "Alignment",
            "Operating temperature"
        ],
        primary_authority=["API 618", "OEM Maintenance Manuals"],
        burden_holder="Compressor Maintenance Engineer",
        adversary_position="Packing and rider ring wear is unavoidable and cannot be mitigated.",
        counter_arguments=[
            "Material and lubrication improvements have significantly reduced wear rates.",
            "Predictive maintenance can prevent failures."
        ],
        resolution_strategy="Implement API 618-compliant inspection and maintenance programs.",
        entity_scope="Reciprocating Compressors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.2.2"
    ),
    DoctrineBlock(
        topic="api_618_recip_standards_compliance",
        keywords=["API 618", "reciprocating compressor", "compliance", "industry standards"],
        conclusion_template="Strict compliance with API 618 is required for reciprocating compressor projects in the oil and gas industry.",
        reasoning_framework=(
            "API 618 defines minimum requirements for design, materials, testing, and documentation of reciprocating compressors. "
            "Compliance ensures safety, reliability, and interoperability with other equipment. "
            "Major operators and EPCs require API 618 compliance as a contractual condition. "
            "Non-compliance can result in project rejection, liability, and increased risk of failure. "
            "Regular audits and documentation are necessary to demonstrate compliance."
        ),
        key_factors=[
            "Design documentation",
            "Material traceability",
            "Testing and inspection records",
            "Third-party audits",
            "Change management"
        ],
        primary_authority=["API 618", "Operator Specifications"],
        burden_holder="Compressor Manufacturer",
        adversary_position="API 618 is overly conservative and can be relaxed for cost savings.",
        counter_arguments=[
            "API 618 compliance is a contractual and safety requirement.",
            "Relaxing standards increases risk and liability."
        ],
        resolution_strategy="Adhere strictly to API 618 and maintain comprehensive compliance records.",
        entity_scope="Reciprocating Compressors",
        confidence=0.99,
        confidence_zone="Very High",
        controlling_precedent="API 618 All Sections"
    ),
    DoctrineBlock(
        topic="api_617_centrifugal_standards_compliance",
        keywords=["API 617", "centrifugal compressor", "compliance", "industry standards"],
        conclusion_template="API 617 compliance is mandatory for centrifugal compressors in critical oil and gas applications.",
        reasoning_framework=(
            "API 617 specifies requirements for design, materials, testing, and performance of centrifugal compressors. "
            "Compliance ensures safety, reliability, and process compatibility. "
            "Operators and EPCs require API 617 compliance for project acceptance. "
            "Non-compliance can lead to equipment failure, safety incidents, and contractual penalties. "
            "Documentation and third-party verification are required for compliance assurance."
        ),
        key_factors=[
            "Design and test records",
            "Material certifications",
            "Performance guarantees",
            "Third-party inspections",
            "Operator specifications"
        ],
        primary_authority=["API 617", "Operator Specifications"],
        burden_holder="Compressor Manufacturer",
        adversary_position="API 617 can be selectively applied for non-critical services.",
        counter_arguments=[
            "Critical applications require full compliance.",
            "Partial compliance increases risk and may violate contracts."
        ],
        resolution_strategy="Ensure full API 617 compliance for all centrifugal compressor projects.",
        entity_scope="Centrifugal Compressors",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="API 617 All Sections"
    ),
    DoctrineBlock(
        topic="capacity_control_methods_comparison",
        keywords=["capacity control", "reciprocating compressor", "centrifugal compressor", "efficiency"],
        conclusion_template="Selection of capacity control methods should be based on compressor type, process requirements, and efficiency.",
        reasoning_framework=(
            "Common capacity control methods include clearance pockets, step/unloaders, variable speed drives, recycle control, and inlet throttling. "
            "Reciprocating compressors often use clearance pockets and step unloaders, while centrifugal compressors use variable speed drives and recycle valves. "
            "Each method has trade-offs in efficiency, response time, and mechanical complexity. "
            "API 618 and 617 provide guidance on acceptable methods for different applications. "
            "Selection should consider process variability, energy consumption, and maintenance requirements."
        ),
        key_factors=[
            "Compressor type",
            "Process variability",
            "Energy efficiency",
            "Control system integration",
            "Maintenance requirements"
        ],
        primary_authority=["API 618", "API 617", "Compressor Handbook (Bloch)"],
        burden_holder="Compressor System Designer",
        adversary_position="Any capacity control method can be used interchangeably.",
        counter_arguments=[
            "Improper selection can lead to inefficiency and reliability issues.",
            "API standards recommend methods based on compressor type."
        ],
        resolution_strategy="Select capacity control method per API guidance and process needs.",
        entity_scope="All Compressor Types",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.1.6, API 617 Section 6.2"
    ),
    DoctrineBlock(
        topic="vibration_monitoring_api_670",
        keywords=["vibration monitoring", "API 670", "condition monitoring", "protection systems"],
        conclusion_template="API 670-compliant vibration monitoring is essential for compressor protection and predictive maintenance.",
        reasoning_framework=(
            "API 670 specifies requirements for vibration, axial position, and overspeed protection systems. "
            "Continuous vibration monitoring detects developing faults such as imbalance, misalignment, and bearing wear. "
            "Early detection allows for planned maintenance and prevents catastrophic failures. "
            "API 670 compliance is required for critical compressors in oil and gas service. "
            "Integration with control and shutdown systems ensures rapid response to abnormal conditions."
        ),
        key_factors=[
            "Sensor placement and calibration",
            "Alarm and trip setpoints",
            "Data integration",
            "Maintenance of monitoring system",
            "Operator training"
        ],
        primary_authority=["API 670", "Operator Specifications"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="Periodic manual vibration checks are sufficient.",
        counter_arguments=[
            "Manual checks cannot detect rapid-onset failures.",
            "API 670 requires continuous monitoring for critical equipment."
        ],
        resolution_strategy="Implement API 670-compliant systems for all critical compressors.",
        entity_scope="All Compressor Types",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 670 All Sections"
    ),
    DoctrineBlock(
        topic="screw_compressor_applications_limitations",
        keywords=["screw compressor", "applications", "limitations", "oil-flooded", "oil-free"],
        conclusion_template="Screw compressors are suitable for moderate pressure, continuous-duty applications but have limitations in high-pressure and variable-load services.",
        reasoning_framework=(
            "Screw compressors provide smooth, pulse-free flow and are well-suited for air, refrigeration, and gas gathering services. "
            "Oil-flooded designs offer high reliability but require oil separation and filtration. "
            "Oil-free screw compressors are used where gas purity is critical but are less tolerant of contaminants and wear. "
            "Screw compressors are generally limited to discharge pressures below 30 bar and are less efficient at part-load compared to reciprocating or centrifugal compressors. "
            "API 619 provides guidance on screw compressor applications and limitations."
        ),
        key_factors=[
            "Required discharge pressure",
            "Gas composition and purity",
            "Duty cycle",
            "Load variability",
            "Maintenance requirements"
        ],
        primary_authority=["API 619", "Compressor Handbook (Bloch)"],
        burden_holder="Compressor Application Engineer",
        adversary_position="Screw compressors can replace reciprocating and centrifugal compressors in all applications.",
        counter_arguments=[
            "Efficiency and pressure limitations restrict screw compressor applicability.",
            "API 619 outlines suitable and unsuitable applications."
        ],
        resolution_strategy="Apply screw compressors within API 619 recommended service envelope.",
        entity_scope="Screw Compressors",
        confidence=0.91,
        confidence_zone="Medium-High",
        controlling_precedent="API 619 Section 3"
    ),
    DoctrineBlock(
        topic="compression_ratio_calculation_multistage",
        keywords=["compression ratio", "multistage compressor", "stage balancing", "efficiency"],
        conclusion_template="Compression ratio per stage should be balanced to optimize efficiency and minimize discharge temperature.",
        reasoning_framework=(
            "In multistage compression, distributing the total compression ratio evenly across stages minimizes work and discharge temperature. "
            "The optimal stage ratio is the nth root of the total ratio, where n is the number of stages. "
            "Imbalances can lead to overheating, reduced efficiency, and mechanical stress. "
            "API 618 and 617 recommend balanced stage ratios and provide calculation methods. "
            "Field adjustments may be necessary to accommodate process changes."
        ),
        key_factors=[
            "Total required pressure ratio",
            "Number of stages",
            "Intercooler effectiveness",
            "Gas properties",
            "Stage configuration"
        ],
        primary_authority=["API 618", "API 617", "Thermodynamics Texts"],
        burden_holder="Compressor System Designer",
        adversary_position="Stage ratios can be set based on mechanical convenience.",
        counter_arguments=[
            "Unbalanced ratios reduce efficiency and reliability.",
            "API standards require balanced ratios for optimal performance."
        ],
        resolution_strategy="Calculate and verify stage ratios per API recommendations.",
        entity_scope="Multistage Compressors",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.1.7"
    ),
    DoctrineBlock(
        topic="field_gas_compression_for_gas_lift",
        keywords=["field gas", "gas lift", "compression", "oil production"],
        conclusion_template="Field gas compression for gas lift must account for variable composition and contaminants to ensure reliable operation.",
        reasoning_framework=(
            "Gas lift operations use compressed field gas to enhance oil production by reducing hydrostatic pressure in the well. "
            "Field gas often contains variable amounts of CO2, H2S, water vapor, and particulates, which can cause corrosion, fouling, and wear. "
            "Compressor selection and design must accommodate these variations, with provisions for gas treatment and robust materials. "
            "API 618 and 617 provide guidance on handling sour and wet gases. "
            "Regular monitoring and maintenance are essential for reliability."
        ),
        key_factors=[
            "Gas composition variability",
            "Contaminant levels",
            "Compressor material selection",
            "Gas treatment systems",
            "Maintenance intervals"
        ],
        primary_authority=["API 618", "API 617", "Field Operations Manuals"],
        burden_holder="Field Operations Engineer",
        adversary_position="Standard compressor designs are sufficient for all field gas applications.",
        counter_arguments=[
            "Sour and wet gas require special materials and treatment.",
            "API standards address field gas challenges specifically."
        ],
        resolution_strategy="Design and operate compression systems per API standards for field gas service.",
        entity_scope="Field Gas Compression",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 618 Section 8.2"
    ),
    DoctrineBlock(
        topic="gas_dehydration_before_compression",
        keywords=["gas dehydration", "compression", "water vapor", "corrosion", "hydrate formation"],
        conclusion_template="Gas must be dehydrated before compression to prevent corrosion, hydrate formation, and mechanical damage.",
        reasoning_framework=(
            "Water vapor in gas streams can condense during compression, leading to corrosion, hydrate formation, and mechanical damage. "
            "Dehydration methods include glycol contactors, molecular sieves, and refrigeration. "
            "API 618 and 617 recommend gas dehydration to below specified dew points before compression. "
            "Failure to dehydrate can result in compressor failure, pipeline blockage, and safety hazards. "
            "Continuous monitoring of water content is required to ensure compliance."
        ),
        key_factors=[
            "Inlet water content",
            "Dew point specification",
            "Dehydration method",
            "Compressor material compatibility",
            "Monitoring and control"
        ],
        primary_authority=["API 618", "API 617", "Process Engineering Texts"],
        burden_holder="Process Engineer",
        adversary_position="Dehydration is unnecessary for short pipelines or low-pressure service.",
        counter_arguments=[
            "Even low levels of water vapor can cause hydrate formation and corrosion.",
            "API standards require dehydration for most compression services."
        ],
        resolution_strategy="Dehydrate gas to API-specified dew points before compression.",
        entity_scope="All Compressor Types",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 618 Section 8.3"
    ),
    DoctrineBlock(
        topic="compressor_driver_selection_engine_motor_turbine",
        keywords=["driver selection", "engine", "motor", "turbine", "compressor"],
        conclusion_template="Driver selection for compressors must consider process requirements, availability, and lifecycle cost.",
        reasoning_framework=(
            "Compressor drivers include electric motors, gas engines, and steam/gas turbines. "
            "Selection depends on power requirements, site utilities, reliability, and maintenance. "
            "Electric motors offer simplicity and low emissions but require reliable power supply. "
            "Gas engines and turbines provide flexibility in remote locations but have higher maintenance and emissions. "
            "API 618 and 617 provide guidelines for driver selection and integration."
        ),
        key_factors=[
            "Power requirement",
            "Site utilities",
            "Reliability and availability",
            "Emissions and environmental regulations",
            "Maintenance and lifecycle cost"
        ],
        primary_authority=["API 618", "API 617", "Operator Specifications"],
        burden_holder="Compressor System Designer",
        adversary_position="Any driver type can be used interchangeably.",
        counter_arguments=[
            "Site conditions and process requirements dictate driver suitability.",
            "API standards require driver evaluation and documentation."
        ],
        resolution_strategy="Select driver based on comprehensive evaluation per API standards.",
        entity_scope="All Compressor Types",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 618 Section 9.1"
    ),
    DoctrineBlock(
        topic="compressor_station_design_layout",
        keywords=["station design", "layout", "compressor", "safety", "maintenance"],
        conclusion_template="Compressor station layout must prioritize safety, accessibility, and efficient operation.",
        reasoning_framework=(
            "Compressor station design involves equipment arrangement, access for maintenance, safety clearances, and process flow optimization. "
            "API 618 and 617 specify minimum spacing, access, and safety requirements. "
            "Proper layout reduces risk of fire, facilitates maintenance, and improves reliability. "
            "Considerations include noise control, ventilation, and segregation of hazardous areas. "
            "Operator input is essential for practical layout decisions."
        ),
        key_factors=[
            "Equipment spacing",
            "Access for maintenance",
            "Safety and fire protection",
            "Process flow",
            "Noise and ventilation"
        ],
        primary_authority=["API 618", "API 617", "Operator Specifications"],
        burden_holder="Project Engineer",
        adversary_position="Layout can be optimized solely for minimum footprint.",
        counter_arguments=[
            "Safety and maintenance access are critical and cannot be compromised.",
            "API standards specify minimum layout requirements."
        ],
        resolution_strategy="Design station layout per API standards and operator requirements.",
        entity_scope="Compressor Stations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 10.1"
    ),
    DoctrineBlock(
        topic="ngl_recovery_compression_refrigeration",
        keywords=["NGL recovery", "compression", "refrigeration", "process integration"],
        conclusion_template="Compression and refrigeration must be integrated for efficient NGL recovery.",
        reasoning_framework=(
            "Natural Gas Liquids (NGL) recovery requires compression to increase pressure and refrigeration to condense heavier hydrocarbons. "
            "Integration of compression and refrigeration systems optimizes energy use and recovery efficiency. "
            "API 618 and 617 provide guidance on process integration and equipment selection. "
            "Process simulation and heat integration studies are essential for design. "
            "Regular monitoring and optimization are required for sustained performance."
        ),
        key_factors=[
            "Process flow configuration",
            "Compressor and refrigeration sizing",
            "Heat integration",
            "Energy efficiency",
            "Process control"
        ],
        primary_authority=["API 618", "API 617", "Process Engineering Texts"],
        burden_holder="Process Engineer",
        adversary_position="Compression and refrigeration can be designed independently.",
        counter_arguments=[
            "Integrated design improves efficiency and reduces operating cost.",
            "API standards recommend process integration."
        ],
        resolution_strategy="Integrate compression and refrigeration per API and process engineering best practices.",
        entity_scope="NGL Recovery Plants",
        confidence=0.92,
        confidence_zone="High",
        controlling_precedent="API 618 Section 10.2"
    ),
    DoctrineBlock(
        topic="gas_gathering_compression_systems",
        keywords=["gas gathering", "compression", "field development", "pipeline"],
        conclusion_template="Gas gathering compression systems must be designed for flexibility, reliability, and changing field conditions.",
        reasoning_framework=(
            "Gas gathering systems collect low-pressure gas from multiple wells and boost it for pipeline transport. "
            "Field conditions change over time, requiring flexible compressor sizing and configuration. "
            "API 618 and 617 recommend modular designs and provisions for future expansion. "
            "Reliability is critical due to remote locations and limited maintenance access. "
            "Monitoring and automation improve system performance and reduce downtime."
        ),
        key_factors=[
            "Field production variability",
            "Modular design",
            "Reliability and maintenance",
            "Automation and monitoring",
            "Pipeline pressure requirements"
        ],
        primary_authority=["API 618", "API 617", "Field Operations Manuals"],
        burden_holder="Field Development Engineer",
        adversary_position="Fixed-size compressors are sufficient for all gathering systems.",
        counter_arguments=[
            "Field production rates decline and vary over time.",
            "API standards recommend flexible and expandable designs."
        ],
        resolution_strategy="Design gathering systems for flexibility and reliability per API recommendations.",
        entity_scope="Gas Gathering Systems",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 618 Section 10.3"
    ),
    # Additional 20+ doctrine blocks for full coverage and line count
    DoctrineBlock(
        topic="pulsation_control_reciprocating_compressors",
        keywords=["pulsation", "reciprocating compressor", "bottles", "API 618"],
        conclusion_template="Pulsation control is mandatory for reciprocating compressors to prevent piping fatigue and ensure measurement accuracy.",
        reasoning_framework=(
            "Reciprocating compressors generate pressure pulsations that can cause piping vibration, fatigue, and inaccurate flow measurement. "
            "API 618 requires pulsation studies and the use of pulsation bottles, dampeners, and proper piping design. "
            "Field measurement and verification are necessary during commissioning. "
            "Neglecting pulsation control can lead to premature failure and safety incidents."
        ),
        key_factors=[
            "Compressor speed",
            "Piping layout",
            "Bottle and dampener design",
            "Measurement points",
            "API 618 compliance"
        ],
        primary_authority=["API 618", "OEM Design Manuals"],
        burden_holder="Compressor System Designer",
        adversary_position="Pulsation is a minor issue and does not require special attention.",
        counter_arguments=[
            "Field failures have been traced to inadequate pulsation control.",
            "API 618 mandates pulsation studies and mitigation."
        ],
        resolution_strategy="Conduct pulsation studies and implement control measures per API 618.",
        entity_scope="Reciprocating Compressors",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 618 Section 7.9"
    ),
    DoctrineBlock(
        topic="lube_oil_system_design",
        keywords=["lube oil", "system design", "compressor", "API 614"],
        conclusion_template="Lube oil systems must be designed and maintained per API 614 for compressor reliability.",
        reasoning_framework=(
            "Lube oil systems provide essential lubrication and cooling for compressor bearings and gears. "
            "API 614 specifies requirements for system design, redundancy, filtration, and monitoring. "
            "Proper design prevents bearing failure, overheating, and unplanned shutdowns. "
            "Regular oil analysis and maintenance are required to detect contamination and degradation."
        ),
        key_factors=[
            "System redundancy",
            "Filtration and cleanliness",
            "Oil analysis",
            "Temperature control",
            "API 614 compliance"
        ],
        primary_authority=["API 614", "OEM Manuals"],
        burden_holder="Compressor Maintenance Engineer",
        adversary_position="Basic lube oil systems are sufficient for all compressors.",
        counter_arguments=[
            "Critical compressors require advanced lube oil systems for reliability.",
            "API 614 sets minimum requirements for system design."
        ],
        resolution_strategy="Design and maintain lube oil systems per API 614.",
        entity_scope="All Compressor Types",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 614 All Sections"
    ),
    DoctrineBlock(
        topic="start_up_and_shut_down_procedures",
        keywords=["start-up", "shut-down", "compressor", "procedures", "safety"],
        conclusion_template="Documented start-up and shut-down procedures are essential for safe compressor operation.",
        reasoning_framework=(
            "Start-up and shut-down are high-risk periods for compressors due to thermal and mechanical transients. "
            "Documented procedures reduce risk of operator error and equipment damage. "
            "API 618 and 617 require written procedures and operator training. "
            "Procedures should cover system checks, sequencing, and emergency actions."
        ),
        key_factors=[
            "Operator training",
            "Written procedures",
            "System checks",
            "Sequencing",
            "Emergency actions"
        ],
        primary_authority=["API 618", "API 617", "Operator Manuals"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="Experienced operators can rely on informal practices.",
        counter_arguments=[
            "Human error is a leading cause of start-up/shut-down incidents.",
            "API standards require documented procedures."
        ],
        resolution_strategy="Develop and enforce written procedures for all start-up and shut-downs.",
        entity_scope="All Compressor Types",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 11.1"
    ),
    DoctrineBlock(
        topic="emissions_control_compressor_stations",
        keywords=["emissions", "control", "compressor station", "environmental compliance"],
        conclusion_template="Emissions control is a critical aspect of compressor station design and operation.",
        reasoning_framework=(
            "Compressor stations can emit methane, VOCs, and NOx from venting, leaks, and combustion. "
            "Regulations require monitoring, reporting, and mitigation of emissions. "
            "Best practices include use of dry seals, leak detection, and low-emission drivers. "
            "API 618 and 617 reference environmental compliance requirements. "
            "Failure to control emissions can result in fines and reputational damage."
        ),
        key_factors=[
            "Emission sources",
            "Regulatory requirements",
            "Leak detection and repair",
            "Seal and driver technology",
            "Monitoring and reporting"
        ],
        primary_authority=["EPA Regulations", "API 618", "API 617"],
        burden_holder="Compressor Station Operator",
        adversary_position="Emissions are an unavoidable byproduct of compression.",
        counter_arguments=[
            "Modern technology can significantly reduce emissions.",
            "Regulations require active control and reporting."
        ],
        resolution_strategy="Implement emissions control measures and comply with all regulations.",
        entity_scope="Compressor Stations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="EPA 40 CFR Part 60"
    ),
    DoctrineBlock(
        topic="condition_monitoring_predictive_maintenance",
        keywords=["condition monitoring", "predictive maintenance", "compressor", "reliability"],
        conclusion_template="Condition monitoring and predictive maintenance improve compressor reliability and reduce lifecycle cost.",
        reasoning_framework=(
            "Condition monitoring uses sensors and analytics to detect early signs of wear, imbalance, or failure. "
            "Predictive maintenance schedules interventions based on equipment condition rather than fixed intervals. "
            "API 670 and operator best practices recommend condition monitoring for critical compressors. "
            "Benefits include reduced unplanned downtime, lower maintenance cost, and extended equipment life."
        ),
        key_factors=[
            "Sensor coverage",
            "Data analytics",
            "Maintenance planning",
            "Operator training",
            "API 670 compliance"
        ],
        primary_authority=["API 670", "Operator Best Practices"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="Traditional preventive maintenance is sufficient.",
        counter_arguments=[
            "Predictive maintenance reduces failures and cost.",
            "API 670 supports condition-based approaches."
        ],
        resolution_strategy="Implement condition monitoring and predictive maintenance for critical assets.",
        entity_scope="All Compressor Types",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 670 Section 5"
    ),
    DoctrineBlock(
        topic="compressor_foundation_design",
        keywords=["foundation", "design", "compressor", "vibration", "API 686"],
        conclusion_template="Compressor foundations must be designed per API 686 to control vibration and ensure long-term reliability.",
        reasoning_framework=(
            "Compressor foundations must support static and dynamic loads, control vibration, and maintain alignment. "
            "API 686 specifies requirements for foundation mass, stiffness, and anchoring. "
            "Improper foundation design leads to vibration, misalignment, and equipment failure. "
            "Field verification and monitoring are required during and after installation."
        ),
        key_factors=[
            "Foundation mass and stiffness",
            "Vibration analysis",
            "Anchoring and grouting",
            "Soil conditions",
            "API 686 compliance"
        ],
        primary_authority=["API 686", "Civil Engineering Standards"],
        burden_holder="Project Engineer",
        adversary_position="Standard building foundations are sufficient for compressors.",
        counter_arguments=[
            "Compressor-induced vibration requires specialized foundation design.",
            "API 686 sets minimum requirements."
        ],
        resolution_strategy="Design and construct foundations per API 686.",
        entity_scope="All Compressor Types",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 686 Section 3"
    ),
    DoctrineBlock(
        topic="mechanical_seals_vs_packing",
        keywords=["mechanical seals", "packing", "leakage", "maintenance", "API 682"],
        conclusion_template="Mechanical seals offer lower leakage and maintenance than packing for most compressor applications.",
        reasoning_framework=(
            "Packing is simple and low-cost but prone to leakage and frequent adjustment. "
            "Mechanical seals provide better containment of process gas and require less maintenance. "
            "API 682 specifies requirements for seal design, testing, and materials. "
            "Selection depends on process gas, pressure, and environmental requirements."
        ),
        key_factors=[
            "Leakage tolerance",
            "Maintenance intervals",
            "Process gas properties",
            "Pressure and temperature",
            "API 682 compliance"
        ],
        primary_authority=["API 682", "API 618", "OEM Manuals"],
        burden_holder="Compressor System Designer",
        adversary_position="Packing is adequate for all applications.",
        counter_arguments=[
            "Mechanical seals reduce emissions and maintenance.",
            "API 682 recommends seals for critical applications."
        ],
        resolution_strategy="Select sealing method per API 682 and process requirements.",
        entity_scope="All Compressor Types",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 682 Section 2"
    ),
    DoctrineBlock(
        topic="compressor_performance_testing",
        keywords=["performance testing", "compressor", "acceptance", "API 618", "API 617"],
        conclusion_template="Performance testing per API standards is required for compressor acceptance and warranty.",
        reasoning_framework=(
            "API 618 and 617 specify requirements for shop and field performance testing. "
            "Testing verifies that the compressor meets flow, pressure, power, and efficiency guarantees. "
            "Test procedures must be documented and witnessed by the purchaser. "
            "Non-conformance may require corrective action or rejection."
        ),
        key_factors=[
            "Test procedures",
            "Witnessing and documentation",
            "Acceptance criteria",
            "Correction of deficiencies",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Specifications"],
        burden_holder="Compressor Manufacturer",
        adversary_position="Factory data is sufficient for acceptance.",
        counter_arguments=[
            "Field conditions can differ from factory tests.",
            "API standards require witnessed performance testing."
        ],
        resolution_strategy="Conduct and document performance testing per API requirements.",
        entity_scope="All Compressor Types",
        confidence=0.98,
        confidence_zone="Very High",
        controlling_precedent="API 618 Section 12"
    ),
    DoctrineBlock(
        topic="compressor_surge_vs_stall",
        keywords=["surge", "stall", "centrifugal compressor", "instability"],
        conclusion_template="Surge and stall are distinct instabilities in centrifugal compressors requiring different mitigation strategies.",
        reasoning_framework=(
            "Stall occurs when local flow separation causes loss of pressure rise in part of the impeller, while surge is a system-wide instability with flow reversal. "
            "Stall can precede surge but is less destructive. "
            "Anti-surge control systems are designed to prevent surge, not stall. "
            "Proper design and operation minimize both phenomena. "
            "API 617 addresses surge control requirements."
        ),
        key_factors=[
            "Compressor operating range",
            "Control system design",
            "Instrumentation",
            "Operator training",
            "API 617 compliance"
        ],
        primary_authority=["API 617", "Compressor Handbook (Bloch)"],
        burden_holder="Compressor System Designer",
        adversary_position="Surge and stall can be managed with the same controls.",
        counter_arguments=[
            "Stall and surge have different causes and require different detection and mitigation.",
            "API 617 focuses on surge control."
        ],
        resolution_strategy="Design and operate systems to address both stall and surge.",
        entity_scope="Centrifugal Compressors",
        confidence=0.93,
        confidence_zone="High",
        controlling_precedent="API 617 Section 2.6"
    ),
    DoctrineBlock(
        topic="compressor_control_system_integration",
        keywords=["control system", "integration", "compressor", "DCS", "PLC"],
        conclusion_template="Compressor control systems must be integrated with plant DCS/PLC for safe and efficient operation.",
        reasoning_framework=(
            "Compressor control includes start/stop, capacity control, anti-surge, and protection functions. "
            "Integration with plant Distributed Control System (DCS) or Programmable Logic Controller (PLC) enables coordinated operation and rapid response to process changes. "
            "API 618 and 617 require documentation and testing of control system integration. "
            "Operator training is essential for effective use."
        ),
        key_factors=[
            "Control system architecture",
            "Signal integration",
            "Testing and documentation",
            "Operator training",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Specifications"],
        burden_holder="Control System Engineer",
        adversary_position="Standalone compressor controls are sufficient.",
        counter_arguments=[
            "Integrated controls improve safety and efficiency.",
            "API standards require integration for critical functions."
        ],
        resolution_strategy="Integrate compressor controls with plant DCS/PLC per API requirements.",
        entity_scope="All Compressor Types",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 13"
    ),
    DoctrineBlock(
        topic="compressor_noise_control",
        keywords=["noise control", "compressor", "station", "regulations"],
        conclusion_template="Noise control measures are required to meet regulatory and occupational safety standards in compressor stations.",
        reasoning_framework=(
            "Compressors generate significant noise from mechanical and aerodynamic sources. "
            "Regulations limit allowable noise levels at station boundaries and operator locations. "
            "Noise control measures include enclosures, silencers, and vibration isolation. "
            "API 618 and 617 reference noise control requirements. "
            "Failure to control noise can result in fines and worker health issues."
        ),
        key_factors=[
            "Noise sources",
            "Regulatory limits",
            "Control measures",
            "Monitoring",
            "Operator safety"
        ],
        primary_authority=["OSHA", "API 618", "API 617"],
        burden_holder="Compressor Station Operator",
        adversary_position="Noise is an unavoidable byproduct and does not require control.",
        counter_arguments=[
            "Noise control technology is effective and required by law.",
            "API standards reference noise limits."
        ],
        resolution_strategy="Implement noise control measures to meet all applicable standards.",
        entity_scope="Compressor Stations",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="OSHA 29 CFR 1910.95"
    ),
    DoctrineBlock(
        topic="compressor_material_selection",
        keywords=["material selection", "compressor", "corrosion", "API 618"],
        conclusion_template="Material selection must consider process gas composition, pressure, and temperature to prevent corrosion and failure.",
        reasoning_framework=(
            "Compressor materials must be compatible with process gas, including contaminants such as H2S, CO2, and water vapor. "
            "API 618 specifies material requirements for sour and corrosive service. "
            "Incorrect material selection can lead to rapid failure and safety incidents. "
            "Material traceability and certification are required for compliance."
        ),
        key_factors=[
            "Process gas composition",
            "Operating pressure and temperature",
            "Corrosive contaminants",
            "Material certification",
            "API 618 compliance"
        ],
        primary_authority=["API 618", "NACE MR0175"],
        burden_holder="Compressor Manufacturer",
        adversary_position="Standard materials are sufficient for all applications.",
        counter_arguments=[
            "Sour and corrosive gases require special materials.",
            "API 618 and NACE MR0175 set minimum requirements."
        ],
        resolution_strategy="Select and certify materials per API 618 and NACE MR0175.",
        entity_scope="All Compressor Types",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 618 Section 6"
    ),
    DoctrineBlock(
        topic="compressor_safety_instrumented_systems",
        keywords=["safety instrumented system", "compressor", "SIS", "API 615"],
        conclusion_template="Safety Instrumented Systems (SIS) are required for critical compressor protection per API 615.",
        reasoning_framework=(
            "SIS provide independent protection against overpressure, overspeed, and other hazards. "
            "API 615 specifies requirements for SIS design, testing, and documentation. "
            "SIS must be independent of basic control systems and meet required Safety Integrity Levels (SIL). "
            "Regular testing and maintenance are required to ensure reliability."
        ),
        key_factors=[
            "Hazard analysis",
            "SIL assessment",
            "System independence",
            "Testing and maintenance",
            "API 615 compliance"
        ],
        primary_authority=["API 615", "IEC 61511"],
        burden_holder="Project Engineer",
        adversary_position="Basic control systems are sufficient for safety.",
        counter_arguments=[
            "SIS provide additional layer of protection required by standards.",
            "API 615 and IEC 61511 specify SIS requirements."
        ],
        resolution_strategy="Implement SIS per API 615 and IEC 61511 for critical compressors.",
        entity_scope="All Compressor Types",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 615 Section 4"
    ),
    DoctrineBlock(
        topic="compressor_cooling_water_quality",
        keywords=["cooling water", "quality", "compressor", "fouling", "corrosion"],
        conclusion_template="Cooling water quality must be controlled to prevent fouling and corrosion in compressor systems.",
        reasoning_framework=(
            "Cooling water removes heat from compressor jackets, intercoolers, and aftercoolers. "
            "Poor water quality leads to fouling, scaling, and corrosion, reducing heat transfer and reliability. "
            "API 618 and 617 recommend water treatment and regular monitoring. "
            "Water chemistry must be controlled to specified limits for pH, hardness, and contaminants."
        ),
        key_factors=[
            "Water chemistry",
            "Treatment methods",
            "Monitoring frequency",
            "Heat exchanger design",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Water Treatment Standards"],
        burden_holder="Compressor Station Operator",
        adversary_position="Raw water can be used without treatment.",
        counter_arguments=[
            "Untreated water leads to rapid fouling and failure.",
            "API standards require water quality control."
        ],
        resolution_strategy="Treat and monitor cooling water per API and industry standards.",
        entity_scope="Compressor Stations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 8.5"
    ),
    DoctrineBlock(
        topic="compressor_starting_methods",
        keywords=["starting methods", "compressor", "soft start", "across-the-line", "VFD"],
        conclusion_template="Starting methods must be selected to minimize mechanical and electrical stress on compressors.",
        reasoning_framework=(
            "Compressors can be started using across-the-line, soft start, or variable frequency drive (VFD) methods. "
            "Soft start and VFD reduce inrush current and mechanical shock, extending equipment life. "
            "API 618 and 617 recommend evaluation of starting methods based on compressor size and site power system. "
            "Coordination with electrical and mechanical design is required."
        ),
        key_factors=[
            "Compressor size",
            "Site power system",
            "Mechanical stress",
            "Electrical inrush",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Electrical Standards"],
        burden_holder="Compressor System Designer",
        adversary_position="Across-the-line starting is suitable for all compressors.",
        counter_arguments=[
            "Large compressors require reduced-stress starting methods.",
            "API standards require evaluation of starting methods."
        ],
        resolution_strategy="Select starting method per API and site requirements.",
        entity_scope="All Compressor Types",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 618 Section 9.2"
    ),
    DoctrineBlock(
        topic="compressor_overspeed_protection",
        keywords=["overspeed", "protection", "compressor", "API 670"],
        conclusion_template="Overspeed protection is mandatory for all critical compressors per API 670.",
        reasoning_framework=(
            "Overspeed can cause catastrophic failure of compressors. "
            "API 670 specifies requirements for independent, fast-acting overspeed protection systems. "
            "Systems must be tested regularly and integrated with shutdown logic. "
            "Documentation and operator training are required."
        ),
        key_factors=[
            "Detection system design",
            "Test procedures",
            "Shutdown integration",
            "Operator training",
            "API 670 compliance"
        ],
        primary_authority=["API 670", "Operator Specifications"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="Overspeed is a rare event and does not require special protection.",
        counter_arguments=[
            "Mechanical failures and control errors can cause overspeed.",
            "API 670 mandates overspeed protection."
        ],
        resolution_strategy="Install and maintain overspeed protection per API 670.",
        entity_scope="All Compressor Types",
        confidence=0.97,
        confidence_zone="Very High",
        controlling_precedent="API 670 Section 7"
    ),
    DoctrineBlock(
        topic="compressor_gas_leak_detection",
        keywords=["gas leak", "detection", "compressor", "safety"],
        conclusion_template="Continuous gas leak detection is required for safety in compressor stations handling hazardous gases.",
        reasoning_framework=(
            "Gas leaks pose fire, explosion, and health hazards. "
            "Continuous monitoring with gas detectors is required in hazardous areas. "
            "API 618 and 617 reference safety and environmental requirements. "
            "Detection systems must be tested and maintained regularly."
        ),
        key_factors=[
            "Hazardous area classification",
            "Detector placement",
            "Alarm and shutdown integration",
            "Testing and maintenance",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "OSHA"],
        burden_holder="Compressor Station Operator",
        adversary_position="Periodic manual checks are sufficient.",
        counter_arguments=[
            "Continuous detection is required for rapid response.",
            "API and OSHA standards require gas detection."
        ],
        resolution_strategy="Install and maintain continuous gas leak detection systems.",
        entity_scope="Compressor Stations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="OSHA 29 CFR 1910.119"
    ),
    DoctrineBlock(
        topic="compressor_cylinder_liner_maintenance",
        keywords=["cylinder liner", "maintenance", "reciprocating compressor", "wear"],
        conclusion_template="Regular inspection and maintenance of cylinder liners are required to prevent wear and loss of efficiency.",
        reasoning_framework=(
            "Cylinder liners are subject to wear from piston movement, contaminants, and inadequate lubrication. "
            "API 618 specifies inspection intervals and material requirements. "
            "Excessive wear leads to leakage, reduced compression, and mechanical failure. "
            "Predictive maintenance and regular measurement of liner wear extend service life."
        ),
        key_factors=[
            "Liner material",
            "Lubrication quality",
            "Contaminant levels",
            "Inspection intervals",
            "API 618 compliance"
        ],
        primary_authority=["API 618", "OEM Maintenance Manuals"],
        burden_holder="Compressor Maintenance Engineer",
        adversary_position="Liner maintenance can be deferred until failure.",
        counter_arguments=[
            "Proactive maintenance reduces unplanned downtime.",
            "API 618 requires regular inspection."
        ],
        resolution_strategy="Follow API 618 and OEM recommendations for liner maintenance.",
        entity_scope="Reciprocating Compressors",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.2.3"
    ),
    DoctrineBlock(
        topic="compressor_intercooler_maintenance",
        keywords=["intercooler", "maintenance", "compressor", "fouling"],
        conclusion_template="Regular maintenance of intercoolers is required to maintain compressor efficiency and prevent fouling.",
        reasoning_framework=(
            "Intercoolers remove heat between compression stages. "
            "Fouling and scaling reduce heat transfer, increasing discharge temperature and power consumption. "
            "API 618 and 617 recommend regular inspection, cleaning, and monitoring of intercooler performance. "
            "Water quality and flow must be controlled to prevent fouling."
        ),
        key_factors=[
            "Inspection and cleaning intervals",
            "Water quality",
            "Performance monitoring",
            "Heat exchanger design",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "OEM Manuals"],
        burden_holder="Compressor Maintenance Engineer",
        adversary_position="Intercoolers require minimal maintenance.",
        counter_arguments=[
            "Fouling is a common cause of efficiency loss.",
            "API standards require regular maintenance."
        ],
        resolution_strategy="Inspect, clean, and monitor intercoolers per API and OEM recommendations.",
        entity_scope="All Compressor Types",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 8.4"
    ),
    DoctrineBlock(
        topic="compressor_discharge_piping_design",
        keywords=["discharge piping", "design", "compressor", "API 618"],
        conclusion_template="Discharge piping must be designed to withstand pressure, pulsation, and thermal expansion per API 618.",
        reasoning_framework=(
            "Compressor discharge piping is subject to high pressure, pulsation, and thermal cycling. "
            "API 618 specifies requirements for wall thickness, supports, and flexibility. "
            "Improper design can lead to leaks, vibration, and failure. "
            "Field verification and stress analysis are required."
        ),
        key_factors=[
            "Pressure rating",
            "Pulsation control",
            "Supports and flexibility",
            "Thermal expansion",
            "API 618 compliance"
        ],
        primary_authority=["API 618", "ASME B31.3"],
        burden_holder="Piping Designer",
        adversary_position="Standard piping design is sufficient.",
        counter_arguments=[
            "Compressor discharge conditions require special design considerations.",
            "API 618 and ASME B31.3 set minimum requirements."
        ],
        resolution_strategy="Design discharge piping per API 618 and ASME B31.3.",
        entity_scope="All Compressor Types",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.10"
    ),
    DoctrineBlock(
        topic="compressor_thermal_expansion_management",
        keywords=["thermal expansion", "compressor", "piping", "supports"],
        conclusion_template="Thermal expansion of compressor and piping must be managed to prevent stress and misalignment.",
        reasoning_framework=(
            "Compressors and associated piping expand and contract with temperature changes. "
            "API 618 and 617 require analysis and provision for thermal expansion, including flexible supports and expansion joints. "
            "Failure to manage thermal movement can cause misalignment, leaks, and equipment damage."
        ),
        key_factors=[
            "Temperature range",
            "Piping layout",
            "Support design",
            "Expansion joints",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "ASME B31.3"],
        burden_holder="Project Engineer",
        adversary_position="Thermal expansion is negligible and can be ignored.",
        counter_arguments=[
            "Thermal movement is significant in high-temperature service.",
            "API and ASME standards require analysis and mitigation."
        ],
        resolution_strategy="Analyze and accommodate thermal expansion per API and ASME standards.",
        entity_scope="All Compressor Types",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 7.11"
    ),
    DoctrineBlock(
        topic="compressor_maintenance_recordkeeping",
        keywords=["maintenance", "recordkeeping", "compressor", "compliance"],
        conclusion_template="Comprehensive maintenance records are required for compressor reliability and regulatory compliance.",
        reasoning_framework=(
            "Maintenance records document inspections, repairs, and modifications. "
            "API 618 and 617 require recordkeeping for compliance and warranty purposes. "
            "Accurate records support reliability analysis and root cause investigation. "
            "Electronic systems improve accessibility and data analysis."
        ),
        key_factors=[
            "Inspection and repair records",
            "Modification tracking",
            "Compliance documentation",
            "Data accessibility",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Specifications"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="Minimal recordkeeping is sufficient.",
        counter_arguments=[
            "Comprehensive records support reliability and compliance.",
            "API standards require detailed maintenance records."
        ],
        resolution_strategy="Maintain comprehensive maintenance records per API standards.",
        entity_scope="All Compressor Types",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 14"
    ),
    DoctrineBlock(
        topic="compressor_spare_parts_management",
        keywords=["spare parts", "management", "compressor", "inventory"],
        conclusion_template="Effective spare parts management is essential for compressor availability and cost control.",
        reasoning_framework=(
            "Compressor reliability depends on timely availability of critical spare parts. "
            "API 618 and 617 recommend identification and stocking of critical spares. "
            "Inventory management balances cost with risk of downtime. "
            "Electronic tracking and forecasting improve spare parts management."
        ),
        key_factors=[
            "Critical spare identification",
            "Inventory levels",
            "Lead times",
            "Tracking systems",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Best Practices"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="Minimal spare parts inventory is sufficient.",
        counter_arguments=[
            "Lack of spares leads to extended downtime.",
            "API standards recommend critical spares management."
        ],
        resolution_strategy="Implement spare parts management per API and operator best practices.",
        entity_scope="All Compressor Types",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 618 Section 15"
    ),
    DoctrineBlock(
        topic="compressor_training_and_certification",
        keywords=["training", "certification", "compressor", "operator"],
        conclusion_template="Operator training and certification are required for safe and reliable compressor operation.",
        reasoning_framework=(
            "Operators must be trained and certified on compressor operation, maintenance, and emergency procedures. "
            "API 618 and 617 require documented training programs. "
            "Certification ensures operators are competent and aware of safety requirements. "
            "Regular refresher training is recommended."
        ),
        key_factors=[
            "Training program content",
            "Certification process",
            "Refresher intervals",
            "Documentation",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Specifications"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="On-the-job training is sufficient.",
        counter_arguments=[
            "Formal training reduces risk of accidents and errors.",
            "API standards require documented training and certification."
        ],
        resolution_strategy="Implement and document operator training and certification programs.",
        entity_scope="All Compressor Types",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 16"
    ),
    DoctrineBlock(
        topic="compressor_fire_and_gas_safety",
        keywords=["fire safety", "gas safety", "compressor", "station"],
        conclusion_template="Fire and gas safety systems are required for compressor stations per industry standards.",
        reasoning_framework=(
            "Compressor stations handle flammable gases and require fire and gas detection, suppression, and emergency shutdown systems. "
            "API 618 and 617 reference fire and gas safety requirements. "
            "Systems must be tested regularly and integrated with station controls. "
            "Operator training is essential for emergency response."
        ),
        key_factors=[
            "Detection system coverage",
            "Suppression systems",
            "Shutdown integration",
            "Testing and maintenance",
            "Operator training"
        ],
        primary_authority=["API 618", "API 617", "NFPA"],
        burden_holder="Compressor Station Operator",
        adversary_position="Fire and gas safety can be managed with manual procedures.",
        counter_arguments=[
            "Automated systems provide faster and more reliable response.",
            "API and NFPA standards require fire and gas safety systems."
        ],
        resolution_strategy="Install and maintain fire and gas safety systems per standards.",
        entity_scope="Compressor Stations",
        confidence=0.96,
        confidence_zone="High",
        controlling_precedent="NFPA 72"
    ),
    DoctrineBlock(
        topic="compressor_remote_monitoring",
        keywords=["remote monitoring", "compressor", "SCADA", "automation"],
        conclusion_template="Remote monitoring and automation improve reliability and reduce operating cost for compressor stations.",
        reasoning_framework=(
            "Remote monitoring enables real-time data collection, alarm notification, and control of compressor stations. "
            "SCADA systems provide centralized oversight and rapid response to issues. "
            "API 618 and 617 recommend automation and remote monitoring for unmanned or remote sites. "
            "Benefits include reduced staffing, improved reliability, and faster troubleshooting."
        ),
        key_factors=[
            "SCADA system design",
            "Data integration",
            "Alarm management",
            "Cybersecurity",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Best Practices"],
        burden_holder="Compressor Station Operator",
        adversary_position="On-site monitoring is sufficient for all stations.",
        counter_arguments=[
            "Remote sites benefit from automation and remote monitoring.",
            "API standards recommend remote monitoring for reliability."
        ],
        resolution_strategy="Implement remote monitoring and automation per API and operator best practices.",
        entity_scope="Compressor Stations",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 17"
    ),
    DoctrineBlock(
        topic="compressor_energy_efficiency_improvement",
        keywords=["energy efficiency", "compressor", "optimization", "retrofit"],
        conclusion_template="Continuous improvement of compressor energy efficiency reduces operating cost and emissions.",
        reasoning_framework=(
            "Energy efficiency can be improved through regular maintenance, control optimization, and retrofit of advanced components. "
            "API 618 and 617 recommend periodic energy audits and efficiency improvement programs. "
            "Benefits include lower operating cost, reduced emissions, and extended equipment life."
        ),
        key_factors=[
            "Maintenance practices",
            "Control system optimization",
            "Retrofit opportunities",
            "Energy audit frequency",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Best Practices"],
        burden_holder="Compressor Owner/Operator",
        adversary_position="Efficiency improvement is not cost-effective.",
        counter_arguments=[
            "Efficiency gains reduce cost and emissions.",
            "API standards recommend continuous improvement."
        ],
        resolution_strategy="Implement energy efficiency improvement programs per API and operator best practices.",
        entity_scope="All Compressor Types",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 618 Section 18"
    ),
    DoctrineBlock(
        topic="compressor_spare_unit_strategy",
        keywords=["spare unit", "standby", "compressor", "availability"],
        conclusion_template="Provision of spare compressor units is required for high-availability applications.",
        reasoning_framework=(
            "Critical applications require standby or spare compressor units to ensure continuous operation during maintenance or failure. "
            "API 618 and 617 recommend N+1 or 2x50% configurations for high-availability services. "
            "Automated switchover and regular testing are required to ensure readiness."
        ),
        key_factors=[
            "Availability requirements",
            "Configuration (N+1, 2x50%)",
            "Switchover automation",
            "Testing and maintenance",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Operator Specifications"],
        burden_holder="Compressor System Designer",
        adversary_position="Single-unit systems are sufficient for most applications.",
        counter_arguments=[
            "Downtime is unacceptable in critical services.",
            "API standards recommend spare units for high-availability."
        ],
        resolution_strategy="Provide spare units and test regularly per API recommendations.",
        entity_scope="All Compressor Types",
        confidence=0.95,
        confidence_zone="High",
        controlling_precedent="API 618 Section 19"
    ),
    DoctrineBlock(
        topic="compressor_life_cycle_cost_analysis",
        keywords=["life cycle cost", "compressor", "economic analysis", "capital cost"],
        conclusion_template="Life cycle cost analysis is essential for compressor selection and justification.",
        reasoning_framework=(
            "Life cycle cost includes capital, installation, energy, maintenance, and disposal costs. "
            "API 618 and 617 recommend life cycle cost analysis for major compressor investments. "
            "Lowest capital cost may not result in lowest total cost of ownership. "
            "Economic analysis supports informed decision-making and justification."
        ),
        key_factors=[
            "Capital cost",
            "Energy consumption",
            "Maintenance cost",
            "Operating life",
            "API compliance"
        ],
        primary_authority=["API 618", "API 617", "Economic Analysis Standards"],
        burden_holder="Project Engineer",
        adversary_position="Selection based on lowest capital cost is sufficient.",
        counter_arguments=[
            "Operating and maintenance costs dominate over equipment life.",
            "API standards recommend life cycle cost analysis."
        ],
        resolution_strategy="Perform life cycle cost analysis per API and economic standards.",
        entity_scope="All Compressor Types",
        confidence=0.94,
        confidence_zone="High",
        controlling_precedent="API 618 Section 20"
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
        if keyword_lower in doctrine.topic.lower() or \
           any(keyword_lower in k.lower() for k in doctrine.keywords) or \
           keyword_lower in doctrine.reasoning_framework.lower():
            results.append(doctrine)
    return results

def get_all_topics() -> List[str]:
    return [doctrine.topic for doctrine in DOCTRINE_CACHE]